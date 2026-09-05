# External SkillRouter I3C V2 Remaining I1/I3C Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Run only the corrected neural matrix cells that remain useful after cancelled job `6a3773a1953ed90bfb9469b7`.

The recovered rows from that cancelled job are:

- `easy_I1_embedding`
- `easy_I1_rerank`

This run skips those rows and runs the remaining `I1`/`I3C` cells first. The `FULL` full-document baseline is intentionally excluded from this pass because it is the expensive baseline and should be run separately.

## Execution Venue

| Field | Value |
|---|---|
| Venue | Hugging Face Jobs |
| Account | `baechuer1` |
| Job ID | `6a37bdd33093dba73ce2b559` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a37bdd33093dba73ce2b559` |
| Hardware | `l4x1` |
| Timeout | `8h` |
| Required secret | `HF_TOKEN` |
| Runtime device | CUDA GPU |
| Quiet progress | disabled |

## Inputs

| Field | Value |
|---|---|
| Dataset repo | `baechuer1/honour-thesis-skillrouter-benchmark-snapshot` |
| Data snapshot | `skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |
| Runner artifact | `job_scripts/run_skillrouter_eval_core_skillrouter_matrix_corrected_2026_06_21.py` |

The job downloads the existing snapshot and corrected runner, then runs each condition as a separate subprocess so completed cells can be uploaded before later cells begin.

## Condition Order

1. `easy_I3C_embedding`
2. `easy_I3C_rerank`
3. `hard_I1_embedding`
4. `hard_I1_rerank`
5. `hard_I3C_embedding`
6. `hard_I3C_rerank`

## Output Persistence

Hub output directory:

`results/skillrouter_eval_core_i3c_v2_neural_matrix_remaining_i1_i3c_4096_2026_06_21`

The wrapper uploads after every completed condition:

- condition JSON
- condition Markdown
- cumulative summary JSON
- cumulative summary Markdown

If the job is stopped during a later condition, previous completed condition outputs should remain recoverable from the Hub.

## Boundary Rule

This job is not the full corrected matrix because it excludes `FULL`. Use it for the I1-vs-I3C corrected neural comparison after merging with the two recovered Easy/I1 rows. Run `FULL` separately for the full-document baseline.
