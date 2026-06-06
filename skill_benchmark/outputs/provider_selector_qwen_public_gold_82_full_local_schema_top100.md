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
| Top-1 accuracy | 25.6% |
| Acceptable top-1 accuracy | 46.3% |
| Top-3 recall | 58.5% |
| Top-5 recall | 72.0% |
| Acceptable top-5 recall | 82.9% |
| MRR | 0.454 |
| Non-main top-1 | 47.6% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 49
- Embedding cache hits: 2434
- Approx uncached embedding input tokens: 2402
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 4 | 4 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, pdf-ocr-extractor, implicit-pdf-evidence-answerer, public-office-pdf-extraction, implicit-pdf-table-reconstructor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 11 | 1 | `pdf-ocr-cleaner` | acceptable | pdf-ocr-cleaner, pdf-ocr-extractor, implicit-pdf-evidence-answerer, pdf-layout-reviewer, pdf-to-docx-converter |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, document-field-extractor, implicit-pdf-evidence-answerer, pdf-layout-table-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 2 | 2 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, public-markitdown, pdf-to-docx-converter, public-office-pdf-ocr, public-office-pdf-to-docx |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-pdf-watermark, pdf-to-docx-converter, implicit-pdf-evidence-answerer, docs-ops-summary-writer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 3 | 3 | `frontend-debugger` | wrong | frontend-debugger, playwright-flow-debugger, public-addy-agent-browser-testing-with-devtools, web-page-snapshotter, implicit-browser-flow-investigator |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 6 | 1 | `accessibility-checker` | acceptable | accessibility-checker, accessibility-interaction-auditor, pdf-layout-reviewer, product-ops-compliance-checker, product-ops-comparison-builder |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, accessibility-checker, web-performance-budget-checker, web-ops-risk-reviewer, web-ops-monitoring-plan-builder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `frontend-debugger` | wrong | frontend-debugger, resilience-pattern-reviewer, geospatial-ops-failure-diagnoser, geospatial-ops-quality-auditor, geospatial-ops-acceptance-test-builder |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 5 | 1 | `ci-log-root-cause-debugger` | acceptable | ci-log-root-cause-debugger, ci-failure-debugger, repo-ops-failure-diagnoser, deployment-build-triager, public-swebench-analyze-ci |
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
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 1 | `gradio-demo-builder` | acceptable | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 2 | 2 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-huggingface-vision-trainer, hf-local-model-selector, implicit-hf-dataset-inspector, public-huggingface-huggingface-llm-trainer |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 1 | `sentence-transformer-finetuner` | acceptable | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, hf-local-model-selector, gradio-demo-builder, public-huggingface-transformers-js |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, hf-dataset-viewer-inspector, public-huggingface-datasets, public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 1 | `public-office-etl-pipeline` | acceptable | public-office-etl-pipeline, public-office-data-pipeline, ci-cd-pipeline-builder, dataset-ops-comparison-builder, public-office-data-analysis |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 5 | 5 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, external-api-integration-planner, database-ops-monitoring-plan-builder, geospatial-ops-monitoring-plan-builder, public-office-database-sync |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 9 | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, vendor-ops-summary-writer, contract-ops-summary-writer, contract-ops-risk-reviewer, vendor-ops-risk-reviewer |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, reply-polisher, professor-email-reply, reply-drafter, email-polisher |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 3 | 3 | `slide-deck-visual-auditor` | wrong | slide-deck-visual-auditor, slide-outline-builder, public-office-ai-slides, deck-template-applier, public-office-ppt-visual |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 2 | 2 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-code-connect-components, public-openai-figma, public-openai-figma-generate-library |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 5 | 1 | `skill-creator` | acceptable | skill-creator, skill-authoring-guide, skill-finder, skill-editor, public-skill-creator |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | - | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, architecture-boundary-reviewer, api-security-threat-reviewer, security-ops-risk-reviewer |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, api-ops-summary-writer, public-anthropic-claude-api, api-documentation-writer, public-openai-cli-creator |
| `public_gold_p34_playwright` | `public-openai-playwright` | 9 | 1 | `playwright-flow-debugger` | acceptable | playwright-flow-debugger, public-addy-agent-browser-testing-with-devtools, web-form-filler, public-office-browser-automation, public-n-skills-dev-browser |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 8 | 8 | `web-page-snapshotter` | wrong | web-page-snapshotter, implicit-visual-diff-reviewer, playwright-flow-debugger, visual-regression-checker, web-ops-quality-auditor |
| `public_gold_p36_sentry` | `public-openai-sentry` | 3 | 3 | `distributed-trace-investigator` | wrong | distributed-trace-investigator, dashboard-ops-timeline-builder, public-openai-sentry, metrics-root-cause-diagnoser, implicit-trace-path-diagnoser |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 4 | 4 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-ops-rewrite-editor, meeting-notes-action-extractor, public-openai-transcribe, meeting-followup-extractor |
| `public_gold_p38_speech` | `public-openai-speech` | 6 | 6 | `public-office-podcast-automation` | wrong | public-office-podcast-automation, public-openai-transcribe, speaker-notes-writer, media-ops-summary-writer, media-ops-rewrite-editor |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | 6 | 6 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, public-office-data-analysis, data-analysis-for-reporting, dataset-ops-rewrite-editor |
| `public_gold_p40_linear` | `public-openai-linear` | 4 | 4 | `github-issue-triager` | wrong | github-issue-triager, public-mattpocock-to-issues, public-office-linear-automation, public-openai-linear, pr-review-comment-resolver |
| `public_gold_p41_yeet` | `public-openai-yeet` | 12 | 12 | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, pr-reviewer, review-comment-resolver, changelog-writer, release-changelog-generator |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 11 | 11 | `skill-installer` | wrong | skill-installer, skill-finder, skill-authoring-guide, public-skill-installer, skill-installer-wrapper |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | 11 | 2 | `meeting-notes-action-extractor` | wrong | meeting-notes-action-extractor, notion-research-database-builder, meeting-ops-summary-writer, knowledge-ops-summary-writer, meeting-agenda-builder |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | - | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-followup-extractor, meeting-agenda-builder, meeting-summary-writer, meeting-ops-summary-writer |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, notion-research-database-builder, product-ops-handoff-brief-writer, product-ops-acceptance-test-builder, product-ops-timeline-builder |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-create-design-system-rules |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 2 | 2 | `public-openai-figma-code-connect-components` | wrong | public-openai-figma-code-connect-components, public-openai-figma-generate-library, public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-create-design-system-rules |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 3 | 3 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-openai-figma-create-design-system-rules, public-openai-figma-implement-design, public-openai-figma-generate-library |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 13 | 1 | `seo-metadata-checker` | acceptable | seo-metadata-checker, web-data-extractor, seo-ops-field-extractor, seo-ops-normalizer, accessibility-interaction-auditor |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 4 | 4 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, public-addy-web-core-web-vitals, code-reviewer, public-addy-web-performance, frontend-debugger |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 1 | 1 | `public-addy-web-web-quality-audit` | gold | public-addy-web-web-quality-audit, web-ops-quality-auditor, web-ops-risk-reviewer, seo-ops-quality-auditor, web-performance-budget-checker |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 3 | 3 | `openapi-contract-reviewer` | wrong | openapi-contract-reviewer, rest-api-contract-designer, public-addy-agent-api-and-interface-design, openapi-contract-tester, api-documentation-writer |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 3 | 3 | `context-compressor` | wrong | context-compressor, public-openai-migrate-to-codex, public-addy-agent-context-engineering, file-organiser, agent-ops-handoff-brief-writer |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | - | - | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, migration-risk-auditor, external-api-integration-planner, database-ops-monitoring-plan-builder, api-ops-monitoring-plan-builder |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | 8 | 8 | `api-ops-scenario-planner` | wrong | api-ops-scenario-planner, database-ops-scenario-planner, api-ops-handoff-brief-writer, architecture-boundary-reviewer, api-documentation-writer |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | - | - | `product-ops-acceptance-test-builder` | wrong | product-ops-acceptance-test-builder, product-ops-compliance-checker, ux-ops-acceptance-test-builder, api-ops-acceptance-test-builder, engineering-design-ops-acceptance-test-builder |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | - | - | `ci-failure-debugger` | wrong | ci-failure-debugger, ci-log-root-cause-debugger, web-ui-tester, implicit-ci-failure-reader, refactor-planner |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 14 | 14 | `code-reviewer` | wrong | code-reviewer, security-code-reviewer, public-addy-agent-code-simplification, review-comment-resolver, code-documentation-writer |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, api-design-reviewer, mcp-server-builder, public-openai-openai-docs, public-anthropic-mcp-builder |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | - | 3 | `docs-ops-rewrite-editor` | wrong | docs-ops-rewrite-editor, partnerships-ops-rewrite-editor, document-rewriter, construction-ops-rewrite-editor, docx-redline-editor |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 3 | 3 | `public-office-ppt-visual` | wrong | public-office-ppt-visual, slide-deck-visual-auditor, public-anthropic-canvas-design, implicit-visual-diff-reviewer, public-office-infographic |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 2 | 2 | `public-office-brand-guidelines` | wrong | public-office-brand-guidelines, public-anthropic-theme-factory, public-anthropic-brand-guidelines, slide-deck-visual-auditor, public-anthropic-frontend-design |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 2 | 2 | `hf-zerogpu-space-deployer` | wrong | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, hf-local-model-selector, implicit-hf-local-model-chooser, gradio-demo-builder |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 3 | 3 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, hf-community-eval-runner, public-huggingface-huggingface-llm-trainer, ml-ops-normalizer, implicit-hf-dataset-inspector |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 4 | 1 | `hf-local-model-selector` | acceptable | hf-local-model-selector, implicit-hf-local-model-chooser, hf-zerogpu-space-deployer, public-huggingface-huggingface-local-models, public-huggingface-huggingface-llm-trainer |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 2 | 2 | `hf-community-eval-runner` | wrong | hf-community-eval-runner, public-huggingface-huggingface-trackio, training-ops-comparison-builder, sentence-transformer-finetuner, ml-ops-comparison-builder |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 1 | 1 | `public-huggingface-huggingface-papers` | gold | public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher, paper-summariser, multi-source-comparison-builder, hf-community-eval-runner |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, paper-summariser, research-ops-artifact-packager, publishing-ops-artifact-packager |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 3 | 3 | `gradio-demo-builder` | wrong | gradio-demo-builder, hf-local-model-selector, public-huggingface-transformers-js, public-huggingface-huggingface-gradio, public-oh-my-lmstudio-cli |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, public-obsidian-obsidian-bases, notion-research-database-builder, public-obsidian-obsidian-cli, public-mattpocock-obsidian-vault |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-mattpocock-obsidian-vault, public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-obsidian-json-canvas |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 2 | 1 | `public-mattpocock-obsidian-vault` | acceptable | public-mattpocock-obsidian-vault, public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-obsidian-obsidian-markdown, public-office-obsidian-automation |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 5 | 1 | `xlsx-formula-model-builder` | acceptable | xlsx-formula-model-builder, spreadsheet-formula-auditor, public-xlsx, public-swebench-xlsx, public-office-excel-automation |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 2 | 2 | `xlsx-formula-model-builder` | wrong | xlsx-formula-model-builder, public-office-sheets-automation, spreadsheet-formula-auditor, public-xlsx, public-swebench-xlsx |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 2 | 1 | `airtable-workflow-automator` | acceptable | airtable-workflow-automator, public-office-airtable-automation, public-office-notion-automation, notion-research-database-builder, crm-ops-monitoring-plan-builder |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 4 | 4 | `invoice-payment-checker` | wrong | invoice-payment-checker, public-office-invoice-template, public-office-invoice-organizer, public-office-invoice-automation, public-office-invoice-generator |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 9 | 9 | `public-office-lead-research` | wrong | public-office-lead-research, sales-ops-monitoring-plan-builder, crm-ops-monitoring-plan-builder, crm-ops-intake-classifier, sales-ops-intake-classifier |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-dcf-valuation, public-office-subscription-management, churn-risk-analyser, data-analysis-for-reporting |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, public-office-dcf-valuation, warehouse-ops-risk-reviewer, risk-ops-risk-reviewer, data-analysis-for-forecasting |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 1 | 1 | `public-office-dcf-valuation` | gold | public-office-dcf-valuation, financial-model-builder, finance-ops-scenario-planner, finance-ops-normalizer, public-swebench-creating-financial-models |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 1 | 1 | `public-office-shopify-automation` | gold | public-office-shopify-automation, ecommerce-ops-timeline-builder, public-office-woocommerce-automation, ecommerce-ops-normalizer, ecommerce-ops-artifact-packager |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 3 | 3 | `support-ticket-triager` | wrong | support-ticket-triager, support-ops-ops-intake-classifier, public-office-zendesk-automation, support-ops-ops-monitoring-plan-builder, support-ops-ops-timeline-builder |
