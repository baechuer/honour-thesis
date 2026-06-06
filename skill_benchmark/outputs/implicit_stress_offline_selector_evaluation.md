# Offline Selector Evaluation Report

This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.

## Scale Regimes

- `core`: 127 skills, approx selector-visible tokens per method vary by representation.
- `current_full`: 2401 skills, approx selector-visible tokens per method vary by representation.

## Method Summary

| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | `core` | 127 | 6915 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.000 | 0.000 | None | 80.0% | 0.0% | 17.27 |
| `m1_tfidf_flat` | `core` | 127 | 6915 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.000 | 0.000 | None | 70.0% | 0.0% | 1091.14 |
| `m3_tfidf_schema` | `core` | 127 | 44895 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.000 | 0.000 | None | 90.0% | 0.0% | 61.83 |
| `m6_bm25_schema_rerank` | `core` | 127 | 14338 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.000 | 0.000 | None | 80.0% | 0.0% | 38.4 |
| `m6_tfidf_schema_rerank` | `core` | 127 | 14338 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.000 | 0.000 | None | 90.0% | 0.0% | 29.64 |
| `m1_bm25_flat` | `current_full` | 2401 | 122537 | 70.0% | 70.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.850 | 0.850 | 1.3 | 20.0% | 70.0% | 284.66 |
| `m1_tfidf_flat` | `current_full` | 2401 | 122537 | 60.0% | 60.0% | 90.0% | 90.0% | 90.0% | 90.0% | 0.750 | 0.750 | 1.33 | 30.0% | 60.0% | 57.33 |
| `m3_tfidf_schema` | `current_full` | 2401 | 629119 | 20.0% | 20.0% | 90.0% | 90.0% | 90.0% | 90.0% | 0.533 | 0.533 | 1.89 | 70.0% | 20.0% | 234.55 |
| `m6_bm25_schema_rerank` | `current_full` | 2401 | 128533 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.467 | 0.467 | 2.2 | 80.0% | 0.0% | 306.22 |
| `m6_tfidf_schema_rerank` | `current_full` | 2401 | 128533 | 10.0% | 10.0% | 90.0% | 90.0% | 90.0% | 90.0% | 0.450 | 0.450 | 2.22 | 80.0% | 10.0% | 80.56 |

Accept metrics count documented acceptable alternatives as correct, while strict metrics require the controlled gold label.

## Benchmark Pressure Read

- `m1_bm25_flat` on `core`: possibly ambiguous or too noisy
- `m1_tfidf_flat` on `core`: possibly ambiguous or too noisy
- `m3_tfidf_schema` on `core`: possibly ambiguous or too noisy
- `m6_bm25_schema_rerank` on `core`: possibly ambiguous or too noisy
- `m6_tfidf_schema_rerank` on `core`: possibly ambiguous or too noisy
- `m1_bm25_flat` on `current_full`: useful pressure
- `m1_tfidf_flat` on `current_full`: useful pressure
- `m3_tfidf_schema` on `current_full`: useful pressure
- `m6_bm25_schema_rerank` on `current_full`: useful pressure; background distractors not yet competing
- `m6_tfidf_schema_rerank` on `current_full`: useful pressure

## Scale Sensitivity

This table compares the controlled core with the current full library. A useful scale condition should create some degradation or non-core false positives without making retrieval random.

