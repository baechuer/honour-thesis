# Offline Selector Evaluation Report

This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.

## Scale Regimes

- `core`: 85 skills, approx selector-visible tokens per method vary by representation.
- `current_full`: 2349 skills, approx selector-visible tokens per method vary by representation.

## Method Summary

| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | `core` | 85 | 4869 | 76.5% | 76.5% | 92.9% | 92.9% | 95.3% | 95.3% | 0.843 | 0.843 | 1.57 | 7.1% | 0.0% | 110.82 |
| `m1_tfidf_flat` | `core` | 85 | 4869 | 75.3% | 75.3% | 92.9% | 92.9% | 95.3% | 95.3% | 0.841 | 0.841 | 1.76 | 9.4% | 0.0% | 1241.83 |
| `m3_tfidf_schema` | `core` | 85 | 35791 | 84.7% | 84.7% | 96.5% | 96.5% | 100.0% | 100.0% | 0.912 | 0.912 | 1.25 | 7.1% | 0.0% | 90.2 |
| `m6_bm25_schema_rerank` | `core` | 85 | 13454 | 80.0% | 80.0% | 96.5% | 96.5% | 97.7% | 97.7% | 0.881 | 0.881 | 1.23 | 3.5% | 0.0% | 333.24 |
| `m6_tfidf_schema_rerank` | `core` | 85 | 13454 | 84.7% | 84.7% | 96.5% | 96.5% | 97.7% | 97.7% | 0.907 | 0.907 | 1.3 | 3.5% | 0.0% | 260.39 |
| `m1_bm25_flat` | `current_full` | 2349 | 120024 | 68.2% | 68.2% | 82.3% | 82.3% | 87.1% | 87.1% | 0.765 | 0.765 | 2.0 | 5.9% | 15.3% | 2509.13 |
| `m1_tfidf_flat` | `current_full` | 2349 | 120024 | 58.8% | 58.8% | 76.5% | 77.6% | 78.8% | 80.0% | 0.688 | 0.692 | 2.24 | 7.1% | 28.2% | 172.42 |
| `m3_tfidf_schema` | `current_full` | 2349 | 619548 | 76.5% | 76.5% | 90.6% | 90.6% | 94.1% | 94.1% | 0.845 | 0.845 | 1.41 | 7.1% | 10.6% | 636.33 |
| `m6_bm25_schema_rerank` | `current_full` | 2349 | 126020 | 78.8% | 78.8% | 90.6% | 90.6% | 91.8% | 91.8% | 0.851 | 0.851 | 1.46 | 1.2% | 5.9% | 2742.42 |
| `m6_tfidf_schema_rerank` | `current_full` | 2349 | 126020 | 74.1% | 74.1% | 84.7% | 84.7% | 87.1% | 87.1% | 0.799 | 0.801 | 1.29 | 3.5% | 14.1% | 387.56 |

Accept metrics count documented acceptable alternatives as correct, while strict metrics require the controlled gold label.

## Benchmark Pressure Read

- `m1_bm25_flat` on `core`: useful pressure
- `m1_tfidf_flat` on `core`: useful pressure
- `m3_tfidf_schema` on `core`: useful pressure
- `m6_bm25_schema_rerank` on `core`: useful pressure
- `m6_tfidf_schema_rerank` on `core`: useful pressure
- `m1_bm25_flat` on `current_full`: useful pressure
- `m1_tfidf_flat` on `current_full`: useful pressure
- `m3_tfidf_schema` on `current_full`: useful pressure
- `m6_bm25_schema_rerank` on `current_full`: useful pressure
- `m6_tfidf_schema_rerank` on `current_full`: useful pressure

## Scale Sensitivity

This table compares the controlled core with the current full library. A useful scale condition should create some degradation or non-core false positives without making retrieval random.

| Method | Core Top-1 | Full Top-1 | Full Accept Top-1 | Top-1 Delta | Core Top-5 | Full Top-5 | Full Accept Top-5 | Top-5 Delta | Core MRR | Full MRR | Full Accept MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | 76.5% | 68.2% | 68.2% | -8.2% | 95.3% | 87.1% | 87.1% | -8.2% | 0.843 | 0.765 | 0.765 | 15.3% |
| `m1_tfidf_flat` | 75.3% | 58.8% | 58.8% | -16.5% | 95.3% | 78.8% | 80.0% | -16.5% | 0.841 | 0.688 | 0.692 | 28.2% |
| `m3_tfidf_schema` | 84.7% | 76.5% | 76.5% | -8.2% | 100.0% | 94.1% | 94.1% | -5.9% | 0.912 | 0.845 | 0.845 | 10.6% |
| `m6_bm25_schema_rerank` | 80.0% | 78.8% | 78.8% | -1.2% | 97.7% | 91.8% | 91.8% | -5.9% | 0.881 | 0.851 | 0.851 | 5.9% |
| `m6_tfidf_schema_rerank` | 84.7% | 74.1% | 74.1% | -10.6% | 97.7% | 87.1% | 87.1% | -10.6% | 0.907 | 0.799 | 0.801 | 14.1% |

## M0 Progressive Disclosure Baseline

- Existing trace manifest: `skill_benchmark/runtime/confusability_results/manifest.csv`
- Runs: 129; prompts: 43
- Top-1 accuracy: 68.2%
- Any-hit rate: 69.8%
- No explicit skill loaded: 21.7%
- Mean full docs loaded: 0.83
- Note: Loaded from the supplied M0 manifest. Use the dedicated M0 report for no-skill and prompt-level failure breakdown.

Required M0 trace fields for future runs:

- `prompt_id`, `gold_skill`, `selected_skills`, `full_docs_loaded`, `selector_visible_tokens`, `final_context_tokens`, `latency_ms`, `cost_estimate`, `failure_mode`

## Family Breakdown

### `m1_bm25_flat` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 85.7% | 85.7% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `data-analysis-with-validation -> accessibility-checker`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> ci-failure-debugger`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> web-data-extractor`: 1
- `layout-preserving-converter -> document-converter`: 1

### `m1_tfidf_flat` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `service-dependency-mapper -> web-performance-budget-checker`: 1
- `web-form-filler -> web-ui-tester`: 1
- `web-ui-tester -> web-page-snapshotter`: 1
- `web-data-extractor -> web-page-snapshotter`: 1
- `deployment-build-triager -> data-analysis-for-root-cause-diagnosis`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> meeting-followup-extractor`: 1

### `m3_tfidf_schema` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 87.5% | 87.5% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 100.0% | 100.0% |
| `skill_lifecycle` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `incident-summary-writer -> metrics-overview`: 1
- `news-briefing-writer -> news-summariser`: 1
- `weekly-planner -> meeting-agenda-builder`: 1
- `document-extractor -> web-data-extractor`: 1
- `multi-source-comparison-builder -> paper-summariser`: 1
- `followup-reply-writer -> document-summariser`: 1

### `m6_bm25_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> ci-failure-debugger`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> web-data-extractor`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `slo-breach-checker -> pr-reviewer`: 1

### `m6_tfidf_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 57.1% | 57.1% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 87.5% | 87.5% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `service-dependency-mapper -> web-performance-budget-checker`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `metrics-root-cause-diagnoser -> data-analysis-for-root-cause-diagnosis`: 1
- `meeting-summary-writer -> meeting-agenda-builder`: 1
- `meeting-followup-extractor -> meeting-agenda-builder`: 1

### `m1_bm25_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 14.3% | 14.3% | 57.1% | 57.1% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `office_artifact_workflows` | 6 | 50.0% | 50.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 40.0% | 40.0% | 40.0% | 40.0% |
| `reading_research` | 8 | 37.5% | 37.5% | 50.0% | 50.0% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `web-form-filler -> public-n-skills-dev-browser`: 1
- `pr-reviewer -> pr-description-writer`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `data-analysis-for-reporting -> public-office-data-analysis`: 1
- `deployment-build-triager -> public-netlify-deploy`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1

### `m1_tfidf_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 50.0% | 50.0% | 66.7% | 83.3% | 66.7% | 83.3% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 71.4% | 71.4% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 40.0% | 40.0% | 60.0% | 60.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `skill_lifecycle` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `external-api-integration-planner -> public-openai-figma-code-connect-components`: 1
- `webhook-contract-planner -> invoice-payment-checker`: 1
- `service-dependency-mapper -> public-office-microsoft-teams`: 1
- `web-form-filler -> variance-analysis-helper`: 1
- `web-ui-tester -> variance-analysis-helper`: 1
- `web-data-extractor -> product-ops-resource-linker`: 1
- `data-analysis-with-validation -> public-addy-web-web-quality-audit`: 1
- `data-analysis-for-ranking-selection -> decision-matrix-builder`: 1

### `m3_tfidf_schema` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 60.0% | 60.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 75.0% | 75.0% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |

Top confusions:
- `service-dependency-mapper -> public-office-microsoft-teams`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `code-reviewer -> git-commit-writer`: 1
- `deployment-build-triager -> public-netlify-deploy`: 1
- `document-field-extractor -> invoice-payment-checker`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `metrics-overview -> public-mattpocock-triage`: 1
- `incident-summary-writer -> metrics-overview`: 1

### `m6_bm25_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> metrics-root-cause-diagnoser`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> receipt-extractor`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `slo-breach-checker -> risk-ops-acceptance-test-builder`: 1

