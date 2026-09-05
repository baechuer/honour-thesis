#!/usr/bin/env python3
"""Materialise a sealed V7 coordinator binding envelope without outcomes.

The frozen V7 reconciliation packet intentionally contains only the two blind
assessments and fresh source.  A strict coordinator return also needs the two
validated return hashes.  This append-only controller utility obtains those
hashes by invoking the frozen protocol's validation path, writes no decision
or assessment outcome, and never changes the historical V7 package.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATH = ROOT / "skill_benchmark/scripts/rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
RECON_ROOT = ROOT / "skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase4-v7-strict-unified-reconciliation-2026-09-05"
ENVELOPE_NAME = "sealed_coordinator_binding_envelope.jsonl"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"Expected object at {path}:{line_number}")
        rows.append(row)
    return rows


def load_protocol() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_frozen_protocol", PROTOCOL_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load frozen V7 protocol")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_rows(batch_id: str) -> list[dict[str, Any]]:
    packet_path = RECON_ROOT / batch_id / "sealed_coordinator_packets.jsonl"
    packets = read_jsonl(packet_path)
    protocol = load_protocol()
    rows: list[dict[str, Any]] = []
    for packet in packets:
        token = packet.get("candidate_token")
        if not isinstance(token, str):
            raise ValueError("Sealed coordinator packet has no candidate token")
        bindings, _, _ = protocol.coordinator_context(batch_id, token)
        rows.append({
            "schema_version": "rq2b_nc_phase5_v7_sealed_coordinator_binding_envelope_v1",
            **bindings,
        })
    tokens = [row["candidate_token"] for row in rows]
    if len(tokens) != len(set(tokens)):
        raise ValueError("Duplicate coordinator token")
    return sorted(rows, key=lambda row: row["candidate_token"])


def serialise(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(row) + b"\n" for row in rows)


def materialise(batch_id: str) -> None:
    target = RECON_ROOT / batch_id / ENVELOPE_NAME
    if target.exists():
        raise ValueError(f"Refusing to overwrite coordinator binding envelope: {target}")
    content = serialise(expected_rows(batch_id))
    target.write_bytes(content)
    print(json.dumps({"batch_id": batch_id, "envelope_sha256": sha_bytes(content), "records": content.count(b"\n"), "status": "PASS_V7_SEALED_COORDINATOR_BINDING_ENVELOPE_MATERIALISED"}, sort_keys=True))


def verify(batch_id: str) -> None:
    target = RECON_ROOT / batch_id / ENVELOPE_NAME
    expected = serialise(expected_rows(batch_id))
    if not target.is_file() or target.read_bytes() != expected:
        raise ValueError("Sealed coordinator binding envelope drift")
    print(json.dumps({"batch_id": batch_id, "envelope_sha256": sha_bytes(expected), "records": expected.count(b"\n"), "status": "PASS_V7_SEALED_COORDINATOR_BINDING_ENVELOPE_REPLAY"}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("materialise", "verify"))
    parser.add_argument("--batch-id", required=True)
    args = parser.parse_args()
    if args.command == "materialise":
        materialise(args.batch_id)
    else:
        verify(args.batch_id)


if __name__ == "__main__":
    main()
