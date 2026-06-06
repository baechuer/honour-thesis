# Procedural Distinctness Report

This report implements Step 2 of the benchmark rubric: each gold skill should be procedurally distinguishable from its closest alternatives before we test semantic confusability or retrieval accuracy.

Important interpretation: `not_for` boundaries are treated as supporting evidence, not as a primary reason by themselves. This prevents the benchmark from passing only because a skill contains a negated rule.

## Overall Status

- Step 2 status: **PASS**
- Prompts with at least one primary procedural differentiator for every alternative: 82/82 (100.0%)
- Gold/alternative pairs with at least one primary differentiator: 315/315 (100.0%)
- Gold/alternative pairs with two or more primary differentiators: 288/315 (91.4%)
- Prompts where all listed alternatives differ on two or more primary axes: 64/82 (78.0%)

Pass rule used here: every pair needs at least one primary procedural axis; the benchmark is considered strong when at least 80% of pairs have two or more primary axes.

What this proves: the current controlled skills expose positive procedural differences in their structured fields. What it does not prove yet: that flat metadata, embeddings, tree routing, graph retrieval, or rerankers will recover those differences under semantic similarity and scale. That is tested in later rubric steps.

Why Step 2 was previously unresolved: the coverage report showed that fields existed, but it did not compare each gold skill against its listed near alternatives. This report performs that pair-level check.

## Axis Frequency

| Primary axis | Pair count |
|---|---:|
| input/precondition | 195 |
| output artifact | 108 |
| workflow | 306 |
| success criterion | 228 |
| dependency/resource | 226 |

| Supporting boundary axis | Pair count |
|---|---:|
| avoid/not-for boundary | 116 |

## Family Summary

| Family | Prompts | Prompt pass | Strong prompts | Weak pairs |
|---|---:|---:|---:|---:|
| public_gold_validation | 82 | 82/82 | 64/82 | 27/315 |

## Weak Or Review-Worthy Pairs

These are not automatically bad; they are the first pairs to inspect manually because they have fewer than two primary procedural differentiators.

| Prompt | Gold | Alternative | Primary axes | Supporting axes | Main evidence |
|---|---|---|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | `public-office-pdf-converter` | workflow | - | gold: 5-10, code, csv, example; alt: 1-5, 300, columns, create |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | `public-office-pdf-compress` | workflow | - | gold: 5-10, alphabetical, combine, document1; alt: compress, compression, critical, email |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | `public-office-pdf-converter` | workflow | - | gold: 5-10, alphabetical, combine, document1; alt: 1-5, 300, columns, convert |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | `public-office-pdf-watermark` | workflow | - | gold: 5-10, alphabetical, combine, document1; alt: add, apply, bottom, center |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | `public-office-mcp-hub` | workflow | - | gold: answer, answers, best, checklist; alt: access, accomplish, analysis, appropriate |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | `public-office-data-extractor` | workflow | - | gold: 100, 1000000, 1000_rows, 2_hours; alt: attachments, body, document, documents |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | `public-office-database-sync` | workflow | - | gold: 1000000, 1000_rows, 2_hours, 2am; alt: 00z, 10000, 12345, 156 |
| `public_gold_p26_database_sync` | `public-office-database-sync` | `public-office-data-pipeline` | workflow | - | gold: 00z, 10000, 12345, 156; alt: 1000000, 1000_rows, 2_hours, 2am |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | `public-office-security-monitoring` | workflow | - | gold: address, click, don't, full; alt: 100, 100mb, 10_minutes, 15_minutes |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | `public-office-dev-slides` | workflow | - | gold: 10-slide, audience, basics, complete; alt: blocks, code, components, describe |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | `public-office-html-slides` | workflow | - | gold: 10-slide, audience, basics, complete; alt: animations, code, describe, features |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | `public-office-md-slides` | workflow | - | gold: 10-slide, audience, basics, complete; alt: content, convert, directives, export |
| `public_gold_p34_playwright` | `public-openai-playwright` | `public-anthropic-webapp-testing` | workflow | - | gold: -; alt: 3000, 5173, actions, already |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | `public-anthropic-webapp-testing` | workflow | - | gold: app, blocked, capture, checks; alt: 3000, 5173, actions, already |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | `public-office-browser-automation` | workflow | - | gold: app, bash, blocked, capture; alt: - |
| `public_gold_p35_screenshot` | `public-openai-screenshot` | `public-openai-playwright` | workflow | - | gold: app, bash, blocked, capture; alt: - |
| `public_gold_p36_sentry` | `public-openai-sentry` | `public-swebench-python-observability` | dependency/resource | - | gold: sentry; alt: observability, python |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | `public-office-notion-automation` | workflow | - | gold: actions, add, again, alternatives; alt: append, capture_data, clearbit, company |
| `public_gold_p43_notion_knowledge_capture` | `public-openai-notion-knowledge-capture` | `public-openai-notion-meeting-intelligence` | workflow | - | gold: actions, alternatives, answers, assets; alt: action, adapt, agenda, approval |
| `public_gold_p44_notion_meeting_intelligence` | `public-openai-notion-meeting-intelligence` | `public-office-notion-automation` | workflow | - | gold: action, adapt, add, again; alt: append, capture_data, clearbit, company |
| `public_gold_p45_notion_spec_to_implementation` | `public-openai-notion-spec-to-implementation` | `public-openai-notion-knowledge-capture` | workflow | - | gold: acceptance, action, assignee, assumptions; alt: actions, alternatives, answers, assets |
| `public_gold_p62_theme_factory` | `public-anthropic-theme-factory` | `public-anthropic-frontend-design` | workflow | - | gold: -; alt: aesthetic, beautiful, choose, code |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | `public-huggingface-huggingface-gradio` | dependency/resource | - | gold: local, models; alt: gradio |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | `public-office-crm-automation` | dependency/resource | - | gold: access, account, airtable, api; alt: artifact, crm |
| `public_gold_p75_airtable_automation` | `public-office-airtable-automation` | `public-office-notion-automation` | workflow | - | gold: -; alt: append, capture_data, clearbit, company |
| `public_gold_p76_invoice_automation` | `public-office-invoice-automation` | `public-office-invoice-organizer` | workflow | - | gold: apply, branding, creation, customer; alt: add, categorize, category, create |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | `public-office-stripe-payments` | workflow | - | gold: checks, fraud_score, inventory_available, payment_captured; alt: auth, capture, card, checkout |

