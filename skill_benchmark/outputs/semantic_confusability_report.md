# Semantic Confusability Report

This report implements Step 3 of the benchmark rubric: listed alternatives should be semantically plausible neighbours, not random unrelated distractors.

Similarity backend: **sklearn_tfidf**.

Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.

## Overall Status

- Step 3 status: **FAIL**
- Prompts with at least two plausible listed alternatives: 27/85 (31.8%)
- Gold/alternative pairs marked plausible: 86/251 (34.3%)
- Gold skill ranked top-1 among all skills by this backend: 48/85 (56.5%)

Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, or whose skill card is similar to the gold skill card.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |
|---|---:|---:|---:|
| api_backend_design | 6 | 1/6 | 3/6 |
| browser_web_automation | 6 | 0/6 | 3/6 |
| code_github_workflow | 6 | 0/6 | 6/6 |
| data_spreadsheet | 7 | 1/7 | 5/7 |
| deployment_browser_qa | 6 | 0/6 | 5/6 |
| documents_files | 7 | 4/7 | 2/7 |
| metrics_observability | 6 | 1/6 | 2/6 |
| news_monitoring | 5 | 5/5 | 3/5 |
| office_artifact_workflows | 6 | 1/6 | 4/6 |
| planning_meetings | 5 | 3/5 | 1/5 |
| reading_research | 8 | 1/8 | 4/8 |
| reply_messaging | 5 | 5/5 | 4/5 |
| security_appsec | 6 | 0/6 | 3/6 |
| skill_lifecycle | 6 | 5/6 | 3/6 |

## Weak Semantic-Confusability Prompts

| Prompt | Gold | Plausible alternatives | Gold all-skill rank |
|---|---|---:|---:|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 0 | 1 |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 2 |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 0 | 1 |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 201 |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 0 | 1 |
| `web_p2_form_filling` | `web-form-filler` | 1 | 7 |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 48 |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 250 |
| `web_p5_frontend_debugging` | `frontend-debugger` | 0 | 1 |
| `web_p6_accessibility_check` | `accessibility-checker` | 0 | 1 |
| `code_p1_local_code_review` | `code-reviewer` | 0 | 1 |
| `code_p2_pr_review` | `pr-reviewer` | 0 | 1 |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 0 | 1 |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 0 | 1 |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 |
| `code_p6_release_notes` | `release-note-writer` | 0 | 1 |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 15 |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 0 | 1 |
| `data_p5_reporting` | `data-analysis-for-reporting` | 0 | 1 |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 0 | 2 |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 0 | 1 |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 0 | 1 |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 0 | 17 |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 0 | 1 |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 0 | 1 |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 2 |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 |
| `obs_p1_metrics_overview` | `metrics-overview` | 0 | 2 |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 0 | 1 |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 0 | 1 |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 0 | 2 |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 21 |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 0 | 1 |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 0 | 1 |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 2 |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 0 | 2 |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 27 |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 2 |
| `read_p3_citation_notes` | `citation-note-extractor` | 0 | 1 |
| `read_p4_document_extraction` | `document-extractor` | 1 | 122 |
| `read_p5_method_notes` | `method-note-builder` | 0 | 181 |
| `read_p6_grounding_check` | `citation-grounding-helper` | 0 | 1 |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 |
| `sec_p1_threat_model` | `security-threat-modeler` | 0 | 2 |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 0 | 21 |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 0 | 1 |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 111 |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | 0.3685 | 0.0489 | 0.0449 | no | api, pagination | endpoint, pagination |
| `webhook-contract-planner` | 0.3685 | 0.0228 | 0.0602 | no | contract, behavior | contract, behavior |
| `architecture-boundary-reviewer` | 0.3685 | 0.0000 | 0.1016 | no | review | review |

Top similarity neighbours: `openapi-contract-reviewer` (0.368), `openapi-contract-tester` (0.181), `public-swebench-add-admin-api-endpoint` (0.081), `contract-ops-acceptance-test-builder` (0.079), `api-design-reviewer` (0.069)

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | 0.0604 | 0.0287 | 0.0449 | yes | endpoint, behavior | endpoint, pagination |
| `webhook-contract-planner` | 0.0604 | 0.0258 | 0.1017 | yes | behavior, verification | payload, retrie |
| `service-dependency-mapper` | 0.0604 | 0.0000 | 0.0320 | no | - | failure |

Top similarity neighbours: `public-openai-figma-code-connect-components` (0.080), `api-integration-planner` (0.073), `public-swebench-add-admin-api-endpoint` (0.071), `api-ops-acceptance-test-builder` (0.064), `public-office-cover-letter` (0.061)

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | 0.0626 | 0.0000 | 0.1017 | no | - | payload, retrie |
| `openapi-contract-reviewer` | 0.0626 | 0.0070 | 0.0602 | no | behavior | contract, behavior |
| `public-office-webhook-automation` | 0.0626 | 0.0145 | 0.1334 | yes | event | event |
| `public-api-design-principles` | 0.0626 | 0.0181 | 0.0000 | no | design | design |

Top similarity neighbours: `invoice-payment-checker` (0.071), `webhook-contract-planner` (0.063), `public-openai-winui-app` (0.060), `duplicate-file-finder` (0.050), `events-ops-failure-diagnoser` (0.050)

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `service-dependency-mapper` | 0.3566 | 0.0075 | 0.0760 | no | - | service |
| `openapi-contract-reviewer` | 0.3566 | 0.0000 | 0.1016 | no | review | review |
| `database-migration-risk-assessor` | 0.3566 | 0.0000 | 0.0237 | no | - | risk |

Top similarity neighbours: `architecture-boundary-reviewer` (0.357), `public-architecture-patterns` (0.120), `public-openai-security-ownership-map` (0.071), `public-addy-agent-api-and-interface-design` (0.068), `public-oh-my-backend-testing` (0.062)

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | 0.1359 | 0.0000 | 0.0237 | no | risk | risk |
| `service-dependency-mapper` | 0.1359 | 0.0000 | 0.0361 | no | - | data |
| `public-office-database-sync` | 0.1359 | 0.0000 | 0.1347 | yes | - | database, migration, data |
| `public-architecture-patterns` | 0.1359 | 0.0000 | 0.0000 | no | - | - |

