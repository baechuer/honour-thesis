# Semantic Confusability Report

This report implements Step 3 of the benchmark rubric: listed alternatives and recorded acceptable equivalents should be semantically plausible neighbours, not random unrelated distractors.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.

## Overall Status

- Step 3 status: **PASS**
- Prompts with at least two plausible listed alternatives: 116/120 (96.7%)
- Gold/alternative pairs marked plausible: 382/517 (73.9%)
- Gold skill ranked top-1 among all skills by this backend: 67/120 (55.8%)

Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, whose skill card is similar to the gold skill card, or whose acceptable-equivalent status has already been manually recorded.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |
|---|---:|---:|---:|
| public_gold_validation | 120 | 116/120 | 67/120 |

## Weak Semantic-Confusability Prompts

| Prompt | Gold | Plausible alternatives | Gold all-skill rank |
|---|---|---:|---:|
| `public_gold_p90_claude_api` | `public-anthropic-claude-api` | 1 | 1 |
| `public_gold_p91_admin_api_endpoint` | `public-swebench-add-admin-api-endpoint` | 0 | 1 |
| `public_gold_p94_security_ownership_map` | `public-openai-security-ownership-map` | 0 | 1 |
| `public_gold_p111_docusign_automation` | `public-office-docusign-automation` | 1 | 1 |

## Prompt Detail

### `public_gold_p01_pdf_extraction`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-extraction`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-chat-with-pdf` | no | 0.6611 | 0.4052 | 0.6329 | yes | extract, pdf, answer | extract |
| `public-office-pdf-ocr` | no | 0.6611 | 0.4545 | 0.7114 | yes | extract, text, scann | extract, text, pdfs |
| `public-office-pdf-converter` | no | 0.6611 | 0.4849 | 0.7258 | yes | pdf, file, format, convert | - |
| `public-openai-pdf` | no | 0.6611 | 0.4408 | 0.6048 | yes | extract, pdf, page, file | extract, pdfplumber |

Top similarity neighbours: `public-office-pdf-extraction` (0.661), `pdf-layout-table-extractor` (0.585), `psc-pdf-native-extraction-pack` (0.565), `implicit-pdf-table-reconstructor` (0.522), `document-field-extractor` (0.501)

### `public_gold_p02_pdf_ocr`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-ocr`
- Plausible listed alternatives: 5
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-pdf-extraction` | no | 0.6261 | 0.4848 | 0.7114 | yes | text | extract, text, pdfs |
| `public-office-chat-with-pdf` | no | 0.6261 | 0.4575 | 0.5920 | yes | pdf | extract |
| `public-office-pdf-converter` | no | 0.6261 | 0.5468 | 0.7035 | yes | pdf, convert, word | - |
| `public-openai-pdf` | no | 0.6261 | 0.4188 | 0.5512 | yes | pdf, page | extract |
| `pdf-ocr-cleaner` | yes | 0.6261 | 0.7211 | 0.6862 | yes | ocr, recover, text, mark, region, page | text, scann, pdfs |

Top similarity neighbours: `pdf-ocr-cleaner` (0.721), `pdf-ocr-extractor` (0.675), `psc-pdf-scan-ocr-recovery` (0.630), `public-office-pdf-ocr` (0.626), `public-pdf` (0.549)

### `public_gold_p03_pdf_form_filler`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-form-filler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-pdf-extraction` | no | 0.4936 | 0.3492 | 0.6703 | yes | extract | extract |
| `public-office-pdf-converter` | no | 0.4936 | 0.2822 | 0.6727 | yes | pdf, convert | pdf |
| `public-office-template-engine` | no | 0.4936 | 0.4067 | 0.4651 | no | data, document, template | data |
| `pdf-form-filler` | yes | 0.4936 | 0.5389 | 0.6335 | yes | pdf, fill, form, field, requir, miss | form, fill, pdf |

Top similarity neighbours: `pdf-form-filler` (0.539), `public-office-pdf-form-filler` (0.494), `public-office-form-builder` (0.435), `public-office-expense-tracker` (0.434), `public-office-financial-modeling` (0.428)

### `public_gold_p04_markitdown_conversion`

- Family: `public_gold_validation`
- Gold skill: `public-markitdown`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | no | 0.6850 | 0.6605 | 0.7194 | yes | file, markdown, convert, mix | convert, file, document, markdown |
| `public-office-pdf-converter` | no | 0.6850 | 0.4717 | 0.5891 | yes | file, convert, pdf, image | convert, file, pdf, image |
| `public-office-batch-convert` | no | 0.6850 | 0.4333 | 0.4842 | no | pipeline, convert | convert, document |
| `public-office-doc-parser` | no | 0.6850 | 0.3333 | 0.5310 | yes | - | - |

Top similarity neighbours: `public-markitdown` (0.685), `office-to-markdown-converter` (0.660), `document-converter` (0.506), `pdf-to-docx-converter` (0.503), `layout-preserving-converter` (0.482)

### `public_gold_p05_pdf_merge_split`

- Family: `public_gold_validation`
- Gold skill: `public-office-pdf-merge-split`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-pdf-converter` | no | 0.4820 | 0.3483 | 0.6813 | yes | file, convert | file |
| `public-office-pdf-watermark` | no | 0.4820 | 0.4388 | 0.5073 | yes | pdfs, page, watermark | pdfs |
| `public-office-pdf-compress` | no | 0.4820 | 0.2751 | 0.5893 | yes | file | file |
| `public-openai-pdf` | no | 0.4820 | 0.3253 | 0.4788 | no | page, file | file |

Top similarity neighbours: `public-office-pdf-merge-split` (0.482), `public-office-pdf-watermark` (0.439), `pdf-layout-table-extractor` (0.417), `psc-pdf-evidence-qa` (0.405), `public-office-invoice-template` (0.401)

### `public_gold_p06_browser_devtools_testing`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-browser-testing-with-devtools`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-playwright` | no | 0.6135 | 0.4549 | 0.5324 | yes | screenshot, script | real, browser, via, debug, data, require |
| `public-playwright-interactive` | no | 0.6135 | 0.5028 | 0.5574 | yes | - | browser, debug |
| `public-office-browser-automation` | no | 0.6135 | 0.4769 | 0.5800 | yes | playwright | browser, test |
| `public-anthropic-webapp-testing` | no | 0.6135 | 0.5150 | 0.6494 | yes | local, screenshot, playwright | browser, test, debug, check |

Top similarity neighbours: `public-addy-agent-browser-testing-with-devtools` (0.614), `psc-playwright-regression-suite` (0.574), `playwright-flow-debugger` (0.571), `public-anthropic-webapp-testing` (0.515), `psc-devtools-runtime-diagnoser` (0.510)

### `public_gold_p07_web_accessibility`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-accessibility`
- Plausible listed alternatives: 5
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-web-quality-audit` | no | 0.6228 | 0.3519 | 0.6057 | yes | audit, page, seo, performance | audit, accessibility, web, ask |
| `public-addy-web-core-web-vitals` | no | 0.6228 | 0.3316 | 0.4420 | no | page | improve, web, ask |
| `public-addy-web-best-practices` | no | 0.6228 | 0.2675 | 0.5311 | yes | audit | audit, web, ask |
| `public-oh-my-web-accessibility` | yes | 0.6228 | 0.1989 | 0.6075 | yes | - | - |
| `accessibility-checker` | yes | 0.6228 | 0.3964 | 0.5852 | yes | keyboard, label, focu, order, contrast, screen-reader, semantic | accessibility, web, keyboard |
| `accessibility-interaction-auditor` | yes | 0.6228 | 0.5334 | 0.6544 | yes | audit, keyboard, navigation, focu, order, contrast | audit, accessibility, web, keyboard, navigation, accessible |

Top similarity neighbours: `public-addy-web-accessibility` (0.623), `accessibility-interaction-auditor` (0.533), `psc-accessibility-interaction-auditor` (0.474), `visual-regression-checker` (0.428), `accessibility-checker` (0.396)

### `public_gold_p08_core_web_vitals`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-core-web-vitals`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | no | 0.6231 | 0.3525 | 0.4420 | no | web, accessibility | web, ask, improve |
| `public-addy-web-best-practices` | no | 0.6231 | 0.3723 | 0.6158 | yes | web, review | web, ask |
| `public-addy-web-performance` | no | 0.6231 | 0.4443 | 0.6495 | yes | web | optimize, web, page, experience, fix, better, ask, improve |
| `public-addy-agent-browser-testing-with-devtools` | no | 0.6231 | 0.3998 | 0.3702 | no | browser | - |

Top similarity neighbours: `public-addy-web-core-web-vitals` (0.623), `psc-devtools-runtime-diagnoser` (0.510), `web-performance-budget-checker` (0.497), `psc-accessibility-interaction-auditor` (0.465), `psc-visual-screenshot-reviewer` (0.445)

### `public_gold_p09_systematic_debugging`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-debugging`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 171

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-agent-code-simplification` | no | 0.2006 | 0.0924 | 0.4312 | no | code, review | - |
| `public-oh-my-code-review` | no | 0.2006 | 0.0960 | 0.7561 | yes | - | - |
| `public-addy-agent-code-review-and-quality` | no | 0.2006 | 0.0976 | 0.4408 | no | code, change, review, quality | - |
| `public-openai-gh-fix-ci` | no | 0.2006 | 0.2676 | 0.5517 | yes | debug, failure, fix, inspect, github | - |
| `public-addy-agent-debugging-and-error-recovery` | yes | 0.2006 | 0.3496 | 0.5549 | yes | debug, build, fix | - |

Top similarity neighbours: `ci-failure-debugger` (0.496), `localization-ops-failure-diagnoser` (0.481), `api-ops-failure-diagnoser` (0.452), `implicit-ci-failure-reader` (0.435), `ci-log-root-cause-debugger` (0.422)

### `public_gold_p100_teams_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-microsoft-teams`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-slack-workflows` | no | 0.7249 | 0.5086 | 0.6552 | yes | workflow, notification, slack | workflow, integration |
| `public-office-calendar-automation` | no | 0.7249 | 0.5376 | 0.6001 | yes | meet, workflow, slack, calendar, schedul | workflow, integration |
| `public-office-meeting-notes` | no | 0.7249 | 0.2208 | 0.6019 | yes | - | - |
| `public-office-office-mcp` | no | 0.7249 | 0.3130 | 0.4768 | no | mcp, operation | - |

Top similarity neighbours: `public-office-microsoft-teams` (0.725), `public-office-calendar-automation` (0.538), `public-office-slack-workflows` (0.509), `groupwork-reply` (0.500), `public-office-clickup-automation` (0.489)

### `public_gold_p101_twilio_sms`

- Family: `public_gold_validation`
- Gold skill: `public-office-twilio-sms`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-whatsapp-automation` | no | 0.7633 | 0.4905 | 0.6271 | yes | automation, notification, whatsapp | messag, notification |
| `public-office-telegram-bot` | no | 0.7633 | 0.4639 | 0.5770 | yes | automation, notification, telegram | notification |
| `public-office-slack-workflows` | no | 0.7633 | 0.3955 | 0.4933 | no | automation, notification, workflow, slack | notification, workflow |
| `public-office-email-drafter` | no | 0.7633 | 0.0520 | 0.3521 | no | - | - |

Top similarity neighbours: `public-office-twilio-sms` (0.763), `public-office-whatsapp-automation` (0.490), `public-office-telegram-bot` (0.464), `public-office-slack-workflows` (0.396), `public-office-intercom-automation` (0.383)

### `public_gold_p102_webhook_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-webhook-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `webhook-contract-planner` | no | 0.8202 | 0.6685 | 0.6091 | yes | webhook, event, receiver, signature, contract | event |
| `api-integration-planner` | no | 0.8202 | 0.4876 | 0.5092 | yes | endpoint, api, failure, plan | api |
| `external-api-integration-planner` | no | 0.8202 | 0.4199 | 0.4271 | no | endpoint, api, failure, integration, plan | integration, api |
| `webhook-integration-planner` | yes | 0.8202 | 0.7153 | 0.6843 | yes | webhook, event, signature, plan | event |

Top similarity neighbours: `public-office-webhook-automation` (0.820), `webhook-setup-planner` (0.736), `webhook-integration-planner` (0.715), `webhook-contract-planner` (0.668), `api-integration-planner` (0.488)

### `public_gold_p103_mailchimp_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-mailchimp-automation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-social-publisher` | no | 0.7990 | 0.4676 | 0.5438 | yes | automation, publish, social, post | automation |
| `public-office-ads-copywriter` | no | 0.7990 | 0.3147 | 0.3855 | no | copy | - |
| `public-office-email-drafter` | no | 0.7990 | 0.2541 | 0.4781 | no | - | - |
| `public-office-linkedin-automation` | no | 0.7990 | 0.3473 | 0.5468 | yes | automate, publish | automate, market |

Top similarity neighbours: `public-office-mailchimp-automation` (0.799), `public-office-email-marketing` (0.629), `public-office-twitter-automation` (0.510), `email-ops-monitoring-plan-builder` (0.509), `email-ops-scenario-planner` (0.490)

### `public_gold_p104_social_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-office-social-publisher`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-linkedin-automation` | no | 0.7608 | 0.5755 | 0.6821 | yes | publish, automate, linkedin | publish, content, linkedin |
| `public-office-twitter-automation` | no | 0.7608 | 0.5380 | 0.7552 | yes | post, social, automate, twitter | social, media, post |
| `public-office-youtube-automation` | no | 0.7608 | 0.3990 | 0.5506 | yes | automate, youtube | content, youtube |
| `public-office-tiktok-marketing` | no | 0.7608 | 0.4017 | 0.5983 | yes | post, tiktok | automation, post, content, tiktok |

Top similarity neighbours: `public-office-social-publisher` (0.761), `public-office-linkedin-automation` (0.576), `public-office-twitter-automation` (0.538), `social-post-planner` (0.521), `social-ops-resource-linker` (0.490)

### `public_gold_p105_youtube_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-youtube-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-social-publisher` | no | 0.7078 | 0.5101 | 0.5506 | yes | youtube, publish, schedule, content, tiktok | youtube, content |
| `public-office-tiktok-marketing` | no | 0.7078 | 0.5729 | 0.4942 | no | workflow, video, analytic, content, tiktok | content, workflow, video, analytic, optimization |
| `public-office-podcast-automation` | no | 0.7078 | 0.5315 | 0.6433 | yes | automate, workflow, publish, podcast, production | automate, workflow, includ |
| `public-office-transcription-automation` | no | 0.7078 | 0.3881 | 0.5768 | yes | automate, video, content, transcription | automate, content, video |