## Prompt Detail

### `public_gold_p01_pdf_extraction`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-extraction`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-chat-with-pdf` | output artifact, workflow, success criterion | - | input/precondition=0.98, output artifact=0.00, workflow=0.09, success criterion=0.00, dependency/resource=0.96, avoid/not-for boundary=1.00 |
| `public-office-pdf-ocr` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.15, output artifact=0.00, workflow=0.11, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=1.00 |
| `public-office-pdf-converter` | workflow | - | input/precondition=0.98, output artifact=1.00, workflow=0.14, success criterion=1.00, dependency/resource=0.96, avoid/not-for boundary=1.00 |
| `public-openai-pdf` | workflow, success criterion | - | input/precondition=1.00, output artifact=1.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=1.00 |

### `public_gold_p02_pdf_ocr`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-ocr`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-pdf-extraction` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.15, output artifact=0.00, workflow=0.11, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=1.00 |
| `public-office-chat-with-pdf` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.15, output artifact=0.07, workflow=0.05, success criterion=0.07, dependency/resource=0.96, avoid/not-for boundary=1.00 |
| `public-office-pdf-converter` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.15, output artifact=0.00, workflow=0.13, success criterion=0.00, dependency/resource=0.96, avoid/not-for boundary=1.00 |
| `public-openai-pdf` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.15, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=1.00 |

### `public_gold_p03_pdf_form_filler`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-form-filler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-pdf-extraction` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.20, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-office-pdf-converter` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.20, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |
| `public-office-template-engine` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.13, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.34, avoid/not-for boundary=1.00 |

### `public_gold_p04_markitdown_conversion`

- Family: `public_gold_validation`
- Gold skill: `public-markitdown`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.02, workflow=0.03, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-pdf-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.20, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=0.20, avoid/not-for boundary=1.00 |
| `public-office-batch-convert` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.17, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.11, avoid/not-for boundary=1.00 |
| `public-office-doc-parser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.20, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.11, avoid/not-for boundary=1.00 |

### `public_gold_p05_pdf_merge_split`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-merge-split`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-pdf-converter` | workflow | - | input/precondition=0.93, output artifact=1.00, workflow=0.17, success criterion=1.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |
| `public-office-pdf-watermark` | workflow | - | input/precondition=0.93, output artifact=1.00, workflow=0.09, success criterion=1.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |
| `public-office-pdf-compress` | workflow | - | input/precondition=0.93, output artifact=1.00, workflow=0.05, success criterion=1.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |
| `public-openai-pdf` | workflow, success criterion | - | input/precondition=0.95, output artifact=1.00, workflow=0.05, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |

### `public_gold_p06_browser_devtools_testing`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-browser-testing-with-devtools`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-playwright` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.66, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=0.00 |
| `public-playwright-interactive` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.03, success criterion=0.01, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `public-office-browser-automation` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.86, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.88, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.96, avoid/not-for boundary=0.00 |

### `public_gold_p07_web_accessibility`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-accessibility`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-web-web-quality-audit` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.43, output artifact=1.00, workflow=0.01, success criterion=0.01, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-addy-web-core-web-vitals` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.33, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-web-best-practices` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.41, output artifact=1.00, workflow=0.01, success criterion=0.02, dependency/resource=0.80, avoid/not-for boundary=1.00 |

### `public_gold_p08_core_web_vitals`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-core-web-vitals`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-web-accessibility` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.33, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-web-best-practices` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.46, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.71, avoid/not-for boundary=1.00 |
| `public-addy-web-performance` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.31, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-agent-browser-testing-with-devtools` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.35, avoid/not-for boundary=0.00 |

### `public_gold_p09_systematic_debugging`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-debugging`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-agent-code-simplification` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.01 |
| `public-oh-my-code-review` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.21, output artifact=0.09, workflow=0.09, success criterion=0.04, dependency/resource=0.80, avoid/not-for boundary=0.12 |
| `public-addy-agent-code-review-and-quality` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=0.00, workflow=0.03, success criterion=0.01, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-openai-gh-fix-ci` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=0.00 |

### `public_gold_p10_analyze_ci`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-analyze-ci`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-github-actions-templates` | input/precondition, workflow, dependency/resource | - | input/precondition=0.51, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-agent-ci-cd-and-automation` | input/precondition, workflow, success criterion | - | input/precondition=0.40, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-oh-my-debugging` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=0.00 |
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `repo-ops-failure-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.08, avoid/not-for boundary=0.00 |

### `public_gold_p11_setup_pre_commit`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-setup-pre-commit`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `git-safety-guardrail-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-mattpocock-git-guardrails-claude-code` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.46, avoid/not-for boundary=1.00 |
| `public-swebench-fix` | workflow, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `git-commit-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.32, avoid/not-for boundary=0.00 |
| `public-swebench-github-actions-templates` | workflow, dependency/resource | - | input/precondition=0.82, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.67, avoid/not-for boundary=1.00 |

### `public_gold_p12_git_guardrails`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-git-guardrails-claude-code`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-mattpocock-setup-pre-commit` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.46, avoid/not-for boundary=1.00 |
| `public-addy-agent-git-workflow-and-versioning` | workflow, dependency/resource | - | input/precondition=0.74, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.54, avoid/not-for boundary=1.00 |
| `public-openai-yeet` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `version-control-helper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.23, avoid/not-for boundary=0.00 |
| `public-swebench-github-actions-templates` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.46, avoid/not-for boundary=1.00 |