### `m6_tfidf_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 42.9% | 42.9% | 85.7% | 85.7% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 60.0% | 60.0% | 60.0% | 60.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 75.0% | 75.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 66.7% | 66.7% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `service-dependency-mapper -> analytics-ops-quality-auditor`: 1
- `web-data-extractor -> product-ops-field-extractor`: 1
- `data-analysis-for-ranking-selection -> decision-matrix-builder`: 1
- `deployment-build-triager -> public-netlify-deploy`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> receipt-extractor`: 1
- `document-converter -> office-to-markdown-converter`: 1

## Prompt-Level Results

### `m1_bm25_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, skill-editor, webhook-contract-planner, frontend-debugger |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, database-migration-risk-assessor, professor-email-reply, openapi-contract-reviewer, webhook-contract-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, data-analysis-with-validation, web-ui-tester, accessibility-checker, followup-reply-writer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, security-threat-modeler, dependency-risk-auditor, data-analysis-with-validation, data-analysis-for-forecasting |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, dependency-risk-auditor, openapi-contract-reviewer, task-extractor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, data-analysis-for-reporting, architecture-boundary-reviewer, skill-evaluator, web-performance-budget-checker |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, web-form-filler, deployment-release-verifier |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, multi-document-comparison-preparer, document-summariser, deployment-release-verifier |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, skill-evaluator, webhook-contract-planner, web-page-snapshotter, data-analysis-with-validation |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, release-note-writer, web-page-snapshotter, pdf-layout-reviewer, office-to-markdown-converter |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, pdf-layout-reviewer, metrics-root-cause-diagnoser, external-api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, web-form-filler, reply-drafter, slo-breach-checker |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, release-note-writer, dependency-risk-auditor, reply-drafter, changelog-writer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, openapi-contract-reviewer, database-migration-risk-assessor, review-comment-resolver, code-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, code-reviewer, reply-drafter, professor-email-reply, pr-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, openapi-contract-reviewer, frontend-debugger, code-reviewer, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, citation-note-extractor, code-reviewer, incident-summary-writer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, slo-breach-checker, news-theme-extractor, data-analysis-for-reporting, review-comment-resolver |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, citation-note-extractor, data-analysis-for-forecasting, incident-summary-writer, followup-reply-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, latency-anomaly-detector, general-source-summariser, release-note-writer |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `accessibility-checker` | wrong | accessibility-checker, data-analysis-with-validation, slo-breach-checker, data-analysis-with-anomaly-focus, pdf-layout-reviewer |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 3 | 3 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-for-root-cause-diagnosis, data-analysis-with-validation, frontend-debugger |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, citation-note-extractor, multi-document-comparison-preparer, spreadsheet-formula-auditor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, followup-reply-writer, metrics-root-cause-diagnoser, incident-summary-writer, meeting-followup-extractor |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, pdf-layout-reviewer, meeting-followup-extractor, meeting-summary-writer, release-note-writer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-performance-budget-checker, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, data-analysis-for-ranking-selection, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, web-form-filler, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 11 | 11 | `ci-failure-debugger` | wrong | ci-failure-debugger, metrics-root-cause-diagnoser, frontend-debugger, data-analysis-with-validation, security-threat-modeler |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, deployment-build-triager, release-note-writer, web-performance-budget-checker, citation-grounding-helper |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, deployment-build-triager, general-source-summariser, data-analysis-with-validation |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `general-source-summariser` | wrong | general-source-summariser, citation-note-extractor, data-analysis-with-validation, document-summariser, skill-finder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, docx-redline-editor, pdf-layout-reviewer, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 3 | 3 | `layout-preserving-converter` | wrong | layout-preserving-converter, docx-redline-editor, document-normaliser, pdf-layout-reviewer, document-rewriter |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-field-extractor, document-extractor, meeting-followup-extractor, pdf-layout-reviewer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, visual-regression-checker, pdf-layout-reviewer, document-normaliser |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `document-converter` | wrong | document-converter, layout-preserving-converter, pdf-layout-reviewer, office-to-markdown-converter, visual-regression-checker |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, related-work-synthesiser, architecture-boundary-reviewer, latency-anomaly-detector, service-dependency-mapper |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, slo-breach-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 3 | 3 | `metrics-overview` | wrong | metrics-overview, architecture-boundary-reviewer, slo-breach-checker, pr-reviewer, web-performance-budget-checker |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, metrics-root-cause-diagnoser, slo-breach-checker, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, deployment-build-triager, service-dependency-mapper, frontend-debugger |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, incident-summary-writer, metrics-overview, dependency-risk-auditor, metrics-root-cause-diagnoser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, paper-summariser, document-summariser, source-grounding-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, data-analysis-for-reporting, document-summariser, meeting-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 4 | 4 | `citation-note-extractor` | wrong | citation-note-extractor, document-field-extractor, document-extractor, source-grounding-extractor, document-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, secret-leak-scanner, data-analysis-for-forecasting, news-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-summariser, capacity-risk-forecaster, news-theme-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, skill-finder, web-page-snapshotter, slo-breach-checker, accessibility-checker |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, slide-deck-visual-auditor, document-converter, task-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, layout-preserving-converter, multi-document-comparison-preparer, review-comment-resolver, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, data-analysis-with-validation, citation-grounding-helper, slo-breach-checker |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, office-to-markdown-converter, deployment-release-verifier, visual-regression-checker |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, document-converter, docx-redline-editor, changelog-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, followup-reply-writer, incident-summary-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, general-source-summariser, paper-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, followup-reply-writer, meeting-followup-extractor, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, release-note-writer, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 12 | 12 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, skill-evaluator, meeting-summary-writer, meeting-followup-extractor, task-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, multi-source-comparison-builder, general-source-summariser, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, professor-email-reply, data-analysis-for-reporting, incident-summary-writer, groupwork-reply |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, method-note-builder, release-note-writer, incident-summary-writer |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, web-data-extractor, document-field-extractor, multi-document-comparison-preparer, weekly-planner |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, citation-grounding-helper, web-data-extractor, review-comment-resolver, data-analysis-for-reporting |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, skill-evaluator, citation-note-extractor, data-analysis-for-reporting, skill-creator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `news-briefing-writer` | wrong | news-briefing-writer, multi-source-comparison-builder, data-analysis-for-ranking-selection, tech-news-trend-extractor, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-document-comparison-preparer, release-note-writer, data-analysis-for-reporting, weekly-planner |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, followup-reply-writer, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, followup-reply-writer, reply-drafter, groupwork-reply |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, meeting-followup-extractor, web-ui-tester |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, meeting-followup-extractor, incident-summary-writer, reply-drafter, document-summariser |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `followup-reply-writer` | wrong | followup-reply-writer, reply-polisher, reply-drafter, citation-note-extractor, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, code-reviewer, skill-editor, skill-creator, reply-drafter |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, pr-reviewer, accessibility-checker, code-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, pr-reviewer, skill-installer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, deployment-release-verifier, webhook-contract-planner, skill-finder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, accessibility-checker, citation-grounding-helper, reply-drafter |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, reply-drafter, news-theme-extractor, pdf-ocr-extractor, web-data-extractor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, incident-summary-writer, meeting-followup-extractor, followup-reply-writer, skill-editor |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, code-reviewer, web-ui-tester, skill-packager, skill-finder |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, meeting-followup-extractor, skill-finder, skill-installer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, document-field-extractor, skill-evaluator, document-extractor, data-analysis-overview |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, citation-grounding-helper, skill-finder, reply-drafter |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, skill-finder, skill-creator, skill-installer |