Top similarity neighbours: `database-migration-risk-assessor` (0.136), `public-addy-agent-shipping-and-launch` (0.112), `deployment-rollback-planner` (0.099), `migration-risk-auditor` (0.079), `query-optimizer` (0.055)

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 201

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | 0.0118 | 0.0227 | 0.0760 | yes | service, direction | service |
| `external-api-integration-planner` | 0.0118 | 0.0000 | 0.0320 | no | failure | failure |
| `public-architecture-patterns` | 0.0118 | 0.0000 | 0.0038 | no | - | - |
| `public-api-design-principles` | 0.0118 | 0.0000 | 0.0000 | no | - | - |

Top similarity neighbours: `public-office-microsoft-teams` (0.061), `analytics-ops-quality-auditor` (0.054), `public-office-data-pipeline` (0.047), `analytics-ops-evidence-grounder` (0.047), `public-office-md-slides` (0.046)

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.2138 | 0.0066 | 0.0548 | no | interaction, test | web, interaction, test |
| `web-data-extractor` | 0.2138 | 0.0000 | 0.0641 | no | page | page, web |
| `frontend-debugger` | 0.2138 | 0.0331 | 0.0312 | no | state, observation | state |

Top similarity neighbours: `web-page-snapshotter` (0.214), `public-n-skills-dev-browser` (0.080), `public-openai-screenshot` (0.079), `dashboard-ops-summary-writer` (0.057), `public-openai-figma-generate-design` (0.055)

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.0549 | 0.0312 | 0.0855 | yes | report, flow, test | interaction, flow |
| `web-page-snapshotter` | 0.0549 | 0.0057 | 0.0363 | no | test | perform, interaction |
| `frontend-debugger` | 0.0549 | 0.0131 | 0.0189 | no | - | - |

Top similarity neighbours: `public-office-pdf-form-filler` (0.075), `variance-analysis-helper` (0.075), `public-openai-playwright` (0.072), `public-office-expense-report` (0.068), `public-office-weekly-report` (0.068)

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 48

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-form-filler` | 0.0469 | 0.0000 | 0.0855 | no | - | interaction, flow |
| `frontend-debugger` | 0.0469 | 0.0092 | 0.0560 | no | behavior | behavior |
| `web-page-snapshotter` | 0.0469 | 0.0576 | 0.0548 | yes | test, page | test, web, interaction |

Top similarity neighbours: `variance-analysis-helper` (0.114), `web-page-snapshotter` (0.058), `public-office-expense-report` (0.052), `compliance-ops-acceptance-test-builder` (0.052), `public-office-weekly-report` (0.051)

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 250

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-page-snapshotter` | 0.0102 | 0.0911 | 0.0641 | yes | page, screenshot | web, page |
| `web-ui-tester` | 0.0102 | 0.0000 | 0.0681 | no | - | web |
| `frontend-debugger` | 0.0102 | 0.0000 | 0.0222 | no | - | - |

Top similarity neighbours: `product-ops-resource-linker` (0.130), `product-ops-field-extractor` (0.126), `product-ops-normalizer` (0.122), `product-ops-compliance-checker` (0.118), `product-ops-dependency-mapper` (0.116)

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.1014 | 0.0235 | 0.0560 | no | - | behavior |
| `web-page-snapshotter` | 0.1014 | 0.0592 | 0.0312 | no | page, open, evidence, inspect, state | state |
| `code-reviewer` | 0.1014 | 0.0210 | 0.0264 | no | code | code |

Top similarity neighbours: `frontend-debugger` (0.101), `api-ops-evidence-grounder` (0.072), `api-ops-field-extractor` (0.062), `api-ops-summary-writer` (0.062), `api-ops-normalizer` (0.062)

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.2001 | 0.0000 | 0.0392 | no | whether | check, web |
| `frontend-debugger` | 0.2001 | 0.0000 | 0.0192 | no | error | - |
| `web-page-snapshotter` | 0.2001 | 0.0000 | 0.0369 | no | - | web |

Top similarity neighbours: `accessibility-checker` (0.200), `accessibility-interaction-auditor` (0.159), `public-addy-web-accessibility` (0.130), `public-office-pdf-form-filler` (0.054), `layout-preserving-converter` (0.046)

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | 0.0739 | 0.0043 | 0.1053 | no | review, risk | review, file, risk |
| `review-comment-resolver` | 0.0739 | 0.0238 | 0.0657 | no | change, review | review, code, change |
| `ci-failure-debugger` | 0.0739 | 0.0131 | 0.0218 | no | test | test |

Top similarity neighbours: `code-reviewer` (0.074), `email-ops-acceptance-test-builder` (0.067), `git-commit-writer` (0.066), `email-ops-risk-reviewer` (0.059), `risk-ops-acceptance-test-builder` (0.056)

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.1916 | 0.0235 | 0.1053 | no | review, change, test | review, file, risk |
| `review-comment-resolver` | 0.1916 | 0.0261 | 0.0309 | no | review, request, change | review, request |
| `ci-failure-debugger` | 0.1916 | 0.0000 | 0.0245 | no | test | check |

Top similarity neighbours: `pr-reviewer` (0.192), `pr-description-writer` (0.165), `public-mattpocock-review` (0.081), `public-swebench-analyze-ci` (0.080), `public-openai-gh-address-comments` (0.069)

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | 0.1151 | 0.0686 | 0.0309 | no | review, request | review, request |
| `code-reviewer` | 0.1151 | 0.0415 | 0.0657 | no | review, test, code, change, miss, implementation | review, code, change |
| `ci-failure-debugger` | 0.1151 | 0.0361 | 0.0218 | no | test, need | - |

Top similarity neighbours: `review-comment-resolver` (0.115), `public-openai-gh-address-comments` (0.090), `pr-reviewer` (0.069), `public-addy-agent-code-review-and-quality` (0.068), `pr-description-writer` (0.062)

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.1292 | 0.0074 | 0.0218 | no | commit, test, change | test |
| `pr-reviewer` | 0.1292 | 0.0000 | 0.0245 | no | - | check |
| `review-comment-resolver` | 0.1292 | 0.0000 | 0.0218 | no | change | - |

Top similarity neighbours: `ci-failure-debugger` (0.129), `auth-flow-reviewer` (0.087), `public-openai-gh-fix-ci` (0.067), `public-mattpocock-diagnose` (0.060), `public-addy-agent-debugging-and-error-recovery` (0.056)

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `release-note-writer` | 0.1675 | 0.1615 | 0.1051 | yes | change, turn, complet, user-fac, release, note | change, complet |
| `pr-reviewer` | 0.1675 | 0.0000 | 0.0197 | no | - | - |
| `code-reviewer` | 0.1675 | 0.0245 | 0.0470 | no | change, test | change |

