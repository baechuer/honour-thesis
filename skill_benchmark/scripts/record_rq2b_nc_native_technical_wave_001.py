#!/usr/bin/env python3
"""Record and mechanically verify RQ2-native technical discovery Wave 001.

This captures source-grounded reading judgments only.  It does not admit a
cluster, author a prompt, freeze a label, or run a selector.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[2]
ROOT = WORKSPACE / "skill_benchmark"
S = "skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/skillme-skills-a28c4ce9/skills"
E = "skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/emmraan-agent-skills-1124ce40/skills"
OUT = ROOT / "rq2b_naturalistic_confusability/candidates/rq2_native_discovery_wave_001_technical_2026-08-31.jsonl"
SCREEN = ROOT / "rq2b_naturalistic_confusability/clusters/RQ2_NATIVE_DISCOVERY_WAVE_001_TECHNICAL_SCREEN_2026-08-31.md"
SUMMARY = ROOT / "rq2b_naturalistic_confusability/candidates/rq2_native_discovery_wave_001_technical_summary_2026-08-31.json"


def candidate(skill_id: str, source_id: str, source_sha256: str, boundary: str, root: str = S) -> dict[str, str]:
    return {
        "skill_id": skill_id,
        "source_id": source_id,
        "source_sha256": source_sha256,
        "source_path": f"{root}/{skill_id}/source/SKILL.original.md",
        "necessary_boundary": boundary,
    }


LEADS: list[dict[str, Any]] = [
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-001",
        "common_envelope": "repair a production service slowdown or failure caused by a dependency",
        "cue_risk": "MEDIUM_LEGITIMATE_FAILURE_MECHANISM",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-rate-limit-handler", "RQ1B-V3-SRC-012364", "6c0d93b678d80841289002b4600e7a28b7ca69112a9ae1c2baaefc85297a5636", "an upstream dependency explicitly signals quota or backoff and the caller must reduce request rate"),
            candidate("public-skillme-circuit-breaker-builder", "RQ1B-V3-SRC-017540", "99146345530691362bf0d31863e0eb90b2f82f01d19ea1ac9a956fd39bbbd8c2", "an upstream dependency hangs or repeatedly fails and the caller needs timeout, fail-fast and isolation behaviour"),
            candidate("public-skillme-connection-pool-tuner", "RQ1B-V3-SRC-005331", "2e7edc6066af450c6c508f342a019e2f0de8e09feaed43d869cd37bc696b84bc", "local database connection slots, checkout waits or connection limits are the constrained resource"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-002",
        "common_envelope": "diagnose and fix an important slow SQL workload with verifiable evidence",
        "cue_risk": "MEDIUM_LEGITIMATE_EXECUTION_EVIDENCE",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-index-advisor", "RQ1B-V3-SRC-002956", "19a4049059f58588afc67ab04c1216e4398565c5b0b2e3dd27b9219aa1308d3a", "selective access performs a full scan because a useful index is absent or ordered incorrectly"),
            candidate("public-skillme-query-rewriter", "RQ1B-V3-SRC-009611", "53fbe535acd118ef9784b0bf3f26563489598785221e4fe622e12ff0a700bedb", "indexes are suitable but the query shape causes correlated work, row explosion or deep-offset cost"),
            candidate("public-skillme-partition-planner", "RQ1B-V3-SRC-011122", "61288e8eefc12a5849a2a79a61e8d272f485991e47128daba2cc54b55f4c2a3d", "table scale makes retention, vacuum or pruning operationally unsafe without a partitioning decision"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-003",
        "common_envelope": "decide how to strengthen a test suite before a high-risk change",
        "cue_risk": "MEDIUM_LEGITIMATE_ASSURANCE_FAILURE",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-coverage-gap-finder", "RQ1B-V3-SRC-010528", "5bf4e790ad4ad98e1dade38846fcb36f4c710cfd704a2f2d22185ad990792b5f", "branch coverage and change history are available and unexecuted critical paths must be prioritised"),
            candidate("public-skillme-mutation-test-runner", "RQ1B-V3-SRC-029222", "ff5350cc7bbb02b7c44959e3a4b354e9ca0361d0e59e0df11d67513018647665", "covered code may have weak assertions and controlled code changes are needed to find surviving cases"),
            candidate("public-skillme-characterization-test-writer", "RQ1B-V3-SRC-023399", "cc3de90e398b9e50e2fae1feb70355d52fa2261e0a270f730d2b0bff3da39e41", "untested legacy code will be refactored and its current observable behaviour must first be preserved"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-004",
        "common_envelope": "create credible non-production inputs for a test, prototype or demonstration",
        "cue_risk": "LOW_MEDIUM_WITH_COMPOSITION_RISK",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_WITH_ARTIFACT_NARROWING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-mock-stub-designer", "RQ1B-V3-SRC-010262", "5971207e6810d081f08d305b1e56cef65c1fa6b79317817e05f40460428ccf3c", "the missing artefact substitutes for a network, clock, SDK, filesystem or similar dependency boundary"),
            candidate("public-skillme-test-data-builder", "RQ1B-V3-SRC-002375", "1483096b1d6756c121bbf3bf0e4de92dfc561927e96f11d3101335156e9148bc", "the missing artefact is locally valid domain objects, factories or edge-case fixtures"),
            candidate("public-skillme-test-placeholder-data", "RQ1B-V3-SRC-017390", "97e86f30e1f3377446fecf0f7b67a32f15c40182a6d181e555f478bc9d94f8a8", "a UI demonstration needs remotely fetchable fake CRUD records or placeholder imagery"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-005",
        "common_envelope": "build reproducible performance evidence and locate the dominant bottleneck",
        "cue_risk": "LOW_MEDIUM_LEGITIMATE_PLATFORM_AND_OBSERVABLE",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-web-performance", "RQ1B-V3-SRC-003839", "21a8ef1939ea45f8e3e14d3c21d7cdb237cf3522b7415e188be498c735ba873d", "browser rendering, interaction latency and layout stability are the performance surface"),
            candidate("public-skillme-load-testing", "RQ1B-V3-SRC-010669", "5d103dde3fd7e62ecbd2e7906d4777ab4893f4678175dc52659692fc0abed65c", "concurrent traffic, capacity limits, ramp behaviour, tail latency and saturation are the evidence needed"),
            candidate("public-skillme-mobile-perf-profiler", "RQ1B-V3-SRC-010835", "5eb00fb70605e4d4d412bbbcca9a35b9ca8c720fe2f767fc39c19f04f1394d91", "a native mobile application needs real-device traces for frame jank, startup or heap growth"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-006",
        "common_envelope": "make an HTTP API reliable for external consumers as it is created or evolved",
        "cue_risk": "LOW_MEDIUM_LEGITIMATE_LIFECYCLE_INPUT",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-api-design", "RQ1B-V3-SRC-003891", "221e583e98a541a98a06531ccb8380641d80bf372cbe967affb4435b416dd8fd", "a new resource surface needs endpoint semantics, errors, pagination and a consumer contract"),
            candidate("public-skillme-api-versioning-strategist", "RQ1B-V3-SRC-006718", "3a8206a8c7acf3922e35807632a25d7ad7791fa1492d64fa9e5e05b4d48f4c79", "existing consumers face a breaking change and need version, deprecation and sunset policy"),
            candidate("public-skillme-api-client-generator", "RQ1B-V3-SRC-007612", "4263c65a5f80b8a25b492d1545b900423a5252b9490a0d59dbb904875b9e0cd9", "an existing machine-readable contract must become a typed client with controlled transport behaviour"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-007",
        "common_envelope": "design or repair a schema or data contract for a specific consumer",
        "cue_risk": "MEDIUM_HIGH_LEGITIMATE_CONSUMER_AND_RESOURCE",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-database-schema", "RQ1B-V3-SRC-025278", "dcd3fb3593a5092dd95b65ec623802d3e2ba5b870615ff35cab8c32602739ff2", "relational persistence needs keys, constraints and a safe migration path"),
            candidate("public-skillme-graphql-schema", "RQ1B-V3-SRC-002478", "156383ef417dcf5c1386183ba7354d10fb938ee8f2af73c483855802fa77bcaa", "client queries need graph types, resolver batching, pagination and cost controls"),
            candidate("public-skillme-feature-store-design", "RQ1B-V3-SRC-002700", "1749e9becd21bbbd6f61048c8142af2594d6dd8d3b194e1f8273d94ee1cf701f", "training and serving need point-in-time feature joins plus online/offline consistency"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-008",
        "common_envelope": "decide whether a model-backed feature is reliable, regressing or needs retraining",
        "cue_risk": "LOW_MEDIUM_LEGITIMATE_MODEL_AND_DEPLOYMENT_STAGE",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-llm-evaluation", "RQ1B-V3-SRC-020895", "b67975de3681a05021900e024d55f84eaf1fa42fff5fb5b913ed21a9f4228f45", "generative outputs need golden cases, deterministic checks, calibrated judging and CI regression"),
            candidate("public-skillme-model-evaluation-report", "RQ1B-V3-SRC-013077", "720c2b06297514d874cd1f74f06e5eaf72df9325f09006eacc33fba819f46b29", "a supervised model needs baseline, business metrics, slices, calibration and a release decision"),
            candidate("public-skillme-data-drift-monitor", "RQ1B-V3-SRC-015881", "8accaaa84c3bfacc31fdc474f9aab32657ff8a8f54f2457356bf5ff6d2baeb82", "a deployed system needs distribution-shift monitoring and retraining triggers"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-009",
        "common_envelope": "cross a breaking change while preserving rollback and service continuity",
        "cue_risk": "LOW_MEDIUM_LEGITIMATE_MIGRATION_TARGET",
        "screen_disposition": "PROMOTE_TO_RQ2_PROMPT_AUTHORING_PENDING_INDEPENDENT_ADEQUACY_REVIEW",
        "candidates": [
            candidate("public-skillme-framework-upgrader", "RQ1B-V3-SRC-018816", "a4661cc165545de4b766ccc7968856a628d54f67b54da44ad00ef2a9ed29a054", "a framework major version needs changelog and codemod guided incremental CI-gated changes"),
            candidate("public-skillme-language-version-migrator", "RQ1B-V3-SRC-004536", "27625a170f24bfc0b57bfd295722fd7823789532e3e508dece7788083264274a", "language or runtime semantics change and require source transforms plus dual-runtime verification"),
            candidate("public-skillme-migration-safety-checker", "RQ1B-V3-SRC-011017", "604e9fe827781f65979484223c566ac749f7f5ecbd00ee60412f173013f46610", "live relational DDL has long-lock risk and needs an expand-contract deployment plan"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-010",
        "common_envelope": "prevent duplicate delivery from causing repeated side effects",
        "cue_risk": "MEDIUM_COMPOSITION_AND_ACCEPTABLE_SET_RISK",
        "screen_disposition": "DEFER_STRICT_RETAIN_AS_ACCEPTABLE_SET_EXPLORATORY_LEAD",
        "candidates": [
            candidate("public-skillme-idempotency-enforcer", "RQ1B-V3-SRC-010542", "5c1b94df347a1f9eb5ccd2c106f1d0d1528c395bf103cdd06a19eee4d2ea9080", "downstream processing needs deduplication semantics for repeated operations"),
            candidate("public-skillme-webhook-receiver-hardener", "RQ1B-V3-SRC-001696", "0eb57a31c8eaadbf52af2b12b269ecf640da6ac37b700256640b1a85ca483520", "the receiving edge needs raw-body signature verification, durable persistence and fast acknowledgement"),
        ],
    },
    {
        "cluster_lead_id": "RQ2B-NC-NATIVE-TECH-011",
        "common_envelope": "select an intervention for an underperforming model-backed product",
        "cue_risk": "MEDIUM_HIGH_SUBSUMPTION_AND_COMPOSITION_RISK",
        "screen_disposition": "DEFER_STRICT_RETAIN_AS_ACCEPTABLE_SET_EXPLORATORY_LEAD",
        "candidates": [
            candidate("public-skillme-prompt-engineer", "RQ1B-V3-SRC-014230", "7c62a62b72faefbd3ce1cd291a84f2e10af381e34ad82b1880673c489ce91b79", "the primary defect is inconsistent instruction or format following"),
            candidate("public-emmraan-databases-data-rag", "RQ1B-V3-SRC-015482", "875fdf781e6d821ddd947ffe1daabb2517e07ae01e2c0a17f8ca906799bb3210", "the missing capability is fast-changing or private knowledge that must be grounded at request time", E),
            candidate("public-emmraan-ai-ml-fine-tuning-expert", "RQ1B-V3-SRC-025029", "da72ef468de313b02176e232e0570fe1064cc95c9e36ea3a987e0abf134dbfe0", "the missing capability is stable learned behaviour or style supported by labelled examples", E),
        ],
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    hashes: set[str] = set()
    for lead in LEADS:
        lead["discovery_line"] = "RQ2_NATIVE_NEW_CLUSTER_EXCLUDING_PRIOR_RQ1_AND_NC_SOURCE_HASHES"
        lead["origin_stratum"] = "mostly_single_origin_SkillMedev_skills_with_two_Emmraan_candidates_in_deferred_lead"
        lead["status"] = "DISCOVERY_LEAD_NOT_AN_ADMITTED_CLUSTER_OR_LABEL"
        for item in lead["candidates"]:
            path = WORKSPACE / item["source_path"]
            if not path.is_file():
                raise SystemExit(f"Missing source: {path}")
            if sha256_file(path) != item["source_sha256"]:
                raise SystemExit(f"Source hash mismatch: {path}")
            if item["source_sha256"] in hashes:
                raise SystemExit(f"Repeated candidate source: {item['source_sha256']}")
            hashes.add(item["source_sha256"])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in LEADS), encoding="utf-8")
    promote = sum(row["screen_disposition"].startswith("PROMOTE") for row in LEADS)
    deferred = len(LEADS) - promote
    screen_text = f"""# RQ2-native discovery Wave 001 — technical screen

