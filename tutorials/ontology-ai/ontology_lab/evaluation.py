from __future__ import annotations

import hashlib
import importlib.metadata
import platform
from datetime import datetime, timedelta, timezone

from .common import DATA, ROOT, FIXED_NOW, NORTH_PLANNER, OTHER_PLANNER, LabError, iso_time, read_json
from .generation import deterministic_recommendation
from .retrieval import Retriever


def implementation_hash() -> str:
    digest = hashlib.sha256()
    for path in sorted((ROOT / "ontology_lab").glob("*.py")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def evaluate() -> dict:
    retriever = Retriever()
    principals = {"north":NORTH_PLANNER, "other":OTHER_PLANNER}
    rows = []
    totals = {mode:{"hits":0,"cases":0} for mode in ["lexical","graph"]}
    guard_cases = []
    for case in read_json(DATA / "evaluation-cases.json"):
        principal = principals[case["principal"]]
        if case["kind"] == "retrieval":
            result = {"id":case["id"], "expected_document":case["expected_document"]}
            for mode in totals:
                bundle = retriever.bundle(principal,case["asset_id"],case["query"],mode=mode,top_k=1)
                selected = [d["id"] for d in bundle["documents"]]
                hit = case["expected_document"] in selected
                totals[mode]["hits"] += int(hit)
                totals[mode]["cases"] += 1
                result[mode] = {"retrieved":selected,"hit_at_1":hit}
            rows.append(result)
        elif case["kind"] == "authorization":
            try:
                retriever.bundle(principal,case["asset_id"],case["query"])
                observed = None
            except LabError as exc:
                observed = exc.code
            guard_cases.append({"id":case["id"],"observed_error":observed,"passed":observed==case["expected_error"]})
        elif case["kind"] == "freshness":
            bundle = retriever.bundle(principal,case["asset_id"],case["query"],now=FIXED_NOW+timedelta(seconds=case["clock_offset_seconds"]))
            decision = deterministic_recommendation(bundle)["decision"]
            guard_cases.append({"id":case["id"],"observed_decision":decision,"passed":decision==case["expected_decision"]})
    for metrics in totals.values():
        metrics["hit_at_1"] = metrics["hits"] / metrics["cases"] if metrics["cases"] else None
    return {"experiment":"synthetic retrieval and deterministic guard demonstration", "schema_version":"1.0",
            "executed_at":iso_time(datetime.now(timezone.utc)), "business_clock":iso_time(FIXED_NOW),
            "python":platform.python_version(), "platform":platform.system(),
            "dependencies":{name:importlib.metadata.version(name) for name in ["rdflib","owlrl","pyshacl","jsonschema"]},
            "implementation_sha256":implementation_hash(), "retrieval_metrics":totals,"retrieval_cases":rows,
            "guard_cases":guard_cases, "live_llm_calls":0, "production_system_calls":0,
            "limits":["Four manually designed retrieval cases are a mechanism demonstration, not an independent benchmark.",
                      "The baseline uses token overlap, not vector embeddings or a tuned search engine.",
                      "Both methods receive an explicit asset identifier; no natural-language entity linker is evaluated.",
                      "No LLM factual accuracy, production latency or incident rate is measured."]}
