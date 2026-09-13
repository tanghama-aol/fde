from __future__ import annotations

import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate
from rdflib import Dataset, Graph, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import SH

from .common import DATA, EX, ROOT, LabError, Principal, entity, graph_id, iso_time, parse_time, require_identifier


def celsius(raw: str, unit: str) -> Decimal:
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise LabError("INVALID_NUMBER", "温度必须是有限数值。") from exc
    if not value.is_finite():
        raise LabError("INVALID_NUMBER", "温度必须是有限数值。")
    if unit == "F":
        value = (value - Decimal(32)) * Decimal(5) / Decimal(9)
    elif unit != "C":
        raise LabError("UNKNOWN_UNIT", f"未定义温标：{unit}")
    return value.quantize(Decimal("0.01"))


def ontology() -> Graph:
    return Graph().parse(DATA / "ontology.ttl", format="turtle")


def build_dataset(assets_path: Path | None = None, observations_path: Path | None = None) -> Dataset:
    dataset = Dataset(default_union=False)
    dataset.bind("ex", EX)
    schema = ontology()
    records = {}
    with (assets_path or DATA / "assets.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            key = (row["tenant_id"], row["asset_id"])
            if key in records:
                raise LabError("DUPLICATE_KEY", "源文件中出现重复的租户和设备主键。")
            if row["kind"] != "CentrifugalPump" or row["region"] not in {"NORTH", "SOUTH"} or row["status"] not in {"Active", "Retired"}:
                raise LabError("INVALID_ENUM", "源文件包含未映射的业务枚举。")
            version = int(row["version"])
            if version < 1:
                raise LabError("INVALID_VERSION", "对象版本必须为正整数。")
            asset = entity(key[0], "asset", key[1])
            records[key] = asset
            graph = dataset.graph(graph_id(row["tenant_id"]))
            for triple in schema:
                graph.add(triple)
            line = entity(row["tenant_id"], "line", row["line_id"])
            site = entity(row["tenant_id"], "site", row["site_id"])
            for triple in [
                (asset, RDF.type, EX[row["kind"]]), (asset, EX.assetId, Literal(row["asset_id"])),
                (asset, RDFS.label, Literal(row["label"], lang="zh")),
                (asset, EX.status, EX[row["status"]]), (asset, EX.version, Literal(version)),
                (asset, EX.asOf, Literal(iso_time(parse_time(row["as_of"])), datatype=XSD.dateTime)),
                (asset, EX.partOf, line), (line, EX.partOf, site),
                (line, RDF.type, EX.ProductionLine), (site, RDF.type, EX.Site),
                (asset, EX.usesProcedure, EX["PROC-PUMP-01"]),
            ]:
                graph.add(triple)
            for node in [asset, line, site]:
                graph.add((node, EX.tenantId, Literal(row["tenant_id"])))
                graph.add((node, EX.region, Literal(row["region"])))
    seen_observations = set()
    with (observations_path or DATA / "observations.csv").open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            key = (row["tenant_id"], row["observation_id"])
            if key in seen_observations:
                raise LabError("DUPLICATE_KEY", "观测主键重复。")
            seen_observations.add(key)
            asset = records.get((row["tenant_id"], row["asset_id"]))
            if asset is None:
                raise LabError("MISSING_ASSET", "观测无法关联同租户设备。")
            observation = entity(row["tenant_id"], "observation", row["observation_id"])
            graph = dataset.graph(graph_id(row["tenant_id"]))
            for triple in [
                (observation, RDF.type, EX.TemperatureObservation), (observation, EX.forAsset, asset),
                (asset, EX.hasObservation, observation),
                (observation, EX.value, Literal(celsius(row["value"], row["unit"]), datatype=XSD.decimal)),
                (observation, EX.unit, EX.DegreeCelsius),
                (observation, EX.observedAt, Literal(iso_time(parse_time(row["observed_at"])), datatype=XSD.dateTime)),
            ]:
                graph.add(triple)
    return dataset


def infer(graph: Graph) -> tuple[Graph, dict]:
    derived = Graph()
    for triple in graph:
        derived.add(triple)
    before = len(derived)
    DeductiveClosure(OWLRL_Semantics).expand(derived)
    return derived, {"asserted_triples": before, "closure_triples": len(derived), "added_triples": len(derived) - before,
                     "profile": "OWL RL rule materialization; not a complete OWL 2 DL reasoner"}


def validate_graph(graph: Graph) -> dict:
    shapes = Graph().parse(DATA / "shapes.ttl", format="turtle")
    conforms, results, _ = validate(graph, shacl_graph=shapes, ont_graph=ontology(), inference="rdfs", advanced=False)
    violations = []
    for result in results.subjects(RDF.type, SH.ValidationResult):
        violations.append({"focus": str(results.value(result, SH.focusNode)), "path": str(results.value(result, SH.resultPath)),
                           "component": str(results.value(result, SH.sourceConstraintComponent)),
                           "message": str(results.value(result, SH.resultMessage))})
    return {"conforms": bool(conforms), "violations": sorted(violations, key=lambda r:(r["focus"],r["path"],r["component"])),
            "inference": "rdfs", "shapes_version": "1.0.0"}


class GraphService:
    """Application-owned query boundary. A graph name alone is not authorization."""
    def __init__(self, dataset: Dataset | None = None):
        self.dataset = dataset if dataset is not None else build_dataset()

    def context(self, principal: Principal, asset_id: str) -> dict:
        require_identifier(asset_id)
        asset = entity(principal.tenant, "asset", asset_id)
        graph = self.dataset.graph(graph_id(principal.tenant))
        tenant = str(graph.value(asset, EX.tenantId) or "")
        region = str(graph.value(asset, EX.region) or "")
        if tenant != principal.tenant or region not in principal.regions:
            raise LabError("NOT_FOUND_OR_FORBIDDEN", "设备不存在或不在当前身份的访问范围内。")
        query = """
        PREFIX ex: <https://example.org/maintenance/>
        SELECT ?observation ?value ?unit ?at WHERE {
          ?asset ex:hasObservation ?observation .
          ?observation ex:value ?value ; ex:unit ?unit ; ex:observedAt ?at .
        } ORDER BY DESC(?at)
        """
        rows = list(graph.query(query, initBindings={"asset":asset}))
        version_value = graph.value(asset, EX.version)
        if version_value is None:
            raise LabError("MISSING_DATA", "缺少对象版本。")
        version = int(version_value)
        observation = rows[0] if rows else None
        if len(rows) > 1 and str(rows[0].at) == str(rows[1].at):
            raise LabError("CONFLICTING_DATA", "同一时点存在多条观测，须先明确选取规则。")
        if observation and observation.unit != EX.DegreeCelsius:
            raise LabError("UNKNOWN_UNIT", "应用仅接受已标准化的摄氏度。")
        procedure = graph.value(asset, EX.usesProcedure)
        context = {"tenant":principal.tenant, "region":region, "asset_id":asset_id,
                   "label":str(graph.value(asset, RDFS.label)), "version":version,
                   "status":str(graph.value(asset, EX.status)).removeprefix(str(EX)),
                   "as_of":str(graph.value(asset, EX.asOf)),
                   "procedure_id":str(procedure).removeprefix(str(EX)) if procedure else None,
                   "temperature_c":float(observation.value) if observation else None,
                   "observed_at":str(observation.at) if observation else None,
                   "evidence_id":None}
        if observation:
            observation_id = str(observation.observation).rsplit("/",1)[-1]
            context["evidence_id"] = f"KG:{principal.tenant}:{asset_id}:v{version}:{observation_id}"
        # Only follow a fixed predicate, with a depth budget and scope checks at each hop.
        ancestry, frontier, visited = [], [asset], {asset}
        for _ in range(3):
            next_frontier = []
            for node in frontier:
                for parent in graph.objects(node, EX.partOf):
                    if parent in visited:
                        continue
                    visited.add(parent)
                    if str(graph.value(parent, EX.tenantId)) == principal.tenant and str(graph.value(parent, EX.region)) in principal.regions:
                        ancestry.append(str(parent))
                        next_frontier.append(parent)
            frontier = next_frontier
        context["ancestry"] = sorted(ancestry)
        return context


def migrate_legacy(graph: Graph) -> dict:
    before = len(list(graph.triples((None, EX.legacyAsset, None))))
    graph.update((ROOT / "queries/migrate-v1-v2.ru").read_text(encoding="utf-8"))
    graph.remove((EX.Ontology, OWL.versionInfo, None))
    graph.add((EX.Ontology, OWL.versionInfo, Literal("1.0.0")))
    graph.add((EX.legacyAsset, OWL.deprecated, Literal(True)))
    return {"moved_edges":before, "remaining_legacy_edges":len(list(graph.triples((None, EX.legacyAsset, None)))),
            "ontology_version":"1.0.0"}