Top similarity neighbours: `public-office-youtube-automation` (0.708), `public-office-tiktok-marketing` (0.573), `public-office-podcast-automation` (0.531), `public-office-social-publisher` (0.510), `public-office-twitter-automation` (0.403)

### `public_gold_p106_google_ads_manager`

- Family: `public_gold_validation`
- Gold skill: `public-office-google-ads-manager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-facebook-ads` | no | 0.6514 | 0.4429 | 0.6870 | yes | campaign, performance, optimization, facebook | campaign, optimization, performance |
| `public-office-ads-copywriter` | no | 0.6514 | 0.4567 | 0.5145 | yes | ads, google, copy, meta, facebook | google, ads |
| `public-office-seo-optimizer` | no | 0.6514 | 0.2923 | 0.6370 | yes | keyword, optimization, seo | keyword, research, optimization |
| `public-office-social-publisher` | no | 0.6514 | 0.3390 | 0.4695 | no | - | - |

Top similarity neighbours: `public-office-google-ads-manager` (0.651), `ads-ops-summary-writer` (0.487), `ads-ops-dependency-mapper` (0.459), `public-office-ads-copywriter` (0.457), `ads-ops-quality-auditor` (0.455)

### `public_gold_p107_proposal_writer`

- Family: `public_gold_validation`
- Gold skill: `public-office-proposal-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-investment-memo` | no | 0.5472 | 0.5559 | 0.6946 | yes | write, investment | - |
| `public-office-report-generator` | no | 0.5472 | 0.1500 | 0.3998 | no | report | - |
| `public-office-content-writer` | no | 0.5472 | 0.2550 | 0.5826 | yes | write | - |
| `public-office-contract-template` | no | 0.5472 | 0.1446 | 0.4658 | no | - | - |

Top similarity neighbours: `public-office-investment-memo` (0.556), `public-office-proposal-writer` (0.547), `proposal-drafter` (0.476), `vendor-ops-scenario-planner` (0.404), `vendor-ops-summary-writer` (0.396)

### `public_gold_p108_report_generator`

- Family: `public_gold_validation`
- Gold skill: `public-office-report-generator`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | no | 0.6711 | 0.5914 | 0.7149 | yes | data, generate, report, spreadsheet, analysi | generate, data, report, visualization |
| `public-office-chart-designer` | no | 0.6711 | 0.6107 | 0.6878 | yes | data, chart, generate, report, design | generate, data, report, chart, visualization |
| `public-office-weekly-report` | no | 0.6711 | 0.2150 | 0.6249 | yes | - | - |
| `public-office-infographic` | no | 0.6711 | 0.3934 | 0.5351 | yes | data, design, infographic, layout | data |

Top similarity neighbours: `public-office-report-generator` (0.671), `public-office-chart-designer` (0.611), `data-analysis-for-reporting` (0.598), `data-analysis-overview` (0.596), `public-office-data-analysis` (0.591)

### `public_gold_p109_job_description`

- Family: `public_gold_validation`
- Gold skill: `public-office-job-description`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 307

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-offer-letter` | no | 0.2743 | 0.3866 | 0.6524 | yes | letter, compensation, offer | - |
| `public-office-applicant-screening` | no | 0.2743 | 0.3155 | 0.6642 | yes | job, screen, candidate | - |
| `public-office-resume-tailor` | no | 0.2743 | 0.2888 | 0.8740 | yes | - | - |
| `public-office-cover-letter` | no | 0.2743 | 0.1917 | 0.8552 | yes | - | - |

Top similarity neighbours: `recruiting-ops-summary-writer` (0.488), `recruiting-ops-handoff-brief-writer` (0.481), `recruiting-ops-rewrite-editor` (0.441), `recruiting-ops-compliance-checker` (0.436), `proposal-drafter` (0.429)

### `public_gold_p10_analyze_ci`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-analyze-ci`
- Plausible listed alternatives: 6
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-github-actions-templates` | no | 0.5643 | 0.4254 | 0.4871 | no | github, action, workflow, template | github, action |
| `public-addy-agent-ci-cd-and-automation` | no | 0.5643 | 0.2980 | 0.2927 | no | - | - |
| `public-oh-my-debugging` | no | 0.5643 | 0.2267 | 0.5074 | yes | - | - |
| `pr-reviewer` | no | 0.5643 | 0.5498 | 0.4924 | yes | github, identify | github, extract, request |
| `repo-ops-failure-diagnoser` | no | 0.5643 | 0.5253 | 0.4503 | yes | fail, workflow | fail |
| `public-openai-gh-fix-ci` | yes | 0.5643 | 0.4955 | 0.5464 | yes | fail, github, action, logs, debug | fail, github, action |
| `ci-failure-debugger` | yes | 0.5643 | 0.7283 | 0.4358 | yes | fail, logs, workflow | fail |
| `ci-log-root-cause-debugger` | yes | 0.5643 | 0.5989 | 0.3414 | yes | fail, logs | fail |

Top similarity neighbours: `ci-failure-debugger` (0.728), `psc-ci-log-first-failure-reader` (0.696), `ci-log-root-cause-debugger` (0.599), `public-swebench-analyze-ci` (0.564), `pr-reviewer` (0.550)

### `public_gold_p110_offer_letter`

- Family: `public_gold_validation`
- Gold skill: `public-office-offer-letter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-job-description` | no | 0.5809 | 0.2569 | 0.6524 | yes | - | - |
| `public-office-contract-template` | no | 0.5809 | 0.1441 | 0.5062 | yes | - | - |
| `public-office-nda-generator` | no | 0.5809 | 0.1627 | 0.4495 | no | - | - |
| `public-office-hr-automation` | no | 0.5809 | 0.3293 | 0.5009 | yes | - | - |

Top similarity neighbours: `public-office-offer-letter` (0.581), `contract-ops-summary-writer` (0.466), `terms-of-service-drafter` (0.447), `recruiting-ops-handoff-brief-writer` (0.443), `public-office-contract-review` (0.441)

### `public_gold_p111_docusign_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-docusign-automation`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-contract-template` | no | 0.7084 | 0.2189 | 0.4594 | no | - | - |
| `public-office-nda-generator` | no | 0.7084 | 0.2246 | 0.4390 | no | - | - |
| `public-office-invoice-automation` | no | 0.7084 | 0.4168 | 0.5917 | yes | automate, track, invoice | automate |
| `public-office-form-builder` | no | 0.7084 | 0.4532 | 0.4939 | no | form | document |

Top similarity neighbours: `public-office-docusign-automation` (0.708), `api-documentation-writer` (0.505), `public-anthropic-doc-coauthoring` (0.503), `docx-redline-editor` (0.501), `public-docx` (0.491)

### `public_gold_p112_expense_tracker`

- Family: `public_gold_validation`
- Gold skill: `public-office-expense-tracker`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-expense-report` | no | 0.6413 | 0.3249 | 0.6980 | yes | - | - |
| `public-office-quickbooks-automation` | no | 0.6413 | 0.6237 | 0.6983 | yes | expense, workflow, report, quickbook, account | automate, expense, workflow |
| `public-office-invoice-organizer` | no | 0.6413 | 0.4806 | 0.7028 | yes | receipt, organize, invoice | track, receipt |
| `public-office-invoice-automation` | no | 0.6413 | 0.4554 | 0.7059 | yes | invoice, account | automate, track |

Top similarity neighbours: `public-office-expense-tracker` (0.641), `public-office-quickbooks-automation` (0.624), `expense-categoriser` (0.488), `public-office-invoice-organizer` (0.481), `receipt-extractor` (0.478)

### `public_gold_p113_quickbooks_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-quickbooks-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-invoice-automation` | no | 0.7670 | 0.5508 | 0.7754 | yes | invoice, automate, account, reconciliation, payment | automate, account, reconciliation |
| `public-office-expense-tracker` | no | 0.7670 | 0.4205 | 0.6983 | yes | workflow, automate, expense | automate, workflow, expense |
| `public-office-stripe-payments` | no | 0.7670 | 0.5220 | 0.6342 | yes | report, automate, financial, stripe, payment | automate, invoic, report |
| `public-office-saas-metrics` | no | 0.7670 | 0.3548 | 0.4650 | no | report, saas, metric | report |

Top similarity neighbours: `public-office-quickbooks-automation` (0.767), `public-office-invoice-automation` (0.551), `public-office-stripe-payments` (0.522), `spreadsheet-formula-auditor` (0.486), `invoice-payment-checker` (0.454)

### `public_gold_p114_stripe_payments`

- Family: `public_gold_validation`
- Gold skill: `public-office-stripe-payments`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-subscription-management` | no | 0.6761 | 0.3465 | 0.6480 | yes | subscription, bill, lifecycle | subscription, management |
| `public-office-invoice-automation` | no | 0.6761 | 0.5052 | 0.7274 | yes | automate, payment, invoice, account | automate, payment |
| `public-office-shopify-automation` | no | 0.6761 | 0.4390 | 0.5549 | yes | process, shopify, order | process, management |
| `public-office-quickbooks-automation` | no | 0.6761 | 0.5387 | 0.6342 | yes | automate, report, quickbook, account | automate, invoic, report |

Top similarity neighbours: `public-office-stripe-payments` (0.676), `public-office-quickbooks-automation` (0.539), `public-office-invoice-automation` (0.505), `invoice-payment-checker` (0.457), `public-office-shopify-automation` (0.439)

### `public_gold_p115_subscription_management`

- Family: `public_gold_validation`
- Gold skill: `public-office-subscription-management`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-saas-metrics` | no | 0.6716 | 0.5238 | 0.6892 | yes | saas, metric | saas, churn |
| `public-office-stripe-payments` | no | 0.6716 | 0.5044 | 0.6480 | yes | subscription, stripe, payment | subscription, management |
| `public-office-customer-success` | no | 0.6716 | 0.3431 | 0.6237 | yes | playbook, retention | management |
| `public-office-invoice-automation` | no | 0.6716 | 0.3062 | 0.5477 | yes | payment | - |

Top similarity neighbours: `public-office-subscription-management` (0.672), `public-office-saas-metrics` (0.524), `public-office-stripe-payments` (0.504), `churn-risk-analyser` (0.422), `procurement-ops-monitoring-plan-builder` (0.376)

### `public_gold_p116_transcription_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-transcription-automation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-transcribe` | no | 0.7412 | 0.5097 | 0.6595 | yes | audio, video, speaker, label | audio, video |
| `public-office-meeting-notes` | no | 0.7412 | 0.2344 | 0.4927 | no | - | - |
| `public-office-podcast-automation` | no | 0.7412 | 0.4817 | 0.6378 | yes | automate | automate |
| `public-markitdown` | no | 0.7412 | 0.4280 | 0.4738 | no | audio, transcription, convert, document, markdown, ocr, image | audio, transcription |
| `public-office-smart-ocr` | no | 0.7412 | 0.2167 | 0.4970 | no | - | - |

Top similarity neighbours: `public-office-transcription-automation` (0.741), `public-openai-transcribe` (0.510), `public-office-podcast-automation` (0.482), `speaker-notes-writer` (0.448), `meeting-notes-action-extractor` (0.438)

### `public_gold_p117_podcast_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-podcast-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-transcription-automation` | no | 0.7608 | 0.4898 | 0.6378 | yes | automate, note, audio, video | automate |
| `public-office-youtube-automation` | no | 0.7608 | 0.5334 | 0.6433 | yes | automate, workflow, youtube, video | automate, workflow, includ |
| `public-office-spotify-automation` | no | 0.7608 | 0.3880 | 0.6285 | yes | automate, workflow, audio | automate, workflow |
| `public-office-social-publisher` | no | 0.7608 | 0.3676 | 0.5004 | yes | publish, youtube, social | publish |

Top similarity neighbours: `public-office-podcast-automation` (0.761), `public-office-youtube-automation` (0.533), `public-office-transcription-automation` (0.490), `public-office-spotify-automation` (0.388), `public-swebench-changelog-automation` (0.388)

### `public_gold_p118_news_monitor`

- Family: `public_gold_validation`
- Gold skill: `public-office-news-monitor`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-web-search` | no | 0.7169 | 0.3844 | 0.5916 | yes | search, web | analysi, strategie, synthesize |
| `public-office-academic-search` | no | 0.7169 | 0.3768 | 0.5846 | yes | search, academic, paper, research | analysi, synthesize |
| `public-office-deep-research` | no | 0.7169 | 0.3867 | 0.5936 | yes | research, report | analysi, synthesize, report |
| `tech-news-trend-extractor` | no | 0.7169 | 0.6548 | 0.5887 | yes | news, trend | news |

Top similarity neighbours: `public-office-news-monitor` (0.717), `tech-news-trend-extractor` (0.655), `news-briefing-writer` (0.646), `news-summariser` (0.629), `journalism-ops-monitoring-plan-builder` (0.624)

### `public_gold_p119_data_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-analysis`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-report-generator` | no | 0.6529 | 0.4004 | 0.7149 | yes | data, chart, generate, report | data, generate, visualization, report |
| `public-office-chart-designer` | no | 0.6529 | 0.4046 | 0.5907 | yes | data, design, chart, generate, report | data, generate, create, visualization, report |
| `public-office-saas-metrics` | no | 0.6529 | 0.4764 | 0.5031 | yes | analysi, busines, saas, metric, report | analysi, report |
| `public-office-xlsx-manipulation` | no | 0.6529 | 0.2463 | 0.4536 | no | spreadsheet, manipulate, excel | spreadsheet, create, excel |

Top similarity neighbours: `data-analysis-for-reporting` (0.666), `data-analysis-overview` (0.654), `public-office-data-analysis` (0.653), `data-analysis-with-validation` (0.587), `psc-anomaly-watchlist-builder` (0.587)

