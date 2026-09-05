#!/usr/bin/env python3
"""Materialise/replay an append-only V7-only Phase-5 handoff from a fresh state.

Unlike the historical V1 materialiser, this script accepts an explicit
execution-state snapshot.  It does not mutate V7, V1, reviewer returns, or a
different RQ2B package.  The only review input it produces is a complete,
role-hidden V7 packet, so no target, label, retrieval, or prior outcome is
exposed to either reviewer lane.
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
V1_SCRIPT = ROOT / "skill_benchmark/scripts/materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06.py"
DEFAULT_STATE = NC_ROOT / (
    "manifests/rq2b_nc_phase5_execution_state_reconciliation_2026_09_06_"
    "v20_v7_dispatch_freshness_replay/execution_state_reconciliation.json"
)
DEFAULT_OUT = NC_ROOT / "manifests/rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2_fresh_v20"
ASSIGNMENT_VERSION = "rq2b_nc_phase5_v7_parallel_handoff_v2_fresh_state"
MACHINES = ("machine_a", "machine_b")
PENDING_STATES = {"STARTED_INCOMPLETE", "UNSTARTED"}
ALLOWED_STATES = PENDING_STATES | {"FINALISED"}


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


def load_v1_helpers() -> Any:
    spec = importlib.util.spec_from_file_location("rq2b_v7_handoff_v1_helpers", V1_SCRIPT)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load historical V1 V7 handoff helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_fresh_state(base: Any, state_file: Path) -> tuple[Any, list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    """Use V1's V7 packet/protocol verification, parameterised by this snapshot."""
    if not state_file.is_file():
        raise ValueError(f"Missing state snapshot: {state_file}")
    state = read_json(state_file)
    records = state.get("records")
    counts = state.get("state_counts")
    if not isinstance(records, list) or not isinstance(counts, dict):
        raise ValueError("State snapshot lacks records or state counts")
    observed = Counter(record.get("state") for record in records if isinstance(record, dict))
    if dict(sorted(observed.items())) != dict(sorted(counts.items())):
        raise ValueError("State record/count mismatch")
    if set(observed) - ALLOWED_STATES:
        raise ValueError(f"State has non-dispatchable records: {sorted(set(observed) - ALLOWED_STATES)}")
    # The historical helper already checks state self-hash, 1,226 V7-manifest
    # membership, V7 manifest binding, the frozen protocol, and K=6/tail joins.
    base.STATE = state_file.resolve()
    base.EXPECTED_COUNTS = dict(sorted(counts.items()))
    protocol, manifests, state_by_batch, replayed_state = base.verified_inputs()
    if replayed_state != state:
        raise ValueError("Fresh-state loading drift")
    return protocol, manifests, state_by_batch, state


def expected_rows(state_file: Path) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    base = load_v1_helpers()
    protocol, manifests, state_by_batch, state = verify_fresh_state(base, state_file)
    _, main_by_id, tail_by_id = protocol.verify_audit()
    instruction, _, _, _ = protocol.reviewer_instruction_and_schema()
    manifest_sha = sha_path(base.V7_MANIFEST)
    ordered: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for manifest in manifests:
        batch_id = manifest["batch_id"]
        record = state_by_batch[batch_id]
        if record["state"] in PENDING_STATES:
            ordered.append((hashlib.sha256(batch_id.encode("utf-8")).hexdigest(), manifest, record))
    ordered.sort(key=lambda item: (item[0], item[1]["batch_id"]))
    if not ordered:
        raise ValueError("No pending V7 groups remain; no dispatch package is required")
    first_machine_count = (len(ordered) + 1) // 2
    assignments: list[dict[str, Any]] = []
    machine_rows: dict[str, list[dict[str, Any]]] = {machine: [] for machine in MACHINES}
    for rank, (sort_sha, manifest, record) in enumerate(ordered, 1):
        owner = "machine_a" if rank <= first_machine_count else "machine_b"
        packet = base.packet_for_manifest(protocol, manifest, main_by_id, tail_by_id, instruction)
        packet_hash = protocol.canonical_sha(packet)
        base_detail = base.reissue_detail(record)
        row = {
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
            **base_detail,
        }
        assignments.append(row)
        machine_rows[owner].append({
            **row,
            "schema_version": "rq2b_nc_phase5_v7_machine_target_blind_packet_v2",
            "sealed_target_blind_packet": packet,
            "blindness_notice": "This packet contains no target identity, gold label, retrieval result, prior return, or reconciliation decision. Reviewer A and reviewer B independently assess every visible candidate.",
        })
    return assignments, machine_rows, state


