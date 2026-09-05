# Frozen Benchmark Version: benchmark-v0.4-2026-06-16

Date: 2026-06-16  
Timezone: Australia/Sydney

This freeze captures the post-expansion benchmark used for representation-layer retrieval reruns. It freezes the benchmark inputs; generated selector outputs may be added after this point, but prompt/skill edits require a new version.

## Composition

| Component | Count |
|---|---:|
| Controlled prompts | 245 |
| Public-gold prompts | 144 |
| Low-information prompts | 12 |
| Broad prompt pool | 401 |
| Total skills | 2433 |

## Skill Categories

| Category | Skills |
|---|---:|
| `api_backend_design` | 6 |
| `api_mcp_tooling` | 6 |
| `background_scale` | 1800 |
| `browser_web_automation` | 6 |
| `code_github_workflow` | 6 |
| `data_spreadsheet` | 7 |
| `deployment_browser_qa` | 6 |
| `documents_files` | 7 |
| `email_communication` | 4 |
| `github_ci_maintenance` | 6 |
| `huggingface_ml_workflows` | 6 |
| `implicit_field_stress` | 10 |
| `metrics_observability` | 6 |
| `news_monitoring` | 5 |
| `observability_reliability` | 6 |
| `office_artifact_workflows` | 6 |
| `office_business_automation` | 6 |
| `pdf_document_operations` | 6 |
| `planning_meetings` | 5 |
| `public_imported_background` | 460 |
| `public_style_controlled` | 32 |
| `reading_research` | 8 |
| `reply_messaging` | 5 |
| `security_appsec` | 6 |
| `skill_lifecycle` | 6 |
| `skill_representation_analysis` | 6 |

## Validation Summary

| Gate | Frozen result |
|---|---|
| `controlled_step1_integrity` | PASS: 245 prompts, 0 missing refs |
| `controlled_step2_procedural_distinctness` | PASS: 245/245 prompts; 830/830 pairs |
| `controlled_step2_prompt_specific_alignment` | 238/245 prompts; strict top-1 236/245; acceptable top-1 241/245 |
| `controlled_step3_semantic_confusability` | PASS: 243/245 prompts; residuals obs_p2_latency_anomaly and obs_p4_capacity_risk |
| `controlled_step4_leakage` | PASS: 0 critical, 0 high |
| `public_gold_step1_integrity` | PASS: 144 prompts, 0 missing refs |
| `public_gold_step2_procedural_distinctness` | PASS: 144/144 prompts; 575/575 pairs |
| `public_gold_step2_prompt_specific_alignment` | 131/144 prompts; strict top-1 118/144; acceptable top-1 138/144 |
| `public_gold_step3_semantic_confusability` | PASS: 144/144 prompts |
| `public_gold_step4_leakage` | PASS: 0 critical, 0 high |

## Aggregate Hashes

| Input group | SHA-256 |
|---|---|
| `controlled_prompts_sha256` | `c74d570169960670e37b33b572cea56b1a648803a633f139e60b6436e22b1cc0` |
| `public_gold_prompts_sha256` | `9721d008e605131c5a7af1daa19fc4e76980dfed50aa9ce2446326fb2cf57ceb` |
| `low_information_prompts_sha256` | `a07b9a8b86ce52ad475eddb6ed924034b8e84f51d7e30876185dc60ae1270106` |
| `all_skills_sha256` | `b7e855991e880ba80c99c9a85fadb56efaa25b3885d6c02c4eceb2ee8d3bc851` |
| `annotations_sha256` | `3143f0d3d839ca4f46c930d083672049d78aec9b87fcdb20aa162ccf248e7080` |
| `representations_sha256` | `f1b679bc8103953e99de66eadd6d5b643774351faee5127780ef9ccfc1015f0f` |
| `validation_reports_sha256` | `22e7ee13ca6ffcef0ad0f08f05ee2ea5f9c7cd7215f9fb82be66cdf5824c03d3` |
| `representation_coverage_reports_sha256` | `35d0d4867c19c38b82ab9f590bbf1f061aaf6db0c9258d1f8faae7eba1eb97e4` |

Derived representation artifacts were refreshed after `export_skill_representations.py` on 2026-06-16.
## Freeze Rules

- Do not edit frozen prompt or skill files while reporting results for this version.
- If a gold-label error is discovered, create a new benchmark version rather than silently patching this one.
- Rerun result files should include this version ID in filenames or report headers.
- Controlled and public-gold strata must be reported separately before any combined score.

## Machine-Readable Manifest

- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.json`

## Retrieval Matrix Outputs

Completed after freezing on 2026-06-16:

- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.md`
- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.json`
- Local offline, Qwen embedding, Qwen rerank, local-schema rerank, M6-v1 field-aware, and field-ablation outputs with `frozen_v0_4_` prefixes.

Pending for this version: SkillRouter R1/R2/full reruns, M4/M5, full-scale M0, downstream checks, and statistical paired tests.