### `public_gold_p11_setup_pre_commit`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-setup-pre-commit`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-repo-guardrail-hook-installer` | no | 0.7449 | 0.5178 | 0.5034 | yes | pre-commit, check, github, command | set, pre-commit, hook, check |
| `git-safety-guardrail-installer` | no | 0.7449 | 0.4602 | 0.3537 | no | commit, configure, dangerou, git, command | hook, configure |
| `public-mattpocock-git-guardrails-claude-code` | no | 0.7449 | 0.3687 | 0.4973 | no | add, block, dangerou, git, command | set, hook, add |
| `public-swebench-fix` | no | 0.7449 | 0.2504 | 0.4116 | no | - | formatt |
| `git-commit-writer` | no | 0.7449 | 0.4448 | 0.4476 | no | type, commit | type |
| `public-swebench-github-actions-templates` | no | 0.7449 | 0.4202 | 0.4720 | no | test, github, action | test |
| `public-oh-my-setup-pre-commit` | yes | 0.7449 | 0.3225 | 0.5589 | yes | - | - |

Top similarity neighbours: `public-mattpocock-setup-pre-commit` (0.745), `psc-repo-guardrail-hook-installer` (0.518), `psc-release-communication-packager` (0.467), `git-safety-guardrail-installer` (0.460), `git-commit-writer` (0.445)

### `public_gold_p120_xlsx_manipulation`

- Family: `public_gold_validation`
- Gold skill: `public-office-xlsx-manipulation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-sheets-automation` | no | 0.6854 | 0.4057 | 0.4584 | no | sheet, google | - |
| `public-office-data-analysis` | no | 0.6854 | 0.3950 | 0.4536 | no | create, analysi | create, excel, spreadsheet |
| `public-swebench-xlsx` | no | 0.6854 | 0.5749 | 0.6206 | yes | sheet, xlsx, create, formula, format, file, google | create, edit, spreadsheet |
| `public-office-excel-automation` | yes | 0.6854 | 0.3400 | 0.6282 | yes | - | - |

Top similarity neighbours: `public-office-xlsx-manipulation` (0.685), `public-swebench-xlsx` (0.575), `public-xlsx` (0.542), `xlsx-formula-model-builder` (0.534), `spreadsheet-formula-auditor` (0.431)

### `public_gold_p12_git_guardrails`

- Family: `public_gold_validation`
- Gold skill: `public-mattpocock-git-guardrails-claude-code`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-mattpocock-setup-pre-commit` | no | 0.7839 | 0.3923 | 0.4973 | no | hook, set, formatt | hook, set, add |
| `public-addy-agent-git-workflow-and-versioning` | no | 0.7839 | 0.4275 | 0.5196 | yes | git, code, branch, workflow | git, code, branch |
| `public-openai-yeet` | no | 0.7839 | 0.2564 | 0.4484 | no | flow | push |
| `version-control-helper` | no | 0.7839 | 0.4721 | 0.4769 | no | git, such, branch, workflow | git, branch |
| `public-swebench-github-actions-templates` | no | 0.7839 | 0.4263 | 0.4800 | no | workflow | - |
| `public-oh-my-git-guardrails-claude-code` | yes | 0.7839 | 0.5475 | 0.7356 | yes | - | - |

Top similarity neighbours: `public-mattpocock-git-guardrails-claude-code` (0.784), `git-safety-guardrail-installer` (0.714), `psc-repo-guardrail-hook-installer` (0.623), `public-oh-my-git-guardrails-claude-code` (0.547), `version-control-helper` (0.472)

### `public_gold_p13_address_pr_comments`

- Family: `public_gold_validation`
- Gold skill: `public-openai-gh-address-comments`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 13

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-gh-fix-ci` | no | 0.4452 | 0.4638 | 0.7495 | yes | github, inspect, report, debug, fail, check | github, check |
| `public-openai-yeet` | no | 0.4452 | 0.2444 | 0.7015 | yes | github, request | open, github, cli |
| `public-lbussell-creating-pull-requests` | no | 0.4452 | 0.2438 | 0.4126 | no | - | - |
| `public-lbussell-triaging-issues` | no | 0.4452 | 0.2586 | 0.3870 | no | - | - |

Top similarity neighbours: `pr-reviewer` (0.579), `pr-review-comment-resolver` (0.565), `review-comment-resolver` (0.531), `psc-ci-log-first-failure-reader` (0.512), `public-swebench-analyze-ci` (0.511)

### `public_gold_p14_netlify_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-netlify-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-vercel-deploy` | no | 0.7001 | 0.4486 | 0.5328 | yes | deploy, deployment, vercel | deploy, link, preview |
| `public-openai-cloudflare-deploy` | no | 0.7001 | 0.4258 | 0.5497 | yes | deploy, project, cloudflare | deploy, project, asks, host, publish |
| `public-openai-render-deploy` | no | 0.7001 | 0.4544 | 0.5343 | yes | deploy, render | deploy, host, publish |
| `public-oh-my-vercel-deploy` | no | 0.7001 | 0.2982 | 0.4725 | no | - | - |

Top similarity neighbours: `public-netlify-deploy` (0.700), `public-openai-render-deploy` (0.454), `public-openai-vercel-deploy` (0.449), `public-openai-cloudflare-deploy` (0.426), `deployment-release-verifier` (0.381)

### `public_gold_p15_cloudflare_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cloudflare-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-netlify-deploy` | no | 0.5601 | 0.4550 | 0.5497 | yes | publish, includ, netlify | deploy, asks, host, publish, project |
| `public-openai-vercel-deploy` | no | 0.5601 | 0.3073 | 0.6909 | yes | vercel | deploy, application |
| `public-openai-render-deploy` | no | 0.5601 | 0.3987 | 0.7215 | yes | publish, platform, render | deploy, application, platform, host, publish, set |
| `public-swebench-k8s-manifest-generator` | no | 0.5601 | 0.3544 | 0.4674 | no | kubernete, manifest | service |

Top similarity neighbours: `public-openai-cloudflare-deploy` (0.560), `public-netlify-deploy` (0.455), `public-openai-render-deploy` (0.399), `cloud-ops-evidence-grounder` (0.361), `cloud-ops-resource-linker` (0.358)

### `public_gold_p16_render_deploy`

- Family: `public_gold_validation`
- Gold skill: `public-openai-render-deploy`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-netlify-deploy` | no | 0.7120 | 0.5455 | 0.5343 | yes | repo, deploy, netlify | deploy, host, publish |
| `public-openai-vercel-deploy` | no | 0.7120 | 0.4534 | 0.7205 | yes | deployment, deploy, vercel | deploy, application |
| `public-openai-cloudflare-deploy` | no | 0.7120 | 0.4484 | 0.7215 | yes | service, deploy, cloudflare | deploy, application, host, publish, set, platform |
| `public-swebench-k8s-manifest-generator` | no | 0.7120 | 0.4760 | 0.4988 | no | deployment, service, generat, yaml, kubernete | generat, yaml |

Top similarity neighbours: `public-openai-render-deploy` (0.712), `public-netlify-deploy` (0.545), `public-swebench-k8s-manifest-generator` (0.476), `k8s-ops-artifact-packager` (0.464), `kubernetes-deployment-helper` (0.456)

### `public_gold_p17_mcp_builder`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-mcp-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-api-design-principles` | no | 0.6014 | 0.2490 | 0.4096 | no | design, api | build, apis |
| `public-office-mcp-hub` | no | 0.6014 | 0.4304 | 0.5815 | yes | tool, mcp | mcp, model, context, protocol, tool |
| `public-openai-chatgpt-apps` | no | 0.6014 | 0.3819 | 0.4351 | no | tool, mcp, design, server | mcp, server, tool, build, apis, sdk |
| `webhook-integration-planner` | no | 0.6014 | 0.5363 | 0.4266 | yes | - | - |
| `mcp-server-builder` | yes | 0.6014 | 0.6406 | 0.6958 | yes | tool, mcp, server | mcp, server, tool, build |

Top similarity neighbours: `mcp-server-builder` (0.641), `public-anthropic-mcp-builder` (0.601), `public-swebench-mcp-builder` (0.587), `auth-flow-integrator` (0.574), `api-security-threat-reviewer` (0.567)

### `public_gold_p18_chatgpt_apps`

- Family: `public_gold_validation`
- Gold skill: `public-openai-chatgpt-apps`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-anthropic-mcp-builder` | no | 0.7777 | 0.4676 | 0.4351 | no | mcp, server, build, sdk | mcp, sdk, tool, build, server, apis |
| `public-openai-cli-creator` | no | 0.7777 | 0.2403 | 0.5055 | yes | app, build, sdk, cli | sdk, tool, build, codex, docs |
| `public-openai-openai-docs` | no | 0.7777 | 0.2282 | 0.5980 | yes | mcp, build, need | mcp, tool, build, need, apis, domain, openai, docs |
| `public-office-ai-agent-builder` | no | 0.7777 | 0.3022 | 0.4342 | no | build, chatgpt | chatgpt, tool, build |

Top similarity neighbours: `public-openai-chatgpt-apps` (0.778), `public-swebench-mcp-builder` (0.491), `mcp-server-builder` (0.475), `public-anthropic-mcp-builder` (0.468), `public-mattpocock-to-prd` (0.369)

### `public_gold_p19_cli_creator`

- Family: `public_gold_validation`
- Gold skill: `public-openai-cli-creator`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-openai-docs` | no | 0.7326 | 0.4475 | 0.6761 | yes | docs, build, documentation, only, mcp | tool, build, docs |
| `public-obsidian-obsidian-cli` | no | 0.7326 | 0.3074 | 0.5412 | yes | note, command, create | cli, create, run, read, command, manage |
| `openapi-contract-reviewer` | no | 0.7326 | 0.5764 | 0.4809 | no | openapi, example, contract, auth | openapi, example, auth |
| `mcp-server-builder` | no | 0.7326 | 0.4904 | 0.3126 | no | example, build, mcp, server | tool, build, example |

Top similarity neighbours: `public-openai-cli-creator` (0.733), `openapi-contract-reviewer` (0.576), `openapi-contract-tester` (0.504), `auth-flow-integrator` (0.499), `mcp-server-builder` (0.490)

### `public_gold_p20_hf_datasets`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-datasets`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-hf-cli` | no | 0.7564 | 0.3896 | 0.6347 | yes | dataset, hugg, face, download, model, train | hugg, face, dataset, search, download, read |
| `public-huggingface-huggingface-tool-builder` | no | 0.7564 | 0.4202 | 0.7699 | yes | hugg, face, api | hugg, face, api, fetch |
| `public-huggingface-train-sentence-transformers` | no | 0.7564 | 0.4348 | 0.5237 | yes | hugg, face, model, train | hugg, face |
| `public-office-data-extractor` | no | 0.7564 | 0.1629 | 0.4600 | no | - | - |

Top similarity neighbours: `public-huggingface-datasets` (0.756), `psc-hf-dataset-card-inspector` (0.634), `hf-dataset-viewer-inspector` (0.616), `psc-local-model-fit-selector` (0.522), `public-huggingface-huggingface-papers` (0.517)

### `public_gold_p21_hf_gradio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-gradio`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-zerogpu` | no | 0.5102 | 0.4525 | 0.3259 | yes | gradio, demo, python, zerogpu | gradio, build, demo, python |
| `public-huggingface-huggingface-tool-builder` | no | 0.5102 | 0.1710 | 0.6648 | yes | create, api, call | build |
| `public-huggingface-datasets` | no | 0.5102 | 0.2670 | 0.5532 | yes | dataset, viewer, api | - |
| `public-huggingface-transformers-js` | no | 0.5102 | 0.2223 | 0.4367 | no | transformer, browser | - |
| `gradio-demo-builder` | yes | 0.5102 | 0.5679 | 0.6282 | yes | gradio, demo, launch, dataset | gradio, build, demo |

Top similarity neighbours: `gradio-demo-builder` (0.568), `public-huggingface-huggingface-gradio` (0.510), `public-huggingface-huggingface-zerogpu` (0.453), `public-swebench-grafana-dashboards` (0.350), `hf-zerogpu-space-deployer` (0.329)

### `public_gold_p22_hf_vision_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-vision-trainer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-llm-trainer` | no | 0.4935 | 0.3919 | 0.7570 | yes | model, train, fine-tune, dataset, vision, local, gguf | model, hugg, face, train, vision, transformer, jobs, fine-tune |
| `public-huggingface-huggingface-community-evals` | no | 0.4935 | 0.2443 | 0.6042 | yes | model, evaluation, local | model, hugg, face, transformer, jobs, evaluation, hardware, selection |
| `public-huggingface-huggingface-local-models` | no | 0.4935 | 0.3025 | 0.5580 | yes | model, local, gguf | model, cover, selection |
| `public-huggingface-train-sentence-transformers` | no | 0.4935 | 0.4114 | 0.5969 | yes | model, train, fine-tune | model, hugg, face, train, classification, fine-tune, cover, loss |

Top similarity neighbours: `public-huggingface-huggingface-vision-trainer` (0.493), `psc-sentence-embedding-trainer` (0.448), `sentence-transformer-finetuner` (0.429), `public-huggingface-train-sentence-transformers` (0.411), `public-huggingface-huggingface-llm-trainer` (0.392)

### `public_gold_p23_sentence_transformer_training`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-train-sentence-transformers`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-transformers-js` | no | 0.5595 | 0.3325 | 0.6427 | yes | text, browser, transformer, model | model, classification, multimodal, hugg, face, hub |
| `public-huggingface-huggingface-llm-trainer` | no | 0.5595 | 0.1334 | 0.6213 | yes | train, fine-tune, transformer, local, model | model, train, fine-tune, cover, selection, hugg, face, hub |
| `public-huggingface-huggingface-local-models` | no | 0.5595 | 0.0445 | 0.4039 | no | local, model | model, cover, selection |
| `public-huggingface-datasets` | no | 0.5595 | 0.0837 | 0.5237 | yes | text | hugg, face |
| `sentence-transformer-finetuner` | yes | 0.5595 | 0.6094 | 0.7465 | yes | train, retrieval, pair, evaluation | retrieval, train, sentence-transformer, embedd, pair, similarity |

Top similarity neighbours: `sentence-transformer-finetuner` (0.609), `public-huggingface-train-sentence-transformers` (0.559), `psc-sentence-embedding-trainer` (0.392), `search-ops-rewrite-editor` (0.361), `search-ops-summary-writer` (0.357)

