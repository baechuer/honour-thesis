# Active Benchmark Snapshot

Date: 2026-06-23

> **2026-08-15 RQ2 status.** The frozen-v0.4 benchmark below remains historical full-library evidence. The separate 350-cluster/750-prompt matched-content RQ2a study is `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`. Its untouched confirmatory split contains 280 clusters, 600 prompts, 22 conditions, and 13,200 aligned rows. The primary Qwen fielded-minus-flat result is `-6.7pp`; frozen Qwen field-aware recovers `+6.6pp` over fielded single-vector but is descriptively tied with flat Qwen. RQ2b base-v1 B0G is blocked before retrieval; a focused review of its 14 disputed gold labels retains six and excludes eight, and its 381-prompt strict-gold-only v1.1 manifest is locally validated. B1X is untransmitted and no RQ2b scientific result exists. Canonical RQ2a analysis: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.

This is the compact source of truth for the currently active benchmark size and validation status.

Frozen benchmark version: `benchmark-v0.4-2026-06-16`

Current thesis framing: use information layers (`I0` progressive disclosure, `I1` flat card, `I2` full artifact, `I3` structured fields, planned `I4` relations, planned `I5` hierarchy) rather than treating embedding, graph, tree, or reranker methods as the information itself. Canonical framing: `thesis_notes/current/Information Layer Framework.md`.

Freeze manifest:

- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.md`
- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.json`

Freeze rule: prompt files, gold labels, skill files, and acceptable-alternative annotations should not be changed for result reporting under this version. If a gold-label or skill-definition error is discovered, create a new benchmark version rather than silently editing this freeze.

## Composition

| Stratum | Count | Role |
|---|---:|---|
| Controlled prompts | 245 | Main causal/stress-test set for semantic confusion under procedural distinctions. |
| Public-gold prompts | 144 | External-validity set using imported public skills as gold labels. |
| Low-information stress prompts | 12 | Robustness check; not merged into headline controlled/public results. |
| Broad prompt pool | 401 | Controlled + public-gold + low-information. |
| Total skills | 2433 | Full scale library used for current-full evaluation. |
| Background-scale skills | 1800 | Generated scale distractors with varied domains/procedures. |
| Public imported skills | 460 | Publicly available skill artifacts retained with normalized wrappers plus upstream originals at `source/SKILL.original.md`. |
| Public-style controlled skills | 32 | Controlled skills written in a more public-style prose format. |

## Latest Validation

| Gate | Controlled | Public-gold |
|---|---|---|
| Step 1 integrity | PASS: 245 prompts, 0 missing refs | PASS: 144 prompts, 0 missing refs |
| Step 2 procedural distinctness | PASS: 245/245 prompts; 830/830 pairs | PASS: 144/144 prompts; 575/575 pairs |
| Step 2 prompt-specific alignment | 238/245 prompts; acceptable top-1 241/245 | 131/144 prompts; acceptable top-1 138/144 |
| Step 3 semantic confusability | PASS: 243/245 prompts | PASS: 144/144 prompts |
| Step 4 leakage | PASS: 0 critical, 0 high | PASS: 0 critical, 0 high |

## Latest Scale Pressure

- R1 flat metadata is approximately 332,992 tokens by chars/4, above a 200k-token context budget.
- Controlled flat semantic non-core top-1: 56/245.
- Controlled best non-core above gold: 88/245.
- Controlled procedural non-core above gold: 14/245 prompts.

## Latest Local Selector Sanity Check

Frozen v0.4 rerun report:

- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.md`
- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.json`

Controlled current-full, 245 prompts:

| Method | Top-1 | Top-5 | MRR |
|---|---:|---:|---:|
| M1 BM25 flat | 55.1% | 86.9% | 0.687 |
| M1 TF-IDF flat | 52.6% | 84.9% | 0.670 |
| M3 TF-IDF schema | 59.6% | 91.4% | 0.731 |
| M6 BM25 -> schema rerank | 56.3% | 88.2% | 0.708 |
| M6 TF-IDF -> schema rerank | 58.8% | 87.4% | 0.716 |

Controlled Qwen representation matrix, 245 prompts:

| Method | Representation | Top-1 | Top-5 | MRR |
|---|---|---:|---:|---:|
| Qwen embedding | R1 flat | 33.9% | 62.0% | 0.464 |
| Qwen embedding | R2 structured | 40.4% | 73.9% | 0.544 |
| Qwen embedding | Full skill | 42.4% | 75.9% | 0.570 |
| Qwen embedding + Qwen rerank top-20 | R1 flat | 51.0% | 73.9% | 0.606 |
| Qwen embedding + Qwen rerank top-20 | R2 structured | 58.4% | 80.0% | 0.680 |
| Qwen embedding + Qwen rerank top-20 | Full skill | 62.9% | 79.6% | 0.704 |
| Qwen + local schema top-20 | R1 flat | 42.9% | 72.2% | 0.559 |
| Qwen + local schema top-20 | R2 structured | 49.4% | 79.2% | 0.625 |
| Qwen + local schema top-20 | Full skill | 49.8% | 80.0% | 0.625 |
| Qwen full + M6-v1 field-aware top-100 | Best field set: core boundary | 64.5% | 91.4% | 0.764 |
| TF-IDF schema + M6-v1 field-aware top-20 | Best field set: core boundary | 69.8% | 97.1% | 0.818 |

Public-gold current-full, 144 prompts:

| Method | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 55.6% | 65.3% | 81.9% | 86.8% |
| M1 TF-IDF flat | 56.9% | 64.6% | 86.8% | 91.0% |
| M3 TF-IDF schema | 50.7% | 59.7% | 81.2% | 86.8% |
| M6 BM25 -> schema rerank | 50.7% | 62.5% | 81.2% | 87.5% |
| M6 TF-IDF -> schema rerank | 53.5% | 63.2% | 86.1% | 90.3% |

Public-gold Qwen representation matrix, 144 prompts:

| Method | Representation | Strict top-1 | Accept top-1 | Strict top-5 | Accept top-5 |
|---|---|---:|---:|---:|---:|
| Qwen embedding | R1 flat | 57.6% | 67.4% | 82.6% | 87.5% |
| Qwen embedding | R2 structured | 61.8% | 71.5% | 88.9% | 91.7% |
| Qwen embedding | Full skill | 70.8% | 79.2% | 93.8% | 96.5% |
| Qwen embedding + Qwen rerank top-20 | R1 flat | 73.6% | 81.9% | 92.4% | 94.4% |
| Qwen embedding + Qwen rerank top-20 | R2 structured | 70.8% | 81.2% | 96.5% | 97.9% |
| Qwen embedding + Qwen rerank top-20 | Full skill | 72.9% | 80.6% | 93.8% | 95.1% |
| Qwen + local schema top-20 | R1 flat | 58.3% | 68.1% | 87.5% | 90.3% |
| Qwen + local schema top-20 | R2 structured | 55.6% | 65.3% | 90.3% | 94.4% |
| Qwen + local schema top-20 | Full skill | 61.1% | 71.5% | 93.1% | 95.8% |
| TF-IDF flat + M6-v1 field-aware top-20 | Best field set: task | 68.1% | n/a | 87.5% | n/a |

SkillRouter representation matrix, 245 controlled prompts:

| Method | Representation | Top-1 | Top-5 | MRR |
|---|---|---:|---:|---:|
| SkillRouter embedding | R1 flat | 62.9% | 93.5% | 0.763 |
| SkillRouter embedding + SkillRouter rerank top-20 | R1 flat | 65.7% | 94.7% | 0.780 |
| SkillRouter embedding | R2 structured | 64.5% | 94.7% | 0.783 |
| SkillRouter embedding + SkillRouter rerank top-20 | R2 structured | 71.0% | 96.7% | 0.823 |
| SkillRouter embedding | Full skill | 59.2% | 91.4% | 0.737 |
| SkillRouter embedding + SkillRouter rerank top-20 | Full skill | 71.8% | 95.9% | 0.827 |

SkillRouter representation matrix, 144 public-gold prompts:

| Method | Representation | Strict top-1 | Accept top-1 | Strict top-5 | MRR |
|---|---|---:|---:|---:|---:|
| SkillRouter embedding | R1 flat | 68.8% | 77.1% | 93.8% | 0.794 |
| SkillRouter embedding + SkillRouter rerank top-20 | R1 flat | 70.8% | 79.2% | 92.4% | 0.804 |
| SkillRouter embedding | R2 structured | 75.0% | 81.2% | 94.4% | 0.831 |
| SkillRouter embedding + SkillRouter rerank top-20 | R2 structured | 71.5% | 78.5% | 93.1% | 0.805 |
| SkillRouter embedding | Full skill | 75.0% | 82.6% | 93.1% | 0.833 |
| SkillRouter embedding + SkillRouter rerank top-20 | Full skill | 70.1% | 76.4% | 92.4% | 0.804 |

M6-v2 semantic field-matching checkpoint:

- Refreshed Qwen fixed task-heavy report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md`
- Refreshed Qwen field-only sensitivity report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md`
- Historical SkillRouter-first-stage focused report: `skill_benchmark/outputs/frozen_v0_4_skillrouter_m6v2_comparison.md`
- M6-v2 is a no-rewrite semantic field-aware reranker. It compares the raw request against selector-visible skill fields using Qwen `text-embedding-v4`; it does not generate missing workflow steps or rewrite underspecified prompts.
- The refreshed fixed task-heavy report currently includes Qwen sources only, so it should not be mixed with older SkillRouter M6-v2 fixed rows.

