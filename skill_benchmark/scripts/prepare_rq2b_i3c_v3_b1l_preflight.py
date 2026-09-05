#!/usr/bin/env python3
"""Freeze the local-only V3 B1L BM25 inputs without ranking any prompt.

This is deliberately a preparation gate, not a retrieval run.  It binds the
strict v1.1 prompt endpoint to the final V3 I3C artefacts, reconstructs local
I1/I2 from the same source manifest, and emits a text-free approval packet for
the later BM25 execution.  No index is built and no query is ranked here.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from rq2b_common import (
    read_json,
    read_jsonl,
    relative,
    repo_root,
    require,
    selector_counts,
    serialize_i1,
    sha256_file,
    sha256_text,
    write_json_new,
    write_jsonl_new,
)
from rq2b_v11_contract import RELATIVE_ROOT as V11_ROOT
from rq2b_v11_contract import verify as verify_v11_contract
from verify_rq2b_i3c_v3_automatic_freeze import (
    FINAL_MANIFEST,
    FREEZE_ROOT,
    SOURCE_MANIFEST,
    VERSION_ID,
    verify_full as verify_v3_automatic_integrity,
)


PREFLIGHT_VERSION = "rq2b-i3c-v3-b1l-preflight-v3"
PREFLIGHT_ROOT = f"skill_benchmark/rq2b_full_library/{VERSION_ID}/b1l_preflight_v3"
FREEZE_CHECKPOINT = f"{FREEZE_ROOT}/automatic_integrity_freeze_checkpoint.json"
STRICT_PROMPT_SCHEMA = "rq2b-i3c-v3-strict-scored-prompt-v3"
REPRESENTATION_SCHEMA = "rq2b-representation-row-v1"
REPRESENTATION_SERIALIZER = "rq2b-i3c-v3-b1l-preflight-serializer-v3"
REPRESENTATIONS = (
    "i1-discovery",
    "i2-original",
    "i3c-fielded-evidence",
    "i3-flat-evidence",
)
STRICT_PROMPT_KEYS = {
    "schema_version",
    "prompt_id",
    "prompt",
    "prompt_sha256",
    "stratum",
    "group",
    "gold_skill",
}
EXECUTION_PACKET_NAME = "b1l_execution_approval_packet.json"
PREFLIGHT_REPORT_NAME = "b1l_preflight_report.json"
PREFLIGHT_CHECKPOINT_NAME = "b1l_preflight_checkpoint.json"
RUNNER_PATH = "skill_benchmark/scripts/run_rq2b_i3c_v3_b1l_bm25.py"


def strict_jsonl(path: Path) -> list[dict[str, Any]]:
    raw = path.read_text(encoding="utf-8")
    require(raw.endswith("\n"), f"JSONL must end with newline: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        require(bool(line.strip()), f"blank JSONL line {line_number}: {path}")
        parsed = json.loads(line)
        require(isinstance(parsed, dict), f"non-object JSONL line {line_number}: {path}")
        rows.append(parsed)
    return rows


def representation_row(source: dict[str, Any], representation: str, selector_text: str) -> dict[str, Any]:
    return {
        "schema_version": REPRESENTATION_SCHEMA,
        "serializer_version": REPRESENTATION_SERIALIZER,
        "representation": representation,
        "source_row_index": source["source_row_index"],
        "skill_id": source["skill_id"],
        "family": source["family"],
        "source_policy": source["source_policy"],
        "source_path": source["source_path"],
        "source_sha256": source["source_sha256"],
        "source_name_sha256": source["source_name_sha256"],
        "source_description_sha256": source["source_description_sha256"],
        "selector_text": selector_text,
        "selector_text_sha256": sha256_text(selector_text),
        "selector_visible_counts": selector_counts(selector_text),
    }


def validate_representation_rows(
    *,
    root: Path,
    sources: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    representation: str,
    require_exact_source: bool,
    require_v3_evidence_alignment: bool,
) -> dict[str, int]:
    require(len(sources) == len(rows) == 2433, f"{representation} row count mismatch")
    seen_ids: set[str] = set()
    total_counts = Counter()
    for source, row in zip(sources, rows, strict=True):
        skill_id = source["skill_id"]
        require(row.get("schema_version") == REPRESENTATION_SCHEMA, f"{representation} schema mismatch: {skill_id}")
        require(row.get("representation") == representation, f"{representation} label mismatch: {skill_id}")
        require(row.get("source_row_index") == source["source_row_index"], f"{representation} row index mismatch: {skill_id}")
        require(row.get("skill_id") == skill_id, f"{representation} skill ID mismatch: {skill_id}")
        require(skill_id not in seen_ids, f"{representation} duplicate skill ID: {skill_id}")
        seen_ids.add(skill_id)
        for key in ("family", "source_path", "source_sha256"):
            require(row.get(key) == source[key], f"{representation} source identity mismatch: {skill_id}:{key}")
        if representation in {"i1-discovery", "i2-original"}:
            require(row.get("source_policy") == source["source_policy"], f"{representation} source policy mismatch: {skill_id}")
        selector_text = row.get("selector_text")
        require(isinstance(selector_text, str) and bool(selector_text), f"{representation} selector text missing: {skill_id}")
        require(row.get("selector_text_sha256") == sha256_text(selector_text), f"{representation} selector hash mismatch: {skill_id}")
        expected_counts = selector_counts(selector_text)
        require(row.get("selector_visible_counts") == expected_counts, f"{representation} selector counts mismatch: {skill_id}")
        total_counts.update(expected_counts)
        expected_i1 = serialize_i1(source["source_name"], source["source_description"])
        if representation == "i1-discovery":
            require(row.get("serializer_version") == REPRESENTATION_SERIALIZER, f"I1 serializer mismatch: {skill_id}")
            require(selector_text == expected_i1, f"I1 serialization mismatch: {skill_id}")
        elif representation == "i2-original":
            require(row.get("serializer_version") == REPRESENTATION_SERIALIZER, f"I2 serializer mismatch: {skill_id}")
            source_bytes = (root / source["source_path"]).read_bytes()
            require(sha256_text(source_bytes.decode("utf-8")) == source["source_sha256"], f"I2 source hash mismatch: {skill_id}")
            require(selector_text.encode("utf-8") == source_bytes, f"I2 is not exact source bytes: {skill_id}")
        else:
            require(selector_text.startswith(expected_i1), f"{representation} does not retain I1 base: {skill_id}")
            spans = row.get("selector_evidence_spans")
            require(isinstance(spans, list), f"{representation} evidence spans missing: {skill_id}")
            if require_v3_evidence_alignment:
                for span in spans:
                    require(
                        isinstance(span, dict) and set(span) == {"field_key", "field_label", "item_id", "selector_evidence", "source_position"},
                        f"{representation} evidence span schema mismatch: {skill_id}",
                    )
                    evidence = span["selector_evidence"]
                    require(isinstance(evidence, str) and bool(evidence), f"{representation} empty evidence: {skill_id}")
                    source_text = (root / source["source_path"]).read_text(encoding="utf-8")
                    require(
                        isinstance(span["source_position"], int) and 0 <= span["source_position"] < len(source_text),
                        f"{representation} evidence source position mismatch: {skill_id}",
                    )
                    require(evidence in selector_text, f"{representation} evidence absent from serialisation: {skill_id}")
        if require_exact_source:
            require(row.get("selector_text_sha256") == source["source_sha256"], f"I2 source digest mismatch: {skill_id}")
    require(len(seen_ids) == 2433, f"{representation} identity count mismatch")
    return dict(sorted(total_counts.items()))


def strict_prompt_row(prompt: dict[str, Any]) -> dict[str, Any]:
    for key in ("prompt_id", "prompt", "prompt_sha256", "stratum", "group", "gold_skill"):
        require(isinstance(prompt.get(key), str) and bool(prompt[key]), f"strict prompt missing {key}")
    require(prompt["prompt_sha256"] == sha256_text(prompt["prompt"]), f"strict prompt hash mismatch: {prompt['prompt_id']}")
    return {
        "schema_version": STRICT_PROMPT_SCHEMA,
        "prompt_id": prompt["prompt_id"],
        "prompt": prompt["prompt"],
        "prompt_sha256": prompt["prompt_sha256"],
        "stratum": prompt["stratum"],
        "group": prompt["group"],
        "gold_skill": prompt["gold_skill"],
    }


def validate_strict_prompts(rows: list[dict[str, Any]], candidate_ids: set[str]) -> dict[str, int]:
    require(len(rows) == 381, "strict scored prompt count mismatch")
    prompt_ids: set[str] = set()
    strata = Counter()
    for row in rows:
        require(set(row) == STRICT_PROMPT_KEYS, f"strict prompt has leakage or schema drift: {row.get('prompt_id')}")
        require(row["schema_version"] == STRICT_PROMPT_SCHEMA, f"strict prompt schema mismatch: {row['prompt_id']}")
        require(row["prompt_id"] not in prompt_ids, f"duplicate strict prompt ID: {row['prompt_id']}")
        prompt_ids.add(row["prompt_id"])
        require(row["prompt_sha256"] == sha256_text(row["prompt"]), f"strict prompt hash drift: {row['prompt_id']}")
        require(row["gold_skill"] in candidate_ids, f"strict gold skill absent from V3 library: {row['prompt_id']}")
        require(row["stratum"] in {"controlled", "public_gold"}, f"non-primary stratum in strict endpoint: {row['prompt_id']}")
        strata[row["stratum"]] += 1
    require(dict(strata) == {"controlled": 243, "public_gold": 138}, "strict prompt stratum mismatch")
    return dict(sorted(strata.items()))


def expect_reject(label: str, action: Callable[[], None]) -> str:
    try:
        action()
    except (AssertionError, ValueError):
        return label
    raise AssertionError(f"synthetic preflight guard did not reject: {label}")


def self_test() -> dict[str, Any]:
    source = {
        "source_row_index": 0,
        "skill_id": "skill-a",
        "family": "family",
        "source_policy": "authored_skill",
        "source_path": "source.md",
        "source_sha256": sha256_text("# source\n"),
        "source_name": "skill-a",
        "source_description": "A source-native description.",
        "source_name_sha256": sha256_text("skill-a"),
        "source_description_sha256": sha256_text("A source-native description."),
    }
    good_prompt = strict_prompt_row(
        {
            "prompt_id": "prompt-a",
            "prompt": "Route this request.",
            "prompt_sha256": sha256_text("Route this request."),
            "stratum": "controlled",
            "group": "family",
            "gold_skill": "skill-a",
        }
    )
    rejected = [
        expect_reject(
            "strict_prompt_leakage",
            lambda: validate_strict_prompts([{**good_prompt, "valid_skills": ["skill-a"]}] * 381, {"skill-a"}),
        ),
        expect_reject(
            "strict_prompt_missing_gold",
            lambda: validate_strict_prompts([{**good_prompt, "gold_skill": "missing"}] * 381, {"skill-a"}),
        ),
        expect_reject(
            "i1_serialization_drift",
            lambda: validate_representation_rows(
                root=Path.cwd(),
                sources=[source] * 2433,
                rows=[representation_row(source, "i1-discovery", "wrong")] * 2433,
                representation="i1-discovery",
                require_exact_source=False,
                require_v3_evidence_alignment=False,
            ),
        ),
    ]
    return {
        "schema_version": "rq2b-i3c-v3-b1l-preflight-self-test-v1",
        "state": "self_test_passed",
        "rejected_cases": rejected,
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
    }


def prepare(root: Path) -> dict[str, Any]:
    # Replay all V3 source and I3C integrity predicates before creating a B1L input freeze.
    automatic_report = verify_v3_automatic_integrity(root)
    v11 = verify_v11_contract(root)
    v3_root = root / f"skill_benchmark/rq2b_full_library/{VERSION_ID}"
    freeze_root = root / FREEZE_ROOT
    checkpoint_path = root / FREEZE_CHECKPOINT
    checkpoint = read_json(checkpoint_path)
    require(checkpoint.get("state") == "automatic_integrity_frozen_b1_preflight_eligible", "V3 automatic freeze checkpoint is not eligible")
    require(checkpoint["report"]["sha256"] == sha256_file(freeze_root / "automatic_integrity_freeze_report.json"), "automatic freeze report hash drift")

    preflight_root = root / PREFLIGHT_ROOT
    staging_root = preflight_root.with_name(".b1l_preflight.staging")
    require(not preflight_root.exists() and not staging_root.exists(), "refusing to overwrite V3 B1L preflight")
    staging_root.mkdir(parents=True, exist_ok=False)

    source_manifest_path = root / SOURCE_MANIFEST
    sources = strict_jsonl(source_manifest_path)
    require(len(sources) == 2433, "V3 source manifest does not contain 2,433 rows")
    i1_rows: list[dict[str, Any]] = []
    i2_rows: list[dict[str, Any]] = []
    for source in sources:
        source_bytes = (root / source["source_path"]).read_bytes()
        require(sha256_text(source_bytes.decode("utf-8")) == source["source_sha256"], f"source hash drift: {source['skill_id']}")
        i1_rows.append(representation_row(source, "i1-discovery", serialize_i1(source["source_name"], source["source_description"])))
        i2_rows.append(representation_row(source, "i2-original", source_bytes.decode("utf-8")))

    representations_root = staging_root / "representations"
    representations_root.mkdir(parents=True, exist_ok=False)
    i1_path = representations_root / "i1-discovery.jsonl"
    i2_path = representations_root / "i2-original.jsonl"
    write_jsonl_new(i1_path, i1_rows)
    write_jsonl_new(i2_path, i2_rows)

    final_manifest = read_json(root / FINAL_MANIFEST)
    i3c_path = root / final_manifest["artifacts"]["i3c-fielded-evidence"]["path"]
    i3flat_path = root / final_manifest["artifacts"]["i3-flat-evidence"]["path"]
    i3c_rows = strict_jsonl(i3c_path)
    i3flat_rows = strict_jsonl(i3flat_path)
    counts = {
        "i1-discovery": validate_representation_rows(root=root, sources=sources, rows=i1_rows, representation="i1-discovery", require_exact_source=False, require_v3_evidence_alignment=False),
        "i2-original": validate_representation_rows(root=root, sources=sources, rows=i2_rows, representation="i2-original", require_exact_source=True, require_v3_evidence_alignment=False),
        "i3c-fielded-evidence": validate_representation_rows(root=root, sources=sources, rows=i3c_rows, representation="i3c-fielded-evidence", require_exact_source=False, require_v3_evidence_alignment=True),
        "i3-flat-evidence": validate_representation_rows(root=root, sources=sources, rows=i3flat_rows, representation="i3-flat-evidence", require_exact_source=False, require_v3_evidence_alignment=True),
    }
    for fielded, flat in zip(i3c_rows, i3flat_rows, strict=True):
        require(fielded["skill_id"] == flat["skill_id"], f"I3C/I3-flat identity mismatch: {fielded['skill_id']}")
        require(fielded["selector_evidence_spans"] == flat["selector_evidence_spans"], f"I3C/I3-flat evidence mismatch: {fielded['skill_id']}")

    v11_root = root / V11_ROOT
    prompt_manifest_path = v11_root / "prompt_manifest.jsonl"
    scored_ids_path = v11_root / "scored_prompt_ids.json"
    prompt_by_id = {row["prompt_id"]: row for row in strict_jsonl(prompt_manifest_path)}
    scored_ids = read_json(scored_ids_path)
    require(isinstance(scored_ids, list) and len(scored_ids) == len(set(scored_ids)) == 381, "V1.1 strict scored prompt IDs drift")
    strict_prompts = [strict_prompt_row(prompt_by_id[prompt_id]) for prompt_id in scored_ids]
    prompt_strata = validate_strict_prompts(strict_prompts, {row["skill_id"] for row in sources})
    strict_prompt_path = staging_root / "strict_scored_prompts.jsonl"
    write_jsonl_new(strict_prompt_path, strict_prompts)

    artifact_records = {
        "i1-discovery": {"path": relative(preflight_root / "representations/i1-discovery.jsonl", root), "sha256": sha256_file(i1_path), "rows": 2433, "selector_visible_counts": counts["i1-discovery"]},
        "i2-original": {"path": relative(preflight_root / "representations/i2-original.jsonl", root), "sha256": sha256_file(i2_path), "rows": 2433, "selector_visible_counts": counts["i2-original"]},
        "i3c-fielded-evidence": {"path": relative(i3c_path, root), "sha256": sha256_file(i3c_path), "rows": 2433, "selector_visible_counts": counts["i3c-fielded-evidence"]},
        "i3-flat-evidence": {"path": relative(i3flat_path, root), "sha256": sha256_file(i3flat_path), "rows": 2433, "selector_visible_counts": counts["i3-flat-evidence"]},
    }
    report = {
        "schema_version": "rq2b-i3c-v3-b1l-preflight-report-v3",
        "version_id": VERSION_ID,
        "state": "b1l_preflight_verified_no_scoring",
        "automatic_freeze": {
            "checkpoint": {"path": relative(checkpoint_path, root), "sha256": sha256_file(checkpoint_path)},
            "report": {"path": relative(freeze_root / "automatic_integrity_freeze_report.json", root), "sha256": sha256_file(freeze_root / "automatic_integrity_freeze_report.json")},
        },
        "strict_endpoint_contract": {"path": relative(v11_root / "v11_strict_endpoint_contract.json", root), "sha256": v11["contract_sha256"], "scored_prompt_count": v11["scored_prompt_count"]},
        "source_manifest": {"path": relative(source_manifest_path, root), "sha256": sha256_file(source_manifest_path), "rows": len(sources)},
        "strict_scored_prompts": {"path": relative(preflight_root / strict_prompt_path.name, root), "sha256": sha256_file(strict_prompt_path), "rows": len(strict_prompts), "strata": prompt_strata, "schema": STRICT_PROMPT_SCHEMA},
        "representations": artifact_records,
        "candidate_library_skills": 2433,
        "b1l_expected_result_rows": 381 * len(REPRESENTATIONS),
        "b1l_protocol": {
            "retriever": "bm25",
            "tokenizer": "lowercase_[a-z0-9]+",
            "k1": 1.5,
            "b": 0.75,
            "candidate_tie_break": "skill_id_ascending",
            "persisted_candidate_ranks": [1, 5, 20, 50, 100],
            "accuracy_endpoint": "strict_gold_only",
            "descriptive_stress_prompts_scored": False,
        },
        "validation": {
            "v3_automatic_integrity_replayed": automatic_report["state"],
            "i3c_i3flat_evidence_spans_identical": 2433,
            "gold_skill_exists_in_candidate_library": 381,
            "prompt_label_leakage_in_scored_prompt_artifact": 0,
            "network_calls": 0,
            "scientific_retrieval_or_reranking": False,
        },
        "methodological_limit": "This validates deterministic provenance, exact representation construction, strict prompt isolation, and gold-ID presence only. It does not add an independent semantic validity judgement for the gold labels or I3C fields.",
    }
    report_path = staging_root / PREFLIGHT_REPORT_NAME
    write_json_new(report_path, report)
    packet = {
        "schema_version": "rq2b-i3c-v3-b1l-local-bm25-execution-approval-packet-v3",
        "version_id": VERSION_ID,
        "state": "awaiting_explicit_user_approval_b1l_local_bm25_only",
        "preflight_report": {"path": relative(preflight_root / PREFLIGHT_REPORT_NAME, root), "sha256": sha256_file(report_path)},
        "execution_script": {"path": RUNNER_PATH, "sha256": sha256_file(root / RUNNER_PATH)},
        "scope": {
            "local_only": True,
            "network_calls": 0,
            "external_api_calls": 0,
            "retriever": "bm25",
            "representations": list(REPRESENTATIONS),
            "candidate_library_skills": 2433,
            "strict_scored_prompts": 381,
            "expected_result_rows": 1524,
            "index_builds": 4,
            "query_rankings": 1524,
            "top_k_persisted": 100,
            "accuracy_endpoint": "strict_gold_only",
        },
        "input_hashes": {
            "strict_scored_prompts": report["strict_scored_prompts"],
            "representations": artifact_records,
        },
        "authorises_if_explicitly_approved": [
            "construct four local BM25 indexes and rank only the 381 strict scored prompts",
            "persist Top-100, strict rank, strict Hit@1, strict Recall@K, strict MRR@10, local timing, and index provenance",
            "run a warm-cache local verification against the persisted BM25 indexes",
        ],
        "does_not_authorise": [
            "network, external API, provider, or hosted compute use",
            "Qwen or SkillRouter embedding/reranking",
            "manual QA or new I3C extraction",
            "B2 reranking",
            "thesis LaTeX/PDF result integration before user review",
        ],
        "raw_prompt_or_document_text_in_packet": False,
    }
    packet_path = staging_root / EXECUTION_PACKET_NAME
    write_json_new(packet_path, packet)
    checkpoint_payload = {
        "schema_version": "rq2b-i3c-v3-b1l-preflight-checkpoint-v3",
        "version_id": VERSION_ID,
        "state": "b1l_preflight_frozen_execution_approval_required",
        "report": {"path": relative(preflight_root / PREFLIGHT_REPORT_NAME, root), "sha256": sha256_file(report_path)},
        "execution_approval_packet": {"path": relative(preflight_root / EXECUTION_PACKET_NAME, root), "sha256": sha256_file(packet_path)},
        "retrieval_execution_authorized": False,
        "network_calls": 0,
        "scientific_retrieval_or_reranking": False,
        "thesis_result_writing": False,
        "next_gate": "obtain a separate exact user approval for B1L local BM25 execution; do not rank before that receipt exists",
    }
    write_json_new(staging_root / PREFLIGHT_CHECKPOINT_NAME, checkpoint_payload)
    staging_root.rename(preflight_root)
    return checkpoint_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=repo_root())
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    require(args.self_test != args.prepare, "choose exactly one of --self-test or --prepare")
    result = self_test() if args.self_test else prepare(args.root.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
