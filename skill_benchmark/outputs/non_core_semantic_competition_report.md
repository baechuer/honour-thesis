# Non-Core Semantic Competition Report

This report checks whether background/public/support skills look more semantically similar to benchmark prompts than the gold core skill under a description-card similarity backend.

Similarity backend: **sklearn_tfidf**.

## Overall Status

- Prompts: 85
- Gold ranked top-1 among all skills: 48/85 (56.5%)
- Non-core skill ranked top-1: 26/85 (30.6%)
- Best non-core skill scores above gold: 30/85 (35.3%)

Interpretation: a non-core skill beating the gold does not automatically mean the gold label is wrong. It means the compressed semantic representation has a plausible scale distractor that may need reranking or richer procedural representation.

## Family Summary

| Prompt family | Prompts | Non-core top-1 | Best non-core beats gold |
|---|---:|---:|---:|
| `api_backend_design` | 6 | 3/6 | 3/6 |
| `browser_web_automation` | 6 | 3/6 | 3/6 |
| `code_github_workflow` | 6 | 0/6 | 0/6 |
| `data_spreadsheet` | 7 | 2/7 | 2/7 |
| `deployment_browser_qa` | 6 | 1/6 | 1/6 |
| `documents_files` | 7 | 2/7 | 4/7 |
| `metrics_observability` | 6 | 3/6 | 3/6 |
| `news_monitoring` | 5 | 1/5 | 1/5 |
| `office_artifact_workflows` | 6 | 1/6 | 1/6 |
| `planning_meetings` | 5 | 3/5 | 4/5 |
| `reading_research` | 8 | 2/8 | 3/8 |
| `reply_messaging` | 5 | 0/5 | 0/5 |
| `security_appsec` | 6 | 3/6 | 3/6 |
| `skill_lifecycle` | 6 | 2/6 | 2/6 |

## Non-Core Families That Beat Gold

| Non-core family | Count |
|---|---:|
| `public_imported_background` | 16 |
| `background_scale` | 14 |

## Prompts Where Non-Core Beats Gold

| Prompt | Gold | Gold rank | Best non-core | Non-core rank | Scores |
|---|---|---:|---|---:|---|
| `api_p2_external_api_integration` | `external-api-integration-planner` | 6 | `public-openai-figma-code-connect-components` (`public_imported_background`) | 1 | gold 0.060; non-core 0.080 |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | `invoice-payment-checker` (`background_scale`) | 1 | gold 0.063; non-core 0.071 |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 201 | `public-office-microsoft-teams` (`public_imported_background`) | 1 | gold 0.012; non-core 0.062 |
| `web_p2_form_filling` | `web-form-filler` | 7 | `public-office-pdf-form-filler` (`public_imported_background`) | 1 | gold 0.055; non-core 0.075 |
| `web_p3_ui_test` | `web-ui-tester` | 48 | `variance-analysis-helper` (`background_scale`) | 1 | gold 0.047; non-core 0.114 |
| `web_p4_data_extraction` | `web-data-extractor` | 250 | `product-ops-resource-linker` (`background_scale`) | 1 | gold 0.010; non-core 0.130 |
| `data_p3_validation` | `data-analysis-with-validation` | 15 | `public-addy-web-web-quality-audit` (`public_imported_background`) | 1 | gold 0.029; non-core 0.063 |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | `decision-matrix-builder` (`background_scale`) | 1 | gold 0.076; non-core 0.120 |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 17 | `public-netlify-deploy` (`public_imported_background`) | 1 | gold 0.027; non-core 0.166 |
| `doc_p3_document_normaliser` | `document-normaliser` | 3 | `deck-template-applier` (`background_scale`) | 2 | gold 0.065; non-core 0.080 |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | `receipt-extractor` (`background_scale`) | 1 | gold 0.043; non-core 0.196 |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | `decision-matrix-builder` (`background_scale`) | 1 | gold 0.038; non-core 0.074 |
| `doc_p6_conversion` | `document-converter` | 5 | `public-obsidian-defuddle` (`public_imported_background`) | 3 | gold 0.061; non-core 0.072 |
| `obs_p1_metrics_overview` | `metrics-overview` | 2 | `public-mattpocock-triage` (`public_imported_background`) | 1 | gold 0.150; non-core 0.160 |
| `obs_p3_slo_breach` | `slo-breach-checker` | 9 | `risk-ops-risk-reviewer` (`background_scale`) | 1 | gold 0.061; non-core 0.091 |
| `obs_p6_incident_summary` | `incident-summary-writer` | 21 | `incident-ops-normalizer` (`background_scale`) | 1 | gold 0.072; non-core 0.088 |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 2 | `product-ops-evidence-grounder` (`background_scale`) | 1 | gold 0.080; non-core 0.081 |
| `office_p3_docx_redline` | `docx-redline-editor` | 2 | `public-docx` (`public_imported_background`) | 1 | gold 0.154; non-core 0.156 |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 27 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.102; non-core 0.289 |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.095; non-core 0.174 |
| `plan_p4_task_extractor` | `task-extractor` | 4 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.093; non-core 0.162 |
| `plan_p5_weekly_planner` | `weekly-planner` | 181 | `meeting-ops-monitoring-plan-builder` (`background_scale`) | 2 | gold 0.019; non-core 0.077 |
| `read_p4_document_extraction` | `document-extractor` | 122 | `public-office-table-extractor` (`public_imported_background`) | 1 | gold 0.043; non-core 0.097 |
| `read_p5_method_notes` | `method-note-builder` | 181 | `research-ops-scenario-planner` (`background_scale`) | 1 | gold 0.019; non-core 0.062 |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 6 | `note-linker` (`background_scale`) | 5 | gold 0.049; non-core 0.072 |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | `public-openai-figma-create-new-file` (`public_imported_background`) | 1 | gold 0.095; non-core 0.096 |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 21 | `supply-chain-ops-risk-reviewer` (`background_scale`) | 1 | gold 0.122; non-core 0.177 |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 111 | `public-office-web-search` (`public_imported_background`) | 1 | gold 0.026; non-core 0.073 |
| `skill_p1_find_existing` | `skill-finder` | 44 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.040; non-core 0.099 |
| `skill_p4_edit_existing` | `skill-editor` | 2 | `public-anthropic-skill-creator` (`public_imported_background`) | 1 | gold 0.155; non-core 0.179 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Gold: `openapi-contract-reviewer`; rank 1; score 0.369
- Best non-core: `openapi-contract-tester`; rank 2; score 0.181
- Top neighbours: `openapi-contract-reviewer`/api_backend_design (0.369), `openapi-contract-tester`/background_scale (0.181), `public-swebench-add-admin-api-endpoint`/public_imported_background (0.081), `contract-ops-acceptance-test-builder`/background_scale (0.079), `api-design-reviewer`/background_scale (0.069)

