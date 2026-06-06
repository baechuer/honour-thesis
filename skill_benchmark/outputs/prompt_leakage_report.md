# Prompt Leakage Report

This report checks whether prompts accidentally reveal the gold skill through exact skill names, dominant skill-title words, or copied phrases from the gold skill card.

## Overall Status

- Prompt leakage status: **PASS**
- Total prompts: 201
- Critical exact-name leaks: 0
- High-risk title/phrase leaks: 0
- Critical risk prompts: 0
- High risk prompts: 0
- Medium risk prompts: 14
- Low risk prompts: 187

Interpretation: critical leaks are exact gold skill-name leaks. High-risk cases usually contain distinctive gold title words or copied gold-card phrases that may make lexical selectors look better than they really are.

## Family Summary

| Family | Critical | High | Medium | Low |
|---|---:|---:|---:|---:|
| `api_backend_design` | 0 | 0 | 0 | 6 |
| `api_mcp_tooling` | 0 | 0 | 0 | 6 |
| `browser_web_automation` | 0 | 0 | 0 | 6 |
| `code_github_workflow` | 0 | 0 | 2 | 4 |
| `data_spreadsheet` | 0 | 0 | 0 | 7 |
| `deployment_browser_qa` | 0 | 0 | 0 | 6 |
| `documents_files` | 0 | 0 | 0 | 7 |
| `github_ci_maintenance` | 0 | 0 | 0 | 6 |
| `huggingface_ml_workflows` | 0 | 0 | 0 | 6 |
| `implicit_field_stress` | 0 | 0 | 0 | 10 |
| `metrics_observability` | 0 | 0 | 1 | 5 |
| `news_monitoring` | 0 | 0 | 2 | 3 |
| `observability_reliability` | 0 | 0 | 1 | 5 |
| `office_artifact_workflows` | 0 | 0 | 0 | 6 |
| `office_business_automation` | 0 | 0 | 2 | 4 |
| `pdf_document_operations` | 0 | 0 | 1 | 5 |
| `planning_meetings` | 0 | 0 | 0 | 5 |
| `public_style_controlled` | 0 | 0 | 3 | 61 |
| `reading_research` | 0 | 0 | 0 | 8 |
| `reply_messaging` | 0 | 0 | 1 | 4 |
| `security_appsec` | 0 | 0 | 0 | 6 |
| `skill_lifecycle` | 0 | 0 | 0 | 6 |
| `skill_representation_analysis` | 0 | 0 | 1 | 5 |

## Prompts To Review

| Risk | Prompt | Gold | Gold title hits | Advantage | Shared phrase | Flags |
|---|---|---|---|---:|---|---|
| medium | `code_p2_pr_review` | `pr-reviewer` | review | 0.50 | - | - |
| medium | `code_p3_review_comment_resolution` | `review-comment-resolver` | review, comment, resolv | 0.00 | - | complete_gold_title_overlap |
| medium | `obs_p4_capacity_risk` | `capacity-risk-forecaster` | capacity, risk, forecast | 0.33 | - | complete_gold_title_overlap |
| medium | `news_p4_theme_extraction` | `news-theme-extractor` | news, theme, extract | 0.25 | - | complete_gold_title_overlap |
| medium | `news_p5_trend_signal` | `tech-news-trend-extractor` | tech, news, trend | 0.42 | - | - |
| medium | `observability_reliability_p4_slo_breach_narrative_writer` | `slo-breach-narrative-writer` | slo, breach, narrative | 0.08 | - | - |
| medium | `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | formula, model, build | 0.42 | build spreadsheet formula model | - |
| medium | `office_business_automation_p3_notion_research_database_builder` | `notion-research-database-builder` | notion, research, database | 0.35 | create notion research database | - |
| medium | `pdf_document_operations_p2_pdf_layout_table_extractor` | `pdf-layout-table-extractor` | pdf, table, extract | 0.08 | - | - |
| medium | `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer` | `psc-visual-screenshot-reviewer` | visual, screenshot, review | 0.50 | - | - |
| medium | `psc_security_appsec_p01_2_psc_feature_threat_modeler` | `psc-feature-threat-modeler` | feature, threat, model | 0.25 | - | - |
| medium | `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder` | `psc-anomaly-watchlist-builder` | anomaly, watchlist, build | 0.75 | - | - |
| medium | `reply_p1_professor_reply` | `professor-email-reply` | profess, email, reply | 0.00 | respectful academic email reply | complete_gold_title_overlap |
| medium | `skill_representation_analysis_p3_skill_router_policy_designer` | `skill-router-policy-designer` | skill, rout, policy, design | 0.33 | - | complete_gold_title_overlap |

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

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Family: `api_mcp_tooling`
- Gold skill: `rest-api-contract-designer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Specify a new client-facing HTTP interface for subscription invoices, including resources, endpoints, request and response shapes, status codes, pagination, and error examples. This is not an MCP wrapper.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: resource endpoint request reply

