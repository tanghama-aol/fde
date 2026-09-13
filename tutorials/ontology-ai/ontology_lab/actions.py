from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

from .common import EX, FIXED_NOW, LabError, Principal, canonical_hash, iso_time, parse_time
from .generation import validate_recommendation
from .retrieval import Retriever


@contextmanager
def database(path: Path):
    connection = sqlite3.connect(path, timeout=10, isolation_level=None)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        if connection.in_transaction:
            connection.rollback()
        connection.close()


class WorkOrderSimulator:
    """Separate durable store, standing in for an external business system."""
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with database(path) as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS assets (
              tenant TEXT NOT NULL, asset_id TEXT NOT NULL, region TEXT NOT NULL,
              version INTEGER NOT NULL, status TEXT NOT NULL, PRIMARY KEY (tenant,asset_id));
            CREATE TABLE IF NOT EXISTS drafts (
              id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT NOT NULL UNIQUE,
              tenant TEXT NOT NULL, asset_id TEXT NOT NULL, payload_hash TEXT NOT NULL, payload_json TEXT NOT NULL);
            """)

    def seed_asset(self, context: dict) -> None:
        with database(self.path) as db:
            db.execute("INSERT OR IGNORE INTO assets VALUES (?,?,?,?,?)",
                       (context["tenant"], context["asset_id"], context["region"], context["version"], context["status"]))

    def change_asset(self, tenant: str, asset_id: str, *, version: int, status: str = "Active") -> None:
        with database(self.path) as db:
            db.execute("UPDATE assets SET version=?,status=? WHERE tenant=? AND asset_id=?", (version,status,tenant,asset_id))

    @staticmethod
    def receipt(row) -> dict:
        return {"request_id":row["request_id"], "receipt_id":f"WO-DRAFT-{row['id']:05d}",
                "status":"DRAFT", "tenant":row["tenant"], "asset_id":row["asset_id"], "payload_hash":row["payload_hash"]}

    def create(self, request_id: str, snapshot: dict, payload_hash: str, *, timeout_after_commit: bool = False) -> dict:
        with database(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT * FROM drafts WHERE request_id=?", (request_id,)).fetchone()
            if existing:
                if existing["payload_hash"] != payload_hash:
                    raise LabError("EXTERNAL_IDEMPOTENCY_CONFLICT", "外部请求标识对应不同载荷。")
                db.commit()
                return self.receipt(existing)
            asset = db.execute("SELECT * FROM assets WHERE tenant=? AND asset_id=?", (snapshot["tenant"],snapshot["asset_id"])).fetchone()
            if asset is None or asset["region"] != snapshot["region"]:
                raise LabError("EXTERNAL_ASSET", "外部系统未找到匹配设备。")
            if asset["status"] != "Active":
                raise LabError("INVALID_STATE", "外部系统中的设备已不可执行此动作。")
            if asset["version"] != snapshot["asset_version"]:
                raise LabError("STALE_PRECONDITION", "外部系统拒绝过期设备版本。")
            db.execute("INSERT INTO drafts(request_id,tenant,asset_id,payload_hash,payload_json) VALUES (?,?,?,?,?)",
                       (request_id,snapshot["tenant"],snapshot["asset_id"],payload_hash,json.dumps(snapshot,sort_keys=True)))
            row = db.execute("SELECT * FROM drafts WHERE request_id=?", (request_id,)).fetchone()
            db.commit()
        if timeout_after_commit:
            raise TimeoutError("Synthetic fault: committed externally, response lost")
        return self.receipt(row)

    def lookup(self, request_id: str) -> dict | None:
        with database(self.path) as db:
            row = db.execute("SELECT * FROM drafts WHERE request_id=?", (request_id,)).fetchone()
        return self.receipt(row) if row else None

    def count(self) -> int:
        with database(self.path) as db:
            return db.execute("SELECT COUNT(*) FROM drafts").fetchone()[0]


class ActionService:
    def __init__(self, directory: Path, retriever: Retriever | None = None):
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / "actions.sqlite"
        self.external = WorkOrderSimulator(directory / "work-orders.sqlite")
        self.retriever = retriever or Retriever()
        self.policy_version = "maintenance-demo-1"
        with database(self.path) as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS proposals (
              id TEXT PRIMARY KEY, tenant TEXT NOT NULL, region TEXT NOT NULL,
              snapshot_json TEXT NOT NULL, payload_hash TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS approvals (
              id TEXT PRIMARY KEY, proposal_id TEXT NOT NULL, payload_hash TEXT NOT NULL,
              approver TEXT NOT NULL, approved_at TEXT NOT NULL, expires_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS operations (
              id TEXT PRIMARY KEY, proposal_id TEXT NOT NULL UNIQUE, tenant TEXT NOT NULL,
              payload_hash TEXT NOT NULL, state TEXT NOT NULL, receipt_json TEXT, error TEXT);
            CREATE TABLE IF NOT EXISTS request_keys (
              tenant TEXT NOT NULL, idempotency_key TEXT NOT NULL, operation_id TEXT NOT NULL,
              PRIMARY KEY(tenant,idempotency_key));
            CREATE TABLE IF NOT EXISTS audit (
              id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT NOT NULL,
              event TEXT NOT NULL, reference_id TEXT NOT NULL, at TEXT NOT NULL);
            """)
        # Initialize synthetic source records once; proposing an action never writes a draft.
        for graph in self.retriever.graph_service.dataset.graphs():
            for asset in graph.subjects(EX.assetId):
                self.external.seed_asset({"tenant":str(graph.value(asset,EX.tenantId)),
                                          "region":str(graph.value(asset,EX.region)),
                                          "asset_id":str(graph.value(asset,EX.assetId)),
                                          "version":int(graph.value(asset,EX.version)),
                                          "status":str(graph.value(asset,EX.status)).removeprefix(str(EX))})

    @staticmethod
    def require_planner(principal: Principal) -> None:
        if "planner" not in principal.roles:
            raise LabError("FORBIDDEN", "当前可信身份没有计划员权限。")

    def proposal(self, principal: Principal, proposal_id: str) -> dict:
        with database(self.path) as db:
            row = db.execute("SELECT * FROM proposals WHERE id=?", (proposal_id,)).fetchone()
        if row is None or row["tenant"] != principal.tenant or row["region"] not in principal.regions:
            raise LabError("NOT_FOUND_OR_FORBIDDEN", "提案不存在或不在访问范围内。")
        return dict(row)

    @staticmethod
    def result(row) -> dict:
        return {"operation_id":row["id"], "state":row["state"],
                "receipt":json.loads(row["receipt_json"]) if row["receipt_json"] else None,
                "error":row["error"], "completion_meaning":"只确认维修工单草稿，不表示正式派工、设备启停或修复"}

    def create_proposal(self, principal: Principal, recommendation: dict, *, now: datetime = FIXED_NOW) -> dict:
        bundle = self.retriever.bundle(principal,recommendation["asset_id"],"",now=now)
        validate_recommendation(recommendation,bundle)
        if recommendation["decision"] != "propose":
            raise LabError("NO_ACTION", "此建议不包含可批准的草稿动作。")
        context = bundle["context"]
        snapshot = {"tenant":context["tenant"], "region":context["region"], "asset_id":context["asset_id"],
                    "asset_version":context["version"], "temperature_c":context["temperature_c"],
                    "observed_at":context["observed_at"], "as_of":context["as_of"],
                    "procedure_id":context["procedure_id"], "evidence_ids":sorted(recommendation["evidence_ids"]),
                    "document_hashes":{d["id"]:d["content_hash"] for d in bundle["documents"] if d["id"] in recommendation["evidence_ids"]},
                    "action":"createMaintenanceDraft", "ontology_version":"1.0.0", "policy_version":self.policy_version}
        proposal_id = "PROP-" + uuid.uuid4().hex
        payload_hash = canonical_hash(snapshot)
        with database(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO proposals VALUES (?,?,?,?,?)", (proposal_id,principal.tenant,context["region"],json.dumps(snapshot,sort_keys=True),payload_hash))
            db.execute("INSERT INTO audit(subject,event,reference_id,at) VALUES (?,?,?,?)", (principal.subject,"proposal_created",proposal_id,iso_time(now)))
            db.commit()
        return {"proposal_id":proposal_id, "payload_hash":payload_hash, "snapshot":snapshot, "state":"awaiting_approval"}

    def approve(self, principal: Principal, proposal_id: str, *, now: datetime = FIXED_NOW) -> str:
        self.require_planner(principal)
        proposal = self.proposal(principal,proposal_id)
        approval_id = "APPR-" + uuid.uuid4().hex
        with database(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT INTO approvals VALUES (?,?,?,?,?,?)", (approval_id,proposal_id,proposal["payload_hash"],principal.subject,iso_time(now),iso_time(now+timedelta(seconds=900))))
            db.execute("INSERT INTO audit(subject,event,reference_id,at) VALUES (?,?,?,?)", (principal.subject,"proposal_approved",approval_id,iso_time(now)))
            db.commit()
        return approval_id

    def check_current(self, principal: Principal, snapshot: dict, now: datetime) -> None:
        current = self.retriever.bundle(principal,snapshot["asset_id"],"",now=now)
        if current["missing_information"]:
            raise LabError("DATA_NOT_ACTIONABLE", "当前数据、状态或程序不满足执行条件。")
        context = current["context"]
        for field, source in [("asset_version","version"),("temperature_c","temperature_c"),("observed_at","observed_at"),
                              ("as_of","as_of"),("procedure_id","procedure_id")]:
            if snapshot[field] != context[source]:
                raise LabError("STALE_PRECONDITION", "批准依赖的事实已经变化，必须刷新提案。")
        hashes = {d["id"]:d["content_hash"] for d in current["documents"] if d["id"] in snapshot["document_hashes"]}
        if hashes != snapshot["document_hashes"] or snapshot["policy_version"] != self.policy_version:
            raise LabError("STALE_PRECONDITION", "程序或策略发生变化，必须重新批准。")

    def update_result(self, operation_id: str, state: str, *, receipt: dict | None = None, error: str | None = None) -> dict:
        with database(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            current = db.execute("SELECT * FROM operations WHERE id=?", (operation_id,)).fetchone()
            if current["state"] in {"executed","failed"}:
                db.commit()
                return self.result(current)
            db.execute("UPDATE operations SET state=?,receipt_json=?,error=? WHERE id=?",
                       (state,json.dumps(receipt,sort_keys=True) if receipt else None,error,operation_id))
            db.execute("INSERT INTO audit(subject,event,reference_id,at) VALUES (?,?,?,?)",
                       ("system:work-order-adapter",state,operation_id,iso_time(FIXED_NOW)))
            row = db.execute("SELECT * FROM operations WHERE id=?", (operation_id,)).fetchone()
            db.commit()
        return self.result(row)

    @staticmethod
    def receipt_matches(receipt: dict, operation_id: str, proposal: dict) -> bool:
        snapshot = json.loads(proposal["snapshot_json"])
        return all([receipt.get("request_id") == operation_id, receipt.get("payload_hash") == proposal["payload_hash"],
                    receipt.get("tenant") == snapshot["tenant"], receipt.get("asset_id") == snapshot["asset_id"],
                    receipt.get("status") == "DRAFT", bool(receipt.get("receipt_id"))])

    def execute(self, principal: Principal, proposal_id: str, approval_id: str | None, idempotency_key: str,
                *, now: datetime = FIXED_NOW, timeout_after_commit: bool = False) -> dict:
        self.require_planner(principal)
        proposal = self.proposal(principal,proposal_id)
        if not isinstance(idempotency_key,str) or not 1 <= len(idempotency_key.strip()) <= 128:
            raise LabError("IDEMPOTENCY_KEY", "必须提供有效幂等键。")
        snapshot = json.loads(proposal["snapshot_json"])
        with database(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT o.* FROM operations o JOIN request_keys k ON o.id=k.operation_id WHERE k.tenant=? AND k.idempotency_key=?",
                                  (principal.tenant,idempotency_key)).fetchone()
            if existing:
                if existing["proposal_id"] != proposal_id or existing["payload_hash"] != proposal["payload_hash"]:
                    raise LabError("IDEMPOTENCY_CONFLICT", "同一幂等键不能绑定不同提案。")
                db.commit()
                return self.result(existing)
            existing = db.execute("SELECT * FROM operations WHERE proposal_id=?", (proposal_id,)).fetchone()
            if existing:
                db.execute("INSERT INTO request_keys VALUES (?,?,?)", (principal.tenant,idempotency_key,existing["id"]))
                db.commit()
                return self.result(existing)
            approval = db.execute("SELECT * FROM approvals WHERE id=?", (approval_id,)).fetchone()
            if approval is None or approval["proposal_id"] != proposal_id or approval["payload_hash"] != proposal["payload_hash"]:
                raise LabError("APPROVAL_REQUIRED", "缺少绑定当前提案的可信批准。")
            if now >= parse_time(approval["expires_at"]) or now < parse_time(approval["approved_at"]):
                raise LabError("APPROVAL_EXPIRED", "批准不在有效时间内。")
            self.check_current(principal,snapshot,now)
            operation_id = "OP-" + uuid.uuid4().hex
            db.execute("INSERT INTO operations VALUES (?,?,?,?,?,?,?)", (operation_id,proposal_id,principal.tenant,proposal["payload_hash"],"executing",None,None))
            db.execute("INSERT INTO request_keys VALUES (?,?,?)", (principal.tenant,idempotency_key,operation_id))
            db.execute("INSERT INTO audit(subject,event,reference_id,at) VALUES (?,?,?,?)", (principal.subject,"execution_claimed",operation_id,iso_time(now)))
            db.commit()
        # The external call is outside the local transaction. There is no shared commit.
        try:
            receipt = self.external.create(operation_id,snapshot,proposal["payload_hash"],timeout_after_commit=timeout_after_commit)
        except (TimeoutError, OSError, sqlite3.Error):
            return self.update_result(operation_id,"outcome_unknown",error="OUTCOME_UNKNOWN")
        except LabError as exc:
            return self.update_result(operation_id,"failed",error=exc.code)
        if not self.receipt_matches(receipt,operation_id,proposal):
            return self.update_result(operation_id,"outcome_unknown",error="RECEIPT_MISMATCH")
        return self.update_result(operation_id,"executed",receipt=receipt)

    def reconcile(self, principal: Principal, operation_id: str) -> dict:
        with database(self.path) as db:
            operation = db.execute("SELECT * FROM operations WHERE id=?", (operation_id,)).fetchone()
        if operation is None:
            raise LabError("NOT_FOUND_OR_FORBIDDEN", "执行记录不存在或无权访问。")
        proposal = self.proposal(principal,operation["proposal_id"])
        if operation["state"] == "executed":
            return self.result(operation)
        if operation["state"] == "failed":
            return self.result(operation)
        receipt = self.external.lookup(operation_id)
        if receipt and self.receipt_matches(receipt,operation_id,proposal):
            return self.update_result(operation_id,"executed",receipt=receipt)
        # No receipt is not proof that a delayed or concurrent operation cannot commit.
        return self.update_result(operation_id,"outcome_unknown",error="OUTCOME_UNKNOWN" if receipt is None else "RECEIPT_MISMATCH")
