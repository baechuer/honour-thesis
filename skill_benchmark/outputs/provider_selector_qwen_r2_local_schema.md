# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 64.2% |
| Acceptable top-1 accuracy | 65.7% |
| Top-3 recall | 73.1% |
| Top-5 recall | 73.1% |
| Acceptable top-5 recall | 74.6% |
| MRR | 0.687 |
| Non-main top-1 | 22.4% |
| Approx selector-visible tokens | 303223 |

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
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, dashboard-ops-acceptance-test-builder, terms-of-service-drafter |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, ux-ops-field-extractor, crm-ops-quality-auditor, medical-admin-ops-quality-auditor |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `email-ops-acceptance-test-builder` | wrong | email-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder, travel-ops-acceptance-test-builder, events-ops-acceptance-test-builder, support-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-comparison-builder, product-ops-scenario-planner, product-ops-priority-ranker, product-ops-handoff-brief-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-handoff-brief-writer` | wrong | api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-ops-normalizer, personal-ops-handoff-brief-writer, personal-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `web-form-filler` | wrong | web-form-filler, accessibility-checker, support-ticket-triager, webhook-setup-planner, terms-of-service-drafter |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, reply-drafter, professor-email-reply, email-thread-summariser |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, migration-risk-auditor, api-ops-acceptance-test-builder, openapi-contract-tester, api-integration-planner |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, openapi-contract-tester, api-ops-quality-auditor, api-integration-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, openapi-contract-tester, refactor-planner, api-ops-quality-auditor, secret-leak-scanner |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, churn-risk-analyser, privacy-risk-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, churn-risk-analyser, frontend-debugger, meeting-scheduler, webhook-setup-planner |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, dataset-ops-summary-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, support-ops-quality-auditor, analytics-ops-quality-auditor, community-ops-quality-auditor, media-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, variance-analysis-helper, analytics-ops-evidence-grounder, analytics-ops-summary-writer |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, support-ops-summary-writer, analytics-ops-summary-writer, news-briefing-writer, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, news-briefing-writer, data-analysis-overview |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `dashboard-ops-priority-ranker` | wrong | dashboard-ops-priority-ranker, travel-ops-priority-ranker, meeting-ops-priority-ranker, analytics-ops-priority-ranker, incident-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, travel-ops-quality-auditor, travel-ops-compliance-checker, travel-ops-normalizer, travel-ops-handoff-brief-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-summary-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-handoff-brief-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-rewrite-editor, events-ops-normalizer, meeting-ops-normalizer, travel-ops-quality-auditor |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | 6 | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-field-extractor, finance-ops-field-extractor, contract-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, privacy-policy-drafter, legal-ops-rewrite-editor, terms-of-service-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, citation-note-extractor, research-ops-risk-reviewer, research-ops-intake-classifier, research-ops-compliance-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, operations-ops-field-extractor, ux-ops-field-extractor, travel-ops-field-extractor, personal-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, cloud-monitoring-configurer, incident-summary-writer, capacity-risk-forecaster |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, slo-breach-checker, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, capacity-risk-forecaster, metrics-overview, dashboard-ops-risk-reviewer, analytics-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, analytics-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, metrics-overview, capacity-risk-forecaster, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, metrics-overview, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, tech-news-trend-extractor, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, events-ops-monitoring-plan-builder, events-ops-handoff-brief-writer, events-ops-scenario-planner |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, vendor-ops-evidence-grounder, general-source-summariser, research-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, web-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-risk-reviewer, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-evidence-grounder |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-normalizer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, meeting-agenda-builder, deadline-reminder-planner, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, meeting-scheduler, refactor-planner, meeting-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, operations-ops-summary-writer, research-ops-evidence-grounder, research-ops-risk-reviewer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, speaker-notes-writer, citation-grounding-helper, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `lab-ops-field-extractor` | wrong | lab-ops-field-extractor, research-ops-field-extractor, ml-ops-field-extractor, analytics-ops-field-extractor, dashboard-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, citation-grounding-helper |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, support-ops-evidence-grounder, agent-eval-coverage-auditor, thesis-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, database-ops-comparison-builder, lab-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ml-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, document-rewriter, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, reply-polisher, meeting-agenda-builder |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, reply-drafter, professor-email-reply, email-polisher |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, privacy-risk-reviewer, email-ops-risk-reviewer, public-brainstorming |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `api-ops-risk-reviewer` | wrong | api-ops-risk-reviewer, webhook-setup-planner, privacy-risk-reviewer, api-ops-compliance-checker, security-ops-handoff-brief-writer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, capacity-risk-forecaster, contract-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, environment-config-auditor, database-ops-monitoring-plan-builder, database-ops-handoff-brief-writer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, security-code-reviewer, privacy-risk-reviewer, email-ops-compliance-checker, policy-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-with-anomaly-focus, search-ops-quality-auditor, analytics-ops-summary-writer, analytics-ops-evidence-grounder |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-ops-comparison-builder, skill-creator, repo-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-for-reporting, analytics-ops-artifact-packager, public-pptx, dataset-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, meeting-followup-extractor, agent-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, thesis-ops-timeline-builder |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, operations-ops-field-extractor, hr-ops-field-extractor, agent-ops-field-extractor, personal-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, groupwork-reply, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, public-pdf, paper-summariser, document-summariser, docs-ops-summary-writer |
