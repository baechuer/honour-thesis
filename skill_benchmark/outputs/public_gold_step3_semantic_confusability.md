# Semantic Confusability Report

This report implements Step 3 of the benchmark rubric: listed alternatives should be semantically plausible neighbours, not random unrelated distractors.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.

## Overall Status

- Step 3 status: **PASS**
- Prompts with at least two plausible listed alternatives: 78/82 (95.1%)
- Gold/alternative pairs marked plausible: 220/315 (69.8%)
- Gold skill ranked top-1 among all skills by this backend: 37/82 (45.1%)

Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, or whose skill card is similar to the gold skill card.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |
|---|---:|---:|---:|
| public_gold_validation | 82 | 78/82 | 37/82 |

## Weak Semantic-Confusability Prompts

| Prompt | Gold | Plausible alternatives | Gold all-skill rank |
|---|---|---:|---:|
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | 0 | 1 |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | 1 | 1 |
| `public_gold_p60_doc_coauthoring` | `public-anthropic-doc-coauthoring` | 1 | 3 |
| `public_gold_p82_zendesk_automation` | `public-office-zendesk-automation` | 1 | 1 |

## Prompt Detail

### `public_gold_p01_pdf_extraction`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-extraction`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-chat-with-pdf` | 0.6611 | 0.4052 | 0.6329 | yes | extract, pdf, answer | extract |
| `public-office-pdf-ocr` | 0.6611 | 0.4545 | 0.7114 | yes | extract, text, scann | extract, text, pdfs |
| `public-office-pdf-converter` | 0.6611 | 0.4849 | 0.7258 | yes | pdf, file, format, convert | - |
| `public-openai-pdf` | 0.6611 | 0.4408 | 0.6048 | yes | extract, pdf, page, file | extract, pdfplumber |

Top similarity neighbours: `public-office-pdf-extraction` (0.661), `pdf-layout-table-extractor` (0.585), `implicit-pdf-table-reconstructor` (0.522), `document-field-extractor` (0.501), `pdf-ocr-extractor` (0.500)

### `public_gold_p02_pdf_ocr`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-ocr`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-pdf-extraction` | 0.6261 | 0.4848 | 0.7114 | yes | text | extract, text, pdfs |
| `public-office-chat-with-pdf` | 0.6261 | 0.4575 | 0.5920 | yes | pdf | extract |
| `public-office-pdf-converter` | 0.6261 | 0.5468 | 0.7035 | yes | pdf, convert, word | - |
| `public-openai-pdf` | 0.6261 | 0.4188 | 0.5512 | yes | pdf, page | extract |

Top similarity neighbours: `pdf-ocr-cleaner` (0.721), `pdf-ocr-extractor` (0.675), `public-office-pdf-ocr` (0.626), `public-pdf` (0.549), `public-office-pdf-converter` (0.547)

### `public_gold_p03_pdf_form_filler`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-pdf-extraction` | 0.4936 | 0.3492 | 0.6703 | yes | extract | extract |
| `public-office-pdf-converter` | 0.4936 | 0.2822 | 0.6727 | yes | pdf, convert | pdf |
| `public-office-template-engine` | 0.4936 | 0.4067 | 0.4651 | no | data, document, template | data |

Top similarity neighbours: `pdf-form-filler` (0.539), `public-office-pdf-form-filler` (0.494), `public-office-form-builder` (0.435), `public-office-expense-tracker` (0.434), `public-office-financial-modeling` (0.428)

### `public_gold_p04_markitdown_conversion`

- Family: `public_gold_validation`
- Gold skill: `public-markitdown`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.6850 | 0.6605 | 0.7194 | yes | file, markdown, convert, mix | convert, file, document, markdown |
| `public-office-pdf-converter` | 0.6850 | 0.4717 | 0.5891 | yes | file, convert, pdf, image | convert, file, pdf, image |
| `public-office-batch-convert` | 0.6850 | 0.4333 | 0.4842 | no | pipeline, convert | convert, document |
| `public-office-doc-parser` | 0.6850 | 0.3333 | 0.5310 | yes | - | - |

Top similarity neighbours: `public-markitdown` (0.685), `office-to-markdown-converter` (0.660), `document-converter` (0.506), `pdf-to-docx-converter` (0.503), `layout-preserving-converter` (0.482)

### `public_gold_p05_pdf_merge_split`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-merge-split`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-pdf-converter` | 0.4820 | 0.3483 | 0.6813 | yes | file, convert | file |
| `public-office-pdf-watermark` | 0.4820 | 0.4388 | 0.5073 | yes | pdfs, page, watermark | pdfs |
| `public-office-pdf-compress` | 0.4820 | 0.2751 | 0.5893 | yes | file | file |
| `public-openai-pdf` | 0.4820 | 0.3253 | 0.4788 | no | page, file | file |

Top similarity neighbours: `public-office-pdf-merge-split` (0.482), `public-office-pdf-watermark` (0.439), `pdf-layout-table-extractor` (0.417), `public-office-invoice-template` (0.401), `pdf-ocr-extractor` (0.391)

### `public_gold_p06_browser_devtools_testing`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-browser-testing-with-devtools`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-playwright` | 0.6135 | 0.4549 | 0.5324 | yes | screenshot, script | real, browser, via, debug, data, require |
| `public-playwright-interactive` | 0.6135 | 0.5028 | 0.5574 | yes | - | browser, debug |
| `public-office-browser-automation` | 0.6135 | 0.4769 | 0.5800 | yes | playwright | browser, test |
| `public-anthropic-webapp-testing` | 0.6135 | 0.5150 | 0.6494 | yes | local, screenshot, playwright | browser, test, debug, check |

Top similarity neighbours: `public-addy-agent-browser-testing-with-devtools` (0.614), `playwright-flow-debugger` (0.571), `public-anthropic-webapp-testing` (0.515), `public-playwright-interactive` (0.503), `public-office-browser-automation` (0.477)

### `public_gold_p07_web_accessibility`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-accessibility`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-web-web-quality-audit` | 0.6228 | 0.3519 | 0.6057 | yes | audit, page, seo, performance | audit, accessibility, web, ask |
| `public-addy-web-core-web-vitals` | 0.6228 | 0.3316 | 0.4420 | no | page | improve, web, ask |
| `public-addy-web-best-practices` | 0.6228 | 0.2675 | 0.5311 | yes | audit | audit, web, ask |

Top similarity neighbours: `public-addy-web-accessibility` (0.623), `accessibility-interaction-auditor` (0.533), `visual-regression-checker` (0.428), `accessibility-checker` (0.396), `product-ops-quality-auditor` (0.375)

### `public_gold_p08_core_web_vitals`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-core-web-vitals`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | 0.6231 | 0.3525 | 0.4420 | no | web, accessibility | web, ask, improve |
| `public-addy-web-best-practices` | 0.6231 | 0.3723 | 0.6158 | yes | web, review | web, ask |
| `public-addy-web-performance` | 0.6231 | 0.4443 | 0.6495 | yes | web | optimize, web, page, experience, fix, better, ask, improve |
| `public-addy-agent-browser-testing-with-devtools` | 0.6231 | 0.3998 | 0.3702 | no | browser | - |

Top similarity neighbours: `public-addy-web-core-web-vitals` (0.623), `web-performance-budget-checker` (0.497), `public-addy-web-performance` (0.444), `public-addy-web-web-quality-audit` (0.431), `implicit-browser-flow-investigator` (0.428)

### `public_gold_p09_systematic_debugging`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-debugging`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 169

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-agent-code-simplification` | 0.2006 | 0.0924 | 0.4312 | no | code, review | - |
| `public-oh-my-code-review` | 0.2006 | 0.0960 | 0.7561 | yes | - | - |
| `public-addy-agent-code-review-and-quality` | 0.2006 | 0.0976 | 0.4408 | no | code, change, review, quality | - |
| `public-openai-gh-fix-ci` | 0.2006 | 0.2676 | 0.5517 | yes | debug, failure, fix, inspect, github | - |

Top similarity neighbours: `ci-failure-debugger` (0.496), `localization-ops-failure-diagnoser` (0.481), `api-ops-failure-diagnoser` (0.452), `implicit-ci-failure-reader` (0.435), `ci-log-root-cause-debugger` (0.422)

### `public_gold_p10_analyze_ci`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-analyze-ci`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-github-actions-templates` | 0.5643 | 0.4254 | 0.4871 | no | github, action, workflow, template | github, action |
| `public-addy-agent-ci-cd-and-automation` | 0.5643 | 0.2980 | 0.2927 | no | - | - |
| `public-oh-my-debugging` | 0.5643 | 0.2267 | 0.5074 | yes | - | - |
| `pr-reviewer` | 0.5643 | 0.5498 | 0.4924 | yes | github, identify | github, extract, request |
| `repo-ops-failure-diagnoser` | 0.5643 | 0.5253 | 0.4503 | yes | fail, workflow | fail |

Top similarity neighbours: `ci-failure-debugger` (0.728), `ci-log-root-cause-debugger` (0.599), `public-swebench-analyze-ci` (0.564), `pr-reviewer` (0.550), `repo-ops-failure-diagnoser` (0.525)

### `public_gold_p11_setup_pre_commit`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-setup-pre-commit`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `git-safety-guardrail-installer` | 0.7449 | 0.4602 | 0.3537 | no | commit, configure, dangerou, git, command | hook, configure |
| `public-mattpocock-git-guardrails-claude-code` | 0.7449 | 0.3687 | 0.4973 | no | add, block, dangerou, git, command | set, hook, add |
| `public-swebench-fix` | 0.7449 | 0.2504 | 0.4116 | no | - | formatt |
| `git-commit-writer` | 0.7449 | 0.4448 | 0.4476 | no | type, commit | type |
| `public-swebench-github-actions-templates` | 0.7449 | 0.4202 | 0.4720 | no | test, github, action | test |

