# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `core` (67 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 100.0% |
| Acceptable top-1 accuracy | 100.0% |
| Top-3 recall | 100.0% |
| Top-5 recall | 100.0% |
| Acceptable top-5 recall | 100.0% |
| MRR | 1.000 |
| Non-main top-1 | 0.0% |
| Approx selector-visible tokens | 84804 |

## API Usage Estimate

- Embedding API calls made in this run: 12
- Embedding cache hits: 0
- Approx uncached embedding input tokens: 31948
- Rerank API calls made in this run: 5
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 53156

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `web_p1_page_snapshot` | `web-page-snapshotter` | 1 | 1 | `web-page-snapshotter` | gold | web-page-snapshotter, frontend-debugger, web-ui-tester, web-data-extractor, web-form-filler |
| `web_p2_form_filling` | `web-form-filler` | 1 | 1 | `web-form-filler` | gold | web-form-filler, web-ui-tester, skill-evaluator, document-field-extractor, web-data-extractor |
| `web_p3_ui_test` | `web-ui-tester` | 1 | 1 | `web-ui-tester` | gold | web-ui-tester, web-form-filler, skill-evaluator, frontend-debugger, web-page-snapshotter |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 | `web-data-extractor` | gold | web-data-extractor, document-extractor, web-ui-tester, web-page-snapshotter, data-analysis-for-ranking-selection |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 | `frontend-debugger` | gold | frontend-debugger, web-ui-tester, web-page-snapshotter, web-form-filler, skill-editor |