### `api_p2_external_api_integration`

- Gold: `external-api-integration-planner`; rank 6; score 0.060
- Best non-core: `public-openai-figma-code-connect-components`; rank 1; score 0.080
- Top neighbours: `public-openai-figma-code-connect-components`/public_imported_background (0.080), `api-integration-planner`/background_scale (0.073), `public-swebench-add-admin-api-endpoint`/public_imported_background (0.071), `api-ops-acceptance-test-builder`/background_scale (0.064), `public-office-cover-letter`/public_imported_background (0.062)

### `api_p3_webhook_contract`

- Gold: `webhook-contract-planner`; rank 2; score 0.063
- Best non-core: `invoice-payment-checker`; rank 1; score 0.071
- Top neighbours: `invoice-payment-checker`/background_scale (0.071), `webhook-contract-planner`/api_backend_design (0.063), `public-openai-winui-app`/public_imported_background (0.060), `duplicate-file-finder`/background_scale (0.050), `events-ops-failure-diagnoser`/background_scale (0.050)

### `api_p4_architecture_boundary`

- Gold: `architecture-boundary-reviewer`; rank 1; score 0.357
- Best non-core: `public-architecture-patterns`; rank 2; score 0.120
- Top neighbours: `architecture-boundary-reviewer`/api_backend_design (0.357), `public-architecture-patterns`/public_imported_background (0.120), `public-openai-security-ownership-map`/public_imported_background (0.071), `public-addy-agent-api-and-interface-design`/public_imported_background (0.068), `public-oh-my-backend-testing`/public_imported_background (0.062)

### `api_p5_database_migration_risk`

- Gold: `database-migration-risk-assessor`; rank 1; score 0.136
- Best non-core: `public-addy-agent-shipping-and-launch`; rank 2; score 0.112
- Top neighbours: `database-migration-risk-assessor`/api_backend_design (0.136), `public-addy-agent-shipping-and-launch`/public_imported_background (0.112), `deployment-rollback-planner`/background_scale (0.099), `migration-risk-auditor`/background_scale (0.079), `query-optimizer`/background_scale (0.055)

### `api_p6_service_dependency_map`

- Gold: `service-dependency-mapper`; rank 201; score 0.012
- Best non-core: `public-office-microsoft-teams`; rank 1; score 0.062
- Top neighbours: `public-office-microsoft-teams`/public_imported_background (0.062), `analytics-ops-quality-auditor`/background_scale (0.054), `public-office-data-pipeline`/public_imported_background (0.047), `analytics-ops-evidence-grounder`/background_scale (0.047), `public-office-md-slides`/public_imported_background (0.046)

### `web_p1_page_snapshot`

- Gold: `web-page-snapshotter`; rank 1; score 0.214
- Best non-core: `public-n-skills-dev-browser`; rank 2; score 0.080
- Top neighbours: `web-page-snapshotter`/browser_web_automation (0.214), `public-n-skills-dev-browser`/public_imported_background (0.080), `public-openai-screenshot`/public_imported_background (0.079), `dashboard-ops-summary-writer`/background_scale (0.057), `public-openai-figma-generate-design`/public_imported_background (0.055)

### `web_p2_form_filling`

- Gold: `web-form-filler`; rank 7; score 0.055
- Best non-core: `public-office-pdf-form-filler`; rank 1; score 0.075
- Top neighbours: `public-office-pdf-form-filler`/public_imported_background (0.075), `variance-analysis-helper`/background_scale (0.075), `public-openai-playwright`/public_imported_background (0.073), `public-office-expense-report`/public_imported_background (0.068), `public-office-weekly-report`/public_imported_background (0.068)

### `web_p3_ui_test`

- Gold: `web-ui-tester`; rank 48; score 0.047
- Best non-core: `variance-analysis-helper`; rank 1; score 0.114
- Top neighbours: `variance-analysis-helper`/background_scale (0.114), `web-page-snapshotter`/browser_web_automation (0.058), `public-office-expense-report`/public_imported_background (0.052), `compliance-ops-acceptance-test-builder`/background_scale (0.052), `public-office-weekly-report`/public_imported_background (0.051)

### `web_p4_data_extraction`

- Gold: `web-data-extractor`; rank 250; score 0.010
- Best non-core: `product-ops-resource-linker`; rank 1; score 0.130
- Top neighbours: `product-ops-resource-linker`/background_scale (0.130), `product-ops-field-extractor`/background_scale (0.126), `product-ops-normalizer`/background_scale (0.122), `product-ops-compliance-checker`/background_scale (0.118), `product-ops-dependency-mapper`/background_scale (0.116)

### `web_p5_frontend_debugging`

- Gold: `frontend-debugger`; rank 1; score 0.101
- Best non-core: `api-ops-evidence-grounder`; rank 2; score 0.072
- Top neighbours: `frontend-debugger`/browser_web_automation (0.101), `api-ops-evidence-grounder`/background_scale (0.072), `api-ops-field-extractor`/background_scale (0.062), `api-ops-summary-writer`/background_scale (0.062), `api-ops-normalizer`/background_scale (0.062)

### `web_p6_accessibility_check`