Top similarity neighbours: `public-mattpocock-setup-pre-commit` (0.745), `git-safety-guardrail-installer` (0.460), `git-commit-writer` (0.445), `code-reviewer` (0.433), `public-swebench-github-actions-templates` (0.420)

### `public_gold_p12_git_guardrails`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-git-guardrails-claude-code`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-mattpocock-setup-pre-commit` | 0.7839 | 0.3923 | 0.4973 | no | hook, set, formatt | hook, set, add |
| `public-addy-agent-git-workflow-and-versioning` | 0.7839 | 0.4275 | 0.5196 | yes | git, code, branch, workflow | git, code, branch |
| `public-openai-yeet` | 0.7839 | 0.2564 | 0.4484 | no | flow | push |
| `version-control-helper` | 0.7839 | 0.4721 | 0.4769 | no | git, such, branch, workflow | git, branch |
| `public-swebench-github-actions-templates` | 0.7839 | 0.4263 | 0.4800 | no | workflow | - |

Top similarity neighbours: `public-mattpocock-git-guardrails-claude-code` (0.784), `git-safety-guardrail-installer` (0.714), `public-oh-my-git-guardrails-claude-code` (0.547), `version-control-helper` (0.472), `code-reviewer` (0.446)

### `public_gold_p13_address_pr_comments`

- Family: `public_gold_validation`
- Gold skill: `public-openai-gh-address-comments`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 11

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-gh-fix-ci` | 0.4452 | 0.4638 | 0.7495 | yes | github, inspect, report, debug, fail, check | github, check |
| `public-openai-yeet` | 0.4452 | 0.2444 | 0.7015 | yes | github, request | open, github, cli |
| `public-lbussell-creating-pull-requests` | 0.4452 | 0.2438 | 0.4126 | no | - | - |
| `public-lbussell-triaging-issues` | 0.4452 | 0.2586 | 0.3870 | no | - | - |

Top similarity neighbours: `pr-reviewer` (0.579), `pr-review-comment-resolver` (0.565), `review-comment-resolver` (0.531), `public-swebench-analyze-ci` (0.511), `code-reviewer` (0.503)

### `public_gold_p14_netlify_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-netlify-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-vercel-deploy` | 0.7001 | 0.4486 | 0.5328 | yes | deploy, deployment, vercel | deploy, link, preview |
| `public-openai-cloudflare-deploy` | 0.7001 | 0.4258 | 0.5497 | yes | deploy, project, cloudflare | deploy, project, asks, host, publish |
| `public-openai-render-deploy` | 0.7001 | 0.4544 | 0.5343 | yes | deploy, render | deploy, host, publish |
| `public-oh-my-vercel-deploy` | 0.7001 | 0.2982 | 0.4725 | no | - | - |

Top similarity neighbours: `public-netlify-deploy` (0.700), `public-openai-render-deploy` (0.454), `public-openai-vercel-deploy` (0.449), `public-openai-cloudflare-deploy` (0.426), `deployment-release-verifier` (0.381)

### `public_gold_p15_cloudflare_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cloudflare-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-netlify-deploy` | 0.5601 | 0.4550 | 0.5497 | yes | publish, includ, netlify | deploy, asks, host, publish, project |
| `public-openai-vercel-deploy` | 0.5601 | 0.3073 | 0.6909 | yes | vercel | deploy, application |
| `public-openai-render-deploy` | 0.5601 | 0.3987 | 0.7215 | yes | publish, platform, render | deploy, application, platform, host, publish, set |
| `public-swebench-k8s-manifest-generator` | 0.5601 | 0.3544 | 0.4674 | no | kubernete, manifest | service |

Top similarity neighbours: `public-openai-cloudflare-deploy` (0.560), `public-netlify-deploy` (0.455), `public-openai-render-deploy` (0.399), `cloud-ops-evidence-grounder` (0.361), `cloud-ops-resource-linker` (0.358)

### `public_gold_p16_render_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-render-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-netlify-deploy` | 0.7120 | 0.5455 | 0.5343 | yes | repo, deploy, netlify | deploy, host, publish |
| `public-openai-vercel-deploy` | 0.7120 | 0.4534 | 0.7205 | yes | deployment, deploy, vercel | deploy, application |
| `public-openai-cloudflare-deploy` | 0.7120 | 0.4484 | 0.7215 | yes | service, deploy, cloudflare | deploy, application, host, publish, set, platform |
| `public-swebench-k8s-manifest-generator` | 0.7120 | 0.4760 | 0.4988 | no | deployment, service, generat, yaml, kubernete | generat, yaml |

Top similarity neighbours: `public-openai-render-deploy` (0.712), `public-netlify-deploy` (0.545), `public-swebench-k8s-manifest-generator` (0.476), `k8s-ops-artifact-packager` (0.464), `kubernetes-deployment-helper` (0.456)

### `public_gold_p17_mcp_builder`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-mcp-builder`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-api-design-principles` | 0.6014 | 0.2490 | 0.4096 | no | design, api | build, apis |
| `public-office-mcp-hub` | 0.6014 | 0.4304 | 0.5815 | yes | tool, mcp | mcp, model, context, protocol, tool |
| `public-openai-chatgpt-apps` | 0.6014 | 0.3819 | 0.4351 | no | tool, mcp, design, server | mcp, server, tool, build, apis, sdk |
| `webhook-integration-planner` | 0.6014 | 0.5363 | 0.4266 | yes | - | - |

Top similarity neighbours: `mcp-server-builder` (0.641), `public-anthropic-mcp-builder` (0.601), `public-swebench-mcp-builder` (0.587), `auth-flow-integrator` (0.574), `api-security-threat-reviewer` (0.567)

### `public_gold_p18_chatgpt_apps`

- Family: `public_gold_validation`
- Gold skill: `public-openai-chatgpt-apps`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-anthropic-mcp-builder` | 0.7777 | 0.4676 | 0.4351 | no | mcp, server, build, sdk | mcp, sdk, tool, build, server, apis |
| `public-openai-cli-creator` | 0.7777 | 0.2403 | 0.5055 | yes | app, build, sdk, cli | sdk, tool, build, codex, docs |
| `public-openai-openai-docs` | 0.7777 | 0.2282 | 0.5980 | yes | mcp, build, need | mcp, tool, build, need, apis, domain, openai, docs |
| `public-office-ai-agent-builder` | 0.7777 | 0.3022 | 0.4342 | no | build, chatgpt | chatgpt, tool, build |

Top similarity neighbours: `public-openai-chatgpt-apps` (0.778), `public-swebench-mcp-builder` (0.491), `mcp-server-builder` (0.475), `public-anthropic-mcp-builder` (0.468), `public-mattpocock-to-prd` (0.369)

### `public_gold_p19_cli_creator`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cli-creator`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-openai-docs` | 0.7326 | 0.4475 | 0.6761 | yes | docs, build, documentation, only, mcp | tool, build, docs |
| `public-obsidian-obsidian-cli` | 0.7326 | 0.3074 | 0.5412 | yes | note, command, create | cli, create, run, read, command, manage |
| `openapi-contract-reviewer` | 0.7326 | 0.5764 | 0.4809 | no | openapi, example, contract, auth | openapi, example, auth |
| `mcp-server-builder` | 0.7326 | 0.4904 | 0.3126 | no | example, build, mcp, server | tool, build, example |

Top similarity neighbours: `public-openai-cli-creator` (0.733), `openapi-contract-reviewer` (0.576), `openapi-contract-tester` (0.504), `auth-flow-integrator` (0.499), `mcp-server-builder` (0.490)

