# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2401 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 53.5% |
| Acceptable top-1 accuracy | 54.3% |
| Top-3 recall | 69.3% |
| Top-5 recall | 72.4% |
| Acceptable top-5 recall | 74.0% |
| MRR | 0.616 |
| Non-main top-1 | 27.6% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 48
- Embedding cache hits: 2434
- Approx uncached embedding input tokens: 13165
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, rest-api-contract-designer, openapi-contract-tester, api-ops-quality-auditor |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, auth-flow-integrator, api-integration-planner, api-ops-artifact-packager, api-ops-handoff-brief-writer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, webhook-setup-planner, receipt-extractor, events-ops-monitoring-plan-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, mcp-server-builder, webhook-integration-planner |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, mobile-ops-monitoring-plan-builder, public-office-subscription-management, webhook-integration-planner, webhook-contract-planner |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 5 | 5 | `finance-ops-monitoring-plan-builder` | wrong | finance-ops-monitoring-plan-builder, customer-success-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, implicit-trace-path-diagnoser, service-dependency-mapper |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 3 | 3 | `public-office-subscription-management` | wrong | public-office-subscription-management, invoice-payment-checker, rest-api-contract-designer, public-office-invoice-organizer, public-office-invoice-automation |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, public-office-office-mcp, api-documentation-writer, api-security-threat-reviewer |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, webhook-setup-planner, external-api-integration-planner, ecommerce-ops-monitoring-plan-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, webhook-integration-planner, webhook-contract-planner, public-swebench-add-admin-api-endpoint, auth-flow-reviewer |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 2 | 2 | `external-api-integration-planner` | wrong | external-api-integration-planner, api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, public-office-stripe-payments |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, invoice-payment-checker, api-ops-risk-reviewer, api-ops-compliance-checker, api-ops-quality-auditor |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, implicit-browser-flow-investigator, frontend-debugger, implicit-visual-diff-reviewer |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, implicit-browser-flow-investigator, web-ops-handoff-brief-writer, web-ops-artifact-packager |
| `web_p3_ui_test` | `web-ui-tester` | 12 | 12 | `ecommerce-ops-compliance-checker` | wrong | ecommerce-ops-compliance-checker, logistics-ops-compliance-checker, ecommerce-ops-acceptance-test-builder, invoice-payment-checker, logistics-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 2 | 2 | `ecommerce-ops-comparison-builder` | wrong | ecommerce-ops-comparison-builder, web-data-extractor, ecommerce-ops-artifact-packager, ecommerce-ops-normalizer, ecommerce-ops-summary-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-normalizer` | wrong | personal-ops-normalizer, public-swebench-add-admin-api-endpoint, personal-ops-rewrite-editor, personal-ops-handoff-brief-writer, personal-ops-artifact-packager |
| `web_p6_accessibility_check` | `accessibility-checker` | 3 | 3 | `web-form-filler` | wrong | web-form-filler, accessibility-interaction-auditor, accessibility-checker, email-drafter, fundraising-ops-normalizer |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-ops-normalizer, personal-ops-normalizer, email-ops-dependency-mapper, reply-polisher |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-integrator` | wrong | auth-flow-integrator, auth-flow-reviewer, external-api-integration-planner, public-swebench-add-admin-api-endpoint, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `resilience-pattern-reviewer` | wrong | resilience-pattern-reviewer, external-api-integration-planner, api-ops-monitoring-plan-builder, api-ops-quality-auditor, api-ops-rewrite-editor |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-integrator` | wrong | auth-flow-integrator, auth-flow-reviewer, external-api-integration-planner, openapi-contract-reviewer, public-swebench-add-admin-api-endpoint |
| `code_p5_changelog_entry` | `changelog-writer` | 10 | 10 | `auth-flow-integrator` | wrong | auth-flow-integrator, auth-flow-reviewer, external-api-integration-planner, churn-risk-analyser, webhook-integration-planner |
| `code_p6_release_notes` | `release-note-writer` | - | - | `auth-flow-integrator` | wrong | auth-flow-integrator, mobile-ops-rewrite-editor, mobile-ops-timeline-builder, mobile-ops-quality-auditor, mobile-ops-monitoring-plan-builder |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, data-analysis-for-reporting, data-analysis-with-anomaly-focus |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 4 | 4 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-with-validation, ads-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, data-analysis-overview, ads-ops-failure-diagnoser, marketing-ops-failure-diagnoser, marketing-ops-monitoring-plan-builder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-reporting, marketing-ops-summary-writer, ads-ops-summary-writer, data-analysis-for-root-cause-diagnosis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, product-ops-priority-ranker, facilities-ops-priority-ranker, analytics-ops-priority-ranker, priority-sorter |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 19 | 19 | `receipt-extractor` | wrong | receipt-extractor, implicit-browser-flow-investigator, ecommerce-ops-acceptance-test-builder, frontend-debugger, web-form-filler |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 4 | 4 | `vendor-ops-summary-writer` | wrong | vendor-ops-summary-writer, proposal-drafter, competitive-battlecard-builder, visual-regression-checker, vendor-ops-scenario-planner |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, ads-ops-normalizer, customer-success-ops-normalizer, ads-ops-quality-auditor, accessibility-checker |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, public-oh-my-game-build-log-triage, public-oh-my-vercel-deploy, deployment-release-verifier |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, deployment-build-triager, release-note-writer, public-oh-my-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-priority-ranker, mobile-ops-summary-writer, mobile-ops-resource-linker, mobile-ops-comparison-builder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-handoff-brief-writer, travel-ops-monitoring-plan-builder, travel-ops-rewrite-editor, travel-ops-normalizer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-normalizer, travel-ops-summary-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-handoff-brief-writer, travel-ops-rewrite-editor, travel-ops-compliance-checker, travel-ops-risk-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, supply-chain-ops-normalizer, procurement-ops-normalizer, supply-chain-ops-field-extractor, supply-chain-ops-evidence-grounder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 3 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-rewrite-editor, legal-ops-comparison-builder, academic-admin-ops-rewrite-editor, legal-ops-artifact-packager |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, research-ops-risk-reviewer, research-ops-artifact-packager, research-ops-intake-classifier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, procurement-ops-field-extractor, email-drafter, pdf-form-filler, web-form-filler |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, implicit-ci-failure-reader, ci-failure-debugger, deployment-build-triager, review-comment-resolver |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, pr-reviewer, release-note-writer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, implicit-review-comment-planner, review-comment-resolver, implicit-visual-diff-reviewer |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, support-ticket-triager, public-lbussell-triaging-issues, support-ops-dependency-mapper, support-ops-handoff-brief-writer |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, release-changelog-generator, changelog-writer, pr-review-comment-resolver, pr-reviewer |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, public-mattpocock-git-guardrails-claude-code, repo-code-reviewer, version-control-helper, security-code-reviewer |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | - | - | `support-ops-normalizer` | wrong | support-ops-normalizer, support-ops-field-extractor, support-ops-summary-writer, support-ticket-triager, support-ops-quality-auditor |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, implicit-hf-local-model-chooser, support-ops-intake-classifier, support-ticket-triager, support-ops-ops-intake-classifier |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | - | - | `skill-router-policy-designer` | wrong | skill-router-policy-designer, agent-ops-normalizer, agent-ops-rewrite-editor, agent-ops-intake-classifier, agent-ops-handoff-brief-writer |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | - | - | `support-ticket-triager` | wrong | support-ticket-triager, support-ops-intake-classifier, web-ops-intake-classifier, ml-ops-intake-classifier, dashboard-ops-intake-classifier |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, gradio-demo-builder, implicit-hf-local-model-chooser, hf-local-model-selector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 3 | 3 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, implicit-hf-dataset-inspector, hf-community-eval-runner, support-ticket-triager, dataset-ops-intake-classifier |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, metrics-root-cause-diagnoser, slo-breach-checker, capacity-risk-forecaster |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, metrics-root-cause-diagnoser, capacity-risk-forecaster, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview, sre-ops-failure-diagnoser |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, implicit-trace-path-diagnoser, metrics-overview, capacity-risk-forecaster, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, slo-breach-narrative-writer, incident-ops-dependency-mapper |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, general-source-summariser, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `events-ops-monitoring-plan-builder` | wrong | events-ops-monitoring-plan-builder, news-briefing-writer, events-ops-handoff-brief-writer, incident-summary-writer, events-ops-risk-reviewer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, tech-news-trend-extractor, product-ops-evidence-grounder, document-extractor, citation-grounding-helper |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, mobile-ops-evidence-grounder, news-summariser |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 3 | 3 | `slo-breach-checker` | wrong | slo-breach-checker, latency-anomaly-detector, prometheus-alert-rule-writer, implicit-slo-alert-author, web-performance-budget-checker |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 3 | 3 | `metrics-overview` | wrong | metrics-overview, slo-breach-checker, grafana-dashboard-builder, ecommerce-ops-monitoring-plan-builder, resilience-pattern-reviewer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 6 | 6 | `implicit-trace-path-diagnoser` | wrong | implicit-trace-path-diagnoser, resilience-pattern-reviewer, latency-anomaly-detector, ecommerce-ops-monitoring-plan-builder, ecommerce-ops-failure-diagnoser |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, incident-summary-writer, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-quality-auditor |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, external-api-integration-planner, public-swebench-python-resilience, invoice-payment-checker, procurement-ops-failure-diagnoser |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, resilience-pattern-reviewer, public-swebench-istio-traffic-management, cloud-monitoring-configurer, prometheus-alert-rule-writer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-normalizer` | wrong | grant-ops-normalizer, grant-ops-field-extractor, grant-ops-summary-writer, grant-ops-artifact-packager, grant-ops-quality-auditor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 4 | 4 | `receipt-extractor` | wrong | receipt-extractor, pdf-ocr-cleaner, implicit-pdf-table-reconstructor, pdf-ocr-extractor, pdf-layout-table-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-handoff-brief-writer, vendor-ops-summary-writer, vendor-ops-risk-reviewer, vendor-ops-artifact-packager |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 2 | 2 | `xlsx-formula-model-builder` | wrong | xlsx-formula-model-builder, spreadsheet-formula-auditor, financial-model-builder, finance-ops-scenario-planner, finance-ops-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, deck-template-applier, slide-outline-builder, public-office-ppt-visual, public-office-pptx-manipulation |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `construction-ops-handoff-brief-writer` | wrong | construction-ops-handoff-brief-writer, product-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, engineering-design-ops-handoff-brief-writer, product-ops-dependency-mapper |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, data-analysis-with-validation, public-office-subscription-management, customer-success-ops-scenario-planner |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 17 | 17 | `partnerships-ops-monitoring-plan-builder` | wrong | partnerships-ops-monitoring-plan-builder, partnerships-ops-intake-classifier, partnerships-ops-normalizer, partnerships-ops-handoff-brief-writer, partnerships-ops-field-extractor |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, thesis-ops-handoff-brief-writer, thesis-ops-normalizer, thesis-ops-dependency-mapper, thesis-ops-field-extractor |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-scheduler, calendar-conflict-checker, meeting-ops-timeline-builder, meeting-agenda-builder |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, meeting-ops-handoff-brief-writer, meeting-agenda-builder |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, email-ops-risk-reviewer, email-ops-intake-classifier, email-ops-priority-ranker, email-ops-monitoring-plan-builder |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | - | - | `travel-ops-evidence-grounder` | wrong | travel-ops-evidence-grounder, travel-ops-compliance-checker, travel-ops-summary-writer, travel-ops-resource-linker, travel-ops-rewrite-editor |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 3 | 3 | `invoice-payment-checker` | wrong | invoice-payment-checker, implicit-pdf-table-reconstructor, pdf-layout-table-extractor, vendor-ops-field-extractor, vendor-ops-summary-writer |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, implicit-pdf-table-reconstructor, pdf-layout-table-extractor, receipt-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, email-drafter, receipt-extractor, travel-ops-field-extractor, hr-ops-handoff-brief-writer |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, contract-ops-artifact-packager, contract-ops-summary-writer, vendor-ops-rewrite-editor, vendor-ops-summary-writer |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | - | - | `training-ops-rewrite-editor` | wrong | training-ops-rewrite-editor, training-ops-normalizer, training-ops-field-extractor, training-ops-summary-writer, training-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 3 | 3 | `meeting-ops-risk-reviewer` | wrong | meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-agenda-builder, meeting-ops-artifact-packager, meeting-ops-dependency-mapper |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-agenda-builder, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, meeting-notes-action-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-notes-action-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, thesis-ops-timeline-builder, meeting-ops-timeline-builder, ux-ops-timeline-builder, meeting-scheduler |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `research-ops-summary-writer` | wrong | research-ops-summary-writer, general-source-summariser, research-ops-scenario-planner, research-ops-comparison-builder, research-ops-priority-ranker |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, citation-grounding-helper, document-extractor, multi-source-comparison-builder |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, research-ops-field-extractor, web-data-extractor, incident-ops-field-extractor, journalism-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 2 | 2 | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, method-note-builder, research-ops-priority-ranker, research-ops-summary-writer, research-ops-handoff-brief-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-rewrite-editor, agent-ops-evidence-grounder, research-ops-rewrite-editor, research-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, related-work-synthesiser, citation-grounding-helper, thesis-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, groupwork-reply, reply-polisher, thesis-ops-handoff-brief-writer, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, groupwork-reply, email-polisher, email-ops-handoff-brief-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-followup-extractor, meeting-summary-writer, construction-ops-handoff-brief-writer, followup-reply-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, email-drafter, professor-email-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, api-security-threat-reviewer, auth-flow-reviewer, public-office-suspicious-email |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, auth-flow-integrator, public-swebench-add-admin-api-endpoint, external-api-integration-planner, webhook-contract-planner |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, public-oh-my-npm-git-install, migration-risk-auditor, public-openai-transcribe, risk-ops-artifact-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 10 | 10 | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-setup-planner, webhook-integration-planner, public-oh-my-deployment-automation, deployment-build-triager |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-quality-auditor, auth-flow-integrator, identity-ops-compliance-checker, identity-ops-comparison-builder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-handoff-brief-writer, analytics-ops-summary-writer, analytics-ops-quality-auditor, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, library-ops-dependency-mapper, library-ops-summary-writer, meeting-ops-dependency-mapper, skill-creator |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-office-data-analysis, public-office-xlsx-manipulation, public-swebench-xlsx, data-analysis-with-validation |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-artifact-packager, personal-ops-handoff-brief-writer, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, docs-ops-field-extractor, operations-ops-field-extractor, document-extractor, knowledge-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, email-polisher, followup-reply-writer, email-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, public-huggingface-huggingface-papers, docs-ops-summary-writer, paper-summariser, public-huggingface-huggingface-paper-publisher |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, public-office-quickbooks-automation, public-oh-my-workflow-automation, public-oh-my-authentication-setup, public-office-airtable-automation |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | - | - | `migration-risk-auditor` | wrong | migration-risk-auditor, database-migration-risk-assessor, database-ops-monitoring-plan-builder, database-ops-risk-reviewer, database-ops-quality-auditor |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, recruiting-ops-intake-classifier, agent-ops-priority-ranker, skill-hierarchy-flattener, skill-benchmark-evaluator |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-authoring-guide, skill-creator, skill-finder, agent-ops-handoff-brief-writer |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-packager, skill-installer, public-skill-installer, public-oh-my-npm-git-install |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, search-ops-evidence-grounder, search-ops-normalizer, search-ops-summary-writer, search-ops-failure-diagnoser |
