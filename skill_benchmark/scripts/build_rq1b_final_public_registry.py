#!/usr/bin/env python3
"""Build the non-pooled final registry for RQ1b public-skill evidence.

The historical cross-source C6 corpus, the V2 field-card ablation, and the
later V3 source-frame curation have different units and gates.  This script
creates one provenance registry while keeping those strata separate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
V2 = REPO / "skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28"
V3 = REPO / "skill_benchmark/rq1b_v3_public_source_frame"
LEGACY_MAP = V3 / "legacy_c6_mapping_2026-08-29/legacy_c6_to_v3_source_frame_mapping.json"
DEFAULT_OUT = REPO / "skill_benchmark/rq1b_final_public_corpus_v1"
V2_V3_EXTENSION = DEFAULT_OUT / "v2_v3_complete_triad_extension_2026-08-30"
FINAL_SCORED_SUMMARY = (
    REPO
    / "skill_benchmark/rq1b_cross_source_public_benchmark/outputs"
    / "field_type_ablation_confirmatory_v2_v3_final_2026-08-30/summary.json"
)

V3_C6_FILES = (
    V3 / "c4b_blind_review_wave_001_v2_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
    V3 / "c4b_blind_review_wave_029_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
    V3 / "d1_directed_discovery_wave_032_2026-08-30/c6_strict_freeze_wave_032_2026-08-30/c6_frozen_strict_cases.jsonl",
    V3 / "d1_directed_discovery_wave_033_2026-08-30/c6_strict_freeze_wave_033_2026-08-30/c6_frozen_strict_cases.jsonl",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def signature(hashes: list[str]) -> str:
    return "|".join(sorted(hashes))


def registry_id(sig: str) -> str:
    return "RQ1B-U-" + sha256_bytes(sig.encode("ascii"))[:16]


def file_digest(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def source_hashes(values: list[Any]) -> list[str]:
    """Normalise the two C6 source-hash encodings used by the frozen ledgers."""
    hashes = []
    for value in values:
        if isinstance(value, str):
            hashes.append(value)
        elif isinstance(value, dict):
            digest = value.get("source_sha256") or value.get("sha256")
            if not digest:
                raise ValueError("V3 C6 candidate entry has no source SHA-256.")
            hashes.append(digest)
        else:
            raise ValueError("Unexpected V3 C6 candidate-source encoding.")
    return sorted(hashes)


def build() -> tuple[dict[str, str], dict[str, Any]]:
    legacy = read_json(LEGACY_MAP)
    legacy_compositions = legacy["compositions"]
    if len(legacy_compositions) != 76 or legacy["legacy_primary_packet_rows"] != 408:
        raise ValueError("Legacy C6 mapping no longer matches its frozen 76-composition / 408-row contract.")

    v2_compositions = read_json(V2 / "composition_manifest_private.json")
    v2_by_id = {row["composition_id"]: row for row in v2_compositions}
    active_v2 = read_json(V2 / "condition_materialisation_freeze_amendment_2026-08-29.json")[
        "canonical_card_file_sha256"
    ]
    if len(v2_compositions) != 74 or len(active_v2) != 48:
        raise ValueError("V2 source or active-card count no longer matches the frozen contract.")
    if not set(active_v2).issubset(v2_by_id):
        raise ValueError("V2 condition freeze refers to an unknown candidate composition.")

    v2_families = read_json(V2 / "routing_family_manifest_private.json")

    extension = read_json(V2_V3_EXTENSION / "combined_matrix_manifest.json")
    extension_audit = read_json(V2_V3_EXTENSION / "compatibility_audit.json")
    final_scored = read_json(FINAL_SCORED_SUMMARY)
    if extension.get("status") != "RQ1B_V2_PLUS_V3_HARMONISED_FUTURE_SELECTOR_MANIFEST_NOT_A_RESULT":
        raise ValueError("V2+V3 extension is missing its frozen future-matrix manifest.")
    if extension_audit.get("status") != "RQ1B_V2_PLUS_V3_COMPLETE_TRIAD_COMPATIBILITY_AUDIT_PASS_NOT_A_SELECTOR_RESULT":
        raise ValueError("V2+V3 extension compatibility audit is not a pass.")
    extension_rows = read_json(V2_V3_EXTENSION / "extension_composition_manifest_private.json")["rows"]
    if len(extension_rows) != 4:
        raise ValueError("V2+V3 extension composition count drift.")
    final_matrix = final_scored.get("matrix", {})
    if (
        final_scored.get("analysis_unit")
        != "one frozen 46-scored-composition / 99-family / 198-prompt experiment drawn from 52 frozen composition artifacts; field effects use composition-level paired bootstrap"
        or final_matrix.get("scored_compositions") != 46
        or final_matrix.get("families") != 99
        or final_matrix.get("prompts") != 198
        or final_matrix.get("frozen_composition_artifacts") != 52
    ):
        raise ValueError("The sealed V2+V3 final-result denominator no longer matches 46 / 99 / 198 from 52 artifacts.")
    extension_by_source = {row["source_composition_id"]: row for row in extension_rows}
    if len(extension_by_source) != 4:
        raise ValueError("V2+V3 extension source composition IDs are not unique.")
    preservation: dict[str, dict[str, Any]] = {}
    for path in sorted((V2 / "preservation_ledger").glob("CFTF-*.json")):
        row = read_json(path)
        preservation[row["routing_family_id"]] = row
    # One family is deliberately retained as a response-format hold and has no
    # preservation ledger record. It remains in the routing manifest.
    active_v2_families = [
        family for family in v2_families if family["composition_id"] in active_v2
    ]
    if len(active_v2_families) != 128 or len(preservation) != 127:
        raise ValueError("V2 routing-family or preservation ledger is incomplete.")

    statuses = Counter(
        "pass" if row["strict_singleton_preserved"] else "fail"
        for row in preservation.values()
    )
    holds = len(active_v2_families) - len(preservation)
    # The hold is represented by an unmaterialised family in the routing manifest.
    if statuses["pass"] != 87 or statuses["fail"] != 40 or holds != 1:
        raise ValueError(
            "V2 preservation status does not match the frozen 87 pass / 40 fail / 1 hold contract."
        )

    family_by_composition: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for family in active_v2_families:
        family_by_composition[family["composition_id"]].append(family)

    v3_rows: list[tuple[Path, dict[str, Any]]] = []
    for path in V3_C6_FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        v3_rows.extend((path, row) for row in read_jsonl(path))
    v3_by_composition: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    for path, row in v3_rows:
        v3_by_composition[row["composition_id"]].append((path, row))
    if len(v3_rows) != 32 or len(v3_by_composition) != 6:
        raise ValueError("Direct V3 C6 evidence is no longer 32 cases across six parent compositions.")

    entries: dict[str, dict[str, Any]] = {}

    def get_entry(hashes: list[str]) -> dict[str, Any]:
        sig = signature(hashes)
        entry = entries.get(sig)
        if entry is None:
            entry = {
                "registry_id": registry_id(sig),
                "candidate_source_sha256": sorted(hashes),
                "candidate_count": len(hashes),
                "strata": {},
                "pooling_rule": "Do not pool metrics across strata. Use only a stratum whose inputs and gates match the claimed analysis.",
            }
            entries[sig] = entry
        return entry

    for row in legacy_compositions:
        entry = get_entry(row["candidate_source_sha256"])
        entry["strata"]["historical_cross_source_c6"] = {
            "legacy_composition_index": row["legacy_composition_index"],
            "strict_prompt_case_count": row["legacy_packet_count"],
            "proposal_ids": row["legacy_proposal_ids"],
            "mapped_to_v3_source_frame": row["fully_mapped_to_v3_source_frame"],
            "role": "historical_source_and_curation_provenance",
        }

    for composition_id in sorted(active_v2):
        source_row = v2_by_id[composition_id]
        hashes = [candidate["source_sha256"] for candidate in source_row["private_candidates"]]
        entry = get_entry(hashes)
        families = family_by_composition[composition_id]
        preserved = sum(
            1
            for family in families
            if family["routing_family_id"] in preservation
            and preservation[family["routing_family_id"]]["strict_singleton_preserved"]
        )
        failed = sum(
            1
            for family in families
            if family["routing_family_id"] in preservation
            and not preservation[family["routing_family_id"]]["strict_singleton_preserved"]
        )
        held = len(families) - preserved - failed
        entry["strata"]["v2_field_card_ablation"] = {
            "composition_id": composition_id,
            "canonical_card_sha256": active_v2[composition_id],
            "routing_families_materialised": len(families),
            "strict_preserved_routing_families": preserved,
            "failed_full_card_preservation_families": failed,
            "held_full_card_preservation_families": held,
            "role": "scored_field_type_availability_ablation",
        }

    for composition_id, rows in sorted(v3_by_composition.items()):
        first = rows[0][1]
        hashes = source_hashes(first["candidate_source_hashes"])
        entry = get_entry(hashes)
        variants = sorted({row.get("prompt_variant", row.get("variant")) for _, row in rows})
        expected = len(hashes) * len(variants)
        entry["strata"]["v3_direct_c6_curation"] = {
            "composition_id": composition_id,
            "strict_prompt_case_count": len(rows),
            "prompt_variants_present": variants,
            "expected_complete_case_count": expected,
            "coverage_status": "complete" if len(rows) == expected else "partial",
            "c6_files": sorted({relative(path) for path, _ in rows}),
            "role": "fresh_source_frame_curation_only",
        }
        imported = extension_by_source.get(composition_id)
        if imported is not None:
            if hashes != sorted(imported["candidate_source_sha256"]):
                raise ValueError("V2+V3 extension candidate hashes do not match direct V3 C6.")
            entry["strata"]["v2_v3_complete_triad_extension"] = {
                "extension_composition_id": imported["composition_id"],
                "source_composition_id": composition_id,
                "strict_routing_family_count": 3,
                "strict_prompt_count": 6,
                "role": "imported_v3_component_of_completed_v2_v3_public_card_result",
            }

    ordered_entries = sorted(entries.values(), key=lambda row: row["registry_id"])
    v3_complete = sum(
        1
        for entry in ordered_entries
        if entry["strata"].get("v3_direct_c6_curation", {}).get("coverage_status") == "complete"
    )
    v3_partial = sum(
        1
        for entry in ordered_entries
        if entry["strata"].get("v3_direct_c6_curation", {}).get("coverage_status") == "partial"
    )
    v2_scored_families = sum(
        item["strict_preserved_routing_families"]
        for entry in ordered_entries
        for item in [entry["strata"].get("v2_field_card_ablation")]
        if item
    )

    summary = {
        "status": "RQ1B_FINAL_PUBLIC_REGISTRY_V1_PASS_CONSOLIDATED_SOURCE_FRAME",
        "claim_boundary": [
            "This is the canonical 82-composition source registry; it is not itself an 82-composition selector denominator.",
            "The completed RQ1b public-card result is exactly 46 scored compositions / 99 routing families / 198 prompts, drawn from 52 frozen artifacts.",
            "The historical native-V2 87-family / 174-prompt subset is provenance and reuse accounting, not a competing corpus version.",
            "Direct V3 C6 records are fresh strict-candidate curation evidence only; no V3 selector or field-effect metric is created.",
            "Four complete V3 triads were imported into the completed V2+V3 public-card result; the two partial V3 compositions remain outside the complete-case result.",
        ],
        "historical_accounting_correction": {
            "superseded_declared_v3_total": "37 compositions / 231 strict cases",
            "finding": "That total inherited the earlier cross-source 34 / 213 curation count and added later wave increments. It is not reproducible from V3 C6 freeze files.",
            "direct_v3_c6_recomputed_total": "6 parent compositions / 32 strict prompt cases",
            "direct_v3_complete_compositions": v3_complete,
            "direct_v3_partial_compositions": v3_partial,
        },
        "strata": {
            "historical_cross_source_c6": {
                "candidate_compositions": len(legacy_compositions),
                "strict_prompt_cases": legacy["legacy_primary_packet_rows"],
                "candidate_cardinality": legacy["composition_cardinality"],
                "role": "historical source and curation provenance",
            },
            "v2_field_card_ablation": {
                "source_candidate_compositions_before_card_eligibility": len(v2_compositions),
                "active_canonical_card_compositions": len(active_v2),
                "routing_families_materialised": len(active_v2_families),
                "strict_preserved_routing_families_scored": v2_scored_families,
                "scored_prompt_variants": v2_scored_families * 2,
                "role": "historical native-V2 component of the completed V2+V3 public-card result",
            },
            "v3_direct_c6_curation": {
                "parent_compositions_with_direct_c6_cases": len(v3_by_composition),
                "strict_prompt_cases": len(v3_rows),
                "complete_compositions": v3_complete,
                "partial_compositions": v3_partial,
                "role": "fresh V3 source-frame strict curation only",
            },
            "v2_v3_complete_triad_extension": {
                "imported_complete_v3_compositions": extension["imported_v3_complete_triads"]["candidate_compositions"],
                "imported_strict_routing_families": extension["imported_v3_complete_triads"]["strict_preserved_routing_families"],
                "imported_strict_prompts": extension["imported_v3_complete_triads"]["strict_prompts"],
                "frozen_artifacts_before_terminal_eligibility": final_matrix["frozen_composition_artifacts"],
                "final_scored_compositions": final_matrix["scored_compositions"],
                "final_scored_families": final_matrix["families"],
                "final_scored_prompts": final_matrix["prompts"],
                "role": "completed V2+V3 public-card result; retain native/imported provenance tags",
            },
            "unified_provenance_union": {
                "unique_candidate_compositions": len(ordered_entries),
                "note": "V2 is entirely contained in the historical 76-composition source set. The six direct V3 C6 compositions are separately represented by their source-hash signatures.",
            },
        },
        "input_file_sha256": {
            relative(LEGACY_MAP): file_digest(LEGACY_MAP),
            relative(V2 / "composition_manifest_private.json"): file_digest(V2 / "composition_manifest_private.json"),
            relative(V2 / "condition_materialisation_freeze_amendment_2026-08-29.json"): file_digest(V2 / "condition_materialisation_freeze_amendment_2026-08-29.json"),
            relative(V2 / "routing_family_manifest_private.json"): file_digest(V2 / "routing_family_manifest_private.json"),
            relative(V2_V3_EXTENSION / "combined_matrix_manifest.json"): file_digest(V2_V3_EXTENSION / "combined_matrix_manifest.json"),
            relative(V2_V3_EXTENSION / "compatibility_audit.json"): file_digest(V2_V3_EXTENSION / "compatibility_audit.json"),
            relative(FINAL_SCORED_SUMMARY): file_digest(FINAL_SCORED_SUMMARY),
            **{relative(path): file_digest(path) for path in V3_C6_FILES},
        },
    }

    jsonl = "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in ordered_entries)
    summary_text = json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    readme = """# RQ1b Final Public Corpus Registry v1