Date: 2026-08-31
Status: **NEW SOURCE-GROUNDED LEADS / NO ADMITTED CLUSTER, PROMPT, OR LABEL**

This pass read complete preserved sources only after exact-hash exclusion of all
79 frozen RQ1 cluster members and prior NC lead/review sources. All {len(hashes)}
candidate files replay their recorded SHA-256. No RQ1 prompt, gold label,
cluster card, field card, selector score, or result was used.

Nine leads are promoted to prompt authoring: backend dependency failure, SQL
bottleneck mechanism, test-suite assurance, narrowed non-production artefacts,
performance evidence surface, API lifecycle artefact, schema consumer,
ML/LLM quality-assurance stage, and migration target. Duplicate-delivery
ownership and LLM intervention selection are deferred from strict prompt
authoring because realistic tasks often require multiple candidates together.

Promotion is a source-screen decision only. Every lead still needs source
evidence cards, pairwise operational-contrast review, title/provider/path-free
prompt authoring, target-blinded candidate-by-candidate adequacy review, cue
audit, provenance/licence admission, and final integrity freezing. It is not a
gold label or evidence of retrieval performance.
"""
    SCREEN.parent.mkdir(parents=True, exist_ok=True)
    SCREEN.write_text(screen_text, encoding="utf-8")
    summary = {
        "status": "PASS_NATIVE_TECHNICAL_WAVE_001_SOURCE_SCREEN_NOT_AN_ADMISSION_OR_RESULT",
        "lead_count": len(LEADS),
        "promote_count": promote,
        "defer_count": deferred,
        "candidate_source_count": len(hashes),
        "source_hash_replay_failure_count": 0,
        "artifacts": {
            str(OUT.relative_to(ROOT)): sha256_file(OUT),
            str(SCREEN.relative_to(ROOT)): sha256_file(SCREEN),
        },
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