### `api_mcp_tooling_p2_mcp_server_builder`

- Family: `api_mcp_tooling`
- Gold skill: `mcp-server-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create an MCP server design that exposes two local file-inspection tools with narrow schemas and resource boundaries. Do not design a public REST API.
- Gold title overlap: 0.67; max alternative title overlap: 0.75; advantage: -0.08
- Gold title hits: mcp, serv
- Longest copied gold phrase: -

### `api_mcp_tooling_p3_webhook_integration_planner`

- Family: `api_mcp_tooling`
- Gold skill: `webhook-integration-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Plan webhook handling for payment events: accepted event types, signature checks, idempotency, retry behavior, ordering, and dead-letter storage.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: webhook
- Longest copied gold phrase: -

### `api_mcp_tooling_p4_auth_flow_integrator`

- Family: `api_mcp_tooling`
- Gold skill: `auth-flow-integrator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Integrate OAuth login for a dashboard app, covering scopes, token refresh, secret storage, logout, and authorization checks. Do not turn it into webhook planning.
- Gold title overlap: 0.00; max alternative title overlap: 0.67; advantage: -0.67
- Gold title hits: -
- Longest copied gold phrase: scope token refresh secret

### `api_mcp_tooling_p5_api_documentation_writer`

- Family: `api_mcp_tooling`
- Gold skill: `api-documentation-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write developer docs for the existing billing API contract in billing_contract.yaml, including quickstart, examples, auth notes, and errors.
- Gold title overlap: 0.33; max alternative title overlap: 0.50; advantage: -0.17
- Gold title hits: api
- Longest copied gold phrase: includ quickstart example auth note

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Family: `api_mcp_tooling`
- Gold skill: `api-security-threat-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Threat-review the billing API for authorization gaps, sensitive data exposure, rate-limit abuse, and validation risks. I need security findings, not user-facing docs.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: api, security
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

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Family: `github_ci_maintenance`
- Gold skill: `ci-log-root-cause-debugger`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Inspect ci_log.txt and identify the CI root cause, the first meaningful error, and the smallest rerun sequence.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: root, cause
- Longest copied gold phrase: -

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Family: `github_ci_maintenance`
- Gold skill: `pr-review-comment-resolver`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use pr_review_comments.md to plan how to resolve the review comments and what response to leave. Do not perform a general code review.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: review, comment
- Longest copied gold phrase: -

### `github_ci_maintenance_p3_repo_code_reviewer`

- Family: `github_ci_maintenance`
- Gold skill: `repo-code-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review the diff described in payment_diff.patch for bugs and missing tests. This is a fresh code review, not a CI log diagnosis.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: code, review
- Longest copied gold phrase: -

### `github_ci_maintenance_p4_github_issue_triager`

- Family: `github_ci_maintenance`
- Gold skill: `github-issue-triager`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Triage the issues in issues.md into bug/feature/support labels, priority, owner guess, and missing reproduction details.
- Gold title overlap: 0.33; max alternative title overlap: 0.00; advantage: 0.33
- Gold title hits: issue
- Longest copied gold phrase: -

### `github_ci_maintenance_p5_release_changelog_generator`

- Family: `github_ci_maintenance`
- Gold skill: `release-changelog-generator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn merged_prs.md into release notes grouped by features, fixes, and breaking changes. Do not review the code.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: release
- Longest copied gold phrase: -

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Family: `github_ci_maintenance`
- Gold skill: `git-safety-guardrail-installer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design repository guardrails to block accidental `git push`, `reset --hard`, and secret commits. I need hook/config steps and verification, not issue triage.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: git, guardrail
- Longest copied gold phrase: -

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-dataset-viewer-inspector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: For the dataset described in customer_tickets_dataset.md, inspect expected subsets, splits, columns, and row examples before we choose any model.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: dataset, inspect
- Longest copied gold phrase: subset split column row example

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-local-model-selector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I need a local model for classifying support tickets on an 8 GB Mac. Choose realistic Hugging Face/GGUF candidates and quantization options; do not design a dataset audit.
- Gold title overlap: 0.67; max alternative title overlap: 0.40; advantage: 0.27
- Gold title hits: local, model
- Longest copied gold phrase: -

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Family: `huggingface_ml_workflows`
- Gold skill: `sentence-transformer-finetuner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: We have labelled skill-query pairs and hard negatives for agent skill routing. Plan a sentence-transformer fine-tuning setup with losses, splits, and retrieval metrics.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Family: `huggingface_ml_workflows`
- Gold skill: `gradio-demo-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create a small Python web UI plan for a ticket classifier with a text box, confidence display, sample inputs, and launch checks. We already have the model; do not discuss fine-tuning.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-zerogpu-space-deployer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare our Gradio classifier for Hugging Face ZeroGPU Spaces. Focus on dependency files, GPU queue behavior, sleep constraints, and deployment verification.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: zerogpu, space
- Longest copied gold phrase: -

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-community-eval-runner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compare two Hugging Face classifiers on a held-out ticket dataset using reproducible metrics. I need an evaluation plan and result table, not a Gradio app.
- Gold title overlap: 0.00; max alternative title overlap: 0.33; advantage: -0.33
- Gold title hits: -
- Longest copied gold phrase: -

