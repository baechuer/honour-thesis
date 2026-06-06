# Provider Selector Evaluation Report

This report evaluates optional API-backed selector baselines. API calls are cached under `skill_benchmark/runtime/provider_cache/`.

## Configuration

- Embedding provider: `qwen`
- Embedding model: `text-embedding-v4`
- Embedding representation: `r1`
- Scale: `current_full` (2401 skills)
- Reranker: `qwen`
- Rerank candidates: 20

## Metrics

| Metric | Value |
|---|---:|
| Top-1 accuracy | 74.4% |
| Acceptable top-1 accuracy | 85.4% |
| Top-3 recall | 92.7% |
| Top-5 recall | 96.3% |
| Acceptable top-5 recall | 97.6% |
| MRR | 0.837 |
| Non-main top-1 | 86.6% |
| Approx selector-visible tokens | 308547 |

## API Usage Estimate

- Embedding API calls made in this run: 0
- Embedding cache hits: 2483
- Approx uncached embedding input tokens: 0
- Rerank API calls made in this run: 82
- Rerank cache hits: 0
- Approx uncached rerank input tokens: 186010

## Prompt-Level Results

| Prompt | Gold | Rank | Accept Rank | Top-1 | Status | Top-5 |
|---|---|---:|---:|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | 1 | 1 | `public-office-pdf-extraction` | gold | public-office-pdf-extraction, public-openai-pdf, pdf-layout-table-extractor, public-pdf, implicit-pdf-table-reconstructor |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | 3 | 1 | `pdf-ocr-cleaner` | acceptable | pdf-ocr-cleaner, pdf-ocr-extractor, public-office-pdf-ocr, public-pdf, public-openai-pdf |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | 2 | 1 | `pdf-form-filler` | acceptable | pdf-form-filler, public-office-pdf-form-filler, public-office-expense-tracker, public-pdf, implicit-pdf-evidence-answerer |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | 1 | 1 | `public-markitdown` | gold | public-markitdown, office-to-markdown-converter, document-converter, public-office-batch-convert, pdf-ocr-extractor |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | 1 | 1 | `public-office-pdf-merge-split` | gold | public-office-pdf-merge-split, legal-ops-artifact-packager, implicit-pdf-evidence-answerer, public-pdf, public-office-doc-pipeline |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | 1 | 1 | `public-addy-agent-browser-testing-with-devtools` | gold | public-addy-agent-browser-testing-with-devtools, frontend-debugger, public-oh-my-playwriter, public-n-skills-dev-browser, public-anthropic-webapp-testing |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | 1 | 1 | `public-addy-web-accessibility` | gold | public-addy-web-accessibility, ux-ops-compliance-checker, product-ops-quality-auditor, product-ops-compliance-checker, product-ops-acceptance-test-builder |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | 1 | 1 | `public-addy-web-core-web-vitals` | gold | public-addy-web-core-web-vitals, public-addy-agent-performance-optimization, public-addy-web-performance, web-ops-evidence-grounder, implicit-browser-flow-investigator |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | - | - | `debugging-root-cause-helper` | wrong | debugging-root-cause-helper, localization-ops-failure-diagnoser, geospatial-ops-failure-diagnoser, implicit-ci-failure-reader, api-ops-evidence-grounder |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | 1 | 1 | `public-swebench-analyze-ci` | gold | public-swebench-analyze-ci, implicit-ci-failure-reader, ci-failure-debugger, ci-log-root-cause-debugger, public-openai-gh-fix-ci |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 1 | 1 | `public-mattpocock-setup-pre-commit` | gold | public-mattpocock-setup-pre-commit, public-oh-my-setup-pre-commit, version-control-helper, public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 | `public-mattpocock-git-guardrails-claude-code` | gold | public-mattpocock-git-guardrails-claude-code, git-safety-guardrail-installer, public-oh-my-git-guardrails-claude-code, repo-ops-compliance-checker, version-control-helper |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | 4 | 4 | `review-comment-resolver` | wrong | review-comment-resolver, public-openai-gh-fix-ci, pr-review-comment-resolver, public-openai-gh-address-comments, implicit-review-comment-planner |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | 1 | 1 | `public-netlify-deploy` | gold | public-netlify-deploy, deployment-release-verifier, web-ops-artifact-packager, public-openai-vercel-deploy, public-openai-cloudflare-deploy |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | 1 | 1 | `public-openai-cloudflare-deploy` | gold | public-openai-cloudflare-deploy, publishing-ops-artifact-packager, platform-ops-artifact-packager, public-openai-vercel-deploy, cloud-ops-artifact-packager |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | 1 | 1 | `public-openai-render-deploy` | gold | public-openai-render-deploy, public-openai-cloudflare-deploy, repo-ops-artifact-packager, public-openai-vercel-deploy, sre-ops-artifact-packager |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | 2 | 1 | `mcp-server-builder` | acceptable | mcp-server-builder, public-anthropic-mcp-builder, public-swebench-mcp-builder, rest-api-contract-designer, public-office-office-mcp |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | 1 | 1 | `public-openai-chatgpt-apps` | gold | public-openai-chatgpt-apps, public-swebench-mcp-builder, public-anthropic-mcp-builder, mcp-server-builder, public-openai-winui-app |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | 1 | 1 | `public-openai-cli-creator` | gold | public-openai-cli-creator, auth-flow-integrator, api-documentation-writer, public-swebench-mcp-builder, public-openai-chatgpt-apps |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | 1 | 1 | `public-huggingface-datasets` | gold | public-huggingface-datasets, hf-dataset-viewer-inspector, implicit-hf-dataset-inspector, dataset-ops-acceptance-test-builder, dataset-ops-field-extractor |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | 1 | 1 | `public-huggingface-huggingface-gradio` | gold | public-huggingface-huggingface-gradio, gradio-demo-builder, public-huggingface-datasets, public-anthropic-frontend-design, public-huggingface-huggingface-zerogpu |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | 1 | 1 | `public-huggingface-huggingface-vision-trainer` | gold | public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-llm-trainer, hf-community-eval-runner, implicit-hf-local-model-chooser, hf-local-model-selector |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | 2 | 1 | `sentence-transformer-finetuner` | acceptable | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-huggingface-transformers-js, public-swebench-rag-implementation, public-swebench-llm-evaluation |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | 1 | 1 | `public-huggingface-hf-cli` | gold | public-huggingface-hf-cli, public-huggingface-huggingface-best, public-huggingface-huggingface-tool-builder, public-huggingface-huggingface-local-models, public-huggingface-huggingface-community-evals |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | 2 | 1 | `public-office-etl-pipeline` | acceptable | public-office-etl-pipeline, public-office-data-pipeline, public-swebench-dbt-transformation-patterns, dataset-ops-field-extractor, dataset-ops-dependency-mapper |
| `public_gold_p26_database_sync` | `public-office-database-sync` | 1 | 1 | `public-office-database-sync` | gold | public-office-database-sync, database-ops-comparison-builder, public-oh-my-database-schema-design, database-schema-designer, database-ops-dependency-mapper |
| `public_gold_p27_contract_review` | `public-office-contract-review` | 2 | 1 | `contract-risk-reviewer` | acceptable | contract-risk-reviewer, public-office-contract-review, contract-ops-risk-reviewer, vendor-ops-risk-reviewer, procurement-ops-risk-reviewer |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | 1 | 1 | `public-office-suspicious-email` | gold | public-office-suspicious-email, email-ops-risk-reviewer, email-ops-evidence-grounder, email-ops-intake-classifier, security-ops-evidence-grounder |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | 1 | 1 | `public-office-ai-slides` | gold | public-office-ai-slides, slide-outline-builder, public-oh-my-presentation-builder, content-ops-handoff-brief-writer, slide-deck-visual-auditor |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | 1 | 1 | `public-openai-figma-implement-design` | gold | public-openai-figma-implement-design, public-openai-figma, public-openai-figma-generate-design, public-openai-figma-generate-library, public-openai-figma-use |
| `public_gold_p31_skill_creator` | `public-skill-creator` | 4 | 1 | `skill-creator` | acceptable | skill-creator, public-mattpocock-write-a-skill, skill-authoring-guide, public-skill-creator, public-anthropic-doc-coauthoring |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | 3 | 3 | `secret-leak-scanner` | wrong | secret-leak-scanner, public-swebench-security-review, public-security-threat-model, security-code-reviewer, security-threat-modeler |
| `public_gold_p33_openai_docs` | `public-openai-openai-docs` | 1 | 1 | `public-openai-openai-docs` | gold | public-openai-openai-docs, public-oh-my-openai-agents-python, public-openai-migrate-to-codex, public-openai-chatgpt-apps, public-oh-my-pydantic-ai |
| `public_gold_p34_playwright` | `public-openai-playwright` | 1 | 1 | `public-openai-playwright` | gold | public-openai-playwright, public-office-browser-automation, public-n-skills-dev-browser, public-oh-my-agent-browser, public-anthropic-webapp-testing |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | 8 | 8 | `web-page-snapshotter` | wrong | web-page-snapshotter, public-openai-playwright, public-n-skills-dev-browser, public-anthropic-webapp-testing, public-office-browser-automation |
| `public_gold_p36_sentry` | `public-openai-sentry` | 1 | 1 | `public-openai-sentry` | gold | public-openai-sentry, metrics-root-cause-diagnoser, public-swebench-python-observability, implicit-trace-path-diagnoser, dashboard-ops-failure-diagnoser |
| `public_gold_p37_transcribe` | `public-openai-transcribe` | 1 | 1 | `public-openai-transcribe` | gold | public-openai-transcribe, public-office-transcription-automation, public-addy-agent-interview-me, public-mattpocock-grill-me, speaker-notes-writer |
| `public_gold_p38_speech` | `public-openai-speech` | 1 | 1 | `public-openai-speech` | gold | public-openai-speech, speaker-notes-writer, public-anthropic-internal-comms, customer-success-ops-rewrite-editor, support-ops-rewrite-editor |
| `public_gold_p39_jupyter_notebook` | `public-openai-jupyter-notebook` | 1 | 1 | `public-openai-jupyter-notebook` | gold | public-openai-jupyter-notebook, public-office-data-analysis, data-analysis-for-reporting, public-oh-my-data-analysis, data-analysis-with-validation |
| `public_gold_p40_linear` | `public-openai-linear` | 1 | 1 | `public-openai-linear` | gold | public-openai-linear, public-office-linear-automation, public-openai-notion-spec-to-implementation, public-mattpocock-to-issues, public-mattpocock-triage |
| `public_gold_p41_yeet` | `public-openai-yeet` | 1 | 1 | `public-openai-yeet` | gold | public-openai-yeet, public-addy-agent-git-workflow-and-versioning, git-commit-writer, pr-description-writer, public-openai-gh-address-comments |
| `public_gold_p42_migrate_to_codex` | `public-openai-migrate-to-codex` | 1 | 1 | `public-openai-migrate-to-codex` | gold | public-openai-migrate-to-codex, public-mattpocock-write-a-skill, public-mattpocock-setup-matt-pocock-skills, skill-authoring-guide, agent-ops-handoff-brief-writer |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | 1 | 1 | `public-openai-notion-knowledge-capture` | gold | public-openai-notion-knowledge-capture, public-openai-notion-meeting-intelligence, public-openai-notion-spec-to-implementation, knowledge-ops-summary-writer, construction-ops-summary-writer |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | 5 | 1 | `meeting-notes-action-extractor` | acceptable | meeting-notes-action-extractor, meeting-followup-extractor, meeting-ops-handoff-brief-writer, public-openai-notion-knowledge-capture, public-openai-notion-meeting-intelligence |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | 1 | 1 | `public-openai-notion-spec-to-implementation` | gold | public-openai-notion-spec-to-implementation, public-addy-agent-planning-and-task-breakdown, public-writing-plans, public-addy-agent-spec-driven-development, engineering-design-ops-handoff-brief-writer |
| `public_gold_p46_figma_code_connect` | `public-openai-figma-code-connect-components` | 1 | 1 | `public-openai-figma-code-connect-components` | gold | public-openai-figma-code-connect-components, public-openai-figma-implement-design, public-openai-figma, public-openai-figma-generate-design, public-openai-figma-use |
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | 1 | 1 | `public-openai-figma-generate-library` | gold | public-openai-figma-generate-library, public-openai-figma-create-design-system-rules, public-openai-figma-generate-design, public-openai-figma-code-connect-components, public-oh-my-frontend-design-system |
| `public_gold_p48_figma_design_system_rules` | `public-openai-figma-create-design-system-rules` | 1 | 1 | `public-openai-figma-create-design-system-rules` | gold | public-openai-figma-create-design-system-rules, public-openai-figma-generate-design, public-openai-figma-generate-library, public-oh-my-frontend-design-system, public-openai-figma |
| `public_gold_p49_web_seo` | `public-addy-web-seo` | 3 | 2 | `seo-ops-quality-auditor` | wrong | seo-ops-quality-auditor, seo-metadata-checker, public-addy-web-seo, seo-ops-failure-diagnoser, seo-ops-evidence-grounder |
| `public_gold_p50_web_performance` | `public-addy-web-performance` | 2 | 2 | `public-addy-web-web-quality-audit` | wrong | public-addy-web-web-quality-audit, public-addy-web-performance, public-anthropic-webapp-testing, public-addy-agent-performance-optimization, web-performance-budget-checker |
| `public_gold_p51_web_quality_audit` | `public-addy-web-web-quality-audit` | 1 | 1 | `public-addy-web-web-quality-audit` | gold | public-addy-web-web-quality-audit, web-ops-quality-auditor, public-addy-web-best-practices, web-ops-risk-reviewer, seo-ops-quality-auditor |
| `public_gold_p52_api_interface_design` | `public-addy-agent-api-and-interface-design` | 1 | 1 | `public-addy-agent-api-and-interface-design` | gold | public-addy-agent-api-and-interface-design, rest-api-contract-designer, architecture-boundary-reviewer, webhook-contract-planner, service-dependency-mapper |
| `public_gold_p53_context_engineering` | `public-addy-agent-context-engineering` | 1 | 1 | `public-addy-agent-context-engineering` | gold | public-addy-agent-context-engineering, context-compressor, public-oh-my-git-guardrails-claude-code, public-n-skills-orchestration, public-mattpocock-improve-codebase-architecture |
| `public_gold_p54_deprecation_migration` | `public-addy-agent-deprecation-and-migration` | 1 | 1 | `public-addy-agent-deprecation-and-migration` | gold | public-addy-agent-deprecation-and-migration, api-ops-scenario-planner, api-ops-timeline-builder, api-integration-planner, external-api-integration-planner |
| `public_gold_p55_documentation_adrs` | `public-addy-agent-documentation-and-adrs` | 1 | 1 | `public-addy-agent-documentation-and-adrs` | gold | public-addy-agent-documentation-and-adrs, public-mattpocock-grill-with-docs, public-mattpocock-improve-codebase-architecture, public-architecture-patterns, public-swebench-django-patterns |
| `public_gold_p56_spec_driven_development` | `public-addy-agent-spec-driven-development` | 1 | 1 | `public-addy-agent-spec-driven-development` | gold | public-addy-agent-spec-driven-development, public-writing-plans, public-brainstorming, public-openai-notion-spec-to-implementation, public-addy-agent-incremental-implementation |
| `public_gold_p57_test_driven_development` | `public-addy-agent-test-driven-development` | - | 1 | `public-mattpocock-tdd` | acceptable | public-mattpocock-tdd, debugging-root-cause-helper, public-addy-agent-debugging-and-error-recovery, public-lbussell-property-testing-cscheck, public-mattpocock-diagnose |
| `public_gold_p58_source_driven_development` | `public-addy-agent-source-driven-development` | 2 | 2 | `refactor-planner` | wrong | refactor-planner, public-addy-agent-source-driven-development, public-oh-my-code-refactoring, public-mattpocock-improve-codebase-architecture, public-swebench-fix |
| `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | 1 | 1 | `public-anthropic-claude-api` | gold | public-anthropic-claude-api, public-anthropic-mcp-builder, public-anthropic-internal-comms, public-swebench-mcp-builder, public-oh-my-git-guardrails-claude-code |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | 1 | 1 | `public-anthropic-doc-coauthoring` | gold | public-anthropic-doc-coauthoring, docs-ops-rewrite-editor, document-rewriter, academic-admin-ops-handoff-brief-writer, docs-ops-handoff-brief-writer |
| `public_gold_p61_canvas_design` | `public-anthropic-canvas-design` | 1 | 1 | `public-anthropic-canvas-design` | gold | public-anthropic-canvas-design, slide-outline-builder, public-office-infographic, public-obsidian-json-canvas, public-anthropic-algorithmic-art |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | 2 | 2 | `public-oh-my-design-system` | wrong | public-oh-my-design-system, public-anthropic-theme-factory, public-oh-my-frontend-design-system, public-oh-my-ui-component-patterns, ux-ops-artifact-packager |
| `public_gold_p63_hf_zerogpu` | `public-huggingface-huggingface-zerogpu` | 2 | 2 | `hf-zerogpu-space-deployer` | wrong | hf-zerogpu-space-deployer, public-huggingface-huggingface-zerogpu, public-huggingface-huggingface-best, public-huggingface-huggingface-gradio, public-huggingface-huggingface-tool-builder |
| `public_gold_p64_hf_llm_trainer` | `public-huggingface-huggingface-llm-trainer` | 3 | 3 | `sentence-transformer-finetuner` | wrong | sentence-transformer-finetuner, public-huggingface-train-sentence-transformers, public-huggingface-huggingface-llm-trainer, hf-community-eval-runner, public-huggingface-huggingface-community-evals |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | 1 | 1 | `public-huggingface-huggingface-local-models` | gold | public-huggingface-huggingface-local-models, implicit-hf-local-model-chooser, hf-local-model-selector, public-huggingface-transformers-js, public-huggingface-huggingface-best |
| `public_gold_p66_hf_trackio` | `public-huggingface-huggingface-trackio` | 1 | 1 | `public-huggingface-huggingface-trackio` | gold | public-huggingface-huggingface-trackio, public-huggingface-huggingface-vision-trainer, public-huggingface-huggingface-llm-trainer, training-ops-comparison-builder, ml-ops-comparison-builder |
| `public_gold_p67_hf_papers` | `public-huggingface-huggingface-papers` | 1 | 1 | `public-huggingface-huggingface-papers` | gold | public-huggingface-huggingface-papers, multi-source-comparison-builder, paper-summariser, sentence-transformer-finetuner, public-huggingface-huggingface-best |
| `public_gold_p68_hf_paper_publisher` | `public-huggingface-huggingface-paper-publisher` | 1 | 1 | `public-huggingface-huggingface-paper-publisher` | gold | public-huggingface-huggingface-paper-publisher, public-huggingface-huggingface-papers, academic-admin-ops-artifact-packager, research-ops-artifact-packager, public-oh-my-research-paper-writing |
| `public_gold_p69_transformers_js` | `public-huggingface-transformers-js` | 1 | 1 | `public-huggingface-transformers-js` | gold | public-huggingface-transformers-js, gradio-demo-builder, public-huggingface-huggingface-gradio, hf-local-model-selector, public-playwright-interactive |
| `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | 1 | 1 | `public-obsidian-json-canvas` | gold | public-obsidian-json-canvas, public-obsidian-obsidian-bases, knowledge-graph-builder, public-oh-my-obsidian-cli, public-office-obsidian-automation |
| `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | 1 | 1 | `public-obsidian-obsidian-bases` | gold | public-obsidian-obsidian-bases, public-mattpocock-obsidian-vault, public-office-obsidian-automation, public-obsidian-obsidian-markdown, public-obsidian-obsidian-cli |
| `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | 1 | 1 | `public-obsidian-obsidian-cli` | gold | public-obsidian-obsidian-cli, public-mattpocock-obsidian-vault, public-office-obsidian-automation, public-oh-my-obsidian-cli, public-oh-my-obsidian |
| `public_gold_p73_excel_automation` | `public-office-excel-automation` | 1 | 1 | `public-office-excel-automation` | gold | public-office-excel-automation, public-xlsx, public-swebench-xlsx, public-office-xlsx-manipulation, xlsx-formula-model-builder |
| `public_gold_p74_sheets_automation` | `public-office-sheets-automation` | 1 | 1 | `public-office-sheets-automation` | gold | public-office-sheets-automation, public-swebench-xlsx, data-analysis-with-validation, xlsx-formula-model-builder, spreadsheet-formula-auditor |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | 1 | 1 | `public-office-airtable-automation` | gold | public-office-airtable-automation, airtable-workflow-automator, public-office-lead-routing, followup-reply-writer, email-classification-router |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | 2 | 2 | `public-office-quickbooks-automation` | wrong | public-office-quickbooks-automation, public-office-invoice-automation, finance-ops-field-extractor, public-office-invoice-organizer, procurement-ops-field-extractor |
| `public_gold_p77_lead_routing` | `public-office-lead-routing` | 1 | 1 | `public-office-lead-routing` | gold | public-office-lead-routing, sales-ops-priority-ranker, sales-ops-intake-classifier, crm-ops-intake-classifier, public-office-lead-qualification |
| `public_gold_p78_saas_metrics` | `public-office-saas-metrics` | 1 | 1 | `public-office-saas-metrics` | gold | public-office-saas-metrics, public-office-subscription-management, financial-report-writer, data-analysis-for-reporting, public-office-data-analysis |
| `public_gold_p79_stock_analysis` | `public-office-stock-analysis` | 1 | 1 | `public-office-stock-analysis` | gold | public-office-stock-analysis, public-office-dcf-valuation, public-office-company-research, finance-ops-risk-reviewer, data-analysis-with-anomaly-focus |
| `public_gold_p80_dcf_valuation` | `public-office-dcf-valuation` | 2 | 2 | `public-swebench-creating-financial-models` | wrong | public-swebench-creating-financial-models, public-office-dcf-valuation, financial-model-builder, public-office-financial-modeling, data-analysis-for-forecasting |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | 1 | 1 | `public-office-shopify-automation` | gold | public-office-shopify-automation, product-ops-handoff-brief-writer, product-ops-normalizer, product-ops-failure-diagnoser, product-ops-intake-classifier |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 1 | 1 | `public-office-zendesk-automation` | gold | public-office-zendesk-automation, support-ticket-triager, support-ops-intake-classifier, support-ops-ops-intake-classifier, operations-ops-intake-classifier |
