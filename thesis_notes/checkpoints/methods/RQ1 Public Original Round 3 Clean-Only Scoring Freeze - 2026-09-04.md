# RQ1 Public Original Round 3 Clean-Only Scoring Freeze

Date: 2026-09-04

## Status

`F0 FREEZE COMPLETE / SELECTORS NOT RUN`

## What Was Frozen

The public-original RQ1 test now has one frozen clean-only frame. It compares
each exact public original (`FULL_ORIGINAL`) with its exact Round-3
field-removal mask (`REMOVE_<FIELD>_R3`) only when the canonical blind ledger
marks every candidate in that composition-field unit as `CLEAR`.

The freeze also requires a deterministic binding to a previously frozen strict
singleton-gold routing family with both a `direct` and a `paraphrase` prompt.
There is no repair or selection after looking at a retrieval score.

## Frozen Frame

| Item | Count |
| --- | ---: |
| Source compositions | 82 |
| Source candidate documents | 265 |
| Round-3 composition-field units | 574 |
| Fully clear units before prompt/gold binding | 439 |
| Frozen complete-case composition-family cases | 1,078 |
| Frozen prompt rows | 2,156 |
| All-seven-fields-clear compositions with prompt binding | 28 |

## Primary Statistical Units

The rows above are not all independent observations. Each composition may have
one to four strict routing families, and each family has two repeated prompt
forms. The primary estimate therefore gives each eligible composition one
equal-weight contribution after averaging its direct/paraphrase prompts and
then its eligible routing families. The paired bootstrap resamples complete
compositions, not prompt rows.

| Field | Eligible compositions | Frozen routing families | Prompt rows |
| --- | ---: | ---: | ---: |
| Use condition | 57 | 158 | 316 |
| Input / precondition | 53 | 139 | 278 |
| Output / artifact | 49 | 129 | 258 |
| Workflow / procedure | 63 | 169 | 338 |
| Success / verification | 59 | 160 | 320 |
| Boundary / not-for | 69 | 185 | 370 |
| Dependency / resource | 52 | 138 | 276 |

All fields exceed the predeclared 30-composition / 60-prompt minimum for a
primary field-specific result. The denominator remains field-specific; the
numbers must not be pooled as one global RQ1 score.

## Integrity Checks

The freeze builder and independent validator both passed. They verified:

- every retained original source SHA-256;
- every retained Round-3 mask SHA-256;
- the aggregate SHA-256 of all 574 canonical clearance records;
- candidate labels/order, field identity, and strict-gold binding;
- exactly one `direct` and one `paraphrase` prompt per retained family;
- no duplicate scoring case; and
- all retained candidates are `CLEAR`.

Frozen output checksums:

```text
a87dc0529fad8ee1cf2c19ff762746c7c9affe18b7145b3b98e7f5476c871861  clean_only_scoring_freeze_v1.json
46405c7c54785f532ccd654dbe84284e06c9c2e135fc59af1fc42db68a8341cc  eligibility_exclusions.json
b3c194a1db958e6e60432e7c011591c14191942c1a49d8a170d67c9cf4fcf4a8  freeze_summary.json
```

## What Has Not Happened

No BM25 score, dense embedding, API call, hosted job, retrieval metric, or
thesis/PDF result has been produced. `RESIDUAL` and `UNCERTAIN` units remain
in the exclusion ledger as overlap/feasibility evidence and are not a negative
field-effect result.

## Next SOP Steps

1. Run the local, deterministic BM25 scorer against the frozen cases only.
2. Validate its complete row coverage and paired condition identity.
3. Review the local BM25 package before preparing an exact Qwen payload.
4. Construct, but do not send, the Qwen `text-embedding-v4` preflight.
5. Obtain separate explicit authorisation for any newly outbound document or
   prompt text, then run dense retrieval and the frozen paired analysis.

The F1 runner has been syntax-checked, passed a synthetic lexical/tie-break
self-test, and passed a no-scoring dry run over the exact freeze. The dry run
plans 1,078 cases x 2 prompt variants x 2 conditions = 4,312 ranking rows; it
does not read scores or create a result directory. The first actual BM25 run
remains a separate result-producing step.

## Evidence

- Method SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md`
- Freeze root: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/`
- Builder: `skill_benchmark/scripts/build_rq1_public_original_round3_clean_scoring_freeze.mjs`
- Validator: `skill_benchmark/scripts/validate_rq1_public_original_round3_clean_scoring_freeze.mjs`
- Local F1 runner: `skill_benchmark/scripts/run_rq1_public_original_round3_clean_bm25.mjs`
