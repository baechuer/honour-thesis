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
| Top-1 accuracy | 62.2% |
| Acceptable top-1 accuracy | 72.0% |
| Top-3 recall | 79.3% |
| Top-5 recall | 84.2% |
| Acceptable top-5 recall | 89.0% |
| MRR | 0.720 |
| Non-main top-1 | 82.9% |
| Approx selector-visible tokens | 122537 |

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
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 1 | 1 | `public-office-pdf-extraction` | gold | public-office-pdf-extraction, pdf-layout-table-extractor, implicit-pdf-table-reconstructor, vendor-ops-field-extractor, pdf-ocr-extractor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 2 | `pdf-ocr-extractor` | wrong | pdf-ocr-extractor, pdf-ocr-cleaner, public-office-pdf-ocr, public-office-chat-with-pdf, implicit-pdf-evidence-answerer |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, implicit-pdf-evidence-answerer, document-summariser, implicit-pdf-table-reconstructor |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, layout-preserving-converter, office-to-markdown-converter, document-converter, public-office-batch-convert |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, public-office-chat-with-pdf, document-summariser, implicit-pdf-evidence-answerer, pdf-redaction-reviewer |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 3 | 3 | `public-oh-my-playwriter` | wrong | public-oh-my-playwriter, public-playwright-interactive, public-addy-agent-browser-testing-with-devtools, playwright-flow-debugger, web-page-snapshotter |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 2 | 2 | `product-ops-rewrite-editor` | wrong | product-ops-rewrite-editor, public-addy-web-accessibility, product-ops-comparison-builder, product-ops-compliance-checker, product-ops-quality-auditor |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, web-ops-evidence-grounder, web-performance-budget-checker, seo-ops-evidence-grounder |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `localization-ops-field-extractor` | wrong | localization-ops-field-extractor, localization-ops-evidence-grounder, implicit-ci-failure-reader, geospatial-ops-evidence-grounder, localization-ops-failure-diagnoser |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 5 | 1 | `ci-log-root-cause-debugger` | acceptable | ci-log-root-cause-debugger, pr-review-comment-resolver, public-openai-gh-fix-ci, ci-failure-debugger, public-swebench-analyze-ci |
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
| `public_gold_p27_contract_review` | `public-office-contract-review` | 15 | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, vendor-ops-risk-reviewer, contract-ops-risk-reviewer, procurement-risk-summariser, vendor-ops-rewrite-editor |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-evidence-grounder, email-ops-risk-reviewer, email-polisher, professor-email-reply |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 2 | 2 | `slide-outline-builder` | wrong | slide-outline-builder, public-office-ai-slides, speaker-notes-writer, deck-template-applier, slide-deck-visual-auditor |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 1 | 1 | `public-openai-figma-implement-design` | gold | public-openai-figma-implement-design, public-openai-figma, public-openai-figma-generate-design, public-openai-figma-use, public-openai-figma-code-connect-components |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 2 | 1 | `skill-creator` | acceptable | skill-creator, public-skill-creator, skill-field-auditor, skill-authoring-guide, public-skill-installer |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 3 | 3 | `public-addy-agent-security-and-hardening` | wrong | public-addy-agent-security-and-hardening, architecture-boundary-reviewer, public-security-threat-model, public-openai-security-ownership-map, service-dependency-mapper |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, public-openai-cli-creator, public-oh-my-lmstudio-cli, public-openai-migrate-to-codex, public-openai-speech |
| `public_gold_p34_playwright` | `public-openai-playwright` | 12 | 6 | `public-oh-my-playwriter` | wrong | public-oh-my-playwriter, public-playwright-interactive, public-anthropic-webapp-testing, web-page-snapshotter, web-form-filler |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 6 | 6 | `web-page-snapshotter` | wrong | web-page-snapshotter, public-anthropic-webapp-testing, playwright-flow-debugger, public-playwright-interactive, public-oh-my-agent-browser |
| `public_gold_p36_sentry` | `public-openai-sentry` | 1 | 1 | `public-openai-sentry` | gold | public-openai-sentry, slo-breach-narrative-writer, incident-summary-writer, distributed-trace-investigator, public-swebench-analytics-events |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 1 | 1 | `public-openai-transcribe` | gold | public-openai-transcribe, speaker-notes-writer, public-addy-agent-interview-me, public-office-transcription-automation, meeting-summary-writer |
| `public_gold_p38_speech` | `public-openai-speech` | 3 | 3 | `speaker-notes-writer` | wrong | speaker-notes-writer, public-openai-transcribe, public-openai-speech, public-office-transcription-automation, knowledge-base-article-writer |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | 4 | 4 | `public-huggingface-datasets` | wrong | public-huggingface-datasets, implicit-hf-dataset-inspector, dataset-ops-summary-writer, public-openai-jupyter-notebook, dataset-ops-evidence-grounder |
| `public_gold_p40_linear` | `public-openai-linear` | 1 | 1 | `public-openai-linear` | gold | public-openai-linear, public-mattpocock-to-issues, public-office-linear-automation, public-openai-notion-spec-to-implementation, implicit-review-comment-planner |
| `public_gold_p41_yeet` | `public-openai-yeet` | 2 | 2 | `pr-description-writer` | wrong | pr-description-writer, public-openai-yeet, public-openai-gh-address-comments, changelog-writer, review-comment-resolver |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 13 | 13 | `public-vercel-find-skills` | wrong | public-vercel-find-skills, public-mattpocock-setup-matt-pocock-skills, public-oh-my-agentic-skills, public-skill-installer, public-addy-agent-using-agent-skills |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | 8 | 8 | `public-openai-notion-meeting-intelligence` | wrong | public-openai-notion-meeting-intelligence, meeting-followup-extractor, meeting-notes-action-extractor, meeting-agenda-builder, task-extractor |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | 6 | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-followup-extractor, meeting-summary-writer, meeting-agenda-builder, task-extractor |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, notion-research-database-builder, public-writing-plans, product-ops-handoff-brief-writer, product-ops-resource-linker |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-implement-design, public-openai-figma-generate-design, public-openai-figma, public-openai-figma-create-design-system-rules |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 1 | 1 | `public-openai-figma-generate-library` | gold | public-openai-figma-generate-library, public-openai-figma-create-design-system-rules, public-openai-figma-generate-design, public-oh-my-design-system, public-openai-figma-implement-design |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 1 | 1 | `public-openai-figma-create-design-system-rules` | gold | public-openai-figma-create-design-system-rules, public-openai-figma-generate-library, ux-ops-normalizer, public-openai-figma-implement-design, public-openai-figma-generate-design |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 5 | 1 | `seo-metadata-checker` | acceptable | seo-metadata-checker, seo-ops-evidence-grounder, landing-page-copy-reviewer, seo-ops-quality-auditor, public-addy-web-seo |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 6 | 6 | `web-performance-budget-checker` | wrong | web-performance-budget-checker, public-addy-agent-performance-optimization, public-addy-web-core-web-vitals, public-swebench-python-performance-optimization, public-addy-web-web-quality-audit |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 1 | 1 | `public-addy-web-web-quality-audit` | gold | public-addy-web-web-quality-audit, web-ops-quality-auditor, seo-ops-quality-auditor, privacy-ops-quality-auditor, analytics-ops-quality-auditor |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 1 | 1 | `public-addy-agent-api-and-interface-design` | gold | public-addy-agent-api-and-interface-design, openapi-contract-reviewer, rest-api-contract-designer, webhook-contract-planner, external-api-integration-planner |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 1 | 1 | `public-addy-agent-context-engineering` | gold | public-addy-agent-context-engineering, public-openai-migrate-to-codex, public-mattpocock-setup-matt-pocock-skills, public-openai-security-best-practices, public-anthropic-claude-api |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | 2 | 2 | `database-migration-risk-assessor` | wrong | database-migration-risk-assessor, public-addy-agent-deprecation-and-migration, migration-risk-auditor, external-api-integration-planner, database-backup-planner |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | 1 | 1 | `public-addy-agent-documentation-and-adrs` | gold | public-addy-agent-documentation-and-adrs, architecture-boundary-reviewer, public-mattpocock-improve-codebase-architecture, service-dependency-mapper, public-addy-agent-api-and-interface-design |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | 3 | 3 | `public-brainstorming` | wrong | public-brainstorming, meeting-ops-acceptance-test-builder, public-addy-agent-spec-driven-development, public-addy-agent-api-and-interface-design, public-addy-agent-incremental-implementation |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | - | 1 | `public-mattpocock-tdd` | acceptable | public-mattpocock-tdd, implicit-ci-failure-reader, public-mattpocock-diagnose, public-lbussell-property-testing-cscheck, debugging-root-cause-helper |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 1 | 1 | `public-addy-agent-source-driven-development` | gold | public-addy-agent-source-driven-development, refactor-planner, public-mattpocock-improve-codebase-architecture, public-oh-my-codebase-search, public-swebench-implementing-jsc-classes-zig |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, public-anthropic-mcp-builder, public-oh-my-git-guardrails-claude-code, public-anthropic-doc-coauthoring, public-anthropic-internal-comms |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | 12 | 12 | `docs-ops-scenario-planner` | wrong | docs-ops-scenario-planner, partnerships-ops-handoff-brief-writer, docs-ops-rewrite-editor, docs-ops-handoff-brief-writer, docs-ops-resource-linker |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 1 | 1 | `public-anthropic-canvas-design` | gold | public-anthropic-canvas-design, slide-outline-builder, compliance-ops-timeline-builder, grant-ops-timeline-builder, speaker-notes-writer |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 10 | 10 | `ux-ops-normalizer` | wrong | ux-ops-normalizer, ux-ops-monitoring-plan-builder, public-oh-my-design-system, ux-ops-timeline-builder, public-oh-my-ui-component-patterns |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 2 | 2 | `hf-zerogpu-space-deployer` | wrong | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, implicit-hf-local-model-chooser, hf-local-model-selector, gradio-demo-builder |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 3 | 3 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-huggingface-huggingface-llm-trainer, training-ops-rewrite-editor, dataset-ops-rewrite-editor |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 1 | 1 | `public-huggingface-huggingface-local-models` | gold | public-huggingface-huggingface-local-models, implicit-hf-local-model-chooser, hf-local-model-selector, hf-zerogpu-space-deployer, public-huggingface-huggingface-community-evals |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 1 | 1 | `public-huggingface-huggingface-trackio` | gold | public-huggingface-huggingface-trackio, training-ops-comparison-builder, public-huggingface-huggingface-llm-trainer, hf-community-eval-runner, training-ops-summary-writer |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 1 | 1 | `public-huggingface-huggingface-papers` | gold | public-huggingface-huggingface-papers, public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-best, public-huggingface-transformers-js, hf-local-model-selector |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, public-office-academic-search, paper-summariser, related-work-synthesiser |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 1 | 1 | `public-huggingface-transformers-js` | gold | public-huggingface-transformers-js, gradio-demo-builder, public-huggingface-huggingface-gradio, ml-ops-rewrite-editor, public-anthropic-web-artifacts-builder |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, public-obsidian-obsidian-bases, research-ops-dependency-mapper, research-ops-timeline-builder, thesis-ops-dependency-mapper |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-obsidian-obsidian-cli, public-mattpocock-obsidian-vault, public-oh-my-obsidian-cli-uri-fallback, public-oh-my-obsidian-cli |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 1 | 1 | `public-obsidian-obsidian-cli` | gold | public-obsidian-obsidian-cli, public-oh-my-obsidian-cli, public-oh-my-obsidian-cli-uri-fallback, public-mattpocock-obsidian-vault, public-obsidian-obsidian-markdown |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 5 | 2 | `spreadsheet-formula-auditor` | wrong | spreadsheet-formula-auditor, xlsx-formula-model-builder, public-office-xlsx-manipulation, public-office-data-analysis, public-office-excel-automation |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 1 | 1 | `public-office-sheets-automation` | gold | public-office-sheets-automation, spreadsheet-formula-auditor, xlsx-formula-model-builder, document-summariser, public-swebench-xlsx |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 1 | 1 | `public-office-airtable-automation` | gold | public-office-airtable-automation, airtable-workflow-automator, public-office-pipedrive-automation, email-drafter, public-office-lead-routing |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 1 | 1 | `public-office-invoice-automation` | gold | public-office-invoice-automation, finance-ops-intake-classifier, public-office-expense-tracker, public-office-quickbooks-automation, invoice-payment-checker |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 1 | 1 | `public-office-lead-routing` | gold | public-office-lead-routing, sales-ops-intake-classifier, public-office-lead-research, crm-ops-intake-classifier, public-office-lead-qualification |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-subscription-management, churn-risk-analyser, customer-success-ops-summary-writer, financial-report-writer |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, procurement-risk-summariser, public-office-company-research, public-swebench-risk-metrics-calculation, analytics-ops-risk-reviewer |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 1 | 1 | `public-office-dcf-valuation` | gold | public-office-dcf-valuation, financial-model-builder, public-swebench-creating-financial-models, finance-ops-scenario-planner, public-office-investment-memo |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 1 | 1 | `public-office-shopify-automation` | gold | public-office-shopify-automation, public-office-woocommerce-automation, ecommerce-ops-handoff-brief-writer, product-ops-intake-classifier, warehouse-ops-handoff-brief-writer |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 1 | 1 | `public-office-zendesk-automation` | gold | public-office-zendesk-automation, support-ticket-triager, support-ops-intake-classifier, support-ops-ops-intake-classifier, customer-success-ops-intake-classifier |