### `public_gold_p13_address_pr_comments`

- Family: `public_gold_validation`
- Gold skill: `public-openai-gh-address-comments`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-gh-fix-ci` | workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.90, output artifact=1.00, workflow=0.08, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-openai-yeet` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=1.00, workflow=0.06, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-lbussell-creating-pull-requests` | workflow, dependency/resource | - | input/precondition=0.78, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.71, avoid/not-for boundary=1.00 |
| `public-lbussell-triaging-issues` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.38, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p14_netlify_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-netlify-deploy`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-vercel-deploy` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.56, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.53, avoid/not-for boundary=1.00 |
| `public-openai-cloudflare-deploy` | workflow, dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.53, avoid/not-for boundary=1.00 |
| `public-openai-render-deploy` | workflow, success criterion, dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=0.12, success criterion=0.00, dependency/resource=0.53, avoid/not-for boundary=1.00 |
| `public-oh-my-vercel-deploy` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=0.53, avoid/not-for boundary=0.00 |

### `public_gold_p15_cloudflare_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cloudflare-deploy`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-netlify-deploy` | workflow, dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.53, avoid/not-for boundary=1.00 |
| `public-openai-vercel-deploy` | output artifact, workflow, success criterion | - | input/precondition=0.72, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.92, avoid/not-for boundary=1.00 |
| `public-openai-render-deploy` | workflow, success criterion | - | input/precondition=1.00, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.92, avoid/not-for boundary=1.00 |
| `public-swebench-k8s-manifest-generator` | input/precondition, workflow, dependency/resource | - | input/precondition=0.07, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.44, avoid/not-for boundary=1.00 |

### `public_gold_p16_render_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-render-deploy`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-netlify-deploy` | workflow, success criterion, dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=0.12, success criterion=0.00, dependency/resource=0.53, avoid/not-for boundary=1.00 |
| `public-openai-vercel-deploy` | output artifact, workflow, success criterion | - | input/precondition=0.72, output artifact=0.00, workflow=0.00, success criterion=0.01, dependency/resource=0.92, avoid/not-for boundary=1.00 |
| `public-openai-cloudflare-deploy` | workflow, success criterion | - | input/precondition=1.00, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.92, avoid/not-for boundary=1.00 |
| `public-swebench-k8s-manifest-generator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.07, output artifact=1.00, workflow=0.07, success criterion=0.00, dependency/resource=0.44, avoid/not-for boundary=1.00 |

### `public_gold_p17_mcp_builder`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-mcp-builder`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-api-design-principles` | input/precondition, workflow, dependency/resource | - | input/precondition=0.23, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.12, avoid/not-for boundary=1.00 |
| `public-office-mcp-hub` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-openai-chatgpt-apps` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=1.00, workflow=0.04, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=0.00 |
| `webhook-integration-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p18_chatgpt_apps`

- Family: `public_gold_validation`
- Gold skill: `public-openai-chatgpt-apps`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-anthropic-mcp-builder` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=1.00, workflow=0.04, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=0.00 |
| `public-openai-cli-creator` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.21, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-openai-openai-docs` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.25, output artifact=1.00, workflow=0.05, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=0.00 |
| `public-office-ai-agent-builder` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |

