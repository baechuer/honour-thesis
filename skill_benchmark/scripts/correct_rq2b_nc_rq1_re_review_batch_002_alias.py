#!/usr/bin/env python3
"""Materialize the one disclosed clerical correction to batch-002 results."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
ORIGINAL_RESULTS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_2026-08-31.jsonl"
PACKETS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_packets_2026-08-31.jsonl"
CORRECTED_RESULTS = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_clerical_corrected_2026-08-31.jsonl"
CORRECTION_RECORD = BASE / "review/rq1_frozen_cluster_reauthored_batch_002_rewrite_target_blinded_results_clerical_correction_2026-08-31.json"
PROMPT_ID = "RQ2B-NC-RQ1-REAUTH-B002-R1-030-02"
WATERMARK_SHA256 = "409bcb57b4543b8044d85144b87336a1b49e464c6e0ba331df5298aa409a6af3"
CONVERTER_SHA256 = "3a5c1e57ee1dbf516b9e64c259bf07f7630a6a1acfe844ae670019ebf21288f9"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    original_lines = ORIGINAL_RESULTS.read_text(encoding="utf-8").splitlines()
    packet_rows = [json.loads(line) for line in PACKETS.read_text(encoding="utf-8").splitlines() if line.strip()]
    packet = next((row for row in packet_rows if row["prompt_id"] == PROMPT_ID), None)
    if packet is None:
        raise SystemExit(f"Correction packet is absent: {PROMPT_ID}")
    packet_aliases = {row["alias"]: row["source_sha256"] for row in packet["candidates"]}
    if packet_aliases != {"A": WATERMARK_SHA256, "B": CONVERTER_SHA256}:
        raise SystemExit("Packet aliases do not establish the disclosed watermark/converter mapping")

    corrected_lines: list[str] = []
    before: list[dict[str, str]] | None = None
    after: list[dict[str, str]] | None = None
    changed = 0
    for line in original_lines:
        row = json.loads(line)
        if row["prompt_id"] != PROMPT_ID:
            corrected_lines.append(line)
            continue
        before = [{"alias": candidate["alias"], "classification": candidate["classification"]} for candidate in row["candidates"]]
        for candidate in row["candidates"]:
            if candidate["alias"] == "A":
                candidate["classification"] = "fully_adequate"
            elif candidate["alias"] == "B":
                candidate["classification"] = "inadequate"
            else:
                raise SystemExit("Correction target has an unexpected candidate alias")
        after = [{"alias": candidate["alias"], "classification": candidate["classification"]} for candidate in row["candidates"]]
        corrected_lines.append(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
        changed += 1
    if changed != 1 or before is None or after is None:
        raise SystemExit("Expected exactly one target result row")
    if before != [{"alias": "A", "classification": "inadequate"}, {"alias": "B", "classification": "fully_adequate"}]:
        raise SystemExit("Original classifications do not match the disclosed clerical error")
    if after != [{"alias": "A", "classification": "fully_adequate"}, {"alias": "B", "classification": "inadequate"}]:
        raise SystemExit("Corrected classifications do not match the packet source mapping")

    CORRECTED_RESULTS.write_text("\n".join(corrected_lines) + "\n", encoding="utf-8")
    correction = {
        "correction_id": "RQ2B-NC-RQ1-B002-CLERICAL-ALIAS-030-02",
        "status": "DISCLOSED_CLERICAL_CORRECTION_NOT_A_SCIENTIFIC_REVIEW_REVISION",
        "prompt_id": PROMPT_ID,
        "original_results_path": str(ORIGINAL_RESULTS.relative_to(ROOT)),
        "original_results_sha256": sha256_file(ORIGINAL_RESULTS),
        "packet_path": str(PACKETS.relative_to(ROOT)),
        "packet_sha256": sha256_file(PACKETS),
        "corrected_results_path": str(CORRECTED_RESULTS.relative_to(ROOT)),
        "corrected_results_sha256": sha256_file(CORRECTED_RESULTS),
        "packet_alias_to_source_sha256": packet_aliases,
        "classification_before": before,
        "classification_after": after,
        "evidence": [
            "The packet explicitly binds alias A to the watermark source and alias B to the PDF-converter source.",
            "The unchanged rationale for the fully adequate classification describes visible watermarks plus page-overlay operations, which are the watermark source capabilities.",
            "The unchanged rationale for the inadequate classification describes missing watermark/header/footer/page-number overlay operations, which is the converter source limitation.",
        ],
        "no_scientific_judgment_drift": {
            "assertion": "Only the two candidate alias classifications are swapped to restore the packet-established source binding; no rationale, prompt, source roster, source hash, adequacy rationale, cue assessment, relationship assessment, or other result row changes.",
            "unchanged_other_result_rows": len(original_lines) - changed,
            "unchanged_prompt_source_roster_rationales": True,
        },
    }
    CORRECTION_RECORD.write_text(json.dumps(correction, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(correction, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