- Gold: `accessibility-checker`; rank 1; score 0.200
- Best non-core: `public-addy-web-accessibility`; rank 3; score 0.130
- Top neighbours: `accessibility-checker`/browser_web_automation (0.200), `accessibility-interaction-auditor`/deployment_browser_qa (0.159), `public-addy-web-accessibility`/public_imported_background (0.130), `public-office-pdf-form-filler`/public_imported_background (0.054), `layout-preserving-converter`/documents_files (0.046)

### `code_p1_local_code_review`

- Gold: `code-reviewer`; rank 1; score 0.074
- Best non-core: `email-ops-acceptance-test-builder`; rank 2; score 0.067
- Top neighbours: `code-reviewer`/code_github_workflow (0.074), `email-ops-acceptance-test-builder`/background_scale (0.067), `git-commit-writer`/background_scale (0.066), `email-ops-risk-reviewer`/background_scale (0.060), `risk-ops-acceptance-test-builder`/background_scale (0.056)

### `code_p2_pr_review`

- Gold: `pr-reviewer`; rank 1; score 0.192
- Best non-core: `pr-description-writer`; rank 2; score 0.165
- Top neighbours: `pr-reviewer`/code_github_workflow (0.192), `pr-description-writer`/background_scale (0.165), `public-mattpocock-review`/public_imported_background (0.081), `public-swebench-analyze-ci`/public_imported_background (0.080), `public-openai-gh-address-comments`/public_imported_background (0.069)

### `code_p3_review_comment_resolution`

- Gold: `review-comment-resolver`; rank 1; score 0.115
- Best non-core: `public-openai-gh-address-comments`; rank 2; score 0.090
- Top neighbours: `review-comment-resolver`/code_github_workflow (0.115), `public-openai-gh-address-comments`/public_imported_background (0.090), `pr-reviewer`/code_github_workflow (0.069), `public-addy-agent-code-review-and-quality`/public_imported_background (0.068), `pr-description-writer`/background_scale (0.062)

### `code_p4_ci_failure_debugging`

- Gold: `ci-failure-debugger`; rank 1; score 0.129
- Best non-core: `public-openai-gh-fix-ci`; rank 3; score 0.067
- Top neighbours: `ci-failure-debugger`/code_github_workflow (0.129), `auth-flow-reviewer`/security_appsec (0.087), `public-openai-gh-fix-ci`/public_imported_background (0.067), `public-mattpocock-diagnose`/public_imported_background (0.060), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.056)

### `code_p5_changelog_entry`

- Gold: `changelog-writer`; rank 1; score 0.168
- Best non-core: `public-swebench-changelog-automation`; rank 3; score 0.139
- Top neighbours: `changelog-writer`/code_github_workflow (0.168), `release-note-writer`/code_github_workflow (0.161), `public-swebench-changelog-automation`/public_imported_background (0.139), `public-oh-my-changelog-maintenance`/public_imported_background (0.127), `public-office-changelog-generator`/public_imported_background (0.115)

### `code_p6_release_notes`

- Gold: `release-note-writer`; rank 1; score 0.162
- Best non-core: `public-oh-my-changelog-maintenance`; rank 2; score 0.089
- Top neighbours: `release-note-writer`/code_github_workflow (0.162), `public-oh-my-changelog-maintenance`/public_imported_background (0.089), `public-office-changelog-generator`/public_imported_background (0.061), `public-swebench-changelog-automation`/public_imported_background (0.056), `public-mattpocock-review`/public_imported_background (0.048)

### `data_p1_overview`

- Gold: `data-analysis-overview`; rank 1; score 0.109
- Best non-core: `public-office-expense-report`; rank 3; score 0.037
- Top neighbours: `data-analysis-overview`/data_spreadsheet (0.109), `data-analysis-for-ranking-selection`/data_spreadsheet (0.046), `public-office-expense-report`/public_imported_background (0.037), `public-office-weekly-report`/public_imported_background (0.036), `public-mattpocock-zoom-out`/public_imported_background (0.033)

### `data_p2_anomaly_focus`

- Gold: `data-analysis-with-anomaly-focus`; rank 1; score 0.191
- Best non-core: `public-addy-agent-debugging-and-error-recovery`; rank 2; score 0.091
- Top neighbours: `data-analysis-with-anomaly-focus`/data_spreadsheet (0.191), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.091), `debugging-root-cause-helper`/background_scale (0.080), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.077), `metrics-root-cause-diagnoser`/metrics_observability (0.060)

### `data_p3_validation`

- Gold: `data-analysis-with-validation`; rank 15; score 0.029
- Best non-core: `public-addy-web-web-quality-audit`; rank 1; score 0.063
- Top neighbours: `public-addy-web-web-quality-audit`/public_imported_background (0.063), `public-oh-my-react-grab`/public_imported_background (0.050), `public-oh-my-react-best-practices`/public_imported_background (0.049), `public-mattpocock-to-issues`/public_imported_background (0.048), `public-oh-my-to-issues`/public_imported_background (0.043)

### `data_p4_root_cause`