### `public_gold_p19_cli_creator`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cli-creator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-openai-docs` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.21, output artifact=1.00, workflow=0.05, success criterion=0.00, dependency/resource=0.52, avoid/not-for boundary=1.00 |
| `public-obsidian-obsidian-cli` | input/precondition, workflow, success criterion | - | input/precondition=0.32, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `openapi-contract-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `mcp-server-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p20_hf_datasets`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-datasets`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-hf-cli` | input/precondition, workflow, dependency/resource | - | input/precondition=0.31, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.14, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.26, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=1.00 |
| `public-huggingface-train-sentence-transformers` | input/precondition, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.25, output artifact=1.00, workflow=1.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.00 |
| `public-office-data-extractor` | input/precondition, workflow, dependency/resource | - | input/precondition=0.34, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.14, avoid/not-for boundary=1.00 |

### `public_gold_p21_hf_gradio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-gradio`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-zerogpu` | input/precondition, workflow, success criterion | - | input/precondition=0.53, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.46, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-huggingface-datasets` | input/precondition, dependency/resource | - | input/precondition=0.32, output artifact=1.00, workflow=1.00, success criterion=1.00, dependency/resource=0.14, avoid/not-for boundary=1.00 |
| `public-huggingface-transformers-js` | workflow, success criterion, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |

### `public_gold_p22_hf_vision_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-vision-trainer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-llm-trainer` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.23, output artifact=1.00, workflow=0.08, success criterion=0.23, dependency/resource=0.88, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-community-evals` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.21, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-local-models` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.22, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=0.00 |
| `public-huggingface-train-sentence-transformers` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=1.00, workflow=0.00, success criterion=0.01, dependency/resource=0.67, avoid/not-for boundary=0.00 |

### `public_gold_p23_sentence_transformer_training`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-train-sentence-transformers`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-transformers-js` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.31, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-llm-trainer` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.16, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.67, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-local-models` | input/precondition, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.30, output artifact=1.00, workflow=1.00, success criterion=0.00, dependency/resource=0.67, avoid/not-for boundary=0.00 |
| `public-huggingface-datasets` | input/precondition, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.25, output artifact=1.00, workflow=1.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.00 |

### `public_gold_p24_hf_cli`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-hf-cli`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-datasets` | input/precondition, workflow, dependency/resource | - | input/precondition=0.31, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.14, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-paper-publisher` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-local-models` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.42, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p25_data_pipeline`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-pipeline`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-data-analysis` | output artifact, workflow, success criterion | - | input/precondition=0.56, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.95, avoid/not-for boundary=1.00 |
| `public-office-data-extractor` | workflow | - | input/precondition=0.97, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.95, avoid/not-for boundary=1.00 |
| `public-office-database-sync` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.10, success criterion=1.00, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-swebench-dbt-transformation-patterns` | workflow, dependency/resource | - | input/precondition=0.72, output artifact=1.00, workflow=0.09, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=1.00 |

### `public_gold_p26_database_sync`

- Family: `public_gold_validation`
- Gold skill: `public-office-database-sync`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-data-pipeline` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.10, success criterion=1.00, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-office-airtable-automation` | input/precondition, workflow, dependency/resource | - | input/precondition=0.52, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.30, avoid/not-for boundary=1.00 |
| `public-office-crm-automation` | workflow, dependency/resource | - | input/precondition=0.70, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.50, avoid/not-for boundary=1.00 |
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.55, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |

### `public_gold_p27_contract_review`

- Family: `public_gold_validation`
- Gold skill: `public-office-contract-review`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-contract-template` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.94, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=0.00 |
| `public-security-threat-model` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.46, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.17, avoid/not-for boundary=0.00 |
| `public-office-proposal-writer` | output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.88, output artifact=0.00, workflow=0.04, success criterion=0.06, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `document-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.03, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.03 |

### `public_gold_p28_suspicious_email`

- Family: `public_gold_validation`
- Gold skill: `public-office-suspicious-email`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-email-classifier` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.21, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.54, avoid/not-for boundary=1.00 |
| `public-office-email-drafter` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.72, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.54, avoid/not-for boundary=1.00 |
| `public-office-gmail-workflows` | input/precondition, workflow, dependency/resource | - | input/precondition=0.50, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.28, avoid/not-for boundary=1.00 |
| `public-office-security-monitoring` | workflow | - | input/precondition=0.93, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.88, avoid/not-for boundary=1.00 |

### `public_gold_p29_ai_slides`

- Family: `public_gold_validation`
- Gold skill: `public-office-ai-slides`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-md-slides` | workflow | - | input/precondition=1.00, output artifact=1.00, workflow=0.29, success criterion=1.00, dependency/resource=1.00, avoid/not-for boundary=1.00 |
| `public-office-html-slides` | workflow | - | input/precondition=0.97, output artifact=1.00, workflow=0.23, success criterion=1.00, dependency/resource=0.95, avoid/not-for boundary=1.00 |
| `public-office-dev-slides` | workflow | - | input/precondition=0.88, output artifact=1.00, workflow=0.18, success criterion=1.00, dependency/resource=0.95, avoid/not-for boundary=1.00 |
| `public-anthropic-theme-factory` | workflow, dependency/resource | - | input/precondition=0.74, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.58, avoid/not-for boundary=1.00 |

### `public_gold_p30_figma_implement_design`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-implement-design`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-figma-generate-design` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.43, output artifact=0.08, workflow=0.04, success criterion=0.19, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-openai-figma-generate-library` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.18, output artifact=0.00, workflow=0.08, success criterion=0.05, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-openai-figma-code-connect-components` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.62, output artifact=0.04, workflow=0.08, success criterion=0.34, dependency/resource=0.83, avoid/not-for boundary=1.00 |
| `public-openai-figma-use` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.28, output artifact=0.00, workflow=0.05, success criterion=0.04, dependency/resource=0.95, avoid/not-for boundary=1.00 |

### `public_gold_p31_skill_creator`

- Family: `public_gold_validation`
- Gold skill: `public-skill-creator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-skill-installer` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.12, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.11, avoid/not-for boundary=1.00 |
| `public-openai-migrate-to-codex` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.12, output artifact=1.00, workflow=0.03, success criterion=0.03, dependency/resource=0.18, avoid/not-for boundary=1.00 |
| `public-oh-my-agentic-skills` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=1.00, workflow=0.02, success criterion=0.01, dependency/resource=0.18, avoid/not-for boundary=0.00 |
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p32_security_threat_model`

- Family: `public_gold_validation`
- Gold skill: `public-security-threat-model`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-security-best-practices` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.30, output artifact=1.00, workflow=0.06, success criterion=1.00, dependency/resource=0.19, avoid/not-for boundary=0.00 |
| `public-openai-security-ownership-map` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.19, avoid/not-for boundary=0.00 |
| `public-swebench-security-review` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.19, avoid/not-for boundary=0.00 |

### `public_gold_p33_openai_docs`

- Family: `public_gold_validation`
- Gold skill: `public-openai-openai-docs`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-chatgpt-apps` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.25, output artifact=1.00, workflow=0.05, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=0.00 |
| `public-openai-cli-creator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.21, output artifact=1.00, workflow=0.05, success criterion=0.00, dependency/resource=0.52, avoid/not-for boundary=1.00 |
| `public-anthropic-claude-api` | input/precondition, workflow, success criterion | - | input/precondition=0.20, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.28, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.56, avoid/not-for boundary=1.00 |

### `public_gold_p34_playwright`

- Family: `public_gold_validation`
- Gold skill: `public-openai-playwright`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-playwright-interactive` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.19, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.28, avoid/not-for boundary=1.00 |
| `public-addy-agent-browser-testing-with-devtools` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.66, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | workflow | - | input/precondition=0.70, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.96, avoid/not-for boundary=1.00 |

