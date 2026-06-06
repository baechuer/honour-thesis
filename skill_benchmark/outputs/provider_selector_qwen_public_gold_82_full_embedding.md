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
| Top-1 accuracy | 31.7% |
| Acceptable top-1 accuracy | 50.0% |
| Top-3 recall | 52.4% |
| Top-5 recall | 58.5% |
| Acceptable top-5 recall | 69.5% |
| MRR | 0.448 |
| Non-main top-1 | 53.7% |
| Approx selector-visible tokens | 1252365 |

## API Usage Estimate

- Embedding API calls made in this run: 50
- Embedding cache hits: 2433
- Approx uncached embedding input tokens: 2453
- Rerank API calls made in this run: 0
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 0

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 5 | 5 | `pdf-layout-table-extractor` | wrong | pdf-layout-table-extractor, implicit-pdf-table-reconstructor, pdf-ocr-extractor, vendor-ops-field-extractor, public-office-pdf-extraction |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 15 | 1 | `pdf-ocr-cleaner` | acceptable | pdf-ocr-cleaner, pdf-ocr-extractor, pdf-to-docx-converter, pdf-layout-reviewer, pdf-question-answerer |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, hr-ops-field-extractor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 3 | 3 | `office-to-markdown-converter` | wrong | office-to-markdown-converter, layout-preserving-converter, public-markitdown, pdf-to-docx-converter, document-converter |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, docs-ops-artifact-packager, pdf-to-docx-converter, pdf-redaction-reviewer, multi-document-comparison-preparer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 7 | 7 | `playwright-flow-debugger` | wrong | playwright-flow-debugger, implicit-browser-flow-investigator, web-page-snapshotter, frontend-debugger, web-ui-tester |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | - | 1 | `accessibility-interaction-auditor` | acceptable | accessibility-interaction-auditor, accessibility-checker, product-ops-compliance-checker, product-ops-comparison-builder, product-ops-rewrite-editor |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 2 | 2 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, public-addy-web-core-web-vitals, frontend-debugger, implicit-browser-flow-investigator, web-ops-evidence-grounder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `geospatial-ops-failure-diagnoser` | wrong | geospatial-ops-failure-diagnoser, geospatial-ops-quality-auditor, geospatial-ops-acceptance-test-builder, geospatial-ops-evidence-grounder, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 10 | 1 | `ci-failure-debugger` | acceptable | ci-failure-debugger, ci-log-root-cause-debugger, implicit-ci-failure-reader, review-comment-resolver, pr-review-comment-resolver |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 2 | 2 | `git-safety-guardrail-installer` | wrong | git-safety-guardrail-installer, public-mattpocock-setup-pre-commit, repo-code-reviewer, code-reviewer, release-changelog-generator |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-oh-my-git-guardrails-claude-code, version-control-helper, repo-code-reviewer |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | - | - | `review-comment-resolver` | wrong | review-comment-resolver, pr-review-comment-resolver, implicit-review-comment-planner, pr-reviewer, code-reviewer |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, public-openai-vercel-deploy, public-oh-my-vercel-deploy, deployment-release-verifier, public-oh-my-vercel-react-best-practices |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, public-netlify-deploy, deployment-build-triager, deployment-release-verifier, public-openai-render-deploy |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-netlify-deploy, deployment-build-triager, public-oh-my-vercel-deploy, public-openai-vercel-deploy |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 5 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, rest-api-contract-designer, public-swebench-mcp-builder, api-documentation-writer, public-anthropic-mcp-builder |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, mcp-server-builder, api-documentation-writer, public-swebench-mcp-builder, rest-api-contract-designer |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 7 | 7 | `api-documentation-writer` | wrong | api-documentation-writer, rest-api-contract-designer, openapi-contract-reviewer, mcp-server-builder, external-api-integration-planner |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 2 | 2 | `hf-dataset-viewer-inspector` | wrong | hf-dataset-viewer-inspector, public-huggingface-datasets, implicit-hf-dataset-inspector, dataset-ops-summary-writer, dataset-ops-comparison-builder |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 2 | 1 | `gradio-demo-builder` | acceptable | gradio-demo-builder, public-huggingface-huggingface-gradio, hf-zerogpu-space-deployer, implicit-hf-dataset-inspector, hf-dataset-viewer-inspector |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, sentence-transformer-finetuner, implicit-hf-dataset-inspector, ml-ops-normalizer, implicit-hf-local-model-chooser |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 1 | `sentence-transformer-finetuner` | acceptable | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, gradio-demo-builder, public-huggingface-transformers-js, implicit-hf-local-model-chooser |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, public-huggingface-datasets, hf-zerogpu-space-deployer |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 1 | `public-office-etl-pipeline` | acceptable | public-office-etl-pipeline, public-office-data-pipeline, public-office-database-sync, dataset-ops-timeline-builder, public-office-data-analysis |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 2 | 2 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, public-office-database-sync, migration-risk-auditor, database-ops-comparison-builder, database-ops-normalizer |
| `public_gold_p27_contract_review` | `public-office-contract-review` | - | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-risk-reviewer, vendor-ops-handoff-brief-writer, vendor-ops-rewrite-editor |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-risk-reviewer, email-polisher, reply-polisher, email-ops-evidence-grounder |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 6 | 6 | `slide-outline-builder` | wrong | slide-outline-builder, slide-deck-visual-auditor, deck-template-applier, speaker-notes-writer, public-office-ppt-visual |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 3 | 3 | `public-openai-figma-generate-design` | wrong | public-openai-figma-generate-design, public-openai-figma, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-code-connect-components |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 6 | 1 | `skill-creator` | acceptable | skill-creator, skill-authoring-guide, public-oh-my-workflow-automation, code-documentation-writer, skill-finder |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 16 | 2 | `privacy-risk-reviewer` | wrong | privacy-risk-reviewer, security-threat-modeler, security-ops-quality-auditor, security-ops-risk-reviewer, security-ops-normalizer |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, public-openai-cli-creator, public-openai-migrate-to-codex, public-oh-my-lmstudio-cli, public-anthropic-claude-api |
| `public_gold_p34_playwright` | `public-openai-playwright` | 19 | 3 | `web-form-filler` | wrong | web-form-filler, web-ui-tester, playwright-flow-debugger, web-page-snapshotter, implicit-browser-flow-investigator |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 11 | 11 | `web-page-snapshotter` | wrong | web-page-snapshotter, playwright-flow-debugger, implicit-browser-flow-investigator, web-ops-artifact-packager, implicit-visual-diff-reviewer |
| `public_gold_p36_sentry` | `public-openai-sentry` | 8 | 8 | `implicit-trace-path-diagnoser` | wrong | implicit-trace-path-diagnoser, slo-breach-narrative-writer, incident-summary-writer, metrics-root-cause-diagnoser, distributed-trace-investigator |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 12 | 12 | `meeting-ops-summary-writer` | wrong | meeting-ops-summary-writer, meeting-ops-quality-auditor, meeting-ops-timeline-builder, meeting-ops-field-extractor, meeting-ops-handoff-brief-writer |
| `public_gold_p38_speech` | `public-openai-speech` | 17 | 17 | `speaker-notes-writer` | wrong | speaker-notes-writer, media-ops-summary-writer, media-ops-artifact-packager, media-ops-handoff-brief-writer, media-ops-rewrite-editor |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | - | - | `implicit-hf-dataset-inspector` | wrong | implicit-hf-dataset-inspector, hf-dataset-viewer-inspector, data-analysis-for-reporting, dataset-ops-summary-writer, dataset-ops-rewrite-editor |
| `public_gold_p40_linear` | `public-openai-linear` | - | - | `pr-review-comment-resolver` | wrong | pr-review-comment-resolver, public-mattpocock-to-issues, implicit-review-comment-planner, public-office-linear-automation, product-ops-dependency-mapper |
| `public_gold_p41_yeet` | `public-openai-yeet` | - | 12 | `pr-reviewer` | wrong | pr-reviewer, pr-review-comment-resolver, code-reviewer, release-note-writer, changelog-writer |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 13 | 13 | `public-oh-my-environment-setup` | wrong | public-oh-my-environment-setup, public-oh-my-system-environment-setup, skill-authoring-guide, public-skill-installer, skill-installer |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | - | 11 | `task-extractor` | wrong | task-extractor, meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, meeting-agenda-builder |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | - | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, meeting-ops-summary-writer, meeting-agenda-builder |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, product-ops-dependency-mapper, product-ops-handoff-brief-writer, notion-research-database-builder, product-ops-normalizer |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-generate-design, public-openai-figma-implement-design, public-openai-figma-generate-library, public-openai-figma-create-design-system-rules |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 1 | 1 | `public-openai-figma-generate-library` | gold | public-openai-figma-generate-library, public-openai-figma-create-design-system-rules, public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-oh-my-design-system |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 1 | 1 | `public-openai-figma-create-design-system-rules` | gold | public-openai-figma-create-design-system-rules, public-openai-figma-generate-library, public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-openai-figma-implement-design |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 12 | 1 | `seo-metadata-checker` | acceptable | seo-metadata-checker, seo-ops-field-extractor, seo-ops-normalizer, landing-page-copy-reviewer, seo-ops-evidence-grounder |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 7 | 7 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, web-page-snapshotter, implicit-browser-flow-investigator, public-addy-web-core-web-vitals, web-ops-summary-writer |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 3 | 3 | `web-ops-quality-auditor` | wrong | web-ops-quality-auditor, web-ops-risk-reviewer, public-addy-web-web-quality-audit, web-performance-budget-checker, seo-ops-quality-auditor |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 5 | 4 | `rest-api-contract-designer` | wrong | rest-api-contract-designer, api-documentation-writer, openapi-contract-reviewer, public-api-design-principles, public-addy-agent-api-and-interface-design |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 12 | 12 | `refactor-planner` | wrong | refactor-planner, public-oh-my-code-review, public-addy-agent-code-review-and-quality, public-addy-agent-code-simplification, public-oh-my-codebase-search |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | - | - | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, migration-risk-auditor, database-ops-timeline-builder, external-api-integration-planner, database-ops-handoff-brief-writer |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | - | - | `architecture-boundary-reviewer` | wrong | architecture-boundary-reviewer, resilience-pattern-reviewer, auth-flow-integrator, service-dependency-mapper, database-ops-scenario-planner |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | - | - | `product-ops-normalizer` | wrong | product-ops-normalizer, product-ops-quality-auditor, product-ops-acceptance-test-builder, product-ops-timeline-builder, product-ops-rewrite-editor |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | - | - | `implicit-ci-failure-reader` | wrong | implicit-ci-failure-reader, auth-flow-integrator, ci-log-root-cause-debugger, ci-failure-debugger, frontend-debugger |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 10 | 10 | `code-reviewer` | wrong | code-reviewer, public-addy-agent-code-simplification, implicit-ci-failure-reader, refactor-planner, security-code-reviewer |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, public-anthropic-mcp-builder, rest-api-contract-designer, public-office-mcp-hub, api-design-reviewer |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | - | 17 | `partnerships-ops-rewrite-editor` | wrong | partnerships-ops-rewrite-editor, partnerships-ops-summary-writer, partnerships-ops-handoff-brief-writer, docs-ops-rewrite-editor, partnerships-ops-normalizer |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 3 | 3 | `chart-caption-writer` | wrong | chart-caption-writer, slide-deck-visual-auditor, public-anthropic-canvas-design, slide-outline-builder, implicit-browser-flow-investigator |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 3 | 3 | `slide-deck-visual-auditor` | wrong | slide-deck-visual-auditor, public-oh-my-web-design-guidelines, public-anthropic-theme-factory, public-oh-my-design-system, public-office-brand-guidelines |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 2 | 2 | `hf-zerogpu-space-deployer` | wrong | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, implicit-hf-local-model-chooser, hf-local-model-selector, gradio-demo-builder |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 11 | 11 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, implicit-hf-dataset-inspector, ml-ops-rewrite-editor, training-ops-normalizer, dataset-ops-rewrite-editor |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 4 | 1 | `hf-local-model-selector` | acceptable | hf-local-model-selector, implicit-hf-local-model-chooser, hf-zerogpu-space-deployer, public-huggingface-huggingface-local-models, public-huggingface-huggingface-zerogpu |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 1 | 1 | `public-huggingface-huggingface-trackio` | gold | public-huggingface-huggingface-trackio, hf-community-eval-runner, training-ops-comparison-builder, implicit-hf-dataset-inspector, gradio-demo-builder |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 1 | 1 | `public-huggingface-huggingface-papers` | gold | public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher, implicit-hf-local-model-chooser, hf-local-model-selector, paper-summariser |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, research-ops-artifact-packager, paper-summariser, method-note-builder |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 1 | 1 | `public-huggingface-transformers-js` | gold | public-huggingface-transformers-js, gradio-demo-builder, public-huggingface-huggingface-gradio, sentence-transformer-finetuner, hf-local-model-selector |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, thesis-ops-dependency-mapper, research-ops-dependency-mapper, notion-research-database-builder, public-obsidian-obsidian-bases |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-obsidian-obsidian-cli, public-mattpocock-obsidian-vault, public-oh-my-obsidian-cli, public-oh-my-obsidian-cli-uri-fallback |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 1 | 1 | `public-obsidian-obsidian-cli` | gold | public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-mattpocock-obsidian-vault, public-oh-my-obsidian-cli-uri-fallback, public-office-obsidian-automation |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 2 | 1 | `xlsx-formula-model-builder` | acceptable | xlsx-formula-model-builder, public-office-excel-automation, public-office-xlsx-manipulation, public-swebench-xlsx, public-xlsx |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 1 | 1 | `public-office-sheets-automation` | gold | public-office-sheets-automation, xlsx-formula-model-builder, public-swebench-xlsx, public-office-xlsx-manipulation, airtable-workflow-automator |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 2 | 1 | `airtable-workflow-automator` | acceptable | airtable-workflow-automator, public-office-airtable-automation, email-drafter, email-classification-router, xlsx-formula-model-builder |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 2 | 2 | `invoice-payment-checker` | wrong | invoice-payment-checker, public-office-invoice-automation, finance-ops-artifact-packager, finance-ops-summary-writer, public-office-invoice-organizer |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 11 | 11 | `crm-ops-intake-classifier` | wrong | crm-ops-intake-classifier, sales-ops-intake-classifier, crm-ops-priority-ranker, crm-ops-monitoring-plan-builder, sales-ops-priority-ranker |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-subscription-management, churn-risk-analyser, customer-success-ops-summary-writer, data-analysis-for-reporting |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, data-analysis-for-forecasting, data-analysis-overview, tech-news-trend-extractor, data-analysis-for-reporting |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 1 | 1 | `public-office-dcf-valuation` | gold | public-office-dcf-valuation, finance-ops-scenario-planner, financial-model-builder, xlsx-formula-model-builder, data-analysis-for-forecasting |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 13 | 13 | `ecommerce-ops-rewrite-editor` | wrong | ecommerce-ops-rewrite-editor, ecommerce-ops-handoff-brief-writer, ecommerce-ops-normalizer, ecommerce-ops-timeline-builder, ecommerce-ops-monitoring-plan-builder |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 5 | 5 | `support-ticket-triager` | wrong | support-ticket-triager, support-ops-ops-intake-classifier, support-ops-ops-normalizer, support-ops-ops-summary-writer, public-office-zendesk-automation |
