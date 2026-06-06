# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2349 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 50.6% |
| Acceptable top-1 accuracy | 51.8% |
| Top-3 recall | 65.9% |
| Top-5 recall | 69.4% |
| Acceptable top-5 recall | 71.8% |
| MRR | 0.590 |
| Non-main top-1 | 30.6% |
| Approx selector-visible tokens | 1240760 |

## API Usage Estimate

- Embedding API calls made in this run: 26
- Embedding cache hits: 2174
- Approx uncached embedding input tokens: 175188
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester, api-ops-quality-auditor, api-ops-dependency-mapper |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-artifact-packager, api-ops-handoff-brief-writer, api-ops-scenario-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, receipt-extractor, events-ops-monitoring-plan-builder, external-api-integration-planner |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, public-swebench-service-mesh-observability, public-addy-agent-api-and-interface-design |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, mobile-ops-monitoring-plan-builder, public-office-subscription-management, webhook-contract-planner, migration-risk-auditor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 4 | 4 | `finance-ops-monitoring-plan-builder` | wrong | finance-ops-monitoring-plan-builder, customer-success-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, service-dependency-mapper, customer-success-ops-dependency-mapper |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, customer-success-ops-acceptance-test-builder, web-form-filler |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, web-ops-handoff-brief-writer, web-ops-artifact-packager, web-ops-acceptance-test-builder |
| `web_p3_ui_test` | `web-ui-tester` | 12 | 12 | `ecommerce-ops-compliance-checker` | wrong | ecommerce-ops-compliance-checker, logistics-ops-compliance-checker, ecommerce-ops-acceptance-test-builder, invoice-payment-checker, logistics-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 2 | 2 | `ecommerce-ops-comparison-builder` | wrong | ecommerce-ops-comparison-builder, web-data-extractor, ecommerce-ops-artifact-packager, ecommerce-ops-normalizer, ecommerce-ops-summary-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-normalizer` | wrong | personal-ops-normalizer, public-swebench-add-admin-api-endpoint, personal-ops-rewrite-editor, personal-ops-handoff-brief-writer, personal-ops-artifact-packager |
| `web_p6_accessibility_check` | `accessibility-checker` | 3 | 3 | `web-form-filler` | wrong | web-form-filler, accessibility-interaction-auditor, accessibility-checker, email-drafter, fundraising-ops-normalizer |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-ops-normalizer, personal-ops-normalizer, email-ops-dependency-mapper, reply-polisher |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, external-api-integration-planner, public-swebench-add-admin-api-endpoint, openapi-contract-reviewer, api-ops-rewrite-editor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `external-api-integration-planner` | wrong | external-api-integration-planner, api-ops-monitoring-plan-builder, api-ops-quality-auditor, api-ops-rewrite-editor, api-ops-failure-diagnoser |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, external-api-integration-planner, openapi-contract-reviewer, public-swebench-add-admin-api-endpoint, api-ops-rewrite-editor |
| `code_p5_changelog_entry` | `changelog-writer` | 7 | 7 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, external-api-integration-planner, churn-risk-analyser, privacy-risk-reviewer, release-note-writer |
| `code_p6_release_notes` | `release-note-writer` | - | - | `mobile-ops-rewrite-editor` | wrong | mobile-ops-rewrite-editor, mobile-ops-timeline-builder, mobile-ops-quality-auditor, mobile-ops-monitoring-plan-builder, mobile-ops-artifact-packager |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, data-analysis-for-reporting, data-analysis-with-anomaly-focus |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 4 | 4 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-with-validation, ads-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, data-analysis-overview, ads-ops-failure-diagnoser, marketing-ops-failure-diagnoser, marketing-ops-monitoring-plan-builder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-reporting, marketing-ops-summary-writer, ads-ops-summary-writer, data-analysis-for-root-cause-diagnosis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, product-ops-priority-ranker, facilities-ops-priority-ranker, analytics-ops-priority-ranker, priority-sorter |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 17 | 17 | `receipt-extractor` | wrong | receipt-extractor, ecommerce-ops-acceptance-test-builder, frontend-debugger, web-form-filler, ecommerce-ops-compliance-checker |
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
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, procurement-ops-field-extractor, email-drafter, web-form-filler, operations-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, metrics-root-cause-diagnoser, slo-breach-checker, capacity-risk-forecaster |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, metrics-root-cause-diagnoser, capacity-risk-forecaster, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview, sre-ops-failure-diagnoser |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, capacity-risk-forecaster, latency-anomaly-detector, service-dependency-mapper |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-dependency-mapper, incident-ops-handoff-brief-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, general-source-summariser, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `events-ops-monitoring-plan-builder` | wrong | events-ops-monitoring-plan-builder, news-briefing-writer, events-ops-handoff-brief-writer, incident-summary-writer, events-ops-risk-reviewer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, tech-news-trend-extractor, product-ops-evidence-grounder, document-extractor, citation-grounding-helper |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, mobile-ops-evidence-grounder, news-summariser |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-normalizer` | wrong | grant-ops-normalizer, grant-ops-field-extractor, grant-ops-summary-writer, grant-ops-artifact-packager, grant-ops-quality-auditor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `receipt-extractor` | wrong | receipt-extractor, pdf-ocr-extractor, invoice-payment-checker, finance-ops-field-extractor, document-field-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-handoff-brief-writer, vendor-ops-summary-writer, vendor-ops-risk-reviewer, vendor-ops-artifact-packager |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, financial-model-builder, finance-ops-scenario-planner, finance-ops-summary-writer, vendor-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, deck-template-applier, slide-outline-builder, public-office-ppt-visual, public-office-pptx-manipulation |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `construction-ops-handoff-brief-writer` | wrong | construction-ops-handoff-brief-writer, product-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, engineering-design-ops-handoff-brief-writer, product-ops-dependency-mapper |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 3 | 3 | `meeting-ops-risk-reviewer` | wrong | meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-agenda-builder, meeting-ops-artifact-packager, meeting-ops-dependency-mapper |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-agenda-builder, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, weekly-planner |
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
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, auth-flow-reviewer, public-office-suspicious-email, public-security-threat-model |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, public-swebench-add-admin-api-endpoint, external-api-integration-planner, webhook-contract-planner, api-ops-rewrite-editor |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, public-oh-my-npm-git-install, migration-risk-auditor, public-openai-transcribe, risk-ops-artifact-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 9 | 9 | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-setup-planner, public-oh-my-deployment-automation, deployment-build-triager, public-openai-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-quality-auditor, identity-ops-compliance-checker, identity-ops-comparison-builder, identity-ops-dependency-mapper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-handoff-brief-writer, analytics-ops-summary-writer, analytics-ops-quality-auditor, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, library-ops-dependency-mapper, library-ops-summary-writer, meeting-ops-dependency-mapper, skill-creator |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-office-data-analysis, public-office-xlsx-manipulation, public-swebench-xlsx, data-analysis-with-validation |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-artifact-packager, personal-ops-handoff-brief-writer, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, docs-ops-field-extractor, operations-ops-field-extractor, document-extractor, knowledge-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, email-polisher, followup-reply-writer, email-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, public-huggingface-huggingface-papers, docs-ops-summary-writer, paper-summariser, public-huggingface-huggingface-paper-publisher |
