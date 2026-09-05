# Local Matrix Rerun After Public Source Correction - 2026-06-23

This checkpoint records the local matrix rerun after two corrections:

- Public imported skills now use upstream `source/SKILL.original.md` for public full-text/I2 comparisons and public R1/R2/R3 export where available.
- The 32 public-style controlled skills were regenerated as messier public-document-style skills while preserving routing-critical information.

## Completed

- Rebuilt local representations: `skill_benchmark/representations/manifest.json` reports 2433 skills, 2433 R1 rows, 2433 R2 rows, 2433 R3 rows, and 62032 R4 edges.
- Integrity check passed: `skill_benchmark/outputs/benchmark_integrity_report.md/json`.
- Reran crossed lexical matrix: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md/json`.
- Reran local offline selectors:
  - `skill_benchmark/outputs/offline_selector_evaluation_2433_245_local.md/json`
  - `skill_benchmark/outputs/public_gold_offline_selector_evaluation_2433_144_local.md/json`
- Reran field ablations:
  - `skill_benchmark/outputs/frozen_v0_4_controlled_field_ablation.md/json`
  - `skill_benchmark/outputs/frozen_v0_4_public_gold_field_ablation.md/json`
- Reran Qwen provider rows for controlled and public-gold, all I1/I3H/I2 combinations:
  - embedding-only
  - Qwen top-20 rerank
  - local-schema top-20 diagnostic
- Reran Qwen-only M6-v2 field-specific `semantic_all` rows and regenerated fixed task-heavy reports:
  - `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md/json`
  - `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md/json`
- Rebuilt consolidated matrix:
  - `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md/json`
- Wrote compact refreshed summary:
  - `skill_benchmark/outputs/frozen_v0_4_refreshed_matrix_summary_2026_06_23.md`

## Headline Top-1 Results

| Stratum | Method | I1 | I3H/R2 | I2/full |
|---|---|---:|---:|---:|
| Controlled | BM25 | 55.1% | 58.0% | 66.5% |
| Controlled | TF-IDF | 52.6% | 59.6% | 69.4% |
| Controlled | Qwen embedding | 33.9% | 40.4% | 42.4% |
| Controlled | Qwen + Qwen rerank | 51.0% | 58.4% | 62.9% |
| Controlled | M6-v2 fixed task-heavy, Qwen only | 35.5% | 38.4% | 40.8% |
| Public-gold | BM25 | 55.6% | 54.9% | 59.0% |
| Public-gold | TF-IDF | 56.9% | 50.7% | 48.6% |
| Public-gold | Qwen embedding | 57.6% | 61.8% | 70.8% |
| Public-gold | Qwen + Qwen rerank | 73.6% | 70.8% | 72.9% |
| Public-gold | M6-v2 fixed task-heavy, Qwen only | 54.9% | 56.9% | 59.7% |

## Interpretation

- Controlled Qwen rows still support the claim that I3H/R2 improves over I1 under the same dense retriever and under the same learned reranker.
- Full source text is now a strong comparator, especially on controlled lexical rows and Qwen full-document conditions. It should be treated as a meaningful upper-information comparator, not a straw baseline.
- Public-gold remains mixed because public names/descriptions and provider/tool cues are highly informative. I1 can be very strong under Qwen rerank, while I2/full is strongest for Qwen embedding after switching to upstream originals.
- M6-v2 fixed task-heavy remains an interpretable diagnostic of field signal. It does not replace Qwen learned reranking.
- SkillRouter local rows were not rerun in this pass. Keep pre-correction local SkillRouter full/I2 and SkillRouter M6-v2 rows caveated until a corrected-source SkillRouter rerun is performed.
- Local I3C still does not exist. These local I3 rows are I3H/R2/R3, not Codex/ChatGPT I3C.
