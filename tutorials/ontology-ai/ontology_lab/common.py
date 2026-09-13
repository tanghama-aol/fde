from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from rdflib import Namespace, URIRef

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
EX = Namespace("https://example.org/maintenance/")
FIXED_NOW = datetime(2026, 9, 1, 9, 2, tzinfo=timezone.utc)
MAX_AGE_SECONDS = 300


class LabError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant: str
    regions: frozenset[str]
    roles: frozenset[str]


# These profiles stand in for a trusted login system, not fields supplied by a model.
NORTH_PLANNER = Principal("planner-a", "TENANT-A", frozenset({"NORTH"}), frozenset({"planner"}))
NORTH_READER = Principal("reader-a", "TENANT-A", frozenset({"NORTH"}), frozenset({"reader"}))
SOUTH_PLANNER = Principal("planner-south", "TENANT-A", frozenset({"SOUTH"}), frozenset({"planner"}))
OTHER_PLANNER = Principal("planner-b", "TENANT-B", frozenset({"NORTH"}), frozenset({"planner"}))


def require_identifier(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{0,39}", value):
        raise LabError("INVALID_ID", "标识必须使用限定的字母、数字和连字符。")
    return value


def entity(tenant: str, kind: str, identifier: str) -> URIRef:
    require_identifier(tenant)
    require_identifier(identifier)
    return URIRef(f"https://example.org/data/{quote(tenant)}/{quote(kind)}/{quote(identifier)}")


def graph_id(tenant: str) -> URIRef:
    return URIRef(f"https://example.org/graph/{quote(require_identifier(tenant))}")


def parse_time(value: str) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError, AttributeError) as exc:
        raise LabError("INVALID_TIME", "时间必须使用带时区的 ISO 8601 表示。") from exc
    if result.tzinfo is None:
        raise LabError("INVALID_TIME", "时间不能缺少时区。")
    return result.astimezone(timezone.utc)


def iso_time(value: datetime) -> str:
    if value.tzinfo is None:
        raise LabError("INVALID_TIME", "服务端时钟必须带时区。")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_hash(value: dict) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8"))