### `implicit_p1_pdf_answer`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-evidence-answerer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Read the PDF packet and answer whether travel meals after a delay are reimbursable. I need the answer and page evidence, not a reconstructed table.
- Gold title overlap: 0.50; max alternative title overlap: 0.75; advantage: -0.25
- Gold title hits: pdf, evidence
- Longest copied gold phrase: -

### `implicit_p2_pdf_table`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-table-reconstructor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Pull the invoice rows from the PDF with page and row anchors. Keep it as structured data rather than a prose answer.
- Gold title overlap: 0.25; max alternative title overlap: 0.33; advantage: -0.08
- Gold title hits: pdf
- Longest copied gold phrase: -

### `implicit_p3_browser_flow`

- Family: `implicit_field_stress`
- Gold skill: `implicit-browser-flow-investigator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The checkout button stops working after a coupon is applied. Reproduce the click path and use console or network evidence to explain the failure.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `implicit_p4_visual_diff`

- Family: `implicit_field_stress`
- Gold skill: `implicit-visual-diff-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compare the baseline and new screenshots for layout shifts, clipping, spacing, and text overflow across desktop and mobile.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `implicit_p5_ci_failure`

- Family: `implicit_field_stress`
- Gold skill: `implicit-ci-failure-reader`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Look at the CI log and find the first meaningful error plus the smallest fix and rerun sequence.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: -

### `implicit_p6_review_comments`

- Family: `implicit_field_stress`
- Gold skill: `implicit-review-comment-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the existing reviewer feedback to group required fixes, note any questions, and prepare responses for each thread; do not do a fresh code review.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: review
- Longest copied gold phrase: prepare reply each thread

### `implicit_p7_hf_dataset`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-dataset-inspector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before modelling, inspect the dataset splits, columns, row examples, labels, and schema caveats.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: dataset, inspect
- Longest copied gold phrase: -

### `implicit_p8_hf_model`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-local-model-chooser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Choose a local model and quantization that can run on an 8 GB laptop for ticket classification.
- Gold title overlap: 0.50; max alternative title overlap: 0.67; advantage: -0.17
- Gold title hits: local, model
- Longest copied gold phrase: -

### `implicit_p9_alert_rule`

- Family: `implicit_field_stress`
- Gold skill: `implicit-slo-alert-author`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Create alert rules from these checkout SLO metrics with windows, severity labels, and verification queries.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: slo, alert
- Longest copied gold phrase: -

### `implicit_p10_trace_path`

- Family: `implicit_field_stress`
- Gold skill: `implicit-trace-path-diagnoser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use these distributed trace spans to locate where checkout latency is introduced across services.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: trace
- Longest copied gold phrase: distribut trace span locate

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

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Family: `observability_reliability`
- Gold skill: `prometheus-alert-rule-writer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Produce PromQL alerting expressions for checkout latency and error-budget burn using metrics.md. Include windows, labels, severity, and verification queries; do not build a dashboard.
- Gold title overlap: 0.25; max alternative title overlap: 0.67; advantage: -0.42
- Gold title hits: alert
- Longest copied gold phrase: -

### `observability_reliability_p2_grafana_dashboard_builder`

- Family: `observability_reliability`
- Gold skill: `grafana-dashboard-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design a Grafana dashboard for checkout service health with panels, variables, queries, thresholds, and operator layout. This is not an alert-rule task.
- Gold title overlap: 0.67; max alternative title overlap: 0.50; advantage: 0.17
- Gold title hits: grafana, dashboard
- Longest copied gold phrase: panel variable querie threshold

### `observability_reliability_p3_distributed_trace_investigator`

