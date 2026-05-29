# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2089 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 63.5% |
| Acceptable top-1 accuracy | 68.2% |
| Top-3 recall | 68.2% |
| Top-5 recall | 69.4% |
| Acceptable top-5 recall | 72.9% |
| MRR | 0.668 |
| Non-main top-1 | 32.9% |
| Approx selector-visible tokens | 1856335 |

## API Usage Estimate

- Embedding API calls made in this run: 26
- Embedding cache hits: 2148
- Approx uncached embedding input tokens: 1594
- Rerank API calls made in this run: 71
- Rerank cache hits: 14
- Approx uncached rerank input tokens: 790763

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-ops-quality-auditor, api-ops-acceptance-test-builder, public-api-design-principles |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 1 | `api-integration-planner` | acceptable | api-integration-planner, external-api-integration-planner, api-ops-acceptance-test-builder, api-ops-scenario-planner, api-ops-timeline-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-acceptance-test-builder, invoice-payment-checker, receipt-extractor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, sre-ops-dependency-mapper, platform-ops-dependency-mapper, cloud-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-office-subscription-management, database-ops-monitoring-plan-builder, customer-success-ops-normalizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, customer-success-ops-dependency-mapper, customer-success-ops-quality-auditor, customer-success-ops-failure-diagnoser, customer-success-ops-timeline-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, frontend-debugger, dashboard-ops-quality-auditor, web-ui-tester, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, web-ops-field-extractor, web-ops-quality-auditor, web-ops-normalizer |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, ecommerce-ops-acceptance-test-builder, ecommerce-ops-quality-auditor, logistics-ops-acceptance-test-builder, web-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, ecommerce-ops-field-extractor, ecommerce-ops-normalizer, ecommerce-ops-resource-linker, ecommerce-ops-quality-auditor |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `ux-ops-handoff-brief-writer` | wrong | ux-ops-handoff-brief-writer, customer-success-ops-normalizer, customer-success-ops-rewrite-editor, api-ops-rewrite-editor, partnerships-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-ui-tester, web-form-filler, events-ops-field-extractor |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-ops-normalizer` | wrong | email-ops-normalizer, personal-ops-quality-auditor, email-ops-quality-auditor, personal-ops-acceptance-test-builder, personal-ops-normalizer |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `migration-risk-auditor` | wrong | migration-risk-auditor, api-ops-acceptance-test-builder, api-ops-quality-auditor, api-ops-risk-reviewer, api-ops-compliance-checker |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `api-integration-planner` | wrong | api-integration-planner, api-ops-acceptance-test-builder, api-ops-risk-reviewer, api-ops-scenario-planner, openapi-contract-tester |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `api-ops-failure-diagnoser` | wrong | api-ops-failure-diagnoser, api-ops-acceptance-test-builder, api-ops-quality-auditor, identity-ops-acceptance-test-builder, api-ops-handoff-brief-writer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, api-ops-rewrite-editor, code-reviewer, refactor-planner |
| `code_p6_release_notes` | `release-note-writer` | - | - | `mobile-ops-rewrite-editor` | wrong | mobile-ops-rewrite-editor, mobile-ops-summary-writer, mobile-ops-handoff-brief-writer, mobile-ops-quality-auditor, mobile-ops-artifact-packager |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, dataset-ops-summary-writer, data-analysis-for-reporting, data-analysis-with-validation, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, analytics-ops-monitoring-plan-builder, dataset-ops-monitoring-plan-builder, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 4 | 4 | `dataset-ops-quality-auditor` | wrong | dataset-ops-quality-auditor, analytics-ops-quality-auditor, marketing-ops-quality-auditor, data-analysis-with-validation, support-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, marketing-ops-failure-diagnoser, marketing-ops-quality-auditor, analytics-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, analytics-ops-summary-writer, analytics-ops-handoff-brief-writer, content-ops-summary-writer, marketing-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-overview, market-opportunity-assessor |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `priority-sorter` | wrong | priority-sorter, analytics-ops-priority-ranker, operations-ops-priority-ranker, sales-ops-priority-ranker, events-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-ui-tester, ecommerce-ops-evidence-grounder, web-form-filler |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, product-ops-comparison-builder, ads-ops-comparison-builder, vendor-ops-comparison-builder, mobile-ops-comparison-builder |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, ads-ops-quality-auditor, customer-success-ops-quality-auditor, fundraising-ops-quality-auditor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, ci-failure-debugger, devops-ops-quality-auditor, environment-config-auditor |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, devops-ops-quality-auditor, public-openai-vercel-deploy, public-openai-cloudflare-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-priority-ranker, mobile-ops-quality-auditor, mobile-ops-compliance-checker, mobile-ops-evidence-grounder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, travel-ops-normalizer, travel-ops-field-extractor, travel-ops-summary-writer, travel-ops-dependency-mapper |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-priority-ranker, travel-ops-quality-auditor, travel-ops-summary-writer, travel-ops-timeline-builder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-field-extractor, travel-ops-rewrite-editor, travel-ops-quality-auditor, travel-ops-evidence-grounder |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `supply-chain-ops-field-extractor` | wrong | supply-chain-ops-field-extractor, procurement-ops-field-extractor, receipt-extractor, supply-chain-ops-normalizer, finance-ops-normalizer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, legal-ops-rewrite-editor, insurance-ops-comparison-builder, legal-ops-artifact-packager, writing-ops-compliance-checker |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, procurement-ops-field-extractor, public-office-pdf-form-filler, procurement-ops-normalizer |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `ux-ops-field-extractor` | wrong | ux-ops-field-extractor, customer-success-ops-field-extractor, partnerships-ops-field-extractor, facilities-ops-field-extractor, grant-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, sre-ops-failure-diagnoser, medical-admin-ops-failure-diagnoser, medical-admin-ops-intake-classifier, medical-admin-ops-dependency-mapper |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, sre-ops-quality-auditor, sre-ops-failure-diagnoser, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, sre-ops-evidence-grounder, sre-ops-quality-auditor, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, sre-ops-risk-reviewer, metrics-overview, sre-ops-scenario-planner, sre-ops-timeline-builder |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, debugging-root-cause-helper, cloud-ops-failure-diagnoser, analytics-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 9 | 1 | `incident-ops-summary-writer` | acceptable | incident-ops-summary-writer, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-resource-linker, incident-ops-rewrite-editor |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, journalism-ops-summary-writer, media-ops-summary-writer, community-ops-summary-writer, property-ops-summary-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, events-ops-summary-writer, incident-ops-handoff-brief-writer, events-ops-evidence-grounder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, retail-ops-evidence-grounder, content-ops-evidence-grounder, product-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, customer-feedback-analyser, news-briefing-writer, news-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-theme-extractor, iot-ops-evidence-grounder, dashboard-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-quality-auditor` | wrong | grant-ops-quality-auditor, grant-ops-failure-diagnoser, grant-ops-risk-reviewer, grant-ops-acceptance-test-builder, grant-ops-artifact-packager |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, receipt-extractor, finance-ops-rewrite-editor, public-office-invoice-organizer, finance-ops-evidence-grounder |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-artifact-packager, vendor-ops-quality-auditor, vendor-ops-dependency-mapper, procurement-ops-rewrite-editor |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, financial-model-builder, finance-ops-risk-reviewer, data-analysis-with-validation, finance-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, public-office-ppt-visual, public-office-pptx-manipulation, public-office-dev-slides |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `engineering-design-ops-handoff-brief-writer` | wrong | engineering-design-ops-handoff-brief-writer, construction-ops-handoff-brief-writer, research-ops-handoff-brief-writer, grant-ops-handoff-brief-writer, bioinformatics-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-dependency-mapper, meeting-ops-scenario-planner, meeting-ops-timeline-builder |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-summary-writer, meeting-ops-normalizer, meeting-ops-handoff-brief-writer, meeting-ops-timeline-builder |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 9 | 9 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-ops-handoff-brief-writer, meeting-ops-field-extractor, meeting-ops-artifact-packager, meeting-ops-normalizer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-ops-normalizer, meeting-ops-rewrite-editor, meeting-ops-summary-writer, weekly-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-scheduler, meeting-ops-timeline-builder, personal-ops-timeline-builder, deadline-reminder-planner |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer, related-work-synthesiser |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, journalism-ops-summary-writer, ux-ops-summary-writer, research-ops-summary-writer, energy-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, research-ops-artifact-packager, research-ops-summary-writer, speaker-notes-writer, research-ops-resource-linker |
| `read_p4_document_extraction` | `document-extractor` | 19 | 19 | `journalism-ops-field-extractor` | wrong | journalism-ops-field-extractor, research-ops-field-extractor, k8s-ops-field-extractor, dataset-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, thesis-ops-evidence-grounder, research-ops-quality-auditor, research-ops-evidence-grounder, research-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, research-ops-evidence-grounder, agent-eval-coverage-auditor, thesis-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 7 | 7 | `research-ops-comparison-builder` | wrong | research-ops-comparison-builder, journalism-ops-comparison-builder, thesis-ops-comparison-builder, course-ops-comparison-builder, partnerships-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, note-linker, research-ops-resource-linker, paper-summariser, research-ops-summary-writer |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, email-ops-rewrite-editor, email-drafter, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `email-polisher` | wrong | email-polisher, reply-polisher, email-ops-rewrite-editor, reply-drafter, fundraising-ops-rewrite-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, email-action-extractor, meeting-ops-summary-writer, construction-ops-timeline-builder |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, personal-ops-handoff-brief-writer, operations-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, email-ops-handoff-brief-writer, email-ops-timeline-builder, email-ops-artifact-packager, email-ops-rewrite-editor |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, auth-flow-reviewer, security-code-reviewer, security-ops-risk-reviewer, public-security-threat-model |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, api-ops-risk-reviewer, api-ops-quality-auditor, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, supply-chain-ops-dependency-mapper, supply-chain-ops-risk-reviewer, risk-ops-dependency-mapper, supply-chain-ops-artifact-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, public-openai-cloudflare-deploy, public-openai-vercel-deploy, public-openai-render-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-risk-reviewer, identity-ops-priority-ranker, identity-ops-compliance-checker, identity-ops-quality-auditor |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 9 | 9 | `analytics-ops-compliance-checker` | wrong | analytics-ops-compliance-checker, analytics-ops-risk-reviewer, analytics-ops-evidence-grounder, analytics-ops-priority-ranker, analytics-ops-timeline-builder |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-ops-comparison-builder, meeting-ops-resource-linker, meeting-ops-dependency-mapper, knowledge-ops-dependency-mapper |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-office-excel-automation, public-office-data-analysis, public-office-sheets-automation, public-office-xlsx-manipulation |
| `skill_p3_create_new` | `skill-creator` | - | - | `meeting-ops-dependency-mapper` | wrong | meeting-ops-dependency-mapper, meeting-ops-summary-writer, meeting-ops-rewrite-editor, thesis-ops-timeline-builder, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, hr-ops-field-extractor, operations-ops-field-extractor, agent-ops-field-extractor, knowledge-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, writing-ops-rewrite-editor, email-ops-quality-auditor, email-ops-rewrite-editor, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, research-ops-artifact-packager, agent-ops-dependency-mapper, knowledge-ops-summary-writer, research-ops-summary-writer |