## Consolidated Default

This is the one canonical source-composition frame for later public RQ1 work:
**82 unique candidate compositions**, formed by deduplicating the 76 historical
cross-source C6 compositions with six direct-V3 C6 additions. Future cluster
work must resolve proposed candidates against this registry first, then run one
fixed eligibility audit and freeze a complete-case scoring subset before a
selector runs. New compositions belong only in a new registry release, never
as an unannounced addition to an existing result.

`82` is therefore a source-registry count, not a selector-result denominator.
The completed RQ1b public-card field-removal result is exactly **46 scored
compositions / 99 strict routing families / 198 prompts**, drawn from 52 frozen
composition artifacts. `87 / 174` denotes the historical native-V2 subset and
is not a competing corpus version.

This directory is the canonical, *stratified* inventory for the public-skill
evidence used by RQ1b. It prevents version counts from being added together as
though every candidate composition had passed the same protocol and been
scored by the same selector.

## What Is Included

| Stratum | Unit | Evidence role | May be pooled with another stratum? |
| --- | ---: | --- | --- |
| Historical cross-source C6 | Candidate composition | Historical public-source and strict-curation provenance | No |
| V2 field-card ablation | Candidate composition / routing family | Historical native-V2 component of the completed V2+V3 result | Only through the sealed V2+V3 result. |
| Direct V3 C6 | Candidate composition / prompt case | Fresh source-frame strict curation, with partial coverage retained explicitly | No |
| V2+V3 complete-triad extension | Candidate composition / routing family | Four complete V3 triads imported into the completed public-card result | Only through the sealed 46/99/198 result. |

