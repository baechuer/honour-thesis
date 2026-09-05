#!/usr/bin/env python3
"""Materialise and replay the frozen V7 Phase-5 two-machine handoff.

This is a dispatch-only controller.  It uses the official execution-state
reconciliation (not incidental files in reviewer directories) to assign only
non-finalised V7 prompt groups.  Each assigned row contains one complete,
role-hidden eight-candidate packet and requires two independent returns.
It neither reads adequacy outcomes nor opens a target, gold, or retrieval join.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
NC_ROOT = ROOT / "skill_benchmark" / "rq2b_naturalistic_confusability"
V7_MANIFEST = NC_ROOT / (
    "manifests/RQ2b-NC-audit-input-300plus-2026-09-05_v7-strict-unified-blind-delivery/"
    "unified_prompt_group_batch_manifest.jsonl"
)
V7_SCHEMA = V7_MANIFEST.parent / "unified_independent_reviewer_return_schema.json"
STATE = NC_ROOT / (
    "manifests/rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_v14_after_m0037_complete/"
    "execution_state_reconciliation.json"
)
PROTOCOL_PATH = ROOT / "skill_benchmark/scripts/rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
DEFAULT_OUT = NC_ROOT / "manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v1"

ASSIGNMENT_VERSION = "rq2b_nc_phase5_v7_parallel_handoff_v1"
PENDING_STATES = {"STARTED_INCOMPLETE", "UNSTARTED"}
MACHINES = ("machine_a", "machine_b")
EXPECTED_COUNTS = {"FINALISED": 147, "STARTED_INCOMPLETE": 1, "UNSTARTED": 1078}
def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_path(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return sha_bytes(canonical_bytes(value))


def pretty_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(row) + b"\n" for row in rows)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"Expected JSON object at {path}:{line_number}")
        rows.append(row)
    return rows


def load_protocol() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_handoff_protocol", PROTOCOL_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load frozen V7 protocol")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if module.EXECUTION / "unified_prompt_group_batch_manifest.jsonl" != V7_MANIFEST:
        raise ValueError("V7 protocol / manifest binding drift")
    return module


def verified_inputs() -> tuple[Any, list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    for path in (V7_MANIFEST, V7_SCHEMA, STATE, PROTOCOL_PATH):
        if not path.is_file():
            raise ValueError(f"Missing required input: {path}")
    protocol = load_protocol()
    protocol.verify_execution()
    manifests = read_jsonl(V7_MANIFEST)
    if len(manifests) != 1226:
        raise ValueError("V7 manifest cardinality drift")
    by_batch = {row.get("batch_id"): row for row in manifests}
    if len(by_batch) != 1226 or any(not isinstance(key, str) for key in by_batch):
        raise ValueError("V7 manifest batch identity drift")
    state = read_json(STATE)
    state_without_hash = dict(state)
    stored_state_hash = state_without_hash.pop("reconciliation_sha256", None)
    if stored_state_hash != canonical_sha(state_without_hash):
        raise ValueError("Official execution-state reconciliation hash drift")
    if state.get("state_counts") != EXPECTED_COUNTS:
        raise ValueError(f"Official state-count drift: {state.get('state_counts')}")
    records = state.get("records")
    if not isinstance(records, list) or len(records) != 1226:
        raise ValueError("Official state record cardinality drift")
    state_by_batch = {record.get("batch_id"): record for record in records if isinstance(record, dict)}
    if set(state_by_batch) != set(by_batch) or len(state_by_batch) != 1226:
        raise ValueError("Official state / V7 manifest membership drift")
    if Counter(record.get("state") for record in records) != Counter(EXPECTED_COUNTS):
        raise ValueError("Official state record count drift")
    manifest_hash = sha_path(V7_MANIFEST)
    if state.get("bound_inputs", {}).get(str(V7_MANIFEST.relative_to(ROOT))) != manifest_hash:
        raise ValueError("Official state V7 manifest hash binding drift")
    return protocol, manifests, state_by_batch, state


def packet_for_manifest(protocol: Any, manifest: dict[str, Any], main_by_id: dict[str, dict[str, Any]], tail_by_id: dict[str, dict[str, Any]], instruction: str) -> dict[str, Any]:
    main_spec = manifest.get("sealed_main_packet")
    if not isinstance(main_spec, dict):
        raise ValueError("Missing sealed main specification")
    main = main_by_id.get(main_spec.get("packet_id"))
    if main is None or protocol.canonical_sha(main) != main_spec.get("packet_sha256") or len(main.get("candidates", [])) != 6:
        raise ValueError(f"Main packet binding drift: {manifest.get('batch_id')}")
    tail_specs = manifest.get("sealed_tail_packets")
    if not isinstance(tail_specs, list) or len(tail_specs) != 2:
        raise ValueError(f"Tail cardinality drift: {manifest.get('batch_id')}")
    tails: list[dict[str, Any]] = []
    for spec in tail_specs:
        if not isinstance(spec, dict):
            raise ValueError("Malformed tail specification")
        tail = tail_by_id.get(spec.get("packet_id"))
        if tail is None or protocol.canonical_sha(tail) != spec.get("packet_sha256") or len(tail.get("candidates", [])) != 1:
            raise ValueError(f"Tail packet binding drift: {manifest.get('batch_id')}")
        tails.append(tail)
    candidates = [
        {"candidate_token": candidate["candidate_token"], "source_full_skill": candidate["source_full_skill"]}
        for candidate in list(main["candidates"]) + [candidate for tail in tails for candidate in tail["candidates"]]
    ]
    candidates.sort(key=lambda candidate: candidate["candidate_token"])
    tokens = [candidate["candidate_token"] for candidate in candidates]
    if len(tokens) != 8 or len(set(tokens)) != 8 or protocol.canonical_sha(tokens) != manifest.get("unified_candidate_tokens_sha256"):
        raise ValueError(f"Unified candidate binding drift: {manifest.get('batch_id')}")
    packet = {
        "blind_packet_id": manifest["blind_packet_id"],
        "prompt": main["prompt"],
        "candidates": candidates,
        "review_instruction": instruction,
    }
    if set(packet) != protocol.PACKET_FIELDS or protocol.keys_deep(packet) & protocol.FORBIDDEN_KEYS:
        raise ValueError(f"Blind packet leakage or schema drift: {manifest.get('batch_id')}")
    return packet


def reissue_detail(state_record: dict[str, Any]) -> dict[str, Any]:
    if state_record["state"] == "UNSTARTED":
        return {
            "state_at_freeze": "UNSTARTED",
            "return_action": "ISSUE_TWO_NEW_INDEPENDENT_RETURNS",
            "preserved_return_paths": [],
        }
    if state_record["state"] != "STARTED_INCOMPLETE":
        raise ValueError(f"Not pending: {state_record['state']}")
    paths: list[str] = []
    batch_id = state_record["batch_id"]
    if state_record.get("reviewer_a_return_present"):
        paths.append(f"skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05/reviewer_A/{batch_id}.json")
    if state_record.get("reviewer_b_return_present"):
        paths.append(f"skill_benchmark/rq2b_naturalistic_confusability/review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05/reviewer_B/{batch_id}.json")
    return {
        "state_at_freeze": "STARTED_INCOMPLETE",
        "return_action": "TRACEABLE_REISSUE_PRESERVE_EXISTING_RETURN_AND_ISSUE_MISSING_OR_INVALID_ROLE",
        "preserved_return_paths": paths,
    }


def expected_rows() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    protocol, manifests, state_by_batch, state = verified_inputs()
    _, main_by_id, tail_by_id = protocol.verify_audit()
    instruction, _, _, _ = protocol.reviewer_instruction_and_schema()
    manifest_sha = sha_path(V7_MANIFEST)
    candidates: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for manifest in manifests:
        batch_id = manifest["batch_id"]
        record = state_by_batch[batch_id]
        if record["state"] in PENDING_STATES:
            candidates.append((hashlib.sha256(batch_id.encode("utf-8")).hexdigest(), manifest, record))
    candidates.sort(key=lambda item: (item[0], item[1]["batch_id"]))
    if len(candidates) != 1079:
        raise ValueError(f"Pending group count drift: {len(candidates)}")
    assignments: list[dict[str, Any]] = []
    machine_rows: dict[str, list[dict[str, Any]]] = {machine: [] for machine in MACHINES}
    for rank, (sort_sha, manifest, record) in enumerate(candidates, 1):
        owner = "machine_a" if rank <= 540 else "machine_b"
        packet = packet_for_manifest(protocol, manifest, main_by_id, tail_by_id, instruction)
        packet_hash = protocol.canonical_sha(packet)
        detail = reissue_detail(record)
        base = {
            "assignment_version": ASSIGNMENT_VERSION,
            "assignment_rank_by_sha256_batch_id": rank,
            "batch_id": manifest["batch_id"],
            "blind_packet_id": manifest["blind_packet_id"],
            "owner_machine": owner,
            "sha256_batch_id": sort_sha,
            "source_manifest_sha256": manifest_sha,
            "packet_input_sha256": packet_hash,
            "protocol_instruction_sha256": manifest["reviewer_instruction_sha256"],
            "sealed_main_packet_sha256": manifest["sealed_main_packet"]["packet_sha256"],
            "sealed_tail_packet_sha256s": [item["packet_sha256"] for item in manifest["sealed_tail_packets"]],
            "required_independent_reviewer_roles": ["A", "B"],
            **detail,
        }
        assignments.append(base)
        machine_rows[owner].append({
            **base,
            "schema_version": "rq2b_nc_phase5_v7_machine_target_blind_packet_v1",
            "sealed_target_blind_packet": packet,
            "blindness_notice": "This packet contains no target identity, gold label, retrieval result or reconciliation decision. Both reviewer roles independently assess every visible candidate.",
        })
    return assignments, machine_rows, state


def readme() -> str:
    return """# RQ2B V7 Phase-5 two-machine handoff freeze

