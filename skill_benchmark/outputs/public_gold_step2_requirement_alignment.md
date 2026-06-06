# Procedural Requirement Alignment Report

This is the stricter Step 2 check. Instead of only asking whether skill fields are textually different, it asks whether the prompt-specific requirement aligns better with the gold skill than with each listed alternative.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Method: the script strips long source text where possible, removes local negated spans before scoring positive procedural fit, and still uses the full instruction when matching an alternative's `not_for` boundary. This prevents phrases such as `not a calendar plan` from positively boosting calendar-planning skills while preserving boundary evidence.

## Overall Status

- Step 2 requirement-alignment status: **PASS**
- Prompts where every alternative is beaten by gold or rejected by its boundary: 79/82 (96.3%)
- Gold/alternative pairs passing requirement alignment: 311/315 (98.7%)
- Gold skill ranked first among gold + listed alternatives: 79/82 (96.3%)

Pass rule used here: for each gold/alternative pair, the gold skill must either score above the alternative by the backend-specific margin threshold, or the prompt must strongly activate the alternative's `not_for` boundary. Current thresholds are stored in the JSON report for each pair.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 |
|---|---:|---:|---:|
| public_gold_validation | 82 | 79/82 | 79/82 |

## Weak Requirement Pairs

| Prompt | Gold | Alternative | Margin | Reason |
|---|---|---|---:|---|
| `public_gold_p47_figma_generate_library` | `public-openai-figma-generate-library` | `public-openai-figma-create-design-system-rules` | 0.0179 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `public_gold_p65_hf_local_models` | `public-huggingface-huggingface-local-models` | `public-huggingface-transformers-js` | 0.0343 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | `public-office-woocommerce-automation` | -0.0291 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | `public-office-amazon-seller` | 0.0230 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |

## Prompt Detail

### `public_gold_p01_pdf_extraction`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-extraction`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Using pdfplumber-style extraction, pull the native text, table cells, and document metadata from `/workspace/public_gold/vendor_pack.pdf` into structured JSON with page anchors. The file is not scanned, and I do not need a conversational answer or format conversion.
- Positive-fit instruction after negation cleanup: Using pdfplumber-style extraction, pull the native text, table cells, and document metadata from `/workspace/public_gold/vendor_pack.pdf` into structured JSON with page anchors. The file is .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-pdf-extraction` | 0.6152 | 0.6152 | -0.0430 | extract, text, table, document, metadata, pdf, json, page | - |
| `public-openai-pdf` | 0.4587 | 0.4587 | -0.0430 | extract, text, table, document, metadata, pdf, json, page | - |
| `public-office-pdf-ocr` | 0.4558 | 0.4558 | -0.0430 | extract, text, table, document, metadata, pdf, structur, json | - |
| `public-office-pdf-converter` | 0.4519 | 0.4519 | -0.0430 | extract, text, document, metadata, pdf, json, page, file | - |
| `public-office-chat-with-pdf` | 0.4280 | 0.4280 | -0.0430 | extract, text, document, metadata, pdf, json, page, file | - |

### `public_gold_p02_pdf_ocr`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-ocr`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The uploaded PDF is a scan of signed forms. Run OCR to recover readable text and mark uncertain recognition regions by page; do not treat it as a normal embedded-text PDF or convert it to Word.
- Positive-fit instruction after negation cleanup: The uploaded PDF is a scan of signed forms. Run OCR to recover readable text and mark uncertain recognition regions by page; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-pdf-ocr` | 0.6318 | 0.6318 | 0.0616 | pdf, form, ocr, text, mark, uncertain, recognition, page | - |
| `public-office-pdf-converter` | 0.5440 | 0.5440 | 0.0616 | pdf, ocr, text, page | - |
| `public-openai-pdf` | 0.5101 | 0.5101 | 0.0616 | pdf, ocr, text, page | - |
| `public-office-pdf-extraction` | 0.4797 | 0.4797 | 0.0616 | pdf, ocr, text, page | - |
| `public-office-chat-with-pdf` | 0.4750 | 0.4750 | 0.0616 | upload, pdf, ocr, text, page | - |

### `public_gold_p03_pdf_form_filler`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-form-filler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the reimbursement PDF and the employee data sheet to fill the form fields and report any required blanks still missing. I am not asking for general extraction, conversion, or a reusable document template.
- Positive-fit instruction after negation cleanup: Use the reimbursement PDF and the employee data sheet to fill the form fields and report any required blanks still missing. I am .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-pdf-form-filler` | 0.4305 | 0.4305 | -0.0559 | pdf, data, fill, form, field, requir, miss | - |
| `public-office-template-engine` | 0.3585 | 0.3585 | -0.0559 | data, form, report, requir | - |
| `public-office-pdf-extraction` | 0.3170 | 0.3170 | -0.0559 | pdf, report | - |
| `public-office-pdf-converter` | 0.2280 | 0.2280 | -0.0559 | pdf | - |

### `public_gold_p04_markitdown_conversion`

- Family: `public_gold_validation`
- Gold skill: `public-markitdown`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use a MarkItDown-style pipeline to convert a mixed folder of PDF, DOCX, PPTX, XLSX, image, HTML, CSV, and JSON files into Markdown text suitable for indexing. Preserve lightweight structure and OCR where needed; do not create Office files from Markdown.
- Positive-fit instruction after negation cleanup: Use a MarkItDown-style pipeline to convert a mixed folder of PDF, DOCX, PPTX, XLSX, image, HTML, CSV, and JSON files into Markdown text suitable for indexing. Preserve lightweight structure and OCR where needed; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-markitdown` | 0.7333 | 0.7333 | -0.0016 | markitdown-style, convert, pdf, docx, pptx, xlsx, image, html | - |
| `public-office-batch-convert` | 0.6158 | 0.6158 | -0.0016 | pipeline, convert, folder, pdf, image, html, json, file | - |
| `office-to-markdown-converter` | 0.5881 | 0.5881 | 0.3460 | convert, mix, file, markdown, text, preserve, structure | pdf |
| `public-office-pdf-converter` | 0.5241 | 0.5241 | -0.0016 | convert, folder, pdf, image, json, file, text, preserve | - |
| `public-office-doc-parser` | 0.2777 | 0.2777 | -0.0016 | convert, pdf, json, file, markdown, text, structure, ocr | - |

### `public_gold_p05_pdf_merge_split`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-merge-split`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Combine three policy PDFs into one packet, then split the appendix pages into a separate file. Do not watermark, compress, summarize, or convert the PDFs.
- Positive-fit instruction after negation cleanup: Combine three policy PDFs into one packet, then split the appendix pages into a separate file. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-pdf-merge-split` | 0.5990 | 0.5990 | -0.0311 | combine, pdfs, split, page, separate, file | - |
| `public-office-pdf-converter` | 0.4108 | 0.4108 | -0.0311 | pdfs, page, file | - |
| `public-openai-pdf` | 0.4023 | 0.4023 | -0.0311 | pdfs, page, file | - |
| `public-office-pdf-watermark` | 0.3863 | 0.3863 | -0.0311 | pdfs, page, file | - |
| `public-office-pdf-compress` | 0.3615 | 0.3615 | -0.0311 | page, file | - |

### `public_gold_p06_browser_devtools_testing`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-browser-testing-with-devtools`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use Chrome DevTools MCP on the local checkout to inspect DOM state, console errors, failed network requests, and runtime screenshots. Do not just write a Playwright script from scratch.
- Positive-fit instruction after negation cleanup: Use Chrome DevTools MCP on the local checkout to inspect DOM state, console errors, failed network requests, and runtime screenshots. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-browser-testing-with-devtools` | 0.5826 | 0.5826 | 0.2652 | chrome, devtool, mcp, inspect, dom, state, console, error | inspect, dom, state |
| `public-playwright-interactive` | 0.3316 | 0.3316 | -0.0188 | local, state, console, runtime, screenshot | - |
| `public-openai-playwright` | 0.2978 | 0.2978 | -0.0188 | dom, state, request, runtime, screenshot | - |
| `public-anthropic-webapp-testing` | 0.2885 | 0.2885 | -0.0188 | local, dom, state, request, runtime, screenshot | - |
| `public-office-browser-automation` | 0.2785 | 0.2785 | -0.0188 | dom, state, request, runtime, screenshot | - |

### `public_gold_p07_web_accessibility`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-accessibility`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit the product settings page against WCAG 2.2, focusing on keyboard navigation, labels, focus order, contrast, and screen-reader semantics. Do not broaden this into SEO or performance.
- Positive-fit instruction after negation cleanup: Audit the product settings page against WCAG 2.2, focusing on keyboard navigation, labels, focus order, contrast, and screen-reader semantics. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-web-accessibility` | 0.5139 | 0.5139 | 0.0887 | audit, product, page, against, wcag, keyboard, navigation, label | - |
| `public-addy-web-web-quality-audit` | 0.3305 | 0.3305 | 0.0706 | audit, page | - |
| `public-addy-web-core-web-vitals` | 0.2571 | 0.2571 | 0.0887 | page | - |
| `public-addy-web-best-practices` | 0.1646 | 0.1646 | 0.0887 | audit | - |

### `public_gold_p08_core_web_vitals`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-core-web-vitals`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Investigate only the page's Core Web Vitals: identify the LCP element, INP handler delay, any CLS source, and metric-specific fixes. Do not broaden this into accessibility, SEO, browser automation, or general best-practice review.
- Positive-fit instruction after negation cleanup: Investigate only the page's Core Web Vitals: identify the LCP element, INP handler delay, any CLS source, and metric-specific fixes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-web-core-web-vitals` | 0.5268 | 0.5268 | 0.0442 | core, web, vital, lcp, inp, handler, cls | - |
| `public-addy-web-performance` | 0.4396 | 0.4396 | 0.0442 | only, web, lcp, element, handler, delay, cls | - |
| `public-addy-agent-browser-testing-with-devtools` | 0.3165 | 0.3165 | 0.4156 | identify, element | - |
| `public-addy-web-best-practices` | 0.3105 | 0.3105 | 0.0442 | web, element | - |
| `public-addy-web-accessibility` | 0.2582 | 0.2582 | 0.0442 | only, web, element | - |