Refreshed Qwen-only fixed M6-v2 task-heavy rows:

| Stratum | Representation | M6-v2 top-1 | M6-v2 top-5 | M6-v2 MRR | Embedding-only top-1 | Learned rerank top-1 |
|---|---|---:|---:|---:|---:|---:|
| Controlled | R1 | 35.5% | 63.7% | 0.477 | 33.9% | 51.0% |
| Controlled | R2 | 38.4% | 70.6% | 0.524 | 40.4% | 58.4% |
| Controlled | Full | 40.8% | 72.2% | 0.546 | 42.4% | 62.9% |
| Public-gold | R1 | 54.9% | 81.9% | 0.663 | 57.6% | 73.6% |
| Public-gold | R2 | 56.9% | 84.7% | 0.691 | 61.8% | 70.8% |
| Public-gold | Full | 59.7% | 87.5% | 0.715 | 70.8% | 72.9% |

Focused SkillRouter-first-stage M6-v2 task rows:

| Stratum | Representation | M6-v2 task Top-1 | SkillRouter embedding Top-1 | SkillRouter rerank Top-1 |
|---|---|---:|---:|---:|
| Controlled | R1 | 60.4% | 62.9% | 65.7% |
| Controlled | R2 | 62.9% | 64.5% | 71.0% |
| Controlled | Full | 59.6% | 59.2% | 71.8% |
| Public-gold | R1 | 69.4% | 68.8% | 70.8% |
| Public-gold | R2 | 72.9% | 75.0% | 71.5% |
| Public-gold | Full | 72.2% | 75.0% | 70.1% |

Crossed lexical representation control:

