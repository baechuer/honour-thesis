# Offline Selector Evaluation Report

This report evaluates deterministic selector baselines over the benchmark prompts. It also records the M0 progressive-disclosure trace schema so later agent runs can be compared with the same metrics.

## Scale Regimes

- `current_full`: 1006 skills, approx selector-visible tokens per method vary by representation.

## Method Summary

| Method | Scale | Skills | Visible Tokens | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 | MRR | Accept MRR | Mean Rank | Listed Alt Top-1 | Non-Core Top-1 | Runtime ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `m1_bm25_flat` | `current_full` | 1006 | 50587 | 8.3% | 8.3% | 16.7% | 25.0% | 25.0% | 33.3% | 0.160 | 0.205 | 4.0 | 16.7% | 33.3% | 149.83 |
| `m1_tfidf_flat` | `current_full` | 1006 | 50587 | 0.0% | 0.0% | 16.7% | 25.0% | 33.3% | 33.3% | 0.111 | 0.146 | 3.25 | 16.7% | 66.7% | 1990.61 |
| `m2a_minilm_description` | `current_full` | 1006 | 50587 | 25.0% | 33.3% | 41.7% | 50.0% | 50.0% | 66.7% | 0.375 | 0.475 | 3.62 | 33.3% | 33.3% | 6334.5 |
| `m2b_minilm_full_skill` | `current_full` | 1006 | 497146 | 41.7% | 50.0% | 66.7% | 75.0% | 66.7% | 75.0% | 0.527 | 0.603 | 3.8 | 25.0% | 41.7% | 10695.38 |
| `m3_tfidf_schema` | `current_full` | 1006 | 303223 | 16.7% | 25.0% | 41.7% | 41.7% | 41.7% | 41.7% | 0.289 | 0.345 | 7.33 | 16.7% | 33.3% | 123.3 |
| `m6_bm25_schema_rerank` | `current_full` | 1006 | 56510 | 8.3% | 8.3% | 33.3% | 41.7% | 41.7% | 41.7% | 0.215 | 0.251 | 2.4 | 16.7% | 16.7% | 179.21 |
| `m6_tfidf_schema_rerank` | `current_full` | 1006 | 56510 | 8.3% | 8.3% | 16.7% | 25.0% | 33.3% | 33.3% | 0.163 | 0.195 | 3.0 | 16.7% | 41.7% | 61.93 |
| `m6_minilm_full_schema_rerank` | `current_full` | 1006 | 503069 | 33.3% | 33.3% | 58.3% | 66.7% | 66.7% | 66.7% | 0.470 | 0.504 | 3.6 | 25.0% | 25.0% | 10769.21 |

Accept metrics count documented acceptable alternatives as correct, while strict metrics require the controlled gold label.

## Benchmark Pressure Read

- `m1_bm25_flat` on `current_full`: possibly ambiguous or too noisy
- `m1_tfidf_flat` on `current_full`: possibly ambiguous or too noisy
- `m2a_minilm_description` on `current_full`: possibly ambiguous or too noisy
- `m2b_minilm_full_skill` on `current_full`: useful pressure
- `m3_tfidf_schema` on `current_full`: possibly ambiguous or too noisy
- `m6_bm25_schema_rerank` on `current_full`: possibly ambiguous or too noisy
- `m6_tfidf_schema_rerank` on `current_full`: possibly ambiguous or too noisy
- `m6_minilm_full_schema_rerank` on `current_full`: useful pressure

## Scale Sensitivity

This table compares the controlled core with the current full library. A useful scale condition should create some degradation or non-core false positives without making retrieval random.

| Method | Core Top-1 | Full Top-1 | Full Accept Top-1 | Top-1 Delta | Core Top-5 | Full Top-5 | Full Accept Top-5 | Top-5 Delta | Core MRR | Full MRR | Full Accept MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

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

