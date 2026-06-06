# M6-v1 SkillRouter Hybrid Summary - 2026-06-05

This file records the hosted hybrid run combining SkillRouter first-stage retrieval with the local M6-v1 field-aware procedural reranker.

- Job ID: `6a2242eee52fdd2a02ed8b51`
- Hardware: Hugging Face Jobs `t4-small`
- First-stage model: `pipizhao/SkillRouter-Embedding-0.6B`
- First-stage representation: full skill artifact
- Reranker: local deterministic M6-v1 field-aware matcher
- Field sets tested: `task`, `task_output_workflow`, `core`, `core_boundary`, `all`
- Note: the remote job printed compact summaries only. Full per-prompt JSON artifacts were not uploaded from the job.

## Best Results

| Prompt set | Candidate budget | Best field set | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| Controlled, 137 prompts | top-20 | `task_output_workflow` | 83.2% | 83.2% | 95.6% | 95.6% | 0.895 | 5.1% |
| Controlled, 137 prompts | top-100 | `task_output_workflow` | 86.9% | 86.9% | 98.5% | 98.5% | 0.927 | 0.7% |
| Public-gold, 32 prompts | top-20 | `task` / `core_boundary` | 62.5% | 68.8% | 93.8-96.9% | 96.9% | 0.765 / 0.762 | 62.5-68.8% |
| Public-gold, 32 prompts | top-100 | `task` | 62.5% | 68.8% | 93.8% | 96.9% | 0.765 | 68.8% |

## Controlled Benchmark Details

| Candidate budget | Field set | Top-1 | Top-5 | MRR | Candidate R@20 | Candidate R@100 | Conditional top-1 | Non-main top-1 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 20 | `task` | 80.3% | 94.9% | 0.872 | 97.8% | 100.0% | 82.1% | 7.3% |
| 20 | `task_output_workflow` | 83.2% | 95.6% | 0.895 | 97.8% | 100.0% | 85.1% | 5.1% |
| 20 | `core` | 81.0% | 97.1% | 0.887 | 97.8% | 100.0% | 82.8% | 5.1% |
| 20 | `core_boundary` | 81.0% | 97.1% | 0.887 | 97.8% | 100.0% | 82.8% | 5.1% |
| 20 | `all` | 81.8% | 96.4% | 0.889 | 97.8% | 100.0% | 83.6% | 7.3% |
| 100 | `task` | 80.3% | 95.6% | 0.876 | 97.8% | 100.0% | 80.3% | 5.1% |
| 100 | `task_output_workflow` | 86.9% | 98.5% | 0.927 | 97.8% | 100.0% | 86.9% | 0.7% |
| 100 | `core` | 85.4% | 98.5% | 0.920 | 97.8% | 100.0% | 85.4% | 0.7% |
| 100 | `core_boundary` | 83.9% | 99.3% | 0.913 | 97.8% | 100.0% | 83.9% | 2.2% |
| 100 | `all` | 81.0% | 97.8% | 0.888 | 97.8% | 100.0% | 81.0% | 6.6% |

## Public-Gold Details

| Candidate budget | Field set | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Candidate R@20 | Candidate R@100 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 20 | `task` | 62.5% | 68.8% | 93.8% | 96.9% | 0.765 | 96.9% | 96.9% |
| 20 | `task_output_workflow` | 59.4% | 65.6% | 96.9% | 96.9% | 0.745 | 96.9% | 96.9% |
| 20 | `core` | 59.4% | 65.6% | 96.9% | 96.9% | 0.760 | 96.9% | 96.9% |
| 20 | `core_boundary` | 62.5% | 68.8% | 96.9% | 96.9% | 0.762 | 96.9% | 96.9% |
| 20 | `all` | 59.4% | 65.6% | 93.8% | 93.8% | 0.750 | 96.9% | 96.9% |
| 100 | `task` | 62.5% | 68.8% | 93.8% | 96.9% | 0.765 | 96.9% | 96.9% |
| 100 | `task_output_workflow` | 56.2% | 62.5% | 96.9% | 100.0% | 0.717 | 96.9% | 96.9% |
| 100 | `core` | 59.4% | 65.6% | 96.9% | 100.0% | 0.755 | 96.9% | 96.9% |
| 100 | `core_boundary` | 59.4% | 65.6% | 96.9% | 100.0% | 0.740 | 96.9% | 96.9% |
| 100 | `all` | 56.2% | 62.5% | 93.8% | 93.8% | 0.724 | 96.9% | 96.9% |

## Interpretation

- Controlled result: this is the strongest current controlled method. SkillRouter first-stage retrieval plus M6-v1 `task_output_workflow` reranking at top-100 reaches 86.9% top-1 and 0.927 MRR.
- Field finding: task/use condition, output, and workflow remain the most useful field group. Adding all fields hurts, which supports the thesis claim that not all structure is equally useful.
- Public-gold result: the same field-aware reranker does not improve public-gold top-1. This suggests the public-skill extraction and field matching layer is not yet robust enough for externally authored skills.
- Candidate recall: SkillRouter candidate recall is very high. Controlled failures are mostly final reranker ordering failures, not first-stage candidate misses.
