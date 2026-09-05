# External SkillRouter I3C Full Context Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Rerun the external SkillRouter-Eval-Core `I3C` neural rows without the earlier 4096-token cap. This follows the SkillRouter paper's full-input framing more closely: use the available model input window, and do not silently drop serialized I3C content.

## Job

| Field | Value |
|---|---|
| Superseded Job ID | `6a37d2413093dba73ce2b60b` |
| Superseded Job URL | `https://huggingface.co/jobs/baechuer1/6a37d2413093dba73ce2b60b` |
| Active Job ID | `6a37d3a23093dba73ce2b60e` |
| Active Job URL | `https://huggingface.co/jobs/baechuer1/6a37d3a23093dba73ce2b60e` |
| Venue | Hugging Face Jobs |
| Hardware | `l4x1` |
| Timeout | `8h` |
| Snapshot | `baechuer1/honour-thesis-skillrouter-benchmark-snapshot/skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |

## Matrix

- Tier: `easy,hard`
- Representation: `I3C`
- Modes: `embedding,rerank`
- Embedding model: `pipizhao/SkillRouter-Embedding-0.6B`
- Reranker model: `pipizhao/SkillRouter-Reranker-0.6B`
- Embedding max length: `32768`
- Reranker max length: `40960`
- Rerank candidates: `20`
- Ranking limit: `50`

## Full-Context Policy

- Serialized I3C documents that fit the model input limit are encoded as complete documents.
- Overlength documents are split into model-limit chunks; retrieval scores are aggregated to the skill level by maximum chunk score.
- Reranker inputs use the same full-content policy: overlength candidate documents are chunked and the candidate score is the maximum chunk score.
- Active replacement job shares the first-stage embedding retrieval per tier between the embedding-only row and the embedding+reranker row.
- Local exact-token check found one I3C outlier, `other/nautilustrader`, at about 42,203 SkillRouter embedder tokens; this row requires chunking.
- Hub upload is disabled because dataset writes are returning `403`; final rows must be recovered from job logs.

## Update

- Job `6a37d2413093dba73ce2b60b` was cancelled before any condition completed.
- Replacement job `6a37d3a23093dba73ce2b60e` completed successfully. Final recovered rows are recorded in `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C Full Context Shared Neural Matrix Completion - 2026-06-21.md`.
