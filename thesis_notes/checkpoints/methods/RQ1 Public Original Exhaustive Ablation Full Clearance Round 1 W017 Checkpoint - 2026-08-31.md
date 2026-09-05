# RQ1 Public-Original Exhaustive Ablation: Full-Clearance Round 1 W017 Checkpoint

Date: 2026-08-31

## Scope

Local-only blind semantic clearance for the frozen public-original RQ1 field
ablation corpus. This work checks whether deleting a target field from a full
skill document leaves a candidate-specific cue for that same field. It is not
embedding, selector, routing, API, hosted-compute, or thesis-result work.

## Frozen Inputs

- 82 compositions, 265 source artifacts, and 574 composition-field units.
- 574 single-field and 246 joint conditions, giving 2,650 deterministic masks.
- Exact-diff audit passed for all masks with zero unlogged edits.
- No-op and near-empty masks remain reported corpus properties, not exclusions.

## Progress After W017

- Reviewed units: 303 / 574; remaining: 271.
- Reviewed candidate masks: 970.
- Candidate dispositions: 355 `CLEAR`, 615 `RESIDUAL`, 0 `UNCERTAIN`.
- Field unit coverage: input 44; output 43; use condition 44; workflow 43;
  success/verification 43; boundary/not-for 43; dependency/resource 43.
- Every adopted submission passed the exact-span validator before canonical
  ingestion. All W016 and W017 reviewers were closed after adoption.

## Provenance Note

The frozen W015 assignment accidentally contained a delayed duplicate of three
units already ingested from W014. The duplicate reviewer output was not adopted;
the disposition is recorded in
`skill_benchmark/rq1_public_original_exhaustive_ablation_v1/full_clearance/round1_assignments/W015_DISPOSITION.md`.

## Next Gate

Generate W018 from the canonical missing-unit ledger and continue blind
clearance with fresh, non-overlapping reviewers. No scoring may start until the
full 574-unit first-round coverage report is available.
