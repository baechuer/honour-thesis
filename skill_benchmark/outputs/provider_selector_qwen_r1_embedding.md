# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (1006 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 35.8% |
| Acceptable top-1 accuracy | 35.8% |
| Top-3 recall | 49.2% |
| Top-5 recall | 56.7% |
| Acceptable top-5 recall | 59.7% |
| MRR | 0.449 |
| Non-main top-1 | 43.3% |
| Approx selector-visible tokens | 50587 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 1073
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `web_p1_page_snapshot` | `web-page-snapshotter` | 3 | 3 | `terms-of-service-drafter` | wrong | terms-of-service-drafter, finance-ops-acceptance-test-builder, web-page-snapshotter, meeting-ops-acceptance-test-builder, ux-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-page-snapshotter, web-ui-tester, web-ops-compliance-checker, accessibility-checker |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, data-analysis-with-validation, email-ops-compliance-checker, compliance-checklist-builder, ux-ops-compliance-checker |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `competitive-battlecard-builder` | wrong | competitive-battlecard-builder, product-ops-comparison-builder, market-opportunity-assessor, decision-matrix-builder, proposal-drafter |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-timeline-builder` | wrong | personal-ops-timeline-builder, api-integration-planner, api-ops-timeline-builder, webhook-setup-planner, personal-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | - | - | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, landing-page-copy-reviewer, terms-of-service-drafter, seo-metadata-checker, market-opportunity-assessor |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-ops-dependency-mapper` | wrong | email-ops-dependency-mapper, email-ops-timeline-builder, professor-email-reply, personal-ops-normalizer, email-drafter |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `api-integration-planner` | wrong | api-integration-planner, auth-flow-reviewer, api-design-reviewer, openapi-contract-tester, api-ops-normalizer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 5 | 5 | `api-integration-planner` | wrong | api-integration-planner, webhook-setup-planner, api-design-reviewer, openapi-contract-tester, review-comment-resolver |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `openapi-contract-tester` | wrong | openapi-contract-tester, api-integration-planner, auth-flow-reviewer, public-playwright-interactive, webhook-setup-planner |
| `code_p5_changelog_entry` | `changelog-writer` | 14 | 14 | `api-integration-planner` | wrong | api-integration-planner, churn-risk-analyser, webhook-setup-planner, api-design-reviewer, refactor-planner |
| `code_p6_release_notes` | `release-note-writer` | - | - | `meeting-scheduler` | wrong | meeting-scheduler, churn-risk-analyser, support-ops-timeline-builder, api-ops-timeline-builder, analytics-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 3 | 3 | `data-analysis-with-anomaly-focus` | wrong | data-analysis-with-anomaly-focus, data-analysis-with-validation, data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, analytics-ops-monitoring-plan-builder, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, churn-risk-analyser, analytics-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 4 | 4 | `analytics-ops-monitoring-plan-builder` | wrong | analytics-ops-monitoring-plan-builder, analytics-ops-evidence-grounder, churn-risk-analyser, data-analysis-for-root-cause-diagnosis, analytics-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 5 | 5 | `support-ops-summary-writer` | wrong | support-ops-summary-writer, email-ops-summary-writer, community-ops-summary-writer, contract-ops-summary-writer, data-analysis-for-reporting |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, churn-risk-analyser, contract-ops-summary-writer, market-opportunity-assessor, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, agent-ops-priority-ranker, legal-ops-priority-ranker, api-ops-priority-ranker, meeting-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-intake-classifier, travel-ops-monitoring-plan-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 3 | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-rewrite-editor, travel-ops-intake-classifier, travel-ops-evidence-grounder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-compliance-checker, travel-ops-intake-classifier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-normalizer, vendor-ops-handoff-brief-writer, vendor-ops-evidence-grounder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 5 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-handoff-brief-writer, meeting-ops-compliance-checker, policy-compliance-checker, legal-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 19 | 19 | `research-ops-intake-classifier` | wrong | research-ops-intake-classifier, procurement-risk-summariser, research-ops-risk-reviewer, research-ops-compliance-checker, research-ops-resource-linker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `document-summariser` | wrong | document-summariser, search-ops-handoff-brief-writer, meeting-ops-intake-classifier, research-ops-intake-classifier, support-ops-handoff-brief-writer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, support-ticket-triager, medical-admin-ops-failure-diagnoser, cloud-ops-failure-diagnoser, security-ops-failure-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-root-cause-diagnoser, capacity-risk-forecaster, metrics-overview, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, procurement-risk-summariser, dashboard-ops-risk-reviewer, incident-ops-risk-reviewer, security-ops-failure-diagnoser |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, support-ops-failure-diagnoser, cloud-ops-failure-diagnoser, operations-ops-failure-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, analytics-ops-failure-diagnoser, support-ops-failure-diagnoser, incident-ops-failure-diagnoser, cloud-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-intake-classifier, incident-ops-handoff-brief-writer, incident-ops-dependency-mapper |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 8 | 8 | `events-ops-handoff-brief-writer` | wrong | events-ops-handoff-brief-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, events-ops-evidence-grounder, events-ops-priority-ranker |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 4 | 4 | `product-ops-evidence-grounder` | wrong | product-ops-evidence-grounder, vendor-ops-evidence-grounder, meeting-ops-evidence-grounder, source-grounding-extractor, research-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, general-source-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, security-ops-evidence-grounder, email-ops-evidence-grounder, analytics-ops-evidence-grounder, legal-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, weekly-planner, meeting-followup-extractor, meeting-summary-writer, meeting-ops-intake-classifier |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-handoff-brief-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 7 | 7 | `weekly-planner` | wrong | weekly-planner, deadline-reminder-planner, meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, meeting-summary-writer, task-extractor, public-writing-plans |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, multi-source-comparison-builder, thesis-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, research-ops-evidence-grounder, research-ops-priority-ranker, operations-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, research-ops-evidence-grounder, citation-grounding-helper, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `incident-ops-field-extractor` | wrong | incident-ops-field-extractor, research-ops-field-extractor, events-ops-field-extractor, lab-ops-field-extractor, meeting-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, multi-source-comparison-builder, research-ops-priority-ranker, thesis-ops-evidence-grounder, research-ops-evidence-grounder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 2 | 2 | `agent-ops-evidence-grounder` | wrong | agent-ops-evidence-grounder, citation-grounding-helper, agent-eval-coverage-auditor, writing-ops-evidence-grounder, thesis-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, thesis-ops-evidence-grounder, research-ops-evidence-grounder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, thesis-ops-handoff-brief-writer, thesis-ops-intake-classifier, email-polisher, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 8 | 8 | `followup-reply-writer` | wrong | followup-reply-writer, community-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, meeting-ops-rewrite-editor, meeting-scheduler |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-summary-writer, meeting-followup-extractor, meeting-ops-handoff-brief-writer, speaker-notes-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, proposal-drafter, thesis-ops-handoff-brief-writer, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 2 | 2 | `followup-reply-writer` | wrong | followup-reply-writer, reply-drafter, professor-email-reply, groupwork-reply, reply-polisher |
| `sec_p1_threat_model` | `security-threat-modeler` | 7 | 7 | `public-security-threat-model` | wrong | public-security-threat-model, security-ops-resource-linker, email-ops-resource-linker, incident-ops-resource-linker, public-brainstorming |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `api-integration-planner` | wrong | api-integration-planner, webhook-setup-planner, api-design-reviewer, openapi-contract-tester, incident-ops-handoff-brief-writer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 2 | 2 | `migration-risk-auditor` | wrong | migration-risk-auditor, dependency-risk-auditor, contract-ops-dependency-mapper, contract-ops-normalizer, web-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `webhook-setup-planner` | wrong | webhook-setup-planner, environment-config-auditor, database-ops-monitoring-plan-builder, events-ops-monitoring-plan-builder, contract-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, policy-compliance-checker, database-ops-compliance-checker, analytics-ops-compliance-checker, api-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `search-ops-monitoring-plan-builder` | wrong | search-ops-monitoring-plan-builder, analytics-ops-quality-auditor, analytics-ops-monitoring-plan-builder, analytics-ops-evidence-grounder, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 4 | 4 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-ops-failure-diagnoser, meeting-ops-comparison-builder, skill-finder, meeting-ops-evidence-grounder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-with-validation, data-analysis-for-forecasting, data-analysis-for-reporting |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, agent-ops-handoff-brief-writer, knowledge-ops-handoff-brief-writer, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, document-summariser, knowledge-ops-field-extractor, document-extractor, agent-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 8 | 8 | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, email-polisher, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, agent-ops-summary-writer, document-summariser, knowledge-ops-summary-writer, legal-ops-summary-writer |
