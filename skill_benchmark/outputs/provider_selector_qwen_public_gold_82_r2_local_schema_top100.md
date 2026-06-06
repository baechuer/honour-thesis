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
| Top-1 accuracy | 39.0% |
| Acceptable top-1 accuracy | 57.3% |
| Top-3 recall | 79.3% |
| Top-5 recall | 85.4% |
| Acceptable top-5 recall | 95.1% |
| MRR | 0.600 |
| Non-main top-1 | 59.8% |
| Approx selector-visible tokens | 1054399 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2483
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 3 | 3 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-ocr-extractor, public-office-pdf-extraction, public-office-chat-with-pdf, implicit-pdf-evidence-answerer |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 4 | 1 | `pdf-ocr-cleaner` | acceptable | pdf-ocr-cleaner, pdf-ocr-extractor, implicit-pdf-evidence-answerer, public-office-pdf-ocr, pdf-to-docx-converter |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 1 | 1 | `public-office-pdf-form-filler` | gold | public-office-pdf-form-filler, pdf-form-filler, implicit-pdf-evidence-answerer, document-field-extractor, docs-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, office-to-markdown-converter, public-office-pdf-ocr, public-office-pdf-to-docx, public-office-file-organizer |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-pdf-watermark, public-pdf, public-office-chat-with-pdf, pdf-to-docx-converter |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, frontend-debugger, playwright-flow-debugger, web-page-snapshotter, implicit-browser-flow-investigator |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 3 | 1 | `accessibility-checker` | acceptable | accessibility-checker, accessibility-interaction-auditor, public-addy-web-accessibility, pdf-layout-reviewer, product-ops-comparison-builder |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, accessibility-checker, public-addy-web-web-quality-audit, web-performance-budget-checker, web-ops-risk-reviewer |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | 6 | 6 | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, resilience-pattern-reviewer, public-addy-agent-code-simplification, frontend-debugger, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 3 | 1 | `ci-log-root-cause-debugger` | acceptable | ci-log-root-cause-debugger, ci-failure-debugger, public-swebench-analyze-ci, deployment-build-triager, repo-ops-failure-diagnoser |
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
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 1 | `gradio-demo-builder` | acceptable | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, hf-dataset-viewer-inspector, public-huggingface-huggingface-zerogpu |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, hf-local-model-selector, public-huggingface-huggingface-llm-trainer, implicit-hf-dataset-inspector |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 1 | `sentence-transformer-finetuner` | acceptable | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-huggingface-transformers-js, hf-local-model-selector, gradio-demo-builder |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-datasets, hf-dataset-viewer-inspector, public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 1 | 1 | `public-office-data-pipeline` | gold | public-office-data-pipeline, public-office-etl-pipeline, public-office-database-sync, ci-cd-pipeline-builder, dataset-ops-comparison-builder |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 2 | 2 | `external-api-integration-planner` | wrong | external-api-integration-planner, public-office-database-sync, geospatial-ops-monitoring-plan-builder, database-migration-risk-assessor, database-ops-monitoring-plan-builder |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 6 | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, vendor-ops-summary-writer, contract-ops-summary-writer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, reply-drafter, professor-email-reply, reply-polisher, followup-reply-writer |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 3 | 3 | `slide-deck-visual-auditor` | wrong | slide-deck-visual-auditor, slide-outline-builder, public-office-ai-slides, public-office-ppt-visual, deck-template-applier |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 1 | 1 | `public-openai-figma-implement-design` | gold | public-openai-figma-implement-design, public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-openai-figma-use, public-openai-figma-generate-library |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 1 | `skill-creator` | acceptable | skill-creator, public-skill-creator, skill-authoring-guide, public-anthropic-skill-creator, skill-finder |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 14 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, architecture-boundary-reviewer, public-addy-agent-security-and-hardening, service-dependency-mapper |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, api-ops-summary-writer, api-documentation-writer, public-anthropic-claude-api, public-openai-cli-creator |
| `public_gold_p34_playwright` | `public-openai-playwright` | 9 | 3 | `public-addy-agent-browser-testing-with-devtools` | wrong | public-addy-agent-browser-testing-with-devtools, public-oh-my-agent-browser, playwright-flow-debugger, public-office-browser-automation, public-n-skills-dev-browser |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 3 | 3 | `web-page-snapshotter` | wrong | web-page-snapshotter, implicit-visual-diff-reviewer, public-openai-screenshot, visual-regression-checker, playwright-flow-debugger |
| `public_gold_p36_sentry` | `public-openai-sentry` | 2 | 2 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, public-openai-sentry, public-swebench-distributed-tracing, public-swebench-analytics-events, dashboard-ops-timeline-builder |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 2 | 2 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, public-openai-transcribe, meeting-notes-action-extractor, meeting-followup-extractor, meeting-ops-rewrite-editor |
| `public_gold_p38_speech` | `public-openai-speech` | 5 | 5 | `public-office-podcast-automation` | wrong | public-office-podcast-automation, public-openai-transcribe, speaker-notes-writer, public-office-transcription-automation, public-openai-speech |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | 3 | 3 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, public-office-data-analysis, public-openai-jupyter-notebook, data-analysis-for-reporting, public-huggingface-datasets |
| `public_gold_p40_linear` | `public-openai-linear` | 1 | 1 | `public-openai-linear` | gold | public-openai-linear, public-mattpocock-to-issues, github-issue-triager, public-office-linear-automation, public-openai-notion-spec-to-implementation |
| `public_gold_p41_yeet` | `public-openai-yeet` | 2 | 2 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, public-openai-yeet, review-comment-resolver, pr-reviewer, public-openai-gh-address-comments |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 11 | 11 | `skill-installer` | wrong | skill-installer, skill-finder, public-skill-installer, public-vercel-find-skills, skill-installer-wrapper |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | 8 | 2 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, notion-research-database-builder, meeting-ops-summary-writer, meeting-followup-extractor, meeting-agenda-builder |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | - | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, meeting-agenda-builder, meeting-ops-summary-writer |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, public-addy-agent-planning-and-task-breakdown, notion-research-database-builder, public-writing-plans, product-ops-handoff-brief-writer |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-create-design-system-rules |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 2 | 2 | `public-openai-figma-code-connect-components` | wrong | public-openai-figma-code-connect-components, public-openai-figma-generate-library, public-openai-figma-implement-design, public-openai-figma-create-design-system-rules, public-openai-figma-generate-design |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 2 | 2 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma-create-design-system-rules, public-openai-figma-generate-library, public-openai-figma-implement-design, public-openai-figma-code-connect-components |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 8 | 1 | `seo-metadata-checker` | acceptable | seo-metadata-checker, web-data-extractor, seo-ops-field-extractor, public-addy-web-core-web-vitals, public-addy-web-web-quality-audit |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 2 | 2 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, public-addy-web-performance, public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, public-addy-web-web-quality-audit |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 1 | 1 | `public-addy-web-web-quality-audit` | gold | public-addy-web-web-quality-audit, web-ops-quality-auditor, web-performance-budget-checker, web-ops-risk-reviewer, seo-ops-quality-auditor |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 1 | 1 | `public-addy-agent-api-and-interface-design` | gold | public-addy-agent-api-and-interface-design, openapi-contract-reviewer, rest-api-contract-designer, openapi-contract-tester, webhook-contract-planner |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 1 | 1 | `public-addy-agent-context-engineering` | gold | public-addy-agent-context-engineering, public-openai-migrate-to-codex, context-compressor, agent-ops-handoff-brief-writer, task-extractor |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | 3 | 3 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, migration-risk-auditor, public-addy-agent-deprecation-and-migration, external-api-integration-planner, database-ops-risk-reviewer |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | 1 | 1 | `public-addy-agent-documentation-and-adrs` | gold | public-addy-agent-documentation-and-adrs, public-mattpocock-improve-codebase-architecture, api-ops-scenario-planner, api-documentation-writer, public-architecture-patterns |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | 2 | 2 | `public-openai-notion-spec-to-implementation` | wrong | public-openai-notion-spec-to-implementation, public-addy-agent-spec-driven-development, product-ops-acceptance-test-builder, ecommerce-ops-acceptance-test-builder, support-ops-acceptance-test-builder |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | 4 | 1 | `public-mattpocock-tdd` | acceptable | public-mattpocock-tdd, ci-failure-debugger, ci-log-root-cause-debugger, public-addy-agent-test-driven-development, public-mattpocock-diagnose |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 6 | 6 | `code-reviewer` | wrong | code-reviewer, security-code-reviewer, public-oh-my-codebase-search, public-addy-agent-code-simplification, public-mattpocock-improve-codebase-architecture |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, public-openai-openai-docs, public-anthropic-mcp-builder, api-design-reviewer, mcp-server-builder |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | - | 2 | `docs-ops-rewrite-editor` | wrong | docs-ops-rewrite-editor, document-rewriter, partnerships-ops-rewrite-editor, document-normaliser, supply-chain-ops-rewrite-editor |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 2 | 2 | `public-office-ppt-visual` | wrong | public-office-ppt-visual, public-anthropic-canvas-design, implicit-visual-diff-reviewer, public-office-infographic, slide-deck-visual-auditor |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 6 | 6 | `public-office-brand-guidelines` | wrong | public-office-brand-guidelines, public-anthropic-frontend-design, public-openai-figma-generate-library, public-addy-agent-frontend-ui-engineering, public-office-ppt-visual |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 2 | 2 | `hf-zerogpu-space-deployer` | wrong | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, hf-local-model-selector, implicit-hf-local-model-chooser, gradio-demo-builder |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-huggingface-llm-trainer, public-huggingface-train-sentence-transformers, public-huggingface-huggingface-vision-trainer, hf-community-eval-runner |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 3 | 1 | `hf-local-model-selector` | acceptable | hf-local-model-selector, implicit-hf-local-model-chooser, public-huggingface-huggingface-local-models, hf-zerogpu-space-deployer, public-huggingface-transformers-js |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 2 | 2 | `hf-community-eval-runner` | wrong | hf-community-eval-runner, public-huggingface-huggingface-trackio, training-ops-comparison-builder, sentence-transformer-finetuner, skill-benchmark-evaluator |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 2 | 2 | `public-huggingface-huggingface-paper-publisher` | wrong | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, paper-summariser, hf-community-eval-runner, multi-source-comparison-builder |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, paper-summariser, public-office-academic-search, publishing-ops-artifact-packager |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 2 | 2 | `gradio-demo-builder` | wrong | gradio-demo-builder, public-huggingface-transformers-js, hf-local-model-selector, public-huggingface-huggingface-gradio, public-oh-my-lmstudio-cli |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, public-obsidian-obsidian-bases, notion-research-database-builder, public-mattpocock-obsidian-vault, public-obsidian-obsidian-cli |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-mattpocock-obsidian-vault, public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-obsidian-json-canvas |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 2 | 1 | `public-mattpocock-obsidian-vault` | acceptable | public-mattpocock-obsidian-vault, public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-obsidian-obsidian-markdown, public-obsidian-obsidian-bases |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 6 | 1 | `xlsx-formula-model-builder` | acceptable | xlsx-formula-model-builder, public-xlsx, spreadsheet-formula-auditor, public-swebench-xlsx, public-office-data-analysis |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 5 | 5 | `public-xlsx` | wrong | public-xlsx, xlsx-formula-model-builder, public-swebench-xlsx, spreadsheet-formula-auditor, public-office-sheets-automation |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 2 | 1 | `airtable-workflow-automator` | acceptable | airtable-workflow-automator, public-office-airtable-automation, public-office-notion-automation, public-oh-my-google-workspace, public-office-gmail-workflows |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 2 | 2 | `public-office-invoice-template` | wrong | public-office-invoice-template, public-office-invoice-automation, public-office-invoice-organizer, invoice-payment-checker, public-office-invoice-generator |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 3 | 3 | `public-office-lead-research` | wrong | public-office-lead-research, public-office-lead-qualification, public-office-lead-routing, sales-ops-monitoring-plan-builder, crm-ops-monitoring-plan-builder |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-dcf-valuation, public-office-subscription-management, public-office-stock-analysis, public-office-data-analysis |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, public-office-dcf-valuation, public-office-crypto-report, public-office-investment-memo, risk-ops-risk-reviewer |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 1 | 1 | `public-office-dcf-valuation` | gold | public-office-dcf-valuation, public-swebench-creating-financial-models, financial-model-builder, finance-ops-scenario-planner, finance-ops-normalizer |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 1 | 1 | `public-office-shopify-automation` | gold | public-office-shopify-automation, public-office-woocommerce-automation, public-office-amazon-seller, ecommerce-ops-timeline-builder, product-ops-monitoring-plan-builder |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 1 | 1 | `public-office-zendesk-automation` | gold | public-office-zendesk-automation, support-ticket-triager, support-ops-ops-intake-classifier, support-ops-ops-monitoring-plan-builder, email-classification-router |