- Family: `observability_reliability`
- Gold skill: `distributed-trace-investigator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use checkout_trace.json to find where checkout latency is introduced across services. I need trace-based diagnosis, not a dashboard.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `observability_reliability_p4_slo_breach_narrative_writer`

- Family: `observability_reliability`
- Gold skill: `slo-breach-narrative-writer`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Using incident_notes.md, write an SLO breach narrative with timeline, user impact, mitigation, and follow-up actions.
- Gold title overlap: 0.75; max alternative title overlap: 0.67; advantage: 0.08
- Gold title hits: slo, breach, narrative
- Longest copied gold phrase: -

### `observability_reliability_p5_resilience_pattern_reviewer`

- Family: `observability_reliability`
- Gold skill: `resilience-pattern-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review payment_client.py for retry, timeout, backoff, fallback, and cascading-failure risks.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: review
- Longest copied gold phrase: -

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Family: `observability_reliability`
- Gold skill: `service-mesh-traffic-debugger`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Debug the service-mesh routing notes in mesh_config.yaml, focusing on traffic split, mTLS, retries, and destination rules.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: traffic
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

### `office_business_automation_p1_xlsx_formula_model_builder`

- Family: `office_business_automation`
- Gold skill: `xlsx-formula-model-builder`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Build a spreadsheet formula model for subscription revenue using revenue_assumptions.md. I need formulas and validation checks, not Airtable automation.
- Gold title overlap: 0.75; max alternative title overlap: 0.33; advantage: 0.42
- Gold title hits: formula, model, build
- Longest copied gold phrase: build spreadsheet formula model

### `office_business_automation_p2_airtable_workflow_automator`

- Family: `office_business_automation`
- Gold skill: `airtable-workflow-automator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design an Airtable automation for inbound partner requests: fields, views, trigger conditions, Slack notification, and testing steps.
- Gold title overlap: 0.33; max alternative title overlap: 0.50; advantage: -0.17
- Gold title hits: airtable
- Longest copied gold phrase: -

### `office_business_automation_p3_notion_research_database_builder`

- Family: `office_business_automation`
- Gold skill: `notion-research-database-builder`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Create a Notion research database structure for thesis papers with properties, relations, review status, tags, and capture templates.
- Gold title overlap: 0.75; max alternative title overlap: 0.40; advantage: 0.35
- Gold title hits: notion, research, database
- Longest copied gold phrase: create notion research database

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Family: `office_business_automation`
- Gold skill: `calendar-scheduling-optimizer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use these availability notes to propose two meeting slots with buffers and conflict tradeoffs. This is scheduling, not meeting-note extraction.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: schedul
- Longest copied gold phrase: -

### `office_business_automation_p5_meeting_notes_action_extractor`

- Family: `office_business_automation`
- Gold skill: `meeting-notes-action-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: From meeting_notes.md, extract decisions, actions, owners, due dates, and open questions. Do not draft a calendar schedule.
- Gold title overlap: 0.50; max alternative title overlap: 0.33; advantage: 0.17
- Gold title hits: action, extract
- Longest copied gold phrase: owner due date open question

### `office_business_automation_p6_email_classification_router`

- Family: `office_business_automation`
- Gold skill: `email-classification-router`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Classify the emails in inbox_sample.md by category, priority, routing destination, and escalation risk. Do not write replies.
- Gold title overlap: 0.67; max alternative title overlap: 0.25; advantage: 0.42
- Gold title hits: email, rout
- Longest copied gold phrase: -

### `pdf_document_operations_p1_pdf_question_answerer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-question-answerer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Please answer this from sample_packet.pdf: what evidence does the policy give for reimbursing delayed travel meals? Cite the page or section evidence rather than converting the whole document.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: pdf
- Longest copied gold phrase: -

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Family: `pdf_document_operations`
- Gold skill: `pdf-layout-table-extractor`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: From vendor_statement.pdf, extract the invoice table into structured rows with invoice id, date, subtotal, tax, total, and page/row anchors. Do not answer it as a general PDF question.
- Gold title overlap: 0.75; max alternative title overlap: 0.67; advantage: 0.08
- Gold title hits: pdf, table, extract
- Longest copied gold phrase: -

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Family: `pdf_document_operations`
- Gold skill: `pdf-ocr-cleaner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The file scanned_receipts.pdf is mostly images. Recover the text page by page and mark uncertain OCR regions; do not treat it as a normal digital table extraction.
- Gold title overlap: 0.67; max alternative title overlap: 0.75; advantage: -0.08
- Gold title hits: pdf, ocr
- Longest copied gold phrase: recov text page page mark

### `pdf_document_operations_p4_pdf_form_filler`

- Family: `pdf_document_operations`
- Gold skill: `pdf-form-filler`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use reimbursement_form.pdf and the supplied employee details to prepare a field-entry checklist for the reimbursement packet. Identify required blanks that still need values; do not summarize the packet.
- Gold title overlap: 0.33; max alternative title overlap: 0.33; advantage: 0.00
- Gold title hits: pdf
- Longest copied gold phrase: -

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-redaction-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before we send client_contract.pdf to an external vendor, identify page-specific redaction targets such as IDs, addresses, pricing, and confidential clauses.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: pdf, redaction
- Longest copied gold phrase: -

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Family: `pdf_document_operations`
- Gold skill: `pdf-to-docx-converter`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Convert training_manual.pdf into an editable DOCX-style structure with headings and tables preserved. Do not just answer questions from it.
- Gold title overlap: 0.67; max alternative title overlap: 0.67; advantage: 0.00
- Gold title hits: pdf, convert
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

### `psc_pdf_document_work_p01_1_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The vendor packet PDF has selectable text and tables. Pull out the document metadata, section text, and invoice rows into structured JSON with page anchors.
- Gold title overlap: 0.20; max alternative title overlap: 0.33; advantage: -0.13
- Gold title hits: pdf
- Longest copied gold phrase: -