### `public_gold_p09_systematic_debugging`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-debugging`
- Gold rank among listed candidates: 1
- Instruction used for scoring: A local feature intermittently returns the wrong result. Use the debugging packet style: freeze the failure definition, build the smallest reproducer, isolate the boundary where behaviour changes, and propose the first evidence-backed fix. Do not review code quality, simplify code, or inspect GitHub CI.
- Positive-fit instruction after negation cleanup: A local feature intermittently returns the wrong result. Use the debugging packet style: freeze the failure definition, build the smallest reproducer, isolate the boundary where behaviour changes, and propose the first evidence-backed fix. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-oh-my-debugging` | 0.2746 | 0.2746 | 0.2033 | local, return, debug, failure, isolate, boundary, change, first | failure, first, review |
| `public-openai-gh-fix-ci` | 0.1695 | 0.1695 | 0.1223 | debug, failure, change, fix | github |
| `public-oh-my-code-review` | 0.0988 | 0.0988 | 0.1330 | local, return, debug, packet, failure, build, isolate, change | debug, failure |
| `public-addy-agent-code-simplification` | -0.0040 | -0.0040 | 0.0721 | feature, result, style, build, change, first | code, result |
| `public-addy-agent-code-review-and-quality` | -0.0376 | -0.0376 | 0.0079 | feature, wrong, style, build, change, first, fix | - |

### `public_gold_p10_analyze_ci`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-analyze-ci`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Given the PR number and failed GitHub Actions job URLs, analyze the failing CI logs and identify the likely cause. Do not design a new workflow template or perform a general debugging session.
- Positive-fit instruction after negation cleanup: Given the PR number and failed GitHub Actions job URLs, analyze the failing CI logs and identify the likely cause. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-swebench-analyze-ci` | 0.5935 | 0.5935 | -0.0118 | fail, github, action, analysi, cause | - |
| `pr-reviewer` | 0.4622 | 0.4622 | 0.4207 | github, identify | fail, job, debug |
| `public-swebench-github-actions-templates` | 0.4061 | 0.4061 | -0.0118 | github, action | - |
| `repo-ops-failure-diagnoser` | 0.3866 | 0.3866 | 0.0742 | fail, action, analysi, logs, identify | identify |
| `public-addy-agent-ci-cd-and-automation` | 0.3061 | 0.3061 | -0.0118 | fail, github, action, analysi | - |
| `public-oh-my-debugging` | 0.2702 | 0.2702 | 0.3192 | fail, job, logs, likely | job, logs, design |

### `public_gold_p11_setup_pre_commit`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-setup-pre-commit`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Add a repo-local Husky pre-commit setup with lint-staged so Prettier, type checking, and tests run before commits. Do not configure GitHub Actions, run a one-off fixer, or block dangerous git commands.
- Positive-fit instruction after negation cleanup: Add a repo-local Husky pre-commit setup with lint-staged so Prettier, type checking, and tests run before commits. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-mattpocock-setup-pre-commit` | 0.6750 | 0.6750 | 0.0760 | add, husky, pre-commit, setup, lint-stag, prettier, type, check | - |
| `git-commit-writer` | 0.3953 | 0.3953 | -0.0044 | type, commit | - |
| `public-swebench-fix` | 0.3768 | 0.3768 | 0.0760 | prettier, type, check, run | - |
| `public-swebench-github-actions-templates` | 0.3182 | 0.3182 | 0.0760 | type, check, test | - |
| `git-safety-guardrail-installer` | 0.3168 | 0.3168 | 0.2673 | setup, check, commit | - |
| `public-mattpocock-git-guardrails-claude-code` | 0.2792 | 0.2792 | 0.0760 | add, type | - |

### `public_gold_p12_git_guardrails`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-git-guardrails-claude-code`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Set up Claude Code git guardrail hooks that prevent dangerous git operations such as force-push, reset --hard, clean, and branch deletion before they execute. I am not asking for formatting hooks, general git workflow advice, or a PR publishing flow.
- Positive-fit instruction after negation cleanup: Set up Claude Code git guardrail hooks that prevent dangerous git operations such as force-push, reset --hard, clean, and branch deletion before they execute. I am .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-mattpocock-git-guardrails-claude-code` | 0.6364 | 0.6364 | 0.0316 | git, set, claude, code, guardrail, hook, prevent, dangerou | - |
| `version-control-helper` | 0.4728 | 0.4728 | -0.0255 | git, code, such, branch | ask |
| `public-openai-yeet` | 0.4051 | 0.4051 | 0.2905 | git, branch, they | code, formatt |
| `public-addy-agent-git-workflow-and-versioning` | 0.4012 | 0.4012 | 0.0316 | git, code, force-push, branch | - |
| `public-swebench-github-actions-templates` | 0.3327 | 0.3327 | 0.0316 | - | - |
| `public-mattpocock-setup-pre-commit` | 0.2961 | 0.2961 | 0.0316 | set, hook | - |

### `public_gold_p13_address_pr_comments`

- Family: `public_gold_validation`
- Gold skill: `public-openai-gh-address-comments`
- Gold rank among listed candidates: 1
- Instruction used for scoring: There are unresolved review comments on the current GitHub PR. Inspect the actionable threads, patch the requested changes, and report what was addressed. Do not create a new PR or debug failing checks.
- Positive-fit instruction after negation cleanup: There are unresolved review comments on the current GitHub PR. Inspect the actionable threads, patch the requested changes, and report what was addressed. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-gh-address-comments` | 0.4302 | 0.4302 | 0.0731 | review, comment, current, github, thread, request, address | - |
| `public-openai-gh-fix-ci` | 0.3515 | 0.3515 | 0.4097 | current, github, inspect, request, change, report | github, report |
| `public-lbussell-triaging-issues` | 0.3203 | 0.3203 | 0.0731 | comment, request, address | - |
| `public-lbussell-creating-pull-requests` | 0.2769 | 0.2769 | 0.0731 | inspect, request, change | - |
| `public-openai-yeet` | 0.2205 | 0.2205 | 0.3283 | review, current, github, request, change | change, new |

### `public_gold_p14_netlify_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-netlify-deploy`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Deploy this static web project to Netlify, using the Netlify CLI and returning the deployment URL with verification. Do not target Vercel, Cloudflare, Render, or Kubernetes.
- Positive-fit instruction after negation cleanup: Deploy this static web project to Netlify, using the Netlify CLI and returning the deployment URL with verification. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-netlify-deploy` | 0.7258 | 0.7258 | 0.0388 | netlify, deploy, web, project, cli, return, deployment, url | - |
| `public-openai-vercel-deploy` | 0.3718 | 0.3718 | 0.0388 | deploy, cli, return, deployment, url, verification | - |
| `public-openai-render-deploy` | 0.3200 | 0.3200 | 0.0388 | deploy, static, web, project, cli, return, deployment, url | - |
| `public-openai-cloudflare-deploy` | 0.3088 | 0.3088 | 0.0388 | deploy, project, deployment, url, verification | - |
| `public-oh-my-vercel-deploy` | 0.2642 | 0.2642 | 0.3344 | deploy, project, cli, return, deployment, url, verification | deploy, cli, deployment, vercel |

### `public_gold_p15_cloudflare_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cloudflare-deploy`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Publish the worker and static assets to Cloudflare Pages/Workers, including the required Wrangler or Cloudflare platform checks. Do not use Netlify, Vercel, Render, or Kubernetes manifests.
- Positive-fit instruction after negation cleanup: Publish the worker and static assets to Cloudflare Pages/Workers, including the required Wrangler or Cloudflare platform checks. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-cloudflare-deploy` | 0.5418 | 0.5418 | 0.0176 | worker, cloudflare, publish, page, platform | - |
| `public-openai-render-deploy` | 0.3105 | 0.3105 | 0.0176 | publish, static, requir, platform, check | - |
| `public-openai-vercel-deploy` | 0.3055 | 0.3055 | 0.0176 | check | - |
| `public-netlify-deploy` | 0.2873 | 0.2873 | 0.0176 | publish, asset, includ, requir, check | - |
| `public-swebench-k8s-manifest-generator` | 0.2826 | 0.2826 | 0.0176 | asset, requir, check | - |

### `public_gold_p16_render_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-render-deploy`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare this service specifically for Render deployment by analyzing the repo, generating a `render.yaml` Blueprint, and giving the Render Dashboard deployment path. Do not deploy to Netlify, Vercel, Cloudflare, or Kubernetes.
- Positive-fit instruction after negation cleanup: Prepare this service specifically for Render deployment by analyzing the repo, generating a `render.yaml` Blueprint, and giving the Render Dashboard deployment path. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-render-deploy` | 0.5809 | 0.5809 | 0.0851 | render, deployment, service, analysi, repo, generat, yaml, blueprint | - |
| `public-openai-vercel-deploy` | 0.3644 | 0.3644 | 0.0851 | deployment | - |
| `public-swebench-k8s-manifest-generator` | 0.3634 | 0.3634 | 0.0851 | deployment, service, generat, yaml, path | - |
| `public-openai-cloudflare-deploy` | 0.3361 | 0.3361 | 0.0851 | deployment, service | - |
| `public-netlify-deploy` | 0.3193 | 0.3193 | 0.0851 | deployment, repo, generat, dashboard | - |

### `public_gold_p17_mcp_builder`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-mcp-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design and implement an MCP server that exposes a third-party issue-tracking API as well-typed tools with authentication and schema-aware tool contracts. Do not just browse a hub of existing MCP tools.
- Positive-fit instruction after negation cleanup: Design and implement an MCP server that exposes a third-party issue-tracking API as well-typed tools with authentication and schema-aware tool contracts. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-anthropic-mcp-builder` | 0.5901 | 0.5901 | 0.0435 | tool, mcp, server, api, authentication, contract | - |
| `webhook-integration-planner` | 0.4866 | 0.4866 | 0.5846 | contract | mcp, design, server, api, exist |
| `public-office-mcp-hub` | 0.4628 | 0.4628 | 0.0435 | tool, mcp, api, authentication, contract | - |
| `public-openai-chatgpt-apps` | 0.3899 | 0.3899 | 0.4367 | tool, design, mcp, server | tool, mcp |
| `public-api-design-principles` | 0.2751 | 0.2751 | 0.0435 | tool, design, api | - |

### `public_gold_p18_chatgpt_apps`