| Method | Core Top-1 | Full Top-1 | Full Accept Top-1 | Top-1 Delta | Core Top-5 | Full Top-5 | Full Accept Top-5 | Top-5 Delta | Core MRR | Full MRR | Full Accept MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | 0.0% | 70.0% | 70.0% | +70.0% | 0.0% | 100.0% | 100.0% | +100.0% | 0.000 | 0.850 | 0.850 | 70.0% |
| `m1_tfidf_flat` | 0.0% | 60.0% | 60.0% | +60.0% | 0.0% | 90.0% | 90.0% | +90.0% | 0.000 | 0.750 | 0.750 | 60.0% |
| `m3_tfidf_schema` | 0.0% | 20.0% | 20.0% | +20.0% | 0.0% | 90.0% | 90.0% | +90.0% | 0.000 | 0.533 | 0.533 | 20.0% |
| `m6_bm25_schema_rerank` | 0.0% | 0.0% | 0.0% | +0.0% | 0.0% | 100.0% | 100.0% | +100.0% | 0.000 | 0.467 | 0.467 | 0.0% |
| `m6_tfidf_schema_rerank` | 0.0% | 10.0% | 10.0% | +10.0% | 0.0% | 90.0% | 90.0% | +90.0% | 0.000 | 0.450 | 0.450 | 10.0% |

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
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-question-answerer`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-failure-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m1_tfidf_flat` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-layout-reviewer`: 1
- `implicit-pdf-table-reconstructor -> pdf-layout-table-extractor`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-failure-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m3_tfidf_schema` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-layout-table-extractor`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-log-root-cause-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m6_bm25_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-question-answerer`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-failure-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m6_tfidf_schema_rerank` on `core`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-layout-table-extractor`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-log-root-cause-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m1_bm25_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 70.0% | 70.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-trace-path-diagnoser -> distributed-trace-investigator`: 1

### `m1_tfidf_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 60.0% | 60.0% | 90.0% | 90.0% | 90.0% | 90.0% |

Top confusions:
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1
- `implicit-slo-alert-author -> prometheus-alert-rule-writer`: 1

### `m3_tfidf_schema` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 20.0% | 20.0% | 90.0% | 90.0% | 90.0% | 90.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-layout-table-extractor`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-log-root-cause-debugger`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1
- `implicit-slo-alert-author -> prometheus-alert-rule-writer`: 1

### `m6_bm25_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-question-answerer`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-failure-debugger`: 1
- `implicit-review-comment-planner -> pr-review-comment-resolver`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1

### `m6_tfidf_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `implicit_field_stress` | 10 | 10.0% | 10.0% | 90.0% | 90.0% | 90.0% | 90.0% |

Top confusions:
- `implicit-pdf-evidence-answerer -> pdf-question-answerer`: 1
- `implicit-pdf-table-reconstructor -> pdf-layout-table-extractor`: 1
- `implicit-browser-flow-investigator -> playwright-flow-debugger`: 1
- `implicit-visual-diff-reviewer -> visual-regression-checker`: 1
- `implicit-ci-failure-reader -> ci-log-root-cause-debugger`: 1
- `implicit-hf-dataset-inspector -> hf-dataset-viewer-inspector`: 1
- `implicit-hf-local-model-chooser -> hf-local-model-selector`: 1
- `implicit-slo-alert-author -> prometheus-alert-rule-writer`: 1

## Prompt-Level Results

### `m1_bm25_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-reviewer, pdf-to-docx-converter, pdf-layout-table-extractor, pdf-redaction-reviewer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, web-data-extractor, pdf-layout-table-extractor, pdf-ocr-cleaner, pdf-ocr-extractor |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | - | - | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, web-performance-budget-checker, release-note-writer, web-form-filler |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, document-converter, news-theme-extractor, latency-anomaly-detector |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | - | - | `ci-failure-debugger` | wrong | ci-failure-debugger, frontend-debugger, ci-log-root-cause-debugger, api-documentation-writer, rest-api-contract-designer |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, reply-drafter, review-comment-resolver, followup-reply-writer, rest-api-contract-designer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | - | - | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, pdf-layout-table-extractor, gradio-demo-builder, mcp-server-builder, openapi-contract-reviewer |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | - | - | `hf-local-model-selector` | wrong | hf-local-model-selector, ci-failure-debugger, skill-installer-wrapper, skill-installer, xlsx-formula-model-builder |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | - | - | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, github-issue-triager, slo-breach-checker, skill-benchmark-evaluator, grafana-dashboard-builder |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, latency-anomaly-detector, news-theme-extractor, web-performance-budget-checker, hf-local-model-selector |

