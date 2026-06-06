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
| Top-1 accuracy | 28.1% |
| Acceptable top-1 accuracy | 34.4% |
| Top-3 recall | 59.4% |
| Top-5 recall | 65.6% |
| Acceptable top-5 recall | 68.8% |
| MRR | 0.469 |
| Non-main top-1 | 43.8% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 32
- Embedding cache hits: 2401
- Approx uncached embedding input tokens: 1680
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 5 | 5 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-ocr-extractor, vendor-ops-field-extractor, public-office-pdf-extraction |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 15 | 15 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-to-docx-converter, pdf-layout-reviewer, pdf-question-answerer |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, hr-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, public-markitdown, pdf-to-docx-converter, document-converter |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, docs-ops-artifact-packager, pdf-to-docx-converter, pdf-redaction-reviewer, multi-document-comparison-preparer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 7 | 7 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, implicit-browser-flow-investigator, web-page-snapshotter, frontend-debugger, web-ui-tester |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 21 | 21 | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, product-ops-compliance-checker, product-ops-comparison-builder, product-ops-rewrite-editor |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 2 | 2 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, public-addy-web-core-web-vitals, frontend-debugger, implicit-browser-flow-investigator, web-ops-evidence-grounder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `geospatial-ops-failure-diagnoser` | wrong | geospatial-ops-failure-diagnoser, geospatial-ops-quality-auditor, geospatial-ops-acceptance-test-builder, geospatial-ops-evidence-grounder, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 10 | 10 | `ci-failure-debugger` | wrong | ci-failure-debugger, ci-log-root-cause-debugger, implicit-ci-failure-reader, review-comment-resolver, pr-review-comment-resolver |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 2 | 2 | `git-safety-guardrail-installer` | wrong | git-safety-guardrail-installer, public-mattpocock-setup-pre-commit, repo-code-reviewer, code-reviewer, release-changelog-generator |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-oh-my-git-guardrails-claude-code, version-control-helper, repo-code-reviewer |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 32 | 32 | `review-comment-resolver` | wrong | review-comment-resolver, pr-review-comment-resolver, implicit-review-comment-planner, pr-reviewer, code-reviewer |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, deployment-release-verifier, public-oh-my-vercel-react-best-practices |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, deployment-build-triager, deployment-release-verifier, public-openai-render-deploy |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-netlify-deploy, deployment-build-triager, public-oh-my-vercel-deploy, public-openai-vercel-deploy |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 5 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, rest-api-contract-designer, public-swebench-mcp-builder, api-documentation-writer, public-anthropic-mcp-builder |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, mcp-server-builder, api-documentation-writer, public-swebench-mcp-builder, rest-api-contract-designer |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 7 | 7 | `api-documentation-writer` | wrong | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, external-api-integration-planner |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, public-huggingface-datasets, implicit-hf-dataset-inspector, dataset-ops-summary-writer, dataset-ops-comparison-builder |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 2 | `gradio-demo-builder` | wrong | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, implicit-hf-dataset-inspector, hf-dataset-viewer-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, sentence-transformer-finetuner, implicit-hf-dataset-inspector, ml-ops-normalizer, implicit-hf-local-model-chooser |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, gradio-demo-builder, public-huggingface-transformers-js, implicit-hf-local-model-chooser |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, public-huggingface-datasets, hf-zerogpu-space-deployer |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 2 | `public-office-etl-pipeline` | wrong | public-office-etl-pipeline, public-office-data-pipeline, public-office-database-sync, dataset-ops-timeline-builder, public-office-data-analysis |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 2 | 2 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, public-office-database-sync, migration-risk-auditor, database-ops-comparison-builder, database-ops-normalizer |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 36 | 36 | `contract-risk-reviewer` | wrong | contract-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-risk-reviewer, vendor-ops-handoff-brief-writer, vendor-ops-rewrite-editor |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-risk-reviewer, email-polisher, reply-polisher, email-ops-evidence-grounder |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 6 | 6 | `slide-outline-builder` | wrong | slide-outline-builder, slide-deck-visual-auditor, deck-template-applier, speaker-notes-writer, public-office-ppt-visual |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 3 | 3 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-code-connect-components |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 6 | 6 | `skill-creator` | wrong | skill-creator, skill-authoring-guide, public-oh-my-workflow-automation, code-documentation-writer, skill-finder |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 16 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, security-ops-quality-auditor, security-ops-risk-reviewer, security-ops-normalizer |
