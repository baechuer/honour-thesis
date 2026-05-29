# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (1006 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 64.2% |
| Acceptable top-1 accuracy | 67.2% |
| Top-3 recall | 64.2% |
| Top-5 recall | 67.2% |
| Acceptable top-5 recall | 70.2% |
| MRR | 0.649 |
| Non-main top-1 | 31.3% |
| Approx selector-visible tokens | 194602 |

## API Usage Estimate

- Embedding API calls made in this run: 101
- Embedding cache hits: 67
- Approx uncached embedding input tokens: 50587
- Rerank API calls made in this run: 67
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 144015

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, dashboard-ops-acceptance-test-builder, dashboard-ops-evidence-grounder, ux-ops-acceptance-test-builder, personal-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, frontend-debugger, web-ops-field-extractor, ux-ops-quality-auditor |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `web-ops-compliance-checker` | wrong | web-ops-compliance-checker, invoice-payment-checker, ux-ops-compliance-checker, support-ops-compliance-checker, product-ops-compliance-checker |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-handoff-brief-writer` | wrong | product-ops-handoff-brief-writer, data-analysis-for-ranking-selection, product-ops-comparison-builder, knowledge-base-article-writer, product-ops-priority-ranker |
| `web_p5_frontend_debugging` | `frontend-debugger` | - | - | `personal-ops-rewrite-editor` | wrong | personal-ops-rewrite-editor, api-ops-rewrite-editor, ux-ops-timeline-builder, api-integration-planner, support-ops-rewrite-editor |
| `web_p6_accessibility_check` | `accessibility-checker` | - | - | `ux-ops-compliance-checker` | wrong | ux-ops-compliance-checker, document-summariser, support-ops-compliance-checker, compliance-checklist-builder, recruiting-ops-rewrite-editor |
| `code_p1_local_code_review` | `code-reviewer` | - | - | `personal-ops-acceptance-test-builder` | wrong | personal-ops-acceptance-test-builder, email-ops-normalizer, email-ops-acceptance-test-builder, churn-risk-analyser, email-ops-failure-diagnoser |
| `code_p2_pr_review` | `pr-reviewer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, migration-risk-auditor, api-ops-acceptance-test-builder, api-ops-risk-reviewer, api-ops-quality-auditor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, api-integration-planner, api-ops-acceptance-test-builder, search-ops-acceptance-test-builder, webhook-setup-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, email-ops-acceptance-test-builder, crm-ops-acceptance-test-builder, contract-ops-acceptance-test-builder, meeting-ops-acceptance-test-builder |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, git-commit-writer, api-ops-handoff-brief-writer, api-ops-normalizer, refactor-planner |
| `code_p6_release_notes` | `release-note-writer` | - | - | `debugging-root-cause-helper` | wrong | debugging-root-cause-helper, docs-ops-timeline-builder, support-ops-timeline-builder, email-ops-timeline-builder, analytics-ops-timeline-builder |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-with-validation, data-analysis-for-forecasting, data-analysis-for-reporting, data-analysis-for-ranking-selection |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-forecasting, data-analysis-with-validation, analytics-ops-monitoring-plan-builder, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, analytics-ops-quality-auditor, research-ops-quality-auditor, data-analysis-with-anomaly-focus, agent-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, analytics-ops-evidence-grounder, analytics-ops-failure-diagnoser, analytics-ops-quality-auditor, support-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, analytics-ops-summary-writer, analytics-ops-handoff-brief-writer, operations-ops-summary-writer, product-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, data-analysis-for-root-cause-diagnosis, data-analysis-overview, data-analysis-with-anomaly-focus, analytics-ops-evidence-grounder |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `events-ops-priority-ranker` | wrong | events-ops-priority-ranker, operations-ops-priority-ranker, agent-ops-priority-ranker, personal-ops-priority-ranker, analytics-ops-priority-ranker |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-handoff-brief-writer` | wrong | travel-ops-handoff-brief-writer, travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-rewrite-editor, travel-ops-normalizer |
| `doc_p2_document_rewriter` | `document-rewriter` | - | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, travel-ops-summary-writer, travel-ops-handoff-brief-writer, travel-ops-field-extractor, travel-ops-evidence-grounder |
| `doc_p3_document_normaliser` | `document-normaliser` | - | - | `travel-ops-normalizer` | wrong | travel-ops-normalizer, travel-ops-rewrite-editor, travel-ops-quality-auditor, travel-ops-evidence-grounder, meeting-ops-normalizer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `vendor-ops-field-extractor` | wrong | vendor-ops-field-extractor, receipt-extractor, vendor-ops-normalizer, invoice-payment-checker, vendor-ops-dependency-mapper |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | - | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, legal-ops-rewrite-editor, legal-ops-compliance-checker, legal-ops-quality-auditor, clause-obligation-extractor |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, method-note-builder, citation-note-extractor, document-summariser, research-ops-handoff-brief-writer |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | - | - | `proposal-drafter` | wrong | proposal-drafter, procurement-risk-summariser, legal-ops-handoff-brief-writer, ux-ops-intake-classifier, compliance-checklist-builder |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, support-ticket-triager, database-ops-intake-classifier, cloud-ops-intake-classifier, operations-ops-intake-classifier |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, slo-breach-checker, analytics-ops-quality-auditor |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, dashboard-ops-risk-reviewer, incident-ops-risk-reviewer, analytics-ops-risk-reviewer, database-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, operations-ops-failure-diagnoser, operations-ops-monitoring-plan-builder, cloud-ops-failure-diagnoser, cloud-ops-monitoring-plan-builder |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, cloud-ops-failure-diagnoser, debugging-root-cause-helper, events-ops-failure-diagnoser, devops-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, incident-ops-handoff-brief-writer, incident-ops-summary-writer, incident-ops-artifact-packager, incident-ops-failure-diagnoser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-briefing-writer, media-ops-summary-writer, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-handoff-brief-writer, incident-ops-handoff-brief-writer, incident-ops-summary-writer, events-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, crm-ops-evidence-grounder, legal-ops-evidence-grounder, research-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, related-work-synthesiser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, cloud-ops-evidence-grounder, agent-ops-evidence-grounder, product-ops-evidence-grounder |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 4 | 4 | `meeting-ops-timeline-builder` | wrong | meeting-ops-timeline-builder, course-ops-timeline-builder, weekly-planner, meeting-agenda-builder, meeting-ops-risk-reviewer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, document-summariser, meeting-followup-extractor, meeting-ops-handoff-brief-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-ops-summary-writer, task-extractor, meeting-summary-writer, meeting-ops-handoff-brief-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-followup-extractor, meeting-summary-writer, meeting-agenda-builder |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, subagent-task-planner, meeting-ops-timeline-builder, meeting-agenda-builder, agent-ops-timeline-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, thesis-ops-summary-writer, method-note-builder, multi-source-comparison-builder, research-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 4 | 4 | `research-ops-summary-writer` | wrong | research-ops-summary-writer, ux-ops-summary-writer, operations-ops-summary-writer, general-source-summariser, meeting-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, method-note-builder, document-converter, citation-grounding-helper, general-source-summariser |
| `read_p4_document_extraction` | `document-extractor` | - | - | `repo-ops-field-extractor` | wrong | repo-ops-field-extractor, research-ops-field-extractor, vendor-ops-field-extractor, web-ops-field-extractor, recruiting-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, multi-source-comparison-builder, research-ops-evidence-grounder, thesis-ops-evidence-grounder, lab-ops-evidence-grounder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, writing-ops-evidence-grounder, agent-ops-rewrite-editor, ml-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, research-ops-comparison-builder, writing-ops-comparison-builder, knowledge-ops-comparison-builder, docs-ops-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, method-note-builder, research-ops-resource-linker, note-linker, research-ops-summary-writer |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, email-drafter, reply-drafter, email-polisher, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, email-polisher, email-ops-rewrite-editor, support-ops-rewrite-editor, meeting-ops-rewrite-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, deadline-reminder-planner, weekly-planner, followup-reply-writer, reply-drafter |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, reply-polisher, groupwork-reply, reply-drafter, research-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, email-drafter, writing-ops-handoff-brief-writer, reply-polisher |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, public-brainstorming, email-ops-scenario-planner, privacy-risk-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | - | - | `ux-ops-risk-reviewer` | wrong | ux-ops-risk-reviewer, api-design-reviewer, api-ops-evidence-grounder, api-ops-quality-auditor, travel-ops-risk-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, repo-ops-risk-reviewer, docs-ops-risk-reviewer, research-ops-risk-reviewer, contract-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | - | - | `environment-config-auditor` | wrong | environment-config-auditor, migration-risk-auditor, webhook-setup-planner, database-ops-handoff-brief-writer, web-ops-monitoring-plan-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, agent-ops-compliance-checker, api-ops-compliance-checker, policy-compliance-checker, security-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `analytics-ops-evidence-grounder` | wrong | analytics-ops-evidence-grounder, analytics-ops-risk-reviewer, analytics-ops-compliance-checker, search-ops-compliance-checker, analytics-ops-timeline-builder |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, search-ops-handoff-brief-writer, task-extractor, knowledge-ops-handoff-brief-writer |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-xlsx` | wrong | public-xlsx, data-analysis-with-validation, data-analysis-for-root-cause-diagnosis, analytics-ops-artifact-packager, data-analysis-for-reporting |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, task-extractor, thesis-ops-handoff-brief-writer, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, document-field-extractor, agent-ops-field-extractor, knowledge-ops-field-extractor, operations-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, email-polisher, groupwork-reply, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | - | - | `paper-summariser` | wrong | paper-summariser, agent-ops-resource-linker, general-source-summariser, document-summariser, research-ops-summary-writer |