- Gold: `data-analysis-for-root-cause-diagnosis`; rank 1; score 0.089
- Best non-core: `public-office-data-analysis`; rank 2; score 0.071
- Top neighbours: `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.089), `public-office-data-analysis`/public_imported_background (0.071), `metrics-root-cause-diagnoser`/metrics_observability (0.069), `public-oh-my-data-analysis`/public_imported_background (0.064), `public-office-stock-analysis`/public_imported_background (0.039)

### `data_p5_reporting`

- Gold: `data-analysis-for-reporting`; rank 1; score 0.100
- Best non-core: `dashboard-ops-handoff-brief-writer`; rank 2; score 0.051
- Top neighbours: `data-analysis-for-reporting`/data_spreadsheet (0.100), `dashboard-ops-handoff-brief-writer`/background_scale (0.051), `geospatial-ops-handoff-brief-writer`/background_scale (0.049), `dashboard-ops-summary-writer`/background_scale (0.040), `public-office-saas-metrics`/public_imported_background (0.039)

### `data_p6_forecasting`

- Gold: `data-analysis-for-forecasting`; rank 1; score 0.138
- Best non-core: `public-oh-my-pattern-detection`; rank 2; score 0.064
- Top neighbours: `data-analysis-for-forecasting`/data_spreadsheet (0.138), `public-oh-my-pattern-detection`/public_imported_background (0.064), `metrics-root-cause-diagnoser`/metrics_observability (0.057), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.043), `duplicate-file-finder`/background_scale (0.041)

### `data_p7_ranking_selection`

- Gold: `data-analysis-for-ranking-selection`; rank 2; score 0.076
- Best non-core: `decision-matrix-builder`; rank 1; score 0.120
- Top neighbours: `decision-matrix-builder`/background_scale (0.120), `data-analysis-for-ranking-selection`/data_spreadsheet (0.076), `risk-ops-comparison-builder`/background_scale (0.060), `dashboard-ops-comparison-builder`/background_scale (0.053), `risk-ops-risk-reviewer`/background_scale (0.043)

### `deploy_p1_playwright_flow_debug`

- Gold: `playwright-flow-debugger`; rank 1; score 0.165
- Best non-core: `public-addy-agent-browser-testing-with-devtools`; rank 3; score 0.076
- Top neighbours: `playwright-flow-debugger`/deployment_browser_qa (0.165), `frontend-debugger`/browser_web_automation (0.076), `public-addy-agent-browser-testing-with-devtools`/public_imported_background (0.076), `public-n-skills-dev-browser`/public_imported_background (0.073), `accessibility-interaction-auditor`/deployment_browser_qa (0.060)

### `deploy_p2_visual_regression`

- Gold: `visual-regression-checker`; rank 1; score 0.326
- Best non-core: `public-anthropic-canvas-design`; rank 3; score 0.063
- Top neighbours: `visual-regression-checker`/deployment_browser_qa (0.326), `slide-deck-visual-auditor`/office_artifact_workflows (0.091), `public-anthropic-canvas-design`/public_imported_background (0.063), `latency-anomaly-detector`/metrics_observability (0.046), `public-addy-agent-performance-optimization`/public_imported_background (0.038)

### `deploy_p3_accessibility_interaction`

- Gold: `accessibility-interaction-auditor`; rank 1; score 0.290
- Best non-core: `public-addy-web-accessibility`; rank 3; score 0.121
- Top neighbours: `accessibility-interaction-auditor`/deployment_browser_qa (0.290), `accessibility-checker`/browser_web_automation (0.143), `public-addy-web-accessibility`/public_imported_background (0.121), `metrics-overview`/metrics_observability (0.057), `public-addy-web-web-quality-audit`/public_imported_background (0.054)

### `deploy_p4_build_log_triage`

- Gold: `deployment-build-triager`; rank 17; score 0.027
- Best non-core: `public-netlify-deploy`; rank 1; score 0.166
- Top neighbours: `public-netlify-deploy`/public_imported_background (0.166), `public-oh-my-game-build-log-triage`/public_imported_background (0.134), `debugging-root-cause-helper`/background_scale (0.129), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.097), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.093)

### `deploy_p5_release_verification`

- Gold: `deployment-release-verifier`; rank 1; score 0.315
- Best non-core: `public-netlify-deploy`; rank 2; score 0.130
- Top neighbours: `deployment-release-verifier`/deployment_browser_qa (0.315), `public-netlify-deploy`/public_imported_background (0.130), `public-openai-vercel-deploy`/public_imported_background (0.093), `public-oh-my-changelog-maintenance`/public_imported_background (0.086), `release-note-writer`/code_github_workflow (0.085)

### `deploy_p6_performance_budget`

- Gold: `web-performance-budget-checker`; rank 1; score 0.169
- Best non-core: `budget-planner`; rank 2; score 0.073
- Top neighbours: `web-performance-budget-checker`/deployment_browser_qa (0.169), `budget-planner`/background_scale (0.073), `mobile-ops-acceptance-test-builder`/background_scale (0.069), `mobile-ops-normalizer`/background_scale (0.064), `mobile-ops-monitoring-plan-builder`/background_scale (0.064)

### `doc_p1_document_summary`

- Gold: `document-summariser`; rank 1; score 0.099
- Best non-core: `knowledge-base-article-writer`; rank 3; score 0.051
- Top neighbours: `document-summariser`/documents_files (0.099), `general-source-summariser`/reading_research (0.055), `knowledge-base-article-writer`/background_scale (0.051), `multi-source-comparison-builder`/reading_research (0.029), `receipt-extractor`/background_scale (0.028)

### `doc_p2_document_rewriter`

- Gold: `document-rewriter`; rank 2; score 0.071
- Best non-core: `public-mattpocock-edit-article`; rank 3; score 0.057
- Top neighbours: `reply-polisher`/reply_messaging (0.112), `document-rewriter`/documents_files (0.071), `public-mattpocock-edit-article`/public_imported_background (0.057), `document-normaliser`/documents_files (0.055), `public-addy-web-accessibility`/public_imported_background (0.046)

### `doc_p3_document_normaliser`

- Gold: `document-normaliser`; rank 3; score 0.065
- Best non-core: `deck-template-applier`; rank 2; score 0.080
- Top neighbours: `layout-preserving-converter`/documents_files (0.085), `deck-template-applier`/background_scale (0.080), `document-normaliser`/documents_files (0.065), `docx-redline-editor`/office_artifact_workflows (0.059), `docs-ops-rewrite-editor`/background_scale (0.051)

### `doc_p4_field_extraction`

- Gold: `document-field-extractor`; rank 6; score 0.043
- Best non-core: `receipt-extractor`; rank 1; score 0.196
- Top neighbours: `receipt-extractor`/background_scale (0.196), `invoice-payment-checker`/background_scale (0.176), `public-office-invoice-automation`/public_imported_background (0.084), `meeting-followup-extractor`/planning_meetings (0.069), `public-office-table-extractor`/public_imported_background (0.055)

### `doc_p5_comparison_preparation`

- Gold: `multi-document-comparison-preparer`; rank 2; score 0.038
- Best non-core: `decision-matrix-builder`; rank 1; score 0.074
- Top neighbours: `decision-matrix-builder`/background_scale (0.074), `multi-document-comparison-preparer`/documents_files (0.038), `compliance-ops-comparison-builder`/background_scale (0.035), `docs-ops-comparison-builder`/background_scale (0.035), `partnerships-ops-comparison-builder`/background_scale (0.034)

### `doc_p6_conversion`

- Gold: `document-converter`; rank 5; score 0.061
- Best non-core: `public-obsidian-defuddle`; rank 3; score 0.072
- Top neighbours: `layout-preserving-converter`/documents_files (0.078), `office-to-markdown-converter`/office_artifact_workflows (0.073), `public-obsidian-defuddle`/public_imported_background (0.072), `pdf-layout-reviewer`/office_artifact_workflows (0.064), `document-converter`/documents_files (0.061)

### `doc_p7_layout_preserving_conversion`

- Gold: `layout-preserving-converter`; rank 1; score 0.167
- Best non-core: `public-office-layout-analyzer`; rank 5; score 0.080
- Top neighbours: `layout-preserving-converter`/documents_files (0.167), `document-converter`/documents_files (0.119), `pdf-layout-reviewer`/office_artifact_workflows (0.107), `office-to-markdown-converter`/office_artifact_workflows (0.090), `public-office-layout-analyzer`/public_imported_background (0.080)

### `obs_p1_metrics_overview`

- Gold: `metrics-overview`; rank 2; score 0.150
- Best non-core: `public-mattpocock-triage`; rank 1; score 0.160
- Top neighbours: `public-mattpocock-triage`/public_imported_background (0.160), `metrics-overview`/metrics_observability (0.150), `public-oh-my-triage`/public_imported_background (0.143), `public-oh-my-game-build-log-triage`/public_imported_background (0.108), `public-oh-my-game-demo-feedback-triage`/public_imported_background (0.105)

### `obs_p2_latency_anomaly`

- Gold: `latency-anomaly-detector`; rank 1; score 0.179
- Best non-core: `public-swebench-service-mesh-observability`; rank 4; score 0.064
- Top neighbours: `latency-anomaly-detector`/metrics_observability (0.179), `metrics-overview`/metrics_observability (0.112), `data-analysis-with-anomaly-focus`/data_spreadsheet (0.085), `public-swebench-service-mesh-observability`/public_imported_background (0.064), `data-analysis-overview`/data_spreadsheet (0.062)

### `obs_p3_slo_breach`

- Gold: `slo-breach-checker`; rank 9; score 0.061
- Best non-core: `risk-ops-risk-reviewer`; rank 1; score 0.091
- Top neighbours: `risk-ops-risk-reviewer`/background_scale (0.091), `sre-ops-risk-reviewer`/background_scale (0.084), `incident-ops-risk-reviewer`/background_scale (0.084), `public-swebench-slo-implementation`/public_imported_background (0.083), `public-swebench-service-mesh-observability`/public_imported_background (0.069)

### `obs_p4_capacity_risk`

- Gold: `capacity-risk-forecaster`; rank 1; score 0.230
- Best non-core: `risk-ops-risk-reviewer`; rank 3; score 0.096
- Top neighbours: `capacity-risk-forecaster`/metrics_observability (0.230), `slo-breach-checker`/metrics_observability (0.114), `risk-ops-risk-reviewer`/background_scale (0.096), `metrics-root-cause-diagnoser`/metrics_observability (0.084), `debugging-root-cause-helper`/background_scale (0.080)

### `obs_p5_root_cause`

- Gold: `metrics-root-cause-diagnoser`; rank 2; score 0.120
- Best non-core: `public-addy-agent-debugging-and-error-recovery`; rank 3; score 0.077
- Top neighbours: `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.162), `metrics-root-cause-diagnoser`/metrics_observability (0.120), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.077), `debugging-root-cause-helper`/background_scale (0.071), `latency-anomaly-detector`/metrics_observability (0.056)