- Family: `public_gold_validation`
- Gold skill: `public-openai-chatgpt-apps`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build a ChatGPT App with an MCP server plus widget UI, following the Apps SDK structure. I need app scaffolding and troubleshooting, not a generic MCP server or CLI.
- Positive-fit instruction after negation cleanup: Build a ChatGPT App with an MCP server plus widget UI, following the Apps SDK structure. I need app scaffolding and troubleshooting, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-chatgpt-apps` | 0.5944 | 0.5944 | 0.4801 | app, build, chatgpt, mcp, server, widget, apps, sdk | mcp, chatgpt, troubleshoot |
| `public-anthropic-mcp-builder` | 0.2672 | 0.2672 | 0.0049 | build, mcp, server, sdk, structure | - |
| `public-openai-openai-docs` | 0.2167 | 0.2167 | 0.0049 | build, mcp, sdk | - |
| `public-openai-cli-creator` | 0.1425 | 0.1425 | 0.0049 | app, build, sdk, scaffold | - |
| `public-office-ai-agent-builder` | 0.1376 | 0.1376 | 0.0049 | build, chatgpt | - |

### `public_gold_p19_cli_creator`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cli-creator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Given an OpenAPI spec, API docs, SDK notes, and a few curl examples, build a composable command-line interface with subcommands, a clear command contract, auth/config handling, and runtime choices. Do not design the API itself, write documentation only, or create an MCP server.
- Positive-fit instruction after negation cleanup: Given an OpenAPI spec, API docs, SDK notes, and a few curl examples, build a composable command-line interface with subcommands, a clear command contract, auth/config handling, and runtime choices. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-cli-creator` | 0.6689 | 0.6689 | -0.0034 | openapi, spec, api, docs, sdk, curl, example, build | - |
| `openapi-contract-reviewer` | 0.5727 | 0.5727 | 0.3585 | openapi, spec, api, example, contract, auth | api, design |
| `public-openai-openai-docs` | 0.4651 | 0.4651 | -0.0034 | api, docs, sdk, example, build, contract, auth | - |
| `public-obsidian-obsidian-cli` | 0.3345 | 0.3345 | -0.0034 | note, command | - |
| `mcp-server-builder` | 0.3156 | 0.3156 | 0.4121 | example, build, auth | api, docs, auth, design |

### `public_gold_p20_hf_datasets`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-datasets`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the Hugging Face Dataset Viewer API to list subsets and splits, paginate sample rows, and inspect schema information for a dataset. Do not download models or train embeddings.
- Positive-fit instruction after negation cleanup: Use the Hugging Face Dataset Viewer API to list subsets and splits, paginate sample rows, and inspect schema information for a dataset. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-datasets` | 0.6343 | 0.6343 | 0.0510 | dataset, hugg, face, viewer, api, subset, split, paginate | - |
| `public-huggingface-huggingface-tool-builder` | 0.3858 | 0.3858 | 0.0510 | hugg, face, api | - |
| `public-huggingface-hf-cli` | 0.3621 | 0.3621 | 0.0510 | dataset, hugg, face | - |
| `public-huggingface-train-sentence-transformers` | 0.3004 | 0.3004 | 0.2605 | hugg, face | - |
| `public-office-data-extractor` | 0.1979 | 0.1979 | 0.0510 | dataset, schema | - |

### `public_gold_p21_hf_gradio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-gradio`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a Gradio demo UI with Python components, event listeners, layout, and launch behavior. This is not about ZeroGPU quota, Dataset Viewer API calls, or Transformers.js in the browser.
- Positive-fit instruction after negation cleanup: Create a Gradio demo UI with Python components, event listeners, layout, and launch behavior. This is .js in the browser.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-gradio` | 0.6274 | 0.6274 | 0.0626 | create, gradio, demo, python, component, event, listener, layout | - |
| `public-huggingface-huggingface-tool-builder` | 0.1777 | 0.1777 | 0.0626 | create, python | - |
| `public-huggingface-transformers-js` | 0.1683 | 0.1683 | 0.0626 | create, browser | - |
| `public-huggingface-huggingface-zerogpu` | 0.1484 | 0.1484 | 0.0626 | gradio, demo, python | - |
| `public-huggingface-datasets` | 0.0330 | 0.0330 | 0.0626 | - | - |

### `public_gold_p22_hf_vision_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-vision-trainer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Fine-tune an object detection model from an image dataset and prepare training/evaluation code for vision labels. Do not choose a local GGUF model or train sentence embeddings.
- Positive-fit instruction after negation cleanup: Fine-tune an object detection model from an image dataset and prepare training/evaluation code for vision labels. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-vision-trainer` | 0.4819 | 0.4819 | 0.0244 | fine-tune, object, detection, model, image, dataset, train, evaluation | - |
| `public-huggingface-huggingface-llm-trainer` | 0.2892 | 0.2892 | 0.1074 | fine-tune, model, dataset, train, code, vision | - |
| `public-huggingface-train-sentence-transformers` | 0.2881 | 0.2881 | 0.1911 | fine-tune, model, image, train | - |
| `public-huggingface-huggingface-local-models` | 0.1962 | 0.1962 | 0.1074 | model | - |
| `public-huggingface-huggingface-community-evals` | 0.1744 | 0.1744 | 0.0959 | model, evaluation | - |

### `public_gold_p23_sentence_transformer_training`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-train-sentence-transformers`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Train or fine-tune a SentenceTransformer bi-encoder for retrieval using paired text data and report evaluation settings. Do not build a browser Transformers.js demo or choose a local inference model.
- Positive-fit instruction after negation cleanup: Train or fine-tune a SentenceTransformer bi-encoder for retrieval using paired text data and report evaluation settings. .js demo or choose a local inference model.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-train-sentence-transformers` | 0.5281 | 0.5281 | 0.2794 | train, fine-tune, sentencetransformer, bi-encoder, retrieval, pair, demo, model | - |
| `public-huggingface-transformers-js` | 0.3228 | 0.3228 | 0.0444 | retrieval, text, inference, model | - |
| `public-huggingface-datasets` | 0.1828 | 0.1828 | 0.0444 | retrieval, text | - |
| `public-huggingface-huggingface-llm-trainer` | 0.1378 | 0.1378 | 0.0444 | train, fine-tune, retrieval, text, setting, demo, local, model | - |
| `public-huggingface-huggingface-local-models` | 0.1202 | 0.1202 | 0.0444 | retrieval, local, model | - |

### `public_gold_p24_hf_cli`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-hf-cli`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the Hugging Face Hub CLI to upload a model repo, manage files, and check repo metadata from the terminal. Do not query the Dataset Viewer API or design a custom tool.
- Positive-fit instruction after negation cleanup: Use the Hugging Face Hub CLI to upload a model repo, manage files, and check repo metadata from the terminal. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-hf-cli` | 0.5257 | 0.5257 | 0.0521 | repo, hugg, face, hub, cli, upload, model, file | - |
| `public-huggingface-huggingface-local-models` | 0.4690 | 0.4690 | 0.0521 | model, file, metadata | - |
| `public-huggingface-huggingface-tool-builder` | 0.4399 | 0.4399 | 0.0521 | hugg, face, model, file, metadata | - |
| `public-huggingface-huggingface-paper-publisher` | 0.4373 | 0.4373 | 0.0521 | hugg, face, hub, model, manage, file, check, metadata | - |
| `public-huggingface-datasets` | 0.2623 | 0.2623 | 0.0521 | hugg, face, file, metadata | - |

### `public_gold_p25_data_pipeline`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-pipeline`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design an ETL workflow that extracts data from two sources, transforms it, loads it into analytics storage, and schedules the pipeline. Do not just analyze a finished dataset or sync two databases.
- Positive-fit instruction after negation cleanup: Design an ETL workflow that extracts data from two sources, transforms it, loads it into analytics storage, and schedules the pipeline. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-data-pipeline` | 0.6364 | 0.6364 | -0.0585 | etl, workflow, extract, data, transform, load, analytic, schedule | - |
| `public-swebench-dbt-transformation-patterns` | 0.4832 | 0.4832 | -0.0585 | workflow, extract, data, load, analytic, pipeline | - |
| `public-office-database-sync` | 0.4221 | 0.4221 | -0.0585 | workflow, data, transform, analytic, storage, schedule, pipeline | - |
| `public-office-data-analysis` | 0.3763 | 0.3763 | -0.0585 | workflow, data, pipeline | - |
| `public-office-data-extractor` | 0.3312 | 0.3312 | -0.0585 | workflow, extract, data, pipeline | - |

### `public_gold_p26_database_sync`

- Family: `public_gold_validation`
- Gold skill: `public-office-database-sync`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Set up a two-way synchronization plan between PostgreSQL and MySQL with table mapping, change handling, and conflict rules. Do not create a general ETL pipeline or dashboard analysis.
- Positive-fit instruction after negation cleanup: Set up a two-way synchronization plan between PostgreSQL and MySQL with table mapping, change handling, and conflict rules. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-database-sync` | 0.3450 | 0.3450 | -0.0099 | synchronization, postgresql, mysql, table, mapp, change, conflict, rule | - |
| `public-office-data-pipeline` | 0.1496 | 0.1496 | -0.0099 | postgresql, mysql, table, mapp, handl, rule | - |
| `public-office-data-analysis` | 0.1466 | 0.1466 | -0.0099 | rule | - |
| `public-office-crm-automation` | 0.1289 | 0.1289 | -0.0099 | synchronization | - |
| `public-office-airtable-automation` | 0.1154 | 0.1154 | -0.0099 | - | - |

### `public_gold_p27_contract_review`

- Family: `public_gold_validation`
- Gold skill: `public-office-contract-review`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this vendor contract for risky clauses, missing protections, obligations, renewal terms, and negotiation recommendations. Do not generate a new template or summarize it generically.
- Positive-fit instruction after negation cleanup: Review this vendor contract for risky clauses, missing protections, obligations, renewal terms, and negotiation recommendations. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-contract-review` | 0.5893 | 0.5893 | 0.5631 | review, contract, clause, miss, protection, term, recommendation | review, contract, term |
| `public-office-contract-template` | 0.4072 | 0.4072 | 0.1307 | contract, clause, term | - |
| `public-office-proposal-writer` | 0.2880 | 0.2880 | 0.1307 | review, term | - |
| `public-security-threat-model` | 0.2054 | 0.2054 | 0.2483 | review, contract, miss, recommendation | - |
| `document-summariser` | 0.1985 | 0.1985 | 0.1226 | contract, obligation | clause |

### `public_gold_p28_suspicious_email`

- Family: `public_gold_validation`
- Gold skill: `public-office-suspicious-email`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Analyze this suspicious email for phishing indicators, spoofed sender details, malicious links, urgency tactics, and recommended safety response. Do not merely classify or draft a reply.
- Positive-fit instruction after negation cleanup: Analyze this suspicious email for phishing indicators, spoofed sender details, malicious links, urgency tactics, and recommended safety response. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-suspicious-email` | 0.6841 | 0.6841 | 0.1413 | analysi, suspiciou, email, phish, indicator, sender, link | - |
| `public-office-email-classifier` | 0.2395 | 0.2395 | 0.1413 | suspiciou, email, phish, indicator, link, urgency, reply | - |
| `public-office-email-drafter` | 0.1957 | 0.1957 | 0.1413 | email, link, reply | - |
| `public-office-security-monitoring` | 0.0724 | 0.0724 | 0.1413 | analysi, email, link, reply | - |
| `public-office-gmail-workflows` | 0.0716 | 0.0716 | 0.1413 | email, sender, link | - |