Top similarity neighbours: `changelog-writer` (0.168), `release-note-writer` (0.162), `public-swebench-changelog-automation` (0.139), `public-oh-my-changelog-maintenance` (0.127), `public-office-changelog-generator` (0.115)

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `changelog-writer` | 0.1617 | 0.0212 | 0.1051 | no | change | complet, change |
| `pr-reviewer` | 0.1617 | 0.0000 | 0.0450 | no | request | chang |
| `code-reviewer` | 0.1617 | 0.0223 | 0.0508 | no | change | change |

Top similarity neighbours: `release-note-writer` (0.162), `public-oh-my-changelog-maintenance` (0.089), `public-office-changelog-generator` (0.060), `public-swebench-changelog-automation` (0.056), `public-mattpocock-review` (0.048)

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-for-reporting` | 0.1091 | 0.0000 | 0.0763 | no | turn | spreadsheet |
| `data-analysis-with-anomaly-focus` | 0.1091 | 0.0000 | 0.1251 | yes | pattern | produce, spreadsheet, pattern |
| `data-analysis-with-validation` | 0.1091 | 0.0000 | 0.0831 | no | need, most | - |

Top similarity neighbours: `data-analysis-overview` (0.109), `data-analysis-for-ranking-selection` (0.046), `public-office-expense-report` (0.037), `public-office-weekly-report` (0.036), `public-mattpocock-zoom-out` (0.033)

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.1908 | 0.0000 | 0.1251 | yes | - | produce, spreadsheet, pattern |
| `data-analysis-for-root-cause-diagnosis` | 0.1908 | 0.0771 | 0.0780 | no | - | spreadsheet |
| `data-analysis-with-validation` | 0.1908 | 0.0000 | 0.1255 | yes | most | data, surfac |

Top similarity neighbours: `data-analysis-with-anomaly-focus` (0.191), `public-addy-agent-debugging-and-error-recovery` (0.091), `debugging-root-cause-helper` (0.080), `data-analysis-for-root-cause-diagnosis` (0.077), `metrics-root-cause-diagnoser` (0.060)

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 15

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.0292 | 0.0000 | 0.0831 | no | - | - |
| `data-analysis-with-anomaly-focus` | 0.0292 | 0.0200 | 0.1255 | yes | value, issue | surfac, data |
| `data-analysis-for-root-cause-diagnosis` | 0.0292 | 0.0000 | 0.0837 | no | - | - |

Top similarity neighbours: `public-addy-web-web-quality-audit` (0.063), `public-oh-my-react-grab` (0.051), `public-oh-my-react-best-practices` (0.049), `public-mattpocock-to-issues` (0.048), `public-oh-my-to-issues` (0.043)

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-with-anomaly-focus` | 0.0890 | 0.0307 | 0.0780 | no | data | spreadsheet |
| `data-analysis-overview` | 0.0890 | 0.0209 | 0.0703 | no | - | spreadsheet |
| `data-analysis-with-validation` | 0.0890 | 0.0324 | 0.0837 | no | data, most | - |

Top similarity neighbours: `data-analysis-for-root-cause-diagnosis` (0.089), `public-office-data-analysis` (0.071), `metrics-root-cause-diagnoser` (0.069), `public-oh-my-data-analysis` (0.064), `public-office-stock-analysis` (0.040)

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.0995 | 0.0334 | 0.0763 | no | broad | spreadsheet |
| `data-analysis-for-root-cause-diagnosis` | 0.0995 | 0.0117 | 0.0831 | no | - | spreadsheet, evidence |
| `data-analysis-with-anomaly-focus` | 0.0995 | 0.0114 | 0.0847 | no | - | spreadsheet |

Top similarity neighbours: `data-analysis-for-reporting` (0.100), `dashboard-ops-handoff-brief-writer` (0.051), `geospatial-ops-handoff-brief-writer` (0.049), `dashboard-ops-summary-writer` (0.040), `public-office-saas-metrics` (0.039)

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.1377 | 0.0000 | 0.0858 | no | pattern | spreadsheet, pattern, produce |
| `data-analysis-for-root-cause-diagnosis` | 0.1377 | 0.0431 | 0.1397 | yes | evidence | uses, spreadsheet |
| `data-analysis-with-anomaly-focus` | 0.1377 | 0.0240 | 0.0811 | no | pattern | spreadsheet, pattern, produce |

Top similarity neighbours: `data-analysis-for-forecasting` (0.138), `public-oh-my-pattern-detection` (0.064), `metrics-root-cause-diagnoser` (0.057), `data-analysis-for-root-cause-diagnosis` (0.043), `duplicate-file-finder` (0.041)

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.0762 | 0.0355 | 0.1041 | no | broad | spreadsheet, produce, strongest |
| `data-analysis-for-reporting` | 0.0762 | 0.0000 | 0.0843 | no | - | spreadsheet |
| `data-analysis-for-forecasting` | 0.0762 | 0.0198 | 0.1026 | no | forecast | spreadsheet, produce |

Top similarity neighbours: `decision-matrix-builder` (0.120), `data-analysis-for-ranking-selection` (0.076), `risk-ops-comparison-builder` (0.060), `dashboard-ops-comparison-builder` (0.053), `risk-ops-risk-reviewer` (0.043)

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.1649 | 0.0176 | 0.0399 | no | identify | screenshot |
| `accessibility-interaction-auditor` | 0.1649 | 0.0597 | 0.0634 | no | interaction, clue | interaction |
| `public-playwright-interactive` | 0.1649 | 0.0436 | 0.1029 | no | interaction, browser | browser, interaction |
| `public-openai-playwright` | 0.1649 | 0.0425 | 0.1417 | yes | browser | browser, screenshot |

Top similarity neighbours: `playwright-flow-debugger` (0.165), `frontend-debugger` (0.076), `public-addy-agent-browser-testing-with-devtools` (0.076), `public-n-skills-dev-browser` (0.072), `accessibility-interaction-auditor` (0.060)

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `playwright-flow-debugger` | 0.3258 | 0.0188 | 0.0399 | no | screenshot | screenshot |
| `accessibility-interaction-auditor` | 0.3258 | 0.0241 | 0.0463 | no | contrast | contrast |
| `public-openai-screenshot` | 0.3258 | 0.0000 | 0.0000 | no | screenshot, need | screenshot |
| `public-anthropic-webapp-testing` | 0.3258 | 0.0167 | 0.0168 | no | screenshot | screenshot |

