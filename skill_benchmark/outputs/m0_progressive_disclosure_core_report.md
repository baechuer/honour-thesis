# M0 Progressive Disclosure Baseline Report

- Manifest: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/runtime/m0_results_core_current/manifest.csv`
- Runs: 67; unique prompts: 67
- Strict top-1 accuracy: 61.2%
- Acceptable top-1 accuracy: 61.2%
- Strict any-hit rate: 64.2%
- Acceptable any-hit rate: 64.2%
- No explicit skill loaded: 31.3%
- Wrong top-1 rate: 7.5%
- Mean full skill docs loaded: 0.78
- Multi-skill consultation rate: 7.5%

Interpretation: M0 measures the normal main-agent progressive-disclosure behavior. It is not a clean retriever-only test, because the main agent may answer directly, load no explicit skill, or load multiple full skill documents before responding.

## By Family

| Family | N | Strict Top-1 | Accept Top-1 | Strict Any-Hit | Accept Any-Hit | No Skill | Multi-Skill |
|---|---:|---:|---:|---:|---:|---:|---:|
| `browser_web_automation` | 6 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 0.0% |
| `code_github_workflow` | 6 | 16.7% | 16.7% | 16.7% | 16.7% | 83.3% | 0.0% |
| `data_spreadsheet` | 7 | 28.6% | 28.6% | 28.6% | 28.6% | 71.4% | 0.0% |
| `documents_files` | 7 | 71.4% | 71.4% | 71.4% | 71.4% | 28.6% | 0.0% |
| `metrics_observability` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 0.0% | 0.0% |
| `planning_meetings` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 20.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 25.0% | 12.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 33.3% | 0.0% |
| `skill_lifecycle` | 6 | 33.3% | 33.3% | 50.0% | 50.0% | 33.3% | 50.0% |

## Non-Gold Top-1 Outcomes

- `news-briefing-writer -> document-converter`: 1
- `general-source-summariser -> document-summariser`: 1
- `document-extractor -> document-field-extractor`: 1
- `skill-editor -> document-extractor`: 1
- `skill-packager -> paper-summariser`: 1

## Prompt-Level Results

| Prompt | Family | Gold | Top-1 | Status | Selected Skills |
|---|---|---|---|---|---|
| `reply_p1_professor_reply` | `reply_messaging` | `professor-email-reply` | `professor-email-reply` | gold | `professor-email-reply` |
| `reply_p2_polish_supervisor` | `reply_messaging` | `reply-polisher` | `reply-polisher` | gold | `reply-polisher` |
| `reply_p3_groupwork_coordination` | `reply_messaging` | `groupwork-reply` | `groupwork-reply` | gold | `groupwork-reply` |
| `reply_p4_followup_commitment` | `reply_messaging` | `followup-reply-writer` | `followup-reply-writer` | gold | `followup-reply-writer` |
| `reply_p5_generic_fresh_draft` | `reply_messaging` | `reply-drafter` | `reply-drafter` | gold | `reply-drafter` |
| `web_p1_page_snapshot` | `browser_web_automation` | `web-page-snapshotter` | `web-page-snapshotter` | gold | `web-page-snapshotter` |
| `web_p2_form_filling` | `browser_web_automation` | `web-form-filler` | `<none>` | no_explicit_skill | `<none>` |
| `web_p3_ui_test` | `browser_web_automation` | `web-ui-tester` | `web-ui-tester` | gold | `web-ui-tester` |
| `web_p4_data_extraction` | `browser_web_automation` | `web-data-extractor` | `<none>` | no_explicit_skill | `<none>` |
| `web_p5_frontend_debugging` | `browser_web_automation` | `frontend-debugger` | `<none>` | no_explicit_skill | `<none>` |
| `web_p6_accessibility_check` | `browser_web_automation` | `accessibility-checker` | `accessibility-checker` | gold | `accessibility-checker` |
| `code_p1_local_code_review` | `code_github_workflow` | `code-reviewer` | `<none>` | no_explicit_skill | `<none>` |
| `code_p2_pr_review` | `code_github_workflow` | `pr-reviewer` | `<none>` | no_explicit_skill | `<none>` |
| `code_p3_review_comment_resolution` | `code_github_workflow` | `review-comment-resolver` | `<none>` | no_explicit_skill | `<none>` |
| `code_p4_ci_failure_debugging` | `code_github_workflow` | `ci-failure-debugger` | `<none>` | no_explicit_skill | `<none>` |
| `code_p5_changelog_entry` | `code_github_workflow` | `changelog-writer` | `<none>` | no_explicit_skill | `<none>` |
| `code_p6_release_notes` | `code_github_workflow` | `release-note-writer` | `release-note-writer` | gold | `release-note-writer` |
| `data_p1_overview` | `data_spreadsheet` | `data-analysis-overview` | `<none>` | no_explicit_skill | `<none>` |
| `data_p2_anomaly_focus` | `data_spreadsheet` | `data-analysis-with-anomaly-focus` | `<none>` | no_explicit_skill | `<none>` |
| `data_p3_validation` | `data_spreadsheet` | `data-analysis-with-validation` | `<none>` | no_explicit_skill | `<none>` |
| `data_p4_root_cause` | `data_spreadsheet` | `data-analysis-for-root-cause-diagnosis` | `<none>` | no_explicit_skill | `<none>` |
| `data_p5_reporting` | `data_spreadsheet` | `data-analysis-for-reporting` | `<none>` | no_explicit_skill | `<none>` |
| `data_p6_forecasting` | `data_spreadsheet` | `data-analysis-for-forecasting` | `data-analysis-for-forecasting` | gold | `data-analysis-for-forecasting` |
| `data_p7_ranking_selection` | `data_spreadsheet` | `data-analysis-for-ranking-selection` | `data-analysis-for-ranking-selection` | gold | `data-analysis-for-ranking-selection` |
| `doc_p1_document_summary` | `documents_files` | `document-summariser` | `document-summariser` | gold | `document-summariser` |
| `doc_p2_document_rewriter` | `documents_files` | `document-rewriter` | `document-rewriter` | gold | `document-rewriter` |
| `doc_p3_document_normaliser` | `documents_files` | `document-normaliser` | `<none>` | no_explicit_skill | `<none>` |
| `doc_p4_field_extraction` | `documents_files` | `document-field-extractor` | `<none>` | no_explicit_skill | `<none>` |
| `doc_p5_comparison_preparation` | `documents_files` | `multi-document-comparison-preparer` | `multi-document-comparison-preparer` | gold | `multi-document-comparison-preparer` |
| `doc_p6_conversion` | `documents_files` | `document-converter` | `document-converter` | gold | `document-converter` |
| `doc_p7_layout_preserving_conversion` | `documents_files` | `layout-preserving-converter` | `layout-preserving-converter` | gold | `layout-preserving-converter` |
| `obs_p1_metrics_overview` | `metrics_observability` | `metrics-overview` | `metrics-overview` | gold | `metrics-overview` |
| `obs_p2_latency_anomaly` | `metrics_observability` | `latency-anomaly-detector` | `latency-anomaly-detector` | gold | `latency-anomaly-detector` |
| `obs_p3_slo_breach` | `metrics_observability` | `slo-breach-checker` | `slo-breach-checker` | gold | `slo-breach-checker` |
| `obs_p4_capacity_risk` | `metrics_observability` | `capacity-risk-forecaster` | `capacity-risk-forecaster` | gold | `capacity-risk-forecaster` |
| `obs_p5_root_cause` | `metrics_observability` | `metrics-root-cause-diagnoser` | `metrics-root-cause-diagnoser` | gold | `metrics-root-cause-diagnoser` |
| `obs_p6_incident_summary` | `metrics_observability` | `incident-summary-writer` | `incident-summary-writer` | gold | `incident-summary-writer` |
| `news_p1_plain_summary` | `news_monitoring` | `news-summariser` | `news-summariser` | gold | `news-summariser` |
| `news_p2_briefing` | `news_monitoring` | `news-briefing-writer` | `document-converter` | wrong | `document-converter` |
| `news_p3_grounded_claims` | `news_monitoring` | `source-grounding-extractor` | `source-grounding-extractor` | gold | `source-grounding-extractor` |
| `news_p4_theme_extraction` | `news_monitoring` | `news-theme-extractor` | `news-theme-extractor` | gold | `news-theme-extractor` |
| `news_p5_trend_signal` | `news_monitoring` | `tech-news-trend-extractor` | `tech-news-trend-extractor` | gold | `tech-news-trend-extractor` |
| `plan_p1_meeting_agenda` | `planning_meetings` | `meeting-agenda-builder` | `meeting-agenda-builder` | gold | `meeting-agenda-builder`, `weekly-planner` |
| `plan_p2_meeting_summary` | `planning_meetings` | `meeting-summary-writer` | `meeting-summary-writer` | gold | `meeting-summary-writer` |
| `plan_p3_meeting_followup` | `planning_meetings` | `meeting-followup-extractor` | `meeting-followup-extractor` | gold | `meeting-followup-extractor` |
| `plan_p4_task_extractor` | `planning_meetings` | `task-extractor` | `task-extractor` | gold | `task-extractor` |
| `plan_p5_weekly_planner` | `planning_meetings` | `weekly-planner` | `weekly-planner` | gold | `weekly-planner` |
| `read_p1_paper_summary` | `reading_research` | `paper-summariser` | `paper-summariser` | gold | `paper-summariser` |
| `read_p2_general_source_summary` | `reading_research` | `general-source-summariser` | `document-summariser` | wrong | `document-summariser`, `general-source-summariser` |
| `read_p3_citation_notes` | `reading_research` | `citation-note-extractor` | `citation-note-extractor` | gold | `citation-note-extractor` |
| `read_p4_document_extraction` | `reading_research` | `document-extractor` | `document-field-extractor` | wrong | `document-field-extractor` |
| `read_p5_method_notes` | `reading_research` | `method-note-builder` | `method-note-builder` | gold | `method-note-builder` |
| `read_p6_grounding_check` | `reading_research` | `citation-grounding-helper` | `<none>` | no_explicit_skill | `<none>` |
| `read_p7_multi_source_comparison` | `reading_research` | `multi-source-comparison-builder` | `<none>` | no_explicit_skill | `<none>` |
| `read_p8_related_work_synthesis` | `reading_research` | `related-work-synthesiser` | `related-work-synthesiser` | gold | `related-work-synthesiser` |
| `sec_p1_threat_model` | `security_appsec` | `security-threat-modeler` | `security-threat-modeler` | gold | `security-threat-modeler` |
| `sec_p2_security_code_review` | `security_appsec` | `security-code-reviewer` | `<none>` | no_explicit_skill | `<none>` |
| `sec_p3_dependency_risk` | `security_appsec` | `dependency-risk-auditor` | `dependency-risk-auditor` | gold | `dependency-risk-auditor` |
| `sec_p4_secret_leak` | `security_appsec` | `secret-leak-scanner` | `<none>` | no_explicit_skill | `<none>` |
| `sec_p5_auth_flow` | `security_appsec` | `auth-flow-reviewer` | `auth-flow-reviewer` | gold | `auth-flow-reviewer` |
| `sec_p6_privacy_review` | `security_appsec` | `privacy-risk-reviewer` | `privacy-risk-reviewer` | gold | `privacy-risk-reviewer` |
| `skill_p1_find_existing` | `skill_lifecycle` | `skill-finder` | `<none>` | no_explicit_skill | `<none>` |
| `skill_p2_install_existing` | `skill_lifecycle` | `skill-installer` | `<none>` | no_explicit_skill | `<none>` |
| `skill_p3_create_new` | `skill_lifecycle` | `skill-creator` | `skill-creator` | gold | `skill-creator` |
| `skill_p4_edit_existing` | `skill_lifecycle` | `skill-editor` | `document-extractor` | wrong | `document-extractor`, `skill-finder`, `document-summariser` |
| `skill_p5_evaluate_existing` | `skill_lifecycle` | `skill-evaluator` | `skill-evaluator` | gold | `skill-evaluator`, `reply-polisher` |
| `skill_p6_package_existing` | `skill_lifecycle` | `skill-packager` | `paper-summariser` | wrong | `paper-summariser`, `skill-packager` |