### `public_gold_p35_screenshot`

- Family: `public_gold_validation`
- Gold skill: `public-openai-screenshot`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-playwright` | workflow | - | input/precondition=0.62, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-addy-agent-browser-testing-with-devtools` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.75, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=0.00 |
| `public-office-browser-automation` | workflow | - | input/precondition=0.82, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-anthropic-webapp-testing` | workflow | - | input/precondition=0.84, output artifact=1.00, workflow=0.06, success criterion=1.00, dependency/resource=0.96, avoid/not-for boundary=1.00 |

### `public_gold_p36_sentry`

- Family: `public_gold_validation`
- Gold skill: `public-openai-sentry`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-oh-my-monitoring-observability` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-swebench-python-observability` | dependency/resource | - | input/precondition=0.90, output artifact=1.00, workflow=1.00, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `distributed-trace-investigator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p37_transcribe`

- Family: `public_gold_validation`
- Gold skill: `public-openai-transcribe`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-speech` | workflow, success criterion | avoid/not-for boundary | input/precondition=0.93, output artifact=1.00, workflow=0.21, success criterion=0.56, dependency/resource=0.86, avoid/not-for boundary=0.00 |
| `public-office-transcription-automation` | workflow, success criterion, dependency/resource | - | input/precondition=0.90, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-office-podcast-automation` | workflow, success criterion, dependency/resource | - | input/precondition=0.90, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-office-meeting-notes` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.90, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |

### `public_gold_p38_speech`

- Family: `public_gold_validation`
- Gold skill: `public-openai-speech`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-transcribe` | workflow, success criterion | avoid/not-for boundary | input/precondition=0.93, output artifact=1.00, workflow=0.21, success criterion=0.56, dependency/resource=0.86, avoid/not-for boundary=0.00 |
| `public-office-transcription-automation` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.90, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-office-podcast-automation` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.90, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-anthropic-slack-gif-creator` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.60, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.37, avoid/not-for boundary=0.00 |

### `public_gold_p39_jupyter_notebook`

- Family: `public_gold_validation`
- Gold skill: `public-openai-jupyter-notebook`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.42, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.52, avoid/not-for boundary=1.00 |
| `public-huggingface-datasets` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.36, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.14, avoid/not-for boundary=1.00 |
| `public-swebench-python-configuration` | workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-report-generator` | workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p40_linear`

- Family: `public_gold_validation`
- Gold skill: `public-openai-linear`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-lbussell-creating-issues` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.37, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.38, avoid/not-for boundary=1.00 |
| `public-lbussell-triaging-issues` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.22, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.38, avoid/not-for boundary=1.00 |
| `public-office-jira-automation` | input/precondition, workflow, success criterion | - | input/precondition=0.40, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-office-asana-automation` | input/precondition, workflow, success criterion | - | input/precondition=0.40, output artifact=1.00, workflow=0.07, success criterion=0.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |

### `public_gold_p41_yeet`

- Family: `public_gold_validation`
- Gold skill: `public-openai-yeet`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-gh-address-comments` | input/precondition, workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=1.00, workflow=0.06, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-openai-gh-fix-ci` | input/precondition, workflow | avoid/not-for boundary | input/precondition=0.41, output artifact=1.00, workflow=0.09, success criterion=1.00, dependency/resource=0.86, avoid/not-for boundary=0.00 |

### `public_gold_p42_migrate_to_codex`

- Family: `public_gold_validation`
- Gold skill: `public-openai-migrate-to-codex`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-skill-creator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.12, output artifact=1.00, workflow=0.03, success criterion=0.03, dependency/resource=0.18, avoid/not-for boundary=1.00 |
| `public-skill-installer` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.23, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.12, avoid/not-for boundary=1.00 |
| `public-addy-agent-context-engineering` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.17, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-oh-my-agentic-skills` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |

### `public_gold_p43_notion_knowledge_capture`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-knowledge-capture`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-notion-meeting-intelligence` | workflow | - | input/precondition=0.91, output artifact=1.00, workflow=0.32, success criterion=1.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-office-notion-automation` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |

### `public_gold_p44_notion_meeting_intelligence`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-meeting-intelligence`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-notion-automation` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |

### `public_gold_p45_notion_spec_to_implementation`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-spec-to-implementation`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-notion-knowledge-capture` | workflow | - | input/precondition=0.91, output artifact=1.00, workflow=0.34, success criterion=1.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-addy-agent-spec-driven-development` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.24, output artifact=1.00, workflow=0.05, success criterion=0.00, dependency/resource=0.39, avoid/not-for boundary=0.00 |
| `public-lbussell-creating-issues` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.50, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.35, avoid/not-for boundary=1.00 |
| `public-openai-linear` | input/precondition, workflow, success criterion | - | input/precondition=0.39, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |

### `public_gold_p46_figma_code_connect`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-code-connect-components`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-figma-implement-design` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.62, output artifact=0.04, workflow=0.08, success criterion=0.34, dependency/resource=0.83, avoid/not-for boundary=1.00 |
| `public-openai-figma-generate-library` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.16, output artifact=0.00, workflow=0.08, success criterion=0.05, dependency/resource=0.79, avoid/not-for boundary=1.00 |
| `public-openai-figma-generate-design` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.42, output artifact=0.03, workflow=0.07, success criterion=0.15, dependency/resource=0.83, avoid/not-for boundary=1.00 |
| `public-openai-figma-use` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.24, output artifact=0.02, workflow=0.05, success criterion=0.04, dependency/resource=0.86, avoid/not-for boundary=1.00 |