### `obs_p6_incident_summary`

- Gold: `incident-summary-writer`; rank 21; score 0.072
- Best non-core: `incident-ops-normalizer`; rank 1; score 0.088
- Top neighbours: `incident-ops-normalizer`/background_scale (0.088), `incident-ops-compliance-checker`/background_scale (0.086), `incident-ops-dependency-mapper`/background_scale (0.084), `incident-ops-scenario-planner`/background_scale (0.083), `incident-ops-risk-reviewer`/background_scale (0.083)

### `news_p1_plain_summary`

- Gold: `news-summariser`; rank 1; score 0.184
- Best non-core: `public-office-news-monitor`; rank 2; score 0.135
- Top neighbours: `news-summariser`/news_monitoring (0.184), `public-office-news-monitor`/public_imported_background (0.135), `tech-news-trend-extractor`/news_monitoring (0.086), `public-mattpocock-edit-article`/public_imported_background (0.071), `news-theme-extractor`/news_monitoring (0.068)

### `news_p2_briefing`

- Gold: `news-briefing-writer`; rank 1; score 0.080
- Best non-core: `public-mattpocock-edit-article`; rank 2; score 0.073
- Top neighbours: `news-briefing-writer`/news_monitoring (0.080), `public-mattpocock-edit-article`/public_imported_background (0.073), `knowledge-base-article-writer`/background_scale (0.051), `support-ticket-triager`/background_scale (0.050), `support-ops-timeline-builder`/background_scale (0.048)

### `news_p3_grounded_claims`

- Gold: `source-grounding-extractor`; rank 2; score 0.080
- Best non-core: `product-ops-evidence-grounder`; rank 1; score 0.081
- Top neighbours: `product-ops-evidence-grounder`/background_scale (0.081), `source-grounding-extractor`/news_monitoring (0.080), `product-ops-scenario-planner`/background_scale (0.073), `knowledge-base-article-writer`/background_scale (0.069), `product-ops-field-extractor`/background_scale (0.065)

### `news_p4_theme_extraction`

