# All Non-Core Procedural Competition Report

This report applies the Step 2 requirement-alignment idea against every non-core skill, not only the listed closest alternatives. It asks whether a background/public/support skill looks procedurally competitive with the gold skill under structured procedural fields.

Similarity backend: **sklearn_tfidf**.

Important limitation: this is a heuristic procedural-fit screen, not a human adjudication. A non-core score above gold means it deserves review; it does not automatically mean the gold label is wrong.

## Overall Status

- Prompts checked: 85
- Non-core skills checked per prompt: 939
- Gold/non-core prompt-skill comparisons: 79815
- Prompts with at least one non-core skill above gold: 14/85 (16.5%)
- Prompts with at least one non-core skill near or above gold: 23/85 (27.1%)
- Above-gold non-core comparisons: 49
- Near-gold non-core comparisons within 0.02 margin: 309

## Family Summary

| Prompt family | Prompts | With non-core above gold | Above-gold pairs | Near/above pairs |
|---|---:|---:|---:|---:|
| `api_backend_design` | 6 | 1/6 | 1 | 17 |
| `browser_web_automation` | 6 | 1/6 | 1 | 1 |
| `code_github_workflow` | 6 | 1/6 | 1 | 1 |
| `data_spreadsheet` | 7 | 0/7 | 0 | 7 |
| `deployment_browser_qa` | 6 | 1/6 | 1 | 2 |
| `documents_files` | 7 | 1/7 | 5 | 88 |
| `metrics_observability` | 6 | 2/6 | 5 | 40 |
| `news_monitoring` | 5 | 0/5 | 0 | 3 |
| `office_artifact_workflows` | 6 | 1/6 | 2 | 32 |
| `planning_meetings` | 5 | 3/5 | 25 | 82 |
| `reading_research` | 8 | 0/8 | 0 | 19 |
| `reply_messaging` | 5 | 1/5 | 2 | 6 |
| `security_appsec` | 6 | 1/6 | 2 | 39 |
| `skill_lifecycle` | 6 | 1/6 | 4 | 21 |

## Above-Gold Competitor Families

| Non-core family | Top-10 appearances above gold |
|---|---:|
| `background_scale` | 20 |
| `public_imported_background` | 18 |

## Prompts With Non-Core Procedural Competitors

