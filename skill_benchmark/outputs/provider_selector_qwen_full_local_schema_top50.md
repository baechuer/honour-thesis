# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 50

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 80.6% |
| Acceptable top-1 accuracy | 80.6% |
| Top-3 recall | 86.6% |
| Top-5 recall | 88.1% |
| Acceptable top-5 recall | 89.5% |
| MRR | 0.834 |
| Non-main top-1 | 11.9% |
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
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, metrics-overview, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, medical-admin-ops-field-extractor, ux-ops-field-extractor, travel-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, travel-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder, web-ops-acceptance-test-builder, support-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-comparison-builder, product-ops-field-extractor, product-ops-scenario-planner, product-ops-priority-ranker |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-handoff-brief-writer` | wrong | api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-integration-planner, personal-ops-handoff-brief-writer, personal-ops-normalizer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, web-form-filler, email-drafter, web-ui-tester, support-ticket-triager |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, professor-email-reply, churn-risk-analyser, email-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, auth-flow-reviewer, api-ops-acceptance-test-builder, migration-risk-auditor, api-ops-comparison-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, api-ops-acceptance-test-builder, api-ops-monitoring-plan-builder |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, web-ui-tester, frontend-debugger, api-ops-acceptance-test-builder |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, privacy-risk-reviewer, review-comment-resolver |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, auth-flow-reviewer, churn-risk-analyser, frontend-debugger, api-ops-rewrite-editor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-reporting, data-analysis-for-forecasting, dataset-ops-summary-writer, dashboard-ops-handoff-brief-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, dataset-ops-quality-auditor, support-ops-quality-auditor, analytics-ops-quality-auditor, media-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, variance-analysis-helper, support-ops-failure-diagnoser, analytics-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, support-ops-summary-writer, news-briefing-writer, financial-report-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, metrics-root-cause-diagnoser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, travel-ops-priority-ranker, meeting-ops-priority-ranker, dashboard-ops-priority-ranker, support-ops-scenario-planner |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, events-ops-summary-writer, meeting-ops-summary-writer, travel-ops-quality-auditor, travel-ops-compliance-checker |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 2 | `reply-polisher` | wrong | reply-polisher, travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-normalizer |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, travel-ops-rewrite-editor, travel-ops-normalizer, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 7 | 7 | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-field-extractor, finance-ops-field-extractor, contract-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, privacy-policy-drafter, legal-ops-rewrite-editor, community-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-risk-reviewer, citation-note-extractor, research-ops-dependency-mapper, research-ops-artifact-packager |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, operations-ops-field-extractor, ux-ops-field-extractor, personal-ops-field-extractor, events-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, cloud-monitoring-configurer, incident-summary-writer, metrics-root-cause-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, capacity-risk-forecaster, metrics-overview, dashboard-ops-risk-reviewer, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, analytics-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, metrics-overview, latency-anomaly-detector, capacity-risk-forecaster |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, news-theme-extractor, tech-news-trend-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, metrics-overview, events-ops-scenario-planner |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, knowledge-base-article-writer, product-ops-evidence-grounder, document-extractor, news-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, metrics-root-cause-diagnoser |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-risk-reviewer, meeting-ops-handoff-brief-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, incident-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-agenda-builder, personal-ops-field-extractor, personal-ops-normalizer |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-ops-acceptance-test-builder` | wrong | meeting-ops-acceptance-test-builder, meeting-scheduler, weekly-planner, meeting-ops-monitoring-plan-builder, meeting-ops-summary-writer |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, data-analysis-for-reporting, paper-summariser, research-ops-evidence-grounder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, speaker-notes-writer, note-linker, method-note-builder, research-ops-field-extractor |
| `read_p4_document_extraction` | `document-extractor` | 5 | 5 | `web-data-extractor` | wrong | web-data-extractor, research-ops-field-extractor, incident-ops-field-extractor, lab-ops-field-extractor, document-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, research-ops-acceptance-test-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-ops-rewrite-editor, support-ops-evidence-grounder, research-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, related-work-synthesiser, database-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ux-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply, reply-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, document-rewriter, email-polisher, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, professor-email-reply, reply-drafter, groupwork-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, email-ops-risk-reviewer, security-ops-scenario-planner, auth-flow-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, api-ops-compliance-checker, api-ops-handoff-brief-writer, api-ops-rewrite-editor |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, repo-ops-risk-reviewer, contract-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, environment-config-auditor, kubernetes-deployment-helper, database-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, accessibility-checker, policy-compliance-checker, email-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-overview, analytics-ops-resource-linker, data-analysis-for-root-cause-diagnosis, analytics-ops-handoff-brief-writer |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, meeting-followup-extractor, meeting-ops-comparison-builder, meeting-ops-dependency-mapper |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-for-reporting, financial-report-writer, dataset-ops-artifact-packager, finance-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, agent-ops-field-extractor, document-field-extractor, hr-ops-field-extractor, operations-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, agent-ops-summary-writer, skill-editor, docs-ops-summary-writer, paper-summariser |
