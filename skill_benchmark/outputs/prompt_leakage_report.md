# Prompt Leakage Report

This report checks whether prompts accidentally reveal the gold skill through exact skill names, dominant skill-title words, or copied phrases from the gold skill card.

## Overall Status

- Prompt leakage status: **PASS**
- Total prompts: 85
- Critical exact-name leaks: 0
- High-risk title/phrase leaks: 0
- Critical risk prompts: 0
- High risk prompts: 0
- Medium risk prompts: 6
- Low risk prompts: 79

Interpretation: critical leaks are exact gold skill-name leaks. High-risk cases usually contain distinctive gold title words or copied gold-card phrases that may make lexical selectors look better than they really are.

## Family Summary

| Family | Critical | High | Medium | Low |
|---|---:|---:|---:|---:|
| `api_backend_design` | 0 | 0 | 0 | 6 |
| `browser_web_automation` | 0 | 0 | 0 | 6 |
| `code_github_workflow` | 0 | 0 | 2 | 4 |
| `data_spreadsheet` | 0 | 0 | 0 | 7 |
| `deployment_browser_qa` | 0 | 0 | 0 | 6 |
| `documents_files` | 0 | 0 | 0 | 7 |
| `metrics_observability` | 0 | 0 | 1 | 5 |
| `news_monitoring` | 0 | 0 | 2 | 3 |
| `office_artifact_workflows` | 0 | 0 | 0 | 6 |
| `planning_meetings` | 0 | 0 | 0 | 5 |
| `reading_research` | 0 | 0 | 0 | 8 |
| `reply_messaging` | 0 | 0 | 1 | 4 |
| `security_appsec` | 0 | 0 | 0 | 6 |
| `skill_lifecycle` | 0 | 0 | 0 | 6 |

## Prompts To Review