### `public_gold_p24_hf_cli`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-hf-cli`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-datasets` | no | 0.5432 | 0.6777 | 0.6347 | yes | hugg, face, metadata, dataset, viewer, api | hugg, face, dataset, download, read, search |
| `public-huggingface-huggingface-paper-publisher` | no | 0.5432 | 0.4759 | 0.5279 | yes | hugg, face, hub, model, manage, dataset | hugg, face, dataset, hub, model, paper |
| `public-huggingface-huggingface-local-models` | no | 0.5432 | 0.4894 | 0.5191 | yes | model, file | model, local, runn |
| `public-huggingface-huggingface-tool-builder` | no | 0.5432 | 0.4614 | 0.6485 | yes | hugg, face, api, tool | hugg, face, data |

Top similarity neighbours: `public-huggingface-datasets` (0.678), `hf-dataset-viewer-inspector` (0.605), `psc-hf-dataset-card-inspector` (0.569), `public-huggingface-hf-cli` (0.543), `public-huggingface-huggingface-community-evals` (0.505)

### `public_gold_p25_data_pipeline`

- Family: `public_gold_validation`
- Gold skill: `public-office-data-pipeline`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | no | 0.6553 | 0.3651 | 0.6670 | yes | data, analysi | data |
| `public-office-data-extractor` | no | 0.6553 | 0.1637 | 0.5458 | yes | - | - |
| `public-office-database-sync` | no | 0.6553 | 0.4442 | 0.6146 | yes | data, database | data, integration |
| `public-swebench-dbt-transformation-patterns` | no | 0.6553 | 0.3829 | 0.4860 | no | data, analytic | data, analytic |
| `public-office-etl-pipeline` | yes | 0.6553 | 0.6108 | 0.9619 | yes | design, extract, data, transform, load, analytic, pipeline | data, pipeline, extract, transform, load, integration, analytic |

Top similarity neighbours: `public-office-data-pipeline` (0.655), `public-office-etl-pipeline` (0.611), `public-office-database-sync` (0.444), `analytics-ops-resource-linker` (0.421), `analytics-ops-dependency-mapper` (0.417)

### `public_gold_p26_database_sync`

- Family: `public_gold_validation`
- Gold skill: `public-office-database-sync`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-data-pipeline` | no | 0.4121 | 0.3998 | 0.6146 | yes | etl, pipeline | data, integration |
| `public-office-airtable-automation` | no | 0.4121 | 0.2749 | 0.5722 | yes | - | database, integration |
| `public-office-crm-automation` | no | 0.4121 | 0.2745 | 0.5899 | yes | synchronization | synchronization |
| `public-office-data-analysis` | no | 0.4121 | 0.2562 | 0.5178 | yes | create, analysi | data |

Top similarity neighbours: `public-office-database-sync` (0.412), `public-office-data-pipeline` (0.400), `graphql-schema-designer` (0.388), `public-office-etl-pipeline` (0.379), `database-ops-dependency-mapper` (0.338)

### `public_gold_p27_contract_review`

- Family: `public_gold_validation`
- Gold skill: `public-office-contract-review`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-contract-template` | no | 0.4547 | 0.2519 | 0.5212 | yes | - | - |
| `public-security-threat-model` | no | 0.4547 | 0.2521 | 0.4274 | no | review | - |
| `public-office-proposal-writer` | no | 0.4547 | 0.2704 | 0.6207 | yes | - | - |
| `document-summariser` | no | 0.4547 | 0.2082 | 0.3637 | no | contract, summary | contract |
| `contract-risk-reviewer` | yes | 0.4547 | 0.6381 | 0.6316 | yes | review, contract, risky, clause, obligation, renewal, term, negotiation | contract |

Top similarity neighbours: `contract-risk-reviewer` (0.638), `vendor-ops-risk-reviewer` (0.537), `procurement-risk-summariser` (0.520), `vendor-ops-summary-writer` (0.517), `contract-ops-risk-reviewer` (0.512)

### `public_gold_p28_suspicious_email`

- Family: `public_gold_validation`
- Gold skill: `public-office-suspicious-email`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-email-classifier` | no | 0.6736 | 0.3451 | 0.5754 | yes | email | email |
| `public-office-email-drafter` | no | 0.6736 | 0.3670 | 0.6319 | yes | - | - |
| `public-office-gmail-workflows` | no | 0.6736 | 0.1546 | 0.4535 | no | email | email |
| `public-office-security-monitoring` | no | 0.6736 | 0.2635 | 0.6193 | yes | response | security, threat |

Top similarity neighbours: `public-office-suspicious-email` (0.674), `email-classification-router` (0.496), `email-ops-risk-reviewer` (0.485), `email-polisher` (0.483), `email-ops-evidence-grounder` (0.472)

### `public_gold_p29_ai_slides`

- Family: `public_gold_validation`
- Gold skill: `public-office-ai-slides`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-md-slides` | no | 0.4528 | 0.2682 | 0.6531 | yes | - | - |
| `public-office-html-slides` | no | 0.4528 | 0.2675 | 0.6312 | yes | - | - |
| `public-office-dev-slides` | no | 0.4528 | 0.2477 | 0.6959 | yes | - | - |
| `public-anthropic-theme-factory` | no | 0.4528 | 0.4179 | 0.4167 | yes | generate, slide, apply, theme | generate, slide |

Top similarity neighbours: `slide-deck-visual-auditor` (0.546), `slide-outline-builder` (0.545), `public-office-ppt-visual` (0.466), `public-office-ai-slides` (0.453), `deck-template-applier` (0.439)

### `public_gold_p30_figma_implement_design`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-implement-design`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-figma-generate-design` | no | 0.5917 | 0.5603 | 0.7891 | yes | figma, design, create, code, update, screen, component | figma, code, design, component, application, build, match, write |
| `public-openai-figma-generate-library` | no | 0.5917 | 0.4924 | 0.8069 | yes | figma, design, create, code, update, component | figma, code, design, component, build, figma-use |
| `public-openai-figma-code-connect-components` | no | 0.5917 | 0.4689 | 0.8217 | yes | figma, design, create, code, component | figma, code, design, component, canva, write, via, figma-use |
| `public-openai-figma-use` | no | 0.5917 | 0.4479 | 0.7525 | yes | figma, context, create, node, component | figma, component, file, build, write |

Top similarity neighbours: `public-openai-figma-implement-design` (0.592), `public-openai-figma-generate-design` (0.560), `public-openai-figma` (0.558), `public-openai-figma-generate-library` (0.492), `public-openai-figma-code-connect-components` (0.469)

### `public_gold_p31_skill_creator`

- Family: `public_gold_validation`
- Gold skill: `public-skill-creator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-skill-installer` | no | 0.5802 | 0.5513 | 0.7007 | yes | codex, includ, install | - |
| `public-openai-migrate-to-codex` | no | 0.5802 | 0.4171 | 0.4998 | no | codex, migrate | - |
| `public-oh-my-agentic-skills` | no | 0.5802 | 0.3679 | 0.6669 | yes | - | - |
| `skill-field-auditor` | no | 0.5802 | 0.4561 | 0.4555 | no | workflow, includ, trigger, resource, exist | exist, workflow |
| `skill-creator` | yes | 0.5802 | 0.6991 | 0.5665 | yes | create, new, repeat, workflow, includ, trigger, description, optional | create, new, workflow |

Top similarity neighbours: `skill-creator` (0.699), `skill-editor` (0.672), `skill-authoring-guide` (0.584), `public-skill-creator` (0.580), `skill-finder` (0.557)

### `public_gold_p32_security_threat_model`

- Family: `public_gold_validation`
- Gold skill: `public-security-threat-model`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 10

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-security-best-practices` | no | 0.4616 | 0.4009 | 0.6228 | yes | best, practice | trigger, only, explicitly, perform, general, code, review, non-security |
| `public-openai-security-ownership-map` | no | 0.4616 | 0.5184 | 0.4860 | yes | sensitive, list, ownership | trigger, only, explicitly, general, code, non-security |
| `public-swebench-security-review` | no | 0.4616 | 0.4129 | 0.5120 | yes | sensitive | work |
| `security-threat-modeler` | yes | 0.4616 | 0.3740 | 0.6965 | yes | architecture, identify, data, mitigation | threat, model, abuse, trust, boundarie, asset, attacker, mitigation |

Top similarity neighbours: `public-oh-my-file-organization` (0.535), `public-openai-security-ownership-map` (0.518), `public-oh-my-changelog-maintenance` (0.516), `public-addy-agent-source-driven-development` (0.491), `public-addy-web-best-practices` (0.486)

### `public_gold_p33_openai_docs`

- Family: `public_gold_validation`
- Gold skill: `public-openai-openai-docs`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-chatgpt-apps` | no | 0.5876 | 0.6329 | 0.5980 | yes | openai, build, chatgpt, docs | openai, build, apis, need, docs, mcp, tool, domain |
| `public-openai-cli-creator` | no | 0.5876 | 0.5116 | 0.6761 | yes | api, build, app, cli, docs | build, docs, tool |
| `public-anthropic-claude-api` | no | 0.5876 | 0.4815 | 0.5233 | yes | api, openai, model, build, anthropic | openai, model, asks, build, citation, tool |
| `public-huggingface-huggingface-tool-builder` | no | 0.5876 | 0.3370 | 0.4335 | no | api, build | build, tool |

Top similarity neighbours: `public-openai-chatgpt-apps` (0.633), `public-openai-openai-docs` (0.588), `public-openai-speech` (0.558), `public-openai-notion-knowledge-capture` (0.533), `public-openai-migrate-to-codex` (0.531)

### `public_gold_p34_playwright`

- Family: `public_gold_validation`
- Gold skill: `public-openai-playwright`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 9

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-playwright-interactive` | no | 0.4885 | 0.5276 | 0.5951 | yes | browser, interaction | browser, debug |
| `public-addy-agent-browser-testing-with-devtools` | no | 0.4885 | 0.6752 | 0.5324 | yes | browser, test, need, chrome, devtool, mcp | require, real, browser, data, debug, via |
| `public-anthropic-webapp-testing` | no | 0.4885 | 0.6089 | 0.6630 | yes | browser, playwright, test, local, screenshot | browser, screenshot, debug |
| `playwright-flow-debugger` | yes | 0.4885 | 0.6008 | 0.5178 | yes | browser, interaction, screenshot | browser, screenshot |

Top similarity neighbours: `public-addy-agent-browser-testing-with-devtools` (0.675), `psc-playwright-regression-suite` (0.624), `public-anthropic-webapp-testing` (0.609), `playwright-flow-debugger` (0.601), `public-office-browser-automation` (0.568)

### `public_gold_p35_screenshot`

- Family: `public_gold_validation`
- Gold skill: `public-openai-screenshot`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 45

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-playwright` | no | 0.2715 | 0.4331 | 0.6378 | yes | screenshot, debug | screenshot |
| `public-addy-agent-browser-testing-with-devtools` | no | 0.2715 | 0.4391 | 0.3327 | yes | capture, visual, test, console, network, debug | capture, need |
| `public-office-browser-automation` | no | 0.2715 | 0.3385 | 0.2067 | yes | playwright, test | - |
| `public-anthropic-webapp-testing` | no | 0.2715 | 0.4909 | 0.3983 | yes | screenshot, local, playwright, test, debug | screenshot |

Top similarity neighbours: `playwright-flow-debugger` (0.537), `public-anthropic-webapp-testing` (0.491), `psc-playwright-regression-suite` (0.480), `public-playwright-interactive` (0.448), `public-addy-agent-browser-testing-with-devtools` (0.439)

### `public_gold_p36_sentry`

- Family: `public_gold_validation`
- Gold skill: `public-openai-sentry`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-oh-my-monitoring-observability` | no | 0.6248 | 0.2663 | 0.5108 | yes | - | - |
| `public-swebench-python-observability` | no | 0.6248 | 0.3994 | 0.3502 | no | observability, distribut, trac | production |
| `metrics-root-cause-diagnoser` | no | 0.6248 | 0.3787 | 0.0660 | no | likely, regression | - |
| `distributed-trace-investigator` | no | 0.6248 | 0.5590 | 0.1830 | yes | distribut, span | - |

Top similarity neighbours: `public-openai-sentry` (0.625), `distributed-trace-investigator` (0.559), `email-ops-failure-diagnoser` (0.523), `analytics-ops-failure-diagnoser` (0.502), `platform-ops-failure-diagnoser` (0.494)

### `public_gold_p37_transcribe`

- Family: `public_gold_validation`
- Gold skill: `public-openai-transcribe`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-speech` | no | 0.5457 | 0.4048 | 0.7527 | yes | audio, speech | audio, asks, speech |
| `public-office-transcription-automation` | no | 0.5457 | 0.5017 | 0.6595 | yes | audio, meet | audio, video |
| `public-office-podcast-automation` | no | 0.5457 | 0.4989 | 0.4800 | yes | record, podcast, workflow | - |
| `public-office-meeting-notes` | no | 0.5457 | 0.2579 | 0.4194 | no | - | - |

Top similarity neighbours: `public-openai-transcribe` (0.546), `public-office-transcription-automation` (0.502), `public-office-podcast-automation` (0.499), `speaker-notes-writer` (0.442), `public-openai-speech` (0.405)

### `public_gold_p38_speech`

- Family: `public_gold_validation`
- Gold skill: `public-openai-speech`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-transcribe` | no | 0.5259 | 0.5359 | 0.7527 | yes | audio, transcribe | audio, asks, speech |
| `public-office-transcription-automation` | no | 0.5259 | 0.5280 | 0.5263 | yes | audio, automate | audio, generation |
| `public-office-podcast-automation` | no | 0.5259 | 0.6222 | 0.4482 | yes | workflow, record, automate, podcast, publish | - |
| `public-anthropic-slack-gif-creator` | no | 0.5259 | 0.1307 | 0.2883 | no | - | - |

Top similarity neighbours: `public-office-podcast-automation` (0.622), `public-openai-transcribe` (0.536), `public-office-transcription-automation` (0.528), `public-openai-speech` (0.526), `speaker-notes-writer` (0.382)

### `public_gold_p39_jupyter_notebook`

- Family: `public_gold_validation`
- Gold skill: `public-openai-jupyter-notebook`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | no | 0.5194 | 0.4969 | 0.3195 | yes | create, csv, analysi, report, excel | create, generate |
| `public-huggingface-datasets` | no | 0.5194 | 0.3409 | 0.3278 | no | hugg, face, dataset | - |
| `public-swebench-python-configuration` | no | 0.5194 | 0.2837 | 0.5567 | yes | python | - |
| `public-office-report-generator` | no | 0.5194 | 0.4026 | 0.2646 | no | report | generate |

Top similarity neighbours: `public-openai-jupyter-notebook` (0.519), `public-office-data-analysis` (0.497), `public-office-report-generator` (0.403), `data-analysis-overview` (0.401), `psc-anomaly-watchlist-builder` (0.382)

### `public_gold_p40_linear`

- Family: `public_gold_validation`
- Gold skill: `public-openai-linear`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 12

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-lbussell-creating-issues` | no | 0.4387 | 0.0588 | 0.4192 | no | - | - |
| `public-lbussell-triaging-issues` | no | 0.4387 | 0.0636 | 0.4074 | no | - | - |
| `public-office-jira-automation` | no | 0.4387 | 0.5218 | 0.4701 | yes | issue, project, jira | issue, project, workflow |
| `public-office-asana-automation` | no | 0.4387 | 0.5382 | 0.4780 | yes | team, project, asana | project, team, workflow |

