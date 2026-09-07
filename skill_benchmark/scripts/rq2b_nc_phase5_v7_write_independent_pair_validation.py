#!/usr/bin/env python3
"""Materialise a target-blind V7 Machine-B pair-validation checkpoint.

This utility intentionally validates only the mechanical/rubric validity of two
independent raw reviewer returns.  It cannot and does not reconcile reviews,
join opaque tokens to targets, or derive an acceptable set.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from collections import Counter
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
PROTOCOL = (
    WORKSPACE
    / "skill_benchmark/scripts/rq2b_nc_phase4_v5_strict_unified_blind_protocol_2026_09_05.py"
)
RAW_ROOT = (
    "skill_benchmark/rq2b_naturalistic_confusability/review/"
    "RQ2B-NC-phase4-v7-strict-unified-independent-returns-2026-09-05"
)
BOUNDARY = (
    "No reconciliation coordinator packet, final disposition, opaque target join, "
    "acceptable set, main-tail designation, retrieval claim, or library claim is "
    "materialised here. The recorded coordinator-context gate remains open."
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_alternate(spec: str) -> tuple[str, str, Path]:
    try:
        lane, batch_id, relative_path = spec.split(":", 2)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "alternate must be LANE:BATCH_ID:REPO_RELATIVE_PATH"
        ) from exc
    if lane not in {"A", "B"}:
        raise argparse.ArgumentTypeError("alternate lane must be A or B")
    return lane, batch_id, WORKSPACE / relative_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--microbatch", type=int, required=True)
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--batch-id", action="append", required=True)
    parser.add_argument(
        "--alternate",
        action="append",
        type=parse_alternate,
        default=[],
        help="validated reissue path; original raw return is retained elsewhere",
    )
    args = parser.parse_args()
    batch_ids = args.batch_id
    if len(batch_ids) != 12 or len(set(batch_ids)) != 12:
        raise SystemExit("a Machine-B microbatch must contain exactly 12 distinct groups")

    destination = (
        WORKSPACE
        / "skill_benchmark/rq2b_naturalistic_confusability/review"
        / f"RQ2B-NC-phase5-v7-machine-b-microbatch-{args.microbatch:03d}-"
        f"independent-pair-validation-2026-09-07-v{args.version}"
    )
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing checkpoint: {destination}")

    protocol = runpy.run_path(str(PROTOCOL))
    globals_ = protocol["load_validated_return"].__globals__
    execution = globals_["verify_execution"]()
    audit = globals_["verify_audit"]()
    globals_["verify_execution"] = lambda: execution
    globals_["verify_audit"] = lambda: audit
    expected_packet = globals_["expected_packet"]
    load_validated_return = protocol["load_validated_return"]

    alternates = {(lane, batch): path for lane, batch, path in args.alternate}
    if any(batch not in batch_ids for _, batch in alternates):
        raise SystemExit("an alternate return is outside this microbatch")

    lanes: dict[str, object] = {}
    for lane in ("A", "B"):
        records = []
        counts: Counter[str] = Counter()
        for batch_id in batch_ids:
            _, packet = expected_packet(batch_id)
            if len(packet["candidates"]) != 8:
                raise RuntimeError(f"{batch_id} does not retain 6 main plus 2 tail candidates")
            alternate_path = alternates.get((lane, batch_id))
            _, returned, validated_path = load_validated_return(
                batch_id, lane, alternate_path
            )
            if len(returned["assessments"]) != 8:
                raise RuntimeError(f"{batch_id}/{lane} does not contain eight assessments")
            counts.update(item["adequacy"] for item in returned["assessments"])
            record = {
                "batch_id": batch_id,
                "raw_return_path": str(validated_path.relative_to(WORKSPACE)),
                "reviewer_output_sha256": returned["reviewer_output_sha256"],
            }
            if alternate_path is not None:
                record["return_role"] = "TRACEABLE_REISSUE_VALIDATED_AS_ALTERNATE"
                record["canonical_raw_return_retained"] = (
                    f"{RAW_ROOT}/reviewer_{lane}/{batch_id}.json"
                )
            else:
                record["return_role"] = "CANONICAL_RAW_RETURN"
            records.append(record)
        lanes[lane] = {
            "validated_return_count": len(records),
            "assessment_counts": dict(sorted(counts.items())),
            "returns": records,
        }

    summary = {
        "schema_version": (
            f"rq2b_nc_phase5_v7_machine_b_microbatch_{args.microbatch:03d}_"
            "independent_pair_validation_v1"
        ),
        "scope": "Machine B V7 target-blind independent return collection only.",
        "status": "PASS_V7_TWO_INDEPENDENT_RAW_RETURNS_COLLECTED_PENDING_METHOD_GATE",
        "batch_ids": batch_ids,
        "bound_inputs": {
            "protocol_sha256": sha256_file(PROTOCOL),
            "execution_status": execution["status"],
            "audit_status": audit[0]["status"],
            "candidate_packet_rule": "each group validated as 6 main plus 2 tail candidates",
        },
        "lanes": lanes,
        "reissue_count": len(alternates),
        "closure_boundary": BOUNDARY,
    }
    destination.mkdir(parents=True)
    (destination / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (destination / "README.md").write_text(
        "# V7 Machine B independent-pair validation\n\n"
        "This checkpoint validates complete target-blind raw-return pairs only. "
        "It records no reconciliation or library outcome because the coordinator-context "
        "method gate remains open.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
