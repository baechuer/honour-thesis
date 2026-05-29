# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 61.2% |
| Acceptable top-1 accuracy | 65.7% |
| Top-3 recall | 65.7% |
| Top-5 recall | 65.7% |
| Acceptable top-5 recall | 70.2% |
| MRR | 0.644 |
| Non-main top-1 | 37.3% |
| Approx selector-visible tokens | 1239425 |

## API Usage Estimate

- Embedding API calls made in this run: 156
- Embedding cache hits: 72
- Approx uncached embedding input tokens: 468951
- Rerank API calls made in this run: 67
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 742279

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, frontend-debugger, web-ops-quality-auditor, web-ops-acceptance-test-builder, dashboard-ops-evidence-grounder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, ux-ops-field-extractor, web-ui-tester, web-ops-field-extractor, medical-admin-ops-acceptance-test-builder |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-ops-acceptance-test-builder, support-ops-acceptance-test-builder, product-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-resource-linker, product-ops-scenario-planner, product-ops-priority-ranker, product-ops-evidence-grounder |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `ux-ops-normalizer` | wrong | ux-ops-normalizer, ux-ops-rewrite-editor, ux-ops-handoff-brief-writer, personal-ops-quality-auditor, api-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, ux-ops-field-extractor, web-ui-tester, web-ops-rewrite-editor, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-ops-normalizer` | wrong | email-ops-normalizer, personal-ops-quality-auditor, email-ops-quality-auditor, personal-ops-acceptance-test-builder, personal-ops-normalizer |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `migration-risk-auditor` | wrong | migration-risk-auditor, api-ops-acceptance-test-builder, api-ops-quality-auditor, api-ops-risk-reviewer, api-ops-compliance-checker |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `api-integration-planner` | wrong | api-integration-planner, api-ops-risk-reviewer, api-ops-acceptance-test-builder, api-ops-scenario-planner, openapi-contract-tester |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `api-ops-failure-diagnoser` | wrong | api-ops-failure-diagnoser, api-ops-acceptance-test-builder, api-ops-quality-auditor, api-ops-compliance-checker, api-ops-dependency-mapper |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, api-ops-handoff-brief-writer, api-ops-normalizer, api-ops-rewrite-editor |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-ops-timeline-builder, analytics-ops-rewrite-editor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, dataset-ops-summary-writer, dataset-ops-field-extractor, dataset-ops-dependency-mapper, dataset-ops-evidence-grounder |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, analytics-ops-monitoring-plan-builder, dataset-ops-monitoring-plan-builder, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 3 | 3 | `dataset-ops-quality-auditor` | wrong | dataset-ops-quality-auditor, analytics-ops-quality-auditor, data-analysis-with-validation, support-ops-quality-auditor, data-analysis-with-anomaly-focus |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, analytics-ops-evidence-grounder, analytics-ops-quality-auditor, analytics-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dataset-ops-summary-writer, dashboard-ops-summary-writer, analytics-ops-summary-writer, dashboard-ops-handoff-brief-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, data-analysis-with-validation, data-analysis-overview |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `priority-sorter` | wrong | priority-sorter, analytics-ops-priority-ranker, operations-ops-priority-ranker, agent-ops-priority-ranker, events-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, travel-ops-normalizer, travel-ops-field-extractor, travel-ops-summary-writer, travel-ops-dependency-mapper |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-priority-ranker, travel-ops-quality-auditor, travel-ops-summary-writer, travel-ops-timeline-builder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-field-extractor, travel-ops-rewrite-editor, travel-ops-quality-auditor, travel-ops-evidence-grounder |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `finance-ops-field-extractor` | wrong | finance-ops-field-extractor, vendor-ops-field-extractor, receipt-extractor, finance-ops-normalizer, finance-ops-evidence-grounder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, legal-ops-rewrite-editor, legal-ops-artifact-packager, writing-ops-compliance-checker, legal-ops-acceptance-test-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, speaker-notes-writer, research-ops-rewrite-editor, lab-ops-risk-reviewer, operations-ops-field-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `ux-ops-field-extractor` | wrong | ux-ops-field-extractor, support-ops-field-extractor, events-ops-field-extractor, product-ops-field-extractor, medical-admin-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, medical-admin-ops-priority-ranker, medical-admin-ops-failure-diagnoser, medical-admin-ops-dependency-mapper, slo-breach-checker |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, analytics-ops-quality-auditor, analytics-ops-failure-diagnoser, cloud-monitoring-configurer |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, cloud-ops-risk-reviewer, incident-ops-risk-reviewer, analytics-ops-risk-reviewer, dashboard-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, cloud-ops-risk-reviewer, incident-ops-risk-reviewer, analytics-ops-risk-reviewer, metrics-overview |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, debugging-root-cause-helper, cloud-ops-failure-diagnoser, analytics-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 9 | 1 | `incident-ops-summary-writer` | acceptable | incident-ops-summary-writer, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-resource-linker, incident-ops-rewrite-editor |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, media-ops-summary-writer, community-ops-summary-writer, medical-admin-ops-summary-writer, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, events-ops-summary-writer, incident-ops-handoff-brief-writer, events-ops-evidence-grounder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, product-ops-evidence-grounder, research-ops-evidence-grounder, vendor-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, customer-feedback-analyser, keyword-researcher, news-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-theme-extractor, dashboard-ops-evidence-grounder, cloud-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 15 | 15 | `meeting-ops-timeline-builder` | wrong | meeting-ops-timeline-builder, meeting-ops-dependency-mapper, course-ops-timeline-builder, meeting-ops-scenario-planner, meeting-ops-risk-reviewer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-summary-writer, meeting-ops-normalizer, meeting-ops-handoff-brief-writer, meeting-ops-timeline-builder |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 9 | 9 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-ops-handoff-brief-writer, meeting-ops-field-extractor, meeting-ops-artifact-packager, meeting-ops-normalizer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-ops-summary-writer, meeting-ops-normalizer, weekly-planner, meeting-ops-timeline-builder |
| `plan_p5_weekly_planner` | `weekly-planner` | 6 | 6 | `deadline-reminder-planner` | wrong | deadline-reminder-planner, meeting-scheduler, meeting-ops-timeline-builder, personal-ops-timeline-builder, research-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, thesis-ops-summary-writer, thesis-ops-quality-auditor, thesis-ops-scenario-planner, thesis-ops-handoff-brief-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, ux-ops-summary-writer, research-ops-handoff-brief-writer, research-ops-quality-auditor |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, research-ops-artifact-packager, research-ops-summary-writer, research-ops-resource-linker, research-ops-dependency-mapper |
| `read_p4_document_extraction` | `document-extractor` | 19 | 19 | `web-ops-field-extractor` | wrong | web-ops-field-extractor, research-ops-field-extractor, dataset-ops-field-extractor, k8s-ops-field-extractor, ml-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, thesis-ops-evidence-grounder, research-ops-quality-auditor, research-ops-evidence-grounder, research-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, writing-ops-evidence-grounder, agent-ops-evidence-grounder, research-ops-evidence-grounder, agent-eval-coverage-auditor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 6 | 6 | `research-ops-comparison-builder` | wrong | research-ops-comparison-builder, ux-ops-comparison-builder, thesis-ops-comparison-builder, course-ops-comparison-builder, database-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, note-linker, research-ops-resource-linker, paper-summariser, research-ops-summary-writer |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, email-ops-handoff-brief-writer, email-ops-rewrite-editor, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `email-polisher` | wrong | email-polisher, reply-polisher, document-rewriter, email-ops-rewrite-editor, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, deadline-reminder-planner, followup-reply-writer, speaker-notes-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, writing-ops-handoff-brief-writer, reply-drafter, email-ops-rewrite-editor, writing-ops-rewrite-editor |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, email-ops-rewrite-editor, email-ops-normalizer, email-ops-handoff-brief-writer, email-ops-artifact-packager |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, auth-flow-reviewer, security-code-reviewer, security-ops-risk-reviewer, public-security-threat-model |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, api-ops-risk-reviewer, api-ops-quality-auditor, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, repo-ops-dependency-mapper, repo-ops-risk-reviewer, web-ops-dependency-mapper, community-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, public-netlify-deploy, devops-ops-handoff-brief-writer, webhook-setup-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, api-ops-risk-reviewer, policy-compliance-checker, cloud-ops-compliance-checker, personal-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 9 | 9 | `analytics-ops-compliance-checker` | wrong | analytics-ops-compliance-checker, analytics-ops-evidence-grounder, analytics-ops-risk-reviewer, analytics-ops-priority-ranker, analytics-ops-quality-auditor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-ops-evidence-grounder, meeting-ops-resource-linker, meeting-ops-comparison-builder, meeting-ops-dependency-mapper |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, dataset-ops-artifact-packager, analytics-ops-artifact-packager, finance-ops-artifact-packager, dataset-ops-evidence-grounder |
| `skill_p3_create_new` | `skill-creator` | - | - | `meeting-ops-dependency-mapper` | wrong | meeting-ops-dependency-mapper, meeting-ops-summary-writer, meeting-ops-rewrite-editor, thesis-ops-timeline-builder, thesis-ops-dependency-mapper |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, hr-ops-field-extractor, research-ops-field-extractor, operations-ops-field-extractor, product-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, writing-ops-rewrite-editor, email-ops-quality-auditor, email-ops-rewrite-editor, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, docs-ops-artifact-packager, research-ops-artifact-packager, agent-ops-dependency-mapper |
