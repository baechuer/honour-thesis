# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (1006 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 65.7% |
| Acceptable top-1 accuracy | 67.2% |
| Top-3 recall | 71.6% |
| Top-5 recall | 71.6% |
| Acceptable top-5 recall | 73.1% |
| MRR | 0.688 |
| Non-main top-1 | 26.9% |
| Approx selector-visible tokens | 821405 |

## API Usage Estimate

- Embedding API calls made in this run: 101
- Embedding cache hits: 67
- Approx uncached embedding input tokens: 303223
- Rerank API calls made in this run: 67
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 518182

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, frontend-debugger, dashboard-ops-quality-auditor, web-ui-tester, dashboard-ops-evidence-grounder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, web-ops-field-extractor, ux-ops-field-extractor, ux-ops-quality-auditor |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `support-ops-acceptance-test-builder` | wrong | support-ops-acceptance-test-builder, web-form-filler, events-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder, community-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, public-playwright-interactive, product-ops-scenario-planner, product-ops-comparison-builder, vendor-ops-comparison-builder |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-rewrite-editor` | wrong | personal-ops-rewrite-editor, api-ops-normalizer, personal-ops-resource-linker, product-ops-rewrite-editor, personal-ops-quality-auditor |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, ux-ops-compliance-checker, web-form-filler, ux-ops-handoff-brief-writer, medical-admin-ops-quality-auditor |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `repo-ops-normalizer` | wrong | repo-ops-normalizer, personal-ops-quality-auditor, email-ops-quality-auditor, email-ops-normalizer, personal-ops-normalizer |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `migration-risk-auditor` | wrong | migration-risk-auditor, api-ops-acceptance-test-builder, security-code-reviewer, openapi-contract-tester, api-ops-quality-auditor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, api-integration-planner, pr-reviewer, email-ops-acceptance-test-builder, api-ops-risk-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `public-playwright-interactive` | wrong | public-playwright-interactive, auth-flow-reviewer, api-ops-quality-auditor, openapi-contract-tester, api-integration-planner |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, code-reviewer, api-ops-rewrite-editor, review-comment-resolver |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, api-ops-summary-writer, support-ops-rewrite-editor, api-ops-rewrite-editor, support-ops-quality-auditor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, public-xlsx, dataset-ops-summary-writer, data-analysis-for-reporting, data-analysis-with-validation |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, analytics-ops-monitoring-plan-builder, data-analysis-overview, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `dataset-ops-quality-auditor` | wrong | dataset-ops-quality-auditor, data-analysis-with-validation, analytics-ops-quality-auditor, support-ops-quality-auditor, data-analysis-with-anomaly-focus |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, variance-analysis-helper, analytics-ops-evidence-grounder, analytics-ops-quality-auditor |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dataset-ops-summary-writer, analytics-ops-summary-writer, dashboard-ops-summary-writer, operations-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus, analytics-ops-evidence-grounder, data-analysis-overview |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `agent-ops-priority-ranker` | wrong | agent-ops-priority-ranker, priority-sorter, operations-ops-priority-ranker, events-ops-priority-ranker, personal-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, travel-ops-field-extractor, travel-ops-priority-ranker, travel-ops-handoff-brief-writer, travel-ops-dependency-mapper |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-quality-auditor, travel-ops-summary-writer, travel-ops-artifact-packager, travel-ops-timeline-builder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-field-extractor, operations-ops-normalizer, travel-ops-rewrite-editor, events-ops-normalizer |
| `doc_p4_field_extraction` | `document-field-extractor` | 3 | 3 | `finance-ops-field-extractor` | wrong | finance-ops-field-extractor, vendor-ops-field-extractor, document-field-extractor, contract-ops-field-extractor, receipt-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, legal-ops-rewrite-editor, legal-ops-quality-auditor, privacy-policy-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, medical-admin-ops-normalizer, research-ops-quality-auditor, public-writing-plans, research-ops-field-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `ux-ops-field-extractor` | wrong | ux-ops-field-extractor, support-ops-field-extractor, events-ops-field-extractor, medical-admin-ops-field-extractor, lab-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, support-ticket-triager, slo-breach-checker, latency-anomaly-detector, medical-admin-ops-intake-classifier |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, analytics-ops-quality-auditor |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, agent-ops-risk-reviewer, metrics-overview, dashboard-ops-risk-reviewer, cloud-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, analytics-ops-risk-reviewer, cloud-ops-risk-reviewer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, cloud-ops-failure-diagnoser, debugging-root-cause-helper, analytics-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, incident-ops-summary-writer, incident-ops-timeline-builder, incident-ops-field-extractor |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, media-ops-summary-writer, operations-ops-summary-writer, contract-ops-summary-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, news-summariser, events-ops-summary-writer, incident-ops-handoff-brief-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, crm-ops-evidence-grounder, document-extractor, support-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, source-grounding-extractor, news-briefing-writer |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, cloud-ops-evidence-grounder, source-grounding-extractor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 11 | 11 | `meeting-ops-timeline-builder` | wrong | meeting-ops-timeline-builder, meeting-ops-dependency-mapper, course-ops-timeline-builder, weekly-planner, meeting-ops-risk-reviewer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-timeline-builder, meeting-followup-extractor, meeting-ops-quality-auditor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, task-extractor, meeting-ops-field-extractor, meeting-ops-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-followup-extractor, meeting-ops-timeline-builder, personal-ops-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-ops-timeline-builder, deadline-reminder-planner, agent-ops-timeline-builder, research-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, thesis-ops-summary-writer, method-note-builder, ml-ops-summary-writer, research-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, ux-ops-summary-writer, operations-ops-summary-writer, thesis-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, research-ops-field-extractor, speaker-notes-writer, note-linker |
| `read_p4_document_extraction` | `document-extractor` | - | - | `support-ops-field-extractor` | wrong | support-ops-field-extractor, lab-ops-field-extractor, contract-ops-field-extractor, incident-ops-field-extractor, search-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, thesis-ops-evidence-grounder, research-ops-evidence-grounder, lab-ops-evidence-grounder, research-ops-acceptance-test-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, writing-ops-evidence-grounder, research-ops-evidence-grounder, docs-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, ml-ops-comparison-builder, research-ops-comparison-builder, search-ops-comparison-builder, knowledge-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, method-note-builder, general-source-summariser, note-linker |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, email-drafter, followup-reply-writer, email-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `email-polisher` | wrong | email-polisher, reply-polisher, document-rewriter, reply-drafter, email-ops-rewrite-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, deadline-reminder-planner, speaker-notes-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, groupwork-reply, reply-polisher, proposal-drafter |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, email-ops-rewrite-editor, email-drafter, email-ops-handoff-brief-writer |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, auth-flow-reviewer, security-code-reviewer, privacy-risk-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-risk-reviewer, api-ops-compliance-checker, api-ops-evidence-grounder, api-ops-quality-auditor |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, contract-ops-dependency-mapper, repo-ops-risk-reviewer, agent-ops-risk-reviewer, community-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, public-netlify-deploy, webhook-setup-planner, migration-risk-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, personal-ops-compliance-checker, api-ops-compliance-checker, security-ops-compliance-checker, policy-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 7 | 7 | `analytics-ops-evidence-grounder` | wrong | analytics-ops-evidence-grounder, analytics-ops-risk-reviewer, analytics-ops-compliance-checker, search-ops-summary-writer, search-ops-quality-auditor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, task-extractor, meeting-followup-extractor, meeting-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, analytics-ops-artifact-packager, dataset-ops-artifact-packager, data-analysis-with-validation, research-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | - | - | `meeting-followup-extractor` | wrong | meeting-followup-extractor, task-extractor, thesis-ops-dependency-mapper, personal-ops-summary-writer, thesis-ops-summary-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `operations-ops-field-extractor` | wrong | operations-ops-field-extractor, agent-ops-field-extractor, hr-ops-field-extractor, ml-ops-field-extractor, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, professor-email-reply, email-polisher, reply-drafter, writing-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, research-ops-summary-writer, general-source-summariser, document-summariser, devops-ops-summary-writer |