- Gold: `news-theme-extractor`; rank 2; score 0.136
- Best non-core: `public-office-news-monitor`; rank 3; score 0.091
- Top neighbours: `tech-news-trend-extractor`/news_monitoring (0.159), `news-theme-extractor`/news_monitoring (0.136), `public-office-news-monitor`/public_imported_background (0.091), `news-summariser`/news_monitoring (0.068), `data-analysis-for-forecasting`/data_spreadsheet (0.061)

### `news_p5_trend_signal`

- Gold: `tech-news-trend-extractor`; rank 1; score 0.205
- Best non-core: `public-office-news-monitor`; rank 3; score 0.072
- Top neighbours: `tech-news-trend-extractor`/news_monitoring (0.205), `news-summariser`/news_monitoring (0.101), `public-office-news-monitor`/public_imported_background (0.072), `news-briefing-writer`/news_monitoring (0.050), `news-theme-extractor`/news_monitoring (0.049)

### `office_p1_pdf_layout_review`

- Gold: `pdf-layout-reviewer`; rank 1; score 0.193
- Best non-core: `public-office-pdf-form-filler`; rank 2; score 0.140
- Top neighbours: `pdf-layout-reviewer`/office_artifact_workflows (0.193), `public-office-pdf-form-filler`/public_imported_background (0.140), `public-office-pdf-watermark`/public_imported_background (0.107), `public-office-chat-with-pdf`/public_imported_background (0.102), `public-office-pdf-extraction`/public_imported_background (0.088)

### `office_p2_scanned_pdf_ocr`

- Gold: `pdf-ocr-extractor`; rank 1; score 0.125
- Best non-core: `public-office-pdf-watermark`; rank 2; score 0.116
- Top neighbours: `pdf-ocr-extractor`/office_artifact_workflows (0.125), `public-office-pdf-watermark`/public_imported_background (0.116), `public-office-pdf-converter`/public_imported_background (0.079), `public-office-pdf-ocr`/public_imported_background (0.077), `pdf-layout-reviewer`/office_artifact_workflows (0.061)

### `office_p3_docx_redline`

- Gold: `docx-redline-editor`; rank 2; score 0.154
- Best non-core: `public-docx`; rank 1; score 0.156
- Top neighbours: `public-docx`/public_imported_background (0.156), `docx-redline-editor`/office_artifact_workflows (0.154), `public-office-docx-manipulation`/public_imported_background (0.089), `document-rewriter`/documents_files (0.063), `public-office-pdf-to-docx`/public_imported_background (0.062)

### `office_p4_formula_audit`

- Gold: `spreadsheet-formula-auditor`; rank 1; score 0.037
- Best non-core: `public-swebench-langsmith-fetch`; rank 2; score 0.033
- Top neighbours: `spreadsheet-formula-auditor`/office_artifact_workflows (0.037), `public-swebench-langsmith-fetch`/public_imported_background (0.033), `rag-failure-diagnoser`/background_scale (0.032), `public-office-xlsx-manipulation`/public_imported_background (0.031), `public-xlsx`/public_imported_background (0.029)

### `office_p5_slide_visual_audit`

- Gold: `slide-deck-visual-auditor`; rank 1; score 0.392
- Best non-core: `public-pptx`; rank 2; score 0.113
- Top neighbours: `slide-deck-visual-auditor`/office_artifact_workflows (0.392), `public-pptx`/public_imported_background (0.113), `slide-outline-builder`/background_scale (0.086), `public-office-ppt-visual`/public_imported_background (0.079), `public-oh-my-presentation-builder`/public_imported_background (0.064)

### `office_p6_office_to_markdown`

- Gold: `office-to-markdown-converter`; rank 2; score 0.151
- Best non-core: `public-docx`; rank 3; score 0.109
- Top neighbours: `layout-preserving-converter`/documents_files (0.163), `office-to-markdown-converter`/office_artifact_workflows (0.151), `public-docx`/public_imported_background (0.109), `docx-redline-editor`/office_artifact_workflows (0.102), `public-office-docx-manipulation`/public_imported_background (0.077)

### `plan_p1_meeting_agenda`

- Gold: `meeting-agenda-builder`; rank 1; score 0.191
- Best non-core: `meeting-ops-scenario-planner`; rank 2; score 0.114
- Top neighbours: `meeting-agenda-builder`/planning_meetings (0.191), `meeting-ops-scenario-planner`/background_scale (0.114), `meeting-ops-normalizer`/background_scale (0.109), `meeting-ops-compliance-checker`/background_scale (0.106), `meeting-ops-dependency-mapper`/background_scale (0.104)

### `plan_p2_meeting_summary`

- Gold: `meeting-summary-writer`; rank 27; score 0.102
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.289
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.289), `meeting-ops-evidence-grounder`/background_scale (0.190), `meeting-ops-normalizer`/background_scale (0.187), `meeting-ops-artifact-packager`/background_scale (0.186), `meeting-ops-compliance-checker`/background_scale (0.181)

### `plan_p3_meeting_followup`

- Gold: `meeting-followup-extractor`; rank 3; score 0.095
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.174
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.174), `meeting-agenda-builder`/planning_meetings (0.109), `meeting-followup-extractor`/planning_meetings (0.095), `meeting-summary-writer`/planning_meetings (0.089), `meeting-ops-evidence-grounder`/background_scale (0.083)

### `plan_p4_task_extractor`

- Gold: `task-extractor`; rank 4; score 0.093
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.162
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.162), `meeting-followup-extractor`/planning_meetings (0.150), `meeting-summary-writer`/planning_meetings (0.141), `task-extractor`/planning_meetings (0.093), `meeting-ops-evidence-grounder`/background_scale (0.080)

### `plan_p5_weekly_planner`

- Gold: `weekly-planner`; rank 181; score 0.019
- Best non-core: `meeting-ops-monitoring-plan-builder`; rank 2; score 0.077
- Top neighbours: `meeting-agenda-builder`/planning_meetings (0.112), `meeting-ops-monitoring-plan-builder`/background_scale (0.077), `meeting-ops-acceptance-test-builder`/background_scale (0.075), `meeting-ops-summary-writer`/background_scale (0.072), `meeting-ops-normalizer`/background_scale (0.067)

