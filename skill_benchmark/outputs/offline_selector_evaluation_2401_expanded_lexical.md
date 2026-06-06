# Offline Selector Evaluation Report

This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.

## Scale Regimes

- `core`: 127 skills, approx selector-visible tokens per method vary by representation.
- `current_full`: 2401 skills, approx selector-visible tokens per method vary by representation.

## Method Summary

| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | `core` | 127 | 6915 | 76.4% | 76.4% | 90.5% | 90.5% | 95.3% | 95.3% | 0.842 | 0.842 | 1.58 | 4.7% | 0.0% | 227.52 |
| `m1_tfidf_flat` | `core` | 127 | 6915 | 77.2% | 77.2% | 92.1% | 92.1% | 95.3% | 95.3% | 0.851 | 0.851 | 1.74 | 5.5% | 0.0% | 1153.4 |
| `m3_tfidf_schema` | `core` | 127 | 44895 | 85.0% | 85.0% | 96.9% | 96.9% | 100.0% | 100.0% | 0.913 | 0.913 | 1.25 | 4.7% | 0.0% | 83.21 |
| `m6_bm25_schema_rerank` | `core` | 127 | 14338 | 79.5% | 79.5% | 95.3% | 95.3% | 96.9% | 96.9% | 0.874 | 0.874 | 1.28 | 2.4% | 0.0% | 518.99 |
| `m6_tfidf_schema_rerank` | `core` | 127 | 14338 | 81.9% | 81.9% | 96.9% | 96.9% | 96.9% | 96.9% | 0.893 | 0.893 | 1.33 | 3.9% | 0.0% | 347.88 |
| `m1_bm25_flat` | `current_full` | 2401 | 122537 | 68.5% | 68.5% | 83.5% | 83.5% | 87.4% | 87.4% | 0.770 | 0.770 | 2.09 | 3.1% | 16.5% | 3849.37 |
| `m1_tfidf_flat` | `current_full` | 2401 | 122537 | 61.4% | 61.4% | 78.0% | 78.7% | 84.2% | 85.0% | 0.717 | 0.720 | 2.21 | 5.5% | 22.8% | 225.04 |
| `m3_tfidf_schema` | `current_full` | 2401 | 629119 | 76.4% | 76.4% | 92.9% | 92.9% | 94.5% | 94.5% | 0.854 | 0.854 | 1.41 | 5.5% | 8.7% | 757.52 |
| `m6_bm25_schema_rerank` | `current_full` | 2401 | 128533 | 76.4% | 76.4% | 89.8% | 89.8% | 92.9% | 92.9% | 0.840 | 0.840 | 1.49 | 1.6% | 4.7% | 4062.87 |
| `m6_tfidf_schema_rerank` | `current_full` | 2401 | 128533 | 78.0% | 78.0% | 89.0% | 89.0% | 90.5% | 91.3% | 0.837 | 0.838 | 1.3 | 3.1% | 7.9% | 526.37 |

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
| `m1_bm25_flat` | 76.4% | 68.5% | 68.5% | -7.9% | 95.3% | 87.4% | 87.4% | -7.9% | 0.842 | 0.770 | 0.770 | 16.5% |
| `m1_tfidf_flat` | 77.2% | 61.4% | 61.4% | -15.8% | 95.3% | 84.2% | 85.0% | -11.0% | 0.851 | 0.717 | 0.720 | 22.8% |
| `m3_tfidf_schema` | 85.0% | 76.4% | 76.4% | -8.7% | 100.0% | 94.5% | 94.5% | -5.5% | 0.913 | 0.854 | 0.854 | 8.7% |
| `m6_bm25_schema_rerank` | 79.5% | 76.4% | 76.4% | -3.1% | 96.9% | 92.9% | 92.9% | -3.9% | 0.874 | 0.840 | 0.840 | 4.7% |
| `m6_tfidf_schema_rerank` | 81.9% | 78.0% | 78.0% | -3.9% | 96.9% | 90.5% | 91.3% | -6.3% | 0.893 | 0.837 | 0.838 | 7.9% |

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
| `api_backend_design` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 71.4% | 71.4% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 60.0% | 60.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `service-dependency-mapper -> distributed-trace-investigator`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-with-validation -> accessibility-checker`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> metrics-root-cause-diagnoser`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> reply-polisher`: 1

### `m1_tfidf_flat` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 40.0% | 40.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 75.0% | 75.0% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `external-api-integration-planner -> rest-api-contract-designer`: 1
- `service-dependency-mapper -> distributed-trace-investigator`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `web-data-extractor -> web-page-snapshotter`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-with-validation -> github-issue-triager`: 1
- `deployment-build-triager -> ci-log-root-cause-debugger`: 1
- `document-rewriter -> reply-polisher`: 1

### `m3_tfidf_schema` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `api_mcp_tooling` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 87.5% | 87.5% | 100.0% | 100.0% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 100.0% | 100.0% |
| `skill_lifecycle` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |

Top confusions:
- `webhook-contract-planner -> webhook-integration-planner`: 1
- `service-dependency-mapper -> distributed-trace-investigator`: 1
- `webhook-integration-planner -> webhook-contract-planner`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `document-converter -> office-to-markdown-converter`: 1
- `repo-code-reviewer -> code-reviewer`: 1
- `incident-summary-writer -> metrics-overview`: 1

### `m6_bm25_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 50.0% | 50.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `web-form-filler -> pdf-form-filler`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> ci-log-root-cause-debugger`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-field-extractor -> web-data-extractor`: 1

### `m6_tfidf_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 57.1% | 57.1% | 100.0% | 100.0% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 62.5% | 62.5% | 87.5% | 87.5% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `service-dependency-mapper -> distributed-trace-investigator`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-with-validation -> github-issue-triager`: 1
- `deployment-build-triager -> ci-log-root-cause-debugger`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1
- `document-converter -> office-to-markdown-converter`: 1

### `m1_bm25_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `api_mcp_tooling` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 42.9% | 42.9% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 16.7% | 16.7% | 66.7% | 66.7% | 66.7% | 66.7% |
| `huggingface_ml_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `observability_reliability` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `office_artifact_workflows` | 6 | 50.0% | 50.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 40.0% | 40.0% | 40.0% | 40.0% |
| `reading_research` | 8 | 37.5% | 37.5% | 50.0% | 50.0% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `mcp-server-builder -> public-addy-agent-api-and-interface-design`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `pr-reviewer -> pr-description-writer`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `data-analysis-for-reporting -> public-office-data-analysis`: 1
- `deployment-build-triager -> implicit-ci-failure-reader`: 1
- `document-summariser -> general-source-summariser`: 1

### `m1_tfidf_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 50.0% | 50.0% | 66.7% | 83.3% | 66.7% | 83.3% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 57.1% | 57.1% | 85.7% | 85.7% |
| `github_ci_maintenance` | 6 | 16.7% | 16.7% | 66.7% | 66.7% | 83.3% | 83.3% |
| `huggingface_ml_workflows` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 20.0% | 20.0% | 60.0% | 60.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `skill_lifecycle` | 6 | 50.0% | 50.0% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `external-api-integration-planner -> rest-api-contract-designer`: 1
- `webhook-contract-planner -> invoice-payment-checker`: 1
- `service-dependency-mapper -> public-office-microsoft-teams`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `web-ui-tester -> variance-analysis-helper`: 1
- `web-data-extractor -> product-ops-resource-linker`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-with-validation -> public-addy-web-web-quality-audit`: 1

### `m3_tfidf_schema` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `api_mcp_tooling` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `documents_files` | 7 | 71.4% | 71.4% | 85.7% | 85.7% | 85.7% | 85.7% |
| `github_ci_maintenance` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 60.0% | 60.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `reading_research` | 8 | 75.0% | 75.0% | 75.0% | 75.0% | 87.5% | 87.5% |
| `reply_messaging` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 66.7% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `webhook-contract-planner -> webhook-integration-planner`: 1
- `service-dependency-mapper -> public-office-microsoft-teams`: 1
- `webhook-integration-planner -> webhook-contract-planner`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `code-reviewer -> git-commit-writer`: 1
- `ci-failure-debugger -> ci-log-root-cause-debugger`: 1
- `deployment-build-triager -> public-netlify-deploy`: 1
- `document-field-extractor -> invoice-payment-checker`: 1

### `m6_bm25_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `documents_files` | 7 | 28.6% | 28.6% | 85.7% | 85.7% | 85.7% | 85.7% |
| `github_ci_maintenance` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 83.3% | 83.3% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `news_monitoring` | 5 | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 80.0% | 80.0% | 80.0% | 80.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 50.0% | 50.0% | 62.5% | 62.5% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `web-form-filler -> pdf-form-filler`: 1
- `accessibility-checker -> accessibility-interaction-auditor`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-for-root-cause-diagnosis -> metrics-root-cause-diagnoser`: 1
- `deployment-build-triager -> ci-log-root-cause-debugger`: 1
- `document-summariser -> general-source-summariser`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1

### `m6_tfidf_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `api_backend_design` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `api_mcp_tooling` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `browser_web_automation` | 6 | 66.7% | 66.7% | 83.3% | 83.3% | 83.3% | 83.3% |
| `code_github_workflow` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `data_spreadsheet` | 7 | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `deployment_browser_qa` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 100.0% | 100.0% |
| `documents_files` | 7 | 42.9% | 42.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| `github_ci_maintenance` | 6 | 83.3% | 83.3% | 100.0% | 100.0% | 100.0% | 100.0% |
| `huggingface_ml_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `metrics_observability` | 6 | 50.0% | 50.0% | 66.7% | 66.7% | 66.7% | 83.3% |
| `news_monitoring` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `observability_reliability` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_artifact_workflows` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `office_business_automation` | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `pdf_document_operations` | 6 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| `planning_meetings` | 5 | 20.0% | 20.0% | 60.0% | 60.0% | 60.0% | 60.0% |
| `reading_research` | 8 | 50.0% | 50.0% | 62.5% | 62.5% | 75.0% | 75.0% |
| `reply_messaging` | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `security_appsec` | 6 | 66.7% | 66.7% | 66.7% | 66.7% | 66.7% | 66.7% |
| `skill_lifecycle` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |
| `skill_representation_analysis` | 6 | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% | 83.3% |

Top confusions:
- `service-dependency-mapper -> analytics-ops-quality-auditor`: 1
- `web-form-filler -> pdf-form-filler`: 1
- `web-data-extractor -> product-ops-field-extractor`: 1
- `review-comment-resolver -> pr-review-comment-resolver`: 1
- `data-analysis-for-ranking-selection -> decision-matrix-builder`: 1
- `deployment-build-triager -> ci-log-root-cause-debugger`: 1
- `document-rewriter -> reply-polisher`: 1
- `document-normaliser -> layout-preserving-converter`: 1

## Prompt-Level Results