### `public_gold_p20_hf_datasets`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-datasets`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-hf-cli` | 0.7564 | 0.3896 | 0.6347 | yes | dataset, hugg, face, download, model, train | hugg, face, dataset, search, download, read |
| `public-huggingface-huggingface-tool-builder` | 0.7564 | 0.4202 | 0.7699 | yes | hugg, face, api | hugg, face, api, fetch |
| `public-huggingface-train-sentence-transformers` | 0.7564 | 0.4348 | 0.5237 | yes | hugg, face, model, train | hugg, face |
| `public-office-data-extractor` | 0.7564 | 0.1629 | 0.4600 | no | - | - |

Top similarity neighbours: `public-huggingface-datasets` (0.756), `hf-dataset-viewer-inspector` (0.616), `public-huggingface-huggingface-papers` (0.517), `public-huggingface-huggingface-vision-trainer` (0.485), `hf-community-eval-runner` (0.477)

### `public_gold_p21_hf_gradio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-gradio`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-zerogpu` | 0.5102 | 0.4525 | 0.3259 | yes | gradio, demo, python, zerogpu | gradio, build, demo, python |
| `public-huggingface-huggingface-tool-builder` | 0.5102 | 0.1710 | 0.6648 | yes | create, api, call | build |
| `public-huggingface-datasets` | 0.5102 | 0.2670 | 0.5532 | yes | dataset, viewer, api | - |
| `public-huggingface-transformers-js` | 0.5102 | 0.2223 | 0.4367 | no | transformer, browser | - |

Top similarity neighbours: `gradio-demo-builder` (0.568), `public-huggingface-huggingface-gradio` (0.510), `public-huggingface-huggingface-zerogpu` (0.453), `public-swebench-grafana-dashboards` (0.350), `hf-zerogpu-space-deployer` (0.329)

### `public_gold_p22_hf_vision_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-vision-trainer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-llm-trainer` | 0.4935 | 0.3919 | 0.7570 | yes | model, train, fine-tune, dataset, vision, local, gguf | model, hugg, face, train, vision, transformer, jobs, fine-tune |
| `public-huggingface-huggingface-community-evals` | 0.4935 | 0.2443 | 0.6042 | yes | model, evaluation, local | model, hugg, face, transformer, jobs, evaluation, hardware, selection |
| `public-huggingface-huggingface-local-models` | 0.4935 | 0.3025 | 0.5580 | yes | model, local, gguf | model, cover, selection |
| `public-huggingface-train-sentence-transformers` | 0.4935 | 0.4114 | 0.5969 | yes | model, train, fine-tune | model, hugg, face, train, classification, fine-tune, cover, loss |

Top similarity neighbours: `public-huggingface-huggingface-vision-trainer` (0.493), `sentence-transformer-finetuner` (0.429), `public-huggingface-train-sentence-transformers` (0.411), `public-huggingface-huggingface-llm-trainer` (0.392), `training-ops-field-extractor` (0.350)

### `public_gold_p23_sentence_transformer_training`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-train-sentence-transformers`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-transformers-js` | 0.5595 | 0.3325 | 0.6427 | yes | text, browser, transformer, model | model, classification, multimodal, hugg, face, hub |
| `public-huggingface-huggingface-llm-trainer` | 0.5595 | 0.1334 | 0.6213 | yes | train, fine-tune, transformer, local, model | model, train, fine-tune, cover, selection, hugg, face, hub |
| `public-huggingface-huggingface-local-models` | 0.5595 | 0.0445 | 0.4039 | no | local, model | model, cover, selection |
| `public-huggingface-datasets` | 0.5595 | 0.0837 | 0.5237 | yes | text | hugg, face |

Top similarity neighbours: `sentence-transformer-finetuner` (0.609), `public-huggingface-train-sentence-transformers` (0.559), `search-ops-rewrite-editor` (0.361), `search-ops-summary-writer` (0.357), `document-extractor` (0.341)

### `public_gold_p24_hf_cli`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-hf-cli`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-datasets` | 0.5432 | 0.6777 | 0.6347 | yes | hugg, face, metadata, dataset, viewer, api | hugg, face, dataset, download, read, search |
| `public-huggingface-huggingface-paper-publisher` | 0.5432 | 0.4759 | 0.5279 | yes | hugg, face, hub, model, manage, dataset | hugg, face, dataset, hub, model, paper |
| `public-huggingface-huggingface-local-models` | 0.5432 | 0.4894 | 0.5191 | yes | model, file | model, local, runn |
| `public-huggingface-huggingface-tool-builder` | 0.5432 | 0.4614 | 0.6485 | yes | hugg, face, api, tool | hugg, face, data |

Top similarity neighbours: `public-huggingface-datasets` (0.678), `hf-dataset-viewer-inspector` (0.605), `public-huggingface-hf-cli` (0.543), `public-huggingface-huggingface-community-evals` (0.505), `public-huggingface-huggingface-papers` (0.489)

### `public_gold_p25_data_pipeline`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-pipeline`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | 0.6553 | 0.3651 | 0.6670 | yes | data, analysi | data |
| `public-office-data-extractor` | 0.6553 | 0.1637 | 0.5458 | yes | - | - |
| `public-office-database-sync` | 0.6553 | 0.4442 | 0.6146 | yes | data, database | data, integration |
| `public-swebench-dbt-transformation-patterns` | 0.6553 | 0.3829 | 0.4860 | no | data, analytic | data, analytic |

Top similarity neighbours: `public-office-data-pipeline` (0.655), `public-office-etl-pipeline` (0.611), `public-office-database-sync` (0.444), `analytics-ops-resource-linker` (0.421), `analytics-ops-dependency-mapper` (0.417)

### `public_gold_p26_database_sync`

- Family: `public_gold_validation`
- Gold skill: `public-office-database-sync`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-data-pipeline` | 0.4121 | 0.3998 | 0.6146 | yes | etl, pipeline | data, integration |
| `public-office-airtable-automation` | 0.4121 | 0.2749 | 0.5722 | yes | - | database, integration |
| `public-office-crm-automation` | 0.4121 | 0.2745 | 0.5899 | yes | synchronization | synchronization |
| `public-office-data-analysis` | 0.4121 | 0.2562 | 0.5178 | yes | create, analysi | data |

Top similarity neighbours: `public-office-database-sync` (0.412), `public-office-data-pipeline` (0.400), `graphql-schema-designer` (0.388), `public-office-etl-pipeline` (0.379), `database-ops-dependency-mapper` (0.338)

### `public_gold_p27_contract_review`

- Family: `public_gold_validation`
- Gold skill: `public-office-contract-review`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-contract-template` | 0.4547 | 0.2519 | 0.5212 | yes | - | - |
| `public-security-threat-model` | 0.4547 | 0.2521 | 0.4274 | no | review | - |
| `public-office-proposal-writer` | 0.4547 | 0.2704 | 0.6207 | yes | - | - |
| `document-summariser` | 0.4547 | 0.2082 | 0.3637 | no | contract, summary | contract |

Top similarity neighbours: `contract-risk-reviewer` (0.638), `vendor-ops-risk-reviewer` (0.537), `procurement-risk-summariser` (0.520), `vendor-ops-summary-writer` (0.517), `contract-ops-risk-reviewer` (0.512)

### `public_gold_p28_suspicious_email`

- Family: `public_gold_validation`
- Gold skill: `public-office-suspicious-email`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-email-classifier` | 0.6736 | 0.3451 | 0.5754 | yes | email | email |
| `public-office-email-drafter` | 0.6736 | 0.3670 | 0.6319 | yes | - | - |
| `public-office-gmail-workflows` | 0.6736 | 0.1546 | 0.4535 | no | email | email |
| `public-office-security-monitoring` | 0.6736 | 0.2635 | 0.6193 | yes | response | security, threat |

Top similarity neighbours: `public-office-suspicious-email` (0.674), `email-classification-router` (0.496), `email-ops-risk-reviewer` (0.485), `email-polisher` (0.483), `email-ops-evidence-grounder` (0.472)

### `public_gold_p29_ai_slides`

- Family: `public_gold_validation`
- Gold skill: `public-office-ai-slides`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-md-slides` | 0.4528 | 0.2682 | 0.6531 | yes | - | - |
| `public-office-html-slides` | 0.4528 | 0.2675 | 0.6312 | yes | - | - |
| `public-office-dev-slides` | 0.4528 | 0.2477 | 0.6959 | yes | - | - |
| `public-anthropic-theme-factory` | 0.4528 | 0.4179 | 0.4167 | yes | generate, slide, apply, theme | generate, slide |

Top similarity neighbours: `slide-deck-visual-auditor` (0.546), `slide-outline-builder` (0.545), `public-office-ppt-visual` (0.466), `public-office-ai-slides` (0.453), `deck-template-applier` (0.439)