### `psc_pdf_document_work_p01_2_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use a pdfplumber-style native extraction workflow on the vendor packet. I need embedded text, table cells, metadata, and page anchors, not OCR or a prose answer.
- Gold title overlap: 0.40; max alternative title overlap: 0.20; advantage: 0.20
- Gold title hits: native, extract
- Longest copied gold phrase: table cell metadata page anchor

### `psc_pdf_document_work_p02_1_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: This signed PDF packet looks like photographed scans. Recover the readable text page by page and flag uncertain handwriting or blurred regions.
- Gold title overlap: 0.40; max alternative title overlap: 0.33; advantage: 0.07
- Gold title hits: pdf, scan
- Longest copied gold phrase: -

### `psc_pdf_document_work_p02_2_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Run an OCR recovery workflow for the scanned receipt PDF. Preserve page order and confidence notes instead of treating it as a born-digital table extraction.
- Gold title overlap: 0.60; max alternative title overlap: 0.40; advantage: 0.20
- Gold title hits: pdf, ocr, recovery
- Longest copied gold phrase: -

### `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: From the policy PDF, tell me whether delayed-travel meals are reimbursable and point to the page evidence that supports the answer.
- Gold title overlap: 0.67; max alternative title overlap: 0.25; advantage: 0.42
- Gold title hits: pdf, evidence
- Longest copied gold phrase: -

### `psc_pdf_document_work_p03_2_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Answer a narrow question from the PDF with cited page evidence. I only need the supported answer and uncertainty notes, not a converted document or extracted table.
- Gold title overlap: 0.67; max alternative title overlap: 0.40; advantage: 0.27
- Gold title hits: pdf, evidence
- Longest copied gold phrase: -

### `psc_pdf_document_work_p04_1_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before I send this contract PDF to a vendor, identify the page-level items that should be hidden, including names, addresses, pricing, IDs, and confidential clauses.
- Gold title overlap: 0.25; max alternative title overlap: 0.33; advantage: -0.08
- Gold title hits: pdf
- Longest copied gold phrase: -

### `psc_pdf_document_work_p04_2_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare a PDF redaction checklist for external sharing. I need sensitive targets with page anchors, not a summary or field extraction table.
- Gold title overlap: 0.50; max alternative title overlap: 0.40; advantage: 0.10
- Gold title hits: pdf, redaction
- Longest copied gold phrase: -

### `psc_browser_quality_p01_1_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The checkout Apply Coupon button stops responding after the first click. Reproduce the path and use browser evidence to explain whether it is DOM state, network, or JavaScript logic.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_browser_quality_p01_2_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use Chrome DevTools-style evidence for the broken checkout interaction: console errors, network failures, DOM state, and screenshots. Do not only write Playwright assertions.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_browser_quality_p02_1_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Build a repeatable browser regression check for the checkout form: navigate, fill fields, apply the coupon, assert the discount message, and capture failure evidence.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: regression
- Longest copied gold phrase: -

### `psc_browser_quality_p02_2_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write a Playwright test for the checkout coupon flow with assertions and screenshots. I need reusable regression coverage, not just a manual DevTools diagnosis.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: playwright, regression
- Longest copied gold phrase: -

### `psc_browser_quality_p03_1_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compare the old and new pricing-page screenshots and call out visible layout regressions, spacing changes, clipped content, and mobile text overflow.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: screenshot
- Longest copied gold phrase: -

### `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Do a visual regression review from screenshot pairs across desktop and mobile. I need layout differences and severity, not browser interaction debugging.
- Gold title overlap: 0.75; max alternative title overlap: 0.25; advantage: 0.50
- Gold title hits: visual, screenshot, review
- Longest copied gold phrase: -

### `psc_browser_quality_p04_1_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit the account settings modal for keyboard navigation, focus trapping, labels, contrast, and whether form errors are announced clearly.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: audit
- Longest copied gold phrase: -