### `public_gold_p29_ai_slides`

- Family: `public_gold_validation`
- Gold skill: `public-office-ai-slides`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Generate a complete presentation from the topic brief, including outline, slide content, and polished deck structure. Do not only convert existing Markdown or apply a visual theme.
- Positive-fit instruction after negation cleanup: Generate a complete presentation from the topic brief, including outline, slide content, and polished deck structure. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-ai-slides` | 0.6095 | 0.6095 | 0.0799 | generate, complete, presentation, topic, outline, slide, polish, deck | - |
| `public-office-html-slides` | 0.5331 | 0.5331 | 0.0799 | generate, presentation, slide, deck | - |
| `public-office-md-slides` | 0.4978 | 0.4978 | 0.0799 | generate, presentation, outline, slide, content, deck | - |
| `public-office-dev-slides` | 0.4862 | 0.4862 | 0.0799 | generate, presentation, slide, deck | - |
| `public-anthropic-theme-factory` | 0.3952 | 0.3952 | 0.0799 | generate, brief, slide | - |

### `public_gold_p30_figma_implement_design`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-implement-design`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Given a Figma URL with a specific node id, fetch the design context and screenshot, download required assets, and implement the existing frame as production UI code inside the repository with 1:1 visual parity. Do not create or update a Figma screen, generate a new design from a prompt, create a component library, or only fetch context.
- Positive-fit instruction after negation cleanup: Given a Figma URL with a specific node id, fetch the design context and screenshot, download required assets, and implement the existing frame as production UI code inside the repository with 1:1 visual parity. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-figma-implement-design` | 0.5713 | 0.5713 | 0.0123 | figma, url, specific, node, fetch, design, context, requir | - |
| `public-openai-figma-generate-design` | 0.5182 | 0.5182 | 0.0123 | figma, url, node, design, context, asset, exist, frame | - |
| `public-openai-figma-code-connect-components` | 0.5132 | 0.5132 | 0.0123 | figma, url, node, design, context, requir, asset, exist | - |
| `public-openai-figma-generate-library` | 0.4709 | 0.4709 | 0.0123 | figma, node, design, context, asset, exist, frame, code | - |
| `public-openai-figma-use` | 0.4359 | 0.4359 | 0.0123 | figma, specific, node, design, context, asset, implement, exist | - |

### `public_gold_p31_skill_creator`

- Family: `public_gold_validation`
- Gold skill: `public-skill-creator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a new Codex skill for a repeated workflow, including the SKILL.md structure, trigger description, and optional resources/scripts guidance. Do not install an existing skill or migrate settings.
- Positive-fit instruction after negation cleanup: Create a new Codex skill for a repeated workflow, including the SKILL.md structure, trigger description, and optional resources/scripts guidance. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-skill-creator` | 0.6407 | 0.6407 | 0.0157 | skill, create, new, codex, workflow, optional, resource, script | - |
| `public-openai-migrate-to-codex` | 0.5762 | 0.5762 | 0.0157 | skill, codex, workflow, resource, guidance | - |
| `public-oh-my-agentic-skills` | 0.5623 | 0.5623 | 0.2526 | skill, workflow, trigger, resource | - |
| `skill-field-auditor` | 0.4794 | 0.4794 | 0.4428 | skill, workflow, includ, trigger, resource | skill, new, install |
| `public-skill-installer` | 0.4640 | 0.4640 | 0.0157 | skill, codex, workflow, includ, resource | - |

### `public_gold_p32_security_threat_model`

- Family: `public_gold_validation`
- Gold skill: `public-security-threat-model`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Given the repository and architecture notes, identify sensitive data and functions, crossings between users/services, likely misuse scenarios, and concrete mitigations. Do not just list generic best practices or ownership files.
- Positive-fit instruction after negation cleanup: Given the repository and architecture notes, identify sensitive data and functions, crossings between users/services, likely misuse scenarios, and concrete mitigations. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-security-threat-model` | 0.6254 | 0.6254 | 0.4569 | repository, architecture, note, identify, data, user, service, concrete | repository, generic |
| `public-openai-security-best-practices` | 0.4534 | 0.4534 | 0.0182 | identify, user | - |
| `public-openai-security-ownership-map` | 0.3518 | 0.3518 | 0.0182 | sensitive, user | - |
| `public-swebench-security-review` | 0.1923 | 0.1923 | 0.0182 | sensitive, function, user | - |

### `public_gold_p33_openai_docs`

- Family: `public_gold_validation`
- Gold skill: `public-openai-openai-docs`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Look up the current OpenAI API documentation for model parameters, tool-calling behavior, and migration notes, then summarize the relevant official guidance with links. Do not build a ChatGPT App, generate a CLI, or use Anthropic API docs.
- Positive-fit instruction after negation cleanup: Look up the current OpenAI API documentation for model parameters, tool-calling behavior, and migration notes, then summarize the relevant official guidance with links. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-openai-docs` | 0.6721 | 0.6721 | 0.0322 | current, openai, api, documentation, model, migration, official, guidance | - |
| `public-anthropic-claude-api` | 0.5108 | 0.5108 | 0.0322 | openai, api, documentation, model, relevant, official, link | - |
| `public-openai-chatgpt-apps` | 0.4790 | 0.4790 | 0.4121 | openai, model, behavior, relevant, official, link | behavior, chatgpt |
| `public-openai-cli-creator` | 0.4751 | 0.4751 | 0.0322 | api, model, link | - |
| `public-huggingface-huggingface-tool-builder` | 0.3445 | 0.3445 | 0.0322 | api, model, link | - |

### `public_gold_p34_playwright`

- Family: `public_gold_validation`
- Gold skill: `public-openai-playwright`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write and run Playwright browser tests for the local checkout, including navigation, form interactions, assertions, and screenshots. I do not need Chrome DevTools MCP inspection or a manual interactive browser session.
- Positive-fit instruction after negation cleanup: Write and run Playwright browser tests for the local checkout, including navigation, form interactions, assertions, and screenshots. I .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-playwright` | 0.6449 | 0.6449 | 0.0155 | playwright, browser, test, navigation, form, interaction, screenshot | - |
| `public-anthropic-webapp-testing` | 0.5563 | 0.5563 | 0.0155 | write, run, playwright, browser, test, local, interaction, screenshot | - |
| `public-playwright-interactive` | 0.4829 | 0.4829 | 0.0155 | run, playwright, browser, local, interaction, screenshot | - |
| `public-addy-agent-browser-testing-with-devtools` | 0.4688 | 0.4688 | 0.2480 | run, browser, test, interaction, screenshot | - |

### `public_gold_p35_screenshot`

- Family: `public_gold_validation`
- Gold skill: `public-openai-screenshot`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Capture a screenshot of the specified local page and return the image artifact for visual inspection. Do not write a full Playwright test suite or perform console/network debugging.
- Positive-fit instruction after negation cleanup: Capture a screenshot of the specified local page and return the image artifact for visual inspection. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-screenshot` | 0.4228 | 0.4228 | 0.0404 | capture, screenshot, image, visual, inspection | - |
| `public-addy-agent-browser-testing-with-devtools` | 0.3023 | 0.3023 | 0.2017 | capture, screenshot, page, visual, inspection | page |
| `public-anthropic-webapp-testing` | 0.2883 | 0.2883 | 0.0404 | screenshot, local, page, visual | - |
| `public-office-browser-automation` | 0.2711 | 0.2711 | 0.0404 | screenshot, visual | - |
| `public-openai-playwright` | 0.2022 | 0.2022 | 0.0404 | screenshot, visual | - |

### `public_gold_p36_sentry`

- Family: `public_gold_validation`
- Gold skill: `public-openai-sentry`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Use Sentry issue data to inspect the event, stack trace, release, affected users, and likely regression source. Do not build a generic observability dashboard or inspect distributed traces.
- Positive-fit instruction after negation cleanup: Use Sentry issue data to inspect the event, stack trace, release, affected users, and likely regression source. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `distributed-trace-investigator` | 0.4834 | 0.4834 | 0.5132 | data, trace, user | trace, build, dashboard |
| `public-openai-sentry` | 0.4674 | 0.4674 | 0.0760 | sentry, issue, data, inspect, event, user | - |
| `metrics-root-cause-diagnoser` | 0.3965 | 0.3965 | 0.4165 | user, likely, regression | - |
| `public-oh-my-monitoring-observability` | 0.2829 | 0.2829 | 0.4356 | data, stack, trace, release, user, regression | trace, data, release, regression, dashboard |
| `public-swebench-python-observability` | 0.2310 | 0.2310 | 0.0760 | user | - |

### `public_gold_p37_transcribe`

- Family: `public_gold_validation`
- Gold skill: `public-openai-transcribe`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Transcribe the recorded interview audio into timestamped text with speaker turns where possible. Do not synthesize speech, produce a podcast workflow, or summarize meeting actions.
- Positive-fit instruction after negation cleanup: Transcribe the recorded interview audio into timestamped text with speaker turns where possible. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-transcribe` | 0.5487 | 0.5487 | 0.0664 | transcribe, interview, audio, text, speaker | - |
| `public-office-transcription-automation` | 0.4255 | 0.4255 | 0.0664 | audio | - |
| `public-openai-speech` | 0.3976 | 0.3976 | 0.1493 | audio, text | - |
| `public-office-podcast-automation` | 0.3469 | 0.3469 | 0.0664 | record, audio | - |
| `public-office-meeting-notes` | 0.2830 | 0.2830 | 0.0664 | turn | - |

### `public_gold_p38_speech`

- Family: `public_gold_validation`
- Gold skill: `public-openai-speech`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Generate spoken audio from the supplied narration script using a text-to-speech workflow. Do not transcribe an existing recording or automate podcast publishing.
- Positive-fit instruction after negation cleanup: Generate spoken audio from the supplied narration script using a text-to-speech workflow. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-speech` | 0.6415 | 0.6415 | 0.1725 | audio, narration, script, text-to-speech, workflow | - |
| `public-openai-transcribe` | 0.5682 | 0.5682 | 0.0006 | audio, workflow | - |
| `public-office-transcription-automation` | 0.5228 | 0.5228 | 0.0006 | audio, workflow | - |
| `public-office-podcast-automation` | 0.3963 | 0.3963 | 0.0006 | audio, workflow | - |
| `public-anthropic-slack-gif-creator` | 0.1116 | 0.1116 | 0.0006 | generate, workflow | - |

### `public_gold_p39_jupyter_notebook`

- Family: `public_gold_validation`
- Gold skill: `public-openai-jupyter-notebook`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create or update a `.ipynb` Jupyter notebook that loads the CSV, runs Python exploratory analysis, and leaves executable cells with plots and explanations. Do not only write a static report, inspect a Hugging Face dataset, or produce an Excel workbook.
- Positive-fit instruction after negation cleanup: Create or update a `.ipynb` Jupyter notebook that loads the CSV, runs Python exploratory analysis, and leaves executable cells with plots and explanations. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-jupyter-notebook` | 0.5384 | 0.5384 | 0.0265 | create, ipynb, jupyter, notebook, python, cell | - |
| `public-office-report-generator` | 0.3536 | 0.3536 | 0.0265 | create, csv, analysi | - |
| `public-office-data-analysis` | 0.3421 | 0.3421 | 0.0265 | create, csv, exploratory, analysi | - |
| `public-swebench-python-configuration` | 0.1982 | 0.1982 | 0.0265 | python | - |
| `public-huggingface-datasets` | 0.1832 | 0.1832 | 0.0265 | - | - |

