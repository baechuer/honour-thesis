# Prompt Leakage Report

This report checks whether prompts accidentally reveal the gold skill through exact skill names, dominant skill-title words, or copied phrases from the gold skill card.

## Overall Status

- Prompt leakage status: **PASS**
- Total prompts: 82
- Critical exact-name leaks: 0
- High-risk title/phrase leaks: 0
- Critical risk prompts: 0
- High risk prompts: 0
- Medium risk prompts: 5
- Low risk prompts: 77

Interpretation: critical leaks are exact gold skill-name leaks. High-risk cases usually contain distinctive gold title words or copied gold-card phrases that may make lexical selectors look better than they really are.

## Family Summary

| Family | Critical | High | Medium | Low |
|---|---:|---:|---:|---:|
| `public_gold_validation` | 0 | 0 | 5 | 77 |

## Prompts To Review

| Risk | Prompt | Gold | Gold title hits | Advantage | Shared phrase | Flags |
|---|---|---|---|---:|---|---|
| medium | `public_gold_p33_openai_docs` | `public-openai-openai-docs` | openai, openai, docs | 0.25 | - | - |
| medium | `public_gold_p59_anthropic_claude_api` | `public-anthropic-claude-api` | anthropic, claude, api | 0.00 | - | - |
| medium | `public_gold_p70_obsidian_json_canvas` | `public-obsidian-json-canvas` | obsidian, json, canva | 0.00 | - | - |
| medium | `public_gold_p71_obsidian_bases` | `public-obsidian-obsidian-bases` | obsidian, obsidian, base | 0.00 | - | - |
| medium | `public_gold_p72_obsidian_cli` | `public-obsidian-obsidian-cli` | obsidian, obsidian, cli | 0.25 | - | - |

## Prompt Detail

### `public_gold_p01_pdf_extraction`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-extraction`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Using pdfplumber-style extraction, pull the native text, table cells, and document metadata from `/workspace/public_gold/vendor_pack.pdf` into structured JSON with page anchors. The file is not scanned, and I do not need a conversational answer or format conversion.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: pdf, extract
- Longest copied gold phrase: -

### `public_gold_p02_pdf_ocr`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-ocr`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The uploaded PDF is a scan of signed forms. Run OCR to recover readable text and mark uncertain recognition regions by page; do not treat it as a normal embedded-text PDF or convert it to Word.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: pdf, ocr
- Longest copied gold phrase: -

### `public_gold_p03_pdf_form_filler`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-form-filler`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the reimbursement PDF and the employee data sheet to fill the form fields and report any required blanks still missing. I am not asking for general extraction, conversion, or a reusable document template.
- Gold title overlap: 0.60; max alternative title overlap: 0.50; advantage: 0.10
- Gold title hits: pdf, form, fill
- Longest copied gold phrase: -

### `public_gold_p04_markitdown_conversion`

- Family: `public_gold_validation`
- Gold skill: `public-markitdown`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use a MarkItDown-style pipeline to convert a mixed folder of PDF, DOCX, PPTX, XLSX, image, HTML, CSV, and JSON files into Markdown text suitable for indexing. Preserve lightweight structure and OCR where needed; do not create Office files from Markdown.
- Gold title overlap: 0.00; max alternative title overlap: 1.00; advantage: -1.00
- Gold title hits: -
- Longest copied gold phrase: pdf docx pptx xlsx image

### `public_gold_p05_pdf_merge_split`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-merge-split`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Combine three policy PDFs into one packet, then split the appendix pages into a separate file. Do not watermark, compress, summarize, or convert the PDFs.
- Gold title overlap: 0.20; max alternative title overlap: 0.25; advantage: -0.05
- Gold title hits: split
- Longest copied gold phrase: -

### `public_gold_p06_browser_devtools_testing`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-browser-testing-with-devtools`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use Chrome DevTools MCP on the local checkout to inspect DOM state, console errors, failed network requests, and runtime screenshots. Do not just write a Playwright script from scratch.
- Gold title overlap: 0.20; max alternative title overlap: 0.33; advantage: -0.13
- Gold title hits: devtool
- Longest copied gold phrase: -

