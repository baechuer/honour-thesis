# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (2349 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 50.6% |
| Acceptable top-1 accuracy | 50.6% |
| Top-3 recall | 62.4% |
| Top-5 recall | 64.7% |
| Acceptable top-5 recall | 65.9% |
| MRR | 0.571 |
| Non-main top-1 | 36.5% |
| Approx selector-visible tokens | 619548 |

## API Usage Estimate

- Embedding API calls made in this run: 135
- Embedding cache hits: 1091
- Approx uncached embedding input tokens: 316325
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester, api-ops-normalizer, invoice-payment-checker |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-summary-writer, webhook-contract-planner, public-swebench-security-review |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-monitoring-plan-builder, email-ops-monitoring-plan-builder, receipt-extractor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, public-addy-agent-api-and-interface-design, external-api-integration-planner |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 2 | 2 | `public-office-subscription-management` | wrong | public-office-subscription-management, database-migration-risk-assessor, customer-success-ops-normalizer, grant-ops-monitoring-plan-builder, mobile-ops-monitoring-plan-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 3 | 3 | `finance-ops-monitoring-plan-builder` | wrong | finance-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, service-dependency-mapper, capacity-risk-forecaster, dataset-ops-monitoring-plan-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, customer-success-ops-summary-writer, frontend-debugger, public-addy-web-accessibility |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, web-page-snapshotter, public-n-skills-dev-browser |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `ecommerce-ops-compliance-checker` | wrong | ecommerce-ops-compliance-checker, ecommerce-ops-acceptance-test-builder, logistics-ops-compliance-checker, invoice-payment-checker, logistics-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `public-office-competitive-analysis` | wrong | public-office-competitive-analysis, public-oh-my-ccpi-marketplace, public-office-table-extractor, public-office-amazon-seller, public-office-shopify-automation |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `public-mattpocock-edit-article` | wrong | public-mattpocock-edit-article, public-swebench-add-admin-api-endpoint, public-openai-figma-create-new-file, personal-ops-normalizer, identity-ops-handoff-brief-writer |
| `web_p6_accessibility_check` | `accessibility-checker` | 17 | 17 | `web-form-filler` | wrong | web-form-filler, accessibility-interaction-auditor, public-addy-web-accessibility, fundraising-ops-compliance-checker, webhook-setup-planner |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, public-oh-my-pretext, email-polisher, email-thread-summariser, public-mattpocock-grill-me |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, external-api-integration-planner, openapi-contract-reviewer, database-migration-risk-assessor, public-swebench-add-admin-api-endpoint |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 15 | 15 | `external-api-integration-planner` | wrong | external-api-integration-planner, public-swebench-python-resilience, openapi-contract-reviewer, public-mattpocock-review, ecommerce-ops-quality-auditor |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, external-api-integration-planner, openapi-contract-reviewer, public-swebench-add-admin-api-endpoint, public-oh-my-authentication-setup |
| `code_p5_changelog_entry` | `changelog-writer` | 13 | 13 | `external-api-integration-planner` | wrong | external-api-integration-planner, auth-flow-reviewer, churn-risk-analyser, privacy-risk-reviewer, customer-success-ops-normalizer |
| `code_p6_release_notes` | `release-note-writer` | - | - | `mobile-ops-timeline-builder` | wrong | mobile-ops-timeline-builder, mobile-ops-normalizer, mobile-ops-quality-auditor, mobile-ops-summary-writer, churn-risk-analyser |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-root-cause-diagnosis, public-office-data-analysis, data-analysis-for-forecasting, data-analysis-with-anomaly-focus |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, data-analysis-overview, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 5 | 5 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, public-office-saas-metrics, web-performance-budget-checker, public-addy-web-performance, data-analysis-with-validation |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, web-performance-budget-checker, public-addy-web-performance, public-office-saas-metrics, public-swebench-analytics-events |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, ads-ops-summary-writer, marketing-ops-summary-writer, sre-ops-summary-writer, analytics-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, public-oh-my-performance-optimization |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, identity-ops-priority-ranker, meeting-ops-priority-ranker, dashboard-ops-priority-ranker, facilities-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 13 | 13 | `receipt-extractor` | wrong | receipt-extractor, ecommerce-ops-normalizer, invoice-payment-checker, ecommerce-ops-compliance-checker, ecommerce-ops-acceptance-test-builder |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 18 | 18 | `public-office-subscription-management` | wrong | public-office-subscription-management, mobile-ops-comparison-builder, public-office-dcf-valuation, public-office-invoice-generator, public-office-competitive-analysis |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, customer-success-ops-normalizer, ads-ops-normalizer, ads-ops-quality-auditor, public-addy-web-accessibility |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, public-oh-my-vercel-deploy, public-oh-my-game-build-log-triage, environment-config-auditor |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-oh-my-vercel-deploy, public-openai-vercel-deploy, public-addy-agent-shipping-and-launch |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, public-addy-web-performance, mobile-ops-summary-writer, public-addy-web-core-web-vitals, mobile-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-normalizer, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-intake-classifier |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 6 | `travel-ops-summary-writer` | borderline | travel-ops-summary-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-handoff-brief-writer, travel-ops-quality-auditor |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-summary-writer, travel-ops-handoff-brief-writer, facilities-ops-normalizer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, supply-chain-ops-summary-writer, public-office-invoice-generator, public-office-invoice-organizer, supply-chain-ops-normalizer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 2 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-comparison-builder, email-polisher, legal-ops-rewrite-editor, terms-of-service-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, research-ops-intake-classifier, public-office-pdf-form-filler, research-ops-compliance-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-normalizer` | wrong | medical-admin-ops-normalizer, public-office-pdf-form-filler, procurement-ops-field-extractor, procurement-ops-normalizer, facilities-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, capacity-risk-forecaster, slo-breach-checker, public-mattpocock-triage |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, service-dependency-mapper, capacity-risk-forecaster, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, latency-anomaly-detector, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, capacity-risk-forecaster, service-dependency-mapper, metrics-overview, slo-breach-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer, metrics-overview |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, events-ops-risk-reviewer, events-ops-monitoring-plan-builder, events-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, supply-chain-ops-evidence-grounder, vendor-ops-evidence-grounder, retail-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, mobile-ops-evidence-grounder, public-swebench-linkerd-patterns |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-normalizer` | wrong | grant-ops-normalizer, grant-ops-field-extractor, grant-ops-summary-writer, grant-ops-quality-auditor, grant-ops-comparison-builder |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `receipt-extractor` | wrong | receipt-extractor, pdf-ocr-extractor, public-office-invoice-organizer, public-office-expense-tracker, invoice-payment-checker |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-handoff-brief-writer` | wrong | vendor-ops-handoff-brief-writer, vendor-ops-rewrite-editor, vendor-ops-risk-reviewer, vendor-ops-normalizer, vendor-ops-summary-writer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 2 | 2 | `public-office-dcf-valuation` | wrong | public-office-dcf-valuation, spreadsheet-formula-auditor, financial-model-builder, public-swebench-creating-financial-models, public-office-financial-modeling |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, deck-template-applier, slide-outline-builder, public-pptx, thesis-ops-quality-auditor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `construction-ops-handoff-brief-writer` | wrong | construction-ops-handoff-brief-writer, bioinformatics-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, lab-ops-handoff-brief-writer, research-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 2 | 2 | `meeting-ops-risk-reviewer` | wrong | meeting-ops-risk-reviewer, meeting-agenda-builder, meeting-ops-scenario-planner, meeting-followup-extractor, meeting-ops-quality-auditor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, meeting-ops-summary-writer, task-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 4 | 4 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, task-extractor, weekly-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-ops-timeline-builder, agent-ops-timeline-builder, meeting-agenda-builder, thesis-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, research-ops-summary-writer, thesis-ops-summary-writer, citation-grounding-helper |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, energy-ops-summary-writer, customer-success-ops-summary-writer, facilities-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, general-source-summariser, public-oh-my-notebooklm, public-oh-my-obsidian-cli-uri-fallback |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, incident-ops-field-extractor, course-ops-field-extractor, social-ops-field-extractor, supply-chain-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, citation-grounding-helper, research-ops-scenario-planner, research-ops-comparison-builder, research-ops-priority-ranker |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, environmental-ops-evidence-grounder, agent-eval-coverage-auditor, real-estate-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `research-ops-comparison-builder` | wrong | research-ops-comparison-builder, multi-source-comparison-builder, citation-grounding-helper, thesis-ops-comparison-builder, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, method-note-builder, citation-grounding-helper, paper-summariser |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-polisher, groupwork-reply, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, groupwork-reply, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-followup-extractor, construction-ops-timeline-builder, construction-ops-handoff-brief-writer, partnerships-ops-timeline-builder |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, reply-polisher, travel-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, email-drafter, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 3 | 3 | `public-office-suspicious-email` | wrong | public-office-suspicious-email, privacy-risk-reviewer, security-threat-modeler, public-security-threat-model, public-addy-agent-security-and-hardening |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-setup-planner, auth-flow-reviewer, public-swebench-security-review, privacy-risk-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, public-oh-my-npm-git-install, public-mattpocock-setup-pre-commit, risk-ops-normalizer, migration-risk-auditor |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 14 | 14 | `webhook-setup-planner` | wrong | webhook-setup-planner, webhook-contract-planner, public-swebench-security-review, public-openai-vercel-deploy, public-swebench-add-admin-api-endpoint |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-quality-auditor, identity-ops-normalizer, identity-ops-summary-writer, identity-ops-evidence-grounder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 2 | 2 | `public-swebench-analytics-events` | wrong | public-swebench-analytics-events, privacy-risk-reviewer, analytics-ops-quality-auditor, public-oh-my-log-analysis, analytics-ops-evidence-grounder |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, public-oh-my-workflow-automation, public-oh-my-aider-cli-workflow, library-ops-dependency-mapper, public-oh-my-git-workflow |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-office-data-analysis` | wrong | public-office-data-analysis, public-xlsx, data-analysis-overview, public-office-xlsx-manipulation, public-swebench-xlsx |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-dependency-mapper, agent-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, sales-ops-field-extractor, document-field-extractor, operations-ops-field-extractor, personal-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, email-polisher, incident-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, paper-summariser, docs-ops-summary-writer, ml-ops-summary-writer, public-office-chat-with-pdf |
