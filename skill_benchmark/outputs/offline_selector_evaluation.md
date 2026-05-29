# Offline Selector Evaluation Report

This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.

## Scale Regimes

- `core`: 85 skills, approx selector-visible tokens per method vary by representation.
- `current_full`: 2089 skills, approx selector-visible tokens per method vary by representation.

## Method Summary

| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | `core` | 85 | 4869 | 76.5% | 76.5% | 92.9% | 92.9% | 95.3% | 95.3% | 0.843 | 0.843 | 1.57 | 7.1% | 0.0% | 158.73 |
| `m1_tfidf_flat` | `core` | 85 | 4869 | 75.3% | 75.3% | 92.9% | 92.9% | 95.3% | 95.3% | 0.841 | 0.841 | 1.76 | 9.4% | 0.0% | 1253.23 |
| `m2a_minilm_description` | `core` | 85 | 4869 | 67.1% | 67.1% | 84.7% | 84.7% | 90.6% | 90.6% | 0.778 | 0.778 | 2.18 | 10.6% | 0.0% | 6172.54 |
| `m2b_minilm_full_skill` | `core` | 85 | 38741 | 71.8% | 71.8% | 84.7% | 84.7% | 91.8% | 91.8% | 0.804 | 0.804 | 2.02 | 9.4% | 0.0% | 3954.71 |
| `m3_tfidf_schema` | `core` | 85 | 35791 | 84.7% | 84.7% | 96.5% | 96.5% | 100.0% | 100.0% | 0.912 | 0.912 | 1.25 | 7.1% | 0.0% | 93.05 |
| `m6_bm25_schema_rerank` | `core` | 85 | 13454 | 80.0% | 80.0% | 96.5% | 96.5% | 97.7% | 97.7% | 0.881 | 0.881 | 1.23 | 3.5% | 0.0% | 540.62 |
| `m6_tfidf_schema_rerank` | `core` | 85 | 13454 | 84.7% | 84.7% | 96.5% | 96.5% | 97.7% | 97.7% | 0.907 | 0.907 | 1.3 | 3.5% | 0.0% | 453.42 |
| `m6_minilm_full_schema_rerank` | `core` | 85 | 47326 | 90.6% | 90.6% | 100.0% | 100.0% | 100.0% | 100.0% | 0.951 | 0.951 | 1.11 | 1.2% | 0.0% | 4328.94 |
| `m1_bm25_flat` | `current_full` | 2089 | 105272 | 70.6% | 70.6% | 82.3% | 82.3% | 87.1% | 87.1% | 0.776 | 0.776 | 1.98 | 4.7% | 14.1% | 3519.98 |
| `m1_tfidf_flat` | `current_full` | 2089 | 105272 | 58.8% | 58.8% | 76.5% | 77.6% | 80.0% | 80.0% | 0.687 | 0.692 | 2.26 | 7.1% | 28.2% | 246.97 |
| `m2a_minilm_description` | `current_full` | 2089 | 105272 | 49.4% | 52.9% | 72.9% | 74.1% | 77.6% | 78.8% | 0.626 | 0.652 | 2.69 | 8.2% | 31.8% | 11545.47 |
| `m2b_minilm_full_skill` | `current_full` | 2089 | 1065572 | 64.7% | 65.9% | 81.2% | 81.2% | 83.5% | 83.5% | 0.738 | 0.744 | 2.18 | 11.8% | 15.3% | 24544.09 |
| `m3_tfidf_schema` | `current_full` | 2089 | 590432 | 78.8% | 78.8% | 90.6% | 90.6% | 94.1% | 94.1% | 0.855 | 0.855 | 1.39 | 8.2% | 7.1% | 632.78 |
| `m6_bm25_schema_rerank` | `current_full` | 2089 | 111268 | 78.8% | 78.8% | 90.6% | 90.6% | 91.8% | 91.8% | 0.853 | 0.853 | 1.45 | 2.4% | 4.7% | 3343.42 |
| `m6_tfidf_schema_rerank` | `current_full` | 2089 | 111268 | 75.3% | 75.3% | 87.1% | 87.1% | 88.2% | 88.2% | 0.812 | 0.814 | 1.28 | 4.7% | 11.8% | 493.13 |
| `m6_minilm_full_schema_rerank` | `current_full` | 2089 | 1071568 | 82.3% | 82.3% | 89.4% | 89.4% | 89.4% | 89.4% | 0.859 | 0.859 | 1.32 | 1.2% | 5.9% | 22963.3 |

Accept metrics count documented acceptable alternatives as correct, while strict metrics require the controlled gold label.

## Benchmark Pressure Read

- `m1_bm25_flat` on `core`: useful pressure
- `m1_tfidf_flat` on `core`: useful pressure
- `m2a_minilm_description` on `core`: useful pressure
- `m2b_minilm_full_skill` on `core`: useful pressure
- `m3_tfidf_schema` on `core`: useful pressure
- `m6_bm25_schema_rerank` on `core`: useful pressure
- `m6_tfidf_schema_rerank` on `core`: useful pressure
- `m6_minilm_full_schema_rerank` on `core`: possibly too easy
- `m1_bm25_flat` on `current_full`: useful pressure
- `m1_tfidf_flat` on `current_full`: useful pressure
- `m2a_minilm_description` on `current_full`: useful pressure
- `m2b_minilm_full_skill` on `current_full`: useful pressure
- `m3_tfidf_schema` on `current_full`: useful pressure
- `m6_bm25_schema_rerank` on `current_full`: useful pressure
- `m6_tfidf_schema_rerank` on `current_full`: useful pressure
- `m6_minilm_full_schema_rerank` on `current_full`: useful pressure

## Scale Sensitivity

This table compares the controlled core with the current full library. A useful scale condition should create some degradation or non-core false positives without making retrieval random.

| Method | Core Top-1 | Full Top-1 | Full Accept Top-1 | Top-1 Delta | Core Top-5 | Full Top-5 | Full Accept Top-5 | Top-5 Delta | Core MRR | Full MRR | Full Accept MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | 76.5% | 70.6% | 70.6% | -5.9% | 95.3% | 87.1% | 87.1% | -8.2% | 0.843 | 0.776 | 0.776 | 14.1% |
| `m1_tfidf_flat` | 75.3% | 58.8% | 58.8% | -16.5% | 95.3% | 80.0% | 80.0% | -15.3% | 0.841 | 0.687 | 0.692 | 28.2% |
| `m2a_minilm_description` | 67.1% | 49.4% | 52.9% | -17.6% | 90.6% | 77.6% | 78.8% | -12.9% | 0.778 | 0.626 | 0.652 | 31.8% |
| `m2b_minilm_full_skill` | 71.8% | 64.7% | 65.9% | -7.1% | 91.8% | 83.5% | 83.5% | -8.2% | 0.804 | 0.738 | 0.744 | 15.3% |
| `m3_tfidf_schema` | 84.7% | 78.8% | 78.8% | -5.9% | 100.0% | 94.1% | 94.1% | -5.9% | 0.912 | 0.855 | 0.855 | 7.1% |
| `m6_bm25_schema_rerank` | 80.0% | 78.8% | 78.8% | -1.2% | 97.7% | 91.8% | 91.8% | -5.9% | 0.881 | 0.853 | 0.853 | 4.7% |
| `m6_minilm_full_schema_rerank` | 90.6% | 82.3% | 82.3% | -8.2% | 100.0% | 89.4% | 89.4% | -10.6% | 0.951 | 0.859 | 0.859 | 5.9% |
| `m6_tfidf_schema_rerank` | 84.7% | 75.3% | 75.3% | -9.4% | 97.7% | 88.2% | 88.2% | -9.4% | 0.907 | 0.812 | 0.814 | 11.8% |

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

### `m2a_minilm_description` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 33.3% | 33.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |
| `data_spreadsheet` | 7 | 57.1% | 57.1% | 71.4% | 71.4% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 57.1% | 57.1% | 71.4% | 71.4% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_lifecycle` | 6 | 16.7% | 16.7% | 16.7% | 16.7% | 50.0% | 50.0% |

Top confusions:
- `service-dependency-mapper -> metrics-root-cause-diagnoser`: 1
- `web-page-snapshotter -> visual-regression-checker`: 1
- `web-form-filler -> web-ui-tester`: 1
- `web-ui-tester -> ci-failure-debugger`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `pr-reviewer -> auth-flow-reviewer`: 1
- `changelog-writer -> release-note-writer`: 1
- `release-note-writer -> auth-flow-reviewer`: 1

### `m2b_minilm_full_skill` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 33.3% | 33.3% | 50.0% | 50.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 85.7% | 85.7% | 85.7% | 85.7% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 60.0% | 60.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 87.5% | 87.5% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 16.7% | 16.7% | 33.3% | 33.3% | 50.0% | 50.0% |

Top confusions:
- `service-dependency-mapper -> latency-anomaly-detector`: 1
- `web-page-snapshotter -> visual-regression-checker`: 1
- `web-ui-tester -> deployment-release-verifier`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `code-reviewer -> auth-flow-reviewer`: 1
- `pr-reviewer -> auth-flow-reviewer`: 1
- `changelog-writer -> release-note-writer`: 1
- `release-note-writer -> auth-flow-reviewer`: 1

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

### `m6_minilm_full_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 87.5% | 87.5% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `data-analysis-overview -> data-analysis-for-forecasting`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `metrics-root-cause-diagnoser -> service-dependency-mapper`: 1
- `weekly-planner -> meeting-agenda-builder`: 1
- `document-extractor -> web-data-extractor`: 1
- `privacy-risk-reviewer -> data-analysis-overview`: 1
- `skill-editor -> document-field-extractor`: 1

### `m1_bm25_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 57.1% | 57.1% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `office_artifact_workflows` | 6 | 50.0% | 50.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 40.0% | 40.0% | 40.0% | 40.0% |
| `reading_research` | 8 | 37.5% | 37.5% | 62.5% | 62.5% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `pr-reviewer -> pr-description-writer`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `data-analysis-for-reporting -> public-office-data-analysis`: 1
- `deployment-build-triager -> public-netlify-deploy`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> public-docx`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> receipt-extractor`: 1

### `m1_tfidf_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 50.0% | 50.0% | 66.7% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 71.4% | 71.4% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `news_monitoring` | 5 | 60.0% | 60.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
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
- `data-analysis-with-validation -> public-openai-linear`: 1
- `data-analysis-for-ranking-selection -> decision-matrix-builder`: 1

### `m2a_minilm_description` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 16.7% | 16.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 33.3% | 33.3% | 66.7% | 66.7% | 83.3% | 83.3% |
| `data_spreadsheet` | 7 | 28.6% | 28.6% | 42.9% | 42.9% | 42.9% | 42.9% |
| `deployment_browser_qa` | 6 | 33.3% | 33.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 0.0% | 28.6% | 42.9% | 57.1% | 57.1% | 71.4% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 60.0% | 60.0% | 60.0% | 60.0% | 60.0% | 60.0% |
| `office_artifact_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% |

Top confusions:
- `external-api-integration-planner -> api-integration-planner`: 1
- `service-dependency-mapper -> customer-feedback-analyser`: 1
- `web-page-snapshotter -> visual-regression-checker`: 1
- `web-form-filler -> web-ui-tester`: 1
- `web-ui-tester -> facilities-ops-acceptance-test-builder`: 1
- `web-data-extractor -> product-ops-field-extractor`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `code-reviewer -> email-ops-acceptance-test-builder`: 1

### `m2b_minilm_full_skill` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 33.3% | 33.3% | 50.0% | 50.0% | 50.0% | 50.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 60.0% | 60.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% | 16.7% |

Top confusions:
- `service-dependency-mapper -> latency-anomaly-detector`: 1
- `web-page-snapshotter -> visual-regression-checker`: 1
- `web-ui-tester -> procurement-ops-acceptance-test-builder`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `code-reviewer -> email-ops-acceptance-test-builder`: 1
- `pr-reviewer -> auth-flow-reviewer`: 1
- `changelog-writer -> release-note-writer`: 1
- `release-note-writer -> auth-flow-reviewer`: 1

### `m3_tfidf_schema` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
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
- `incident-summary-writer -> metrics-overview`: 1
- `news-briefing-writer -> news-summariser`: 1

### `m6_bm25_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 42.9% | 42.9% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> metrics-root-cause-diagnoser`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> receipt-extractor`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `slo-breach-checker -> metrics-overview`: 1

