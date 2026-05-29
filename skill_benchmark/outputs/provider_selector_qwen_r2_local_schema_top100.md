# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 79.1% |
| Acceptable top-1 accuracy | 79.1% |
| Top-3 recall | 89.5% |
| Top-5 recall | 89.5% |
| Acceptable top-5 recall | 89.5% |
| MRR | 0.838 |
| Non-main top-1 | 10.4% |
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
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-ui-tester, frontend-debugger, dashboard-ops-acceptance-test-builder, dashboard-ops-handoff-brief-writer |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, crm-ops-field-extractor, web-ops-field-extractor, medical-admin-ops-field-extractor, ux-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, email-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder, travel-ops-acceptance-test-builder, events-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-comparison-builder, product-ops-scenario-planner, product-ops-priority-ranker, product-ops-field-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-handoff-brief-writer` | wrong | api-ops-handoff-brief-writer, api-ops-rewrite-editor, api-ops-timeline-builder, api-ops-normalizer, api-ops-evidence-grounder |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `web-form-filler` | wrong | web-form-filler, accessibility-checker, support-ticket-triager, terms-of-service-drafter, webhook-setup-planner |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-polisher` | wrong | email-polisher, email-drafter, professor-email-reply, reply-drafter, email-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, auth-flow-reviewer, migration-risk-auditor, openapi-contract-tester, api-ops-acceptance-test-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, openapi-contract-tester, api-ops-quality-auditor |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, ci-failure-debugger, web-ui-tester, openapi-contract-tester, frontend-debugger |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, churn-risk-analyser, privacy-risk-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, churn-risk-analyser, frontend-debugger, meeting-scheduler, webhook-setup-planner |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, data-analysis-overview, financial-report-writer, data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, support-ops-quality-auditor, analytics-ops-quality-auditor, community-ops-quality-auditor, dataset-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, variance-analysis-helper, analytics-ops-evidence-grounder, support-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, support-ops-summary-writer, news-briefing-writer, financial-report-writer, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, news-briefing-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, dashboard-ops-priority-ranker, dashboard-ops-scenario-planner, travel-ops-priority-ranker, meeting-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-normalizer, travel-ops-quality-auditor |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, travel-ops-summary-writer, travel-ops-normalizer, travel-ops-risk-reviewer |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, travel-ops-normalizer, travel-ops-rewrite-editor, travel-ops-risk-reviewer, travel-ops-summary-writer |
| `doc_p4_field_extraction` | `document-field-extractor` | 7 | 7 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, vendor-ops-field-extractor, finance-ops-field-extractor, contract-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, privacy-policy-drafter, community-ops-comparison-builder, writing-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, layout-preserving-converter, citation-note-extractor, research-ops-risk-reviewer, research-ops-intake-classifier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-field-extractor` | wrong | medical-admin-ops-field-extractor, operations-ops-field-extractor, ux-ops-field-extractor, travel-ops-field-extractor, personal-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, cloud-monitoring-configurer, incident-summary-writer, capacity-risk-forecaster |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, capacity-risk-forecaster, dashboard-ops-risk-reviewer, metrics-overview, analytics-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, metrics-overview, capacity-risk-forecaster, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, metrics-overview, incident-ops-handoff-brief-writer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, tech-news-trend-extractor, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, events-ops-monitoring-plan-builder, events-ops-handoff-brief-writer, metrics-overview |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, general-source-summariser, document-extractor, knowledge-base-article-writer |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, web-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-ops-risk-reviewer, meeting-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-scheduler |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, incident-summary-writer, meeting-ops-field-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, speaker-notes-writer, meeting-agenda-builder, personal-ops-field-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-ops-acceptance-test-builder, weekly-planner, meeting-scheduler, refactor-planner |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, ux-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, paper-summariser, data-analysis-for-reporting, operations-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, speaker-notes-writer, research-ops-field-extractor, research-ops-evidence-grounder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, incident-ops-field-extractor, lab-ops-field-extractor, course-ops-field-extractor, ml-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, research-ops-rewrite-editor, thesis-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, support-ops-evidence-grounder, agent-eval-coverage-auditor, thesis-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, database-ops-comparison-builder, lab-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ux-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, document-rewriter, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, reply-drafter, professor-email-reply, email-polisher |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, email-ops-risk-reviewer, privacy-risk-reviewer, public-brainstorming |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, webhook-setup-planner, privacy-risk-reviewer, api-ops-risk-reviewer, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, contract-ops-dependency-mapper, capacity-risk-forecaster |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, environment-config-auditor, database-ops-monitoring-plan-builder, kubernetes-deployment-helper |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-polisher, data-analysis-with-validation, accessibility-checker, security-code-reviewer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, search-ops-quality-auditor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-ops-comparison-builder, skill-creator, repo-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-for-reporting, financial-report-writer, analytics-ops-artifact-packager, public-pptx |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, skill-finder, thesis-ops-timeline-builder, meeting-followup-extractor |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, agent-ops-field-extractor, hr-ops-field-extractor, operations-ops-field-extractor, research-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, skill-finder |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, agent-ops-summary-writer, paper-summariser, docs-ops-summary-writer, ml-ops-summary-writer |