`composition_registry.jsonl` uses the sorted candidate-source SHA-256 list as
the composition identity. A record can therefore show whether the same public
candidate set belongs to multiple strata, without silently duplicating it.

## Counting Rule

Use the count printed for the relevant stratum. Do not report the union as a
single selector benchmark size. The union is a provenance inventory; it is not
a common scored population.

The historical `37 compositions / 231 strict cases` V3 statement is
superseded: it cannot be reconstructed from direct V3 C6 files. The registry
records the direct, reproducible V3 C6 total instead and retains all prior
files unchanged for audit.

The `v2_v3_complete_triad_extension_2026-08-30/` child directory imports only
the four V3 parents with complete strict triad coverage. It provides the same
`FULL + seven all-candidate masks` format as V2, adding 12 strict routing
families and 24 prompts. The sealed combined analysis contains 52 frozen
composition artifacts, of which 46 contribute valid paired
composition-bootstrap units over 99 families and 198 prompts. The two partial
V3 parents remain outside that complete-case result.

## Rebuild And Verify

```zsh
python3 skill_benchmark/scripts/build_rq1b_final_public_registry.py --write
python3 skill_benchmark/scripts/build_rq1b_final_public_registry.py --check
```
"""
    report = f"""# RQ1b Final Registry Integrity Report