### `psc_browser_quality_p04_2_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this web form specifically for accessibility interaction quality: keyboard path, accessible names, ARIA state, focus order, and screen-reader error feedback.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: accessibility, interaction
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p01_1_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use Hugging Face dataset information to inspect the ticket dataset's splits, columns, labels, row examples, and licensing caveats before we model it.
- Gold title overlap: 0.50; max alternative title overlap: 0.20; advantage: 0.30
- Gold title hits: dataset, inspect
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p01_2_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before training anything, audit the dataset card: subsets, train/validation/test split, feature schema, example rows, labels, and data caveats.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: dataset, card
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p02_1_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: I need a support-ticket classifier that can run locally on an 8 GB laptop. Shortlist realistic model sizes, quantization choices, and latency tradeoffs.
- Gold title overlap: 0.20; max alternative title overlap: 0.00; advantage: 0.20
- Gold title hits: model
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p02_2_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Choose Hugging Face or GGUF local model candidates for an 8 GB Mac. I need memory-fit and quantization reasoning, not a dataset card audit.
- Gold title overlap: 0.40; max alternative title overlap: 0.50; advantage: -0.10
- Gold title hits: local, model
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p03_1_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: We have labelled skill queries, gold skills, and hard negatives. Design the embedding fine-tuning setup and retrieval evaluation for a skill router.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: embedd
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p03_2_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Plan a SentenceTransformer fine-tuning run with positives, hard negatives, loss function, splits, top-k recall, and MRR. Do not choose a local chatbot model.
- Gold title overlap: 0.00; max alternative title overlap: 0.40; advantage: -0.40
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_huggingface_workflow_p04_1_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare the classifier demo for Hugging Face Spaces with requirements, app entrypoint, secrets, hardware tier, queue behavior, and verification after launch.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: space
- Longest copied gold phrase: hardware tier queue behavi

### `psc_huggingface_workflow_p04_2_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Package this model demo for a hosted Space-style deployment. Focus on runtime files, dependency pins, GPU/queue assumptions, and launch checks rather than training.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: deployment
- Longest copied gold phrase: -

### `psc_github_maintenance_p01_1_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: The build failed after the last push. Read the CI output, identify the first real error, explain the likely cause, and give the smallest rerun sequence.
- Gold title overlap: 0.40; max alternative title overlap: 0.00; advantage: 0.40
- Gold title hits: first, read
- Longest copied gold phrase: -

### `psc_github_maintenance_p01_2_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Analyze the failed GitHub Actions log for the first meaningful failure and minimal fix path. Do not turn this into a PR review or release note.
- Gold title overlap: 0.60; max alternative title overlap: 0.25; advantage: 0.35
- Gold title hits: log, first, failure
- Longest copied gold phrase: -

### `psc_github_maintenance_p02_1_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the review threads on this PR to plan the required fixes, tests, and replies. The comments already exist; I need an action map.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: thread
- Longest copied gold phrase: -

### `psc_github_maintenance_p02_2_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Address unresolved GitHub PR review comments by mapping each thread to code/test changes and response text. Do not perform a fresh review from scratch.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: thread
- Longest copied gold phrase: each thread code test

### `psc_github_maintenance_p03_1_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Set up repository safeguards so contributors cannot accidentally commit secrets or run destructive git operations without confirmation.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_github_maintenance_p03_2_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design git hook guardrails for secret commits, force pushes, reset --hard, branch deletion, and unsafe clean commands, including verification steps.
- Gold title overlap: 0.40; max alternative title overlap: 0.00; advantage: 0.40
- Gold title hits: guardrail, hook
- Longest copied gold phrase: -

### `psc_github_maintenance_p04_1_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn the merged PR list into release notes grouped by features, fixes, and breaking changes, with upgrade notes where needed.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: release
- Longest copied gold phrase: group feature fixe break change

### `psc_github_maintenance_p04_2_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Prepare user-facing release communication from completed changes. I need release notes/changelog language, not bug-finding or CI triage.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: release, communication
- Longest copied gold phrase: -

### `psc_security_appsec_p01_1_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before building invite-by-link file sharing, map what needs protection, who can interact with it, where control changes hands, how it could be abused, and what safeguards we should add.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_security_appsec_p01_2_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Create a design-stage threat model for the new collaborator-invite feature. I need abuse paths and mitigations, not a code-level vulnerability review.
- Gold title overlap: 0.75; max alternative title overlap: 0.50; advantage: 0.25
- Gold title hits: feature, threat, model
- Longest copied gold phrase: -

### `psc_security_appsec_p02_1_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this redirect handler for concrete security bugs around user input, auth checks, URL validation, and test coverage.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: handl, review
- Longest copied gold phrase: -

