# External SkillRouter I2 Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Run the external SkillRouter-Eval-Core `I2` full-document baseline under the same released SkillRouter embedding and SkillRouter reranker setup used for the recovered I1/I3C neural rows.

Update: this job was cancelled before completion because it used the earlier 4096-token cap. It is invalid as a full-context/full-document comparator and should not be reported as a result row.

## Job

| Field | Value |
|---|---|
| Job ID | `6a37cf7f953ed90bfb946ea4` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a37cf7f953ed90bfb946ea4` |
| Final status | Cancelled |
| Venue | Hugging Face Jobs |
| Hardware | `l4x1` |
| Timeout | `8h` |
| Snapshot | `baechuer1/honour-thesis-skillrouter-benchmark-snapshot/skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |
| Runner artifact | `job_scripts/run_skillrouter_eval_core_skillrouter_matrix_corrected_2026_06_21.py` |

## Matrix

- Tier: `easy,hard`
- Representation: `I2`
- Modes: `embedding,rerank`
- Embedding model: `pipizhao/SkillRouter-Embedding-0.6B`
- Reranker model: `pipizhao/SkillRouter-Reranker-0.6B`
- Embedding max length: `4096` (invalid for full-context baseline)
- Reranker max length: `4096` (invalid for full-context baseline)
- Rerank candidates: `20`
- Ranking limit: `50`
- Embedding batch size: `8`

## Operational Notes

- Quiet progress is disabled.
- Easy and Hard are run in the same job so the Hard condition can reuse the Easy full-document embedding cache and only encode the 780 Hard-only extras.
- Hub upload is disabled because the same dataset repo write path is currently returning `403`; the final summary table is printed to job logs and must be recovered from there.
- This is the expensive `I2`/full-document comparator for the completed I1/I3C external neural rows.
- Do not use this run for thesis claims. Replacement should use model-limit context: SkillRouter embedding `32768`, SkillRouter reranker `40960`, with chunking if any document exceeds the model limit.
