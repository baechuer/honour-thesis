# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 25.0% |
| Acceptable top-1 accuracy | 25.0% |
| Top-3 recall | 58.3% |
| Top-5 recall | 66.7% |
| Acceptable top-5 recall | 66.7% |
| MRR | 0.421 |
| Non-main top-1 | 33.3% |
| Approx selector-visible tokens | 497146 |

## API Usage Estimate

- Embedding API calls made in this run: 12
- Embedding cache hits: 1006
- Approx uncached embedding input tokens: 214
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-handoff-brief-writer, travel-ops-risk-reviewer, travel-ops-monitoring-plan-builder, travel-ops-normalizer |
| `low_doc_get_details` | `document-field-extractor` | 11 | 11 | `vendor-ops-summary-writer` | wrong | vendor-ops-summary-writer, finance-ops-summary-writer, document-summariser, events-ops-summary-writer, support-ops-summary-writer |
| `low_doc_clean_up` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, web-form-filler, email-action-extractor, email-drafter, web-ops-rewrite-editor |
| `low_data_check_sheet` | `data-analysis-overview` | 3 | 3 | `data-analysis-with-anomaly-focus` | borderline | data-analysis-with-anomaly-focus, dataset-ops-quality-auditor, data-analysis-overview, dataset-ops-timeline-builder, dataset-ops-summary-writer |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | 3 | 3 | `data-analysis-with-validation` | wrong | data-analysis-with-validation, data-analysis-overview, data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, dataset-ops-compliance-checker |
| `low_code_check_change` | `pr-reviewer` | 2 | 2 | `version-control-helper` | wrong | version-control-helper, pr-reviewer, data-analysis-with-validation, support-ops-acceptance-test-builder, operations-ops-acceptance-test-builder |
| `low_code_red_build` | `ci-failure-debugger` | 20 | 20 | `changelog-writer` | wrong | changelog-writer, release-note-writer, review-comment-resolver, ci-cd-pipeline-builder, webhook-setup-planner |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, source-grounding-extractor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-handoff-brief-writer, meeting-ops-field-extractor |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, professor-email-reply, followup-reply-writer, groupwork-reply |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `lab-ops-risk-reviewer` | wrong | lab-ops-risk-reviewer, web-ops-risk-reviewer, community-ops-risk-reviewer, personal-ops-risk-reviewer, events-ops-risk-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, skill-installer, skill-editor, skill-packager |