### `m6_tfidf_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 60.0% | 60.0% | 60.0% | 60.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 75.0% | 75.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
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

### `m6_minilm_full_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 75.0% | 75.0% | 75.0% | 75.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_lifecycle` | 6 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |

Top confusions:
- `service-dependency-mapper -> latency-anomaly-detector`: 1
- `web-ui-tester -> procurement-ops-acceptance-test-builder`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `release-note-writer -> deployment-release-verifier`: 1
- `data-analysis-overview -> data-analysis-for-forecasting`: 1
- `document-summariser -> travel-ops-summary-writer`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `metrics-root-cause-diagnoser -> service-dependency-mapper`: 1

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

### `m2a_minilm_description` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, architecture-boundary-reviewer, database-migration-risk-assessor, service-dependency-mapper |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, auth-flow-reviewer, openapi-contract-reviewer, privacy-risk-reviewer, webhook-contract-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, followup-reply-writer, auth-flow-reviewer, external-api-integration-planner, latency-anomaly-detector |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, openapi-contract-reviewer, database-migration-risk-assessor, service-dependency-mapper, external-api-integration-planner |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, dependency-risk-auditor, deployment-release-verifier, privacy-risk-reviewer, external-api-integration-planner |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 14 | 14 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, metrics-overview, latency-anomaly-detector, spreadsheet-formula-auditor, slo-breach-checker |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, web-page-snapshotter, accessibility-interaction-auditor, web-ui-tester, playwright-flow-debugger |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `web-ui-tester` | wrong | web-ui-tester, web-form-filler, auth-flow-reviewer, web-page-snapshotter, accessibility-checker |
| `web_p3_ui_test` | `web-ui-tester` | 7 | 7 | `ci-failure-debugger` | wrong | ci-failure-debugger, data-analysis-with-validation, code-reviewer, pr-reviewer, slo-breach-checker |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, document-field-extractor, document-extractor, layout-preserving-converter, meeting-followup-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, playwright-flow-debugger, deployment-build-triager, deployment-release-verifier, external-api-integration-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, visual-regression-checker, web-ui-tester, auth-flow-reviewer |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, reply-drafter, release-note-writer, review-comment-resolver, deployment-release-verifier |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, pr-reviewer, openapi-contract-reviewer, security-code-reviewer, code-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, ci-failure-debugger, code-reviewer, auth-flow-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, frontend-debugger, auth-flow-reviewer, web-ui-tester, deployment-build-triager |
| `code_p5_changelog_entry` | `changelog-writer` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, changelog-writer, deployment-build-triager, review-comment-resolver, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 13 | 13 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, deployment-release-verifier, privacy-risk-reviewer, deployment-build-triager, slo-breach-checker |
| `data_p1_overview` | `data-analysis-overview` | 7 | 7 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, news-theme-extractor, news-briefing-writer, paper-summariser, news-summariser |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, tech-news-trend-extractor, news-theme-extractor |
| `data_p3_validation` | `data-analysis-with-validation` | 3 | 3 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, data-analysis-with-anomaly-focus, data-analysis-with-validation, capacity-risk-forecaster, slo-breach-checker |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 4 | 4 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, latency-anomaly-detector, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, visual-regression-checker |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-summariser, news-briefing-writer, incident-summary-writer, source-grounding-extractor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, tech-news-trend-extractor, capacity-risk-forecaster, news-theme-extractor, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, followup-reply-writer, meeting-followup-extractor, weekly-planner, capacity-risk-forecaster |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 2 | 2 | `frontend-debugger` | wrong | frontend-debugger, playwright-flow-debugger, web-ui-tester, auth-flow-reviewer, ci-failure-debugger |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, pdf-layout-reviewer, web-page-snapshotter, slide-deck-visual-auditor, web-performance-budget-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, visual-regression-checker, frontend-debugger, pdf-layout-reviewer |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, ci-failure-debugger, deployment-release-verifier, playwright-flow-debugger, frontend-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, deployment-build-triager, visual-regression-checker, playwright-flow-debugger, ci-failure-debugger |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, visual-regression-checker, accessibility-interaction-auditor, architecture-boundary-reviewer, accessibility-checker |
| `doc_p1_document_summary` | `document-summariser` | 10 | 10 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, document-rewriter, external-api-integration-planner, dependency-risk-auditor, incident-summary-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | 4 | 4 | `method-note-builder` | wrong | method-note-builder, paper-summariser, document-summariser, document-rewriter, citation-note-extractor |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `document-rewriter` | wrong | document-rewriter, document-normaliser, method-note-builder, layout-preserving-converter, document-converter |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, method-note-builder, spreadsheet-formula-auditor, document-summariser, document-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, method-note-builder, document-summariser, pdf-layout-reviewer |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, layout-preserving-converter, office-to-markdown-converter, document-rewriter, method-note-builder |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, method-note-builder, document-converter, pdf-layout-reviewer, document-rewriter |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, web-page-snapshotter, service-dependency-mapper, slo-breach-checker, deployment-build-triager |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, web-performance-budget-checker, metrics-overview, slo-breach-checker, capacity-risk-forecaster |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, dependency-risk-auditor, capacity-risk-forecaster, database-migration-risk-assessor |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, latency-anomaly-detector, data-analysis-for-forecasting, service-dependency-mapper |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, latency-anomaly-detector, slo-breach-checker, metrics-overview, web-performance-budget-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, groupwork-reply, metrics-overview, meeting-followup-extractor, news-summariser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, paper-summariser, source-grounding-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 3 | 3 | `incident-summary-writer` | wrong | incident-summary-writer, meeting-summary-writer, news-briefing-writer, meeting-followup-extractor, news-summariser |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, citation-note-extractor, citation-grounding-helper, document-extractor, general-source-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, related-work-synthesiser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, source-grounding-extractor, news-summariser |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, document-extractor, layout-preserving-converter, document-field-extractor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, document-extractor, document-converter, layout-preserving-converter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, pdf-layout-reviewer, document-rewriter, document-summariser, document-normaliser |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, data-analysis-with-validation, data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, related-work-synthesiser, method-note-builder, visual-regression-checker |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `docx-redline-editor` | wrong | docx-redline-editor, office-to-markdown-converter, layout-preserving-converter, document-normaliser, document-field-extractor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, task-extractor, meeting-summary-writer, meeting-followup-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, task-extractor, meeting-followup-extractor, method-note-builder |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 4 | 4 | `meeting-summary-writer` | wrong | meeting-summary-writer, task-extractor, meeting-agenda-builder, meeting-followup-extractor, release-note-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-summary-writer, meeting-followup-extractor, meeting-agenda-builder |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, task-extractor, meeting-agenda-builder, meeting-summary-writer, groupwork-reply |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, general-source-summariser, multi-source-comparison-builder, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, citation-note-extractor, citation-grounding-helper, data-analysis-for-reporting |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, method-note-builder, general-source-summariser, related-work-synthesiser |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, web-data-extractor, source-grounding-extractor, citation-note-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, paper-summariser, spreadsheet-formula-auditor, related-work-synthesiser, document-extractor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, incident-summary-writer, citation-note-extractor, method-note-builder, document-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, citation-note-extractor, related-work-synthesiser, citation-grounding-helper, general-source-summariser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, method-note-builder, multi-source-comparison-builder, general-source-summariser, citation-note-extractor |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, reply-polisher, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `followup-reply-writer` | wrong | followup-reply-writer, reply-polisher, reply-drafter, groupwork-reply, release-note-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, meeting-summary-writer, followup-reply-writer, slide-deck-visual-auditor, meeting-followup-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, groupwork-reply, reply-drafter, reply-polisher, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply, professor-email-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 3 | 3 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, auth-flow-reviewer, security-threat-modeler, security-code-reviewer, secret-leak-scanner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, openapi-contract-reviewer, privacy-risk-reviewer, web-ui-tester |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, capacity-risk-forecaster, database-migration-risk-assessor, service-dependency-mapper, slo-breach-checker |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, deployment-build-triager, security-code-reviewer, dependency-risk-auditor |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, secret-leak-scanner, dependency-risk-auditor, security-code-reviewer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-for-reporting, data-analysis-overview, metrics-overview, database-migration-risk-assessor |
| `skill_p1_find_existing` | `skill-finder` | 7 | 7 | `method-note-builder` | wrong | method-note-builder, task-extractor, meeting-followup-extractor, release-note-writer, meeting-summary-writer |
| `skill_p2_install_existing` | `skill-installer` | 10 | 10 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, data-analysis-overview, data-analysis-with-validation, spreadsheet-formula-auditor, data-analysis-for-ranking-selection |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, task-extractor, skill-finder, meeting-followup-extractor |
| `skill_p4_edit_existing` | `skill-editor` | 5 | 5 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, task-extractor, document-summariser, skill-editor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 6 | 6 | `reply-drafter` | wrong | reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 4 | 4 | `document-summariser` | wrong | document-summariser, paper-summariser, general-source-summariser, skill-packager, method-note-builder |