Top similarity neighbours: `visual-regression-checker` (0.326), `slide-deck-visual-auditor` (0.091), `public-anthropic-canvas-design` (0.063), `latency-anomaly-detector` (0.046), `public-addy-agent-performance-optimization` (0.038)

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.2904 | 0.0000 | 0.0463 | no | - | contrast |
| `playwright-flow-debugger` | 0.2904 | 0.0196 | 0.0634 | no | interaction | interaction |
| `web-ui-tester` | 0.2904 | 0.0000 | 0.0201 | no | interaction, whether | interaction, web |
| `public-anthropic-webapp-testing` | 0.2904 | 0.0000 | 0.0092 | no | - | web |

Top similarity neighbours: `accessibility-interaction-auditor` (0.290), `accessibility-checker` (0.142), `public-addy-web-accessibility` (0.121), `metrics-overview` (0.058), `public-addy-web-web-quality-audit` (0.054)

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 17

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `deployment-release-verifier` | 0.0270 | 0.0000 | 0.1078 | no | - | deployment, environment, version |
| `playwright-flow-debugger` | 0.0270 | 0.0000 | 0.0214 | no | - | failure |
| `web-performance-budget-checker` | 0.0270 | 0.0000 | 0.0208 | no | - | - |

Top similarity neighbours: `public-netlify-deploy` (0.166), `public-oh-my-game-build-log-triage` (0.134), `debugging-root-cause-helper` (0.129), `data-analysis-for-root-cause-diagnosis` (0.097), `public-addy-agent-debugging-and-error-recovery` (0.093)

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `deployment-build-triager` | 0.3154 | 0.0183 | 0.1078 | no | version, environment | deployment, environment, version |
| `visual-regression-checker` | 0.3154 | 0.0000 | 0.0216 | no | - | - |
| `public-netlify-deploy` | 0.3154 | 0.1305 | 0.0000 | no | production, deploy, netlify | - |
| `public-openai-vercel-deploy` | 0.3154 | 0.0933 | 0.0545 | no | deploy, live, app | deployment |

Top similarity neighbours: `deployment-release-verifier` (0.315), `public-netlify-deploy` (0.131), `public-openai-vercel-deploy` (0.093), `public-oh-my-changelog-maintenance` (0.086), `release-note-writer` (0.086)

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.1690 | 0.0000 | 0.0547 | no | - | - |
| `deployment-release-verifier` | 0.1690 | 0.0000 | 0.0233 | no | - | load, evidence |
| `accessibility-interaction-auditor` | 0.1690 | 0.0000 | 0.0635 | no | - | web, clue |

Top similarity neighbours: `web-performance-budget-checker` (0.169), `budget-planner` (0.073), `mobile-ops-acceptance-test-builder` (0.069), `mobile-ops-normalizer` (0.064), `mobile-ops-monitoring-plan-builder` (0.064)

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.0988 | 0.0000 | 0.0762 | no | - | document |
| `document-field-extractor` | 0.0988 | 0.0000 | 0.0711 | no | - | document |
| `document-converter` | 0.0988 | 0.0209 | 0.1287 | yes | - | document, such, memo, form |

Top similarity neighbours: `document-summariser` (0.099), `general-source-summariser` (0.055), `knowledge-base-article-writer` (0.051), `multi-source-comparison-builder` (0.029), `receipt-extractor` (0.028)

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.0712 | 0.0553 | 0.1573 | yes | document, mean | document, structure, preserv, mean, content |
| `document-summariser` | 0.0712 | 0.0389 | 0.0706 | yes | document, form | document |
| `document-converter` | 0.0712 | 0.0421 | 0.0766 | yes | document, form | document |

Top similarity neighbours: `reply-polisher` (0.112), `document-rewriter` (0.071), `public-mattpocock-edit-article` (0.057), `document-normaliser` (0.055), `public-addy-web-accessibility` (0.046)

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-rewriter` | 0.0654 | 0.0340 | 0.1573 | yes | document, structure, rewrite | document, structure, preserv, content, mean |
| `document-converter` | 0.0654 | 0.0407 | 0.0828 | yes | document, layout | document |
| `document-summariser` | 0.0654 | 0.0218 | 0.0762 | no | document | document |

Top similarity neighbours: `layout-preserving-converter` (0.085), `deck-template-applier` (0.080), `document-normaliser` (0.065), `docx-redline-editor` (0.059), `docs-ops-rewrite-editor` (0.051)

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-summariser` | 0.0434 | 0.0190 | 0.0711 | yes | detail, summary | document |
| `multi-document-comparison-preparer` | 0.0434 | 0.0271 | 0.0882 | yes | field, detail | field, clause, document |
| `layout-preserving-converter` | 0.0434 | 0.0000 | 0.0485 | no | table | document |

Top similarity neighbours: `receipt-extractor` (0.196), `invoice-payment-checker` (0.176), `public-office-invoice-automation` (0.084), `meeting-followup-extractor` (0.069), `public-office-table-extractor` (0.055)

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-field-extractor` | 0.0384 | 0.0000 | 0.0882 | no | - | document, field, clause |
| `document-normaliser` | 0.0384 | 0.0108 | 0.0751 | yes | section | document, section, structure |
| `document-converter` | 0.0384 | 0.0000 | 0.0479 | no | - | document |

Top similarity neighbours: `decision-matrix-builder` (0.074), `multi-document-comparison-preparer` (0.038), `compliance-ops-comparison-builder` (0.035), `docs-ops-comparison-builder` (0.035), `partnerships-ops-comparison-builder` (0.034)

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 5

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.0613 | 0.0140 | 0.0828 | no | clean, content | document |
| `layout-preserving-converter` | 0.0613 | 0.0779 | 0.2296 | yes | convert, preserve, label, layout | convert, document, another, format, layout |
| `document-summariser` | 0.0613 | 0.0171 | 0.1287 | yes | form | document, such, memo, form |

Top similarity neighbours: `layout-preserving-converter` (0.078), `office-to-markdown-converter` (0.073), `public-obsidian-defuddle` (0.072), `pdf-layout-reviewer` (0.064), `document-converter` (0.061)

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-converter` | 0.1673 | 0.1192 | 0.2296 | yes | layout, markdown, priority, fidelity, note | convert, document, another, format, layout |
| `document-field-extractor` | 0.1673 | 0.0067 | 0.0485 | no | field | document |
| `document-normaliser` | 0.1673 | 0.0100 | 0.0617 | no | preserv | document, section |

Top similarity neighbours: `layout-preserving-converter` (0.167), `document-converter` (0.119), `pdf-layout-reviewer` (0.107), `office-to-markdown-converter` (0.090), `public-office-layout-analyzer` (0.080)

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `incident-summary-writer` | 0.1497 | 0.0000 | 0.0635 | no | - | summary, metric, operational |
| `metrics-root-cause-diagnoser` | 0.1497 | 0.0000 | 0.0772 | no | - | current, operational |
| `latency-anomaly-detector` | 0.1497 | 0.0398 | 0.0734 | no | service | metric, service |

