# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 58.2% |
| Acceptable top-1 accuracy | 61.2% |
| Top-3 recall | 67.2% |
| Top-5 recall | 67.2% |
| Acceptable top-5 recall | 70.2% |
| MRR | 0.622 |
| Non-main top-1 | 25.4% |
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
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, terms-of-service-drafter, finance-ops-acceptance-test-builder, ux-ops-acceptance-test-builder, meeting-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ops-field-extractor, web-ops-quality-auditor, web-ui-tester, data-analysis-with-validation |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `data-analysis-with-validation` | wrong | data-analysis-with-validation, invoice-payment-checker, email-ops-compliance-checker, web-ops-compliance-checker, compliance-checklist-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-comparison-builder` | wrong | product-ops-comparison-builder, product-ops-priority-ranker, product-ops-handoff-brief-writer, product-ops-evidence-grounder, product-ops-monitoring-plan-builder |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `api-ops-timeline-builder` | wrong | api-ops-timeline-builder, api-integration-planner, personal-ops-timeline-builder, api-ops-rewrite-editor, api-ops-handoff-brief-writer |
| `web_p6_accessibility_check` | `accessibility-checker` | - | - | `document-summariser` | wrong | document-summariser, knowledge-base-article-writer, terms-of-service-drafter, landing-page-copy-reviewer, seo-metadata-checker |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `professor-email-reply` | wrong | professor-email-reply, email-polisher, email-drafter, email-ops-dependency-mapper, churn-risk-analyser |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `api-design-reviewer` | wrong | api-design-reviewer, api-integration-planner, openapi-contract-tester, migration-risk-auditor, api-ops-acceptance-test-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, api-integration-planner, openapi-contract-tester, api-design-reviewer, search-ops-acceptance-test-builder |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `openapi-contract-tester` | wrong | openapi-contract-tester, auth-flow-reviewer, git-commit-writer, travel-ops-acceptance-test-builder, contract-ops-acceptance-test-builder |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, api-integration-planner, webhook-setup-planner, churn-risk-analyser, api-design-reviewer |
| `code_p6_release_notes` | `release-note-writer` | - | - | `debugging-root-cause-helper` | wrong | debugging-root-cause-helper, meeting-scheduler, webhook-setup-planner, support-ops-timeline-builder, analytics-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, data-analysis-overview, data-analysis-for-forecasting, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting, analytics-ops-monitoring-plan-builder |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, support-ops-quality-auditor, analytics-ops-quality-auditor, email-ops-quality-auditor, community-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, analytics-ops-evidence-grounder, analytics-ops-monitoring-plan-builder, analytics-ops-failure-diagnoser, support-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, support-ops-summary-writer, email-ops-summary-writer, community-ops-summary-writer, contract-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, support-ops-evidence-grounder, email-ops-evidence-grounder, churn-risk-analyser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `meeting-ops-priority-ranker` | wrong | meeting-ops-priority-ranker, travel-ops-priority-ranker, personal-ops-priority-ranker, analytics-ops-priority-ranker, incident-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-quality-auditor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-intake-classifier, travel-ops-evidence-grounder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-rewrite-editor, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-intake-classifier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-field-extractor, vendor-ops-summary-writer, vendor-ops-timeline-builder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, privacy-policy-drafter, legal-ops-handoff-brief-writer, legal-ops-rewrite-editor, terms-of-service-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-intake-classifier, research-ops-risk-reviewer, procurement-risk-summariser, citation-note-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `meeting-ops-intake-classifier` | wrong | meeting-ops-intake-classifier, research-ops-intake-classifier, ux-ops-intake-classifier, crm-ops-intake-classifier, personal-ops-intake-classifier |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, support-ticket-triager, incident-ops-failure-diagnoser, medical-admin-ops-failure-diagnoser, cloud-ops-failure-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, procurement-risk-summariser, dashboard-ops-risk-reviewer, incident-ops-risk-reviewer, capacity-risk-forecaster |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, procurement-risk-summariser, support-ops-failure-diagnoser, cloud-ops-failure-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, analytics-ops-failure-diagnoser, support-ops-failure-diagnoser, incident-ops-failure-diagnoser, cloud-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-intake-classifier, incident-ops-handoff-brief-writer, incident-ops-failure-diagnoser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, paper-summariser, recruiting-ops-summary-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, events-ops-monitoring-plan-builder, events-ops-handoff-brief-writer, events-ops-evidence-grounder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, vendor-ops-evidence-grounder, meeting-ops-evidence-grounder, research-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, security-ops-evidence-grounder, email-ops-evidence-grounder, analytics-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-intake-classifier, meeting-ops-handoff-brief-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-scheduler |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-handoff-brief-writer, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, meeting-agenda-builder, deadline-reminder-planner, meeting-ops-timeline-builder |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, weekly-planner, meeting-ops-summary-writer, agent-ops-scenario-planner |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, thesis-ops-summary-writer, multi-source-comparison-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, operations-ops-summary-writer, research-ops-evidence-grounder, thesis-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-linker, speaker-notes-writer, research-ops-evidence-grounder, writing-ops-evidence-grounder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `lab-ops-field-extractor` | wrong | lab-ops-field-extractor, recruiting-ops-field-extractor, incident-ops-field-extractor, research-ops-field-extractor, repo-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, research-ops-scenario-planner, research-ops-handoff-brief-writer, multi-source-comparison-builder, thesis-ops-handoff-brief-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-eval-coverage-auditor, writing-ops-evidence-grounder, support-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, thesis-ops-comparison-builder, knowledge-ops-comparison-builder, database-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, ml-ops-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, followup-reply-writer, reply-drafter, reply-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, followup-reply-writer, meeting-scheduler, meeting-ops-rewrite-editor, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, meeting-followup-extractor, meeting-summary-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-drafter, professor-email-reply, proposal-drafter, thesis-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `followup-reply-writer` | wrong | followup-reply-writer, reply-polisher, reply-drafter, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, email-ops-risk-reviewer, security-ops-resource-linker, email-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `api-design-reviewer` | wrong | api-design-reviewer, api-integration-planner, api-ops-compliance-checker, webhook-setup-planner, api-ops-handoff-brief-writer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, contract-ops-dependency-mapper, repo-ops-risk-reviewer, web-ops-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `webhook-setup-planner` | wrong | webhook-setup-planner, environment-config-auditor, database-ops-monitoring-plan-builder, database-ops-handoff-brief-writer, database-ops-timeline-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, policy-compliance-checker, email-ops-compliance-checker, database-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `data-analysis-with-anomaly-focus` | wrong | data-analysis-with-anomaly-focus, search-ops-monitoring-plan-builder, analytics-ops-monitoring-plan-builder, search-ops-quality-auditor, analytics-ops-evidence-grounder |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-ops-comparison-builder, meeting-ops-failure-diagnoser, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-for-reporting, dataset-ops-artifact-packager, analytics-ops-artifact-packager, public-pptx |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, thesis-ops-handoff-brief-writer, agent-ops-handoff-brief-writer, meeting-followup-extractor, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, agent-ops-field-extractor, knowledge-ops-field-extractor, hr-ops-field-extractor, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, skill-evaluator, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-resource-linker` | wrong | agent-ops-resource-linker, public-pptx, agent-ops-summary-writer, document-summariser, paper-summariser |
