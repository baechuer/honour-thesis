# Non-Core Semantic Competition Report

This report checks whether background/public/support skills look more semantically similar to benchmark prompts than the gold core skill under a description-card similarity backend.

Similarity backend: **sklearn_tfidf**.

## Overall Status

- Prompts: 127
- Gold ranked top-1 among all skills: 76/127 (59.8%)
- Non-core skill ranked top-1: 31/127 (24.4%)
- Best non-core skill scores above gold: 42/127 (33.1%)

Interpretation: a non-core skill beating the gold does not automatically mean the gold label is wrong. It means the compressed semantic representation has a plausible scale distractor that may need reranking or richer procedural representation.

## Family Summary

| Prompt family | Prompts | Non-core top-1 | Best non-core beats gold |
|---|---:|---:|---:|
| `api_backend_design` | 6 | 2/6 | 3/6 |
| `api_mcp_tooling` | 6 | 0/6 | 0/6 |
| `browser_web_automation` | 6 | 2/6 | 3/6 |
| `code_github_workflow` | 6 | 0/6 | 1/6 |
| `data_spreadsheet` | 7 | 2/7 | 2/7 |
| `deployment_browser_qa` | 6 | 1/6 | 1/6 |
| `documents_files` | 7 | 2/7 | 4/7 |
| `github_ci_maintenance` | 6 | 5/6 | 5/6 |
| `huggingface_ml_workflows` | 6 | 0/6 | 0/6 |
| `metrics_observability` | 6 | 3/6 | 3/6 |
| `news_monitoring` | 5 | 1/5 | 1/5 |
| `observability_reliability` | 6 | 3/6 | 3/6 |
| `office_artifact_workflows` | 6 | 1/6 | 1/6 |
| `office_business_automation` | 6 | 1/6 | 1/6 |
| `pdf_document_operations` | 6 | 0/6 | 1/6 |
| `planning_meetings` | 5 | 2/5 | 4/5 |
| `reading_research` | 8 | 2/8 | 3/8 |
| `reply_messaging` | 5 | 0/5 | 0/5 |
| `security_appsec` | 6 | 3/6 | 3/6 |
| `skill_lifecycle` | 6 | 1/6 | 2/6 |
| `skill_representation_analysis` | 6 | 0/6 | 1/6 |

## Non-Core Families That Beat Gold

| Non-core family | Count |
|---|---:|
| `public_imported_background` | 22 |
| `background_scale` | 14 |
| `implicit_field_stress` | 6 |

## Prompts Where Non-Core Beats Gold

| Prompt | Gold | Gold rank | Best non-core | Non-core rank | Scores |
|---|---|---:|---|---:|---|
| `api_p2_external_api_integration` | `external-api-integration-planner` | 7 | `public-openai-figma-code-connect-components` (`public_imported_background`) | 2 | gold 0.060; non-core 0.081 |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | `invoice-payment-checker` (`background_scale`) | 1 | gold 0.063; non-core 0.071 |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 208 | `public-office-microsoft-teams` (`public_imported_background`) | 1 | gold 0.012; non-core 0.062 |
| `web_p2_form_filling` | `web-form-filler` | 8 | `public-office-pdf-form-filler` (`public_imported_background`) | 2 | gold 0.055; non-core 0.075 |
| `web_p3_ui_test` | `web-ui-tester` | 43 | `variance-analysis-helper` (`background_scale`) | 1 | gold 0.047; non-core 0.115 |
| `web_p4_data_extraction` | `web-data-extractor` | 260 | `product-ops-resource-linker` (`background_scale`) | 1 | gold 0.010; non-core 0.131 |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 3 | `implicit-review-comment-planner` (`implicit_field_stress`) | 2 | gold 0.109; non-core 0.134 |
| `data_p3_validation` | `data-analysis-with-validation` | 14 | `public-addy-web-web-quality-audit` (`public_imported_background`) | 1 | gold 0.029; non-core 0.059 |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | `decision-matrix-builder` (`background_scale`) | 1 | gold 0.076; non-core 0.119 |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 18 | `implicit-ci-failure-reader` (`implicit_field_stress`) | 1 | gold 0.027; non-core 0.189 |
| `doc_p3_document_normaliser` | `document-normaliser` | 4 | `deck-template-applier` (`background_scale`) | 2 | gold 0.065; non-core 0.078 |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | `receipt-extractor` (`background_scale`) | 1 | gold 0.041; non-core 0.196 |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | `decision-matrix-builder` (`background_scale`) | 1 | gold 0.039; non-core 0.074 |
| `doc_p6_conversion` | `document-converter` | 5 | `public-obsidian-defuddle` (`public_imported_background`) | 2 | gold 0.060; non-core 0.072 |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 3 | `implicit-ci-failure-reader` (`implicit_field_stress`) | 1 | gold 0.129; non-core 0.259 |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 4 | `public-oh-my-code-review` (`public_imported_background`) | 1 | gold 0.112; non-core 0.171 |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | `public-oh-my-code-review` (`public_imported_background`) | 1 | gold 0.144; non-core 0.163 |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 8 | `public-mattpocock-triage` (`public_imported_background`) | 1 | gold 0.082; non-core 0.232 |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 2 | `public-mattpocock-git-guardrails-claude-code` (`public_imported_background`) | 1 | gold 0.162; non-core 0.253 |
| `obs_p1_metrics_overview` | `metrics-overview` | 2 | `public-mattpocock-triage` (`public_imported_background`) | 1 | gold 0.150; non-core 0.153 |
| `obs_p3_slo_breach` | `slo-breach-checker` | 8 | `risk-ops-risk-reviewer` (`background_scale`) | 1 | gold 0.061; non-core 0.091 |
| `obs_p6_incident_summary` | `incident-summary-writer` | 21 | `incident-ops-normalizer` (`background_scale`) | 1 | gold 0.073; non-core 0.089 |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 2 | `product-ops-evidence-grounder` (`background_scale`) | 1 | gold 0.080; non-core 0.081 |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 2 | `implicit-slo-alert-author` (`implicit_field_stress`) | 1 | gold 0.116; non-core 0.164 |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 15 | `implicit-trace-path-diagnoser` (`implicit_field_stress`) | 1 | gold 0.059; non-core 0.090 |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 2 | `public-oh-my-obsidian-cli-uri-fallback` (`public_imported_background`) | 1 | gold 0.055; non-core 0.064 |
| `office_p3_docx_redline` | `docx-redline-editor` | 2 | `public-docx` (`public_imported_background`) | 1 | gold 0.152; non-core 0.153 |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 2 | `public-office-airtable-automation` (`public_imported_background`) | 1 | gold 0.156; non-core 0.192 |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 3 | `implicit-pdf-table-reconstructor` (`implicit_field_stress`) | 2 | gold 0.124; non-core 0.125 |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 28 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.100; non-core 0.283 |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 4 | `public-office-meeting-notes` (`public_imported_background`) | 1 | gold 0.094; non-core 0.171 |
| `plan_p4_task_extractor` | `task-extractor` | 5 | `public-office-meeting-notes` (`public_imported_background`) | 2 | gold 0.093; non-core 0.160 |
| `plan_p5_weekly_planner` | `weekly-planner` | 181 | `meeting-ops-monitoring-plan-builder` (`background_scale`) | 2 | gold 0.019; non-core 0.076 |
| `read_p4_document_extraction` | `document-extractor` | 123 | `public-office-table-extractor` (`public_imported_background`) | 1 | gold 0.043; non-core 0.088 |
| `read_p5_method_notes` | `method-note-builder` | 184 | `research-ops-scenario-planner` (`background_scale`) | 1 | gold 0.019; non-core 0.063 |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 6 | `note-linker` (`background_scale`) | 5 | gold 0.048; non-core 0.071 |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | `public-openai-figma-create-new-file` (`public_imported_background`) | 1 | gold 0.093; non-core 0.096 |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 21 | `supply-chain-ops-risk-reviewer` (`background_scale`) | 1 | gold 0.123; non-core 0.177 |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 112 | `public-office-web-search` (`public_imported_background`) | 1 | gold 0.026; non-core 0.072 |
| `skill_p1_find_existing` | `skill-finder` | 46 | `public-office-meeting-notes` (`public_imported_background`) | 2 | gold 0.039; non-core 0.097 |
| `skill_p4_edit_existing` | `skill-editor` | 2 | `public-anthropic-skill-creator` (`public_imported_background`) | 1 | gold 0.153; non-core 0.175 |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 15 | `public-anthropic-skill-creator` (`public_imported_background`) | 4 | gold 0.069; non-core 0.136 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Gold: `openapi-contract-reviewer`; rank 1; score 0.357
- Best non-core: `openapi-contract-tester`; rank 3; score 0.172
- Top neighbours: `openapi-contract-reviewer`/api_backend_design (0.357), `rest-api-contract-designer`/api_mcp_tooling (0.202), `openapi-contract-tester`/background_scale (0.172), `public-swebench-add-admin-api-endpoint`/public_imported_background (0.081), `api-documentation-writer`/api_mcp_tooling (0.081)

### `api_p2_external_api_integration`