### `m1_tfidf_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, review-comment-resolver, pr-reviewer, skill-editor |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, web-page-snapshotter, openapi-contract-reviewer, webhook-contract-planner, skill-evaluator |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, reply-drafter, reply-polisher, review-comment-resolver, database-migration-risk-assessor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, review-comment-resolver, skill-creator, security-threat-modeler, dependency-risk-auditor |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, dependency-risk-auditor, privacy-risk-reviewer, capacity-risk-forecaster, deployment-release-verifier |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `web-performance-budget-checker` | wrong | web-performance-budget-checker, skill-evaluator, data-analysis-for-reporting, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, metrics-overview, pdf-layout-reviewer, accessibility-interaction-auditor, changelog-writer |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `web-ui-tester` | wrong | web-ui-tester, web-form-filler, playwright-flow-debugger, data-analysis-with-validation, multi-document-comparison-preparer |
| `web_p3_ui_test` | `web-ui-tester` | 2 | 2 | `web-page-snapshotter` | wrong | web-page-snapshotter, web-ui-tester, reply-drafter, webhook-contract-planner, pdf-layout-reviewer |
| `web_p4_data_extraction` | `web-data-extractor` | 12 | 12 | `web-page-snapshotter` | wrong | web-page-snapshotter, pdf-layout-reviewer, release-note-writer, pdf-ocr-extractor, web-performance-budget-checker |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, external-api-integration-planner, pdf-layout-reviewer, data-analysis-for-root-cause-diagnosis |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, web-form-filler, layout-preserving-converter, pdf-layout-reviewer |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, review-comment-resolver, web-page-snapshotter, changelog-writer, privacy-risk-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, database-migration-risk-assessor, review-comment-resolver, external-api-integration-planner, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, ci-failure-debugger, followup-reply-writer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, openapi-contract-reviewer, data-analysis-for-root-cause-diagnosis, web-ui-tester |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, auth-flow-reviewer, web-ui-tester, citation-note-extractor |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, slo-breach-checker, web-ui-tester, docx-redline-editor, service-dependency-mapper |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-forecasting, spreadsheet-formula-auditor, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, latency-anomaly-detector, deployment-build-triager |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-for-ranking-selection, ci-failure-debugger, pdf-layout-reviewer |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-for-forecasting, data-analysis-for-reporting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, web-ui-tester, data-analysis-overview, release-note-writer, citation-note-extractor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, followup-reply-writer, capacity-risk-forecaster |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, database-migration-risk-assessor, release-note-writer, data-analysis-overview, meeting-followup-extractor |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, accessibility-interaction-auditor, web-page-snapshotter, web-performance-budget-checker |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, code-reviewer, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, frontend-debugger, data-analysis-with-anomaly-focus |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 5 | 5 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, frontend-debugger, ci-failure-debugger, deployment-build-triager |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-note-writer, data-analysis-for-root-cause-diagnosis, deployment-build-triager, slide-deck-visual-auditor |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pdf-ocr-extractor, deployment-build-triager, layout-preserving-converter |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, ci-failure-debugger, multi-document-comparison-preparer, multi-source-comparison-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, docx-redline-editor, pdf-layout-reviewer, document-converter |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, document-field-extractor, web-data-extractor, document-extractor, multi-document-comparison-preparer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, visual-regression-checker, document-normaliser, multi-source-comparison-builder, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, document-converter, pdf-layout-reviewer, visual-regression-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, visual-regression-checker |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, related-work-synthesiser, data-analysis-overview, architecture-boundary-reviewer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, data-analysis-overview, web-performance-budget-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, service-dependency-mapper, dependency-risk-auditor, privacy-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview, data-analysis-for-root-cause-diagnosis |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, service-dependency-mapper, dependency-risk-auditor |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, document-converter, document-summariser, multi-document-comparison-preparer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, document-field-extractor, citation-note-extractor, general-source-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, data-analysis-for-forecasting, news-summariser, general-source-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, dependency-risk-auditor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, web-page-snapshotter, pdf-ocr-extractor, layout-preserving-converter, accessibility-checker |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, web-page-snapshotter, document-converter, slide-deck-visual-auditor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, review-comment-resolver, document-normaliser, document-rewriter, layout-preserving-converter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, incident-summary-writer, architecture-boundary-reviewer, auth-flow-reviewer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, review-comment-resolver, pr-reviewer, visual-regression-checker |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, docx-redline-editor, document-converter, visual-regression-checker |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, task-extractor, groupwork-reply |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, task-extractor, general-source-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 3 | 3 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-summary-writer, task-extractor, meeting-agenda-builder, release-note-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 16 | 16 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, task-extractor, news-briefing-writer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, method-note-builder, professor-email-reply, news-briefing-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, professor-email-reply, document-converter, data-analysis-for-reporting |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, reply-drafter, ci-failure-debugger, source-grounding-extractor |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, multi-document-comparison-preparer, document-field-extractor, pdf-layout-reviewer, task-extractor |
| `read_p5_method_notes` | `method-note-builder` | 2 | 2 | `citation-grounding-helper` | wrong | citation-grounding-helper, method-note-builder, related-work-synthesiser, multi-source-comparison-builder, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, document-extractor, source-grounding-extractor, citation-note-extractor, web-performance-budget-checker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `related-work-synthesiser` | wrong | related-work-synthesiser, method-note-builder, citation-note-extractor, citation-grounding-helper, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, release-note-writer, multi-document-comparison-preparer, multi-source-comparison-builder, groupwork-reply |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, groupwork-reply, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, playwright-flow-debugger, deployment-release-verifier |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, news-briefing-writer, meeting-followup-extractor, incident-summary-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, document-summariser, citation-note-extractor |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, auth-flow-reviewer, external-api-integration-planner, skill-editor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, code-reviewer, data-analysis-with-validation |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, privacy-risk-reviewer, database-migration-risk-assessor, capacity-risk-forecaster, deployment-build-triager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, deployment-release-verifier, webhook-contract-planner, deployment-build-triager |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, release-note-writer, data-analysis-with-validation, accessibility-checker, reply-polisher |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 12 | 12 | `web-data-extractor` | wrong | web-data-extractor, data-analysis-for-reporting, release-note-writer, data-analysis-for-ranking-selection, data-analysis-for-forecasting |
| `skill_p1_find_existing` | `skill-finder` | 3 | 3 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-agenda-builder, skill-finder, skill-editor, skill-creator |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, code-reviewer, spreadsheet-formula-auditor, skill-finder, multi-source-comparison-builder |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, meeting-followup-extractor, skill-finder, skill-installer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-finder, skill-installer, skill-evaluator, skill-packager |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, skill-installer, skill-editor, skill-finder |

### `m3_tfidf_schema` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, webhook-contract-planner, auth-flow-reviewer, pr-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, webhook-contract-planner, web-page-snapshotter, code-reviewer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, external-api-integration-planner, followup-reply-writer, reply-drafter, playwright-flow-debugger |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, data-analysis-for-forecasting, groupwork-reply, security-threat-modeler, dependency-risk-auditor |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, dependency-risk-auditor, playwright-flow-debugger, openapi-contract-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, architecture-boundary-reviewer, web-performance-budget-checker, data-analysis-for-forecasting, privacy-risk-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-data-extractor, pdf-layout-reviewer, metrics-overview, pdf-ocr-extractor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, frontend-debugger, web-data-extractor, document-converter |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, web-data-extractor, web-form-filler, pdf-layout-reviewer |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, pdf-layout-reviewer, pdf-ocr-extractor, layout-preserving-converter |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, web-ui-tester, webhook-contract-planner, openapi-contract-reviewer |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, layout-preserving-converter, release-note-writer, web-ui-tester |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, changelog-writer, ci-failure-debugger, pr-reviewer, web-page-snapshotter |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, code-reviewer, database-migration-risk-assessor, openapi-contract-reviewer, review-comment-resolver |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, ci-failure-debugger, changelog-writer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, frontend-debugger, auth-flow-reviewer, deployment-build-triager, changelog-writer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, code-reviewer, pr-reviewer, auth-flow-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, slo-breach-checker, deployment-release-verifier, capacity-risk-forecaster |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-reporting, spreadsheet-formula-auditor, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, deployment-build-triager, ci-failure-debugger, metrics-root-cause-diagnoser |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, data-analysis-with-anomaly-focus, web-data-extractor, data-analysis-for-ranking-selection, spreadsheet-formula-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-with-validation, data-analysis-with-anomaly-focus |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, data-analysis-with-validation, release-note-writer, data-analysis-for-root-cause-diagnosis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, architecture-boundary-reviewer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, data-analysis-overview, data-analysis-for-forecasting, metrics-overview, data-analysis-for-root-cause-diagnosis |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, web-ui-tester, web-page-snapshotter |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, web-page-snapshotter, accessibility-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, frontend-debugger, playwright-flow-debugger, deployment-build-triager |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, frontend-debugger, ci-failure-debugger, secret-leak-scanner, deployment-release-verifier |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-note-writer, database-migration-risk-assessor, deployment-build-triager, changelog-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, frontend-debugger, pdf-ocr-extractor, layout-preserving-converter |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, citation-note-extractor, metrics-overview, general-source-summariser, paper-summariser |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, document-normaliser, document-converter, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, docx-redline-editor, document-rewriter, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, web-data-extractor, document-extractor, method-note-builder, meeting-followup-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, citation-grounding-helper, release-note-writer, visual-regression-checker |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, pdf-layout-reviewer, layout-preserving-converter, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, document-converter, pdf-layout-reviewer, document-normaliser |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, latency-anomaly-detector, data-analysis-overview, service-dependency-mapper |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, web-performance-budget-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, capacity-risk-forecaster, dependency-risk-auditor, database-migration-risk-assessor |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, latency-anomaly-detector, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, slo-breach-checker, latency-anomaly-detector, capacity-risk-forecaster |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-theme-extractor, news-briefing-writer, tech-news-trend-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `news-summariser` | wrong | news-summariser, news-briefing-writer, news-theme-extractor, metrics-overview, webhook-contract-planner |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, general-source-summariser, news-briefing-writer, news-summariser, news-theme-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, source-grounding-extractor, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, source-grounding-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, web-data-extractor, web-page-snapshotter, office-to-markdown-converter |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, web-page-snapshotter, pdf-layout-reviewer, web-data-extractor, office-to-markdown-converter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, document-normaliser, review-comment-resolver, document-rewriter, code-reviewer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-data-extractor, skill-evaluator, incident-summary-writer, service-dependency-mapper |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, skill-evaluator, pdf-layout-reviewer, office-to-markdown-converter |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, docx-redline-editor, layout-preserving-converter, pdf-layout-reviewer, document-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-followup-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, task-extractor, weekly-planner |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, task-extractor, weekly-planner |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-followup-extractor, weekly-planner, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, task-extractor, meeting-summary-writer, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, method-note-builder, citation-note-extractor, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, professor-email-reply, data-analysis-for-reporting, citation-note-extractor |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, document-extractor, paper-summariser, multi-source-comparison-builder, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-extractor, document-summariser, method-note-builder, document-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, weekly-planner, multi-source-comparison-builder, citation-note-extractor, document-extractor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, document-extractor, citation-note-extractor, web-performance-budget-checker, source-grounding-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `paper-summariser` | wrong | paper-summariser, method-note-builder, related-work-synthesiser, citation-note-extractor, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, multi-source-comparison-builder, general-source-summariser, citation-grounding-helper |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, professor-email-reply, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, professor-email-reply, reply-drafter, followup-reply-writer, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, meeting-summary-writer, reply-drafter, meeting-followup-extractor |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 4 | 4 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, privacy-risk-reviewer, security-threat-modeler, skill-packager |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, security-threat-modeler, code-reviewer, pr-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, security-threat-modeler, architecture-boundary-reviewer, privacy-risk-reviewer, database-migration-risk-assessor |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, database-migration-risk-assessor, webhook-contract-planner, accessibility-interaction-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, release-note-writer, accessibility-checker, changelog-writer, data-analysis-for-root-cause-diagnosis |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 4 | 4 | `pdf-layout-reviewer` | wrong | pdf-layout-reviewer, data-analysis-with-validation, data-analysis-overview, privacy-risk-reviewer, data-analysis-for-root-cause-diagnosis |
| `skill_p1_find_existing` | `skill-finder` | 3 | 3 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-agenda-builder, skill-finder, skill-creator, skill-editor |
| `skill_p2_install_existing` | `skill-installer` | 2 | 2 | `skill-packager` | wrong | skill-packager, skill-installer, skill-finder, web-ui-tester, skill-creator |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-finder, meeting-followup-extractor, skill-editor, skill-installer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-creator, skill-finder, skill-installer, skill-evaluator |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, skill-creator, skill-installer, skill-finder |

