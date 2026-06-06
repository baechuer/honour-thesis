# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `full`
- Scale: `current_full` (2401 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 68.8% |
| Acceptable top-1 accuracy | 71.9% |
| Top-3 recall | 84.4% |
| Top-5 recall | 84.4% |
| Acceptable top-5 recall | 84.4% |
| MRR | 0.763 |
| Non-main top-1 | 84.4% |
| Approx selector-visible tokens | 1599226 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2433
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 32
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 346861

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 1 | 1 | `public-office-pdf-extraction` | gold | public-office-pdf-extraction, public-pdf, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-layout-table-extractor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 3 | `pdf-ocr-cleaner` | wrong | pdf-ocr-cleaner, pdf-ocr-extractor, public-office-pdf-ocr, implicit-pdf-evidence-answerer, docs-ops-scenario-planner |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, implicit-pdf-evidence-answerer, hr-ops-field-extractor, docs-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, public-office-batch-convert, docs-ops-normalizer, public-office-pdf-converter, office-to-markdown-converter |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, legal-ops-artifact-packager, docs-ops-artifact-packager, public-pdf, docs-ops-normalizer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, public-office-browser-automation, public-openai-playwright, frontend-debugger, public-oh-my-playwriter |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | - | - | `accessibility-interaction-auditor` | wrong | accessibility-interaction-auditor, accessibility-checker, product-ops-quality-auditor, product-ops-compliance-checker, ecommerce-ops-quality-auditor |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, web-ops-quality-auditor, web-ops-evidence-grounder, web-ops-failure-diagnoser, frontend-debugger |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `localization-ops-failure-diagnoser` | wrong | localization-ops-failure-diagnoser, product-ops-failure-diagnoser, geospatial-ops-failure-diagnoser, mobile-ops-failure-diagnoser, localization-ops-evidence-grounder |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 1 | 1 | `public-swebench-analyze-ci` | gold | public-swebench-analyze-ci, repo-ops-failure-diagnoser, implicit-ci-failure-reader, ci-failure-debugger, ci-log-root-cause-debugger |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 1 | 1 | `public-mattpocock-setup-pre-commit` | gold | public-mattpocock-setup-pre-commit, public-oh-my-setup-pre-commit, version-control-helper, git-safety-guardrail-installer, public-mattpocock-git-guardrails-claude-code |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, public-oh-my-git-guardrails-claude-code, git-safety-guardrail-installer, version-control-helper, repo-ops-compliance-checker |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | - | - | `review-comment-resolver` | wrong | review-comment-resolver, pr-review-comment-resolver, repo-ops-risk-reviewer, implicit-review-comment-planner, pr-reviewer |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-render-deploy, public-oh-my-deployment-automation, public-openai-vercel-deploy, public-openai-cloudflare-deploy |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, platform-ops-artifact-packager, public-openai-vercel-deploy, public-addy-web-best-practices, public-openai-render-deploy |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, kubernetes-deployment-helper, platform-ops-artifact-packager, public-oh-my-deployment-automation, platform-ops-dependency-mapper |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 1 | 1 | `public-anthropic-mcp-builder` | gold | public-anthropic-mcp-builder, public-swebench-mcp-builder, public-office-office-mcp, mcp-server-builder, public-office-mcp-hub |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, public-anthropic-mcp-builder, public-swebench-mcp-builder, mcp-server-builder, public-openai-winui-app |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 1 | 1 | `public-openai-cli-creator` | gold | public-openai-cli-creator, api-documentation-writer, openapi-contract-tester, api-ops-acceptance-test-builder, openapi-contract-reviewer |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 1 | 1 | `public-huggingface-datasets` | gold | public-huggingface-datasets, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-dependency-mapper, dataset-ops-resource-linker |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 1 | 1 | `public-huggingface-huggingface-gradio` | gold | public-huggingface-huggingface-gradio, gradio-demo-builder, public-huggingface-datasets, public-huggingface-huggingface-zerogpu, public-huggingface-transformers-js |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-llm-trainer, ml-ops-dependency-mapper, ml-ops-artifact-packager, implicit-hf-local-model-chooser |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 1 | 1 | `public-huggingface-train-sentence-transformers` | gold | public-huggingface-train-sentence-transformers, sentence-transformer-finetuner, public-huggingface-transformers-js, public-huggingface-huggingface-vision-trainer, hf-community-eval-runner |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-huggingface-best, public-huggingface-huggingface-local-models, public-huggingface-huggingface-tool-builder, public-huggingface-huggingface-trackio |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 2 | `public-office-etl-pipeline` | wrong | public-office-etl-pipeline, public-office-data-pipeline, dataset-ops-timeline-builder, dataset-ops-dependency-mapper, public-office-data-extractor |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 1 | 1 | `public-office-database-sync` | gold | public-office-database-sync, database-schema-designer, database-ops-comparison-builder, database-ops-resource-linker, database-ops-dependency-mapper |
| `public_gold_p27_contract_review` | `public-office-contract-review` | - | - | `contract-risk-reviewer` | wrong | contract-risk-reviewer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-quality-auditor, contract-ops-scenario-planner |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-risk-reviewer, email-ops-priority-ranker, email-ops-evidence-grounder, email-ops-intake-classifier |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 1 | 1 | `public-office-ai-slides` | gold | public-office-ai-slides, slide-outline-builder, public-oh-my-presentation-builder, public-office-ppt-visual, public-office-md-slides |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 2 | 2 | `public-openai-figma` | wrong | public-openai-figma, public-openai-figma-implement-design, public-openai-figma-use, public-openai-figma-generate-design, public-anthropic-frontend-design |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 2 | `skill-creator` | wrong | skill-creator, public-skill-creator, skill-authoring-guide, public-anthropic-doc-coauthoring, public-oh-my-workflow-automation |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 10 | 10 | `security-ops-risk-reviewer` | wrong | security-ops-risk-reviewer, api-security-threat-reviewer, repo-ops-risk-reviewer, security-ops-dependency-mapper, security-ops-quality-auditor |