### `public_gold_p40_linear`

- Family: `public_gold_validation`
- Gold skill: `public-openai-linear`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create and update Linear issues for the implementation plan, including team/project fields, labels, priorities, and links back to the spec. Do not create GitHub, Jira, or Asana issues.
- Positive-fit instruction after negation cleanup: Create and update Linear issues for the implementation plan, including team/project fields, labels, priorities, and links back to the spec. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-linear` | 0.5034 | 0.5034 | 0.0762 | create, update, linear, issue, team, project, label, link | - |
| `public-lbussell-triaging-issues` | 0.3479 | 0.3479 | 0.0762 | issue, label, link | - |
| `public-office-jira-automation` | 0.3275 | 0.3275 | 0.0762 | issue, plan, project, link | - |
| `public-office-asana-automation` | 0.3012 | 0.3012 | 0.0762 | team, project, link | - |
| `public-lbussell-creating-issues` | 0.2744 | 0.2744 | 0.0762 | create, issue, link | - |

### `public_gold_p41_yeet`

- Family: `public_gold_validation`
- Gold skill: `public-openai-yeet`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Package the current local changes, create an intentional commit, push the branch, and open a draft GitHub pull request. Do not address existing review comments or debug CI logs.
- Positive-fit instruction after negation cleanup: Package the current local changes, create an intentional commit, push the branch, and open a draft GitHub pull request. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-yeet` | 0.4521 | 0.4521 | 0.3281 | current, change, create, commit, push, branch, open, draft | change |
| `public-openai-gh-fix-ci` | 0.4101 | 0.4101 | 0.3550 | current, change, create, branch, open, draft, github, extract | github |
| `public-openai-gh-address-comments` | 0.2717 | 0.2717 | 0.0101 | current, branch, open, github, request | - |

### `public_gold_p42_migrate_to_codex`

- Family: `public_gold_validation`
- Gold skill: `public-openai-migrate-to-codex`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Migrate an existing agent setup into Codex conventions, including local instructions, skills, and environment notes. Do not author a brand-new skill or install an existing one.
- Positive-fit instruction after negation cleanup: Migrate an existing agent setup into Codex conventions, including local instructions, skills, and environment notes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-migrate-to-codex` | 0.6068 | 0.6068 | 0.0477 | migrate, agent, setup, codex, instruction, skill, note | - |
| `public-oh-my-agentic-skills` | 0.5214 | 0.5214 | 0.3206 | exist, agent, skill | agent |
| `public-skill-creator` | 0.4832 | 0.4832 | 0.0477 | exist, setup, codex, convention, skill | - |
| `public-skill-installer` | 0.4823 | 0.4823 | 0.0477 | codex, includ, local, skill | - |
| `public-addy-agent-context-engineering` | 0.4500 | 0.4500 | 0.4291 | exist, agent, setup, convention, instruction, skill | exist, agent, convention |

### `public_gold_p43_notion_knowledge_capture`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-knowledge-capture`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Capture mixed project notes, decisions, links, and loose observations into a durable Notion knowledge base with structured pages, tags, summaries, and backlinks. Do not extract meeting action items or build a research database only.
- Positive-fit instruction after negation cleanup: Capture mixed project notes, decisions, links, and loose observations into a durable Notion knowledge base with structured pages, tags, summaries, and backlinks. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-notion-knowledge-capture` | 0.4817 | 0.4817 | 0.0670 | capture, note, decision, link, notion, knowledge, structur, page | - |
| `public-openai-notion-meeting-intelligence` | 0.3799 | 0.3799 | 0.0670 | capture, project, note, decision, link, notion, page | - |
| `public-office-notion-automation` | 0.3233 | 0.3233 | 0.0670 | link, notion | - |

### `public_gold_p44_notion_meeting_intelligence`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-meeting-intelligence`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn the meeting transcript into Notion-ready decisions, action items, owners, due dates, and follow-up pages linked to the meeting record. Do not create a general knowledge base or research documentation page.
- Positive-fit instruction after negation cleanup: Turn the meeting transcript into Notion-ready decisions, action items, owners, due dates, and follow-up pages linked to the meeting record. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-notion-meeting-intelligence` | 0.4039 | 0.4039 | 0.0035 | meet, decision, action, item, owner, date, follow-up, page | - |
| `public-office-notion-automation` | 0.3504 | 0.3504 | 0.0035 | link, record | - |

### `public_gold_p45_notion_spec_to_implementation`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-spec-to-implementation`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Convert a Notion product spec into an implementation plan with scoped engineering tasks, dependencies, acceptance criteria, and links back to the source spec. Do not just document research or create generic issues.
- Positive-fit instruction after negation cleanup: Convert a Notion product spec into an implementation plan with scoped engineering tasks, dependencies, acceptance criteria, and links back to the source spec. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-spec-driven-development` | 0.4630 | 0.4630 | 0.4471 | spec, implementation, plan, task, dependencie, acceptance, criteria, link | spec, document |
| `public-openai-notion-spec-to-implementation` | 0.4435 | 0.4435 | -0.0381 | spec, notion, implementation, plan, task, dependencie, acceptance, criteria | - |
| `public-openai-notion-knowledge-capture` | 0.3479 | 0.3479 | -0.0381 | spec, notion, task, link | - |
| `public-openai-linear` | 0.3006 | 0.3006 | -0.0381 | task, link | - |
| `public-lbussell-creating-issues` | 0.1448 | 0.1448 | -0.0381 | task, link | - |

### `public_gold_p46_figma_code_connect`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-code-connect-components`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Map existing Figma components to code components using Code Connect so design components are linked to implementation examples. Do not implement a single Figma screen or generate a new component library.
- Positive-fit instruction after negation cleanup: Map existing Figma components to code components using Code Connect so design components are linked to implementation examples. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-figma-code-connect-components` | 0.5641 | 0.5641 | -0.0259 | component, code, map, exist, figma, connect, design, link | - |
| `public-openai-figma-implement-design` | 0.5199 | 0.5199 | -0.0259 | component, code, map, exist, figma, connect, design, link | - |
| `public-openai-figma-generate-design` | 0.5069 | 0.5069 | -0.0259 | component, code, map, exist, figma, connect, design, link | - |
| `public-openai-figma-generate-library` | 0.4783 | 0.4783 | -0.0259 | component, code, exist, figma, design, link | - |
| `public-openai-figma-use` | 0.4042 | 0.4042 | -0.0259 | component, code, exist, figma, design, link, example | - |

### `public_gold_p47_figma_generate_library`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-generate-library`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Generate a reusable component library inside Figma with variants, variables, tokens, and theming foundations from the design-system brief. Do not implement an existing frame in application code, only write design-system rules, or only create Code Connect mappings.
- Positive-fit instruction after negation cleanup: Generate a reusable component library inside Figma with variants, variables, tokens, and theming foundations from the design-system brief. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-figma-generate-library` | 0.5973 | 0.5973 | 0.0485 | generate, component, library, inside, figma, variant, variable, token | - |
| `public-openai-figma-create-design-system-rules` | 0.5794 | 0.5794 | 0.0485 | generate, component, library, figma, variant, token, them, design-system | - |
| `public-openai-figma-implement-design` | 0.5368 | 0.5368 | 0.0485 | generate, reusable, component, library, figma, token, brief | - |
| `public-openai-figma-code-connect-components` | 0.4654 | 0.4654 | 0.0485 | component, library, figma, brief | - |

### `public_gold_p48_figma_design_system_rules`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-create-design-system-rules`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create design-system rules for Figma usage, naming, layout, component variants, and token conventions. Do not generate the actual screen or convert Figma to code.
- Positive-fit instruction after negation cleanup: Create design-system rules for Figma usage, naming, layout, component variants, and token conventions. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-openai-figma-create-design-system-rules` | 0.6619 | 0.6619 | 0.0415 | create, design-system, rule, figma, nam, component, variant, token | - |
| `public-openai-figma-generate-design` | 0.5799 | 0.5799 | 0.0415 | create, figma, nam, layout, component, token | - |
| `public-openai-figma-generate-library` | 0.5410 | 0.5410 | 0.0415 | create, rule, figma, nam, component, variant, token, convention | - |
| `public-anthropic-brand-guidelines` | 0.4868 | 0.4868 | 0.0415 | nam | - |
| `public-anthropic-theme-factory` | 0.4266 | 0.4266 | 0.0415 | nam | - |

### `public_gold_p49_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit the landing page for technical SEO: title, meta description, canonical, structured data, headings, crawlability, and search snippets. Do not focus on accessibility or Core Web Vitals.
- Positive-fit instruction after negation cleanup: Audit the landing page for technical SEO: title, meta description, canonical, structured data, headings, crawlability, and search snippets. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-web-seo` | 0.4536 | 0.4536 | 0.3467 | seo, meta, structur, data, search | - |
| `public-addy-web-core-web-vitals` | 0.3596 | 0.3596 | 0.1100 | page, search | - |
| `public-addy-web-best-practices` | 0.3126 | 0.3126 | 0.1100 | audit | - |
| `public-addy-web-accessibility` | 0.2838 | 0.2838 | 0.1100 | audit, land, page, title, description | - |

### `public_gold_p50_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Profile the web app's overall loading and runtime performance, including bundle size, network waterfalls, render blocking, and expensive client code. Do not limit the review only to LCP, INP, and CLS.
- Positive-fit instruction after negation cleanup: Profile the web app's overall loading and runtime performance, including bundle size, network waterfalls, render blocking, and expensive client code. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-web-performance` | 0.4717 | 0.4717 | 0.0950 | web, load, performance, size, render, code | - |
| `public-addy-agent-performance-optimization` | 0.3959 | 0.3959 | 0.0950 | web, load, performance | - |
| `public-addy-web-web-quality-audit` | 0.3875 | 0.3875 | 0.1404 | web, performance, render, code | - |
| `public-addy-web-core-web-vitals` | 0.3514 | 0.3514 | 0.0950 | web, load, code | - |
| `public-addy-web-best-practices` | 0.2419 | 0.2419 | 0.0950 | web, load, runtime, block, code | - |