### `public_gold_p30_figma_implement_design`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-implement-design`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-figma-generate-design` | 0.5917 | 0.5603 | 0.7891 | yes | figma, design, create, code, update, screen, component | figma, code, design, component, application, build, match, write |
| `public-openai-figma-generate-library` | 0.5917 | 0.4924 | 0.8069 | yes | figma, design, create, code, update, component | figma, code, design, component, build, figma-use |
| `public-openai-figma-code-connect-components` | 0.5917 | 0.4689 | 0.8217 | yes | figma, design, create, code, component | figma, code, design, component, canva, write, via, figma-use |
| `public-openai-figma-use` | 0.5917 | 0.4479 | 0.7525 | yes | figma, context, create, node, component | figma, component, file, build, write |

Top similarity neighbours: `public-openai-figma-implement-design` (0.592), `public-openai-figma-generate-design` (0.560), `public-openai-figma` (0.558), `public-openai-figma-generate-library` (0.492), `public-openai-figma-code-connect-components` (0.469)

### `public_gold_p31_skill_creator`

- Family: `public_gold_validation`
- Gold skill: `public-skill-creator`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-skill-installer` | 0.5802 | 0.5513 | 0.7007 | yes | codex, includ, install | - |
| `public-openai-migrate-to-codex` | 0.5802 | 0.4171 | 0.4998 | no | codex, migrate | - |
| `public-oh-my-agentic-skills` | 0.5802 | 0.3679 | 0.6669 | yes | - | - |
| `skill-field-auditor` | 0.5802 | 0.4561 | 0.4555 | no | workflow, includ, trigger, resource, exist | exist, workflow |

Top similarity neighbours: `skill-creator` (0.699), `skill-editor` (0.672), `skill-authoring-guide` (0.584), `public-skill-creator` (0.580), `skill-finder` (0.557)

### `public_gold_p32_security_threat_model`

- Family: `public_gold_validation`
- Gold skill: `public-security-threat-model`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 9

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-security-best-practices` | 0.4616 | 0.4009 | 0.6228 | yes | best, practice | trigger, only, explicitly, perform, general, code, review, non-security |
| `public-openai-security-ownership-map` | 0.4616 | 0.5184 | 0.4860 | yes | sensitive, list, ownership | trigger, only, explicitly, general, code, non-security |
| `public-swebench-security-review` | 0.4616 | 0.4129 | 0.5120 | yes | sensitive | work |

Top similarity neighbours: `public-oh-my-file-organization` (0.535), `public-openai-security-ownership-map` (0.518), `public-oh-my-changelog-maintenance` (0.516), `public-addy-agent-source-driven-development` (0.491), `public-addy-web-best-practices` (0.486)

### `public_gold_p33_openai_docs`

- Family: `public_gold_validation`
- Gold skill: `public-openai-openai-docs`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-chatgpt-apps` | 0.5876 | 0.6329 | 0.5980 | yes | openai, build, chatgpt, docs | openai, build, apis, need, docs, mcp, tool, domain |
| `public-openai-cli-creator` | 0.5876 | 0.5116 | 0.6761 | yes | api, build, app, cli, docs | build, docs, tool |
| `public-anthropic-claude-api` | 0.5876 | 0.4815 | 0.5233 | yes | api, openai, model, build, anthropic | openai, model, asks, build, citation, tool |
| `public-huggingface-huggingface-tool-builder` | 0.5876 | 0.3370 | 0.4335 | no | api, build | build, tool |

Top similarity neighbours: `public-openai-chatgpt-apps` (0.633), `public-openai-openai-docs` (0.588), `public-openai-speech` (0.558), `public-openai-notion-knowledge-capture` (0.533), `public-openai-migrate-to-codex` (0.531)

### `public_gold_p34_playwright`

- Family: `public_gold_validation`
- Gold skill: `public-openai-playwright`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-playwright-interactive` | 0.4885 | 0.5276 | 0.5951 | yes | browser, interaction | browser, debug |
| `public-addy-agent-browser-testing-with-devtools` | 0.4885 | 0.6752 | 0.5324 | yes | browser, test, need, chrome, devtool, mcp | require, real, browser, data, debug, via |
| `public-anthropic-webapp-testing` | 0.4885 | 0.6089 | 0.6630 | yes | browser, playwright, test, local, screenshot | browser, screenshot, debug |

Top similarity neighbours: `public-addy-agent-browser-testing-with-devtools` (0.675), `public-anthropic-webapp-testing` (0.609), `playwright-flow-debugger` (0.601), `public-office-browser-automation` (0.568), `public-playwright-interactive` (0.528)

### `public_gold_p35_screenshot`

- Family: `public_gold_validation`
- Gold skill: `public-openai-screenshot`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 42

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-playwright` | 0.2715 | 0.4331 | 0.6378 | yes | screenshot, debug | screenshot |
| `public-addy-agent-browser-testing-with-devtools` | 0.2715 | 0.4391 | 0.3327 | yes | capture, visual, test, console, network, debug | capture, need |
| `public-office-browser-automation` | 0.2715 | 0.3385 | 0.2067 | yes | playwright, test | - |
| `public-anthropic-webapp-testing` | 0.2715 | 0.4909 | 0.3983 | yes | screenshot, local, playwright, test, debug | screenshot |

Top similarity neighbours: `playwright-flow-debugger` (0.537), `public-anthropic-webapp-testing` (0.491), `public-playwright-interactive` (0.448), `public-addy-agent-browser-testing-with-devtools` (0.439), `web-page-snapshotter` (0.434)

### `public_gold_p36_sentry`

- Family: `public_gold_validation`
- Gold skill: `public-openai-sentry`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-oh-my-monitoring-observability` | 0.5726 | 0.3167 | 0.5108 | yes | - | - |
| `public-swebench-python-observability` | 0.5726 | 0.3975 | 0.3502 | no | observability, distribut | production |
| `metrics-root-cause-diagnoser` | 0.5726 | 0.4253 | 0.0660 | no | likely, regression | - |
| `distributed-trace-investigator` | 0.5726 | 0.5501 | 0.1830 | yes | trace, distribut | - |

Top similarity neighbours: `public-openai-sentry` (0.573), `distributed-trace-investigator` (0.550), `email-ops-failure-diagnoser` (0.513), `analytics-ops-failure-diagnoser` (0.512), `public-swebench-distributed-tracing` (0.490)

### `public_gold_p37_transcribe`

- Family: `public_gold_validation`
- Gold skill: `public-openai-transcribe`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-speech` | 0.5457 | 0.4048 | 0.7527 | yes | audio, speech | audio, asks, speech |
| `public-office-transcription-automation` | 0.5457 | 0.5017 | 0.6595 | yes | audio, meet | audio, video |
| `public-office-podcast-automation` | 0.5457 | 0.4989 | 0.4800 | yes | record, podcast, workflow | - |
| `public-office-meeting-notes` | 0.5457 | 0.2579 | 0.4194 | no | - | - |

Top similarity neighbours: `public-openai-transcribe` (0.546), `public-office-transcription-automation` (0.502), `public-office-podcast-automation` (0.499), `speaker-notes-writer` (0.442), `public-openai-speech` (0.405)

### `public_gold_p38_speech`

- Family: `public_gold_validation`
- Gold skill: `public-openai-speech`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-transcribe` | 0.5259 | 0.5359 | 0.7527 | yes | audio, transcribe | audio, asks, speech |
| `public-office-transcription-automation` | 0.5259 | 0.5280 | 0.5263 | yes | audio, automate | audio, generation |
| `public-office-podcast-automation` | 0.5259 | 0.6222 | 0.4482 | yes | workflow, record, automate, podcast, publish | - |
| `public-anthropic-slack-gif-creator` | 0.5259 | 0.1307 | 0.2883 | no | - | - |

Top similarity neighbours: `public-office-podcast-automation` (0.622), `public-openai-transcribe` (0.536), `public-office-transcription-automation` (0.528), `public-openai-speech` (0.526), `speaker-notes-writer` (0.382)

### `public_gold_p39_jupyter_notebook`

- Family: `public_gold_validation`
- Gold skill: `public-openai-jupyter-notebook`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | 0.5194 | 0.4969 | 0.3195 | yes | create, csv, analysi, report, excel | create, generate |
| `public-huggingface-datasets` | 0.5194 | 0.3409 | 0.3278 | no | hugg, face, dataset | - |
| `public-swebench-python-configuration` | 0.5194 | 0.2837 | 0.5567 | yes | python | - |
| `public-office-report-generator` | 0.5194 | 0.4026 | 0.2646 | no | report | generate |

Top similarity neighbours: `public-openai-jupyter-notebook` (0.519), `public-office-data-analysis` (0.497), `public-office-report-generator` (0.403), `data-analysis-overview` (0.401), `public-office-xlsx-manipulation` (0.368)

### `public_gold_p40_linear`

