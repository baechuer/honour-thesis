# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2401 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 0.0% |
| Acceptable top-1 accuracy | 0.0% |
| Top-3 recall | 80.0% |
| Top-5 recall | 100.0% |
| Acceptable top-5 recall | 100.0% |
| MRR | 0.395 |
| Non-main top-1 | 0.0% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2411
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 5 | 5 | `pdf-question-answerer` | wrong | pdf-question-answerer, travel-ops-evidence-grounder, travel-ops-summary-writer, travel-ops-field-extractor, implicit-pdf-evidence-answerer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 4 | 4 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-question-answerer, pdf-ocr-extractor, implicit-pdf-table-reconstructor, pdf-ocr-cleaner |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 3 | 3 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, frontend-debugger, implicit-browser-flow-investigator, web-ui-tester, ecommerce-ops-failure-diagnoser |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, implicit-visual-diff-reviewer, web-page-snapshotter, mobile-ops-rewrite-editor, pdf-layout-reviewer |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 3 | 3 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, implicit-ci-failure-reader, deployment-build-triager, frontend-debugger |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 3 | 3 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, code-reviewer, pr-reviewer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-normalizer, ml-ops-normalizer, dataset-ops-intake-classifier |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `hf-local-model-selector` | wrong | hf-local-model-selector, implicit-hf-local-model-chooser, support-ticket-triager, support-ops-intake-classifier, localization-ops-intake-classifier |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 2 | 2 | `prometheus-alert-rule-writer` | wrong | prometheus-alert-rule-writer, implicit-slo-alert-author, slo-breach-checker, cloud-monitoring-configurer, sre-ops-risk-reviewer |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, implicit-trace-path-diagnoser, service-dependency-mapper, latency-anomaly-detector, resilience-pattern-reviewer |