def counts_for(assignments: list[dict[str, Any]], machine_rows: dict[str, list[dict[str, Any]]], state: dict[str, Any]) -> dict[str, int]:
    counts = Counter(state["state_counts"])
    return {
        "v7_prompt_groups": sum(counts.values()),
        "finalised_locked": counts["FINALISED"],
        "started_incomplete_traceable_reissues": counts["STARTED_INCOMPLETE"],
        "unstarted_issued": counts["UNSTARTED"],
        "pending_assigned": len(assignments),
        "machine_a": len(machine_rows["machine_a"]),
        "machine_b": len(machine_rows["machine_b"]),
        "required_independent_reviewer_lanes": 2 * len(assignments),
    }


def readme(state_file: Path, counts: dict[str, int]) -> str:
    state_relative = state_file.resolve().relative_to(ROOT)
    return f"""# RQ2B V7 Phase-5 current two-machine handoff

This is an append-only dispatch package for the historical **V7 unified
dispatch package**. It is not the newer 528-group package, and it neither
creates results nor reads adequacy outcomes, target joins, retrieval,
reranking, provider outputs, or metrics.

## Frozen scope and current state

- V7 has `{counts['v7_prompt_groups']}` prompt groups.
- This package is bound to `{state_relative}`.
- `{counts['finalised_locked']}` `FINALISED` groups are locked and omitted.
- `{counts['started_incomplete_traceable_reissues']}` `STARTED_INCOMPLETE`
  group is retained as a traceable reissue: preserve its existing return(s),
  validate them, and issue only a missing or invalid reviewer role.
- `{counts['unstarted_issued']}` `UNSTARTED` groups are issued.
- The `{counts['pending_assigned']}` pending groups are SHA-256 ordered by
  `batch_id`; Machine A owns ranks 1--{counts['machine_a']} and Machine B owns
  the remainder ({counts['machine_b']}).

A group is indivisible: one prompt, six sealed main candidates, and two sealed
tail candidates. Reviewer-facing packets deliberately hide main/tail role,
target identity, labels, ranks, paths, provenance, peer returns, and outcomes.

## Deferred successor boundary

The newer 528-group current package is deferred. Do not mix its packets,
candidate tokens, returns, labels, outcomes, or reconciliation artifacts with
this V7 audit. This audit's completed groups count only toward V7 execution
completion; they do not establish whole-library closure, strict-gold closure,
retrieval performance, or coverage of deferred additions.

## Two-computer launch

Both machines first clone the same commit containing this directory, then use
their own review branch.

Machine A:

```bash
git switch -c codex/rq2b-v7-review-machine-a
python3 skill_benchmark/scripts/materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2.py verify --state-file {state_relative} --output-dir {DEFAULT_OUT.relative_to(ROOT)}
# Review only: {DEFAULT_OUT.relative_to(ROOT)}/machine_a_manifest.jsonl
```

Machine B:

```bash
git switch -c codex/rq2b-v7-review-machine-b
python3 skill_benchmark/scripts/materialize_rq2b_nc_phase5_v7_parallel_handoff_2026_09_06_v2.py verify --state-file {state_relative} --output-dir {DEFAULT_OUT.relative_to(ROOT)}
# Review only: {DEFAULT_OUT.relative_to(ROOT)}/machine_b_manifest.jsonl
```

For each owned group, create two separate **target-blind** reviewer returns,
one for role A and one for role B. Machine ownership is workload partitioning,
not a substitute for independent A/B review. Keep A and B sealed from one
another. Send disagreements only to the sealed coordinator. Never overwrite an
existing canonical return; write traceable reissues as new files/records under
the V7 return contract.

Before every commit, rerun this verifier, the frozen V7 return validator for
each changed reviewer file, and a fresh execution-state reconciliation. Merge
is blocked unless packet/input hashes, schema, target blindness, complete A/B
coverage, machine disjointness, and pending-scope coverage pass.

## Files

- `current_phase5_pending_assignment_v1.jsonl`: administrative assignment
  ledger; it is not reviewer input.
- `machine_a_manifest.jsonl`, `machine_b_manifest.jsonl`: complete,
  role-hidden packets owned by exactly one machine.
- `reviewer_return_schema.json`: frozen V7 independent-return schema.
- `integrity_report.json` / `.md`: hash-bound state, counts, and checks.
- `V7_SCOPE_AMENDMENT.md`: the operative-scope and deferred-successor boundary.
"""


