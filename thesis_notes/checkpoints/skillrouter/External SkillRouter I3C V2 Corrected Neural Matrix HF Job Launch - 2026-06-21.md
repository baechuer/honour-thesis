# External SkillRouter I3C V2 Corrected Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Run the corrected external SkillRouter-Eval-Core neural matrix for the thesis-facing information-layer comparison.

The target comparison is:

- SkillRouter embedding-only retrieval.
- SkillRouter embedding retrieval followed by SkillRouter reranking over the top-20 embedding candidates.

The representation layer is the experimental variable.

## Correction From Previous Neural Run

The earlier job `6a373487953ed90bfb94663e` is now treated as diagnostic only. It should not be used as the final neural comparison because it used the older derived `I2` serialization and 2048-token model caps.

This corrected run uses:

- `I1`: `name | description`
- `FULL`: `name | description | body`
- `I3C`: `name | description | cleaned I3C fields`
- embedding max length: `4096`
- reranker max length: `4096`
- rerank budget: top-20 candidates from SkillRouter embedding
- ranking output limit: top-50

## Execution Venue

| Field | Value |
|---|---|
| Venue | Hugging Face Jobs |
| Account | `baechuer1` |
| Job ID | `6a3773a1953ed90bfb9469b7` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a3773a1953ed90bfb9469b7` |
| Hardware | `l4x1` |
| Timeout | `24h` |
| Required secret | `HF_TOKEN` |
| Runtime device | CUDA GPU |

## Inputs

| Field | Value |
|---|---|
| Dataset repo | `baechuer1/honour-thesis-skillrouter-benchmark-snapshot` |
| Data snapshot | `skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |
| Corrected runner artifact | `job_scripts/run_skillrouter_eval_core_skillrouter_matrix_corrected_2026_06_21.py` |
| Local runner source | `skill_benchmark/scripts/run_skillrouter_eval_core_skillrouter_matrix.py` |

The job downloads the previous data snapshot, overwrites the matrix runner inside the job with the corrected runner artifact, then runs the corrected matrix.

## Expected Outputs

Expected Hub result directory:

`results/skillrouter_eval_core_i3c_v2_neural_matrix_corrected_4096_2026_06_21`

Expected output prefix:

`skillrouter_eval_core_skillrouter_neural_i3c_v2_corrected_4096`

The job prints the compact matrix to logs and uploads:

- full Markdown report
- compact summary JSON
- compact summary Markdown
- gzipped full JSON
- job manifest
- compressed result bundle

## Boundary Rule

Use this run, not the earlier diagnostic neural job, when making final claims about whether I3C improves external SkillRouter-Eval-Core neural selection.

Do not compare the old `I2` row from job `6a373487953ed90bfb94663e` against the paper's full-document result. The corrected `FULL` row is the intended full-document baseline.

## Cancellation Update

Job `6a3773a1953ed90bfb9469b7` was cancelled before completion to stop Hugging Face GPU spend. It emitted only the Easy/I1 embedding and Easy/I1 rerank rows before spending several hours in the next full-document condition.

Partial recovery checkpoint:

`thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Corrected Neural Matrix Cancelled Partial - 2026-06-21.md`

Do not use this cancelled job for the I3C-vs-FULL claim.