### `m1_bm25_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_documents` | 3 | 0.0% | 0.0% | 33.3% | 33.3% | 33.3% | 33.3% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_reply` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> news-theme-extractor`: 1
- `document-field-extractor -> citation-note-extractor`: 1
- `document-normaliser -> changelog-writer`: 1
- `data-analysis-overview -> public-markitdown`: 1
- `data-analysis-with-anomaly-focus -> public-markitdown`: 1
- `pr-reviewer -> version-control-helper`: 1
- `ci-failure-debugger -> pr-description-writer`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1

### `m1_tfidf_flat` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_documents` | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_reply` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_skill_lifecycle` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> news-theme-extractor`: 1
- `document-field-extractor -> note-tagger`: 1
- `document-normaliser -> public-architecture-patterns`: 1
- `data-analysis-overview -> public-markitdown`: 1
- `data-analysis-with-anomaly-focus -> public-markitdown`: 1
- `pr-reviewer -> pr-description-writer`: 1
- `ci-failure-debugger -> knowledge-base-article-writer`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1

### `m2a_minilm_description` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.0% |
| `low_information_documents` | 3 | 0.0% | 33.3% | 33.3% | 66.7% | 33.3% | 66.7% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| `low_information_reply` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> travel-ops-compliance-checker`: 1
- `document-field-extractor -> receipt-extractor`: 1
- `document-normaliser -> document-rewriter`: 1
- `data-analysis-overview -> news-theme-extractor`: 1
- `data-analysis-with-anomaly-focus -> news-theme-extractor`: 1
- `pr-reviewer -> version-control-helper`: 1
- `ci-failure-debugger -> repo-ops-timeline-builder`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1

### `m2b_minilm_full_skill` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_documents` | 3 | 33.3% | 66.7% | 33.3% | 66.7% | 33.3% | 66.7% |
| `low_information_news` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_reply` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> travel-ops-compliance-checker`: 1
- `document-field-extractor -> receipt-extractor`: 1
- `data-analysis-overview -> dataset-ops-summary-writer`: 1
- `data-analysis-with-anomaly-focus -> dataset-ops-summary-writer`: 1
- `ci-failure-debugger -> public-skill-creator`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1
- `meeting-followup-extractor -> meeting-summary-writer`: 1

### `m3_tfidf_schema` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_documents` | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_news` | 1 | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_reply` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_skill_lifecycle` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Top confusions:
- `document-summariser -> capacity-risk-forecaster`: 1
- `document-field-extractor -> citation-note-extractor`: 1
- `document-normaliser -> public-architecture-patterns`: 1
- `data-analysis-overview -> dataset-ops-summary-writer`: 1
- `pr-reviewer -> pr-description-writer`: 1
- `ci-failure-debugger -> release-note-writer`: 1
- `news-briefing-writer -> news-summariser`: 1
- `meeting-followup-extractor -> meeting-agenda-builder`: 1

### `m6_bm25_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_documents` | 3 | 0.0% | 0.0% | 33.3% | 33.3% | 33.3% | 33.3% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_reply` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> news-theme-extractor`: 1
- `document-field-extractor -> citation-note-extractor`: 1
- `document-normaliser -> changelog-writer`: 1
- `data-analysis-overview -> public-markitdown`: 1
- `data-analysis-with-anomaly-focus -> citation-grounding-helper`: 1
- `pr-reviewer -> version-control-helper`: 1
- `ci-failure-debugger -> changelog-writer`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1

### `m6_tfidf_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_documents` | 3 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_reply` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> news-theme-extractor`: 1
- `document-field-extractor -> citation-note-extractor`: 1
- `document-normaliser -> changelog-writer`: 1
- `data-analysis-overview -> public-markitdown`: 1
- `data-analysis-with-anomaly-focus -> public-markitdown`: 1
- `pr-reviewer -> pr-description-writer`: 1
- `ci-failure-debugger -> changelog-writer`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1

### `m6_minilm_full_schema_rerank` on `current_full`

