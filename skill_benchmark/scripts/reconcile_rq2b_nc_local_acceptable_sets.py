#!/usr/bin/env python3
"""Reconcile cluster-local acceptable-set reviews without creating final gold."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
PROMPTS = BASE / "manifests/current_pre_freeze_consolidated_2026-08-31/admitted_prompt_manifest_current_pre_freeze.jsonl"
PRIMARY = [
    BASE / "review/acceptable_set_local_native_review_terra_2026-08-31.jsonl",
    BASE / "review/acceptable_set_local_rq1_batches_001_002_terra_2026-08-31.jsonl",
    BASE / "review/acceptable_set_local_rq1_batches_003_004_terra_2026-08-31.jsonl",
]
CHALLENGES = [
    BASE / "review/acceptable_set_local_native_adversarial_challenge_terra_2026-08-31.jsonl",
    BASE / "review/acceptable_set_local_rq1_batches_001_002_adversarial_challenge_terra_2026-08-31.jsonl",
    BASE / "review/acceptable_set_local_rq1_batches_003_004_adversarial_challenge_terra_2026-08-31.jsonl",
]
OUTPUT = BASE / "review/acceptable_set_local_reconciliation_2026-08-31"

MULTI_PROMPT = "RQ2B-NC-RQ1-REAUTH-B004-064-02"
MULTI_ADDED = "576360d267216b3689044e635a54843e581084177a5a25d861744f27d4add826"
MULTI_BEST = "ce7e79d8801cb66f2231bfc08e4c9f4a57f15dcd397bb5e8cbf28dd93fa6f251"
DISPUTED_PROMPT = "RQ2B-NC-RQ1-REAUTH-B002-R1-021-02"
DISPUTED_PARTIAL = "3a23090aa07a7ce102eae2b389efd71a73eef6d9f052a85b32b7f5f8202fbf9b"
BLOCKED = {
    "RQ2B-NC-RQ1-REAUTH-B001-004-01",
    "RQ2B-NC-RQ1-REAUTH-B002-R1-030-01",
    "RQ2B-NC-RQ1-REAUTH-B002-R1-030-02",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    required = [PROMPTS, *PRIMARY, *CHALLENGES]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing review input: {missing}")

    prompt_rows = read_jsonl(PROMPTS)
    prompt_by_id = {str(row["prompt_id"]): row for row in prompt_rows}
    if len(prompt_rows) != 129 or len(prompt_by_id) != 129:
        raise SystemExit("Expected 129 unique current pre-freeze prompts")

    primary_rows = [row for path in PRIMARY for row in read_jsonl(path)]
    primary_by_id = {str(row["prompt_id"]): row for row in primary_rows}
    if len(primary_rows) != 129 or set(primary_by_id) != set(prompt_by_id):
        raise SystemExit("Primary local review must cover the exact 129-prompt roster")

    for prompt_id, review in primary_by_id.items():
        prompt = prompt_by_id[prompt_id]
        if review["prompt"] != prompt["prompt"] or review["cluster_id"] != prompt["cluster_id"]:
            raise SystemExit(f"Prompt or cluster drift: {prompt_id}")
        reviewed_roster = {str(row["source_sha256"]) for row in review["candidate_assessments"]}
        expected_roster = {str(value) for value in prompt["candidate_source_sha256"]}
        if reviewed_roster != expected_roster:
            raise SystemExit(f"Candidate roster drift: {prompt_id}")
        labels = {str(row["source_sha256"]): str(row["label"]) for row in review["candidate_assessments"]}
        derived_acceptable = {
            source for source, label in labels.items() if label in {"MOST_SUITABLE", "FULLY_ACCEPTABLE"}
        }
        if derived_acceptable != set(review["acceptable_set_source_sha256"]):
            raise SystemExit(f"Primary acceptable-set invariant failed: {prompt_id}")

    challenge_rows = [row for path in CHALLENGES for row in read_jsonl(path)]
    b34_proposal = [
        row for row in challenge_rows
        if row.get("prompt_id") == MULTI_PROMPT
        and (row.get("source_sha256") or row.get("candidate_source_sha256")) == MULTI_ADDED
        and row.get("challenge_disposition") == "PROPOSE_FULLY_ACCEPTABLE"
    ]
    if len(b34_proposal) != 1:
        raise SystemExit("Expected one exact B004-064-02 false-singleton proposal")

    b12_proposal = [
        row for row in challenge_rows
        if row.get("prompt_id") == DISPUTED_PROMPT
        and (row.get("source_sha256") or row.get("candidate_source_sha256")) == DISPUTED_PARTIAL
        and row.get("challenge_disposition") == "PROPOSE_FULLY_ACCEPTABLE"
    ]
    if len(b12_proposal) != 1:
        raise SystemExit("Expected one exact B002-R1-021-02 disputed proposal")

    reconciled: list[dict[str, Any]] = []
    for prompt_id in sorted(primary_by_id):
        row = json.loads(json.dumps(primary_by_id[prompt_id]))
        decision = "CONFIRM_PRIMARY_LOCAL_REVIEW"
        rationale = "No root override after roster and challenge reconciliation."
        if prompt_id == MULTI_PROMPT:
            assessments = {item["source_sha256"]: item for item in row["candidate_assessments"]}
            if assessments[MULTI_BEST]["label"] != "MOST_SUITABLE" or assessments[MULTI_ADDED]["label"] != "PARTIALLY_ADEQUATE":
                raise SystemExit("Unexpected primary labels for accepted false singleton")
            assessments[MULTI_ADDED]["label"] = "FULLY_ACCEPTABLE"
            assessments[MULTI_ADDED]["root_reconciliation_note"] = (
                "Full source independently supplies the requested PR, release, nightly and local execution-lane split "
                "for the concrete backend change; testing-strategies remains most suitable for the policy framing."
            )
            row["acceptable_set_source_sha256"] = [MULTI_BEST, MULTI_ADDED]
            row["local_disposition"] = "ACCEPTABLE_SET_LOCAL"
            decision = "ACCEPT_ADVERSARIAL_FALSE_SINGLETON"
            rationale = "Backend-testing is fully acceptable but not most suitable for this concrete policy prompt."
        elif prompt_id == DISPUTED_PROMPT:
            assessments = {item["source_sha256"]: item for item in row["candidate_assessments"]}
            if assessments[DISPUTED_PARTIAL]["label"] != "PARTIALLY_ADEQUATE":
                raise SystemExit("Unexpected primary label for disputed meeting-notes candidate")
            decision = "REJECT_ADVERSARIAL_FULLY_ACCEPTABLE_PROPOSAL_KEEP_PARTIAL"
            rationale = (
                "Meeting-notes has a useful project-review template but its declared input is meeting notes, transcripts "
                "or audio summaries; the prompt supplies asynchronous work updates. The input-object mismatch is material."
            )
        elif prompt_id in BLOCKED:
            if row["local_disposition"] != "BLOCK_NO_FULL" or row["acceptable_set_source_sha256"]:
                raise SystemExit(f"Expected confirmed no-full block: {prompt_id}")
            decision = "CONFIRM_BLOCK_NO_FULL"
            rationale = "The closest source explicitly states that it provides guidance and cannot execute the requested file operation."

        row["root_reconciliation"] = {
            "decision": decision,
            "rationale": rationale,
            "scope": "CLUSTER_LOCAL_ONLY_NOT_WHOLE_LIBRARY_FINAL_GOLD",
        }
        row["status"] = "ROOT_RECONCILED_CLUSTER_LOCAL_PENDING_WHOLE_LIBRARY_DISCOVERY_AND_FINAL_FREEZE"
        reconciled.append(row)

    dispositions: dict[str, int] = {}
    for row in reconciled:
        dispositions[row["local_disposition"]] = dispositions.get(row["local_disposition"], 0) + 1
    if dispositions != {"STRICT_LOCAL": 125, "ACCEPTABLE_SET_LOCAL": 1, "BLOCK_NO_FULL": 3}:
        raise SystemExit(f"Unexpected reconciled dispositions: {dispositions}")

    remediation_assessments = [
        (row["prompt_id"], assessment["source_sha256"])
        for row in reconciled
        for assessment in row["candidate_assessments"]
        if assessment.get("description_remediation_needed") is True
    ]
    remediation_sources = sorted({source for _, source in remediation_assessments})
    if len(remediation_assessments) != 4 or remediation_sources != sorted([DISPUTED_PARTIAL, "9a3038a03430dab8842819b78f49714a19f749c774c8952b40d028796cf875fe"]):
        raise SystemExit("Unexpected description-remediation queue")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    ledger_path = OUTPUT / "reconciled_local_acceptable_set_ledger.jsonl"
    write_jsonl(ledger_path, reconciled)
    markdown_path = OUTPUT / "summary.md"
    markdown_path.write_text(
        "# RQ2b-NC cluster-local acceptable-set reconciliation\n\n"
        "Status: **PASS LOCAL RECONCILIATION / NOT WHOLE-LIBRARY GOLD**\n\n"
        "The 381 parent V3 prompts plus 129 NC pre-freeze prompts give 510 cases before this local audit. "
        "After full-source primary review, adversarial challenge and root reconciliation, the NC rows are "
        "125 `STRICT_LOCAL`, one `ACCEPTABLE_SET_LOCAL`, and three `BLOCK_NO_FULL`. Therefore 126 NC "
        "prompts, or 507 parent-plus-NC prompts, remain locally admissible before whole-library alternative discovery.\n\n"
        "## Reconciled changes\n\n"
        "- `RQ2B-NC-RQ1-REAUTH-B004-064-02` is a real false singleton. `testing-strategies` remains most "
        "suitable, while `backend-testing` is also fully acceptable for the concrete PR/release/nightly lane split.\n"
        "- `RQ2B-NC-RQ1-REAUTH-B002-R1-021-02` keeps `meeting-notes` partial: its declared input is meeting "
        "notes/transcripts/audio summaries, whereas the prompt supplies asynchronous work updates.\n"
        "- Three file-operation prompts are blocked because the closest sources explicitly provide guidance but "
        "cannot execute the requested PDF output operation.\n"
        "- `meeting-notes` and `weekly-report` have malformed placeholder frontmatter descriptions (`>`). They "
        "enter the source-grounded description-remediation queue and require fresh target-blind review.\n\n"
        "## Remaining boundary\n\n"
        "These decisions apply only to each authored cluster roster. All 126 locally admissible prompts still need "
        "outcome-blind alternative discovery and source-visible adjudication over the complete 3,094-candidate "
        "library. No final gold, retrieval result or metric is created.\n",
        encoding="utf-8",
    )
    summary = {
        "status": "PASS_CLUSTER_LOCAL_ACCEPTABLE_SET_RECONCILIATION_NOT_FINAL_GOLD_OR_EXPERIMENT_INPUT",
        "combined_test_case_count_before_local_blocks": 510,
        "parent_v3_test_case_count": 381,
        "nc_prompt_count_reviewed": 129,
        "strict_local_count": 125,
        "acceptable_set_local_count": 1,
        "block_no_full_count": 3,
        "locally_admissible_nc_prompt_count": 126,
        "combined_parent_plus_locally_admissible_count": 507,
        "accepted_false_singleton": {
            "prompt_id": MULTI_PROMPT,
            "most_suitable_source_sha256": MULTI_BEST,
            "additional_fully_acceptable_source_sha256": MULTI_ADDED,
        },
        "rejected_fully_acceptable_challenge_kept_partial": {
            "prompt_id": DISPUTED_PROMPT,
            "source_sha256": DISPUTED_PARTIAL,
            "reason": "material input-object mismatch: asynchronous work updates versus meeting notes/transcript/audio summary",
        },
        "blocked_prompt_ids": sorted(BLOCKED),
        "description_remediation_assessment_count": len(remediation_assessments),
        "description_remediation_unique_source_count": len(remediation_sources),
        "description_remediation_source_sha256": remediation_sources,
        "input_sha256": {str(path.relative_to(ROOT)): sha256_file(path) for path in required},
        "artifact_sha256": {
            ledger_path.name: sha256_file(ledger_path),
            markdown_path.name: sha256_file(markdown_path),
        },
        "remaining_gates": [
            "The 126 locally admissible NC prompts still require outcome-blind whole-library alternative discovery over all 3,094 candidates.",
            "Description repairs must be source-grounded, versioned, and freshly target-blind reviewed before representation freeze.",
            "The blocked prompts and affected cluster completeness require replacement, rewrite under the real source capability, or exclusion.",
            "No final strict gold, acceptable set, selector result, metric, or thesis result is created here.",
        ],
    }
    summary_path = OUTPUT / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
