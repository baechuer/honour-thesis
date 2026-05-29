# Step 8 Candidate Readiness Report

Status: retrieval-readiness check only; downstream artifact generation has not been executed.

This report checks whether the planned Step 8 prompt sample has the gold or documented acceptable skill inside each selector's top-5 candidate set.

## Summary

| Method | Top-1 Gold/Accept | Top-5 Gold/Accept |
|---|---:|---:|
| M1 BM25 flat | 9/12 (75.0%) | 11/12 (91.7%) |
| M1 TF-IDF flat | 5/12 (41.7%) | 12/12 (100.0%) |
| M2b MiniLM full skill | 6/12 (50.0%) | 10/12 (83.3%) |
| M3 TF-IDF schema | 8/12 (66.7%) | 11/12 (91.7%) |
| M6 BM25 -> schema rerank | 9/12 (75.0%) | 11/12 (91.7%) |
| M6 TF-IDF -> schema rerank | 6/12 (50.0%) | 11/12 (91.7%) |
| M6 MiniLM full -> schema rerank | 10/12 (83.3%) | 11/12 (91.7%) |

## Prompt Details

| Prompt | Method | Gold/Accept Rank | Top-1 | Top-5 |
|---|---|---:|---|---|
| `reply_p2_polish_supervisor` | M1 BM25 flat | 1 | `reply-polisher` | `reply-polisher`, `document-rewriter`, `email-polisher`, `followup-reply-writer`, `reply-drafter` |
| `doc_p2_document_rewriter` | M1 BM25 flat | 3 | `public-docx` | `public-docx`, `reply-polisher`, `document-rewriter`, `web-form-filler`, `document-normaliser` |
| `doc_p4_field_extraction` | M1 BM25 flat | 4 | `receipt-extractor` | `receipt-extractor`, `invoice-payment-checker`, `web-data-extractor`, `document-field-extractor`, `meeting-followup-extractor` |
| `doc_p6_conversion` | M1 BM25 flat | 1 | `document-converter` | `document-converter`, `layout-preserving-converter`, `deck-template-applier`, `document-normaliser`, `public-docx` |
| `data_p3_validation` | M1 BM25 flat | 1 | `data-analysis-with-validation` | `data-analysis-with-validation`, `accessibility-checker`, `data-analysis-with-anomaly-focus`, `slo-breach-checker`, `public-huggingface-datasets` |
| `obs_p5_root_cause` | M1 BM25 flat | 1 | `metrics-root-cause-diagnoser` | `metrics-root-cause-diagnoser`, `metrics-overview`, `capacity-risk-forecaster`, `rag-failure-diagnoser`, `latency-anomaly-detector` |
| `news_p2_briefing` | M1 BM25 flat | 1 | `news-briefing-writer` | `news-briefing-writer`, `knowledge-base-article-writer`, `metrics-overview`, `email-thread-summariser`, `data-analysis-for-reporting` |
| `read_p2_general_source_summary` | M1 BM25 flat | - | `paper-summariser` | `paper-summariser`, `operations-ops-summary-writer`, `dashboard-ops-summary-writer`, `professor-email-reply`, `email-drafter` |
| `read_p7_multi_source_comparison` | M1 BM25 flat | 1 | `multi-source-comparison-builder` | `multi-source-comparison-builder`, `news-briefing-writer`, `note-tagger`, `data-analysis-for-ranking-selection`, `tech-news-trend-extractor` |
| `sec_p2_security_code_review` | M1 BM25 flat | 1 | `security-code-reviewer` | `security-code-reviewer`, `review-comment-resolver`, `accessibility-checker`, `metrics-overview`, `api-ops-acceptance-test-builder` |
| `skill_p4_edit_existing` | M1 BM25 flat | 1 | `skill-editor` | `skill-editor`, `skill-evaluator`, `docs-ops-field-extractor`, `agent-ops-field-extractor`, `data-analysis-overview` |
| `skill_p6_package_existing` | M1 BM25 flat | 1 | `skill-packager` | `skill-packager`, `agent-ops-resource-linker`, `skill-editor`, `skill-finder`, `public-skill-creator` |
| `reply_p2_polish_supervisor` | M1 TF-IDF flat | 1 | `reply-polisher` | `reply-polisher`, `reply-drafter`, `document-rewriter`, `email-polisher`, `deck-template-applier` |
| `doc_p2_document_rewriter` | M1 TF-IDF flat | 2 | `reply-polisher` | `reply-polisher`, `document-rewriter`, `document-normaliser`, `document-converter`, `document-summariser` |
| `doc_p4_field_extraction` | M1 TF-IDF flat | 4 | `receipt-extractor` | `receipt-extractor`, `invoice-payment-checker`, `meeting-followup-extractor`, `document-field-extractor`, `deadline-reminder-planner` |
| `doc_p6_conversion` | M1 TF-IDF flat | 2 | `layout-preserving-converter` | `layout-preserving-converter`, `document-converter`, `deck-template-applier`, `public-markitdown`, `repo-ops-evidence-grounder` |
| `data_p3_validation` | M1 TF-IDF flat | 2 | `public-huggingface-datasets` | `public-huggingface-datasets`, `data-analysis-with-validation`, `accessibility-checker`, `market-opportunity-assessor`, `public-xlsx` |
| `obs_p5_root_cause` | M1 TF-IDF flat | 2 | `data-analysis-for-root-cause-diagnosis` | `data-analysis-for-root-cause-diagnosis`, `metrics-root-cause-diagnoser`, `debugging-root-cause-helper`, `metrics-overview`, `latency-anomaly-detector` |
| `news_p2_briefing` | M1 TF-IDF flat | 1 | `news-briefing-writer` | `news-briefing-writer`, `knowledge-base-article-writer`, `support-ticket-triager`, `support-ops-timeline-builder`, `support-ops-comparison-builder` |
| `read_p2_general_source_summary` | M1 TF-IDF flat | 3 | `paper-summariser` | `paper-summariser`, `professor-email-reply`, `general-source-summariser`, `operations-ops-summary-writer`, `research-ops-summary-writer` |
| `read_p7_multi_source_comparison` | M1 TF-IDF flat | 2 | `related-work-synthesiser` | `related-work-synthesiser`, `multi-source-comparison-builder`, `decision-matrix-builder`, `receipt-extractor`, `competitive-battlecard-builder` |
| `sec_p2_security_code_review` | M1 TF-IDF flat | 1 | `security-code-reviewer` | `security-code-reviewer`, `pr-reviewer`, `code-reviewer`, `review-comment-resolver`, `api-ops-acceptance-test-builder` |
| `skill_p4_edit_existing` | M1 TF-IDF flat | 1 | `skill-editor` | `skill-editor`, `skill-finder`, `skill-installer`, `public-skill-creator`, `skill-packager` |
| `skill_p6_package_existing` | M1 TF-IDF flat | 1 | `skill-packager` | `skill-packager`, `paper-summariser`, `skill-installer`, `public-skill-creator`, `agent-ops-resource-linker` |
| `reply_p2_polish_supervisor` | M2b MiniLM full skill | 1 | `reply-polisher` | `reply-polisher`, `email-ops-rewrite-editor`, `email-polisher`, `reply-drafter`, `support-ops-rewrite-editor` |
| `doc_p2_document_rewriter` | M2b MiniLM full skill | 1 | `document-rewriter` | `document-rewriter`, `travel-ops-rewrite-editor`, `document-converter`, `travel-ops-summary-writer`, `document-normaliser` |
| `doc_p4_field_extraction` | M2b MiniLM full skill | 1 | `document-field-extractor` | `document-field-extractor`, `receipt-extractor`, `finance-ops-field-extractor`, `vendor-ops-field-extractor`, `vendor-ops-summary-writer` |
| `doc_p6_conversion` | M2b MiniLM full skill | 1 | `document-converter` | `document-converter`, `document-normaliser`, `public-markitdown`, `layout-preserving-converter`, `document-rewriter` |
| `data_p3_validation` | M2b MiniLM full skill | 2 | `data-analysis-with-anomaly-focus` | `data-analysis-with-anomaly-focus`, `data-analysis-with-validation`, `latency-anomaly-detector`, `dataset-ops-quality-auditor`, `data-analysis-overview` |
| `obs_p5_root_cause` | M2b MiniLM full skill | - | `latency-anomaly-detector` | `latency-anomaly-detector`, `metrics-overview`, `slo-breach-checker`, `support-ops-failure-diagnoser`, `capacity-risk-forecaster` |
| `news_p2_briefing` | M2b MiniLM full skill | 1 | `news-briefing-writer` | `news-briefing-writer`, `news-summariser`, `meeting-summary-writer`, `events-ops-summary-writer`, `meeting-followup-extractor` |
| `read_p2_general_source_summary` | M2b MiniLM full skill | 1 | `general-source-summariser` | `general-source-summariser`, `document-extractor`, `source-grounding-extractor`, `paper-summariser`, `method-note-builder` |
| `read_p7_multi_source_comparison` | M2b MiniLM full skill | 2 | `related-work-synthesiser` | `related-work-synthesiser`, `multi-source-comparison-builder`, `paper-summariser`, `general-source-summariser`, `method-note-builder` |
| `sec_p2_security_code_review` | M2b MiniLM full skill | 4 | `auth-flow-reviewer` | `auth-flow-reviewer`, `frontend-debugger`, `web-ui-tester`, `security-code-reviewer`, `secret-leak-scanner` |
| `skill_p4_edit_existing` | M2b MiniLM full skill | - | `writing-ops-field-extractor` | `writing-ops-field-extractor`, `docs-ops-field-extractor`, `document-field-extractor`, `thesis-ops-field-extractor`, `knowledge-ops-field-extractor` |
| `skill_p6_package_existing` | M2b MiniLM full skill | 3 | `paper-summariser` | `paper-summariser`, `general-source-summariser`, `skill-packager`, `public-pdf`, `document-summariser` |
| `reply_p2_polish_supervisor` | M3 TF-IDF schema | 1 | `reply-polisher` | `reply-polisher`, `reply-drafter`, `document-rewriter`, `email-polisher`, `professor-email-reply` |
| `doc_p2_document_rewriter` | M3 TF-IDF schema | 1 | `document-rewriter` | `document-rewriter`, `reply-polisher`, `email-polisher`, `document-normaliser`, `document-converter` |
| `doc_p4_field_extraction` | M3 TF-IDF schema | - | `invoice-payment-checker` | `invoice-payment-checker`, `receipt-extractor`, `finance-ops-field-extractor`, `ml-ops-field-extractor`, `recruiting-ops-field-extractor` |
| `doc_p6_conversion` | M3 TF-IDF schema | 1 | `document-converter` | `document-converter`, `layout-preserving-converter`, `document-normaliser`, `deck-template-applier`, `slide-outline-builder` |
| `data_p3_validation` | M3 TF-IDF schema | 1 | `data-analysis-with-validation` | `data-analysis-with-validation`, `lab-ops-quality-auditor`, `data-analysis-for-ranking-selection`, `lab-ops-normalizer`, `data-analysis-with-anomaly-focus` |
| `obs_p5_root_cause` | M3 TF-IDF schema | 1 | `metrics-root-cause-diagnoser` | `metrics-root-cause-diagnoser`, `latency-anomaly-detector`, `data-analysis-for-root-cause-diagnosis`, `capacity-risk-forecaster`, `metrics-overview` |
| `news_p2_briefing` | M3 TF-IDF schema | 2 | `news-summariser` | `news-summariser`, `news-briefing-writer`, `knowledge-base-article-writer`, `news-theme-extractor`, `support-ops-monitoring-plan-builder` |
| `read_p2_general_source_summary` | M3 TF-IDF schema | 1 | `general-source-summariser` | `general-source-summariser`, `paper-summariser`, `data-analysis-for-reporting`, `professor-email-reply`, `document-summariser` |
| `read_p7_multi_source_comparison` | M3 TF-IDF schema | 5 | `paper-summariser` | `paper-summariser`, `related-work-synthesiser`, `method-note-builder`, `data-analysis-for-ranking-selection`, `multi-source-comparison-builder` |
| `sec_p2_security_code_review` | M3 TF-IDF schema | 2 | `auth-flow-reviewer` | `auth-flow-reviewer`, `security-code-reviewer`, `security-threat-modeler`, `code-reviewer`, `pr-reviewer` |
| `skill_p4_edit_existing` | M3 TF-IDF schema | 1 | `skill-editor` | `skill-editor`, `skill-finder`, `skill-creator`, `skill-evaluator`, `docs-ops-field-extractor` |
| `skill_p6_package_existing` | M3 TF-IDF schema | 1 | `skill-packager` | `skill-packager`, `paper-summariser`, `docs-ops-resource-linker`, `public-skill-creator`, `agent-ops-resource-linker` |
| `reply_p2_polish_supervisor` | M6 BM25 -> schema rerank | 1 | `reply-polisher` | `reply-polisher`, `document-rewriter`, `reply-drafter`, `followup-reply-writer`, `email-polisher` |
| `doc_p2_document_rewriter` | M6 BM25 -> schema rerank | 1 | `document-rewriter` | `document-rewriter`, `reply-polisher`, `public-docx`, `document-normaliser`, `layout-preserving-converter` |
| `doc_p4_field_extraction` | M6 BM25 -> schema rerank | 5 | `receipt-extractor` | `receipt-extractor`, `invoice-payment-checker`, `web-data-extractor`, `docs-ops-field-extractor`, `document-field-extractor` |
| `doc_p6_conversion` | M6 BM25 -> schema rerank | 1 | `document-converter` | `document-converter`, `layout-preserving-converter`, `deck-template-applier`, `document-normaliser`, `note-tagger` |
| `data_p3_validation` | M6 BM25 -> schema rerank | 1 | `data-analysis-with-validation` | `data-analysis-with-validation`, `accessibility-checker`, `data-analysis-with-anomaly-focus`, `research-ops-quality-auditor`, `docs-ops-quality-auditor` |
| `obs_p5_root_cause` | M6 BM25 -> schema rerank | 1 | `metrics-root-cause-diagnoser` | `metrics-root-cause-diagnoser`, `data-analysis-for-root-cause-diagnosis`, `metrics-overview`, `latency-anomaly-detector`, `data-analysis-with-validation` |
| `news_p2_briefing` | M6 BM25 -> schema rerank | 1 | `news-briefing-writer` | `news-briefing-writer`, `knowledge-base-article-writer`, `metrics-overview`, `support-ops-timeline-builder`, `data-analysis-for-reporting` |
| `read_p2_general_source_summary` | M6 BM25 -> schema rerank | - | `paper-summariser` | `paper-summariser`, `operations-ops-summary-writer`, `dashboard-ops-summary-writer`, `research-ops-summary-writer`, `web-ops-summary-writer` |
| `read_p7_multi_source_comparison` | M6 BM25 -> schema rerank | 2 | `news-briefing-writer` | `news-briefing-writer`, `multi-source-comparison-builder`, `data-analysis-for-ranking-selection`, `note-tagger`, `related-work-synthesiser` |
| `sec_p2_security_code_review` | M6 BM25 -> schema rerank | 1 | `security-code-reviewer` | `security-code-reviewer`, `pr-reviewer`, `review-comment-resolver`, `accessibility-checker`, `api-ops-acceptance-test-builder` |
| `skill_p4_edit_existing` | M6 BM25 -> schema rerank | 1 | `skill-editor` | `skill-editor`, `docs-ops-field-extractor`, `agent-ops-field-extractor`, `document-field-extractor`, `skill-evaluator` |
| `skill_p6_package_existing` | M6 BM25 -> schema rerank | 1 | `skill-packager` | `skill-packager`, `skill-editor`, `agent-ops-resource-linker`, `skill-finder`, `hr-ops-resource-linker` |
| `reply_p2_polish_supervisor` | M6 TF-IDF -> schema rerank | 1 | `reply-polisher` | `reply-polisher`, `document-rewriter`, `reply-drafter`, `email-polisher`, `followup-reply-writer` |
| `doc_p2_document_rewriter` | M6 TF-IDF -> schema rerank | 2 | `reply-polisher` | `reply-polisher`, `document-rewriter`, `document-normaliser`, `document-converter`, `layout-preserving-converter` |
| `doc_p4_field_extraction` | M6 TF-IDF -> schema rerank | - | `receipt-extractor` | `receipt-extractor`, `invoice-payment-checker`, `docs-ops-field-extractor`, `ml-ops-field-extractor`, `lab-ops-field-extractor` |
| `doc_p6_conversion` | M6 TF-IDF -> schema rerank | 2 | `layout-preserving-converter` | `layout-preserving-converter`, `document-converter`, `deck-template-applier`, `note-tagger`, `content-strategy-builder` |
| `data_p3_validation` | M6 TF-IDF -> schema rerank | 1 | `data-analysis-with-validation` | `data-analysis-with-validation`, `accessibility-checker`, `lab-ops-quality-auditor`, `docs-ops-quality-auditor`, `events-ops-quality-auditor` |
| `obs_p5_root_cause` | M6 TF-IDF -> schema rerank | 2 | `data-analysis-for-root-cause-diagnosis` | `data-analysis-for-root-cause-diagnosis`, `metrics-root-cause-diagnoser`, `metrics-overview`, `latency-anomaly-detector`, `debugging-root-cause-helper` |
| `news_p2_briefing` | M6 TF-IDF -> schema rerank | 1 | `news-briefing-writer` | `news-briefing-writer`, `knowledge-base-article-writer`, `support-ops-timeline-builder`, `metrics-overview`, `support-ops-monitoring-plan-builder` |
| `read_p2_general_source_summary` | M6 TF-IDF -> schema rerank | 2 | `paper-summariser` | `paper-summariser`, `general-source-summariser`, `research-ops-summary-writer`, `operations-ops-summary-writer`, `professor-email-reply` |
| `read_p7_multi_source_comparison` | M6 TF-IDF -> schema rerank | 2 | `related-work-synthesiser` | `related-work-synthesiser`, `multi-source-comparison-builder`, `data-analysis-for-ranking-selection`, `method-note-builder`, `agent-eval-coverage-auditor` |
| `sec_p2_security_code_review` | M6 TF-IDF -> schema rerank | 1 | `security-code-reviewer` | `security-code-reviewer`, `pr-reviewer`, `review-comment-resolver`, `api-ops-acceptance-test-builder`, `code-reviewer` |
| `skill_p4_edit_existing` | M6 TF-IDF -> schema rerank | 1 | `skill-editor` | `skill-editor`, `agent-ops-field-extractor`, `docs-ops-field-extractor`, `skill-finder`, `skill-creator` |
| `skill_p6_package_existing` | M6 TF-IDF -> schema rerank | 1 | `skill-packager` | `skill-packager`, `paper-summariser`, `skill-editor`, `agent-ops-resource-linker`, `public-skill-creator` |
| `reply_p2_polish_supervisor` | M6 MiniLM full -> schema rerank | 1 | `reply-polisher` | `reply-polisher`, `reply-drafter`, `email-polisher`, `email-ops-rewrite-editor`, `followup-reply-writer` |
| `doc_p2_document_rewriter` | M6 MiniLM full -> schema rerank | 1 | `document-rewriter` | `document-rewriter`, `reply-polisher`, `document-converter`, `document-normaliser`, `travel-ops-rewrite-editor` |
| `doc_p4_field_extraction` | M6 MiniLM full -> schema rerank | 2 | `receipt-extractor` | `receipt-extractor`, `document-field-extractor`, `finance-ops-field-extractor`, `vendor-ops-field-extractor`, `crm-ops-field-extractor` |
| `doc_p6_conversion` | M6 MiniLM full -> schema rerank | 1 | `document-converter` | `document-converter`, `layout-preserving-converter`, `document-normaliser`, `document-rewriter`, `public-markitdown` |
| `data_p3_validation` | M6 MiniLM full -> schema rerank | 1 | `data-analysis-with-validation` | `data-analysis-with-validation`, `dataset-ops-quality-auditor`, `data-analysis-with-anomaly-focus`, `finance-ops-quality-auditor`, `incident-ops-quality-auditor` |
| `obs_p5_root_cause` | M6 MiniLM full -> schema rerank | 1 | `metrics-root-cause-diagnoser` | `metrics-root-cause-diagnoser`, `latency-anomaly-detector`, `metrics-overview`, `slo-breach-checker`, `support-ops-failure-diagnoser` |
| `news_p2_briefing` | M6 MiniLM full -> schema rerank | 1 | `news-briefing-writer` | `news-briefing-writer`, `events-ops-summary-writer`, `news-summariser`, `meeting-summary-writer`, `events-ops-timeline-builder` |
| `read_p2_general_source_summary` | M6 MiniLM full -> schema rerank | 1 | `general-source-summariser` | `general-source-summariser`, `paper-summariser`, `research-ops-summary-writer`, `data-analysis-for-reporting`, `research-ops-evidence-grounder` |
| `read_p7_multi_source_comparison` | M6 MiniLM full -> schema rerank | 1 | `multi-source-comparison-builder` | `multi-source-comparison-builder`, `related-work-synthesiser`, `research-ops-comparison-builder`, `thesis-ops-comparison-builder`, `paper-summariser` |
| `sec_p2_security_code_review` | M6 MiniLM full -> schema rerank | 1 | `security-code-reviewer` | `security-code-reviewer`, `auth-flow-reviewer`, `frontend-debugger`, `api-ops-acceptance-test-builder`, `api-ops-compliance-checker` |
| `skill_p4_edit_existing` | M6 MiniLM full -> schema rerank | - | `docs-ops-field-extractor` | `docs-ops-field-extractor`, `agent-ops-field-extractor`, `writing-ops-field-extractor`, `hr-ops-field-extractor`, `knowledge-ops-field-extractor` |
| `skill_p6_package_existing` | M6 MiniLM full -> schema rerank | 1 | `skill-packager` | `skill-packager`, `paper-summariser`, `public-pdf`, `public-skill-creator`, `general-source-summariser` |

Interpretation: Step 8 downstream runs are fair only when gold/acceptable is present in the candidate set. Missing top-5 cases should be labelled as retrieval failures before judging the main agent's artifact quality.