| Family | Total | Top-1 | Accept Top-1 | Top-3 | Accept Top-3 | Top-5 | Accept Top-5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `low_information_code` | 2 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |
| `low_information_data` | 2 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| `low_information_documents` | 3 | 33.3% | 33.3% | 66.7% | 66.7% | 66.7% | 66.7% |
| `low_information_news` | 1 | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% |
| `low_information_planning` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_reply` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_security` | 1 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| `low_information_skill_lifecycle` | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

Top confusions:
- `document-summariser -> travel-ops-compliance-checker`: 1
- `document-field-extractor -> document-summariser`: 1
- `data-analysis-overview -> dataset-ops-summary-writer`: 1
- `data-analysis-with-anomaly-focus -> dataset-ops-summary-writer`: 1
- `ci-failure-debugger -> changelog-writer`: 1
- `news-briefing-writer -> tech-news-trend-extractor`: 1
- `meeting-followup-extractor -> meeting-agenda-builder`: 1
- `auth-flow-reviewer -> code-reviewer`: 1

## Prompt-Level Results

### `m1_bm25_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `news-theme-extractor` | wrong | news-theme-extractor, tech-news-trend-extractor, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_doc_get_details` | `document-field-extractor` | - | 8 | `citation-note-extractor` | wrong | citation-note-extractor, note-tagger, social-post-planner, pr-description-writer, skill-packager |
| `low_doc_clean_up` | `document-normaliser` | 3 | 3 | `changelog-writer` | wrong | changelog-writer, public-architecture-patterns, document-normaliser, tech-news-trend-extractor, public-xlsx |
| `low_data_check_sheet` | `data-analysis-overview` | - | - | `public-markitdown` | wrong | public-markitdown, public-xlsx, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `public-markitdown` | wrong | public-markitdown, public-xlsx, citation-grounding-helper, contract-ops-compliance-checker, database-ops-compliance-checker |
| `low_code_check_change` | `pr-reviewer` | - | - | `version-control-helper` | wrong | version-control-helper, pr-description-writer, public-pdf, citation-grounding-helper, contract-ops-compliance-checker |
| `low_code_red_build` | `ci-failure-debugger` | - | 11 | `pr-description-writer` | wrong | pr-description-writer, release-note-writer, changelog-writer, chart-caption-writer, variance-analysis-helper |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, web-ui-tester |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 6 | 6 | `incident-summary-writer` | wrong | incident-summary-writer, citation-note-extractor, release-note-writer, meeting-agenda-builder, meeting-ops-handoff-brief-writer |
| `low_reply_make_better` | `reply-polisher` | 6 | 4 | `reply-drafter` | wrong | reply-drafter, followup-reply-writer, groupwork-reply, email-polisher, proposal-drafter |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `method-note-builder` | wrong | method-note-builder, multi-source-comparison-builder, research-ops-risk-reviewer, vendor-ops-risk-reviewer, pr-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, keyword-researcher, meeting-scheduler, public-skill-installer, public-skill-creator |

