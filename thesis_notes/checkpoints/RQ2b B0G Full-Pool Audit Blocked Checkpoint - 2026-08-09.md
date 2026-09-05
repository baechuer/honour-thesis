# RQ2b B0G Full-Pool Audit Blocked Checkpoint

Date: 2026-08-09  
Status: **BLOCKED BEFORE RETRIEVAL - NOT AN RQ2b RETRIEVAL RESULT**

## What completed locally

- The frozen B0G initial-review controller validated 384 blinded A/B packets and 15,420 decisions.
- The separately validated C controller adjudicated all 250 eligible A/B disagreements in eight blinded batches.
- The final-freeze controller rebuilt the packet, decision, prompt-identity, source-hash, and evidence bindings for 7,710 reviewed units spanning 389 scored prompts.
- An independent read-only metadata review checked the proposal, outcomes, strict-status, report bindings, and stop rules. No raw prompt or skill text was reviewed in that final metadata check.

## Why finalisation stopped

The controller's two coverage hard stops fail:

- 14 strict-gold rows are rejected or otherwise not `fully_acceptable`.
- 8 scored prompts have no reviewed `fully_acceptable` candidate.

The complete review set resolves and prompt identity aligns, but those two failures prohibit freezing an acceptable set. The controller's verification state is `independent_review_confirms_block`; the independent reviewer recommendation is `do_not_finalize`.

The eight empty-coverage prompts are a subset of the 14 strict-gold rejections, so there are 14 distinct affected prompts rather than 22. The other six affected prompts have at least one `fully_acceptable` reviewed candidate even though their recorded strict gold is not fully acceptable. This is still a review-pool conclusion, not proof that no additional full-library alternative exists.

## Audit-only facts

- Direct fully acceptable candidates: 1,227.
- Candidates after exact-I2 duplicate closure: 1,231.
- Added alternatives after closure: 813 (809 direct additions plus 4 duplicate-closure additions).
- Network calls: 0. Provider calls: 0. Retrieval/selector runs: 0.

These counts describe label coverage and audit mechanics. They must not be reported as Hit@1, Recall, MRR, representation, retriever, or reranker outcomes.

## Canonical artifacts

- Proposal manifest: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1-2026-08-02/b0g_semantic_review_v2_2026-08-09/final_freeze_v2_2026-08-09/proposal_manifest.json`
- Freeze report: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1-2026-08-02/b0g_semantic_review_v2_2026-08-09/final_freeze_v2_2026-08-09/freeze_report.json`
- Independent review: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1-2026-08-02/b0g_semantic_review_v2_2026-08-09/final_freeze_v2_2026-08-09/independent_freeze_review.json`
- Canonical protocol and ledger: `thesis_notes/current/RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md`

## Superseding focused remediation decision (2026-08-15)

The base v1 audit remains immutable and blocked; it is not reopened or
finalised. The user instead directed a routing-focused review of only the 14
affected strict-gold rows. The term remains **gold label skill**: it now means
the main skill to load for the frozen request, not a promise that its static
document has every live runtime capability.

The resulting prospective patch retains six original gold labels and excludes
eight prompts with a material workflow mismatch. It deliberately assigns no
new replacement gold labels and does not rerun B0G. The evidence and decisions
are in `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.1-2026-08-15/gold_label_remediation_v1_2026-08-15/`.

This produces a strict-gold-only materialised v1.1 path, not a frozen
acceptable-alternative set. Its 393-prompt manifest and 381-prompt scored-ID
list passed local identity/count validation. Acceptable Hit@K/Recall@K remain
unavailable without a separately scoped acceptable-label audit. B1R,
I3C extraction, all B1/B2 retrieval or reranking, external/provider work, and
RQ2b thesis-result writing remain blocked pending later explicit approvals.
