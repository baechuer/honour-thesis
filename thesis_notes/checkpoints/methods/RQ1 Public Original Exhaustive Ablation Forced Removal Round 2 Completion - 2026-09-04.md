# RQ1 Public-Original Exhaustive Ablation: Forced-Removal Round 2 Completion

Date: 2026-09-04

## Completion Status

Fresh source/prompt/gold/map/selector-blind Round-2 clearance is complete for
the frozen 82-composition primary frame. The parent-thread validator re-ran
over every canonical record after ingestion and passed all 574 files.

| Measure | Count |
|---|---:|
| Field units | 574 / 574 |
| Compositions | 82 / 82 |
| Candidate cards | 1,855 / 1,855 |
| `CLEAR` candidate decisions | 1,464 |
| `RESIDUAL` candidate decisions | 383 |
| `UNCERTAIN` candidate decisions | 8 |
| Units with every candidate `CLEAR` | 377 |

## Field-Level Clearance

| Target field | Fully clear units / 82 | Clear cards / 265 | Residual cards | Uncertain cards |
|---|---:|---:|---:|---:|
| Boundary / not-for | 72 | 249 | 16 | 0 |
| Dependency / resource | 44 | 184 | 75 | 6 |
| Input / precondition | 40 | 187 | 77 | 1 |
| Output / artifact | 44 | 183 | 82 | 0 |
| Success / verification | 59 | 229 | 35 | 1 |
| Use condition | 57 | 207 | 58 | 0 |
| Workflow / procedure | 61 | 225 | 40 | 0 |

## What This Establishes

Round 2 materially removes many known Round-1 residual expressions, but it
does not yet establish a clean isolated-field representation for all units.
Only the 377 all-candidate-clear units are eligible for a strict clean-field
stratum after the protocol's later denominator decision. The 383 residual and
8 uncertain cards are retained as auditable overlap evidence rather than
discarded.

This remains a clearance result only. It does not authorise selector scoring,
BM25, Qwen, external APIs, hosted work, or thesis/PDF result writing.

## Round 3 Boundary

Round 3 may deterministically remove only the exact spans cited in these 383
canonical Round-2 `RESIDUAL` records. It must copy Round-2 `CLEAR` cards
unchanged. It cannot delete an `UNCERTAIN` card without new exact evidence, so
those eight cards remain explicitly non-clean unless a future blind reviewer
supplies line-addressable residual evidence. A new exact-diff audit and fresh
blind clearance are mandatory before any Round-3 card is treated as clean.

## Canonical Evidence

- Round-2 SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND2_SOP.md`
- Round-2 masks: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_masks/`
- Round-2 canonical clearance: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_clearance/canonical_round2/`
