# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (2401 skills)
- Reranker: `local-schema`
- Rerank candidates: 100

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 46.9% |
| Acceptable top-1 accuracy | 50.0% |
| Top-3 recall | 84.4% |
| Top-5 recall | 90.6% |
| Acceptable top-5 recall | 93.8% |
| MRR | 0.653 |
| Non-main top-1 | 50.0% |
| Approx selector-visible tokens | 1054399 |

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
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 3 | 3 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-ocr-extractor, public-office-pdf-extraction, public-office-chat-with-pdf, implicit-pdf-evidence-answerer |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 4 | 4 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, implicit-pdf-evidence-answerer, public-office-pdf-ocr, pdf-to-docx-converter |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 1 | 1 | `public-office-pdf-form-filler` | gold | public-office-pdf-form-filler, pdf-form-filler, implicit-pdf-evidence-answerer, document-field-extractor, docs-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, office-to-markdown-converter, public-office-pdf-ocr, public-office-pdf-to-docx, public-office-file-organizer |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-pdf-watermark, public-pdf, public-office-chat-with-pdf, pdf-to-docx-converter |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, frontend-debugger, playwright-flow-debugger, web-page-snapshotter, implicit-browser-flow-investigator |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 3 | 3 | `accessibility-checker` | wrong | accessibility-checker, accessibility-interaction-auditor, public-addy-web-accessibility, pdf-layout-reviewer, product-ops-comparison-builder |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, accessibility-checker, public-addy-web-web-quality-audit, web-performance-budget-checker, web-ops-risk-reviewer |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | 6 | 6 | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, resilience-pattern-reviewer, public-addy-agent-code-simplification, frontend-debugger, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 3 | 3 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, ci-failure-debugger, public-swebench-analyze-ci, deployment-build-triager, repo-ops-failure-diagnoser |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 1 | 1 | `public-mattpocock-setup-pre-commit` | gold | public-mattpocock-setup-pre-commit, git-safety-guardrail-installer, ci-failure-debugger, public-openai-yeet, public-mattpocock-git-guardrails-claude-code |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, version-control-helper, public-addy-agent-git-workflow-and-versioning, public-oh-my-git-guardrails-claude-code |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 4 | 4 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, pr-reviewer, public-openai-gh-address-comments, public-mattpocock-review |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, deployment-release-verifier, public-openai-render-deploy |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, public-swebench-k8s-manifest-generator, public-openai-render-deploy, platform-ops-artifact-packager |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-openai-vercel-deploy, kubernetes-deployment-helper, public-netlify-deploy, public-swebench-k8s-manifest-generator |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 3 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, public-swebench-mcp-builder, public-anthropic-mcp-builder, public-office-mcp-hub, public-office-office-mcp |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, mcp-server-builder, public-swebench-mcp-builder, public-anthropic-mcp-builder, public-openai-winui-app |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 3 | 3 | `api-documentation-writer` | wrong | api-documentation-writer, openapi-contract-reviewer, public-openai-cli-creator, rest-api-contract-designer, mcp-server-builder |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, public-huggingface-datasets, implicit-hf-dataset-inspector, public-huggingface-huggingface-vision-trainer, dataset-ops-comparison-builder |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 2 | `gradio-demo-builder` | wrong | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, hf-dataset-viewer-inspector, public-huggingface-huggingface-zerogpu |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, hf-local-model-selector, public-huggingface-huggingface-llm-trainer, implicit-hf-dataset-inspector |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-huggingface-transformers-js, hf-local-model-selector, gradio-demo-builder |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-datasets, hf-dataset-viewer-inspector, public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 1 | 1 | `public-office-data-pipeline` | gold | public-office-data-pipeline, public-office-etl-pipeline, public-office-database-sync, ci-cd-pipeline-builder, dataset-ops-comparison-builder |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 2 | 2 | `external-api-integration-planner` | wrong | external-api-integration-planner, public-office-database-sync, geospatial-ops-monitoring-plan-builder, database-migration-risk-assessor, database-ops-monitoring-plan-builder |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 6 | 6 | `contract-risk-reviewer` | wrong | contract-risk-reviewer, vendor-ops-summary-writer, contract-ops-summary-writer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, reply-drafter, professor-email-reply, reply-polisher, followup-reply-writer |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 3 | 3 | `slide-deck-visual-auditor` | wrong | slide-deck-visual-auditor, slide-outline-builder, public-office-ai-slides, public-office-ppt-visual, deck-template-applier |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 1 | 1 | `public-openai-figma-implement-design` | gold | public-openai-figma-implement-design, public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-openai-figma-use, public-openai-figma-generate-library |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 2 | `skill-creator` | wrong | skill-creator, public-skill-creator, skill-authoring-guide, public-anthropic-skill-creator, skill-finder |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 14 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, architecture-boundary-reviewer, public-addy-agent-security-and-hardening, service-dependency-mapper |
