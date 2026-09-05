#!/usr/bin/env python3
"""Write or verify the local opaque RQ1b v2 input freeze."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rq1b_field_type_confirmatory_v2_opaque_freeze import (
    CONDITION_FREEZE_NAME,
    FREEZE_NAME,
    snapshot,
    verify_freeze,
    verify_opaque_core,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--write-condition-amendment", action="store_true")
    args = parser.parse_args()
    if args.write and args.write_condition_amendment:
        raise ValueError("choose one freeze write mode")
    if args.write_condition_amendment:
        path = args.root / CONDITION_FREEZE_NAME
        if path.exists():
            raise ValueError(f"condition freeze amendment already exists: {path}")
        payload = verify_opaque_core(args.root)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print({"mode": "condition_amendment_written", "selection_packet_count": payload["selection_packet_count"], "residual_packet_count": payload["residual_packet_count"]})
        return
    path = args.root / FREEZE_NAME
    if args.write:
        if path.exists():
            raise ValueError(f"freeze already exists: {path}")
        payload = snapshot(args.root)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print({"mode": "written", "selection_packet_count": payload["selection_packet_count"], "residual_packet_count": payload["residual_packet_count"]})
    else:
        payload = verify_freeze(args.root)
        print({"mode": "verified", "selection_packet_count": payload["selection_packet_count"], "residual_packet_count": payload["residual_packet_count"]})


if __name__ == "__main__":
    main()