def scope_amendment(counts: dict[str, int]) -> bytes:
    return (f"""# V7 Phase-5 scope amendment

The operative acceptable-set audit scope for this round is the historical V7
strict-unified dispatch package only. Its canonical manifest has
`{counts['v7_prompt_groups']}` prompt groups. The `{counts['finalised_locked']}`
groups that are currently `FINALISED` count toward V7 execution completion and
are locked: they must not be rerun or overwritten.

The deferred successor is the newer 528-group current package. It is retained
but is not executed in this round. Do not combine its packets, opaque tokens,
returns, labels, outcomes, or reconciliation artifacts with the V7 audit, and
do not present this round as covering deferred additions.

This amendment is a dispatch-scope statement only. It does not create an
acceptable-set result, strict-gold result, retrieval result, metric, or
whole-library closure claim.
""").encode("utf-8")


def integrity_payload(assignments: list[dict[str, Any]], machine_rows: dict[str, list[dict[str, Any]]], state_file: Path, state: dict[str, Any]) -> dict[str, Any]:
    base = load_v1_helpers()
    state_by_id = {record["batch_id"]: record for record in state["records"]}
    pending = {batch_id for batch_id, record in state_by_id.items() if record["state"] in PENDING_STATES}
    finalised = {batch_id for batch_id, record in state_by_id.items() if record["state"] == "FINALISED"}
    owners = {machine: {row["batch_id"] for row in rows} for machine, rows in machine_rows.items()}
    assigned = {row["batch_id"] for row in assignments}
    counts = counts_for(assignments, machine_rows, state)
    validations = {
        "fresh_state_has_only_dispatchable_states": set(state["state_counts"]) <= ALLOWED_STATES,
        "state_counts_match_manifest_total": counts["v7_prompt_groups"] == 1226,
        "pending_assignment_matches_fresh_state": assigned == pending,
        "machine_sets_disjoint": not (owners["machine_a"] & owners["machine_b"]),
        "machine_union_equals_pending": owners["machine_a"] | owners["machine_b"] == pending,
        "machine_balance_within_one_group": abs(counts["machine_a"] - counts["machine_b"]) <= 1,
        "no_finalised_batch_assigned": not (assigned & finalised),
        "started_incomplete_reissues_are_traceable": all(
            row["state_at_freeze"] != "STARTED_INCOMPLETE" or row["return_action"].startswith("TRACEABLE_REISSUE")
            for row in assignments
        ),
        "all_packets_are_complete_eight_candidate_v7_packets": all(
            len(row["sealed_target_blind_packet"]["candidates"]) == 8
            for rows in machine_rows.values() for row in rows
        ),
        "all_main_and_tail_packet_hashes_bind_to_v7_manifest": all(
            len(row["sealed_tail_packet_sha256s"]) == 2 and isinstance(row["sealed_main_packet_sha256"], str)
            for row in assignments
        ),
        "reviewer_packets_are_role_hidden": all(
            set(row["sealed_target_blind_packet"]) == {"blind_packet_id", "prompt", "candidates", "review_instruction"}
            and all(set(candidate) == {"candidate_token", "source_full_skill"} for candidate in row["sealed_target_blind_packet"]["candidates"])
            for rows in machine_rows.values() for row in rows
        ),
    }
    if not all(validations.values()):
        raise ValueError(f"V7 handoff integrity failure: {[name for name, passed in validations.items() if not passed]}")
    return {
        "schema_version": "rq2b_nc_phase5_v7_parallel_handoff_integrity_v2",
        "status": "PASS_RQ2B_V7_PHASE5_FRESH_TWO_MACHINE_HANDOFF_FREEZE",
        "claim_boundary": "Dispatch and integrity only. No reviewer adequacy outcome, target join, acceptable-set result, retrieval, reranking, provider call, metric, or thesis result is read or generated.",
        "assignment_version": ASSIGNMENT_VERSION,
        "bound_inputs": {
            str(base.V7_MANIFEST.relative_to(ROOT)): sha_path(base.V7_MANIFEST),
            str(state_file.resolve().relative_to(ROOT)): sha_path(state_file),
            str(base.PROTOCOL_PATH.relative_to(ROOT)): sha_path(base.PROTOCOL_PATH),
            str(base.V7_SCHEMA.relative_to(ROOT)): sha_path(base.V7_SCHEMA),
            str(V1_SCRIPT.relative_to(ROOT)): sha_path(V1_SCRIPT),
            str(Path(__file__).resolve().relative_to(ROOT)): sha_path(Path(__file__).resolve()),
        },
        "fresh_state_counts": state["state_counts"],
        "counts": counts,
        "validation": validations,
        "scope_boundary": {
            "operative_library": "historical_v7_unified_dispatch_package",
            "deferred_successor_package": "newer_528_group_current_package",
            "token_return_label_or_outcome_mixing_permitted": False,
        },
    }