- Family: `public_gold_validation`
- Gold skill: `public-openai-linear`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 12

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-lbussell-creating-issues` | 0.4387 | 0.0588 | 0.4192 | no | - | - |
| `public-lbussell-triaging-issues` | 0.4387 | 0.0636 | 0.4074 | no | - | - |
| `public-office-jira-automation` | 0.4387 | 0.5218 | 0.4701 | yes | issue, project, jira | issue, project, workflow |
| `public-office-asana-automation` | 0.4387 | 0.5382 | 0.4780 | yes | team, project, asana | project, team, workflow |

Top similarity neighbours: `public-office-asana-automation` (0.538), `public-office-jira-automation` (0.522), `public-openai-notion-spec-to-implementation` (0.499), `repo-ops-scenario-planner` (0.490), `engineering-design-ops-scenario-planner` (0.475)

### `public_gold_p41_yeet`

- Family: `public_gold_validation`
- Gold skill: `public-openai-yeet`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 195

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-gh-address-comments` | 0.2407 | 0.3908 | 0.7015 | yes | current, branch, open, github, addres, review, comment | github, open, cli |
| `public-openai-gh-fix-ci` | 0.2407 | 0.4781 | 0.7148 | yes | draft, github, debug, logs | github, only, asks |

Top similarity neighbours: `pr-review-comment-resolver` (0.625), `ci-log-root-cause-debugger` (0.620), `code-reviewer` (0.578), `ci-failure-debugger` (0.572), `repo-code-reviewer` (0.559)

### `public_gold_p42_migrate_to_codex`

- Family: `public_gold_validation`
- Gold skill: `public-openai-migrate-to-codex`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-skill-creator` | 0.5822 | 0.5715 | 0.4998 | yes | exist | - |
| `public-skill-installer` | 0.5822 | 0.6470 | 0.5912 | yes | codex, includ, install | codex |
| `public-addy-agent-context-engineering` | 0.5822 | 0.4490 | 0.4387 | no | agent, setup | file, agent, project |
| `public-oh-my-agentic-skills` | 0.5822 | 0.5389 | 0.5174 | yes | - | - |

Top similarity neighbours: `public-skill-installer` (0.647), `skill-authoring-guide` (0.607), `public-mattpocock-setup-matt-pocock-skills` (0.585), `public-openai-migrate-to-codex` (0.582), `public-skill-creator` (0.572)

### `public_gold_p43_notion_knowledge_capture`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-knowledge-capture`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-notion-meeting-intelligence` | 0.5687 | 0.5619 | 0.8132 | yes | notion, meet, research | notion |
| `public-office-notion-automation` | 0.5687 | 0.4001 | 0.5413 | yes | notion, database | notion |

Top similarity neighbours: `meeting-notes-action-extractor` (0.624), `public-openai-notion-knowledge-capture` (0.569), `public-openai-notion-meeting-intelligence` (0.562), `meeting-ops-summary-writer` (0.549), `task-extractor` (0.543)

### `public_gold_p44_notion_meeting_intelligence`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-meeting-intelligence`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 5

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | 0.5185 | 0.3483 | 0.5101 | yes | - | notion |

Top similarity neighbours: `meeting-notes-action-extractor` (0.636), `meeting-followup-extractor` (0.608), `meeting-summary-writer` (0.577), `meeting-agenda-builder` (0.560), `public-openai-notion-meeting-intelligence` (0.518)

### `public_gold_p45_notion_spec_to_implementation`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-spec-to-implementation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-notion-knowledge-capture` | 0.6198 | 0.3772 | 0.7377 | yes | notion, link | notion, turn |
| `public-addy-agent-spec-driven-development` | 0.6198 | 0.3734 | 0.6383 | yes | spec, create | spec, feature |
| `public-lbussell-creating-issues` | 0.6198 | -0.0528 | 0.2443 | no | - | - |
| `public-openai-linear` | 0.6198 | 0.1181 | 0.5553 | yes | create, issue | - |

Top similarity neighbours: `public-openai-notion-spec-to-implementation` (0.620), `notion-research-database-builder` (0.495), `product-ops-scenario-planner` (0.494), `engineering-design-ops-scenario-planner` (0.455), `public-openai-notion-research-documentation` (0.438)

### `public_gold_p46_figma_code_connect`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-code-connect-components`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-figma-implement-design` | 0.7008 | 0.6075 | 0.8217 | yes | component, figma, code, design, implement, generate | code, component, figma, design, canva, write, via, figma-use |
| `public-openai-figma-generate-library` | 0.7008 | 0.5495 | 0.7586 | yes | component, figma, code, design | code, component, figma, design, create, figma-use |
| `public-openai-figma-generate-design` | 0.7008 | 0.5246 | 0.6680 | yes | component, figma, code, design, screen | code, component, figma, design, create, write, via, figma-use |
| `public-openai-figma-use` | 0.7008 | 0.4134 | 0.7254 | yes | component, figma | component, figma, tool, create, write |

Top similarity neighbours: `public-openai-figma-code-connect-components` (0.701), `public-openai-figma-implement-design` (0.608), `public-openai-figma-generate-library` (0.549), `public-openai-figma-generate-design` (0.525), `public-openai-figma` (0.449)

### `public_gold_p47_figma_generate_library`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-generate-library`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-figma-code-connect-components` | 0.5826 | 0.5830 | 0.7586 | yes | code, component, figma, write, create, connect, mapping | figma, design, create, component, code, figma-use |
| `public-openai-figma-implement-design` | 0.5826 | 0.6062 | 0.8069 | yes | code, generate, component, figma, implement, application, write | build, figma, design, component, code, figma-use |
| `public-openai-figma-create-design-system-rules` | 0.5826 | 0.5389 | 0.6901 | yes | generate, figma, rule, create | figma, design, system, codebase, create, set |

Top similarity neighbours: `public-openai-figma-implement-design` (0.606), `public-openai-figma-code-connect-components` (0.583), `public-openai-figma-generate-library` (0.583), `public-openai-figma-generate-design` (0.564), `public-openai-figma-create-design-system-rules` (0.539)

### `public_gold_p48_figma_design_system_rules`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-create-design-system-rules`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-figma-generate-library` | 0.5933 | 0.5420 | 0.6901 | yes | figma, create, component, token, code | design, system, codebase, create, set, figma |
| `public-openai-figma-generate-design` | 0.5933 | 0.5892 | 0.6559 | yes | figma, create, layout, component, token, screen, code | design, system, create, workflow, figma |
| `public-anthropic-brand-guidelines` | 0.5933 | 0.2393 | 0.3508 | no | - | design, guideline |
| `public-anthropic-theme-factory` | 0.5933 | 0.2536 | 0.3098 | no | generate | generate |

Top similarity neighbours: `public-openai-figma-implement-design` (0.616), `public-openai-figma-create-design-system-rules` (0.593), `public-openai-figma-generate-design` (0.589), `public-openai-figma-generate-library` (0.542), `public-openai-figma-code-connect-components` (0.533)

### `public_gold_p49_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 24

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | 0.4450 | 0.3603 | 0.4011 | no | audit, accessibility, web | ask, improve |
| `public-addy-web-core-web-vitals` | 0.4450 | 0.4138 | 0.6434 | yes | page, search, core, web, vital | search, optimize, optimization, rank, ask, improve, fix |
| `public-addy-web-best-practices` | 0.4450 | 0.3601 | 0.5454 | yes | audit, web | ask |

Top similarity neighbours: `seo-ops-quality-auditor` (0.633), `seo-metadata-checker` (0.623), `public-addy-web-web-quality-audit` (0.591), `seo-ops-risk-reviewer` (0.574), `seo-ops-compliance-checker` (0.559)

### `public_gold_p50_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-web-core-web-vitals` | 0.5313 | 0.4798 | 0.6495 | yes | web, lcp, inp, cls | optimize, web, better, experience, ask, reduce, fix, improve |
| `public-addy-web-best-practices` | 0.5313 | 0.3926 | 0.6306 | yes | web, code, review | web, ask, audit |
| `public-addy-agent-performance-optimization` | 0.5313 | 0.4690 | 0.7709 | yes | web, load, performance | performance, load, optimize, web, time, fix |
| `public-addy-web-web-quality-audit` | 0.5313 | 0.4594 | 0.6769 | yes | web, performance, review | performance, optimize, web, ask, site, page, audit |

Top similarity neighbours: `web-performance-budget-checker` (0.620), `public-addy-web-performance` (0.531), `api-design-reviewer` (0.483), `public-addy-web-core-web-vitals` (0.480), `public-addy-agent-performance-optimization` (0.469)

### `public_gold_p51_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | 0.6056 | 0.4925 | 0.6057 | yes | web, audit, accessibility, wcag | audit, web, accessibility, ask |
| `public-addy-web-core-web-vitals` | 0.6056 | 0.4377 | 0.5805 | yes | web, core, vital | web, ask, page, optimize |
| `public-addy-web-seo` | 0.6056 | 0.2377 | 0.6184 | yes | seo | seo, ask, optimize |
| `public-addy-web-best-practices` | 0.6056 | 0.4483 | 0.7283 | yes | web, quality, audit, best, practice | quality, audit, web, best, practice, ask, review, check |