Top similarity neighbours: `public-mattpocock-triage` (0.160), `metrics-overview` (0.150), `public-oh-my-triage` (0.143), `public-oh-my-game-build-log-triage` (0.108), `public-oh-my-game-demo-feedback-triage` (0.104)

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `metrics-root-cause-diagnoser` | 0.1795 | 0.0141 | 0.0366 | no | identify | regression |
| `metrics-overview` | 0.1795 | 0.1116 | 0.0734 | no | service, snapshot, metric | metric, service |
| `slo-breach-checker` | 0.1795 | 0.0280 | 0.0537 | no | service, whether, metric | metric, service |

Top similarity neighbours: `latency-anomaly-detector` (0.179), `metrics-overview` (0.112), `data-analysis-with-anomaly-focus` (0.085), `public-swebench-service-mesh-observability` (0.064), `data-analysis-overview` (0.062)

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 9

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `capacity-risk-forecaster` | 0.0612 | 0.0252 | 0.0322 | yes | risk | risk |
| `metrics-overview` | 0.0612 | 0.0668 | 0.0699 | yes | service, snapshot | service, metric |
| `metrics-root-cause-diagnoser` | 0.0612 | 0.0000 | 0.0348 | no | - | - |

Top similarity neighbours: `risk-ops-risk-reviewer` (0.091), `sre-ops-risk-reviewer` (0.084), `incident-ops-risk-reviewer` (0.084), `public-swebench-slo-implementation` (0.084), `public-swebench-service-mesh-observability` (0.069)

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `slo-breach-checker` | 0.2297 | 0.1142 | 0.0322 | no | risk, service, slo | risk |
| `metrics-root-cause-diagnoser` | 0.2297 | 0.0838 | 0.0368 | no | likely, operational, current, cause | likely |
| `metrics-overview` | 0.2297 | 0.0704 | 0.0282 | no | service, snapshot, focu, operational, current | signal |

Top similarity neighbours: `capacity-risk-forecaster` (0.230), `slo-breach-checker` (0.114), `risk-ops-risk-reviewer` (0.096), `metrics-root-cause-diagnoser` (0.084), `debugging-root-cause-helper` (0.080)

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `latency-anomaly-detector` | 0.1201 | 0.0557 | 0.0366 | no | service, latency | regression |
| `capacity-risk-forecaster` | 0.1201 | 0.0199 | 0.0368 | no | queue, pressure | likely |
| `incident-summary-writer` | 0.1201 | 0.0000 | 0.0848 | no | - | operational, incident |

Top similarity neighbours: `data-analysis-for-root-cause-diagnosis` (0.162), `metrics-root-cause-diagnoser` (0.120), `public-addy-agent-debugging-and-error-recovery` (0.077), `debugging-root-cause-helper` (0.071), `latency-anomaly-detector` (0.056)

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 21

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `metrics-overview` | 0.0722 | 0.0614 | 0.0635 | yes | service, snapshot | metric, operational, summary |
| `metrics-root-cause-diagnoser` | 0.0722 | 0.0232 | 0.0848 | no | incident | incident, operational |
| `slo-breach-checker` | 0.0722 | 0.0252 | 0.0366 | no | service | metric |

Top similarity neighbours: `incident-ops-normalizer` (0.088), `incident-ops-compliance-checker` (0.086), `incident-ops-dependency-mapper` (0.085), `incident-ops-scenario-planner` (0.083), `incident-ops-risk-reviewer` (0.083)

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-briefing-writer` | 0.1842 | 0.0599 | 0.2759 | yes | summary, news | news, summary, provid, item, theme, brief |
| `source-grounding-extractor` | 0.1842 | 0.0338 | 0.1748 | yes | summary, news | news, summary, provid, content |

Top similarity neighbours: `news-summariser` (0.184), `public-office-news-monitor` (0.135), `tech-news-trend-extractor` (0.086), `public-mattpocock-edit-article` (0.070), `news-theme-extractor` (0.069)

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-summariser` | 0.0801 | 0.0000 | 0.2759 | yes | summary | brief, provid, news, item, summary, theme |
| `tech-news-trend-extractor` | 0.0801 | 0.0158 | 0.1238 | yes | signal, just | provid, news |

Top similarity neighbours: `news-briefing-writer` (0.080), `public-mattpocock-edit-article` (0.073), `knowledge-base-article-writer` (0.051), `support-ticket-triager` (0.050), `support-ops-timeline-builder` (0.048)

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-summariser` | 0.0797 | 0.0057 | 0.1748 | yes | - | provid, news, content, summary |
| `news-briefing-writer` | 0.0797 | 0.0050 | 0.1948 | yes | - | extract, source-ground, provid, news, need, summary |

Top similarity neighbours: `product-ops-evidence-grounder` (0.081), `source-grounding-extractor` (0.080), `product-ops-scenario-planner` (0.073), `knowledge-base-article-writer` (0.069), `product-ops-field-extractor` (0.065)

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `tech-news-trend-extractor` | 0.1355 | 0.1591 | 0.2523 | yes | acros, tech, news | topic, acros, provid, news, know, appear |
| `news-briefing-writer` | 0.1355 | 0.0404 | 0.2390 | yes | extract, theme, news | extract, theme, provid, news, item, summary, brief |

Top similarity neighbours: `tech-news-trend-extractor` (0.159), `news-theme-extractor` (0.136), `public-office-news-monitor` (0.091), `news-summariser` (0.068), `data-analysis-for-forecasting` (0.060)

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-theme-extractor` | 0.2050 | 0.0490 | 0.2523 | yes | pattern, acros, news | news, provid, topic, know, appear, acros |
| `news-briefing-writer` | 0.2050 | 0.0503 | 0.1238 | yes | news, why, they, matter | news, provid |