### `m1_bm25_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, mcp-server-builder, gradio-demo-builder |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, rest-api-contract-designer, pr-review-comment-resolver, api-security-threat-reviewer, auth-flow-integrator |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, auth-flow-integrator, skill-router-policy-designer, rest-api-contract-designer |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, security-threat-modeler, dependency-risk-auditor, github-issue-triager, data-analysis-with-validation |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, webhook-integration-planner, dependency-risk-auditor, grafana-dashboard-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, service-dependency-mapper, data-analysis-for-reporting, architecture-boundary-reviewer, skill-evaluator |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, pr-review-comment-resolver, skill-editor |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, skill-installer-wrapper, api-security-threat-reviewer, skill-creator |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, auth-flow-integrator, external-api-integration-planner, database-migration-risk-assessor |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, incident-summary-writer, secret-leak-scanner, grafana-dashboard-builder |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, openapi-contract-reviewer, skill-field-auditor, slo-breach-narrative-writer, rest-api-contract-designer |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, security-threat-modeler, auth-flow-reviewer, privacy-risk-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, metrics-overview, pdf-layout-reviewer, web-form-filler, deployment-release-verifier |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, web-form-filler, web-ui-tester, notion-research-database-builder, multi-document-comparison-preparer |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, skill-evaluator, pdf-form-filler, web-page-snapshotter, pdf-layout-table-extractor |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, release-note-writer, pdf-layout-table-extractor, web-page-snapshotter, pdf-layout-reviewer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, rest-api-contract-designer, pdf-layout-reviewer, metrics-root-cause-diagnoser |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, reply-drafter, skill-benchmark-evaluator, slo-breach-checker |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, repo-code-reviewer, release-note-writer, dependency-risk-auditor, reply-drafter |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-review-comment-resolver, openapi-contract-reviewer, database-migration-risk-assessor, review-comment-resolver |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, code-reviewer, rest-api-contract-designer, repo-code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, frontend-debugger, openapi-contract-reviewer, code-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, citation-note-extractor, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, slo-breach-checker, release-changelog-generator, news-theme-extractor, data-analysis-for-reporting |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, pdf-question-answerer, data-analysis-for-forecasting, citation-note-extractor, pr-review-comment-resolver |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, latency-anomaly-detector, general-source-summariser, release-note-writer |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `accessibility-checker` | wrong | accessibility-checker, data-analysis-with-validation, slo-breach-checker, pdf-form-filler, data-analysis-with-anomaly-focus |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 3 | 3 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-for-root-cause-diagnosis, data-analysis-with-validation, frontend-debugger |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, citation-note-extractor, multi-document-comparison-preparer, spreadsheet-formula-auditor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, followup-reply-writer, metrics-root-cause-diagnoser, incident-summary-writer, meeting-followup-extractor |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, meeting-notes-action-extractor, pdf-layout-reviewer, release-note-writer, pdf-to-docx-converter |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-performance-budget-checker, web-ui-tester |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, data-analysis-for-ranking-selection, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, web-form-filler, web-ui-tester |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, ci-failure-debugger, frontend-debugger, ci-log-root-cause-debugger, xlsx-formula-model-builder |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, deployment-build-triager, release-changelog-generator, release-note-writer, web-performance-budget-checker |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, calendar-scheduling-optimizer, general-source-summariser, deployment-build-triager |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `general-source-summariser` | wrong | general-source-summariser, citation-note-extractor, data-analysis-with-validation, document-summariser, skill-finder |
| `doc_p2_document_rewriter` | `document-rewriter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, pdf-to-docx-converter, document-rewriter, docx-redline-editor, document-normaliser |
| `doc_p3_document_normaliser` | `document-normaliser` | 4 | 4 | `pdf-to-docx-converter` | wrong | pdf-to-docx-converter, layout-preserving-converter, docx-redline-editor, document-normaliser, document-rewriter |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-field-extractor, meeting-notes-action-extractor, meeting-followup-extractor, document-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, visual-regression-checker, pdf-to-docx-converter, pdf-question-answerer |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, office-to-markdown-converter, pdf-layout-reviewer, layout-preserving-converter, document-normaliser |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `document-converter` | wrong | document-converter, layout-preserving-converter, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-to-docx-converter |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 8 | 8 | `frontend-debugger` | wrong | frontend-debugger, metrics-root-cause-diagnoser, ci-failure-debugger, hf-dataset-viewer-inspector, secret-leak-scanner |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, resilience-pattern-reviewer, pdf-redaction-reviewer, openapi-contract-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 1 | 1 | `repo-code-reviewer` | gold | repo-code-reviewer, code-reviewer, security-code-reviewer, pr-reviewer, pr-review-comment-resolver |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, accessibility-checker, slo-breach-checker, citation-note-extractor, data-analysis-with-anomaly-focus |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 5 | 5 | `review-comment-resolver` | wrong | review-comment-resolver, release-note-writer, pr-review-comment-resolver, code-reviewer, release-changelog-generator |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, pr-review-comment-resolver, webhook-contract-planner, calendar-scheduling-optimizer, auth-flow-reviewer |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, gradio-demo-builder, pdf-layout-table-extractor, openapi-contract-reviewer, web-ui-tester |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, hf-dataset-viewer-inspector, hf-community-eval-runner, data-analysis-for-ranking-selection, gradio-demo-builder |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-benchmark-evaluator, skill-authoring-guide, service-mesh-traffic-debugger, skill-hierarchy-flattener |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, sentence-transformer-finetuner, xlsx-formula-model-builder, task-extractor, hf-community-eval-runner |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, gradio-demo-builder, hf-dataset-viewer-inspector, hf-community-eval-runner, hf-local-model-selector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, gradio-demo-builder, multi-source-comparison-builder, web-data-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, related-work-synthesiser, architecture-boundary-reviewer, resilience-pattern-reviewer, latency-anomaly-detector |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, slo-breach-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 3 | 3 | `metrics-overview` | wrong | metrics-overview, architecture-boundary-reviewer, slo-breach-checker, web-performance-budget-checker, pr-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, metrics-root-cause-diagnoser, data-analysis-for-forecasting, slo-breach-checker |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, ci-log-root-cause-debugger, service-dependency-mapper, deployment-build-triager |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, incident-summary-writer, metrics-overview, dependency-risk-auditor, metrics-root-cause-diagnoser |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, paper-summariser, document-summariser, source-grounding-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, data-analysis-for-reporting, document-summariser, meeting-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 4 | 4 | `citation-note-extractor` | wrong | citation-note-extractor, document-field-extractor, document-extractor, source-grounding-extractor, document-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, secret-leak-scanner, data-analysis-for-forecasting, news-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-summariser, capacity-risk-forecaster, news-theme-extractor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, grafana-dashboard-builder, github-issue-triager, metrics-overview, latency-anomaly-detector |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, prometheus-alert-rule-writer, deployment-build-triager, task-extractor |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 5 | 5 | `metrics-overview` | wrong | metrics-overview, latency-anomaly-detector, grafana-dashboard-builder, news-theme-extractor, distributed-trace-investigator |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, incident-summary-writer, meeting-notes-action-extractor, followup-reply-writer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, pr-reviewer, pdf-redaction-reviewer, repo-code-reviewer, architecture-boundary-reviewer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, email-classification-router, skill-router-policy-designer, review-comment-resolver, hf-dataset-viewer-inspector |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-form-filler, pdf-to-docx-converter, pdf-layout-table-extractor, skill-finder |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-question-answerer, pdf-layout-reviewer, slide-deck-visual-auditor |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, layout-preserving-converter, multi-document-comparison-preparer, pr-review-comment-resolver, review-comment-resolver |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, data-analysis-with-validation, sentence-transformer-finetuner, citation-grounding-helper |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, office-to-markdown-converter, deployment-release-verifier, visual-regression-checker |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, pdf-to-docx-converter, document-converter, docx-redline-editor |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, pdf-form-filler, gradio-demo-builder |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, skill-authoring-guide, pr-review-comment-resolver, rest-api-contract-designer, review-comment-resolver |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, openapi-contract-reviewer, database-migration-risk-assessor, skill-authoring-guide, citation-note-extractor |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-notes-action-extractor, weekly-planner, task-extractor, meeting-agenda-builder |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, related-work-synthesiser, document-field-extractor, followup-reply-writer |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, service-mesh-traffic-debugger, prometheus-alert-rule-writer, api-documentation-writer, slo-breach-narrative-writer |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, pdf-to-docx-converter, pdf-redaction-reviewer, pdf-layout-table-extractor, layout-preserving-converter |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, pdf-layout-reviewer, web-data-extractor, pdf-to-docx-converter |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-reviewer, pdf-layout-table-extractor, web-data-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, multi-document-comparison-preparer, pdf-redaction-reviewer, skill-packager, document-summariser |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, document-field-extractor, external-api-integration-planner, multi-document-comparison-preparer, document-extractor |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, layout-preserving-converter, office-to-markdown-converter, pdf-layout-table-extractor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-notes-action-extractor, followup-reply-writer, meeting-summary-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 4 | 4 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, calendar-scheduling-optimizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, followup-reply-writer, meeting-followup-extractor, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, release-note-writer, meeting-followup-extractor, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 18 | 18 | `calendar-scheduling-optimizer` | wrong | calendar-scheduling-optimizer, meeting-agenda-builder, skill-evaluator, meeting-summary-writer, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, multi-source-comparison-builder, general-source-summariser, method-note-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, professor-email-reply, data-analysis-for-reporting, incident-summary-writer, groupwork-reply |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, release-changelog-generator, method-note-builder, api-documentation-writer |
| `read_p4_document_extraction` | `document-extractor` | 1 | 1 | `document-extractor` | gold | document-extractor, pdf-layout-table-extractor, web-data-extractor, document-field-extractor, pdf-form-filler |
| `read_p5_method_notes` | `method-note-builder` | 2 | 2 | `hf-community-eval-runner` | wrong | hf-community-eval-runner, method-note-builder, citation-grounding-helper, review-comment-resolver, web-data-extractor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, skill-evaluator, citation-note-extractor, data-analysis-for-reporting, skill-creator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 2 | 2 | `news-briefing-writer` | wrong | news-briefing-writer, multi-source-comparison-builder, data-analysis-for-ranking-selection, pdf-layout-table-extractor, pdf-to-docx-converter |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-document-comparison-preparer, release-note-writer, data-analysis-for-reporting, weekly-planner |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, followup-reply-writer, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, followup-reply-writer, reply-drafter, groupwork-reply |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, meeting-followup-extractor, web-ui-tester |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, meeting-followup-extractor, slo-breach-narrative-writer, incident-summary-writer, reply-drafter |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, followup-reply-writer, reply-drafter, citation-note-extractor, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, code-reviewer, skill-hierarchy-flattener, api-security-threat-reviewer, skill-editor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, accessibility-checker, pr-reviewer, api-security-threat-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, pr-reviewer, skill-installer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, deployment-release-verifier, skill-finder, notion-research-database-builder |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, data-analysis-with-validation, email-classification-router, accessibility-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, reply-drafter, grafana-dashboard-builder, repo-code-reviewer, news-theme-extractor |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-notes-action-extractor, incident-summary-writer, meeting-followup-extractor, followup-reply-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, code-reviewer, web-ui-tester, skill-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, skill-editor, meeting-followup-extractor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-field-auditor, document-field-extractor, skill-authoring-guide, skill-evaluator |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, citation-grounding-helper, reply-polisher, reply-drafter, skill-finder |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, skill-hierarchy-flattener, skill-editor, skill-field-auditor |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, airtable-workflow-automator, skill-creator, skill-authoring-guide, gradio-demo-builder |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-field-auditor, skill-editor, skill-hierarchy-flattener, skill-finder |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-installer, skill-hierarchy-flattener, skill-finder |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-installer-wrapper, skill-editor, skill-router-policy-designer |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-finder, skill-hierarchy-flattener, skill-packager |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, slo-breach-checker |

### `m1_tfidf_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, mcp-server-builder, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 2 | 2 | `rest-api-contract-designer` | wrong | rest-api-contract-designer, external-api-integration-planner, api-security-threat-reviewer, pr-review-comment-resolver, openapi-contract-reviewer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, reply-drafter, auth-flow-integrator, reply-polisher |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, pr-review-comment-resolver, review-comment-resolver, skill-creator, security-threat-modeler |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, dependency-risk-auditor, pdf-redaction-reviewer, grafana-dashboard-builder, privacy-risk-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, web-performance-budget-checker, skill-evaluator, data-analysis-for-reporting, data-analysis-for-forecasting |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, api-documentation-writer, skill-editor |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, security-threat-modeler, skill-installer-wrapper, review-comment-resolver |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, auth-flow-integrator, privacy-risk-reviewer, pdf-redaction-reviewer |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, webhook-integration-planner, grafana-dashboard-builder, webhook-contract-planner |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, skill-field-auditor, api-security-threat-reviewer |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, security-threat-modeler, auth-flow-reviewer, api-documentation-writer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, metrics-overview, accessibility-interaction-auditor, pdf-layout-reviewer, changelog-writer |
| `web_p2_form_filling` | `web-form-filler` | 3 | 3 | `pdf-form-filler` | wrong | pdf-form-filler, web-ui-tester, web-form-filler, playwright-flow-debugger, gradio-demo-builder |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, reply-drafter, webhook-contract-planner, pdf-layout-reviewer |
| `web_p4_data_extraction` | `web-data-extractor` | 15 | 15 | `web-page-snapshotter` | wrong | web-page-snapshotter, pdf-layout-reviewer, pdf-layout-table-extractor, release-note-writer, prometheus-alert-rule-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, rest-api-contract-designer, web-page-snapshotter, api-documentation-writer, api-security-threat-reviewer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, web-form-filler, layout-preserving-converter, pdf-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, repo-code-reviewer, pr-review-comment-resolver, review-comment-resolver, web-page-snapshotter |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-review-comment-resolver, database-migration-risk-assessor, review-comment-resolver, api-documentation-writer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, ci-log-root-cause-debugger, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, auth-flow-reviewer, auth-flow-integrator, data-analysis-for-root-cause-diagnosis |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, auth-flow-reviewer, auth-flow-integrator |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, release-changelog-generator, slo-breach-checker, web-ui-tester, docx-redline-editor |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, pdf-question-answerer, data-analysis-for-forecasting, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, ci-log-root-cause-debugger, metrics-root-cause-diagnoser, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `github-issue-triager` | wrong | github-issue-triager, data-analysis-with-validation, pdf-form-filler, accessibility-checker, data-analysis-for-ranking-selection |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, data-analysis-for-forecasting, data-analysis-for-reporting, tech-news-trend-extractor |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, web-ui-tester, skill-hierarchy-flattener, citation-note-extractor |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, frontend-debugger |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, meeting-notes-action-extractor, database-migration-risk-assessor, release-note-writer, data-analysis-overview |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, auth-flow-integrator, accessibility-interaction-auditor, web-performance-budget-checker |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, code-reviewer, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, data-analysis-with-anomaly-focus, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 6 | 6 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, data-analysis-for-root-cause-diagnosis, frontend-debugger, metrics-root-cause-diagnoser, ci-failure-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-note-writer, release-changelog-generator, meeting-notes-action-extractor, data-analysis-for-root-cause-diagnosis |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pr-review-comment-resolver, deployment-build-triager, pdf-ocr-extractor |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, ci-failure-debugger, multi-document-comparison-preparer, multi-source-comparison-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, pdf-to-docx-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-to-docx-converter, docx-redline-editor, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `meeting-followup-extractor` | wrong | meeting-followup-extractor, document-field-extractor, web-data-extractor, meeting-notes-action-extractor, pdf-layout-table-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, visual-regression-checker, document-normaliser, multi-source-comparison-builder, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, document-converter, pdf-layout-reviewer, visual-regression-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, pdf-layout-table-extractor, office-to-markdown-converter |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, data-analysis-for-root-cause-diagnosis, ci-failure-debugger, metrics-root-cause-diagnoser, frontend-debugger |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, general-source-summariser, followup-reply-writer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 1 | 1 | `repo-code-reviewer` | gold | repo-code-reviewer, code-reviewer, ci-log-root-cause-debugger, pr-review-comment-resolver, review-comment-resolver |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, accessibility-checker, email-classification-router, skill-creator, security-threat-modeler |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, review-comment-resolver, release-note-writer, pr-review-comment-resolver, code-reviewer |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, pr-review-comment-resolver, auth-flow-reviewer, repo-code-reviewer, review-comment-resolver |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, gradio-demo-builder, pdf-layout-table-extractor, skill-creator, web-ui-tester |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, hf-dataset-viewer-inspector, hf-community-eval-runner, hf-zerogpu-space-deployer, data-analysis-for-ranking-selection |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-authoring-guide, skill-router-policy-designer, skill-benchmark-evaluator, skill-editor |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 3 | 3 | `web-ui-tester` | wrong | web-ui-tester, sentence-transformer-finetuner, gradio-demo-builder, xlsx-formula-model-builder, task-extractor |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, gradio-demo-builder, hf-dataset-viewer-inspector, hf-community-eval-runner, hf-local-model-selector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, gradio-demo-builder, hf-local-model-selector, hf-zerogpu-space-deployer |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger, related-work-synthesiser, data-analysis-overview |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, data-analysis-overview, web-performance-budget-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, service-dependency-mapper, dependency-risk-auditor, privacy-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-narrative-writer, slo-breach-checker, metrics-root-cause-diagnoser, metrics-overview |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, ci-log-root-cause-debugger, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, document-converter, document-summariser, multi-document-comparison-preparer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, document-field-extractor, citation-note-extractor, general-source-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, data-analysis-for-forecasting, news-summariser, general-source-summariser |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, dependency-risk-auditor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, grafana-dashboard-builder, slo-breach-narrative-writer, deployment-build-triager, latency-anomaly-detector |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, prometheus-alert-rule-writer, metrics-overview, pdf-layout-table-extractor, layout-preserving-converter |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 2 | 2 | `grafana-dashboard-builder` | wrong | grafana-dashboard-builder, distributed-trace-investigator, latency-anomaly-detector, hf-local-model-selector, data-analysis-for-root-cause-diagnosis |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, slo-breach-checker, web-performance-budget-checker, incident-summary-writer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, pr-review-comment-resolver, review-comment-resolver, pr-reviewer, skill-router-policy-designer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, email-classification-router, skill-router-policy-designer, resilience-pattern-reviewer, service-dependency-mapper |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-layout-table-extractor, pdf-form-filler, pdf-question-answerer, web-page-snapshotter |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, pdf-question-answerer, web-page-snapshotter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, pdf-to-docx-converter, pr-review-comment-resolver, review-comment-resolver, document-normaliser |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, xlsx-formula-model-builder, skill-hierarchy-flattener, distributed-trace-investigator, incident-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, pdf-layout-reviewer, pr-review-comment-resolver, review-comment-resolver, visual-regression-checker |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, docx-redline-editor, pdf-to-docx-converter, pdf-layout-table-extractor |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, deployment-build-triager, data-analysis-with-validation |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, skill-authoring-guide, release-changelog-generator, pdf-form-filler, review-comment-resolver |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, pr-review-comment-resolver, database-migration-risk-assessor, review-comment-resolver, multi-source-comparison-builder |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-agenda-builder, meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, related-work-synthesiser, calendar-scheduling-optimizer, reply-drafter |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, service-mesh-traffic-debugger, dependency-risk-auditor, privacy-risk-reviewer, database-migration-risk-assessor |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, pdf-layout-table-extractor, web-page-snapshotter, pdf-redaction-reviewer, pdf-layout-reviewer |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, pdf-layout-reviewer, pdf-ocr-extractor, pdf-ocr-cleaner |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 2 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, web-page-snapshotter, pdf-layout-table-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, pdf-question-answerer, pdf-redaction-reviewer, pdf-to-docx-converter, pdf-layout-reviewer |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, pdf-question-answerer, pdf-layout-reviewer, external-api-integration-planner, web-page-snapshotter |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, pdf-ocr-extractor, layout-preserving-converter, docx-redline-editor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-notes-action-extractor, meeting-followup-extractor, groupwork-reply |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 4 | 4 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, task-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 3 | 3 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, task-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 4 | 4 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, task-extractor, meeting-agenda-builder |
| `plan_p5_weekly_planner` | `weekly-planner` | 18 | 18 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, calendar-scheduling-optimizer, meeting-summary-writer, meeting-followup-extractor, task-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, method-note-builder, notion-research-database-builder, professor-email-reply |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, professor-email-reply, document-converter, data-analysis-for-reporting |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, citation-grounding-helper, reply-drafter, ci-failure-debugger, source-grounding-extractor |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, document-extractor, pdf-layout-table-extractor, multi-document-comparison-preparer, document-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 4 | 4 | `citation-grounding-helper` | wrong | citation-grounding-helper, hf-community-eval-runner, related-work-synthesiser, method-note-builder, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, sentence-transformer-finetuner, document-extractor, source-grounding-extractor, citation-note-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `related-work-synthesiser` | wrong | related-work-synthesiser, method-note-builder, citation-note-extractor, citation-grounding-helper, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, release-note-writer, multi-document-comparison-preparer, notion-research-database-builder, multi-source-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, groupwork-reply, followup-reply-writer |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, auth-flow-integrator, playwright-flow-debugger |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, news-briefing-writer, rest-api-contract-designer, meeting-followup-extractor |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, citation-note-extractor, document-summariser |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, privacy-risk-reviewer, external-api-integration-planner, auth-flow-reviewer, skill-hierarchy-flattener |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, pr-reviewer, pr-review-comment-resolver, api-security-threat-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, privacy-risk-reviewer, database-migration-risk-assessor, capacity-risk-forecaster, deployment-build-triager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, database-migration-risk-assessor, webhook-integration-planner, webhook-contract-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-classification-router, auth-flow-integrator, release-note-writer, data-analysis-with-validation |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 13 | 13 | `web-data-extractor` | wrong | web-data-extractor, data-analysis-for-reporting, release-note-writer, repo-code-reviewer, data-analysis-for-forecasting |
| `skill_p1_find_existing` | `skill-finder` | 3 | 3 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-followup-extractor, skill-finder, meeting-agenda-builder, skill-editor |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, hf-local-model-selector, code-reviewer, spreadsheet-formula-auditor |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, meeting-followup-extractor, skill-editor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-installer, skill-finder, skill-evaluator, skill-packager |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, skill-installer, skill-installer-wrapper, skill-editor |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, gradio-demo-builder, skill-creator, xlsx-formula-model-builder, airtable-workflow-automator |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 9 | 9 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-finder, skill-installer |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-installer, skill-finder, skill-field-auditor, skill-editor |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, skill-installer-wrapper, skill-installer |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-finder, skill-editor, skill-packager |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, resilience-pattern-reviewer |

