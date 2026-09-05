#!/usr/bin/env python3
"""Freeze and verify the locally regenerated RQ2b v1.2 background overlay."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


VERSION_ID = "rq2b-full-library-v1.2-2026-08-16"
RELATIVE_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
BATCH_COUNT = 18
BATCH_SIZE = 100
EXPECTED_ROWS = BATCH_COUNT * BATCH_SIZE
BANNED = {
    "benchmark_scale_explanation": r"background scale skill used to create realistic retrieval pressure in the benchmark|background scale skill|retrieval pressure",
    "benchmark_gold_label": r"gold-label core benchmark skill|core benchmark skill",
    "benchmark_confusability": r"neighboring confusable skill|neighboring skill",
    "benchmark_artifact_reference": r"expected artifact below",
    "benchmark_switch_rule": r"do not silently switch to a more specific benchmark core skill",
}
OLD_TEMPLATE = r"## Workflow\n\n1\. Read the user request and identify the intended operational goal\.|## Why this skill is distinct"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    version_root = root / RELATIVE_ROOT
    batch_root = version_root / "source_overlay_generation_batches"
    output = version_root / "source_overlay_manifest.json"
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite frozen manifest: {output}")

    batch_paths = [batch_root / f"batch_{index:03d}.json" for index in range(BATCH_COUNT)]
    missing_batches = [path.as_posix() for path in batch_paths if not path.exists()]
    if missing_batches:
        raise ValueError(f"Missing batch manifests: {missing_batches}")

    rows = []
    batch_records = []
    for expected_index, path in enumerate(batch_paths):
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch["version_id"] != VERSION_ID or batch["batch_index"] != expected_index:
            raise ValueError(f"Unexpected batch identity: {path}")
        if len(batch["rows"]) != BATCH_SIZE:
            raise ValueError(f"Unexpected batch row count: {path}")
        if batch["network_calls"] != 0 or batch["external_api_calls"] != 0:
            raise ValueError(f"Non-local activity recorded by {path}")
        if batch["subagent_source_assignment"] or batch["scientific_retrieval_or_reranking"]:
            raise ValueError(f"Out-of-scope activity recorded by {path}")
        batch_records.append({
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256(path),
            "batch_index": expected_index,
            "row_count": len(batch["rows"]),
            "recovered_existing_sources": batch["recovered_existing_sources"],
        })
        rows.extend(batch["rows"])

    expected_indexes = list(range(EXPECTED_ROWS))
    indexes = [row["inventory_index"] for row in rows]
    ids = [row["skill_id"] for row in rows]
    if len(rows) != EXPECTED_ROWS or indexes != expected_indexes or len(ids) != len(set(ids)):
        raise ValueError("The v1.2 overlay inventory is not a complete ordered 1,800-row set")

    lint_counts = {name: 0 for name in [*BANNED, "old_generic_template"]}
    total_bytes = 0
    for row in rows:
        path = root / row["path"]
        if not path.exists():
            raise FileNotFoundError(path)
        content = path.read_text(encoding="utf-8")
        if sha256(path) != row["sha256"] or len(content.encode("utf-8")) != row["utf8_bytes"]:
            raise ValueError(f"Source identity drift: {row['skill_id']}")
        if row["scaffold_lint_failures"]:
            raise ValueError(f"Recorded lint failure: {row['skill_id']}")
        total_bytes += row["utf8_bytes"]
        for name, pattern in BANNED.items():
            lint_counts[name] += int(bool(re.search(pattern, content, flags=re.IGNORECASE)))
        lint_counts["old_generic_template"] += int(bool(re.search(OLD_TEMPLATE, content, flags=re.IGNORECASE)))

    if any(lint_counts.values()):
        raise ValueError(f"Contamination lint failed: {lint_counts}")

    receipt = version_root / "v12_local_source_regeneration_approval_receipt.json"
    manifest = {
        "schema_version": "rq2b-v12-background-source-overlay-manifest-v1",
        "version_id": VERSION_ID,
        "state": "local_source_regeneration_complete_extraction_unauthorised",
        "scope": {
            "source_family": "background_scale",
            "skill_count": EXPECTED_ROWS,
            "source_root": f"{RELATIVE_ROOT}/source_overlay/background_scale",
            "parent_v11_is_immutable": True,
        },
        "approval_receipt": {
            "path": receipt.relative_to(root).as_posix(),
            "sha256": sha256(receipt),
        },
        "generation_batches": batch_records,
        "rows": rows,
        "verification": {
            "ordered_inventory_indices": True,
            "unique_skill_ids": len(set(ids)),
            "unique_source_hashes": len({row["sha256"] for row in rows}),
            "total_utf8_bytes": total_bytes,
            "scaffold_lint_match_counts": lint_counts,
            "network_calls": 0,
            "external_api_calls": 0,
            "subagent_source_assignment": False,
            "scientific_retrieval_or_reranking": False,
        },
        "not_authorised": [
            "source text assignment to subagents",
            "I3C extraction",
            "retrieval, embedding, reranking, or scoring",
            "network, external API, paid model, or hosted compute use",
            "thesis LaTeX or PDF result writing",
        ],
    }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "manifest": output.relative_to(root).as_posix(),
        "sha256": sha256(output),
        "skill_count": EXPECTED_ROWS,
        "total_utf8_bytes": total_bytes,
        "lint_counts": lint_counts,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
