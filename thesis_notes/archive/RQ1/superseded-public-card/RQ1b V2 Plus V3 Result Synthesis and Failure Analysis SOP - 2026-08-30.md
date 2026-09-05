# RQ1b V2+V3 Result Synthesis and Failure-Analysis SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `USER-APPROVED / LOCAL DESCRIPTIVE REVIEW COMPLETE / THESIS UNCHANGED`

Date: 2026-08-30

## Approval Record

On 2026-08-30, the researcher approved this SOP and authorised its local
execution. The approval covers result synthesis and descriptive case review
only. It does **not** authorise changes to frozen scientific inputs, network or
provider calls, hosted computation, or thesis LaTeX/PDF writes.

## Purpose

Produce one auditable synthesis of the completed RQ1b V2+V3 results, then
explain rather than conceal their heterogeneous outcomes. This work is
post-hoc: it cannot alter prompts, cards, masks, strict gold labels,
eligibility, retrievers, cache entries, or the scored rows.

## Evidence Strata

1. **Primary single-field availability experiment.** The unified V2+V3 matrix
   contains 46 scored candidate compositions, 99 strict routing families, 198
   prompt instances, eight conditions and 1,584 rows per retriever. Its unit of
   inference is a candidate composition after direct/paraphrase outcomes are
   averaged. This remains the primary RQ1b result.
2. **Supporting joint-field availability experiment.** Each information set is
   a separate `FULL` versus group-mask paired comparison, with a different
   frozen V2 eligibility intersection plus 12 complete V3 families: task
   specification `85/170/41`, execution/verification `89/178/44`, and
   applicability/capability `82/164/41` for families/prompts/compositions. It
   is not pooled with the primary single-field estimator and cannot attribute a
   joint effect to one member field.
3. **Retriever comparison.** BM25 and Qwen score the same frozen cards and
   prompt lineages, but their numeric margins have different scales. Compare
   direction, Top-1/MRR transitions and within-retriever CIs; do not compare
   absolute margin magnitudes across retrievers.

## Local Analysis Procedure

1. Rehash every source result manifest/output and validate exact row coverage.
2. Build one pair ledger for every `FULL`/mask prompt pair. Retain prompt text,
   V2/V3 provenance, candidate composition, strict gold, winner/ranking, gold
   rank, native score margin and deltas.
3. Assign a deterministic transition class:
   - `routing_regression`: `FULL` Top-1 `1` to mask Top-1 `0`;
   - `mask_recovery`: `0` to `1`;
   - `stable_correct`: `1` to `1`;
   - `stable_wrong`: `0` to `0`.
   A regression is a routing failure for this frozen strict label; a recovery
   is a counterexample to an unqualified “more information is always better”
   claim.
4. Separately quantify rank worsening and margin weakening. A margin decrease
   with stable Top-1 is **not** a routing failure; it is an ordering-fragility
   signal.
5. Produce audit queues without changing scientific inputs:
   - all cross-retriever-concordant regressions;
   - all cross-retriever-concordant recoveries;
   - capped, deterministically ordered retriever-discordant regressions;
   - capped, deterministically ordered large-margin stable-correct cases.
6. For each queued case, prepare exact original card fields and prompt/ranking
   evidence for a descriptive review. Allow only these labels:
   `removed_field_directly_matches_intent`, `residual_field_redundancy`,
   `competitor_residual_advantage`, `lexical_or_embedding_sensitivity`,
   `strict_gold_or_adequacy_concern`, and `insufficient_evidence`. These labels
   describe the observed mechanism; they cannot edit a frozen label.

## Acceptance Criteria

- No network, provider, model, hosted compute or thesis-PDF action occurs.
- Every analysis row rehashes to a manifest-bound source artifact and has a
  unique `retriever × stratum × field/group × family × prompt` key.
- Primary single-field and supporting group strata remain separate in every
  table, figure and conclusion.
- Every reported failure count has matching transition-ledger rows; every
  audit queue item includes enough local evidence to reproduce the review.
- The final narrative reports both regressions and recoveries, states which
  confidence intervals span zero, and does not claim universal field causality.

## Outputs

`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/`

The output package contains a machine-readable pair ledger, summary, audit
queues, method/result Markdown, source hashes and the completed local
descriptive review (`descriptive_case_review.json` and
`DESCRIPTIVE_CASE_REVIEW.md`). Thesis LaTeX/PDF remains unchanged pending
researcher review.
