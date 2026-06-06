# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2349 skills)
- Reranker: `local-schema`
- Rerank candidates: 50

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 80.0% |
| Acceptable top-1 accuracy | 81.2% |
| Top-3 recall | 84.7% |
| Top-5 recall | 84.7% |
| Acceptable top-5 recall | 85.9% |
| MRR | 0.822 |
| Non-main top-1 | 12.9% |
| Approx selector-visible tokens | 1240760 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2434
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester, api-ops-normalizer, api-design-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-acceptance-test-builder, customer-success-ops-acceptance-test-builder, api-ops-monitoring-plan-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, ecommerce-ops-timeline-builder, events-ops-monitoring-plan-builder, events-ops-acceptance-test-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, public-addy-agent-api-and-interface-design, platform-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, mobile-ops-monitoring-plan-builder, public-office-subscription-management, webhook-contract-planner |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, finance-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, customer-success-ops-monitoring-plan-builder, analytics-ops-failure-diagnoser |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, accessibility-interaction-auditor, metrics-overview |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, web-ui-tester, qa-ops-field-extractor, playwright-flow-debugger |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, ecommerce-ops-acceptance-test-builder, logistics-ops-acceptance-test-builder, ecommerce-ops-compliance-checker, partnerships-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, ecommerce-ops-field-extractor, ecommerce-ops-comparison-builder, ecommerce-ops-summary-writer, product-ops-comparison-builder |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `public-swebench-add-admin-api-endpoint` | wrong | public-swebench-add-admin-api-endpoint, api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-integration-planner, external-api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, email-drafter, web-ui-tester |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, professor-email-reply, churn-risk-analyser, email-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `external-api-integration-planner` | wrong | external-api-integration-planner, database-migration-risk-assessor, auth-flow-reviewer, openapi-contract-reviewer, api-ops-acceptance-test-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, external-api-integration-planner, pr-reviewer, code-reviewer, api-ops-acceptance-test-builder |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, ci-failure-debugger, web-ui-tester, external-api-integration-planner, openapi-contract-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, external-api-integration-planner, privacy-risk-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, mobile-ops-timeline-builder, mobile-ops-rewrite-editor, mobile-ops-quality-auditor, mobile-ops-evidence-grounder |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting, dataset-ops-summary-writer, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, dataset-ops-quality-auditor, support-ops-quality-auditor, ads-ops-quality-auditor, marketing-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, ads-ops-failure-diagnoser, marketing-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, marketing-ops-summary-writer, ads-ops-summary-writer, content-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, metrics-root-cause-diagnoser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, dashboard-ops-priority-ranker, risk-ops-priority-ranker, product-ops-priority-ranker, analytics-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, web-ui-tester, receipt-extractor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, proposal-drafter, vendor-ops-summary-writer, competitive-battlecard-builder, slide-deck-visual-auditor |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, web-form-filler, ads-ops-normalizer, ads-ops-quality-auditor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, ci-failure-debugger, secret-leak-scanner, frontend-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-note-writer, deployment-build-triager, public-openai-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-evidence-grounder, mobile-ops-summary-writer, mobile-ops-priority-ranker, mobile-ops-acceptance-test-builder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, facilities-ops-summary-writer, travel-ops-quality-auditor, travel-ops-compliance-checker, travel-ops-handoff-brief-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, facilities-ops-rewrite-editor, medical-admin-ops-rewrite-editor, logistics-ops-rewrite-editor, events-ops-rewrite-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-rewrite-editor` | wrong | travel-ops-rewrite-editor, travel-ops-normalizer, facilities-ops-rewrite-editor, events-ops-rewrite-editor, procurement-ops-rewrite-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, supply-chain-ops-field-extractor, receipt-extractor, procurement-ops-field-extractor, vendor-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, privacy-policy-drafter, legal-ops-rewrite-editor, insurance-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, research-ops-risk-reviewer, citation-note-extractor, research-ops-dependency-mapper |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, procurement-ops-field-extractor, operations-ops-field-extractor, academic-admin-ops-field-extractor, ux-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, public-mattpocock-triage, cloud-monitoring-configurer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, service-dependency-mapper, platform-ops-risk-reviewer, risk-ops-acceptance-test-builder |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, sre-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, journalism-ops-summary-writer, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, metrics-overview, events-ops-scenario-planner |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, document-extractor, knowledge-base-article-writer, retail-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, metrics-root-cause-diagnoser |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, grant-ops-field-extractor, grant-ops-quality-auditor, grant-ops-normalizer, grant-ops-summary-writer |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, receipt-extractor, finance-ops-rewrite-editor, pdf-layout-reviewer, vendor-ops-rewrite-editor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, vendor-ops-rewrite-editor, vendor-ops-handoff-brief-writer, vendor-ops-artifact-packager, vendor-ops-risk-reviewer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, finance-ops-scenario-planner, data-analysis-with-validation, vendor-ops-scenario-planner, procurement-risk-summariser |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, slide-outline-builder, deck-template-applier, public-office-ppt-visual, thesis-ops-rewrite-editor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `repo-ops-handoff-brief-writer` | wrong | repo-ops-handoff-brief-writer, construction-ops-summary-writer, construction-ops-handoff-brief-writer, construction-ops-normalizer, product-ops-quality-auditor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-followup-extractor, meeting-summary-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, incident-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-field-extractor, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-scheduler, meeting-agenda-builder, meeting-ops-timeline-builder, meeting-ops-acceptance-test-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, data-analysis-for-reporting, construction-ops-summary-writer, energy-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, speaker-notes-writer, note-linker, method-note-builder, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | - | - | `web-data-extractor` | wrong | web-data-extractor, research-ops-field-extractor, lab-ops-field-extractor, incident-ops-field-extractor, journalism-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, research-ops-acceptance-test-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-ops-rewrite-editor, research-ops-evidence-grounder, support-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder, related-work-synthesiser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ux-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply, reply-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, email-polisher, groupwork-reply, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, meeting-followup-extractor, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, groupwork-reply, reply-polisher, travel-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, email-ops-risk-reviewer, public-office-suspicious-email, auth-flow-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, external-api-integration-planner, public-swebench-add-admin-api-endpoint, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, migration-risk-auditor, risk-ops-artifact-packager, public-oh-my-npm-git-install |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, webhook-contract-planner, environment-config-auditor, public-openai-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-evidence-grounder, identity-ops-acceptance-test-builder, identity-ops-monitoring-plan-builder, identity-ops-quality-auditor |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-resource-linker, data-analysis-with-anomaly-focus, churn-risk-analyser, analytics-ops-handoff-brief-writer |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, library-ops-dependency-mapper, library-ops-comparison-builder, meeting-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, public-office-data-analysis, data-analysis-for-reporting, public-office-sheets-automation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, document-field-extractor, agent-ops-field-extractor, operations-ops-field-extractor, hr-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, public-huggingface-huggingface-papers, agent-ops-summary-writer, public-huggingface-huggingface-paper-publisher, docs-ops-summary-writer |