### `public_gold_p07_web_accessibility`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-accessibility`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit the product settings page against WCAG 2.2, focusing on keyboard navigation, labels, focus order, contrast, and screen-reader semantics. Do not broaden this into SEO or performance.
- Gold title overlap: 0.00; max alternative title overlap: 0.17; advantage: -0.17
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p08_core_web_vitals`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-core-web-vitals`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Investigate only the page's Core Web Vitals: identify the LCP element, INP handler delay, any CLS source, and metric-specific fixes. Do not broaden this into accessibility, SEO, browser automation, or general best-practice review.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: web, core, web, vital
- Longest copied gold phrase: -

### `public_gold_p09_systematic_debugging`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-debugging`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: A local feature intermittently returns the wrong result. Use the debugging packet style: freeze the failure definition, build the smallest reproducer, isolate the boundary where behaviour changes, and propose the first evidence-backed fix. Do not review code quality, simplify code, or inspect GitHub CI.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: debug
- Longest copied gold phrase: -

### `public_gold_p10_analyze_ci`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-analyze-ci`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Given the PR number and failed GitHub Actions job URLs, analyze the failing CI logs and identify the likely cause. Do not design a new workflow template or perform a general debugging session.
- Gold title overlap: 0.33; max alternative title overlap: 0.60; advantage: -0.27
- Gold title hits: analysi
- Longest copied gold phrase: -

### `public_gold_p11_setup_pre_commit`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-setup-pre-commit`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Add a repo-local Husky pre-commit setup with lint-staged so Prettier, type checking, and tests run before commits. Do not configure GitHub Actions, run a one-off fixer, or block dangerous git commands.
- Gold title overlap: 0.40; max alternative title overlap: 0.67; advantage: -0.27
- Gold title hits: setup, commit
- Longest copied gold phrase: lint-stag pretti type check test

### `public_gold_p12_git_guardrails`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-git-guardrails-claude-code`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Set up Claude Code git guardrail hooks that prevent dangerous git operations such as force-push, reset --hard, clean, and branch deletion before they execute. I am not asking for formatting hooks, general git workflow advice, or a PR publishing flow.
- Gold title overlap: 0.67; max alternative title overlap: 0.40; advantage: 0.27
- Gold title hits: git, guardrail, claude, code
- Longest copied gold phrase: reset hard clean branch

### `public_gold_p13_address_pr_comments`

- Family: `public_gold_validation`
- Gold skill: `public-openai-gh-address-comments`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: There are unresolved review comments on the current GitHub PR. Inspect the actionable threads, patch the requested changes, and report what was addressed. Do not create a new PR or debug failing checks.
- Gold title overlap: 0.25; max alternative title overlap: 0.20; advantage: 0.05
- Gold title hits: comment
- Longest copied gold phrase: -

### `public_gold_p14_netlify_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-netlify-deploy`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Deploy this static web project to Netlify, using the Netlify CLI and returning the deployment URL with verification. Do not target Vercel, Cloudflare, Render, or Kubernetes.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: netlify, deploy
- Longest copied gold phrase: web project netlify netlify cli

### `public_gold_p15_cloudflare_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cloudflare-deploy`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Publish the worker and static assets to Cloudflare Pages/Workers, including the required Wrangler or Cloudflare platform checks. Do not use Netlify, Vercel, Render, or Kubernetes manifests.
- Gold title overlap: 0.25; max alternative title overlap: 0.33; advantage: -0.08
- Gold title hits: cloudflare
- Longest copied gold phrase: -

### `public_gold_p16_render_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-render-deploy`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare this service specifically for Render deployment by analyzing the repo, generating a `render.yaml` Blueprint, and giving the Render Dashboard deployment path. Do not deploy to Netlify, Vercel, Cloudflare, or Kubernetes.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: rend, deploy
- Longest copied gold phrase: generat rend yaml blueprint

### `public_gold_p17_mcp_builder`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-mcp-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design and implement an MCP server that exposes a third-party issue-tracking API as well-typed tools with authentication and schema-aware tool contracts. Do not just browse a hub of existing MCP tools.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: mcp
- Longest copied gold phrase: -

### `public_gold_p18_chatgpt_apps`

- Family: `public_gold_validation`
- Gold skill: `public-openai-chatgpt-apps`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Build a ChatGPT App with an MCP server plus widget UI, following the Apps SDK structure. I need app scaffolding and troubleshooting, not a generic MCP server or CLI.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: chatgpt, apps
- Longest copied gold phrase: -

