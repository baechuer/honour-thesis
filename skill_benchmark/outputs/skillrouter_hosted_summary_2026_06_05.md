# SkillRouter Hosted Summary - 2026-06-05

This file records the compact Hugging Face Jobs run for the released SkillRouter models.

- Job ID: `6a22409ce6aa50b87b9eb371`
- Hardware: Hugging Face Jobs `t4-small`
- Snapshot repo: `baechuer1/honour-thesis-skillrouter-benchmark-snapshot`
- Embedding model: `pipizhao/SkillRouter-Embedding-0.6B`
- Reranker model: `pipizhao/SkillRouter-Reranker-0.6B`
- Representation: full skill artifact
- Rerank candidate budget: top-20
- Note: the remote job printed compact summaries only. Full per-prompt JSON artifacts were not uploaded from the job.

| Prompt set | Method | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 | Wall time |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Controlled, 137 prompts | SkillRouter full embedding | 73.0% | 75.9% | 94.2% | 94.9% | 0.827 | 14.6% | 48.7s |
| Controlled, 137 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 83.2% | 83.2% | 97.8% | 98.5% | 0.898 | 4.4% | 116.5s |
| Public-gold, 32 prompts | SkillRouter full embedding | 65.6% | 75.0% | 96.9% | 96.9% | 0.770 | 84.4% | 9.5s |
| Public-gold, 32 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 65.6% | 68.8% | 93.8% | 96.9% | 0.788 | 87.5% | 34.1s |

## Interpretation

- The controlled SkillRouter retrieve-and-rerank result is the strongest controlled result currently recorded.
- The public-gold result shows stronger first-stage retrieval than generic Qwen full-skill embedding, but reranking does not improve strict top-1.
- These results should be treated as a domain-specific neural baseline, not as a direct ablation of the proposed field taxonomy.