Top similarity neighbours: `public-office-asana-automation` (0.538), `public-office-jira-automation` (0.522), `public-openai-notion-spec-to-implementation` (0.499), `repo-ops-scenario-planner` (0.490), `engineering-design-ops-scenario-planner` (0.475)

### `public_gold_p41_yeet`

- Family: `public_gold_validation`
- Gold skill: `public-openai-yeet`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 200

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-gh-address-comments` | no | 0.2407 | 0.3908 | 0.7015 | yes | current, branch, open, github, addres, review, comment | github, open, cli |
| `public-openai-gh-fix-ci` | no | 0.2407 | 0.4781 | 0.7148 | yes | draft, github, debug, logs | github, only, asks |
| `public-lbussell-creating-pull-requests` | yes | 0.2407 | 0.1820 | 0.6210 | yes | - | - |
| `public-addy-agent-git-workflow-and-versioning` | yes | 0.2407 | 0.3259 | 0.5607 | yes | change, branch | - |

Top similarity neighbours: `pr-review-comment-resolver` (0.625), `ci-log-root-cause-debugger` (0.620), `code-reviewer` (0.578), `ci-failure-debugger` (0.572), `repo-code-reviewer` (0.559)

### `public_gold_p42_migrate_to_codex`

- Family: `public_gold_validation`
- Gold skill: `public-openai-migrate-to-codex`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-skill-creator` | no | 0.5822 | 0.5715 | 0.4998 | yes | exist | - |
| `public-skill-installer` | no | 0.5822 | 0.6470 | 0.5912 | yes | codex, includ, install | codex |
| `public-addy-agent-context-engineering` | no | 0.5822 | 0.4490 | 0.4387 | no | agent, setup | file, agent, project |
| `public-oh-my-agentic-skills` | no | 0.5822 | 0.5389 | 0.5174 | yes | - | - |

Top similarity neighbours: `public-skill-installer` (0.647), `skill-authoring-guide` (0.607), `public-mattpocock-setup-matt-pocock-skills` (0.585), `public-openai-migrate-to-codex` (0.582), `public-skill-creator` (0.572)

### `public_gold_p43_notion_knowledge_capture`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-knowledge-capture`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-notion-meeting-intelligence` | no | 0.5687 | 0.5619 | 0.8132 | yes | notion, meet, research | notion |
| `public-office-notion-automation` | no | 0.5687 | 0.4001 | 0.5413 | yes | notion, database | notion |
| `notion-research-database-builder` | yes | 0.5687 | 0.4933 | 0.4030 | yes | capture, notion, research, database | capture, notion |
| `public-openai-notion-research-documentation` | yes | 0.5687 | 0.5291 | 0.8252 | yes | notion, structur, research | structur, notion |

Top similarity neighbours: `meeting-notes-action-extractor` (0.624), `public-openai-notion-knowledge-capture` (0.569), `public-openai-notion-meeting-intelligence` (0.562), `meeting-ops-summary-writer` (0.549), `task-extractor` (0.543)

### `public_gold_p44_notion_meeting_intelligence`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-meeting-intelligence`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 5

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | no | 0.5185 | 0.3483 | 0.5101 | yes | - | notion |
| `public-office-meeting-notes` | yes | 0.5185 | 0.4047 | 0.5456 | yes | - | - |
| `meeting-notes-action-extractor` | yes | 0.5185 | 0.6360 | 0.5133 | yes | meet, transcript, decision, action, item, owner, due, date | meet |
| `public-openai-notion-knowledge-capture` | yes | 0.5185 | 0.4514 | 0.8132 | yes | page, turn, decision, link | notion |

Top similarity neighbours: `meeting-notes-action-extractor` (0.636), `meeting-followup-extractor` (0.608), `meeting-summary-writer` (0.577), `meeting-agenda-builder` (0.560), `public-openai-notion-meeting-intelligence` (0.518)

### `public_gold_p45_notion_spec_to_implementation`

- Family: `public_gold_validation`
- Gold skill: `public-openai-notion-spec-to-implementation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-notion-knowledge-capture` | no | 0.7173 | 0.4381 | 0.7377 | yes | notion, link | notion, turn |
| `public-addy-agent-spec-driven-development` | no | 0.7173 | 0.3919 | 0.6383 | yes | spec, create | spec, feature |
| `public-lbussell-creating-issues` | no | 0.7173 | -0.0461 | 0.2443 | no | - | - |
| `public-openai-linear` | no | 0.7173 | 0.1747 | 0.5553 | yes | create, issue | - |

Top similarity neighbours: `public-openai-notion-spec-to-implementation` (0.717), `notion-research-database-builder` (0.518), `product-ops-scenario-planner` (0.502), `public-openai-notion-research-documentation` (0.492), `engineering-design-ops-scenario-planner` (0.473)

### `public_gold_p46_figma_code_connect`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-code-connect-components`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-figma-implement-design` | no | 0.7008 | 0.6075 | 0.8217 | yes | component, figma, code, design, implement, generate | code, component, figma, design, canva, write, via, figma-use |
| `public-openai-figma-generate-library` | no | 0.7008 | 0.5495 | 0.7586 | yes | component, figma, code, design | code, component, figma, design, create, figma-use |
| `public-openai-figma-generate-design` | no | 0.7008 | 0.5246 | 0.6680 | yes | component, figma, code, design, screen | code, component, figma, design, create, write, via, figma-use |
| `public-openai-figma-use` | no | 0.7008 | 0.4134 | 0.7254 | yes | component, figma | component, figma, tool, create, write |

Top similarity neighbours: `public-openai-figma-code-connect-components` (0.701), `public-openai-figma-implement-design` (0.608), `public-openai-figma-generate-library` (0.549), `public-openai-figma-generate-design` (0.525), `public-openai-figma` (0.449)

### `public_gold_p47_figma_generate_library`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-generate-library`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-figma-code-connect-components` | no | 0.6374 | 0.6174 | 0.7586 | yes | component, code, figma, write, create, connect, mapping | figma, design, create, component, code, figma-use |
| `public-openai-figma-implement-design` | no | 0.6374 | 0.6292 | 0.8069 | yes | component, code, build, figma, implement, application, write | build, figma, design, component, code, figma-use |
| `public-openai-figma-create-design-system-rules` | no | 0.6374 | 0.5431 | 0.6901 | yes | figma, codebase, rule, create | figma, design, system, codebase, create, set |
| `public-openai-figma-generate-design` | yes | 0.6374 | 0.5781 | 0.7816 | yes | component, code, build, update, figma, variable, token, application | build, figma, update, design, system, create, variable, token |

Top similarity neighbours: `public-openai-figma-generate-library` (0.637), `public-openai-figma-implement-design` (0.629), `public-openai-figma-code-connect-components` (0.617), `public-openai-figma-generate-design` (0.578), `public-openai-figma-create-design-system-rules` (0.543)

### `public_gold_p48_figma_design_system_rules`

- Family: `public_gold_validation`
- Gold skill: `public-openai-figma-create-design-system-rules`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-figma-generate-library` | no | 0.5933 | 0.5420 | 0.6901 | yes | figma, create, component, token, code | design, system, codebase, create, set, figma |
| `public-openai-figma-generate-design` | no | 0.5933 | 0.5892 | 0.6559 | yes | figma, create, layout, component, token, screen, code | design, system, create, workflow, figma |
| `public-anthropic-brand-guidelines` | no | 0.5933 | 0.2393 | 0.3508 | no | - | design, guideline |
| `public-anthropic-theme-factory` | no | 0.5933 | 0.2536 | 0.3098 | no | generate | generate |

Top similarity neighbours: `public-openai-figma-implement-design` (0.616), `public-openai-figma-create-design-system-rules` (0.593), `public-openai-figma-generate-design` (0.589), `public-openai-figma-generate-library` (0.542), `public-openai-figma-code-connect-components` (0.533)

### `public_gold_p49_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 24

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | no | 0.4450 | 0.3603 | 0.4011 | no | audit, accessibility, web | ask, improve |
| `public-addy-web-core-web-vitals` | no | 0.4450 | 0.4138 | 0.6434 | yes | page, search, core, web, vital | search, optimize, optimization, rank, ask, improve, fix |
| `public-addy-web-best-practices` | no | 0.4450 | 0.3601 | 0.5454 | yes | audit, web | ask |
| `public-office-seo-optimizer` | yes | 0.4450 | 0.5443 | 0.7681 | yes | audit, technical, seo | optimization, rank, seo |
| `seo-metadata-checker` | yes | 0.4450 | 0.6229 | 0.5683 | yes | page, title, meta, description, structur, heading, search, snippet | search, visibility, meta, structur |

Top similarity neighbours: `seo-ops-quality-auditor` (0.633), `seo-metadata-checker` (0.623), `public-addy-web-web-quality-audit` (0.591), `seo-ops-risk-reviewer` (0.574), `seo-ops-compliance-checker` (0.559)

### `public_gold_p50_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-core-web-vitals` | no | 0.5313 | 0.4798 | 0.6495 | yes | web, lcp, inp, cls | optimize, web, better, experience, ask, reduce, fix, improve |
| `public-addy-web-best-practices` | no | 0.5313 | 0.3926 | 0.6306 | yes | web, code, review | web, ask, audit |
| `public-addy-agent-performance-optimization` | no | 0.5313 | 0.4690 | 0.7709 | yes | web, load, performance | performance, load, optimize, web, time, fix |
| `public-addy-web-web-quality-audit` | no | 0.5313 | 0.4594 | 0.6769 | yes | web, performance, review | performance, optimize, web, ask, site, page, audit |

Top similarity neighbours: `web-performance-budget-checker` (0.620), `public-addy-web-performance` (0.531), `psc-visual-screenshot-reviewer` (0.491), `api-design-reviewer` (0.483), `public-addy-web-core-web-vitals` (0.480)

### `public_gold_p51_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | no | 0.6056 | 0.4925 | 0.6057 | yes | web, audit, accessibility, wcag | audit, web, accessibility, ask |
| `public-addy-web-core-web-vitals` | no | 0.6056 | 0.4377 | 0.5805 | yes | web, core, vital | web, ask, page, optimize |
| `public-addy-web-seo` | no | 0.6056 | 0.2377 | 0.6184 | yes | seo | seo, ask, optimize |
| `public-addy-web-best-practices` | no | 0.6056 | 0.4483 | 0.7283 | yes | web, quality, audit, best, practice | quality, audit, web, best, practice, ask, review, check |

Top similarity neighbours: `public-addy-web-web-quality-audit` (0.606), `web-ops-quality-auditor` (0.604), `web-ops-risk-reviewer` (0.532), `content-ops-quality-auditor` (0.528), `seo-ops-quality-auditor` (0.504)

### `public_gold_p52_api_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | no | 0.5447 | 0.6576 | 0.5047 | yes | contract, review, openapi | endpoint, contract |
| `public-openai-cli-creator` | no | 0.5447 | 0.4450 | 0.4493 | no | stable, exist, openapi, build, cli | stable, api |
| `external-api-integration-planner` | no | 0.5447 | 0.5586 | 0.5106 | yes | - | api, endpoint |
| `public-oh-my-api-design` | yes | 0.5447 | 0.2726 | 0.5396 | yes | - | - |
| `public-api-design-principles` | yes | 0.5447 | 0.5239 | 0.7135 | yes | design, rest, review, build | design, api, apis, rest, graphql, establish |

Top similarity neighbours: `openapi-contract-reviewer` (0.658), `external-api-integration-planner` (0.559), `architecture-boundary-reviewer` (0.545), `public-addy-agent-api-and-interface-design` (0.545), `openapi-contract-tester` (0.534)

### `public_gold_p53_context_engineering`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-context-engineering`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-agent-source-driven-development` | no | 0.6171 | 0.4432 | 0.6046 | yes | - | - |
| `public-addy-agent-planning-and-task-breakdown` | no | 0.6171 | 0.4868 | 0.7219 | yes | - | start, need |
| `public-oh-my-codebase-search` | no | 0.6171 | 0.2418 | 0.4202 | no | - | - |
| `public-openai-migrate-to-codex` | no | 0.6171 | 0.4430 | 0.4387 | no | project, agent, file, migrate, codex | agent, file, project |

Top similarity neighbours: `public-addy-agent-context-engineering` (0.617), `public-n-skills-orchestration` (0.541), `public-addy-agent-idea-refine` (0.513), `public-mattpocock-improve-codebase-architecture` (0.497), `public-addy-agent-spec-driven-development` (0.493)