### `public_gold_p19_cli_creator`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cli-creator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Given an OpenAPI spec, API docs, SDK notes, and a few curl examples, build a composable command-line interface with subcommands, a clear command contract, auth/config handling, and runtime choices. Do not design the API itself, write documentation only, or create an MCP server.
- Gold title overlap: 0.00; max alternative title overlap: 1.00; advantage: -1.00
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p20_hf_datasets`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-datasets`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the Hugging Face Dataset Viewer API to list subsets and splits, paginate sample rows, and inspect schema information for a dataset. Do not download models or train embeddings.
- Gold title overlap: 0.33; max alternative title overlap: 0.20; advantage: 0.13
- Gold title hits: dataset
- Longest copied gold phrase: hugg face dataset view api

### `public_gold_p21_hf_gradio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-gradio`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create a Gradio demo UI with Python components, event listeners, layout, and launch behavior. This is not about ZeroGPU quota, Dataset Viewer API calls, or Transformers.js in the browser.
- Gold title overlap: 0.25; max alternative title overlap: 0.33; advantage: -0.08
- Gold title hits: gradio
- Longest copied gold phrase: component event listener layout

### `public_gold_p22_hf_vision_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-vision-trainer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Fine-tune an object detection model from an image dataset and prepare training/evaluation code for vision labels. Do not choose a local GGUF model or train sentence embeddings.
- Gold title overlap: 0.40; max alternative title overlap: 0.40; advantage: 0.00
- Gold title hits: vision, train
- Longest copied gold phrase: -

### `public_gold_p23_sentence_transformer_training`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-train-sentence-transformers`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Train or fine-tune a SentenceTransformer bi-encoder for retrieval using paired text data and report evaluation settings. Do not build a browser Transformers.js demo or choose a local inference model.
- Gold title overlap: 0.40; max alternative title overlap: 0.40; advantage: 0.00
- Gold title hits: train, transformer
- Longest copied gold phrase: -

### `public_gold_p24_hf_cli`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-hf-cli`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the Hugging Face Hub CLI to upload a model repo, manage files, and check repo metadata from the terminal. Do not query the Dataset Viewer API or design a custom tool.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: cli
- Longest copied gold phrase: hugg face hub cli

### `public_gold_p25_data_pipeline`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-pipeline`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design an ETL workflow that extracts data from two sources, transforms it, loads it into analytics storage, and schedules the pipeline. Do not just analyze a finished dataset or sync two databases.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: data, pipeline
- Longest copied gold phrase: -

### `public_gold_p26_database_sync`

- Family: `public_gold_validation`
- Gold skill: `public-office-database-sync`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Set up a two-way synchronization plan between PostgreSQL and MySQL with table mapping, change handling, and conflict rules. Do not create a general ETL pipeline or dashboard analysis.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p27_contract_review`

- Family: `public_gold_validation`
- Gold skill: `public-office-contract-review`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this vendor contract for risky clauses, missing protections, obligations, renewal terms, and negotiation recommendations. Do not generate a new template or summarize it generically.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: contract, review
- Longest copied gold phrase: -

### `public_gold_p28_suspicious_email`

- Family: `public_gold_validation`
- Gold skill: `public-office-suspicious-email`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Analyze this suspicious email for phishing indicators, spoofed sender details, malicious links, urgency tactics, and recommended safety response. Do not merely classify or draft a reply.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: suspiciou, email
- Longest copied gold phrase: -

### `public_gold_p29_ai_slides`

- Family: `public_gold_validation`
- Gold skill: `public-office-ai-slides`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Generate a complete presentation from the topic brief, including outline, slide content, and polished deck structure. Do not only convert existing Markdown or apply a visual theme.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: slide
- Longest copied gold phrase: -

### `public_gold_p30_figma_implement_design`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-implement-design`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Given a Figma URL with a specific node id, fetch the design context and screenshot, download required assets, and implement the existing frame as production UI code inside the repository with 1:1 visual parity. Do not create or update a Figma screen, generate a new design from a prompt, create a component library, or only fetch context.
- Gold title overlap: 0.60; max alternative title overlap: 0.60; advantage: 0.00
- Gold title hits: figma, implement, design
- Longest copied gold phrase: -

### `public_gold_p31_skill_creator`