### `psc_security_appsec_p02_2_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Do an implementation-level security review of the API handler. Focus on exploitable flaws and code fixes, not feature-level threat modeling.
- Gold title overlap: 0.50; max alternative title overlap: 0.50; advantage: 0.00
- Gold title hits: handl, review
- Longest copied gold phrase: -

### `psc_security_appsec_p03_1_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: We are about to add an npm package with a postinstall script and many transitive dependencies. Assess the supply-chain risk and mitigation options.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_security_appsec_p03_2_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit a third-party dependency before adoption: maintainer health, install scripts, transitive risk, old packages, and safer alternatives.
- Gold title overlap: 0.40; max alternative title overlap: 0.00; advantage: 0.40
- Gold title hits: dependency, audit
- Longest copied gold phrase: -

### `psc_security_appsec_p04_1_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review the analytics plan that logs search queries, account region, role, clicked filters, and partial email domains for 18 months.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: review
- Longest copied gold phrase: -

### `psc_security_appsec_p04_2_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Assess privacy risk for a telemetry change: data minimization, retention, consent, access controls, and re-identification. Do not focus on code exploits.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: privacy, telemetry
- Longest copied gold phrase: minimization retention consent acces

### `psc_research_reading_p01_1_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: For this paper, map how the study was carried out: data, method components, baselines, metrics, assumptions, and evaluation limits.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: pap, method
- Longest copied gold phrase: -

### `psc_research_reading_p01_2_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Extract method and evaluation details from the paper. I need setup, baselines, metrics, assumptions, and limitations, not a broad summary.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: pap, method
- Longest copied gold phrase: -

### `psc_research_reading_p02_1_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Check whether this source really supports my sentence about skill libraries improving agent reliability, and suggest safer wording if it overclaims.
- Gold title overlap: 0.20; max alternative title overlap: 0.00; advantage: 0.20
- Gold title hits: support
- Longest copied gold phrase: -

### `psc_research_reading_p02_2_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Perform a citation-grounding audit for one draft claim: support strength, exact evidence, caveats, and revised claim wording.
- Gold title overlap: 0.60; max alternative title overlap: 0.00; advantage: 0.60
- Gold title hits: claim, support, audit
- Longest copied gold phrase: -

### `psc_research_reading_p03_1_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use these three papers to write related-work notes that compare approaches, show where they agree or diverge, and identify the gap my thesis targets.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_research_reading_p03_2_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Synthesize multiple sources into a related-work argument with themes, contrasts, unresolved limitations, and thesis positioning.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_research_reading_p04_1_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Extract each paper's dataset, task, model, baseline, metric, result, and limitation into a comparison table with source evidence.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: table, extract
- Longest copied gold phrase: -

### `psc_research_reading_p04_2_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn the source into a structured field table. I need field values and evidence snippets, not a narrative summary or related-work synthesis.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: field, table
- Longest copied gold phrase: -

### `psc_skill_representation_p01_1_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Review this rough capability note and produce a selector-facing inventory: when it should trigger, required inputs, expected artifact, steps, tools, examples, and gaps.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_skill_representation_p01_2_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Perform a field-taxonomy audit of an existing skill artifact with evidence spans. Do not write or install a new skill.
- Gold title overlap: 0.20; max alternative title overlap: 0.25; advantage: -0.05
- Gold title hits: skill
- Longest copied gold phrase: -

### `psc_skill_representation_p02_1_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: This public skill has separate finance, document, and research branches inside one file. Split it into atomic skill candidates and keep shared resources linked.
- Gold title overlap: 0.50; max alternative title overlap: 0.20; advantage: 0.30
- Gold title hits: public, skill
- Longest copied gold phrase: -

### `psc_skill_representation_p02_2_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Atomize a broad hierarchical skill into standalone child skills with preserved resource references and routing boundaries.
- Gold title overlap: 0.25; max alternative title overlap: 0.40; advantage: -0.15
- Gold title hits: skill
- Longest copied gold phrase: -

### `psc_skill_representation_p03_1_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Design a routing policy for a 2000-skill library: candidate generation, representation fields, reranking, fallback, and cost controls.
- Gold title overlap: 0.40; max alternative title overlap: 0.40; advantage: 0.00
- Gold title hits: skill, rout
- Longest copied gold phrase: rout policy skill library

### `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Specify a candidate-subsetting architecture for skill retrieval with top-k budgets, field-aware reranking, fallback, and evaluation metrics.
- Gold title overlap: 0.40; max alternative title overlap: 0.25; advantage: 0.15
- Gold title hits: skill, budget
- Longest copied gold phrase: -

### `psc_skill_representation_p04_1_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Evaluate these skill retrieval rankings with strict gold labels, acceptable alternatives, top-1, top-5, MRR, and failure categories.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: retrieval
- Longest copied gold phrase: strict gold label acceptable alternative