Top similarity neighbours: `tech-news-trend-extractor` (0.205), `news-summariser` (0.101), `public-office-news-monitor` (0.072), `news-briefing-writer` (0.050), `news-theme-extractor` (0.049)

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-ocr-extractor` | 0.1930 | 0.0593 | 0.0837 | no | extract | page |
| `office-to-markdown-converter` | 0.1930 | 0.0168 | 0.0199 | no | table | table |
| `public-office-pdf-extraction` | 0.1930 | 0.0884 | 0.0427 | no | table, extract | table |
| `public-pdf` | 0.1930 | 0.0816 | 0.0857 | no | pdf, table, anyth, form, read, extract | page, pdf, form, table, read |

Top similarity neighbours: `pdf-layout-reviewer` (0.193), `public-office-pdf-form-filler` (0.140), `public-office-pdf-watermark` (0.107), `public-office-chat-with-pdf` (0.102), `public-office-pdf-extraction` (0.088)

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | 0.1247 | 0.0607 | 0.0837 | no | pdf, page | page |
| `office-to-markdown-converter` | 0.1247 | 0.0000 | 0.0229 | no | - | preserv |
| `document-field-extractor` | 0.1247 | 0.0000 | 0.0186 | no | - | extract |

Top similarity neighbours: `pdf-ocr-extractor` (0.125), `public-office-pdf-watermark` (0.117), `public-office-pdf-converter` (0.079), `public-office-pdf-ocr` (0.077), `pdf-layout-reviewer` (0.061)

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.1542 | 0.0195 | 0.0299 | no | document | document, preserv |
| `document-rewriter` | 0.1542 | 0.0630 | 0.0687 | no | document, substantive | document, preserv, structure |
| `public-docx` | 0.1542 | 0.1563 | 0.2124 | yes | docx, word, document, edit, comment, change | document, track, change, comment, word, edit |
| `public-office-docx-manipulation` | 0.1542 | 0.0889 | 0.1070 | no | word, document, edit | document, word, edit |

Top similarity neighbours: `public-docx` (0.156), `docx-redline-editor` (0.154), `public-office-docx-manipulation` (0.089), `document-rewriter` (0.063), `public-office-pdf-to-docx` (0.062)

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.0373 | 0.0000 | 0.0236 | no | - | spreadsheet |
| `data-analysis-with-validation` | 0.0373 | 0.0000 | 0.0595 | no | check, assumption, whether | assumption |
| `public-xlsx` | 0.0373 | 0.0286 | 0.0813 | yes | xlsx | spreadsheet, formula, reference, sheet |
| `public-office-xlsx-manipulation` | 0.0373 | 0.0311 | 0.0000 | yes | - | spreadsheet |

Top similarity neighbours: `spreadsheet-formula-auditor` (0.037), `public-swebench-langsmith-fetch` (0.033), `rag-failure-diagnoser` (0.032), `public-office-xlsx-manipulation` (0.031), `public-xlsx` (0.029)

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.3918 | 0.0259 | 0.0639 | no | hierarchy | slide, hierarchy |
| `pdf-layout-reviewer` | 0.3918 | 0.0608 | 0.1062 | no | review, visual, alignment | review, visual, alignment |
| `public-pptx` | 0.3918 | 0.1127 | 0.0735 | no | pptx, presentation, need, text | presentation, slide, text |
| `public-office-ppt-visual` | 0.3918 | 0.0786 | 0.1239 | yes | presentation, visual | presentation, slide, visual |

Top similarity neighbours: `slide-deck-visual-auditor` (0.392), `public-pptx` (0.113), `slide-outline-builder` (0.086), `public-office-ppt-visual` (0.079), `public-oh-my-presentation-builder` (0.065)

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | 0.1508 | 0.0346 | 0.0199 | no | table, layout | table |
| `docx-redline-editor` | 0.1508 | 0.1016 | 0.0299 | no | track, change | document, preserv |
| `document-converter` | 0.1508 | 0.0401 | 0.0880 | no | convert, markdown, layout | convert, document, markdown |

Top similarity neighbours: `layout-preserving-converter` (0.163), `office-to-markdown-converter` (0.151), `public-docx` (0.108), `docx-redline-editor` (0.102), `public-office-docx-manipulation` (0.077)

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `weekly-planner` | 0.1908 | 0.0313 | 0.0928 | no | need, week, extract | note, need, structur, plan |
| `task-extractor` | 0.1908 | 0.0504 | 0.1211 | yes | need, extract | note, need, plan, summary |

Top similarity neighbours: `meeting-agenda-builder` (0.191), `meeting-ops-scenario-planner` (0.114), `meeting-ops-normalizer` (0.109), `meeting-ops-compliance-checker` (0.106), `meeting-ops-dependency-mapper` (0.104)

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 27

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `meeting-followup-extractor` | 0.1015 | 0.1079 | 0.2847 | yes | meet, summary | summary, complet, meet, need, list |
| `task-extractor` | 0.1015 | 0.0563 | 0.1155 | no | summary, note | summary, need, plan |

Top similarity neighbours: `public-office-meeting-notes` (0.289), `meeting-ops-evidence-grounder` (0.190), `meeting-ops-normalizer` (0.188), `meeting-ops-artifact-packager` (0.186), `meeting-ops-compliance-checker` (0.181)

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `meeting-summary-writer` | 0.0945 | 0.0889 | 0.2847 | yes | need, meet, happen | complet, meet, need, list, summary |
| `task-extractor` | 0.0945 | 0.0706 | 0.1880 | yes | need, note | extract, need, summary |

Top similarity neighbours: `public-office-meeting-notes` (0.174), `meeting-agenda-builder` (0.109), `meeting-followup-extractor` (0.095), `meeting-summary-writer` (0.089), `meeting-ops-evidence-grounder` (0.083)

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `weekly-planner` | 0.0926 | 0.0454 | 0.2174 | yes | note, schedul, week | plan, extract, note, need, schedul, weekly |
| `meeting-followup-extractor` | 0.0926 | 0.1501 | 0.1880 | yes | list, complet, meet | extract, need, summary |

Top similarity neighbours: `public-office-meeting-notes` (0.163), `meeting-followup-extractor` (0.150), `meeting-summary-writer` (0.141), `task-extractor` (0.093), `meeting-ops-evidence-grounder` (0.080)

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 181

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `task-extractor` | 0.0191 | 0.0307 | 0.2174 | yes | plan, need, summary, extract | weekly, plan, need, schedul, extract, note |
| `meeting-agenda-builder` | 0.0191 | 0.1120 | 0.0928 | yes | meet, plan, need, summary, agenda | plan, need, structur, note |

Top similarity neighbours: `meeting-agenda-builder` (0.112), `meeting-ops-monitoring-plan-builder` (0.077), `meeting-ops-acceptance-test-builder` (0.075), `meeting-ops-summary-writer` (0.072), `meeting-ops-normalizer` (0.067)

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `general-source-summariser` | 0.2813 | 0.0453 | 0.1787 | yes | recap, summary | summary, recap |
| `method-note-builder` | 0.2813 | 0.0856 | 0.0994 | no | paper, note | paper |
| `citation-note-extractor` | 0.2813 | 0.1272 | 0.0299 | no | citation-ready, note | concise |

Top similarity neighbours: `paper-summariser` (0.281), `citation-note-extractor` (0.127), `public-office-academic-search` (0.103), `public-oh-my-research-paper-writing` (0.091), `method-note-builder` (0.086)

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `paper-summariser` | 0.1026 | 0.1407 | 0.1787 | yes | summary, academic, paper, limit | summary, recap |
| `document-extractor` | 0.1026 | 0.0081 | 0.0462 | no | - | - |
| `citation-note-extractor` | 0.1026 | 0.0069 | 0.0659 | no | - | important |

Top similarity neighbours: `paper-summariser` (0.141), `general-source-summariser` (0.103), `academic-admin-ops-summary-writer` (0.099), `professor-email-reply` (0.090), `academic-admin-ops-evidence-grounder` (0.079)

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-extractor` | 0.2341 | 0.0106 | 0.0869 | no | - | claim |
| `paper-summariser` | 0.2341 | 0.0000 | 0.0299 | no | - | concise |
| `citation-grounding-helper` | 0.2341 | 0.0576 | 0.1193 | no | note | note, claim, support |