- Family: `public_gold_validation`
- Gold skill: `public-skill-creator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create a new Codex skill for a repeated workflow, including the SKILL.md structure, trigger description, and optional resources/scripts guidance. Do not install an existing skill or migrate settings.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: skill
- Longest copied gold phrase: -

### `public_gold_p32_security_threat_model`

- Family: `public_gold_validation`
- Gold skill: `public-security-threat-model`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Given the repository and architecture notes, identify sensitive data and functions, crossings between users/services, likely misuse scenarios, and concrete mitigations. Do not just list generic best practices or ownership files.
- Gold title overlap: 0.00; max alternative title overlap: 0.40; advantage: -0.40
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p33_openai_docs`

- Family: `public_gold_validation`
- Gold skill: `public-openai-openai-docs`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Look up the current OpenAI API documentation for model parameters, tool-calling behavior, and migration notes, then summarize the relevant official guidance with links. Do not build a ChatGPT App, generate a CLI, or use Anthropic API docs.
- Gold title overlap: 0.75; max alternative title overlap: 0.50; advantage: 0.25
- Gold title hits: openai, openai, docs
- Longest copied gold phrase: -

### `public_gold_p34_playwright`

- Family: `public_gold_validation`
- Gold skill: `public-openai-playwright`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write and run Playwright browser tests for the local checkout, including navigation, form interactions, assertions, and screenshots. I do not need Chrome DevTools MCP inspection or a manual interactive browser session.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: playwright
- Longest copied gold phrase: -

### `public_gold_p35_screenshot`

- Family: `public_gold_validation`
- Gold skill: `public-openai-screenshot`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Capture a screenshot of the specified local page and return the image artifact for visual inspection. Do not write a full Playwright test suite or perform console/network debugging.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: screenshot
- Longest copied gold phrase: -

### `public_gold_p36_sentry`

- Family: `public_gold_validation`
- Gold skill: `public-openai-sentry`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use Sentry issue data to inspect the event, stack trace, release, affected users, and likely regression source. Do not build a generic observability dashboard or inspect distributed traces.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: sentry
- Longest copied gold phrase: -

### `public_gold_p37_transcribe`

- Family: `public_gold_validation`
- Gold skill: `public-openai-transcribe`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Transcribe the recorded interview audio into timestamped text with speaker turns where possible. Do not synthesize speech, produce a podcast workflow, or summarize meeting actions.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: transcribe
- Longest copied gold phrase: -

### `public_gold_p38_speech`

- Family: `public_gold_validation`
- Gold skill: `public-openai-speech`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Generate spoken audio from the supplied narration script using a text-to-speech workflow. Do not transcribe an existing recording or automate podcast publishing.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p39_jupyter_notebook`

- Family: `public_gold_validation`
- Gold skill: `public-openai-jupyter-notebook`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create or update a `.ipynb` Jupyter notebook that loads the CSV, runs Python exploratory analysis, and leaves executable cells with plots and explanations. Do not only write a static report, inspect a Hugging Face dataset, or produce an Excel workbook.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: jupyt, notebook
- Longest copied gold phrase: -

### `public_gold_p40_linear`

- Family: `public_gold_validation`
- Gold skill: `public-openai-linear`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create and update Linear issues for the implementation plan, including team/project fields, labels, priorities, and links back to the spec. Do not create GitHub, Jira, or Asana issues.
- Gold title overlap: 0.33; max alternative title overlap: 0.25; advantage: 0.08
- Gold title hits: linear
- Longest copied gold phrase: -

### `public_gold_p41_yeet`

- Family: `public_gold_validation`
- Gold skill: `public-openai-yeet`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Package the current local changes, create an intentional commit, push the branch, and open a draft GitHub pull request. Do not address existing review comments or debug CI logs.
- Gold title overlap: 0.00; max alternative title overlap: 0.50; advantage: -0.50
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p42_migrate_to_codex`

- Family: `public_gold_validation`
- Gold skill: `public-openai-migrate-to-codex`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Migrate an existing agent setup into Codex conventions, including local instructions, skills, and environment notes. Do not author a brand-new skill or install an existing one.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: migrate, codex
- Longest copied gold phrase: -