### `psc_skill_representation_p04_2_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Adjudicate retrieval results: separate strict and acceptable scoring, identify candidate misses versus reranker losses, and flag better-than-gold cases.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: retrieval, result
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p01_1_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Before we make a decision from this weekly channel CSV, check whether the data is trustworthy: missing values, duplicate rows, invalid ranges, and schema issues.
- Gold title overlap: 0.25; max alternative title overlap: 0.25; advantage: 0.00
- Gold title hits: data
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p01_2_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit the spreadsheet's data quality and assumptions. I need trustworthiness checks, not a ranking recommendation or executive summary.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: data, audit
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p02_1_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Scan the weekly channel metrics for unusual spikes, drops, outliers, or concentrated deviations that deserve follow-up.
- Gold title overlap: 0.00; max alternative title overlap: 0.25; advantage: -0.25
- Gold title hits: -
- Longest copied gold phrase: unusual spike drop outlier

### `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Risk level: **medium**
- Risk flags: -
- Instruction used for scoring: Build an anomaly watchlist from the CSV with evidence windows and priorities. Do not turn it into a broad reporting brief.
- Gold title overlap: 0.75; max alternative title overlap: 0.00; advantage: 0.75
- Gold title hits: anomaly, watchlist, build
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p03_1_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Compare the pilot options and rank which one we should act on first, using cost, impact, risk, confidence, and time-to-value.
- Gold title overlap: 0.25; max alternative title overlap: 0.00; advantage: 0.25
- Gold title hits: rank
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p03_2_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Use the option table to produce a decision ranking with criteria, tradeoffs, and first-choice recommendation. Do not just summarize the dataset.
- Gold title overlap: 0.50; max alternative title overlap: 0.00; advantage: 0.50
- Gold title hits: decision, rank
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p04_1_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Turn the weekly performance table into a leadership-ready brief: headline, key movements, risks, and two recommended next steps.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -

### `psc_data_analysis_intent_p04_2_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Write an executive metric narrative from the spreadsheet. I need business takeaways and actions, not data validation or anomaly hunting.
- Gold title overlap: 0.50; max alternative title overlap: 0.25; advantage: 0.25
- Gold title hits: executive, metric
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

### `skill_representation_analysis_p1_skill_field_auditor`

- Family: `skill_representation_analysis`
- Gold skill: `skill-field-auditor`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Audit public_skill_sample.md and extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and missing fields.
- Gold title overlap: 0.67; max alternative title overlap: 0.00; advantage: 0.67
- Gold title hits: field, audit
- Longest copied gold phrase: trigger input output workflow

### `skill_representation_analysis_p2_skill_authoring_guide`

- Family: `skill_representation_analysis`
- Gold skill: `skill-authoring-guide`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Draft a new atomic skill for reviewing database migrations, including triggers, boundaries, workflow, dependencies, and examples. Do not just audit an existing skill.
- Gold title overlap: 0.33; max alternative title overlap: 0.67; advantage: -0.33
- Gold title hits: skill
- Longest copied gold phrase: -

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Family: `skill_representation_analysis`
- Gold skill: `skill-router-policy-designer`
- Risk level: **medium**
- Risk flags: complete_gold_title_overlap
- Instruction used for scoring: Design a two-stage skill routing policy for a 2000-skill library, including candidate budget, representation fields, reranking, and fallback behavior.
- Gold title overlap: 1.00; max alternative title overlap: 0.67; advantage: 0.33
- Gold title hits: skill, rout, policy, design
- Longest copied gold phrase: -

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Family: `skill_representation_analysis`
- Gold skill: `skill-hierarchy-flattener`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Decompose the broad all-in-one skill in hierarchical_skill.md into atomic standalone skill definitions while preserving cross-references, common resources, and routing boundaries.
- Gold title overlap: 0.33; max alternative title overlap: 0.50; advantage: -0.17
- Gold title hits: skill
- Longest copied gold phrase: -

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Family: `skill_representation_analysis`
- Gold skill: `skill-installer-wrapper`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Install the public skill from  into the local library, preserving resources and source metadata.
- Gold title overlap: 0.67; max alternative title overlap: 0.33; advantage: 0.33
- Gold title hits: skill, install
- Longest copied gold phrase: install public skill local

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Family: `skill_representation_analysis`
- Gold skill: `skill-benchmark-evaluator`
- Risk level: **low**
- Risk flags: -
- Instruction used for scoring: Evaluate retrieval_results.json with top-1, top-5, MRR, non-core false positives, and failure-mode categories.
- Gold title overlap: 0.00; max alternative title overlap: 0.00; advantage: 0.00
- Gold title hits: -
- Longest copied gold phrase: -