- Gold: `external-api-integration-planner`; rank 7; score 0.060
- Best non-core: `public-openai-figma-code-connect-components`; rank 2; score 0.081
- Top neighbours: `rest-api-contract-designer`/api_mcp_tooling (0.088), `public-openai-figma-code-connect-components`/public_imported_background (0.081), `api-integration-planner`/background_scale (0.073), `public-swebench-add-admin-api-endpoint`/public_imported_background (0.071), `api-ops-acceptance-test-builder`/background_scale (0.063)

### `api_p3_webhook_contract`

- Gold: `webhook-contract-planner`; rank 2; score 0.063
- Best non-core: `invoice-payment-checker`; rank 1; score 0.071
- Top neighbours: `invoice-payment-checker`/background_scale (0.071), `webhook-contract-planner`/api_backend_design (0.063), `public-openai-winui-app`/public_imported_background (0.058), `duplicate-file-finder`/background_scale (0.050), `events-ops-failure-diagnoser`/background_scale (0.050)

### `api_p4_architecture_boundary`

- Gold: `architecture-boundary-reviewer`; rank 1; score 0.357
- Best non-core: `public-architecture-patterns`; rank 2; score 0.121
- Top neighbours: `architecture-boundary-reviewer`/api_backend_design (0.357), `public-architecture-patterns`/public_imported_background (0.121), `public-openai-security-ownership-map`/public_imported_background (0.069), `public-addy-agent-api-and-interface-design`/public_imported_background (0.066), `public-oh-my-backend-testing`/public_imported_background (0.063)

### `api_p5_database_migration_risk`

- Gold: `database-migration-risk-assessor`; rank 1; score 0.134
- Best non-core: `public-addy-agent-shipping-and-launch`; rank 2; score 0.112
- Top neighbours: `database-migration-risk-assessor`/api_backend_design (0.134), `public-addy-agent-shipping-and-launch`/public_imported_background (0.112), `deployment-rollback-planner`/background_scale (0.097), `migration-risk-auditor`/background_scale (0.080), `risk-ops-monitoring-plan-builder`/background_scale (0.054)

### `api_p6_service_dependency_map`

- Gold: `service-dependency-mapper`; rank 208; score 0.012
- Best non-core: `public-office-microsoft-teams`; rank 1; score 0.062
- Top neighbours: `public-office-microsoft-teams`/public_imported_background (0.062), `analytics-ops-quality-auditor`/background_scale (0.055), `analytics-ops-evidence-grounder`/background_scale (0.047), `public-office-data-pipeline`/public_imported_background (0.047), `implicit-trace-path-diagnoser`/implicit_field_stress (0.045)

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Gold: `rest-api-contract-designer`; rank 1; score 0.311
- Best non-core: `openapi-contract-tester`; rank 5; score 0.067
- Top neighbours: `rest-api-contract-designer`/api_mcp_tooling (0.311), `openapi-contract-reviewer`/api_backend_design (0.144), `mcp-server-builder`/api_mcp_tooling (0.084), `api-documentation-writer`/api_mcp_tooling (0.068), `openapi-contract-tester`/background_scale (0.067)

### `api_mcp_tooling_p2_mcp_server_builder`

- Gold: `mcp-server-builder`; rank 1; score 0.207
- Best non-core: `public-office-office-mcp`; rank 3; score 0.134
- Top neighbours: `mcp-server-builder`/api_mcp_tooling (0.207), `rest-api-contract-designer`/api_mcp_tooling (0.165), `public-office-office-mcp`/public_imported_background (0.134), `public-openai-figma-create-design-system-rules`/public_imported_background (0.114), `public-oh-my-api-design`/public_imported_background (0.109)

### `api_mcp_tooling_p3_webhook_integration_planner`

- Gold: `webhook-integration-planner`; rank 1; score 0.294
- Best non-core: `webhook-setup-planner`; rank 3; score 0.231
- Top neighbours: `webhook-integration-planner`/api_mcp_tooling (0.294), `webhook-contract-planner`/api_backend_design (0.260), `webhook-setup-planner`/background_scale (0.231), `public-office-webhook-automation`/public_imported_background (0.076), `events-ops-acceptance-test-builder`/background_scale (0.072)

### `api_mcp_tooling_p4_auth_flow_integrator`

- Gold: `auth-flow-integrator`; rank 1; score 0.286
- Best non-core: `dashboard-ops-compliance-checker`; rank 3; score 0.063
- Top neighbours: `auth-flow-integrator`/api_mcp_tooling (0.286), `auth-flow-reviewer`/security_appsec (0.104), `dashboard-ops-compliance-checker`/background_scale (0.063), `dashboard-ops-acceptance-test-builder`/background_scale (0.060), `public-office-webhook-automation`/public_imported_background (0.056)

### `api_mcp_tooling_p5_api_documentation_writer`

- Gold: `api-documentation-writer`; rank 1; score 0.229
- Best non-core: `openapi-contract-tester`; rank 2; score 0.079
- Top neighbours: `api-documentation-writer`/api_mcp_tooling (0.229), `openapi-contract-tester`/background_scale (0.079), `rest-api-contract-designer`/api_mcp_tooling (0.075), `contract-ops-evidence-grounder`/background_scale (0.070), `public-openai-cli-creator`/public_imported_background (0.070)

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Gold: `api-security-threat-reviewer`; rank 1; score 0.229
- Best non-core: `public-security-threat-model`; rank 3; score 0.109
- Top neighbours: `api-security-threat-reviewer`/api_mcp_tooling (0.229), `security-code-reviewer`/security_appsec (0.152), `public-security-threat-model`/public_imported_background (0.109), `security-threat-modeler`/security_appsec (0.096), `api-integration-planner`/background_scale (0.065)

### `web_p1_page_snapshot`

- Gold: `web-page-snapshotter`; rank 1; score 0.208
- Best non-core: `public-n-skills-dev-browser`; rank 2; score 0.079
- Top neighbours: `web-page-snapshotter`/browser_web_automation (0.208), `public-n-skills-dev-browser`/public_imported_background (0.079), `public-openai-screenshot`/public_imported_background (0.078), `dashboard-ops-summary-writer`/background_scale (0.055), `changelog-writer`/code_github_workflow (0.055)

### `web_p2_form_filling`

- Gold: `web-form-filler`; rank 8; score 0.055
- Best non-core: `public-office-pdf-form-filler`; rank 2; score 0.075
- Top neighbours: `pdf-form-filler`/pdf_document_operations (0.120), `public-office-pdf-form-filler`/public_imported_background (0.075), `variance-analysis-helper`/background_scale (0.075), `public-openai-playwright`/public_imported_background (0.072), `public-office-expense-report`/public_imported_background (0.069)

### `web_p3_ui_test`

- Gold: `web-ui-tester`; rank 43; score 0.047
- Best non-core: `variance-analysis-helper`; rank 1; score 0.115
- Top neighbours: `variance-analysis-helper`/background_scale (0.115), `web-page-snapshotter`/browser_web_automation (0.053), `public-office-expense-report`/public_imported_background (0.052), `public-office-weekly-report`/public_imported_background (0.052), `compliance-ops-acceptance-test-builder`/background_scale (0.052)

### `web_p4_data_extraction`

- Gold: `web-data-extractor`; rank 260; score 0.010
- Best non-core: `product-ops-resource-linker`; rank 1; score 0.131
- Top neighbours: `product-ops-resource-linker`/background_scale (0.131), `product-ops-field-extractor`/background_scale (0.128), `product-ops-normalizer`/background_scale (0.123), `product-ops-compliance-checker`/background_scale (0.119), `product-ops-dependency-mapper`/background_scale (0.118)

### `web_p5_frontend_debugging`

- Gold: `frontend-debugger`; rank 1; score 0.100
- Best non-core: `api-ops-evidence-grounder`; rank 2; score 0.070
- Top neighbours: `frontend-debugger`/browser_web_automation (0.100), `api-ops-evidence-grounder`/background_scale (0.070), `api-ops-field-extractor`/background_scale (0.060), `api-ops-summary-writer`/background_scale (0.060), `api-ops-normalizer`/background_scale (0.059)

### `web_p6_accessibility_check`

- Gold: `accessibility-checker`; rank 1; score 0.197
- Best non-core: `public-addy-web-accessibility`; rank 3; score 0.131
- Top neighbours: `accessibility-checker`/browser_web_automation (0.197), `accessibility-interaction-auditor`/deployment_browser_qa (0.160), `public-addy-web-accessibility`/public_imported_background (0.131), `public-office-pdf-form-filler`/public_imported_background (0.054), `layout-preserving-converter`/documents_files (0.043)

### `code_p1_local_code_review`

- Gold: `code-reviewer`; rank 1; score 0.072
- Best non-core: `email-ops-acceptance-test-builder`; rank 2; score 0.068
- Top neighbours: `code-reviewer`/code_github_workflow (0.072), `email-ops-acceptance-test-builder`/background_scale (0.068), `git-commit-writer`/background_scale (0.067), `email-ops-risk-reviewer`/background_scale (0.060), `risk-ops-acceptance-test-builder`/background_scale (0.056)

### `code_p2_pr_review`