### `public_gold_p54_deprecation_migration`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-deprecation-and-migration`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 7

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-mattpocock-migrate-to-shoehorn` | no | 0.4546 | 0.1844 | 0.2827 | no | - | - |
| `public-addy-agent-incremental-implementation` | no | 0.4546 | 0.1493 | 0.7172 | yes | - | feature, code |
| `public-addy-agent-api-and-interface-design` | no | 0.4546 | 0.3725 | 0.6434 | yes | api | apis |
| `database-migration-risk-assessor` | no | 0.4546 | 0.6315 | 0.4665 | yes | plan, compatibility, database, migration, risk | migration |

Top similarity neighbours: `database-migration-risk-assessor` (0.631), `migration-risk-auditor` (0.492), `architecture-boundary-reviewer` (0.487), `api-ops-scenario-planner` (0.479), `api-ops-risk-reviewer` (0.471)

### `public_gold_p55_documentation_adrs`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-documentation-and-adrs`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 24

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-oh-my-api-documentation` | no | 0.3877 | 0.1798 | 0.5090 | yes | - | - |
| `code-documentation-writer` | no | 0.3877 | 0.3326 | 0.4263 | yes | write, documentation | documentation, apis, future, understand |
| `public-openai-notion-research-documentation` | no | 0.3877 | 0.2068 | 0.5239 | yes | documentation, report | documentation |
| `public-office-report-generator` | no | 0.3877 | 0.0519 | 0.3262 | no | report | - |

Top similarity neighbours: `architecture-boundary-reviewer` (0.518), `public-anthropic-claude-api` (0.477), `api-ops-summary-writer` (0.476), `api-design-reviewer` (0.460), `api-ops-scenario-planner` (0.456)

### `public_gold_p56_spec_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-spec-driven-development`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-agent-test-driven-development` | no | 0.4171 | 0.2450 | 0.7098 | yes | test | exist |
| `public-addy-agent-incremental-implementation` | no | 0.4171 | 0.1992 | 0.7334 | yes | feature | feature, change |
| `public-openai-notion-spec-to-implementation` | no | 0.4171 | 0.5328 | 0.6383 | yes | spec, turn, feature, implementation, notion | spec, feature |
| `public-mattpocock-to-prd` | no | 0.4171 | 0.1093 | 0.4916 | no | turn | create, project |

Top similarity neighbours: `public-openai-notion-spec-to-implementation` (0.533), `engineering-design-ops-scenario-planner` (0.431), `notion-research-database-builder` (0.420), `public-addy-agent-spec-driven-development` (0.417), `public-office-notion-automation` (0.391)

### `public_gold_p57_test_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-test-driven-development`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 187

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-agent-spec-driven-development` | no | 0.2175 | 0.0485 | 0.7098 | yes | only, specification | exist |
| `public-oh-my-testing-strategies` | no | 0.2175 | 0.2398 | 0.6087 | yes | - | - |
| `public-mattpocock-tdd` | yes | 0.2175 | 0.3893 | 0.5828 | yes | test, fix, red-green-refactor, loop | development, test, fix |
| `public-swebench-tdd-workflow` | yes | 0.2175 | 0.2608 | 0.6178 | yes | test, fix | development, test, fix, code |

Top similarity neighbours: `ci-failure-debugger` (0.522), `implicit-ci-failure-reader` (0.419), `debugging-root-cause-helper` (0.406), `ux-ops-failure-diagnoser` (0.399), `public-mattpocock-tdd` (0.389)

### `public_gold_p58_source_driven_development`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-source-driven-development`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-agent-context-engineering` | no | 0.3554 | 0.1763 | 0.6046 | yes | context | - |
| `public-oh-my-codebase-search` | no | 0.3554 | 0.2759 | 0.4333 | yes | - | - |
| `public-addy-agent-incremental-implementation` | no | 0.3554 | 0.2145 | 0.7010 | yes | code | code |
| `public-mattpocock-diagnose` | no | 0.3554 | 0.2029 | 0.3359 | no | - | - |

Top similarity neighbours: `public-mattpocock-improve-codebase-architecture` (0.378), `public-swebench-python-anti-patterns` (0.358), `public-addy-agent-source-driven-development` (0.355), `public-architecture-patterns` (0.347), `public-swebench-add-uint-support` (0.344)

### `public_gold_p59_anthropic_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 10

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-openai-docs` | no | 0.4764 | 0.5062 | 0.5233 | yes | guidance, tool, model, openai, docs, build, mcp | model, openai, build, asks, tool, citation |
| `public-openai-cli-creator` | no | 0.4764 | 0.4869 | 0.5011 | yes | api, tool, docs, cli, build | sdk, api, build, exist, tool |
| `public-anthropic-mcp-builder` | no | 0.4764 | 0.4963 | 0.2944 | yes | tool, model, build, mcp, server | sdk, model, build, tool |
| `public-huggingface-hf-cli` | no | 0.4764 | 0.4048 | 0.4119 | yes | model, hugg, face, cli | model, manag, agent, cache, like, general |

Top similarity neighbours: `openapi-contract-reviewer` (0.549), `public-openai-speech` (0.544), `public-openai-chatgpt-apps` (0.540), `public-openai-openai-docs` (0.506), `external-api-integration-planner` (0.497)

### `public_gold_p60_doc_coauthoring`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-doc-coauthoring`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-report-generator` | no | 0.4751 | 0.2627 | 0.3511 | no | generate, report | - |
| `public-office-content-writer` | no | 0.4751 | 0.2767 | 0.5855 | yes | - | content, write |
| `document-rewriter` | yes | 0.4751 | 0.3957 | 0.3499 | yes | document, preserv, exist, structure, rewrite, tone | content |
| `public-mattpocock-edit-article` | yes | 0.4751 | 0.3775 | 0.5323 | yes | improv, section | draft |

Top similarity neighbours: `method-note-builder` (0.518), `partnerships-ops-rewrite-editor` (0.482), `public-anthropic-doc-coauthoring` (0.475), `vendor-ops-rewrite-editor` (0.454), `research-ops-rewrite-editor` (0.449)

### `public_gold_p61_canvas_design`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-canvas-design`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-anthropic-frontend-design` | no | 0.5186 | 0.4579 | 0.6515 | yes | create, layout, build, frontend, web, design | create, design, asks, poster, avoid |
| `public-anthropic-web-artifacts-builder` | no | 0.5186 | 0.4108 | 0.4673 | no | frontend, web | - |
| `public-anthropic-theme-factory` | no | 0.5186 | 0.2510 | 0.4588 | no | - | - |
| `public-openai-figma-generate-design` | no | 0.5186 | 0.4085 | 0.4175 | no | create, layout, build, app, figma, design | create, design |
| `public-office-diagram-creator` | no | 0.5186 | 0.5397 | 0.5158 | yes | create | create |
| `public-office-infographic` | no | 0.5186 | 0.5152 | 0.5663 | yes | visual, layout, design | design, visual |

Top similarity neighbours: `public-office-diagram-creator` (0.540), `public-anthropic-canvas-design` (0.519), `public-office-infographic` (0.515), `public-obsidian-json-canvas` (0.473), `public-office-chart-designer` (0.466)

### `public_gold_p62_theme_factory`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-theme-factory`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-figma-create-design-system-rules` | no | 0.4999 | 0.2194 | 0.3098 | no | generate, guideline | generate |
| `public-office-brand-guidelines` | no | 0.4999 | 0.4680 | 0.4262 | yes | visual, brand | - |
| `public-oh-my-design-system` | no | 0.4999 | 0.2077 | 0.4958 | no | - | - |
| `public-anthropic-canvas-design` | no | 0.4999 | 0.3234 | 0.4588 | no | visual | - |
| `public-anthropic-frontend-design` | no | 0.4999 | 0.4652 | 0.5767 | yes | generate, component, styl, frontend | artifact, styl, html, land, page, generate |
| `public-mattpocock-prototype` | no | 0.4999 | 0.4072 | 0.3518 | no | prototype | - |

Top similarity neighbours: `public-anthropic-theme-factory` (0.500), `product-ops-rewrite-editor` (0.479), `public-office-brand-guidelines` (0.468), `public-anthropic-frontend-design` (0.465), `public-mattpocock-prototype` (0.407)

### `public_gold_p63_hf_zerogpu`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-zerogpu`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | no | 0.6184 | 0.5916 | 0.3259 | yes | build, gradio | build, demo, gradio, python |
| `public-huggingface-huggingface-local-models` | no | 0.6184 | 0.4716 | 0.4764 | no | run, local, model | cuda |
| `public-huggingface-hf-cli` | no | 0.6184 | 0.3928 | 0.3888 | no | hugg, face, space, local, model | space, hugg, face, configur, handl, sure, whenever, mention |
| `public-huggingface-huggingface-tool-builder` | no | 0.6184 | 0.3425 | 0.3359 | no | hugg, face, build | build, hugg, face, proces |
| `gradio-demo-builder` | no | 0.6184 | 0.5850 | 0.3498 | yes | constraint, build, gradio, model | build, demo, gradio, constraint |
| `public-huggingface-huggingface-llm-trainer` | no | 0.6184 | 0.4691 | 0.4730 | no | hugg, face, deployment, local, model | gpu, hugg, face, mention, package, guidance |

Top similarity neighbours: `public-huggingface-huggingface-zerogpu` (0.618), `public-huggingface-huggingface-gradio` (0.592), `gradio-demo-builder` (0.585), `hf-zerogpu-space-deployer` (0.582), `public-huggingface-huggingface-local-models` (0.472)

### `public_gold_p64_hf_llm_trainer`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-llm-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-vision-trainer` | no | 0.4967 | 0.4356 | 0.7570 | yes | model, train, fine-tune, hugg, face, dataset, evaluation, vision | train, model, jobs, hugg, face, selection, fine-tune, vision |
| `public-huggingface-huggingface-community-evals` | no | 0.4967 | 0.3280 | 0.6820 | yes | model, hugg, face, evaluation | model, jobs, hugg, face, local, selection, gpu, transformer |
| `public-huggingface-huggingface-local-models` | no | 0.4967 | 0.3004 | 0.6421 | yes | model | model, gguf, convert, local, selection, cover |
| `public-swebench-llm-evaluation` | no | 0.4967 | 0.3947 | 0.4644 | no | evaluation, llm | - |

Top similarity neighbours: `psc-sentence-embedding-trainer` (0.625), `public-huggingface-train-sentence-transformers` (0.621), `sentence-transformer-finetuner` (0.598), `public-huggingface-huggingface-llm-trainer` (0.497), `public-huggingface-huggingface-vision-trainer` (0.436)

### `public_gold_p65_hf_local_models`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-local-models`
- Plausible listed alternatives: 5
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | no | 0.6549 | 0.2338 | 0.4832 | no | build | - |
| `public-huggingface-huggingface-zerogpu` | no | 0.6549 | 0.4182 | 0.4764 | no | hugg, face, runtime, space, build | cuda |
| `public-huggingface-transformers-js` | no | 0.6549 | 0.5842 | 0.5031 | yes | model, run, hugg, face, runtime, transformer, webgpu | model, run |
| `public-huggingface-huggingface-llm-trainer` | no | 0.6549 | 0.5526 | 0.6421 | yes | local, model, hugg, face, gguf, selection, train, transformer | gguf, model, cover, selection, convert, local |
| `public-huggingface-huggingface-community-evals` | no | 0.6549 | 0.5191 | 0.6436 | yes | local, model, run, hugg, face, selection, transformer | model, run, selection, local |
| `implicit-hf-local-model-chooser` | yes | 0.6549 | 0.4970 | 0.4968 | yes | local, model, choose, hugg, face, runtime, gguf, quantization | gguf, model, local |
| `hf-local-model-selector` | yes | 0.6549 | 0.5980 | 0.6159 | yes | local, model, hugg, face, gguf, quantization, tradeoff | gguf, select, model, local |

Top similarity neighbours: `public-huggingface-huggingface-local-models` (0.655), `hf-local-model-selector` (0.598), `psc-local-model-fit-selector` (0.595), `public-huggingface-transformers-js` (0.584), `public-huggingface-huggingface-llm-trainer` (0.553)

### `public_gold_p66_hf_trackio`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-trackio`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-community-evals` | no | 0.7123 | 0.3403 | 0.4825 | no | run, evaluation | automation |
| `public-swebench-llm-evaluation` | no | 0.7123 | 0.4740 | 0.4898 | no | metric, evaluation | metric |
| `public-huggingface-huggingface-llm-trainer` | no | 0.7123 | 0.3616 | 0.5568 | yes | train, trackio | train, trackio |
| `public-office-saas-metrics` | no | 0.7123 | 0.4139 | 0.2836 | no | metric, saas | metric, analysi |
| `dashboard-ops-monitoring-plan-builder` | no | 0.7123 | 0.5144 | 0.5392 | yes | metric, dashboard | metric, dashboard |
| `metrics-overview` | no | 0.7123 | 0.5256 | 0.4836 | no | metric, dashboard | metric, dashboard |

Top similarity neighbours: `public-huggingface-huggingface-trackio` (0.712), `dashboard-ops-quality-auditor` (0.558), `metrics-overview` (0.526), `dashboard-ops-acceptance-test-builder` (0.525), `dashboard-ops-resource-linker` (0.523)

### `public_gold_p67_hf_papers`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-papers`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-paper-publisher` | no | 0.6557 | 0.6509 | 0.8486 | yes | paper, hugg, face, model, link, publish, page | paper, page, hugg, face, link, model, dataset, research |
| `public-office-academic-search` | no | 0.6557 | 0.3724 | 0.4620 | no | paper, find | paper, project, analysi, research |
| `public-office-deep-research` | no | 0.6557 | 0.3646 | 0.4140 | no | topic | structur, analysi, research |
| `public-oh-my-research-paper-writing` | no | 0.6557 | 0.3279 | 0.5448 | yes | - | - |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.656), `public-huggingface-huggingface-paper-publisher` (0.651), `hf-community-eval-runner` (0.476), `public-huggingface-datasets` (0.457), `psc-hf-dataset-card-inspector` (0.453)

### `public_gold_p68_hf_paper_publisher`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-huggingface-paper-publisher`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-oh-my-research-paper-writing` | no | 0.6989 | 0.4085 | 0.5059 | yes | - | - |
| `public-office-academic-search` | no | 0.6989 | 0.3363 | 0.4622 | no | paper, search, academic | paper, research |
| `public-huggingface-hf-cli` | no | 0.6989 | 0.4739 | 0.5279 | yes | paper, model, hugg, face, search, academic | paper, hugg, face, hub, model, dataset |
| `public-huggingface-huggingface-papers` | yes | 0.6989 | 0.7368 | 0.8486 | yes | paper, model, hugg, face, metadata, link, page | paper, research, hugg, face, page, link, model, dataset |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.737), `public-huggingface-huggingface-paper-publisher` (0.699), `public-huggingface-datasets` (0.523), `psc-hf-dataset-card-inspector` (0.519), `hf-community-eval-runner` (0.500)

### `public_gold_p69_transformers_js`

