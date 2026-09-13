from __future__ import annotations

import math
import re
from datetime import datetime

from .common import DATA, FIXED_NOW, MAX_AGE_SECONDS, LabError, Principal, canonical_hash, parse_time, read_json
from .graph import GraphService


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*|[\u4e00-\u9fff]", text.lower()))


def token_score(query: str, document: dict) -> float:
    terms = tokens(document["title"] + " " + document["text"])
    return len(tokens(query) & terms) / math.sqrt(max(len(terms), 1))


def freshness_issues(context: dict, now: datetime) -> list[str]:
    issues = []
    if context["temperature_c"] is None:
        issues.append("缺少温度观测")
    if context["status"] != "Active":
        issues.append("设备当前状态不允许此教学动作")
    for field, label in [("as_of", "设备快照"), ("observed_at", "温度观测")]:
        if not context[field]:
            issues.append(f"缺少{label}时间")
            continue
        age = (now - parse_time(context[field])).total_seconds()
        if age < -5:
            issues.append(f"{label}时间超前，需核对时钟")
        elif age > MAX_AGE_SECONDS:
            issues.append(f"{label}超过 {MAX_AGE_SECONDS} 秒新鲜度门槛")
    return issues


class Retriever:
    def __init__(self, graph_service: GraphService | None = None, documents: list[dict] | None = None):
        self.graph_service = graph_service or GraphService()
        self.documents = documents if documents is not None else read_json(DATA / "documents.json")
        if len({d["id"] for d in self.documents}) != len(self.documents):
            raise LabError("DUPLICATE_DOCUMENT", "示例文档 ID 必须唯一。")

    def allowed_documents(self, principal: Principal, now: datetime) -> list[dict]:
        # Filter before scoring and before constructing model context.
        return [dict(d) for d in self.documents
                if d["tenant"] == principal.tenant and principal.regions.intersection(d["regions"])
                and parse_time(d["effective_from"]) <= now < parse_time(d["effective_until"])]

    def bundle(self, principal: Principal, asset_id: str, query: str, *, mode: str = "graph",
               top_k: int = 2, now: datetime = FIXED_NOW) -> dict:
        if mode not in {"graph", "lexical"} or not 1 <= top_k <= 5:
            raise LabError("INVALID_RETRIEVAL", "检索模式或候选数量无效。")
        context = self.graph_service.context(principal, asset_id)
        candidates = []
        for document in self.allowed_documents(principal, now):
            lexical = token_score(query, document)
            related = document["procedure_id"] == context["procedure_id"] and bool(context["procedure_id"])
            score = lexical + (100.0 if mode == "graph" and related else 0.0)
            if score > 0:
                candidates.append({**document, "score":round(score, 6), "via_relation":bool(mode == "graph" and related),
                                   "content_hash":canonical_hash(document)})
        documents = sorted(candidates, key=lambda d:(-d["score"], d["id"]))[:top_k]
        issues = freshness_issues(context, now)
        if not any(d["procedure_id"] == context["procedure_id"] for d in documents):
            issues.append("未取得有权使用且在有效期内的适用程序")
        return {"task_scope":"maintenance_recommendation", "context":context, "documents":documents,
                "missing_information":issues, "retrieval_mode":mode,
                "ranking_note":"token overlap baseline; graph mode additionally follows usesProcedure; no embedding model"}