- Gold: `pr-reviewer`; rank 1; score 0.187
- Best non-core: `pr-description-writer`; rank 2; score 0.161
- Top neighbours: `pr-reviewer`/code_github_workflow (0.187), `pr-description-writer`/background_scale (0.161), `pr-review-comment-resolver`/github_ci_maintenance (0.135), `public-mattpocock-review`/public_imported_background (0.080), `public-swebench-analyze-ci`/public_imported_background (0.077)

### `code_p3_review_comment_resolution`

- Gold: `review-comment-resolver`; rank 3; score 0.109
- Best non-core: `implicit-review-comment-planner`; rank 2; score 0.134
- Top neighbours: `pr-review-comment-resolver`/github_ci_maintenance (0.145), `implicit-review-comment-planner`/implicit_field_stress (0.134), `review-comment-resolver`/code_github_workflow (0.109), `public-openai-gh-address-comments`/public_imported_background (0.088), `pr-reviewer`/code_github_workflow (0.068)

### `code_p4_ci_failure_debugging`

- Gold: `ci-failure-debugger`; rank 1; score 0.126
- Best non-core: `public-openai-gh-fix-ci`; rank 5; score 0.065
- Top neighbours: `ci-failure-debugger`/code_github_workflow (0.126), `auth-flow-reviewer`/security_appsec (0.081), `auth-flow-integrator`/api_mcp_tooling (0.079), `ci-log-root-cause-debugger`/github_ci_maintenance (0.078), `public-openai-gh-fix-ci`/public_imported_background (0.065)

### `code_p5_changelog_entry`

- Gold: `changelog-writer`; rank 1; score 0.167
- Best non-core: `public-swebench-changelog-automation`; rank 4; score 0.134
- Top neighbours: `changelog-writer`/code_github_workflow (0.167), `release-note-writer`/code_github_workflow (0.158), `release-changelog-generator`/github_ci_maintenance (0.139), `public-swebench-changelog-automation`/public_imported_background (0.134), `public-oh-my-changelog-maintenance`/public_imported_background (0.124)

### `code_p6_release_notes`

- Gold: `release-note-writer`; rank 1; score 0.156
- Best non-core: `public-oh-my-changelog-maintenance`; rank 2; score 0.086
- Top neighbours: `release-note-writer`/code_github_workflow (0.156), `public-oh-my-changelog-maintenance`/public_imported_background (0.086), `release-changelog-generator`/github_ci_maintenance (0.073), `public-office-changelog-generator`/public_imported_background (0.058), `public-swebench-changelog-automation`/public_imported_background (0.054)

### `data_p1_overview`

- Gold: `data-analysis-overview`; rank 1; score 0.109
- Best non-core: `public-office-expense-report`; rank 3; score 0.037
- Top neighbours: `data-analysis-overview`/data_spreadsheet (0.109), `data-analysis-for-ranking-selection`/data_spreadsheet (0.046), `public-office-expense-report`/public_imported_background (0.037), `public-office-weekly-report`/public_imported_background (0.036), `public-mattpocock-zoom-out`/public_imported_background (0.032)

### `data_p2_anomaly_focus`

- Gold: `data-analysis-with-anomaly-focus`; rank 1; score 0.192
- Best non-core: `public-addy-agent-debugging-and-error-recovery`; rank 2; score 0.084
- Top neighbours: `data-analysis-with-anomaly-focus`/data_spreadsheet (0.192), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.084), `debugging-root-cause-helper`/background_scale (0.075), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.072), `ci-log-root-cause-debugger`/github_ci_maintenance (0.063)

### `data_p3_validation`

- Gold: `data-analysis-with-validation`; rank 14; score 0.029
- Best non-core: `public-addy-web-web-quality-audit`; rank 1; score 0.059
- Top neighbours: `public-addy-web-web-quality-audit`/public_imported_background (0.059), `public-oh-my-react-grab`/public_imported_background (0.051), `public-oh-my-react-best-practices`/public_imported_background (0.049), `public-mattpocock-to-issues`/public_imported_background (0.047), `public-oh-my-vercel-react-best-practices`/public_imported_background (0.043)

### `data_p4_root_cause`

- Gold: `data-analysis-for-root-cause-diagnosis`; rank 1; score 0.088
- Best non-core: `public-office-data-analysis`; rank 2; score 0.071
- Top neighbours: `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.088), `public-office-data-analysis`/public_imported_background (0.071), `metrics-root-cause-diagnoser`/metrics_observability (0.069), `public-oh-my-data-analysis`/public_imported_background (0.064), `implicit-trace-path-diagnoser`/implicit_field_stress (0.047)

### `data_p5_reporting`

- Gold: `data-analysis-for-reporting`; rank 1; score 0.100
- Best non-core: `dashboard-ops-handoff-brief-writer`; rank 2; score 0.051
- Top neighbours: `data-analysis-for-reporting`/data_spreadsheet (0.100), `dashboard-ops-handoff-brief-writer`/background_scale (0.051), `geospatial-ops-handoff-brief-writer`/background_scale (0.049), `dashboard-ops-summary-writer`/background_scale (0.040), `public-office-saas-metrics`/public_imported_background (0.040)

### `data_p6_forecasting`

- Gold: `data-analysis-for-forecasting`; rank 1; score 0.138
- Best non-core: `public-oh-my-pattern-detection`; rank 2; score 0.061
- Top neighbours: `data-analysis-for-forecasting`/data_spreadsheet (0.138), `public-oh-my-pattern-detection`/public_imported_background (0.061), `metrics-root-cause-diagnoser`/metrics_observability (0.056), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.043), `duplicate-file-finder`/background_scale (0.041)

### `data_p7_ranking_selection`

- Gold: `data-analysis-for-ranking-selection`; rank 2; score 0.076
- Best non-core: `decision-matrix-builder`; rank 1; score 0.119
- Top neighbours: `decision-matrix-builder`/background_scale (0.119), `data-analysis-for-ranking-selection`/data_spreadsheet (0.076), `risk-ops-comparison-builder`/background_scale (0.060), `dashboard-ops-comparison-builder`/background_scale (0.053), `risk-ops-risk-reviewer`/background_scale (0.043)

### `deploy_p1_playwright_flow_debug`

- Gold: `playwright-flow-debugger`; rank 1; score 0.163
- Best non-core: `implicit-browser-flow-investigator`; rank 2; score 0.114
- Top neighbours: `playwright-flow-debugger`/deployment_browser_qa (0.163), `implicit-browser-flow-investigator`/implicit_field_stress (0.114), `public-addy-agent-browser-testing-with-devtools`/public_imported_background (0.075), `frontend-debugger`/browser_web_automation (0.075), `public-n-skills-dev-browser`/public_imported_background (0.072)

### `deploy_p2_visual_regression`

- Gold: `visual-regression-checker`; rank 1; score 0.325
- Best non-core: `implicit-visual-diff-reviewer`; rank 2; score 0.099
- Top neighbours: `visual-regression-checker`/deployment_browser_qa (0.325), `implicit-visual-diff-reviewer`/implicit_field_stress (0.099), `slide-deck-visual-auditor`/office_artifact_workflows (0.090), `public-anthropic-canvas-design`/public_imported_background (0.063), `latency-anomaly-detector`/metrics_observability (0.046)

### `deploy_p3_accessibility_interaction`

- Gold: `accessibility-interaction-auditor`; rank 1; score 0.288
- Best non-core: `public-addy-web-accessibility`; rank 3; score 0.119
- Top neighbours: `accessibility-interaction-auditor`/deployment_browser_qa (0.288), `accessibility-checker`/browser_web_automation (0.141), `public-addy-web-accessibility`/public_imported_background (0.119), `metrics-overview`/metrics_observability (0.057), `public-addy-web-web-quality-audit`/public_imported_background (0.050)

### `deploy_p4_build_log_triage`

- Gold: `deployment-build-triager`; rank 18; score 0.027
- Best non-core: `implicit-ci-failure-reader`; rank 1; score 0.189
- Top neighbours: `implicit-ci-failure-reader`/implicit_field_stress (0.189), `public-netlify-deploy`/public_imported_background (0.169), `public-oh-my-game-build-log-triage`/public_imported_background (0.133), `debugging-root-cause-helper`/background_scale (0.123), `ci-log-root-cause-debugger`/github_ci_maintenance (0.100)

### `deploy_p5_release_verification`

- Gold: `deployment-release-verifier`; rank 1; score 0.314
- Best non-core: `public-netlify-deploy`; rank 2; score 0.131
- Top neighbours: `deployment-release-verifier`/deployment_browser_qa (0.314), `public-netlify-deploy`/public_imported_background (0.131), `public-openai-vercel-deploy`/public_imported_background (0.093), `public-oh-my-changelog-maintenance`/public_imported_background (0.083), `release-note-writer`/code_github_workflow (0.082)

### `deploy_p6_performance_budget`

- Gold: `web-performance-budget-checker`; rank 1; score 0.166
- Best non-core: `mobile-ops-acceptance-test-builder`; rank 2; score 0.069
- Top neighbours: `web-performance-budget-checker`/deployment_browser_qa (0.166), `mobile-ops-acceptance-test-builder`/background_scale (0.069), `mobile-ops-normalizer`/background_scale (0.064), `mobile-ops-monitoring-plan-builder`/background_scale (0.064), `mobile-ops-compliance-checker`/background_scale (0.062)

### `doc_p1_document_summary`

- Gold: `document-summariser`; rank 1; score 0.098
- Best non-core: `knowledge-base-article-writer`; rank 3; score 0.050
- Top neighbours: `document-summariser`/documents_files (0.098), `general-source-summariser`/reading_research (0.055), `knowledge-base-article-writer`/background_scale (0.050), `multi-source-comparison-builder`/reading_research (0.029), `receipt-extractor`/background_scale (0.027)

### `doc_p2_document_rewriter`

- Gold: `document-rewriter`; rank 2; score 0.071
- Best non-core: `public-mattpocock-edit-article`; rank 3; score 0.058
- Top neighbours: `reply-polisher`/reply_messaging (0.112), `document-rewriter`/documents_files (0.071), `public-mattpocock-edit-article`/public_imported_background (0.058), `document-normaliser`/documents_files (0.055), `public-office-pdf-form-filler`/public_imported_background (0.046)

### `doc_p3_document_normaliser`

- Gold: `document-normaliser`; rank 4; score 0.065
- Best non-core: `deck-template-applier`; rank 2; score 0.078
- Top neighbours: `layout-preserving-converter`/documents_files (0.082), `deck-template-applier`/background_scale (0.078), `pdf-to-docx-converter`/pdf_document_operations (0.070), `document-normaliser`/documents_files (0.065), `docx-redline-editor`/office_artifact_workflows (0.059)

### `doc_p4_field_extraction`

- Gold: `document-field-extractor`; rank 6; score 0.041
- Best non-core: `receipt-extractor`; rank 1; score 0.196
- Top neighbours: `receipt-extractor`/background_scale (0.196), `invoice-payment-checker`/background_scale (0.173), `public-office-invoice-automation`/public_imported_background (0.081), `meeting-followup-extractor`/planning_meetings (0.067), `public-office-table-extractor`/public_imported_background (0.049)

### `doc_p5_comparison_preparation`

- Gold: `multi-document-comparison-preparer`; rank 2; score 0.039
- Best non-core: `decision-matrix-builder`; rank 1; score 0.074
- Top neighbours: `decision-matrix-builder`/background_scale (0.074), `multi-document-comparison-preparer`/documents_files (0.039), `compliance-ops-comparison-builder`/background_scale (0.035), `docs-ops-comparison-builder`/background_scale (0.035), `partnerships-ops-comparison-builder`/background_scale (0.035)

### `doc_p6_conversion`

- Gold: `document-converter`; rank 5; score 0.060
- Best non-core: `public-obsidian-defuddle`; rank 2; score 0.072
- Top neighbours: `layout-preserving-converter`/documents_files (0.074), `public-obsidian-defuddle`/public_imported_background (0.072), `office-to-markdown-converter`/office_artifact_workflows (0.071), `pdf-layout-reviewer`/office_artifact_workflows (0.062), `document-converter`/documents_files (0.060)

### `doc_p7_layout_preserving_conversion`

- Gold: `layout-preserving-converter`; rank 1; score 0.161
- Best non-core: `public-office-layout-analyzer`; rank 6; score 0.076
- Top neighbours: `layout-preserving-converter`/documents_files (0.161), `document-converter`/documents_files (0.119), `pdf-layout-reviewer`/office_artifact_workflows (0.105), `office-to-markdown-converter`/office_artifact_workflows (0.088), `pdf-layout-table-extractor`/pdf_document_operations (0.088)

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Gold: `ci-log-root-cause-debugger`; rank 3; score 0.129
- Best non-core: `implicit-ci-failure-reader`; rank 1; score 0.259
- Top neighbours: `implicit-ci-failure-reader`/implicit_field_stress (0.259), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.144), `ci-log-root-cause-debugger`/github_ci_maintenance (0.129), `debugging-root-cause-helper`/background_scale (0.096), `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.093)

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Gold: `pr-review-comment-resolver`; rank 4; score 0.112
- Best non-core: `public-oh-my-code-review`; rank 1; score 0.171
- Top neighbours: `public-oh-my-code-review`/public_imported_background (0.171), `implicit-review-comment-planner`/implicit_field_stress (0.156), `public-addy-agent-code-review-and-quality`/public_imported_background (0.133), `pr-review-comment-resolver`/github_ci_maintenance (0.112), `review-comment-resolver`/code_github_workflow (0.105)

