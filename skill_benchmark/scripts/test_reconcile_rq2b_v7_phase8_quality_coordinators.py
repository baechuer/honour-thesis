#!/usr/bin/env python3
"""Focused fail-closed tests for Phase-8 coordinator-return validation."""
from __future__ import annotations

import copy

from reconcile_rq2b_v7_phase8_quality_coordinators import validate_return


ASSIGNMENT = {
    "packet_id": "Q8-CUE-0001",
    "packet_sha256": "a" * 64,
    "gate": "cue",
    "allowed_decisions": ["AVOIDABLE_IDENTITY_CUE", "NECESSARY_TASK_CONDITION", "BLOCKED_OR_UNCLEAR"],
}
VALID = {
    "schema_version": "rq2b-v7-phase8-quality-coordinator-return-v1",
    "packet_id": "Q8-CUE-0001",
    "packet_sha256": "a" * 64,
    "gate": "cue",
    "decision": "NECESSARY_TASK_CONDITION",
    "source_anchors": ["visible exact anchor"],
    "rationale": "The phrase states a necessary user-side condition.",
}


def rejects(mutation) -> None:
    returned = copy.deepcopy(VALID)
    mutation(returned)
    try:
        validate_return(ASSIGNMENT, returned)
    except ValueError:
        return
    raise AssertionError("invalid coordinator return was accepted")


def main() -> None:
    validate_return(ASSIGNMENT, VALID)
    rejects(lambda row: row.update(packet_sha256="b" * 64))
    rejects(lambda row: row.update(decision="NOT_AN_ALLOWED_DECISION"))
    rejects(lambda row: row.update(source_anchors=[]))
    rejects(lambda row: row.update(rationale=""))
    rejects(lambda row: row.update(extra="drift"))
    print("PASS: 7 coordinator-return validation checks")


if __name__ == "__main__":
    main()