| Risk | Prompt | Gold | Gold title hits | Advantage | Shared phrase | Flags |
|---|---|---|---|---:|---|---|
| medium | `code_p2_pr_review` | `pr-reviewer` | review | 0.50 | - | - |
| medium | `code_p3_review_comment_resolution` | `review-comment-resolver` | review, comment, resolv | 0.00 | - | complete_gold_title_overlap |
| medium | `obs_p4_capacity_risk` | `capacity-risk-forecaster` | capacity, risk, forecast | 0.33 | - | complete_gold_title_overlap |
| medium | `news_p4_theme_extraction` | `news-theme-extractor` | news, theme, extract | 0.25 | - | complete_gold_title_overlap |
| medium | `news_p5_trend_signal` | `tech-news-trend-extractor` | tech, news, trend | 0.42 | - | - |
| medium | `reply_p1_professor_reply` | `professor-email-reply` | profess, email, reply | 0.00 | respectful academic email reply | complete_gold_title_overlap |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please review billing_openapi.yaml as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: contract, review
- Longest copied gold phrase: schema example statu code auth

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.
- Gold title overlap: 0.25; max alternative title overlap: 0.33; advantage: -0.08
- Gold title hits: api
- Longest copied gold phrase: -

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: -

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please review service_modules.md for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: architecture, review
- Longest copied gold phrase: -

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please assess add_subscription_status_migration.sql before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: risk
- Longest copied gold phrase: app version rollback path

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please trace how the billing, notification, account, and analytics services rely on each other using service_trace_notes.md. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: service
- Longest copied gold phrase: -

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Open the staging dashboard and capture a page snapshot of what the user sees on the account settings page right now. I need the visible state, screenshot-style observations, and any obvious rendering issue; do not click through a full interaction test.
- Gold title overlap: 0.33; max alternative title overlap: 0.50; advantage: -0.17
- Gold title hits: page
- Longest copied gold phrase: -

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Go through the demo signup flow and fill in the form fields with the sample details I provided. Report which fields were entered and pause before final submission if it would create a real account. This is delegated browser form completion, not expected-versus-actual UI validation or a general test report.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: form, fill
- Longest copied gold phrase: -

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Test whether the checkout page correctly shows a validation message when the postcode field is empty, and report the expected versus actual behavior.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: test
- Longest copied gold phrase: -

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: From this product listing page, extract the product names, prices, availability labels, and detail-page links into a structured table. I do not need a screenshot.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: extract
- Longest copied gold phrase: -

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The settings page opens but clicking Save does nothing, and the console shows `Cannot read properties of undefined (reading 'id')` after the profile API call. Use the UI symptom as evidence, then inspect the frontend event handler, state update path, and API response contract. The deliverable is the likely source-level cause plus the smallest code patch.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: frontend
- Longest copied gold phrase: -

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Evaluate the signup form for keyboard navigation, input labels, focus order, and whether screen-reader users can understand the error messages.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this local change before I commit it. The patch updates the cache key from `user.id` to `user.email`, adds a fallback for missing names, and changes the unit test fixture. I want to know if this could introduce bugs or missing-test risk, not have you rewrite it yet.
- Gold title overlap: 0.50; max alternative title overlap: 1.00; advantage: -0.50
- Gold title hits: review
- Longest copied gold phrase: -

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Can you review this pull request as if you were leaving PR feedback? It changes the auth middleware, adds a migration, updates two API tests, and the PR discussion says the branch is meant to preserve backward compatibility.
- Gold title overlap: 1.00; max alternative title overlap: 0.50; advantage: 0.50
- Gold title hits: review
- Longest copied gold phrase: -

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Risk level: **medium**
- Risk flags: complete_gold_title_overlap
- Instruction used for scoring: I already got review comments on this branch. Please address this specific reviewer request by planning and making the requested code/test change: `The retry loop can spin forever if the response is 429 and Retry-After is missing. Please add a cap and a test.` I need the existing comment resolved with an implementation response, not a fresh PR review or CI debugging.
- Gold title overlap: 1.00; max alternative title overlap: 1.00; advantage: 0.00
- Gold title hits: review, comment, resolv
- Longest copied gold phrase: -

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The CI run failed after my last commit. The failing job is `unit-tests`, and the first useful error says `Expected status 200, received 401` in `auth.middleware.test.ts` after the token refresh change. Help me find the cause and the smallest fix.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn these completed changes into a concise internal changelog entry for the repository changelog, grouped by change type if useful: fixed retry timeout handling, added token-refresh tests, improved cache invalidation for renamed users, and removed an unused feature flag. Do not write user-facing release notes.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: changelog
- Longest copied gold phrase: -

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write user-facing release notes for this update. We improved sign-in reliability when sessions expire, made profile changes appear faster across devices, and fixed a retry issue that could delay requests during temporary service pressure.
- Gold title overlap: 0.67; max alternative title overlap: 0.00; advantage: 0.67
- Gold title hits: release, note
- Longest copied gold phrase: -

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. I need a broad exploratory orientation: what the sheet contains, the overall picture, the main patterns, the most useful caveats, and a few sensible next questions. Do not turn it into an executive report, forecast, ranking recommendation, or diagnosis of one specific problem yet.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. Build an anomaly watchlist: which spikes, dips, outliers, or concentrated deviations look most worth worrying about, and how confident should I be that each one is real? Do not explain root cause yet.
- Gold title overlap: 0.25; max alternative title overlap: 0.40; advantage: -0.15
- Gold title hits: anomaly
- Longest copied gold phrase: -

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. Before I react to it, audit whether the numbers are trustworthy: check for missing values, inconsistent rows, suspicious outliers, denominator issues, or measurement artifacts that could make a genuine problem look worse than it is.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. This seems to be getting worse. Assume the data is usable enough for analysis and trace the most likely driver: which channel, metric, or segment appears to explain the degradation, and what evidence supports that diagnosis?
- Gold title overlap: 0.60; max alternative title overlap: 0.67; advantage: -0.07
- Gold title hits: data, analysi, diagnose
- Longest copied gold phrase: -

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. Turn this into an upward-facing reporting brief: a headline, two or three executive takeaways, the clearest supporting numbers, and one caveat. Do not give me a broad exploratory analysis.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: analysi, report
- Longest copied gold phrase: -

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read channel_performance_weekly.csv. Forecast the likely next direction if the current pattern keeps going: what seems likely to happen next, what evidence supports that continuation, and how much should I trust the forecast?
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: forecast
- Longest copied gold phrase: -

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read pilot_priority_options.csv. Compare the options, rank them for action now, recommend the first choice, explain the decision criteria and trade-offs behind that ordering, and say what follow-up check would reduce decision risk. This is a selection task, not a forecast of one metric or a broad overview.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: rank, selection
- Longest copied gold phrase: -

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: flow
- Longest copied gold phrase: -

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please compare the baseline and current screenshots for pricing_page_desktop.png and pricing_page_mobile.png. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: visual, regression
- Longest copied gold phrase: compare baseline current screenshot

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.
- Gold title overlap: 0.67; max alternative title overlap: 0.00; advantage: 0.67
- Gold title hits: interaction, audit
- Longest copied gold phrase: accessible name aria state

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The Netlify deploy for build_log.txt failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: build
- Longest copied gold phrase: -

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: release
- Longest copied gold phrase: -

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please review lighthouse_trace_summary.txt against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: performance, budget
- Longest copied gold phrase: -

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read internal_travel_policy_update.txt and help me make sense of it quickly. I want the main point, the most important details, and anything I should pay attention to.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read travel_request_note_raw.txt and produce a revised full prose version for a human reader. Keep it as continuous paragraphs in the same document form, improve wording, flow, and polish, and preserve the same meaning and commitments.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: document
- Longest copied gold phrase: -

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read travel_request_note_raw.txt and normalise the document structure: keep the original wording and order as much as possible, but fix inconsistent headings, spacing, list style, and layout noise. Do not substantially rewrite the prose.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: document
- Longest copied gold phrase: -

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read invoice_northbridge_supplies.txt and extract the reusable fields into a structured table, including supplier, invoice number, dates, line items, totals, and payment details. Do not write a narrative summary.
- Gold title overlap: 0.67; max alternative title overlap: 0.00; advantage: 0.67
- Gold title hits: field, extract
- Longest copied gold phrase: -

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read policy_draft_a.txt and policy_draft_b.txt, then prepare a side-by-side comparison matrix so I can quickly see matching sections, changed wording, additions, removals, and unresolved differences.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: comparison
- Longest copied gold phrase: -

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read request_form.txt and convert the whole form into clean markdown notes I can drop into my repo. Preserve the content and labels, but simplify the source formatting rather than keeping the exact visual layout.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: convert
- Longest copied gold phrase: -

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please read request_form.txt and turn it into markdown while preserving the layout cues: headings, labels, rows, and grouped fields should remain recognizable. The priority is layout fidelity, not just simplified notes.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: layout, preserv
- Longest copied gold phrase: label rows group field

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Give me a triage overview of this service snapshot
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: overview
- Longest copied gold phrase: -

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Run an anomaly-focused readout on this service snapshot. Identify unusual performance behavior, especially tail-latency spikes, outliers, and whether the deviation is broad or concentrated in a smaller slice of requests. Do not give only a general metrics overview
- Gold title overlap: 0.00; max alternative title overlap: 1.00; advantage: -1.00
- Gold title hits: -
- Longest copied gold phrase: -

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Check this service snapshot against a reliability-objective risk frame
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: check
- Longest copied gold phrase: -

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Risk level: **medium**
- Risk flags: complete_gold_title_overlap
- Instruction used for scoring: Forecast capacity risk from this service snapshot if the pattern keeps going. Focus on future pressure, saturation risk, queue growth, headroom, and likely bottlenecks that could turn into a bigger operational problem. Do not decide current SLO breach or root cause
- Gold title overlap: 1.00; max alternative title overlap: 0.67; advantage: 0.33
- Gold title hits: capacity, risk, forecast
- Longest copied gold phrase: -

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Do a root-cause diagnosis for this service snapshot. Compare hypotheses such as downstream dependency latency, queue buildup, CPU pressure, and request mix; identify the most plausible driver of the degradation; and tie the diagnosis to evidence. Snapshot data
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn this service snapshot into an incident update I could quickly share with the team
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: incident
- Longest copied gold phrase: -

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Summarise this news article in a straightforward neutral recap
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: news
- Longest copied gold phrase: -

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn this article into a short decision memo with clear sections for the key event, current state of play, significance now, affected parties, and follow-up signals. The output should support quick situation awareness, not just summarize the article chronologically
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: From this article, identify the source-backed claims and facts, including important product details, named companies or people, and any figures or stated plans
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Risk level: **medium**
- Risk flags: complete_gold_title_overlap
- Instruction used for scoring: Extract the recurring themes across these three tech news snippets, grouping repeated ideas without forecasting market direction. Snippet 1
- Gold title overlap: 1.00; max alternative title overlap: 0.75; advantage: 0.25
- Gold title hits: news, theme, extract
- Longest copied gold phrase: -

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Identify which patterns across these three tech news snippets look like actionable tech trend signals right now, why they matter strategically, and what evidence would confirm or weaken the trend. Snippet 1
- Gold title overlap: 0.75; max alternative title overlap: 0.33; advantage: 0.42
- Gold title hits: tech, news, trend
- Longest copied gold phrase: -

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please inspect grant_application_packet.pdf as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. Do not just extract the fields.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: pdf, layout
- Longest copied gold phrase: -

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please recover the text from scanned_receipts_packet.pdf. It looks like image scans, so keep page numbers and mark uncertain OCR text instead of pretending every amount is reliable.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: pdf, ocr
- Longest copied gold phrase: -

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please review vendor_agreement_draft.docx as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: docx, edit
- Longest copied gold phrase: -

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please check pricing_model.xlsx for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.
- Gold title overlap: 0.00; max alternative title overlap: 0.50; advantage: -0.50
- Gold title hits: -
- Longest copied gold phrase: -

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please review thesis_proposal_deck.pptx for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.
- Gold title overlap: 0.25; max alternative title overlap: 0.50; advantage: -0.25
- Gold title hits: visual
- Longest copied gold phrase: -

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please convert project_brief.docx into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but do not create tracked changes or a layout audit.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: markdown, convert
- Longest copied gold phrase: -

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I have a short group project meeting tomorrow for a class presentation on AI study assistants. Please turn these topics into an agenda for that upcoming meeting: who will cover the demo, who will finish the slides, what risks could delay us before Friday, and what we need to prepare before the next check-in. The output should guide the meeting discussion, not schedule my whole week or only extract tasks.
- Gold title overlap: 0.67; max alternative title overlap: 1.00; advantage: -0.33
- Gold title hits: meet, agenda
- Longest copied gold phrase: -

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Summarise these meeting notes into a clean meeting recap
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: meet, summary
- Longest copied gold phrase: -

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I need something clean from these meeting notes so I can quickly see what needs to happen next and what still needs attention
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: meet
- Longest copied gold phrase: -

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn these rough notes into a plain action-item list without scheduling the week and without treating them as completed meeting notes
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Help me make a realistic week-level plan with sequencing and time buffers. I need to finish the planning skill family, revise prompts for the reply cluster, prepare for a Tuesday project meeting about collaborating on a prototype and brainstorming test cases for a multi-agent system, review two papers, send my supervisor a grounded summary by Thursday, and leave time for benchmark testing. I also have classes on Tuesday and Thursday afternoon. Do not just extract a raw task list or prepare a single meeting agenda.
- Gold title overlap: 0.50; max alternative title overlap: 1.00; advantage: -0.50
- Gold title hits: plann
- Longest copied gold phrase: -

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Give me a balanced research-oriented recap of this academic paper. I want the research problem, overall approach, main findings, and limitations in one readable summary, not citation-ready notes and not a method-only audit
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: pap
- Longest copied gold phrase: -

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Summarise this as a general source report rather than an academic paper. I need the context, main observations, practical recommendations, and evidence limits in plain language
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: general
- Longest copied gold phrase: -

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Make this source usable for me later when I'm writing by producing citation-ready notes
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: note
- Longest copied gold phrase: -

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Extract the specific details from this source into a structured table of fields and values
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: extract
- Longest copied gold phrase: -

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Help me make sense of this source by focusing on how the work was actually carried out, how it was evaluated, and what assumptions or constraints shaped the result
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I wrote this exact sentence from the source: 'Explicit task decomposition reliably improves agent performance in realistic environments.' Perform a citation-grounding support audit: mark which parts of the sentence are supported, overstated, or unsupported, explain the overreach, and give a safer revised sentence if needed.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compare these two sources in a side-by-side table with separate columns for Source A and Source B so I can clearly see how they line up, where they differ, and what each one contributes. Use rows such as approach, evaluation, strengths, limitations, and contribution; do not turn it into a synthesized related-work paragraph, method-only note, or citation-note list.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Synthesize these two sources into related-work style notes: explain the main approaches, how they relate, the shared research direction, and what remains unresolved across them. I want an integrated synthesis, not a side-by-side comparison table.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Risk level: **medium**
- Risk flags: complete_gold_title_overlap
- Instruction used for scoring: Draft a respectful academic email reply to this message from my professor, including availability and a polite tone suitable for a supervisor relationship: 'Hi Jacky, thanks for your update. Would you be available to meet next Tuesday afternoon to discuss the revised thesis scope? Please let me know what time suits you best.'
- Gold title overlap: 1.00; max alternative title overlap: 1.00; advantage: 0.00
- Gold title hits: profess, email, reply
- Longest copied gold phrase: respectful academic email reply

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Edit this already-written message only. Keep the same meaning, availability, and commitments, but improve flow, phrasing, tone, and readability. Return the refined version of this message.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: improve flow phras tone readability

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Draft a reply to these teammates about shared project coordination. The reply should clarify what I can take ownership of, confirm the deadline situation, and help the group move the work forward: 'Hey everyone, we need to lock in who is doing the slides, who is writing the report section, and whether we can still meet the Friday deadline. Can each of you confirm what you can finish by tomorrow?'
- Gold title overlap: 0.50; max alternative title overlap: 1.00; advantage: -0.50
- Gold title hits: reply
- Longest copied gold phrase: -

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write a response whose main purpose is to state my next actions clearly
- Gold title overlap: 0.33; max alternative title overlap: 0.50; advantage: -0.17
- Gold title hits: reply
- Longest copied gold phrase: -

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compose a concise new response from the source message only, confirming that I can send the requested file tomorrow. There is no existing reply text to polish, and I do not need a detailed action plan: 'Thanks for the update. Could you send me the file by tomorrow if possible?'
- Gold title overlap: 0.50; max alternative title overlap: 1.00; advantage: -0.50
- Gold title hits: reply
- Longest copied gold phrase: -

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: We are designing a new file-sharing feature where users can invite collaborators by email, generate public links, and revoke access later. Before implementation, reason across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: security
- Longest copied gold phrase: -

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this single API handler for concrete code-level security vulnerabilities and fixes tied to the implementation. It accepts `redirectUrl` from the request body, checks the current user, updates the user's profile, and redirects. Focus on handler-level flaws such as open redirects, unsafe validation, and incorrect access checks in this function.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: security, review
- Longest copied gold phrase: vulnerabilitie fixe tied implementation

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Check the risk of adding this new npm package. It has a broad dependency tree, a postinstall script, and the lockfile pulls in several old transitive packages. I need a dependency and supply-chain risk assessment.
- Gold title overlap: 0.67; max alternative title overlap: 0.00; advantage: 0.67
- Gold title hits: dependency, risk
- Longest copied gold phrase: -

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Look at this diff and tell me if I accidentally exposed anything sensitive: it adds `.env.example`, updates a deployment log, and includes strings that look like `sk_live_...`, a database URL, and a webhook signing secret.
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: secret
- Longest copied gold phrase: -

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Check whether this account-access change is safe. Users can refresh expired sessions, reset passwords by email link, and switch between workspace roles. I care about bypasses, stale permissions, and privilege escalation.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Assess the data-protection concerns in this analytics change. We want to log search queries, account region, user role, clicked filters, and partial email domains for 18 months so the product team can study usage patterns.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before I make anything new, search my existing capability library, shortlist available entries, assess fit and confidence, and decide whether one of them covers a workflow for turning messy meeting notes into action items and follow-up messages. I only want a reuse recommendation, not creation.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I found an existing spreadsheet-analysis capability in a public catalog and want it added to my active local library. Please fetch or prepare the package, verify the expected files, and report the source, local path, setup result, and any activation caveats.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create a new atomic skill for a repeated workflow: I often need to turn supervisor meeting notes into a thesis action list with owners, deadlines, and open questions. There is no existing skill for this exact workflow.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: skill
- Longest copied gold phrase: create new atomic skill

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: This existing skill's description is too broad and it keeps triggering for document summaries when it should only handle structured field extraction. Please revise the skill so its selection boundary is clearer.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: skill
- Longest copied gold phrase: -

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Test whether my `reply-polisher` skill actually triggers only when there is already a draft reply. I want an evaluation with realistic near-boundary prompts before deciding whether to edit it.
- Gold title overlap: 0.50; max alternative title overlap: 1.00; advantage: -0.50
- Gold title hits: skill
- Longest copied gold phrase: -

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I finished an existing `paper-summariser` skill and want to share it with someone else. Check the folder shape, metadata, resource links, and unnecessary files so it is package-ready.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: skill
- Longest copied gold phrase: -