### `github_ci_maintenance_p3_repo_code_reviewer`

- Gold: `repo-code-reviewer`; rank 2; score 0.144
- Best non-core: `public-oh-my-code-review`; rank 1; score 0.163
- Top neighbours: `public-oh-my-code-review`/public_imported_background (0.163), `repo-code-reviewer`/github_ci_maintenance (0.144), `ci-log-root-cause-debugger`/github_ci_maintenance (0.114), `public-addy-agent-code-review-and-quality`/public_imported_background (0.110), `code-reviewer`/code_github_workflow (0.109)

### `github_ci_maintenance_p4_github_issue_triager`

- Gold: `github-issue-triager`; rank 8; score 0.082
- Best non-core: `public-mattpocock-triage`; rank 1; score 0.232
- Top neighbours: `public-mattpocock-triage`/public_imported_background (0.232), `public-mattpocock-to-issues`/public_imported_background (0.123), `public-oh-my-to-issues`/public_imported_background (0.109), `public-n-skills-open-source-maintainer`/public_imported_background (0.101), `public-mattpocock-setup-matt-pocock-skills`/public_imported_background (0.101)

### `github_ci_maintenance_p5_release_changelog_generator`

- Gold: `release-changelog-generator`; rank 1; score 0.134
- Best non-core: `public-oh-my-changelog-maintenance`; rank 3; score 0.107
- Top neighbours: `release-changelog-generator`/github_ci_maintenance (0.134), `release-note-writer`/code_github_workflow (0.119), `public-oh-my-changelog-maintenance`/public_imported_background (0.107), `review-comment-resolver`/code_github_workflow (0.087), `public-office-changelog-generator`/public_imported_background (0.086)

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Gold: `git-safety-guardrail-installer`; rank 2; score 0.162
- Best non-core: `public-mattpocock-git-guardrails-claude-code`; rank 1; score 0.253
- Top neighbours: `public-mattpocock-git-guardrails-claude-code`/public_imported_background (0.253), `git-safety-guardrail-installer`/github_ci_maintenance (0.162), `public-mattpocock-triage`/public_imported_background (0.116), `public-oh-my-git-guardrails-claude-code`/public_imported_background (0.087), `public-mattpocock-setup-matt-pocock-skills`/public_imported_background (0.073)

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Gold: `hf-dataset-viewer-inspector`; rank 1; score 0.206
- Best non-core: `implicit-hf-dataset-inspector`; rank 2; score 0.162
- Top neighbours: `hf-dataset-viewer-inspector`/huggingface_ml_workflows (0.206), `implicit-hf-dataset-inspector`/implicit_field_stress (0.162), `dataset-ops-acceptance-test-builder`/background_scale (0.070), `dataset-ops-intake-classifier`/background_scale (0.067), `dataset-ops-normalizer`/background_scale (0.062)

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Gold: `hf-local-model-selector`; rank 1; score 0.212
- Best non-core: `implicit-hf-local-model-chooser`; rank 2; score 0.210
- Top neighbours: `hf-local-model-selector`/huggingface_ml_workflows (0.212), `implicit-hf-local-model-chooser`/implicit_field_stress (0.210), `public-huggingface-hf-cli`/public_imported_background (0.127), `public-huggingface-huggingface-llm-trainer`/public_imported_background (0.105), `support-ticket-triager`/background_scale (0.095)

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Gold: `sentence-transformer-finetuner`; rank 1; score 0.351
- Best non-core: `agent-ops-monitoring-plan-builder`; rank 2; score 0.116
- Top neighbours: `sentence-transformer-finetuner`/huggingface_ml_workflows (0.351), `agent-ops-monitoring-plan-builder`/background_scale (0.116), `agent-ops-intake-classifier`/background_scale (0.107), `agent-ops-normalizer`/background_scale (0.106), `agent-ops-compliance-checker`/background_scale (0.102)

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Gold: `gradio-demo-builder`; rank 3; score 0.063
- Best non-core: `public-swebench-python-packaging`; rank 4; score 0.062
- Top neighbours: `web-ui-tester`/browser_web_automation (0.107), `sentence-transformer-finetuner`/huggingface_ml_workflows (0.075), `gradio-demo-builder`/huggingface_ml_workflows (0.063), `public-swebench-python-packaging`/public_imported_background (0.062), `public-huggingface-huggingface-vision-trainer`/public_imported_background (0.062)

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Gold: `hf-zerogpu-space-deployer`; rank 1; score 0.270
- Best non-core: `public-huggingface-huggingface-zerogpu`; rank 2; score 0.216
- Top neighbours: `hf-zerogpu-space-deployer`/huggingface_ml_workflows (0.270), `public-huggingface-huggingface-zerogpu`/public_imported_background (0.216), `public-huggingface-hf-cli`/public_imported_background (0.157), `public-huggingface-huggingface-papers`/public_imported_background (0.087), `public-huggingface-huggingface-llm-trainer`/public_imported_background (0.085)

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Gold: `hf-community-eval-runner`; rank 1; score 0.142
- Best non-core: `public-huggingface-hf-cli`; rank 2; score 0.129
- Top neighbours: `hf-community-eval-runner`/huggingface_ml_workflows (0.142), `public-huggingface-hf-cli`/public_imported_background (0.129), `hf-dataset-viewer-inspector`/huggingface_ml_workflows (0.096), `public-huggingface-huggingface-vision-trainer`/public_imported_background (0.078), `public-swebench-llm-evaluation`/public_imported_background (0.075)