| Prompt | Gold | Gold score | Above-gold count | Top non-core competitors |
|---|---|---:|---:|---|
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 0.206 | 21 | +`public-office-meeting-notes`/public_imported_background (0.279, +0.073); +`meeting-ops-resource-linker`/background_scale (0.239, +0.033); +`meeting-ops-priority-ranker`/background_scale (0.235, +0.029); +`meeting-ops-comparison-builder`/background_scale (0.232, +0.026); +`meeting-ops-failure-diagnoser`/background_scale (0.229, +0.023) |
| `doc_p4_field_extraction` | `document-field-extractor` | 0.059 | 5 | +`invoice-payment-checker`/background_scale (0.146, +0.087); +`receipt-extractor`/background_scale (0.135, +0.076); +`finance-ops-field-extractor`/background_scale (0.071, +0.012); +`supply-chain-ops-field-extractor`/background_scale (0.070, +0.011); +`public-office-invoice-automation`/public_imported_background (0.061, +0.002) |
| `obs_p1_metrics_overview` | `metrics-overview` | 0.093 | 4 | +`public-mattpocock-triage`/public_imported_background (0.200, +0.107); +`public-oh-my-triage`/public_imported_background (0.180, +0.087); +`public-oh-my-game-build-log-triage`/public_imported_background (0.115, +0.022); +`public-oh-my-game-demo-feedback-triage`/public_imported_background (0.109, +0.016) |
| `skill_p1_find_existing` | `skill-finder` | 0.073 | 4 | +`public-office-meeting-notes`/public_imported_background (0.098, +0.025); +`meeting-ops-priority-ranker`/background_scale (0.081, +0.008); +`meeting-ops-comparison-builder`/background_scale (0.080, +0.007); +`meeting-ops-intake-classifier`/background_scale (0.077, +0.004); ~`meeting-ops-evidence-grounder`/background_scale (0.073, -0.000) |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 0.113 | 3 | +`public-office-meeting-notes`/public_imported_background (0.166, +0.054); +`meeting-ops-resource-linker`/background_scale (0.115, +0.002); +`meeting-ops-priority-ranker`/background_scale (0.113, +0.000); ~`meeting-ops-comparison-builder`/background_scale (0.110, -0.002); ~`meeting-ops-failure-diagnoser`/background_scale (0.109, -0.004) |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 0.044 | 2 | +`public-office-xlsx-manipulation`/public_imported_background (0.048, +0.004); +`public-swebench-xlsx`/public_imported_background (0.045, +0.001); ~`agent-ops-summary-writer`/background_scale (0.041, -0.003); ~`engineering-design-ops-summary-writer`/background_scale (0.040, -0.004); ~`journalism-ops-summary-writer`/background_scale (0.038, -0.006) |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 0.067 | 2 | +`public-oh-my-write-a-skill`/public_imported_background (0.094, +0.027); +`public-mattpocock-write-a-skill`/public_imported_background (0.093, +0.026); ~`public-swebench-clojure-write`/public_imported_background (0.056, -0.011); ~`public-office-investment-memo`/public_imported_background (0.054, -0.013); ~`email-action-extractor`/email_communication (0.052, -0.015) |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 0.057 | 2 | +`public-office-web-search`/public_imported_background (0.063, +0.007); +`public-swebench-similarity-search-patterns`/public_imported_background (0.059, +0.002); ~`search-ops-resource-linker`/background_scale (0.048, -0.009); ~`analytics-ops-resource-linker`/background_scale (0.043, -0.013); ~`search-ops-priority-ranker`/background_scale (0.043, -0.014) |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 0.057 | 1 | +`public-office-microsoft-teams`/public_imported_background (0.065, +0.008); ~`analytics-ops-quality-auditor`/background_scale (0.043, -0.014); ~`analytics-ops-timeline-builder`/background_scale (0.042, -0.015); ~`analytics-ops-evidence-grounder`/background_scale (0.041, -0.016); ~`analytics-ops-resource-linker`/background_scale (0.041, -0.016) |
| `web_p6_accessibility_check` | `accessibility-checker` | 0.100 | 1 | +`public-addy-web-accessibility`/public_imported_background (0.110, +0.010) |
| `code_p2_pr_review` | `pr-reviewer` | 0.144 | 1 | +`pr-description-writer`/background_scale (0.173, +0.029) |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 0.116 | 1 | +`public-netlify-deploy`/public_imported_background (0.169, +0.053); ~`public-oh-my-game-build-log-triage`/public_imported_background (0.101, -0.014) |
| `obs_p3_slo_breach` | `slo-breach-checker` | 0.095 | 1 | +`sre-ops-risk-reviewer`/background_scale (0.112, +0.017); ~`sre-ops-resource-linker`/background_scale (0.091, -0.004); ~`sre-ops-priority-ranker`/background_scale (0.090, -0.005); ~`sre-ops-comparison-builder`/background_scale (0.089, -0.006); ~`sre-ops-dependency-mapper`/background_scale (0.089, -0.006) |
| `plan_p4_task_extractor` | `task-extractor` | 0.122 | 1 | +`public-office-meeting-notes`/public_imported_background (0.139, +0.017); ~`meeting-ops-priority-ranker`/background_scale (0.111, -0.011); ~`meeting-ops-summary-writer`/background_scale (0.111, -0.011); ~`meeting-ops-resource-linker`/background_scale (0.110, -0.012); ~`meeting-ops-evidence-grounder`/background_scale (0.110, -0.012) |
| `data_p3_validation` | `data-analysis-with-validation` | 0.062 | 0 | ~`public-office-suspicious-email`/public_imported_background (0.058, -0.004); ~`public-oh-my-react-best-practices`/public_imported_background (0.056, -0.006); ~`public-oh-my-react-grab`/public_imported_background (0.056, -0.006); ~`lab-ops-quality-auditor`/background_scale (0.045, -0.017); ~`compliance-ops-quality-auditor`/background_scale (0.043, -0.019) |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 0.084 | 0 | ~`decision-matrix-builder`/background_scale (0.067, -0.017) |
| `obs_p6_incident_summary` | `incident-summary-writer` | 0.079 | 0 | ~`incident-ops-resource-linker`/background_scale (0.065, -0.014); ~`incident-ops-priority-ranker`/background_scale (0.064, -0.015); ~`incident-ops-comparison-builder`/background_scale (0.063, -0.015); ~`incident-ops-normalizer`/background_scale (0.063, -0.016); ~`incident-ops-scenario-planner`/background_scale (0.062, -0.016) |
| `news_p1_plain_summary` | `news-summariser` | 0.117 | 0 | ~`public-office-news-monitor`/public_imported_background (0.108, -0.008) |
| `news_p2_briefing` | `news-briefing-writer` | 0.088 | 0 | ~`support-ops-ops-timeline-builder`/background_scale (0.071, -0.017); ~`support-ops-ops-monitoring-plan-builder`/background_scale (0.069, -0.019) |
| `plan_p5_weekly_planner` | `weekly-planner` | 0.095 | 0 | ~`meeting-ops-acceptance-test-builder`/background_scale (0.093, -0.001); ~`meeting-ops-summary-writer`/background_scale (0.091, -0.003); ~`meeting-ops-scenario-planner`/background_scale (0.091, -0.004); ~`meeting-ops-priority-ranker`/background_scale (0.091, -0.004); ~`meeting-ops-resource-linker`/background_scale (0.089, -0.006) |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 0.066 | 0 | ~`research-ops-field-extractor`/background_scale (0.062, -0.005); ~`research-ops-comparison-builder`/background_scale (0.061, -0.005); ~`research-ops-normalizer`/background_scale (0.058, -0.008); ~`research-ops-summary-writer`/background_scale (0.058, -0.009); ~`research-ops-risk-reviewer`/background_scale (0.057, -0.009) |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 0.083 | 0 | ~`docker-compose-configurator`/background_scale (0.067, -0.017) |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 0.065 | 0 | ~`public-oh-my-deployment-automation`/public_imported_background (0.056, -0.010) |

## Review Guidance

- `+` means the non-core skill scored above the gold skill on structured procedural fields.
- `~` means the non-core skill was within 0.02 of the gold score.
- Treat high counts as review pressure, not automatic invalidation.
- If a `+` competitor has the same input type, output artifact, workflow, and success criterion as gold, mark it as acceptable or remove it from the background library.
- If it only shares generic words such as summary, rewrite, rank, check, evidence, or test while missing the task-specific artifact, keep it as a semantic distractor.
