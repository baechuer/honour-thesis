# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2401 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 50.0% |
| Acceptable top-1 accuracy | 50.0% |
| Top-3 recall | 90.0% |
| Top-5 recall | 90.0% |
| Acceptable top-5 recall | 90.0% |
| MRR | 0.691 |
| Non-main top-1 | 70.0% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 10
- Embedding cache hits: 2401
- Approx uncached embedding input tokens: 287
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | 13 | 13 | `travel-ops-evidence-grounder` | wrong | travel-ops-evidence-grounder, travel-ops-summary-writer, travel-ops-compliance-checker, travel-ops-risk-reviewer, travel-ops-handoff-brief-writer |
| `implicit_p2_pdf_table` | `implicit-pdf-table-reconstructor` | 2 | 2 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-question-answerer, implicit-pdf-evidence-answerer, pdf-ocr-extractor |
| `implicit_p3_browser_flow` | `implicit-browser-flow-investigator` | 1 | 1 | `implicit-browser-flow-investigator` | gold | implicit-browser-flow-investigator, ecommerce-ops-acceptance-test-builder, ecommerce-ops-compliance-checker, web-form-filler, web-ui-tester |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | 2 | 2 | `visual-regression-checker` | wrong | visual-regression-checker, implicit-visual-diff-reviewer, web-performance-budget-checker, web-page-snapshotter, implicit-browser-flow-investigator |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 3 | 3 | `ci-failure-debugger` | wrong | ci-failure-debugger, ci-log-root-cause-debugger, implicit-ci-failure-reader, review-comment-resolver, deployment-build-triager |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | 1 | 1 | `implicit-review-comment-planner` | gold | implicit-review-comment-planner, pr-review-comment-resolver, review-comment-resolver, code-reviewer, pr-reviewer |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | 1 | 1 | `implicit-hf-dataset-inspector` | gold | implicit-hf-dataset-inspector, hf-dataset-viewer-inspector, ml-ops-normalizer, dataset-ops-normalizer, dataset-ops-quality-auditor |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | 2 | 2 | `support-ticket-triager` | wrong | support-ticket-triager, implicit-hf-local-model-chooser, hf-local-model-selector, support-ops-intake-classifier, localization-ops-intake-classifier |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | 1 | 1 | `implicit-slo-alert-author` | gold | implicit-slo-alert-author, prometheus-alert-rule-writer, slo-breach-checker, sre-ops-monitoring-plan-builder, slo-breach-narrative-writer |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | 1 | 1 | `implicit-trace-path-diagnoser` | gold | implicit-trace-path-diagnoser, distributed-trace-investigator, resilience-pattern-reviewer, ecommerce-ops-monitoring-plan-builder, service-dependency-mapper |