### `m1_tfidf_flat` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `news-theme-extractor` | wrong | news-theme-extractor, tech-news-trend-extractor, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_doc_get_details` | `document-field-extractor` | - | 6 | `note-tagger` | wrong | note-tagger, pr-description-writer, citation-note-extractor, social-post-planner, skill-packager |
| `low_doc_clean_up` | `document-normaliser` | - | - | `public-architecture-patterns` | wrong | public-architecture-patterns, version-control-helper, tech-news-trend-extractor, git-commit-writer, data-analysis-for-ranking-selection |
| `low_data_check_sheet` | `data-analysis-overview` | - | - | `public-markitdown` | wrong | public-markitdown, public-xlsx, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `public-markitdown` | wrong | public-markitdown, public-xlsx, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_code_check_change` | `pr-reviewer` | - | - | `pr-description-writer` | wrong | pr-description-writer, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator, agent-ops-acceptance-test-builder |
| `low_code_red_build` | `ci-failure-debugger` | 4 | 4 | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, ci-cd-pipeline-builder, pr-description-writer, ci-failure-debugger, infrastructure-as-code-planner |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, dependency-risk-auditor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | - | - | `meeting-ops-normalizer` | wrong | meeting-ops-normalizer, meeting-ops-compliance-checker, meeting-ops-dependency-mapper, meeting-ops-scenario-planner, meeting-ops-summary-writer |
| `low_reply_make_better` | `reply-polisher` | 2 | 2 | `reply-drafter` | wrong | reply-drafter, reply-polisher, followup-reply-writer, professor-email-reply, groupwork-reply |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `multi-source-comparison-builder` | wrong | multi-source-comparison-builder, method-note-builder, webhook-setup-planner, research-ops-scenario-planner, vendor-ops-scenario-planner |
| `low_skill_existing_help` | `skill-finder` | 3 | 3 | `public-skill-creator` | wrong | public-skill-creator, skill-editor, skill-finder, skill-installer, knowledge-base-article-writer |

### `m2a_minilm_description` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, policy-compliance-checker, privacy-policy-drafter, travel-ops-risk-reviewer, travel-ops-resource-linker |
| `low_doc_get_details` | `document-field-extractor` | - | 1 | `receipt-extractor` | acceptable | receipt-extractor, finance-ops-artifact-packager, operations-ops-artifact-packager, vendor-ops-artifact-packager, invoice-payment-checker |
| `low_doc_clean_up` | `document-normaliser` | 2 | 2 | `document-rewriter` | borderline | document-rewriter, document-normaliser, web-form-filler, document-converter, docs-ops-rewrite-editor |
| `low_data_check_sheet` | `data-analysis-overview` | - | - | `news-theme-extractor` | wrong | news-theme-extractor, news-summariser, tech-news-trend-extractor, latency-anomaly-detector, media-ops-failure-diagnoser |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | 5 | `news-theme-extractor` | wrong | news-theme-extractor, media-ops-failure-diagnoser, news-summariser, media-ops-intake-classifier, latency-anomaly-detector |
| `low_code_check_change` | `pr-reviewer` | 2 | 2 | `version-control-helper` | wrong | version-control-helper, pr-reviewer, community-ops-acceptance-test-builder, repo-ops-acceptance-test-builder, devops-ops-acceptance-test-builder |
| `low_code_red_build` | `ci-failure-debugger` | 12 | 12 | `repo-ops-timeline-builder` | wrong | repo-ops-timeline-builder, ci-cd-pipeline-builder, devops-ops-timeline-builder, public-playwright-interactive, ux-ops-timeline-builder |
| `low_news_catch_up` | `news-briefing-writer` | 6 | 6 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, web-ops-timeline-builder, media-ops-timeline-builder, media-ops-resource-linker, media-ops-monitoring-plan-builder |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 4 | 4 | `meeting-summary-writer` | borderline | meeting-summary-writer, meeting-agenda-builder, meeting-ops-rewrite-editor, meeting-followup-extractor, meeting-ops-summary-writer |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, email-polisher, professor-email-reply, followup-reply-writer |
| `low_security_login_risk` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, security-ops-risk-reviewer, migration-risk-auditor, ux-ops-risk-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, skill-editor, public-skill-creator, skill-installer |

### `m2b_minilm_full_skill` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, support-ops-compliance-checker, travel-ops-scenario-planner, legal-ops-compliance-checker, travel-ops-risk-reviewer |
| `low_doc_get_details` | `document-field-extractor` | 11 | 1 | `receipt-extractor` | acceptable | receipt-extractor, finance-ops-artifact-packager, support-ops-artifact-packager, invoice-payment-checker, vendor-ops-resource-linker |
| `low_doc_clean_up` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, document-rewriter, docs-ops-rewrite-editor, medical-admin-ops-rewrite-editor, document-converter |
| `low_data_check_sheet` | `data-analysis-overview` | 3 | 3 | `dataset-ops-summary-writer` | wrong | dataset-ops-summary-writer, dataset-ops-timeline-builder, data-analysis-overview, data-analysis-for-forecasting, dataset-ops-field-extractor |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `dataset-ops-summary-writer` | wrong | dataset-ops-summary-writer, dataset-ops-timeline-builder, public-writing-plans, dataset-ops-field-extractor, dataset-ops-risk-reviewer |
| `low_code_check_change` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, code-reviewer, ci-failure-debugger, version-control-helper, auth-flow-reviewer |
| `low_code_red_build` | `ci-failure-debugger` | 14 | 14 | `public-skill-creator` | wrong | public-skill-creator, devops-ops-evidence-grounder, public-playwright-interactive, frontend-debugger, changelog-writer |
| `low_news_catch_up` | `news-briefing-writer` | 2 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-briefing-writer, news-summariser, release-note-writer, news-theme-extractor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 3 | 3 | `meeting-summary-writer` | borderline | meeting-summary-writer, meeting-agenda-builder, meeting-followup-extractor, task-extractor, meeting-ops-rewrite-editor |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, professor-email-reply, reply-drafter, email-polisher, email-drafter |
| `low_security_login_risk` | `auth-flow-reviewer` | 1 | 1 | `auth-flow-reviewer` | gold | auth-flow-reviewer, privacy-risk-reviewer, secret-leak-scanner, dependency-risk-auditor, security-threat-modeler |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, skill-editor, skill-evaluator, skill-installer |

### `m3_tfidf_schema` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `capacity-risk-forecaster` | wrong | capacity-risk-forecaster, data-analysis-with-anomaly-focus, metrics-root-cause-diagnoser, news-theme-extractor, skill-finder |
| `low_doc_get_details` | `document-field-extractor` | 9 | 9 | `citation-note-extractor` | wrong | citation-note-extractor, repo-ops-summary-writer, pr-description-writer, context-compressor, note-tagger |
| `low_doc_clean_up` | `document-normaliser` | 13 | 13 | `public-architecture-patterns` | wrong | public-architecture-patterns, changelog-writer, data-analysis-for-root-cause-diagnosis, general-source-summariser, news-summariser |
| `low_data_check_sheet` | `data-analysis-overview` | 17 | 17 | `dataset-ops-summary-writer` | wrong | dataset-ops-summary-writer, dataset-ops-normalizer, dataset-ops-risk-reviewer, dataset-ops-evidence-grounder, dataset-ops-field-extractor |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | 1 | 1 | `data-analysis-with-anomaly-focus` | gold | data-analysis-with-anomaly-focus, data-analysis-for-root-cause-diagnosis, data-analysis-with-validation, data-analysis-for-forecasting, dataset-ops-summary-writer |
| `low_code_check_change` | `pr-reviewer` | 2 | 2 | `pr-description-writer` | wrong | pr-description-writer, pr-reviewer, data-analysis-with-validation, changelog-writer, accessibility-checker |
| `low_code_red_build` | `ci-failure-debugger` | 17 | 17 | `release-note-writer` | wrong | release-note-writer, changelog-writer, git-commit-writer, devops-ops-summary-writer, devops-ops-normalizer |
| `low_news_catch_up` | `news-briefing-writer` | 3 | 1 | `news-summariser` | acceptable | news-summariser, tech-news-trend-extractor, news-briefing-writer, news-theme-extractor, source-grounding-extractor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 3 | 3 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-summary-writer, meeting-followup-extractor, meeting-scheduler, meeting-ops-priority-ranker |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, followup-reply-writer, professor-email-reply, groupwork-reply |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `method-note-builder` | wrong | method-note-builder, webhook-setup-planner, research-ops-scenario-planner, vendor-ops-scenario-planner, docs-ops-scenario-planner |
| `low_skill_existing_help` | `skill-finder` | - | - | `knowledge-base-article-writer` | wrong | knowledge-base-article-writer, citation-note-extractor, data-analysis-overview, metrics-overview, incident-summary-writer |

### `m6_bm25_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `news-theme-extractor` | wrong | news-theme-extractor, tech-news-trend-extractor, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_doc_get_details` | `document-field-extractor` | - | 10 | `citation-note-extractor` | wrong | citation-note-extractor, pr-description-writer, document-summariser, note-tagger, multi-document-comparison-preparer |
| `low_doc_clean_up` | `document-normaliser` | 2 | 2 | `changelog-writer` | wrong | changelog-writer, document-normaliser, review-comment-resolver, data-analysis-for-root-cause-diagnosis, public-architecture-patterns |
| `low_data_check_sheet` | `data-analysis-overview` | - | - | `public-markitdown` | wrong | public-markitdown, agent-ops-quality-auditor, public-xlsx, agent-ops-normalizer, agent-ops-comparison-builder |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `citation-grounding-helper` | wrong | citation-grounding-helper, dataset-ops-compliance-checker, public-markitdown, contract-ops-compliance-checker, database-ops-compliance-checker |
| `low_code_check_change` | `pr-reviewer` | - | - | `version-control-helper` | wrong | version-control-helper, contract-ops-compliance-checker, database-ops-compliance-checker, docs-ops-compliance-checker, research-ops-compliance-checker |
| `low_code_red_build` | `ci-failure-debugger` | - | 13 | `changelog-writer` | wrong | changelog-writer, release-note-writer, pr-description-writer, review-comment-resolver, chart-caption-writer |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, dependency-risk-auditor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 3 | 3 | `incident-summary-writer` | wrong | incident-summary-writer, meeting-agenda-builder, meeting-followup-extractor, release-note-writer, citation-note-extractor |
| `low_reply_make_better` | `reply-polisher` | 2 | 2 | `reply-drafter` | wrong | reply-drafter, reply-polisher, followup-reply-writer, groupwork-reply, professor-email-reply |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `pr-reviewer` | wrong | pr-reviewer, research-ops-risk-reviewer, vendor-ops-risk-reviewer, method-note-builder, contract-ops-risk-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, skill-installer, skill-editor, public-skill-creator |

### `m6_tfidf_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `news-theme-extractor` | wrong | news-theme-extractor, tech-news-trend-extractor, accessibility-checker, agent-eval-coverage-auditor, agent-handoff-orchestrator |
| `low_doc_get_details` | `document-field-extractor` | - | 7 | `citation-note-extractor` | wrong | citation-note-extractor, pr-description-writer, document-summariser, note-tagger, social-post-planner |
| `low_doc_clean_up` | `document-normaliser` | - | - | `changelog-writer` | wrong | changelog-writer, data-analysis-for-root-cause-diagnosis, public-architecture-patterns, git-commit-writer, data-analysis-for-ranking-selection |
| `low_data_check_sheet` | `data-analysis-overview` | - | - | `public-markitdown` | wrong | public-markitdown, agent-ops-quality-auditor, public-xlsx, agent-ops-normalizer, agent-ops-comparison-builder |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `public-markitdown` | wrong | public-markitdown, accessibility-checker, agent-ops-compliance-checker, agent-ops-acceptance-test-builder, public-xlsx |
| `low_code_check_change` | `pr-reviewer` | - | - | `pr-description-writer` | wrong | pr-description-writer, accessibility-checker, agent-ops-compliance-checker, agent-ops-acceptance-test-builder, agent-ops-evidence-grounder |
| `low_code_red_build` | `ci-failure-debugger` | 5 | 5 | `changelog-writer` | wrong | changelog-writer, release-note-writer, review-comment-resolver, pr-description-writer, ci-failure-debugger |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, source-grounding-extractor |
| `low_meeting_next_steps` | `meeting-followup-extractor` | - | - | `meeting-ops-normalizer` | wrong | meeting-ops-normalizer, meeting-ops-field-extractor, meeting-ops-evidence-grounder, meeting-ops-resource-linker, meeting-ops-timeline-builder |
| `low_reply_make_better` | `reply-polisher` | 2 | 2 | `reply-drafter` | wrong | reply-drafter, reply-polisher, professor-email-reply, followup-reply-writer, groupwork-reply |
| `low_security_login_risk` | `auth-flow-reviewer` | - | - | `research-ops-scenario-planner` | wrong | research-ops-scenario-planner, vendor-ops-scenario-planner, method-note-builder, webhook-setup-planner, multi-source-comparison-builder |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-installer, skill-editor, skill-creator, public-skill-creator |