### `public_gold_p47_figma_generate_library`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-generate-library`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-figma-code-connect-components` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.16, output artifact=0.00, workflow=0.08, success criterion=0.05, dependency/resource=0.79, avoid/not-for boundary=1.00 |
| `public-openai-figma-implement-design` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.18, output artifact=0.00, workflow=0.08, success criterion=0.05, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-openai-figma-create-design-system-rules` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.18, output artifact=1.00, workflow=0.08, success criterion=0.04, dependency/resource=0.79, avoid/not-for boundary=1.00 |

### `public_gold_p48_figma_design_system_rules`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-create-design-system-rules`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-figma-generate-library` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.18, output artifact=1.00, workflow=0.08, success criterion=0.04, dependency/resource=0.79, avoid/not-for boundary=1.00 |
| `public-openai-figma-generate-design` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.42, output artifact=0.00, workflow=0.03, success criterion=0.07, dependency/resource=0.83, avoid/not-for boundary=1.00 |
| `public-anthropic-brand-guidelines` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.37, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.78, avoid/not-for boundary=1.00 |
| `public-anthropic-theme-factory` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.36, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p49_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-web-accessibility` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=0.00 |
| `public-addy-web-core-web-vitals` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.53, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-addy-web-best-practices` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.74, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |

### `public_gold_p50_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-web-core-web-vitals` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.31, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-web-best-practices` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.41, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-addy-agent-performance-optimization` | input/precondition, workflow | - | input/precondition=0.34, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-addy-web-web-quality-audit` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.41, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |

### `public_gold_p51_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-web-accessibility` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.43, output artifact=1.00, workflow=0.01, success criterion=0.01, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-addy-web-core-web-vitals` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.54, output artifact=1.00, workflow=0.00, success criterion=0.13, dependency/resource=0.77, avoid/not-for boundary=0.00 |
| `public-addy-web-seo` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.06 |
| `public-addy-web-best-practices` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.70, output artifact=1.00, workflow=0.00, success criterion=0.01, dependency/resource=0.71, avoid/not-for boundary=0.00 |

### `public_gold_p52_api_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `openapi-contract-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-cli-creator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.25, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.43, avoid/not-for boundary=1.00 |
| `external-api-integration-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p53_context_engineering`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-context-engineering`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-agent-source-driven-development` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.26, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-addy-agent-planning-and-task-breakdown` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.19, output artifact=0.00, workflow=0.01, success criterion=0.04, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-oh-my-codebase-search` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-openai-migrate-to-codex` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.17, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |

### `public_gold_p54_deprecation_migration`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-deprecation-and-migration`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-mattpocock-migrate-to-shoehorn` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.24, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-agent-incremental-implementation` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.24, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-addy-agent-api-and-interface-design` | input/precondition, workflow, dependency/resource | - | input/precondition=0.27, output artifact=1.00, workflow=0.04, success criterion=1.00, dependency/resource=0.43, avoid/not-for boundary=1.00 |
| `database-migration-risk-assessor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p55_documentation_adrs`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-documentation-and-adrs`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-oh-my-api-documentation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.17, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.65, avoid/not-for boundary=0.00 |
| `code-documentation-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.02, success criterion=0.04, dependency/resource=0.33, avoid/not-for boundary=0.00 |
| `public-openai-notion-research-documentation` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.24, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.40, avoid/not-for boundary=1.00 |
| `public-office-report-generator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.25, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p56_spec_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-spec-driven-development`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-agent-test-driven-development` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.30, output artifact=1.00, workflow=0.01, success criterion=0.01, dependency/resource=0.88, avoid/not-for boundary=0.00 |
| `public-addy-agent-incremental-implementation` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.27, output artifact=1.00, workflow=0.03, success criterion=0.03, dependency/resource=0.71, avoid/not-for boundary=0.00 |
| `public-openai-notion-spec-to-implementation` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.24, output artifact=1.00, workflow=0.05, success criterion=0.00, dependency/resource=0.39, avoid/not-for boundary=0.00 |
| `public-mattpocock-to-prd` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.27, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |

### `public_gold_p57_test_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-test-driven-development`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-agent-spec-driven-development` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.30, output artifact=1.00, workflow=0.01, success criterion=0.01, dependency/resource=0.88, avoid/not-for boundary=0.00 |
| `public-oh-my-testing-strategies` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=0.71, avoid/not-for boundary=0.00 |

### `public_gold_p58_source_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-source-driven-development`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-addy-agent-context-engineering` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.26, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-oh-my-codebase-search` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-addy-agent-incremental-implementation` | workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-mattpocock-diagnose` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.52, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |

### `public_gold_p59_anthropic_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-openai-docs` | input/precondition, workflow, success criterion | - | input/precondition=0.20, output artifact=1.00, workflow=0.01, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-openai-cli-creator` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.17, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.55, avoid/not-for boundary=1.00 |
| `public-anthropic-mcp-builder` | input/precondition, workflow, success criterion | - | input/precondition=0.26, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-huggingface-hf-cli` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.27, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.57, avoid/not-for boundary=1.00 |

### `public_gold_p60_doc_coauthoring`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-doc-coauthoring`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-report-generator` | input/precondition, workflow, dependency/resource | - | input/precondition=0.49, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-content-writer` | input/precondition, workflow, dependency/resource | - | input/precondition=0.34, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p61_canvas_design`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-canvas-design`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-anthropic-frontend-design` | workflow, success criterion | - | input/precondition=0.94, output artifact=1.00, workflow=0.06, success criterion=0.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |
| `public-anthropic-web-artifacts-builder` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.74, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.55, avoid/not-for boundary=0.00 |
| `public-anthropic-theme-factory` | workflow, success criterion | - | input/precondition=0.92, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-openai-figma-generate-design` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.35, output artifact=0.00, workflow=0.00, success criterion=0.02, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-office-diagram-creator` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.76, output artifact=0.00, workflow=0.00, success criterion=0.01, dependency/resource=0.57, avoid/not-for boundary=1.00 |
| `public-office-infographic` | output artifact, workflow, success criterion | - | input/precondition=0.94, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.90, avoid/not-for boundary=1.00 |

### `public_gold_p62_theme_factory`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-theme-factory`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-figma-create-design-system-rules` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.36, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-brand-guidelines` | workflow, success criterion | - | input/precondition=0.92, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-oh-my-design-system` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=0.00 |
| `public-anthropic-canvas-design` | workflow, success criterion | - | input/precondition=0.92, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-anthropic-frontend-design` | workflow | - | input/precondition=0.92, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.86, avoid/not-for boundary=1.00 |
| `public-mattpocock-prototype` | workflow, success criterion, dependency/resource | - | input/precondition=0.76, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.57, avoid/not-for boundary=1.00 |

### `public_gold_p63_hf_zerogpu`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-zerogpu`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-gradio` | input/precondition, workflow, success criterion | - | input/precondition=0.53, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-local-models` | workflow, success criterion, dependency/resource | - | input/precondition=0.63, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-huggingface-hf-cli` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.52, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.41, output artifact=1.00, workflow=0.02, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `gradio-demo-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-llm-trainer` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.25, output artifact=1.00, workflow=0.01, success criterion=0.01, dependency/resource=0.81, avoid/not-for boundary=1.00 |

### `public_gold_p64_hf_llm_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-llm-trainer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-vision-trainer` | input/precondition, workflow, success criterion | avoid/not-for boundary | input/precondition=0.23, output artifact=1.00, workflow=0.08, success criterion=0.23, dependency/resource=0.88, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-community-evals` | input/precondition, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.29, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-local-models` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.29, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=1.00 |
| `public-swebench-llm-evaluation` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.27, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.54, avoid/not-for boundary=1.00 |

### `public_gold_p65_hf_local_models`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-local-models`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-gradio` | dependency/resource | - | input/precondition=0.69, output artifact=1.00, workflow=1.00, success criterion=1.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-zerogpu` | workflow, success criterion, dependency/resource | - | input/precondition=0.63, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-huggingface-transformers-js` | workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-llm-trainer` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.29, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-community-evals` | workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.77, avoid/not-for boundary=0.00 |

### `public_gold_p66_hf_trackio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-trackio`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-community-evals` | workflow, dependency/resource | avoid/not-for boundary | input/precondition=0.91, output artifact=1.00, workflow=0.01, success criterion=1.00, dependency/resource=0.81, avoid/not-for boundary=0.00 |
| `public-swebench-llm-evaluation` | workflow, dependency/resource | - | input/precondition=0.70, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.50, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-llm-trainer` | input/precondition, workflow, success criterion, dependency/resource | - | input/precondition=0.29, output artifact=1.00, workflow=0.04, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-office-saas-metrics` | workflow, dependency/resource | - | input/precondition=0.72, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.52, avoid/not-for boundary=1.00 |
| `dashboard-ops-monitoring-plan-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.02, avoid/not-for boundary=0.00 |
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `public_gold_p67_hf_papers`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-papers`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-paper-publisher` | workflow, success criterion, dependency/resource | - | input/precondition=0.91, output artifact=1.00, workflow=0.03, success criterion=0.00, dependency/resource=0.81, avoid/not-for boundary=1.00 |
| `public-office-academic-search` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=0.00, workflow=0.00, success criterion=0.01, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-deep-research` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-oh-my-research-paper-writing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.42, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.71, avoid/not-for boundary=0.00 |

### `public_gold_p68_hf_paper_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-paper-publisher`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-oh-my-research-paper-writing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.44, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.77, avoid/not-for boundary=0.00 |
| `public-office-academic-search` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.85, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.71, avoid/not-for boundary=1.00 |
| `public-huggingface-hf-cli` | workflow, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p69_transformers_js`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-transformers-js`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-gradio` | workflow, success criterion, dependency/resource | - | input/precondition=0.68, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-huggingface-huggingface-local-models` | workflow, success criterion, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-anthropic-web-artifacts-builder` | workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=0.00 |
| `public-office-browser-automation` | workflow, success criterion, dependency/resource | - | input/precondition=0.60, output artifact=1.00, workflow=0.00, success criterion=0.00, dependency/resource=0.38, avoid/not-for boundary=1.00 |

### `public_gold_p70_obsidian_json_canvas`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-json-canvas`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-obsidian-obsidian-markdown` | workflow, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-obsidian-obsidian-bases` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-obsidian-obsidian-cli` | workflow, dependency/resource | - | input/precondition=0.82, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-mattpocock-obsidian-vault` | workflow, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |

### `public_gold_p71_obsidian_bases`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-bases`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-obsidian-json-canvas` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.80, avoid/not-for boundary=0.00 |
| `public-obsidian-obsidian-markdown` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.40, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=0.00 |
| `public-oh-my-obsidian-plugin` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.00, workflow=0.01, success criterion=0.03, dependency/resource=0.87, avoid/not-for boundary=0.00 |
| `public-office-notion-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.38, avoid/not-for boundary=0.00 |

### `public_gold_p72_obsidian_cli`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-cli`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-obsidian-json-canvas` | workflow, dependency/resource | - | input/precondition=0.82, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.80, avoid/not-for boundary=1.00 |
| `public-obsidian-obsidian-bases` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=0.00 |

### `public_gold_p73_excel_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-excel-automation`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-sheets-automation` | input/precondition, workflow | - | input/precondition=0.11, output artifact=1.00, workflow=0.04, success criterion=1.00, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.10, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.40, avoid/not-for boundary=1.00 |