### `public_gold_p51_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Run a broad web quality audit that covers accessibility, performance, SEO, best practices, and user-facing quality risks in one prioritized report. Do not narrow it to only WCAG or only Core Web Vitals.
- Positive-fit instruction after negation cleanup: Run a broad web quality audit that covers accessibility, performance, SEO, best practices, and user-facing quality risks in one prioritized report. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-web-web-quality-audit` | 0.6392 | 0.6392 | 0.1275 | quality, run, web, audit, cover, accessibility, performance, seo | - |
| `public-addy-web-core-web-vitals` | 0.3820 | 0.3820 | 0.0409 | web | - |
| `public-addy-web-best-practices` | 0.3297 | 0.3297 | 0.0409 | quality, web, audit, best, practice | - |
| `public-addy-web-accessibility` | 0.3286 | 0.3286 | 0.0409 | web, audit, accessibility, best | - |
| `public-addy-web-seo` | 0.2997 | 0.2997 | 0.2452 | seo | - |

### `public_gold_p52_api_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design stable REST module boundaries and typed request/response contracts between the frontend and backend before implementation. Do not review an existing OpenAPI contract or build a CLI.
- Positive-fit instruction after negation cleanup: Design stable REST module boundaries and typed request/response contracts between the frontend and backend before implementation. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-api-and-interface-design` | 0.5437 | 0.5437 | 0.0244 | design, stable, rest, module, boundarie, typ, request, reply | - |
| `external-api-integration-planner` | 0.4566 | 0.4566 | 0.5514 | request, reply, contract, implementation | contract, design, review, openapi |
| `openapi-contract-reviewer` | 0.4166 | 0.4166 | 0.4683 | request, reply, contract, implementation | design, boundarie, review |
| `public-openai-cli-creator` | 0.2789 | 0.2789 | 0.0244 | stable, request | - |

### `public_gold_p53_context_engineering`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-context-engineering`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare focused agent context for a new coding session by selecting relevant files, rules, project constraints, and task state without flooding the model. Do not search the codebase for one answer or migrate the project to Codex.
- Positive-fit instruction after negation cleanup: Prepare focused agent context for a new coding session by selecting relevant files, rules, project constraints, and task state . .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-context-engineering` | 0.6445 | 0.6445 | 0.6619 | agent, context, new, session, relevant, file, rule, project | focus, agent, context, new, session, relevant, file, rule |
| `public-addy-agent-planning-and-task-breakdown` | 0.5195 | 0.5195 | 0.0122 | agent, context, session, relevant, file, task, state | - |
| `public-addy-agent-source-driven-development` | 0.4336 | 0.4336 | 0.0122 | context, relevant, file, task, state | - |
| `public-oh-my-codebase-search` | 0.4320 | 0.4320 | 0.2383 | context, file, rule, task | search |
| `public-openai-migrate-to-codex` | 0.3747 | 0.3747 | 0.0122 | agent, context, select, file, project, task | - |

### `public_gold_p54_deprecation_migration`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-deprecation-and-migration`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Plan how to sunset the legacy API while migrating callers to the new implementation, including compatibility, rollout, communication, and removal criteria. Do not perform a database migration risk review.
- Positive-fit instruction after negation cleanup: Plan how to sunset the legacy API while migrating callers to the new implementation, including compatibility, rollout, communication, and removal criteria. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-deprecation-and-migration` | 0.4136 | 0.4136 | 0.0354 | plan, sunset, legacy, api, migrat, new, implementation, removal | - |
| `public-addy-agent-api-and-interface-design` | 0.3427 | 0.3427 | 0.0354 | api, new, implementation, removal | - |
| `database-migration-risk-assessor` | 0.3138 | 0.3138 | 0.5181 | plan, new, compatibility, rollout | plan, api, review |
| `public-mattpocock-migrate-to-shoehorn` | 0.2350 | 0.2350 | 0.0354 | - | - |
| `public-addy-agent-incremental-implementation` | 0.2031 | 0.2031 | 0.0354 | implementation | - |

### `public_gold_p55_documentation_adrs`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-documentation-and-adrs`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write an Architecture Decision Record for the caching approach, including context, considered options, decision, consequences, and follow-up documentation. Do not write API docs or a general report.
- Positive-fit instruction after negation cleanup: Write an Architecture Decision Record for the caching approach, including context, considered options, decision, consequences, and follow-up documentation. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-documentation-and-adrs` | 0.4126 | 0.4126 | 0.0359 | decision, write, record, context, consider, documentation | - |
| `public-oh-my-api-documentation` | 0.3798 | 0.3798 | 0.4360 | write, architecture, record, context, consider, documentation | api, docs |
| `code-documentation-writer` | 0.3534 | 0.3534 | 0.0823 | write, context, follow-up, documentation | context |
| `public-openai-notion-research-documentation` | 0.2883 | 0.2883 | 0.0359 | decision, record, context, consider, option, follow-up, documentation | - |
| `public-office-report-generator` | 0.2282 | 0.2282 | 0.0359 | context, consider | - |

### `public_gold_p56_spec_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-spec-driven-development`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn the feature idea into a precise implementation spec with requirements, acceptance criteria, edge cases, and sequencing before coding. Do not start with tests or convert a Notion spec.
- Positive-fit instruction after negation cleanup: Turn the feature idea into a precise implementation spec with requirements, acceptance criteria, edge cases, and sequencing before coding. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-spec-driven-development` | 0.4897 | 0.4897 | 0.4645 | feature, idea, implementation, spec, requirement, acceptance, criteria, cod | spec |
| `public-addy-agent-incremental-implementation` | 0.3618 | 0.3618 | 0.0202 | feature, implementation, requirement | - |
| `public-mattpocock-to-prd` | 0.3316 | 0.3316 | 0.2846 | turn, implementation, requirement | - |
| `public-openai-notion-spec-to-implementation` | 0.3259 | 0.3259 | 0.0202 | turn, feature, implementation, spec, requirement, acceptance, criteria | - |
| `public-addy-agent-test-driven-development` | 0.1394 | 0.1394 | 0.0202 | implementation, requirement | - |

### `public_gold_p57_test_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-test-driven-development`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Implement the bug fix using a red-green-refactor loop: write the failing test first, make it pass, then clean up. Do not only draft a specification or general testing strategy.
- Positive-fit instruction after negation cleanup: Implement the bug fix using a red-green-refactor loop: write the failing test first, make it pass, then clean up. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-test-driven-development` | 0.3167 | 0.3167 | -0.0382 | implement, bug, fix, write, fail, test, pass | - |
| `public-oh-my-testing-strategies` | 0.2529 | 0.2529 | 0.3151 | implement, bug, fix, loop, test, first | test, implement, first |
| `public-addy-agent-spec-driven-development` | 0.1157 | 0.1157 | 0.1701 | implement, test, first | implement, first |

### `public_gold_p58_source_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-source-driven-development`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before changing code, inspect the existing source paths, local conventions, helper APIs, and tests so the implementation follows the codebase. Do not merely prepare generic context or search for one symbol.
- Positive-fit instruction after negation cleanup: Before changing code, inspect the existing source paths, local conventions, helper APIs, and tests so the implementation follows the codebase. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-addy-agent-source-driven-development` | 0.3854 | 0.3854 | -0.0248 | code, implementation, follow | - |
| `public-addy-agent-incremental-implementation` | 0.2894 | 0.2894 | -0.0248 | code, exist, test, implementation | - |
| `public-oh-my-codebase-search` | 0.2857 | 0.2857 | 0.3679 | code, path, test, codebase | search |
| `public-mattpocock-diagnose` | 0.2383 | 0.2383 | 0.0822 | chang, test | - |
| `public-addy-agent-context-engineering` | 0.2072 | 0.2072 | 0.2596 | exist, convention, apis, test, follow, codebase | code, exist, convention, apis, follow, context |

