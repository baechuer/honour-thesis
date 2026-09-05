# External SkillRouter I3C V2 Corrected Neural Matrix Cancelled Partial - 2026-06-21

## Job

| Field | Value |
|---|---|
| Job ID | `6a3773a1953ed90bfb9469b7` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a3773a1953ed90bfb9469b7` |
| Final status | `CANCELED` |
| Reason | Cancelled to stop Hugging Face GPU spend after only two rows had emitted and the job appeared to be spending several hours on the full-document condition. |

## Recovery Check

- HF job logs showed two completed rows.
- Hub result directory `results/skillrouter_eval_core_i3c_v2_neural_matrix_corrected_4096_2026_06_21` had no uploaded result files.
- Therefore, the two rows below are log-recovered only.

## Recovered Rows

| Tier | Layer | Mode | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Query total ms |
|---|---|---|---:|---:|---:|---:|---:|
| Easy | I1 | SkillRouter embedding only | 49.3% | 0.568 | 59.0% | 40.0% | 2318.0 |
| Easy | I1 | SkillRouter embedding top-20 -> reranker | 57.3% | 0.622 | 59.0% | 40.0% | 47548.5 |

## Local Recovery Artifacts

- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_v2_corrected_4096_partial_recovered.md`
- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_v2_corrected_4096_partial_recovered.json`

## Do Not Overclaim

This cancelled job does not answer the I3C-vs-FULL question. It only preserves the corrected Easy/I1 rows.

Next run should split the matrix:

1. `I1,I3C` first, with progress logs and per-row uploads.
2. `FULL` separately.
3. Same method: SkillRouter embedding-only and SkillRouter embedding top-20 -> SkillRouter reranker.
