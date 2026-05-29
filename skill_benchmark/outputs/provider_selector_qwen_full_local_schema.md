# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 68.7% |
| Acceptable top-1 accuracy | 71.6% |
| Top-3 recall | 74.6% |
| Top-5 recall | 74.6% |
| Acceptable top-5 recall | 77.6% |
| MRR | 0.715 |
| Non-main top-1 | 22.4% |
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
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, ux-ops-field-extractor, web-ui-tester, web-ops-quality-auditor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, travel-ops-acceptance-test-builder, invoice-payment-checker, vendor-ops-acceptance-test-builder, web-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-comparison-builder, product-ops-scenario-planner, product-ops-priority-ranker, product-ops-resource-linker |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-handoff-brief-writer` | wrong | api-ops-handoff-brief-writer, api-ops-rewrite-editor, personal-ops-normalizer, personal-ops-handoff-brief-writer, personal-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, web-form-filler, email-drafter, web-ui-tester, terms-of-service-drafter |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, professor-email-reply, churn-risk-analyser, reply-polisher |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `api-ops-acceptance-test-builder` | wrong | api-ops-acceptance-test-builder, auth-flow-reviewer, migration-risk-auditor, api-ops-comparison-builder, api-ops-risk-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | - | - | `api-ops-acceptance-test-builder` | wrong | api-ops-acceptance-test-builder, openapi-contract-tester, api-ops-monitoring-plan-builder, api-ops-quality-auditor, api-ops-failure-diagnoser |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-acceptance-test-builder, openapi-contract-tester, api-ops-compliance-checker, api-ops-failure-diagnoser |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, privacy-risk-reviewer, churn-risk-analyser |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, auth-flow-reviewer, churn-risk-analyser, frontend-debugger, api-ops-rewrite-editor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-reporting, data-analysis-for-forecasting, dataset-ops-summary-writer, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-overview |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, dataset-ops-quality-auditor, support-ops-quality-auditor, analytics-ops-quality-auditor, media-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, support-ops-failure-diagnoser, data-analysis-overview, analytics-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, support-ops-summary-writer, news-briefing-writer, data-analysis-for-root-cause-diagnosis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, metrics-root-cause-diagnoser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `support-ops-scenario-planner` | wrong | support-ops-scenario-planner, dashboard-ops-priority-ranker, travel-ops-priority-ranker, meeting-ops-priority-ranker, events-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, travel-ops-quality-auditor, travel-ops-compliance-checker, travel-ops-handoff-brief-writer, travel-ops-monitoring-plan-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-normalizer, travel-ops-summary-writer |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-rewrite-editor` | wrong | travel-ops-rewrite-editor, travel-ops-normalizer, travel-ops-timeline-builder, travel-ops-quality-auditor, travel-ops-risk-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-field-extractor, finance-ops-field-extractor, vendor-ops-summary-writer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, community-ops-comparison-builder, legal-ops-rewrite-editor, privacy-policy-drafter, legal-ops-artifact-packager |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-risk-reviewer, citation-note-extractor, research-ops-dependency-mapper, research-ops-artifact-packager |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, operations-ops-field-extractor, ux-ops-field-extractor, personal-ops-field-extractor, events-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, cloud-monitoring-configurer, incident-summary-writer, metrics-root-cause-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, capacity-risk-forecaster, metrics-overview, dashboard-ops-risk-reviewer, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, analytics-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, metrics-overview, latency-anomaly-detector, capacity-risk-forecaster |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, news-theme-extractor, tech-news-trend-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-monitoring-plan-builder, events-ops-summary-writer, metrics-overview, events-ops-handoff-brief-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, document-extractor, knowledge-base-article-writer, news-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, metrics-root-cause-diagnoser |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-risk-reviewer, meeting-ops-handoff-brief-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, meeting-agenda-builder, personal-ops-normalizer, personal-ops-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-scheduler` | wrong | meeting-scheduler, weekly-planner, meeting-ops-summary-writer, thesis-ops-timeline-builder, meeting-ops-handoff-brief-writer |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, data-analysis-for-reporting, research-ops-evidence-grounder, research-ops-scenario-planner |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, speaker-notes-writer, note-linker, method-note-builder, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | 20 | 20 | `web-data-extractor` | wrong | web-data-extractor, research-ops-field-extractor, lab-ops-field-extractor, incident-ops-field-extractor, course-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, research-ops-priority-ranker |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-ops-rewrite-editor, research-ops-evidence-grounder, agent-eval-coverage-auditor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, related-work-synthesiser, database-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, research-ops-resource-linker |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply, reply-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, groupwork-reply, email-polisher, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, professor-email-reply, reply-drafter, groupwork-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, email-ops-risk-reviewer, auth-flow-reviewer, public-security-threat-model |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, api-ops-compliance-checker, api-ops-handoff-brief-writer, api-ops-rewrite-editor |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, repo-ops-risk-reviewer, web-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, environment-config-auditor, database-ops-monitoring-plan-builder, public-netlify-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, policy-compliance-checker, email-ops-compliance-checker, security-code-reviewer, privacy-risk-reviewer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-resource-linker, churn-risk-analyser, analytics-ops-monitoring-plan-builder, analytics-ops-normalizer |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, meeting-ops-comparison-builder, meeting-ops-dependency-mapper, meeting-ops-evidence-grounder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-for-reporting, dataset-ops-artifact-packager, finance-ops-artifact-packager, analytics-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer, thesis-ops-dependency-mapper, thesis-ops-timeline-builder, thesis-ops-intake-classifier |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, agent-ops-field-extractor, document-field-extractor, hr-ops-field-extractor, operations-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, agent-ops-summary-writer, docs-ops-summary-writer, paper-summariser, research-ops-summary-writer |
