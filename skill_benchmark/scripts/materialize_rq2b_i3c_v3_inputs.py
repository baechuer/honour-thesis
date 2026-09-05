#!/usr/bin/env python3
"""Materialise only an explicitly approved RQ2b I3C V3 source assignment."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


SOURCE_VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
SOURCE_ROOT = f"skill_benchmark/rq2b_full_library/{SOURCE_VERSION_ID}"
V3_VERSION_ID = "rq2b-i3c-v3-2026-08-18"
V3_ROOT = f"skill_benchmark/rq2b_full_library/{V3_VERSION_ID}"
SOURCE_MANIFEST = f"{SOURCE_ROOT}/source_manifest.jsonl"
PACKET_PATH = f"{V3_ROOT}/source_assignment_approval_packet_sealed.json"
RECEIPT_PATH = f"{V3_ROOT}/source_assignment_approval_receipt.json"
OUTPUT_ROOT = f"{V3_ROOT}/i3c_extraction"
ALLOWED_INPUT_KEYS = {
    "source_row_index",
    "skill_id",
    "name",
    "description",
    "family",
    "source",
    "source_sha256",
    "text",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_jsonl(rows: list[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def input_row(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    raw = (root / source["source_path"]).read_bytes()
    if sha256_bytes(raw) != source["source_sha256"]:
        raise ValueError(f"Source drift: {source['skill_id']}")
    row = {
        "source_row_index": source["source_row_index"],
        "skill_id": source["skill_id"],
        "name": source["source_name"],
        "description": source["source_description"],
        "family": source["family"],
        "source": source["source_path"],
        "source_sha256": source["source_sha256"],
        "text": raw.decode("utf-8"),
    }
    if set(row) != ALLOWED_INPUT_KEYS:
        raise ValueError(f"V3 input schema violation: {source['skill_id']}")
    return row


def verify_approval(root: Path) -> dict[str, Any]:
    packet_path = root / PACKET_PATH
    receipt_path = root / RECEIPT_PATH
    if not packet_path.is_file() or not receipt_path.is_file():
        raise ValueError("V3 source-assignment packet or approval receipt is missing")
    packet = read_json(packet_path)
    receipt = read_json(receipt_path)
    packet_sha = sha256_file(packet_path)
    if packet["schema_version"] != "rq2b-i3c-v3-source-assignment-approval-packet-v1":
        raise ValueError("Unexpected V3 packet schema")
    if packet["state"] != "draft_pending_explicit_source_assignment_approval":
        raise ValueError("Unexpected V3 packet state")
    if receipt.get("state") != "explicitly_approved_for_v3_i3c_source_assignment_once":
        raise ValueError("V3 source assignment is not explicitly approved")
    if receipt.get("approved_packet", {}).get("sha256") != packet_sha:
        raise ValueError("V3 receipt does not bind the current packet")
    if receipt.get("approved_packet", {}).get("path") != PACKET_PATH:
        raise ValueError("V3 receipt packet path mismatch")
    if receipt.get("source_manifest", {}).get("sha256") != packet["source_corpus"]["source_manifest"]["sha256"]:
        raise ValueError("V3 receipt source manifest mismatch")
    return packet


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    packet = verify_approval(root)
    output_root = root / OUTPUT_ROOT
    staging_root = output_root.with_name(f".{output_root.name}.staging")
    if output_root.exists() or staging_root.exists():
        raise FileExistsError("Refusing to overwrite existing V3 I3C inputs")
    sources = read_jsonl(root / SOURCE_MANIFEST)
    if sha256_file(root / SOURCE_MANIFEST) != packet["source_corpus"]["source_manifest"]["sha256"]:
        raise ValueError("V3 source manifest hash drift")
    source_by_index = {row["source_row_index"]: row for row in sources}
    if sorted(source_by_index) != list(range(2433)):
        raise ValueError("V3 source row-index coverage mismatch")

    inputs_root = staging_root / "inputs"
    outputs_root = staging_root / "outputs"
    inputs_root.mkdir(parents=True, exist_ok=False)
    outputs_root.mkdir(parents=True, exist_ok=False)
    identities: list[dict[str, Any]] = []
    materialised: list[dict[str, Any]] = []
    try:
        for chunk in packet["chunks"]:
            indexes = range(chunk["first_source_row_index"], chunk["last_source_row_index"] + 1)
            rows = [input_row(root, source_by_index[index]) for index in indexes]
            payload = canonical_jsonl(rows)
            if sha256_bytes(payload) != chunk["planned_input_sha256"]:
                raise ValueError(f"V3 planned input hash mismatch: {chunk['chunk_index']}")
            path = inputs_root / Path(chunk["input_path"]).name
            path.write_bytes(payload)
            materialised.append({**chunk, "input_sha256": sha256_file(path)})
            identities.extend(
                {
                    "source_row_index": row["source_row_index"],
                    "skill_id": row["skill_id"],
                    "source": row["source"],
                    "source_sha256": row["source_sha256"],
                    "chunk_index": chunk["chunk_index"],
                    "chunk_row_index": index,
                }
                for index, row in enumerate(rows)
            )
        if len(identities) != 2433:
            raise ValueError("V3 materialised identity coverage mismatch")
        identity_path = staging_root / "identity_manifest.jsonl"
        identity_path.write_bytes(canonical_jsonl(identities))
        manifest = {
            "schema_version": "rq2b-i3c-v3-materialized-inputs-v1",
            "version_id": V3_VERSION_ID,
            "state": "inputs_materialized_not_assigned",
            "approved_packet": {"path": PACKET_PATH, "sha256": sha256_file(root / PACKET_PATH)},
            "approval_receipt": {"path": RECEIPT_PATH, "sha256": sha256_file(root / RECEIPT_PATH)},
            "source_manifest": packet["source_corpus"]["source_manifest"],
            "chunks": materialised,
            "identity_manifest": {"path": f"{OUTPUT_ROOT}/identity_manifest.jsonl", "sha256": sha256_file(identity_path), "rows": len(identities)},
            "counts": {"input_rows": len(identities), "chunks": len(materialised), "total_input_utf8_bytes": sum(row["input_utf8_bytes"] for row in materialised), "total_qwen_proxy_tokens": sum(row["qwen_proxy_tokens"] for row in materialised)},
            "network_calls": 0,
            "external_api_calls": 0,
            "external_texts_transmitted": 0,
            "worker_count": 0,
            "assignment_ledger": [{"chunk_index": row["chunk_index"], "status": "not_assigned", "attempt": 0} for row in materialised],
        }
        (staging_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        staging_root.replace(output_root)
    except BaseException:
        shutil.rmtree(staging_root, ignore_errors=True)
        raise
    print(json.dumps({"manifest": f"{OUTPUT_ROOT}/manifest.json", **manifest["counts"], "network_calls": 0, "external_api_calls": 0, "external_texts_transmitted": 0, "worker_count": 0}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
