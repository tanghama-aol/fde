from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import uuid
from pathlib import Path

from rdflib import Graph, RDF

from .actions import ActionService
from .common import DATA, ROOT, EX, FIXED_NOW, NORTH_PLANNER, LabError, entity, graph_id, read_json, write_json
from .evaluation import evaluate
from .generation import deterministic_recommendation, ollama_recommendation, validate_recommendation
from .graph import GraphService, build_dataset, infer, migrate_legacy, validate_graph
from .retrieval import Retriever


def rdf_demo() -> dict:
    dataset = build_dataset()
    graph = dataset.graph(graph_id("TENANT-A"))
    query = (ROOT / "queries/assets.rq").read_text(encoding="utf-8")
    rows = [{str(k):str(v) for k,v in row.asdict().items()} for row in graph.query(query)]
    return {"scope":"administrative synthetic-data lesson; not the end-user API", "assets":rows,
            "named_graphs":sorted(str(g.identifier) for g in dataset.graphs() if g.identifier != dataset.default_context.identifier),
            "default_union":False}


def reasoning_demo() -> dict:
    graph = build_dataset().graph(graph_id("TENANT-A"))
    asset = entity("TENANT-A","asset","P-101")
    line = entity("TENANT-A","line","LINE-N")
    site = entity("TENANT-A","site","SITE-N")
    derived, stats = infer(graph)
    return {**stats, "asserted_asset_type":(asset,RDF.type,EX.Asset) in graph,
            "inferred_asset_type":(asset,RDF.type,EX.Asset) in derived,
            "inferred_inverse":(line,EX.hasPart,asset) in derived,
            "inferred_transitive_part":(asset,EX.partOf,site) in derived}


def validation_demo() -> dict:
    valid = validate_graph(build_dataset().graph(graph_id("TENANT-A")))
    invalid = validate_graph(Graph().parse(DATA / "invalid.ttl",format="turtle"))
    return {"valid_fixture":valid,"deliberately_invalid_fixture":invalid,
            "expected_behavior":valid["conforms"] and not invalid["conforms"]}


def ingestion_demo(directory: Path) -> dict:
    directory.mkdir(parents=True,exist_ok=True)
    dataset = build_dataset()
    dataset.serialize(destination=directory / "dataset.trig",format="trig")
    result = {"sources":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [DATA/"assets.csv",DATA/"observations.csv"]},
              "output":"dataset.trig", "source_hash_meaning":"raw file identity, not RDF semantic canonicalization",
              "normalization":"Fahrenheit to Celsius; timestamps require timezone; duplicate business keys are rejected",
              "p102_temperature_c":GraphService(dataset).context(NORTH_PLANNER,"P-102")["temperature_c"]}
    write_json(directory / "ingestion-manifest.json",result)
    return result


def action_demo(directory: Path, *, timeout: bool = True, reconcile: bool = True) -> dict:
    if (directory / "actions.sqlite").exists():
        raise LabError("RUN_EXISTS", "此演示目录已有执行状态，请使用新目录；程序不会清空旧记录。")
    retriever = Retriever()
    bundle = retriever.bundle(NORTH_PLANNER,"P-101","P-101")
    recommendation = deterministic_recommendation(bundle)
    service = ActionService(directory,retriever)
    proposal = service.create_proposal(NORTH_PLANNER,recommendation)
    approval = service.approve(NORTH_PLANNER,proposal["proposal_id"])
    first = service.execute(NORTH_PLANNER,proposal["proposal_id"],approval,"demo-request",timeout_after_commit=timeout)
    retry = service.execute(NORTH_PLANNER,proposal["proposal_id"],approval,"demo-request")
    final = service.reconcile(NORTH_PLANNER,first["operation_id"]) if reconcile else retry
    return {"business_system":"local durable simulator; no real equipment or work-order service connected",
            "approval_source":"trusted synthetic planner profile, not a model claim", "proposal":proposal,
            "first_attempt":first,"same_key_retry":retry,"final":final,"total_external_drafts":service.external.count()}