### `m3_tfidf_schema` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, mcp-server-builder, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, webhook-contract-planner, auth-flow-integrator, rest-api-contract-designer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | 2 | `webhook-integration-planner` | wrong | webhook-integration-planner, webhook-contract-planner, auth-flow-integrator, followup-reply-writer, external-api-integration-planner |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, data-analysis-for-forecasting, groupwork-reply, security-threat-modeler, dependency-risk-auditor |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, skill-installer-wrapper, deployment-release-verifier, grafana-dashboard-builder, dependency-risk-auditor |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, service-dependency-mapper, architecture-boundary-reviewer, data-analysis-for-forecasting, web-performance-budget-checker |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, external-api-integration-planner, api-documentation-writer |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, api-documentation-writer, skill-packager, api-security-threat-reviewer |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 2 | 2 | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-integration-planner, auth-flow-integrator, external-api-integration-planner, openapi-contract-reviewer |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, grafana-dashboard-builder, secret-leak-scanner, gradio-demo-builder |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, external-api-integration-planner, api-security-threat-reviewer |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, external-api-integration-planner, security-threat-modeler, privacy-risk-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, metrics-overview, web-data-extractor, visual-regression-checker, frontend-debugger |
| `web_p2_form_filling` | `web-form-filler` | 3 | 3 | `pdf-form-filler` | wrong | pdf-form-filler, web-ui-tester, web-form-filler, frontend-debugger, gradio-demo-builder |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, web-data-extractor, web-form-filler, pdf-layout-reviewer |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, pdf-layout-table-extractor, pdf-layout-reviewer, pdf-ocr-extractor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, web-ui-tester, rest-api-contract-designer, webhook-contract-planner |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, release-note-writer, layout-preserving-converter, github-issue-triager |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, repo-code-reviewer, changelog-writer, email-classification-router, ci-failure-debugger |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, code-reviewer, database-migration-risk-assessor, pr-review-comment-resolver, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-review-comment-resolver, pr-reviewer, code-reviewer, ci-failure-debugger |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, auth-flow-integrator, frontend-debugger, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, auth-flow-integrator, code-reviewer |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, release-changelog-generator, slo-breach-checker, capacity-risk-forecaster |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-reporting, spreadsheet-formula-auditor, data-analysis-for-root-cause-diagnosis |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, deployment-build-triager, ci-log-root-cause-debugger, ci-failure-debugger |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, pdf-form-filler, skill-field-auditor, data-analysis-with-anomaly-focus, web-data-extractor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, distributed-trace-investigator, web-performance-budget-checker, data-analysis-with-validation |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, data-analysis-with-validation, data-analysis-for-root-cause-diagnosis, release-note-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, architecture-boundary-reviewer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, data-analysis-overview, meeting-notes-action-extractor, data-analysis-for-forecasting, hf-local-model-selector |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, web-form-filler, web-ui-tester, web-page-snapshotter |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, latency-anomaly-detector, web-page-snapshotter, accessibility-checker |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, playwright-flow-debugger, frontend-debugger, deployment-build-triager |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 1 | 1 | `deployment-build-triager` | gold | deployment-build-triager, ci-log-root-cause-debugger, frontend-debugger, ci-failure-debugger, secret-leak-scanner |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, database-migration-risk-assessor, release-note-writer, release-changelog-generator, deployment-build-triager |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, frontend-debugger, pdf-ocr-cleaner, pdf-ocr-extractor |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, citation-note-extractor, metrics-overview, paper-summariser, general-source-summariser |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, document-normaliser, document-converter, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, docx-redline-editor, pdf-to-docx-converter, document-rewriter |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, web-data-extractor, document-extractor, method-note-builder, skill-field-auditor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, citation-grounding-helper, release-note-writer, repo-code-reviewer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, pdf-layout-reviewer, document-normaliser, layout-preserving-converter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, document-converter, pdf-layout-reviewer, pdf-layout-table-extractor |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, ci-failure-debugger, deployment-build-triager, frontend-debugger, pr-review-comment-resolver |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, code-reviewer, repo-code-reviewer, pr-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, review-comment-resolver, pr-reviewer, ci-log-root-cause-debugger |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, security-threat-modeler, data-analysis-with-validation, release-changelog-generator, accessibility-checker |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, changelog-writer, release-note-writer, code-reviewer, review-comment-resolver |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, secret-leak-scanner, github-issue-triager, release-changelog-generator, auth-flow-reviewer |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, hf-local-model-selector, pdf-layout-table-extractor, gradio-demo-builder, sentence-transformer-finetuner |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, hf-dataset-viewer-inspector, hf-zerogpu-space-deployer, hf-community-eval-runner, data-analysis-for-ranking-selection |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-authoring-guide, skill-installer, skill-hierarchy-flattener, skill-creator |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, sentence-transformer-finetuner, hf-local-model-selector, xlsx-formula-model-builder, web-ui-tester |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, hf-community-eval-runner, hf-dataset-viewer-inspector, gradio-demo-builder, hf-local-model-selector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, hf-zerogpu-space-deployer, sentence-transformer-finetuner, gradio-demo-builder |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, slo-breach-checker, latency-anomaly-detector, github-issue-triager, data-analysis-overview |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, web-performance-budget-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, metrics-overview, resilience-pattern-reviewer, capacity-risk-forecaster, dependency-risk-auditor |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-overview, slo-breach-narrative-writer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, latency-anomaly-detector, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, slo-breach-checker, capacity-risk-forecaster, latency-anomaly-detector |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-theme-extractor, news-briefing-writer, tech-news-trend-extractor, general-source-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `news-summariser` | wrong | news-summariser, news-briefing-writer, news-theme-extractor, metrics-overview, capacity-risk-forecaster |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, general-source-summariser, news-briefing-writer, news-summariser, news-theme-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, news-summariser, source-grounding-extractor, news-briefing-writer |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, source-grounding-extractor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, grafana-dashboard-builder, deployment-build-triager, latency-anomaly-detector, metrics-overview |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, prometheus-alert-rule-writer, metrics-overview, pdf-layout-reviewer, latency-anomaly-detector |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 1 | 1 | `distributed-trace-investigator` | gold | distributed-trace-investigator, grafana-dashboard-builder, latency-anomaly-detector, metrics-overview, web-performance-budget-checker |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, incident-summary-writer, slo-breach-checker, meeting-followup-extractor, followup-reply-writer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, skill-router-policy-designer, ci-failure-debugger, review-comment-resolver, playwright-flow-debugger |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, email-classification-router, resilience-pattern-reviewer, skill-hierarchy-flattener, skill-router-policy-designer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-question-answerer, pdf-layout-table-extractor, pdf-ocr-extractor, pdf-form-filler |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-question-answerer, pdf-layout-table-extractor, web-page-snapshotter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, pdf-to-docx-converter, document-normaliser, pr-review-comment-resolver, review-comment-resolver |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-data-extractor, incident-summary-writer, skill-evaluator, skill-installer-wrapper |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, skill-evaluator, pdf-layout-reviewer, office-to-markdown-converter |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, pdf-to-docx-converter, docx-redline-editor, layout-preserving-converter, document-converter |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, deployment-build-triager, hf-local-model-selector |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, notion-research-database-builder, skill-authoring-guide, skill-creator, skill-evaluator |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, paper-summariser, citation-note-extractor, related-work-synthesiser, multi-source-comparison-builder |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-followup-extractor |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, followup-reply-writer, reply-polisher |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, service-mesh-traffic-debugger, pdf-redaction-reviewer, skill-hierarchy-flattener, skill-router-policy-designer |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, pdf-redaction-reviewer, pdf-ocr-extractor, pdf-layout-reviewer, web-page-snapshotter |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, pdf-ocr-extractor, pdf-form-filler, pdf-layout-reviewer |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-question-answerer |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, pdf-question-answerer, pdf-to-docx-converter, pdf-redaction-reviewer, pdf-layout-table-extractor |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, pdf-question-answerer, pdf-to-docx-converter, pdf-ocr-cleaner, pdf-ocr-extractor |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, office-to-markdown-converter, docx-redline-editor, layout-preserving-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, task-extractor, meeting-followup-extractor, weekly-planner |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-notes-action-extractor, meeting-followup-extractor, task-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 1 | 1 | `meeting-followup-extractor` | gold | meeting-followup-extractor, meeting-agenda-builder, meeting-notes-action-extractor, meeting-summary-writer, task-extractor |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, meeting-notes-action-extractor, meeting-agenda-builder, weekly-planner, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 1 | 1 | `weekly-planner` | gold | weekly-planner, meeting-agenda-builder, task-extractor, meeting-summary-writer, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, general-source-summariser, method-note-builder, citation-note-extractor, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, professor-email-reply, data-analysis-for-reporting, citation-note-extractor |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, document-extractor, paper-summariser, multi-source-comparison-builder, method-note-builder |
| `read_p4_document_extraction` | `document-extractor` | 3 | 3 | `web-data-extractor` | wrong | web-data-extractor, pdf-form-filler, document-extractor, pdf-layout-table-extractor, document-summariser |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, multi-source-comparison-builder, weekly-planner, citation-note-extractor, document-extractor |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, document-extractor, citation-note-extractor, sentence-transformer-finetuner, web-performance-budget-checker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `paper-summariser` | wrong | paper-summariser, method-note-builder, related-work-synthesiser, citation-note-extractor, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, paper-summariser, multi-source-comparison-builder, general-source-summariser, citation-grounding-helper |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, professor-email-reply, followup-reply-writer |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, professor-email-reply, reply-drafter, followup-reply-writer, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, meeting-summary-writer, reply-drafter, general-source-summariser |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, pr-review-comment-resolver |
| `sec_p1_threat_model` | `security-threat-modeler` | 4 | 4 | `security-code-reviewer` | wrong | security-code-reviewer, auth-flow-reviewer, privacy-risk-reviewer, security-threat-modeler, api-security-threat-reviewer |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, security-threat-modeler, api-security-threat-reviewer, pr-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, security-threat-modeler, architecture-boundary-reviewer, database-migration-risk-assessor, privacy-risk-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, deployment-release-verifier, database-migration-risk-assessor, notion-research-database-builder, webhook-contract-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-classification-router, auth-flow-integrator, release-note-writer, accessibility-checker |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 5 | 5 | `email-classification-router` | wrong | email-classification-router, pdf-layout-reviewer, grafana-dashboard-builder, data-analysis-with-validation, privacy-risk-reviewer |
| `skill_p1_find_existing` | `skill-finder` | 2 | 2 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, skill-finder, skill-creator, meeting-followup-extractor, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | 2 | 2 | `skill-packager` | wrong | skill-packager, skill-installer, skill-installer-wrapper, web-ui-tester, skill-finder |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, skill-finder, meeting-notes-action-extractor, skill-editor |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-creator, skill-finder, skill-authoring-guide, skill-field-auditor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, professor-email-reply, followup-reply-writer |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-editor, skill-creator, skill-installer, skill-finder |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, gradio-demo-builder, xlsx-formula-model-builder, skill-authoring-guide, spreadsheet-formula-auditor |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 5 | 5 | `skill-creator` | wrong | skill-creator, skill-editor, skill-finder, skill-field-auditor, skill-authoring-guide |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-finder, skill-installer, skill-creator, skill-authoring-guide |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-authoring-guide, skill-editor, skill-installer |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-packager, skill-editor, skill-installer, skill-finder |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, resilience-pattern-reviewer, ci-failure-debugger, service-dependency-mapper, email-classification-router |

### `m6_bm25_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, mcp-server-builder, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, rest-api-contract-designer, pr-review-comment-resolver, web-ui-tester, api-security-threat-reviewer |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, xlsx-formula-model-builder, auth-flow-integrator, data-analysis-with-validation |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, dependency-risk-auditor, security-threat-modeler, pr-reviewer, data-analysis-for-forecasting |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-release-verifier, dependency-risk-auditor, skill-installer-wrapper, grafana-dashboard-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, distributed-trace-investigator, data-analysis-for-reporting, privacy-risk-reviewer, web-performance-budget-checker |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, api-documentation-writer, pr-review-comment-resolver |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, skill-creator, skill-installer-wrapper, security-threat-modeler |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, external-api-integration-planner, web-ui-tester, auth-flow-integrator |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, grafana-dashboard-builder, secret-leak-scanner, webhook-contract-planner |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, openapi-contract-reviewer, rest-api-contract-designer, skill-field-auditor, external-api-integration-planner |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-threat-modeler, privacy-risk-reviewer, security-code-reviewer, pdf-redaction-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, web-data-extractor, pdf-question-answerer |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, web-form-filler, web-ui-tester, skill-field-auditor, pdf-layout-table-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, pdf-layout-table-extractor, web-page-snapshotter, pdf-form-filler, skill-evaluator |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, pdf-layout-table-extractor, web-page-snapshotter, release-note-writer, pdf-layout-reviewer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, rest-api-contract-designer, pdf-layout-reviewer, metrics-root-cause-diagnoser |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, slo-breach-checker, layout-preserving-converter, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, repo-code-reviewer, release-note-writer, changelog-writer, pr-review-comment-resolver |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-review-comment-resolver, database-migration-risk-assessor, review-comment-resolver, openapi-contract-reviewer |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, code-reviewer, pr-reviewer, reply-drafter |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, web-ui-tester, frontend-debugger, auth-flow-integrator |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, citation-note-extractor, pr-review-comment-resolver |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, release-changelog-generator, slo-breach-checker, changelog-writer, github-issue-triager |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, pdf-question-answerer, data-analysis-for-ranking-selection, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, deployment-build-triager, metrics-root-cause-diagnoser, ci-failure-debugger, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, pdf-form-filler, accessibility-checker, github-issue-triager, data-analysis-with-anomaly-focus |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, web-performance-budget-checker, data-analysis-for-reporting, data-analysis-with-validation |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, news-briefing-writer, citation-grounding-helper, citation-note-extractor, data-analysis-overview |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, followup-reply-writer, metrics-root-cause-diagnoser, meeting-followup-extractor, capacity-risk-forecaster |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, meeting-notes-action-extractor, meeting-followup-extractor, hf-community-eval-runner, data-analysis-for-forecasting |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, auth-flow-reviewer |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, changelog-writer, review-comment-resolver, web-page-snapshotter |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, web-ui-tester, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, metrics-root-cause-diagnoser, frontend-debugger, data-analysis-with-validation |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-changelog-generator, release-note-writer, deployment-build-triager, web-performance-budget-checker |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pr-reviewer, skill-router-policy-designer, news-briefing-writer |
| `doc_p1_document_summary` | `document-summariser` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, document-summariser, citation-note-extractor, news-summariser, data-analysis-with-validation |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, pdf-to-docx-converter, docx-redline-editor, document-normaliser |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-to-docx-converter, document-rewriter, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 2 | 2 | `web-data-extractor` | wrong | web-data-extractor, document-field-extractor, skill-field-auditor, pdf-layout-table-extractor, document-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, pdf-question-answerer, visual-regression-checker, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, pdf-to-docx-converter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-table-extractor, pdf-layout-reviewer, office-to-markdown-converter |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 2 | 2 | `frontend-debugger` | wrong | frontend-debugger, ci-log-root-cause-debugger, ci-failure-debugger, metrics-root-cause-diagnoser, deployment-build-triager |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, code-reviewer, pr-reviewer, security-code-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, pr-reviewer, security-code-reviewer, review-comment-resolver |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, accessibility-checker, slo-breach-checker, citation-note-extractor, citation-grounding-helper |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 3 | 3 | `review-comment-resolver` | wrong | review-comment-resolver, release-note-writer, release-changelog-generator, pr-review-comment-resolver, code-reviewer |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, github-issue-triager, secret-leak-scanner, playwright-flow-debugger, pr-review-comment-resolver |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, gradio-demo-builder, pdf-layout-table-extractor, web-ui-tester, api-documentation-writer |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, hf-dataset-viewer-inspector, hf-community-eval-runner, citation-grounding-helper, data-analysis-for-ranking-selection |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-hierarchy-flattener, skill-benchmark-evaluator, hf-community-eval-runner, skill-authoring-guide |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, xlsx-formula-model-builder, sentence-transformer-finetuner, pdf-ocr-extractor, pdf-ocr-cleaner |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, database-migration-risk-assessor, gradio-demo-builder, deployment-build-triager, hf-dataset-viewer-inspector |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, sentence-transformer-finetuner, gradio-demo-builder, web-data-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger, slo-breach-checker, architecture-boundary-reviewer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 3 | 3 | `pr-reviewer` | wrong | pr-reviewer, metrics-overview, slo-breach-checker, architecture-boundary-reviewer, service-dependency-mapper |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, data-analysis-for-forecasting, metrics-root-cause-diagnoser, metrics-overview |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, data-analysis-for-root-cause-diagnosis, metrics-overview, ci-log-root-cause-debugger |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, news-theme-extractor, tech-news-trend-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, data-analysis-for-reporting, meeting-summary-writer, tech-news-trend-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, citation-note-extractor, document-extractor, document-summariser, document-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, pdf-layout-table-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-briefing-writer, news-theme-extractor, news-summariser, capacity-risk-forecaster |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, grafana-dashboard-builder, github-issue-triager, metrics-overview, skill-benchmark-evaluator |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, task-extractor, service-mesh-traffic-debugger, architecture-boundary-reviewer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 4 | 4 | `metrics-overview` | wrong | metrics-overview, latency-anomaly-detector, grafana-dashboard-builder, distributed-trace-investigator, service-dependency-mapper |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, incident-summary-writer, meeting-notes-action-extractor, slo-breach-checker |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, pr-reviewer, code-reviewer, skill-router-policy-designer, dependency-risk-auditor |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, email-classification-router, prometheus-alert-rule-writer, skill-router-policy-designer, hf-dataset-viewer-inspector |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-form-filler, pdf-layout-table-extractor, pdf-to-docx-converter, skill-field-auditor |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-question-answerer, pdf-layout-reviewer, web-page-snapshotter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, pr-review-comment-resolver, review-comment-resolver, multi-document-comparison-preparer, layout-preserving-converter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, data-analysis-with-validation, web-ui-tester, xlsx-formula-model-builder, sentence-transformer-finetuner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, pdf-layout-reviewer, pr-reviewer, news-theme-extractor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, pdf-to-docx-converter, document-converter, pdf-layout-table-extractor |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, gradio-demo-builder, pdf-form-filler |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, skill-authoring-guide, skill-field-auditor, pr-review-comment-resolver, rest-api-contract-designer |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, paper-summariser, pr-reviewer, related-work-synthesiser, citation-note-extractor |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-notes-action-extractor, meeting-agenda-builder, task-extractor, weekly-planner |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, followup-reply-writer, document-field-extractor, related-work-synthesiser |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, service-mesh-traffic-debugger, prometheus-alert-rule-writer, capacity-risk-forecaster, skill-hierarchy-flattener |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, web-page-snapshotter, pdf-to-docx-converter, layout-preserving-converter, pdf-layout-reviewer |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, web-data-extractor, pdf-layout-reviewer, pdf-ocr-extractor |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-reviewer, pdf-layout-table-extractor, web-data-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, skill-packager, pdf-redaction-reviewer, document-summariser, multi-document-comparison-preparer |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, document-field-extractor, external-api-integration-planner, pdf-question-answerer, document-extractor |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, layout-preserving-converter, office-to-markdown-converter, pdf-layout-table-extractor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-notes-action-extractor, followup-reply-writer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-notes-action-extractor, meeting-followup-extractor, general-source-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, incident-summary-writer, followup-reply-writer, meeting-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, meeting-notes-action-extractor, meeting-agenda-builder, weekly-planner |
| `plan_p5_weekly_planner` | `weekly-planner` | 4 | 4 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, calendar-scheduling-optimizer, meeting-summary-writer, weekly-planner, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, citation-note-extractor, general-source-summariser, incident-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, data-analysis-for-reporting, professor-email-reply, incident-summary-writer, news-theme-extractor |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, release-changelog-generator, release-note-writer, meeting-notes-action-extractor, task-extractor |
| `read_p4_document_extraction` | `document-extractor` | 3 | 3 | `web-data-extractor` | wrong | web-data-extractor, pdf-layout-table-extractor, document-extractor, document-field-extractor, pdf-form-filler |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, hf-community-eval-runner, weekly-planner, review-comment-resolver, web-ui-tester |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, data-analysis-for-reporting, citation-note-extractor, task-extractor, skill-evaluator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 3 | 3 | `news-briefing-writer` | wrong | news-briefing-writer, pdf-layout-table-extractor, multi-source-comparison-builder, pdf-to-docx-converter, data-analysis-for-ranking-selection |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, multi-document-comparison-preparer, release-note-writer, pdf-to-docx-converter, notion-research-database-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, reply-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, skill-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, meeting-followup-extractor, reply-drafter, groupwork-reply, incident-summary-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, api-security-threat-reviewer, code-reviewer, skill-creator, spreadsheet-formula-auditor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, api-security-threat-reviewer, accessibility-checker |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, pr-reviewer, database-migration-risk-assessor |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, notion-research-database-builder, pdf-redaction-reviewer, database-migration-risk-assessor, data-analysis-with-anomaly-focus |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, email-classification-router, data-analysis-with-validation, changelog-writer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, changelog-writer, grafana-dashboard-builder, email-classification-router, data-analysis-overview |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-notes-action-extractor, meeting-followup-extractor, followup-reply-writer, incident-summary-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, hf-community-eval-runner, web-ui-tester, hf-local-model-selector |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, skill-editor, meeting-followup-extractor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `skill-field-auditor` | wrong | skill-field-auditor, skill-editor, document-field-extractor, skill-authoring-guide, skill-evaluator |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, skill-finder, reply-polisher, reply-drafter, skill-authoring-guide |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, skill-editor, skill-hierarchy-flattener, skill-field-auditor |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, airtable-workflow-automator, gradio-demo-builder, skill-authoring-guide, skill-creator |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-hierarchy-flattener, skill-finder |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-hierarchy-flattener, skill-creator, skill-finder |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, skill-installer-wrapper, skill-authoring-guide |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-finder, skill-editor, skill-hierarchy-flattener |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, slo-breach-checker |

