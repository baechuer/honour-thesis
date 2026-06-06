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
| Top-1 accuracy | 25.0% |
| Acceptable top-1 accuracy | 31.2% |
| Top-3 recall | 62.5% |
| Top-5 recall | 78.1% |
| Acceptable top-5 recall | 81.2% |
| MRR | 0.482 |
| Non-main top-1 | 34.4% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2433
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 4 | 4 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-ocr-extractor, implicit-pdf-evidence-answerer, public-office-pdf-extraction, implicit-pdf-table-reconstructor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 11 | 11 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, implicit-pdf-evidence-answerer, pdf-layout-reviewer, pdf-to-docx-converter |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, document-field-extractor, implicit-pdf-evidence-answerer, pdf-layout-table-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, public-markitdown, pdf-to-docx-converter, public-office-pdf-ocr, public-office-pdf-to-docx |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-pdf-watermark, pdf-to-docx-converter, implicit-pdf-evidence-answerer, docs-ops-summary-writer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 3 | 3 | `frontend-debugger` | wrong | frontend-debugger, playwright-flow-debugger, public-addy-agent-browser-testing-with-devtools, web-page-snapshotter, implicit-browser-flow-investigator |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 6 | 6 | `accessibility-checker` | wrong | accessibility-checker, accessibility-interaction-auditor, pdf-layout-reviewer, product-ops-compliance-checker, product-ops-comparison-builder |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, accessibility-checker, web-performance-budget-checker, web-ops-risk-reviewer, web-ops-monitoring-plan-builder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `frontend-debugger` | wrong | frontend-debugger, resilience-pattern-reviewer, geospatial-ops-failure-diagnoser, geospatial-ops-quality-auditor, geospatial-ops-acceptance-test-builder |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 5 | 5 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, repo-ops-failure-diagnoser, deployment-build-triager, public-swebench-analyze-ci |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 2 | 2 | `git-safety-guardrail-installer` | wrong | git-safety-guardrail-installer, public-mattpocock-setup-pre-commit, ci-failure-debugger, public-mattpocock-git-guardrails-claude-code, pr-reviewer |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, version-control-helper, public-addy-agent-git-workflow-and-versioning, security-code-reviewer |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 8 | 8 | `review-comment-resolver` | wrong | review-comment-resolver, pr-review-comment-resolver, pr-reviewer, implicit-review-comment-planner, public-mattpocock-review |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, deployment-release-verifier, public-openai-cloudflare-deploy |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, deployment-release-verifier, platform-ops-artifact-packager, skill-packager |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-openai-vercel-deploy, kubernetes-deployment-helper, public-netlify-deploy, public-openai-cloudflare-deploy |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 4 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, public-swebench-mcp-builder, public-office-mcp-hub, public-anthropic-mcp-builder, public-office-office-mcp |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 2 | 2 | `mcp-server-builder` | wrong | mcp-server-builder, public-openai-chatgpt-apps, public-swebench-mcp-builder, public-anthropic-mcp-builder, public-openai-winui-app |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 7 | 7 | `api-documentation-writer` | wrong | api-documentation-writer, openapi-contract-reviewer, rest-api-contract-designer, external-api-integration-planner, mcp-server-builder |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, public-huggingface-datasets, implicit-hf-dataset-inspector, dataset-ops-comparison-builder, dataset-ops-scenario-planner |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 2 | `gradio-demo-builder` | wrong | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, hf-local-model-selector, implicit-hf-dataset-inspector, public-huggingface-huggingface-llm-trainer |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, hf-local-model-selector, gradio-demo-builder, public-huggingface-transformers-js |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, hf-dataset-viewer-inspector, public-huggingface-datasets, public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 2 | `public-office-etl-pipeline` | wrong | public-office-etl-pipeline, public-office-data-pipeline, ci-cd-pipeline-builder, dataset-ops-comparison-builder, public-office-data-analysis |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 5 | 5 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, external-api-integration-planner, database-ops-monitoring-plan-builder, geospatial-ops-monitoring-plan-builder, public-office-database-sync |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 9 | 9 | `contract-risk-reviewer` | wrong | contract-risk-reviewer, vendor-ops-summary-writer, contract-ops-summary-writer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, reply-polisher, professor-email-reply, reply-drafter, email-polisher |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 3 | 3 | `slide-deck-visual-auditor` | wrong | slide-deck-visual-auditor, slide-outline-builder, public-office-ai-slides, deck-template-applier, public-office-ppt-visual |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 2 | 2 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-code-connect-components, public-openai-figma, public-openai-figma-generate-library |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 5 | 5 | `skill-creator` | wrong | skill-creator, skill-authoring-guide, skill-finder, skill-editor, public-skill-creator |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 37 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, architecture-boundary-reviewer, api-security-threat-reviewer, security-ops-risk-reviewer |
