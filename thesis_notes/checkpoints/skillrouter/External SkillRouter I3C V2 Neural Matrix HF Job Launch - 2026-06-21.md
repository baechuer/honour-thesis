# External SkillRouter I3C V2 Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Run the external SkillRouter-Eval-Core neural matrix with the released SkillRouter embedding and reranking models against the full Easy/Hard tier I1/I2/I3C representations.

This is a hosted GPU experiment. It is not a local Mac run. Local work is limited to packaging the snapshot, uploading it to Hugging Face, and submitting/monitoring the job.

## Execution Venue

| Field | Value |
|---|---|
| Venue | Hugging Face Jobs |
| Account | `baechuer1` |
| Job ID | `6a373487953ed90bfb94663e` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a373487953ed90bfb94663e` |
| Hardware | `l4x1` |
| Timeout | `24h` |
| Required secret | `HF_TOKEN` |
| Runtime device | CUDA GPU |

## Snapshot

| Field | Value |
|---|---|
| Dataset repo | `baechuer1/honour-thesis-skillrouter-benchmark-snapshot` |
| Snapshot artifact | `skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |
| Snapshot upload URL | `https://huggingface.co/datasets/baechuer1/honour-thesis-skillrouter-benchmark-snapshot/blob/main/skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz` |
| Local snapshot size | `417M` compressed |
| Included runner | `skill_benchmark/scripts/run_skillrouter_eval_core_skillrouter_matrix.py` |

The snapshot includes only the runner scripts and the external SkillRouter-Eval-Core artifacts needed for the matrix:

- `tasks_scored.jsonl`
- `relevance.json`
- `hard_only_skill_ids.txt`
- Easy/Hard `I1`, `I2`, and `I3C` representation JSONL files
- selector/helper scripts required by the matrix runner

## Matrix

| Dimension | Values |
|---|---|
| Tiers | `easy`, `hard` |
| Information layers | `I1`, `I2`, `I3C` |
| Modes | SkillRouter embedding-only, SkillRouter embedding + SkillRouter rerank |
| Rerank budget | top-20 |
| Ranking output limit | top-50 |
| Metrics | Hit@1, MRR@10, nDCG@10, Recall@5/10/20/50, FullCoverage@5/10/20/50, hard-only top-1, approximate selector-visible tokens, runtime |

## Expected Outputs

Results are expected under the same dataset repo:

`results/skillrouter_eval_core_i3c_v2_neural_matrix_2026_06_21`

Expected output prefix:

`skillrouter_eval_core_skillrouter_neural_i3c_v2`

The job wrapper uploads:

- Markdown report
- JSON report
- job manifest
- compressed result bundle

## Boundary Rule

Do not run the full SkillRouter matrix locally on the laptop. A local SkillRouter run is only a smoke test if it uses a tiny prompt/skill subset and is explicitly labelled as smoke-test output. Full matrix results must come from Hugging Face Jobs or an equivalent hosted GPU environment.

Do not mix this external neural matrix with:

- local frozen-v0.4 controlled/public-gold results;
- provider/API Qwen or DeepSeek runs;
- I3M paid-model extraction;
- I3C subagent extraction QA checkpoints.

This job is an external verification run for the thesis information-layer claim: whether cleaned I3C structured fields remain useful under the released SkillRouter neural retriever/reranker on SkillRouter-Eval-Core.