### `m6_bm25_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, security-code-reviewer, code-reviewer, webhook-contract-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, web-ui-tester, professor-email-reply, openapi-contract-reviewer, database-migration-risk-assessor |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, data-analysis-with-validation, web-ui-tester, followup-reply-writer, spreadsheet-formula-auditor |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, dependency-risk-auditor, security-threat-modeler, pr-reviewer, data-analysis-for-forecasting |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, dependency-risk-auditor, spreadsheet-formula-auditor, capacity-risk-forecaster |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, data-analysis-for-reporting, privacy-risk-reviewer, web-performance-budget-checker, playwright-flow-debugger |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, web-data-extractor, accessibility-interaction-auditor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, document-field-extractor, multi-document-comparison-preparer, document-summariser |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, web-data-extractor, skill-evaluator, webhook-contract-planner |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, pdf-layout-reviewer, release-note-writer, pdf-ocr-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, pdf-layout-reviewer, metrics-root-cause-diagnoser, service-dependency-mapper |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, slo-breach-checker, layout-preserving-converter, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, changelog-writer, release-note-writer, review-comment-resolver, dependency-risk-auditor |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, review-comment-resolver, database-migration-risk-assessor, openapi-contract-reviewer, code-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, code-reviewer, pr-reviewer, reply-drafter, professor-email-reply |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, web-ui-tester, frontend-debugger, openapi-contract-reviewer, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, citation-note-extractor, deployment-release-verifier, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, slo-breach-checker, changelog-writer, review-comment-resolver, news-theme-extractor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-ranking-selection, citation-note-extractor, meeting-followup-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, deployment-build-triager, metrics-root-cause-diagnoser, ci-failure-debugger, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, slo-breach-checker, data-analysis-with-anomaly-focus, pdf-layout-reviewer |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, web-performance-budget-checker, data-analysis-for-reporting, data-analysis-with-validation |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, citation-grounding-helper, citation-note-extractor, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, followup-reply-writer, metrics-root-cause-diagnoser, meeting-followup-extractor, capacity-risk-forecaster |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, meeting-followup-extractor, task-extractor, data-analysis-for-forecasting, pr-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, auth-flow-reviewer |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, changelog-writer, review-comment-resolver, web-page-snapshotter |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, frontend-debugger, web-ui-tester |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 4 | 4 | `ci-failure-debugger` | wrong | ci-failure-debugger, metrics-root-cause-diagnoser, frontend-debugger, deployment-build-triager, data-analysis-with-validation |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-note-writer, deployment-build-triager, web-performance-budget-checker, playwright-flow-debugger |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pr-reviewer, code-reviewer, news-briefing-writer |
| `doc_p1_document_summary` | `document-summariser` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, document-summariser, citation-note-extractor, news-summariser, data-analysis-with-validation |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, docx-redline-editor, document-normaliser, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-layout-reviewer, document-rewriter, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-field-extractor, document-extractor, multi-document-comparison-preparer, method-note-builder |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, visual-regression-checker, document-normaliser, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, release-note-writer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, related-work-synthesiser |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 3 | 3 | `pr-reviewer` | wrong | pr-reviewer, metrics-overview, slo-breach-checker, architecture-boundary-reviewer, service-dependency-mapper |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, data-analysis-for-forecasting, metrics-root-cause-diagnoser, metrics-overview |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, deployment-build-triager |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, service-dependency-mapper, slo-breach-checker |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-theme-extractor, tech-news-trend-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, data-analysis-for-reporting, meeting-summary-writer, tech-news-trend-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, citation-note-extractor, document-extractor, document-summariser, document-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, secret-leak-scanner |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-theme-extractor, news-summariser, capacity-risk-forecaster |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, web-data-extractor, document-field-extractor, document-extractor, data-analysis-with-validation |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, web-page-snapshotter, document-converter, slide-deck-visual-auditor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, review-comment-resolver, multi-document-comparison-preparer, layout-preserving-converter, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, data-analysis-with-validation, web-ui-tester, pr-reviewer, citation-grounding-helper |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, visual-regression-checker, pr-reviewer, news-theme-extractor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, document-converter, changelog-writer, pdf-layout-reviewer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, followup-reply-writer, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, general-source-summariser, incident-summary-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, incident-summary-writer, meeting-summary-writer, followup-reply-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, meeting-agenda-builder, citation-note-extractor, weekly-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, weekly-planner, meeting-followup-extractor, skill-installer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, citation-note-extractor, general-source-summariser, incident-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, data-analysis-for-reporting, professor-email-reply, incident-summary-writer, news-theme-extractor |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, release-note-writer, task-extractor, incident-summary-writer, document-converter |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-extractor, document-field-extractor, multi-document-comparison-preparer, secret-leak-scanner |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, weekly-planner, data-analysis-with-validation, web-ui-tester, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, data-analysis-for-reporting, citation-note-extractor, task-extractor, skill-evaluator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `news-briefing-writer` | wrong | news-briefing-writer, multi-source-comparison-builder, data-analysis-for-ranking-selection, release-note-writer, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-document-comparison-preparer, release-note-writer, data-analysis-for-reporting, data-analysis-for-forecasting |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, reply-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, skill-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, meeting-followup-extractor, reply-drafter, groupwork-reply, incident-summary-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 2 | 2 | `followup-reply-writer` | wrong | followup-reply-writer, reply-drafter, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, code-reviewer, spreadsheet-formula-auditor, skill-creator, skill-editor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, accessibility-checker, data-analysis-with-validation |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, pr-reviewer, database-migration-risk-assessor |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, data-analysis-with-anomaly-focus, deployment-release-verifier, webhook-contract-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, changelog-writer, accessibility-checker, citation-grounding-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, changelog-writer, data-analysis-overview, reply-drafter, docx-redline-editor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, followup-reply-writer, incident-summary-writer, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, web-ui-tester, code-reviewer, skill-finder, data-analysis-for-reporting |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, skill-finder, meeting-followup-extractor, skill-installer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, document-field-extractor, skill-creator, skill-evaluator, document-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, skill-finder, reply-polisher, reply-drafter, skill-creator |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, skill-creator, skill-finder, skill-installer |

### `m6_tfidf_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, pr-reviewer, review-comment-resolver, webhook-contract-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, web-ui-tester, openapi-contract-reviewer, webhook-contract-planner, web-page-snapshotter |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, data-analysis-with-validation, reply-drafter, spreadsheet-formula-auditor, web-ui-tester |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, pr-reviewer, dependency-risk-auditor, security-threat-modeler, review-comment-resolver |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, dependency-risk-auditor, deployment-release-verifier, capacity-risk-forecaster, privacy-risk-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `web-performance-budget-checker` | wrong | web-performance-budget-checker, privacy-risk-reviewer, data-analysis-for-reporting, data-analysis-for-forecasting, playwright-flow-debugger |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, pdf-ocr-extractor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, document-summariser, multi-document-comparison-preparer |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, webhook-contract-planner, pdf-ocr-extractor, pdf-layout-reviewer |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, pdf-layout-reviewer, pdf-ocr-extractor, release-note-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, pdf-layout-reviewer, external-api-integration-planner, metrics-root-cause-diagnoser |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, layout-preserving-converter, web-form-filler, pdf-layout-reviewer |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, changelog-writer, review-comment-resolver, release-note-writer, privacy-risk-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, review-comment-resolver, database-migration-risk-assessor, external-api-integration-planner, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, reply-drafter, followup-reply-writer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, web-ui-tester, auth-flow-reviewer, frontend-debugger, openapi-contract-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, citation-note-extractor, deployment-release-verifier, web-ui-tester |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, deployment-release-verifier, slo-breach-checker, service-dependency-mapper |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-ranking-selection, spreadsheet-formula-auditor, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, deployment-build-triager, metrics-root-cause-diagnoser, ci-failure-debugger, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-with-anomaly-focus, pdf-layout-reviewer, secret-leak-scanner |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-for-forecasting, data-analysis-for-reporting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, citation-note-extractor, web-ui-tester, data-analysis-with-validation |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, dependency-risk-auditor, database-migration-risk-assessor, data-analysis-for-forecasting, task-extractor |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, accessibility-interaction-auditor, auth-flow-reviewer |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, changelog-writer, web-page-snapshotter, pdf-ocr-extractor |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, frontend-debugger, metrics-overview, web-form-filler |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, frontend-debugger, metrics-root-cause-diagnoser, ci-failure-debugger, data-analysis-for-root-cause-diagnosis |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-note-writer, deployment-build-triager, playwright-flow-debugger, web-performance-budget-checker |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pr-reviewer, news-briefing-writer, code-reviewer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, citation-note-extractor, news-summariser, multi-document-comparison-preparer |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-layout-reviewer, docx-redline-editor, document-rewriter |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, web-data-extractor, document-extractor, meeting-followup-extractor, multi-document-comparison-preparer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, visual-regression-checker, document-normaliser, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, visual-regression-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, document-converter, pdf-layout-reviewer, release-note-writer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, data-analysis-overview |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, data-analysis-with-anomaly-focus, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, service-dependency-mapper, dependency-risk-auditor, metrics-overview, capacity-risk-forecaster |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, data-analysis-for-forecasting, dependency-risk-auditor |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, data-analysis-for-reporting, service-dependency-mapper, dependency-risk-auditor |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, tech-news-trend-extractor, general-source-summariser, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, document-converter, data-analysis-for-reporting, tech-news-trend-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, document-summariser, citation-note-extractor, general-source-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, news-briefing-writer |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, source-grounding-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, web-data-extractor, pdf-ocr-extractor, web-page-snapshotter, document-field-extractor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, web-page-snapshotter, document-converter, task-extractor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, review-comment-resolver, multi-document-comparison-preparer, document-normaliser, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, pr-reviewer, incident-summary-writer, code-reviewer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, pr-reviewer, pdf-layout-reviewer, news-theme-extractor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, docx-redline-editor, document-converter, pdf-layout-reviewer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, task-extractor, slide-deck-visual-auditor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, general-source-summariser, incident-summary-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, incident-summary-writer, followup-reply-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, weekly-planner, meeting-followup-extractor, task-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, method-note-builder, incident-summary-writer, general-source-summariser |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, professor-email-reply, data-analysis-for-reporting, incident-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, release-note-writer, task-extractor, incident-summary-writer, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, document-field-extractor, web-data-extractor, multi-document-comparison-preparer, secret-leak-scanner |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, citation-grounding-helper, weekly-planner, review-comment-resolver, related-work-synthesiser |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, citation-note-extractor, source-grounding-extractor, web-performance-budget-checker, task-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, news-briefing-writer, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, release-note-writer, multi-document-comparison-preparer, multi-source-comparison-builder, office-to-markdown-converter |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, skill-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, meeting-followup-extractor, incident-summary-writer, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, dependency-risk-auditor, skill-creator, skill-editor, code-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, data-analysis-with-validation, accessibility-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, architecture-boundary-reviewer, database-migration-risk-assessor, capacity-risk-forecaster, deployment-build-triager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, deployment-release-verifier, webhook-contract-planner, pr-reviewer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, changelog-writer, release-note-writer, data-analysis-with-validation, accessibility-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 11 | 11 | `release-note-writer` | wrong | release-note-writer, changelog-writer, data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-root-cause-diagnosis |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-agenda-builder, followup-reply-writer, skill-creator |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, code-reviewer, web-ui-tester, skill-finder, data-analysis-for-reporting |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, skill-finder, meeting-followup-extractor, skill-installer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-finder, skill-creator, skill-installer, document-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, skill-finder, skill-editor |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, skill-finder, skill-installer, skill-creator |