### `m1_tfidf_flat` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | - | - | `pdf-layout-reviewer` | wrong | pdf-layout-reviewer, pdf-layout-table-extractor, pdf-question-answerer, web-page-snapshotter, pdf-redaction-reviewer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | - | - | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer, pdf-question-answerer |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | - | - | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, web-performance-budget-checker, release-note-writer, data-analysis-for-root-cause-diagnosis |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, pdf-layout-table-extractor, document-converter, layout-preserving-converter |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | - | - | `ci-failure-debugger` | wrong | ci-failure-debugger, ci-log-root-cause-debugger, frontend-debugger, api-documentation-writer, openapi-contract-reviewer |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, meeting-summary-writer, code-reviewer, security-code-reviewer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | - | - | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, openapi-contract-reviewer, gradio-demo-builder, pdf-layout-table-extractor, sentence-transformer-finetuner |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | - | - | `hf-local-model-selector` | wrong | hf-local-model-selector, email-classification-router, ci-failure-debugger, skill-installer-wrapper, skill-installer |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | - | - | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, slo-breach-checker, slo-breach-narrative-writer, github-issue-triager, skill-benchmark-evaluator |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, latency-anomaly-detector, web-performance-budget-checker, hf-local-model-selector, meeting-followup-extractor |

### `m3_tfidf_schema` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-ocr-extractor, web-page-snapshotter |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | - | - | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-question-answerer, pdf-ocr-extractor, pdf-ocr-cleaner, pdf-layout-reviewer |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | - | - | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, ci-failure-debugger, web-performance-budget-checker, web-ui-tester |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-layout-reviewer, latency-anomaly-detector |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | - | - | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, deployment-build-triager, frontend-debugger, review-comment-resolver |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, code-reviewer, pr-reviewer, reply-drafter |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | - | - | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, pdf-layout-table-extractor, sentence-transformer-finetuner, github-issue-triager, openapi-contract-reviewer |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | - | - | `hf-local-model-selector` | wrong | hf-local-model-selector, email-classification-router, gradio-demo-builder, hf-dataset-viewer-inspector, sentence-transformer-finetuner |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | - | - | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, grafana-dashboard-builder, slo-breach-narrative-writer, github-issue-triager, slo-breach-checker |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, latency-anomaly-detector, web-performance-budget-checker, hf-local-model-selector, service-dependency-mapper |

### `m6_bm25_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-reviewer, pdf-layout-table-extractor, pdf-to-docx-converter, web-data-extractor |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, web-data-extractor, pdf-layout-table-extractor, pdf-ocr-extractor, pdf-ocr-cleaner |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | - | - | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, service-dependency-mapper, web-performance-budget-checker, pdf-question-answerer |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-layout-reviewer, document-converter |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | - | - | `ci-failure-debugger` | wrong | ci-failure-debugger, ci-log-root-cause-debugger, frontend-debugger, deployment-build-triager, rest-api-contract-designer |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, reply-drafter, followup-reply-writer, code-reviewer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | - | - | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, pdf-layout-table-extractor, mcp-server-builder, gradio-demo-builder, openapi-contract-reviewer |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | - | - | `hf-local-model-selector` | wrong | hf-local-model-selector, hf-community-eval-runner, xlsx-formula-model-builder, security-threat-modeler, ci-failure-debugger |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | - | - | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, github-issue-triager, skill-benchmark-evaluator, slo-breach-checker, grafana-dashboard-builder |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, latency-anomaly-detector, service-dependency-mapper, service-mesh-traffic-debugger, news-theme-extractor |

### `m6_tfidf_schema_rerank` on `core`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | - | - | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-reviewer, pdf-layout-table-extractor, web-page-snapshotter, pdf-redaction-reviewer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | - | - | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-question-answerer, pdf-ocr-extractor, pdf-ocr-cleaner, web-data-extractor |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | - | - | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, service-dependency-mapper, web-performance-budget-checker, pdf-question-answerer |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, web-page-snapshotter, pdf-layout-reviewer, pdf-layout-table-extractor |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | - | - | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, frontend-debugger, deployment-build-triager, rest-api-contract-designer |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, code-reviewer, reply-drafter, followup-reply-writer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | - | - | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, pdf-layout-table-extractor, openapi-contract-reviewer, gradio-demo-builder, mcp-server-builder |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | - | - | `hf-local-model-selector` | wrong | hf-local-model-selector, hf-community-eval-runner, xlsx-formula-model-builder, security-threat-modeler, email-classification-router |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | - | - | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, slo-breach-checker, github-issue-triager, skill-benchmark-evaluator, slo-breach-narrative-writer |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | - | - | `distributed-trace-investigator` | wrong | distributed-trace-investigator, latency-anomaly-detector, hf-local-model-selector, web-performance-budget-checker, news-theme-extractor |

