#!/usr/bin/env python3
"""Materialise only the explicitly approved RQ2b v1.2 I3C worker inputs."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
ROOT_RELATIVE = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
SOURCE_MANIFEST = f"{ROOT_RELATIVE}/source_manifest.jsonl"
PACKET_PATH = f"{ROOT_RELATIVE}/i3c_source_assignment_approval_packet.json"
RECEIPT_PATH = f"{ROOT_RELATIVE}/i3c_source_assignment_approval_receipt.json"
OUTPUT_ROOT = f"{ROOT_RELATIVE}/i3c_extraction"
EXPECTED_PACKET_SHA256 = "472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe"
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def canonical_jsonl(rows: list[dict[str, Any]]) -> bytes:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
    ).encode("utf-8")


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
        raise ValueError(f"Input schema violation: {source['skill_id']}")
    return row


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    packet_path = root / PACKET_PATH
    receipt_path = root / RECEIPT_PATH
    packet = read_json(packet_path)
    receipt = read_json(receipt_path)
    if sha256_file(packet_path) != EXPECTED_PACKET_SHA256:
        raise ValueError("Packet hash differs from the explicitly approved packet")
    if receipt["state"] != "explicitly_approved_for_v12_i3c_source_assignment_once":
        raise ValueError("Source-assignment receipt is not approved")
    if receipt["approved_packet"]["sha256"] != EXPECTED_PACKET_SHA256:
        raise ValueError("Receipt does not bind the approved packet")
    if packet["state"] != "draft_pending_explicit_source_assignment_approval":
        raise ValueError("Unexpected packet state")

    output_root = root / OUTPUT_ROOT
    staging_root = output_root.parent / f".{output_root.name}.staging"
    if output_root.exists() or staging_root.exists():
        raise FileExistsError("Refusing to overwrite an existing I3C input workspace")
    sources = read_jsonl(root / SOURCE_MANIFEST)
    if sha256_file(root / SOURCE_MANIFEST) != packet["source_manifest"]["sha256"]:
        raise ValueError("Source manifest differs from packet")
    source_by_index = {row["source_row_index"]: row for row in sources}
    if sorted(source_by_index) != list(range(packet["source_manifest"]["rows"])):
        raise ValueError("Source manifest row-index coverage mismatch")

    input_root = staging_root / "inputs"
    output_dir = staging_root / "outputs"
    input_root.mkdir(parents=True, exist_ok=False)
    output_dir.mkdir(parents=True, exist_ok=False)
    identities = []
    materialised_chunks = []
    try:
        for chunk in packet["chunks"]:
            indexes = range(chunk["first_source_row_index"], chunk["last_source_row_index"] + 1)
            source_rows = [source_by_index[index] for index in indexes]
            rows = [input_row(root, source) for source in source_rows]
            payload = canonical_jsonl(rows)
            if sha256_bytes(payload) != chunk["planned_input_sha256"]:
                raise ValueError(f"Planned input hash mismatch: chunk {chunk['chunk_index']}")
            if len(rows) != chunk["row_count"] or len(payload) != chunk["input_utf8_bytes"]:
                raise ValueError(f"Planned input dimensions mismatch: chunk {chunk['chunk_index']}")
            expected_prefix = f"{OUTPUT_ROOT}/inputs/"
            if not chunk["input_path"].startswith(expected_prefix):
                raise ValueError(f"Unexpected input location: {chunk['input_path']}")
            path = input_root / Path(chunk["input_path"]).name
            path.write_bytes(payload)
            materialised_chunks.append({
                **chunk,
                "input_sha256": sha256_file(path),
                "input_path": chunk["input_path"],
            })
            for chunk_row_index, source in enumerate(source_rows):
                identities.append({
                    "source_row_index": source["source_row_index"],
                    "skill_id": source["skill_id"],
                    "source": source["source_path"],
                    "source_sha256": source["source_sha256"],
                    "chunk_index": chunk["chunk_index"],
                    "chunk_row_index": chunk_row_index,
                })
        if len(identities) != packet["source_manifest"]["rows"]:
            raise ValueError("Materialised identity coverage mismatch")
        identity_path = staging_root / "identity_manifest.jsonl"
        identity_path.write_bytes(canonical_jsonl(identities))
        execution_manifest = {
            "schema_version": "rq2b-v12-i3c-materialized-inputs-v1",
            "version_id": VERSION_ID,
            "state": "inputs_materialized_not_assigned",
            "approved_packet": {"path": PACKET_PATH, "sha256": EXPECTED_PACKET_SHA256},
            "approval_receipt": {"path": RECEIPT_PATH, "sha256": sha256_file(receipt_path)},
            "source_manifest": packet["source_manifest"],
            "chunks": materialised_chunks,
            "identity_manifest": {
                "path": f"{OUTPUT_ROOT}/identity_manifest.jsonl",
                "sha256": sha256_file(identity_path),
                "rows": len(identities),
            },
            "counts": {
                "input_rows": len(identities),
                "chunks": len(materialised_chunks),
                "total_input_utf8_bytes": sum(row["input_utf8_bytes"] for row in materialised_chunks),
                "total_qwen_proxy_tokens": sum(row["qwen_proxy_tokens"] for row in materialised_chunks),
            },
            "network_calls": 0,
            "external_api_calls": 0,
            "external_texts_transmitted": 0,
            "worker_count": 0,
            "assignment_ledger": [
                {"chunk_index": row["chunk_index"], "status": "not_assigned", "attempt": 0}
                for row in materialised_chunks
            ],
        }
        (staging_root / "manifest.json").write_text(
            json.dumps(execution_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        staging_root.replace(output_root)
    except BaseException:
        shutil.rmtree(staging_root, ignore_errors=True)
        raise

    print(json.dumps({
        "manifest": f"{OUTPUT_ROOT}/manifest.json",
        "input_rows": len(identities),
        "chunks": len(materialised_chunks),
        "total_input_utf8_bytes": sum(row["input_utf8_bytes"] for row in materialised_chunks),
        "total_qwen_proxy_tokens": sum(row["qwen_proxy_tokens"] for row in materialised_chunks),
        "network_calls": 0,
        "external_api_calls": 0,
        "external_texts_transmitted": 0,
        "worker_count": 0,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
