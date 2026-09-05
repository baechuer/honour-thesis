#!/usr/bin/env python3
"""Rewrite high source-echo prompts from RQ1 re-review batch 001.

The script carries forward provenance and candidate rosters, but replaces the
prompt text with shorter naturalistic scenarios.  It emits private authoring
rows and target-blinded packets only; it does not create labels or admissions.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "rq2b_naturalistic_confusability"
AUTHORS_IN = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_001_private_2026-08-31.jsonl"
PACKETS_IN = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_target_blinded_packets_2026-08-31.jsonl"
AUTHORS_OUT = BASE / "prompts/rq1_frozen_cluster_reauthored_batch_001_rewrite_private_2026-08-31.jsonl"
PACKETS_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_rewrite_target_blinded_packets_2026-08-31.jsonl"
SUMMARY_OUT = BASE / "review/rq1_frozen_cluster_reauthored_batch_001_rewrite_packet_summary_2026-08-31.json"


REWRITES = {
    "RQ2B-NC-RQ1-REAUTH-B001-008-01": (
        "Our application repository needs to include firmware maintained by another team. "
        "Their repository must keep its own history, while each application release must identify "
        "the exact firmware revision it was tested with. Show how to add it under `vendor/firmware`, "
        "clone the project in CI, and deliberately move to a newer tested revision later."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-008-02": (
        "A TypeScript service needs an unpublished fix from an external repository for the next "
        "two releases. The team uses pnpm and needs repeatable CI installs even if the upstream "
        "branch changes. Recommend how to reference and pin the dependency until a registry release is available."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-013-01": (
        "I have attached my current resume and a senior data-engineering job description. Tell me "
        "the three changes that would most improve this application, explain why, and illustrate "
        "the advice by revising at most two weak bullets."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-013-02": (
        "My notes list three past roles, projects, education and the kind of senior data-engineering "
        "job I want, but I have no current resume to submit. Turn those notes into a complete "
        "one-page application document and mark facts or metrics I still need to provide."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-014-01": (
        "A new enterprise customer has accepted our commercial order form but still needs the "
        "privacy terms. They have not sent their own document. Use our approved internal template "
        "and the supplied processing facts to prepare a clean first draft for counsel."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-014-02": (
        "A customer has sent its privacy addendum and security schedule for signature. We are the "
        "service provider. Assess the supplied wording, rank the provisions that need negotiation, "
        "and propose edits and fallback language against that document."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-015-01": (
        "We are about to sell our hosted product and implementation services to our first enterprise "
        "customer. No customer contract has been supplied. Starting from our approved internal "
        "template and the deal facts, prepare a complete provider-side agreement for counsel."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-015-02": (
        "A buyer has sent its SaaS services agreement, order form and statement of work. We represent "
        "the provider. Review this package, prioritise the commercial and legal risks, and propose "
        "negotiation edits in the buyer's document."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-016-01": (
        "An enterprise customer will join a six-month co-design program with product access, regular "
        "feedback sessions and limited feature commitments. No agreement exists yet. Use our approved "
        "internal template and the program facts to prepare the first contract for counsel."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-016-02": (
        "A prospective co-design partner has sent its proposed terms for a six-month early-access "
        "program. Review the supplied agreement from our provider-side position, identify obligations "
        "that are too broad, and propose edits on that document."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-019-01": (
        "Last night's dependency setup failed with the attached log, and the team has not attempted "
        "a fix yet. Record the failure for triage so another engineer can reproduce it, see the "
        "observed and expected behaviour, and understand the outcome we need."
    ),
    "RQ2B-NC-RQ1-REAUTH-B001-019-02": (
        "The digest-validation fix is complete on a branch and its focused tests pass. Submit the "
        "change for a teammate to review and merge, briefly explaining the cause, the change, how it "
        "was verified and any remaining limitation."
    ),
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    authors_by_id = {row["prompt_id"]: row for row in read_jsonl(AUTHORS_IN)}
    packets_by_id = {row["prompt_id"]: row for row in read_jsonl(PACKETS_IN)}
    if set(REWRITES) - authors_by_id.keys() or set(REWRITES) - packets_by_id.keys():
        raise SystemExit("Rewrite IDs are absent from an input artifact")

    author_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    for source_prompt_id, prompt in REWRITES.items():
        source_author = authors_by_id[source_prompt_id]
        source_packet = packets_by_id[source_prompt_id]
        prompt_id = source_prompt_id.replace("REAUTH-B001", "REAUTH-B001-R1")
        author_rows.append({
            **source_author,
            "prompt_id": prompt_id,
            "supersedes_prompt_id": source_prompt_id,
            "prompt": prompt,
            "initial_cue_audit": (
                "REWRITE_AFTER_TARGET_BLINDED_ECHO_REVIEW: preserves the task's necessary input or "
                "artifact-state boundary while removing sibling-exclusion language and source-like checklists."
            ),
            "status": "REWRITTEN_PRIVATE_AUTHORING_ONLY_NOT_A_GOLD_LABEL_OR_ADMITTED_RQ2_CASE",
        })
        packet_rows.append({
            **source_packet,
            "packet_id": f"RQ2B-NC-TARGET-BLIND-{prompt_id}",
            "prompt_id": prompt_id,
            "prompt": prompt,
            "supersedes_prompt_id": source_prompt_id,
            "status": "REWRITE_TARGET_BLINDED_REVIEW_INPUT_NOT_A_LABEL_OR_RESULT",
        })

    write_jsonl(AUTHORS_OUT, author_rows)
    write_jsonl(PACKETS_OUT, packet_rows)
    summary = {
        "status": "PASS_RQ1_REVIEW_BATCH_001_HIGH_ECHO_REWRITE_PACKETISATION_NOT_A_LABEL_OR_ADMISSION",
        "rewritten_prompt_count": len(author_rows),
        "target_blinded_packet_count": len(packet_rows),
        "candidate_judgment_slot_count": sum(len(row["candidates"]) for row in packet_rows),
        "input_sha256": {
            str(AUTHORS_IN.relative_to(ROOT)): sha256_file(AUTHORS_IN),
            str(PACKETS_IN.relative_to(ROOT)): sha256_file(PACKETS_IN),
        },
        "artifacts": {
            str(AUTHORS_OUT.relative_to(ROOT)): sha256_file(AUTHORS_OUT),
            str(PACKETS_OUT.relative_to(ROOT)): sha256_file(PACKETS_OUT),
        },
        "claim_boundary": [
            "These rewrites address source-description echo; they are not labels or admissions.",
            "The author-intended source remains private and is absent from target-blinded packets.",
            "Every rewrite still requires independent adequacy and cue review before admission."
        ],
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