This directory is a dispatch artifact, not an experiment, result, acceptable-set
decision, or reconciliation output. It is frozen from the V7 unified manifest
and the official execution-state reconciliation.

## Scope

- 147 `FINALISED` groups are locked and deliberately absent.
- `RQ2B-P4-V7-U0077` is a traceable reissue: its existing return remains in
  the canonical return directory and must be revalidated rather than replaced.
- The remaining 1,078 `UNSTARTED` groups are newly issued.
- Pending `batch_id`s are ordered by `SHA-256(batch_id)`; ranks 1--540 are
  `machine_a`, ranks 541--1,079 are `machine_b`.
- A group is indivisible: one prompt, six sealed main candidates, and two
  sealed tail candidates. The reviewer-facing packet intentionally hides
  main/tail role, target identity, labels, ranks, paths, provenance and all
  outcomes.

### State-snapshot freshness gate

This handoff is intentionally bound to the named V14 execution-state snapshot,
not to a count inferred from files in a reviewer directory. Before anyone
begins dispatch, rerun the execution-state reconciler. If its replay differs
from the V14 snapshot, stop and create a new state-pinned handoff rather than
reviewing any group whose current state may have changed.

## Two-computer procedure

1. Both computers clone the same frozen commit containing this directory.
2. Machine A reads only `machine_a_manifest.jsonl`; machine B reads only
   `machine_b_manifest.jsonl`. Do not redistribute a group between machines.
