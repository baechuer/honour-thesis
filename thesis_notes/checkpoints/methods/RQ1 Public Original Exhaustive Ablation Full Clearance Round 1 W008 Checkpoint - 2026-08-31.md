# RQ1 Public-Original Exhaustive Ablation: Full-Clearance Round 1 W008 Checkpoint

Date: 2026-08-31

## Scope

This is local-only semantic clearance for the public-original RQ1 exhaustive
field-ablation corpus. It evaluates whether a deterministic target-field
deletion leaves a candidate-specific cue for the same field. It is not a
selector, embedding, routing, or thesis-result run.

## Frozen Inputs

- 82 compositions, 265 source artifacts, and 574 single-field units.
- 2,650 deterministically generated masks passed exact-diff validation before
  this review round.
- Reviewers receive anonymous masked packets only: no prompts, gold labels,
  source identities, source maps, historical results, or retrieval outputs.

## Round 1 Progress After W008

- Reviewed units: 144 / 574.
- Reviewed candidate masks: 468.
- Candidate dispositions: 173 `CLEAR`, 295 `RESIDUAL`, 0 `UNCERTAIN`.
- Fully clear units by field: boundary 3/20; dependency 2/20; input 2/21;
  output 1/21; success 9/20; use 2/21; workflow 2/21.

Every submitted unit in W001F-W008 passed the exact-span validator and was
ingested into the canonical first-round ledger. Completed reviewers were
closed. A missing explanatory JSON schema was added after W005; it is only a
human-readable companion to the already authoritative validator, so it does
not change earlier validated dispositions.

## Next Gate

Continue first-round blind clearance until all 574 units are covered. Only
after that coverage report may the project inspect residual patterns and design
source-only remapping/remediation with fresh clearance review. No selector,
external API, hosted job, metric calculation, or thesis LaTeX/PDF update is
authorised at this stage.