Top similarity neighbours: `public-addy-web-web-quality-audit` (0.606), `web-ops-quality-auditor` (0.604), `web-ops-risk-reviewer` (0.532), `content-ops-quality-auditor` (0.528), `seo-ops-quality-auditor` (0.504)

### `public_gold_p52_api_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | 0.5447 | 0.6576 | 0.5047 | yes | contract, review, openapi | endpoint, contract |
| `public-openai-cli-creator` | 0.5447 | 0.4450 | 0.4493 | no | stable, exist, openapi, build, cli | stable, api |
| `external-api-integration-planner` | 0.5447 | 0.5586 | 0.5106 | yes | - | api, endpoint |

Top similarity neighbours: `openapi-contract-reviewer` (0.658), `external-api-integration-planner` (0.559), `architecture-boundary-reviewer` (0.545), `public-addy-agent-api-and-interface-design` (0.545), `openapi-contract-tester` (0.534)

### `public_gold_p53_context_engineering`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-context-engineering`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-agent-source-driven-development` | 0.6171 | 0.4432 | 0.6046 | yes | - | - |
| `public-addy-agent-planning-and-task-breakdown` | 0.6171 | 0.4868 | 0.7219 | yes | - | start, need |
| `public-oh-my-codebase-search` | 0.6171 | 0.2418 | 0.4202 | no | - | - |
| `public-openai-migrate-to-codex` | 0.6171 | 0.4430 | 0.4387 | no | project, agent, file, migrate, codex | agent, file, project |

Top similarity neighbours: `public-addy-agent-context-engineering` (0.617), `public-n-skills-orchestration` (0.541), `public-addy-agent-idea-refine` (0.513), `public-mattpocock-improve-codebase-architecture` (0.497), `public-addy-agent-spec-driven-development` (0.493)

### `public_gold_p54_deprecation_migration`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-deprecation-and-migration`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-mattpocock-migrate-to-shoehorn` | 0.4546 | 0.1844 | 0.2827 | no | - | - |
| `public-addy-agent-incremental-implementation` | 0.4546 | 0.1493 | 0.7172 | yes | - | feature, code |
| `public-addy-agent-api-and-interface-design` | 0.4546 | 0.3725 | 0.6434 | yes | api | apis |
| `database-migration-risk-assessor` | 0.4546 | 0.6315 | 0.4665 | yes | plan, compatibility, database, migration, risk | migration |

Top similarity neighbours: `database-migration-risk-assessor` (0.631), `migration-risk-auditor` (0.492), `architecture-boundary-reviewer` (0.487), `api-ops-scenario-planner` (0.479), `api-ops-risk-reviewer` (0.471)

### `public_gold_p55_documentation_adrs`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-documentation-and-adrs`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 24

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-oh-my-api-documentation` | 0.3877 | 0.1798 | 0.5090 | yes | - | - |
| `code-documentation-writer` | 0.3877 | 0.3326 | 0.4263 | yes | write, documentation | documentation, apis, future, understand |
| `public-openai-notion-research-documentation` | 0.3877 | 0.2068 | 0.5239 | yes | documentation, report | documentation |
| `public-office-report-generator` | 0.3877 | 0.0519 | 0.3262 | no | report | - |

Top similarity neighbours: `architecture-boundary-reviewer` (0.518), `public-anthropic-claude-api` (0.477), `api-ops-summary-writer` (0.476), `api-design-reviewer` (0.460), `api-ops-scenario-planner` (0.456)

### `public_gold_p56_spec_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-spec-driven-development`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-agent-test-driven-development` | 0.4171 | 0.2450 | 0.7098 | yes | test | exist |
| `public-addy-agent-incremental-implementation` | 0.4171 | 0.1992 | 0.7334 | yes | feature | feature, change |
| `public-openai-notion-spec-to-implementation` | 0.4171 | 0.5328 | 0.6383 | yes | spec, turn, feature, implementation, notion | spec, feature |
| `public-mattpocock-to-prd` | 0.4171 | 0.1093 | 0.4916 | no | turn | create, project |

Top similarity neighbours: `public-openai-notion-spec-to-implementation` (0.533), `engineering-design-ops-scenario-planner` (0.431), `notion-research-database-builder` (0.420), `public-addy-agent-spec-driven-development` (0.417), `public-office-notion-automation` (0.391)

### `public_gold_p57_test_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-test-driven-development`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 183

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-agent-spec-driven-development` | 0.2175 | 0.0485 | 0.7098 | yes | only, specification | exist |
| `public-oh-my-testing-strategies` | 0.2175 | 0.2398 | 0.6087 | yes | - | - |

Top similarity neighbours: `ci-failure-debugger` (0.522), `implicit-ci-failure-reader` (0.419), `debugging-root-cause-helper` (0.406), `ux-ops-failure-diagnoser` (0.399), `public-mattpocock-tdd` (0.389)

### `public_gold_p58_source_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-source-driven-development`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-addy-agent-context-engineering` | 0.3554 | 0.1763 | 0.6046 | yes | context | - |
| `public-oh-my-codebase-search` | 0.3554 | 0.2759 | 0.4333 | yes | - | - |
| `public-addy-agent-incremental-implementation` | 0.3554 | 0.2145 | 0.7010 | yes | code | code |
| `public-mattpocock-diagnose` | 0.3554 | 0.2029 | 0.3359 | no | - | - |

Top similarity neighbours: `public-mattpocock-improve-codebase-architecture` (0.378), `public-swebench-python-anti-patterns` (0.358), `public-addy-agent-source-driven-development` (0.355), `public-architecture-patterns` (0.347), `public-swebench-add-uint-support` (0.344)

### `public_gold_p59_anthropic_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 10

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-openai-docs` | 0.4764 | 0.5062 | 0.5233 | yes | guidance, tool, model, openai, docs, build, mcp | model, openai, build, asks, tool, citation |
| `public-openai-cli-creator` | 0.4764 | 0.4869 | 0.5011 | yes | api, tool, docs, cli, build | sdk, api, build, exist, tool |
| `public-anthropic-mcp-builder` | 0.4764 | 0.4963 | 0.2944 | yes | tool, model, build, mcp, server | sdk, model, build, tool |
| `public-huggingface-hf-cli` | 0.4764 | 0.4048 | 0.4119 | yes | model, hugg, face, cli | model, manag, agent, cache, like, general |

Top similarity neighbours: `openapi-contract-reviewer` (0.549), `public-openai-speech` (0.544), `public-openai-chatgpt-apps` (0.540), `public-openai-openai-docs` (0.506), `external-api-integration-planner` (0.497)

### `public_gold_p60_doc_coauthoring`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-doc-coauthoring`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-report-generator` | 0.4751 | 0.2627 | 0.3511 | no | generate, report | - |
| `public-office-content-writer` | 0.4751 | 0.2767 | 0.5855 | yes | - | content, write |

Top similarity neighbours: `method-note-builder` (0.518), `partnerships-ops-rewrite-editor` (0.482), `public-anthropic-doc-coauthoring` (0.475), `vendor-ops-rewrite-editor` (0.454), `research-ops-rewrite-editor` (0.449)

### `public_gold_p61_canvas_design`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-canvas-design`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-anthropic-frontend-design` | 0.5186 | 0.4579 | 0.6515 | yes | create, layout, build, frontend, web, design | create, design, asks, poster, avoid |
| `public-anthropic-web-artifacts-builder` | 0.5186 | 0.4108 | 0.4673 | no | frontend, web | - |
| `public-anthropic-theme-factory` | 0.5186 | 0.2510 | 0.4588 | no | - | - |
| `public-openai-figma-generate-design` | 0.5186 | 0.4085 | 0.4175 | no | create, layout, build, app, figma, design | create, design |
| `public-office-diagram-creator` | 0.5186 | 0.5397 | 0.5158 | yes | create | create |
| `public-office-infographic` | 0.5186 | 0.5152 | 0.5663 | yes | visual, layout, design | design, visual |

Top similarity neighbours: `public-office-diagram-creator` (0.540), `public-anthropic-canvas-design` (0.519), `public-office-infographic` (0.515), `public-obsidian-json-canvas` (0.473), `public-office-chart-designer` (0.466)

### `public_gold_p62_theme_factory`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-theme-factory`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-figma-create-design-system-rules` | 0.4999 | 0.2194 | 0.3098 | no | generate, guideline | generate |
| `public-office-brand-guidelines` | 0.4999 | 0.4680 | 0.4262 | yes | visual, brand | - |
| `public-oh-my-design-system` | 0.4999 | 0.2077 | 0.4958 | no | - | - |
| `public-anthropic-canvas-design` | 0.4999 | 0.3234 | 0.4588 | no | visual | - |
| `public-anthropic-frontend-design` | 0.4999 | 0.4652 | 0.5767 | yes | generate, component, styl, frontend | artifact, styl, html, land, page, generate |
| `public-mattpocock-prototype` | 0.4999 | 0.4072 | 0.3518 | no | prototype | - |

Top similarity neighbours: `public-anthropic-theme-factory` (0.500), `product-ops-rewrite-editor` (0.479), `public-office-brand-guidelines` (0.468), `public-anthropic-frontend-design` (0.465), `public-mattpocock-prototype` (0.407)

### `public_gold_p63_hf_zerogpu`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-zerogpu`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | 0.6184 | 0.5916 | 0.3259 | yes | build, gradio | build, demo, gradio, python |
| `public-huggingface-huggingface-local-models` | 0.6184 | 0.4716 | 0.4764 | no | run, local, model | cuda |
| `public-huggingface-hf-cli` | 0.6184 | 0.3928 | 0.3888 | no | hugg, face, space, local, model | space, hugg, face, configur, handl, sure, whenever, mention |
| `public-huggingface-huggingface-tool-builder` | 0.6184 | 0.3425 | 0.3359 | no | hugg, face, build | build, hugg, face, proces |
| `gradio-demo-builder` | 0.6184 | 0.5850 | 0.3498 | yes | constraint, build, gradio, model | build, demo, gradio, constraint |
| `public-huggingface-huggingface-llm-trainer` | 0.6184 | 0.4691 | 0.4730 | no | hugg, face, deployment, local, model | gpu, hugg, face, mention, package, guidance |