### `m1_bm25_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 1 | 1 | `implicit-pdf-evidence-answerer` | gold | implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-question-answerer, pdf-layout-reviewer, pdf-to-docx-converter |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 1 | 1 | `implicit-pdf-table-reconstructor` | gold | implicit-pdf-table-reconstructor, implicit-pdf-evidence-answerer, pdf-question-answerer, public-office-invoice-template, web-data-extractor |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 2 | 2 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, implicit-browser-flow-investigator, frontend-debugger, public-security-threat-model, public-addy-agent-browser-testing-with-devtools |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, implicit-visual-diff-reviewer, public-openai-screenshot, slide-deck-visual-auditor, mobile-ops-comparison-builder |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 1 | 1 | `implicit-ci-failure-reader` | gold | implicit-ci-failure-reader, ci-failure-debugger, public-addy-agent-debugging-and-error-recovery, public-vercel-find-skills, frontend-debugger |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 1 | 1 | `implicit-review-comment-planner` | gold | implicit-review-comment-planner, pr-review-comment-resolver, reply-drafter, email-action-extractor, review-comment-resolver |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 1 | 1 | `implicit-hf-dataset-inspector` | gold | implicit-hf-dataset-inspector, hf-dataset-viewer-inspector, implicit-pdf-table-reconstructor, pdf-layout-table-extractor, gradio-demo-builder |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 1 | 1 | `implicit-hf-local-model-chooser` | gold | implicit-hf-local-model-chooser, hf-local-model-selector, public-oh-my-lmstudio-cli, public-huggingface-transformers-js, public-huggingface-huggingface-community-evals |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 1 | 1 | `implicit-slo-alert-author` | gold | implicit-slo-alert-author, prometheus-alert-rule-writer, github-issue-triager, public-openai-figma-create-design-system-rules, public-huggingface-huggingface-trackio |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, implicit-trace-path-diagnoser, public-swebench-service-mesh-observability, public-swebench-distributed-tracing, latency-anomaly-detector |

### `m1_tfidf_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 1 | 1 | `implicit-pdf-evidence-answerer` | gold | implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, travel-ops-failure-diagnoser, pdf-layout-reviewer, public-office-chat-with-pdf |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 1 | 1 | `implicit-pdf-table-reconstructor` | gold | implicit-pdf-table-reconstructor, pdf-layout-table-extractor, pdf-ocr-extractor, public-office-invoice-template, pdf-ocr-cleaner |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 2 | 2 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, implicit-browser-flow-investigator, public-skill-installer, frontend-debugger, public-addy-agent-browser-testing-with-devtools |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, slide-deck-visual-auditor, mobile-ops-rewrite-editor, mobile-ops-normalizer, mobile-ops-compliance-checker |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 1 | 1 | `implicit-ci-failure-reader` | gold | implicit-ci-failure-reader, ci-failure-debugger, ci-log-root-cause-debugger, public-oh-my-log-analysis, public-openai-gh-fix-ci |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 1 | 1 | `implicit-review-comment-planner` | gold | implicit-review-comment-planner, public-oh-my-code-review, email-thread-summariser, public-addy-agent-code-review-and-quality, public-openai-figma-code-connect-components |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 1 | 1 | `implicit-hf-dataset-inspector` | gold | implicit-hf-dataset-inspector, hf-dataset-viewer-inspector, dataset-ops-normalizer, dataset-ops-compliance-checker, dataset-ops-dependency-mapper |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `hf-local-model-selector` | wrong | hf-local-model-selector, implicit-hf-local-model-chooser, public-oh-my-lmstudio-cli, public-huggingface-transformers-js, public-huggingface-huggingface-community-evals |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 2 | 2 | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, implicit-slo-alert-author, public-openai-figma-create-design-system-rules, slo-breach-checker, github-issue-triager |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 1 | 1 | `implicit-trace-path-diagnoser` | gold | implicit-trace-path-diagnoser, distributed-trace-investigator, public-swebench-distributed-tracing, latency-anomaly-detector, public-swebench-service-mesh-observability |

