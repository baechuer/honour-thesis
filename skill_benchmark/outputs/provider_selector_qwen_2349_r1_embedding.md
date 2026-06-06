# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (2349 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 35.3% |
| Acceptable top-1 accuracy | 36.5% |
| Top-3 recall | 44.7% |
| Top-5 recall | 48.2% |
| Acceptable top-5 recall | 50.6% |
| MRR | 0.426 |
| Non-main top-1 | 50.6% |
| Approx selector-visible tokens | 120024 |

## API Usage Estimate

- Embedding API calls made in this run: 135
- Embedding cache hits: 1091
- Approx uncached embedding input tokens: 69437
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester, api-integration-planner, api-design-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 1 | `api-integration-planner` | acceptable | api-integration-planner, external-api-integration-planner, api-design-reviewer, api-ops-timeline-builder, invoice-payment-checker |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-monitoring-plan-builder, public-office-stripe-payments, receipt-extractor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-addy-agent-api-and-interface-design, public-architecture-patterns, external-api-integration-planner |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 5 | 5 | `public-office-subscription-management` | wrong | public-office-subscription-management, public-addy-agent-deprecation-and-migration, database-ops-monitoring-plan-builder, publishing-ops-monitoring-plan-builder, database-migration-risk-assessor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 15 | 15 | `analytics-ops-monitoring-plan-builder` | wrong | analytics-ops-monitoring-plan-builder, analytics-ops-failure-diagnoser, api-ops-monitoring-plan-builder, email-ops-monitoring-plan-builder, support-ops-monitoring-plan-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 6 | 6 | `public-oh-my-authentication-setup` | wrong | public-oh-my-authentication-setup, terms-of-service-drafter, social-ops-acceptance-test-builder, academic-admin-ops-acceptance-test-builder, finance-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, playwright-flow-debugger, web-page-snapshotter, public-oh-my-agent-browser, web-ui-tester |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, ecommerce-ops-compliance-checker, logistics-ops-compliance-checker, privacy-ops-compliance-checker, retail-ops-compliance-checker |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `competitive-battlecard-builder` | wrong | competitive-battlecard-builder, product-ops-comparison-builder, public-office-amazon-seller, market-opportunity-assessor, public-office-dcf-valuation |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `identity-ops-timeline-builder` | wrong | identity-ops-timeline-builder, public-mattpocock-to-prd, personal-ops-timeline-builder, identity-ops-rewrite-editor, api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | - | - | `public-addy-web-accessibility` | wrong | public-addy-web-accessibility, knowledge-base-article-writer, public-office-applicant-screening, landing-page-copy-reviewer, terms-of-service-drafter |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `public-mattpocock-to-prd` | wrong | public-mattpocock-to-prd, public-mattpocock-grill-me, email-ops-dependency-mapper, public-addy-agent-interview-me, public-mattpocock-tdd |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `public-swebench-add-admin-api-endpoint` | wrong | public-swebench-add-admin-api-endpoint, public-swebench-add-malli-schemas, external-api-integration-planner, openapi-contract-reviewer, public-addy-agent-deprecation-and-migration |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 6 | 6 | `api-integration-planner` | wrong | api-integration-planner, external-api-integration-planner, public-mattpocock-review, public-swebench-python-resilience, openapi-contract-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `openapi-contract-reviewer` | wrong | openapi-contract-reviewer, public-oh-my-authentication-setup, external-api-integration-planner, public-swebench-add-malli-schemas, openapi-contract-tester |
| `code_p5_changelog_entry` | `changelog-writer` | - | - | `public-addy-agent-deprecation-and-migration` | wrong | public-addy-agent-deprecation-and-migration, external-api-integration-planner, api-integration-planner, public-addy-agent-incremental-implementation, churn-risk-analyser |
| `code_p6_release_notes` | `release-note-writer` | - | - | `mobile-ops-timeline-builder` | wrong | mobile-ops-timeline-builder, public-addy-agent-incremental-implementation, meeting-scheduler, ads-ops-timeline-builder, public-addy-agent-performance-optimization |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-with-validation, data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, analytics-ops-monitoring-plan-builder, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, ecommerce-ops-monitoring-plan-builder |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, data-analysis-with-anomaly-focus, ads-ops-quality-auditor, data-analysis-for-root-cause-diagnosis, journalism-ops-failure-diagnoser |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 11 | 11 | `ads-ops-monitoring-plan-builder` | wrong | ads-ops-monitoring-plan-builder, ads-ops-failure-diagnoser, analytics-ops-monitoring-plan-builder, web-performance-budget-checker, ads-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 14 | 14 | `customer-success-ops-summary-writer` | wrong | customer-success-ops-summary-writer, ecommerce-ops-summary-writer, support-ops-summary-writer, email-ops-summary-writer, supply-chain-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, churn-risk-analyser, contract-ops-summary-writer, market-opportunity-assessor, supply-chain-ops-evidence-grounder |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, compliance-ops-priority-ranker, api-ops-priority-ranker, agent-ops-priority-ranker, privacy-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | - | - | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, ecommerce-ops-compliance-checker, retail-ops-compliance-checker, ecommerce-ops-acceptance-test-builder |
| `deploy_p2_visual_regression` | `visual-regression-checker` | - | - | `landing-page-copy-reviewer` | wrong | landing-page-copy-reviewer, public-office-subscription-management, business-plan-builder, proposal-drafter, mobile-ops-monitoring-plan-builder |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | - | - | `public-addy-web-accessibility` | wrong | public-addy-web-accessibility, identity-ops-rewrite-editor, privacy-ops-rewrite-editor, finance-ops-rewrite-editor, support-ops-ops-rewrite-editor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, public-oh-my-game-build-log-triage, public-swebench-fix, public-oh-my-vercel-deploy |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-release-verifier, public-addy-agent-shipping-and-launch, public-oh-my-vercel-deploy, public-openai-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, public-addy-agent-performance-optimization, public-addy-web-core-web-vitals, mobile-ops-summary-writer, mobile-ops-evidence-grounder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-handoff-brief-writer, public-anthropic-internal-comms, travel-ops-risk-reviewer, travel-ops-intake-classifier |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 3 | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-rewrite-editor, travel-ops-intake-classifier, travel-ops-evidence-grounder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-compliance-checker, travel-ops-intake-classifier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, public-office-invoice-generator, vendor-ops-normalizer, vendor-ops-handoff-brief-writer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 5 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-handoff-brief-writer, meeting-ops-compliance-checker, policy-compliance-checker, legal-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | - | - | `research-ops-intake-classifier` | wrong | research-ops-intake-classifier, procurement-risk-summariser, research-ops-risk-reviewer, research-ops-compliance-checker, risk-ops-handoff-brief-writer |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `procurement-ops-handoff-brief-writer` | wrong | procurement-ops-handoff-brief-writer, facilities-ops-handoff-brief-writer, risk-ops-handoff-brief-writer, public-office-form-builder, compliance-ops-handoff-brief-writer |
| `obs_p1_metrics_overview` | `metrics-overview` | 2 | 2 | `public-oh-my-triage` | wrong | public-oh-my-triage, metrics-overview, support-ticket-triager, medical-admin-ops-failure-diagnoser, cloud-ops-failure-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-root-cause-diagnoser, capacity-risk-forecaster, metrics-overview, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 13 | 13 | `risk-ops-failure-diagnoser` | wrong | risk-ops-failure-diagnoser, incident-ops-risk-reviewer, procurement-risk-summariser, risk-ops-compliance-checker, customer-success-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, sre-ops-failure-diagnoser, risk-ops-failure-diagnoser, support-ops-failure-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, sre-ops-failure-diagnoser, analytics-ops-failure-diagnoser, support-ops-failure-diagnoser, incident-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-intake-classifier, incident-ops-handoff-brief-writer, incident-ops-dependency-mapper |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 10 | 10 | `events-ops-handoff-brief-writer` | wrong | events-ops-handoff-brief-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, journalism-ops-handoff-brief-writer, events-ops-evidence-grounder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 5 | 5 | `product-ops-evidence-grounder` | wrong | product-ops-evidence-grounder, vendor-ops-evidence-grounder, supply-chain-ops-evidence-grounder, meeting-ops-evidence-grounder, source-grounding-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, public-office-news-monitor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, security-ops-evidence-grounder, email-ops-evidence-grounder, journalism-ops-evidence-grounder, analytics-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | - | - | `grant-ops-compliance-checker` | wrong | grant-ops-compliance-checker, grant-ops-normalizer, grant-ops-rewrite-editor, grant-ops-quality-auditor, grant-ops-handoff-brief-writer |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 6 | 6 | `receipt-extractor` | wrong | receipt-extractor, public-office-pdf-ocr, finance-ops-field-extractor, invoice-payment-checker, procurement-ops-field-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | - | - | `vendor-ops-rewrite-editor` | wrong | vendor-ops-rewrite-editor, vendor-ops-risk-reviewer, vendor-ops-compliance-checker, vendor-ops-handoff-brief-writer, vendor-ops-evidence-grounder |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 6 | 6 | `financial-model-builder` | wrong | financial-model-builder, public-office-dcf-valuation, procurement-risk-summariser, public-swebench-creating-financial-models, procurement-ops-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, deck-template-applier, slide-outline-builder, public-office-ai-slides, public-office-dev-slides |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `construction-ops-handoff-brief-writer` | wrong | construction-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, procurement-ops-handoff-brief-writer, manufacturing-ops-handoff-brief-writer, bioinformatics-ops-handoff-brief-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-followup-extractor, meeting-summary-writer, meeting-ops-intake-classifier |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-handoff-brief-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 5 | 5 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, weekly-planner, task-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, public-addy-agent-planning-and-task-breakdown, meeting-summary-writer, agent-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, thesis-ops-summary-writer, research-ops-summary-writer, multi-source-comparison-builder, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, facilities-ops-summary-writer, procurement-ops-summary-writer, ecommerce-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, research-ops-evidence-grounder, citation-grounding-helper, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `incident-ops-field-extractor` | wrong | incident-ops-field-extractor, facilities-ops-field-extractor, research-ops-field-extractor, platform-ops-field-extractor, compliance-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, multi-source-comparison-builder, research-ops-priority-ranker, thesis-ops-evidence-grounder, research-ops-evidence-grounder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 2 | 2 | `agent-ops-evidence-grounder` | wrong | agent-ops-evidence-grounder, citation-grounding-helper, real-estate-ops-evidence-grounder, agent-eval-coverage-auditor, writing-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, thesis-ops-evidence-grounder, research-ops-evidence-grounder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, thesis-ops-handoff-brief-writer, thesis-ops-intake-classifier, email-polisher, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 16 | 16 | `followup-reply-writer` | wrong | followup-reply-writer, facilities-ops-handoff-brief-writer, community-ops-handoff-brief-writer, public-anthropic-internal-comms, meeting-ops-handoff-brief-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-ops-handoff-brief-writer, meeting-followup-extractor, thesis-ops-handoff-brief-writer, construction-ops-handoff-brief-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, retail-ops-handoff-brief-writer, travel-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 2 | 2 | `followup-reply-writer` | wrong | followup-reply-writer, reply-drafter, document-summariser, groupwork-reply, email-drafter |
| `sec_p1_threat_model` | `security-threat-modeler` | 15 | 15 | `public-security-threat-model` | wrong | public-security-threat-model, public-office-suspicious-email, public-addy-agent-security-and-hardening, public-openai-security-ownership-map, security-ops-resource-linker |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `public-addy-agent-security-and-hardening` | wrong | public-addy-agent-security-and-hardening, public-swebench-add-malli-schemas, public-swebench-add-admin-api-endpoint, public-swebench-security-review, api-integration-planner |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 8 | 8 | `public-oh-my-npm-git-install` | wrong | public-oh-my-npm-git-install, migration-risk-auditor, risk-ops-normalizer, risk-ops-artifact-packager, risk-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `webhook-setup-planner` | wrong | webhook-setup-planner, public-office-webhook-automation, public-swebench-security-review, public-openai-vercel-deploy, logistics-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-compliance-checker, identity-ops-quality-auditor, identity-ops-monitoring-plan-builder, identity-ops-failure-diagnoser |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `search-ops-monitoring-plan-builder` | wrong | search-ops-monitoring-plan-builder, analytics-ops-quality-auditor, analytics-ops-monitoring-plan-builder, analytics-ops-evidence-grounder, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 6 | 6 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-ops-failure-diagnoser, engineering-design-ops-summary-writer, public-openai-define-goal, meeting-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-with-validation, spreadsheet-formula-auditor, data-analysis-for-forecasting |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, public-anthropic-skill-creator, public-openai-define-goal, agent-ops-handoff-brief-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, document-summariser, knowledge-ops-field-extractor, document-extractor, sales-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 9 | 9 | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, email-polisher, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, agent-ops-summary-writer, document-summariser, public-anthropic-skill-creator, knowledge-ops-summary-writer |