### `read_p1_paper_summary`

- Gold: `paper-summariser`; rank 1; score 0.281
- Best non-core: `public-office-academic-search`; rank 3; score 0.104
- Top neighbours: `paper-summariser`/reading_research (0.281), `citation-note-extractor`/reading_research (0.127), `public-office-academic-search`/public_imported_background (0.104), `public-oh-my-research-paper-writing`/public_imported_background (0.091), `method-note-builder`/reading_research (0.086)

### `read_p2_general_source_summary`

- Gold: `general-source-summariser`; rank 2; score 0.103
- Best non-core: `academic-admin-ops-summary-writer`; rank 3; score 0.099
- Top neighbours: `paper-summariser`/reading_research (0.141), `general-source-summariser`/reading_research (0.103), `academic-admin-ops-summary-writer`/background_scale (0.099), `professor-email-reply`/reply_messaging (0.090), `academic-admin-ops-evidence-grounder`/background_scale (0.079)

### `read_p3_citation_notes`

- Gold: `citation-note-extractor`; rank 1; score 0.234
- Best non-core: `writing-ops-evidence-grounder`; rank 2; score 0.099
- Top neighbours: `citation-note-extractor`/reading_research (0.234), `writing-ops-evidence-grounder`/background_scale (0.099), `writing-ops-field-extractor`/background_scale (0.083), `writing-ops-artifact-packager`/background_scale (0.082), `writing-ops-normalizer`/background_scale (0.075)

### `read_p4_document_extraction`

- Gold: `document-extractor`; rank 122; score 0.043
- Best non-core: `public-office-table-extractor`; rank 1; score 0.097
- Top neighbours: `public-office-table-extractor`/public_imported_background (0.097), `research-ops-field-extractor`/background_scale (0.074), `compliance-ops-field-extractor`/background_scale (0.065), `docs-ops-field-extractor`/background_scale (0.064), `partnerships-ops-field-extractor`/background_scale (0.064)

### `read_p5_method_notes`

- Gold: `method-note-builder`; rank 181; score 0.019
- Best non-core: `research-ops-scenario-planner`; rank 1; score 0.062
- Top neighbours: `research-ops-scenario-planner`/background_scale (0.062), `compliance-ops-scenario-planner`/background_scale (0.056), `docs-ops-scenario-planner`/background_scale (0.055), `partnerships-ops-scenario-planner`/background_scale (0.055), `events-ops-scenario-planner`/background_scale (0.053)

### `read_p6_grounding_check`

- Gold: `citation-grounding-helper`; rank 1; score 0.159
- Best non-core: `public-huggingface-train-sentence-transformers`; rank 2; score 0.089
- Top neighbours: `citation-grounding-helper`/reading_research (0.159), `public-huggingface-train-sentence-transformers`/public_imported_background (0.089), `public-addy-agent-performance-optimization`/public_imported_background (0.056), `document-extractor`/reading_research (0.052), `tool-use-coach`/background_scale (0.052)

### `read_p7_multi_source_comparison`

- Gold: `multi-source-comparison-builder`; rank 6; score 0.049
- Best non-core: `note-linker`; rank 5; score 0.072
- Top neighbours: `method-note-builder`/reading_research (0.128), `citation-note-extractor`/reading_research (0.111), `related-work-synthesiser`/reading_research (0.110), `citation-grounding-helper`/reading_research (0.075), `note-linker`/background_scale (0.072)

### `read_p8_related_work_synthesis`

- Gold: `related-work-synthesiser`; rank 1; score 0.215
- Best non-core: `public-office-table-extractor`; rank 3; score 0.056
- Top neighbours: `related-work-synthesiser`/reading_research (0.215), `release-note-writer`/code_github_workflow (0.059), `public-office-table-extractor`/public_imported_background (0.056), `public-openai-notion-research-documentation`/public_imported_background (0.056), `public-office-deep-research`/public_imported_background (0.052)

### `reply_p1_professor_reply`

- Gold: `professor-email-reply`; rank 1; score 0.122
- Best non-core: `email-polisher`; rank 4; score 0.062
- Top neighbours: `professor-email-reply`/reply_messaging (0.122), `reply-drafter`/reply_messaging (0.119), `reply-polisher`/reply_messaging (0.090), `email-polisher`/email_communication (0.062), `email-drafter`/email_communication (0.058)

### `reply_p2_polish_supervisor`

- Gold: `reply-polisher`; rank 1; score 0.147
- Best non-core: `public-mattpocock-edit-article`; rank 4; score 0.090
- Top neighbours: `reply-polisher`/reply_messaging (0.147), `reply-drafter`/reply_messaging (0.112), `document-rewriter`/documents_files (0.097), `public-mattpocock-edit-article`/public_imported_background (0.090), `email-polisher`/email_communication (0.049)

### `reply_p3_groupwork_coordination`

- Gold: `groupwork-reply`; rank 1; score 0.181
- Best non-core: `deadline-reminder-planner`; rank 4; score 0.061
- Top neighbours: `groupwork-reply`/reply_messaging (0.181), `reply-drafter`/reply_messaging (0.100), `reply-polisher`/reply_messaging (0.064), `deadline-reminder-planner`/background_scale (0.061), `followup-reply-writer`/reply_messaging (0.059)

### `reply_p4_followup_commitment`

- Gold: `followup-reply-writer`; rank 2; score 0.111
- Best non-core: `public-office-investment-memo`; rank 3; score 0.078
- Top neighbours: `document-summariser`/documents_files (0.121), `followup-reply-writer`/reply_messaging (0.111), `public-office-investment-memo`/public_imported_background (0.078), `public-oh-my-state-management`/public_imported_background (0.077), `public-oh-my-write-a-skill`/public_imported_background (0.068)

### `reply_p5_generic_fresh_draft`

- Gold: `reply-drafter`; rank 1; score 0.107
- Best non-core: `public-openai-figma-create-new-file`; rank 2; score 0.083
- Top neighbours: `reply-drafter`/reply_messaging (0.107), `public-openai-figma-create-new-file`/public_imported_background (0.083), `reply-polisher`/reply_messaging (0.078), `file-renamer`/background_scale (0.050), `followup-reply-writer`/reply_messaging (0.050)

