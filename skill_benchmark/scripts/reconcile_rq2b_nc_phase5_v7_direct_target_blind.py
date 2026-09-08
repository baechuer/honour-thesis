#!/usr/bin/env python3
"""Materialise the V7 direct target-blind reconciliation queue.

This program is deliberately mechanical: it replays the selected Git blobs
for the 228 groups whose A/B adequacy vectors were exactly equal and contained
no ``UNCLEAR`` value.  It never opens the target join or builds an acceptable
set/library outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
NC = WORKSPACE / "skill_benchmark" / "rq2b_naturalistic_confusability"
INTEGRATION = NC / "manifests" / "rq2b_nc_phase5_v7_mechanical_integration_2026_09_08_v1"
V7 = NC / "manifests" / "RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery"
OUTPUT = NC / "manifests" / "rq2b_nc_phase5_v7_direct_target_blind_reconciliation_2026_09_08_v1"
VALID = {"FULLY_ACCEPTABLE", "PARTIALLY_ADEQUATE", "INADEQUATE", "UNCLEAR"}


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def vector_hash(returned: dict[str, Any]) -> str:
    vector = sorted((item["candidate_token"], item["adequacy"]) for item in returned["assessments"])
    return sha_bytes(json.dumps(vector, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def git_blobs(revision: str, paths: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(paths))
    process = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=WORKSPACE,
        input=("\n".join(f"{revision}:{path}" for path in unique) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        raise ValueError(process.stderr.decode("utf-8"))
    result: dict[str, bytes] = {}
    cursor = 0
    for path in unique:
        end = process.stdout.index(b"\n", cursor)
        header = process.stdout[cursor:end].decode("utf-8").split()
        cursor = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"missing/unexpected source blob: {revision}:{path}")
        size = int(header[2])
        result[path] = process.stdout[cursor:cursor + size]
        cursor += size
        if process.stdout[cursor:cursor + 1] != b"\n":
            raise ValueError(f"truncated source blob: {revision}:{path}")
        cursor += 1
    return result


def build_reconciliation() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    direct_queue = load_jsonl(INTEGRATION / "direct_reconciliation_queue.jsonl")
    ledger = load_jsonl(INTEGRATION / "integration_intake_ledger.jsonl")
    v7_rows = load_jsonl(V7 / "unified_prompt_group_batch_manifest.jsonl")
    if len(direct_queue) != 228 or len({row["batch_id"] for row in direct_queue}) != 228:
        raise ValueError("direct queue cardinality/identity drift")
    direct_ids = {row["batch_id"] for row in direct_queue}
    v7_by_id = {row["batch_id"]: row for row in v7_rows}
    if len(v7_by_id) != 1226 or not direct_ids <= set(v7_by_id):
        raise ValueError("V7 manifest/direct queue identity drift")

    selected = [row for row in ledger if row["group_route"] == "DIRECT_RECONCILIATION_ELIGIBLE"]
    by_group: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in selected:
        if not row["active_return_selected"] or row["validation"] != "PASS_V7_STRICT_UNIFIED_TARGET_BLIND_RETURN_VALIDATION":
            raise ValueError(f"direct lane not validator-passing: {row['batch_id']}/{row['reviewer_lane']}")
        by_group[row["batch_id"]][row["reviewer_lane"]] = row
    if set(by_group) != direct_ids or any(set(lanes) != {"A", "B"} for lanes in by_group.values()):
        raise ValueError("direct queue/active lane partition drift")

    blobs_by_commit = {
        commit: git_blobs(commit, [row["source_return_path"] for row in selected if row["source_commit"] == commit])
        for commit in sorted({row["source_commit"] for row in selected})
    }
    queue_by_id = {row["batch_id"]: row for row in direct_queue}
    group_rows: list[dict[str, Any]] = []
    adequacy_counts: Counter[str] = Counter()
    for batch_id in sorted(direct_ids):
        pair = by_group[batch_id]
        queue = queue_by_id[batch_id]
        v7 = v7_by_id[batch_id]
        if v7["blind_packet_id"] != queue["blind_packet_id"]:
            raise ValueError(f"V7 blind packet identity drift: {batch_id}")
        if v7["sealed_main_packet"].get("candidate_count") != 6 or len(v7["sealed_tail_packets"]) != 2 or any(item.get("candidate_count") != 1 for item in v7["sealed_tail_packets"]):
            raise ValueError(f"K=6/two-tail manifest shape drift: {batch_id}")
        returned: dict[str, dict[str, Any]] = {}
        for lane, evidence in pair.items():
            raw = blobs_by_commit[evidence["source_commit"]][evidence["source_return_path"]]
            if sha_bytes(raw) != evidence["source_return_sha256"]:
                raise ValueError(f"selected source-return hash drift: {batch_id}/{lane}")
            item = json.loads(raw)
            if item.get("reviewer_blind_id") != lane or item.get("batch_id") != batch_id or item.get("blind_packet_id") != queue["blind_packet_id"] or item.get("batch_input_sha256") != queue["packet_input_sha256"]:
                raise ValueError(f"selected source-return binding drift: {batch_id}/{lane}")
            if vector_hash(item) != evidence["assessment_vector_sha256"]:
                raise ValueError(f"selected source-return vector hash drift: {batch_id}/{lane}")
            returned[lane] = item
        a = {item["candidate_token"]: item["adequacy"] for item in returned["A"]["assessments"]}
        b = {item["candidate_token"]: item["adequacy"] for item in returned["B"]["assessments"]}
        if len(a) != 8 or set(a) != set(b) or a != b or any(value not in VALID - {"UNCLEAR"} for value in a.values()):
            raise ValueError(f"direct exact-agreement/unclear condition drift: {batch_id}")
        dispositions = [{"candidate_token": token, "final_adequacy": a[token], "decision_route": "EXACT_INDEPENDENT_AGREEMENT"} for token in sorted(a)]
        adequacy_counts.update(a.values())
        group_rows.append({
            "batch_id": batch_id,
            "blind_packet_id": queue["blind_packet_id"],
            "packet_input_sha256": queue["packet_input_sha256"],
            "sealed_main_packet_sha256": v7["sealed_main_packet"]["packet_sha256"],
            "sealed_tail_packet_sha256s": [item["packet_sha256"] for item in v7["sealed_tail_packets"]],
            "candidate_dispositions": dispositions,
            "group_reconciliation_state": "TARGET_BLIND_DIRECT_RECONCILIATION_PENDING_GLOBAL_MASTER_SOP_READINESS",
        })
    if len(group_rows) != 228 or sum(len(row["candidate_dispositions"]) for row in group_rows) != 1824:
        raise ValueError("direct reconciliation output cardinality drift")
    report = {
        "schema_version": "rq2b_nc_phase5_v7_direct_target_blind_reconciliation_v1",
        "status": "PASS_TARGET_BLIND_DIRECT_RECONCILIATION_PENDING_GLOBAL_MASTER_SOP_READINESS",
        "claim_boundary": "Target-blind mechanical reconciliation only; no target join, acceptable set, library update, retrieval result, metric, thesis result, or K change.",
        "counts": {"reconciled_direct_groups": 228, "candidate_dispositions": 1824, "final_adequacy_counts": dict(sorted(adequacy_counts.items())), "blocked_groups": 0},
        "bound_inputs": {
            "integration_ledger": str((INTEGRATION / "integration_intake_ledger.jsonl").relative_to(WORKSPACE)),
            "integration_ledger_sha256": sha_path(INTEGRATION / "integration_intake_ledger.jsonl"),
            "direct_queue": str((INTEGRATION / "direct_reconciliation_queue.jsonl").relative_to(WORKSPACE)),
            "direct_queue_sha256": sha_path(INTEGRATION / "direct_reconciliation_queue.jsonl"),
            "v7_unified_manifest": str((V7 / "unified_prompt_group_batch_manifest.jsonl").relative_to(WORKSPACE)),
            "v7_unified_manifest_sha256": sha_path(V7 / "unified_prompt_group_batch_manifest.jsonl"),
        },
        "mechanical_checks": {"two_active_lanes_per_group": True, "source_return_hash_replay": "PASS", "exact_vector_agreement_without_unclear": "PASS", "k6_two_tail_manifest_shape": "PASS"},
    }
    return group_rows, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite frozen direct reconciliation: {output}")
    rows, report = build_reconciliation()
    output.mkdir(parents=True)
    write_jsonl(output / "target_blind_direct_group_reconciliation.jsonl", rows)
    write_json(output / "integrity_report.json", report)
    (output / "integrity_report.md").write_text(
        "# V7 direct target-blind reconciliation\n\n"
        "- Reconciled groups: 228\n- Candidate dispositions: 1,824\n- Blocked groups: 0\n\n"
        "Only exact, validator-passing A/B evidence is combined. This is not an acceptable-set or library outcome.\n",
        encoding="utf-8",
    )
    (output / "README.md").write_text(
        "# V7 direct target-blind reconciliation\n\n"
        "The materialiser intentionally refuses to overwrite this frozen package. Verify it with:\n\n"
        "```sh\npython3 skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_direct_target_blind.py\n```\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": report["status"], "output": str(output), "counts": report["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