Top similarity neighbours: `public-huggingface-huggingface-zerogpu` (0.618), `public-huggingface-huggingface-gradio` (0.592), `gradio-demo-builder` (0.585), `hf-zerogpu-space-deployer` (0.582), `public-huggingface-huggingface-local-models` (0.472)

### `public_gold_p64_hf_llm_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-llm-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-vision-trainer` | 0.4967 | 0.4356 | 0.7570 | yes | model, train, fine-tune, hugg, face, dataset, evaluation, vision | train, model, jobs, hugg, face, selection, fine-tune, vision |
| `public-huggingface-huggingface-community-evals` | 0.4967 | 0.3280 | 0.6820 | yes | model, hugg, face, evaluation | model, jobs, hugg, face, local, selection, gpu, transformer |
| `public-huggingface-huggingface-local-models` | 0.4967 | 0.3004 | 0.6421 | yes | model | model, gguf, convert, local, selection, cover |
| `public-swebench-llm-evaluation` | 0.4967 | 0.3947 | 0.4644 | no | evaluation, llm | - |

Top similarity neighbours: `public-huggingface-train-sentence-transformers` (0.621), `sentence-transformer-finetuner` (0.598), `public-huggingface-huggingface-llm-trainer` (0.497), `public-huggingface-huggingface-vision-trainer` (0.436), `public-huggingface-transformers-js` (0.407)

### `public_gold_p65_hf_local_models`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-local-models`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | 0.6186 | 0.2940 | 0.4832 | no | build | - |
| `public-huggingface-huggingface-zerogpu` | 0.6186 | 0.3171 | 0.4764 | no | hugg, face, runtime, space, build | cuda |
| `public-huggingface-transformers-js` | 0.6186 | 0.6317 | 0.5031 | yes | model, run, hugg, face, runtime, transformer | model, run |
| `public-huggingface-huggingface-llm-trainer` | 0.6186 | 0.5569 | 0.6421 | yes | local, model, hugg, face, gguf, train, transformer | gguf, model, cover, selection, convert, local |
| `public-huggingface-huggingface-community-evals` | 0.6186 | 0.5211 | 0.6436 | yes | local, model, run, hugg, face, transformer | model, run, selection, local |

Top similarity neighbours: `public-huggingface-transformers-js` (0.632), `public-huggingface-huggingface-local-models` (0.619), `public-huggingface-huggingface-llm-trainer` (0.557), `hf-local-model-selector` (0.551), `public-huggingface-huggingface-community-evals` (0.521)

### `public_gold_p66_hf_trackio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-trackio`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-community-evals` | 0.7123 | 0.3403 | 0.4825 | no | run, evaluation | automation |
| `public-swebench-llm-evaluation` | 0.7123 | 0.4740 | 0.4898 | no | metric, evaluation | metric |
| `public-huggingface-huggingface-llm-trainer` | 0.7123 | 0.3616 | 0.5568 | yes | train, trackio | train, trackio |
| `public-office-saas-metrics` | 0.7123 | 0.4139 | 0.2836 | no | metric, saas | metric, analysi |
| `dashboard-ops-monitoring-plan-builder` | 0.7123 | 0.5144 | 0.5392 | yes | metric, dashboard | metric, dashboard |
| `metrics-overview` | 0.7123 | 0.5256 | 0.4836 | no | metric, dashboard | metric, dashboard |

Top similarity neighbours: `public-huggingface-huggingface-trackio` (0.712), `dashboard-ops-quality-auditor` (0.558), `metrics-overview` (0.526), `dashboard-ops-acceptance-test-builder` (0.525), `dashboard-ops-resource-linker` (0.523)

### `public_gold_p67_hf_papers`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-papers`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-paper-publisher` | 0.6557 | 0.6509 | 0.8486 | yes | paper, hugg, face, model, link, publish, page | paper, page, hugg, face, link, model, dataset, research |
| `public-office-academic-search` | 0.6557 | 0.3724 | 0.4620 | no | paper, find | paper, project, analysi, research |
| `public-office-deep-research` | 0.6557 | 0.3646 | 0.4140 | no | topic | structur, analysi, research |
| `public-oh-my-research-paper-writing` | 0.6557 | 0.3279 | 0.5448 | yes | - | - |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.656), `public-huggingface-huggingface-paper-publisher` (0.651), `hf-community-eval-runner` (0.476), `public-huggingface-datasets` (0.457), `public-huggingface-huggingface-community-evals` (0.448)

### `public_gold_p68_hf_paper_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-paper-publisher`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-oh-my-research-paper-writing` | 0.6989 | 0.4085 | 0.5059 | yes | - | - |
| `public-office-academic-search` | 0.6989 | 0.3363 | 0.4622 | no | paper, search, academic | paper, research |
| `public-huggingface-hf-cli` | 0.6989 | 0.4739 | 0.5279 | yes | paper, model, hugg, face, search, academic | paper, hugg, face, hub, model, dataset |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.737), `public-huggingface-huggingface-paper-publisher` (0.699), `public-huggingface-datasets` (0.523), `hf-community-eval-runner` (0.500), `public-huggingface-huggingface-community-evals` (0.500)

### `public_gold_p69_transformers_js`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-transformers-js`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | 0.4668 | 0.3885 | 0.4367 | yes | build, demo, python, gradio | - |
| `public-huggingface-huggingface-local-models` | 0.4668 | 0.2727 | 0.5031 | yes | model, local, server | model, run |
| `public-anthropic-web-artifacts-builder` | 0.4668 | 0.2324 | 0.4757 | no | - | - |
| `public-office-browser-automation` | 0.4668 | 0.4073 | 0.3572 | yes | - | browser |

Top similarity neighbours: `gradio-demo-builder` (0.571), `public-huggingface-transformers-js` (0.467), `public-office-browser-automation` (0.407), `web-ui-tester` (0.404), `public-addy-agent-browser-testing-with-devtools` (0.401)

### `public_gold_p70_obsidian_json_canvas`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-json-canvas`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-obsidian-obsidian-markdown` | 0.4887 | 0.4546 | 0.5939 | yes | create, obsidian, markdown, note | file, create, edit, work, mention, obsidian |
| `public-obsidian-obsidian-bases` | 0.4887 | 0.3926 | 0.5832 | yes | create, obsidian, note, base, view | file, create, edit, work, creat, mention, obsidian |
| `public-obsidian-obsidian-cli` | 0.4887 | 0.3954 | 0.5749 | yes | create, obsidian, note, cli, command | create, obsidian |
| `public-mattpocock-obsidian-vault` | 0.4887 | 0.3799 | 0.4332 | no | create, obsidian, note | create, obsidian |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.494), `public-obsidian-json-canvas` (0.489), `method-note-builder` (0.471), `citation-note-extractor` (0.469), `document-extractor` (0.456)

### `public_gold_p71_obsidian_bases`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-bases`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-obsidian-json-canvas` | 0.4847 | 0.4480 | 0.5832 | yes | obsidian, create, json, canva | obsidian, file, create, edit, work, creat, mention |
| `public-obsidian-obsidian-markdown` | 0.4847 | 0.4617 | 0.7588 | yes | obsidian, note, tags, create | obsidian, file, create, edit, work, note, mention |
| `public-oh-my-obsidian-plugin` | 0.4847 | 0.2366 | 0.5761 | yes | - | - |
| `public-office-notion-automation` | 0.4847 | 0.2572 | 0.3469 | no | - | - |

