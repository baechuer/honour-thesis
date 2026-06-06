# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (2349 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 69.4% |
| Acceptable top-1 accuracy | 70.6% |
| Top-3 recall | 74.1% |
| Top-5 recall | 74.1% |
| Acceptable top-5 recall | 76.5% |
| MRR | 0.719 |
| Non-main top-1 | 21.2% |
| Approx selector-visible tokens | 120024 |

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
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, openapi-contract-tester, api-design-reviewer, api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-acceptance-test-builder, api-design-reviewer, api-ops-monitoring-plan-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, events-ops-monitoring-plan-builder, email-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, public-architecture-patterns, public-addy-agent-api-and-interface-design, database-ops-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, public-office-subscription-management, public-addy-agent-deprecation-and-migration, database-ops-monitoring-plan-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, analytics-ops-failure-diagnoser, analytics-ops-monitoring-plan-builder, support-ops-failure-diagnoser, analytics-ops-timeline-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, terms-of-service-drafter, finance-ops-acceptance-test-builder, social-ops-acceptance-test-builder, academic-admin-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, playwright-flow-debugger, web-ops-field-extractor, web-ui-tester, public-n-skills-dev-browser |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `logistics-ops-acceptance-test-builder` | wrong | logistics-ops-acceptance-test-builder, ecommerce-ops-acceptance-test-builder, customer-success-ops-acceptance-test-builder, retail-ops-acceptance-test-builder, procurement-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-comparison-builder` | wrong | product-ops-comparison-builder, product-ops-priority-ranker, product-ops-resource-linker, product-ops-handoff-brief-writer, product-ops-rewrite-editor |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-timeline-builder` | wrong | api-ops-timeline-builder, api-integration-planner, identity-ops-timeline-builder, api-ops-rewrite-editor, api-ops-handoff-brief-writer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, knowledge-base-article-writer, public-addy-web-accessibility, terms-of-service-drafter, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `professor-email-reply` | wrong | professor-email-reply, email-polisher, git-commit-writer, email-drafter, email-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `external-api-integration-planner` | wrong | external-api-integration-planner, database-migration-risk-assessor, openapi-contract-reviewer, api-design-reviewer, public-swebench-add-admin-api-endpoint |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, public-mattpocock-review, external-api-integration-planner, api-integration-planner, pr-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `openapi-contract-reviewer` | wrong | openapi-contract-reviewer, openapi-contract-tester, auth-flow-reviewer, git-commit-writer, external-api-integration-planner |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, external-api-integration-planner, public-addy-agent-deprecation-and-migration, public-addy-agent-incremental-implementation, api-integration-planner |
| `code_p6_release_notes` | `release-note-writer` | - | - | `debugging-root-cause-helper` | wrong | debugging-root-cause-helper, mobile-ops-timeline-builder, public-addy-agent-incremental-implementation, meeting-scheduler, sre-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-forecasting` | wrong | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-reporting, financial-report-writer, data-analysis-with-anomaly-focus |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, real-estate-ops-monitoring-plan-builder, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, ads-ops-quality-auditor, support-ops-quality-auditor, analytics-ops-quality-auditor, email-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, web-performance-budget-checker, ads-ops-failure-diagnoser, analytics-ops-evidence-grounder, ads-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, customer-success-ops-summary-writer, support-ops-summary-writer, support-ops-ops-summary-writer, ads-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, supply-chain-ops-evidence-grounder, data-analysis-for-root-cause-diagnosis, support-ops-evidence-grounder, support-ops-ops-evidence-grounder |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `risk-ops-priority-ranker` | wrong | risk-ops-priority-ranker, travel-ops-priority-ranker, compliance-ops-priority-ranker, api-ops-priority-ranker, meeting-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, receipt-extractor, invoice-payment-checker, ecommerce-ops-compliance-checker, retail-ops-compliance-checker |
| `deploy_p2_visual_regression` | `visual-regression-checker` | - | - | `mobile-ops-rewrite-editor` | wrong | mobile-ops-rewrite-editor, terms-of-service-drafter, privacy-policy-drafter, proposal-drafter, mobile-ops-comparison-builder |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, public-addy-web-accessibility, identity-ops-rewrite-editor, privacy-ops-rewrite-editor, finance-ops-rewrite-editor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, public-oh-my-game-build-log-triage, public-oh-my-vercel-deploy, environment-config-auditor |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-addy-agent-shipping-and-launch, public-openai-vercel-deploy, public-oh-my-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, public-addy-agent-performance-optimization, mobile-ops-summary-writer, mobile-ops-evidence-grounder, public-addy-web-core-web-vitals |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-handoff-brief-writer, public-anthropic-internal-comms |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 2 | `hr-ops-handoff-brief-writer` | wrong | hr-ops-handoff-brief-writer, travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, speaker-notes-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-rewrite-editor` | wrong | travel-ops-rewrite-editor, travel-ops-normalizer, meeting-ops-normalizer, travel-ops-risk-reviewer, travel-ops-intake-classifier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, vendor-ops-field-extractor, procurement-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, compliance-ops-comparison-builder, support-ops-ops-comparison-builder, academic-admin-ops-comparison-builder, meeting-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-intake-classifier, research-ops-risk-reviewer, citation-note-extractor, procurement-risk-summariser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `grant-ops-field-extractor` | wrong | grant-ops-field-extractor, incident-ops-field-extractor, research-ops-field-extractor, support-ops-field-extractor, compliance-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, public-oh-my-triage, public-mattpocock-triage, support-ticket-triager |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, data-analysis-with-anomaly-focus, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 7 | 7 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, risk-ops-compliance-checker, incident-ops-risk-reviewer, procurement-risk-summariser, risk-ops-acceptance-test-builder |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, procurement-risk-summariser, risk-ops-failure-diagnoser, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, sre-ops-failure-diagnoser, analytics-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-intake-classifier, incident-ops-handoff-brief-writer, incident-ops-failure-diagnoser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, journalism-ops-summary-writer, paper-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, events-ops-monitoring-plan-builder, events-ops-handoff-brief-writer, events-ops-evidence-grounder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, supply-chain-ops-evidence-grounder, customer-success-ops-evidence-grounder, retail-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, journalism-ops-evidence-grounder, news-summariser |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, grant-ops-field-extractor, grant-ops-quality-auditor, public-office-pdf-form-filler, grant-ops-compliance-checker |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, receipt-extractor, public-office-pdf-ocr, procurement-ops-rewrite-editor, vendor-ops-rewrite-editor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, vendor-ops-rewrite-editor, vendor-ops-risk-reviewer, vendor-ops-compliance-checker, vendor-ops-handoff-brief-writer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, procurement-risk-summariser, financial-model-builder, procurement-ops-summary-writer, public-office-dcf-valuation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, deck-template-applier, slide-outline-builder, public-office-ai-slides, public-pptx |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | - | - | `repo-ops-handoff-brief-writer` | wrong | repo-ops-handoff-brief-writer, construction-ops-summary-writer, construction-ops-comparison-builder, construction-ops-handoff-brief-writer, construction-ops-normalizer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-summary-writer, meeting-followup-extractor, meeting-ops-intake-classifier |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-scheduler, meeting-followup-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-handoff-brief-writer, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, task-extractor, meeting-summary-writer, meeting-followup-extractor, speaker-notes-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, meeting-scheduler, meeting-summary-writer, meeting-ops-summary-writer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, method-note-builder, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, facilities-ops-summary-writer, ecommerce-ops-summary-writer, retail-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, speaker-notes-writer, research-ops-evidence-grounder, writing-ops-evidence-grounder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `incident-ops-field-extractor` | wrong | incident-ops-field-extractor, facilities-ops-field-extractor, research-ops-field-extractor, lab-ops-field-extractor, compliance-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, multi-source-comparison-builder, thesis-ops-handoff-brief-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, support-ops-ops-evidence-grounder, agent-eval-coverage-auditor, support-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder, knowledge-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ml-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-drafter, reply-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, meeting-scheduler, email-polisher, facilities-ops-handoff-brief-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-followup-extractor, meeting-ops-handoff-brief-writer, construction-ops-handoff-brief-writer, meeting-summary-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, retail-ops-handoff-brief-writer, travel-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer, thesis-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, public-office-suspicious-email, public-addy-agent-security-and-hardening, public-openai-security-ownership-map |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `api-design-reviewer` | wrong | api-design-reviewer, public-addy-agent-security-and-hardening, api-ops-compliance-checker, identity-ops-compliance-checker, api-integration-planner |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, risk-ops-artifact-packager, migration-risk-auditor, risk-ops-normalizer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `webhook-setup-planner` | wrong | webhook-setup-planner, webhook-contract-planner, database-migration-risk-assessor, environment-config-auditor, public-openai-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, identity-ops-compliance-checker, policy-compliance-checker, identity-ops-monitoring-plan-builder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `search-ops-monitoring-plan-builder` | wrong | search-ops-monitoring-plan-builder, data-analysis-with-anomaly-focus, public-swebench-analytics-events, analytics-ops-monitoring-plan-builder, search-ops-quality-auditor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-ops-comparison-builder, meeting-agenda-builder, meeting-ops-evidence-grounder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, public-swebench-xlsx, data-analysis-for-reporting, public-office-data-analysis, financial-report-writer |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, public-anthropic-skill-creator, agent-ops-handoff-brief-writer, meeting-followup-extractor |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, agent-ops-field-extractor, knowledge-ops-field-extractor, hr-ops-field-extractor, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, skill-evaluator, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, public-anthropic-skill-creator, agent-ops-resource-linker, agent-ops-summary-writer, paper-summariser |
