# Public Gold 82 Provider Rerun - 2026-06-05

Purpose:

- Rerun stronger provider and SkillRouter methods on the cleaned 82-prompt public-gold stratum.
- Replace the older 32-prompt public-gold provider numbers with same-stratum results.
- Check whether the public-gold findings support or challenge the controlled benchmark results.

Scope:

- Prompts: `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`
- Prompt count: 82
- Candidate library: 2401 skills, `current_full`
- Acceptable alternatives: `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`
- Qwen model: `text-embedding-v4`; reranker: `qwen3-rerank`, top-20
- SkillRouter models: `pipizhao/SkillRouter-Embedding-0.6B` and `pipizhao/SkillRouter-Reranker-0.6B`
- SkillRouter hosted job: `6a22ef1cece949d7b3dca3a2`, `t4-small`, PyTorch 2.7.1 CUDA image

## Qwen Results

| Method | Representation | Reranker | Candidate budget | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 | MRR | Accept MRR |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen embedding | R1 flat metadata | none | all | 62.2% | 72.0% | 84.2% | 89.0% | 0.720 | 0.802 |
| Qwen embedding + Qwen rerank | R1 flat metadata | Qwen | 20 | 74.4% | 85.4% | 96.3% | 97.6% | 0.837 | 0.909 |
| Qwen embedding + local schema rerank | R1 flat metadata | local schema | 100 | 40.2% | 59.8% | 85.4% | 95.1% | 0.592 | 0.740 |
| Qwen embedding | R2 structured procedural | none | all | 59.8% | 73.2% | 82.9% | 87.8% | 0.714 | 0.813 |
| Qwen embedding + Qwen rerank | R2 structured procedural | Qwen | 20 | 76.8% | 90.2% | 100.0% | 100.0% | 0.861 | 0.939 |
| Qwen embedding + local schema rerank | R2 structured procedural | local schema | 100 | 39.0% | 57.3% | 85.4% | 95.1% | 0.600 | 0.743 |
| Qwen embedding | Full skill text | none | all | 31.7% | 50.0% | 58.5% | 69.5% | 0.448 | 0.596 |
| Qwen embedding + Qwen rerank | Full skill text | Qwen | 20 | 68.3% | 79.3% | 80.5% | 87.8% | 0.739 | 0.827 |
| Qwen embedding + local schema rerank | Full skill text | local schema | 100 | 25.6% | 46.3% | 72.0% | 82.9% | 0.454 | 0.620 |

Output files:

- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r1_embedding.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r1_qwen_rerank_top20.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r1_local_schema_top100.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r2_embedding.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r2_qwen_rerank_top20.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_r2_local_schema_top100.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_full_embedding.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_full_qwen_rerank_top20.json`
- `skill_benchmark/outputs/provider_selector_qwen_public_gold_82_full_local_schema_top100.json`

## M6-v1 With Qwen First Stage

First stage: Qwen full-skill embedding. Candidate recall at top-100 is 95.1% for all field sets.

| Field set | Strict top-1 | Accept top-1 | Strict top-5 | MRR | Candidate R@100 | Conditional top-1 |
|---|---:|---:|---:|---:|---:|---:|
| task | 54.9% | 65.8% | 79.3% | 0.663 | 95.1% | 57.7% |
| task + output + workflow | 47.6% | 67.1% | 80.5% | 0.609 | 95.1% | 50.0% |
| core | 48.8% | 67.1% | 79.3% | 0.619 | 95.1% | 51.3% |
| core + boundary | 48.8% | 67.1% | 82.9% | 0.617 | 95.1% | 51.3% |
| all fields | 43.9% | 63.4% | 81.7% | 0.604 | 95.1% | 46.2% |

Output file:

- `skill_benchmark/outputs/m6v1_public_gold_82_qwen_full_field_aware_top100.json`

## SkillRouter Results

Hosted SkillRouter outputs were printed from the Hugging Face job logs. The job completed successfully.

| Method | Candidate budget | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 | MRR | Accept MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| SkillRouter embedding | all | 68.3% | 79.3% | 95.1% | 97.6% | 0.790 | 0.866 |
| SkillRouter embedding + SkillRouter rerank | 20 | 64.6% | 73.2% | 92.7% | 95.1% | 0.778 | 0.835 |

## M6-v1 With SkillRouter First Stage

First stage: SkillRouter full-skill embedding. Candidate recall at top-100 is 98.8% for all field sets.

| Field set | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 | MRR | Accept MRR | Candidate R@100 | Conditional top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| task | 68.3% | 78.1% | 90.2% | 95.1% | 0.788 | 0.866 | 98.8% | 69.1% |
| task + output + workflow | 59.8% | 75.6% | 91.5% | 96.3% | 0.730 | 0.841 | 98.8% | 60.5% |
| core | 63.4% | 79.3% | 92.7% | 97.6% | 0.762 | 0.871 | 98.8% | 64.2% |
| core + boundary | 61.0% | 76.8% | 92.7% | 97.6% | 0.743 | 0.856 | 98.8% | 61.7% |
| all fields | 57.3% | 74.4% | 89.0% | 92.7% | 0.709 | 0.818 | 98.8% | 58.0% |

## Interpretation

- The cleaned public-gold stratum behaves differently from the controlled benchmark.
- Strong generic reranking is very effective on public-gold. The best current public-gold result is Qwen R2 + Qwen rerank top-20: 76.8% strict top-1, 90.2% accept top-1, and 100.0% strict/acceptable top-5.
- SkillRouter embedding is strong as a first-stage retriever, but SkillRouter reranking does not improve public-gold top-1 in this run.
- M6-v1-local field-aware reranking is not competitive on public-gold. This supports the current critique: the local field matcher is too lexical and likely overfits cleaner controlled skills.
- Public-gold therefore strengthens the thesis if framed carefully: it shows that extracting useful skill information is not enough; the retrieval architecture must use that information with robust semantic field matching and good request-side parsing.
- Do not claim "structure-aware always wins." The stronger claim is that field information can help in controlled near-neighbour cases, but public-authored skills expose extraction and semantic-matching limitations that the final method must address.