### `obs_p1_metrics_overview`

- Gold: `metrics-overview`; rank 2; score 0.150
- Best non-core: `public-mattpocock-triage`; rank 1; score 0.153
- Top neighbours: `public-mattpocock-triage`/public_imported_background (0.153), `metrics-overview`/metrics_observability (0.150), `public-oh-my-triage`/public_imported_background (0.135), `public-oh-my-game-build-log-triage`/public_imported_background (0.102), `public-oh-my-game-demo-feedback-triage`/public_imported_background (0.099)

### `obs_p2_latency_anomaly`

- Gold: `latency-anomaly-detector`; rank 1; score 0.172
- Best non-core: `public-swebench-service-mesh-observability`; rank 5; score 0.059
- Top neighbours: `latency-anomaly-detector`/metrics_observability (0.172), `metrics-overview`/metrics_observability (0.110), `data-analysis-with-anomaly-focus`/data_spreadsheet (0.086), `data-analysis-overview`/data_spreadsheet (0.061), `public-swebench-service-mesh-observability`/public_imported_background (0.059)

### `obs_p3_slo_breach`

- Gold: `slo-breach-checker`; rank 8; score 0.061
- Best non-core: `risk-ops-risk-reviewer`; rank 1; score 0.091
- Top neighbours: `risk-ops-risk-reviewer`/background_scale (0.091), `sre-ops-risk-reviewer`/background_scale (0.084), `incident-ops-risk-reviewer`/background_scale (0.084), `public-swebench-slo-implementation`/public_imported_background (0.081), `public-swebench-service-mesh-observability`/public_imported_background (0.066)

### `obs_p4_capacity_risk`

- Gold: `capacity-risk-forecaster`; rank 1; score 0.231
- Best non-core: `risk-ops-risk-reviewer`; rank 4; score 0.097
- Top neighbours: `capacity-risk-forecaster`/metrics_observability (0.231), `slo-breach-narrative-writer`/observability_reliability (0.123), `slo-breach-checker`/metrics_observability (0.104), `risk-ops-risk-reviewer`/background_scale (0.097), `metrics-root-cause-diagnoser`/metrics_observability (0.080)

### `obs_p5_root_cause`

- Gold: `metrics-root-cause-diagnoser`; rank 2; score 0.118
- Best non-core: `public-addy-agent-debugging-and-error-recovery`; rank 3; score 0.072
- Top neighbours: `data-analysis-for-root-cause-diagnosis`/data_spreadsheet (0.157), `metrics-root-cause-diagnoser`/metrics_observability (0.118), `public-addy-agent-debugging-and-error-recovery`/public_imported_background (0.072), `implicit-ci-failure-reader`/implicit_field_stress (0.069), `debugging-root-cause-helper`/background_scale (0.067)

### `obs_p6_incident_summary`

- Gold: `incident-summary-writer`; rank 21; score 0.073
- Best non-core: `incident-ops-normalizer`; rank 1; score 0.089
- Top neighbours: `incident-ops-normalizer`/background_scale (0.089), `incident-ops-compliance-checker`/background_scale (0.086), `incident-ops-dependency-mapper`/background_scale (0.085), `incident-ops-scenario-planner`/background_scale (0.084), `incident-ops-risk-reviewer`/background_scale (0.083)

### `news_p1_plain_summary`

- Gold: `news-summariser`; rank 1; score 0.185
- Best non-core: `public-office-news-monitor`; rank 2; score 0.135
- Top neighbours: `news-summariser`/news_monitoring (0.185), `public-office-news-monitor`/public_imported_background (0.135), `tech-news-trend-extractor`/news_monitoring (0.087), `public-mattpocock-edit-article`/public_imported_background (0.071), `news-theme-extractor`/news_monitoring (0.069)

### `news_p2_briefing`

- Gold: `news-briefing-writer`; rank 1; score 0.080
- Best non-core: `public-mattpocock-edit-article`; rank 2; score 0.074
- Top neighbours: `news-briefing-writer`/news_monitoring (0.080), `public-mattpocock-edit-article`/public_imported_background (0.074), `knowledge-base-article-writer`/background_scale (0.051), `support-ticket-triager`/background_scale (0.050), `support-ops-timeline-builder`/background_scale (0.047)

### `news_p3_grounded_claims`

- Gold: `source-grounding-extractor`; rank 2; score 0.080
- Best non-core: `product-ops-evidence-grounder`; rank 1; score 0.081
- Top neighbours: `product-ops-evidence-grounder`/background_scale (0.081), `source-grounding-extractor`/news_monitoring (0.080), `product-ops-scenario-planner`/background_scale (0.073), `knowledge-base-article-writer`/background_scale (0.068), `product-ops-field-extractor`/background_scale (0.065)

### `news_p4_theme_extraction`

- Gold: `news-theme-extractor`; rank 2; score 0.136
- Best non-core: `public-office-news-monitor`; rank 3; score 0.091
- Top neighbours: `tech-news-trend-extractor`/news_monitoring (0.160), `news-theme-extractor`/news_monitoring (0.136), `public-office-news-monitor`/public_imported_background (0.091), `news-summariser`/news_monitoring (0.069), `data-analysis-for-forecasting`/data_spreadsheet (0.061)

### `news_p5_trend_signal`

- Gold: `tech-news-trend-extractor`; rank 1; score 0.205
- Best non-core: `public-office-news-monitor`; rank 3; score 0.072
- Top neighbours: `tech-news-trend-extractor`/news_monitoring (0.205), `news-summariser`/news_monitoring (0.101), `public-office-news-monitor`/public_imported_background (0.072), `news-briefing-writer`/news_monitoring (0.051), `news-theme-extractor`/news_monitoring (0.049)

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Gold: `prometheus-alert-rule-writer`; rank 2; score 0.116
- Best non-core: `implicit-slo-alert-author`; rank 1; score 0.164
- Top neighbours: `implicit-slo-alert-author`/implicit_field_stress (0.164), `prometheus-alert-rule-writer`/observability_reliability (0.116), `slo-breach-narrative-writer`/observability_reliability (0.070), `latency-anomaly-detector`/metrics_observability (0.056), `budget-planner`/background_scale (0.056)

### `observability_reliability_p2_grafana_dashboard_builder`

- Gold: `grafana-dashboard-builder`; rank 1; score 0.485
- Best non-core: `dashboard-ops-monitoring-plan-builder`; rank 4; score 0.066
- Top neighbours: `grafana-dashboard-builder`/observability_reliability (0.485), `prometheus-alert-rule-writer`/observability_reliability (0.137), `metrics-overview`/metrics_observability (0.102), `dashboard-ops-monitoring-plan-builder`/background_scale (0.066), `dashboard-ops-normalizer`/background_scale (0.058)

### `observability_reliability_p3_distributed_trace_investigator`

- Gold: `distributed-trace-investigator`; rank 15; score 0.059
- Best non-core: `implicit-trace-path-diagnoser`; rank 1; score 0.090
- Top neighbours: `implicit-trace-path-diagnoser`/implicit_field_stress (0.090), `dashboard-ops-normalizer`/background_scale (0.064), `dashboard-ops-compliance-checker`/background_scale (0.063), `dashboard-ops-dependency-mapper`/background_scale (0.062), `dashboard-ops-risk-reviewer`/background_scale (0.061)

### `observability_reliability_p4_slo_breach_narrative_writer`

- Gold: `slo-breach-narrative-writer`; rank 1; score 0.511
- Best non-core: `compliance-ops-timeline-builder`; rank 5; score 0.068
- Top neighbours: `slo-breach-narrative-writer`/observability_reliability (0.511), `slo-breach-checker`/metrics_observability (0.126), `meeting-followup-extractor`/planning_meetings (0.110), `web-performance-budget-checker`/deployment_browser_qa (0.068), `compliance-ops-timeline-builder`/background_scale (0.068)

### `observability_reliability_p5_resilience_pattern_reviewer`

- Gold: `resilience-pattern-reviewer`; rank 2; score 0.055
- Best non-core: `public-oh-my-obsidian-cli-uri-fallback`; rank 1; score 0.064
- Top neighbours: `public-oh-my-obsidian-cli-uri-fallback`/public_imported_background (0.064), `resilience-pattern-reviewer`/observability_reliability (0.055), `public-swebench-python-resilience`/public_imported_background (0.049), `webhook-setup-planner`/background_scale (0.049), `skill-router-policy-designer`/skill_representation_analysis (0.035)

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Gold: `service-mesh-traffic-debugger`; rank 1; score 0.386
- Best non-core: `public-swebench-linkerd-patterns`; rank 2; score 0.137
- Top neighbours: `service-mesh-traffic-debugger`/observability_reliability (0.386), `public-swebench-linkerd-patterns`/public_imported_background (0.137), `public-swebench-istio-traffic-management`/public_imported_background (0.135), `public-swebench-service-mesh-observability`/public_imported_background (0.116), `public-office-pdf-merge-split`/public_imported_background (0.080)

