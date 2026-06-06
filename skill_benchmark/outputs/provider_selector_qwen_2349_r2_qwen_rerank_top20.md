# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (2349 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 65.9% |
| Acceptable top-1 accuracy | 68.2% |
| Top-3 recall | 70.6% |
| Top-5 recall | 70.6% |
| Acceptable top-5 recall | 72.9% |
| MRR | 0.682 |
| Non-main top-1 | 27.1% |
| Approx selector-visible tokens | 1184372 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2434
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 83
- Rerank cache hits: 2
- Approx uncached rerank input tokens: 564824

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, api-ops-quality-auditor, public-office-subscription-management |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, public-swebench-security-review, public-office-subscription-management, api-ops-timeline-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-acceptance-test-builder, external-api-integration-planner, invoice-payment-checker |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, service-dependency-mapper, database-ops-dependency-mapper, api-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-office-subscription-management, public-addy-agent-deprecation-and-migration, customer-success-ops-normalizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, analytics-ops-timeline-builder, finance-ops-monitoring-plan-builder, analytics-ops-compliance-checker, ads-ops-monitoring-plan-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, frontend-debugger, public-anthropic-webapp-testing, dashboard-ops-quality-auditor, web-ui-tester |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-n-skills-dev-browser, public-oh-my-agent-browser, public-office-browser-automation, public-anthropic-webapp-testing |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `ecommerce-ops-acceptance-test-builder` | wrong | ecommerce-ops-acceptance-test-builder, ecommerce-ops-quality-auditor, retail-ops-acceptance-test-builder, logistics-ops-acceptance-test-builder, procurement-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `public-office-shopify-automation` | wrong | public-office-shopify-automation, public-office-table-extractor, public-oh-my-react-grab, public-office-amazon-seller, public-oh-my-to-prd |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `public-oh-my-state-management` | wrong | public-oh-my-state-management, public-oh-my-standup-meeting, public-office-cv-builder, public-oh-my-obsidian-cli-uri-fallback, public-oh-my-game-performance-profiler |
| `web_p6_accessibility_check` | `accessibility-checker` | 3 | 3 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, public-addy-web-accessibility, accessibility-checker, public-oh-my-web-accessibility, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-ops-normalizer` | wrong | email-ops-normalizer, social-ops-normalizer, personal-ops-normalizer, community-ops-normalizer, email-ops-dependency-mapper |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `public-addy-agent-deprecation-and-migration` | wrong | public-addy-agent-deprecation-and-migration, migration-risk-auditor, public-swebench-security-review, security-code-reviewer, api-ops-quality-auditor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, public-openai-gh-address-comments, api-integration-planner, public-swebench-python-resilience, public-mattpocock-review |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `public-oh-my-authentication-setup` | wrong | public-oh-my-authentication-setup, public-openai-gh-address-comments, public-mattpocock-setup-pre-commit, public-mattpocock-triage, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-oh-my-changelog-maintenance, public-openai-gh-fix-ci, public-addy-agent-deprecation-and-migration |
| `code_p6_release_notes` | `release-note-writer` | - | - | `public-oh-my-firebase-cli` | wrong | public-oh-my-firebase-cli, mobile-ops-summary-writer, mobile-ops-rewrite-editor, public-addy-web-performance, customer-success-ops-summary-writer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-reporting, data-analysis-for-root-cause-diagnosis, dataset-ops-summary-writer, public-office-data-analysis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, analytics-ops-monitoring-plan-builder, data-analysis-overview, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `analytics-ops-quality-auditor` | wrong | analytics-ops-quality-auditor, data-analysis-with-validation, data-analysis-with-anomaly-focus, ads-ops-quality-auditor, social-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, marketing-ops-evidence-grounder, marketing-ops-quality-auditor, analytics-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, analytics-ops-summary-writer, marketing-ops-summary-writer, ads-ops-summary-writer, energy-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, public-oh-my-pattern-detection, data-analysis-overview |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `analytics-ops-priority-ranker` | wrong | analytics-ops-priority-ranker, events-ops-priority-ranker, meeting-ops-priority-ranker, api-ops-priority-ranker, training-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, ecommerce-ops-evidence-grounder, web-form-filler, ecommerce-ops-acceptance-test-builder |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, ads-ops-comparison-builder, product-ops-comparison-builder, mobile-ops-comparison-builder, public-oh-my-to-prd |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, public-addy-web-accessibility, ads-ops-quality-auditor, customer-success-ops-quality-auditor, community-ops-quality-auditor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, environment-config-auditor, public-oh-my-game-build-log-triage, public-openai-cloudflare-deploy |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-anthropic-webapp-testing, public-openai-cloudflare-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, public-addy-web-web-quality-audit, mobile-ops-quality-auditor |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-field-extractor` | wrong | travel-ops-field-extractor, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-priority-ranker, travel-ops-normalizer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-summary-writer, travel-ops-quality-auditor, travel-ops-artifact-packager, travel-ops-timeline-builder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-field-extractor, operations-ops-normalizer, travel-ops-quality-auditor, travel-ops-rewrite-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `supply-chain-ops-field-extractor` | wrong | supply-chain-ops-field-extractor, procurement-ops-field-extractor, vendor-ops-field-extractor, receipt-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, legal-ops-rewrite-editor, legal-ops-quality-auditor, privacy-policy-drafter, legal-ops-summary-writer |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, public-office-form-builder, procurement-ops-field-extractor, public-office-meeting-notes, risk-ops-field-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `public-office-form-builder` | wrong | public-office-form-builder, platform-ops-field-extractor, academic-admin-ops-field-extractor, procurement-ops-field-extractor, customer-success-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, public-oh-my-triage, support-ticket-triager, slo-breach-checker |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, analytics-ops-quality-auditor, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, analytics-ops-risk-reviewer, incident-ops-risk-reviewer, platform-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, sre-ops-risk-reviewer, analytics-ops-risk-reviewer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, debugging-root-cause-helper, cloud-ops-failure-diagnoser, analytics-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, incident-ops-summary-writer, incident-ops-field-extractor, incident-ops-handoff-brief-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, journalism-ops-summary-writer, general-source-summariser, media-ops-summary-writer, fundraising-ops-summary-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, news-summariser, events-ops-summary-writer, journalism-ops-monitoring-plan-builder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, retail-ops-evidence-grounder, sales-ops-evidence-grounder, content-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, source-grounding-extractor, news-briefing-writer |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, iot-ops-evidence-grounder, public-oh-my-pattern-detection |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-quality-auditor` | wrong | grant-ops-quality-auditor, grant-ops-compliance-checker, grant-ops-risk-reviewer, grant-ops-acceptance-test-builder, grant-ops-artifact-packager |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-ocr, receipt-extractor, public-office-expense-tracker, public-office-invoice-organizer |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-artifact-packager, vendor-ops-acceptance-test-builder, vendor-ops-quality-auditor, vendor-ops-evidence-grounder |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, financial-model-builder, public-office-financial-modeling, public-swebench-creating-financial-models, finance-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, public-office-ppt-visual, speaker-notes-writer, deck-template-applier |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `repo-ops-handoff-brief-writer` | wrong | repo-ops-handoff-brief-writer, engineering-design-ops-handoff-brief-writer, energy-ops-handoff-brief-writer, research-ops-handoff-brief-writer, construction-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-timeline-builder, meeting-ops-dependency-mapper, meeting-ops-scenario-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-followup-extractor, public-office-meeting-notes, meeting-ops-timeline-builder |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, task-extractor, meeting-ops-field-extractor, meeting-ops-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-followup-extractor, meeting-ops-normalizer, meeting-ops-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-ops-timeline-builder, meeting-scheduler, public-addy-agent-planning-and-task-breakdown, agent-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, general-source-summariser, search-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, journalism-ops-summary-writer, sre-ops-summary-writer, energy-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, document-extractor, research-ops-summary-writer, public-openai-notion-research-documentation |
| `read_p4_document_extraction` | `document-extractor` | - | - | `sre-ops-field-extractor` | wrong | sre-ops-field-extractor, dataset-ops-field-extractor, incident-ops-field-extractor, events-ops-field-extractor, supply-chain-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, thesis-ops-evidence-grounder, research-ops-evidence-grounder, lab-ops-evidence-grounder, research-ops-acceptance-test-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, writing-ops-evidence-grounder, research-ops-evidence-grounder, agent-ops-rewrite-editor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, bioinformatics-ops-comparison-builder, research-ops-comparison-builder, journalism-ops-comparison-builder, environmental-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, method-note-builder, general-source-summariser, note-linker |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, email-drafter, followup-reply-writer, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `email-polisher` | wrong | email-polisher, reply-polisher, document-rewriter, reply-drafter, support-ops-rewrite-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, deadline-reminder-planner, meeting-ops-handoff-brief-writer, task-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, agent-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, personal-ops-handoff-brief-writer, grant-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, email-ops-handoff-brief-writer, followup-reply-writer, email-drafter, public-office-email-drafter |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, auth-flow-reviewer, public-swebench-security-review, privacy-risk-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, public-swebench-security-review, public-addy-agent-security-and-hardening, api-ops-risk-reviewer, api-ops-evidence-grounder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, risk-ops-artifact-packager, media-ops-risk-reviewer, public-oh-my-npm-git-install |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, public-swebench-security-review, public-openai-vercel-deploy, public-oh-my-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-risk-reviewer, identity-ops-compliance-checker, identity-ops-priority-ranker, identity-ops-comparison-builder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 9 | 9 | `public-swebench-analytics-events` | wrong | public-swebench-analytics-events, analytics-ops-evidence-grounder, analytics-ops-risk-reviewer, search-ops-summary-writer, public-oh-my-log-analysis |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, public-oh-my-workflow-automation, task-extractor, public-oh-my-aider-cli-workflow, public-oh-my-skill-autoresearch |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, public-office-data-analysis, public-office-sheets-automation, public-office-excel-automation |
| `skill_p3_create_new` | `skill-creator` | - | - | `task-extractor` | wrong | task-extractor, thesis-ops-dependency-mapper, thesis-ops-summary-writer, thesis-ops-handoff-brief-writer, personal-ops-summary-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `operations-ops-field-extractor` | wrong | operations-ops-field-extractor, agent-ops-field-extractor, product-ops-field-extractor, docs-ops-field-extractor, hr-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, professor-email-reply, reply-drafter, email-polisher, groupwork-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, public-huggingface-huggingface-papers, research-ops-summary-writer, document-summariser, public-oh-my-notebooklm |