Top similarity neighbours: `citation-note-extractor` (0.234), `writing-ops-evidence-grounder` (0.099), `writing-ops-field-extractor` (0.083), `writing-ops-artifact-packager` (0.082), `writing-ops-normalizer` (0.075)

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 122

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | 0.0429 | 0.0102 | 0.0869 | yes | detail | claim |
| `method-note-builder` | 0.0429 | 0.0000 | 0.0749 | no | extract | extract |
| `paper-summariser` | 0.0429 | 0.0000 | 0.0255 | no | - | - |

Top similarity neighbours: `public-office-table-extractor` (0.097), `research-ops-field-extractor` (0.074), `compliance-ops-field-extractor` (0.065), `docs-ops-field-extractor` (0.064), `partnerships-ops-field-extractor` (0.064)

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 181

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `paper-summariser` | 0.0189 | 0.0000 | 0.0994 | no | - | paper |
| `document-extractor` | 0.0189 | 0.0087 | 0.0749 | no | - | extract |
| `citation-note-extractor` | 0.0189 | 0.0074 | 0.0508 | no | - | note |

Top similarity neighbours: `research-ops-scenario-planner` (0.062), `compliance-ops-scenario-planner` (0.056), `docs-ops-scenario-planner` (0.055), `partnerships-ops-scenario-planner` (0.054), `events-ops-scenario-planner` (0.053)

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | 0.1586 | 0.0400 | 0.1193 | no | support | claim, note, support |
| `paper-summariser` | 0.1586 | 0.0000 | 0.0225 | no | - | - |
| `document-extractor` | 0.1586 | 0.0522 | 0.0409 | no | explicit | claim |

Top similarity neighbours: `citation-grounding-helper` (0.159), `public-huggingface-train-sentence-transformers` (0.089), `public-addy-agent-performance-optimization` (0.056), `document-extractor` (0.052), `tool-use-coach` (0.052)

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `related-work-synthesiser` | 0.0491 | 0.1096 | 0.1548 | yes | related-work | multiple, paper |
| `method-note-builder` | 0.0491 | 0.1276 | 0.1245 | yes | evaluation, note | paper, assumption, evaluation, setup |
| `citation-note-extractor` | 0.0491 | 0.1112 | 0.0565 | yes | turn, note | important |

Top similarity neighbours: `method-note-builder` (0.128), `citation-note-extractor` (0.111), `related-work-synthesiser` (0.110), `citation-grounding-helper` (0.075), `note-linker` (0.072)

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `multi-source-comparison-builder` | 0.2153 | 0.0334 | 0.1548 | yes | compare | multiple, paper |
| `citation-note-extractor` | 0.2153 | 0.0059 | 0.0216 | no | note | - |
| `paper-summariser` | 0.2153 | 0.0100 | 0.0218 | no | - | paper, question |

Top similarity neighbours: `related-work-synthesiser` (0.215), `release-note-writer` (0.059), `public-office-table-extractor` (0.056), `public-openai-notion-research-documentation` (0.056), `public-office-deep-research` (0.052)

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.1218 | 0.1187 | 0.1942 | yes | draft, email, reply, message | draft, reply, email, context |
| `reply-polisher` | 0.1218 | 0.0902 | 0.1238 | yes | email, reply, message, tone | reply, email |

Top similarity neighbours: `professor-email-reply` (0.122), `reply-drafter` (0.119), `reply-polisher` (0.090), `email-polisher` (0.062), `email-drafter` (0.058)

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `professor-email-reply` | 0.1474 | 0.0000 | 0.1238 | yes | - | reply, email |
| `reply-drafter` | 0.1474 | 0.1116 | 0.3018 | yes | message | reply, message, email |

Top similarity neighbours: `reply-polisher` (0.147), `reply-drafter` (0.112), `document-rewriter` (0.097), `public-mattpocock-edit-article` (0.090), `email-polisher` (0.049)

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.1807 | 0.1005 | 0.2213 | yes | reply, draft, need | reply, draft, message |
| `followup-reply-writer` | 0.1807 | 0.0590 | 0.2257 | yes | reply, draft | reply, draft, message |

Top similarity neighbours: `groupwork-reply` (0.181), `reply-drafter` (0.101), `reply-polisher` (0.064), `deadline-reminder-planner` (0.061), `followup-reply-writer` (0.059)

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.1111 | 0.0000 | 0.2193 | yes | - | draft, reply, message |
| `groupwork-reply` | 0.1111 | 0.0000 | 0.2257 | yes | - | draft, reply, message |

