# RQ1 Public-Original Exhaustive Ablation: Forced-Removal Round 3 Completion

Date: 2026-09-04

## Status

`FULL FRESH BLIND CLEARANCE COMPLETE / NO SCORING`

## What This Round Did

Round 3 began from the frozen Round-2 masks. For every candidate that the
canonical Round-2 blind ledger marked `RESIDUAL`, it deleted only the exact
line-addressable spans cited in that ledger. Round-2 `CLEAR` and `UNCERTAIN`
cards were copied unchanged. This remains a routing-only intervention: a
masked document may be damaged or not runnable, because the question is
whether removal changes selection information rather than whether the edited
skill can execute.

The local materialisation covered all 574 composition-field units and 1,855
candidate cards. It deleted 573 exact cited lines, and the exact-diff audit
found zero unlogged changes.

## Fresh Blind-Clearance Result

Fresh reviewers saw only anonymous Round-3 cards and the target-field name;
they did not receive originals, source identity, prompts, gold labels, maps,
prior ledgers, selectors or metrics. The parent re-ran the submission validator
for every canonical record.

| Check | Result |
| --- | ---: |
| Expected field units | 574 |
| Canonical records | 574 |
| Missing or duplicate unit records | 0 |
| Candidate-label / identity mismatches | 0 |
| Parent validator passes | 574 / 574 |
| Candidate cards | 1,855 |
| `CLEAR` cards | 1,609 |
| `RESIDUAL` cards | 232 |
| `UNCERTAIN` cards | 14 |
| Units clear across every candidate | 439 / 574 |

## Fully-Clear Units by Field

| Target field | Fully clear / 82 |
| --- | ---: |
| Boundary / not-for | 77 |
| Dependency / resource | 55 |
| Input / precondition | 58 |
| Output / artifact | 55 |
| Success / verification | 65 |
| Use condition | 62 |
| Workflow / procedure | 67 |

## Interpretation Boundary

Round 3 improves the clearance state relative to the Round-2 ledger, but it
does **not** establish an RQ1 routing effect. A `RESIDUAL` or `UNCERTAIN`
record means the isolated-field claim is not available for that candidate/unit;
it does not mean the field lacks routing value. Conversely, a fully clear unit
is a potential member of a future clean-only denominator, not a score or an
observed retrieval gain.

No selector, embedding API, hosted job, metric calculation, or thesis/PDF
result writing occurred in this round.

## Evidence

- SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND3_SOP.md`
- Round-3 manifest: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/FORCED_ROUND3_MASK_MANIFEST.json`
- Exact-diff audit: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_masks/audit/exact_diff_audit.json`
- Canonical blind ledger: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_clearance/canonical_round3/`
- Full parent validation transcript: `/tmp/rq1_round3_canonical_validator.jsonl` (574 records)

## Next Gate

The next action is a method decision, not automatic scoring. The project must
either:

1. construct a further forced-removal round using only the 232 fresh,
   line-addressable `RESIDUAL` findings; or
2. freeze an explicit clean-only complete-case selection denominator, keeping
   non-clear units as an overlap/feasibility stratum rather than silently
   dropping them.

Either option must preserve this Round-3 ledger and state the selection rule
before any BM25, embedding or reranker result is calculated.
