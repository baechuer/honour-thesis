# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (2349 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 80.0% |
| Acceptable top-1 accuracy | 80.0% |
| Top-3 recall | 84.7% |
| Top-5 recall | 84.7% |
| Acceptable top-5 recall | 84.7% |
| MRR | 0.820 |
| Non-main top-1 | 14.1% |
| Approx selector-visible tokens | 619548 |

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
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-acceptance-test-builder, webhook-contract-planner, openapi-contract-reviewer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, events-ops-acceptance-test-builder, events-ops-monitoring-plan-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, public-addy-agent-api-and-interface-design, mobile-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-office-subscription-management, grant-ops-monitoring-plan-builder, customer-success-ops-normalizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, analytics-ops-monitoring-plan-builder, finance-ops-monitoring-plan-builder, analytics-ops-failure-diagnoser, analytics-ops-timeline-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, accessibility-interaction-auditor, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, qa-ops-field-extractor, playwright-flow-debugger, mobile-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `ecommerce-ops-acceptance-test-builder` | wrong | ecommerce-ops-acceptance-test-builder, logistics-ops-acceptance-test-builder, retail-ops-acceptance-test-builder, procurement-ops-acceptance-test-builder, fundraising-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, public-office-competitive-analysis, product-ops-comparison-builder, public-office-table-extractor, public-oh-my-ccpi-marketplace |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `public-swebench-add-admin-api-endpoint` | wrong | public-swebench-add-admin-api-endpoint, api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-ops-normalizer, external-api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 3 | 3 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, web-form-filler, accessibility-checker, support-ticket-triager, public-addy-web-accessibility |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-polisher` | wrong | email-polisher, email-drafter, reply-drafter, professor-email-reply, email-thread-summariser |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `external-api-integration-planner` | wrong | external-api-integration-planner, pr-reviewer, database-migration-risk-assessor, auth-flow-reviewer, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, external-api-integration-planner, code-reviewer, public-swebench-python-resilience |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, web-ui-tester, openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, external-api-integration-planner, auth-flow-reviewer, churn-risk-analyser |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, mobile-ops-timeline-builder, mobile-ops-normalizer, mobile-ops-evidence-grounder, mobile-ops-summary-writer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting, data-analysis-for-root-cause-diagnosis, data-analysis-for-ranking-selection |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, social-ops-quality-auditor, support-ops-quality-auditor, ads-ops-quality-auditor, analytics-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, web-performance-budget-checker, metrics-root-cause-diagnoser, variance-analysis-helper, analytics-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, ads-ops-summary-writer, marketing-ops-summary-writer, support-ops-ops-summary-writer, sre-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, supply-chain-ops-evidence-grounder, news-briefing-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `dashboard-ops-priority-ranker` | wrong | dashboard-ops-priority-ranker, travel-ops-priority-ranker, risk-ops-priority-ranker, meeting-ops-priority-ranker, risk-ops-scenario-planner |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, receipt-extractor, ecommerce-ops-compliance-checker |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, public-office-subscription-management, mobile-ops-comparison-builder, public-office-competitive-analysis, public-office-dcf-valuation |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, web-form-filler, customer-success-ops-normalizer, public-addy-web-accessibility |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, frontend-debugger, secret-leak-scanner, public-openai-vercel-deploy |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, release-note-writer, public-oh-my-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-summary-writer, mobile-ops-evidence-grounder, mobile-ops-normalizer, public-addy-web-performance |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-normalizer, travel-ops-handoff-brief-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 6 | `reply-polisher` | wrong | reply-polisher, travel-ops-summary-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-handoff-brief-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, travel-ops-normalizer, travel-ops-rewrite-editor, facilities-ops-normalizer, travel-ops-risk-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 15 | 15 | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, vendor-ops-field-extractor, procurement-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, privacy-policy-drafter, insurance-ops-comparison-builder, publishing-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, citation-note-extractor, public-office-form-builder, research-ops-risk-reviewer, public-office-pdf-form-filler |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `procurement-ops-field-extractor` | wrong | procurement-ops-field-extractor, medical-admin-ops-field-extractor, facilities-ops-field-extractor, risk-ops-field-extractor, academic-admin-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, public-mattpocock-triage, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, web-performance-budget-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, service-dependency-mapper, risk-ops-risk-reviewer, sre-ops-risk-reviewer, capacity-risk-forecaster |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, supply-chain-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, capacity-risk-forecaster |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, metrics-overview, incident-ops-handoff-brief-writer, service-dependency-mapper |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, tech-news-trend-extractor, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, events-ops-monitoring-plan-builder, events-ops-handoff-brief-writer, metrics-overview |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, retail-ops-evidence-grounder, supply-chain-ops-evidence-grounder, customer-success-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, mobile-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, grant-ops-field-extractor, grant-ops-quality-auditor, grant-ops-normalizer, grant-ops-summary-writer |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, receipt-extractor, public-office-pdf-ocr, vendor-ops-rewrite-editor, finance-ops-rewrite-editor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, vendor-ops-rewrite-editor, vendor-ops-handoff-brief-writer, vendor-ops-risk-reviewer, vendor-ops-normalizer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, procurement-risk-summariser, risk-ops-scenario-planner, public-office-dcf-valuation, fundraising-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, slide-outline-builder, deck-template-applier, public-pptx, thesis-ops-rewrite-editor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `repo-ops-handoff-brief-writer` | wrong | repo-ops-handoff-brief-writer, construction-ops-comparison-builder, construction-ops-normalizer, construction-ops-handoff-brief-writer, construction-ops-summary-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-followup-extractor, meeting-ops-scenario-planner, meeting-summary-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-scheduler |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, incident-summary-writer, meeting-ops-field-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-field-extractor, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-agenda-builder, meeting-scheduler, meeting-ops-timeline-builder, meeting-ops-acceptance-test-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, method-note-builder, thesis-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, energy-ops-summary-writer, construction-ops-summary-writer, facilities-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, speaker-notes-writer, citation-grounding-helper, public-mattpocock-obsidian-vault |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, incident-ops-field-extractor, course-ops-field-extractor, lab-ops-field-extractor, social-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, thesis-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, support-ops-evidence-grounder, support-ops-ops-evidence-grounder, agent-eval-coverage-auditor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, method-note-builder, thesis-ops-comparison-builder, database-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ml-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, document-rewriter, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, meeting-followup-extractor, reply-drafter, meeting-ops-handoff-brief-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, reply-polisher, groupwork-reply, travel-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-office-suspicious-email, public-addy-agent-security-and-hardening, public-security-threat-model, privacy-risk-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, webhook-contract-planner, webhook-setup-planner, public-swebench-security-review, privacy-risk-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, public-oh-my-npm-git-install, database-migration-risk-assessor, risk-ops-artifact-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, webhook-contract-planner, public-openai-vercel-deploy, environment-config-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-evidence-grounder, identity-ops-normalizer, identity-ops-summary-writer, data-analysis-with-validation |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 2 | 2 | `public-swebench-analytics-events` | wrong | public-swebench-analytics-events, privacy-risk-reviewer, data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, library-ops-dependency-mapper, meeting-ops-comparison-builder, library-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, public-office-data-analysis, data-analysis-for-reporting, library-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, skill-finder, agent-ops-handoff-brief-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, agent-ops-field-extractor, sales-ops-field-extractor, hr-ops-field-extractor, operations-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | - | - | `public-oh-my-git-guardrails-claude-code` | wrong | public-oh-my-git-guardrails-claude-code, public-oh-my-notebooklm, public-anthropic-skill-creator, public-oh-my-agentic-skills, public-oh-my-improve-codebase-architecture |
