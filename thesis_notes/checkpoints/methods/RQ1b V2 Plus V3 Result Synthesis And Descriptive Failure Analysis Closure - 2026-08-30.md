# RQ1b V2+V3 Result Synthesis and Descriptive Failure Analysis Closure

Date: 2026-08-30

Status: `COMPLETE / LOCAL-ONLY / THESIS UNCHANGED`

## Scope

The researcher approved the frozen RQ1b V2+V3 synthesis and descriptive
failure-analysis SOP. This closure only validates and explains completed,
manifest-bound outcomes. It does not modify candidate cards, masks, prompts,
strict gold labels, eligibility, selector results or the thesis LaTeX/PDF.

## Completed Inputs and Checks

- Primary single-field and supporting joint-group result artifacts were
  revalidated through the synthesis package.
- The pair ledger contains 3,796 unique `retriever x stratum x analysis x
  family x prompt` records: 2,772 primary and 1,024 supporting records.
- The predeclared audit queues contain 13 cross-retriever-concordant routing
  regressions and 3 cross-retriever-concordant mask recoveries.
- The descriptive review contains exactly those 16 cases, no more and no less;
  its source hashes bind to `audit_queues.json`
  `65335447a9dea7ef28e95565c6ae41746583274b1220385e764db89cab44e879`
  and `pair_ledger.jsonl`
  `174aeb84bdc804457f1051408badd27b0db5816f6bee8261e5ac1bc9a431ce4b`.
- `python3 skill_benchmark/scripts/analyze_rq1b_v2_v3_result_failure_analysis.py --check`
  passed with 3,796 pair records, 16 descriptive-review cases, 13 regressions,
  3 recoveries and zero network calls.

## Descriptive Findings

- Eleven of the 13 concordant regressions include a withheld field or field
  group that directly expresses the request's distinguishing operational
  condition. In ten of those cases, a nearby alternative retains generic but
  request-adjacent residual text and becomes the winner after the target loses
  its specific evidence.
- Two gene-list cases are explicit counterexamples: their unmasked input, use
  and output text still identify the strict target, while the removed command
  entry-point or exit-code material does not express the request's distinction.
  Their post-mask switches are recorded as lexical/embedding sensitivity, not
  as support for universal workflow or verification-field causality.
- All three concordant recoveries remain in the evidence. They show that
  remaining fields can sometimes compensate for a withheld field and that more
  full-card information does not unconditionally improve native retrieval.
- No case was relabelled or removed. No case was marked a strict-gold or
  adequacy concern during this limited descriptive review; this does not replace
  the benchmark's prior strict-label audit.

## Claim Boundary

The result supports a bounded RQ1b interpretation: natural public skill cards
often distribute useful routing evidence across fields; a field/group can be
decisive where it is the only explicit operational distinction, but individual
field removals do not have a universal corpus-wide Top-1 or MRR effect. The
primary single-field and supporting group strata remain separate.

## Evidence

- SOP: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Result Synthesis and Failure Analysis SOP - 2026-08-30.md`
- Pair ledger and queues: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/`
- Case review: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/DESCRIPTIVE_CASE_REVIEW.md`

No thesis prose or result table was written in this closure.
