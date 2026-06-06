# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2401 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 82.7% |
| Acceptable top-1 accuracy | 82.7% |
| Top-3 recall | 90.5% |
| Top-5 recall | 90.5% |
| Acceptable top-5 recall | 90.5% |
| MRR | 0.867 |
| Non-main top-1 | 7.1% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2528
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, external-api-integration-planner, api-documentation-writer, openapi-contract-tester |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, auth-flow-integrator, api-ops-acceptance-test-builder, rest-api-contract-designer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, events-ops-timeline-builder, webhook-setup-planner, ecommerce-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, refactor-planner, mcp-server-builder |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, mobile-ops-monitoring-plan-builder, webhook-integration-planner, public-office-subscription-management |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, distributed-trace-investigator, finance-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, implicit-trace-path-diagnoser |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, public-office-subscription-management, invoice-payment-checker, openapi-contract-reviewer, api-documentation-writer |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, api-design-reviewer, public-office-office-mcp, engineering-design-ops-resource-linker |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 2 | 2 | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-integration-planner, webhook-setup-planner, events-ops-monitoring-plan-builder, ecommerce-ops-timeline-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, grafana-dashboard-builder, webhook-contract-planner, auth-flow-reviewer, webhook-setup-planner |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, external-api-integration-planner, rest-api-contract-designer, openapi-contract-reviewer, openapi-contract-tester |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, api-ops-risk-reviewer, security-threat-modeler, privacy-risk-reviewer, api-ops-quality-auditor |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, accessibility-interaction-auditor, implicit-browser-flow-investigator |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, pdf-form-filler, web-ops-field-extractor, web-ui-tester, qa-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, ecommerce-ops-acceptance-test-builder, logistics-ops-acceptance-test-builder, partnerships-ops-acceptance-test-builder, travel-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, ecommerce-ops-field-extractor, product-ops-comparison-builder, ecommerce-ops-comparison-builder, ecommerce-ops-summary-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-handoff-brief-writer` | wrong | api-ops-handoff-brief-writer, public-swebench-add-admin-api-endpoint, api-ops-rewrite-editor, api-integration-planner, external-api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, pdf-form-filler, email-drafter |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, git-commit-writer, professor-email-reply, churn-risk-analyser |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `auth-flow-integrator` | wrong | auth-flow-integrator, pr-reviewer, external-api-integration-planner, pr-review-comment-resolver, database-migration-risk-assessor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, resilience-pattern-reviewer, external-api-integration-planner, pr-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 3 | 3 | `auth-flow-integrator` | wrong | auth-flow-integrator, ci-log-root-cause-debugger, ci-failure-debugger, auth-flow-reviewer, web-ui-tester |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, auth-flow-integrator, auth-flow-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, auth-flow-integrator, mobile-ops-timeline-builder, mobile-ops-evidence-grounder, mobile-ops-rewrite-editor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting, dataset-ops-summary-writer, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, dataset-ops-quality-auditor, support-ops-quality-auditor, ads-ops-quality-auditor, marketing-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, variance-analysis-helper, ads-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, marketing-ops-summary-writer, ads-ops-summary-writer, content-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, metrics-root-cause-diagnoser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, travel-ops-priority-ranker, dashboard-ops-priority-ranker, risk-ops-priority-ranker, risk-ops-scenario-planner |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, web-ui-tester, implicit-browser-flow-investigator |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, implicit-visual-diff-reviewer, slide-deck-visual-auditor, proposal-drafter, vendor-ops-summary-writer |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, web-form-filler, ads-ops-normalizer, ads-ops-quality-auditor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, ci-log-root-cause-debugger, public-netlify-deploy, ci-failure-debugger, secret-leak-scanner |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-note-writer, release-changelog-generator, deployment-build-triager |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-evidence-grounder, mobile-ops-summary-writer, mobile-ops-priority-ranker, mobile-ops-acceptance-test-builder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, facilities-ops-summary-writer, logistics-ops-summary-writer, events-ops-summary-writer, meeting-ops-summary-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, travel-ops-rewrite-editor, travel-ops-normalizer, facilities-ops-rewrite-editor, travel-ops-handoff-brief-writer |
| `doc_p4_field_extraction` | `document-field-extractor` | 17 | 17 | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, procurement-ops-field-extractor, vendor-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, insurance-ops-comparison-builder, academic-admin-ops-comparison-builder, privacy-policy-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, research-ops-risk-reviewer, pdf-form-filler, citation-note-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, procurement-ops-field-extractor, operations-ops-field-extractor, academic-admin-ops-field-extractor, ux-ops-field-extractor |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, ci-failure-debugger, implicit-ci-failure-reader, deployment-build-triager, frontend-debugger |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, implicit-review-comment-planner, code-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | - | - | `review-comment-resolver` | wrong | review-comment-resolver, pr-review-comment-resolver, implicit-review-comment-planner, invoice-payment-checker, finance-ops-acceptance-test-builder |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, support-ticket-triager, support-ops-handoff-brief-writer, public-mattpocock-triage, support-ops-quality-auditor |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, release-note-writer, review-comment-resolver, changelog-writer, pr-review-comment-resolver |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, public-mattpocock-git-guardrails-claude-code, secret-leak-scanner, git-commit-writer, github-issue-triager |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, support-ops-normalizer, support-ops-field-extractor, support-ops-quality-auditor |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, implicit-hf-local-model-chooser, support-ticket-triager, public-huggingface-huggingface-local-models, support-ops-evidence-grounder |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, agent-ops-intake-classifier, skill-router-policy-designer, agent-ops-normalizer, skill-hierarchy-flattener |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, support-ticket-triager, web-ops-intake-classifier, support-ops-intake-classifier, ml-ops-intake-classifier |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, gradio-demo-builder, implicit-hf-local-model-chooser, hf-local-model-selector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, sentence-transformer-finetuner, hf-dataset-viewer-inspector, dataset-ops-comparison-builder, support-ops-comparison-builder |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger, slo-breach-checker, public-mattpocock-triage |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, service-dependency-mapper, risk-ops-risk-reviewer, platform-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, sre-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, journalism-ops-summary-writer, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, metrics-overview, events-ops-scenario-planner |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, knowledge-base-article-writer, product-ops-evidence-grounder, document-extractor, retail-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, metrics-root-cause-diagnoser |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, slo-breach-checker, implicit-slo-alert-author, latency-anomaly-detector, dashboard-ops-acceptance-test-builder |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, slo-breach-checker, ecommerce-ops-monitoring-plan-builder, dashboard-ops-monitoring-plan-builder |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 2 | 2 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, distributed-trace-investigator, metrics-overview, service-dependency-mapper, implicit-trace-path-diagnoser |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, incident-summary-writer, slo-breach-checker, incident-ops-timeline-builder, incident-ops-risk-reviewer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, customer-success-ops-risk-reviewer, procurement-ops-risk-reviewer, ecommerce-ops-risk-reviewer, retail-ops-risk-reviewer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, prometheus-alert-rule-writer, resilience-pattern-reviewer, public-swebench-istio-traffic-management, cloud-monitoring-configurer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, grant-ops-field-extractor, pdf-layout-table-extractor, pdf-form-filler, grant-ops-quality-auditor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-table-extractor, receipt-extractor, implicit-pdf-table-reconstructor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, vendor-ops-rewrite-editor, vendor-ops-handoff-brief-writer, vendor-ops-artifact-packager, vendor-ops-risk-reviewer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, xlsx-formula-model-builder, data-analysis-with-validation, procurement-risk-summariser, finance-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, slide-outline-builder, deck-template-applier, public-office-ppt-visual, thesis-ops-rewrite-editor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `repo-ops-handoff-brief-writer` | wrong | repo-ops-handoff-brief-writer, construction-ops-comparison-builder, construction-ops-summary-writer, construction-ops-normalizer, construction-ops-handoff-brief-writer |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, data-analysis-with-validation, public-office-subscription-management, financial-model-builder |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, partnerships-ops-field-extractor, partnerships-ops-monitoring-plan-builder, partnerships-ops-intake-classifier, partnerships-ops-normalizer |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, thesis-ops-handoff-brief-writer, thesis-ops-monitoring-plan-builder, thesis-ops-normalizer, thesis-ops-dependency-mapper |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-scheduler, meeting-ops-comparison-builder, meeting-agenda-builder, calendar-conflict-checker |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, meeting-ops-handoff-brief-writer, meeting-ops-summary-writer, meeting-ops-timeline-builder |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, email-ops-risk-reviewer, email-ops-intake-classifier, risk-ops-intake-classifier, email-ops-monitoring-plan-builder |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | - | - | `travel-ops-evidence-grounder` | wrong | travel-ops-evidence-grounder, travel-ops-compliance-checker, insurance-ops-evidence-grounder, travel-ops-risk-reviewer, travel-ops-summary-writer |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 1 | 1 | `pdf-layout-table-extractor` | gold | pdf-layout-table-extractor, invoice-payment-checker, pdf-question-answerer, implicit-pdf-table-reconstructor, vendor-ops-field-extractor |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 2 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-table-extractor, pdf-layout-reviewer, implicit-pdf-table-reconstructor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, travel-ops-summary-writer, events-ops-summary-writer, compliance-ops-summary-writer, grant-ops-summary-writer |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, vendor-ops-normalizer, vendor-ops-summary-writer, vendor-ops-risk-reviewer, vendor-ops-rewrite-editor |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, training-ops-rewrite-editor, training-ops-field-extractor, training-ops-normalizer, layout-preserving-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-followup-extractor, meeting-summary-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-notes-action-extractor, meeting-followup-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-notes-action-extractor, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-notes-action-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-field-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-scheduler, meeting-agenda-builder, meeting-ops-acceptance-test-builder, meeting-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, data-analysis-for-reporting, construction-ops-summary-writer, energy-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, speaker-notes-writer, note-linker, method-note-builder, note-tagger |
| `read_p4_document_extraction` | `document-extractor` | 11 | 11 | `web-data-extractor` | wrong | web-data-extractor, research-ops-field-extractor, incident-ops-field-extractor, lab-ops-field-extractor, journalism-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, research-ops-acceptance-test-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-ops-rewrite-editor, support-ops-evidence-grounder, support-ops-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder, related-work-synthesiser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ux-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply, reply-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, document-rewriter, reply-drafter, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, meeting-followup-extractor, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, groupwork-reply, reply-polisher, meeting-followup-extractor |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, api-security-threat-reviewer, privacy-risk-reviewer, email-ops-risk-reviewer, public-office-suspicious-email |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-integrator, api-security-threat-reviewer, auth-flow-reviewer, external-api-integration-planner |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, migration-risk-auditor, risk-ops-artifact-packager, database-migration-risk-assessor |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, webhook-contract-planner, webhook-integration-planner, environment-config-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, identity-ops-evidence-grounder, identity-ops-acceptance-test-builder, identity-ops-monitoring-plan-builder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-overview, analytics-ops-resource-linker, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, meeting-followup-extractor, library-ops-comparison-builder, library-ops-dependency-mapper |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, public-office-data-analysis, data-analysis-for-reporting, public-office-sheets-automation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, meeting-notes-action-extractor, meeting-ops-handoff-brief-writer, thesis-ops-timeline-builder |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, skill-field-auditor, document-field-extractor, agent-ops-field-extractor, operations-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, skill-evaluator, reply-drafter, followup-reply-writer, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, public-huggingface-huggingface-papers, agent-ops-summary-writer, public-huggingface-huggingface-paper-publisher, skill-authoring-guide |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, skill-authoring-guide, skill-creator, skill-evaluator, skill-editor |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 8 | 8 | `skill-creator` | wrong | skill-creator, migration-risk-auditor, skill-editor, database-migration-risk-assessor, skill-hierarchy-flattener |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-hierarchy-flattener, skill-finder, skill-creator, skill-field-auditor |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-authoring-guide, skill-editor, skill-finder |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-editor, skill-packager, public-skill-installer |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, search-ops-evidence-grounder, search-ops-normalizer, search-ops-summary-writer, search-ops-failure-diagnoser |