### `m3_tfidf_schema` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, travel-ops-failure-diagnoser, pdf-layout-reviewer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 2 | 2 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-question-answerer, pdf-ocr-extractor, pdf-ocr-cleaner |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 3 | 3 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, public-skill-installer, web-ui-tester |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, mobile-ops-rewrite-editor, slide-deck-visual-auditor, mobile-ops-resource-linker, mobile-ops-priority-ranker |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 2 | 2 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, implicit-ci-failure-reader, ci-failure-debugger, deployment-build-triager, frontend-debugger |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 1 | 1 | `implicit-review-comment-planner` | gold | implicit-review-comment-planner, review-comment-resolver, pr-review-comment-resolver, public-addy-agent-code-review-and-quality, public-oh-my-code-review |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, pdf-layout-table-extractor, sentence-transformer-finetuner, dataset-ops-intake-classifier |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `hf-local-model-selector` | wrong | hf-local-model-selector, implicit-hf-local-model-chooser, public-oh-my-lmstudio-cli, support-ticket-triager, gradio-demo-builder |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 2 | 2 | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, implicit-slo-alert-author, grafana-dashboard-builder, slo-breach-narrative-writer, slo-breach-checker |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 1 | 1 | `implicit-trace-path-diagnoser` | gold | implicit-trace-path-diagnoser, distributed-trace-investigator, public-swebench-distributed-tracing, latency-anomaly-detector, public-swebench-service-mesh-observability |

### `m6_bm25_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 3 | 3 | `pdf-question-answerer` | wrong | pdf-question-answerer, pdf-layout-reviewer, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-layout-table-extractor |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, implicit-pdf-table-reconstructor, web-data-extractor, pdf-layout-table-extractor, pdf-ocr-extractor |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 3 | 3 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, web-performance-budget-checker, rag-failure-diagnoser |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, implicit-visual-diff-reviewer, mobile-ops-rewrite-editor, slide-deck-visual-auditor, mobile-ops-comparison-builder |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 2 | 2 | `ci-failure-debugger` | wrong | ci-failure-debugger, implicit-ci-failure-reader, ci-log-root-cause-debugger, frontend-debugger, sales-email-sequence-writer |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, implicit-review-comment-planner, review-comment-resolver, reply-drafter, followup-reply-writer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, mcp-server-builder |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `hf-local-model-selector` | wrong | hf-local-model-selector, implicit-hf-local-model-chooser, public-oh-my-lmstudio-cli, public-huggingface-transformers-js, public-huggingface-huggingface-community-evals |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 2 | 2 | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, implicit-slo-alert-author, github-issue-triager, skill-benchmark-evaluator, slo-breach-checker |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, implicit-trace-path-diagnoser, public-swebench-service-mesh-observability, latency-anomaly-detector, public-swebench-distributed-tracing |

### `m6_tfidf_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 2 | 2 | `pdf-question-answerer` | wrong | pdf-question-answerer, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-layout-reviewer, travel-ops-failure-diagnoser |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 3 | 3 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-question-answerer, implicit-pdf-table-reconstructor, pdf-ocr-extractor, pdf-ocr-cleaner |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 3 | 3 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, web-performance-budget-checker, compliance-ops-failure-diagnoser |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | - | - | `visual-regression-checker` | wrong | visual-regression-checker, mobile-ops-rewrite-editor, slide-deck-visual-auditor, mobile-ops-comparison-builder, mobile-ops-normalizer |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 3 | 3 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, implicit-ci-failure-reader, sales-email-sequence-writer, public-openai-gh-fix-ci |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 1 | 1 | `implicit-review-comment-planner` | gold | implicit-review-comment-planner, pr-review-comment-resolver, review-comment-resolver, public-addy-agent-code-review-and-quality, email-thread-summariser |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-normalizer, dataset-ops-comparison-builder, dataset-ops-intake-classifier |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `hf-local-model-selector` | wrong | hf-local-model-selector, implicit-hf-local-model-chooser, public-oh-my-lmstudio-cli, support-ticket-triager, public-huggingface-transformers-js |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 2 | 2 | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, implicit-slo-alert-author, slo-breach-checker, public-openai-figma-create-design-system-rules, github-issue-triager |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, implicit-trace-path-diagnoser, latency-anomaly-detector, public-swebench-distributed-tracing, public-swebench-service-mesh-observability |
