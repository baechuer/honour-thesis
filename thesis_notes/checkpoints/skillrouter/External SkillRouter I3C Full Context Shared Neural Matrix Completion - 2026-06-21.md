# External SkillRouter I3C Full Context Shared Neural Matrix Completion - 2026-06-21

## Job

| Field | Value |
|---|---|
| Job ID | `6a37d3a23093dba73ce2b60e` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a37d3a23093dba73ce2b60e` |
| Status | Completed |
| Venue | Hugging Face Jobs |
| Hardware | `l4x1` |

## Method

- Representation: `I3C`
- Tiers: `easy`, `hard`
- First stage: SkillRouter embedding over full serialized I3C content
- Reranker: SkillRouter reranker over the same top-20 first-stage candidates
- Embedding max length: `32768`
- Reranker max length: `40960`
- Overlength documents: chunked and max-aggregated
- First-stage retrieval: shared per tier between embedding-only and rerank rows

## Results

| Condition | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Query total ms | Doc emb ms | Chunks | Overlength docs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `easy_I3C_embedding` | 46.7% | 0.531 | 55.1% | 37.3% | 4010.4 | 928597.4 | 78362 | 1 |
| `easy_I3C_rerank` | 57.3% | 0.631 | 55.1% | 37.3% | 60074.6 | 928597.4 | 78362 | 1 |
| `hard_I3C_embedding` | 37.3% | 0.477 | 53.7% | 37.3% | 1063.8 | 35020.1 | 79142 | 1 |
| `hard_I3C_rerank` | 48.0% | 0.563 | 53.7% | 37.3% | 12810.6 | 35020.1 | 79142 | 1 |

## Interpretation Note

Compared with the earlier 4096-token I3C neural rows, the full-context rerun only changes Easy embedding materially: 45.3% to 46.7% Hit@1. Easy rerank remains 57.3% Hit@1, and the Hard rows remain effectively unchanged. This suggests that the earlier I3C neural underperformance was not primarily caused by the 4096-token cap, although the full-context rerun is the methodologically valid row to report.

Recovered local summaries:

- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_fullcontext_shared_2026_06_21_recovered_summary.md`
- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_fullcontext_shared_2026_06_21_recovered_summary.json`
