# RQ1 82-Registry S3 Blind Residual Closure

Status: `CLOSED / FULL-ORIGINAL REMOVAL FEASIBILITY / NO SELECTOR EXECUTION`

## What Closed

The 82-composition, 265-document public-original branch completed its blind
residual gate. S1 source-only mapping and S2 exact-diff technical checks had
already completed without using prompts, gold labels, retrieval scores or
external services. S3 reviewed 183 single-field composition conditions in 61
anonymous batches. Reviewers saw only the masked candidate documents, the
target field category, and the response schema.

Every reissued submission passed the independent validator before it was
canonicalised. An early six-batch interface wave was discarded before
canonicalisation because the item-local target field was missing; it contributes
no decision to this closure.

## Residual Gate Result

| Field | S2 materialised compositions | S3 clear | S3 residual | S3 uncertain |
| --- | ---: | ---: | ---: | ---: |
| Use condition | 21 | 2 | 19 | 0 |
| Input/precondition | 19 | 2 | 17 | 0 |
| Output artifact | 25 | 3 | 21 | 1 |
| Workflow/procedure | 22 | 0 | 22 | 0 |
| Success/verification | 32 | 11 | 21 | 0 |
| Boundary/not-for | 37 | 15 | 22 | 0 |
| Dependency/resource | 27 | 0 | 27 | 0 |

Only 33 of 183 single-field conditions are clear. All three pre-specified
joint groups have zero clear compositions because every technical group has at
least one component field that is residual, uncertain, not map-ready, or the
recorded S2 edit conflict.

## Decision

The full-original branch stops before strict-family linkage, denominator
freezing and selectors. A survivor-only experiment would contain no joint
group and only 0--15 conditions per single field; it would not test the
intended seven-field/three-group public RQ1 comparison. No BM25, Qwen,
embedding, API, hosted job, routing metric or thesis LaTeX/PDF result was run.

This is a feasibility result about conservative source-document deletion: the
operational facts to be removed remain explicitly distributed through natural
skill documents. It is not a field-effect estimate and does not claim that a
field is unimportant for routing.

## Evidence

- S3 SOP: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document S3 Blind Residual Review SOP - 2026-08-31.md`
- Single-field ledger: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_ledger/blind_residual_ledger.json`
- Derived group ledger: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_ledger/group_eligibility_ledger.json`
- Canonical review batches: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_submissions/canonical/`