### `public_gold_p59_anthropic_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use Anthropic Claude API guidance to design a Messages API call with tools, model parameters, and error-handling notes. Do not use OpenAI docs, Hugging Face CLI guidance, or build an MCP server.
- Positive-fit instruction after negation cleanup: Use Anthropic Claude API guidance to design a Messages API call with tools, model parameters, and error-handling notes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-anthropic-claude-api` | 0.4563 | 0.4563 | 0.1041 | api, anthropic, claude, call, tool, model | - |
| `public-openai-cli-creator` | 0.3315 | 0.3315 | 0.1041 | api, call, tool, model | - |
| `public-anthropic-mcp-builder` | 0.3222 | 0.3222 | 0.1041 | api, tool, model | - |
| `public-huggingface-hf-cli` | 0.3158 | 0.3158 | 0.1041 | tool, model | - |
| `public-openai-openai-docs` | 0.2561 | 0.2561 | 0.1041 | api, guidance, tool, model | - |

### `public_gold_p60_doc_coauthoring`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-doc-coauthoring`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Co-author the strategy document by preserving the existing argument, improving structure, adding missing sections, and keeping revision notes. Do not only rewrite tone or generate a report from scratch.
- Positive-fit instruction after negation cleanup: Co-author the strategy document by preserving the existing argument, improving structure, adding missing sections, and keeping revision notes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-anthropic-doc-coauthoring` | 0.4217 | 0.4217 | 0.0421 | co-author, document, section | - |
| `public-office-content-writer` | 0.3655 | 0.3655 | 0.0421 | - | - |
| `public-office-report-generator` | 0.3059 | 0.3059 | 0.0421 | - | - |

### `public_gold_p61_canvas_design`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-canvas-design`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a canvas-based visual composition for an explainer, with layout, typography, and interactive visual elements. Do not build a frontend web app or Figma design file.
- Positive-fit instruction after negation cleanup: Create a canvas-based visual composition for an explainer, with layout, typography, and interactive visual elements. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-anthropic-canvas-design` | 0.5324 | 0.5324 | 0.0755 | visual, create, composition, layout, element | - |
| `public-office-diagram-creator` | 0.4704 | 0.4704 | 0.0755 | create | - |
| `public-office-infographic` | 0.3561 | 0.3561 | 0.0755 | visual, layout, typography, element | - |
| `public-anthropic-frontend-design` | 0.2964 | 0.2964 | 0.0755 | visual, create, layout, typography | - |
| `public-anthropic-theme-factory` | 0.2340 | 0.2340 | 0.0755 | visual | - |
| `public-anthropic-web-artifacts-builder` | 0.2183 | 0.2183 | 0.3153 | - | - |
| `public-openai-figma-generate-design` | 0.2164 | 0.2164 | 0.0755 | visual, create, layout | - |

### `public_gold_p62_theme_factory`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-theme-factory`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Generate a reusable visual theme with palette, type scale, spacing, and component styling tokens for a product prototype. Do not write full brand guidelines or implement the frontend.
- Positive-fit instruction after negation cleanup: Generate a reusable visual theme with palette, type scale, spacing, and component styling tokens for a product prototype. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-anthropic-theme-factory` | 0.4818 | 0.4818 | 0.0693 | generate, visual, theme, type, styl | - |
| `public-oh-my-design-system` | 0.4002 | 0.4002 | 0.2867 | reusable, visual, palette, type, scale, spac, component, token | reusable, implement |
| `public-office-brand-guidelines` | 0.3675 | 0.3675 | 0.0693 | generate, visual, palette, type | - |
| `public-anthropic-canvas-design` | 0.3439 | 0.3439 | 0.0693 | visual, type, product | - |
| `public-anthropic-frontend-design` | 0.3193 | 0.3193 | 0.0693 | generate, visual, type, component, styl | - |
| `public-mattpocock-prototype` | 0.2987 | 0.2987 | 0.0693 | type, prototype | - |
| `public-openai-figma-create-design-system-rules` | 0.2649 | 0.2649 | 0.0693 | generate, visual, theme, type, scale, spac, component, styl | - |

### `public_gold_p63_hf_zerogpu`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-zerogpu`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare the Hugging Face Space to run on ZeroGPU, including decorators, GPU-duration constraints, queue behavior, and deployment caveats. Do not just build a Gradio UI or choose a local model.
- Positive-fit instruction after negation cleanup: Prepare the Hugging Face Space to run on ZeroGPU, including decorators, GPU-duration constraints, queue behavior, and deployment caveats. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-zerogpu` | 0.7167 | 0.7167 | 0.0914 | hugg, face, space, run, zerogpu, decorator, constraint | - |
| `public-huggingface-huggingface-llm-trainer` | 0.4625 | 0.4625 | 0.0914 | hugg, face, run, deployment | - |
| `public-huggingface-hf-cli` | 0.4227 | 0.4227 | 0.0914 | hugg, face, space | - |
| `public-huggingface-huggingface-local-models` | 0.3960 | 0.3960 | 0.0914 | run | - |
| `public-huggingface-huggingface-tool-builder` | 0.3067 | 0.3067 | 0.0914 | hugg, face | - |
| `public-huggingface-huggingface-gradio` | 0.2108 | 0.2108 | 0.0914 | - | - |
| `gradio-demo-builder` | 0.2105 | 0.2105 | 0.1768 | constraint, behavior | local, model |

### `public_gold_p64_hf_llm_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-llm-trainer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Fine-tune a causal language model with Hugging Face training code, tokenizer setup, instruction dataset formatting, evaluation, and push-to-hub notes. Do not train a vision model, train a SentenceTransformer embedding model, or only evaluate an LLM.
- Positive-fit instruction after negation cleanup: Fine-tune a causal language model with Hugging Face training code, tokenizer setup, instruction dataset formatting, evaluation, and push-to-hub notes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-llm-trainer` | 0.4721 | 0.4721 | 0.1634 | fine-tune, language, model, hugg, face, train, code, setup | - |
| `public-huggingface-huggingface-vision-trainer` | 0.4225 | 0.4225 | 0.1074 | fine-tune, model, hugg, face, train, code, dataset, formatt | - |
| `public-huggingface-huggingface-local-models` | 0.3906 | 0.3906 | 0.1634 | model | - |
| `public-huggingface-huggingface-community-evals` | 0.3508 | 0.3508 | 0.1862 | model, hugg, face, evaluation | - |
| `public-swebench-llm-evaluation` | 0.2171 | 0.2171 | 0.1634 | evaluation | - |

### `public_gold_p65_hf_local_models`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-local-models`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Choose and run a local Hugging Face model for laptop inference with GGUF or llama.cpp-style runtime choices, quantization, memory limits, and local serving options. Do not train a model, deploy a Space, or build browser-side Transformers.js inference.
- Positive-fit instruction after negation cleanup: Choose and run a local Hugging Face model for laptop inference with GGUF or llama.cpp-style runtime choices, quantization, memory limits, and local serving options. .js inference.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-local-models` | 0.5136 | 0.5136 | 0.1423 | local, run, model, gguf, llama, serv | - |
| `public-huggingface-transformers-js` | 0.4793 | 0.4793 | 0.1423 | inference, run, hugg, face, model, runtime, memory | - |
| `public-huggingface-huggingface-llm-trainer` | 0.4619 | 0.4619 | 0.1423 | local, run, hugg, face, model, gguf, memory | - |
| `public-huggingface-huggingface-community-evals` | 0.4037 | 0.4037 | 0.1729 | local, run, hugg, face, model | - |
| `public-huggingface-huggingface-zerogpu` | 0.3104 | 0.3104 | 0.1423 | run, hugg, face, runtime, memory | - |
| `public-huggingface-huggingface-gradio` | 0.2392 | 0.2392 | 0.1423 | - | - |

### `public_gold_p66_hf_trackio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-trackio`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Instrument the training run with Trackio experiment tracking, logging metrics, configs, artifacts, and run comparison. Do not design a community evaluation or SaaS metrics dashboard.
- Positive-fit instruction after negation cleanup: Instrument the training run with Trackio experiment tracking, logging metrics, configs, artifacts, and run comparison. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-trackio` | 0.6989 | 0.6989 | 0.1468 | run, train, trackio, experiment, track, logg, metric, config | - |
| `dashboard-ops-monitoring-plan-builder` | 0.4683 | 0.4683 | 0.0546 | metric, artifact | - |
| `public-huggingface-huggingface-llm-trainer` | 0.4037 | 0.4037 | 0.1468 | run, train, trackio, config, artifact | - |
| `public-swebench-llm-evaluation` | 0.3948 | 0.3948 | 0.1468 | metric, artifact | - |
| `metrics-overview` | 0.3932 | 0.3932 | 0.3213 | metric | - |
| `public-office-saas-metrics` | 0.3097 | 0.3097 | 0.1468 | metric, artifact | - |
| `public-huggingface-huggingface-community-evals` | 0.2500 | 0.2500 | 0.3386 | run, artifact | - |

### `public_gold_p67_hf_papers`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-papers`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Find relevant Hugging Face paper entries for this model topic, compare abstracts and linked artifacts, and summarize which papers are most relevant. Do not publish a paper page or write a manuscript.
- Positive-fit instruction after negation cleanup: Find relevant Hugging Face paper entries for this model topic, compare abstracts and linked artifacts, and summarize which papers are most relevant. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-papers` | 0.5943 | 0.5943 | 0.0692 | paper, hugg, face, model, link, artifact, summary | - |
| `public-huggingface-huggingface-paper-publisher` | 0.5327 | 0.5327 | 0.0692 | paper, hugg, face, model, link, artifact | - |
| `public-office-academic-search` | 0.3439 | 0.3439 | 0.0692 | paper, find, topic, compare, abstract, link, artifact, summary | - |
| `public-office-deep-research` | 0.3280 | 0.3280 | 0.0692 | topic, link, artifact, summary | - |
| `public-oh-my-research-paper-writing` | 0.2982 | 0.2982 | 0.3137 | paper, abstract, link, artifact, most | manuscript |

### `public_gold_p68_hf_paper_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-paper-publisher`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare and publish the model paper artifacts to Hugging Face, including metadata, model links, and paper page details. Do not merely search existing papers or write the academic manuscript.
- Positive-fit instruction after negation cleanup: Prepare and publish the model paper artifacts to Hugging Face, including metadata, model links, and paper page details. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-paper-publisher` | 0.6801 | 0.6801 | 0.1468 | model, paper, publish, artifact, hugg, face, metadata, link | - |
| `public-huggingface-hf-cli` | 0.4935 | 0.4935 | 0.1468 | model, paper, artifact, hugg, face, metadata, link | - |
| `public-oh-my-research-paper-writing` | 0.3820 | 0.3820 | 0.3274 | paper, artifact, metadata, link | academic, manuscript |
| `public-office-academic-search` | 0.2237 | 0.2237 | 0.1468 | paper, artifact, metadata, link | - |