- Family: `public_gold_validation`
- Gold skill: `public-huggingface-transformers-js`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-gradio` | no | 0.4668 | 0.3885 | 0.4367 | yes | build, demo, python, gradio | - |
| `public-huggingface-huggingface-local-models` | no | 0.4668 | 0.2727 | 0.5031 | yes | model, local, server | model, run |
| `public-anthropic-web-artifacts-builder` | no | 0.4668 | 0.2324 | 0.4757 | no | - | - |
| `public-office-browser-automation` | no | 0.4668 | 0.4073 | 0.3572 | yes | - | browser |

Top similarity neighbours: `gradio-demo-builder` (0.571), `public-huggingface-transformers-js` (0.467), `public-office-browser-automation` (0.407), `web-ui-tester` (0.404), `public-addy-agent-browser-testing-with-devtools` (0.401)

### `public_gold_p70_obsidian_json_canvas`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-json-canvas`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-obsidian-obsidian-markdown` | no | 0.4887 | 0.4546 | 0.5939 | yes | create, obsidian, markdown, note | file, create, edit, work, mention, obsidian |
| `public-obsidian-obsidian-bases` | no | 0.4887 | 0.3926 | 0.5832 | yes | create, obsidian, note, base, view | file, create, edit, work, creat, mention, obsidian |
| `public-obsidian-obsidian-cli` | no | 0.4887 | 0.3954 | 0.5749 | yes | create, obsidian, note, cli, command | create, obsidian |
| `public-mattpocock-obsidian-vault` | no | 0.4887 | 0.3799 | 0.4332 | no | create, obsidian, note | create, obsidian |

Top similarity neighbours: `public-huggingface-huggingface-papers` (0.494), `public-obsidian-json-canvas` (0.489), `method-note-builder` (0.471), `citation-note-extractor` (0.469), `document-extractor` (0.456)

### `public_gold_p71_obsidian_bases`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-bases`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-obsidian-json-canvas` | no | 0.4847 | 0.4480 | 0.5832 | yes | obsidian, create, json, canva | obsidian, file, create, edit, work, creat, mention |
| `public-obsidian-obsidian-markdown` | no | 0.4847 | 0.4617 | 0.7588 | yes | obsidian, note, tags, create | obsidian, file, create, edit, work, note, mention |
| `public-oh-my-obsidian-plugin` | no | 0.4847 | 0.2366 | 0.5761 | yes | - | - |
| `public-office-notion-automation` | no | 0.4847 | 0.2572 | 0.3469 | no | - | - |

Top similarity neighbours: `public-obsidian-obsidian-cli` (0.630), `public-mattpocock-obsidian-vault` (0.540), `public-obsidian-obsidian-bases` (0.485), `public-obsidian-obsidian-markdown` (0.462), `public-office-obsidian-automation` (0.450)

### `public_gold_p72_obsidian_cli`

- Family: `public_gold_validation`
- Gold skill: `public-obsidian-obsidian-cli`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-obsidian-json-canvas` | no | 0.6585 | 0.3477 | 0.5749 | yes | create, obsidian, canva, file | obsidian, create |
| `public-obsidian-obsidian-bases` | no | 0.6585 | 0.4281 | 0.6554 | yes | create, note, obsidian, file | obsidian, note, create |
| `public-oh-my-obsidian-cli` | yes | 0.6585 | 0.2603 | 0.6905 | yes | - | - |
| `public-mattpocock-obsidian-vault` | yes | 0.6585 | 0.5370 | 0.6737 | yes | create, vault, note, obsidian | obsidian, vault, search, manage, note, create |

Top similarity neighbours: `public-obsidian-obsidian-cli` (0.658), `public-mattpocock-obsidian-vault` (0.537), `public-obsidian-obsidian-markdown` (0.475), `public-office-obsidian-automation` (0.431), `public-obsidian-obsidian-bases` (0.428)

### `public_gold_p73_excel_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-excel-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 23

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-sheets-automation` | no | 0.3416 | 0.4223 | 0.6111 | yes | google, sheet, data | - |
| `public-office-data-analysis` | no | 0.3416 | 0.5043 | 0.5948 | yes | excel, analysi, data | - |
| `public-office-xlsx-manipulation` | yes | 0.3416 | 0.3370 | 0.6282 | yes | excel | - |
| `xlsx-formula-model-builder` | yes | 0.3416 | 0.6059 | 0.4595 | yes | formula, output, sheet | - |

Top similarity neighbours: `xlsx-formula-model-builder` (0.606), `data-analysis-overview` (0.514), `public-office-data-analysis` (0.504), `spreadsheet-formula-auditor` (0.503), `data-analysis-for-reporting` (0.463)

### `public_gold_p74_sheets_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-sheets-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-data-analysis` | no | 0.5691 | 0.4400 | 0.6749 | yes | excel | data, report |
| `public-office-data-pipeline` | no | 0.5691 | 0.4074 | 0.7034 | yes | workflow | automation, workflow, data, integration |
| `public-office-excel-automation` | yes | 0.5691 | 0.4396 | 0.6111 | yes | - | - |
| `public-office-xlsx-manipulation` | yes | 0.5691 | 0.5091 | 0.4584 | yes | excel | - |

Top similarity neighbours: `xlsx-formula-model-builder` (0.707), `public-xlsx` (0.570), `public-office-sheets-automation` (0.569), `public-swebench-xlsx` (0.557), `public-office-xlsx-manipulation` (0.509)

### `public_gold_p75_airtable_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-airtable-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | no | 0.5773 | 0.2915 | 0.6615 | yes | automation, notion, workflow | automation, database, integration, workflow |
| `public-office-crm-automation` | no | 0.5773 | 0.3529 | 0.6067 | yes | automation, crm, workflow | automation, workflow |
| `public-office-sheets-automation` | no | 0.5773 | 0.2711 | 0.6410 | yes | automation, workflow | automation, integration, workflow |
| `airtable-workflow-automator` | yes | 0.5773 | 0.6185 | 0.8337 | yes | airtable, automation, workflow | automation, airtable, view, integration, workflow, trigger |

Top similarity neighbours: `airtable-workflow-automator` (0.619), `public-office-airtable-automation` (0.577), `public-office-webhook-automation` (0.362), `public-office-crm-automation` (0.353), `public-office-podcast-automation` (0.342)

### `public_gold_p76_invoice_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-invoice-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-invoice-organizer` | no | 0.6589 | 0.4625 | 0.7035 | yes | invoice | invoice, track |
| `public-office-quickbooks-automation` | no | 0.6589 | 0.5644 | 0.7754 | yes | automate, workflow | automate, reconciliation, account |
| `public-office-expense-report` | no | 0.6589 | 0.1617 | 0.5053 | yes | - | - |
| `public-office-invoice-generator` | yes | 0.6589 | 0.5652 | 0.7227 | yes | invoice | invoice |

Top similarity neighbours: `public-office-invoice-automation` (0.659), `public-office-invoice-generator` (0.565), `public-office-quickbooks-automation` (0.564), `invoice-payment-checker` (0.549), `public-office-invoice-template` (0.507)

### `public_gold_p77_lead_routing`

- Family: `public_gold_validation`
- Gold skill: `public-office-lead-routing`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-lead-qualification` | no | 0.5479 | 0.3747 | 0.5100 | yes | lead, bas, qualify | lead |
| `public-office-lead-research` | no | 0.5479 | 0.4468 | 0.4818 | no | sale, company, research | - |
| `public-office-crm-automation` | no | 0.5479 | 0.2523 | 0.5203 | yes | lead | lead |
| `public-office-pipedrive-automation` | no | 0.5479 | 0.2659 | 0.4034 | no | sale | - |

Top similarity neighbours: `public-office-lead-routing` (0.548), `public-office-lead-research` (0.447), `public-office-amazon-seller` (0.419), `sales-ops-summary-writer` (0.410), `ecommerce-ops-summary-writer` (0.401)

### `public_gold_p78_saas_metrics`

- Family: `public_gold_validation`
- Gold skill: `public-office-saas-metrics`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-dcf-valuation` | no | 0.7300 | 0.5340 | 0.4875 | no | calculate, build, dcf, valuation, report | report |
| `public-office-financial-modeling` | no | 0.7300 | 0.3171 | 0.5137 | yes | build | - |
| `public-office-stock-analysis` | no | 0.7300 | 0.3083 | 0.5582 | yes | metric, stock, analysi, report | analysi, metric, report |
| `public-office-data-analysis` | no | 0.7300 | 0.2397 | 0.5031 | yes | build, analysi, report | analysi, report |

Top similarity neighbours: `public-office-saas-metrics` (0.730), `public-office-subscription-management` (0.576), `public-office-dcf-valuation` (0.534), `public-swebench-risk-metrics-calculation` (0.427), `public-swebench-creating-financial-models` (0.378)

### `public_gold_p79_stock_analysis`

- Family: `public_gold_validation`
- Gold skill: `public-office-stock-analysis`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-dcf-valuation` | no | 0.5550 | 0.4723 | 0.4347 | yes | valuation, report, build, dcf | generate, report |
| `public-office-investment-memo` | no | 0.5550 | 0.3591 | 0.5750 | yes | risk, investment, write | market, investment |
| `public-office-crypto-report` | no | 0.5550 | 0.5575 | 0.5277 | yes | analysi, crypto, report | analysi, market, generate, report, metric |
| `public-office-company-research` | no | 0.5550 | 0.3409 | 0.6146 | yes | analysi | analysi, market |

Top similarity neighbours: `public-office-crypto-report` (0.557), `public-office-stock-analysis` (0.555), `public-office-dcf-valuation` (0.472), `finance-ops-summary-writer` (0.442), `public-office-saas-metrics` (0.421)

### `public_gold_p80_dcf_valuation`

- Family: `public_gold_validation`
- Gold skill: `public-office-dcf-valuation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-stock-analysis` | no | 0.6991 | 0.3734 | 0.4347 | no | stock | generate, report |
| `public-office-financial-modeling` | no | 0.6991 | 0.3923 | 0.5571 | yes | build | build, cash, flow, model |
| `public-office-investment-memo` | no | 0.6991 | 0.4292 | 0.4982 | no | write | professional |
| `public-swebench-creating-financial-models` | no | 0.6991 | 0.4737 | 0.5933 | yes | dcf, sensitivity | dcf, model |

Top similarity neighbours: `public-office-dcf-valuation` (0.699), `public-swebench-creating-financial-models` (0.474), `public-office-investment-memo` (0.429), `finance-ops-summary-writer` (0.406), `public-office-financial-modeling` (0.392)

### `public_gold_p81_shopify_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-shopify-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-woocommerce-automation` | no | 0.6467 | 0.5785 | 0.7484 | yes | automate, e-commerce, operation, includ, inventory, order, customer, woocommerce | e-commerce, inventory, order, customer |
| `public-office-stripe-payments` | no | 0.6467 | 0.3324 | 0.5549 | yes | automate, management, process, stripe, payment | management, process |
| `public-office-amazon-seller` | no | 0.6467 | 0.4154 | 0.6546 | yes | automate, operation, includ, inventory, management, order, amazon, seller | inventory, management, order |
| `public-office-invoice-automation` | no | 0.6467 | 0.3852 | 0.6164 | yes | automate, payment | - |

Top similarity neighbours: `public-office-shopify-automation` (0.647), `public-office-woocommerce-automation` (0.579), `public-office-spotify-automation` (0.432), `ecommerce-ops-monitoring-plan-builder` (0.426), `public-office-crm-automation` (0.417)

### `public_gold_p82_zendesk_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-zendesk-automation`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-intercom-automation` | no | 0.6884 | 0.4955 | 0.5107 | yes | automate, support, intercom | automate, customer, support, workflow |
| `public-office-customer-success` | no | 0.6884 | 0.2139 | 0.3447 | no | - | customer, management |
| `public-office-email-classifier` | no | 0.6884 | 0.2775 | 0.3070 | no | email | - |
| `public-office-slack-workflows` | no | 0.6884 | 0.4288 | 0.4485 | no | slack, automation | workflow |
| `support-ticket-triager` | no | 0.6884 | 0.4020 | 0.4560 | no | ticket, support | support, ticket, rout |
| `support-ops-monitoring-plan-builder` | no | 0.6884 | 0.3677 | 0.4617 | no | escalation, support, build | customer, support |
| `public-office-crm-automation` | no | 0.6884 | 0.3689 | 0.5652 | yes | automation | workflow, management |

Top similarity neighbours: `public-office-zendesk-automation` (0.688), `public-office-intercom-automation` (0.495), `webhook-integration-planner` (0.452), `public-office-obsidian-automation` (0.444), `webhook-setup-planner` (0.442)

### `public_gold_p83_web_seo`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-seo`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 5

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-web-quality-audit` | no | 0.4657 | 0.4086 | 0.6184 | yes | page, performance, accessibility, audit | optimize, ask, seo |
| `public-addy-web-best-practices` | no | 0.4657 | 0.2666 | 0.5454 | yes | audit | ask |
| `public-addy-web-performance` | no | 0.4657 | 0.3345 | 0.7418 | yes | improve, page, fix, performance, audit | optimize, ask, improve, fix |
| `public-office-seo-optimizer` | yes | 0.4657 | 0.4413 | 0.7681 | yes | audit | optimization, rank, seo |

Top similarity neighbours: `seo-ops-quality-auditor` (0.532), `seo-ops-evidence-grounder` (0.506), `public-office-web-search` (0.489), `seo-metadata-checker` (0.484), `public-addy-web-seo` (0.466)

### `public_gold_p84_web_performance`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-performance`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-core-web-vitals` | no | 0.6070 | 0.4821 | 0.6495 | yes | web, lcp, inp, cls | optimize, web, better, experience, ask, reduce, fix, improve |
| `public-addy-web-web-quality-audit` | no | 0.6070 | 0.3304 | 0.6769 | yes | web | performance, optimize, web, ask, site, page, audit |
| `public-addy-agent-browser-testing-with-devtools` | no | 0.6070 | 0.4275 | 0.4316 | no | runtime, browser, test | performance |
| `public-addy-agent-performance-optimization` | no | 0.6070 | 0.5364 | 0.7709 | yes | web, profil, load, time, bottleneck | performance, load, optimize, web, time, fix |

Top similarity neighbours: `web-performance-budget-checker` (0.613), `public-addy-web-performance` (0.607), `public-addy-agent-performance-optimization` (0.536), `public-addy-web-core-web-vitals` (0.482), `public-anthropic-webapp-testing` (0.471)

### `public_gold_p85_web_quality_audit`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-web-quality-audit`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | no | 0.4682 | 0.4481 | 0.6057 | yes | accessibility | audit, web, accessibility, ask |
| `public-addy-web-core-web-vitals` | no | 0.4682 | 0.3146 | 0.5805 | yes | search | web, ask, page, optimize |
| `public-addy-web-seo` | no | 0.4682 | 0.3993 | 0.6184 | yes | search, visibility, seo | seo, ask, optimize |
| `public-addy-web-best-practices` | no | 0.4682 | 0.3573 | 0.7283 | yes | review, security, compatibility, practice | quality, audit, web, best, practice, ask, review, check |