### `m6_tfidf_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, mcp-server-builder, external-api-integration-planner |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, rest-api-contract-designer, api-security-threat-reviewer, pr-review-comment-resolver, web-ui-tester |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, auth-flow-integrator, reply-drafter, xlsx-formula-model-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, pr-reviewer, dependency-risk-auditor, security-threat-modeler, pr-review-comment-resolver |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, dependency-risk-auditor, deployment-release-verifier, skill-installer-wrapper, grafana-dashboard-builder |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, web-performance-budget-checker, data-analysis-for-reporting, skill-evaluator, data-analysis-for-forecasting |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, api-documentation-writer, skill-editor |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, skill-creator, security-threat-modeler, skill-editor |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, external-api-integration-planner, auth-flow-integrator, database-migration-risk-assessor |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, grafana-dashboard-builder, webhook-contract-planner, secret-leak-scanner |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, external-api-integration-planner, skill-field-auditor |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-threat-modeler, security-code-reviewer, privacy-risk-reviewer, pdf-redaction-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, pdf-question-answerer |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, web-form-filler, skill-field-auditor, pdf-layout-table-extractor, playwright-flow-debugger |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-page-snapshotter, pdf-layout-table-extractor, reply-drafter, webhook-contract-planner |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, pdf-layout-table-extractor, web-page-snapshotter, pdf-layout-reviewer, release-note-writer |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, rest-api-contract-designer, web-page-snapshotter, api-documentation-writer, pdf-layout-reviewer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, layout-preserving-converter, pdf-form-filler, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, repo-code-reviewer, pr-review-comment-resolver, changelog-writer, review-comment-resolver |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-review-comment-resolver, database-migration-risk-assessor, review-comment-resolver, external-api-integration-planner |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, code-reviewer, reply-drafter |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, auth-flow-integrator, web-ui-tester, auth-flow-reviewer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-changelog-generator, release-note-writer, citation-note-extractor, deployment-release-verifier |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, release-changelog-generator, changelog-writer, github-issue-triager, service-mesh-traffic-debugger |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-ranking-selection, pdf-question-answerer, spreadsheet-formula-auditor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, ci-log-root-cause-debugger, deployment-build-triager, metrics-root-cause-diagnoser, ci-failure-debugger |
| `data_p3_validation` | `data-analysis-with-validation` | 2 | 2 | `github-issue-triager` | wrong | github-issue-triager, data-analysis-with-validation, pdf-form-filler, accessibility-checker, pdf-layout-reviewer |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, web-performance-budget-checker, data-analysis-for-forecasting, data-analysis-for-reporting |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, citation-note-extractor, hf-community-eval-runner, data-analysis-with-validation |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, capacity-risk-forecaster, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, meeting-notes-action-extractor, database-migration-risk-assessor, dependency-risk-auditor, data-analysis-for-forecasting |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, auth-flow-integrator, web-form-filler, accessibility-interaction-auditor |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-ocr-extractor, review-comment-resolver |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, frontend-debugger, metrics-overview, pdf-form-filler |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 2 | 2 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, deployment-build-triager, frontend-debugger, metrics-root-cause-diagnoser, ci-failure-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, release-changelog-generator, release-note-writer, deployment-build-triager, pdf-question-answerer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, pr-reviewer, pr-review-comment-resolver, news-briefing-writer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, citation-note-extractor, news-summariser, multi-document-comparison-preparer |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, pdf-to-docx-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-to-docx-converter, docx-redline-editor, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 1 | 1 | `document-field-extractor` | gold | document-field-extractor, web-data-extractor, pdf-layout-table-extractor, skill-field-auditor, document-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, multi-source-comparison-builder, visual-regression-checker, document-normaliser, release-note-writer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, visual-regression-checker |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-table-extractor, document-converter, pdf-layout-reviewer |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, ci-failure-debugger, frontend-debugger, metrics-root-cause-diagnoser, deployment-build-triager |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, code-reviewer, security-code-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, pr-reviewer, review-comment-resolver, pr-review-comment-resolver |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, accessibility-checker, data-analysis-with-validation, security-threat-modeler, pdf-form-filler |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, review-comment-resolver, release-note-writer, pr-review-comment-resolver, code-reviewer |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, github-issue-triager, secret-leak-scanner, pr-review-comment-resolver, database-migration-risk-assessor |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, gradio-demo-builder, pdf-layout-table-extractor, web-ui-tester, api-documentation-writer |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, hf-dataset-viewer-inspector, hf-community-eval-runner, data-analysis-for-ranking-selection, security-threat-modeler |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-hierarchy-flattener, skill-authoring-guide, skill-router-policy-designer, skill-benchmark-evaluator |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, xlsx-formula-model-builder, sentence-transformer-finetuner, web-ui-tester, pdf-ocr-extractor |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, gradio-demo-builder, database-migration-risk-assessor, deployment-release-verifier, deployment-build-triager |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, gradio-demo-builder, hf-zerogpu-space-deployer, skill-benchmark-evaluator |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger, slo-breach-checker, architecture-boundary-reviewer |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, web-performance-budget-checker, data-analysis-with-anomaly-focus, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, service-dependency-mapper, metrics-overview, dependency-risk-auditor, capacity-risk-forecaster |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, metrics-root-cause-diagnoser, slo-breach-narrative-writer, data-analysis-for-forecasting |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, ci-log-root-cause-debugger, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, service-dependency-mapper, service-mesh-traffic-debugger |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, tech-news-trend-extractor, general-source-summariser, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, metrics-overview, document-converter, data-analysis-for-reporting, tech-news-trend-extractor |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, document-extractor, document-summariser, citation-note-extractor, general-source-summariser |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, pdf-layout-table-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, pdf-question-answerer |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, grafana-dashboard-builder, metrics-overview, latency-anomaly-detector, skill-benchmark-evaluator |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, task-extractor, prometheus-alert-rule-writer, pdf-layout-reviewer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 2 | 2 | `grafana-dashboard-builder` | wrong | grafana-dashboard-builder, distributed-trace-investigator, latency-anomaly-detector, metrics-overview, hf-local-model-selector |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, slo-breach-checker, incident-summary-writer, followup-reply-writer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, pr-reviewer, pr-review-comment-resolver, review-comment-resolver, code-reviewer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, prometheus-alert-rule-writer, email-classification-router, skill-router-policy-designer, release-note-writer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-layout-table-extractor, pdf-form-filler, pdf-to-docx-converter, pdf-question-answerer |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-question-answerer, pdf-layout-reviewer, web-page-snapshotter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, pr-review-comment-resolver, review-comment-resolver, pdf-to-docx-converter, multi-document-comparison-preparer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, xlsx-formula-model-builder, distributed-trace-investigator, web-ui-tester, incident-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, visual-regression-checker, pr-reviewer, pdf-layout-reviewer, news-theme-extractor |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, pdf-to-docx-converter, docx-redline-editor, pdf-layout-table-extractor |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, deployment-build-triager, data-analysis-with-validation |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, skill-authoring-guide, skill-field-auditor, pdf-form-filler, document-field-extractor |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, paper-summariser, pr-reviewer, pr-review-comment-resolver, review-comment-resolver |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-agenda-builder, meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, meeting-followup-extractor, related-work-synthesiser, followup-reply-writer, document-field-extractor |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, service-mesh-traffic-debugger, dependency-risk-auditor, capacity-risk-forecaster, database-migration-risk-assessor |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, web-page-snapshotter, pdf-layout-reviewer, pdf-to-docx-converter, layout-preserving-converter |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, pdf-layout-reviewer, pdf-ocr-extractor, pdf-ocr-cleaner |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 2 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-question-answerer |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, pdf-redaction-reviewer, pdf-question-answerer, secret-leak-scanner, document-summariser |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, pdf-question-answerer, pdf-layout-reviewer, external-api-integration-planner, document-field-extractor |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, layout-preserving-converter, office-to-markdown-converter, pdf-layout-table-extractor |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, meeting-notes-action-extractor, task-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-notes-action-extractor, meeting-summary-writer, meeting-followup-extractor, general-source-summariser |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-notes-action-extractor, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 3 | 3 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, release-note-writer, task-extractor, meeting-agenda-builder, meeting-summary-writer |
| `plan_p5_weekly_planner` | `weekly-planner` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, weekly-planner, calendar-scheduling-optimizer, pr-review-comment-resolver |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, method-note-builder, general-source-summariser, incident-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, professor-email-reply, data-analysis-for-reporting, incident-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, release-changelog-generator, release-note-writer, meeting-notes-action-extractor, task-extractor |
| `read_p4_document_extraction` | `document-extractor` | 2 | 2 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, document-extractor, pdf-form-filler, document-field-extractor, web-data-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, hf-community-eval-runner, citation-grounding-helper, related-work-synthesiser, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, sentence-transformer-finetuner, citation-note-extractor, source-grounding-extractor, web-performance-budget-checker |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 6 | 6 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, pdf-layout-table-extractor, news-briefing-writer |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, release-note-writer, multi-document-comparison-preparer, multi-source-comparison-builder, pdf-to-docx-converter |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, skill-editor |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, meeting-followup-extractor, professor-email-reply, incident-summary-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, api-security-threat-reviewer, skill-creator, email-classification-router, dependency-risk-auditor |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, api-security-threat-reviewer, pr-review-comment-resolver |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, architecture-boundary-reviewer, database-migration-risk-assessor, capacity-risk-forecaster, deployment-build-triager |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, database-migration-risk-assessor, deployment-release-verifier, notion-research-database-builder, webhook-contract-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, email-classification-router, auth-flow-integrator, changelog-writer, release-note-writer |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | 11 | 11 | `release-note-writer` | wrong | release-note-writer, changelog-writer, data-analysis-overview, grafana-dashboard-builder, data-analysis-for-ranking-selection |
| `skill_p1_find_existing` | `skill-finder` | 2 | 2 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, skill-finder, meeting-followup-extractor, followup-reply-writer, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, hf-local-model-selector, code-reviewer, hf-community-eval-runner |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, meeting-followup-extractor, skill-editor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-field-auditor, skill-finder, skill-creator, skill-installer |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, skill-finder, followup-reply-writer |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, skill-editor, skill-installer, paper-summariser |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, airtable-workflow-automator, gradio-demo-builder, skill-creator, skill-authoring-guide |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-finder, skill-hierarchy-flattener |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-finder, skill-creator, skill-installer |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, skill-authoring-guide, skill-installer-wrapper |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-editor, skill-finder, skill-creator |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, skill-evaluator |

### `m1_bm25_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, openapi-contract-tester, api-documentation-writer, api-design-reviewer |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, rest-api-contract-designer, api-integration-planner, public-swebench-security-review, openapi-contract-tester |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-setup-planner, webhook-integration-planner, invoice-payment-checker, public-office-invoice-automation |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-addy-agent-api-and-interface-design, public-mattpocock-improve-codebase-architecture, agent-handoff-orchestrator |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, public-addy-agent-shipping-and-launch, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, distributed-trace-investigator, privacy-policy-drafter, data-analysis-for-reporting, architecture-boundary-reviewer |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, openapi-contract-tester, api-documentation-writer, public-swebench-add-admin-api-endpoint |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 2 | 2 | `public-addy-agent-api-and-interface-design` | wrong | public-addy-agent-api-and-interface-design, mcp-server-builder, rest-api-contract-designer, public-api-design-principles, public-openai-figma-create-design-system-rules |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-setup-planner, webhook-contract-planner, public-addy-agent-security-and-hardening, events-ops-acceptance-test-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, secret-leak-scanner, incident-summary-writer, public-openai-winui-app |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, openapi-contract-reviewer, public-openai-cli-creator, skill-field-auditor, public-api-design-principles |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, privacy-risk-reviewer, security-threat-modeler, public-swebench-security-review |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, public-n-skills-dev-browser, public-mattpocock-triage, pdf-layout-reviewer, implicit-browser-flow-investigator |
| `web_p2_form_filling` | `web-form-filler` | 3 | 3 | `pdf-form-filler` | wrong | pdf-form-filler, public-n-skills-dev-browser, web-form-filler, public-office-pdf-form-filler, public-openai-playwright |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, dashboard-ops-acceptance-test-builder, skill-evaluator, pdf-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, implicit-pdf-table-reconstructor, pdf-layout-table-extractor, product-ops-resource-linker |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, implicit-browser-flow-investigator, implicit-ci-failure-reader, public-addy-agent-code-simplification, debugging-root-cause-helper |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, reply-drafter, skill-benchmark-evaluator, slo-breach-checker |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, public-mattpocock-review, repo-code-reviewer, email-thread-summariser, public-oh-my-changelog-maintenance |
| `code_p2_pr_review` | `pr-reviewer` | 2 | 2 | `pr-description-writer` | wrong | pr-description-writer, pr-reviewer, public-mattpocock-review, pr-review-comment-resolver, public-oh-my-changelog-maintenance |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 3 | 3 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, implicit-review-comment-planner, review-comment-resolver, pr-description-writer, public-openai-gh-address-comments |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, public-addy-agent-debugging-and-error-recovery, implicit-ci-failure-reader, ci-log-root-cause-debugger, public-mattpocock-diagnose |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, public-oh-my-changelog-maintenance, public-swebench-changelog-automation, public-swebench-python-resilience |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, public-office-changelog-generator, pr-description-writer, public-n-skills-open-source-maintainer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, citation-note-extractor, data-analysis-for-forecasting, public-office-data-analysis, market-opportunity-assessor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, implicit-ci-failure-reader, debugging-root-cause-helper, public-addy-agent-debugging-and-error-recovery, public-huggingface-huggingface-papers |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, accessibility-checker, data-analysis-with-anomaly-focus, slo-breach-checker, pdf-form-filler |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 17 | 17 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, public-office-data-analysis, variance-analysis-helper, public-office-stock-analysis, financial-model-builder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 2 | 2 | `public-office-data-analysis` | wrong | public-office-data-analysis, data-analysis-for-reporting, public-office-stock-analysis, financial-report-writer, public-office-crypto-report |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, implicit-ci-failure-reader, metrics-root-cause-diagnoser, public-office-weather-automation, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, variance-analysis-helper, priority-sorter, dashboard-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, implicit-browser-flow-investigator, frontend-debugger, public-addy-agent-browser-testing-with-devtools |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, implicit-visual-diff-reviewer, public-anthropic-canvas-design, slide-deck-visual-auditor, latency-anomaly-detector |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, public-addy-web-accessibility, public-n-skills-dev-browser |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, public-netlify-deploy, metrics-root-cause-diagnoser, debugging-root-cause-helper, frontend-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-addy-agent-shipping-and-launch, public-oh-my-changelog-maintenance |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, decision-matrix-builder, mobile-ops-acceptance-test-builder, review-comment-resolver, public-swebench-slo-implementation |
| `doc_p1_document_summary` | `document-summariser` | 4 | 4 | `general-source-summariser` | wrong | general-source-summariser, citation-note-extractor, data-analysis-with-validation, document-summariser, public-swebench-v3-performance-optimization |
| `doc_p2_document_rewriter` | `document-rewriter` | 4 | 4 | `reply-polisher` | wrong | reply-polisher, public-docx, pdf-to-docx-converter, document-rewriter, public-mattpocock-edit-article |
| `doc_p3_document_normaliser` | `document-normaliser` | 5 | 5 | `pdf-to-docx-converter` | wrong | pdf-to-docx-converter, layout-preserving-converter, public-docx, deck-template-applier, document-normaliser |
| `doc_p4_field_extraction` | `document-field-extractor` | 4 | 4 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, document-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, public-docx, decision-matrix-builder, public-addy-agent-code-simplification |
| `doc_p6_conversion` | `document-converter` | 1 | 1 | `document-converter` | gold | document-converter, layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, public-obsidian-defuddle |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 2 | 2 | `document-converter` | wrong | document-converter, layout-preserving-converter, pdf-layout-reviewer, pdf-layout-table-extractor, note-tagger |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | - | - | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, frontend-debugger, public-addy-agent-debugging-and-error-recovery, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 2 | 2 | `implicit-review-comment-planner` | wrong | implicit-review-comment-planner, pr-review-comment-resolver, public-openai-security-best-practices, review-comment-resolver, operations-ops-monitoring-plan-builder |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 1 | 1 | `repo-code-reviewer` | gold | repo-code-reviewer, code-reviewer, security-code-reviewer, public-swebench-tdd-workflow, pr-reviewer |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 3 | 3 | `public-mattpocock-triage` | wrong | public-mattpocock-triage, public-mattpocock-setup-matt-pocock-skills, github-issue-triager, public-n-skills-open-source-maintainer, public-mattpocock-to-issues |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 13 | 13 | `release-note-writer` | wrong | release-note-writer, review-comment-resolver, pr-review-comment-resolver, public-office-changelog-generator, public-addy-agent-incremental-implementation |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 2 | 2 | `public-mattpocock-git-guardrails-claude-code` | wrong | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-mattpocock-triage, public-n-skills-open-source-maintainer, public-mattpocock-setup-matt-pocock-skills |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, gradio-demo-builder, public-huggingface-datasets, pdf-layout-table-extractor |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 2 | 2 | `implicit-hf-local-model-chooser` | wrong | implicit-hf-local-model-chooser, hf-local-model-selector, public-huggingface-huggingface-llm-trainer, public-huggingface-huggingface-local-models, public-huggingface-hf-cli |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, skill-benchmark-evaluator, agent-ops-intake-classifier, public-addy-agent-context-engineering |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, public-office-invoice-generator, public-mattpocock-to-issues |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-hf-cli, public-huggingface-huggingface-llm-trainer, public-huggingface-huggingface-papers |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, public-huggingface-hf-cli, public-huggingface-huggingface-vision-trainer, hf-dataset-viewer-inspector, public-huggingface-huggingface-papers |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, related-work-synthesiser, public-mattpocock-setup-matt-pocock-skills, public-swebench-slo-implementation |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, slo-breach-checker, data-analysis-overview |
| `obs_p3_slo_breach` | `slo-breach-checker` | 7 | 7 | `metrics-overview` | wrong | metrics-overview, public-office-contract-review, risk-ops-compliance-checker, risk-ops-acceptance-test-builder, architecture-boundary-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, metrics-overview, metrics-root-cause-diagnoser, implicit-ci-failure-reader, debugging-root-cause-helper |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, metrics-overview, public-openai-playwright, capacity-risk-forecaster, rag-failure-diagnoser |
| `obs_p6_incident_summary` | `incident-summary-writer` | 3 | 3 | `data-analysis-for-reporting` | wrong | data-analysis-for-reporting, public-openai-linear, incident-summary-writer, metrics-overview, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, public-office-news-monitor, paper-summariser, document-summariser |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, public-mattpocock-edit-article, metrics-overview, knowledge-base-article-writer, data-analysis-for-reporting |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 7 | 7 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, citation-note-extractor, document-field-extractor, document-summariser, document-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-anthropic-theme-factory, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-briefing-writer, capacity-risk-forecaster, news-theme-extractor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 2 | 2 | `implicit-slo-alert-author` | wrong | implicit-slo-alert-author, prometheus-alert-rule-writer, public-huggingface-huggingface-trackio, grafana-dashboard-builder, public-swebench-grafana-dashboards |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, cloud-monitoring-configurer, public-swebench-grafana-dashboards, public-openai-sentry |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 13 | 13 | `meeting-scheduler` | wrong | meeting-scheduler, public-swebench-service-mesh-observability, latency-anomaly-detector, cloud-monitoring-configurer, metrics-overview |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, public-mattpocock-writing-beats, incident-summary-writer, email-action-extractor |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, public-swebench-python-resilience, skill-router-policy-designer, webhook-setup-planner, risk-ops-risk-reviewer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, email-classification-router, public-swebench-istio-traffic-management, skill-router-policy-designer, speaker-notes-writer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-pdf, public-openai-pdf, public-office-pdf-form-filler, pdf-form-filler |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 3 | 3 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, public-pdf, pdf-ocr-extractor, public-markitdown, public-office-pdf-watermark |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, public-office-docx-manipulation, layout-preserving-converter, pr-review-comment-resolver |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 3 | 3 | `rag-failure-diagnoser` | wrong | rag-failure-diagnoser, web-ui-tester, spreadsheet-formula-auditor, data-analysis-with-validation, sentence-transformer-finetuner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, public-office-infographic, customer-feedback-analyser, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, pdf-to-docx-converter, public-markitdown |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, public-office-subscription-management, public-office-airtable-automation, public-obsidian-obsidian-bases |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, public-office-airtable-automation, public-office-slack-workflows, skill-authoring-guide, public-anthropic-slack-gif-creator |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, public-office-notion-automation, public-obsidian-obsidian-markdown, public-huggingface-huggingface-paper-publisher, thesis-ops-rewrite-editor |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 2 | 2 | `meeting-scheduler` | wrong | meeting-scheduler, calendar-scheduling-optimizer, calendar-conflict-checker, weekly-planner, meeting-ops-comparison-builder |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, invoice-payment-checker, calendar-conflict-checker, deadline-reminder-planner, email-action-extractor |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, public-office-email-classifier, service-mesh-traffic-debugger, expense-categoriser, implicit-visual-diff-reviewer |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 2 | 2 | `implicit-pdf-evidence-answerer` | wrong | implicit-pdf-evidence-answerer, pdf-question-answerer, public-office-pdf-to-docx, pdf-to-docx-converter, public-office-pdf-converter |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 7 | 7 | `public-office-invoice-template` | wrong | public-office-invoice-template, invoice-payment-checker, implicit-pdf-table-reconstructor, pdf-question-answerer, public-office-chat-with-pdf |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, public-pdf, pdf-layout-reviewer, pdf-layout-table-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, multi-document-comparison-preparer, public-addy-agent-shipping-and-launch |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, document-field-extractor, procurement-risk-summariser, public-openai-pdf, public-office-invoice-automation |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, public-office-pdf-to-docx, layout-preserving-converter, public-office-chat-with-pdf, implicit-pdf-evidence-answerer |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, public-openai-notion-meeting-intelligence, public-pptx, followup-reply-writer, public-office-telegram-bot |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 10 | 10 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, general-source-summariser, meeting-ops-summary-writer, paper-summariser, public-office-transcription-automation |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 9 | 9 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, followup-reply-writer, meeting-summary-writer, meeting-ops-handoff-brief-writer, public-swebench-v3-performance-optimization |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `weekly-planner` | wrong | weekly-planner, task-extractor, release-note-writer, public-mattpocock-writing-shape, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `calendar-scheduling-optimizer` | wrong | calendar-scheduling-optimizer, public-openai-notion-meeting-intelligence, meeting-scheduler, meeting-agenda-builder, agent-eval-coverage-auditor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, multi-source-comparison-builder |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, dashboard-ops-summary-writer, public-office-academic-search |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-evidence-grounder, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | 10 | 10 | `web-data-extractor` | wrong | web-data-extractor, pdf-layout-table-extractor, public-office-pdf-extraction, pdf-form-filler, bioinformatics-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `pr-description-writer` | wrong | pr-description-writer, hf-community-eval-runner, citation-grounding-helper, speaker-notes-writer, review-comment-resolver |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-addy-web-accessibility, agent-eval-coverage-auditor, public-mattpocock-writing-fragments, seed-data-generator |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 4 | 4 | `public-mattpocock-writing-shape` | wrong | public-mattpocock-writing-shape, news-briefing-writer, note-tagger, multi-source-comparison-builder, pdf-to-docx-converter |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 2 | 2 | `public-openai-notion-research-documentation` | wrong | public-openai-notion-research-documentation, related-work-synthesiser, multi-document-comparison-preparer, public-office-academic-search, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, groupwork-reply, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, email-polisher, followup-reply-writer, reply-drafter |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, proposal-drafter, email-action-extractor, followup-reply-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, public-office-investment-memo, email-action-extractor, bioinformatics-ops-handoff-brief-writer, compliance-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, implicit-review-comment-planner, reply-polisher, followup-reply-writer, email-polisher |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-security-threat-model, public-brainstorming, public-openai-figma-code-connect-components, public-addy-agent-api-and-interface-design |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, review-comment-resolver, accessibility-checker, public-addy-agent-security-and-hardening, public-addy-web-best-practices |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, priority-sorter, pr-reviewer, architecture-boundary-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, public-huggingface-huggingface-papers, public-vercel-find-skills, public-addy-agent-frontend-ui-engineering, public-openai-vercel-deploy |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, data-analysis-with-validation, version-control-helper, public-addy-agent-context-engineering |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `churn-risk-analyser` | wrong | churn-risk-analyser, public-swebench-analytics-events, query-optimizer, release-note-writer, public-office-web-search |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, incident-summary-writer, implicit-review-comment-planner, meeting-notes-action-extractor, public-openai-notion-knowledge-capture |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, public-anthropic-webapp-testing, public-huggingface-huggingface-community-evals, public-oh-my-lmstudio-cli |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, public-skill-creator, public-anthropic-skill-creator, skill-editor, public-mattpocock-write-a-skill |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-field-auditor, skill-authoring-guide, skill-evaluator |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, agent-eval-coverage-auditor, citation-grounding-helper, reply-polisher, public-addy-agent-deprecation-and-migration |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, agent-ops-resource-linker, skill-editor, public-anthropic-skill-creator |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, skill-authoring-guide, repo-ops-quality-auditor, hr-ops-quality-auditor, gradio-demo-builder |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 8 | 8 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, public-anthropic-skill-creator, skill-hierarchy-flattener |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, public-skill-installer, skill-installer, skill-finder |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, skill-installer-wrapper, public-anthropic-skill-creator |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-finder, public-skill-installer, skill-packager |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, public-office-saas-metrics, budget-planner, email-classification-router, note-tagger |