def report_markdown(report: dict[str, Any]) -> bytes:
    return ("\n".join([
        "# RQ2B V7 fresh two-machine handoff integrity report", "",
        f"Status: `{report['status']}`", "",
        "| Check | Result |", "| --- | --- |",
        *[f"| {name} | {'PASS' if report['validation'][name] else 'FAIL'} |" for name in sorted(report["validation"])], "",
        f"Pending: {report['counts']['pending_assigned']}; machine A: {report['counts']['machine_a']}; machine B: {report['counts']['machine_b']}; finalised locked: {report['counts']['finalised_locked']}.", "",
        "No adequacy outcomes, target joins, retrieval outputs, provider calls, metrics, or thesis results were read or generated.", "",
    ])).encode("utf-8")


def expected_files(state_file: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    base = load_v1_helpers()
    assignments, machine_rows, state = expected_rows(state_file)
    counts = counts_for(assignments, machine_rows, state)
    files = {
        "current_phase5_pending_assignment_v1.jsonl": jsonl_bytes(assignments),
        "machine_a_manifest.jsonl": jsonl_bytes(machine_rows["machine_a"]),
        "machine_b_manifest.jsonl": jsonl_bytes(machine_rows["machine_b"]),
        "reviewer_return_schema.json": pretty_json(read_json(base.V7_SCHEMA)),
        "README.md": readme(state_file, counts).encode("utf-8"),
        "V7_SCOPE_AMENDMENT.md": scope_amendment(counts),
    }
    report = integrity_payload(assignments, machine_rows, state_file, state)
    report["outputs"] = {name: sha_bytes(value) for name, value in files.items()}
    report["integrity_report_sha256"] = canonical_sha(report)
    return files, report


def materialise(state_file: Path, output_dir: Path) -> None:
    if output_dir.exists():
        raise ValueError(f"Refusing to overwrite frozen handoff package: {output_dir}")
    files, report = expected_files(state_file)
    output_dir.mkdir(parents=True)
    for name, value in files.items():
        (output_dir / name).write_bytes(value)
    (output_dir / "integrity_report.json").write_bytes(pretty_json(report))
    (output_dir / "integrity_report.md").write_bytes(report_markdown(report))
    print(json.dumps({"output_dir": str(output_dir), "status": report["status"], "counts": report["counts"]}, sort_keys=True))


def verify(state_file: Path, output_dir: Path) -> None:
    files, regenerated = expected_files(state_file)
    for name, expected in files.items():
        path = output_dir / name
        if not path.is_file() or path.read_bytes() != expected:
            raise ValueError(f"Frozen handoff drift: {path}")
    report_path = output_dir / "integrity_report.json"
    report = read_json(report_path)
    copied = dict(report)
    stored_hash = copied.pop("integrity_report_sha256", None)
    if stored_hash != canonical_sha(copied) or report != regenerated:
        raise ValueError("Integrity report drift")
    expected_md = report_markdown(report)
    if (output_dir / "integrity_report.md").read_bytes() != expected_md:
        raise ValueError("Integrity report Markdown drift")
    print(json.dumps({"output_dir": str(output_dir), "status": "PASS_RQ2B_V7_PHASE5_FRESH_TWO_MACHINE_HANDOFF_REPLAY", "counts": report["counts"]}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("materialise", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--state-file", type=Path, default=DEFAULT_STATE)
        subparser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    state_file = args.state_file.resolve()
    output_dir = args.output_dir.resolve()
    if args.command == "materialise":
        materialise(state_file, output_dir)
    else:
        verify(state_file, output_dir)


if __name__ == "__main__":
    main()