Top similarity neighbours: `accessibility-interaction-auditor` (0.514), `seo-ops-risk-reviewer` (0.495), `psc-accessibility-interaction-auditor` (0.481), `public-addy-web-web-quality-audit` (0.468), `accessibility-checker` (0.466)

### `public_gold_p86_web_best_practices`

- Family: `public_gold_validation`
- Gold skill: `public-addy-web-best-practices`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-addy-web-accessibility` | no | 0.6356 | 0.4463 | 0.5311 | yes | web, audit | web, ask, audit |
| `public-addy-web-performance` | no | 0.6356 | 0.4490 | 0.6306 | yes | site, web, performance, audit | web, ask, audit |
| `public-openai-security-best-practices` | no | 0.6356 | 0.3963 | 0.6675 | yes | review, best, practice | code, best, practice, security, review |
| `public-addy-web-web-quality-audit` | yes | 0.6356 | 0.5571 | 0.7283 | yes | review, site, web, best, practice, run, performance, audit | best, practice, quality, web, ask, audit, review, check |

Top similarity neighbours: `public-addy-web-best-practices` (0.636), `public-addy-web-web-quality-audit` (0.557), `web-performance-budget-checker` (0.549), `web-ops-risk-reviewer` (0.515), `web-ops-quality-auditor` (0.496)

### `public_gold_p87_api_design_principles`

- Family: `public_gold_validation`
- Gold skill: `public-api-design-principles`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | no | 0.5142 | 0.7323 | 0.4958 | yes | contract, pagination, error, review, openapi | review |
| `public-oh-my-api-design` | yes | 0.5142 | 0.2288 | 0.4402 | yes | - | - |
| `rest-api-contract-designer` | yes | 0.5142 | 0.5781 | 0.5119 | yes | design, rest, api, resource, pagination, error | api, design, rest |
| `public-addy-agent-api-and-interface-design` | yes | 0.5142 | 0.4793 | 0.7135 | yes | design, rest, api, contract | api, design, apis, rest, graphql, establish |

Top similarity neighbours: `openapi-contract-reviewer` (0.732), `openapi-contract-tester` (0.582), `rest-api-contract-designer` (0.578), `api-ops-summary-writer` (0.522), `api-design-reviewer` (0.514)

### `public_gold_p88_interface_design`

- Family: `public_gold_validation`
- Gold skill: `public-addy-agent-api-and-interface-design`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-api-design-principles` | no | 0.5971 | 0.4382 | 0.7135 | yes | api, design, rest | design, api, apis, rest, graphql, establish |
| `public-architecture-patterns` | no | 0.5971 | 0.3919 | 0.5855 | yes | design, includ, backend, architecture, pattern | design, backend |
| `api-design-reviewer` | no | 0.5971 | 0.3678 | 0.5373 | yes | api, design, rest | design, api, rest, graphql |
| `rest-api-contract-designer` | no | 0.5971 | 0.4723 | 0.4825 | no | api, design, rest, endpoint | design, api, rest, endpoint |

Top similarity neighbours: `public-addy-agent-api-and-interface-design` (0.597), `openapi-contract-reviewer` (0.507), `external-api-integration-planner` (0.483), `rest-api-contract-designer` (0.472), `architecture-boundary-reviewer` (0.465)

### `public_gold_p89_api_documentation`

- Family: `public_gold_validation`
- Gold skill: `public-oh-my-api-documentation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 38

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-api-design-principles` | no | 0.4010 | 0.3969 | 0.3640 | yes | api | - |
| `public-openai-openai-docs` | no | 0.4010 | 0.5952 | 0.5674 | yes | documentation, reference, case, openai, product, docs | - |
| `openapi-contract-reviewer` | no | 0.4010 | 0.6925 | 0.2285 | yes | example, contract, endpoint, error, behavior, openapi | - |
| `api-documentation-writer` | yes | 0.4010 | 0.5954 | 0.3534 | yes | api, example, note, contract, write, developer-fac, documentation, quickstart | - |

Top similarity neighbours: `openapi-contract-reviewer` (0.693), `api-documentation-writer` (0.595), `public-openai-openai-docs` (0.595), `openapi-contract-tester` (0.567), `public-openai-cli-creator` (0.558)

### `public_gold_p90_claude_api`

- Family: `public_gold_validation`
- Gold skill: `public-anthropic-claude-api`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-openai-docs` | no | 0.7357 | 0.4780 | 0.5233 | yes | openai, docs, mcp | model, openai, build, asks, tool, citation |
| `public-office-ai-agent-builder` | no | 0.7357 | 0.4850 | 0.4894 | no | claude, integration, chatgpt | claude, build, agent, tool, memory |
| `public-anthropic-mcp-builder` | no | 0.7357 | 0.3843 | 0.2944 | no | sdk, mcp, server | sdk, model, build, tool |
| `public-openai-chatgpt-apps` | no | 0.7357 | 0.5806 | 0.3979 | no | sdk, openai, docs, chatgpt, apps, mcp, server | sdk, code, apps, openai, build, tool, project |
| `api-integration-planner` | no | 0.7357 | 0.4861 | 0.3882 | no | api, handl | api, rate |
| `external-api-integration-planner` | no | 0.7357 | 0.4766 | 0.3747 | no | api, integration, handl | api, rate |

Top similarity neighbours: `public-anthropic-claude-api` (0.736), `public-openai-chatgpt-apps` (0.581), `api-integration-planner` (0.486), `public-office-ai-agent-builder` (0.485), `public-openai-playwright` (0.483)

### `public_gold_p91_admin_api_endpoint`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-add-admin-api-endpoint`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-api-design-principles` | no | 0.6590 | 0.3276 | 0.2891 | no | api, design, rest | api, new |
| `rest-api-contract-designer` | no | 0.6590 | 0.4066 | 0.2212 | no | api, endpoint, design, rest, schema | endpoint, api |
| `public-swebench-add-malli-schemas` | no | 0.6590 | 0.4434 | 0.4747 | no | add, api, endpoint, pattern, malli, schema | endpoint, api, add |
| `api-security-threat-reviewer` | no | 0.6590 | 0.2846 | 0.2010 | no | api, design | api |

Top similarity neighbours: `public-swebench-add-admin-api-endpoint` (0.659), `public-swebench-add-malli-schemas` (0.443), `openapi-contract-reviewer` (0.413), `rest-api-contract-designer` (0.407), `public-openai-cli-creator` (0.396)

### `public_gold_p92_security_review`

- Family: `public_gold_validation`
- Gold skill: `public-swebench-security-review`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 20

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-security-best-practices` | no | 0.4702 | 0.4599 | 0.5670 | yes | review, code, general | security |
| `public-addy-agent-security-and-hardening` | no | 0.4702 | 0.4468 | 0.6257 | yes | code, authentication, input, handl, harden | authentication, handl, input, feature |
| `api-security-threat-reviewer` | no | 0.4702 | 0.5588 | 0.4990 | yes | review, authentication, input, api | authentication, input, api |
| `security-code-reviewer` | yes | 0.4702 | 0.6178 | 0.4895 | yes | review, code, diff, concrete | security |

Top similarity neighbours: `security-code-reviewer` (0.618), `repo-code-reviewer` (0.606), `psc-handler-vulnerability-reviewer` (0.563), `api-security-threat-reviewer` (0.559), `repo-ops-risk-reviewer` (0.540)

### `public_gold_p93_security_best_practices`

- Family: `public_gold_validation`
- Gold skill: `public-openai-security-best-practices`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-security-review` | no | 0.5898 | 0.4951 | 0.5670 | yes | provide, security, input, handl | security |
| `security-code-reviewer` | no | 0.5898 | 0.5963 | 0.4813 | yes | security, default, diff, concrete, vulnerabilitie | security, review, code |
| `public-oh-my-security-best-practices` | yes | 0.5898 | 0.3586 | 0.6465 | yes | - | - |
| `public-addy-agent-security-and-hardening` | yes | 0.5898 | 0.5292 | 0.6214 | yes | service, input, handl, vulnerabilitie | code |

Top similarity neighbours: `public-addy-web-best-practices` (0.604), `security-code-reviewer` (0.596), `public-openai-security-best-practices` (0.590), `psc-handler-vulnerability-reviewer` (0.577), `public-addy-agent-security-and-hardening` (0.529)

### `public_gold_p94_security_ownership_map`

- Family: `public_gold_validation`
- Gold skill: `public-openai-security-ownership-map`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-security-threat-model` | no | 0.7553 | 0.5085 | 0.4860 | no | threat, model | trigger, only, explicitly, code, general, non-security |
| `security-threat-modeler` | no | 0.7553 | 0.4235 | 0.3201 | no | build, security, threat, model | security, build |
| `public-office-security-monitoring` | no | 0.7553 | 0.3793 | 0.4298 | no | security, threat, monitor | security |
| `repo-code-reviewer` | no | 0.7553 | 0.4636 | 0.3234 | no | repository, risk | risk |

Top similarity neighbours: `public-openai-security-ownership-map` (0.755), `git-safety-guardrail-installer` (0.538), `public-security-threat-model` (0.508), `version-control-helper` (0.505), `public-n-skills-open-source-maintainer` (0.500)

### `public_gold_p95_security_monitoring`

- Family: `public_gold_validation`
- Gold skill: `public-office-security-monitoring`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-security-ownership-map` | no | 0.6139 | 0.5036 | 0.4298 | no | security, code, ownership | security |
| `public-security-threat-model` | no | 0.6139 | 0.5698 | 0.5838 | yes | threat, code, design, model | threat |
| `public-office-devops-automation` | no | 0.6139 | 0.4451 | 0.6882 | yes | monitor, workflow, incident | monitor, incident, workflow |
| `public-swebench-distributed-tracing` | no | 0.6139 | 0.3262 | 0.3678 | no | - | - |

Top similarity neighbours: `public-office-security-monitoring` (0.614), `public-security-threat-model` (0.570), `security-ops-dependency-mapper` (0.552), `security-ops-monitoring-plan-builder` (0.548), `security-ops-risk-reviewer` (0.524)

### `public_gold_p96_jira_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-jira-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-linear` | no | 0.7913 | 0.3641 | 0.4701 | no | project, issue, workflow, linear | project, workflow, issue |
| `public-office-linear-automation` | no | 0.7913 | 0.4561 | 0.6440 | yes | automate, issue, workflow, linear | automate, management, workflow, plann, issue, track |
| `public-office-trello-automation` | no | 0.7913 | 0.4251 | 0.5861 | yes | automate, workflow, trello | automate, management, workflow |
| `public-office-monday-automation` | no | 0.7913 | 0.4856 | 0.5975 | yes | automate, workflow, monday, com | automate, management, workflow |

Top similarity neighbours: `public-office-jira-automation` (0.791), `public-office-monday-automation` (0.486), `public-office-linear-automation` (0.456), `public-swebench-gitlab-ci-patterns` (0.429), `public-office-asana-automation` (0.427)

### `public_gold_p97_linear_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-linear-automation`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-jira-automation` | no | 0.7192 | 0.5952 | 0.6440 | yes | automate, issue, track, workflow, report, jira | automate, issue, track, plann, management, workflow |
| `public-office-trello-automation` | no | 0.7192 | 0.4798 | 0.6562 | yes | automate, workflow, trello | automate, management, workflow |
| `public-office-clickup-automation` | no | 0.7192 | 0.5594 | 0.6608 | yes | automate, track, workflow, workspace, clickup | automate, track, management, workflow |
| `public-openai-linear` | yes | 0.7192 | 0.4501 | 0.5784 | yes | linear, issue, update, workflow | linear, issue, workflow |

Top similarity neighbours: `public-office-linear-automation` (0.719), `public-office-jira-automation` (0.595), `public-office-clickup-automation` (0.559), `public-office-sheets-automation` (0.501), `airtable-workflow-automator` (0.489)

### `public_gold_p98_trello_automation`

- Family: `public_gold_validation`
- Gold skill: `public-office-trello-automation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-jira-automation` | no | 0.5706 | 0.4801 | 0.5861 | yes | automate, jira | automate, management, workflow |
| `public-office-linear-automation` | no | 0.5706 | 0.3961 | 0.6562 | yes | automate, linear | automate, management, workflow |
| `public-office-asana-automation` | no | 0.5706 | 0.3429 | 0.6039 | yes | automate, team, collaboration, asana | automate, management, workflow, team, collaboration |

Top similarity neighbours: `public-office-trello-automation` (0.571), `public-office-monday-automation` (0.506), `public-office-jira-automation` (0.480), `public-office-linear-automation` (0.396), `weekly-planner` (0.344)

### `public_gold_p99_slack_workflows`

- Family: `public_gold_validation`
- Gold skill: `public-office-slack-workflows`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-microsoft-teams` | no | 0.7571 | 0.5535 | 0.6552 | yes | workflow, channel, microsoft, team | workflow, integration |
| `public-office-twilio-sms` | no | 0.7571 | 0.4814 | 0.4933 | no | workflow, notification, sms | workflow, notification |
| `public-office-whatsapp-automation` | no | 0.7571 | 0.5097 | 0.6347 | yes | automation, notification, whatsapp | automation, notification |
| `public-office-telegram-bot` | no | 0.7571 | 0.5527 | 0.7006 | yes | automation, notification, telegram | automation, notification |

Top similarity neighbours: `public-office-slack-workflows` (0.757), `public-office-microsoft-teams` (0.553), `public-office-telegram-bot` (0.553), `public-office-calendar-automation` (0.523), `public-office-whatsapp-automation` (0.510)