Top similarity neighbours: `document-summariser` (0.121), `followup-reply-writer` (0.111), `public-office-investment-memo` (0.078), `public-oh-my-state-management` (0.077), `public-oh-my-write-a-skill` (0.068)

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-polisher` | 0.1073 | 0.0780 | 0.3018 | yes | message, reply, polish | reply, message, email |
| `followup-reply-writer` | 0.1073 | 0.0500 | 0.2193 | yes | response, message, reply, action | draft, reply, message |

Top similarity neighbours: `reply-drafter` (0.107), `public-openai-figma-create-new-file` (0.083), `reply-polisher` (0.078), `file-renamer` (0.050), `followup-reply-writer` (0.050)

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.0947 | 0.0116 | 0.0549 | no | security | security |
| `auth-flow-reviewer` | 0.0947 | 0.0183 | 0.0513 | no | security, risk | security, flow |
| `privacy-risk-reviewer` | 0.0947 | 0.0319 | 0.0412 | no | risk | data |

Top similarity neighbours: `public-openai-figma-create-new-file` (0.096), `security-threat-modeler` (0.095), `email-ops-risk-reviewer` (0.066), `public-security-threat-model` (0.059), `email-ops-scenario-planner` (0.058)

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.0970 | 0.0416 | 0.0933 | no | review, implementation | review, code |
| `auth-flow-reviewer` | 0.0970 | 0.0165 | 0.1249 | yes | review, security | review, security, authorization |
| `security-threat-modeler` | 0.0970 | 0.0100 | 0.0549 | no | security | security |

Top similarity neighbours: `security-code-reviewer` (0.097), `public-addy-agent-security-and-hardening` (0.061), `public-swebench-slo-implementation` (0.055), `api-ops-acceptance-test-builder` (0.050), `pr-reviewer` (0.049)

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 21

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.1223 | 0.0000 | 0.0548 | no | - | review |
| `secret-leak-scanner` | 0.1223 | 0.0000 | 0.0220 | no | - | - |
| `ci-failure-debugger` | 0.1223 | 0.0000 | 0.0000 | no | check, need | - |

Top similarity neighbours: `supply-chain-ops-risk-reviewer` (0.177), `supply-chain-ops-dependency-mapper` (0.153), `supply-chain-ops-priority-ranker` (0.146), `supply-chain-ops-artifact-packager` (0.141), `supply-chain-ops-normalizer` (0.140)

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `dependency-risk-auditor` | 0.0926 | 0.0000 | 0.0220 | no | update | - |
| `security-code-reviewer` | 0.0926 | 0.0196 | 0.0899 | no | diff | diff, unsafe |
| `privacy-risk-reviewer` | 0.0926 | 0.0000 | 0.0209 | no | - | - |

Top similarity neighbours: `secret-leak-scanner` (0.093), `public-oh-my-log-analysis` (0.054), `public-office-webhook-automation` (0.053), `webhook-setup-planner` (0.051), `deployment-release-verifier` (0.050)

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.1594 | 0.0000 | 0.1249 | yes | - | review, authorization, security |
| `security-threat-modeler` | 0.1594 | 0.0000 | 0.0513 | no | - | flow, security |
| `privacy-risk-reviewer` | 0.1594 | 0.0000 | 0.0902 | no | - | review, risk |

Top similarity neighbours: `auth-flow-reviewer` (0.159), `public-oh-my-google-workspace` (0.050), `email-ops-monitoring-plan-builder` (0.050), `email-ops-normalizer` (0.043), `version-control-helper` (0.042)

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 111

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-threat-modeler` | 0.0263 | 0.0090 | 0.0412 | no | - | data |
| `secret-leak-scanner` | 0.0263 | 0.0000 | 0.0209 | no | - | - |
| `auth-flow-reviewer` | 0.0263 | 0.0180 | 0.0902 | yes | - | review, risk |

Top similarity neighbours: `public-office-web-search` (0.073), `public-swebench-similarity-search-patterns` (0.053), `query-optimizer` (0.051), `public-oh-my-log-analysis` (0.051), `public-swebench-dbt-transformation-patterns` (0.047)

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 44

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.0398 | 0.0243 | 0.1183 | yes | new, workflow | new |
| `skill-installer` | 0.0398 | 0.0266 | 0.2102 | yes | exist, library | exist, library, user', install |
| `skill-editor` | 0.0398 | 0.0342 | 0.1927 | yes | new, exist, workflow | exist, creat, new |

Top similarity neighbours: `public-office-meeting-notes` (0.099), `library-ops-evidence-grounder` (0.064), `meeting-ops-evidence-grounder` (0.061), `library-ops-timeline-builder` (0.057), `library-ops-rewrite-editor` (0.055)

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-finder` | 0.1337 | 0.0270 | 0.2102 | yes | exist, library | install, exist, user', library |
| `skill-creator` | 0.1337 | 0.0000 | 0.1032 | no | - | - |
| `skill-packager` | 0.1337 | 0.0208 | 0.1503 | yes | exist, prepare, check, file | prepare, exist |

Top similarity neighbours: `skill-installer` (0.134), `library-ops-resource-linker` (0.056), `library-ops-acceptance-test-builder` (0.053), `library-ops-evidence-grounder` (0.052), `library-ops-field-extractor` (0.051)

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-editor` | 0.2381 | 0.1350 | 0.2807 | yes | workflow, new, exist | workflow, new, artifact, description, boundarie, resource |
| `skill-finder` | 0.2381 | 0.1142 | 0.1183 | no | new, exist | new |
| `skill-packager` | 0.2381 | 0.0792 | 0.0773 | no | exist | resource |

Top similarity neighbours: `skill-creator` (0.238), `public-anthropic-skill-creator` (0.157), `meeting-followup-extractor` (0.144), `public-skill-creator` (0.142), `skill-editor` (0.135)

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.1552 | 0.0798 | 0.2807 | yes | description, trigger | artifact, description, workflow, boundarie, resource, new |
| `skill-evaluator` | 0.1552 | 0.1069 | 0.1633 | yes | exist, skill', description, trigger | exist, description, behavior |
| `skill-packager` | 0.1552 | 0.0831 | 0.1309 | yes | exist | exist, resource |

Top similarity neighbours: `public-anthropic-skill-creator` (0.179), `skill-editor` (0.155), `skill-evaluator` (0.107), `public-skill-creator` (0.104), `skill-finder` (0.103)

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-editor` | 0.1331 | 0.0333 | 0.1633 | yes | - | exist, behavior, description |
| `skill-finder` | 0.1331 | 0.0321 | 0.1247 | yes | whether, already | exist, whether |
| `skill-creator` | 0.1331 | 0.0292 | 0.1439 | yes | trigger | trigger, description |

Top similarity neighbours: `reply-polisher` (0.159), `reply-drafter` (0.146), `skill-evaluator` (0.133), `followup-reply-writer` (0.086), `professor-email-reply` (0.081)

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.1425 | 0.0292 | 0.0773 | no | resource | resource |
| `skill-installer` | 0.1425 | 0.0716 | 0.1503 | yes | exist | prepare, exist |
| `skill-editor` | 0.1425 | 0.0503 | 0.1309 | yes | exist, resource | exist, resource |

Top similarity neighbours: `skill-packager` (0.142), `paper-summariser` (0.131), `public-anthropic-skill-creator` (0.078), `skill-installer` (0.072), `agent-ops-resource-linker` (0.067)