### `public_gold_p69_transformers_js`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-transformers-js`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build a browser-side ML demo using Transformers.js so inference runs in the client, with model loading and UI wiring. Do not build a Python Gradio demo or local server inference script.
- Positive-fit instruction after negation cleanup: Build a browser-side ML demo using Transformers.js so inference runs in the client, with model loading and UI wiring. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-transformers-js` | 0.5642 | 0.5642 | 0.0639 | transformer, inference, model | - |
| `public-office-browser-automation` | 0.3158 | 0.3158 | 0.0639 | - | - |
| `public-anthropic-web-artifacts-builder` | 0.2347 | 0.2347 | 0.2462 | - | - |
| `public-huggingface-huggingface-local-models` | 0.1649 | 0.1649 | 0.0639 | model | - |
| `public-huggingface-huggingface-gradio` | 0.1479 | 0.1479 | 0.0639 | build, demo | - |

### `public_gold_p70_obsidian_json_canvas`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-json-canvas`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create an Obsidian JSON Canvas map with nodes and edges representing the research argument. Do not just write Markdown notes, a Bases view, or CLI commands.
- Positive-fit instruction after negation cleanup: Create an Obsidian JSON Canvas map with nodes and edges representing the research argument. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-obsidian-json-canvas` | 0.5604 | 0.5604 | 0.0591 | create, obsidian, json, canva, node, edge | - |
| `public-obsidian-obsidian-cli` | 0.3367 | 0.3367 | 0.0591 | create, obsidian, json | - |
| `public-obsidian-obsidian-markdown` | 0.3346 | 0.3346 | 0.0591 | create, obsidian, json | - |
| `public-mattpocock-obsidian-vault` | 0.3144 | 0.3144 | 0.0591 | create, obsidian, json, research | - |
| `public-obsidian-obsidian-bases` | 0.3007 | 0.3007 | 0.0680 | create, obsidian, json, map | create |

### `public_gold_p71_obsidian_bases`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-bases`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build an Obsidian Bases view for the vault that filters notes by metadata fields, status, and tags. Do not create a JSON Canvas graph or run generic CLI commands.
- Positive-fit instruction after negation cleanup: Build an Obsidian Bases view for the vault that filters notes by metadata fields, status, and tags. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-obsidian-obsidian-bases` | 0.5882 | 0.5882 | 0.1040 | obsidian, base, view, vault, filter, note, metadata, statu | field, create |
| `public-obsidian-obsidian-markdown` | 0.5309 | 0.5309 | 0.0543 | obsidian, note, metadata, tags | - |
| `public-obsidian-json-canvas` | 0.3712 | 0.3712 | 0.0543 | obsidian, metadata | - |
| `public-oh-my-obsidian-plugin` | 0.2469 | 0.2469 | 0.0543 | build, obsidian, view, vault, note, metadata, field | - |
| `public-office-notion-automation` | 0.2311 | 0.2311 | 0.0543 | metadata, field, statu | - |

### `public_gold_p72_obsidian_cli`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-cli`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the Obsidian CLI to create, update, and query vault notes from the terminal with command-line operations. Do not hand-write a Markdown note, maintain a general vault workflow, or create a canvas file.
- Positive-fit instruction after negation cleanup: Use the Obsidian CLI to create, update, and query vault notes from the terminal with command-line operations. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-obsidian-obsidian-cli` | 0.5791 | 0.5791 | 0.0258 | obsidian, cli, create, vault, note, operation | - |
| `public-obsidian-obsidian-bases` | 0.4308 | 0.4308 | 0.0747 | obsidian, create, vault, note | create, file |
| `public-obsidian-json-canvas` | 0.2976 | 0.2976 | 0.0258 | obsidian, create | - |

### `public_gold_p73_excel_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-excel-automation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Automate an Excel workbook by adding formulas, formatting, pivot-style summaries, and saved workbook output. Do not use Google Sheets or only analyze the data.
- Positive-fit instruction after negation cleanup: Automate an Excel workbook by adding formulas, formatting, pivot-style summaries, and saved workbook output. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-excel-automation` | 0.6352 | 0.6352 | -0.0664 | workbook, automate, excel, add, formula, summary | - |
| `public-office-sheets-automation` | 0.4705 | 0.4705 | -0.0664 | workbook, formula | - |
| `public-office-data-analysis` | 0.3762 | 0.3762 | -0.0664 | excel, formula | - |

### `public_gold_p74_sheets_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-sheets-automation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Automate a Google Sheets workbook with formulas, tabs, formatting, and update steps using the online Sheets workflow. Do not produce a local Excel or XLSX file.
- Positive-fit instruction after negation cleanup: Automate a Google Sheets workbook with formulas, tabs, formatting, and update steps using the online Sheets workflow. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-sheets-automation` | 0.5571 | 0.5571 | -0.0609 | sheet, google, workbook, formula, workflow | - |
| `public-office-data-analysis` | 0.3826 | 0.3826 | -0.0609 | formula, workflow | - |
| `public-office-data-pipeline` | 0.3023 | 0.3023 | -0.0609 | sheet, google, update, workflow | - |

### `public_gold_p75_airtable_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-airtable-automation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create an Airtable automation that routes new form submissions, updates linked records, and sends follow-up notifications. Do not build a Notion or CRM workflow.
- Positive-fit instruction after negation cleanup: Create an Airtable automation that routes new form submissions, updates linked records, and sends follow-up notifications. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-airtable-automation` | 0.3484 | 0.3484 | 0.0146 | airtable, automation, link, record | - |
| `public-office-notion-automation` | 0.1969 | 0.1969 | 0.0146 | automation, new, form, link, record | - |
| `public-office-crm-automation` | 0.1878 | 0.1878 | 0.0146 | automation, link | - |
| `public-office-sheets-automation` | 0.1869 | 0.1869 | 0.0146 | automation, link | - |

### `public_gold_p76_invoice_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-invoice-automation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Automate the accounts-payable invoice workflow from incoming invoice files through extraction, validation, approval routing, and accounting-system update. Do not merely generate a single outbound invoice template.
- Positive-fit instruction after negation cleanup: Automate the accounts-payable invoice workflow from incoming invoice files through extraction, validation, approval routing, and accounting-system update. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-invoice-automation` | 0.6369 | 0.6369 | 0.0994 | invoice, automate, workflow, file | - |
| `public-office-invoice-organizer` | 0.5608 | 0.5608 | 0.0994 | invoice, workflow, file, extract | - |
| `public-office-quickbooks-automation` | 0.4990 | 0.4990 | 0.0994 | invoice, automate, workflow, file | - |
| `public-office-expense-report` | 0.3742 | 0.3742 | 0.0994 | workflow, file | - |

### `public_gold_p77_lead_routing`

- Family: `public_gold_validation`
- Gold skill: `public-office-lead-routing`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Route inbound leads to the right sales owner based on region, company size, product interest, and priority rules. Do not only research or qualify the lead.
- Positive-fit instruction after negation cleanup: Route inbound leads to the right sales owner based on region, company size, product interest, and priority rules. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-lead-routing` | 0.3559 | 0.3559 | 0.0706 | lead, owner, bas, priority | - |
| `public-office-lead-research` | 0.2981 | 0.2981 | 0.0706 | lead, sale, bas, company, product | - |
| `public-office-pipedrive-automation` | 0.2538 | 0.2538 | 0.0706 | inbound, lead, sale, owner, company, product, interest | - |
| `public-office-lead-qualification` | 0.2378 | 0.2378 | 0.0706 | lead, bas, company, size | - |
| `public-office-crm-automation` | 0.1618 | 0.1618 | 0.0706 | lead | - |

### `public_gold_p78_saas_metrics`

- Family: `public_gold_validation`
- Gold skill: `public-office-saas-metrics`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Calculate SaaS metrics such as MRR, ARR, churn, expansion, retention cohorts, CAC payback, and LTV from the subscription export. Do not build a DCF valuation or stock analysis report.
- Positive-fit instruction after negation cleanup: Calculate SaaS metrics such as MRR, ARR, churn, expansion, retention cohorts, CAC payback, and LTV from the subscription export. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-saas-metrics` | 0.5772 | 0.5772 | 0.0555 | saas, metric, mrr, arr, churn, cohort, cac, ltv | - |
| `public-office-dcf-valuation` | 0.3811 | 0.3811 | 0.0555 | calculate, metric | - |
| `public-office-financial-modeling` | 0.3508 | 0.3508 | 0.0555 | metric | - |
| `public-office-stock-analysis` | 0.3018 | 0.3018 | 0.3649 | metric | valuation, analysi |
| `public-office-data-analysis` | 0.1830 | 0.1830 | 0.0555 | export | - |

### `public_gold_p79_stock_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-stock-analysis`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Analyze a listed company's stock using recent financials, valuation multiples, catalysts, risks, and investment view. Do not write a crypto report or only build a DCF spreadsheet.
- Positive-fit instruction after negation cleanup: Analyze a listed company's stock using recent financials, valuation multiples, catalysts, risks, and investment view. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-stock-analysis` | 0.5275 | 0.5275 | 0.5194 | analysi, stock, financial, valuation, risk, investment | analysi, financial, valuation, only |
| `public-office-investment-memo` | 0.4730 | 0.4730 | 0.0110 | analysi, financial, valuation, risk, investment | - |
| `public-office-company-research` | 0.4661 | 0.4661 | 0.0110 | analysi, investment | - |
| `public-office-crypto-report` | 0.3489 | 0.3489 | 0.0110 | analysi, recent | - |
| `public-office-dcf-valuation` | 0.3205 | 0.3205 | 0.0110 | stock, financial, valuation, multiple | - |

### `public_gold_p80_dcf_valuation`

- Family: `public_gold_validation`
- Gold skill: `public-office-dcf-valuation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build a DCF valuation with revenue forecasts, margin assumptions, WACC, terminal value, sensitivity table, and implied share value. Do not only write a stock memo.
- Positive-fit instruction after negation cleanup: Build a DCF valuation with revenue forecasts, margin assumptions, WACC, terminal value, sensitivity table, and implied share value. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-dcf-valuation` | 0.6961 | 0.6961 | 0.0201 | value, build, dcf, valuation, revenue, margin, assumption, wacc | - |
| `public-swebench-creating-financial-models` | 0.5293 | 0.5293 | 0.5644 | value, dcf, valuation, revenue, forecast, margin, assumption, terminal | build, dcf, valuation, assumption, wacc, sensitivity, only |
| `public-office-investment-memo` | 0.4401 | 0.4401 | 0.0201 | valuation | - |
| `public-office-financial-modeling` | 0.4385 | 0.4385 | 0.0201 | build, revenue, forecast, margin | - |
| `public-office-stock-analysis` | 0.3403 | 0.3403 | 0.4430 | valuation, assumption | valuation, assumption, only |

### `public_gold_p81_shopify_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-shopify-automation`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Automate Shopify Admin product and order workflows for a Shopify store, including product updates, fulfillment status changes, and customer notifications through Shopify-specific operations. Do not build WooCommerce, Amazon seller, or Stripe payment automation.
- Positive-fit instruction after negation cleanup: Automate Shopify Admin product and order workflows for a Shopify store, including product updates, fulfillment status changes, and customer notifications through Shopify-specific operations. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-woocommerce-automation` | 0.4977 | 0.4977 | 0.0106 | automate, order, workflow, includ, customer, operation | - |
| `public-office-shopify-automation` | 0.4686 | 0.4686 | 0.0106 | shopify, order, workflow, customer | - |
| `public-office-amazon-seller` | 0.4456 | 0.4456 | 0.0106 | product, automate, order, workflow, includ, fulfillment, operation | - |
| `public-office-invoice-automation` | 0.2393 | 0.2393 | 0.0106 | product, automate, workflow, customer | - |
| `public-office-stripe-payments` | 0.2029 | 0.2029 | 0.0106 | automate, workflow, customer | - |

### `public_gold_p82_zendesk_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-zendesk-automation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Automate Zendesk ticket triage, tags, macros, assignments, and escalation rules for support requests. Do not build Intercom, Slack, or email classification automation.
- Positive-fit instruction after negation cleanup: Automate Zendesk ticket triage, tags, macros, assignments, and escalation rules for support requests. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-zendesk-automation` | 0.6760 | 0.6760 | 0.1404 | automate, zendesk, ticket, support, request | - |
| `support-ticket-triager` | 0.5432 | 0.5432 | 0.1550 | ticket, triage, support, request | - |
| `support-ops-monitoring-plan-builder` | 0.4496 | 0.4496 | 0.1550 | ticket, escalation, rule, support | - |
| `public-office-intercom-automation` | 0.3531 | 0.3531 | 0.1404 | automate, triage, support, request | - |
| `public-office-slack-workflows` | 0.3124 | 0.3124 | 0.1404 | request | - |
| `public-office-customer-success` | 0.3083 | 0.3083 | 0.1404 | request | - |
| `public-office-email-classifier` | 0.2653 | 0.2653 | 0.1404 | request | - |

