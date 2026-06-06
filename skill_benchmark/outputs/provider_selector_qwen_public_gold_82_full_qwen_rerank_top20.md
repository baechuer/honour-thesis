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
| Top-1 accuracy | 68.3% |
| Acceptable top-1 accuracy | 79.3% |
| Top-3 recall | 79.3% |
| Top-5 recall | 80.5% |
| Acceptable top-5 recall | 87.8% |
| MRR | 0.739 |
| Non-main top-1 | 91.5% |
| Approx selector-visible tokens | 1367661 |

## API Usage Estimate

- Embedding API calls made in this run: 1
- Embedding cache hits: 2482
- Approx uncached embedding input tokens: 40
- Rerank API calls made in this run: 10
- Rerank cache hits: 72
- Approx uncached rerank input tokens: 115296

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 1 | 1 | `public-office-pdf-extraction` | gold | public-office-pdf-extraction, public-pdf, implicit-pdf-evidence-answerer, implicit-pdf-table-reconstructor, pdf-layout-table-extractor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 1 | `pdf-ocr-cleaner` | acceptable | pdf-ocr-cleaner, pdf-ocr-extractor, public-office-pdf-ocr, implicit-pdf-evidence-answerer, docs-ops-scenario-planner |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, implicit-pdf-evidence-answerer, hr-ops-field-extractor, docs-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, public-office-batch-convert, docs-ops-normalizer, public-office-pdf-converter, office-to-markdown-converter |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, legal-ops-artifact-packager, docs-ops-artifact-packager, public-pdf, docs-ops-normalizer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, public-office-browser-automation, public-openai-playwright, frontend-debugger, public-oh-my-playwriter |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | - | 1 | `accessibility-interaction-auditor` | acceptable | accessibility-interaction-auditor, accessibility-checker, product-ops-quality-auditor, product-ops-compliance-checker, ecommerce-ops-quality-auditor |
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
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 1 | `public-office-etl-pipeline` | acceptable | public-office-etl-pipeline, public-office-data-pipeline, dataset-ops-timeline-builder, dataset-ops-dependency-mapper, public-office-data-extractor |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 1 | 1 | `public-office-database-sync` | gold | public-office-database-sync, database-schema-designer, database-ops-comparison-builder, database-ops-resource-linker, database-ops-dependency-mapper |
| `public_gold_p27_contract_review` | `public-office-contract-review` | - | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-quality-auditor, contract-ops-scenario-planner |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-risk-reviewer, email-ops-priority-ranker, email-ops-evidence-grounder, email-ops-intake-classifier |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 1 | 1 | `public-office-ai-slides` | gold | public-office-ai-slides, slide-outline-builder, public-oh-my-presentation-builder, public-office-ppt-visual, public-office-md-slides |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 2 | 2 | `public-openai-figma` | wrong | public-openai-figma, public-openai-figma-implement-design, public-openai-figma-use, public-openai-figma-generate-design, public-anthropic-frontend-design |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 1 | `skill-creator` | acceptable | skill-creator, public-skill-creator, skill-authoring-guide, public-anthropic-doc-coauthoring, public-oh-my-workflow-automation |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 10 | 10 | `security-ops-risk-reviewer` | wrong | security-ops-risk-reviewer, api-security-threat-reviewer, repo-ops-risk-reviewer, security-ops-dependency-mapper, security-ops-quality-auditor |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, public-openai-migrate-to-codex, public-oh-my-api-documentation, public-openai-chatgpt-apps, api-documentation-writer |
| `public_gold_p34_playwright` | `public-openai-playwright` | 1 | 1 | `public-openai-playwright` | gold | public-openai-playwright, public-office-browser-automation, public-playwright-interactive, public-addy-agent-browser-testing-with-devtools, web-ops-acceptance-test-builder |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 4 | 4 | `public-openai-playwright` | wrong | public-openai-playwright, web-ops-acceptance-test-builder, web-ops-quality-auditor, public-openai-screenshot, public-playwright-interactive |
| `public_gold_p36_sentry` | `public-openai-sentry` | 1 | 1 | `public-openai-sentry` | gold | public-openai-sentry, metrics-root-cause-diagnoser, implicit-trace-path-diagnoser, incident-ops-dependency-mapper, dashboard-ops-dependency-mapper |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 1 | 1 | `public-openai-transcribe` | gold | public-openai-transcribe, public-office-transcription-automation, public-addy-agent-interview-me, recruiting-ops-timeline-builder, recruiting-ops-rewrite-editor |
| `public_gold_p38_speech` | `public-openai-speech` | 1 | 1 | `public-openai-speech` | gold | public-openai-speech, public-office-podcast-automation, speaker-notes-writer, media-ops-rewrite-editor, media-ops-quality-auditor |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | - | - | `public-office-data-analysis` | wrong | public-office-data-analysis, dataset-ops-dependency-mapper, dataset-ops-normalizer, dataset-ops-rewrite-editor, dataset-ops-field-extractor |
| `public_gold_p40_linear` | `public-openai-linear` | - | - | `public-office-linear-automation` | wrong | public-office-linear-automation, public-lbussell-creating-issues, public-mattpocock-to-issues, repo-ops-timeline-builder, repo-ops-dependency-mapper |
| `public_gold_p41_yeet` | `public-openai-yeet` | - | 3 | `version-control-helper` | wrong | version-control-helper, repo-ops-artifact-packager, public-addy-agent-git-workflow-and-versioning, git-commit-writer, public-lbussell-creating-pull-requests |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 1 | 1 | `public-openai-migrate-to-codex` | gold | public-openai-migrate-to-codex, public-oh-my-system-environment-setup, skill-authoring-guide, public-oh-my-environment-setup, agent-ops-dependency-mapper |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | - | 19 | `public-openai-notion-meeting-intelligence` | wrong | public-openai-notion-meeting-intelligence, knowledge-ops-summary-writer, meeting-ops-summary-writer, meeting-ops-resource-linker, meeting-ops-evidence-grounder |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | - | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-ops-normalizer, meeting-ops-dependency-mapper, meeting-ops-timeline-builder, meeting-ops-handoff-brief-writer |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, engineering-design-ops-dependency-mapper, engineering-design-ops-handoff-brief-writer, product-ops-acceptance-test-builder, product-ops-dependency-mapper |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-implement-design, public-openai-figma, public-openai-figma-generate-design, public-openai-figma-use |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 1 | 1 | `public-openai-figma-generate-library` | gold | public-openai-figma-generate-library, public-openai-figma-create-design-system-rules, public-openai-figma-code-connect-components, public-openai-figma-generate-design, public-openai-figma-use |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 1 | 1 | `public-openai-figma-create-design-system-rules` | gold | public-openai-figma-create-design-system-rules, public-openai-figma-use, public-openai-figma-generate-design, public-oh-my-frontend-design-system, public-openai-figma |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 12 | 1 | `seo-metadata-checker` | acceptable | seo-metadata-checker, seo-ops-quality-auditor, seo-ops-resource-linker, seo-ops-dependency-mapper, seo-ops-evidence-grounder |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 1 | 1 | `public-addy-web-performance` | gold | public-addy-web-performance, public-addy-web-web-quality-audit, web-ops-quality-auditor, public-addy-web-core-web-vitals, web-ops-priority-ranker |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 1 | 1 | `public-addy-web-web-quality-audit` | gold | public-addy-web-web-quality-audit, web-ops-quality-auditor, web-ops-priority-ranker, seo-ops-quality-auditor, web-ops-risk-reviewer |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 1 | 1 | `public-addy-agent-api-and-interface-design` | gold | public-addy-agent-api-and-interface-design, rest-api-contract-designer, api-design-reviewer, openapi-contract-tester, public-api-design-principles |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 1 | 1 | `public-addy-agent-context-engineering` | gold | public-addy-agent-context-engineering, context-compressor, file-organiser, subagent-task-planner, refactor-planner |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | - | - | `api-ops-timeline-builder` | wrong | api-ops-timeline-builder, api-ops-scenario-planner, api-ops-handoff-brief-writer, api-integration-planner, deployment-rollback-planner |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | - | - | `engineering-design-ops-dependency-mapper` | wrong | engineering-design-ops-dependency-mapper, public-mattpocock-improve-codebase-architecture, analytics-ops-dependency-mapper, api-ops-dependency-mapper, database-ops-dependency-mapper |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | - | - | `product-ops-acceptance-test-builder` | wrong | product-ops-acceptance-test-builder, product-ops-monitoring-plan-builder, ux-ops-acceptance-test-builder, product-ops-risk-reviewer, product-ops-handoff-brief-writer |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | - | - | `refactor-planner` | wrong | refactor-planner, mobile-ops-acceptance-test-builder, ci-failure-debugger, implicit-ci-failure-reader, mobile-ops-normalizer |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 2 | 2 | `refactor-planner` | wrong | refactor-planner, public-addy-agent-source-driven-development, public-mattpocock-improve-codebase-architecture, public-oh-my-code-refactoring, public-oh-my-improve-codebase-architecture |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, public-anthropic-mcp-builder, public-oh-my-claudekit, public-anthropic-internal-comms, public-office-office-mcp |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | - | 5 | `docs-ops-rewrite-editor` | wrong | docs-ops-rewrite-editor, construction-ops-rewrite-editor, partnerships-ops-rewrite-editor, product-ops-rewrite-editor, document-rewriter |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 1 | 1 | `public-anthropic-canvas-design` | gold | public-anthropic-canvas-design, public-obsidian-json-canvas, public-office-ppt-visual, public-office-infographic, deck-template-applier |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 1 | 1 | `public-anthropic-theme-factory` | gold | public-anthropic-theme-factory, public-openai-figma-generate-design, public-openai-figma-generate-library, public-oh-my-frontend-design-system, public-oh-my-design-system |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 1 | 1 | `public-huggingface-huggingface-zerogpu` | gold | public-huggingface-huggingface-zerogpu, hf-zerogpu-space-deployer, public-huggingface-huggingface-gradio, public-huggingface-huggingface-trackio, public-huggingface-huggingface-local-models |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 1 | 1 | `public-huggingface-huggingface-llm-trainer` | gold | public-huggingface-huggingface-llm-trainer, sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, training-ops-normalizer, training-ops-quality-auditor |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 2 | 1 | `implicit-hf-local-model-chooser` | acceptable | implicit-hf-local-model-chooser, public-huggingface-huggingface-local-models, hf-local-model-selector, public-huggingface-transformers-js, public-huggingface-hf-cli |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 1 | 1 | `public-huggingface-huggingface-trackio` | gold | public-huggingface-huggingface-trackio, public-huggingface-huggingface-llm-trainer, ml-ops-quality-auditor, ml-ops-normalizer, ml-ops-artifact-packager |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 1 | 1 | `public-huggingface-huggingface-papers` | gold | public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher, public-huggingface-hf-cli, public-huggingface-huggingface-best, multi-source-comparison-builder |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, publishing-ops-artifact-packager, publishing-ops-dependency-mapper, publishing-ops-resource-linker |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 1 | 1 | `public-huggingface-transformers-js` | gold | public-huggingface-transformers-js, gradio-demo-builder, public-huggingface-huggingface-gradio, public-huggingface-huggingface-zerogpu, public-huggingface-huggingface-llm-trainer |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, public-obsidian-obsidian-bases, public-oh-my-obsidian, public-oh-my-obsidian-cli, public-obsidian-obsidian-cli |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-mattpocock-obsidian-vault, public-oh-my-obsidian, public-office-obsidian-automation, public-obsidian-obsidian-cli |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 1 | 1 | `public-obsidian-obsidian-cli` | gold | public-obsidian-obsidian-cli, public-mattpocock-obsidian-vault, public-oh-my-obsidian-cli, public-oh-my-obsidian, public-office-obsidian-automation |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 1 | 1 | `public-office-excel-automation` | gold | public-office-excel-automation, public-office-xlsx-manipulation, public-office-sheets-automation, public-swebench-xlsx, public-xlsx |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 1 | 1 | `public-office-sheets-automation` | gold | public-office-sheets-automation, public-swebench-xlsx, public-office-excel-automation, public-xlsx, public-oh-my-google-workspace |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 1 | 1 | `public-office-airtable-automation` | gold | public-office-airtable-automation, airtable-workflow-automator, customer-success-ops-field-extractor, customer-success-ops-normalizer, email-ops-handoff-brief-writer |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 2 | 2 | `public-office-quickbooks-automation` | wrong | public-office-quickbooks-automation, public-office-invoice-automation, public-office-invoice-organizer, finance-ops-field-extractor, public-office-invoice-template |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 3 | 3 | `crm-ops-priority-ranker` | wrong | crm-ops-priority-ranker, sales-ops-priority-ranker, public-office-lead-routing, crm-ops-intake-classifier, crm-ops-dependency-mapper |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-subscription-management, financial-report-writer, finance-ops-field-extractor, finance-ops-artifact-packager |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, public-office-company-research, data-analysis-for-reporting, data-analysis-for-forecasting, data-analysis-overview |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 1 | 1 | `public-office-dcf-valuation` | gold | public-office-dcf-valuation, financial-model-builder, finance-ops-priority-ranker, finance-ops-scenario-planner, finance-ops-handoff-brief-writer |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 1 | 1 | `public-office-shopify-automation` | gold | public-office-shopify-automation, ecommerce-ops-resource-linker, ecommerce-ops-dependency-mapper, ecommerce-ops-priority-ranker, ecommerce-ops-scenario-planner |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 1 | 1 | `public-office-zendesk-automation` | gold | public-office-zendesk-automation, support-ticket-triager, support-ops-ops-intake-classifier, support-ops-intake-classifier, support-ops-ops-priority-ranker |
