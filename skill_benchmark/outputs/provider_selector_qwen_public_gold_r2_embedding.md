# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r2`
- Scale: `current_full` (2401 skills)
- Reranker: `none`
- Rerank candidates: 0

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 59.4% |
| Acceptable top-1 accuracy | 62.5% |
| Top-3 recall | 87.5% |
| Top-5 recall | 87.5% |
| Acceptable top-5 recall | 87.5% |
| MRR | 0.732 |
| Non-main top-1 | 71.9% |
| Approx selector-visible tokens | 1054399 |

## API Usage Estimate

- Embedding API calls made in this run: 144
- Embedding cache hits: 997
- Approx uncached embedding input tokens: 697865
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 6 | 6 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, public-office-table-extractor, implicit-pdf-table-reconstructor, public-office-pdf-ocr, vendor-ops-field-extractor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 3 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, public-office-pdf-ocr, pdf-to-docx-converter, public-office-chat-with-pdf |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 1 | 1 | `public-office-pdf-form-filler` | gold | public-office-pdf-form-filler, pdf-form-filler, implicit-pdf-table-reconstructor, pdf-layout-table-extractor, public-office-chat-with-pdf |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, office-to-markdown-converter, public-office-pdf-ocr, pdf-to-docx-converter, public-office-office-mcp |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-chat-with-pdf, public-pdf, pdf-redaction-reviewer, pdf-to-docx-converter |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, public-playwright-interactive, public-oh-my-playwriter, playwright-flow-debugger, public-oh-my-browser-harness |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 1 | 1 | `public-addy-web-accessibility` | gold | public-addy-web-accessibility, accessibility-interaction-auditor, public-oh-my-web-design-guidelines, product-ops-comparison-builder, accessibility-checker |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, public-addy-web-performance, public-addy-web-web-quality-audit, public-addy-agent-performance-optimization, web-performance-budget-checker |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | 12 | 12 | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, localization-ops-failure-diagnoser, public-mattpocock-diagnose, public-lbussell-property-testing-cscheck, mobile-ops-evidence-grounder |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 2 | 2 | `ci-log-root-cause-debugger` | wrong | ci-log-root-cause-debugger, public-swebench-analyze-ci, ci-failure-debugger, implicit-ci-failure-reader, public-openai-gh-fix-ci |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 1 | 1 | `public-mattpocock-setup-pre-commit` | gold | public-mattpocock-setup-pre-commit, git-safety-guardrail-installer, public-oh-my-environment-setup, public-addy-agent-security-and-hardening, public-oh-my-file-organization |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, public-oh-my-git-guardrails-claude-code, git-safety-guardrail-installer, public-oh-my-git-workflow, public-mattpocock-review |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 6 | 6 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, review-comment-resolver, implicit-review-comment-planner, public-mattpocock-review, pr-reviewer |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, public-openai-render-deploy, public-oh-my-vercel-react-best-practices |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, public-openai-render-deploy, public-openai-vercel-deploy, public-swebench-k8s-manifest-generator |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-netlify-deploy, public-openai-vercel-deploy, public-swebench-k8s-manifest-generator, public-oh-my-environment-setup |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 3 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, public-swebench-mcp-builder, public-anthropic-mcp-builder, api-documentation-writer, rest-api-contract-designer |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, public-swebench-mcp-builder, public-anthropic-mcp-builder, mcp-server-builder, api-documentation-writer |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 2 | 2 | `api-documentation-writer` | wrong | api-documentation-writer, public-openai-cli-creator, mcp-server-builder, rest-api-contract-designer, openapi-contract-reviewer |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 1 | 1 | `public-huggingface-datasets` | gold | public-huggingface-datasets, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, public-office-data-analysis, public-huggingface-huggingface-vision-trainer |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 2 | `gradio-demo-builder` | wrong | gradio-demo-builder, public-huggingface-huggingface-gradio, public-huggingface-huggingface-zerogpu, public-huggingface-transformers-js, implicit-hf-dataset-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, sentence-transformer-finetuner, public-huggingface-huggingface-llm-trainer, implicit-hf-dataset-inspector, public-huggingface-train-sentence-transformers |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 1 | 1 | `public-huggingface-train-sentence-transformers` | gold | public-huggingface-train-sentence-transformers, sentence-transformer-finetuner, public-huggingface-transformers-js, public-swebench-vector-index-tuning, public-n-skills-zai-cli |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-datasets, public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, public-huggingface-huggingface-tool-builder |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 2 | `public-office-etl-pipeline` | wrong | public-office-etl-pipeline, public-office-data-pipeline, public-office-database-sync, public-swebench-dbt-transformation-patterns, analytics-ops-timeline-builder |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 1 | 1 | `public-office-database-sync` | gold | public-office-database-sync, database-migration-risk-assessor, database-ops-comparison-builder, migration-risk-auditor, public-oh-my-database-schema-design |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 6 | 6 | `contract-risk-reviewer` | wrong | contract-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-risk-reviewer, vendor-ops-evidence-grounder, vendor-ops-rewrite-editor |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-polisher, email-ops-risk-reviewer, professor-email-reply, email-ops-evidence-grounder |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 3 | 3 | `slide-outline-builder` | wrong | slide-outline-builder, slide-deck-visual-auditor, public-office-ai-slides, public-oh-my-presentation-builder, public-office-ppt-visual |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 2 | 2 | `public-openai-figma-use` | wrong | public-openai-figma-use, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-generate-design, public-addy-agent-frontend-ui-engineering |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 1 | 1 | `public-skill-creator` | gold | public-skill-creator, public-anthropic-skill-creator, skill-creator, skill-authoring-guide, skill-finder |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 3 | 3 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, public-addy-agent-security-and-hardening, public-security-threat-model, service-dependency-mapper, secret-leak-scanner |
