# RQ1a Researcher Review Protocol

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_RETROSPECTIVE_REVIEW`.** Retains the retrospective author-confirmation record. The prospective gold-hidden review workspace at skill_benchmark/rq1_human_review/2026-09-04/ is now the active human-review route. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `AUTHOR REVIEW CONFIRMED / NOT INDEPENDENT OR BLINDED ANNOTATION`

Date: 2026-08-30

## Purpose

RQ1a has seven researcher-authored, mechanically rubric-checked controlled
field-isolation suites. This protocol records the author's iterative
researcher sign-off for the core clusters. It does not establish independent or
blinded annotation.

The review is not a new selector run and does not alter a frozen score. It
checks whether the intended label and controlled contrast remain defensible
under close reading of the unit, prompts and three sibling skills.

## Scope

- Seven core RQ1a fields: use condition, input/precondition, output/artifact,
  dependency/resource, boundary/not-for, success/verification, and
  workflow/procedure.
- 50 clusters per field; 350 core clusters total.
- The `examples_test` suite is outside this ledger because it is a
  negative-control/support-information experiment, not a primary field suite.
- The review source of truth is
  `skill_benchmark/rq1a_field_discriminability/human_review_2026-08-30/`.

## Per-Cluster Sign-Off

For a cluster, the researcher reads its `unit.json`, all prompt variants and
the rendered three sibling skills. The ledger records the five decisions:

1. Is the intended gold skill uniquely fully adequate for every prompt variant?
2. Are both alternatives plausible near-neighbours rather than irrelevant
   distractors?
3. Is the named target field the decisive skill-side distinction while
   non-target shared context remains genuinely shared?
4. Do the prompt variants preserve the same intended gold without title/name
   leakage or copied distinctive wording?
5. Should the cluster remain in the primary RQ1a analysis?

Record the researcher name, date and a short rationale. A negative answer may
retain the unit as an excluded audit record, but it must set
`retain_in_primary_rq1a` to `false` and state the reason. Frozen selector rows
are never deleted or silently relabelled.

## Reporting Rule

The 350 core rows are retrospectively recorded as author-reviewed and retained
after iterative design review. They may be described as "author-reviewed" or
"researcher-reviewed by the author". This protocol does not create an
independent or blinded human annotation claim. Independent review would require
a separately planned, de-identified annotation study.

## Current State

- Core clusters in ledger: 350
- Author-reviewed retained clusters: 350
- Pending clusters: 0
- Confirmation receipt: `author_review_confirmation_receipt.json`
- Selector reruns, label changes and external calls authorised by this protocol: none

## Related Evidence

- Controlled units: `skill_benchmark/rq1a_field_discriminability/<field>/clusters/<cluster>/unit.json`
- Row-level results: `skill_benchmark/outputs/rq1a_*_bm25_qwen_embedding_rows.jsonl`
- Cluster-bootstrap/leading-negative analysis:
  `skill_benchmark/outputs/rq1a_cluster_uncertainty_2026-08-30/`
- Author-review ledger:
  `skill_benchmark/rq1a_field_discriminability/human_review_2026-08-30/review_ledger.jsonl`