### `m1_bm25_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, public-openai-gh-address-comments, public-addy-web-best-practices |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, public-swebench-security-review, openapi-contract-tester, public-openai-figma-code-connect-components |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, invoice-payment-checker, public-office-invoice-automation, api-design-reviewer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-addy-agent-api-and-interface-design, public-architecture-patterns, public-mattpocock-improve-codebase-architecture, agent-handoff-orchestrator |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, public-addy-agent-shipping-and-launch, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, privacy-policy-drafter, data-analysis-for-reporting, architecture-boundary-reviewer, skill-evaluator |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, public-n-skills-dev-browser, public-mattpocock-triage, pdf-layout-reviewer, public-openai-screenshot |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `public-n-skills-dev-browser` | wrong | public-n-skills-dev-browser, web-form-filler, public-office-pdf-form-filler, public-openai-playwright, web-ui-tester |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, dashboard-ops-acceptance-test-builder, skill-evaluator, bioinformatics-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, product-ops-resource-linker, pdf-layout-reviewer, office-to-markdown-converter |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, public-addy-agent-code-simplification, debugging-root-cause-helper, web-page-snapshotter, public-oh-my-changelog-maintenance |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, slo-breach-checker, reply-drafter, public-addy-web-accessibility |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, public-mattpocock-review, email-thread-summariser, public-addy-agent-spec-driven-development, public-oh-my-changelog-maintenance |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `pr-description-writer` | wrong | pr-description-writer, pr-reviewer, public-mattpocock-review, public-oh-my-changelog-maintenance, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-description-writer, public-openai-gh-address-comments, public-addy-agent-git-workflow-and-versioning, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, public-addy-agent-debugging-and-error-recovery, openapi-contract-reviewer, public-mattpocock-diagnose, frontend-debugger |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-oh-my-changelog-maintenance, public-swebench-changelog-automation, public-swebench-python-resilience |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, public-office-changelog-generator, pr-description-writer, public-n-skills-open-source-maintainer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, citation-note-extractor, data-analysis-for-forecasting, public-office-data-analysis, public-office-sheets-automation |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, debugging-root-cause-helper, public-addy-agent-debugging-and-error-recovery, public-huggingface-huggingface-papers, public-office-data-analysis |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-with-anomaly-focus, slo-breach-checker, public-openai-linear |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 17 | 17 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, public-office-data-analysis, variance-analysis-helper, public-office-stock-analysis, web-performance-budget-checker |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `public-office-data-analysis` | wrong | public-office-data-analysis, data-analysis-for-reporting, public-office-stock-analysis, financial-report-writer, public-office-crypto-report |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, public-office-weather-automation, followup-reply-writer, debugging-root-cause-helper |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, priority-sorter, variance-analysis-helper, dashboard-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, public-addy-agent-browser-testing-with-devtools, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, public-anthropic-canvas-design, slide-deck-visual-auditor, latency-anomaly-detector, metrics-root-cause-diagnoser |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, public-addy-web-accessibility, public-n-skills-dev-browser |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `public-netlify-deploy` | wrong | public-netlify-deploy, metrics-root-cause-diagnoser, debugging-root-cause-helper, frontend-debugger, public-addy-agent-debugging-and-error-recovery |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-addy-agent-shipping-and-launch, public-oh-my-changelog-maintenance |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, decision-matrix-builder, mobile-ops-acceptance-test-builder, public-swebench-slo-implementation, review-comment-resolver |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `general-source-summariser` | wrong | general-source-summariser, citation-note-extractor, data-analysis-with-validation, document-summariser, public-swebench-v3-performance-optimization |
| `doc_p2_document_rewriter` | `document-rewriter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, public-docx, document-rewriter, public-mattpocock-edit-article, public-addy-web-accessibility |
| `doc_p3_document_normaliser` | `document-normaliser` | 4 | 4 | `layout-preserving-converter` | wrong | layout-preserving-converter, public-docx, deck-template-applier, document-normaliser, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 4 | 4 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, document-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, public-docx, decision-matrix-builder, public-addy-agent-code-simplification |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-converter, office-to-markdown-converter, pdf-layout-reviewer, public-obsidian-defuddle |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `document-converter` | wrong | document-converter, layout-preserving-converter, pdf-layout-reviewer, note-tagger, public-mattpocock-setup-matt-pocock-skills |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, related-work-synthesiser, public-mattpocock-setup-matt-pocock-skills, public-swebench-slo-implementation |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, slo-breach-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 7 | 7 | `metrics-overview` | wrong | metrics-overview, public-office-contract-review, risk-ops-compliance-checker, risk-ops-acceptance-test-builder, architecture-boundary-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, metrics-root-cause-diagnoser, debugging-root-cause-helper, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, public-openai-playwright, capacity-risk-forecaster, rag-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 3 | 3 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, public-openai-linear, incident-summary-writer, metrics-overview, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, public-office-news-monitor, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, public-mattpocock-edit-article, metrics-overview, knowledge-base-article-writer, data-analysis-for-reporting |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 7 | 7 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, citation-note-extractor, document-field-extractor, document-summariser, document-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-anthropic-theme-factory, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-briefing-writer, capacity-risk-forecaster, news-theme-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-pdf, public-openai-pdf, public-office-pdf-form-filler, public-office-chat-with-pdf |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `public-pdf` | wrong | public-pdf, pdf-ocr-extractor, public-markitdown, public-office-pdf-watermark, public-office-office-mcp |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, public-office-docx-manipulation, layout-preserving-converter, multi-document-comparison-preparer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 3 | 3 | `rag-failure-diagnoser` | wrong | rag-failure-diagnoser, web-ui-tester, spreadsheet-formula-auditor, data-analysis-with-validation, public-swebench-langsmith-fetch |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, public-office-infographic, customer-feedback-analyser, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, public-markitdown, document-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, public-openai-notion-meeting-intelligence, public-pptx, followup-reply-writer, public-office-telegram-bot |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 10 | 10 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, general-source-summariser, meeting-ops-summary-writer, paper-summariser, public-office-transcription-automation |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 9 | 9 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, followup-reply-writer, meeting-summary-writer, meeting-ops-handoff-brief-writer, public-swebench-v3-performance-optimization |
| `plan_p4_task_extractor` | `task-extractor` | 3 | 3 | `weekly-planner` | wrong | weekly-planner, release-note-writer, task-extractor, public-mattpocock-writing-shape, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `public-openai-notion-meeting-intelligence` | wrong | public-openai-notion-meeting-intelligence, meeting-scheduler, meeting-agenda-builder, agent-eval-coverage-auditor, multi-document-comparison-preparer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, multi-source-comparison-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, dashboard-ops-summary-writer, public-office-academic-search |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-evidence-grounder, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | 8 | 8 | `web-data-extractor` | wrong | web-data-extractor, public-office-pdf-extraction, bioinformatics-ops-field-extractor, compliance-ops-field-extractor, contract-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `pr-description-writer` | wrong | pr-description-writer, citation-grounding-helper, speaker-notes-writer, review-comment-resolver, web-data-extractor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-addy-web-accessibility, agent-eval-coverage-auditor, public-mattpocock-writing-fragments, seed-data-generator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 4 | 4 | `public-mattpocock-writing-shape` | wrong | public-mattpocock-writing-shape, news-briefing-writer, note-tagger, multi-source-comparison-builder, public-addy-agent-interview-me |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 2 | 2 | `public-openai-notion-research-documentation` | wrong | public-openai-notion-research-documentation, related-work-synthesiser, multi-document-comparison-preparer, public-office-academic-search, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, email-polisher, followup-reply-writer, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, proposal-drafter, email-action-extractor, followup-reply-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, public-office-investment-memo, email-action-extractor, bioinformatics-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, email-polisher, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, public-brainstorming, public-openai-figma-code-connect-components, public-addy-agent-api-and-interface-design |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, accessibility-checker, public-addy-agent-security-and-hardening, public-addy-web-best-practices |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, priority-sorter, pr-reviewer, architecture-boundary-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, public-huggingface-huggingface-papers, public-vercel-find-skills, public-addy-agent-frontend-ui-engineering, public-openai-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, version-control-helper, public-addy-agent-context-engineering, public-mattpocock-teach |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `churn-risk-analyser` | wrong | churn-risk-analyser, public-swebench-analytics-events, query-optimizer, public-office-web-search, release-note-writer |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, incident-summary-writer, public-openai-notion-knowledge-capture, slo-breach-checker, followup-reply-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, public-anthropic-webapp-testing, public-huggingface-huggingface-community-evals, public-oh-my-lmstudio-cli, skill-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, public-skill-creator, public-anthropic-skill-creator, skill-editor, public-mattpocock-write-a-skill |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-evaluator, docs-ops-field-extractor, data-analysis-overview |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, agent-eval-coverage-auditor, citation-grounding-helper, reply-polisher, public-addy-agent-deprecation-and-migration |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, agent-ops-resource-linker, skill-editor, public-anthropic-skill-creator, skill-finder |

### `m1_tfidf_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, public-swebench-add-admin-api-endpoint, contract-ops-acceptance-test-builder, api-design-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 6 | 3 | `public-openai-figma-code-connect-components` | wrong | public-openai-figma-code-connect-components, public-swebench-add-admin-api-endpoint, api-integration-planner, public-office-cover-letter, api-ops-acceptance-test-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | 2 | `invoice-payment-checker` | wrong | invoice-payment-checker, webhook-contract-planner, public-openai-winui-app, duplicate-file-finder, events-ops-failure-diagnoser |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-openai-security-ownership-map, public-addy-agent-api-and-interface-design, public-oh-my-backend-testing |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, public-addy-agent-shipping-and-launch, deployment-rollback-planner, migration-risk-auditor, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, analytics-ops-quality-auditor, public-office-data-pipeline, public-office-md-slides, analytics-ops-evidence-grounder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, public-n-skills-dev-browser, public-openai-screenshot, public-openai-figma-generate-design, landing-page-copy-reviewer |
| `web_p2_form_filling` | `web-form-filler` | 7 | 7 | `variance-analysis-helper` | wrong | variance-analysis-helper, public-office-pdf-form-filler, public-openai-playwright, public-office-expense-report, public-office-weekly-report |
| `web_p3_ui_test` | `web-ui-tester` | 7 | 7 | `variance-analysis-helper` | wrong | variance-analysis-helper, web-page-snapshotter, public-office-expense-report, public-office-weekly-report, reply-drafter |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-resource-linker` | wrong | product-ops-resource-linker, product-ops-field-extractor, product-ops-normalizer, product-ops-compliance-checker, product-ops-dependency-mapper |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, api-ops-evidence-grounder, api-ops-field-extractor, api-ops-summary-writer, api-ops-normalizer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, public-addy-web-accessibility, public-office-pdf-form-filler, layout-preserving-converter |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer, public-oh-my-changelog-maintenance |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, public-mattpocock-review, public-swebench-analyze-ci, public-openai-gh-address-comments |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, public-openai-gh-address-comments, public-addy-agent-code-review-and-quality, pr-reviewer, pr-description-writer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, public-openai-gh-fix-ci, public-mattpocock-diagnose, public-addy-agent-debugging-and-error-recovery |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-swebench-changelog-automation, public-oh-my-changelog-maintenance, public-office-changelog-generator |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, public-office-changelog-generator, public-swebench-changelog-automation, public-mattpocock-review |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, public-office-expense-report, public-office-weekly-report, data-analysis-for-forecasting |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, public-addy-agent-debugging-and-error-recovery, debugging-root-cause-helper, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser |
| `data_p3_validation` | `data-analysis-with-validation` | 16 | 16 | `public-addy-web-web-quality-audit` | wrong | public-addy-web-web-quality-audit, public-oh-my-react-grab, public-addy-web-accessibility, public-mattpocock-to-issues, public-oh-my-react-best-practices |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-office-data-analysis, public-oh-my-data-analysis, data-analysis-for-forecasting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dashboard-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer, public-office-data-analysis, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, public-oh-my-pattern-detection, metrics-root-cause-diagnoser, duplicate-file-finder, data-analysis-for-root-cause-diagnosis |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, risk-ops-comparison-builder, dashboard-ops-comparison-builder, data-analysis-overview |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, public-addy-agent-browser-testing-with-devtools, public-n-skills-dev-browser, accessibility-interaction-auditor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector, public-addy-agent-performance-optimization |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, metrics-overview, public-addy-web-web-quality-audit |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 18 | 18 | `public-netlify-deploy` | wrong | public-netlify-deploy, debugging-root-cause-helper, public-oh-my-game-build-log-triage, data-analysis-for-root-cause-diagnosis, public-addy-agent-debugging-and-error-recovery |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-changelog-maintenance, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, budget-planner, mobile-ops-acceptance-test-builder, mobile-ops-monitoring-plan-builder, mobile-ops-normalizer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, knowledge-base-article-writer, general-source-summariser, receipt-extractor, multi-source-comparison-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, public-mattpocock-edit-article, document-normaliser, public-office-pdf-form-filler |
| `doc_p3_document_normaliser` | `document-normaliser` | 3 | 3 | `layout-preserving-converter` | wrong | layout-preserving-converter, deck-template-applier, document-normaliser, docx-redline-editor, docs-ops-rewrite-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | 6 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, public-office-invoice-automation, meeting-followup-extractor, public-office-table-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, multi-document-comparison-preparer, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 5 | 5 | `layout-preserving-converter` | wrong | layout-preserving-converter, public-obsidian-defuddle, office-to-markdown-converter, pdf-layout-reviewer, document-converter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, public-office-layout-analyzer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, public-oh-my-triage, public-oh-my-game-build-log-triage, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, data-analysis-overview, public-swebench-service-mesh-observability |
| `obs_p3_slo_breach` | `slo-breach-checker` | 9 | 9 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, public-swebench-slo-implementation, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, risk-ops-risk-reviewer, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-addy-agent-debugging-and-error-recovery, debugging-root-cause-helper, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 6 | `incident-ops-normalizer` | wrong | incident-ops-normalizer, incident-ops-compliance-checker, incident-ops-dependency-mapper, incident-ops-scenario-planner, incident-ops-risk-reviewer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, public-mattpocock-edit-article, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, public-mattpocock-edit-article, knowledge-base-article-writer, public-mattpocock-to-prd, support-ticket-triager |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, knowledge-base-article-writer, product-ops-scenario-planner, product-ops-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, public-office-news-monitor, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, public-office-news-monitor, news-briefing-writer, news-theme-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-office-pdf-watermark, public-office-chat-with-pdf, public-office-pdf-extraction |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, public-office-pdf-converter, public-office-pdf-ocr, pdf-layout-reviewer |
| `office_p3_docx_redline` | `docx-redline-editor` | 2 | 2 | `public-docx` | wrong | public-docx, docx-redline-editor, public-office-docx-manipulation, document-rewriter, public-office-pdf-to-docx |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-swebench-langsmith-fetch, rag-failure-diagnoser, public-office-contract-review, public-office-xlsx-manipulation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, public-office-ppt-visual, public-oh-my-presentation-builder |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, docx-redline-editor, public-office-docx-manipulation |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-scenario-planner, meeting-ops-normalizer, meeting-ops-compliance-checker, meeting-ops-dependency-mapper |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | - | - | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-ops-evidence-grounder, meeting-ops-normalizer, meeting-ops-artifact-packager, meeting-ops-compliance-checker |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, public-office-transcription-automation |
| `plan_p4_task_extractor` | `task-extractor` | 4 | 4 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-followup-extractor, meeting-summary-writer, task-extractor, meeting-ops-evidence-grounder |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-ops-monitoring-plan-builder, meeting-ops-acceptance-test-builder, meeting-ops-summary-writer, meeting-ops-normalizer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, public-office-academic-search, method-note-builder, public-oh-my-research-paper-writing |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, academic-admin-ops-summary-writer, professor-email-reply, academic-admin-ops-evidence-grounder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, writing-ops-evidence-grounder, writing-ops-field-extractor, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | - | - | `public-office-table-extractor` | wrong | public-office-table-extractor, research-ops-field-extractor, compliance-ops-field-extractor, docs-ops-field-extractor, partnerships-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, compliance-ops-scenario-planner, docs-ops-scenario-planner, citation-grounding-helper, partnerships-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-huggingface-train-sentence-transformers, public-addy-agent-performance-optimization, public-addy-web-web-quality-audit, document-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 7 | 7 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, citation-grounding-helper, note-linker |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, public-office-table-extractor, release-note-writer, public-openai-notion-research-documentation, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, email-polisher, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, reply-polisher, followup-reply-writer, deadline-reminder-planner |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, public-office-investment-memo, public-oh-my-state-management, public-oh-my-write-a-skill |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, public-openai-figma-create-new-file, followup-reply-writer, docker-compose-configurator |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `public-openai-figma-create-new-file` | wrong | public-openai-figma-create-new-file, security-threat-modeler, email-ops-risk-reviewer, public-security-threat-model, email-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, public-addy-agent-security-and-hardening, public-swebench-slo-implementation, pr-reviewer, api-ops-acceptance-test-builder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | - | - | `supply-chain-ops-risk-reviewer` | wrong | supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-artifact-packager, supply-chain-ops-normalizer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, public-oh-my-log-analysis, public-huggingface-huggingface-papers, public-office-webhook-automation, webhook-setup-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-ops-monitoring-plan-builder, public-oh-my-google-workspace, version-control-helper, email-ops-normalizer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, public-oh-my-log-analysis, query-optimizer, public-swebench-similarity-search-patterns, public-swebench-dbt-transformation-patterns |
| `skill_p1_find_existing` | `skill-finder` | - | - | `public-office-meeting-notes` | wrong | public-office-meeting-notes, library-ops-evidence-grounder, meeting-ops-evidence-grounder, library-ops-timeline-builder, library-ops-rewrite-editor |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, library-ops-resource-linker, library-ops-acceptance-test-builder, public-xlsx, public-swebench-xlsx |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, public-anthropic-skill-creator, meeting-followup-extractor, public-skill-creator, skill-editor |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `public-anthropic-skill-creator` | wrong | public-anthropic-skill-creator, skill-editor, public-skill-creator, skill-finder, skill-installer |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-anthropic-skill-creator, skill-installer, public-skill-creator |

### `m3_tfidf_schema` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, external-api-integration-planner, webhook-contract-planner, public-swebench-add-admin-api-endpoint |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, api-ops-acceptance-test-builder, webhook-contract-planner, public-openai-figma-code-connect-components |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, invoice-payment-checker, duplicate-file-finder, public-openai-winui-app, events-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-openai-security-ownership-map, public-addy-agent-api-and-interface-design, public-mattpocock-improve-codebase-architecture |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, public-addy-agent-shipping-and-launch, migration-risk-auditor, deployment-rollback-planner, deployment-release-verifier |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 5 | 5 | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, analytics-ops-quality-auditor, analytics-ops-timeline-builder, analytics-ops-evidence-grounder, service-dependency-mapper |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-data-extractor, pdf-layout-reviewer, pdf-ocr-extractor, public-n-skills-dev-browser |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, variance-analysis-helper, mobile-ops-field-extractor, web-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, web-page-snapshotter, web-data-extractor, web-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, product-ops-resource-linker, ecommerce-ops-field-extractor, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, web-ui-tester, api-ops-failure-diagnoser, security-code-reviewer |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, release-note-writer, public-office-applicant-screening |
| `code_p1_local_code_review` | `code-reviewer` | 2 | 2 | `git-commit-writer` | wrong | git-commit-writer, code-reviewer, changelog-writer, test-case-generator, email-ops-risk-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, public-mattpocock-review, code-reviewer, database-migration-risk-assessor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, ci-failure-debugger, public-openai-gh-address-comments |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, frontend-debugger, git-commit-writer, public-openai-gh-fix-ci |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-swebench-changelog-automation, public-oh-my-changelog-maintenance, public-office-changelog-generator |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, public-oh-my-changelog-maintenance, deployment-release-verifier, capacity-risk-forecaster |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-root-cause-diagnosis, data-analysis-for-reporting, finance-ops-summary-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, real-estate-ops-failure-diagnoser, deployment-build-triager, debugging-root-cause-helper |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, public-addy-web-web-quality-audit, public-oh-my-react-best-practices, public-oh-my-react-grab, public-oh-my-vercel-react-best-practices |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, public-office-data-analysis, data-analysis-with-validation |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, release-note-writer, dashboard-ops-handoff-brief-writer, dashboard-ops-resource-linker |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, frontend-debugger, public-oh-my-pattern-detection, metrics-root-cause-diagnoser |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, data-analysis-overview, data-analysis-for-forecasting, dataset-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, public-addy-agent-browser-testing-with-devtools, public-n-skills-dev-browser |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector, accessibility-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, public-addy-web-web-quality-audit, playwright-flow-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, public-oh-my-game-build-log-triage, frontend-debugger, debugging-root-cause-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, deployment-rollback-planner, public-openai-vercel-deploy, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-resource-linker, mobile-ops-acceptance-test-builder, mobile-ops-summary-writer, mobile-ops-normalizer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, citation-note-extractor, data-analysis-overview, metrics-overview, paper-summariser |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, email-polisher, document-normaliser, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, docx-redline-editor, deck-template-applier, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, finance-ops-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, pdf-layout-reviewer, document-converter, public-obsidian-defuddle, slide-deck-visual-auditor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, office-to-markdown-converter, pdf-layout-reviewer, public-office-layout-analyzer |
| `obs_p1_metrics_overview` | `metrics-overview` | 2 | 2 | `public-mattpocock-triage` | wrong | public-mattpocock-triage, metrics-overview, public-oh-my-triage, public-mattpocock-setup-matt-pocock-skills, public-oh-my-game-build-log-triage |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, data-analysis-overview, public-swebench-service-mesh-observability |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, public-swebench-slo-implementation, metrics-overview, risk-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, slo-breach-checker, incident-ops-resource-linker, public-swebench-service-mesh-observability |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-theme-extractor, public-office-news-monitor, general-source-summariser, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `news-summariser` | wrong | news-summariser, news-briefing-writer, support-ops-ops-timeline-builder, knowledge-base-article-writer, support-ops-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, product-ops-resource-linker, product-ops-scenario-planner, content-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-office-news-monitor, news-summariser, market-opportunity-assessor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, public-office-news-monitor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, web-page-snapshotter, web-data-extractor, public-office-pdf-watermark |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, web-page-snapshotter, pdf-layout-reviewer, public-office-pdf-ocr |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, document-normaliser, public-office-docx-manipulation, review-comment-resolver |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-xlsx, public-swebench-xlsx, public-office-xlsx-manipulation, agent-ops-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, speaker-notes-writer, public-office-ppt-visual |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, docx-redline-editor, public-docx, layout-preserving-converter, pdf-layout-reviewer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, weekly-planner, task-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, public-office-meeting-notes, meeting-followup-extractor, meeting-ops-resource-linker |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, public-office-transcription-automation |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, task-extractor, meeting-summary-writer, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, general-source-summariser, citation-note-extractor, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, data-analysis-for-reporting, professor-email-reply, academic-admin-ops-failure-diagnoser |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, document-extractor, paper-summariser, writing-ops-resource-linker, writing-ops-priority-ranker |
| `read_p4_document_extraction` | `document-extractor` | - | - | `ml-ops-field-extractor` | wrong | ml-ops-field-extractor, bioinformatics-ops-field-extractor, recruiting-ops-field-extractor, analytics-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner, qa-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-huggingface-train-sentence-transformers, public-addy-agent-performance-optimization, document-extractor, citation-note-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `paper-summariser` | wrong | paper-summariser, method-note-builder, related-work-synthesiser, citation-note-extractor, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, general-source-summariser, paper-summariser, research-ops-comparison-builder, multi-source-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, public-mattpocock-write-a-skill, public-office-investment-memo, public-oh-my-write-a-skill |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, docker-compose-configurator |
| `sec_p1_threat_model` | `security-threat-modeler` | 4 | 4 | `security-code-reviewer` | wrong | security-code-reviewer, privacy-risk-reviewer, auth-flow-reviewer, security-threat-modeler, public-openai-figma-create-new-file |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, security-threat-modeler, code-reviewer, pr-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-risk-reviewer, supply-chain-ops-resource-linker |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, public-huggingface-huggingface-papers, deployment-release-verifier, database-ops-resource-linker |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-polisher, email-drafter, email-ops-monitoring-plan-builder, version-control-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, public-swebench-similarity-search-patterns, email-polisher, product-ops-resource-linker, public-swebench-dbt-transformation-patterns |
| `skill_p1_find_existing` | `skill-finder` | 6 | 6 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, skill-creator, skill-editor, meeting-agenda-builder, meeting-followup-extractor |
| `skill_p2_install_existing` | `skill-installer` | 2 | 2 | `skill-packager` | wrong | skill-packager, skill-installer, library-ops-artifact-packager, public-huggingface-huggingface-local-models, library-ops-rewrite-editor |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, public-openai-figma-create-new-file, skill-finder, meeting-ops-summary-writer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-finder, skill-creator, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 6 | 6 | `reply-drafter` | wrong | reply-drafter, professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-oh-my-research-paper-writing, public-huggingface-huggingface-papers, general-source-summariser |

### `m6_bm25_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, external-api-integration-planner, api-design-reviewer, graphql-schema-designer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, openapi-contract-tester, database-backup-planner, api-ops-acceptance-test-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, engineering-design-ops-timeline-builder, invoice-payment-checker |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, refactor-planner, public-addy-agent-api-and-interface-design, security-threat-modeler |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, deployment-release-verifier, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, privacy-policy-drafter, privacy-risk-reviewer, architecture-boundary-reviewer, data-analysis-for-reporting |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, public-n-skills-dev-browser, public-mattpocock-triage |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-n-skills-dev-browser, public-office-pdf-form-filler, dashboard-ops-field-extractor, public-openai-playwright |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, dashboard-ops-acceptance-test-builder, docs-ops-acceptance-test-builder, ecommerce-ops-acceptance-test-builder, energy-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, product-ops-resource-linker, web-page-snapshotter, pdf-layout-reviewer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, debugging-root-cause-helper, public-addy-agent-code-simplification, openapi-contract-tester |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, slo-breach-checker, layout-preserving-converter, reply-drafter |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, changelog-writer, release-note-writer, git-commit-writer, review-comment-resolver |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, database-migration-risk-assessor, public-mattpocock-review, review-comment-resolver |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-description-writer, code-reviewer, reply-drafter, public-openai-gh-address-comments |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, public-addy-agent-debugging-and-error-recovery, frontend-debugger, openapi-contract-reviewer, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-oh-my-changelog-maintenance, public-swebench-changelog-automation, git-commit-writer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, public-office-changelog-generator, pr-description-writer, slo-breach-checker |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, financial-report-writer, dashboard-ops-priority-ranker, dashboard-ops-handoff-brief-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, debugging-root-cause-helper, latency-anomaly-detector, frontend-debugger |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, compliance-ops-quality-auditor, energy-ops-quality-auditor, data-analysis-with-anomaly-focus |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, variance-analysis-helper, web-performance-budget-checker, public-office-data-analysis |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, public-office-data-analysis, financial-report-writer, public-office-stock-analysis, news-briefing-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, followup-reply-writer, capacity-risk-forecaster, frontend-debugger |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, dashboard-ops-comparison-builder, dashboard-ops-scenario-planner, risk-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, accessibility-interaction-auditor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, changelog-writer, public-anthropic-canvas-design, data-analysis-for-root-cause-diagnosis |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, web-ui-tester, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, frontend-debugger, public-netlify-deploy, ci-failure-debugger, debugging-root-cause-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, release-note-writer, deployment-build-triager |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, mobile-ops-acceptance-test-builder, budget-planner, mobile-ops-risk-reviewer |
| `doc_p1_document_summary` | `document-summariser` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, document-summariser, citation-note-extractor, news-summariser, data-analysis-with-validation |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, public-docx, document-normaliser, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-layout-reviewer, public-docx, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | 6 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, docs-ops-field-extractor, energy-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, decision-matrix-builder, public-docx, skill-installer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, deck-template-applier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, note-tagger |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, service-dependency-mapper, public-swebench-slo-implementation, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 4 | 4 | `risk-ops-acceptance-test-builder` | wrong | risk-ops-acceptance-test-builder, metrics-overview, risk-ops-compliance-checker, slo-breach-checker, architecture-boundary-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, data-analysis-for-forecasting, metrics-root-cause-diagnoser, risk-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, deployment-build-triager, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, public-openai-linear, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, metrics-overview, support-ops-ops-timeline-builder, public-mattpocock-edit-article |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 2 | 2 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, source-grounding-extractor, citation-note-extractor, document-summariser, document-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, public-anthropic-theme-factory |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, capacity-risk-forecaster |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-pdf, public-office-pdf-form-filler, public-openai-pdf, public-office-chat-with-pdf |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-pdf, pdf-layout-reviewer, public-office-pdf-watermark, public-markitdown |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, review-comment-resolver, multi-document-comparison-preparer, layout-preserving-converter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, data-analysis-with-validation, rag-failure-diagnoser, risk-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, customer-feedback-analyser, research-ops-rewrite-editor, vendor-ops-rewrite-editor, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, document-converter, public-docx, changelog-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, meeting-ops-risk-reviewer, meeting-ops-failure-diagnoser |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-evidence-grounder, meeting-ops-failure-diagnoser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, followup-reply-writer, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, weekly-planner, meeting-summary-writer, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-scheduler` | wrong | meeting-scheduler, meeting-agenda-builder, meeting-ops-acceptance-test-builder, public-openai-notion-meeting-intelligence, test-case-generator |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, research-ops-summary-writer, method-note-builder, academic-admin-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, dashboard-ops-summary-writer, compliance-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-evidence-grounder, writing-ops-resource-linker, writing-ops-artifact-packager |
| `read_p4_document_extraction` | `document-extractor` | 19 | 19 | `web-data-extractor` | wrong | web-data-extractor, docs-ops-field-extractor, bioinformatics-ops-field-extractor, research-ops-field-extractor, privacy-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `pr-description-writer` | wrong | pr-description-writer, manufacturing-ops-scenario-planner, journalism-ops-scenario-planner, docs-ops-scenario-planner, fundraising-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-addy-web-accessibility, agent-eval-coverage-auditor, public-addy-web-performance, public-mattpocock-writing-fragments |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 3 | 3 | `news-briefing-writer` | wrong | news-briefing-writer, public-mattpocock-writing-shape, multi-source-comparison-builder, note-tagger, release-note-writer |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, public-openai-notion-research-documentation, multi-document-comparison-preparer, release-note-writer, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, groupwork-reply, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, proposal-drafter, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, email-action-extractor, procurement-ops-handoff-brief-writer, journalism-ops-handoff-brief-writer, docs-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, email-ops-scenario-planner, identity-ops-scenario-planner, security-ops-scenario-planner, public-brainstorming |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, accessibility-checker, identity-ops-acceptance-test-builder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, risk-ops-risk-reviewer, pr-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, webhook-setup-planner, deployment-release-verifier, environment-config-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, email-polisher, accessibility-checker, citation-grounding-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, churn-risk-analyser, public-swebench-analytics-events, query-optimizer, public-office-web-search |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, followup-reply-writer, meeting-followup-extractor, incident-summary-writer, release-note-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, library-ops-artifact-packager, public-anthropic-webapp-testing, code-reviewer, public-huggingface-huggingface-community-evals |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, skill-finder, public-skill-creator, meeting-followup-extractor |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, docs-ops-field-extractor, agent-ops-field-extractor, public-anthropic-skill-creator, document-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, agent-eval-coverage-auditor, skill-finder, reply-polisher, reply-drafter |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, agent-ops-resource-linker, skill-finder, hr-ops-resource-linker |

### `m6_tfidf_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, graphql-schema-designer, contract-ops-normalizer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-acceptance-test-builder, public-swebench-add-admin-api-endpoint, public-openai-figma-code-connect-components |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, invoice-payment-checker, events-ops-timeline-builder, public-openai-winui-app, events-ops-scenario-planner |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, security-threat-modeler, version-control-helper, public-addy-agent-api-and-interface-design |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-rollback-planner, migration-risk-auditor, public-addy-agent-shipping-and-launch, risk-ops-risk-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `analytics-ops-quality-auditor` | wrong | analytics-ops-quality-auditor, analytics-ops-evidence-grounder, public-office-microsoft-teams, web-performance-budget-checker, analytics-ops-summary-writer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-office-pdf-form-filler, public-openai-playwright, public-n-skills-dev-browser, real-estate-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, web-page-snapshotter, docs-ops-acceptance-test-builder, compliance-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-field-extractor` | wrong | product-ops-field-extractor, product-ops-resource-linker, product-ops-scenario-planner, product-ops-comparison-builder, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, api-ops-evidence-grounder, api-ops-field-extractor, api-ops-timeline-builder |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, layout-preserving-converter, web-form-filler, public-addy-web-accessibility |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer, changelog-writer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, database-migration-risk-assessor, api-ops-acceptance-test-builder, public-mattpocock-review |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, public-openai-gh-address-comments, pr-description-writer, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, git-commit-writer, public-addy-agent-debugging-and-error-recovery, openapi-contract-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-swebench-changelog-automation, public-oh-my-changelog-maintenance, public-office-changelog-generator |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, public-office-changelog-generator, service-dependency-mapper, slo-breach-checker |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-ranking-selection, spreadsheet-formula-auditor, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, debugging-root-cause-helper, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, public-addy-web-web-quality-audit, public-mattpocock-to-issues, market-opportunity-assessor, public-addy-web-accessibility |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-office-data-analysis, web-performance-budget-checker, data-analysis-for-forecasting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dashboard-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer, data-analysis-overview, public-office-data-analysis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, risk-ops-comparison-builder, dashboard-ops-comparison-builder, risk-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, accessibility-interaction-auditor, public-addy-agent-browser-testing-with-devtools, public-n-skills-dev-browser |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, review-comment-resolver, code-reviewer, public-anthropic-canvas-design |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, metrics-overview, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, frontend-debugger, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-note-writer, public-openai-vercel-deploy, public-oh-my-changelog-maintenance |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, budget-planner, mobile-ops-acceptance-test-builder, mobile-ops-risk-reviewer, mobile-ops-evidence-grounder |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, citation-note-extractor, knowledge-base-article-writer, multi-document-comparison-preparer |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, deck-template-applier, pdf-layout-reviewer, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 4 | 4 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, docs-ops-field-extractor, document-field-extractor, compliance-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, docs-ops-comparison-builder, compliance-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, document-converter, pdf-layout-reviewer, public-obsidian-defuddle |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-converter, docs-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, public-mattpocock-triage, public-swebench-service-mesh-observability, public-oh-my-triage |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 6 | 6 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, service-dependency-mapper, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, risk-ops-risk-reviewer, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, debugging-root-cause-helper |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 6 | `incident-ops-normalizer` | wrong | incident-ops-normalizer, metrics-overview, incident-ops-scenario-planner, incident-ops-timeline-builder, incident-ops-risk-reviewer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, general-source-summariser, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, support-ops-ops-timeline-builder, public-mattpocock-edit-article, support-ops-timeline-builder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, knowledge-base-article-writer, product-ops-scenario-planner, document-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, public-office-news-monitor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, public-office-news-monitor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-office-chat-with-pdf, public-pdf, public-office-pdf-extraction |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, pdf-layout-reviewer, public-office-pdf-ocr, public-office-pdf-converter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, review-comment-resolver, public-office-docx-manipulation, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-swebench-langsmith-fetch, public-office-contract-review, web-ui-tester, rag-failure-diagnoser |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, research-ops-rewrite-editor, vendor-ops-rewrite-editor, public-pptx, customer-feedback-analyser |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, docx-redline-editor, public-docx, document-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-ops-failure-diagnoser, meeting-ops-normalizer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | - | - | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-ops-evidence-grounder, meeting-ops-field-extractor, meeting-ops-normalizer, meeting-ops-priority-ranker |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, public-office-meeting-notes, meeting-ops-evidence-grounder |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, meeting-summary-writer, meeting-followup-extractor, public-office-meeting-notes |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-scheduler, meeting-ops-acceptance-test-builder, meeting-ops-summary-writer, meeting-ops-monitoring-plan-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, research-ops-summary-writer, method-note-builder, public-office-academic-search |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, professor-email-reply |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, writing-ops-resource-linker, writing-ops-priority-ranker, writing-ops-acceptance-test-builder, writing-ops-evidence-grounder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, docs-ops-field-extractor, ml-ops-field-extractor, lab-ops-field-extractor, compliance-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner, events-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-huggingface-train-sentence-transformers, support-ops-evidence-grounder, support-ops-ops-evidence-grounder, public-addy-agent-performance-optimization |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, release-note-writer, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, release-note-writer, multi-source-comparison-builder, public-openai-notion-research-documentation |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, email-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, email-action-extractor, public-office-investment-memo, public-oh-my-state-management |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, public-openai-figma-create-new-file |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-openai-figma-create-new-file, email-ops-scenario-planner, email-ops-risk-reviewer, risk-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, api-ops-acceptance-test-builder, security-ops-acceptance-test-builder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | - | - | `supply-chain-ops-risk-reviewer` | wrong | supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-artifact-packager, supply-chain-ops-scenario-planner, supply-chain-ops-timeline-builder |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, webhook-contract-planner, deployment-release-verifier, database-ops-normalizer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-ops-monitoring-plan-builder, email-ops-acceptance-test-builder, version-control-helper, email-ops-resource-linker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, product-ops-resource-linker, public-swebench-similarity-search-patterns, public-swebench-analytics-events, query-optimizer |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-ops-evidence-grounder, meeting-ops-comparison-builder, public-office-meeting-notes, library-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, library-ops-acceptance-test-builder, public-xlsx, public-huggingface-huggingface-local-models, public-swebench-xlsx |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, skill-editor, skill-finder, public-anthropic-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, agent-ops-field-extractor, docs-ops-field-extractor, skill-finder |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-anthropic-skill-creator, skill-editor, agent-ops-resource-linker |
