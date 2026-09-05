#!/usr/bin/env python3
"""Build a hash-bound, non-executing RQ2b scientific-protocol approval packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "skill_benchmark" / "outputs" / "rq2b" / "preflight"
OUTPUT_JSON = PREFLIGHT / "protocol_approval_packet.json"
OUTPUT_MD = PREFLIGHT / "protocol_approval_packet.md"

PROTOCOL = "thesis_notes/current/RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md"
FILES = [
    PROTOCOL,
    "thesis_notes/current/RQ2 Comprehensive Methodology Specification - 2026-07-26.md",
    "thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md",
    "thesis_notes/current/Thesis Progress Tracker.md",
    "thesis_notes/current/Experiment Methodology Tracker.md",
    "thesis_notes/current/Thesis Experiment Roadmap.md",
    "thesis_notes/README.md",
    "skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md",
    "skill_benchmark/annotations/acceptable_alternatives.json",
    "skill_benchmark/annotations/public_gold_acceptable_alternatives.json",
    "skill_benchmark/annotations/low_information_acceptables.json",
    "skill_benchmark/versions/benchmark-v0.4-2026-06-16.json",
    "skill_benchmark/scripts/run_rq2a_fixed_candidate_matrix.py",
    "skill_benchmark/scripts/audit_rq2b_preflight.py",
    "skill_benchmark/scripts/test_rq2b_preflight.py",
    "skill_benchmark/scripts/audit_rq2b_token_limits.py",
    "skill_benchmark/scripts/audit_rq2b_precision.py",
    "skill_benchmark/scripts/validate_rq2b_prefreeze_protocol.py",
    "skill_benchmark/scripts/build_rq2b_protocol_approval_packet.py",
    "skill_benchmark/outputs/rq2b/preflight/audit.json",
    "skill_benchmark/outputs/rq2b/preflight/source_inventory.jsonl",
    "skill_benchmark/outputs/rq2b/preflight/prompt_inventory.jsonl",
    "skill_benchmark/outputs/rq2b/preflight/token_limit_audit.json",
    "skill_benchmark/outputs/rq2b/preflight/precision_audit.json",
    "skill_benchmark/outputs/rq2b/preflight/protocol_validation.json",
    "skill_benchmark/outputs/rq2b/preflight/independent_protocol_review.md",
    "skill_benchmark/outputs/rq2b/preflight/independent_protocol_rereview.md",
    "skill_benchmark/outputs/rq2b/preflight/README.md",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(raw.encode("utf-8"))


def file_record(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    data = path.read_bytes()
    return {"path": relative, "sha256": sha256_bytes(data), "bytes": len(data)}


def main() -> None:
    audit = json.loads((PREFLIGHT / "audit.json").read_text(encoding="utf-8"))
    token = json.loads((PREFLIGHT / "token_limit_audit.json").read_text(encoding="utf-8"))
    precision = json.loads((PREFLIGHT / "precision_audit.json").read_text(encoding="utf-8"))
    validation = json.loads((PREFLIGHT / "protocol_validation.json").read_text(encoding="utf-8"))
    if not audit["pass_preflight"] or not validation["pass_validation"]:
        raise SystemExit("prefreeze audit or protocol validation did not pass")

    files = [file_record(path) for path in FILES]
    scope = {
        "approval_type": "rq2b_scientific_protocol_freeze_only",
        "authorises": [
            "freeze the approved scientific protocol and create a new date-stamped RQ2b corpus version",
            "build hash-bound I1/I2 manifests and zero-network implementation/smoke artifacts",
            "build an exact I3C extraction transfer packet without transmitting source text",
        ],
        "does_not_authorise": [
            "sending any I2 source artifact to Codex or another model worker",
            "sending any benchmark text to DashScope or another embedding provider",
            "paid API calls",
            "hosted SkillRouter computation or text transfer",
            "writing RQ2b results into thesis LaTeX/PDF",
        ],
        "study": {
            "skills": 2433,
            "controlled_prompts": 245,
            "public_gold_prompts": 144,
            "stress_prompts": 12,
            "representations": ["I1-discovery", "I2-original", "I3C-fielded-evidence", "I3-flat-evidence"],
            "first_stage": ["global BM25", "Qwen text-embedding-v4 max-chunk multi-vector"],
            "reranker": "pipizhao/SkillRouter-Reranker-0.6B revision 78986e1142d12857cfd85b8005e62902cd42d858",
            "primary_rerank_k": 20,
        },
        "decisions": [
            "minimal B1 candidate-generation plus B2 immutable-candidate reranking scope; graph/tree, downstream, external 79K, SkillRouter embedding, I2+I3C, and K50 excluded",
            "new date-stamped corpus version; public I2 uses source/SKILL.original.md and all other I2 uses authored SKILL.md",
            "I1 source-native name+description; I2 exact source; I3C source-native name+description plus fielded exact evidence spans; I3-flat identical spans without labels",
            "acceptable closure from strict gold plus all pre-existing acceptable skills through exact I2 SHA-256 equivalence; no post-ranking additions",
            "I3C V2 extraction with byte-deterministic whitespace normalization, global/frontmatter deduplication, selector-visible exact evidence only, automatic gates, blinded 120-row QA, and rejection/corpus-wide correction rules",
            "Qwen 1024 dimensions, 8192 documented ceiling, 7500-token chunks, 256-token overlap, max aggregation, and mean/length sensitivities",
            "SkillRouter fixed prompt hash, 2048 total tokens, query-specific candidate budget, 128-token overlap, max aggregation, and mean/length sensitivities",
            "eight atomic primary hypotheses P1-C through P4-P; acceptable Recall@20 and conditional acceptable Hit@1 primary endpoints, with end-to-end Hit@1 as the required pipeline counterpart",
            "3-point non-inferiority margin; one-sided 95% grouped-bootstrap lower bound must exceed -0.03 in both strata; cost separate",
            "prompt_inventory.group-bound prompt-weighted percentile bootstrap seed 2026080201, grouped paired sign-flip seed 2026080202, frozen tails/p-value formula, equal-group sensitivity, and Holm over six superiority/effect tests",
            "protocol, I3C transfer, Qwen transfer/cost, hosted SkillRouter, result review, and thesis writing remain separate gates",
            "future serializers, runners, and analysis code must pass zero-network smoke tests and receive a B1S implementation hash seal before scientific execution",
        ],
        "no_scientific_rq2b_result_exists": True,
        "network_calls_during_b0": 0,
    }
    packet = {
        "schema_version": "rq2b-scientific-protocol-approval-packet-v1",
        "created_date": "2026-08-02",
        "state": "awaiting_explicit_user_approval_not_frozen_not_result",
        "scope": scope,
        "scope_sha256": canonical_sha256(scope),
        "files": files,
        "evidence": {
            "prefreeze_pass": audit["pass_preflight"],
            "protocol_validation_pass": validation["pass_validation"],
            "independent_final_focused_verdict": "PASS",
            "legacy_drifted_files": len(audit["legacy_freeze_drift"]["drifted"]),
            "exact_duplicate_groups": len(audit["exact_duplicate_sources"]),
            "qwen_sources_requiring_chunking": token["qwen"]["sources_requiring_proposed_chunking"],
            "qwen_proxy_max_tokens": token["qwen"]["source_max_tokens"],
            "skillrouter_min_document_budget": token["skillrouter"]["minimum_document_window_budget"],
            "controlled_groups": precision["strata"]["controlled"]["group_count"],
            "public_groups": precision["strata"]["public_gold"]["group_count"],
        },
    }
    OUTPUT_JSON.write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# RQ2b Scientific-Protocol Approval Packet",
        "",
        f"State: `{packet['state']}`",
        f"Scope SHA-256: `{packet['scope_sha256']}`",
        "",
        "Approval freezes scientific choices and permits only local versioning, implementation, "
        "and zero-network smoke preparation. It does not authorize I3C source transfer, Qwen "
        "calls, hosted SkillRouter work, or thesis-result writing.",
        "",
        "## Decisions",
        "",
        *[f"{index}. {decision}" for index, decision in enumerate(scope["decisions"], 1)],
        "",
        "## Evidence",
        "",
        f"- Prefreeze audit: {'PASS' if audit['pass_preflight'] else 'FAIL'}",
        f"- Protocol validation: {'PASS' if validation['pass_validation'] else 'FAIL'}",
        f"- Bound files: {len(files)}",
        "- B0 network calls: 0",
        "",
    ]
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"state": packet["state"], "scope_sha256": packet["scope_sha256"], "bound_files": len(files)}, indent=2))


if __name__ == "__main__":
    main()