### `office_p1_pdf_layout_review`

- Gold: `pdf-layout-reviewer`; rank 1; score 0.181
- Best non-core: `public-office-pdf-form-filler`; rank 2; score 0.129
- Top neighbours: `pdf-layout-reviewer`/office_artifact_workflows (0.181), `public-office-pdf-form-filler`/public_imported_background (0.129), `pdf-layout-table-extractor`/pdf_document_operations (0.115), `pdf-form-filler`/pdf_document_operations (0.103), `public-office-pdf-watermark`/public_imported_background (0.099)

### `office_p2_scanned_pdf_ocr`

- Gold: `pdf-ocr-extractor`; rank 1; score 0.121
- Best non-core: `public-office-pdf-watermark`; rank 3; score 0.112
- Top neighbours: `pdf-ocr-extractor`/office_artifact_workflows (0.121), `pdf-ocr-cleaner`/pdf_document_operations (0.118), `public-office-pdf-watermark`/public_imported_background (0.112), `public-office-pdf-ocr`/public_imported_background (0.073), `public-office-pdf-converter`/public_imported_background (0.071)

### `office_p3_docx_redline`

- Gold: `docx-redline-editor`; rank 2; score 0.152
- Best non-core: `public-docx`; rank 1; score 0.153
- Top neighbours: `public-docx`/public_imported_background (0.153), `docx-redline-editor`/office_artifact_workflows (0.152), `public-office-docx-manipulation`/public_imported_background (0.086), `pdf-to-docx-converter`/pdf_document_operations (0.081), `document-rewriter`/documents_files (0.063)

### `office_p4_formula_audit`

- Gold: `spreadsheet-formula-auditor`; rank 1; score 0.038
- Best non-core: `rag-failure-diagnoser`; rank 2; score 0.032
- Top neighbours: `spreadsheet-formula-auditor`/office_artifact_workflows (0.038), `rag-failure-diagnoser`/background_scale (0.032), `public-swebench-langsmith-fetch`/public_imported_background (0.031), `public-office-xlsx-manipulation`/public_imported_background (0.030), `public-xlsx`/public_imported_background (0.028)

### `office_p5_slide_visual_audit`

- Gold: `slide-deck-visual-auditor`; rank 1; score 0.391
- Best non-core: `public-pptx`; rank 2; score 0.113
- Top neighbours: `slide-deck-visual-auditor`/office_artifact_workflows (0.391), `public-pptx`/public_imported_background (0.113), `slide-outline-builder`/background_scale (0.086), `public-office-ppt-visual`/public_imported_background (0.078), `public-oh-my-presentation-builder`/public_imported_background (0.065)

### `office_p6_office_to_markdown`

- Gold: `office-to-markdown-converter`; rank 2; score 0.149
- Best non-core: `public-docx`; rank 3; score 0.105
- Top neighbours: `layout-preserving-converter`/documents_files (0.157), `office-to-markdown-converter`/office_artifact_workflows (0.149), `public-docx`/public_imported_background (0.105), `docx-redline-editor`/office_artifact_workflows (0.101), `pdf-to-docx-converter`/pdf_document_operations (0.093)

### `office_business_automation_p1_xlsx_formula_model_builder`

- Gold: `xlsx-formula-model-builder`; rank 1; score 0.287
- Best non-core: `public-office-airtable-automation`; rank 2; score 0.149
- Top neighbours: `xlsx-formula-model-builder`/office_business_automation (0.287), `public-office-airtable-automation`/public_imported_background (0.149), `spreadsheet-formula-auditor`/office_artifact_workflows (0.147), `public-office-subscription-management`/public_imported_background (0.101), `airtable-workflow-automator`/office_business_automation (0.070)

### `office_business_automation_p2_airtable_workflow_automator`

- Gold: `airtable-workflow-automator`; rank 2; score 0.156
- Best non-core: `public-office-airtable-automation`; rank 1; score 0.192
- Top neighbours: `public-office-airtable-automation`/public_imported_background (0.192), `airtable-workflow-automator`/office_business_automation (0.156), `skill-authoring-guide`/skill_representation_analysis (0.123), `public-anthropic-slack-gif-creator`/public_imported_background (0.084), `public-office-slack-workflows`/public_imported_background (0.081)

### `office_business_automation_p3_notion_research_database_builder`

- Gold: `notion-research-database-builder`; rank 1; score 0.402
- Best non-core: `public-openai-notion-research-documentation`; rank 2; score 0.127
- Top neighbours: `notion-research-database-builder`/office_business_automation (0.402), `public-openai-notion-research-documentation`/public_imported_background (0.127), `public-office-notion-automation`/public_imported_background (0.121), `thesis-ops-rewrite-editor`/background_scale (0.100), `public-openai-notion-knowledge-capture`/public_imported_background (0.096)

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Gold: `calendar-scheduling-optimizer`; rank 1; score 0.170
- Best non-core: `meeting-ops-comparison-builder`; rank 2; score 0.128
- Top neighbours: `calendar-scheduling-optimizer`/office_business_automation (0.170), `meeting-ops-comparison-builder`/background_scale (0.128), `meeting-ops-evidence-grounder`/background_scale (0.120), `meeting-ops-normalizer`/background_scale (0.118), `meeting-ops-artifact-packager`/background_scale (0.118)

### `office_business_automation_p5_meeting_notes_action_extractor`

- Gold: `meeting-notes-action-extractor`; rank 1; score 0.182
- Best non-core: `calendar-conflict-checker`; rank 2; score 0.120
- Top neighbours: `meeting-notes-action-extractor`/office_business_automation (0.182), `calendar-conflict-checker`/background_scale (0.120), `compliance-ops-summary-writer`/background_scale (0.083), `docs-ops-summary-writer`/background_scale (0.082), `partnerships-ops-summary-writer`/background_scale (0.081)

### `office_business_automation_p6_email_classification_router`

- Gold: `email-classification-router`; rank 1; score 0.281
- Best non-core: `risk-ops-risk-reviewer`; rank 2; score 0.067
- Top neighbours: `email-classification-router`/office_business_automation (0.281), `risk-ops-risk-reviewer`/background_scale (0.067), `public-office-email-classifier`/public_imported_background (0.062), `risk-ops-priority-ranker`/background_scale (0.055), `public-office-md-slides`/public_imported_background (0.054)

### `pdf_document_operations_p1_pdf_question_answerer`

- Gold: `pdf-question-answerer`; rank 1; score 0.181
- Best non-core: `implicit-pdf-evidence-answerer`; rank 2; score 0.116
- Top neighbours: `pdf-question-answerer`/pdf_document_operations (0.181), `implicit-pdf-evidence-answerer`/implicit_field_stress (0.116), `travel-ops-evidence-grounder`/background_scale (0.087), `travel-ops-compliance-checker`/background_scale (0.079), `travel-ops-failure-diagnoser`/background_scale (0.078)

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Gold: `pdf-layout-table-extractor`; rank 3; score 0.124
- Best non-core: `implicit-pdf-table-reconstructor`; rank 2; score 0.125
- Top neighbours: `pdf-question-answerer`/pdf_document_operations (0.145), `implicit-pdf-table-reconstructor`/implicit_field_stress (0.125), `pdf-layout-table-extractor`/pdf_document_operations (0.124), `public-office-invoice-template`/public_imported_background (0.109), `public-office-chat-with-pdf`/public_imported_background (0.108)

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Gold: `pdf-ocr-cleaner`; rank 2; score 0.130
- Best non-core: `implicit-pdf-evidence-answerer`; rank 4; score 0.088
- Top neighbours: `pdf-ocr-extractor`/office_artifact_workflows (0.134), `pdf-ocr-cleaner`/pdf_document_operations (0.130), `pdf-layout-reviewer`/office_artifact_workflows (0.099), `implicit-pdf-evidence-answerer`/implicit_field_stress (0.088), `implicit-pdf-table-reconstructor`/implicit_field_stress (0.084)

### `pdf_document_operations_p4_pdf_form_filler`

- Gold: `pdf-form-filler`; rank 1; score 0.088
- Best non-core: `public-office-chat-with-pdf`; rank 2; score 0.069
- Top neighbours: `pdf-form-filler`/pdf_document_operations (0.088), `public-office-chat-with-pdf`/public_imported_background (0.069), `public-addy-agent-shipping-and-launch`/public_imported_background (0.052), `public-office-pdf-converter`/public_imported_background (0.037), `public-office-pdf-compress`/public_imported_background (0.036)

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Gold: `pdf-redaction-reviewer`; rank 1; score 0.109
- Best non-core: `vendor-ops-evidence-grounder`; rank 2; score 0.073
- Top neighbours: `pdf-redaction-reviewer`/pdf_document_operations (0.109), `vendor-ops-evidence-grounder`/background_scale (0.073), `pdf-question-answerer`/pdf_document_operations (0.070), `vendor-ops-normalizer`/background_scale (0.062), `vendor-ops-compliance-checker`/background_scale (0.060)

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Gold: `pdf-to-docx-converter`; rank 1; score 0.320
- Best non-core: `public-office-pdf-to-docx`; rank 2; score 0.163
- Top neighbours: `pdf-to-docx-converter`/pdf_document_operations (0.320), `public-office-pdf-to-docx`/public_imported_background (0.163), `public-office-chat-with-pdf`/public_imported_background (0.133), `public-office-pdf-converter`/public_imported_background (0.084), `public-docx`/public_imported_background (0.078)