### `public_gold_p43_notion_knowledge_capture`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-knowledge-capture`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Capture mixed project notes, decisions, links, and loose observations into a durable Notion knowledge base with structured pages, tags, summaries, and backlinks. Do not extract meeting action items or build a research database only.
- Gold title overlap: 0.60; max alternative title overlap: 0.40; advantage: 0.20
- Gold title hits: notion, knowledge, capture
- Longest copied gold phrase: -

### `public_gold_p44_notion_meeting_intelligence`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-meeting-intelligence`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn the meeting transcript into Notion-ready decisions, action items, owners, due dates, and follow-up pages linked to the meeting record. Do not create a general knowledge base or research documentation page.
- Gold title overlap: 0.20; max alternative title overlap: 0.00; advantage: 0.20
- Gold title hits: meet
- Longest copied gold phrase: -

### `public_gold_p45_notion_spec_to_implementation`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-spec-to-implementation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Convert a Notion product spec into an implementation plan with scoped engineering tasks, dependencies, acceptance criteria, and links back to the source spec. Do not just document research or create generic issues.
- Gold title overlap: 0.60; max alternative title overlap: 0.25; advantage: 0.35
- Gold title hits: notion, spec, implementation
- Longest copied gold phrase: criteria link back spec

### `public_gold_p46_figma_code_connect`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-code-connect-components`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Map existing Figma components to code components using Code Connect so design components are linked to implementation examples. Do not implement a single Figma screen or generate a new component library.
- Gold title overlap: 0.67; max alternative title overlap: 0.60; advantage: 0.07
- Gold title hits: figma, code, connect, component
- Longest copied gold phrase: component code component code connect

### `public_gold_p47_figma_generate_library`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-generate-library`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Generate a reusable component library inside Figma with variants, variables, tokens, and theming foundations from the design-system brief. Do not implement an existing frame in application code, only write design-system rules, or only create Code Connect mappings.
- Gold title overlap: 0.60; max alternative title overlap: 0.67; advantage: -0.07
- Gold title hits: figma, generate, library
- Longest copied gold phrase: -

### `public_gold_p48_figma_design_system_rules`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-create-design-system-rules`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create design-system rules for Figma usage, naming, layout, component variants, and token conventions. Do not generate the actual screen or convert Figma to code.
- Gold title overlap: 0.43; max alternative title overlap: 0.40; advantage: 0.03
- Gold title hits: figma, create, rule
- Longest copied gold phrase: -

### `public_gold_p49_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit the landing page for technical SEO: title, meta description, canonical, structured data, headings, crawlability, and search snippets. Do not focus on accessibility or Core Web Vitals.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: web, seo
- Longest copied gold phrase: -

### `public_gold_p50_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Profile the web app's overall loading and runtime performance, including bundle size, network waterfalls, render blocking, and expensive client code. Do not limit the review only to LCP, INP, and CLS.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: web, performance
- Longest copied gold phrase: -

### `public_gold_p51_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Run a broad web quality audit that covers accessibility, performance, SEO, best practices, and user-facing quality risks in one prioritized report. Do not narrow it to only WCAG or only Core Web Vitals.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: web, web, quality, audit
- Longest copied gold phrase: web quality audit cover

### `public_gold_p52_api_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design stable REST module boundaries and typed request/response contracts between the frontend and backend before implementation. Do not review an existing OpenAPI contract or build a CLI.
- Gold title overlap: 0.20; max alternative title overlap: 1.00; advantage: -0.80
- Gold title hits: design
- Longest copied gold phrase: -

### `public_gold_p53_context_engineering`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-context-engineering`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare focused agent context for a new coding session by selecting relevant files, rules, project constraints, and task state without flooding the model. Do not search the codebase for one answer or migrate the project to Codex.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: context
- Longest copied gold phrase: -

### `public_gold_p54_deprecation_migration`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-deprecation-and-migration`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Plan how to sunset the legacy API while migrating callers to the new implementation, including compatibility, rollout, communication, and removal criteria. Do not perform a database migration risk review.
- Gold title overlap: 0.25; max alternative title overlap: 0.75; advantage: -0.50
- Gold title hits: migration
- Longest copied gold phrase: -

### `public_gold_p55_documentation_adrs`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-documentation-and-adrs`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write an Architecture Decision Record for the caching approach, including context, considered options, decision, consequences, and follow-up documentation. Do not write API docs or a general report.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: documentation
- Longest copied gold phrase: -