### `public_gold_p74_sheets_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-sheets-automation`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.38, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.40, avoid/not-for boundary=1.00 |
| `public-office-data-pipeline` | workflow, dependency/resource | - | input/precondition=0.62, output artifact=1.00, workflow=0.03, success criterion=1.00, dependency/resource=0.41, avoid/not-for boundary=1.00 |

### `public_gold_p75_airtable_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-airtable-automation`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-notion-automation` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.93, avoid/not-for boundary=1.00 |
| `public-office-crm-automation` | dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=1.00, success criterion=1.00, dependency/resource=0.43, avoid/not-for boundary=1.00 |
| `public-office-sheets-automation` | workflow, dependency/resource | - | input/precondition=0.56, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.34, avoid/not-for boundary=1.00 |

### `public_gold_p76_invoice_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-invoice-automation`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-invoice-organizer` | workflow | - | input/precondition=0.95, output artifact=1.00, workflow=0.05, success criterion=1.00, dependency/resource=0.91, avoid/not-for boundary=1.00 |
| `public-office-quickbooks-automation` | workflow, dependency/resource | - | input/precondition=0.58, output artifact=1.00, workflow=0.06, success criterion=1.00, dependency/resource=0.37, avoid/not-for boundary=1.00 |
| `public-office-expense-report` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.90, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.83, avoid/not-for boundary=1.00 |

### `public_gold_p77_lead_routing`

- Family: `public_gold_validation`
- Gold skill: `public-office-lead-routing`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-lead-qualification` | input/precondition, output artifact, success criterion | - | input/precondition=0.13, output artifact=0.00, workflow=1.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-office-lead-research` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.16, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-office-crm-automation` | input/precondition, dependency/resource | - | input/precondition=0.15, output artifact=1.00, workflow=1.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-pipedrive-automation` | input/precondition, workflow, dependency/resource | - | input/precondition=0.11, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |

### `public_gold_p78_saas_metrics`

- Family: `public_gold_validation`
- Gold skill: `public-office-saas-metrics`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-dcf-valuation` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.49, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-office-financial-modeling` | output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.76, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.59, avoid/not-for boundary=1.00 |
| `public-office-stock-analysis` | output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.92, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.87, avoid/not-for boundary=0.00 |
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.38, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.40, avoid/not-for boundary=1.00 |

### `public_gold_p79_stock_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-stock-analysis`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-dcf-valuation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.48, output artifact=0.11, workflow=0.04, success criterion=0.11, dependency/resource=0.83, avoid/not-for boundary=0.00 |
| `public-office-investment-memo` | output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.70, output artifact=0.10, workflow=0.16, success criterion=0.10, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `public-office-crypto-report` | output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.70, output artifact=0.18, workflow=0.19, success criterion=0.18, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `public-office-company-research` | output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.70, output artifact=0.21, workflow=0.18, success criterion=0.15, dependency/resource=0.50, avoid/not-for boundary=0.00 |

### `public_gold_p80_dcf_valuation`

- Family: `public_gold_validation`
- Gold skill: `public-office-dcf-valuation`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-stock-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.48, output artifact=0.11, workflow=0.04, success criterion=0.11, dependency/resource=0.83, avoid/not-for boundary=0.00 |
| `public-office-financial-modeling` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.39, output artifact=0.05, workflow=0.16, success criterion=0.02, dependency/resource=0.56, avoid/not-for boundary=1.00 |
| `public-office-investment-memo` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.37, output artifact=0.10, workflow=0.04, success criterion=0.10, dependency/resource=0.50, avoid/not-for boundary=1.00 |
| `public-swebench-creating-financial-models` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.21, output artifact=0.04, workflow=0.00, success criterion=0.04, dependency/resource=0.54, avoid/not-for boundary=0.00 |

### `public_gold_p81_shopify_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-shopify-automation`
- Status: PASS; needs review

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-woocommerce-automation` | workflow, dependency/resource | - | input/precondition=0.65, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.43, avoid/not-for boundary=1.00 |
| `public-office-stripe-payments` | workflow | - | input/precondition=0.93, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.89, avoid/not-for boundary=1.00 |
| `public-office-amazon-seller` | workflow, dependency/resource | - | input/precondition=0.61, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.38, avoid/not-for boundary=1.00 |
| `public-office-invoice-automation` | workflow, dependency/resource | - | input/precondition=0.58, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.37, avoid/not-for boundary=1.00 |

### `public_gold_p82_zendesk_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-zendesk-automation`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-intercom-automation` | input/precondition, workflow | - | input/precondition=0.19, output artifact=1.00, workflow=0.10, success criterion=1.00, dependency/resource=0.87, avoid/not-for boundary=1.00 |
| `public-office-customer-success` | workflow, dependency/resource | - | input/precondition=0.88, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-email-classifier` | input/precondition, output artifact, workflow, success criterion, dependency/resource | - | input/precondition=0.20, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.75, avoid/not-for boundary=1.00 |
| `public-office-slack-workflows` | workflow, dependency/resource | - | input/precondition=0.64, output artifact=1.00, workflow=0.00, success criterion=1.00, dependency/resource=0.41, avoid/not-for boundary=1.00 |
| `support-ticket-triager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.33, avoid/not-for boundary=0.00 |
| `support-ops-monitoring-plan-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.04, avoid/not-for boundary=0.00 |