Status: `{summary['status']}`

## Reconciled Counts

| Evidence stratum | Recomputed count | Interpretation |
| --- | ---: | --- |
| Historical cross-source C6 | 76 compositions / 408 strict prompt cases | Historical provenance and curation line. |
| V2 active field cards | 48 compositions / 128 routing families | Historical native-V2 component: 87 strict-preserved families / 174 prompts. |
| Direct V3 C6 | 6 compositions / 32 strict prompt cases | 4 complete compositions and 2 partial compositions; curation only. |
| V2+V3 complete-triad extension | 4 compositions / 12 routing families / 24 prompts | Imported V3 component of the completed result. |
| Completed public-card result | 46 scored compositions / 99 routing families / 198 prompts | Drawn from 52 frozen artifacts after terminal paired-coverage eligibility. |
| Unified source-hash union | {len(ordered_entries)} compositions | Provenance inventory only, never a pooled retrieval denominator. |

## Correction

The direct V3 C6 file audit finds 32 strict prompt cases across six parent
compositions. Earlier `37 / 231` V3 prose is retained as historical record but
is not a reproducible V3 C6 count and is superseded by this registry.

## Guardrails

- Do not treat the 82-source union as a claim of 82 independent scored tasks.
- Use the completed 46/99/198 matrix for current public-card results; retain
  native and imported provenance tags when inspecting it.