### `public_gold_p56_spec_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-spec-driven-development`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn the feature idea into a precise implementation spec with requirements, acceptance criteria, edge cases, and sequencing before coding. Do not start with tests or convert a Notion spec.
- Gold title overlap: 0.20; max alternative title overlap: 0.60; advantage: -0.40
- Gold title hits: spec
- Longest copied gold phrase: -

### `public_gold_p57_test_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-test-driven-development`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Implement the bug fix using a red-green-refactor loop: write the failing test first, make it pass, then clean up. Do not only draft a specification or general testing strategy.
- Gold title overlap: 0.20; max alternative title overlap: 0.33; advantage: -0.13
- Gold title hits: test
- Longest copied gold phrase: -

### `public_gold_p58_source_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-source-driven-development`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before changing code, inspect the existing source paths, local conventions, helper APIs, and tests so the implementation follows the codebase. Do not merely prepare generic context or search for one symbol.
- Gold title overlap: 0.00; max alternative title overlap: 0.67; advantage: -0.67
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p59_anthropic_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Use Anthropic Claude API guidance to design a Messages API call with tools, model parameters, and error-handling notes. Do not use OpenAI docs, Hugging Face CLI guidance, or build an MCP server.
- Gold title overlap: 0.75; max alternative title overlap: 0.75; advantage: 0.00
- Gold title hits: anthropic, claude, api
- Longest copied gold phrase: -

### `public_gold_p60_doc_coauthoring`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-doc-coauthoring`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Co-author the strategy document by preserving the existing argument, improving structure, adding missing sections, and keeping revision notes. Do not only rewrite tone or generate a report from scratch.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: -

### `public_gold_p61_canvas_design`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-canvas-design`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create a canvas-based visual composition for an explainer, with layout, typography, and interactive visual elements. Do not build a frontend web app or Figma design file.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: design
- Longest copied gold phrase: -

### `public_gold_p62_theme_factory`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-theme-factory`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Generate a reusable visual theme with palette, type scale, spacing, and component styling tokens for a product prototype. Do not write full brand guidelines or implement the frontend.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: theme
- Longest copied gold phrase: -

### `public_gold_p63_hf_zerogpu`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-zerogpu`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare the Hugging Face Space to run on ZeroGPU, including decorators, GPU-duration constraints, queue behavior, and deployment caveats. Do not just build a Gradio UI or choose a local model.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: zerogpu
- Longest copied gold phrase: -

### `public_gold_p64_hf_llm_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-llm-trainer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Fine-tune a causal language model with Hugging Face training code, tokenizer setup, instruction dataset formatting, evaluation, and push-to-hub notes. Do not train a vision model, train a SentenceTransformer embedding model, or only evaluate an LLM.
- Gold title overlap: 0.40; max alternative title overlap: 0.50; advantage: -0.10
- Gold title hits: llm, train
- Longest copied gold phrase: -

### `public_gold_p65_hf_local_models`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-local-models`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Choose and run a local Hugging Face model for laptop inference with GGUF or llama.cpp-style runtime choices, quantization, memory limits, and local serving options. Do not train a model, deploy a Space, or build browser-side Transformers.js inference.
- Gold title overlap: 0.40; max alternative title overlap: 0.33; advantage: 0.07
- Gold title hits: local, model
- Longest copied gold phrase: -

### `public_gold_p66_hf_trackio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-trackio`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Instrument the training run with Trackio experiment tracking, logging metrics, configs, artifacts, and run comparison. Do not design a community evaluation or SaaS metrics dashboard.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: trackio
- Longest copied gold phrase: -

### `public_gold_p67_hf_papers`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-papers`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Find relevant Hugging Face paper entries for this model topic, compare abstracts and linked artifacts, and summarize which papers are most relevant. Do not publish a paper page or write a manuscript.
- Gold title overlap: 0.25; max alternative title overlap: 0.40; advantage: -0.15
- Gold title hits: paper
- Longest copied gold phrase: -

### `public_gold_p68_hf_paper_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-paper-publisher`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare and publish the model paper artifacts to Hugging Face, including metadata, model links, and paper page details. Do not merely search existing papers or write the academic manuscript.
- Gold title overlap: 0.40; max alternative title overlap: 0.50; advantage: -0.10
- Gold title hits: pap, publish
- Longest copied gold phrase: -