### `plan_p1_meeting_agenda`

- Gold: `meeting-agenda-builder`; rank 1; score 0.190
- Best non-core: `meeting-ops-scenario-planner`; rank 2; score 0.111
- Top neighbours: `meeting-agenda-builder`/planning_meetings (0.190), `meeting-ops-scenario-planner`/background_scale (0.111), `meeting-ops-normalizer`/background_scale (0.107), `meeting-ops-compliance-checker`/background_scale (0.103), `meeting-ops-dependency-mapper`/background_scale (0.102)

### `plan_p2_meeting_summary`

- Gold: `meeting-summary-writer`; rank 28; score 0.100
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.283
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.283), `meeting-notes-action-extractor`/office_business_automation (0.223), `meeting-ops-evidence-grounder`/background_scale (0.186), `meeting-ops-normalizer`/background_scale (0.184), `meeting-ops-artifact-packager`/background_scale (0.183)

### `plan_p3_meeting_followup`

- Gold: `meeting-followup-extractor`; rank 4; score 0.094
- Best non-core: `public-office-meeting-notes`; rank 1; score 0.171
- Top neighbours: `public-office-meeting-notes`/public_imported_background (0.171), `meeting-notes-action-extractor`/office_business_automation (0.134), `meeting-agenda-builder`/planning_meetings (0.108), `meeting-followup-extractor`/planning_meetings (0.094), `meeting-summary-writer`/planning_meetings (0.088)

### `plan_p4_task_extractor`

- Gold: `task-extractor`; rank 5; score 0.093
- Best non-core: `public-office-meeting-notes`; rank 2; score 0.160
- Top neighbours: `meeting-notes-action-extractor`/office_business_automation (0.171), `public-office-meeting-notes`/public_imported_background (0.160), `meeting-followup-extractor`/planning_meetings (0.150), `meeting-summary-writer`/planning_meetings (0.140), `task-extractor`/planning_meetings (0.093)

### `plan_p5_weekly_planner`

- Gold: `weekly-planner`; rank 181; score 0.019
- Best non-core: `meeting-ops-monitoring-plan-builder`; rank 2; score 0.076
- Top neighbours: `meeting-agenda-builder`/planning_meetings (0.112), `meeting-ops-monitoring-plan-builder`/background_scale (0.076), `meeting-ops-acceptance-test-builder`/background_scale (0.074), `meeting-ops-summary-writer`/background_scale (0.071), `meeting-ops-normalizer`/background_scale (0.066)

### `read_p1_paper_summary`

- Gold: `paper-summariser`; rank 1; score 0.281
- Best non-core: `public-office-academic-search`; rank 3; score 0.103
- Top neighbours: `paper-summariser`/reading_research (0.281), `citation-note-extractor`/reading_research (0.128), `public-office-academic-search`/public_imported_background (0.103), `public-oh-my-research-paper-writing`/public_imported_background (0.091), `method-note-builder`/reading_research (0.086)

### `read_p2_general_source_summary`

- Gold: `general-source-summariser`; rank 2; score 0.102
- Best non-core: `academic-admin-ops-summary-writer`; rank 3; score 0.099
- Top neighbours: `paper-summariser`/reading_research (0.141), `general-source-summariser`/reading_research (0.102), `academic-admin-ops-summary-writer`/background_scale (0.099), `professor-email-reply`/reply_messaging (0.090), `academic-admin-ops-evidence-grounder`/background_scale (0.080)

### `read_p3_citation_notes`

- Gold: `citation-note-extractor`; rank 1; score 0.235
- Best non-core: `writing-ops-evidence-grounder`; rank 2; score 0.099
- Top neighbours: `citation-note-extractor`/reading_research (0.235), `writing-ops-evidence-grounder`/background_scale (0.099), `writing-ops-field-extractor`/background_scale (0.083), `writing-ops-artifact-packager`/background_scale (0.082), `writing-ops-normalizer`/background_scale (0.075)

### `read_p4_document_extraction`

- Gold: `document-extractor`; rank 123; score 0.043
- Best non-core: `public-office-table-extractor`; rank 1; score 0.088
- Top neighbours: `public-office-table-extractor`/public_imported_background (0.088), `research-ops-field-extractor`/background_scale (0.075), `compliance-ops-field-extractor`/background_scale (0.065), `docs-ops-field-extractor`/background_scale (0.065), `pdf-form-filler`/pdf_document_operations (0.064)

### `read_p5_method_notes`

- Gold: `method-note-builder`; rank 184; score 0.019
- Best non-core: `research-ops-scenario-planner`; rank 1; score 0.063
- Top neighbours: `research-ops-scenario-planner`/background_scale (0.063), `compliance-ops-scenario-planner`/background_scale (0.056), `docs-ops-scenario-planner`/background_scale (0.055), `partnerships-ops-scenario-planner`/background_scale (0.055), `events-ops-scenario-planner`/background_scale (0.054)

### `read_p6_grounding_check`

- Gold: `citation-grounding-helper`; rank 1; score 0.153
- Best non-core: `public-huggingface-train-sentence-transformers`; rank 3; score 0.082
- Top neighbours: `citation-grounding-helper`/reading_research (0.153), `sentence-transformer-finetuner`/huggingface_ml_workflows (0.104), `public-huggingface-train-sentence-transformers`/public_imported_background (0.082), `public-addy-agent-performance-optimization`/public_imported_background (0.057), `document-extractor`/reading_research (0.053)

### `read_p7_multi_source_comparison`

- Gold: `multi-source-comparison-builder`; rank 6; score 0.048
- Best non-core: `note-linker`; rank 5; score 0.071
- Top neighbours: `method-note-builder`/reading_research (0.126), `citation-note-extractor`/reading_research (0.111), `related-work-synthesiser`/reading_research (0.110), `citation-grounding-helper`/reading_research (0.075), `note-linker`/background_scale (0.071)

### `read_p8_related_work_synthesis`

- Gold: `related-work-synthesiser`; rank 1; score 0.215
- Best non-core: `public-openai-notion-research-documentation`; rank 3; score 0.056
- Top neighbours: `related-work-synthesiser`/reading_research (0.215), `release-note-writer`/code_github_workflow (0.060), `public-openai-notion-research-documentation`/public_imported_background (0.056), `public-office-deep-research`/public_imported_background (0.053), `public-office-table-extractor`/public_imported_background (0.050)

### `reply_p1_professor_reply`

- Gold: `professor-email-reply`; rank 1; score 0.122
- Best non-core: `email-polisher`; rank 4; score 0.061
- Top neighbours: `professor-email-reply`/reply_messaging (0.122), `reply-drafter`/reply_messaging (0.117), `reply-polisher`/reply_messaging (0.090), `email-polisher`/email_communication (0.061), `email-drafter`/email_communication (0.057)

### `reply_p2_polish_supervisor`

- Gold: `reply-polisher`; rank 1; score 0.148
- Best non-core: `public-mattpocock-edit-article`; rank 4; score 0.090
- Top neighbours: `reply-polisher`/reply_messaging (0.148), `reply-drafter`/reply_messaging (0.112), `document-rewriter`/documents_files (0.097), `public-mattpocock-edit-article`/public_imported_background (0.090), `email-polisher`/email_communication (0.049)

### `reply_p3_groupwork_coordination`

- Gold: `groupwork-reply`; rank 1; score 0.180
- Best non-core: `deadline-reminder-planner`; rank 4; score 0.061
- Top neighbours: `groupwork-reply`/reply_messaging (0.180), `reply-drafter`/reply_messaging (0.098), `reply-polisher`/reply_messaging (0.063), `deadline-reminder-planner`/background_scale (0.061), `followup-reply-writer`/reply_messaging (0.058)

### `reply_p4_followup_commitment`

- Gold: `followup-reply-writer`; rank 2; score 0.108
- Best non-core: `public-office-investment-memo`; rank 3; score 0.077
- Top neighbours: `document-summariser`/documents_files (0.122), `followup-reply-writer`/reply_messaging (0.108), `public-office-investment-memo`/public_imported_background (0.077), `public-oh-my-state-management`/public_imported_background (0.076), `public-oh-my-write-a-skill`/public_imported_background (0.065)

### `reply_p5_generic_fresh_draft`

- Gold: `reply-drafter`; rank 1; score 0.107
- Best non-core: `implicit-review-comment-planner`; rank 2; score 0.093
- Top neighbours: `reply-drafter`/reply_messaging (0.107), `implicit-review-comment-planner`/implicit_field_stress (0.093), `public-openai-figma-create-new-file`/public_imported_background (0.083), `reply-polisher`/reply_messaging (0.078), `file-renamer`/background_scale (0.051)