- Do not count V2.1 separately: it is a subset amendment of V2.
- Keep the two partial V3 compositions out of a future complete-composition
  selector denominator unless a new frozen protocol explicitly permits
  case-level analysis.
"""
    return {
        "composition_registry.jsonl": jsonl,
        "summary.json": summary_text,
        "README.md": readme,
        "INTEGRITY_REPORT.md": report,
    }, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        parser.error("choose exactly one of --write or --check")

    expected, summary = build()
    out = args.out.resolve()
    if args.check:
        missing = [name for name in expected if not (out / name).exists()]
        mismatched = [
            name
            for name, text in expected.items()
            if (out / name).exists() and (out / name).read_text(encoding="utf-8") != text
        ]
        if missing or mismatched:
            raise SystemExit(
                "RQ1b final registry check failed: "
                + json.dumps({"missing": missing, "mismatched": mismatched}, sort_keys=True)
            )
        print(json.dumps({"status": summary["status"], "out": str(out), "check": "PASS"}, sort_keys=True))
        return

    staging = out.with_name(out.name + ".tmp")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for name, text in expected.items():
        (staging / name).write_text(text, encoding="utf-8")
    # The extension is immutable experiment input under the registry root.
    # Copy it before replacing the parent directory so a root rebuild cannot
    # silently erase its condition materials or quarantine ledger.
    if not V2_V3_EXTENSION.is_dir():
        raise FileNotFoundError(V2_V3_EXTENSION)
    shutil.copytree(V2_V3_EXTENSION, staging / V2_V3_EXTENSION.name)
    if out.exists():
        shutil.rmtree(out)
    staging.rename(out)
    print(json.dumps({"status": summary["status"], "out": str(out), "write": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