def migration_demo(directory: Path) -> dict:
    directory.mkdir(parents=True,exist_ok=True)
    graph = Graph().parse(DATA/"migration-v1.ttl",format="turtle")
    first = migrate_legacy(graph)
    second = migrate_legacy(graph)
    graph.serialize(destination=directory/"migrated.ttl",format="turtle")
    return {"first_run":first,"repeat_run":second,"output":"migrated.ttl"}


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="本体在 AI 中的应用：合成数据实战教程")
    subparsers = cli.add_subparsers(dest="command",required=True)
    for name in ["doctor","rdf","reason","validate","ingest","retrieve","generate","actions","reconcile","evaluate","migrate","demo"]:
        sub = subparsers.add_parser(name)
        sub.add_argument("--output",type=Path,help="另存 JSON 报告")
        if name in {"ingest","actions","reconcile","migrate","demo"}:
            sub.add_argument("--workdir",type=Path,default=None,help="本地结果目录；演示创建新目录，不覆盖已有执行状态")
        if name in {"retrieve","generate"}:
            sub.add_argument("--asset",default="P-101")
            sub.add_argument("--query",default="P-101")
        if name == "retrieve":
            sub.add_argument("--mode",choices=["lexical","graph"],default="graph")
            sub.add_argument("--top-k",type=int,default=2)
        if name == "generate":
            sub.add_argument("--mode",choices=["baseline","fixture","live"],default="baseline")
            sub.add_argument("--model",default="")
            sub.add_argument("--base-url",default="http://127.0.0.1:11434")
            sub.add_argument("--allow-remote",action="store_true")
            sub.add_argument("--timeout",type=float,default=120)
        if name == "actions":
            sub.add_argument("--scenario",choices=["normal","timeout"],default="timeout")
            sub.add_argument("--no-reconcile",action="store_true")
        if name == "reconcile":
            sub.add_argument("--operation",required=True)
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    directory = getattr(args,"workdir",None) or ROOT/".runs"/(args.command+"-"+uuid.uuid4().hex[:8])
    try:
        if args.command == "doctor":
            result = {"python":platform.python_version(),"dependencies":{n:importlib.metadata.version(n) for n in ["rdflib","owlrl","pyshacl","jsonschema"]},
                      "data_present":all((DATA/n).exists() for n in ["ontology.ttl","assets.csv","observations.csv","shapes.ttl","documents.json"]),
                      "network_needed_for_core_lessons":False,"business_clock":FIXED_NOW.isoformat()}
        elif args.command == "rdf": result = rdf_demo()
        elif args.command == "reason": result = reasoning_demo()
        elif args.command == "validate": result = validation_demo()
        elif args.command == "ingest": result = ingestion_demo(directory)
        elif args.command == "retrieve": result = Retriever().bundle(NORTH_PLANNER,args.asset,args.query,mode=args.mode,top_k=args.top_k)
        elif args.command == "generate":
            bundle = Retriever().bundle(NORTH_PLANNER,args.asset,args.query)
            if args.mode == "live":
                recommendation, run = ollama_recommendation(bundle,args.model,base_url=args.base_url,timeout=args.timeout,allow_remote=args.allow_remote)
            elif args.mode == "fixture":
                recommendation = validate_recommendation(read_json(DATA/"recommendation.fixture.json"),bundle)
                run = {"mode":"handwritten_reference_fixture","live_llm_calls":0}
            else:
                recommendation = deterministic_recommendation(bundle)
                run = {"mode":"deterministic_rule_template_baseline","live_llm_calls":0}
            result = {"recommendation":recommendation,"run":run,
                      "validation_scope":"schema and selected critical fields; free-text claims still require separate review"}
        elif args.command == "actions": result = action_demo(directory,timeout=args.scenario=="timeout",reconcile=not args.no_reconcile)
        elif args.command == "reconcile":
            if args.workdir is None or not (directory/"actions.sqlite").is_file():
                raise LabError("RUN_MISSING", "对账必须指定已有演示目录。")
            result = ActionService(directory).reconcile(NORTH_PLANNER,args.operation)
        elif args.command == "evaluate": result = evaluate()
        elif args.command == "migrate": result = migration_demo(directory)
        elif args.command == "demo":
            if directory.exists() and any(directory.iterdir()):
                raise LabError("RUN_EXISTS", "完整案例需要新的结果目录，以便保留原运行证据。")
            directory.mkdir(parents=True,exist_ok=True)
            result = {"ingestion":ingestion_demo(directory/"ingestion"),"reasoning":reasoning_demo(),"validation":validation_demo(),
                      "retrieval":Retriever().bundle(NORTH_PLANNER,"P-101","P-101"),
                      "actions":action_demo(directory/"actions"),"evaluation":evaluate(),"migration":migration_demo(directory/"migration")}
            write_json(directory/"demo-report.json",result)
        if args.output:
            write_json(args.output,result)
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
        return 0
    except LabError as exc:
        print(json.dumps({"error":exc.code,"message":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