### `public_gold_p69_transformers_js`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-transformers-js`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Build a browser-side ML demo using Transformers.js so inference runs in the client, with model loading and UI wiring. Do not build a Python Gradio demo or local server inference script.
- Gold title overlap: 0.33; max alternative title overlap: 0.40; advantage: -0.07
- Gold title hits: transformer
- Longest copied gold phrase: -

### `public_gold_p70_obsidian_json_canvas`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-json-canvas`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Create an Obsidian JSON Canvas map with nodes and edges representing the research argument. Do not just write Markdown notes, a Bases view, or CLI commands.
- Gold title overlap: 0.75; max alternative title overlap: 0.75; advantage: 0.00
- Gold title hits: obsidian, json, canva
- Longest copied gold phrase: -

### `public_gold_p71_obsidian_bases`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-bases`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Build an Obsidian Bases view for the vault that filters notes by metadata fields, status, and tags. Do not create a JSON Canvas graph or run generic CLI commands.
- Gold title overlap: 0.75; max alternative title overlap: 0.75; advantage: 0.00
- Gold title hits: obsidian, obsidian, base
- Longest copied gold phrase: -

### `public_gold_p72_obsidian_cli`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-cli`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Use the Obsidian CLI to create, update, and query vault notes from the terminal with command-line operations. Do not hand-write a Markdown note, maintain a general vault workflow, or create a canvas file.
- Gold title overlap: 0.75; max alternative title overlap: 0.50; advantage: 0.25
- Gold title hits: obsidian, obsidian, cli
- Longest copied gold phrase: -

### `public_gold_p73_excel_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-excel-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Automate an Excel workbook by adding formulas, formatting, pivot-style summaries, and saved workbook output. Do not use Google Sheets or only analyze the data.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: excel
- Longest copied gold phrase: -

### `public_gold_p74_sheets_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-sheets-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Automate a Google Sheets workbook with formulas, tabs, formatting, and update steps using the online Sheets workflow. Do not produce a local Excel or XLSX file.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: sheet
- Longest copied gold phrase: -

### `public_gold_p75_airtable_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-airtable-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create an Airtable automation that routes new form submissions, updates linked records, and sends follow-up notifications. Do not build a Notion or CRM workflow.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: airtable, automation
- Longest copied gold phrase: -

### `public_gold_p76_invoice_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-invoice-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Automate the accounts-payable invoice workflow from incoming invoice files through extraction, validation, approval routing, and accounting-system update. Do not merely generate a single outbound invoice template.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: invoice
- Longest copied gold phrase: -

### `public_gold_p77_lead_routing`

- Family: `public_gold_validation`
- Gold skill: `public-office-lead-routing`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Route inbound leads to the right sales owner based on region, company size, product interest, and priority rules. Do not only research or qualify the lead.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: lead
- Longest copied gold phrase: -

### `public_gold_p78_saas_metrics`

- Family: `public_gold_validation`
- Gold skill: `public-office-saas-metrics`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Calculate SaaS metrics such as MRR, ARR, churn, expansion, retention cohorts, CAC payback, and LTV from the subscription export. Do not build a DCF valuation or stock analysis report.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: saas, metric
- Longest copied gold phrase: -

### `public_gold_p79_stock_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-stock-analysis`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Analyze a listed company's stock using recent financials, valuation multiples, catalysts, risks, and investment view. Do not write a crypto report or only build a DCF spreadsheet.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: stock, analysi
- Longest copied gold phrase: -

### `public_gold_p80_dcf_valuation`

- Family: `public_gold_validation`
- Gold skill: `public-office-dcf-valuation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Build a DCF valuation with revenue forecasts, margin assumptions, WACC, terminal value, sensitivity table, and implied share value. Do not only write a stock memo.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: dcf, valuation
- Longest copied gold phrase: -

### `public_gold_p81_shopify_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-shopify-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Automate Shopify Admin product and order workflows for a Shopify store, including product updates, fulfillment status changes, and customer notifications through Shopify-specific operations. Do not build WooCommerce, Amazon seller, or Stripe payment automation.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: shopify, automation
- Longest copied gold phrase: -

### `public_gold_p82_zendesk_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-zendesk-automation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Automate Zendesk ticket triage, tags, macros, assignments, and escalation rules for support requests. Do not build Intercom, Slack, or email classification automation.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: zendesk, automation
- Longest copied gold phrase: -