- Report: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md`
- Controlled BM25 top-1: R1 55.1%, R2 58.0%, full 66.5%.
- Controlled TF-IDF top-1: R1 52.6%, R2 59.6%, full 69.4%.
- Public-gold BM25 strict top-1: R1 55.6%, R2 54.9%, full 59.0%; candidate recall@20 improves from 87.5% on R1 to 97.2% on R2 and 99.3% on full.
- Public-gold TF-IDF strict top-1: R1 56.9%, R2 50.7%, full 48.6%; candidate recall@20 improves from 92.4% on R1 to 94.4% on R2 and 96.5% on full.

M6-v2 blend calibration:

- Fine sweep report: `skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`
- The fine sweep varies first-stage weight and semantic-field weight without new API calls.
- Use dev/test-selected weights or cross-validation for thesis-facing tuned M6-v2 claims. Full-set best weights are diagnostic only.

M6-v2 explicit field-use sweep:

- Explicit sweep report: `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md`
- Focused R2 tuning report: `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md`
- Fixed global policy report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_global_core.md`
- Field-only sensitivity report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_global_core_field_only.md`
- Internal-weight ablation report: `skill_benchmark/outputs/frozen_v0_4_m6v2_internal_weight_ablation_fixed_detailed.md`
- Selected task-heavy fixed report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md`
- Task-heavy field-only sensitivity report: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md`
- This sweep uses field-specific request-side spans and saved per-field component similarities; it does not rewrite the query or make new embedding calls.
- The thesis-facing M6-v2-fixed method uses one global setting: 0.30 first-stage score, 0.70 semantic-field score, 0.25 penalty/bonus adjustment, `semantic_all`, cue-gated activation, and task-heavy field weights: task 0.50, output 0.20, workflow 0.15, input 0.10, dependency 0.05.
- The refreshed task-heavy fixed report is Qwen-only. R2 top-1 is 38.4% on controlled and 56.9% on public-gold.
- Task-heavy field-only sensitivity is regenerated for Qwen only and remains a diagnostic; older SkillRouter M6-v2 fixed rows are historical until a corrected-source SkillRouter rerun is performed.
- R2 controlled: Qwen fixed field-specific 40.0% top-1, focused tuned full-set 41.6%, dev-selected held-out 40.7%; SkillRouter fixed 64.5%, focused tuned full-set 66.1%, held-out 63.6%.
- R2 public-gold: Qwen fixed 61.8% strict top-1, focused tuned full-set 68.8%, held-out 66.7%; SkillRouter fixed 73.6%, focused tuned full-set 76.4%, held-out 71.8%.
- Main read: M6-v2 shows useful field signal, but most R2 tuned winners remain task-only or first-stage-heavy. This is evidence for selective field use and better calibration, not a final proof that every proposed field should be added as positive evidence.

Current interpretation:

- On controlled prompts, R2 structured representation improves over R1 under the same Qwen embedding and the same Qwen reranker, but full skill text is strongest under Qwen rerank after the public-style controlled regeneration.
- On public-gold prompts, full skill text is strongest for Qwen embedding and close to strongest for Qwen rerank after switching to upstream public originals. R1 remains strong under Qwen rerank because public names/descriptions contain real-world provider/task cues.
- Public-original source correction, 2026-06-23: final public-gold full-artifact comparisons should use upstream public `source/SKILL.original.md` files, not normalized public wrappers. Local deterministic and Qwen rows now follow this policy; local SkillRouter rows remain historical until rerun.
- M6-v2 currently supports a cautious claim: no-rewrite semantic field matching can slightly improve some embedding-only rows and is interpretable, but it does not replace learned rerankers. Task-only is usually strongest; extra fields often hurt unless the reranker learns when to trust them.
- The newly rerun M6-v1 local first-stage variants show strong lexical baselines. Controlled TF-IDF/schema plus field-aware reranking reaches 69.8% top-1, and public-gold TF-IDF/flat plus task-field reranking reaches 68.1% strict top-1. This means the thesis should not be framed as "embedding versus structure" only; lexical candidate generation plus structured field reranking is also a serious baseline.
- Current local schema and M6-v1 field-aware rerankers are diagnostic, not final robust methods. They help controlled cases but are brittle on public-gold because lexical field matching does not fully handle messy public prose.
- M4/M5 graph/tree, full-scale M0 progressive disclosure, downstream task success, per-source public-gold failure slicing, and cost/latency reporting remain pending for frozen v0.4. First-pass top-1 confidence intervals, paired McNemar tests, SkillRouter R1/R2/full embedding/rerank runs, SkillRouter-to-M6-v1 top-20 hybrid reports, and failure-mode reports now exist.

External SkillRouter-Eval-Core I3C status:

- This is an external verification track for RQ1, not a replacement for the controlled frozen-v0.4 benchmark.
- Corpus/prompt audit: `skill_benchmark/outputs/skill_corpus_richness_audit.md`; checkpoint `thesis_notes/checkpoints/skillrouter/External SkillRouter Corpus Richness Audit - 2026-06-23.md`.
- Audit caveat: the external benchmark is more cue-rich than the local controlled benchmark. SkillRouter scored tasks have mean 198.4 rough tokens, median 169, 97.3% file/path references, 92.0% explicit input cues, 85.3% explicit output cues, and 40.0% numbered steps. Local controlled prompts have mean 36.8 rough tokens, median 25, and 3.4 listed closest alternatives on average.
- Skill-body caveat: SkillRouter-Eval-Core is not uniformly "rich I3" data, but it is highly markdown-normalized. In the scored gold-name subset, 98.5% have H1 headings, 79.2% show procedural signal, and frequent headings include `overview`, `best practices`, `quick start`, `dependencies`, `when to use this skill`, and `workflow`.
- Full-all I3C V2 extraction is complete for the 79,141-skill Hard tier. Canonical cleaned artifact: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`.
- Top-20 task-relevant I3C V2 extraction is also complete for fixed-candidate reranking/information-layer tests: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`.
- Clean QA: 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 498836/498836 exact evidence matches, and 0 heading-only evidence after cleaning.
- Full-library/full-tier external I3C FTS/BM25 retrieval has been run. Report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.md`.
- Easy I3C: 53.3% Hit@1, 0.586 MRR@10, 60.5% Recall@20, 44.0% FullCoverage@20, 15,677,596 approximate selector-visible tokens.
- Hard I3C: 45.3% Hit@1, 0.527 MRR@10, 59.2% Recall@20, 40.0% FullCoverage@20, 15,833,065 approximate selector-visible tokens.
- Local frozen-v0.4 I3C is not yet produced. The local `I3M_model_parsed.jsonl` artifact is the paid DeepSeek attempt and should not be relabelled as I3C.
- I3C remains a structured field layer, not an I4 relation graph or I5 hierarchy/tree.

## Semantic Repair Note

Step 3 was repaired on 2026-06-16 by adding semantically close but procedurally rejectable alternatives. Two controlled observability prompts remain documented residuals: `obs_p2_latency_anomaly` and `obs_p4_capacity_risk`.

## Reports

- Expansion checkpoint: `thesis_notes/checkpoints/benchmark_validation/Test Case Expansion Toward 400 - 2026-06-16.md`
- Background scale validation: `skill_benchmark/outputs/background_scale_validation_2026_06_16.md`
- Rubric: `skill_benchmark/notes/benchmark_methodology_rubric.md`