### `m6_minilm_full_schema_rerank` on `current_full`

| Prompt | Gold | Rank | Accept Rank | Top-1 | Top-1 Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `low_doc_understand_file` | `document-summariser` | - | - | `travel-ops-compliance-checker` | wrong | travel-ops-compliance-checker, support-ops-compliance-checker, travel-ops-scenario-planner, legal-ops-compliance-checker, travel-ops-risk-reviewer |
| `low_doc_get_details` | `document-field-extractor` | 3 | 2 | `document-summariser` | wrong | document-summariser, receipt-extractor, document-field-extractor, vendor-ops-summary-writer, release-note-writer |
| `low_doc_clean_up` | `document-normaliser` | 1 | 1 | `document-normaliser` | gold | document-normaliser, document-rewriter, web-form-filler, docs-ops-rewrite-editor, medical-admin-ops-rewrite-editor |
| `low_data_check_sheet` | `data-analysis-overview` | 7 | 7 | `dataset-ops-summary-writer` | wrong | dataset-ops-summary-writer, dataset-ops-timeline-builder, data-analysis-with-anomaly-focus, dataset-ops-field-extractor, dataset-ops-risk-reviewer |
| `low_data_something_off` | `data-analysis-with-anomaly-focus` | - | - | `dataset-ops-summary-writer` | wrong | dataset-ops-summary-writer, dataset-ops-timeline-builder, dataset-ops-evidence-grounder, dataset-ops-field-extractor, dataset-ops-risk-reviewer |
| `low_code_check_change` | `pr-reviewer` | 1 | 1 | `pr-reviewer` | gold | pr-reviewer, version-control-helper, ci-failure-debugger, code-reviewer, devops-ops-compliance-checker |
| `low_code_red_build` | `ci-failure-debugger` | 13 | 13 | `changelog-writer` | wrong | changelog-writer, devops-ops-evidence-grounder, release-note-writer, public-skill-creator, public-playwright-interactive |
| `low_news_catch_up` | `news-briefing-writer` | 4 | 2 | `tech-news-trend-extractor` | wrong | tech-news-trend-extractor, news-summariser, news-theme-extractor, news-briefing-writer, web-ops-priority-ranker |
| `low_meeting_next_steps` | `meeting-followup-extractor` | 2 | 2 | `meeting-agenda-builder` | wrong | meeting-agenda-builder, meeting-followup-extractor, meeting-summary-writer, meeting-ops-field-extractor, meeting-ops-summary-writer |
| `low_reply_make_better` | `reply-polisher` | 1 | 1 | `reply-polisher` | gold | reply-polisher, reply-drafter, professor-email-reply, followup-reply-writer, email-polisher |
| `low_security_login_risk` | `auth-flow-reviewer` | 3 | 3 | `code-reviewer` | wrong | code-reviewer, privacy-risk-reviewer, auth-flow-reviewer, dependency-risk-auditor, web-ops-risk-reviewer |
| `low_skill_existing_help` | `skill-finder` | 1 | 1 | `skill-finder` | gold | skill-finder, skill-creator, skill-editor, skill-installer, skill-evaluator |