3. For every assigned group, create two **independent, target-blind** returns:
   one for reviewer role `A` and one for reviewer role `B`. Machine ownership
   is workload partitioning; it is not a substitute for the two reviewers.
4. Keep reviewer A and B work sealed from each other until submission. Each
   reviewer reads only the assigned role-hidden packet and the frozen V7 return
   schema in `reviewer_return_schema.json`.
5. Write returns on separate branches and directories:
   - `codex/rq2b-v7-review-machine-a`
   - `codex/rq2b-v7-review-machine-b`
   Canonical integration locations remain
   `.../review/RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05/reviewer_A/`
   and `reviewer_B/`; never overwrite an existing return. For U0077, first
   validate the preserved A return under the V7 contract, then issue only the
   missing or invalid role as a separate traceable reissue.
6. Before merge, rerun this handoff verifier plus the frozen V7 return
   validator/reconciliation contract. Merge is blocked unless coverage,
   machine disjointness, packet hashes, schema, and two-return coverage all
   pass.

## Files

- `phase5_v7_pending_assignment_v1.jsonl`: administrative provenance and
  assignment ledger; it is not reviewer input.
- `machine_a_manifest.jsonl`, `machine_b_manifest.jsonl`: role-hidden,
  complete eight-candidate packets owned by exactly one machine.
