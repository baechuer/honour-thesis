# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (1006 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 47.8% |
| Acceptable top-1 accuracy | 47.8% |
| Top-3 recall | 64.2% |
| Top-5 recall | 65.7% |
| Acceptable top-5 recall | 67.2% |
| MRR | 0.563 |
| Non-main top-1 | 31.3% |
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
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, web-page-snapshotter, web-ops-field-extractor, web-ops-normalizer |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, vendor-ops-compliance-checker, email-ops-compliance-checker, ux-ops-compliance-checker, email-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 6 | 6 | `product-ops-comparison-builder` | wrong | product-ops-comparison-builder, competitive-battlecard-builder, product-ops-scenario-planner, public-playwright-interactive, product-ops-priority-ranker |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-normalizer` | wrong | personal-ops-normalizer, personal-ops-rewrite-editor, personal-ops-handoff-brief-writer, community-ops-normalizer, webhook-setup-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 9 | 9 | `web-form-filler` | wrong | web-form-filler, webhook-setup-planner, medical-admin-ops-quality-auditor, events-ops-quality-auditor, support-ticket-triager |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `email-drafter` | wrong | email-drafter, email-polisher, email-thread-summariser, reply-polisher, personal-ops-normalizer |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, api-ops-normalizer, api-integration-planner, api-ops-quality-auditor, migration-risk-auditor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 12 | 12 | `api-ops-quality-auditor` | wrong | api-ops-quality-auditor, api-integration-planner, openapi-contract-tester, slo-breach-checker, webhook-setup-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, openapi-contract-tester, api-integration-planner, security-code-reviewer, secret-leak-scanner |
| `code_p5_changelog_entry` | `changelog-writer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, churn-risk-analyser, privacy-risk-reviewer, file-renamer, changelog-writer |
| `code_p6_release_notes` | `release-note-writer` | 18 | 18 | `churn-risk-analyser` | wrong | churn-risk-analyser, api-ops-timeline-builder, webhook-setup-planner, meeting-scheduler, support-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-forecasting, data-analysis-with-validation |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, data-analysis-overview, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, data-analysis-with-validation, data-analysis-with-anomaly-focus, analytics-ops-quality-auditor, data-analysis-overview |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, churn-risk-analyser, analytics-ops-evidence-grounder, analytics-ops-monitoring-plan-builder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, analytics-ops-summary-writer, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, support-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, data-analysis-overview, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `travel-ops-priority-ranker` | wrong | travel-ops-priority-ranker, meeting-ops-priority-ranker, dashboard-ops-priority-ranker, events-ops-priority-ranker, agent-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-normalizer, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-intake-classifier |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 6 | `travel-ops-summary-writer` | borderline | travel-ops-summary-writer, travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-handoff-brief-writer, travel-ops-quality-auditor |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-risk-reviewer, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-compliance-checker |
| `doc_p4_field_extraction` | `document-field-extractor` | 16 | 16 | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, vendor-ops-handoff-brief-writer, vendor-ops-normalizer, vendor-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 19 | 2 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, legal-ops-comparison-builder, email-polisher, legal-ops-rewrite-editor, terms-of-service-drafter |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, research-ops-intake-classifier, research-ops-compliance-checker, research-ops-risk-reviewer, citation-note-extractor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `medical-admin-ops-normalizer` | wrong | medical-admin-ops-normalizer, medical-admin-ops-field-extractor, web-form-filler, medical-admin-ops-summary-writer, medical-admin-ops-quality-auditor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, capacity-risk-forecaster, slo-breach-checker, incident-summary-writer, metrics-root-cause-diagnoser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, capacity-risk-forecaster, metrics-overview, dashboard-ops-risk-reviewer, analytics-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, latency-anomaly-detector, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, capacity-risk-forecaster, metrics-overview, slo-breach-checker, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-normalizer, incident-ops-handoff-brief-writer, incident-ops-summary-writer, metrics-overview |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, events-ops-risk-reviewer, events-ops-monitoring-plan-builder, events-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, vendor-ops-evidence-grounder, research-ops-evidence-grounder, tech-news-trend-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, security-ops-evidence-grounder, analytics-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-risk-reviewer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, meeting-ops-summary-writer, task-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 3 | 3 | `weekly-planner` | wrong | weekly-planner, meeting-agenda-builder, task-extractor, meeting-followup-extractor, deadline-reminder-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-agenda-builder, thesis-ops-timeline-builder, agent-ops-timeline-builder, research-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 2 | 2 | `method-note-builder` | wrong | method-note-builder, paper-summariser, research-ops-summary-writer, citation-grounding-helper, thesis-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, research-ops-summary-writer, research-ops-comparison-builder, research-ops-scenario-planner, research-ops-risk-reviewer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, general-source-summariser, research-ops-normalizer, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, incident-ops-field-extractor, course-ops-field-extractor, dataset-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, citation-grounding-helper, research-ops-scenario-planner, research-ops-comparison-builder, research-ops-priority-ranker |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, agent-eval-coverage-auditor, agent-ops-rewrite-editor, thesis-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `research-ops-comparison-builder` | wrong | research-ops-comparison-builder, multi-source-comparison-builder, thesis-ops-comparison-builder, citation-grounding-helper, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, method-note-builder, citation-grounding-helper, paper-summariser |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-polisher, groupwork-reply, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, groupwork-reply, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, meeting-followup-extractor, meeting-summary-writer, meeting-agenda-builder |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, reply-drafter, email-polisher, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `followup-reply-writer` | wrong | followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply, professor-email-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, public-security-threat-model, auth-flow-reviewer, public-brainstorming |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `webhook-setup-planner` | wrong | webhook-setup-planner, auth-flow-reviewer, privacy-risk-reviewer, api-ops-risk-reviewer, incident-ops-handoff-brief-writer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, migration-risk-auditor, media-ops-risk-reviewer, public-skill-installer, capacity-risk-forecaster |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 3 | 3 | `webhook-setup-planner` | wrong | webhook-setup-planner, environment-config-auditor, secret-leak-scanner, public-netlify-deploy, web-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, security-code-reviewer, privacy-risk-reviewer, database-ops-compliance-checker, analytics-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-quality-auditor, analytics-ops-evidence-grounder, analytics-ops-summary-writer, analytics-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-ops-comparison-builder, task-extractor, citation-note-extractor, research-ops-dependency-mapper |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-overview, data-analysis-for-reporting, data-analysis-for-forecasting, data-analysis-with-validation |
| `skill_p3_create_new` | `skill-creator` | - | - | `thesis-ops-handoff-brief-writer` | wrong | thesis-ops-handoff-brief-writer, thesis-ops-timeline-builder, thesis-ops-dependency-mapper, agent-ops-handoff-brief-writer, meeting-ops-handoff-brief-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, document-field-extractor, operations-ops-field-extractor, personal-ops-field-extractor, product-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | - | - | `reply-polisher` | wrong | reply-polisher, reply-drafter, followup-reply-writer, email-polisher, incident-ops-rewrite-editor |
| `skill_p6_package_existing` | `skill-packager` | - | - | `agent-ops-summary-writer` | wrong | agent-ops-summary-writer, paper-summariser, docs-ops-summary-writer, ml-ops-summary-writer, support-ops-summary-writer |
