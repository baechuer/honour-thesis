# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 46.3% |
| Acceptable top-1 accuracy | 47.8% |
| Top-3 recall | 65.7% |
| Top-5 recall | 71.6% |
| Acceptable top-5 recall | 74.6% |
| MRR | 0.574 |
| Non-main top-1 | 29.8% |
| Approx selector-visible tokens | 497146 |

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
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, web-form-filler, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, web-ops-field-extractor, web-ops-handoff-brief-writer, web-ops-normalizer |
| `web_p3_ui_test` | `web-ui-tester` | 5 | 5 | `invoice-payment-checker` | wrong | invoice-payment-checker, web-form-filler, web-ops-compliance-checker, travel-ops-compliance-checker, web-ui-tester |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-comparison-builder, vendor-ops-scenario-planner, accessibility-checker, vendor-ops-priority-ranker |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-normalizer` | wrong | personal-ops-normalizer, personal-ops-rewrite-editor, personal-ops-handoff-brief-writer, personal-ops-artifact-packager, privacy-policy-drafter |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `web-form-filler` | wrong | web-form-filler, accessibility-checker, email-drafter, web-ui-tester, events-ops-normalizer |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-ops-normalizer, personal-ops-normalizer, email-ops-dependency-mapper, reply-polisher |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-rewrite-editor, api-ops-quality-auditor, api-ops-normalizer, api-ops-compliance-checker |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `api-ops-monitoring-plan-builder` | wrong | api-ops-monitoring-plan-builder, api-ops-quality-auditor, api-ops-rewrite-editor, api-ops-failure-diagnoser, api-integration-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-rewrite-editor, api-ops-quality-auditor, api-integration-planner, api-ops-evidence-grounder |
| `code_p5_changelog_entry` | `changelog-writer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, churn-risk-analyser, privacy-risk-reviewer, release-note-writer, changelog-writer |
| `code_p6_release_notes` | `release-note-writer` | 6 | 6 | `churn-risk-analyser` | wrong | churn-risk-analyser, auth-flow-reviewer, api-ops-timeline-builder, api-ops-rewrite-editor, frontend-debugger |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, data-analysis-with-anomaly-focus, data-analysis-for-reporting |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 4 | 4 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-with-validation, data-analysis-for-reporting |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, data-analysis-overview, churn-risk-analyser, analytics-ops-failure-diagnoser, analytics-ops-monitoring-plan-builder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, data-analysis-for-reporting, data-analysis-for-root-cause-diagnosis, analytics-ops-summary-writer, media-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, priority-sorter, meeting-ops-priority-ranker, events-ops-priority-ranker, product-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-handoff-brief-writer, travel-ops-monitoring-plan-builder, travel-ops-rewrite-editor, travel-ops-normalizer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-normalizer, travel-ops-summary-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-handoff-brief-writer, travel-ops-rewrite-editor, travel-ops-compliance-checker, travel-ops-risk-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-normalizer, finance-ops-normalizer, vendor-ops-timeline-builder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 3 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-rewrite-editor, legal-ops-comparison-builder, legal-ops-artifact-packager, legal-ops-handoff-brief-writer |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-risk-reviewer, research-ops-artifact-packager, research-ops-intake-classifier, research-ops-handoff-brief-writer |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, email-drafter, web-form-filler, operations-ops-field-extractor, medical-admin-ops-normalizer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, metrics-root-cause-diagnoser, slo-breach-checker, capacity-risk-forecaster, incident-summary-writer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, metrics-root-cause-diagnoser, capacity-risk-forecaster, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, capacity-risk-forecaster, dashboard-ops-risk-reviewer, latency-anomaly-detector |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, capacity-risk-forecaster, latency-anomaly-detector, slo-breach-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-dependency-mapper, incident-ops-handoff-brief-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, general-source-summariser, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `events-ops-monitoring-plan-builder` | wrong | events-ops-monitoring-plan-builder, news-briefing-writer, events-ops-handoff-brief-writer, incident-summary-writer, events-ops-risk-reviewer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, tech-news-trend-extractor, product-ops-evidence-grounder, document-extractor, citation-grounding-helper |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, data-analysis-for-forecasting |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, meeting-agenda-builder, groupwork-reply, meeting-summary-writer, meeting-followup-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-agenda-builder, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `thesis-ops-timeline-builder` | wrong | thesis-ops-timeline-builder, weekly-planner, thesis-ops-handoff-brief-writer, public-writing-plans, meeting-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, thesis-ops-summary-writer, research-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `research-ops-summary-writer` | wrong | research-ops-summary-writer, general-source-summariser, research-ops-scenario-planner, research-ops-comparison-builder, research-ops-priority-ranker |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, citation-grounding-helper, document-extractor, multi-source-comparison-builder |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, research-ops-field-extractor, web-data-extractor, incident-ops-field-extractor, course-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 2 | 2 | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, method-note-builder, research-ops-priority-ranker, research-ops-summary-writer, research-ops-handoff-brief-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-rewrite-editor, agent-ops-evidence-grounder, research-ops-rewrite-editor, research-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, related-work-synthesiser, thesis-ops-comparison-builder, citation-grounding-helper |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, groupwork-reply, reply-polisher, thesis-ops-handoff-brief-writer, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, groupwork-reply, email-polisher, email-ops-handoff-brief-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, meeting-followup-extractor, meeting-summary-writer, meeting-ops-handoff-brief-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply, reply-drafter |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 5 | 5 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply, reply-drafter |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, auth-flow-reviewer, public-security-threat-model, email-ops-risk-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 15 | 15 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-rewrite-editor, privacy-risk-reviewer, webhook-setup-planner, api-ops-handoff-brief-writer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, privacy-risk-reviewer, skill-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 3 | 3 | `webhook-setup-planner` | wrong | webhook-setup-planner, environment-config-auditor, secret-leak-scanner, public-netlify-deploy, api-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, security-code-reviewer, privacy-risk-reviewer, policy-compliance-checker, migration-risk-auditor |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-handoff-brief-writer, analytics-ops-summary-writer, analytics-ops-quality-auditor, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-ops-dependency-mapper, skill-creator, personal-ops-dependency-mapper, meeting-ops-resource-linker |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-with-validation, data-analysis-overview, data-analysis-for-reporting, data-analysis-with-anomaly-focus |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-artifact-packager, personal-ops-handoff-brief-writer, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, docs-ops-field-extractor, operations-ops-field-extractor, document-extractor, knowledge-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, email-polisher, followup-reply-writer, email-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | 19 | 19 | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, docs-ops-summary-writer, paper-summariser, research-ops-summary-writer, ml-ops-summary-writer |
