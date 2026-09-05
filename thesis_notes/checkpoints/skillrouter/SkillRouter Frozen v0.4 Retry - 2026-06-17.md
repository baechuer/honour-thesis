# SkillRouter Frozen v0.4 Retry - 2026-06-17

## What Changed

- A frozen-v0.4 SkillRouter job was run over 12 conditions:
  - controlled and public-gold strata;
  - R1 flat metadata, R2 structured procedural cards, and full `SKILL.md` representations;
  - SkillRouter embedding-only and SkillRouter embedding plus SkillRouter rerank top-20.
- The first hosted job completed the metric runs but failed at final artifact upload with a Hugging Face write-permission error.
- The summary metrics were recovered from job logs and saved locally:
  - `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_recovered_summary.md`
  - `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_recovered_summary.json`
- A write-permission probe using the local `.env` token succeeded.
- A safer retry job was submitted:
  - job ID: `6a32a10ffb114ff24a388670`
  - URL: `https://huggingface.co/jobs/baechuer1/6a32a10ffb114ff24a388670`
- Retry status: completed successfully.
- Completed at: `2026-06-17T15:28:36.485Z`.
- Uploaded artifacts were downloaded and extracted locally:
  - `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_retry2_summary.md`
  - `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_retry2_summary.json`
  - `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_retry2_outputs.tar.gz`

## Recovered Summary Metrics

| Split | Representation | Method | Top-1 | Top-5 | MRR | Non-main top-1 |
|---|---|---|---:|---:|---:|---:|
| controlled | R1 | embedding | 62.9% | 93.5% | 0.763 | 11.8% |
| controlled | R1 | rerank top-20 | 65.7% | 94.7% | 0.780 | 8.6% |
| controlled | R2 | embedding | 64.5% | 94.7% | 0.783 | 13.1% |
| controlled | R2 | rerank top-20 | 71.0% | 96.7% | 0.823 | 4.9% |
| controlled | full | embedding | 59.2% | 91.4% | 0.737 | 15.1% |
| controlled | full | rerank top-20 | 71.8% | 95.9% | 0.827 | 4.5% |
| public-gold | R1 | embedding | 68.8% | 93.8% | 0.794 | 86.1% |
| public-gold | R1 | rerank top-20 | 70.8% | 92.4% | 0.804 | 89.6% |
| public-gold | R2 | embedding | 75.0% | 94.4% | 0.831 | 89.6% |
| public-gold | R2 | rerank top-20 | 71.5% | 93.1% | 0.805 | 89.6% |
| public-gold | full | embedding | 75.0% | 93.1% | 0.833 | 91.7% |
| public-gold | full | rerank top-20 | 70.1% | 92.4% | 0.804 | 89.6% |

## Interpretation So Far

- SkillRouter is much stronger than generic Qwen on the controlled stratum, especially in top-5 recall.
- R2 structured cards improve over R1 under SkillRouter embedding-only and reranked controlled conditions.
- Full artifact text is not automatically best: it is weaker than R2 for controlled embedding-only, but slightly stronger after SkillRouter reranking.
- On public-gold, SkillRouter embedding is strong over R2 and full artifacts, but SkillRouter reranking reduces strict top-1 for R2 and full text.
- Prompt-level SkillRouter artifacts are now available. Failure-mode analysis has been generated as working notes, but has not yet been incorporated into the thesis body.

## Next Steps

1. Decide how much of the SkillRouter-specific failure-mode analysis belongs in the thesis body:
   - first-stage exclusion;
   - reranker misordering;
   - representation-specific dilution;
   - public/provider cue bias;
   - controlled semantic near-neighbour confusion.
2. Run SkillRouter first-stage plus M6-v1 field-aware reranking at matched top-20, and optionally top-100, budgets.

## Local Failure-Mode Preparation

While the retry job is running, a reusable local analyzer was added:

- `skill_benchmark/scripts/analyze_failure_modes.py`

Current non-SkillRouter failure-mode reports:

- `skill_benchmark/outputs/failure_modes_controlled_qwen_r2_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_controlled_m6v1_tfidf_schema_core_boundary_top20.md`
- `skill_benchmark/outputs/failure_modes_public_gold_qwen_r2_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_public_gold_m6v1_tfidf_flat_task_top20.md`
- `skill_benchmark/outputs/frozen_v0_4_failure_mode_comparison.md`

Current SkillRouter failure-mode reports:

- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_controlled_r1_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_controlled_r2_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_controlled_full_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_public_gold_r1_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_public_gold_r2_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_public_gold_full_rerank_top20.md`
- `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_comparison.md`

Current interpretation:

- Controlled Qwen R2 + Qwen rerank has a first-stage exclusion problem: about 18.0% of controlled prompts never expose the strict gold skill to the reranker.
- Controlled TF-IDF schema + M6-v1 has much better candidate recall, with first-stage exclusion around 2.9%, but still has ordering failures around 27.4%.
- Public-gold Qwen R2 + Qwen rerank has very low first-stage exclusion, around 0.7%, and mostly fails through ordering among plausible public or near-public skills.
- Public-gold M6-v1 remains weaker than Qwen R2 reranking, suggesting that lexical field-aware matching is not robust enough for messy public-authored skills.