### `m2b_minilm_full_skill` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, architecture-boundary-reviewer, database-migration-risk-assessor, service-dependency-mapper |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, auth-flow-reviewer, openapi-contract-reviewer, webhook-contract-planner, privacy-risk-reviewer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, openapi-contract-reviewer, latency-anomaly-detector, external-api-integration-planner, auth-flow-reviewer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, database-migration-risk-assessor, openapi-contract-reviewer, security-threat-modeler |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, architecture-boundary-reviewer, deployment-build-triager, dependency-risk-auditor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 9 | 9 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, metrics-root-cause-diagnoser, metrics-overview, slo-breach-checker, incident-summary-writer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, web-page-snapshotter, web-ui-tester, playwright-flow-debugger, accessibility-interaction-auditor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, web-page-snapshotter, frontend-debugger |
| `web_p3_ui_test` | `web-ui-tester` | 8 | 8 | `deployment-release-verifier` | wrong | deployment-release-verifier, ci-failure-debugger, code-reviewer, visual-regression-checker, web-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, document-field-extractor, web-page-snapshotter, pdf-layout-reviewer, layout-preserving-converter |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, playwright-flow-debugger, deployment-release-verifier, auth-flow-reviewer, web-ui-tester |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, visual-regression-checker, frontend-debugger |
| `code_p1_local_code_review` | `code-reviewer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, professor-email-reply, privacy-risk-reviewer, deployment-release-verifier, code-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 4 | 4 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, code-reviewer, openapi-contract-reviewer, pr-reviewer, external-api-integration-planner |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, ci-failure-debugger, code-reviewer, pr-reviewer, auth-flow-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, deployment-release-verifier, frontend-debugger, deployment-build-triager |
| `code_p5_changelog_entry` | `changelog-writer` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, changelog-writer, review-comment-resolver, deployment-release-verifier, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, deployment-release-verifier, privacy-risk-reviewer, deployment-build-triager, release-note-writer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting, news-briefing-writer, news-theme-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, incident-summary-writer, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `data-analysis-with-anomaly-focus` | wrong | data-analysis-with-anomaly-focus, data-analysis-with-validation, latency-anomaly-detector, data-analysis-overview, data-analysis-for-root-cause-diagnosis |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, metrics-root-cause-diagnoser, data-analysis-with-anomaly-focus |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, news-summariser, news-theme-extractor, tech-news-trend-extractor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-with-anomaly-focus, tech-news-trend-extractor, news-theme-extractor |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, data-analysis-for-forecasting, data-analysis-with-validation, weekly-planner, capacity-risk-forecaster |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, auth-flow-reviewer, web-form-filler, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, web-performance-budget-checker, web-page-snapshotter, pdf-layout-reviewer, office-to-markdown-converter |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, visual-regression-checker, web-form-filler, playwright-flow-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, deployment-release-verifier, ci-failure-debugger, changelog-writer, playwright-flow-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, deployment-build-triager, playwright-flow-debugger, visual-regression-checker, frontend-debugger |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, visual-regression-checker, deployment-build-triager, accessibility-checker, accessibility-interaction-auditor |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `release-note-writer` | wrong | release-note-writer, privacy-risk-reviewer, database-migration-risk-assessor, document-summariser, meeting-followup-extractor |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, document-converter, document-normaliser, document-summariser, reply-polisher |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, document-rewriter, document-converter, layout-preserving-converter, document-summariser |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, document-summariser, document-extractor, layout-preserving-converter, document-rewriter |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, changelog-writer, related-work-synthesiser, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, office-to-markdown-converter, document-normaliser, layout-preserving-converter, document-rewriter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, document-normaliser, office-to-markdown-converter |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, web-page-snapshotter, service-dependency-mapper, slo-breach-checker, deployment-build-triager |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, incident-summary-writer, openapi-contract-reviewer |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, deployment-release-verifier, capacity-risk-forecaster, latency-anomaly-detector |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, incident-summary-writer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 7 | 7 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, metrics-overview, slo-breach-checker, capacity-risk-forecaster, web-performance-budget-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, slo-breach-checker, deployment-release-verifier, deployment-build-triager |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, news-theme-extractor, tech-news-trend-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, news-summariser, meeting-summary-writer, meeting-followup-extractor, news-theme-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, source-grounding-extractor, document-extractor, related-work-synthesiser, citation-grounding-helper |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, office-to-markdown-converter, layout-preserving-converter, web-page-snapshotter |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, office-to-markdown-converter, document-normaliser, document-converter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, document-rewriter, document-normaliser, pdf-layout-reviewer, document-summariser |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, data-analysis-with-validation, data-analysis-for-ranking-selection, data-analysis-for-reporting, data-analysis-overview |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, pdf-layout-reviewer, news-briefing-writer, related-work-synthesiser |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `docx-redline-editor` | wrong | docx-redline-editor, office-to-markdown-converter, document-normaliser, document-field-extractor, layout-preserving-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, task-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, task-extractor, meeting-followup-extractor, news-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `meeting-summary-writer` | wrong | meeting-summary-writer, task-extractor, meeting-followup-extractor, meeting-agenda-builder, news-briefing-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, multi-source-comparison-builder, method-note-builder, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, document-extractor, source-grounding-extractor, paper-summariser, method-note-builder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, paper-summariser, related-work-synthesiser, general-source-summariser, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, web-data-extractor, source-grounding-extractor, method-note-builder |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, paper-summariser, document-extractor, related-work-synthesiser, citation-grounding-helper |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, document-extractor, method-note-builder, citation-note-extractor, source-grounding-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, related-work-synthesiser, general-source-summariser, citation-note-extractor, paper-summariser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, multi-source-comparison-builder, general-source-summariser, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, groupwork-reply, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, professor-email-reply, release-note-writer, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, weekly-planner, meeting-followup-extractor, meeting-summary-writer, task-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, groupwork-reply, professor-email-reply, reply-drafter, reply-polisher |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 6 | 6 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-code-reviewer, secret-leak-scanner, auth-flow-reviewer, dependency-risk-auditor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, frontend-debugger, openapi-contract-reviewer, web-ui-tester, security-code-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, secret-leak-scanner, service-dependency-mapper, database-migration-risk-assessor, privacy-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-build-triager, deployment-release-verifier, privacy-risk-reviewer, code-reviewer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, secret-leak-scanner, security-code-reviewer, accessibility-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-overview, data-analysis-for-reporting, secret-leak-scanner, metrics-overview |
| `skill_p1_find_existing` | `skill-finder` | 9 | 9 | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, task-extractor, meeting-agenda-builder, skill-editor |
| `skill_p2_install_existing` | `skill-installer` | 8 | 8 | `data-analysis-overview` | wrong | data-analysis-overview, spreadsheet-formula-auditor, data-analysis-for-reporting, data-analysis-with-validation, data-analysis-for-root-cause-diagnosis |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, task-extractor, skill-editor, meeting-summary-writer, meeting-followup-extractor |
| `skill_p4_edit_existing` | `skill-editor` | 12 | 12 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, document-summariser, method-note-builder, document-rewriter |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 5 | 5 | `reply-polisher` | wrong | reply-polisher, reply-drafter, professor-email-reply, followup-reply-writer, skill-evaluator |
| `skill_p6_package_existing` | `skill-packager` | 3 | 3 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, skill-packager, document-summariser, citation-note-extractor |

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

### `m6_minilm_full_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, webhook-contract-planner, database-migration-risk-assessor, service-dependency-mapper |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, auth-flow-reviewer, webhook-contract-planner, database-migration-risk-assessor |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, latency-anomaly-detector, openapi-contract-reviewer, auth-flow-reviewer, followup-reply-writer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, service-dependency-mapper, dependency-risk-auditor, security-threat-modeler, database-migration-risk-assessor |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, dependency-risk-auditor, architecture-boundary-reviewer, openapi-contract-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, latency-anomaly-detector, metrics-root-cause-diagnoser, metrics-overview, slo-breach-checker |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, visual-regression-checker, accessibility-interaction-auditor, web-ui-tester, pdf-layout-reviewer |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, web-page-snapshotter, web-data-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, deployment-release-verifier, ci-failure-debugger, code-reviewer, web-page-snapshotter |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, pdf-ocr-extractor, document-field-extractor, pdf-layout-reviewer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, playwright-flow-debugger, openapi-contract-reviewer, webhook-contract-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, slo-breach-checker, web-ui-tester |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, professor-email-reply, auth-flow-reviewer, privacy-risk-reviewer, changelog-writer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, auth-flow-reviewer, external-api-integration-planner, review-comment-resolver, code-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, code-reviewer, pr-reviewer, ci-failure-debugger, reply-drafter |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, web-ui-tester, frontend-debugger, auth-flow-reviewer, deployment-build-triager |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, deployment-release-verifier, review-comment-resolver, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, deployment-release-verifier, auth-flow-reviewer, changelog-writer, frontend-debugger |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-forecasting` | wrong | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-reporting, data-analysis-for-ranking-selection, news-briefing-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, data-analysis-with-anomaly-focus, latency-anomaly-detector, slo-breach-checker, data-analysis-for-root-cause-diagnosis |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, latency-anomaly-detector, data-analysis-with-anomaly-focus |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, news-summariser, data-analysis-overview, data-analysis-for-forecasting |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, data-analysis-for-forecasting, capacity-risk-forecaster, meeting-followup-extractor, weekly-planner |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, auth-flow-reviewer, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-layout-reviewer, web-performance-budget-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, frontend-debugger, web-form-filler, web-ui-tester |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, ci-failure-debugger, frontend-debugger, metrics-root-cause-diagnoser, deployment-release-verifier |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, deployment-build-triager, release-note-writer, playwright-flow-debugger, web-performance-budget-checker |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, pdf-layout-reviewer, visual-regression-checker, frontend-debugger, deployment-build-triager |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, release-note-writer, privacy-risk-reviewer, database-migration-risk-assessor, meeting-followup-extractor |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, document-converter, document-normaliser, document-summariser |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, document-rewriter, document-converter, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, web-data-extractor, document-extractor, method-note-builder, document-summariser |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, release-note-writer, docx-redline-editor, pr-reviewer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-converter, task-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, incident-summary-writer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, data-analysis-with-anomaly-focus, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, deployment-release-verifier, service-dependency-mapper, metrics-overview, dependency-risk-auditor |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, data-analysis-for-forecasting, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `service-dependency-mapper` | wrong | service-dependency-mapper, metrics-root-cause-diagnoser, latency-anomaly-detector, metrics-overview, web-performance-budget-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, slo-breach-checker, service-dependency-mapper, release-note-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, news-theme-extractor, general-source-summariser, tech-news-trend-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, meeting-summary-writer, news-summariser, incident-summary-writer, metrics-overview |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, general-source-summariser, document-extractor, citation-note-extractor, news-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, metrics-root-cause-diagnoser |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, web-data-extractor, document-field-extractor, web-page-snapshotter |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, web-page-snapshotter, document-converter, office-to-markdown-converter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, review-comment-resolver, multi-document-comparison-preparer, document-rewriter, document-normaliser |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, data-analysis-with-validation, capacity-risk-forecaster, database-migration-risk-assessor, data-analysis-for-reporting |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, pdf-layout-reviewer, pr-reviewer, news-theme-extractor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, docx-redline-editor, document-converter, changelog-writer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, weekly-planner, task-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, task-extractor, news-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, task-extractor, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, release-note-writer, meeting-summary-writer, weekly-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, meeting-summary-writer, task-extractor, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, method-note-builder, citation-note-extractor, multi-source-comparison-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, data-analysis-for-reporting, document-extractor, method-note-builder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, method-note-builder, general-source-summariser, release-note-writer |
| `read_p4_document_extraction` | `document-extractor` | 3 | 3 | `web-data-extractor` | wrong | web-data-extractor, document-field-extractor, document-extractor, method-note-builder, source-grounding-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, paper-summariser, related-work-synthesiser, spreadsheet-formula-auditor, multi-source-comparison-builder |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, citation-note-extractor, document-extractor, source-grounding-extractor, method-note-builder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, related-work-synthesiser, citation-note-extractor, method-note-builder, news-briefing-writer |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-source-comparison-builder, multi-document-comparison-preparer, release-note-writer, citation-note-extractor |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, reply-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, followup-reply-writer, professor-email-reply |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, meeting-followup-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, groupwork-reply, reply-drafter, meeting-followup-extractor, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, dependency-risk-auditor, auth-flow-reviewer, release-note-writer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, frontend-debugger, openapi-contract-reviewer, web-ui-tester |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, architecture-boundary-reviewer, database-migration-risk-assessor, service-dependency-mapper, capacity-risk-forecaster |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, deployment-build-triager, metrics-overview, pr-reviewer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, accessibility-checker, changelog-writer, data-analysis-with-validation |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, privacy-risk-reviewer, data-analysis-for-ranking-selection, data-analysis-for-root-cause-diagnosis, data-analysis-with-anomaly-focus |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, release-note-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, data-analysis-for-reporting, data-analysis-overview, spreadsheet-formula-auditor, data-analysis-with-validation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-finder, skill-editor, meeting-followup-extractor, task-extractor |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `document-field-extractor` | wrong | document-field-extractor, skill-editor, document-extractor, skill-finder, multi-document-comparison-preparer |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, professor-email-reply, followup-reply-writer |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, general-source-summariser, skill-installer, document-summariser |

### `m1_bm25_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, public-openai-gh-address-comments, graphql-schema-designer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, openapi-contract-tester, public-openai-figma-code-connect-components, database-backup-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, invoice-payment-checker, public-office-invoice-automation, api-design-reviewer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, agent-handoff-orchestrator, refactor-planner, public-office-diagram-creator |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, query-optimizer, infrastructure-as-code-planner |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, privacy-policy-drafter, architecture-boundary-reviewer, data-analysis-for-reporting, skill-evaluator |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, public-openai-screenshot, public-openai-figma-generate-design, metrics-overview |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-office-pdf-form-filler, public-openai-playwright, seed-data-generator, web-ui-tester |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, dashboard-ops-acceptance-test-builder, skill-evaluator, openapi-contract-tester |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, product-ops-resource-linker, pdf-layout-reviewer, web-page-snapshotter |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, debugging-root-cause-helper, public-openai-figma-use, public-openai-speech |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, reply-drafter, slo-breach-checker, deck-template-applier |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, email-thread-summariser, release-note-writer, git-commit-writer, changelog-writer |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `pr-description-writer` | wrong | pr-description-writer, pr-reviewer, public-openai-gh-address-comments, openapi-contract-reviewer, database-migration-risk-assessor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-description-writer, public-openai-gh-address-comments, code-reviewer, reply-drafter |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, openapi-contract-reviewer, frontend-debugger, public-openai-gh-fix-ci, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, git-commit-writer, pr-description-writer, citation-note-extractor |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-office-changelog-generator, slo-breach-checker, pr-description-writer, news-theme-extractor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, citation-note-extractor, data-analysis-for-forecasting, public-office-data-analysis, financial-report-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, debugging-root-cause-helper, public-office-data-analysis, metrics-root-cause-diagnoser, general-source-summariser |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-with-anomaly-focus, slo-breach-checker, public-openai-linear |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 15 | 15 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, public-office-data-analysis, variance-analysis-helper, web-performance-budget-checker, public-office-stock-analysis |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `public-office-data-analysis` | wrong | public-office-data-analysis, data-analysis-for-reporting, public-office-stock-analysis, financial-report-writer, public-office-crypto-report |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, public-office-weather-automation, followup-reply-writer, debugging-root-cause-helper |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, priority-sorter, variance-analysis-helper, dashboard-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, security-threat-modeler |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, public-anthropic-canvas-design, slide-deck-visual-auditor, latency-anomaly-detector, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, infrastructure-as-code-planner, web-form-filler |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `public-netlify-deploy` | wrong | public-netlify-deploy, metrics-root-cause-diagnoser, debugging-root-cause-helper, frontend-debugger, kubernetes-deployment-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, deployment-build-triager, public-office-changelog-generator |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, decision-matrix-builder, mobile-ops-acceptance-test-builder, review-comment-resolver, docker-compose-configurator |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `general-source-summariser` | wrong | general-source-summariser, citation-note-extractor, data-analysis-with-validation, document-summariser, public-pdf |
| `doc_p2_document_rewriter` | `document-rewriter` | 3 | 3 | `public-docx` | wrong | public-docx, reply-polisher, document-rewriter, public-office-form-builder, public-office-docx-manipulation |
| `doc_p3_document_normaliser` | `document-normaliser` | 5 | 5 | `layout-preserving-converter` | wrong | layout-preserving-converter, public-docx, deck-template-applier, pdf-layout-reviewer, document-normaliser |
| `doc_p4_field_extraction` | `document-field-extractor` | 4 | 4 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, document-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, public-docx, decision-matrix-builder, public-office-docx-manipulation |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, deck-template-applier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `document-converter` | wrong | document-converter, layout-preserving-converter, pdf-layout-reviewer, note-tagger, office-to-markdown-converter |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, related-work-synthesiser, public-openai-vercel-deploy, public-anthropic-mcp-builder, cloud-monitoring-configurer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, slo-breach-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 6 | 6 | `metrics-overview` | wrong | metrics-overview, public-office-contract-review, architecture-boundary-reviewer, risk-ops-compliance-checker, risk-ops-acceptance-test-builder |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, metrics-root-cause-diagnoser, debugging-root-cause-helper, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, public-openai-playwright, capacity-risk-forecaster, rag-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 4 | 4 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, public-openai-linear, metrics-overview, incident-summary-writer, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, public-office-news-monitor, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, metrics-overview, public-office-content-writer, data-analysis-for-reporting |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 8 | 8 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, citation-note-extractor, document-field-extractor, document-summariser, agent-handoff-orchestrator |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-anthropic-theme-factory, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-briefing-writer, news-theme-extractor, capacity-risk-forecaster |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-pdf, public-openai-pdf, public-office-pdf-form-filler, public-office-chat-with-pdf |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `public-pdf` | wrong | public-pdf, pdf-ocr-extractor, public-markitdown, public-office-pdf-watermark, public-office-office-mcp |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, public-office-docx-manipulation, layout-preserving-converter, multi-document-comparison-preparer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 3 | 3 | `rag-failure-diagnoser` | wrong | rag-failure-diagnoser, web-ui-tester, spreadsheet-formula-auditor, data-analysis-with-validation, citation-grounding-helper |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, customer-feedback-analyser, public-office-infographic, public-office-ppt-visual |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, document-converter, public-markitdown |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, public-openai-notion-meeting-intelligence, public-pptx, followup-reply-writer, public-office-telegram-bot |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 11 | 11 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, general-source-summariser, paper-summariser, meeting-ops-summary-writer, public-office-transcription-automation |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 9 | 9 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, followup-reply-writer, meeting-summary-writer, public-architecture-patterns, document-normaliser |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, release-note-writer, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-scheduler` | wrong | meeting-scheduler, public-openai-notion-meeting-intelligence, meeting-agenda-builder, multi-document-comparison-preparer, agent-eval-coverage-auditor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, multi-source-comparison-builder, general-source-summariser, citation-note-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, public-openai-security-best-practices, academic-admin-ops-summary-writer, operations-ops-summary-writer, public-office-academic-search |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-evidence-grounder, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | 8 | 8 | `web-data-extractor` | wrong | web-data-extractor, public-office-pdf-extraction, bioinformatics-ops-field-extractor, compliance-ops-field-extractor, contract-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `pr-description-writer` | wrong | pr-description-writer, citation-grounding-helper, speaker-notes-writer, web-data-extractor, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-eval-coverage-auditor, seed-data-generator, skill-evaluator, agent-ops-resource-linker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 3 | 3 | `news-briefing-writer` | wrong | news-briefing-writer, note-tagger, multi-source-comparison-builder, public-openai-define-goal, data-analysis-for-ranking-selection |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 3 | 3 | `public-openai-notion-research-documentation` | wrong | public-openai-notion-research-documentation, multi-document-comparison-preparer, related-work-synthesiser, public-office-academic-search, data-analysis-for-reporting |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, email-polisher, followup-reply-writer, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, proposal-drafter, email-action-extractor, followup-reply-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, public-office-investment-memo, email-action-extractor, bioinformatics-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, email-polisher, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-brainstorming, public-security-threat-model, public-openai-figma-code-connect-components, business-plan-builder |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, accessibility-checker, public-openai-gh-address-comments, identity-ops-acceptance-test-builder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, pr-reviewer, priority-sorter, architecture-boundary-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, public-openai-vercel-deploy, deployment-release-verifier, public-anthropic-internal-comms |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, version-control-helper, accessibility-checker, email-action-extractor |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `churn-risk-analyser` | wrong | churn-risk-analyser, query-optimizer, release-note-writer, public-office-web-search, knowledge-base-article-writer |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, incident-summary-writer, public-openai-notion-knowledge-capture, slo-breach-checker, skill-editor |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, public-anthropic-webapp-testing, code-reviewer, docker-compose-configurator, skill-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, public-skill-creator, public-anthropic-skill-creator, skill-editor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-evaluator, data-analysis-overview, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, agent-eval-coverage-auditor, citation-grounding-helper, reply-polisher, skill-finder |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, agent-ops-resource-linker, public-anthropic-skill-creator, skill-finder |

### `m1_tfidf_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, contract-ops-acceptance-test-builder, api-design-reviewer, api-ops-acceptance-test-builder |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 5 | 2 | `public-openai-figma-code-connect-components` | wrong | public-openai-figma-code-connect-components, api-integration-planner, api-ops-acceptance-test-builder, public-office-cover-letter, external-api-integration-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 3 | 3 | `invoice-payment-checker` | wrong | invoice-payment-checker, public-openai-winui-app, webhook-contract-planner, duplicate-file-finder, webhook-setup-planner |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-openai-security-ownership-map, public-office-md-slides, public-office-office-to-md |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-rollback-planner, migration-risk-auditor, query-optimizer, public-openai-winui-app |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, public-office-md-slides, public-office-office-to-md, public-office-md-to-office, analytics-ops-quality-auditor |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, public-openai-screenshot, public-openai-figma-generate-design, landing-page-copy-reviewer, pdf-layout-reviewer |
| `web_p2_form_filling` | `web-form-filler` | 6 | 6 | `variance-analysis-helper` | wrong | variance-analysis-helper, public-office-pdf-form-filler, public-openai-playwright, public-office-expense-report, public-office-weekly-report |
| `web_p3_ui_test` | `web-ui-tester` | 9 | 9 | `variance-analysis-helper` | wrong | variance-analysis-helper, web-page-snapshotter, public-office-expense-report, public-office-weekly-report, compliance-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-resource-linker` | wrong | product-ops-resource-linker, product-ops-field-extractor, product-ops-normalizer, product-ops-compliance-checker, product-ops-dependency-mapper |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, api-ops-evidence-grounder, api-ops-field-extractor, api-ops-normalizer, api-ops-summary-writer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, public-office-pdf-form-filler, layout-preserving-converter, public-openai-playwright |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer, risk-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, public-openai-gh-address-comments, public-openai-yeet, api-ops-acceptance-test-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, public-openai-gh-address-comments, pr-reviewer, pr-description-writer, webhook-setup-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, public-openai-gh-fix-ci, git-commit-writer, public-office-job-description |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-office-changelog-generator, auth-flow-reviewer, public-anthropic-internal-comms |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-office-changelog-generator, web-ui-tester, slo-breach-checker, terms-of-service-drafter |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-forecasting, public-office-expense-report, public-office-weekly-report |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, debugging-root-cause-helper, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 6 | 6 | `public-openai-linear` | wrong | public-openai-linear, public-office-suspicious-email, public-anthropic-web-artifacts-builder, public-huggingface-datasets, public-office-pdf-watermark |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, public-office-data-analysis, metrics-root-cause-diagnoser, public-office-stock-analysis, public-xlsx |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dashboard-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer, public-office-data-analysis, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, duplicate-file-finder, data-analysis-for-root-cause-diagnosis, public-markitdown |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, risk-ops-comparison-builder, dashboard-ops-comparison-builder, data-analysis-overview |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, accessibility-interaction-auditor, public-playwright-interactive, public-office-browser-automation |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector, code-reviewer |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, public-office-pdf-form-filler, infrastructure-as-code-planner |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 12 | 12 | `public-netlify-deploy` | wrong | public-netlify-deploy, debugging-root-cause-helper, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, frontend-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, release-note-writer, public-office-changelog-generator |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, budget-planner, mobile-ops-acceptance-test-builder, mobile-ops-normalizer, mobile-ops-monitoring-plan-builder |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, knowledge-base-article-writer, general-source-summariser, receipt-extractor, multi-source-comparison-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, public-office-pdf-form-filler, public-office-form-builder |
| `doc_p3_document_normaliser` | `document-normaliser` | 3 | 3 | `layout-preserving-converter` | wrong | layout-preserving-converter, deck-template-applier, document-normaliser, docx-redline-editor, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 7 | 7 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, public-office-invoice-automation, meeting-followup-extractor, public-office-table-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, multi-document-comparison-preparer, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 4 | 4 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-converter, content-ops-evidence-grounder |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, public-office-layout-analyzer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, terms-of-service-drafter, related-work-synthesiser, data-analysis-overview |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, data-analysis-overview, web-performance-budget-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 8 | 8 | `public-office-contract-review` | wrong | public-office-contract-review, risk-ops-risk-reviewer, metrics-overview, sre-ops-risk-reviewer, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, debugging-root-cause-helper, risk-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, debugging-root-cause-helper, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 7 | `incident-ops-normalizer` | wrong | incident-ops-normalizer, incident-ops-compliance-checker, incident-ops-dependency-mapper, metrics-overview, incident-ops-scenario-planner |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, support-ticket-triager, support-ops-timeline-builder, support-ops-comparison-builder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 3 | 3 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, product-ops-evidence-grounder, source-grounding-extractor, product-ops-scenario-planner, product-ops-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, public-office-news-monitor, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, public-office-news-monitor, news-theme-extractor, news-briefing-writer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-office-pdf-watermark, public-office-chat-with-pdf, public-office-pdf-extraction |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, public-office-pdf-converter, public-office-pdf-ocr, pdf-layout-reviewer |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, public-office-docx-manipulation, document-rewriter, public-office-pdf-to-docx |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-office-contract-review, rag-failure-diagnoser, public-office-xlsx-manipulation, public-xlsx |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, public-office-ppt-visual, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, docx-redline-editor, public-office-docx-manipulation |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-scenario-planner, meeting-ops-normalizer, meeting-ops-compliance-checker, meeting-ops-dependency-mapper |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | - | - | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-ops-evidence-grounder, meeting-ops-normalizer, meeting-ops-artifact-packager, meeting-ops-compliance-checker |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, public-office-transcription-automation |
| `plan_p4_task_extractor` | `task-extractor` | 4 | 4 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-followup-extractor, meeting-summary-writer, task-extractor, meeting-ops-evidence-grounder |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-ops-monitoring-plan-builder, meeting-ops-acceptance-test-builder, meeting-ops-summary-writer, meeting-ops-normalizer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, public-office-academic-search, method-note-builder, research-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, academic-admin-ops-summary-writer, professor-email-reply, academic-admin-ops-evidence-grounder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, writing-ops-evidence-grounder, writing-ops-field-extractor, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | - | - | `public-office-table-extractor` | wrong | public-office-table-extractor, research-ops-field-extractor, compliance-ops-field-extractor, docs-ops-field-extractor, partnerships-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, citation-grounding-helper, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, tool-use-coach, document-extractor, citation-note-extractor, source-grounding-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 7 | 7 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, citation-grounding-helper, note-linker |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, public-office-table-extractor, release-note-writer, public-openai-notion-research-documentation, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 2 | 2 | `reply-drafter` | wrong | reply-drafter, professor-email-reply, reply-polisher, email-polisher, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, email-polisher, deck-template-applier |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, reply-polisher, followup-reply-writer, deadline-reminder-planner |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, public-office-investment-memo, email-action-extractor, public-office-security-monitoring |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, public-openai-figma-create-new-file, reply-polisher, followup-reply-writer, docker-compose-configurator |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `public-openai-figma-create-new-file` | wrong | public-openai-figma-create-new-file, security-threat-modeler, email-ops-risk-reviewer, public-security-threat-model, email-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, api-ops-acceptance-test-builder, review-comment-resolver, code-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 19 | 19 | `supply-chain-ops-risk-reviewer` | wrong | supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-artifact-packager, supply-chain-ops-normalizer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, public-office-webhook-automation, webhook-setup-planner, database-ops-normalizer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-ops-monitoring-plan-builder, version-control-helper, email-ops-normalizer, email-ops-compliance-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, query-optimizer, product-ops-normalizer, public-office-data-pipeline, product-ops-compliance-checker |
| `skill_p1_find_existing` | `skill-finder` | - | - | `public-office-meeting-notes` | wrong | public-office-meeting-notes, library-ops-evidence-grounder, meeting-ops-evidence-grounder, library-ops-timeline-builder, search-ops-evidence-grounder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, library-ops-resource-linker, library-ops-acceptance-test-builder, public-office-expense-report, code-reviewer |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, public-anthropic-skill-creator, public-skill-creator, public-openai-figma-create-new-file, skill-editor |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `public-anthropic-skill-creator` | wrong | public-anthropic-skill-creator, skill-editor, public-skill-creator, skill-finder, skill-installer |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, public-anthropic-skill-creator |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-anthropic-skill-creator, public-skill-creator, skill-installer |

### `m2a_minilm_description` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-ops-summary-writer, api-integration-planner, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 1 | `api-integration-planner` | acceptable | api-integration-planner, external-api-integration-planner, auth-flow-reviewer, api-ops-summary-writer, api-ops-scenario-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, events-ops-acceptance-test-builder, events-ops-intake-classifier, events-ops-artifact-packager, customer-success-ops-artifact-packager |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, openapi-contract-reviewer, database-migration-risk-assessor, service-dependency-mapper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, database-ops-acceptance-test-builder, publishing-ops-acceptance-test-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `customer-feedback-analyser` | wrong | customer-feedback-analyser, dashboard-ops-quality-auditor, api-ops-quality-auditor, analytics-ops-failure-diagnoser, analytics-ops-quality-auditor |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, web-page-snapshotter, analytics-ops-acceptance-test-builder, dashboard-ops-acceptance-test-builder, environment-config-auditor |
| `web_p2_form_filling` | `web-form-filler` | 3 | 3 | `web-ui-tester` | wrong | web-ui-tester, identity-ops-acceptance-test-builder, web-form-filler, web-ops-acceptance-test-builder, marketing-ops-acceptance-test-builder |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `facilities-ops-acceptance-test-builder` | wrong | facilities-ops-acceptance-test-builder, email-ops-acceptance-test-builder, vendor-ops-acceptance-test-builder, contract-ops-acceptance-test-builder, customer-success-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 2 | 2 | `product-ops-field-extractor` | wrong | product-ops-field-extractor, web-data-extractor, sales-ops-field-extractor, receipt-extractor, supply-chain-ops-field-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, api-ops-failure-diagnoser, environment-config-auditor, property-ops-failure-diagnoser, deployment-rollback-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, mobile-ops-failure-diagnoser, public-office-form-builder, mobile-ops-acceptance-test-builder |
| `code_p1_local_code_review` | `code-reviewer` | 4 | 4 | `email-ops-acceptance-test-builder` | wrong | email-ops-acceptance-test-builder, localization-ops-acceptance-test-builder, repo-ops-acceptance-test-builder, code-reviewer, api-ops-acceptance-test-builder |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, pr-reviewer, api-ops-acceptance-test-builder, public-openai-gh-address-comments, api-integration-planner |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, ci-failure-debugger, code-reviewer, sre-ops-risk-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, api-ops-failure-diagnoser, identity-ops-failure-diagnoser, frontend-debugger, grant-ops-failure-diagnoser |
| `code_p5_changelog_entry` | `changelog-writer` | 3 | 2 | `release-note-writer` | wrong | release-note-writer, public-office-changelog-generator, changelog-writer, repo-ops-failure-diagnoser, git-commit-writer |
| `code_p6_release_notes` | `release-note-writer` | - | - | `identity-ops-failure-diagnoser` | wrong | identity-ops-failure-diagnoser, auth-flow-reviewer, identity-ops-timeline-builder, identity-ops-acceptance-test-builder, deployment-rollback-planner |
| `data_p1_overview` | `data-analysis-overview` | 13 | 13 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, news-theme-extractor, content-strategy-builder, dashboard-ops-summary-writer, news-briefing-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, debugging-root-cause-helper, churn-risk-analyser, metrics-root-cause-diagnoser |
| `data_p3_validation` | `data-analysis-with-validation` | - | - | `latency-anomaly-detector` | wrong | latency-anomaly-detector, data-analysis-with-anomaly-focus, dataset-ops-quality-auditor, real-estate-ops-failure-diagnoser, analytics-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | - | - | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, latency-anomaly-detector, media-ops-failure-diagnoser, capacity-risk-forecaster, dataset-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `dashboard-ops-summary-writer` | wrong | dashboard-ops-summary-writer, data-analysis-for-reporting, financial-report-writer, news-summariser, news-briefing-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, tech-news-trend-extractor, capacity-risk-forecaster, news-theme-extractor, deadline-reminder-planner |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | - | - | `priority-sorter` | wrong | priority-sorter, decision-matrix-builder, risk-ops-priority-ranker, travel-ops-priority-ranker, database-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 2 | 2 | `frontend-debugger` | wrong | frontend-debugger, playwright-flow-debugger, ecommerce-ops-failure-diagnoser, grant-ops-failure-diagnoser, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, mobile-ops-comparison-builder, dashboard-ops-comparison-builder, docs-ops-comparison-builder, ux-ops-comparison-builder |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, visual-regression-checker, mobile-ops-quality-auditor, writing-ops-quality-auditor |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, ci-failure-debugger, devops-ops-failure-diagnoser, construction-ops-failure-diagnoser |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-release-verifier, deployment-build-triager, public-openai-vercel-deploy, public-openai-render-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 2 | 2 | `mobile-ops-resource-linker` | wrong | mobile-ops-resource-linker, web-performance-budget-checker, mobile-ops-summary-writer, mobile-ops-dependency-mapper, mobile-ops-quality-auditor |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-risk-reviewer` | wrong | travel-ops-risk-reviewer, travel-ops-summary-writer, travel-ops-rewrite-editor, travel-ops-dependency-mapper, travel-ops-compliance-checker |
| `doc_p2_document_rewriter` | `document-rewriter` | 8 | 1 | `travel-ops-rewrite-editor` | acceptable | travel-ops-rewrite-editor, method-note-builder, travel-ops-summary-writer, travel-ops-handoff-brief-writer, paper-summariser |
| `doc_p3_document_normaliser` | `document-normaliser` | 4 | 4 | `travel-ops-rewrite-editor` | wrong | travel-ops-rewrite-editor, public-office-meeting-notes, document-rewriter, document-normaliser, method-note-builder |
| `doc_p4_field_extraction` | `document-field-extractor` | 10 | 10 | `receipt-extractor` | wrong | receipt-extractor, public-office-invoice-organizer, public-office-invoice-automation, public-office-invoice-generator, procurement-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | 2 | `privacy-policy-drafter` | wrong | privacy-policy-drafter, multi-document-comparison-preparer, docs-ops-comparison-builder, writing-ops-comparison-builder, terms-of-service-drafter |
| `doc_p6_conversion` | `document-converter` | 3 | 1 | `public-markitdown` | acceptable | public-markitdown, public-office-form-builder, document-converter, layout-preserving-converter, public-office-template-engine |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `public-office-form-builder` | wrong | public-office-form-builder, layout-preserving-converter, method-note-builder, document-converter, note-tagger |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, iot-ops-quality-auditor, web-page-snapshotter, cloud-ops-failure-diagnoser, cloud-ops-summary-writer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, cloud-ops-failure-diagnoser, api-ops-failure-diagnoser, iot-ops-failure-diagnoser, analytics-ops-failure-diagnoser |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-failure-diagnoser, metrics-overview, sre-ops-risk-reviewer, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, cloud-ops-scenario-planner, risk-ops-failure-diagnoser, support-ops-scenario-planner |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, cloud-ops-failure-diagnoser, platform-ops-failure-diagnoser, support-ops-failure-diagnoser, library-ops-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 14 | 7 | `incident-ops-resource-linker` | wrong | incident-ops-resource-linker, incident-ops-failure-diagnoser, incident-ops-timeline-builder, incident-ops-rewrite-editor, incident-ops-priority-ranker |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, paper-summariser, source-grounding-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 6 | 6 | `events-ops-summary-writer` | wrong | events-ops-summary-writer, events-ops-priority-ranker, events-ops-handoff-brief-writer, incident-summary-writer, meeting-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 18 | 18 | `product-ops-evidence-grounder` | wrong | product-ops-evidence-grounder, public-office-crypto-report, vendor-ops-evidence-grounder, product-ops-summary-writer, ecommerce-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, content-strategy-builder, news-briefing-writer |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, content-strategy-builder, public-office-twitter-automation, news-briefing-writer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-office-pdf-watermark, pdf-ocr-extractor, public-office-pdf-extraction |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-ocr, public-office-pdf-extraction, public-office-smart-ocr, public-office-chat-with-pdf |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, pdf-layout-reviewer, vendor-ops-rewrite-editor, docs-ops-risk-reviewer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 2 | 2 | `public-xlsx` | wrong | public-xlsx, spreadsheet-formula-auditor, public-office-xlsx-manipulation, public-office-financial-modeling, data-analysis-with-validation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-office-ppt-visual, slide-outline-builder, speaker-notes-writer, public-office-ai-slides |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `docx-redline-editor` | wrong | docx-redline-editor, office-to-markdown-converter, public-docx, public-markitdown, layout-preserving-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, task-extractor, meeting-summary-writer, meeting-followup-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-rewrite-editor, meeting-agenda-builder, task-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 5 | 5 | `meeting-summary-writer` | wrong | meeting-summary-writer, task-extractor, meeting-agenda-builder, meeting-ops-rewrite-editor, meeting-followup-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-summary-writer, meeting-followup-extractor, meeting-ops-rewrite-editor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, thesis-ops-scenario-planner, meeting-ops-scenario-planner, research-ops-scenario-planner, agent-ops-scenario-planner |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, general-source-summariser, thesis-ops-summary-writer, multi-source-comparison-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | 3 | 3 | `thesis-ops-evidence-grounder` | wrong | thesis-ops-evidence-grounder, paper-summariser, general-source-summariser, research-ops-evidence-grounder, thesis-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, method-note-builder, general-source-summariser, related-work-synthesiser |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, database-ops-field-extractor, finance-ops-field-extractor, research-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, thesis-ops-summary-writer, paper-summariser, thesis-ops-dependency-mapper, spreadsheet-formula-auditor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, incident-summary-writer, citation-note-extractor, incident-ops-rewrite-editor, agent-ops-summary-writer |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, citation-note-extractor, related-work-synthesiser, citation-grounding-helper, general-source-summariser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, method-note-builder, multi-source-comparison-builder, general-source-summariser, citation-note-extractor |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, email-drafter, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 2 | 2 | `followup-reply-writer` | wrong | followup-reply-writer, reply-polisher, partnerships-ops-rewrite-editor, reply-drafter, groupwork-reply |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, deadline-reminder-planner, meeting-summary-writer, partnerships-ops-handoff-brief-writer, meeting-ops-summary-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, email-action-extractor, groupwork-reply, reply-drafter, reply-polisher |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, email-polisher, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 9 | 9 | `public-openai-security-ownership-map` | wrong | public-openai-security-ownership-map, privacy-risk-reviewer, privacy-ops-resource-linker, security-ops-resource-linker, identity-ops-resource-linker |
| `sec_p2_security_code_review` | `security-code-reviewer` | 4 | 4 | `api-ops-rewrite-editor` | wrong | api-ops-rewrite-editor, auth-flow-reviewer, security-ops-rewrite-editor, security-code-reviewer, api-ops-risk-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-artifact-packager, risk-ops-dependency-mapper, sre-ops-dependency-mapper, security-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, environment-config-auditor, security-ops-rewrite-editor, security-ops-artifact-packager, deployment-release-verifier |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, identity-ops-failure-diagnoser, identity-ops-resource-linker, identity-ops-summary-writer, identity-ops-risk-reviewer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, analytics-ops-risk-reviewer, analytics-ops-quality-auditor, analytics-ops-compliance-checker, data-analysis-for-reporting |
| `skill_p1_find_existing` | `skill-finder` | 10 | 10 | `method-note-builder` | wrong | method-note-builder, task-extractor, meeting-followup-extractor, release-note-writer, meeting-summary-writer |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-office-data-analysis` | wrong | public-office-data-analysis, data-analysis-for-reporting, data-analysis-overview, public-office-sheets-automation, data-analysis-with-validation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, task-extractor, skill-finder, thesis-ops-timeline-builder |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `document-field-extractor` | wrong | document-field-extractor, docs-ops-field-extractor, writing-ops-field-extractor, course-ops-field-extractor, thesis-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 11 | 11 | `reply-drafter` | wrong | reply-drafter, reply-polisher, email-polisher, followup-reply-writer, email-drafter |
| `skill_p6_package_existing` | `skill-packager` | - | - | `public-anthropic-doc-coauthoring` | wrong | public-anthropic-doc-coauthoring, public-office-content-writer, document-summariser, docs-ops-summary-writer, public-office-chat-with-pdf |

### `m2b_minilm_full_skill` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, architecture-boundary-reviewer, database-migration-risk-assessor, service-dependency-mapper |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, auth-flow-reviewer, openapi-contract-reviewer, api-ops-monitoring-plan-builder, webhook-contract-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, openapi-contract-reviewer, latency-anomaly-detector, receipt-extractor, invoice-payment-checker |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, service-dependency-mapper, database-migration-risk-assessor, openapi-contract-reviewer |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, architecture-boundary-reviewer, deployment-build-triager, deployment-rollback-planner |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `latency-anomaly-detector` | wrong | latency-anomaly-detector, metrics-root-cause-diagnoser, metrics-overview, support-ops-monitoring-plan-builder, dashboard-ops-monitoring-plan-builder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, web-page-snapshotter, web-ui-tester, playwright-flow-debugger, accessibility-interaction-auditor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, web-page-snapshotter, marketing-ops-acceptance-test-builder |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `procurement-ops-acceptance-test-builder` | wrong | procurement-ops-acceptance-test-builder, facilities-ops-acceptance-test-builder, property-ops-acceptance-test-builder, email-ops-acceptance-test-builder, social-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, ecommerce-ops-field-extractor, product-ops-field-extractor, ecommerce-ops-summary-writer, retail-ops-field-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, public-api-design-principles, public-playwright-interactive, public-openai-gh-fix-ci, public-office-calendar-automation |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, visual-regression-checker, frontend-debugger |
| `code_p1_local_code_review` | `code-reviewer` | 16 | 16 | `email-ops-acceptance-test-builder` | wrong | email-ops-acceptance-test-builder, email-ops-failure-diagnoser, public-office-email-drafter, auth-flow-reviewer, professor-email-reply |
| `code_p2_pr_review` | `pr-reviewer` | 8 | 8 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, code-reviewer, api-ops-risk-reviewer, api-ops-acceptance-test-builder, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, ci-failure-debugger, code-reviewer, pr-reviewer, auth-flow-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, repo-ops-failure-diagnoser, ci-cd-pipeline-builder, deployment-release-verifier |
| `code_p5_changelog_entry` | `changelog-writer` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, changelog-writer, review-comment-resolver, deployment-release-verifier, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | - | - | `auth-flow-reviewer` | wrong | auth-flow-reviewer, mobile-ops-risk-reviewer, mobile-ops-timeline-builder, mobile-ops-compliance-checker, identity-ops-failure-diagnoser |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-reporting, news-briefing-writer, news-theme-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, incident-summary-writer, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `data-analysis-with-anomaly-focus` | wrong | data-analysis-with-anomaly-focus, data-analysis-with-validation, latency-anomaly-detector, dataset-ops-quality-auditor, data-analysis-overview |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 3 | 3 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, dataset-ops-failure-diagnoser, data-analysis-for-root-cause-diagnosis, marketing-ops-failure-diagnoser, ml-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, news-summariser, news-theme-extractor, tech-news-trend-extractor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-with-anomaly-focus, tech-news-trend-extractor, news-theme-extractor |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, travel-ops-priority-ranker, finance-ops-priority-ranker, supply-chain-ops-priority-ranker, logistics-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, auth-flow-reviewer, public-office-stripe-payments, web-form-filler |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, web-performance-budget-checker, web-page-snapshotter, pdf-layout-reviewer, office-to-markdown-converter |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, visual-regression-checker, web-form-filler, playwright-flow-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, devops-ops-failure-diagnoser, deployment-release-verifier, devops-ops-summary-writer |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-release-verifier, deployment-build-triager, public-openai-vercel-deploy, public-openai-render-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-summary-writer, mobile-ops-quality-auditor, mobile-ops-resource-linker, mobile-ops-risk-reviewer |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-scenario-planner, travel-ops-rewrite-editor, travel-ops-priority-ranker, travel-ops-risk-reviewer |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, travel-ops-rewrite-editor, document-converter, travel-ops-summary-writer, document-normaliser |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, document-rewriter, travel-ops-rewrite-editor, document-converter, layout-preserving-converter |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, supply-chain-ops-field-extractor, receipt-extractor, procurement-ops-field-extractor, supply-chain-ops-summary-writer |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | 1 | `legal-ops-comparison-builder` | acceptable | legal-ops-comparison-builder, multi-document-comparison-preparer, writing-ops-comparison-builder, docs-ops-comparison-builder, multi-source-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, office-to-markdown-converter, document-normaliser, layout-preserving-converter, document-rewriter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, document-normaliser, office-to-markdown-converter |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, web-page-snapshotter, service-dependency-mapper, slo-breach-checker, deployment-build-triager |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, cloud-monitoring-configurer, api-ops-monitoring-plan-builder |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, sre-ops-failure-diagnoser, sre-ops-risk-reviewer, sre-ops-quality-auditor |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, incident-summary-writer, sre-ops-scenario-planner |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 19 | 19 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, metrics-overview, slo-breach-checker, support-ops-failure-diagnoser, capacity-risk-forecaster |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-field-extractor, incident-ops-timeline-builder, slo-breach-checker |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, news-theme-extractor, tech-news-trend-extractor, journalism-ops-summary-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, news-summariser, meeting-summary-writer, events-ops-summary-writer, meeting-followup-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 4 | 4 | `public-office-crypto-report` | wrong | public-office-crypto-report, public-office-stock-analysis, general-source-summariser, source-grounding-extractor, ecommerce-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-summariser, news-briefing-writer, social-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-pdf, public-office-pdf-form-filler, public-office-pdf-watermark, pdf-ocr-extractor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, public-office-pdf-ocr, public-office-pdf-extraction, public-office-chat-with-pdf |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, document-rewriter, document-normaliser, docs-ops-rewrite-editor |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 2 | 2 | `public-office-xlsx-manipulation` | wrong | public-office-xlsx-manipulation, spreadsheet-formula-auditor, public-xlsx, public-office-excel-automation, public-office-financial-modeling |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-office-ppt-visual, public-pptx, public-office-html-to-ppt, speaker-notes-writer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `docx-redline-editor` | wrong | docx-redline-editor, office-to-markdown-converter, public-docx, public-office-docx-manipulation, document-normaliser |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, task-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, task-extractor, meeting-followup-extractor, meeting-ops-summary-writer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `meeting-summary-writer` | wrong | meeting-summary-writer, task-extractor, meeting-followup-extractor, meeting-agenda-builder, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, multi-source-comparison-builder, method-note-builder, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, document-extractor, source-grounding-extractor, paper-summariser, method-note-builder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, paper-summariser, related-work-synthesiser, general-source-summariser, citation-grounding-helper |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `document-field-extractor` | wrong | document-field-extractor, document-extractor, web-data-extractor, environmental-ops-field-extractor, publishing-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 2 | 2 | `fundraising-ops-summary-writer` | wrong | fundraising-ops-summary-writer, method-note-builder, procurement-ops-summary-writer, construction-ops-summary-writer, manufacturing-ops-summary-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | - | - | `research-ops-risk-reviewer` | wrong | research-ops-risk-reviewer, incident-ops-rewrite-editor, research-ops-summary-writer, incident-ops-summary-writer, research-ops-failure-diagnoser |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, related-work-synthesiser, general-source-summariser, citation-note-extractor, paper-summariser |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, multi-source-comparison-builder, general-source-summariser, method-note-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, email-drafter, email-polisher, reply-drafter, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, email-ops-rewrite-editor, partnerships-ops-rewrite-editor, email-polisher, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, weekly-planner, meeting-followup-extractor, meeting-summary-writer, task-extractor |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, groupwork-reply, professor-email-reply, email-action-extractor, reply-drafter |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, email-polisher, email-drafter |
| `sec_p1_threat_model` | `security-threat-modeler` | 7 | 7 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-code-reviewer, secret-leak-scanner, auth-flow-reviewer, public-openai-security-ownership-map |
| `sec_p2_security_code_review` | `security-code-reviewer` | 5 | 5 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, frontend-debugger, openapi-contract-reviewer, web-ui-tester, security-code-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-artifact-packager, secret-leak-scanner, risk-ops-dependency-mapper, supply-chain-ops-artifact-packager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, public-office-suspicious-email, public-office-security-monitoring, public-office-webhook-automation, deployment-build-triager |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, identity-ops-failure-diagnoser, identity-ops-handoff-brief-writer, identity-ops-summary-writer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 1 | 1 | `privacy-risk-reviewer` | gold | privacy-risk-reviewer, data-analysis-overview, data-analysis-for-reporting, privacy-ops-monitoring-plan-builder, secret-leak-scanner |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-summary-writer` | wrong | meeting-summary-writer, meeting-followup-extractor, task-extractor, meeting-ops-rewrite-editor, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-office-data-analysis` | wrong | public-office-data-analysis, public-office-excel-automation, public-office-xlsx-manipulation, data-analysis-overview, spreadsheet-formula-auditor |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, task-extractor, thesis-ops-timeline-builder, thesis-ops-handoff-brief-writer, thesis-ops-normalizer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `writing-ops-field-extractor` | wrong | writing-ops-field-extractor, docs-ops-field-extractor, real-estate-ops-field-extractor, content-ops-field-extractor, document-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 7 | 7 | `reply-polisher` | wrong | reply-polisher, reply-drafter, email-polisher, professor-email-reply, followup-reply-writer |
| `skill_p6_package_existing` | `skill-packager` | 17 | 17 | `public-office-content-writer` | wrong | public-office-content-writer, public-office-pdf-merge-split, public-office-file-organizer, public-office-chat-with-pdf, public-office-proposal-writer |

### `m3_tfidf_schema` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, external-api-integration-planner, webhook-contract-planner, api-design-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-ops-acceptance-test-builder, openapi-contract-reviewer, webhook-contract-planner, public-openai-figma-code-connect-components |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, invoice-payment-checker, duplicate-file-finder, public-openai-winui-app, events-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-openai-security-ownership-map, groupwork-reply, refactor-planner |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-rollback-planner, migration-risk-auditor, deployment-release-verifier, license-compatibility-checker |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 4 | 4 | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, analytics-ops-quality-auditor, analytics-ops-timeline-builder, service-dependency-mapper, analytics-ops-evidence-grounder |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-data-extractor, pdf-layout-reviewer, pdf-ocr-extractor, public-openai-screenshot |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, variance-analysis-helper, mobile-ops-field-extractor, web-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, variance-analysis-helper, web-data-extractor, web-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, product-ops-resource-linker, ecommerce-ops-field-extractor, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, web-ui-tester, security-code-reviewer, api-ops-failure-diagnoser |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, release-note-writer, public-openai-figma-generate-design, public-office-applicant-screening |
| `code_p1_local_code_review` | `code-reviewer` | 2 | 2 | `git-commit-writer` | wrong | git-commit-writer, code-reviewer, changelog-writer, test-case-generator, email-ops-risk-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, database-migration-risk-assessor, code-reviewer, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, code-reviewer, ci-failure-debugger, pr-description-writer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, git-commit-writer, auth-flow-reviewer, frontend-debugger, public-openai-gh-fix-ci |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-office-changelog-generator, pr-reviewer, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, deployment-release-verifier, capacity-risk-forecaster, public-office-changelog-generator |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-root-cause-diagnosis, data-analysis-for-reporting, metrics-overview |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, real-estate-ops-failure-diagnoser, deployment-build-triager, debugging-root-cause-helper |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, public-anthropic-web-artifacts-builder, lab-ops-quality-auditor, data-analysis-for-ranking-selection, lab-ops-normalizer |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-with-validation, public-office-data-analysis |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, release-note-writer, dashboard-ops-handoff-brief-writer, dashboard-ops-resource-linker |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, frontend-debugger, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, data-analysis-overview, data-analysis-for-forecasting, dataset-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, web-ui-tester, accessibility-interaction-auditor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector, accessibility-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, playwright-flow-debugger, data-analysis-with-anomaly-focus, ads-ops-timeline-builder |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, frontend-debugger, debugging-root-cause-helper, devops-ops-timeline-builder |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, deployment-rollback-planner, public-openai-vercel-deploy, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-acceptance-test-builder, mobile-ops-resource-linker, mobile-ops-summary-writer, mobile-ops-normalizer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, citation-note-extractor, data-analysis-overview, metrics-overview, paper-summariser |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, email-polisher, document-normaliser, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, docx-redline-editor, deck-template-applier, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, finance-ops-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, pdf-layout-reviewer, document-converter, slide-deck-visual-auditor, layout-preserving-converter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, office-to-markdown-converter, pdf-layout-reviewer, public-office-layout-analyzer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, cloud-monitoring-configurer, slo-breach-checker, data-analysis-overview, latency-anomaly-detector |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, data-analysis-overview, web-performance-budget-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, metrics-overview, risk-ops-risk-reviewer, journalism-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, metrics-root-cause-diagnoser, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, slo-breach-checker, incident-ops-resource-linker, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-theme-extractor, public-office-news-monitor, general-source-summariser, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `news-summariser` | wrong | news-summariser, news-briefing-writer, support-ops-ops-timeline-builder, knowledge-base-article-writer, support-ops-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, product-ops-resource-linker, product-ops-scenario-planner, content-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-office-news-monitor, news-summariser, market-opportunity-assessor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, public-office-news-monitor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-ocr-extractor, web-page-snapshotter, web-data-extractor, public-office-pdf-watermark |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, web-page-snapshotter, pdf-layout-reviewer, public-office-pdf-ocr |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, document-normaliser, review-comment-resolver, public-office-docx-manipulation |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-office-xlsx-manipulation, public-xlsx, agent-ops-summary-writer, engineering-design-ops-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, speaker-notes-writer, public-office-ppt-visual |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, docx-redline-editor, public-docx, layout-preserving-converter, pdf-layout-reviewer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, weekly-planner, meeting-followup-extractor, task-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, public-office-meeting-notes, meeting-ops-resource-linker |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, public-office-meeting-notes, meeting-summary-writer, meeting-ops-resource-linker |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, task-extractor, meeting-summary-writer, meeting-scheduler |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, general-source-summariser, citation-note-extractor, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, data-analysis-for-reporting, professor-email-reply, academic-admin-ops-failure-diagnoser |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, document-extractor, writing-ops-resource-linker, writing-ops-priority-ranker, paper-summariser |
| `read_p4_document_extraction` | `document-extractor` | - | - | `ml-ops-field-extractor` | wrong | ml-ops-field-extractor, bioinformatics-ops-field-extractor, recruiting-ops-field-extractor, analytics-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner, qa-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, document-extractor, citation-note-extractor, support-ops-evidence-grounder, support-ops-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `paper-summariser` | wrong | paper-summariser, method-note-builder, related-work-synthesiser, citation-note-extractor, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, general-source-summariser, paper-summariser, research-ops-comparison-builder, multi-source-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, email-polisher, professor-email-reply |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 3 | 3 | `document-summariser` | wrong | document-summariser, public-office-investment-memo, followup-reply-writer, general-source-summariser, reply-drafter |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, docker-compose-configurator |
| `sec_p1_threat_model` | `security-threat-modeler` | 4 | 4 | `security-code-reviewer` | wrong | security-code-reviewer, privacy-risk-reviewer, auth-flow-reviewer, security-threat-modeler, public-openai-figma-create-new-file |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, security-threat-modeler, code-reviewer, pr-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-risk-reviewer, supply-chain-ops-resource-linker |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, deployment-release-verifier, public-anthropic-internal-comms, database-ops-resource-linker |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-polisher, email-drafter, email-ops-monitoring-plan-builder, version-control-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, email-polisher, product-ops-resource-linker, search-ops-resource-linker, email-drafter |
| `skill_p1_find_existing` | `skill-finder` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-editor, meeting-agenda-builder, public-office-meeting-notes, meeting-followup-extractor |
| `skill_p2_install_existing` | `skill-installer` | 2 | 2 | `skill-packager` | wrong | skill-packager, skill-installer, library-ops-artifact-packager, library-ops-rewrite-editor, library-ops-failure-diagnoser |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, public-openai-figma-create-new-file, skill-finder, meeting-ops-summary-writer |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-finder, skill-creator, skill-evaluator |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 6 | 6 | `reply-drafter` | wrong | reply-drafter, professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-skill-creator, general-source-summariser, public-anthropic-skill-creator |

### `m6_bm25_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, external-api-integration-planner, api-design-reviewer, graphql-schema-designer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, openapi-contract-tester, database-backup-planner, api-ops-acceptance-test-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, engineering-design-ops-timeline-builder, invoice-payment-checker |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, refactor-planner, security-threat-modeler, version-control-helper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, deployment-release-verifier, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, privacy-policy-drafter, privacy-risk-reviewer, architecture-boundary-reviewer, data-analysis-for-reporting |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, pdf-ocr-extractor |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-office-pdf-form-filler, dashboard-ops-field-extractor, public-openai-playwright, document-summariser |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, dashboard-ops-acceptance-test-builder, web-page-snapshotter, docs-ops-acceptance-test-builder, ecommerce-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, product-ops-resource-linker, web-page-snapshotter, pdf-layout-reviewer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, debugging-root-cause-helper, openapi-contract-tester, pdf-layout-reviewer |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, slo-breach-checker, layout-preserving-converter, reply-drafter |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, release-note-writer, changelog-writer, git-commit-writer, review-comment-resolver |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, database-migration-risk-assessor, review-comment-resolver, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, code-reviewer, pr-description-writer, reply-drafter, public-openai-gh-address-comments |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, frontend-debugger, openapi-contract-reviewer, auth-flow-reviewer, git-commit-writer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, git-commit-writer, citation-note-extractor, pr-description-writer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-office-changelog-generator, pr-description-writer, slo-breach-checker, changelog-writer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, financial-report-writer, dashboard-ops-priority-ranker, dashboard-ops-handoff-brief-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, debugging-root-cause-helper, latency-anomaly-detector, frontend-debugger |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-with-anomaly-focus, compliance-ops-quality-auditor, energy-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, variance-analysis-helper, web-performance-budget-checker, public-office-data-analysis |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, public-office-data-analysis, financial-report-writer, public-office-stock-analysis, news-briefing-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, followup-reply-writer, capacity-risk-forecaster, frontend-debugger |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, dashboard-ops-comparison-builder, dashboard-ops-scenario-planner, risk-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, accessibility-interaction-auditor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, changelog-writer, review-comment-resolver, data-analysis-for-root-cause-diagnosis |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, frontend-debugger, web-ui-tester |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, frontend-debugger, public-netlify-deploy, ci-failure-debugger, debugging-root-cause-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, release-note-writer, deployment-build-triager |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, mobile-ops-acceptance-test-builder, budget-planner, mobile-ops-risk-reviewer |
| `doc_p1_document_summary` | `document-summariser` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, document-summariser, citation-note-extractor, news-summariser, data-analysis-with-validation |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, public-docx, document-normaliser, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-layout-reviewer, public-docx, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | 6 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, docs-ops-field-extractor, energy-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, decision-matrix-builder, public-docx, skill-installer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, deck-template-applier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, note-tagger |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, cloud-monitoring-configurer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 4 | 4 | `metrics-overview` | wrong | metrics-overview, risk-ops-acceptance-test-builder, risk-ops-compliance-checker, slo-breach-checker, architecture-boundary-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, data-analysis-for-forecasting, metrics-root-cause-diagnoser, risk-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, deployment-build-triager |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, public-openai-linear, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, metrics-overview, support-ops-ops-timeline-builder, data-analysis-for-reporting |
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
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-evidence-grounder, general-source-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, followup-reply-writer, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, weekly-planner, meeting-summary-writer, citation-note-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-scheduler` | wrong | meeting-scheduler, meeting-agenda-builder, meeting-ops-acceptance-test-builder, public-openai-notion-meeting-intelligence, test-case-generator |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, research-ops-summary-writer, method-note-builder, academic-admin-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, dashboard-ops-summary-writer, compliance-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-resource-linker, writing-ops-evidence-grounder, writing-ops-priority-ranker |
| `read_p4_document_extraction` | `document-extractor` | 19 | 19 | `web-data-extractor` | wrong | web-data-extractor, docs-ops-field-extractor, bioinformatics-ops-field-extractor, research-ops-field-extractor, privacy-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `pr-description-writer` | wrong | pr-description-writer, manufacturing-ops-scenario-planner, journalism-ops-scenario-planner, docs-ops-scenario-planner, fundraising-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-eval-coverage-auditor, support-ops-resource-linker, support-ops-ops-resource-linker, agent-ops-resource-linker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `news-briefing-writer` | wrong | news-briefing-writer, multi-source-comparison-builder, note-tagger, release-note-writer, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, public-openai-notion-research-documentation, multi-document-comparison-preparer, release-note-writer, note-tagger |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, groupwork-reply, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, proposal-drafter, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, email-action-extractor, procurement-ops-handoff-brief-writer, journalism-ops-handoff-brief-writer, docs-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-brainstorming, email-ops-scenario-planner, identity-ops-scenario-planner, security-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, accessibility-checker, api-ops-acceptance-test-builder |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, risk-ops-risk-reviewer, pr-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, data-analysis-with-anomaly-focus, database-migration-risk-assessor, webhook-setup-planner, kubernetes-deployment-helper |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, data-analysis-with-validation, changelog-writer, email-polisher, release-note-writer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, churn-risk-analyser, query-optimizer, email-polisher, public-office-web-search |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, followup-reply-writer, meeting-followup-extractor, incident-summary-writer, release-note-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, public-anthropic-webapp-testing, library-ops-artifact-packager, library-ops-acceptance-test-builder, code-reviewer |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, skill-finder, public-skill-creator, public-anthropic-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, docs-ops-field-extractor, agent-ops-field-extractor, public-anthropic-skill-creator, document-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, skill-finder, agent-eval-coverage-auditor, reply-polisher, reply-drafter |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, agent-ops-resource-linker, skill-finder, public-anthropic-skill-creator |

### `m6_tfidf_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, openapi-contract-tester, api-design-reviewer, graphql-schema-designer, contract-ops-normalizer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, api-ops-acceptance-test-builder, public-openai-figma-code-connect-components, api-ops-monitoring-plan-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, invoice-payment-checker, events-ops-timeline-builder, public-openai-winui-app, events-ops-scenario-planner |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, refactor-planner, security-threat-modeler, version-control-helper |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-rollback-planner, migration-risk-auditor, risk-ops-risk-reviewer, dependency-risk-auditor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `analytics-ops-quality-auditor` | wrong | analytics-ops-quality-auditor, analytics-ops-evidence-grounder, public-office-microsoft-teams, web-performance-budget-checker, public-office-data-pipeline |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, public-office-pdf-form-filler, public-openai-playwright, real-estate-ops-field-extractor, financial-report-writer |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, web-page-snapshotter, docs-ops-acceptance-test-builder, compliance-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-field-extractor` | wrong | product-ops-field-extractor, product-ops-resource-linker, product-ops-scenario-planner, product-ops-comparison-builder, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, api-ops-evidence-grounder, api-ops-timeline-builder, api-ops-field-extractor |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, layout-preserving-converter, web-form-filler, pdf-layout-reviewer |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, changelog-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, database-migration-risk-assessor, api-ops-acceptance-test-builder, license-compatibility-checker |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-reviewer, pr-description-writer, public-openai-gh-address-comments, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, frontend-debugger, git-commit-writer, public-openai-gh-fix-ci |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-office-changelog-generator, git-commit-writer, citation-note-extractor |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-office-changelog-generator, pr-description-writer, service-dependency-mapper, slo-breach-checker |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, financial-report-writer, data-analysis-for-ranking-selection, spreadsheet-formula-auditor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, debugging-root-cause-helper, latency-anomaly-detector, data-analysis-for-root-cause-diagnosis |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, compliance-ops-quality-auditor, docs-ops-quality-auditor, partnerships-ops-quality-auditor, procurement-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-office-data-analysis, web-performance-budget-checker, data-analysis-for-forecasting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, geospatial-ops-handoff-brief-writer, dashboard-ops-handoff-brief-writer, data-analysis-overview, public-office-data-analysis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, risk-ops-comparison-builder, dashboard-ops-comparison-builder, risk-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, accessibility-interaction-auditor, auth-flow-reviewer, web-performance-budget-checker |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, review-comment-resolver, code-reviewer, public-anthropic-canvas-design |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, frontend-debugger, web-page-snapshotter |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `public-netlify-deploy` | wrong | public-netlify-deploy, deployment-build-triager, frontend-debugger, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-note-writer, public-openai-vercel-deploy, deployment-rollback-planner |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, budget-planner, mobile-ops-acceptance-test-builder, mobile-ops-risk-reviewer, mobile-ops-evidence-grounder |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, citation-note-extractor, news-summariser, knowledge-base-article-writer |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, layout-preserving-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, deck-template-applier, pdf-layout-reviewer, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 3 | 3 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, document-field-extractor, compliance-ops-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, docs-ops-comparison-builder, compliance-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, document-converter, pdf-layout-reviewer, content-ops-evidence-grounder |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-converter, docs-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, cloud-monitoring-configurer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 6 | 6 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, service-dependency-mapper, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, risk-ops-risk-reviewer, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, latency-anomaly-detector |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 6 | `metrics-overview` | wrong | metrics-overview, incident-ops-normalizer, incident-ops-scenario-planner, incident-ops-timeline-builder, incident-ops-risk-reviewer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, general-source-summariser, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, support-ops-ops-timeline-builder, support-ops-timeline-builder, metrics-overview |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, knowledge-base-article-writer, product-ops-evidence-grounder, product-ops-scenario-planner, document-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, public-office-news-monitor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, public-office-news-monitor |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-office-chat-with-pdf, public-pdf, public-office-pdf-extraction |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, pdf-layout-reviewer, public-office-pdf-converter, public-office-pdf-ocr |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, review-comment-resolver, public-office-docx-manipulation, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-office-contract-review, web-ui-tester, rag-failure-diagnoser, public-office-xlsx-manipulation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, research-ops-rewrite-editor, customer-feedback-analyser, vendor-ops-rewrite-editor, public-pptx |
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
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, agent-ops-evidence-grounder, citation-note-extractor, agent-eval-coverage-auditor, agent-ops-resource-linker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, release-note-writer, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, release-note-writer, multi-source-comparison-builder, note-linker |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, email-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, email-polisher, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, email-action-extractor, public-office-investment-memo, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, public-openai-figma-create-new-file, professor-email-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-openai-figma-create-new-file, email-ops-scenario-planner, email-ops-risk-reviewer, security-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, api-ops-acceptance-test-builder, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-artifact-packager, supply-chain-ops-priority-ranker |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, deployment-release-verifier, webhook-contract-planner, database-ops-normalizer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-ops-monitoring-plan-builder, email-ops-acceptance-test-builder, version-control-helper, email-ops-resource-linker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, product-ops-resource-linker, query-optimizer, product-ops-failure-diagnoser, product-ops-acceptance-test-builder |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-ops-evidence-grounder, meeting-ops-comparison-builder, public-office-meeting-notes, library-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, library-ops-acceptance-test-builder, public-xlsx, code-reviewer, library-ops-resource-linker |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, skill-finder, meeting-followup-extractor, public-anthropic-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, agent-ops-field-extractor, docs-ops-field-extractor, public-anthropic-skill-creator, skill-finder |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-anthropic-skill-creator, skill-editor, agent-ops-resource-linker |

### `m6_minilm_full_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, external-api-integration-planner, webhook-contract-planner, openapi-contract-tester, database-migration-risk-assessor |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, auth-flow-reviewer, api-integration-planner, api-ops-acceptance-test-builder |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, invoice-payment-checker, latency-anomaly-detector, events-ops-acceptance-test-builder, procurement-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, service-dependency-mapper, dependency-risk-auditor, security-threat-modeler |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, migration-risk-auditor, deployment-rollback-planner, dependency-risk-auditor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `latency-anomaly-detector` | wrong | latency-anomaly-detector, slo-breach-checker, dashboard-ops-failure-diagnoser, metrics-root-cause-diagnoser, metrics-overview |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, visual-regression-checker, accessibility-interaction-auditor, web-ui-tester, playwright-flow-debugger |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, playwright-flow-debugger, finance-ops-acceptance-test-builder, web-page-snapshotter |
| `web_p3_ui_test` | `web-ui-tester` | - | - | `procurement-ops-acceptance-test-builder` | wrong | procurement-ops-acceptance-test-builder, facilities-ops-acceptance-test-builder, property-ops-acceptance-test-builder, email-ops-acceptance-test-builder, social-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, ecommerce-ops-field-extractor, product-ops-field-extractor, retail-ops-field-extractor, warehouse-ops-field-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, public-api-design-principles, playwright-flow-debugger, public-playwright-interactive, public-openai-gh-fix-ci |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, web-form-filler, web-ui-tester, frontend-debugger |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, email-ops-acceptance-test-builder, email-polisher, professor-email-reply, auth-flow-reviewer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, auth-flow-reviewer, api-ops-acceptance-test-builder, external-api-integration-planner, code-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, code-reviewer, pr-reviewer, ci-failure-debugger, auth-flow-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, repo-ops-failure-diagnoser, customer-success-ops-acceptance-test-builder, api-ops-failure-diagnoser |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, deployment-release-verifier, git-commit-writer, review-comment-resolver |
| `code_p6_release_notes` | `release-note-writer` | - | - | `deployment-release-verifier` | wrong | deployment-release-verifier, auth-flow-reviewer, mobile-ops-risk-reviewer, mobile-ops-timeline-builder, mobile-ops-evidence-grounder |
| `data_p1_overview` | `data-analysis-overview` | 2 | 2 | `data-analysis-for-forecasting` | wrong | data-analysis-for-forecasting, data-analysis-overview, data-analysis-for-reporting, news-briefing-writer, data-analysis-for-ranking-selection |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, data-analysis-for-forecasting |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, dataset-ops-quality-auditor, data-analysis-with-anomaly-focus, finance-ops-quality-auditor, incident-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, dataset-ops-failure-diagnoser, support-ops-failure-diagnoser, marketing-ops-failure-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, news-summariser, data-analysis-overview, marketing-ops-summary-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-with-anomaly-focus |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, risk-ops-priority-ranker, travel-ops-priority-ranker, supply-chain-ops-priority-ranker, finance-ops-priority-ranker |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, auth-flow-reviewer, web-form-filler, public-office-stripe-payments |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-layout-reviewer, web-performance-budget-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, frontend-debugger, web-form-filler, web-ui-tester |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, public-netlify-deploy, devops-ops-timeline-builder, devops-ops-quality-auditor, public-openai-vercel-deploy |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, deployment-build-triager, public-openai-vercel-deploy, devops-ops-evidence-grounder |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-summary-writer, mobile-ops-quality-auditor, mobile-ops-risk-reviewer, mobile-ops-monitoring-plan-builder |
| `doc_p1_document_summary` | `document-summariser` | - | - | `travel-ops-summary-writer` | wrong | travel-ops-summary-writer, legal-ops-summary-writer, travel-ops-compliance-checker, travel-ops-quality-auditor, travel-ops-scenario-planner |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, document-converter, document-normaliser, travel-ops-rewrite-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, document-rewriter, travel-ops-rewrite-editor, document-converter |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, supply-chain-ops-field-extractor, receipt-extractor, finance-ops-field-extractor, procurement-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, legal-ops-comparison-builder, writing-ops-comparison-builder, docs-ops-comparison-builder, multi-source-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, document-converter, medical-admin-ops-field-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, slo-breach-checker, architecture-boundary-reviewer, web-page-snapshotter |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, data-analysis-with-anomaly-focus, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, sre-ops-risk-reviewer, deployment-release-verifier, incident-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, data-analysis-for-forecasting, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `service-dependency-mapper` | wrong | service-dependency-mapper, metrics-root-cause-diagnoser, latency-anomaly-detector, metrics-overview, web-performance-budget-checker |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, metrics-overview, incident-ops-timeline-builder, incident-ops-field-extractor, slo-breach-checker |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-briefing-writer, news-theme-extractor, tech-news-trend-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, events-ops-summary-writer, news-summariser, meeting-summary-writer, events-ops-timeline-builder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, general-source-summariser, ecommerce-ops-evidence-grounder, partnerships-ops-evidence-grounder, public-office-crypto-report |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, news-briefing-writer, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, journalism-ops-evidence-grounder |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, public-pdf, public-openai-pdf, docs-ops-field-extractor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-layout-reviewer, public-office-pdf-ocr, public-office-pdf-extraction, public-office-pdf-watermark |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, multi-document-comparison-preparer, document-rewriter, document-normaliser |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-office-xlsx-manipulation, public-xlsx, data-analysis-with-validation, public-office-excel-automation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, public-office-ppt-visual, public-pptx, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, docx-redline-editor, layout-preserving-converter, public-docx, document-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, meeting-scheduler, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-ops-field-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-ops-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-agenda-builder, meeting-ops-field-extractor, meeting-summary-writer, meeting-ops-evidence-grounder |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, meeting-scheduler, meeting-summary-writer, meeting-ops-summary-writer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, method-note-builder, research-ops-summary-writer, citation-note-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, research-ops-summary-writer, data-analysis-for-reporting, risk-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, general-source-summariser, method-note-builder, paper-summariser |
| `read_p4_document_extraction` | `document-extractor` | 20 | 20 | `web-data-extractor` | wrong | web-data-extractor, docs-ops-field-extractor, publishing-ops-field-extractor, crm-ops-field-extractor, environmental-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, fundraising-ops-summary-writer, paper-summariser, manufacturing-ops-summary-writer, procurement-ops-summary-writer |
| `read_p6_grounding_check` | `citation-grounding-helper` | - | - | `support-ops-ops-rewrite-editor` | wrong | support-ops-ops-rewrite-editor, research-ops-evidence-grounder, journalism-ops-evidence-grounder, writing-ops-evidence-grounder, content-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 1 | 1 | `multi-source-comparison-builder` | gold | multi-source-comparison-builder, related-work-synthesiser, citation-note-extractor, research-ops-comparison-builder, method-note-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, thesis-ops-comparison-builder, multi-source-comparison-builder, multi-document-comparison-preparer |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, email-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, email-polisher, email-ops-rewrite-editor, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, professor-email-reply, meeting-followup-extractor, weekly-planner |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, groupwork-reply, reply-drafter, meeting-followup-extractor, professor-email-reply |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, dependency-risk-auditor, public-openai-security-ownership-map, auth-flow-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, auth-flow-reviewer, frontend-debugger, openapi-contract-reviewer, api-ops-compliance-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, risk-ops-dependency-mapper, risk-ops-artifact-packager, architecture-boundary-reviewer, supply-chain-ops-dependency-mapper |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, deployment-build-triager, public-office-webhook-automation, public-office-suspicious-email |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, identity-ops-summary-writer, identity-ops-resource-linker, identity-ops-evidence-grounder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 2 | 2 | `data-analysis-overview` | wrong | data-analysis-overview, privacy-risk-reviewer, data-analysis-for-ranking-selection, data-analysis-with-anomaly-focus, data-analysis-for-forecasting |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-followup-extractor` | wrong | meeting-followup-extractor, meeting-agenda-builder, meeting-ops-rewrite-editor, meeting-summary-writer, meeting-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | - | - | `public-office-data-analysis` | wrong | public-office-data-analysis, public-xlsx, data-analysis-for-reporting, public-office-sheets-automation, public-office-excel-automation |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, skill-editor, task-extractor, thesis-ops-timeline-builder, thesis-ops-handoff-brief-writer |
| `skill_p4_edit_existing` | `skill-editor` | - | - | `docs-ops-field-extractor` | wrong | docs-ops-field-extractor, writing-ops-field-extractor, agent-ops-field-extractor, content-ops-field-extractor, real-estate-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, professor-email-reply, email-polisher |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, public-office-content-writer, public-office-pdf-merge-split, public-office-file-organizer, public-office-chat-with-pdf |