Top similarity neighbours: `public-obsidian-obsidian-cli` (0.630), `public-mattpocock-obsidian-vault` (0.540), `public-obsidian-obsidian-bases` (0.485), `public-obsidian-obsidian-markdown` (0.462), `public-office-obsidian-automation` (0.450)

### `public_gold_p72_obsidian_cli`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-cli`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-obsidian-json-canvas` | 0.6585 | 0.3477 | 0.5749 | yes | create, obsidian, canva, file | obsidian, create |
| `public-obsidian-obsidian-bases` | 0.6585 | 0.4281 | 0.6554 | yes | create, note, obsidian, file | obsidian, note, create |

Top similarity neighbours: `public-obsidian-obsidian-cli` (0.658), `public-mattpocock-obsidian-vault` (0.537), `public-obsidian-obsidian-markdown` (0.475), `public-office-obsidian-automation` (0.431), `public-obsidian-obsidian-bases` (0.428)

### `public_gold_p73_excel_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-excel-automation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 21

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-sheets-automation` | 0.3416 | 0.4223 | 0.6111 | yes | google, sheet, data | - |
| `public-office-data-analysis` | 0.3416 | 0.5043 | 0.5948 | yes | excel, analysi, data | - |

Top similarity neighbours: `xlsx-formula-model-builder` (0.606), `data-analysis-overview` (0.514), `public-office-data-analysis` (0.504), `spreadsheet-formula-auditor` (0.503), `data-analysis-for-reporting` (0.463)

### `public_gold_p74_sheets_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-sheets-automation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | 0.5691 | 0.4400 | 0.6749 | yes | excel | data, report |
| `public-office-data-pipeline` | 0.5691 | 0.4074 | 0.7034 | yes | workflow | automation, workflow, data, integration |

Top similarity neighbours: `xlsx-formula-model-builder` (0.707), `public-xlsx` (0.570), `public-office-sheets-automation` (0.569), `public-swebench-xlsx` (0.557), `public-office-xlsx-manipulation` (0.509)

### `public_gold_p75_airtable_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-airtable-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | 0.5773 | 0.2915 | 0.6615 | yes | automation, notion, workflow | automation, database, integration, workflow |
| `public-office-crm-automation` | 0.5773 | 0.3529 | 0.6067 | yes | automation, crm, workflow | automation, workflow |
| `public-office-sheets-automation` | 0.5773 | 0.2711 | 0.6410 | yes | automation, workflow | automation, integration, workflow |

Top similarity neighbours: `airtable-workflow-automator` (0.619), `public-office-airtable-automation` (0.577), `public-office-webhook-automation` (0.362), `public-office-crm-automation` (0.353), `public-office-podcast-automation` (0.342)

### `public_gold_p76_invoice_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-invoice-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-invoice-organizer` | 0.6589 | 0.4625 | 0.7035 | yes | invoice | invoice, track |
| `public-office-quickbooks-automation` | 0.6589 | 0.5644 | 0.7754 | yes | automate, workflow | automate, reconciliation, account |
| `public-office-expense-report` | 0.6589 | 0.1617 | 0.5053 | yes | - | - |

Top similarity neighbours: `public-office-invoice-automation` (0.659), `public-office-invoice-generator` (0.565), `public-office-quickbooks-automation` (0.564), `invoice-payment-checker` (0.549), `public-office-invoice-template` (0.507)

### `public_gold_p77_lead_routing`

- Family: `public_gold_validation`
- Gold skill: `public-office-lead-routing`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-lead-qualification` | 0.5479 | 0.3747 | 0.5100 | yes | lead, bas, qualify | lead |
| `public-office-lead-research` | 0.5479 | 0.4468 | 0.4818 | no | sale, company, research | - |
| `public-office-crm-automation` | 0.5479 | 0.2523 | 0.5203 | yes | lead | lead |
| `public-office-pipedrive-automation` | 0.5479 | 0.2659 | 0.4034 | no | sale | - |

Top similarity neighbours: `public-office-lead-routing` (0.548), `public-office-lead-research` (0.447), `public-office-amazon-seller` (0.419), `sales-ops-summary-writer` (0.410), `ecommerce-ops-summary-writer` (0.401)

### `public_gold_p78_saas_metrics`

- Family: `public_gold_validation`
- Gold skill: `public-office-saas-metrics`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-dcf-valuation` | 0.7300 | 0.5340 | 0.4875 | no | calculate, build, dcf, valuation, report | report |
| `public-office-financial-modeling` | 0.7300 | 0.3171 | 0.5137 | yes | build | - |
| `public-office-stock-analysis` | 0.7300 | 0.3083 | 0.5582 | yes | metric, stock, analysi, report | analysi, metric, report |
| `public-office-data-analysis` | 0.7300 | 0.2397 | 0.5031 | yes | build, analysi, report | analysi, report |

Top similarity neighbours: `public-office-saas-metrics` (0.730), `public-office-subscription-management` (0.576), `public-office-dcf-valuation` (0.534), `public-swebench-risk-metrics-calculation` (0.427), `public-swebench-creating-financial-models` (0.378)

### `public_gold_p79_stock_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-stock-analysis`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-dcf-valuation` | 0.5550 | 0.4723 | 0.4347 | yes | valuation, report, build, dcf | generate, report |
| `public-office-investment-memo` | 0.5550 | 0.3591 | 0.5750 | yes | risk, investment, write | market, investment |
| `public-office-crypto-report` | 0.5550 | 0.5575 | 0.5277 | yes | analysi, crypto, report | analysi, market, generate, report, metric |
| `public-office-company-research` | 0.5550 | 0.3409 | 0.6146 | yes | analysi | analysi, market |

Top similarity neighbours: `public-office-crypto-report` (0.557), `public-office-stock-analysis` (0.555), `public-office-dcf-valuation` (0.472), `finance-ops-summary-writer` (0.442), `public-office-saas-metrics` (0.421)

### `public_gold_p80_dcf_valuation`

- Family: `public_gold_validation`
- Gold skill: `public-office-dcf-valuation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-stock-analysis` | 0.6991 | 0.3734 | 0.4347 | no | stock | generate, report |
| `public-office-financial-modeling` | 0.6991 | 0.3923 | 0.5571 | yes | build | build, cash, flow, model |
| `public-office-investment-memo` | 0.6991 | 0.4292 | 0.4982 | no | write | professional |
| `public-swebench-creating-financial-models` | 0.6991 | 0.4737 | 0.5933 | yes | dcf, sensitivity | dcf, model |

Top similarity neighbours: `public-office-dcf-valuation` (0.699), `public-swebench-creating-financial-models` (0.474), `public-office-investment-memo` (0.429), `finance-ops-summary-writer` (0.406), `public-office-financial-modeling` (0.392)

### `public_gold_p81_shopify_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-shopify-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-woocommerce-automation` | 0.6106 | 0.5315 | 0.7484 | yes | automate, order, includ, customer, operation, woocommerce | e-commerce, inventory, order, customer |
| `public-office-stripe-payments` | 0.6106 | 0.3089 | 0.5549 | yes | automate, stripe, payment | management, process |
| `public-office-amazon-seller` | 0.6106 | 0.3826 | 0.6546 | yes | automate, order, includ, operation, amazon, seller | inventory, management, order |
| `public-office-invoice-automation` | 0.6106 | 0.3649 | 0.6164 | yes | automate, payment | - |

Top similarity neighbours: `public-office-shopify-automation` (0.611), `public-office-woocommerce-automation` (0.531), `public-office-spotify-automation` (0.442), `ecommerce-ops-monitoring-plan-builder` (0.420), `public-office-crm-automation` (0.419)

### `public_gold_p82_zendesk_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-zendesk-automation`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-intercom-automation` | 0.6884 | 0.4955 | 0.5107 | yes | automate, support, intercom | automate, customer, support, workflow |
| `public-office-customer-success` | 0.6884 | 0.2139 | 0.3447 | no | - | customer, management |
| `public-office-email-classifier` | 0.6884 | 0.2775 | 0.3070 | no | email | - |
| `public-office-slack-workflows` | 0.6884 | 0.4288 | 0.4485 | no | slack, automation | workflow |
| `support-ticket-triager` | 0.6884 | 0.4020 | 0.4560 | no | ticket, support | support, ticket, rout |
| `support-ops-monitoring-plan-builder` | 0.6884 | 0.3677 | 0.4617 | no | escalation, support, build | customer, support |

Top similarity neighbours: `public-office-zendesk-automation` (0.688), `public-office-intercom-automation` (0.495), `webhook-integration-planner` (0.452), `public-office-obsidian-automation` (0.444), `webhook-setup-planner` (0.442)

