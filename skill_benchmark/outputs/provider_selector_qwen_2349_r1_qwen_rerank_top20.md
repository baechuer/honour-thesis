# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (2349 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 60.0% |
| Acceptable top-1 accuracy | 63.5% |
| Top-3 recall | 62.4% |
| Top-5 recall | 63.5% |
| Acceptable top-5 recall | 65.9% |
| MRR | 0.615 |
| Non-main top-1 | 36.5% |
| Approx selector-visible tokens | 305354 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2434
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 85
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 185330

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, api-ops-quality-auditor, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 1 | `api-integration-planner` | acceptable | api-integration-planner, external-api-integration-planner, api-design-reviewer, api-ops-timeline-builder, api-ops-handoff-brief-writer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, public-office-webhook-automation, public-office-stripe-payments, events-ops-acceptance-test-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, service-dependency-mapper, public-addy-agent-api-and-interface-design, medical-admin-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-addy-agent-shipping-and-launch, public-office-subscription-management, public-addy-agent-deprecation-and-migration |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, metrics-root-cause-diagnoser, analytics-ops-failure-diagnoser, ads-ops-failure-diagnoser, support-ops-failure-diagnoser |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, ux-ops-acceptance-test-builder, finance-ops-acceptance-test-builder, customer-success-ops-acceptance-test-builder, support-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-n-skills-dev-browser, public-oh-my-agent-browser, public-office-browser-automation, public-oh-my-playwriter |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `ecommerce-ops-acceptance-test-builder` | wrong | ecommerce-ops-acceptance-test-builder, customer-success-ops-acceptance-test-builder, logistics-ops-acceptance-test-builder, real-estate-ops-acceptance-test-builder, customer-success-ops-compliance-checker |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `public-oh-my-to-prd` | wrong | public-oh-my-to-prd, public-office-amazon-seller, ecommerce-ops-comparison-builder, public-oh-my-notebooklm, data-analysis-for-ranking-selection |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `public-mattpocock-prototype` | wrong | public-mattpocock-prototype, identity-ops-rewrite-editor, personal-ops-rewrite-editor, api-integration-planner, public-mattpocock-edit-article |
| `web_p6_accessibility_check` | `accessibility-checker` | - | - | `public-addy-web-accessibility` | wrong | public-addy-web-accessibility, public-office-form-builder, public-office-applicant-screening, support-ops-ops-rewrite-editor, compliance-checklist-builder |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `public-mattpocock-tdd` | wrong | public-mattpocock-tdd, email-ops-normalizer, public-mattpocock-triage, personal-ops-normalizer, public-mattpocock-edit-article |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `public-addy-agent-deprecation-and-migration` | wrong | public-addy-agent-deprecation-and-migration, auth-flow-reviewer, migration-risk-auditor, database-migration-risk-assessor, public-oh-my-authentication-setup |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, public-openai-gh-address-comments, api-integration-planner, public-openai-gh-fix-ci, public-swebench-python-resilience |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `public-openai-gh-fix-ci` | wrong | public-openai-gh-fix-ci, auth-flow-reviewer, public-swebench-fix, public-openai-gh-address-comments, public-oh-my-backend-testing |
| `code_p5_changelog_entry` | `changelog-writer` | - | - | `public-addy-agent-incremental-implementation` | wrong | public-addy-agent-incremental-implementation, public-addy-agent-deprecation-and-migration, public-openai-gh-fix-ci, public-swebench-fix, public-addy-agent-security-and-hardening |
| `code_p6_release_notes` | `release-note-writer` | - | - | `public-addy-agent-incremental-implementation` | wrong | public-addy-agent-incremental-implementation, public-addy-agent-performance-optimization, identity-ops-timeline-builder, api-integration-planner, support-ops-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, public-office-data-analysis, data-analysis-with-validation, data-analysis-for-reporting, data-analysis-for-forecasting |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-forecasting, analytics-ops-monitoring-plan-builder, latency-anomaly-detector, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, analytics-ops-quality-auditor, data-analysis-with-anomaly-focus, support-ops-quality-auditor, ads-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, marketing-ops-failure-diagnoser, ads-ops-failure-diagnoser, analytics-ops-failure-diagnoser, analytics-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, analytics-ops-summary-writer, retail-ops-summary-writer, support-ops-ops-summary-writer, journalism-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-overview, data-analysis-with-anomaly-focus, public-swebench-creating-financial-models |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `agent-ops-priority-ranker` | wrong | agent-ops-priority-ranker, events-ops-priority-ranker, risk-ops-priority-ranker, operations-ops-priority-ranker, meeting-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | - | - | `ecommerce-ops-acceptance-test-builder` | wrong | ecommerce-ops-acceptance-test-builder, ecommerce-ops-quality-auditor, public-oh-my-state-management, public-oh-my-ccpi-marketplace, logistics-ops-acceptance-test-builder |
| `deploy_p2_visual_regression` | `visual-regression-checker` | - | - | `support-ops-comparison-builder` | wrong | support-ops-comparison-builder, ads-ops-comparison-builder, mobile-ops-comparison-builder, landing-page-copy-reviewer, proposal-drafter |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | - | - | `public-addy-web-accessibility` | wrong | public-addy-web-accessibility, meeting-ops-quality-auditor, fundraising-ops-quality-auditor, academic-admin-ops-quality-auditor, public-oh-my-authentication-setup |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, environment-config-auditor, public-oh-my-game-build-log-triage, public-openai-vercel-deploy |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-addy-agent-shipping-and-launch, public-oh-my-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, mobile-ops-quality-auditor, public-addy-web-performance |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-rewrite-editor, travel-ops-priority-ranker, travel-ops-compliance-checker, travel-ops-summary-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-field-extractor, travel-ops-quality-auditor |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-rewrite-editor, travel-ops-quality-auditor, travel-ops-evidence-grounder, travel-ops-intake-classifier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `receipt-extractor` | wrong | receipt-extractor, public-office-invoice-automation, supply-chain-ops-normalizer, public-office-invoice-organizer, public-office-invoice-generator |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, legal-ops-rewrite-editor, legal-ops-compliance-checker, clause-obligation-extractor, legal-ops-handoff-brief-writer |
| `doc_p6_conversion` | `document-converter` | - | - | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, document-summariser, research-ops-handoff-brief-writer, procurement-risk-summariser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `public-office-form-builder` | wrong | public-office-form-builder, public-office-pdf-form-filler, fundraising-ops-handoff-brief-writer, academic-admin-ops-handoff-brief-writer, grant-ops-handoff-brief-writer |
| `obs_p1_metrics_overview` | `metrics-overview` | 4 | 4 | `public-mattpocock-triage` | wrong | public-mattpocock-triage, public-oh-my-triage, support-ticket-triager, metrics-overview, database-ops-intake-classifier |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, slo-breach-checker, analytics-ops-failure-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, incident-ops-failure-diagnoser, incident-ops-risk-reviewer, risk-ops-failure-diagnoser |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, risk-ops-failure-diagnoser, operations-ops-failure-diagnoser, cloud-ops-failure-diagnoser, incident-ops-failure-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, debugging-root-cause-helper, cloud-ops-failure-diagnoser, analytics-ops-failure-diagnoser, qa-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-handoff-brief-writer, incident-ops-summary-writer, incident-ops-failure-diagnoser, facilities-ops-handoff-brief-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, journalism-ops-summary-writer, news-briefing-writer, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, journalism-ops-handoff-brief-writer, events-ops-handoff-brief-writer, incident-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, sales-ops-evidence-grounder, research-ops-evidence-grounder, ecommerce-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, general-source-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, iot-ops-evidence-grounder, engineering-design-ops-evidence-grounder, analytics-ops-evidence-grounder, journalism-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-quality-auditor` | wrong | grant-ops-quality-auditor, grant-ops-compliance-checker, grant-ops-failure-diagnoser, grant-ops-rewrite-editor, grant-ops-artifact-packager |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-ocr, receipt-extractor, public-office-expense-tracker, finance-ops-field-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-risk-reviewer, vendor-ops-quality-auditor, vendor-ops-artifact-packager, vendor-ops-compliance-checker |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, financial-model-builder, public-office-financial-modeling, public-swebench-creating-financial-models, procurement-risk-summariser |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, public-office-ppt-visual, public-oh-my-presentation-builder, public-office-ai-slides |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `engineering-design-ops-handoff-brief-writer` | wrong | engineering-design-ops-handoff-brief-writer, energy-ops-handoff-brief-writer, knowledge-ops-handoff-brief-writer, research-ops-handoff-brief-writer, manufacturing-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, public-openai-notion-meeting-intelligence, meeting-ops-timeline-builder, meeting-ops-risk-reviewer, meeting-ops-scenario-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, document-summariser, public-office-meeting-notes, meeting-followup-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-ops-summary-writer, meeting-summary-writer, task-extractor, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-followup-extractor, meeting-agenda-builder, public-addy-agent-planning-and-task-breakdown |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, public-addy-agent-planning-and-task-breakdown, subagent-task-planner, meeting-ops-timeline-builder, meeting-scheduler |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, public-oh-my-research-paper-writing, docs-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 6 | 6 | `research-ops-summary-writer` | wrong | research-ops-summary-writer, supply-chain-ops-summary-writer, manufacturing-ops-summary-writer, retail-ops-summary-writer, environmental-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, document-converter, public-openai-notion-research-documentation, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | - | - | `support-ops-ops-field-extractor` | wrong | support-ops-ops-field-extractor, research-ops-field-extractor, sre-ops-field-extractor, retail-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, multi-source-comparison-builder, engineering-design-ops-evidence-grounder, research-ops-evidence-grounder, manufacturing-ops-evidence-grounder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, writing-ops-evidence-grounder, agent-ops-rewrite-editor, agent-eval-coverage-auditor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, knowledge-ops-comparison-builder, engineering-design-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, method-note-builder, research-ops-resource-linker, research-ops-summary-writer, research-ops-failure-diagnoser |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, email-drafter, reply-drafter, reply-polisher, email-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, meeting-ops-rewrite-editor, compliance-ops-rewrite-editor, public-anthropic-internal-comms, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, deadline-reminder-planner, academic-admin-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, meeting-followup-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, operations-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, incident-ops-handoff-brief-writer, risk-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `email-ops-handoff-brief-writer` | wrong | email-ops-handoff-brief-writer, followup-reply-writer, reply-drafter, compliance-ops-handoff-brief-writer, public-anthropic-internal-comms |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, public-swebench-security-review, public-brainstorming, public-addy-agent-security-and-hardening |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `public-swebench-security-review` | wrong | public-swebench-security-review, public-addy-agent-security-and-hardening, public-addy-web-best-practices, public-swebench-add-malli-schemas, api-design-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, supply-chain-ops-dependency-mapper, risk-ops-artifact-packager, contract-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `environment-config-auditor` | wrong | environment-config-auditor, public-swebench-security-review, public-openai-vercel-deploy, public-swebench-python-configuration, public-swebench-fix |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-compliance-checker, identity-ops-quality-auditor, public-addy-agent-security-and-hardening, public-swebench-security-review |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-swebench-analytics-events` | wrong | public-swebench-analytics-events, analytics-ops-evidence-grounder, analytics-ops-compliance-checker, analytics-ops-risk-reviewer, privacy-ops-quality-auditor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, search-ops-handoff-brief-writer, task-extractor, knowledge-ops-handoff-brief-writer |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, public-office-data-analysis, data-analysis-with-validation, public-office-sheets-automation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, public-anthropic-skill-creator, task-extractor, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, agent-ops-field-extractor, knowledge-ops-field-extractor, operations-ops-field-extractor, legal-discovery-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, email-polisher, public-anthropic-skill-creator, groupwork-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, document-summariser, general-source-summariser, public-anthropic-skill-creator, research-ops-summary-writer |