### `m1_tfidf_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, openapi-contract-tester, api-documentation-writer, public-swebench-add-admin-api-endpoint |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 7 | 3 | `rest-api-contract-designer` | wrong | rest-api-contract-designer, public-openai-figma-code-connect-components, api-integration-planner, public-swebench-add-admin-api-endpoint, public-office-cover-letter |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | 2 | `invoice-payment-checker` | wrong | invoice-payment-checker, webhook-contract-planner, public-openai-winui-app, duplicate-file-finder, events-ops-failure-diagnoser |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-openai-security-ownership-map, public-addy-agent-api-and-interface-design, public-oh-my-backend-testing |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, public-addy-agent-shipping-and-launch, deployment-rollback-planner, migration-risk-auditor, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, analytics-ops-quality-auditor, implicit-trace-path-diagnoser, public-office-data-pipeline, public-office-md-slides |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, api-documentation-writer, openapi-contract-tester |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, public-office-office-mcp, public-openai-figma-create-design-system-rules, public-oh-my-api-design |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, webhook-setup-planner, public-office-webhook-automation, events-ops-acceptance-test-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, dashboard-ops-compliance-checker, public-office-webhook-automation, dashboard-ops-acceptance-test-builder |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, openapi-contract-tester, rest-api-contract-designer, public-openai-cli-creator, contract-ops-evidence-grounder |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, public-security-threat-model, security-threat-modeler, api-integration-planner |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, public-n-skills-dev-browser, public-openai-screenshot, changelog-writer, dashboard-ops-summary-writer |
| `web_p2_form_filling` | `web-form-filler` | 8 | 8 | `pdf-form-filler` | wrong | pdf-form-filler, variance-analysis-helper, public-office-pdf-form-filler, public-openai-playwright, public-office-expense-report |
| `web_p3_ui_test` | `web-ui-tester` | 7 | 7 | `variance-analysis-helper` | wrong | variance-analysis-helper, web-page-snapshotter, public-office-expense-report, public-office-weekly-report, reply-drafter |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-resource-linker` | wrong | product-ops-resource-linker, product-ops-field-extractor, product-ops-normalizer, product-ops-compliance-checker, product-ops-dependency-mapper |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, api-ops-evidence-grounder, api-ops-field-extractor, api-ops-summary-writer, api-ops-normalizer |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, public-addy-web-accessibility, public-office-pdf-form-filler, pdf-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer, public-oh-my-changelog-maintenance |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, pr-review-comment-resolver, public-mattpocock-review, public-swebench-analyze-ci |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 3 | 3 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, implicit-review-comment-planner, review-comment-resolver, public-openai-gh-address-comments, public-addy-agent-code-review-and-quality |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, auth-flow-reviewer, auth-flow-integrator, ci-log-root-cause-debugger, public-openai-gh-fix-ci |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, public-swebench-changelog-automation, public-oh-my-changelog-maintenance |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, public-oh-my-changelog-maintenance, release-changelog-generator, public-office-changelog-generator, public-swebench-changelog-automation |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, public-office-expense-report, public-office-weekly-report, data-analysis-for-forecasting |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, public-addy-agent-debugging-and-error-recovery, debugging-root-cause-helper, data-analysis-for-root-cause-diagnosis, ci-log-root-cause-debugger |
| `data_p3_validation` | `data-analysis-with-validation` | 16 | 16 | `public-addy-web-web-quality-audit` | wrong | public-addy-web-web-quality-audit, public-oh-my-react-grab, public-addy-web-accessibility, public-oh-my-react-best-practices, public-mattpocock-to-issues |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-office-data-analysis, public-oh-my-data-analysis, implicit-trace-path-diagnoser |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dashboard-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer, public-office-data-analysis, public-office-pdf-watermark |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, public-oh-my-pattern-detection, metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, duplicate-file-finder |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, risk-ops-comparison-builder, dashboard-ops-comparison-builder, risk-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, implicit-browser-flow-investigator, frontend-debugger, public-addy-agent-browser-testing-with-devtools, public-n-skills-dev-browser |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, implicit-visual-diff-reviewer, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, metrics-overview, public-addy-web-web-quality-audit |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 19 | 19 | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, public-netlify-deploy, public-oh-my-game-build-log-triage, debugging-root-cause-helper, ci-log-root-cause-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-changelog-maintenance, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-acceptance-test-builder, budget-planner, mobile-ops-monitoring-plan-builder, mobile-ops-normalizer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, knowledge-base-article-writer, general-source-summariser, receipt-extractor, multi-source-comparison-builder |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, public-mattpocock-edit-article, document-normaliser, public-office-pdf-form-filler |
| `doc_p3_document_normaliser` | `document-normaliser` | 4 | 4 | `layout-preserving-converter` | wrong | layout-preserving-converter, deck-template-applier, pdf-to-docx-converter, document-normaliser, docx-redline-editor |
| `doc_p4_field_extraction` | `document-field-extractor` | 6 | 6 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, public-office-invoice-automation, meeting-followup-extractor, public-office-table-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, multi-document-comparison-preparer, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 5 | 5 | `layout-preserving-converter` | wrong | layout-preserving-converter, public-obsidian-defuddle, office-to-markdown-converter, pdf-layout-reviewer, document-converter |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, office-to-markdown-converter, pdf-layout-table-extractor |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 3 | 3 | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, public-addy-agent-debugging-and-error-recovery, ci-log-root-cause-debugger, debugging-root-cause-helper, data-analysis-for-root-cause-diagnosis |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 4 | 4 | `public-oh-my-code-review` | wrong | public-oh-my-code-review, implicit-review-comment-planner, public-addy-agent-code-review-and-quality, pr-review-comment-resolver, review-comment-resolver |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `public-oh-my-code-review` | wrong | public-oh-my-code-review, repo-code-reviewer, ci-log-root-cause-debugger, public-addy-agent-code-review-and-quality, code-reviewer |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 8 | 8 | `public-mattpocock-triage` | wrong | public-mattpocock-triage, public-mattpocock-to-issues, public-mattpocock-setup-matt-pocock-skills, public-oh-my-to-issues, public-n-skills-open-source-maintainer |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, release-note-writer, public-oh-my-changelog-maintenance, review-comment-resolver, public-office-changelog-generator |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 2 | 2 | `public-mattpocock-git-guardrails-claude-code` | wrong | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-mattpocock-triage, public-oh-my-git-guardrails-claude-code, public-mattpocock-setup-matt-pocock-skills |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-acceptance-test-builder, dataset-ops-intake-classifier, dataset-ops-normalizer |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, implicit-hf-local-model-chooser, public-huggingface-hf-cli, public-huggingface-huggingface-llm-trainer, support-ticket-triager |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, agent-ops-monitoring-plan-builder, agent-ops-intake-classifier, agent-ops-normalizer, agent-ops-compliance-checker |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 4 | 4 | `web-ui-tester` | wrong | web-ui-tester, sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, gradio-demo-builder, public-swebench-python-packaging |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-hf-cli, public-huggingface-huggingface-papers, public-huggingface-huggingface-llm-trainer |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, public-huggingface-hf-cli, hf-dataset-viewer-inspector, public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-gradio |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, public-oh-my-triage, public-oh-my-game-build-log-triage, public-oh-my-game-demo-feedback-triage |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, data-analysis-overview, public-swebench-service-mesh-observability |
| `obs_p3_slo_breach` | `slo-breach-checker` | 9 | 9 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, public-swebench-slo-implementation, sre-ops-risk-reviewer, incident-ops-risk-reviewer, metrics-overview |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-narrative-writer, slo-breach-checker, risk-ops-risk-reviewer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-addy-agent-debugging-and-error-recovery, implicit-ci-failure-reader, debugging-root-cause-helper |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 6 | `incident-ops-normalizer` | wrong | incident-ops-normalizer, incident-ops-compliance-checker, incident-ops-dependency-mapper, incident-ops-scenario-planner, incident-ops-risk-reviewer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, public-mattpocock-edit-article, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, public-mattpocock-edit-article, knowledge-base-article-writer, support-ticket-triager, public-mattpocock-to-prd |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, knowledge-base-article-writer, product-ops-scenario-planner, product-ops-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-theme-extractor, public-office-news-monitor, news-summariser, data-analysis-for-forecasting |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, public-office-news-monitor, news-briefing-writer, news-theme-extractor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 2 | 2 | `implicit-slo-alert-author` | wrong | implicit-slo-alert-author, prometheus-alert-rule-writer, slo-breach-narrative-writer, budget-planner, latency-anomaly-detector |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, prometheus-alert-rule-writer, metrics-overview, dashboard-ops-monitoring-plan-builder, dashboard-ops-normalizer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 4 | 4 | `implicit-trace-path-diagnoser` | wrong | implicit-trace-path-diagnoser, dashboard-ops-normalizer, dashboard-ops-compliance-checker, distributed-trace-investigator, dashboard-ops-dependency-mapper |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, slo-breach-checker, meeting-followup-extractor, web-performance-budget-checker, compliance-ops-timeline-builder |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 4 | 4 | `public-oh-my-obsidian-cli-uri-fallback` | wrong | public-oh-my-obsidian-cli-uri-fallback, webhook-setup-planner, public-swebench-python-resilience, resilience-pattern-reviewer, skill-router-policy-designer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, public-swebench-linkerd-patterns, public-swebench-istio-traffic-management, public-swebench-service-mesh-observability, public-office-pdf-merge-split |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, public-office-pdf-form-filler, pdf-layout-table-extractor, pdf-form-filler, public-office-pdf-watermark |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, public-office-pdf-watermark, pdf-ocr-cleaner, public-office-pdf-converter, public-office-pdf-ocr |
| `office_p3_docx_redline` | `docx-redline-editor` | 2 | 2 | `public-docx` | wrong | public-docx, docx-redline-editor, public-office-docx-manipulation, pdf-to-docx-converter, document-rewriter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, rag-failure-diagnoser, public-office-contract-review, public-swebench-langsmith-fetch, public-office-xlsx-manipulation |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, public-office-ppt-visual, public-oh-my-presentation-builder |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, office-to-markdown-converter, public-docx, docx-redline-editor, pdf-to-docx-converter |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, public-office-airtable-automation, spreadsheet-formula-auditor, public-office-subscription-management, airtable-workflow-automator |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 2 | 2 | `public-office-airtable-automation` | wrong | public-office-airtable-automation, airtable-workflow-automator, skill-authoring-guide, public-anthropic-slack-gif-creator, public-office-slack-workflows |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, public-openai-notion-research-documentation, public-office-notion-automation, thesis-ops-rewrite-editor, public-openai-notion-knowledge-capture |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-ops-comparison-builder, meeting-scheduler, meeting-ops-evidence-grounder, meeting-ops-normalizer |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, calendar-conflict-checker, compliance-ops-summary-writer, docs-ops-summary-writer, partnerships-ops-summary-writer |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, risk-ops-risk-reviewer, public-office-md-slides, public-office-office-to-md, public-office-email-classifier |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, implicit-pdf-evidence-answerer, travel-ops-evidence-grounder, travel-ops-compliance-checker, travel-ops-failure-diagnoser |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, public-office-chat-with-pdf, public-office-invoice-template |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 2 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, public-office-chat-with-pdf, public-addy-agent-shipping-and-launch, public-office-pdf-converter, public-openai-gh-fix-ci |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, vendor-ops-evidence-grounder, pdf-question-answerer, pdf-layout-reviewer, vendor-ops-normalizer |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, public-office-pdf-to-docx, public-office-chat-with-pdf, public-office-pdf-converter, public-docx |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-scenario-planner, meeting-ops-normalizer, meeting-ops-compliance-checker, meeting-ops-dependency-mapper |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | - | - | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-notes-action-extractor, meeting-ops-evidence-grounder, meeting-ops-normalizer, meeting-ops-artifact-packager |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 4 | 4 | `public-office-meeting-notes` | wrong | public-office-meeting-notes, meeting-notes-action-extractor, meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 5 | 5 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, public-office-meeting-notes, meeting-followup-extractor, meeting-summary-writer, task-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-ops-monitoring-plan-builder, meeting-ops-acceptance-test-builder, meeting-ops-summary-writer, meeting-ops-normalizer |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, public-office-academic-search, method-note-builder, public-oh-my-research-paper-writing |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, academic-admin-ops-summary-writer, professor-email-reply, academic-admin-ops-evidence-grounder |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, writing-ops-evidence-grounder, writing-ops-field-extractor, writing-ops-artifact-packager, writing-ops-normalizer |
| `read_p4_document_extraction` | `document-extractor` | - | - | `public-office-table-extractor` | wrong | public-office-table-extractor, research-ops-field-extractor, pdf-form-filler, compliance-ops-field-extractor, docs-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, compliance-ops-scenario-planner, citation-grounding-helper, docs-ops-scenario-planner, partnerships-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-addy-agent-performance-optimization, public-addy-web-web-quality-audit |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 7 | 7 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, citation-grounding-helper, note-linker |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, release-note-writer, public-office-table-extractor, public-openai-notion-research-documentation, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, email-polisher, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, reply-polisher, deadline-reminder-planner, followup-reply-writer |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, public-office-investment-memo, public-oh-my-state-management, public-oh-my-write-a-skill |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, implicit-review-comment-planner, reply-polisher, public-openai-figma-create-new-file, followup-reply-writer |
| `sec_p1_threat_model` | `security-threat-modeler` | 2 | 2 | `public-openai-figma-create-new-file` | wrong | public-openai-figma-create-new-file, security-threat-modeler, email-ops-risk-reviewer, public-security-threat-model, email-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, public-addy-agent-security-and-hardening, public-swebench-slo-implementation, pr-reviewer, review-comment-resolver |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | - | - | `supply-chain-ops-risk-reviewer` | wrong | supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-artifact-packager, supply-chain-ops-normalizer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, public-oh-my-log-analysis, public-huggingface-huggingface-papers, public-office-webhook-automation, webhook-setup-planner |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, public-oh-my-google-workspace, email-ops-monitoring-plan-builder, auth-flow-integrator, version-control-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, public-oh-my-log-analysis, public-swebench-similarity-search-patterns, query-optimizer, public-swebench-dbt-transformation-patterns |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, public-office-meeting-notes, library-ops-evidence-grounder, meeting-ops-evidence-grounder, library-ops-timeline-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, hf-local-model-selector, implicit-hf-local-model-chooser, library-ops-resource-linker, library-ops-acceptance-test-builder |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, public-anthropic-skill-creator, meeting-followup-extractor, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `public-anthropic-skill-creator` | wrong | public-anthropic-skill-creator, skill-editor, public-skill-creator, skill-installer, skill-finder |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 3 | 3 | `reply-polisher` | wrong | reply-polisher, reply-drafter, skill-evaluator, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-anthropic-skill-creator, skill-installer, public-skill-creator |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, gradio-demo-builder, public-addy-web-web-quality-audit, agent-handoff-orchestrator, xlsx-formula-model-builder |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 15 | 15 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, public-anthropic-skill-creator, skill-finder |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-installer, skill-finder, public-anthropic-skill-creator |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, public-anthropic-skill-creator, public-oh-my-write-a-skill |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, public-skill-installer, library-ops-field-extractor, skill-installer, library-ops-dependency-mapper |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, public-swebench-implementing-agent-modes, public-addy-web-core-web-vitals, public-openai-aspnet-core, budget-planner |

### `m3_tfidf_schema` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, openapi-contract-tester, api-documentation-writer, mcp-server-builder |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, openapi-contract-reviewer, api-ops-acceptance-test-builder, webhook-contract-planner, public-swebench-add-admin-api-endpoint |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 2 | 2 | `webhook-integration-planner` | wrong | webhook-integration-planner, webhook-contract-planner, invoice-payment-checker, duplicate-file-finder, public-openai-winui-app |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, public-addy-agent-api-and-interface-design, public-openai-security-ownership-map, public-mattpocock-improve-codebase-architecture |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, public-addy-agent-shipping-and-launch, migration-risk-auditor, deployment-rollback-planner, skill-installer-wrapper |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 6 | 6 | `public-office-microsoft-teams` | wrong | public-office-microsoft-teams, distributed-trace-investigator, analytics-ops-quality-auditor, analytics-ops-timeline-builder, analytics-ops-evidence-grounder |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, external-api-integration-planner, api-documentation-writer |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, public-office-office-mcp, public-openai-figma-create-design-system-rules, api-design-reviewer |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 2 | 2 | `webhook-contract-planner` | wrong | webhook-contract-planner, webhook-integration-planner, webhook-setup-planner, invoice-payment-checker, auth-flow-integrator |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, webhook-setup-planner, secret-leak-scanner, dashboard-ops-acceptance-test-builder |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, openapi-contract-tester, external-api-integration-planner |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, external-api-integration-planner, security-threat-modeler, privacy-risk-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, web-data-extractor, pdf-layout-reviewer, pdf-ocr-extractor, public-n-skills-dev-browser |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, pdf-form-filler, web-ui-tester, variance-analysis-helper, mobile-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, web-page-snapshotter, web-data-extractor, web-form-filler |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, web-page-snapshotter, product-ops-resource-linker, ecommerce-ops-field-extractor, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, web-ui-tester, rest-api-contract-designer, api-ops-timeline-builder |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, release-note-writer, public-office-applicant-screening |
| `code_p1_local_code_review` | `code-reviewer` | 2 | 2 | `git-commit-writer` | wrong | git-commit-writer, code-reviewer, repo-code-reviewer, changelog-writer, test-case-generator |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, public-mattpocock-review, pr-review-comment-resolver, database-migration-risk-assessor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 1 | 1 | `review-comment-resolver` | gold | review-comment-resolver, pr-review-comment-resolver, pr-reviewer, implicit-review-comment-planner, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 2 | 2 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, auth-flow-integrator, auth-flow-reviewer, frontend-debugger |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, public-swebench-changelog-automation, public-oh-my-changelog-maintenance |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, changelog-writer, release-changelog-generator, public-oh-my-changelog-maintenance, deployment-release-verifier |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-ranking-selection, data-analysis-for-root-cause-diagnosis, data-analysis-for-reporting, finance-ops-summary-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, latency-anomaly-detector, real-estate-ops-failure-diagnoser, deployment-build-triager, debugging-root-cause-helper |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, public-addy-web-web-quality-audit, public-oh-my-react-best-practices, public-oh-my-react-grab, pdf-form-filler |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, distributed-trace-investigator, web-performance-budget-checker, data-analysis-with-validation |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, data-analysis-overview, dashboard-ops-handoff-brief-writer, release-note-writer, dashboard-ops-resource-linker |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, capacity-risk-forecaster, frontend-debugger, metrics-root-cause-diagnoser, public-oh-my-pattern-detection |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, data-analysis-overview, data-analysis-for-forecasting, dataset-ops-risk-reviewer |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, web-form-filler, public-addy-agent-browser-testing-with-devtools |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, implicit-visual-diff-reviewer, slide-deck-visual-auditor, public-anthropic-canvas-design, latency-anomaly-detector |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, public-addy-web-web-quality-audit, playwright-flow-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 3 | 3 | `public-netlify-deploy` | wrong | public-netlify-deploy, implicit-ci-failure-reader, deployment-build-triager, ci-log-root-cause-debugger, public-oh-my-game-build-log-triage |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, deployment-rollback-planner, public-openai-vercel-deploy, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, mobile-ops-resource-linker, mobile-ops-acceptance-test-builder, mobile-ops-summary-writer, mobile-ops-normalizer |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, citation-note-extractor, data-analysis-overview, metrics-overview, paper-summariser |
| `doc_p2_document_rewriter` | `document-rewriter` | 1 | 1 | `document-rewriter` | gold | document-rewriter, reply-polisher, email-polisher, document-normaliser, docx-redline-editor |
| `doc_p3_document_normaliser` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, layout-preserving-converter, docx-redline-editor, pdf-to-docx-converter, deck-template-applier |
| `doc_p4_field_extraction` | `document-field-extractor` | - | - | `invoice-payment-checker` | wrong | invoice-payment-checker, receipt-extractor, supply-chain-ops-field-extractor, finance-ops-field-extractor, public-office-invoice-automation |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, compliance-ops-comparison-builder, docs-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, pdf-layout-reviewer, public-obsidian-defuddle, implicit-visual-diff-reviewer |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, office-to-markdown-converter, pdf-layout-reviewer, pdf-layout-table-extractor |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, implicit-ci-failure-reader, ci-failure-debugger, deployment-build-triager, public-addy-agent-debugging-and-error-recovery |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, public-addy-agent-code-review-and-quality, code-reviewer |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, review-comment-resolver, public-oh-my-code-review, public-addy-agent-code-review-and-quality |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, public-mattpocock-triage, debugging-root-cause-helper, public-mattpocock-setup-matt-pocock-skills, public-n-skills-open-source-maintainer |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, changelog-writer, release-note-writer, code-reviewer, review-comment-resolver |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 2 | 2 | `public-mattpocock-git-guardrails-claude-code` | wrong | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-mattpocock-triage, public-oh-my-git-guardrails-claude-code, secret-leak-scanner |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, hf-local-model-selector, gradio-demo-builder, pdf-layout-table-extractor |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 2 | 2 | `implicit-hf-local-model-chooser` | wrong | implicit-hf-local-model-chooser, hf-local-model-selector, public-huggingface-hf-cli, hf-dataset-viewer-inspector, public-huggingface-huggingface-llm-trainer |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, agent-ops-intake-classifier, agent-ops-monitoring-plan-builder, public-huggingface-train-sentence-transformers, agent-ops-resource-linker |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, sentence-transformer-finetuner, hf-local-model-selector, public-huggingface-huggingface-vision-trainer, public-swebench-python-packaging |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-hf-cli, public-huggingface-huggingface-papers, public-huggingface-huggingface-llm-trainer |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 2 | 2 | `public-huggingface-hf-cli` | wrong | public-huggingface-hf-cli, hf-community-eval-runner, hf-dataset-viewer-inspector, public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-papers |
| `obs_p1_metrics_overview` | `metrics-overview` | 2 | 2 | `public-mattpocock-triage` | wrong | public-mattpocock-triage, metrics-overview, public-oh-my-triage, public-mattpocock-setup-matt-pocock-skills, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, data-analysis-with-anomaly-focus, metrics-overview, data-analysis-overview, public-swebench-service-mesh-observability |
| `obs_p3_slo_breach` | `slo-breach-checker` | 1 | 1 | `slo-breach-checker` | gold | slo-breach-checker, sre-ops-risk-reviewer, public-swebench-slo-implementation, metrics-overview, risk-ops-risk-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, slo-breach-narrative-writer, metrics-overview, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, latency-anomaly-detector, capacity-risk-forecaster, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | 2 | 2 | `metrics-overview` | wrong | metrics-overview, incident-summary-writer, slo-breach-checker, incident-ops-resource-linker, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, news-theme-extractor, public-office-news-monitor, general-source-summariser, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 2 | 2 | `news-summariser` | wrong | news-summariser, news-briefing-writer, support-ops-ops-timeline-builder, knowledge-base-article-writer, support-ops-ops-summary-writer |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, product-ops-resource-linker, product-ops-scenario-planner, content-ops-evidence-grounder |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, public-office-news-monitor, news-summariser, source-grounding-extractor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, public-office-news-monitor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 2 | 2 | `implicit-slo-alert-author` | wrong | implicit-slo-alert-author, prometheus-alert-rule-writer, grafana-dashboard-builder, latency-anomaly-detector, metrics-overview |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, prometheus-alert-rule-writer, metrics-overview, dashboard-ops-monitoring-plan-builder, dashboard-ops-summary-writer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 1 | 1 | `distributed-trace-investigator` | gold | distributed-trace-investigator, implicit-trace-path-diagnoser, grafana-dashboard-builder, latency-anomaly-detector, dashboard-ops-resource-linker |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, slo-breach-checker, incident-summary-writer, sre-ops-timeline-builder, sre-ops-risk-reviewer |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, skill-router-policy-designer, public-oh-my-obsidian-cli-uri-fallback, public-swebench-python-resilience, research-ops-failure-diagnoser |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, public-swebench-linkerd-patterns, public-swebench-istio-traffic-management, public-swebench-service-mesh-observability, public-office-pdf-merge-split |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-layout-table-extractor, pdf-question-answerer, pdf-ocr-extractor, pdf-ocr-cleaner |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-ocr-cleaner, public-office-pdf-watermark, pdf-question-answerer, web-page-snapshotter |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, pdf-to-docx-converter, document-normaliser, pr-review-comment-resolver |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, public-xlsx, public-swebench-xlsx, public-office-xlsx-manipulation, engineering-design-ops-summary-writer |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, public-pptx, slide-outline-builder, speaker-notes-writer, public-office-ppt-visual |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, pdf-to-docx-converter, docx-redline-editor, public-docx, layout-preserving-converter |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, public-office-airtable-automation, public-office-subscription-management, airtable-workflow-automator |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, public-office-airtable-automation, public-anthropic-slack-gif-creator, public-office-slack-workflows, public-obsidian-obsidian-bases |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, public-openai-notion-research-documentation, public-office-notion-automation, thesis-ops-timeline-builder, public-openai-notion-knowledge-capture |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-agenda-builder, meeting-scheduler, meeting-summary-writer, meeting-ops-comparison-builder |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, email-action-extractor, meeting-followup-extractor, content-ops-summary-writer, social-ops-summary-writer |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, risk-ops-intake-classifier, public-office-email-classifier, service-mesh-traffic-debugger, compliance-ops-intake-classifier |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, implicit-pdf-evidence-answerer, pdf-redaction-reviewer, pdf-ocr-extractor, pdf-layout-reviewer |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-ocr-extractor, public-office-invoice-template |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-reviewer, pdf-question-answerer, pdf-layout-table-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, compliance-ops-normalizer, compliance-ops-field-extractor, public-office-chat-with-pdf, compliance-ops-quality-auditor |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, pdf-question-answerer, pdf-to-docx-converter, pdf-ocr-cleaner, vendor-ops-normalizer |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, public-office-pdf-to-docx, public-office-chat-with-pdf, pdf-question-answerer, office-to-markdown-converter |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, weekly-planner, meeting-followup-extractor, task-extractor |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 1 | 1 | `meeting-summary-writer` | gold | meeting-summary-writer, meeting-agenda-builder, meeting-notes-action-extractor, public-office-meeting-notes, meeting-followup-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-followup-extractor, public-office-meeting-notes, meeting-agenda-builder, meeting-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 1 | 1 | `task-extractor` | gold | task-extractor, weekly-planner, meeting-notes-action-extractor, meeting-agenda-builder, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, weekly-planner, task-extractor, meeting-summary-writer, meeting-followup-extractor |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, method-note-builder, general-source-summariser, citation-note-extractor, document-extractor |
| `read_p2_general_source_summary` | `general-source-summariser` | 1 | 1 | `general-source-summariser` | gold | general-source-summariser, paper-summariser, data-analysis-for-reporting, professor-email-reply, academic-admin-ops-failure-diagnoser |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, document-extractor, paper-summariser, writing-ops-resource-linker, multi-source-comparison-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `ml-ops-field-extractor` | wrong | ml-ops-field-extractor, bioinformatics-ops-field-extractor, recruiting-ops-field-extractor, analytics-ops-field-extractor, lab-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | 1 | 1 | `method-note-builder` | gold | method-note-builder, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner, research-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-huggingface-train-sentence-transformers, sentence-transformer-finetuner, public-addy-agent-performance-optimization, document-extractor |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `paper-summariser` | wrong | paper-summariser, method-note-builder, related-work-synthesiser, citation-note-extractor, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, general-source-summariser, paper-summariser, research-ops-comparison-builder, multi-source-comparison-builder |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, followup-reply-writer, email-drafter |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, document-rewriter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, followup-reply-writer, reply-drafter, professor-email-reply, reply-polisher |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 2 | 2 | `document-summariser` | wrong | document-summariser, followup-reply-writer, public-office-investment-memo, public-mattpocock-write-a-skill, public-oh-my-write-a-skill |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, implicit-review-comment-planner |
| `sec_p1_threat_model` | `security-threat-modeler` | 4 | 4 | `security-code-reviewer` | wrong | security-code-reviewer, privacy-risk-reviewer, auth-flow-reviewer, security-threat-modeler, public-openai-figma-create-new-file |
| `sec_p2_security_code_review` | `security-code-reviewer` | 2 | 2 | `auth-flow-reviewer` | wrong | auth-flow-reviewer, security-code-reviewer, security-threat-modeler, code-reviewer, pr-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, supply-chain-ops-dependency-mapper, supply-chain-ops-priority-ranker, supply-chain-ops-risk-reviewer, supply-chain-ops-resource-linker |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, public-huggingface-huggingface-papers, deployment-release-verifier, public-anthropic-internal-comms |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, email-polisher, email-drafter, email-ops-monitoring-plan-builder |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, public-swebench-similarity-search-patterns, email-polisher, product-ops-resource-linker, public-swebench-dbt-transformation-patterns |
| `skill_p1_find_existing` | `skill-finder` | 7 | 7 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, skill-creator, public-office-meeting-notes, skill-editor, meeting-agenda-builder |
| `skill_p2_install_existing` | `skill-installer` | 2 | 2 | `skill-packager` | wrong | skill-packager, skill-installer, implicit-hf-local-model-chooser, hf-local-model-selector, library-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-followup-extractor, meeting-notes-action-extractor, public-openai-figma-create-new-file, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, public-anthropic-skill-creator, skill-finder, skill-creator, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 6 | 6 | `reply-drafter` | wrong | reply-drafter, professor-email-reply, followup-reply-writer, reply-polisher, groupwork-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, paper-summariser, public-oh-my-research-paper-writing, public-huggingface-huggingface-papers, skill-installer-wrapper |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, gradio-demo-builder, skill-authoring-guide, public-addy-web-web-quality-audit, hr-ops-dependency-mapper |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 7 | 7 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-finder, skill-hierarchy-flattener |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, library-ops-intake-classifier, skill-field-auditor, library-ops-resource-linker, library-ops-compliance-checker |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-authoring-guide, hr-ops-resource-linker, skill-editor |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-packager, library-ops-resource-linker, public-skill-installer, public-oh-my-npm-git-install |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, resilience-pattern-reviewer, ci-failure-debugger, public-swebench-implementing-agent-modes, public-addy-web-core-web-vitals |

### `m6_bm25_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, api-documentation-writer, openapi-contract-tester, mcp-server-builder |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, api-integration-planner, rest-api-contract-designer, openapi-contract-tester, database-backup-planner |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, webhook-setup-planner, events-ops-timeline-builder, engineering-design-ops-timeline-builder |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, refactor-planner, public-addy-agent-api-and-interface-design, security-threat-modeler |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, migration-risk-auditor, deployment-rollback-planner, deployment-release-verifier, query-optimizer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | 1 | 1 | `service-dependency-mapper` | gold | service-dependency-mapper, distributed-trace-investigator, privacy-policy-drafter, privacy-risk-reviewer, architecture-boundary-reviewer |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, api-documentation-writer, mcp-server-builder, pr-review-comment-resolver |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, public-addy-agent-api-and-interface-design, api-design-reviewer, public-api-design-principles |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, events-ops-acceptance-test-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, secret-leak-scanner, dashboard-ops-acceptance-test-builder, webhook-setup-planner |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, openapi-contract-reviewer, rest-api-contract-designer, public-openai-cli-creator, skill-field-auditor |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-threat-modeler, api-ops-risk-reviewer, privacy-risk-reviewer, security-code-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, public-n-skills-dev-browser, public-mattpocock-triage |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, web-form-filler, public-n-skills-dev-browser, public-office-pdf-form-filler, dashboard-ops-field-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, dashboard-ops-acceptance-test-builder, docs-ops-acceptance-test-builder, ecommerce-ops-acceptance-test-builder, energy-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, product-ops-field-extractor, pdf-layout-table-extractor, product-ops-resource-linker, implicit-pdf-table-reconstructor |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, rest-api-contract-designer, implicit-browser-flow-investigator, debugging-root-cause-helper |
| `web_p6_accessibility_check` | `accessibility-checker` | 2 | 2 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, slo-breach-checker, layout-preserving-converter, reply-drafter |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, changelog-writer, release-note-writer, repo-code-reviewer, pr-review-comment-resolver |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, pr-review-comment-resolver, public-mattpocock-review, database-migration-risk-assessor |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, code-reviewer, pr-description-writer, implicit-review-comment-planner |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, public-addy-agent-debugging-and-error-recovery, frontend-debugger, auth-flow-integrator |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, public-oh-my-changelog-maintenance, public-swebench-changelog-automation |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, release-changelog-generator, public-oh-my-changelog-maintenance, public-office-changelog-generator, pr-description-writer |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, financial-report-writer, dashboard-ops-priority-ranker, dashboard-ops-handoff-brief-writer |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, implicit-ci-failure-reader, debugging-root-cause-helper, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, pdf-form-filler, accessibility-checker, github-issue-triager, compliance-ops-quality-auditor |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 2 | 2 | `metrics-root-cause-diagnoser` | wrong | metrics-root-cause-diagnoser, data-analysis-for-root-cause-diagnosis, variance-analysis-helper, web-performance-budget-checker, public-office-data-analysis |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, public-office-data-analysis, financial-report-writer, public-office-stock-analysis, news-briefing-writer |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, followup-reply-writer, capacity-risk-forecaster, frontend-debugger |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 1 | 1 | `data-analysis-for-ranking-selection` | gold | data-analysis-for-ranking-selection, decision-matrix-builder, meeting-notes-action-extractor, dashboard-ops-comparison-builder, risk-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, web-form-filler, frontend-debugger, web-ui-tester, implicit-browser-flow-investigator |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, implicit-visual-diff-reviewer, slide-deck-visual-auditor, changelog-writer, public-anthropic-canvas-design |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, metrics-overview, web-ui-tester, frontend-debugger |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | - | - | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, implicit-ci-failure-reader, metrics-root-cause-diagnoser, frontend-debugger, ci-failure-debugger |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-changelog-generator, public-openai-vercel-deploy, release-note-writer |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, review-comment-resolver, mobile-ops-acceptance-test-builder, mobile-ops-risk-reviewer, budget-planner |
| `doc_p1_document_summary` | `document-summariser` | 2 | 2 | `general-source-summariser` | wrong | general-source-summariser, document-summariser, citation-note-extractor, news-summariser, data-analysis-with-validation |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, public-docx, pdf-to-docx-converter, document-normaliser |
| `doc_p3_document_normaliser` | `document-normaliser` | 3 | 3 | `layout-preserving-converter` | wrong | layout-preserving-converter, pdf-to-docx-converter, document-normaliser, pdf-layout-reviewer, public-docx |
| `doc_p4_field_extraction` | `document-field-extractor` | 7 | 7 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, web-data-extractor, docs-ops-field-extractor, energy-ops-field-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, docx-redline-editor, decision-matrix-builder, public-docx, pdf-redaction-reviewer |
| `doc_p6_conversion` | `document-converter` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, document-converter, layout-preserving-converter, pdf-layout-reviewer, deck-template-applier |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, document-converter, pdf-layout-reviewer, pdf-layout-table-extractor, office-to-markdown-converter |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | - | - | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, frontend-debugger, ci-failure-debugger, metrics-root-cause-diagnoser, debugging-root-cause-helper |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, public-openai-security-best-practices, operations-ops-monitoring-plan-builder |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, pr-reviewer, security-code-reviewer, review-comment-resolver |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, public-mattpocock-triage, public-mattpocock-setup-matt-pocock-skills, public-mattpocock-to-issues, support-ticket-triager |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 4 | 4 | `review-comment-resolver` | wrong | review-comment-resolver, release-note-writer, pr-review-comment-resolver, release-changelog-generator, code-reviewer |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, public-mattpocock-git-guardrails-claude-code, public-mattpocock-triage, public-n-skills-open-source-maintainer, public-mattpocock-setup-matt-pocock-skills |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, gradio-demo-builder, pdf-layout-table-extractor, public-huggingface-datasets |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, implicit-hf-local-model-chooser, hf-dataset-viewer-inspector, public-huggingface-huggingface-local-models, public-huggingface-hf-cli |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, skill-hierarchy-flattener, agent-ops-monitoring-plan-builder, agent-ops-intake-classifier, skill-benchmark-evaluator |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, xlsx-formula-model-builder, sentence-transformer-finetuner, public-swebench-python-packaging, web-ops-rewrite-editor |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-hf-cli, database-migration-risk-assessor, public-huggingface-huggingface-llm-trainer |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, public-huggingface-hf-cli, sentence-transformer-finetuner, web-data-extractor |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, public-mattpocock-triage, service-mesh-traffic-debugger, public-swebench-slo-implementation, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 4 | 4 | `risk-ops-acceptance-test-builder` | wrong | risk-ops-acceptance-test-builder, metrics-overview, risk-ops-compliance-checker, slo-breach-checker, architecture-boundary-reviewer |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, data-analysis-for-forecasting, metrics-root-cause-diagnoser, risk-ops-risk-reviewer |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 1 | `metrics-root-cause-diagnoser` | gold | metrics-root-cause-diagnoser, service-dependency-mapper, metrics-overview, distributed-trace-investigator, ci-log-root-cause-debugger |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 1 | `incident-summary-writer` | gold | incident-summary-writer, data-analysis-for-reporting, metrics-overview, public-openai-linear, public-anthropic-internal-comms |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, general-source-summariser, tech-news-trend-extractor, news-theme-extractor, news-briefing-writer |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, metrics-overview, support-ops-ops-timeline-builder, public-mattpocock-edit-article |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 2 | 2 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, source-grounding-extractor, citation-note-extractor, document-summariser, document-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, public-anthropic-theme-factory |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, capacity-risk-forecaster |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, implicit-slo-alert-author, grafana-dashboard-builder, dashboard-ops-timeline-builder, dashboard-ops-acceptance-test-builder |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, dashboard-ops-monitoring-plan-builder, engineering-design-ops-monitoring-plan-builder, ux-ops-monitoring-plan-builder |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 4 | 4 | `latency-anomaly-detector` | wrong | latency-anomaly-detector, metrics-overview, public-swebench-service-mesh-observability, distributed-trace-investigator, meeting-scheduler |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, meeting-followup-extractor, incident-summary-writer, email-action-extractor, fundraising-ops-timeline-builder |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, pr-reviewer, risk-ops-risk-reviewer, public-swebench-python-resilience, research-ops-risk-reviewer |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, speaker-notes-writer, prometheus-alert-rule-writer, email-classification-router, skill-router-policy-designer |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-form-filler, pdf-layout-table-extractor, public-pdf, public-office-pdf-form-filler |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 2 | 2 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, public-pdf, pdf-question-answerer, pdf-layout-reviewer |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, pr-review-comment-resolver, review-comment-resolver, multi-document-comparison-preparer |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, web-ui-tester, data-analysis-with-validation, rag-failure-diagnoser, risk-ops-scenario-planner |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, customer-feedback-analyser, research-ops-rewrite-editor, vendor-ops-rewrite-editor, pdf-layout-reviewer |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, pdf-to-docx-converter, document-converter, public-docx |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, airtable-workflow-automator, public-office-airtable-automation, financial-model-builder |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, public-office-airtable-automation, public-office-slack-workflows, skill-authoring-guide, public-anthropic-slack-gif-creator |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, public-office-notion-automation, thesis-ops-rewrite-editor, thesis-ops-monitoring-plan-builder, thesis-ops-acceptance-test-builder |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 2 | 2 | `meeting-scheduler` | wrong | meeting-scheduler, calendar-scheduling-optimizer, meeting-ops-comparison-builder, meeting-notes-action-extractor, calendar-conflict-checker |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, email-action-extractor, meeting-followup-extractor, invoice-payment-checker, calendar-conflict-checker |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, email-ops-intake-classifier, email-ops-risk-reviewer, service-mesh-traffic-debugger, public-office-email-classifier |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, implicit-pdf-evidence-answerer, pdf-to-docx-converter, web-page-snapshotter, layout-preserving-converter |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, invoice-payment-checker, public-office-invoice-template, pdf-layout-reviewer |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 1 | 1 | `pdf-ocr-cleaner` | gold | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-layout-reviewer, pdf-layout-table-extractor, web-data-extractor |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-redaction-reviewer, compliance-checklist-builder |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, document-field-extractor, procurement-risk-summariser, public-openai-pdf, public-office-invoice-automation |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, layout-preserving-converter, pdf-question-answerer, office-to-markdown-converter, public-office-pdf-to-docx |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, meeting-ops-risk-reviewer, meeting-ops-failure-diagnoser |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer, meeting-ops-evidence-grounder, meeting-notes-action-extractor |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, followup-reply-writer, meeting-summary-writer, incident-summary-writer |
| `plan_p4_task_extractor` | `task-extractor` | 2 | 2 | `release-note-writer` | wrong | release-note-writer, task-extractor, weekly-planner, meeting-summary-writer, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-scheduler` | wrong | meeting-scheduler, meeting-agenda-builder, calendar-scheduling-optimizer, meeting-ops-acceptance-test-builder, public-openai-notion-meeting-intelligence |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, public-office-academic-search, research-ops-summary-writer, method-note-builder, academic-admin-ops-summary-writer |
| `read_p2_general_source_summary` | `general-source-summariser` | - | - | `paper-summariser` | wrong | paper-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, dashboard-ops-summary-writer, compliance-ops-summary-writer |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, note-tagger, writing-ops-evidence-grounder, writing-ops-resource-linker, writing-ops-artifact-packager |
| `read_p4_document_extraction` | `document-extractor` | 18 | 18 | `web-data-extractor` | wrong | web-data-extractor, pdf-layout-table-extractor, docs-ops-field-extractor, bioinformatics-ops-field-extractor, privacy-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `hf-community-eval-runner` | wrong | hf-community-eval-runner, pr-description-writer, journalism-ops-scenario-planner, docs-ops-scenario-planner, fundraising-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-addy-web-accessibility, agent-eval-coverage-auditor, public-addy-web-performance, public-mattpocock-writing-fragments |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `news-briefing-writer` | wrong | news-briefing-writer, pdf-layout-table-extractor, public-mattpocock-writing-shape, pdf-to-docx-converter, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, public-openai-notion-research-documentation, multi-document-comparison-preparer, release-note-writer, public-office-deep-research |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, followup-reply-writer, groupwork-reply, reply-polisher |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, followup-reply-writer, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, proposal-drafter, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, email-action-extractor, procurement-ops-handoff-brief-writer, journalism-ops-handoff-brief-writer, docs-ops-handoff-brief-writer |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply, groupwork-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, email-ops-scenario-planner, identity-ops-scenario-planner, public-brainstorming, security-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, accessibility-checker, api-security-threat-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | 1 | 1 | `dependency-risk-auditor` | gold | dependency-risk-auditor, deployment-build-triager, architecture-boundary-reviewer, risk-ops-risk-reviewer, pr-reviewer |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, pdf-redaction-reviewer, database-migration-risk-assessor, deployment-release-verifier, public-huggingface-huggingface-papers |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, email-classification-router, data-analysis-with-validation, email-polisher |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `release-note-writer` | wrong | release-note-writer, churn-risk-analyser, public-swebench-analytics-events, query-optimizer, public-office-web-search |
| `skill_p1_find_existing` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, meeting-notes-action-extractor, followup-reply-writer, meeting-followup-extractor, incident-summary-writer |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, skill-installer-wrapper, hf-community-eval-runner, hf-local-model-selector, library-ops-artifact-packager |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, skill-editor, skill-finder, public-skill-creator |
| `skill_p4_edit_existing` | `skill-editor` | 2 | 2 | `skill-field-auditor` | wrong | skill-field-auditor, skill-editor, docs-ops-field-extractor, agent-ops-field-extractor, skill-authoring-guide |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, agent-eval-coverage-auditor, skill-finder, reply-polisher, reply-drafter |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, skill-editor, agent-ops-resource-linker, skill-hierarchy-flattener |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, airtable-workflow-automator, gradio-demo-builder, skill-authoring-guide, skill-creator |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-hierarchy-flattener, skill-finder |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-creator, skill-hierarchy-flattener, skill-finder |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, skill-installer-wrapper, public-oh-my-agentic-skills |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, skill-installer, skill-finder, skill-editor, skill-hierarchy-flattener |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, public-obsidian-json-canvas |

### `m6_tfidf_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `api_p1_openapi_contract_review` | `openapi-contract-reviewer` | 1 | 1 | `openapi-contract-reviewer` | gold | openapi-contract-reviewer, rest-api-contract-designer, openapi-contract-tester, api-documentation-writer, mcp-server-builder |
| `api_p2_external_api_integration` | `external-api-integration-planner` | 1 | 1 | `external-api-integration-planner` | gold | external-api-integration-planner, rest-api-contract-designer, api-integration-planner, api-ops-acceptance-test-builder, public-swebench-add-admin-api-endpoint |
| `api_p3_webhook_contract` | `webhook-contract-planner` | 1 | 1 | `webhook-contract-planner` | gold | webhook-contract-planner, webhook-integration-planner, invoice-payment-checker, events-ops-timeline-builder, public-openai-winui-app |
| `api_p4_architecture_boundary` | `architecture-boundary-reviewer` | 1 | 1 | `architecture-boundary-reviewer` | gold | architecture-boundary-reviewer, public-architecture-patterns, security-threat-modeler, version-control-helper, public-addy-agent-api-and-interface-design |
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 | `database-migration-risk-assessor` | gold | database-migration-risk-assessor, deployment-rollback-planner, migration-risk-auditor, public-addy-agent-shipping-and-launch, risk-ops-risk-reviewer |
| `api_p6_service_dependency_map` | `service-dependency-mapper` | - | - | `analytics-ops-quality-auditor` | wrong | analytics-ops-quality-auditor, analytics-ops-evidence-grounder, public-office-microsoft-teams, analytics-ops-summary-writer, analytics-ops-risk-reviewer |
| `api_mcp_tooling_p1_rest_api_contract_designer` | `rest-api-contract-designer` | 1 | 1 | `rest-api-contract-designer` | gold | rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, api-documentation-writer, external-api-integration-planner |
| `api_mcp_tooling_p2_mcp_server_builder` | `mcp-server-builder` | 1 | 1 | `mcp-server-builder` | gold | mcp-server-builder, rest-api-contract-designer, api-design-reviewer, public-api-design-principles, public-addy-agent-api-and-interface-design |
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | 1 | 1 | `webhook-integration-planner` | gold | webhook-integration-planner, webhook-contract-planner, webhook-setup-planner, events-ops-timeline-builder, events-ops-monitoring-plan-builder |
| `api_mcp_tooling_p4_auth_flow_integrator` | `auth-flow-integrator` | 1 | 1 | `auth-flow-integrator` | gold | auth-flow-integrator, auth-flow-reviewer, dashboard-ops-acceptance-test-builder, webhook-setup-planner, dashboard-ops-compliance-checker |
| `api_mcp_tooling_p5_api_documentation_writer` | `api-documentation-writer` | 1 | 1 | `api-documentation-writer` | gold | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, openapi-contract-tester, contract-ops-artifact-packager |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 | `api-security-threat-reviewer` | gold | api-security-threat-reviewer, security-code-reviewer, security-threat-modeler, api-ops-risk-reviewer, privacy-risk-reviewer |
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, pdf-layout-reviewer, metrics-overview, accessibility-interaction-auditor, dashboard-ops-acceptance-test-builder |
| `web_p2_form_filling` | `web-form-filler` | 2 | 2 | `pdf-form-filler` | wrong | pdf-form-filler, web-form-filler, public-office-pdf-form-filler, real-estate-ops-field-extractor, financial-report-writer |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, variance-analysis-helper, web-page-snapshotter, docs-ops-acceptance-test-builder, compliance-ops-acceptance-test-builder |
| `web_p4_data_extraction` | `web-data-extractor` | - | - | `product-ops-field-extractor` | wrong | product-ops-field-extractor, product-ops-resource-linker, product-ops-scenario-planner, product-ops-comparison-builder, product-ops-intake-classifier |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-page-snapshotter, api-ops-evidence-grounder, rest-api-contract-designer, api-ops-field-extractor |
| `web_p6_accessibility_check` | `accessibility-checker` | 1 | 1 | `accessibility-checker` | gold | accessibility-checker, accessibility-interaction-auditor, layout-preserving-converter, pdf-form-filler, web-form-filler |
| `code_p1_local_code_review` | `code-reviewer` | 1 | 1 | `code-reviewer` | gold | code-reviewer, git-commit-writer, email-ops-acceptance-test-builder, email-ops-risk-reviewer, changelog-writer |
| `code_p2_pr_review` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, pr-description-writer, pr-review-comment-resolver, database-migration-risk-assessor, api-ops-acceptance-test-builder |
| `code_p3_review_comment_resolution` | `review-comment-resolver` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, pr-reviewer, code-reviewer |
| `code_p4_ci_failure_debugging` | `ci-failure-debugger` | 1 | 1 | `ci-failure-debugger` | gold | ci-failure-debugger, ci-log-root-cause-debugger, auth-flow-integrator, auth-flow-reviewer, git-commit-writer |
| `code_p5_changelog_entry` | `changelog-writer` | 1 | 1 | `changelog-writer` | gold | changelog-writer, release-note-writer, release-changelog-generator, public-swebench-changelog-automation, public-oh-my-changelog-maintenance |
| `code_p6_release_notes` | `release-note-writer` | 1 | 1 | `release-note-writer` | gold | release-note-writer, release-changelog-generator, public-oh-my-changelog-maintenance, public-office-changelog-generator, service-dependency-mapper |
| `data_p1_overview` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, data-analysis-for-forecasting, data-analysis-for-ranking-selection, spreadsheet-formula-auditor, citation-note-extractor |
| `data_p2_anomaly_focus` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, ci-log-root-cause-debugger, metrics-root-cause-diagnoser, debugging-root-cause-helper, latency-anomaly-detector |
| `data_p3_validation` | `data-analysis-with-validation` | 1 | 1 | `data-analysis-with-validation` | gold | data-analysis-with-validation, pdf-form-filler, public-addy-web-web-quality-audit, public-mattpocock-to-issues, public-addy-web-accessibility |
| `data_p4_root_cause` | `data-analysis-for-root-cause-diagnosis` | 1 | 1 | `data-analysis-for-root-cause-diagnosis` | gold | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, public-office-data-analysis, data-analysis-for-forecasting, dashboard-ops-evidence-grounder |
| `data_p5_reporting` | `data-analysis-for-reporting` | 1 | 1 | `data-analysis-for-reporting` | gold | data-analysis-for-reporting, dashboard-ops-handoff-brief-writer, geospatial-ops-handoff-brief-writer, data-analysis-overview, public-office-data-analysis |
| `data_p6_forecasting` | `data-analysis-for-forecasting` | 1 | 1 | `data-analysis-for-forecasting` | gold | data-analysis-for-forecasting, metrics-root-cause-diagnoser, capacity-risk-forecaster, data-analysis-for-root-cause-diagnosis, followup-reply-writer |
| `data_p7_ranking_selection` | `data-analysis-for-ranking-selection` | 2 | 2 | `decision-matrix-builder` | wrong | decision-matrix-builder, data-analysis-for-ranking-selection, meeting-notes-action-extractor, risk-ops-comparison-builder, dashboard-ops-comparison-builder |
| `deploy_p1_playwright_flow_debug` | `playwright-flow-debugger` | 1 | 1 | `playwright-flow-debugger` | gold | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, accessibility-interaction-auditor, auth-flow-integrator |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 1 | 1 | `visual-regression-checker` | gold | visual-regression-checker, slide-deck-visual-auditor, implicit-visual-diff-reviewer, review-comment-resolver, code-reviewer |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 1 | 1 | `accessibility-interaction-auditor` | gold | accessibility-interaction-auditor, accessibility-checker, public-addy-web-accessibility, metrics-overview, pdf-form-filler |
| `deploy_p4_build_log_triage` | `deployment-build-triager` | 5 | 5 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, implicit-ci-failure-reader, public-netlify-deploy, frontend-debugger, deployment-build-triager |
| `deploy_p5_release_verification` | `deployment-release-verifier` | 1 | 1 | `deployment-release-verifier` | gold | deployment-release-verifier, public-netlify-deploy, release-changelog-generator, release-note-writer, public-openai-vercel-deploy |
| `deploy_p6_performance_budget` | `web-performance-budget-checker` | 1 | 1 | `web-performance-budget-checker` | gold | web-performance-budget-checker, budget-planner, mobile-ops-acceptance-test-builder, mobile-ops-risk-reviewer, mobile-ops-evidence-grounder |
| `doc_p1_document_summary` | `document-summariser` | 1 | 1 | `document-summariser` | gold | document-summariser, general-source-summariser, citation-note-extractor, knowledge-base-article-writer, multi-document-comparison-preparer |
| `doc_p2_document_rewriter` | `document-rewriter` | 2 | 2 | `reply-polisher` | wrong | reply-polisher, document-rewriter, document-normaliser, document-converter, pdf-to-docx-converter |
| `doc_p3_document_normaliser` | `document-normaliser` | 2 | 2 | `layout-preserving-converter` | wrong | layout-preserving-converter, document-normaliser, pdf-to-docx-converter, deck-template-applier, pdf-layout-reviewer |
| `doc_p4_field_extraction` | `document-field-extractor` | 3 | 3 | `receipt-extractor` | wrong | receipt-extractor, invoice-payment-checker, document-field-extractor, pdf-layout-table-extractor, meeting-notes-action-extractor |
| `doc_p5_comparison_preparation` | `multi-document-comparison-preparer` | 1 | 1 | `multi-document-comparison-preparer` | gold | multi-document-comparison-preparer, decision-matrix-builder, docs-ops-comparison-builder, compliance-ops-comparison-builder, partnerships-ops-comparison-builder |
| `doc_p6_conversion` | `document-converter` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, document-converter, pdf-layout-reviewer, public-obsidian-defuddle |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | 1 | 1 | `layout-preserving-converter` | gold | layout-preserving-converter, office-to-markdown-converter, pdf-layout-reviewer, pdf-layout-table-extractor, document-converter |
| `github_ci_maintenance_p1_ci_log_root_cause_debugger` | `ci-log-root-cause-debugger` | 1 | 1 | `ci-log-root-cause-debugger` | gold | ci-log-root-cause-debugger, implicit-ci-failure-reader, ci-failure-debugger, frontend-debugger, metrics-root-cause-diagnoser |
| `github_ci_maintenance_p2_pr_review_comment_resolver` | `pr-review-comment-resolver` | 1 | 1 | `pr-review-comment-resolver` | gold | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, public-oh-my-code-review, public-addy-agent-code-review-and-quality |
| `github_ci_maintenance_p3_repo_code_reviewer` | `repo-code-reviewer` | 2 | 2 | `code-reviewer` | wrong | code-reviewer, repo-code-reviewer, public-oh-my-code-review, public-addy-agent-code-review-and-quality, ci-log-root-cause-debugger |
| `github_ci_maintenance_p4_github_issue_triager` | `github-issue-triager` | 1 | 1 | `github-issue-triager` | gold | github-issue-triager, public-mattpocock-triage, public-mattpocock-to-issues, public-mattpocock-setup-matt-pocock-skills, public-n-skills-open-source-maintainer |
| `github_ci_maintenance_p5_release_changelog_generator` | `release-changelog-generator` | 1 | 1 | `release-changelog-generator` | gold | release-changelog-generator, release-note-writer, review-comment-resolver, code-reviewer, pr-review-comment-resolver |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 | `git-safety-guardrail-installer` | gold | git-safety-guardrail-installer, public-mattpocock-git-guardrails-claude-code, public-mattpocock-triage, environment-config-auditor, public-mattpocock-setup-matt-pocock-skills |
| `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector` | `hf-dataset-viewer-inspector` | 1 | 1 | `hf-dataset-viewer-inspector` | gold | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-acceptance-test-builder, gradio-demo-builder, dataset-ops-intake-classifier |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | 1 | 1 | `hf-local-model-selector` | gold | hf-local-model-selector, implicit-hf-local-model-chooser, hf-dataset-viewer-inspector, public-huggingface-hf-cli, support-ticket-triager |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 | `sentence-transformer-finetuner` | gold | sentence-transformer-finetuner, agent-ops-monitoring-plan-builder, agent-ops-intake-classifier, agent-ops-scenario-planner, agent-ops-normalizer |
| `huggingface_ml_workflows_p4_gradio_demo_builder` | `gradio-demo-builder` | 1 | 1 | `gradio-demo-builder` | gold | gradio-demo-builder, web-ui-tester, sentence-transformer-finetuner, xlsx-formula-model-builder, web-ops-monitoring-plan-builder |
| `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer` | `hf-zerogpu-space-deployer` | 1 | 1 | `hf-zerogpu-space-deployer` | gold | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-hf-cli, public-huggingface-huggingface-papers, public-huggingface-huggingface-llm-trainer |
| `huggingface_ml_workflows_p6_hf_community_eval_runner` | `hf-community-eval-runner` | 1 | 1 | `hf-community-eval-runner` | gold | hf-community-eval-runner, hf-dataset-viewer-inspector, public-huggingface-hf-cli, dataset-ops-monitoring-plan-builder, gradio-demo-builder |
| `obs_p1_metrics_overview` | `metrics-overview` | 1 | 1 | `metrics-overview` | gold | metrics-overview, service-dependency-mapper, public-mattpocock-triage, service-mesh-traffic-debugger, public-swebench-service-mesh-observability |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 | `latency-anomaly-detector` | gold | latency-anomaly-detector, metrics-overview, data-analysis-with-anomaly-focus, web-performance-budget-checker, slo-breach-checker |
| `obs_p3_slo_breach` | `slo-breach-checker` | 6 | 6 | `risk-ops-risk-reviewer` | wrong | risk-ops-risk-reviewer, sre-ops-risk-reviewer, incident-ops-risk-reviewer, service-dependency-mapper, metrics-overview |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 1 | 1 | `capacity-risk-forecaster` | gold | capacity-risk-forecaster, slo-breach-checker, risk-ops-risk-reviewer, slo-breach-narrative-writer, metrics-root-cause-diagnoser |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 2 | 2 | `data-analysis-for-root-cause-diagnosis` | wrong | data-analysis-for-root-cause-diagnosis, metrics-root-cause-diagnoser, service-dependency-mapper, ci-log-root-cause-debugger, metrics-overview |
| `obs_p6_incident_summary` | `incident-summary-writer` | - | 5 | `incident-ops-normalizer` | wrong | incident-ops-normalizer, incident-ops-scenario-planner, incident-ops-timeline-builder, incident-ops-risk-reviewer, incident-ops-summary-writer |
| `news_p1_plain_summary` | `news-summariser` | 1 | 1 | `news-summariser` | gold | news-summariser, public-office-news-monitor, tech-news-trend-extractor, general-source-summariser, news-theme-extractor |
| `news_p2_briefing` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, knowledge-base-article-writer, support-ops-ops-timeline-builder, public-mattpocock-edit-article, support-ops-timeline-builder |
| `news_p3_grounded_claims` | `source-grounding-extractor` | 1 | 1 | `source-grounding-extractor` | gold | source-grounding-extractor, product-ops-evidence-grounder, knowledge-base-article-writer, product-ops-scenario-planner, document-field-extractor |
| `news_p4_theme_extraction` | `news-theme-extractor` | 1 | 1 | `news-theme-extractor` | gold | news-theme-extractor, tech-news-trend-extractor, data-analysis-for-forecasting, news-summariser, public-office-news-monitor |
| `news_p5_trend_signal` | `tech-news-trend-extractor` | 1 | 1 | `tech-news-trend-extractor` | gold | tech-news-trend-extractor, news-theme-extractor, news-briefing-writer, news-summariser, public-office-news-monitor |
| `observability_reliability_p1_prometheus_alert_rule_writer` | `prometheus-alert-rule-writer` | 1 | 1 | `prometheus-alert-rule-writer` | gold | prometheus-alert-rule-writer, implicit-slo-alert-author, grafana-dashboard-builder, dashboard-ops-risk-reviewer, dashboard-ops-timeline-builder |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 | `grafana-dashboard-builder` | gold | grafana-dashboard-builder, metrics-overview, dashboard-ops-monitoring-plan-builder, prometheus-alert-rule-writer, dashboard-ops-risk-reviewer |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 1 | 1 | `distributed-trace-investigator` | gold | distributed-trace-investigator, dashboard-ops-comparison-builder, implicit-trace-path-diagnoser, dashboard-ops-failure-diagnoser, dashboard-ops-normalizer |
| `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | 1 | 1 | `slo-breach-narrative-writer` | gold | slo-breach-narrative-writer, slo-breach-checker, meeting-followup-extractor, risk-ops-timeline-builder, compliance-ops-timeline-builder |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 | `resilience-pattern-reviewer` | gold | resilience-pattern-reviewer, public-oh-my-obsidian-cli-uri-fallback, public-swebench-python-resilience, skill-router-policy-designer, research-ops-scenario-planner |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 | `service-mesh-traffic-debugger` | gold | service-mesh-traffic-debugger, public-swebench-istio-traffic-management, speaker-notes-writer, public-swebench-linkerd-patterns, email-classification-router |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 1 | `pdf-layout-reviewer` | gold | pdf-layout-reviewer, pdf-layout-table-extractor, pdf-form-filler, public-office-pdf-form-filler, public-office-chat-with-pdf |
| `office_p2_scanned_pdf_ocr` | `pdf-ocr-extractor` | 1 | 1 | `pdf-ocr-extractor` | gold | pdf-ocr-extractor, pdf-ocr-cleaner, public-office-pdf-watermark, pdf-question-answerer, public-office-pdf-ocr |
| `office_p3_docx_redline` | `docx-redline-editor` | 1 | 1 | `docx-redline-editor` | gold | docx-redline-editor, public-docx, pr-review-comment-resolver, review-comment-resolver, pdf-to-docx-converter |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | 1 | 1 | `spreadsheet-formula-auditor` | gold | spreadsheet-formula-auditor, xlsx-formula-model-builder, distributed-trace-investigator, public-office-contract-review, public-swebench-langsmith-fetch |
| `office_p5_slide_visual_audit` | `slide-deck-visual-auditor` | 1 | 1 | `slide-deck-visual-auditor` | gold | slide-deck-visual-auditor, research-ops-rewrite-editor, vendor-ops-rewrite-editor, public-pptx, customer-feedback-analyser |
| `office_p6_office_to_markdown` | `office-to-markdown-converter` | 1 | 1 | `office-to-markdown-converter` | gold | office-to-markdown-converter, layout-preserving-converter, pdf-to-docx-converter, docx-redline-editor, pdf-layout-table-extractor |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 | `xlsx-formula-model-builder` | gold | xlsx-formula-model-builder, spreadsheet-formula-auditor, public-office-airtable-automation, airtable-workflow-automator, financial-model-builder |
| `office_business_automation_p2_airtable_workflow_automator` | `airtable-workflow-automator` | 1 | 1 | `airtable-workflow-automator` | gold | airtable-workflow-automator, public-office-airtable-automation, skill-authoring-guide, engineering-design-ops-field-extractor, public-office-slack-workflows |
| `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | 1 | 1 | `notion-research-database-builder` | gold | notion-research-database-builder, thesis-ops-rewrite-editor, public-office-notion-automation, thesis-ops-monitoring-plan-builder, thesis-ops-acceptance-test-builder |
| `office_business_automation_p4_calendar_scheduling_optimizer` | `calendar-scheduling-optimizer` | 1 | 1 | `calendar-scheduling-optimizer` | gold | calendar-scheduling-optimizer, meeting-ops-comparison-builder, meeting-scheduler, meeting-ops-field-extractor, meeting-ops-evidence-grounder |
| `office_business_automation_p5_meeting_notes_action_extractor` | `meeting-notes-action-extractor` | 1 | 1 | `meeting-notes-action-extractor` | gold | meeting-notes-action-extractor, calendar-conflict-checker, docs-ops-summary-writer, partnerships-ops-summary-writer, compliance-ops-summary-writer |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 | `email-classification-router` | gold | email-classification-router, risk-ops-risk-reviewer, risk-ops-intake-classifier, risk-ops-monitoring-plan-builder, service-mesh-traffic-debugger |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | 1 | 1 | `pdf-question-answerer` | gold | pdf-question-answerer, implicit-pdf-evidence-answerer, travel-ops-evidence-grounder, travel-ops-compliance-checker, travel-ops-failure-diagnoser |
| `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-layout-reviewer, public-office-chat-with-pdf |
| `pdf_document_operations_p3_pdf_ocr_cleaner` | `pdf-ocr-cleaner` | 2 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-question-answerer |
| `pdf_document_operations_p4_pdf_form_filler` | `pdf-form-filler` | 1 | 1 | `pdf-form-filler` | gold | pdf-form-filler, public-office-chat-with-pdf, public-addy-agent-shipping-and-launch, pdf-redaction-reviewer, pdf-question-answerer |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 | `pdf-redaction-reviewer` | gold | pdf-redaction-reviewer, vendor-ops-normalizer, pdf-question-answerer, vendor-ops-evidence-grounder, vendor-ops-risk-reviewer |
| `pdf_document_operations_p6_pdf_to_docx_converter` | `pdf-to-docx-converter` | 1 | 1 | `pdf-to-docx-converter` | gold | pdf-to-docx-converter, pdf-question-answerer, layout-preserving-converter, public-office-pdf-to-docx, public-office-chat-with-pdf |
| `plan_p1_meeting_agenda` | `meeting-agenda-builder` | 1 | 1 | `meeting-agenda-builder` | gold | meeting-agenda-builder, meeting-ops-risk-reviewer, meeting-ops-scenario-planner, meeting-ops-failure-diagnoser, meeting-ops-normalizer |
| `plan_p2_meeting_summary` | `meeting-summary-writer` | - | - | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-ops-summary-writer, meeting-ops-evidence-grounder, meeting-ops-field-extractor, meeting-ops-normalizer |
| `plan_p3_meeting_followup` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-notes-action-extractor, meeting-summary-writer, public-office-meeting-notes |
| `plan_p4_task_extractor` | `task-extractor` | 3 | 3 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, release-note-writer, task-extractor, meeting-summary-writer, meeting-followup-extractor |
| `plan_p5_weekly_planner` | `weekly-planner` | - | - | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-scheduler, meeting-ops-acceptance-test-builder, meeting-ops-summary-writer, meeting-ops-monitoring-plan-builder |
| `read_p1_paper_summary` | `paper-summariser` | 1 | 1 | `paper-summariser` | gold | paper-summariser, citation-note-extractor, research-ops-summary-writer, method-note-builder, public-office-academic-search |
| `read_p2_general_source_summary` | `general-source-summariser` | 2 | 2 | `paper-summariser` | wrong | paper-summariser, general-source-summariser, academic-admin-ops-summary-writer, operations-ops-summary-writer, professor-email-reply |
| `read_p3_citation_notes` | `citation-note-extractor` | 1 | 1 | `citation-note-extractor` | gold | citation-note-extractor, writing-ops-resource-linker, writing-ops-priority-ranker, note-tagger, writing-ops-acceptance-test-builder |
| `read_p4_document_extraction` | `document-extractor` | - | - | `research-ops-field-extractor` | wrong | research-ops-field-extractor, docs-ops-field-extractor, ml-ops-field-extractor, compliance-ops-field-extractor, partnerships-ops-field-extractor |
| `read_p5_method_notes` | `method-note-builder` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, compliance-ops-scenario-planner, docs-ops-scenario-planner, partnerships-ops-scenario-planner, events-ops-scenario-planner |
| `read_p6_grounding_check` | `citation-grounding-helper` | 1 | 1 | `citation-grounding-helper` | gold | citation-grounding-helper, public-huggingface-train-sentence-transformers, sentence-transformer-finetuner, support-ops-evidence-grounder, support-ops-ops-evidence-grounder |
| `read_p7_multi_source_comparison` | `multi-source-comparison-builder` | 5 | 5 | `method-note-builder` | wrong | method-note-builder, citation-note-extractor, related-work-synthesiser, release-note-writer, multi-source-comparison-builder |
| `read_p8_related_work_synthesis` | `related-work-synthesiser` | 1 | 1 | `related-work-synthesiser` | gold | related-work-synthesiser, research-ops-comparison-builder, release-note-writer, multi-source-comparison-builder, public-openai-notion-research-documentation |
| `reply_p1_professor_reply` | `professor-email-reply` | 1 | 1 | `professor-email-reply` | gold | professor-email-reply, reply-drafter, reply-polisher, email-polisher, groupwork-reply |
| `reply_p2_polish_supervisor` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, document-rewriter, reply-drafter, public-mattpocock-edit-article, email-polisher |
| `reply_p3_groupwork_coordination` | `groupwork-reply` | 1 | 1 | `groupwork-reply` | gold | groupwork-reply, reply-drafter, followup-reply-writer, reply-polisher, professor-email-reply |
| `reply_p4_followup_commitment` | `followup-reply-writer` | 1 | 1 | `followup-reply-writer` | gold | followup-reply-writer, document-summariser, public-office-investment-memo, email-action-extractor, public-oh-my-state-management |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | 1 | 1 | `reply-drafter` | gold | reply-drafter, reply-polisher, followup-reply-writer, public-openai-figma-create-new-file, professor-email-reply |
| `sec_p1_threat_model` | `security-threat-modeler` | 1 | 1 | `security-threat-modeler` | gold | security-threat-modeler, public-openai-figma-create-new-file, email-ops-scenario-planner, email-ops-risk-reviewer, risk-ops-scenario-planner |
| `sec_p2_security_code_review` | `security-code-reviewer` | 1 | 1 | `security-code-reviewer` | gold | security-code-reviewer, pr-reviewer, review-comment-resolver, api-ops-acceptance-test-builder, api-security-threat-reviewer |
| `sec_p3_dependency_risk` | `dependency-risk-auditor` | - | - | `supply-chain-ops-risk-reviewer` | wrong | supply-chain-ops-risk-reviewer, supply-chain-ops-dependency-mapper, supply-chain-ops-artifact-packager, supply-chain-ops-scenario-planner, supply-chain-ops-timeline-builder |
| `sec_p4_secret_leak` | `secret-leak-scanner` | 1 | 1 | `secret-leak-scanner` | gold | secret-leak-scanner, webhook-setup-planner, deployment-release-verifier, webhook-contract-planner, database-ops-normalizer |
| `sec_p5_auth_flow` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, auth-flow-integrator, email-ops-monitoring-plan-builder, email-ops-acceptance-test-builder, version-control-helper |
| `sec_p6_privacy_review` | `privacy-risk-reviewer` | - | - | `public-office-web-search` | wrong | public-office-web-search, product-ops-resource-linker, public-swebench-similarity-search-patterns, public-swebench-analytics-events, query-optimizer |
| `skill_p1_find_existing` | `skill-finder` | - | - | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, meeting-followup-extractor, meeting-ops-evidence-grounder, meeting-ops-comparison-builder, library-ops-comparison-builder |
| `skill_p2_install_existing` | `skill-installer` | 1 | 1 | `skill-installer` | gold | skill-installer, hf-local-model-selector, skill-installer-wrapper, library-ops-acceptance-test-builder, public-xlsx |
| `skill_p3_create_new` | `skill-creator` | 1 | 1 | `skill-creator` | gold | skill-creator, meeting-notes-action-extractor, meeting-followup-extractor, skill-editor, skill-finder |
| `skill_p4_edit_existing` | `skill-editor` | 1 | 1 | `skill-editor` | gold | skill-editor, skill-field-auditor, public-anthropic-skill-creator, agent-ops-field-extractor, docs-ops-field-extractor |
| `skill_p5_evaluate_existing` | `skill-evaluator` | 1 | 1 | `skill-evaluator` | gold | skill-evaluator, reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply |
| `skill_p6_package_existing` | `skill-packager` | 1 | 1 | `skill-packager` | gold | skill-packager, skill-installer-wrapper, paper-summariser, public-anthropic-skill-creator, agent-ops-resource-linker |
| `skill_representation_analysis_p1_skill_field_auditor` | `skill-field-auditor` | 1 | 1 | `skill-field-auditor` | gold | skill-field-auditor, gradio-demo-builder, airtable-workflow-automator, skill-creator, skill-editor |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-editor, skill-field-auditor, skill-finder, skill-hierarchy-flattener |
| `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | 1 | 1 | `skill-router-policy-designer` | gold | skill-router-policy-designer, skill-field-auditor, skill-finder, skill-creator, skill-installer |
| `skill_representation_analysis_p4_skill_hierarchy_flattener` | `skill-hierarchy-flattener` | 1 | 1 | `skill-hierarchy-flattener` | gold | skill-hierarchy-flattener, skill-creator, skill-editor, public-oh-my-write-a-skill, skill-authoring-guide |
| `skill_representation_analysis_p5_skill_installer_wrapper` | `skill-installer-wrapper` | 1 | 1 | `skill-installer-wrapper` | gold | skill-installer-wrapper, public-skill-installer, skill-installer, library-ops-resource-linker, public-vercel-find-skills |
| `skill_representation_analysis_p6_skill_benchmark_evaluator` | `skill-benchmark-evaluator` | 1 | 1 | `skill-benchmark-evaluator` | gold | skill-benchmark-evaluator, email-classification-router, pdf-redaction-reviewer, release-changelog-generator, public-obsidian-json-canvas |
