# RQ1 Public Original Round 3 BM25 Result

Date: 2026-09-04

## Status

`F1 LOCAL BM25 COMPLETE AND VALIDATED / QWEN NOT YET PREFLIGHTED`

## What Was Tested

This is the frozen naturalistic public-original RQ1 test. Within the same
three- or four-candidate composition and the same strict prompt/gold family,
local BM25 ranked:

1. exact public originals (`FULL_ORIGINAL`); and
2. the corresponding canonical Round-3 card after complete removal of one
   target field (`REMOVE_<FIELD>_R3`).

Only clean-only units entered: every candidate was independently marked
`CLEAR` for the removed field. The intervention can leave a skill incomplete
or non-executable; this is permitted because the outcome is routing, not
execution.

## Integrity

- Frozen cases: 1,078 composition-family cases, 2,156 repeated prompt rows.
- Result rows: 4,312 = case x direct/paraphrase x full/removed condition.
- Independent result validator: `PASS`; no missing or duplicate paired row,
  candidate-label drift, gold drift, rank error, or freeze-hash mismatch.
- Result SHA-256:
  `010fee2f8f548bcd22c08f2eb8b65bdece0850c2cce231fdad58f178967ee1d3`.
- Local only: no external text transfer, query rewrite, reranker, hosted job,
  or Qwen embedding occurred.

## Primary BM25 Results

Each estimate gives equal weight to each eligible composition: direct and
paraphrase prompts are first averaged within each routing family, then
families are averaged within a composition. The 95% interval is from 10,000
seeded composition-clustered paired bootstrap resamples. It is an interval,
not a p-value, and fields retain distinct complete-case denominators.

| Removed field | Compositions | Full Hit@1 | Removed Hit@1 | Full - removed Hit@1 (95% CI) | MRR change |
| --- | ---: | ---: | ---: | ---: | ---: |
| Use condition | 57 | 0.784 | 0.670 | +0.114 [0.067, 0.167] | +0.070 |
| Input / precondition | 53 | 0.778 | 0.679 | +0.098 [0.051, 0.149] | +0.058 |
| Output / artifact | 49 | 0.772 | 0.650 | +0.122 [0.065, 0.187] | +0.073 |
| Workflow / procedure | 63 | 0.779 | 0.628 | +0.151 [0.086, 0.215] | +0.091 |
| Success / verification | 59 | 0.794 | 0.677 | +0.117 [0.059, 0.182] | +0.065 |
| Boundary / not-for | 69 | 0.775 | 0.751 | +0.024 [-0.014, 0.064] | +0.016 |
| Dependency / resource | 52 | 0.785 | 0.695 | +0.091 [0.046, 0.139] | +0.057 |

For use condition, input/precondition, output/artifact, workflow/procedure,
success/verification, and dependency/resource, the paired Hit@1 bootstrap
interval excludes zero. Workflow/procedure has the largest observed lexical
Top-1 decline. For boundary/not-for, the Hit@1 and MRR intervals include zero;
its current BM25 evidence is therefore insufficient to claim a stable Top-1
routing effect.

## Diagnostics and Failure Pattern

The direct and paraphrase slices point in the same direction for all seven
fields. The count below is descriptive prompt-row transition evidence only,
not an independent-sample significance calculation.

| Removed field | Full correct -> removed wrong | Full wrong -> removed correct |
| --- | ---: | ---: |
| Use condition | 32 | 2 |
| Input / precondition | 32 | 4 |
| Output / artifact | 28 | 4 |
| Workflow / procedure | 75 | 17 |
| Success / verification | 33 | 5 |
| Boundary / not-for | 21 | 11 |
| Dependency / resource | 31 | 3 |

The boundary/not-for condition still has a positive BM25 gold-vs-leading-wrong
margin change of +0.552 [0.151, 0.950], but it rarely changes the winning
candidate enough to yield a stable Top-1 effect. This is the right nuanced
interpretation: the field can contribute lexical support without being a
decisive routing signal under these prompts and candidate sets.

## Claim Boundary

This result supports a retriever-specific statement: for cleanly isolated
instances in these public-skill compositions, six documented fields provide
useful lexical routing information. It does not show that any field is the
only reason an original skill is selected, that the edited documents are
runnable, that unscored `RESIDUAL`/`UNCERTAIN` units have no value, or that the
result necessarily replicates for dense retrieval or another library.

## Next Gate

Construct an exact, local-only Qwen `text-embedding-v4` preflight from the
same freeze. It must state unique query/document text counts, cache validity,
maximum calls and token proxy before asking for a separate external-transfer
authorisation. Do not write this BM25 result into thesis LaTex/PDF until the
Qwen twin is available for review.

## Evidence

- Freeze: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/`
- BM25 rows: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_bm25_results/bm25_results.json`
- Paired analysis: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_bm25_results/analysis/bm25_paired_analysis.json`
- BM25 runner: `skill_benchmark/scripts/run_rq1_public_original_round3_clean_bm25.mjs`
- Row validator: `skill_benchmark/scripts/validate_rq1_public_original_round3_clean_bm25_results.mjs`
- Analysis validator: `skill_benchmark/scripts/validate_rq1_public_original_round3_clean_bm25_analysis.mjs`