- `integrity_report.json` / `.md`: frozen inputs, counts, and replay checks.

Do not inspect V7 allocation, token joins, targets, historical gold, peer
returns, reconciliation material, retrieval/reranking/provider outputs, or
metrics while reviewing.
"""


def integrity_payload(assignments: list[dict[str, Any]], machine_rows: dict[str, list[dict[str, Any]]], state: dict[str, Any]) -> dict[str, Any]:
    assigned_ids = {row["batch_id"] for row in assignments}
    state_by_id = {row["batch_id"]: row for row in state["records"]}
    finalised = {batch_id for batch_id, row in state_by_id.items() if row["state"] == "FINALISED"}
    owners = {machine: {row["batch_id"] for row in rows} for machine, rows in machine_rows.items()}
    validations = {
        "official_state_counts_exact": state["state_counts"] == EXPECTED_COUNTS,
        "pending_count_exact": len(assignments) == 1079,
        "machine_a_count_exact": len(machine_rows["machine_a"]) == 540,
        "machine_b_count_exact": len(machine_rows["machine_b"]) == 539,
        "machine_sets_disjoint": not (owners["machine_a"] & owners["machine_b"]),
        "machine_union_equals_pending": owners["machine_a"] | owners["machine_b"] == assigned_ids,
        "no_finalised_batch_assigned": not (assigned_ids & finalised),
        "one_started_incomplete_traceable_reissue": sum(row["state_at_freeze"] == "STARTED_INCOMPLETE" for row in assignments) == 1,
        "all_packets_are_complete_eight_candidate_v7_packets": all(len(row["sealed_target_blind_packet"]["candidates"]) == 8 for rows in machine_rows.values() for row in rows),
        "machine_rows_expose_only_the_expected_role_hidden_packet_fields": all(
            set(row["sealed_target_blind_packet"]) == {"blind_packet_id", "prompt", "candidates", "review_instruction"}
            and all(set(candidate) == {"candidate_token", "source_full_skill"} for candidate in row["sealed_target_blind_packet"]["candidates"])
            for rows in machine_rows.values()
            for row in rows
        ),
    }
    if not all(validations.values()):
        failed = sorted(name for name, passed in validations.items() if not passed)
        raise ValueError(f"Handoff integrity failure: {failed}")
    return {
        "schema_version": "rq2b_nc_phase5_v7_parallel_handoff_integrity_v1",
        "status": "PASS_RQ2B_V7_PHASE5_TWO_MACHINE_HANDOFF_FREEZE",
        "claim_boundary": "Dispatch and integrity only; no reviewer adequacy outcome, reconciliation decision, target join, acceptable-set result, retrieval, reranking, provider output or metric is read or produced.",
        "assignment_version": ASSIGNMENT_VERSION,
        "bound_inputs": {
            str(V7_MANIFEST.relative_to(ROOT)): sha_path(V7_MANIFEST),
            str(STATE.relative_to(ROOT)): sha_path(STATE),
            str(PROTOCOL_PATH.relative_to(ROOT)): sha_path(PROTOCOL_PATH),
            str(V7_SCHEMA.relative_to(ROOT)): sha_path(V7_SCHEMA),
        },
        "official_state_counts": state["state_counts"],
        "counts": {
            "v7_prompt_groups": 1226,
            "finalised_locked": 147,
            "started_incomplete_reissued": 1,
            "unstarted_issued": 1078,
            "pending_assigned": 1079,
            "machine_a": 540,
            "machine_b": 539,
            "required_new_or_revalidated_independent_returns": 2158,
        },
        "validation": validations,
        "compatibility": {
            "frozen_v7_protocol_verify_execution": "PASS",
            "official_execution_state_reconciliation_hash": "PASS",
            "packet_reconstruction_against_v7_main_tail_hashes": "PASS",
            "existing_return_and_reconciliation_contract": "V7 protocol validates returned files after they are integrated into its canonical reviewer return paths; this handoff does not alter those paths or returns.",
            "execution_state_reconciler_validate_handoff": "The existing execution-state reconciliation script exposes validate-handoff for this state-pinned package; it verifies assignment coverage without reading outcomes.",
        },
    }


def write_package(out: Path) -> None:
    if out.exists():
        raise ValueError(f"Refusing to overwrite frozen handoff package: {out}")
    assignments, machine_rows, state = expected_rows()
    out.mkdir(parents=True)
    (out / "phase5_v7_pending_assignment_v1.jsonl").write_bytes(jsonl_bytes(assignments))
    (out / "machine_a_manifest.jsonl").write_bytes(jsonl_bytes(machine_rows["machine_a"]))
    (out / "machine_b_manifest.jsonl").write_bytes(jsonl_bytes(machine_rows["machine_b"]))
    (out / "reviewer_return_schema.json").write_bytes(pretty_json(read_json(V7_SCHEMA)))
    (out / "README.md").write_text(readme(), encoding="utf-8")
    report = integrity_payload(assignments, machine_rows, state)
    report["outputs"] = {
        name: sha_path(out / name)
        for name in ("phase5_v7_pending_assignment_v1.jsonl", "machine_a_manifest.jsonl", "machine_b_manifest.jsonl", "reviewer_return_schema.json", "README.md")
    }
    report["integrity_report_sha256"] = canonical_sha(report)
    (out / "integrity_report.json").write_bytes(pretty_json(report))
    md = "\n".join([
        "# RQ2B V7 parallel handoff integrity report",
        "",
        f"Status: `{report['status']}`",
        "",
        "| Check | Result |",
        "| --- | --- |",
        *[f"| {key} | {'PASS' if value else 'FAIL'} |" for key, value in report["validation"].items()],
        "",
        f"Pending: {report['counts']['pending_assigned']}; machine A: {report['counts']['machine_a']}; machine B: {report['counts']['machine_b']}; finalised locked: {report['counts']['finalised_locked']}.",
        "",
        "No reviewer outcomes, target joins, retrieval outputs, or metrics were read or generated.",
        "",
    ])
    (out / "integrity_report.md").write_text(md, encoding="utf-8")
    print(json.dumps({"output_dir": str(out), "status": report["status"], "counts": report["counts"]}, sort_keys=True))


def verify_package(out: Path) -> None:
    assignments, machine_rows, state = expected_rows()
    expected_files = {
        "phase5_v7_pending_assignment_v1.jsonl": jsonl_bytes(assignments),
        "machine_a_manifest.jsonl": jsonl_bytes(machine_rows["machine_a"]),
        "machine_b_manifest.jsonl": jsonl_bytes(machine_rows["machine_b"]),
        "reviewer_return_schema.json": pretty_json(read_json(V7_SCHEMA)),
        "README.md": readme().encode("utf-8"),
    }
    for name, expected in expected_files.items():
        path = out / name
        if not path.is_file() or path.read_bytes() != expected:
            raise ValueError(f"Frozen handoff drift: {path}")
    report = read_json(out / "integrity_report.json")
    copied = dict(report)
    stored_hash = copied.pop("integrity_report_sha256", None)
    if stored_hash != canonical_sha(copied):
        raise ValueError("Integrity report self-hash drift")
    regenerated = integrity_payload(assignments, machine_rows, state)
    if report.get("status") != regenerated["status"] or report.get("validation") != regenerated["validation"] or report.get("counts") != regenerated["counts"]:
        raise ValueError("Integrity report semantic drift")
    for name, expected in expected_files.items():
        if report.get("outputs", {}).get(name) != sha_bytes(expected):
            raise ValueError(f"Integrity report output hash drift: {name}")
    print(json.dumps({"output_dir": str(out), "status": "PASS_RQ2B_V7_PHASE5_TWO_MACHINE_HANDOFF_REPLAY", "counts": regenerated["counts"]}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("materialise", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    if args.command == "materialise":
        write_package(args.output_dir.resolve())
    else:
        verify_package(args.output_dir.resolve())


if __name__ == "__main__":
    main()