### `sec_p1_threat_model`

- Gold: `security-threat-modeler`; rank 2; score 0.095
- Best non-core: `public-openai-figma-create-new-file`; rank 1; score 0.096
- Top neighbours: `public-openai-figma-create-new-file`/public_imported_background (0.096), `security-threat-modeler`/security_appsec (0.095), `email-ops-risk-reviewer`/background_scale (0.066), `public-security-threat-model`/public_imported_background (0.059), `email-ops-scenario-planner`/background_scale (0.058)

### `sec_p2_security_code_review`

- Gold: `security-code-reviewer`; rank 1; score 0.097
- Best non-core: `public-addy-agent-security-and-hardening`; rank 2; score 0.061
- Top neighbours: `security-code-reviewer`/security_appsec (0.097), `public-addy-agent-security-and-hardening`/public_imported_background (0.061), `public-swebench-slo-implementation`/public_imported_background (0.055), `api-ops-acceptance-test-builder`/background_scale (0.050), `pr-reviewer`/code_github_workflow (0.049)

### `sec_p3_dependency_risk`

- Gold: `dependency-risk-auditor`; rank 21; score 0.122
- Best non-core: `supply-chain-ops-risk-reviewer`; rank 1; score 0.177
- Top neighbours: `supply-chain-ops-risk-reviewer`/background_scale (0.177), `supply-chain-ops-dependency-mapper`/background_scale (0.153), `supply-chain-ops-priority-ranker`/background_scale (0.146), `supply-chain-ops-artifact-packager`/background_scale (0.141), `supply-chain-ops-normalizer`/background_scale (0.140)

### `sec_p4_secret_leak`

- Gold: `secret-leak-scanner`; rank 1; score 0.093
- Best non-core: `public-oh-my-log-analysis`; rank 2; score 0.054
- Top neighbours: `secret-leak-scanner`/security_appsec (0.093), `public-oh-my-log-analysis`/public_imported_background (0.054), `public-office-webhook-automation`/public_imported_background (0.053), `webhook-setup-planner`/background_scale (0.050), `deployment-release-verifier`/deployment_browser_qa (0.050)

### `sec_p5_auth_flow`

- Gold: `auth-flow-reviewer`; rank 1; score 0.159
- Best non-core: `public-oh-my-google-workspace`; rank 2; score 0.050
- Top neighbours: `auth-flow-reviewer`/security_appsec (0.159), `public-oh-my-google-workspace`/public_imported_background (0.050), `email-ops-monitoring-plan-builder`/background_scale (0.049), `email-ops-normalizer`/background_scale (0.043), `version-control-helper`/background_scale (0.042)

### `sec_p6_privacy_review`

- Gold: `privacy-risk-reviewer`; rank 111; score 0.026
- Best non-core: `public-office-web-search`; rank 1; score 0.073
- Top neighbours: `public-office-web-search`/public_imported_background (0.073), `public-swebench-similarity-search-patterns`/public_imported_background (0.053), `query-optimizer`/background_scale (0.052), `public-oh-my-log-analysis`/public_imported_background (0.051), `public-swebench-dbt-transformation-patterns`/public_imported_background (0.047)

### `skill_p1_find_existing`

- Gold: `skill-finder`; rank 44; score 0.040
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.099
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.099), `library-ops-evidence-grounder`/background_scale (0.064), `meeting-ops-evidence-grounder`/background_scale (0.061), `library-ops-timeline-builder`/background_scale (0.057), `library-ops-rewrite-editor`/background_scale (0.055)

### `skill_p2_install_existing`

- Gold: `skill-installer`; rank 1; score 0.134
- Best non-core: `library-ops-resource-linker`; rank 2; score 0.056
- Top neighbours: `skill-installer`/skill_lifecycle (0.134), `library-ops-resource-linker`/background_scale (0.056), `library-ops-acceptance-test-builder`/background_scale (0.053), `library-ops-evidence-grounder`/background_scale (0.052), `library-ops-field-extractor`/background_scale (0.051)

### `skill_p3_create_new`

- Gold: `skill-creator`; rank 1; score 0.238
- Best non-core: `public-anthropic-skill-creator`; rank 2; score 0.157
- Top neighbours: `skill-creator`/skill_lifecycle (0.238), `public-anthropic-skill-creator`/public_imported_background (0.157), `meeting-followup-extractor`/planning_meetings (0.144), `public-skill-creator`/public_imported_background (0.142), `skill-editor`/skill_lifecycle (0.135)

### `skill_p4_edit_existing`

- Gold: `skill-editor`; rank 2; score 0.155
- Best non-core: `public-anthropic-skill-creator`; rank 1; score 0.179
- Top neighbours: `public-anthropic-skill-creator`/public_imported_background (0.179), `skill-editor`/skill_lifecycle (0.155), `skill-evaluator`/skill_lifecycle (0.107), `public-skill-creator`/public_imported_background (0.104), `skill-finder`/skill_lifecycle (0.103)

### `skill_p5_evaluate_existing`

- Gold: `skill-evaluator`; rank 3; score 0.133
- Best non-core: `public-anthropic-skill-creator`; rank 7; score 0.076
- Top neighbours: `reply-polisher`/reply_messaging (0.159), `reply-drafter`/reply_messaging (0.146), `skill-evaluator`/skill_lifecycle (0.133), `followup-reply-writer`/reply_messaging (0.086), `professor-email-reply`/reply_messaging (0.081)

### `skill_p6_package_existing`

- Gold: `skill-packager`; rank 1; score 0.142
- Best non-core: `public-anthropic-skill-creator`; rank 3; score 0.078
- Top neighbours: `skill-packager`/skill_lifecycle (0.142), `paper-summariser`/reading_research (0.131), `public-anthropic-skill-creator`/public_imported_background (0.078), `skill-installer`/skill_lifecycle (0.072), `agent-ops-resource-linker`/background_scale (0.067)