### `sec_p1_threat_model`

- Gold: `security-threat-modeler`; rank 2; score 0.093
- Best non-core: `public-openai-figma-create-new-file`; rank 1; score 0.096
- Top neighbours: `public-openai-figma-create-new-file`/public_imported_background (0.096), `security-threat-modeler`/security_appsec (0.093), `email-ops-risk-reviewer`/background_scale (0.066), `email-ops-scenario-planner`/background_scale (0.058), `public-security-threat-model`/public_imported_background (0.057)

### `sec_p2_security_code_review`

- Gold: `security-code-reviewer`; rank 1; score 0.097
- Best non-core: `public-addy-agent-security-and-hardening`; rank 2; score 0.061
- Top neighbours: `security-code-reviewer`/security_appsec (0.097), `public-addy-agent-security-and-hardening`/public_imported_background (0.061), `public-swebench-slo-implementation`/public_imported_background (0.055), `pr-reviewer`/code_github_workflow (0.049), `api-ops-acceptance-test-builder`/background_scale (0.048)

### `sec_p3_dependency_risk`

- Gold: `dependency-risk-auditor`; rank 21; score 0.123
- Best non-core: `supply-chain-ops-risk-reviewer`; rank 1; score 0.177
- Top neighbours: `supply-chain-ops-risk-reviewer`/background_scale (0.177), `supply-chain-ops-dependency-mapper`/background_scale (0.153), `supply-chain-ops-priority-ranker`/background_scale (0.146), `supply-chain-ops-artifact-packager`/background_scale (0.141), `supply-chain-ops-normalizer`/background_scale (0.140)

### `sec_p4_secret_leak`

- Gold: `secret-leak-scanner`; rank 1; score 0.088
- Best non-core: `public-oh-my-log-analysis`; rank 2; score 0.050
- Top neighbours: `secret-leak-scanner`/security_appsec (0.088), `public-oh-my-log-analysis`/public_imported_background (0.050), `public-huggingface-huggingface-papers`/public_imported_background (0.050), `deployment-release-verifier`/deployment_browser_qa (0.050), `public-office-webhook-automation`/public_imported_background (0.047)

### `sec_p5_auth_flow`

- Gold: `auth-flow-reviewer`; rank 1; score 0.157
- Best non-core: `public-oh-my-google-workspace`; rank 2; score 0.050
- Top neighbours: `auth-flow-reviewer`/security_appsec (0.157), `public-oh-my-google-workspace`/public_imported_background (0.050), `email-ops-monitoring-plan-builder`/background_scale (0.049), `auth-flow-integrator`/api_mcp_tooling (0.043), `email-ops-normalizer`/background_scale (0.043)

### `sec_p6_privacy_review`

- Gold: `privacy-risk-reviewer`; rank 112; score 0.026
- Best non-core: `public-office-web-search`; rank 1; score 0.072
- Top neighbours: `public-office-web-search`/public_imported_background (0.072), `public-swebench-similarity-search-patterns`/public_imported_background (0.052), `query-optimizer`/background_scale (0.050), `public-oh-my-log-analysis`/public_imported_background (0.048), `public-swebench-dbt-transformation-patterns`/public_imported_background (0.047)

### `skill_p1_find_existing`

- Gold: `skill-finder`; rank 46; score 0.039
- Best non-core: `public-office-meeting-notes`; rank 2; score 0.097
- Top neighbours: `meeting-notes-action-extractor`/office_business_automation (0.179), `public-office-meeting-notes`/public_imported_background (0.097), `library-ops-evidence-grounder`/background_scale (0.064), `meeting-ops-evidence-grounder`/background_scale (0.060), `library-ops-timeline-builder`/background_scale (0.056)

### `skill_p2_install_existing`

- Gold: `skill-installer`; rank 1; score 0.132
- Best non-core: `implicit-hf-local-model-chooser`; rank 3; score 0.060
- Top neighbours: `skill-installer`/skill_lifecycle (0.132), `hf-local-model-selector`/huggingface_ml_workflows (0.060), `implicit-hf-local-model-chooser`/implicit_field_stress (0.060), `library-ops-resource-linker`/background_scale (0.055), `library-ops-acceptance-test-builder`/background_scale (0.053)

### `skill_p3_create_new`

- Gold: `skill-creator`; rank 1; score 0.229
- Best non-core: `public-anthropic-skill-creator`; rank 3; score 0.154
- Top neighbours: `skill-creator`/skill_lifecycle (0.229), `meeting-notes-action-extractor`/office_business_automation (0.165), `public-anthropic-skill-creator`/public_imported_background (0.154), `meeting-followup-extractor`/planning_meetings (0.146), `public-skill-creator`/public_imported_background (0.139)

### `skill_p4_edit_existing`

- Gold: `skill-editor`; rank 2; score 0.153
- Best non-core: `public-anthropic-skill-creator`; rank 1; score 0.175
- Top neighbours: `public-anthropic-skill-creator`/public_imported_background (0.175), `skill-editor`/skill_lifecycle (0.153), `skill-evaluator`/skill_lifecycle (0.105), `skill-installer`/skill_lifecycle (0.100), `public-skill-creator`/public_imported_background (0.100)

### `skill_p5_evaluate_existing`

- Gold: `skill-evaluator`; rank 3; score 0.133
- Best non-core: `public-anthropic-skill-creator`; rank 7; score 0.075
- Top neighbours: `reply-polisher`/reply_messaging (0.158), `reply-drafter`/reply_messaging (0.143), `skill-evaluator`/skill_lifecycle (0.133), `followup-reply-writer`/reply_messaging (0.084), `professor-email-reply`/reply_messaging (0.079)

### `skill_p6_package_existing`

- Gold: `skill-packager`; rank 1; score 0.139
- Best non-core: `public-anthropic-skill-creator`; rank 3; score 0.076
- Top neighbours: `skill-packager`/skill_lifecycle (0.139), `paper-summariser`/reading_research (0.132), `public-anthropic-skill-creator`/public_imported_background (0.076), `skill-installer`/skill_lifecycle (0.070), `agent-ops-resource-linker`/background_scale (0.066)

### `skill_representation_analysis_p1_skill_field_auditor`

- Gold: `skill-field-auditor`; rank 1; score 0.364
- Best non-core: `agent-handoff-orchestrator`; rank 3; score 0.084
- Top neighbours: `skill-field-auditor`/skill_representation_analysis (0.364), `gradio-demo-builder`/huggingface_ml_workflows (0.097), `agent-handoff-orchestrator`/background_scale (0.084), `xlsx-formula-model-builder`/office_business_automation (0.080), `public-addy-web-web-quality-audit`/public_imported_background (0.072)

### `skill_representation_analysis_p2_skill_authoring_guide`

- Gold: `skill-authoring-guide`; rank 15; score 0.069
- Best non-core: `public-anthropic-skill-creator`; rank 4; score 0.136
- Top neighbours: `skill-creator`/skill_lifecycle (0.211), `skill-editor`/skill_lifecycle (0.179), `skill-field-auditor`/skill_representation_analysis (0.160), `public-anthropic-skill-creator`/public_imported_background (0.136), `skill-finder`/skill_lifecycle (0.122)

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Gold: `skill-router-policy-designer`; rank 1; score 0.239
- Best non-core: `public-anthropic-skill-creator`; rank 5; score 0.092
- Top neighbours: `skill-router-policy-designer`/skill_representation_analysis (0.239), `skill-field-auditor`/skill_representation_analysis (0.125), `skill-installer`/skill_lifecycle (0.116), `skill-finder`/skill_lifecycle (0.116), `public-anthropic-skill-creator`/public_imported_background (0.092)

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Gold: `skill-hierarchy-flattener`; rank 1; score 0.194
- Best non-core: `public-anthropic-skill-creator`; rank 4; score 0.090
- Top neighbours: `skill-hierarchy-flattener`/skill_representation_analysis (0.194), `skill-creator`/skill_lifecycle (0.126), `skill-editor`/skill_lifecycle (0.095), `public-anthropic-skill-creator`/public_imported_background (0.090), `public-oh-my-write-a-skill`/public_imported_background (0.090)

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Gold: `skill-installer-wrapper`; rank 1; score 0.206
- Best non-core: `public-skill-installer`; rank 2; score 0.165
- Top neighbours: `skill-installer-wrapper`/skill_representation_analysis (0.206), `public-skill-installer`/public_imported_background (0.165), `library-ops-field-extractor`/background_scale (0.120), `skill-installer`/skill_lifecycle (0.103), `library-ops-dependency-mapper`/background_scale (0.102)

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Gold: `skill-benchmark-evaluator`; rank 1; score 0.198
- Best non-core: `public-swebench-implementing-agent-modes`; rank 2; score 0.059
- Top neighbours: `skill-benchmark-evaluator`/skill_representation_analysis (0.198), `public-swebench-implementing-agent-modes`/public_imported_background (0.059), `public-addy-web-core-web-vitals`/public_imported_background (0.054), `public-openai-aspnet-core`/public_imported_background (0.052), `budget-planner`/background_scale (0.038)
