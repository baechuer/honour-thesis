# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (1006 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 33.3% |
| Acceptable top-1 accuracy | 41.7% |
| Top-3 recall | 41.7% |
| Top-5 recall | 50.0% |
| Acceptable top-5 recall | 58.3% |
| MRR | 0.408 |
| Non-main top-1 | 66.7% |
| Approx selector-visible tokens | 548397 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 1018
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 5
- Rerank cache hits: 7
- Approx uncached rerank input tokens: 51251

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, travel-ops-dependency-mapper, travel-ops-resource-linker, travel-ops-rewrite-editor, travel-ops-evidence-grounder |
| `low_doc_get_details` | `document-field-extractor` | - | 1 | `receipt-extractor` | acceptable | receipt-extractor, vendor-ops-field-extractor, finance-ops-artifact-packager, finance-ops-normalizer, finance-ops-handoff-brief-writer |
| `low_doc_clean_up` | `document-normaliser` | - | - | `web-ops-rewrite-editor` | wrong | web-ops-rewrite-editor, medical-admin-ops-rewrite-editor, operations-ops-normalizer, medical-admin-ops-summary-writer, medical-admin-ops-quality-auditor |
| `low_data_check_sheet` | `data-analysis-overview` | 1 | 1 | `data-analysis-overview` | gold | data-analysis-overview, dataset-ops-handoff-brief-writer, dataset-ops-summary-writer, data-analysis-for-root-cause-diagnosis, dataset-ops-timeline-builder |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | 2 | 2 | `dataset-ops-quality-auditor` | wrong | dataset-ops-quality-auditor, data-analysis-with-anomaly-focus, dataset-ops-risk-reviewer, dataset-ops-normalizer, data-analysis-for-root-cause-diagnosis |
| `low_code_check_change` | `pr-reviewer` | 13 | 13 | `version-control-helper` | wrong | version-control-helper, product-ops-quality-auditor, migration-risk-auditor, operations-ops-compliance-checker, product-ops-evidence-grounder |
| `low_code_red_build` | `ci-failure-debugger` | - | - | `ci-cd-pipeline-builder` | wrong | ci-cd-pipeline-builder, devops-ops-quality-auditor, devops-ops-evidence-grounder, devops-ops-artifact-packager, devops-ops-handoff-brief-writer |
| `low_news_catch_up` | `news-briefing-writer` | 1 | 1 | `news-briefing-writer` | gold | news-briefing-writer, news-summariser, tech-news-trend-extractor, general-source-summariser, media-ops-summary-writer |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 15 | 15 | `meeting-ops-normalizer` | wrong | meeting-ops-normalizer, meeting-ops-dependency-mapper, meeting-ops-summary-writer, meeting-ops-rewrite-editor, meeting-ops-artifact-packager |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, email-ops-rewrite-editor, personal-ops-rewrite-editor, email-ops-quality-auditor, support-ops-rewrite-editor |
| `low_security_login_risk` | `auth-flow-reviewer` | 4 | 4 | `web-ops-risk-reviewer` | wrong | web-ops-risk-reviewer, personal-ops-risk-reviewer, support-ops-risk-reviewer, auth-flow-reviewer, lab-ops-risk-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, agent-ops-resource-linker, agent-ops-intake-classifier, agent-ops-dependency-mapper, agent-ops-normalizer |
