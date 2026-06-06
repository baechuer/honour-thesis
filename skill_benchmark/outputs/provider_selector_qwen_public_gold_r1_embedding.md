# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (2401 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 59.4% |
| Acceptable top-1 accuracy | 65.6% |
| Top-3 recall | 84.4% |
| Top-5 recall | 87.5% |
| Acceptable top-5 recall | 90.6% |
| MRR | 0.716 |
| Non-main top-1 | 78.1% |
| Approx selector-visible tokens | 122537 |

## API Usage Estimate

- Embedding API calls made in this run: 6
- Embedding cache hits: 2381
- Approx uncached embedding input tokens: 2513
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 1 | 1 | `public-office-pdf-extraction` | gold | public-office-pdf-extraction, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, vendor-ops-field-extractor, pdf-ocr-extractor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 3 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, public-office-pdf-ocr, public-office-chat-with-pdf, implicit-pdf-evidence-answerer |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, implicit-pdf-evidence-answerer, document-summariser, implicit-pdf-table-reconstructor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, layout-preserving-converter, office-to-markdown-converter, document-converter, public-office-batch-convert |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-chat-with-pdf, document-summariser, implicit-pdf-evidence-answerer, pdf-redaction-reviewer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 3 | 3 | `public-oh-my-playwriter` | wrong | public-oh-my-playwriter, public-playwright-interactive, public-addy-agent-browser-testing-with-devtools, playwright-flow-debugger, web-page-snapshotter |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 2 | 2 | `product-ops-rewrite-editor` | wrong | product-ops-rewrite-editor, public-addy-web-accessibility, product-ops-comparison-builder, product-ops-compliance-checker, product-ops-quality-auditor |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, web-ops-evidence-grounder, web-performance-budget-checker, seo-ops-evidence-grounder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | 26 | `localization-ops-field-extractor` | wrong | localization-ops-field-extractor, localization-ops-evidence-grounder, implicit-ci-failure-reader, geospatial-ops-evidence-grounder, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 5 | 5 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, pr-review-comment-resolver, public-openai-gh-fix-ci, ci-failure-debugger, public-swebench-analyze-ci |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 1 | 1 | `public-mattpocock-setup-pre-commit` | gold | public-mattpocock-setup-pre-commit, git-safety-guardrail-installer, git-commit-writer, public-mattpocock-git-guardrails-claude-code, public-swebench-fix |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, public-oh-my-git-guardrails-claude-code, git-safety-guardrail-installer, public-openai-gh-fix-ci, git-commit-writer |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 7 | 7 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, public-mattpocock-review, implicit-review-comment-planner, pr-reviewer |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, public-openai-cloudflare-deploy, deployment-release-verifier |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, public-swebench-fix, public-openai-render-deploy, publishing-ops-artifact-packager |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-netlify-deploy, public-openai-vercel-deploy, deployment-build-triager, public-openai-cloudflare-deploy |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 6 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, rest-api-contract-designer, api-documentation-writer, auth-flow-integrator, public-swebench-mcp-builder |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, public-swebench-mcp-builder, public-anthropic-mcp-builder, mcp-server-builder, auth-flow-integrator |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 3 | 3 | `api-documentation-writer` | wrong | api-documentation-writer, rest-api-contract-designer, public-openai-cli-creator, openapi-contract-reviewer, mcp-server-builder |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 1 | 1 | `public-huggingface-datasets` | gold | public-huggingface-datasets, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-evidence-grounder, dataset-ops-quality-auditor |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 1 | 1 | `public-huggingface-huggingface-gradio` | gold | public-huggingface-huggingface-gradio, gradio-demo-builder, public-huggingface-transformers-js, public-huggingface-huggingface-zerogpu, implicit-hf-dataset-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-llm-trainer, sentence-transformer-finetuner, public-huggingface-huggingface-community-evals, hf-local-model-selector |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 1 | 1 | `public-huggingface-train-sentence-transformers` | gold | public-huggingface-train-sentence-transformers, sentence-transformer-finetuner, public-huggingface-transformers-js, training-ops-evidence-grounder, search-ops-evidence-grounder |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-datasets, public-huggingface-huggingface-paper-publisher, hf-dataset-viewer-inspector, public-huggingface-huggingface-local-models |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 1 | 1 | `public-office-data-pipeline` | gold | public-office-data-pipeline, public-office-etl-pipeline, dataset-ops-field-extractor, analytics-ops-field-extractor, dataset-ops-monitoring-plan-builder |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 1 | 1 | `public-office-database-sync` | gold | public-office-database-sync, database-migration-risk-assessor, database-ops-dependency-mapper, database-backup-planner, migration-risk-auditor |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 15 | 15 | `contract-risk-reviewer` | wrong | contract-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-risk-reviewer, procurement-risk-summariser, vendor-ops-rewrite-editor |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-evidence-grounder, email-ops-risk-reviewer, email-polisher, professor-email-reply |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 2 | 2 | `slide-outline-builder` | wrong | slide-outline-builder, public-office-ai-slides, speaker-notes-writer, deck-template-applier, slide-deck-visual-auditor |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 1 | 1 | `public-openai-figma-implement-design` | gold | public-openai-figma-implement-design, public-openai-figma, public-openai-figma-generate-design, public-openai-figma-use, public-openai-figma-code-connect-components |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 2 | `skill-creator` | wrong | skill-creator, public-skill-creator, skill-field-auditor, skill-authoring-guide, public-skill-installer |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 3 | 3 | `public-addy-agent-security-and-hardening` | wrong | public-addy-agent-security-and-hardening, architecture-boundary-reviewer, public-security-threat-model, public-openai-security-ownership-map, service-dependency-mapper |
