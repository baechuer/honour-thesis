# Procedural Requirement Alignment Report

This is the stricter Step 2 check. Instead of only asking whether skill fields are textually different, it asks whether the prompt-specific requirement aligns better with the gold skill than with each listed alternative.

Similarity backend: **sklearn_tfidf**.

Method: the script strips long source text where possible, removes local negated spans before scoring positive procedural fit, and still uses the full instruction when matching an alternative's `not_for` boundary. This prevents phrases such as `not a calendar plan` from positively boosting calendar-planning skills while preserving boundary evidence.

## Overall Status

- Step 2 requirement-alignment status: **PASS**
- Prompts where every alternative is beaten by gold or rejected by its boundary: 85/85 (100.0%)
- Gold/alternative pairs passing requirement alignment: 251/251 (100.0%)
- Gold skill ranked first among gold + listed alternatives: 85/85 (100.0%)

Pass rule used here: for each gold/alternative pair, the gold skill must either score above the alternative by the backend-specific margin threshold, or the prompt must strongly activate the alternative's `not_for` boundary. Current thresholds are stored in the JSON report for each pair.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 |
|---|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 |
| browser_web_automation | 6 | 6/6 | 6/6 |
| code_github_workflow | 6 | 6/6 | 6/6 |
| data_spreadsheet | 7 | 7/7 | 7/7 |
| deployment_browser_qa | 6 | 6/6 | 6/6 |
| documents_files | 7 | 7/7 | 7/7 |
| metrics_observability | 6 | 6/6 | 6/6 |
| news_monitoring | 5 | 5/5 | 5/5 |
| office_artifact_workflows | 6 | 6/6 | 6/6 |
| planning_meetings | 5 | 5/5 | 5/5 |
| reading_research | 8 | 8/8 | 8/8 |
| reply_messaging | 5 | 5/5 | 5/5 |
| security_appsec | 6 | 6/6 | 6/6 |
| skill_lifecycle | 6 | 6/6 | 6/6 |

## Weak Requirement Pairs

- No weak requirement-alignment pairs under this heuristic.

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review billing_openapi.yaml as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.
- Positive-fit instruction after negation cleanup: Please review billing_openapi.yaml as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `openapi-contract-reviewer` | 0.3624 | 0.3624 | 0.0529 | review, api, contract, endpoint-level, issue, schema, example, statu | review, api, behavior |
| `external-api-integration-planner` | 0.0754 | 0.0754 | 0.0301 | review, api, contract, example, auth, behavior, pagination | review, api, contract |
| `webhook-contract-planner` | 0.0415 | 0.0415 | 0.0521 | contract, schema, example, auth, behavior | review, api |
| `architecture-boundary-reviewer` | 0.0052 | 0.0052 | 0.0481 | review, contract | review, api, schema, auth |

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.
- Positive-fit instruction after negation cleanup: Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `external-api-integration-planner` | 0.1170 | 0.1170 | 0.0297 | plan, connect, api, authentication, endpoint, request, reply, mapp | api, mapp |
| `openapi-contract-reviewer` | 0.0465 | 0.0465 | 0.0294 | api, endpoint, request, reply, behavior | plan, api, behavior |
| `webhook-contract-planner` | 0.0448 | 0.0448 | 0.0326 | plan, endpoint, provider, behavior, secret, verification, test | api, endpoint |
| `service-dependency-mapper` | 0.0028 | 0.0028 | 0.0000 | plan, reply | - |

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.
- Positive-fit instruction after negation cleanup: A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `webhook-contract-planner` | 0.1630 | 0.1630 | 0.0000 | event, check, provider, design, receiver, behavior, signature, duplicate | - |
| `public-api-design-principles` | 0.0298 | 0.0298 | 0.0000 | design, behavior | - |
| `openapi-contract-reviewer` | 0.0173 | 0.0173 | 0.0372 | check, behavior, assumption | design, behavior, retry |
| `external-api-integration-planner` | 0.0159 | 0.0159 | 0.0183 | provider, behavior | design, receiver |
| `public-office-webhook-automation` | 0.0058 | 0.0058 | 0.0000 | event | - |

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review service_modules.md for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.
- Positive-fit instruction after negation cleanup: Please review service_modules.md for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `architecture-boundary-reviewer` | 0.2656 | 0.2656 | 0.0000 | review, backend, architecture, boundarie, module, ownership, dependency, direction | review |
| `service-dependency-mapper` | 0.0333 | 0.0333 | 0.0000 | architecture, ownership, dependency, direction | review |
| `openapi-contract-reviewer` | 0.0095 | 0.0095 | 0.0617 | review, architecture | review, architecture, boundarie |
| `database-migration-risk-assessor` | 0.0064 | 0.0064 | 0.0717 | safe | review, architecture |

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please assess add_subscription_status_migration.sql before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.
- Positive-fit instruction after negation cleanup: Please assess add_subscription_status_migration.sql before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `database-migration-risk-assessor` | 0.2702 | 0.2702 | 0.0000 | sql, production, rollout, lock, risk, backfill, plan, compatibility | plan |
| `architecture-boundary-reviewer` | 0.0161 | 0.0161 | 0.0469 | risk, verification | rollout, risk, plan |
| `service-dependency-mapper` | 0.0000 | 0.0000 | 0.0000 | risk, plan, path | - |
| `public-office-database-sync` | 0.0000 | 0.0000 | 0.0000 | - | - |
| `public-architecture-patterns` | 0.0000 | 0.0000 | 0.0000 | - | - |

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please trace how the billing, notification, account, and analytics services rely on each other using service_trace_notes.md. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.
- Positive-fit instruction after negation cleanup: Please trace how the billing, notification, account, and analytics services rely on each other using service_trace_notes.md. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `service-dependency-mapper` | 0.0632 | 0.0632 | 0.0000 | trace, service, call, direction, data, failure, evidence, gaps | - |
| `architecture-boundary-reviewer` | 0.0363 | 0.0363 | 0.0000 | service, each, call, direction, evidence | call |
| `external-api-integration-planner` | 0.0170 | 0.0170 | 0.0000 | call, data, failure | service |
| `public-architecture-patterns` | 0.0097 | 0.0097 | 0.0000 | direction | - |
| `public-api-design-principles` | 0.0049 | 0.0049 | 0.0000 | - | - |

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Open the staging dashboard and capture a page snapshot of what the user sees on the account settings page right now. I need the visible state, screenshot-style observations, and any obvious rendering issue; do not click through a full interaction test.
- Positive-fit instruction after negation cleanup: Open the staging dashboard and capture a page snapshot of what the user sees on the account settings page right now. I need the visible state, screenshot-style observations, and any obvious rendering issue; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-page-snapshotter` | 0.1281 | 0.1281 | 0.0238 | page, open, capture, user, visible, state, observation, render | page, test |
| `web-data-extractor` | 0.0412 | 0.0412 | 0.0146 | page, open, user, visible, observation | page, test |
| `frontend-debugger` | 0.0405 | 0.0405 | 0.0387 | page, open, user, visible, state, observation, render, issue | page, user, test |
| `web-ui-tester` | 0.0201 | 0.0201 | 0.0301 | page, open, user, state, observation, render | page |

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Go through the demo signup flow and fill in the form fields with the sample details I provided. Report which fields were entered and pause before final submission if it would create a real account. This is delegated browser form completion, not expected-versus-actual UI validation or a general test report.
- Positive-fit instruction after negation cleanup: Go through the demo signup flow and fill in the form fields with the sample details I provided. Report which fields were entered and pause before final submission if it would create a real account. This is delegated browser form completion, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-form-filler` | 0.1032 | 0.1032 | 0.0215 | form, field, signup, flow, fill, provid, report, enter | flow, test |
| `web-ui-tester` | 0.0173 | 0.0173 | 0.0303 | flow, report, real | form, fill, real |
| `web-page-snapshotter` | 0.0094 | 0.0094 | 0.0292 | form, flow, report | form, fill, browser, test |
| `frontend-debugger` | 0.0088 | 0.0088 | 0.0691 | flow, report, browser | form, fill, browser, test |

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Test whether the checkout page correctly shows a validation message when the postcode field is empty, and report the expected versus actual behavior.
- Positive-fit instruction after negation cleanup: Test whether the checkout page correctly shows a validation message when the postcode field is empty, and report the expected versus actual behavior.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-ui-tester` | 0.1457 | 0.1457 | 0.0133 | test, whether, page, correctly, check, message, report, expect | page |
| `web-page-snapshotter` | 0.0516 | 0.0516 | 0.0243 | test, whether, page, show, report, behavior | test, page |
| `web-form-filler` | 0.0338 | 0.0338 | 0.0151 | test, whether, checkout, page, check, field, report | test, whether, page |
| `frontend-debugger` | 0.0149 | 0.0149 | 0.0250 | test, whether, page, check, report, behavior | test, page |

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From this product listing page, extract the product names, prices, availability labels, and detail-page links into a structured table. I do not need a screenshot.
- Positive-fit instruction after negation cleanup: From this product listing page, extract the product names, prices, availability labels, and detail-page links into a structured table. I .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-data-extractor` | 0.1274 | 0.1274 | 0.0180 | list, page, extract, name, price, label, link, structur | page |
| `web-page-snapshotter` | 0.0564 | 0.0564 | 0.0581 | page, extract, structur | page, extract, structur |
| `web-ui-tester` | 0.0050 | 0.0050 | 0.0247 | page, extract | page, extract |
| `frontend-debugger` | 0.0045 | 0.0045 | 0.0159 | page, extract | page |

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The settings page opens but clicking Save does nothing, and the console shows `Cannot read properties of undefined (reading 'id')` after the profile API call. Use the UI symptom as evidence, then inspect the frontend event handler, state update path, and API response contract. The deliverable is the likely source-level cause plus the smallest code patch.
- Positive-fit instruction after negation cleanup: The settings page opens but clicking Save does nothing, and the console shows `Cannot read properties of undefined (reading 'id')` after the profile API call. Use the UI symptom as evidence, then inspect the frontend event handler, state update path, and API response contract. The deliverable is the likely source-level cause plus the smallest code patch.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `frontend-debugger` | 0.1485 | 0.1485 | 0.0269 | api, page, open, console, symptom, evidence, inspect, frontend | page, code |
| `web-page-snapshotter` | 0.0633 | 0.0633 | 0.0341 | page, open, show, evidence, inspect, state, code | page, frontend, cause |
| `web-ui-tester` | 0.0356 | 0.0356 | 0.0885 | page, open, console, evidence, state, path | page, frontend, source-level, cause, code, patch |
| `code-reviewer` | 0.0254 | 0.0254 | 0.0000 | evidence, path, likely, code | - |

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Evaluate the signup form for keyboard navigation, input labels, focus order, and whether screen-reader users can understand the error messages.
- Positive-fit instruction after negation cleanup: Evaluate the signup form for keyboard navigation, input labels, focus order, and whether screen-reader users can understand the error messages.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `accessibility-checker` | 0.1489 | 0.1489 | 0.0000 | keyboard, label, focu, order, whether, screen-reader, user | form, user |
| `web-ui-tester` | 0.0206 | 0.0206 | 0.0123 | navigation, input, whether, user, error, message | form |
| `frontend-debugger` | 0.0063 | 0.0063 | 0.0160 | whether, user, error | form, user |
| `web-page-snapshotter` | 0.0000 | 0.0000 | 0.0000 | form, whether, user | form |

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this local change before I commit it. The patch updates the cache key from `user.id` to `user.email`, adds a fallback for missing names, and changes the unit test fixture. I want to know if this could introduce bugs or missing-test risk, not have you rewrite it yet.
- Positive-fit instruction after negation cleanup: Review this local change before I commit it. The patch updates the cache key from `user.id` to `user.email`, adds a fallback for missing names, and changes the unit test fixture. I want to know if this could introduce bugs or missing-test risk, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `code-reviewer` | 0.1337 | 0.1337 | 0.0165 | change, user, review, local, commit, miss, test, bugs | change, review |
| `pr-reviewer` | 0.0464 | 0.0464 | 0.0281 | user, review, commit, test, risk | change, review, local |
| `review-comment-resolver` | 0.0378 | 0.0378 | 0.0132 | change, user, review, test | review |
| `ci-failure-debugger` | 0.0364 | 0.0364 | 0.0337 | user, review, test | review, test |

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Can you review this pull request as if you were leaving PR feedback? It changes the auth middleware, adds a migration, updates two API tests, and the PR discussion says the branch is meant to preserve backward compatibility.
- Positive-fit instruction after negation cleanup: Can you review this pull request as if you were leaving PR feedback? It changes the auth middleware, adds a migration, updates two API tests, and the PR discussion says the branch is meant to preserve backward compatibility.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pr-reviewer` | 0.1319 | 0.1319 | 0.0335 | review, extract, request, migration, test, discussion, branch, compatibility | review, change |
| `review-comment-resolver` | 0.0434 | 0.0434 | 0.0505 | review, request, change, test, preserve | review, extract, request |
| `code-reviewer` | 0.0314 | 0.0314 | 0.0896 | review, request, change, test | review, extract, request, change |
| `ci-failure-debugger` | 0.0078 | 0.0078 | 0.0240 | review, request, test | review, test |

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I already got review comments on this branch. Please address this specific reviewer request by planning and making the requested code/test change: `The retry loop can spin forever if the response is 429 and Retry-After is missing. Please add a cap and a test.` I need the existing comment resolved with an implementation response, not a fresh PR review or CI debugging.
- Positive-fit instruction after negation cleanup: I already got review comments on this branch. Please address this specific reviewer request by planning and making the requested code/test change: `The retry loop can spin forever if the response is 429 and Retry-After is missing. Please add a cap and a test.` I need the existing comment resolved with an implementation response, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `review-comment-resolver` | 0.1532 | 0.1532 | 0.1091 | comment, request, test, reply, already, review, addres, plan | review, comment, request, addres, specific, code, fresh, debug |
| `code-reviewer` | 0.0751 | 0.0751 | 0.0774 | comment, request, test, review, code, change, miss, implementation | review, comment, request, change, debug |
| `pr-reviewer` | 0.0617 | 0.0617 | 0.0545 | comment, request, test, review, branch, code | review, code, change, debug |
| `ci-failure-debugger` | 0.0405 | 0.0405 | 0.0822 | comment, request, test, review, code | review, comment, test, plan, code |

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The CI run failed after my last commit. The failing job is `unit-tests`, and the first useful error says `Expected status 200, received 401` in `auth.middleware.test.ts` after the token refresh change. Help me find the cause and the smallest fix.
- Positive-fit instruction after negation cleanup: The CI run failed after my last commit. The failing job is `unit-tests`, and the first useful error says `Expected status 200, received 401` in `auth.middleware.test.ts` after the token refresh change. Help me find the cause and the smallest fix.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `ci-failure-debugger` | 0.1434 | 0.1434 | 0.0268 | fail, run, job, first, useful, error, test, cause | fail, test |
| `review-comment-resolver` | 0.0225 | 0.0225 | 0.0051 | run, receiv, test, change, smallest | - |
| `code-reviewer` | 0.0152 | 0.0152 | 0.0431 | commit, test, change | fail, run, change |
| `pr-reviewer` | 0.0113 | 0.0113 | 0.0329 | commit, first, test | fail, job, change |

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn these completed changes into a concise internal changelog entry for the repository changelog, grouped by change type if useful: fixed retry timeout handling, added token-refresh tests, improved cache invalidation for renamed users, and removed an unused feature flag. Do not write user-facing release notes.
- Positive-fit instruction after negation cleanup: Turn these completed changes into a concise internal changelog entry for the repository changelog, grouped by change type if useful: fixed retry timeout handling, added token-refresh tests, improved cache invalidation for renamed users, and removed an unused feature flag. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `changelog-writer` | 0.1255 | 0.1255 | 0.0444 | change, changelog, complet, concise, internal, entry, group, type | change, release, note |
| `release-note-writer` | 0.0564 | 0.0564 | 0.0635 | change, changelog, turn, complet, useful, user | change, changelog, internal, release |
| `code-reviewer` | 0.0237 | 0.0237 | 0.0227 | change, changelog, concise, test, user | change, changelog |
| `pr-reviewer` | 0.0128 | 0.0128 | 0.0505 | changelog, concise, test, user | change, changelog, release, note |

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write user-facing release notes for this update. We improved sign-in reliability when sessions expire, made profile changes appear faster across devices, and fixed a retry issue that could delay requests during temporary service pressure.
- Positive-fit instruction after negation cleanup: Write user-facing release notes for this update. We improved sign-in reliability when sessions expire, made profile changes appear faster across devices, and fixed a retry issue that could delay requests during temporary service pressure.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `release-note-writer` | 0.1092 | 0.1092 | 0.0367 | user-fac, release, note, update, change, request | release, change, request |
| `changelog-writer` | 0.0651 | 0.0651 | 0.0338 | write, user-fac, release, note, change, request | release, note, change |
| `code-reviewer` | 0.0239 | 0.0239 | 0.0127 | release, note, change, issue, request | change, request |
| `pr-reviewer` | 0.0190 | 0.0190 | 0.0423 | user-fac, release, note, issue, request | release, note, change |

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. I need a broad exploratory orientation: what the sheet contains, the overall picture, the main patterns, the most useful caveats, and a few sensible next questions. Do not turn it into an executive report, forecast, ranking recommendation, or diagnosis of one specific problem yet.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. I need a broad exploratory orientation: what the sheet contains, the overall picture, the main patterns, the most useful caveats, and a few sensible next questions. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-overview` | 0.1248 | 0.1248 | 0.1255 | csv, broad, overall, picture, main, pattern, most | report, forecast, rank, recommendation, specific |
| `data-analysis-for-reporting` | 0.0187 | 0.0187 | 0.0258 | csv, main, most, useful, caveat, question | main, forecast, rank |
| `data-analysis-with-anomaly-focus` | 0.0075 | 0.0075 | 0.0082 | csv, broad, pattern | pattern, report, forecast |
| `data-analysis-with-validation` | 0.0061 | 0.0061 | 0.0392 | csv, main, most, next | broad, report, rank |

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Build an anomaly watchlist: which spikes, dips, outliers, or concentrated deviations look most worth worrying about, and how confident should I be that each one is real? Do not explain root cause yet.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Build an anomaly watchlist: which spikes, dips, outliers, or concentrated deviations look most worth worrying about, and how confident should I be that each one is real? .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-with-anomaly-focus` | 0.1612 | 0.1612 | 0.0679 | csv, anomaly, watchlist, spike, dips, outlier, concentrat, deviation | anomaly, explain, root, cause |
| `data-analysis-for-root-cause-diagnosis` | 0.0101 | 0.0101 | 0.0000 | csv, anomaly, look, most | look |
| `data-analysis-overview` | 0.0055 | 0.0055 | 0.0100 | csv, anomaly, most | spike, explain, cause |
| `data-analysis-with-validation` | 0.0054 | 0.0054 | 0.0110 | csv, anomaly, most | explain, cause |

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Before I react to it, audit whether the numbers are trustworthy: check for missing values, inconsistent rows, suspicious outliers, denominator issues, or measurement artifacts that could make a genuine problem look worse than it is.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Before I react to it, audit whether the numbers are trustworthy: check for missing values, inconsistent rows, suspicious outliers, denominator issues, or measurement artifacts that could make a genuine problem look worse than it is.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-with-validation` | 0.0808 | 0.0808 | 0.0000 | csv, whether, check, miss, value, inconsistent, issue, problem | - |
| `data-analysis-with-anomaly-focus` | 0.0221 | 0.0221 | 0.0000 | csv, check, value, outlier, issue, look, than | check |
| `data-analysis-overview` | 0.0159 | 0.0159 | 0.0000 | csv, check, miss, value, rows | whether |
| `data-analysis-for-root-cause-diagnosis` | 0.0159 | 0.0159 | 0.0000 | csv, check, issue, problem, look, than | whether, look |

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. This seems to be getting worse. Assume the data is usable enough for analysis and trace the most likely driver: which channel, metric, or segment appears to explain the degradation, and what evidence supports that diagnosis?
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. This seems to be getting worse. Assume the data is usable enough for analysis and trace the most likely driver: which channel, metric, or segment appears to explain the degradation, and what evidence supports that diagnosis?

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-root-cause-diagnosis` | 0.1091 | 0.1091 | 0.0107 | csv, data, analysi, most, likely, driver, channel, metric | data |
| `data-analysis-with-validation` | 0.0353 | 0.0353 | 0.0213 | csv, data, analysi, most, support, diagnosi | likely, explain |
| `data-analysis-with-anomaly-focus` | 0.0350 | 0.0350 | 0.0088 | csv, data, analysi, segment, appear, explain, evidence, diagnosi | data, explain |
| `data-analysis-overview` | 0.0237 | 0.0237 | 0.0094 | csv, data, analysi, most, diagnosi | data, explain |

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Turn this into an upward-facing reporting brief: a headline, two or three executive takeaways, the clearest supporting numbers, and one caveat. Do not give me a broad exploratory analysis.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Turn this into an upward-facing reporting brief: a headline, two or three executive takeaways, the clearest supporting numbers, and one caveat. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-reporting` | 0.1551 | 0.1551 | 0.0000 | csv, turn, upward-fac, report, headline, executive, takeaway, support | - |
| `data-analysis-overview` | 0.0174 | 0.0174 | 0.0000 | csv, report, takeaway | report |
| `data-analysis-for-root-cause-diagnosis` | 0.0161 | 0.0161 | 0.0232 | csv, report, support | report, broad |
| `data-analysis-with-anomaly-focus` | 0.0057 | 0.0057 | 0.0000 | csv, report | report |

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Forecast the likely next direction if the current pattern keeps going: what seems likely to happen next, what evidence supports that continuation, and how much should I trust the forecast?
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Forecast the likely next direction if the current pattern keeps going: what seems likely to happen next, what evidence supports that continuation, and how much should I trust the forecast?

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-forecasting` | 0.1736 | 0.1736 | 0.0254 | forecast, likely, next, csv, direction, current, pattern, happen | current, happen |
| `data-analysis-for-root-cause-diagnosis` | 0.0451 | 0.0451 | 0.0325 | forecast, likely, next, csv, pattern, evidence, support | forecast |
| `data-analysis-with-anomaly-focus` | 0.0227 | 0.0227 | 0.0197 | forecast, csv, pattern, evidence | forecast, pattern |
| `data-analysis-overview` | 0.0025 | 0.0025 | 0.0286 | forecast, csv, pattern, keep | forecast, trust |

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read pilot_priority_options.csv. Compare the options, rank them for action now, recommend the first choice, explain the decision criteria and trade-offs behind that ordering, and say what follow-up check would reduce decision risk. This is a selection task, not a forecast of one metric or a broad overview.
- Positive-fit instruction after negation cleanup: Please read pilot_priority_options.csv. Compare the options, rank them for action now, recommend the first choice, explain the decision criteria and trade-offs behind that ordering, and say what follow-up check would reduce decision risk. This is a selection task, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-ranking-selection` | 0.1154 | 0.1154 | 0.1192 | decision, csv, compare, option, rank, recommend, choice, criteria | decision, option, selection, forecast, broad, overview |
| `data-analysis-for-forecasting` | 0.0257 | 0.0257 | 0.0000 | csv, compare, option, rank, explain, check, risk, task | rank, explain |
| `data-analysis-overview` | 0.0043 | 0.0043 | 0.0166 | csv, rank, check, task | rank, explain, forecast |
| `data-analysis-for-reporting` | 0.0040 | 0.0040 | 0.0454 | csv, rank, them, check, risk, task | decision, option, rank, selection, forecast |

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.
- Positive-fit instruction after negation cleanup: The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `playwright-flow-debugger` | 0.1495 | 0.1495 | 0.0192 | flow, fail, reproduce, interaction, browser, evidence, capture, console | interaction |
| `public-openai-playwright` | 0.0532 | 0.0532 | 0.0000 | flow, interaction, browser, evidence | - |
| `accessibility-interaction-auditor` | 0.0358 | 0.0358 | 0.0000 | flow, interaction, evidence, clue, identify | - |
| `public-playwright-interactive` | 0.0208 | 0.0208 | 0.0000 | interaction, browser, evidence | - |
| `visual-regression-checker` | 0.0169 | 0.0169 | 0.0418 | flow, evidence, capture, identify | fail, click, why |

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please compare the baseline and current screenshots for pricing_page_desktop.png and pricing_page_mobile.png. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.
- Positive-fit instruction after negation cleanup: Please compare the baseline and current screenshots for pricing_page_desktop.png and pricing_page_mobile.png. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `visual-regression-checker` | 0.2400 | 0.2400 | 0.0000 | compare, baseline, current, screenshot, visual, regression, clipp, spac | - |
| `accessibility-interaction-auditor` | 0.0183 | 0.0183 | 0.0185 | visual, contrast, change | compare, visual, regression |
| `public-anthropic-webapp-testing` | 0.0131 | 0.0131 | 0.0000 | screenshot, visual | - |
| `public-openai-screenshot` | 0.0101 | 0.0101 | 0.0000 | screenshot, visual | - |
| `playwright-flow-debugger` | 0.0074 | 0.0074 | 0.0355 | screenshot, visual | compare, screenshot, visual |

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.
- Positive-fit instruction after negation cleanup: Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `accessibility-interaction-auditor` | 0.2184 | 0.2184 | 0.0000 | focu, audit, modal, keyboard, screen-reader, interaction, order, accessible | - |
| `web-ui-tester` | 0.0205 | 0.0205 | 0.0141 | interaction, state, whether, error | form |
| `playwright-flow-debugger` | 0.0193 | 0.0193 | 0.0201 | interaction, state, whether | interaction |
| `public-anthropic-webapp-testing` | 0.0082 | 0.0082 | 0.0000 | interaction, state | - |
| `visual-regression-checker` | 0.0078 | 0.0078 | 0.0000 | name, state | audit |

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The Netlify deploy for build_log.txt failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.
- Positive-fit instruction after negation cleanup: The Netlify deploy for build_log.txt failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `deployment-build-triager` | 0.1354 | 0.1354 | 0.0113 | deploy, fail, build, identify, likely, root, cause, miss | deploy, build |
| `deployment-release-verifier` | 0.0087 | 0.0087 | 0.0783 | deploy, fail, build, config | fail, build, log |
| `web-performance-budget-checker` | 0.0066 | 0.0066 | 0.0000 | identify, assumption | - |
| `playwright-flow-debugger` | 0.0031 | 0.0031 | 0.0106 | fail, identify | build |

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.
- Positive-fit instruction after negation cleanup: The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `deployment-release-verifier` | 0.2949 | 0.2949 | 0.0000 | check, deploy, release, readines, url, smoke, version, evidence | - |
| `public-netlify-deploy` | 0.0984 | 0.0984 | 0.0000 | production, deploy, netlify, url, environment | - |
| `public-openai-vercel-deploy` | 0.0492 | 0.0492 | 0.0000 | deploy, live, app, url, environment | - |
| `deployment-build-triager` | 0.0286 | 0.0286 | 0.0199 | check, deploy, release, version, evidence, environment | check, deploy, url |
| `visual-regression-checker` | 0.0060 | 0.0060 | 0.0196 | check, evidence | smoke |

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review lighthouse_trace_summary.txt against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.
- Positive-fit instruction after negation cleanup: Please review lighthouse_trace_summary.txt against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-performance-budget-checker` | 0.1808 | 0.1808 | 0.0000 | review, against, performance, budget, block, network, weight, image | - |
| `visual-regression-checker` | 0.0069 | 0.0069 | 0.0000 | image, size | - |
| `deployment-release-verifier` | 0.0044 | 0.0044 | 0.0000 | block | - |
| `accessibility-interaction-auditor` | 0.0000 | 0.0000 | 0.0305 | - | review |

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read internal_travel_policy_update.txt and help me make sense of it quickly. I want the main point, the most important details, and anything I should pay attention to.
- Positive-fit instruction after negation cleanup: Please read internal_travel_policy_update.txt and help me make sense of it quickly. I want the main point, the most important details, and anything I should pay attention to.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-summariser` | 0.0764 | 0.0764 | 0.0000 | read, quickly, main, point, most, important, detail | - |
| `document-converter` | 0.0220 | 0.0220 | 0.0000 | main, most, important, detail | - |
| `document-normaliser` | 0.0106 | 0.0106 | 0.0183 | important | main |
| `document-field-extractor` | 0.0082 | 0.0082 | 0.0166 | read, important | main |

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read travel_request_note_raw.txt and produce a revised full prose version for a human reader. Keep it as continuous paragraphs in the same document form, improve wording, flow, and polish, and preserve the same meaning and commitments.
- Positive-fit instruction after negation cleanup: Please read travel_request_note_raw.txt and produce a revised full prose version for a human reader. Keep it as continuous paragraphs in the same document form, improve wording, flow, and polish, and preserve the same meaning and commitments.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-rewriter` | 0.1712 | 0.1712 | 0.0000 | same, revis, prose, version, human, reader, keep, document | - |
| `document-normaliser` | 0.0488 | 0.0488 | 0.0323 | version, keep, document, form, word, preserve, mean | document, mean |
| `document-converter` | 0.0481 | 0.0481 | 0.0115 | keep, document, form, preserve, mean | document |
| `document-summariser` | 0.0405 | 0.0405 | 0.0094 | read, document, form, preserve | document, polish |

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read travel_request_note_raw.txt and normalise the document structure: keep the original wording and order as much as possible, but fix inconsistent headings, spacing, list style, and layout noise. Do not substantially rewrite the prose.
- Positive-fit instruction after negation cleanup: Please read travel_request_note_raw.txt and normalise the document structure: keep the original wording and order as much as possible, but fix inconsistent headings, spacing, list style, and layout noise. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-normaliser` | 0.1282 | 0.1282 | 0.0208 | normalize, document, structure, keep, original, word, order, possible | document, layout |
| `document-converter` | 0.0417 | 0.0417 | 0.0227 | document, structure, keep, layout, noise | document, layout, rewrite |
| `document-rewriter` | 0.0338 | 0.0338 | 0.0226 | document, structure, keep, original, word | normalize, noise, rewrite |
| `document-summariser` | 0.0275 | 0.0275 | 0.0186 | read, document | document, layout, rewrite |

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read invoice_northbridge_supplies.txt and extract the reusable fields into a structured table, including supplier, invoice number, dates, line items, totals, and payment details. Do not write a narrative summary.
- Positive-fit instruction after negation cleanup: Please read invoice_northbridge_supplies.txt and extract the reusable fields into a structured table, including supplier, invoice number, dates, line items, totals, and payment details. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-field-extractor` | 0.0507 | 0.0507 | 0.0375 | read, extract, field, structur, invoice, date, item, total | narrative, summary |
| `layout-preserving-converter` | 0.0248 | 0.0248 | 0.0397 | extract, field, structur, table, invoice | extract, field, narrative, summary |
| `multi-document-comparison-preparer` | 0.0197 | 0.0197 | 0.0094 | extract, field, structur, invoice, detail | extract, summary |
| `document-summariser` | 0.0192 | 0.0192 | 0.0370 | read, extract, structur, invoice, detail | extract, field, date |

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read policy_draft_a.txt and policy_draft_b.txt, then prepare a side-by-side comparison matrix so I can quickly see matching sections, changed wording, additions, removals, and unresolved differences.
- Positive-fit instruction after negation cleanup: Please read policy_draft_a.txt and policy_draft_b.txt, then prepare a side-by-side comparison matrix so I can quickly see matching sections, changed wording, additions, removals, and unresolved differences.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `multi-document-comparison-preparer` | 0.0699 | 0.0699 | 0.0139 | prepare, compare, see, match, section, difference | chang |
| `document-normaliser` | 0.0195 | 0.0195 | 0.0000 | compare, see, section, word | chang |
| `document-field-extractor` | 0.0093 | 0.0093 | 0.0147 | read, compare, see | compare |
| `document-converter` | 0.0051 | 0.0051 | 0.0000 | compare, see, section | - |

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read request_form.txt and convert the whole form into clean markdown notes I can drop into my repo. Preserve the content and labels, but simplify the source formatting rather than keeping the exact visual layout.
- Positive-fit instruction after negation cleanup: Please read request_form.txt and convert the whole form into clean markdown notes I can drop into my repo. Preserve the content and labels, but simplify the source formatting .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-converter` | 0.1243 | 0.1243 | 0.0200 | convert, form, markdown, note, preserve, content, label, simplify | content, layout |
| `document-normaliser` | 0.0554 | 0.0554 | 0.0181 | convert, form, clean, preserve, content, label, formatt | convert, content, layout |
| `layout-preserving-converter` | 0.0408 | 0.0408 | 0.0171 | convert, form, preserve, content, label, but, formatt | convert, content, layout |
| `document-summariser` | 0.0238 | 0.0238 | 0.0069 | read, convert, form, note, preserve | convert, layout |

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read request_form.txt and turn it into markdown while preserving the layout cues: headings, labels, rows, and grouped fields should remain recognizable. The priority is layout fidelity, not just simplified notes.
- Positive-fit instruction after negation cleanup: Please read request_form.txt and turn it into markdown while preserving the layout cues: headings, labels, rows, and grouped fields should remain recognizable. The priority is layout fidelity, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `layout-preserving-converter` | 0.1723 | 0.1723 | 0.0199 | layout, preserv, cues, heading, label, rows, group, field | layout, field |
| `document-converter` | 0.0798 | 0.0798 | 0.1175 | layout, turn, markdown, preserv, label, priority, fidelity | layout, preserv, field, fidelity |
| `document-field-extractor` | 0.0229 | 0.0229 | 0.0000 | read, field | - |
| `document-normaliser` | 0.0182 | 0.0182 | 0.0663 | preserv, heading, label | layout, preserv, field |

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Give me a triage overview of this service snapshot
- Positive-fit instruction after negation cleanup: Give me a triage overview of this service snapshot

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `metrics-overview` | 0.0904 | 0.0904 | 0.0000 | overview, service, snapshot | - |
| `latency-anomaly-detector` | 0.0223 | 0.0223 | 0.0812 | service, snapshot | overview |
| `incident-summary-writer` | 0.0165 | 0.0165 | 0.0000 | overview, service | - |
| `metrics-root-cause-diagnoser` | 0.0054 | 0.0054 | 0.0000 | service | - |

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Run an anomaly-focused readout on this service snapshot. Identify unusual performance behavior, especially tail-latency spikes, outliers, and whether the deviation is broad or concentrated in a smaller slice of requests. Do not give only a general metrics overview
- Positive-fit instruction after negation cleanup: Run an anomaly-focused readout on this service snapshot. Identify unusual performance behavior, especially tail-latency spikes, outliers, and whether the deviation is broad or concentrated in a smaller slice of requests.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `latency-anomaly-detector` | 0.1526 | 0.1526 | 0.0456 | anomaly-focus, service, snapshot, identify, unusual, performance, behavior, spike | broad, only, overview |
| `metrics-overview` | 0.0317 | 0.0317 | 0.0000 | readout, service, snapshot, identify, whether | whether |
| `slo-breach-checker` | 0.0205 | 0.0205 | 0.0000 | service, snapshot, identify, whether | - |
| `metrics-root-cause-diagnoser` | 0.0136 | 0.0136 | 0.0216 | service, identify, performance, whether | only |

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check this service snapshot against a reliability-objective risk frame
- Positive-fit instruction after negation cleanup: Check this service snapshot against a reliability-objective risk frame

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `slo-breach-checker` | 0.1000 | 0.1000 | 0.1443 | check, service, snapshot, risk | risk |
| `capacity-risk-forecaster` | 0.0656 | 0.0656 | 0.0000 | service, risk | check, against |
| `metrics-overview` | 0.0375 | 0.0375 | 0.0188 | service, snapshot | risk |
| `metrics-root-cause-diagnoser` | 0.0038 | 0.0038 | 0.0208 | check, service, against | check, risk |

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Forecast capacity risk from this service snapshot if the pattern keeps going. Focus on future pressure, saturation risk, queue growth, headroom, and likely bottlenecks that could turn into a bigger operational problem. Do not decide current SLO breach or root cause
- Positive-fit instruction after negation cleanup: Forecast capacity risk from this service snapshot if the pattern keeps going. Focus on future pressure, saturation risk, queue growth, headroom, and likely bottlenecks that could turn into a bigger operational problem.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `capacity-risk-forecaster` | 0.2715 | 0.2715 | 0.1170 | risk, forecast, capacity, service, pattern, focu, future, pressure | current, slo, breach, root, cause |
| `slo-breach-checker` | 0.0517 | 0.0517 | 0.0677 | risk, forecast, service, snapshot, operational | risk, forecast, capacity, root, cause |
| `metrics-overview` | 0.0380 | 0.0380 | 0.0871 | forecast, service, snapshot, keep, focu, saturation, queue, operational | risk, forecast, capacity, future, slo, breach, root, cause |
| `metrics-root-cause-diagnoser` | 0.0277 | 0.0277 | 0.0653 | forecast, service, saturation, likely, operational, problem | risk, forecast, capacity, future, slo |

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Do a root-cause diagnosis for this service snapshot. Compare hypotheses such as downstream dependency latency, queue buildup, CPU pressure, and request mix; identify the most plausible driver of the degradation; and tie the diagnosis to evidence. Snapshot data
- Positive-fit instruction after negation cleanup: Do a root-cause diagnosis for this service snapshot. Compare hypotheses such as downstream dependency latency, queue buildup, CPU pressure, and request mix; identify the most plausible driver of the degradation; and tie the diagnosis to evidence. Snapshot data

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `metrics-root-cause-diagnoser` | 0.1100 | 0.1100 | 0.0000 | diagnosi, service, compare, hypothese, dependency, latency, identify, most | - |
| `latency-anomaly-detector` | 0.0644 | 0.0644 | 0.0921 | snapshot, service, compare, latency, identify, driver, evidence | compare, hypothese, most, plausible, driver, degradation |
| `capacity-risk-forecaster` | 0.0541 | 0.0541 | 0.0776 | service, queue, buildup, cpu, pressure, identify, most, plausible | compare, hypothese, driver, degradation, evidence |
| `incident-summary-writer` | 0.0276 | 0.0276 | 0.0253 | diagnosi, service, identify, most, degradation | root-cause |

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn this service snapshot into an incident update I could quickly share with the team
- Positive-fit instruction after negation cleanup: Turn this service snapshot into an incident update I could quickly share with the team

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `incident-summary-writer` | 0.0539 | 0.0539 | 0.0000 | turn, service, incident, quickly | - |
| `metrics-overview` | 0.0421 | 0.0421 | 0.0847 | service, snapshot, incident | incident, update |
| `slo-breach-checker` | 0.0281 | 0.0281 | 0.0177 | service, snapshot, incident | incident |
| `metrics-root-cause-diagnoser` | 0.0170 | 0.0170 | 0.0189 | service, incident | incident |

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise this news article in a straightforward neutral recap
- Positive-fit instruction after negation cleanup: Summarise this news article in a straightforward neutral recap

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-summariser` | 0.1063 | 0.1063 | 0.0169 | summary, news, article, straightforward, recap | news |
| `news-briefing-writer` | 0.0407 | 0.0407 | 0.0201 | summary, news, article, recap | summary, news, article |
| `source-grounding-extractor` | 0.0213 | 0.0213 | 0.0000 | summary, news, article, recap | summary |

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn this article into a short decision memo with clear sections for the key event, current state of play, significance now, affected parties, and follow-up signals. The output should support quick situation awareness, not just summarize the article chronologically
- Positive-fit instruction after negation cleanup: Turn this article into a short decision memo with clear sections for the key event, current state of play, significance now, affected parties, and follow-up signals. The output should support quick situation awareness,

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-briefing-writer` | 0.1036 | 0.1036 | 0.0000 | turn, article, short, decision, section, key, current, state | article, summary |
| `tech-news-trend-extractor` | 0.0335 | 0.0335 | 0.0000 | article, clear, significance, now, signal, output, support | summary |
| `news-summariser` | 0.0238 | 0.0238 | 0.2817 | article, event, signal, output, support | decision, memo, current, state, play, significance, now, affect |

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From this article, identify the source-backed claims and facts, including important product details, named companies or people, and any figures or stated plans
- Positive-fit instruction after negation cleanup: From this article, identify the source-backed claims and facts, including important product details, named companies or people, and any figures or stated plans

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `source-grounding-extractor` | 0.1194 | 0.1194 | 0.0000 | article, identify, claim, fact, nam, figure, plan | - |
| `news-summariser` | 0.0550 | 0.0550 | 0.0202 | article, identify, fact, important, detail | claim |
| `news-briefing-writer` | 0.0293 | 0.0293 | 0.0744 | article, identify, fact, important, detail | article, claim, fact |

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Extract the recurring themes across these three tech news snippets, grouping repeated ideas without forecasting market direction. Snippet 1
- Positive-fit instruction after negation cleanup: Extract the recurring themes across these three tech news snippets, grouping repeated ideas . Snippet 1

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-theme-extractor` | 0.1312 | 0.1312 | 0.0000 | snippet, extract, recurr, theme, acros, news, group, repeat | extract |
| `tech-news-trend-extractor` | 0.0715 | 0.0715 | 0.0149 | snippet, theme, acros, tech, news, repeat | extract, theme |
| `news-briefing-writer` | 0.0247 | 0.0247 | 0.0345 | snippet, extract, theme, acros, news | extract, theme, acros, news |

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Identify which patterns across these three tech news snippets look like actionable tech trend signals right now, why they matter strategically, and what evidence would confirm or weaken the trend. Snippet 1
- Positive-fit instruction after negation cleanup: Identify which patterns across these three tech news snippets look like actionable tech trend signals right now, why they matter strategically, and what evidence would confirm or weaken the trend. Snippet 1

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `tech-news-trend-extractor` | 0.1088 | 0.1088 | 0.0321 | tech, snippet, trend, identify, acros, news, signal, now | trend |
| `news-theme-extractor` | 0.0601 | 0.0601 | 0.0302 | snippet, trend, identify, pattern, acros, news, signal, they | trend, strategically |
| `news-briefing-writer` | 0.0303 | 0.0303 | 0.0313 | snippet, trend, identify, acros, news, signal, now, why | trend, acros, news |

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please inspect grant_application_packet.pdf as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. Do not just extract the fields.
- Positive-fit instruction after negation cleanup: Please inspect grant_application_packet.pdf as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-layout-reviewer` | 0.1582 | 0.1582 | 0.0171 | pdf, inspect, render, layout, issue, cropp, table, header | table, extract, field |
| `pdf-ocr-extractor` | 0.0755 | 0.0755 | 0.0743 | pdf, area | pdf, render, layout |
| `public-pdf` | 0.0688 | 0.0688 | 0.0000 | pdf, render, layout, table, anyth, form, read | - |
| `public-office-pdf-extraction` | 0.0579 | 0.0579 | 0.0000 | pdf, render, layout, table | - |
| `office-to-markdown-converter` | 0.0201 | 0.0201 | 0.1016 | layout, table | pdf, render |

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please recover the text from scanned_receipts_packet.pdf. It looks like image scans, so keep page numbers and mark uncertain OCR text instead of pretending every amount is reliable.
- Positive-fit instruction after negation cleanup: Please recover the text from scanned_receipts_packet.pdf. It looks like image scans, so keep page numbers and mark uncertain OCR text .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-ocr-extractor` | 0.2294 | 0.2294 | 0.0305 | text, recover, pdf, image, keep, page, number, mark | pdf, ocr |
| `pdf-layout-reviewer` | 0.0606 | 0.0606 | 0.0137 | pdf, page | page, ocr |
| `office-to-markdown-converter` | 0.0224 | 0.0224 | 0.0403 | text, keep, page, mark, uncertain | pdf, page |
| `document-field-extractor` | 0.0000 | 0.0000 | 0.0000 | scan, keep | - |

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review vendor_agreement_draft.docx as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.
- Positive-fit instruction after negation cleanup: Please review vendor_agreement_draft.docx as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `docx-redline-editor` | 0.2296 | 0.2296 | 0.0415 | review, word, document, prepare, redline-style, edit, reviewer, comment | document |
| `public-docx` | 0.1208 | 0.1208 | 0.0000 | docx, word, document, edit, comment, change | - |
| `public-office-docx-manipulation` | 0.0569 | 0.0569 | 0.0000 | docx, word, document, edit, comment, change | - |
| `document-rewriter` | 0.0407 | 0.0407 | 0.0244 | word, document, edit, preserve, substantive | substantive |
| `office-to-markdown-converter` | 0.0186 | 0.0186 | 0.0695 | review, document, preserve, section | word, document, change |

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please check pricing_model.xlsx for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.
- Positive-fit instruction after negation cleanup: Please check pricing_model.xlsx for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `spreadsheet-formula-auditor` | 0.0619 | 0.0619 | 0.0000 | check, calculation, assumption, risk, cell, link, range, whether | summary |
| `public-office-xlsx-manipulation` | 0.0261 | 0.0261 | 0.0000 | xlsx, link | - |
| `public-xlsx` | 0.0215 | 0.0215 | 0.0000 | xlsx, link | - |
| `data-analysis-with-validation` | 0.0134 | 0.0134 | 0.0000 | check, assumption, whether, summary | - |
| `office-to-markdown-converter` | 0.0058 | 0.0058 | 0.0000 | embedd, summary | check |

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review thesis_proposal_deck.pptx for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.
- Positive-fit instruction after negation cleanup: Please review thesis_proposal_deck.pptx for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `slide-deck-visual-auditor` | 0.3136 | 0.3136 | 0.0227 | review, presentation, readines, slide-level, feedback, visual, hierarchy, text | presentation |
| `public-pptx` | 0.0955 | 0.0955 | 0.0000 | pptx, presentation, visual, text, theme | - |
| `public-office-ppt-visual` | 0.0422 | 0.0422 | 0.0000 | presentation, visual, theme | - |
| `pdf-layout-reviewer` | 0.0272 | 0.0272 | 0.0000 | review, visual, alignment | - |
| `office-to-markdown-converter` | 0.0256 | 0.0256 | 0.0000 | review, visual, hierarchy, text | - |

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please convert project_brief.docx into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but do not create tracked changes or a layout audit.
- Positive-fit instruction after negation cleanup: Please convert project_brief.docx into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `office-to-markdown-converter` | 0.2676 | 0.2676 | 0.0762 | convert, clean, markdown, preserve, heading, table, label, traceability | track, change, audit |
| `document-converter` | 0.0489 | 0.0489 | 0.0162 | convert, markdown, preserve, label | layout |
| `docx-redline-editor` | 0.0415 | 0.0415 | 0.0409 | preserve, heading | convert, markdown, layout, audit |
| `pdf-layout-reviewer` | 0.0104 | 0.0104 | 0.0140 | table | convert, markdown, table |

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I have a short group project meeting tomorrow for a class presentation on AI study assistants. Please turn these topics into an agenda for that upcoming meeting: who will cover the demo, who will finish the slides, what risks could delay us before Friday, and what we need to prepare before the next check-in. The output should guide the meeting discussion, not schedule my whole week or only extract tasks.
- Positive-fit instruction after negation cleanup: I have a short group project meeting tomorrow for a class presentation on AI study assistants. Please turn these topics into an agenda for that upcoming meeting: who will cover the demo, who will finish the slides, what risks could delay us before Friday, and what we need to prepare before the next check-in. The output should guide the meeting discussion, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-agenda-builder` | 0.1805 | 0.1805 | 0.0785 | meet, group, turn, topic, agenda, upcom, output, guide | meet, discussion, extract, task |
| `weekly-planner` | 0.0311 | 0.0311 | 0.0913 | meet, group, risk, output | meet, agenda, only, extract, task |
| `task-extractor` | 0.0297 | 0.0297 | 0.1061 | meet, output | meet, agenda, schedule, extract |

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise these meeting notes into a clean meeting recap
- Positive-fit instruction after negation cleanup: Summarise these meeting notes into a clean meeting recap

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-summary-writer` | 0.1713 | 0.1713 | 0.0882 | meet, summary, note, recap | meet, note |
| `meeting-followup-extractor` | 0.1135 | 0.1135 | 0.0598 | meet, summary, note | meet, summary, note |
| `task-extractor` | 0.0788 | 0.0788 | 0.1149 | meet, summary, note | meet, summary |

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I need something clean from these meeting notes so I can quickly see what needs to happen next and what still needs attention
- Positive-fit instruction after negation cleanup: I need something clean from these meeting notes so I can quickly see what needs to happen next and what still needs attention

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-followup-extractor` | 0.0919 | 0.0919 | 0.0313 | meet, note, happen, next | meet, note |
| `meeting-summary-writer` | 0.0501 | 0.0501 | 0.0411 | meet, note, happen | meet, note |
| `task-extractor` | 0.0496 | 0.0496 | 0.0421 | meet, note | meet |

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn these rough notes into a plain action-item list without scheduling the week and without treating them as completed meeting notes
- Positive-fit instruction after negation cleanup: Turn these rough notes into a plain action-item list

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `task-extractor` | 0.0954 | 0.0954 | 0.0919 | rough, note, list | complet, meet |
| `meeting-followup-extractor` | 0.0393 | 0.0393 | 0.0798 | note, list | note, rough, meet |
| `weekly-planner` | 0.0147 | 0.0147 | 0.1537 | note, list | note, rough, complet, meet |

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Help me make a realistic week-level plan with sequencing and time buffers. I need to finish the planning skill family, revise prompts for the reply cluster, prepare for a Tuesday project meeting about collaborating on a prototype and brainstorming test cases for a multi-agent system, review two papers, send my supervisor a grounded summary by Thursday, and leave time for benchmark testing. I also have classes on Tuesday and Thursday afternoon. Do not just extract a raw task list or prepare a single meeting agenda.
- Positive-fit instruction after negation cleanup: Help me make a realistic week-level plan with sequencing and time buffers. I need to finish the planning skill family, revise prompts for the reply cluster, prepare for a Tuesday project meeting about collaborating on a prototype and brainstorming test cases for a multi-agent system, review two papers, send my supervisor a grounded summary by Thursday, and leave time for benchmark testing. I also have classes on Tuesday and Thursday afternoon. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `weekly-planner` | 0.0687 | 0.0687 | 0.0428 | plan, time, realistic, week-level, sequenc, buffer, meet | meet, summary, extract, task, agenda |
| `meeting-agenda-builder` | 0.0421 | 0.0421 | 0.0345 | plan, time, week-level, prompt, meet, summary | plan, meet, summary, extract, task |
| `task-extractor` | 0.0207 | 0.0207 | 0.0903 | plan, week-level, meet, summary | plan, meet, week-level, summary, extract, agenda |

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Give me a balanced research-oriented recap of this academic paper. I want the research problem, overall approach, main findings, and limitations in one readable summary, not citation-ready notes and not a method-only audit
- Positive-fit instruction after negation cleanup: Give me a balanced research-oriented recap of this academic paper. I want the research problem, overall approach, main findings, and limitations in one readable summary,

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `paper-summariser` | 0.2284 | 0.2284 | 0.1409 | research-orient, recap, academic, paper, research, approach, main, finding | main, citation-ready, note |
| `general-source-summariser` | 0.0861 | 0.0861 | 0.1024 | recap, paper, research, main, readable, summary | research, summary |
| `method-note-builder` | 0.0464 | 0.0464 | 0.0412 | recap, paper, research, problem, limitation, summary | paper, summary, note |
| `citation-note-extractor` | 0.0322 | 0.0322 | 0.0238 | paper, research, main, finding, limitation, summary | paper, summary |

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise this as a general source report rather than an academic paper. I need the context, main observations, practical recommendations, and evidence limits in plain language
- Positive-fit instruction after negation cleanup: Summarise this as a general source report . I need the context, main observations, practical recommendations, and evidence limits in plain language

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `general-source-summariser` | 0.1852 | 0.1852 | 0.0292 | summary, report, context, main, observation, recommendation, evidence, limit | summary |
| `citation-note-extractor` | 0.0256 | 0.0256 | 0.0158 | summary, main, observation, limit | summary, paper |
| `paper-summariser` | 0.0231 | 0.0231 | 0.0367 | summary, main, limit | main |
| `document-extractor` | 0.0124 | 0.0124 | 0.0000 | summary | summary |

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Make this source usable for me later when I'm writing by producing citation-ready notes
- Positive-fit instruction after negation cleanup: Make this source usable for me later when I'm writing by producing citation-ready notes

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `citation-note-extractor` | 0.1988 | 0.1988 | 0.0422 | writ, citation-ready, note | writ, produc |
| `citation-grounding-helper` | 0.0308 | 0.0308 | 0.0598 | note | writ, note |
| `document-extractor` | 0.0237 | 0.0237 | 0.1846 | note | writ, produc, citation-ready, note |
| `paper-summariser` | 0.0108 | 0.0108 | 0.1557 | note | citation-ready, note |

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Extract the specific details from this source into a structured table of fields and values
- Positive-fit instruction after negation cleanup: Extract the specific details from this source into a structured table of fields and values

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-extractor` | 0.1074 | 0.1074 | 0.0000 | extract, specific, structur, field, value | - |
| `method-note-builder` | 0.0698 | 0.0698 | 0.0000 | extract, specific, detail, structur, field | extract |
| `citation-note-extractor` | 0.0266 | 0.0266 | 0.0000 | detail | - |
| `paper-summariser` | 0.0053 | 0.0053 | 0.0319 | extract, detail | extract |

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Help me make sense of this source by focusing on how the work was actually carried out, how it was evaluated, and what assumptions or constraints shaped the result
- Positive-fit instruction after negation cleanup: Help me make sense of this source by focusing on how the work was actually carried out, how it was evaluated, and what assumptions or constraints shaped the result

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `method-note-builder` | 0.0915 | 0.0915 | 0.0095 | was, work, carri, assumption, constraint, result | work |
| `citation-note-extractor` | 0.0384 | 0.0384 | 0.0090 | work, result | - |
| `document-extractor` | 0.0217 | 0.0217 | 0.0425 | result | focus, work |
| `paper-summariser` | 0.0150 | 0.0150 | 0.0340 | was, assumption, result | - |

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I wrote this exact sentence from the source: 'Explicit task decomposition reliably improves agent performance in realistic environments.' Perform a citation-grounding support audit: mark which parts of the sentence are supported, overstated, or unsupported, explain the overreach, and give a safer revised sentence if needed.
- Positive-fit instruction after negation cleanup: I wrote this exact sentence from the source: 'Explicit task decomposition reliably improves agent performance in realistic environments.' Perform a citation-grounding support audit: mark which parts of the sentence are supported, overstated, or unsupported, explain the overreach, and give a safer revised sentence if needed.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `citation-grounding-helper` | 0.1767 | 0.1767 | 0.0087 | sentence, support, exact, task, part, overstat, unsupport, explain | - |
| `document-extractor` | 0.0517 | 0.0517 | 0.0091 | explicit, task | - |
| `citation-note-extractor` | 0.0317 | 0.0317 | 0.0159 | support, task | support |
| `paper-summariser` | 0.0052 | 0.0052 | 0.0221 | - | - |

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compare these two sources in a side-by-side table with separate columns for Source A and Source B so I can clearly see how they line up, where they differ, and what each one contributes. Use rows such as approach, evaluation, strengths, limitations, and contribution; do not turn it into a synthesized related-work paragraph, method-only note, or citation-note list.
- Positive-fit instruction after negation cleanup: Compare these two sources in a side-by-side table with separate columns for Source A and Source B so I can clearly see how they line up, where they differ, and what each one contributes. Use rows such as approach, evaluation, strengths, limitations, and contribution; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `multi-source-comparison-builder` | 0.0655 | 0.0655 | 0.0701 | compare, two, side-by-side, see, each, such, evaluation | related-work, note |
| `citation-note-extractor` | 0.0445 | 0.0445 | 0.0250 | compare, see, limitation | compare, related-work |
| `method-note-builder` | 0.0380 | 0.0380 | 0.0534 | compare, see, evaluation, limitation | synthesiz, note |
| `related-work-synthesiser` | 0.0330 | 0.0330 | 0.0740 | compare, see, each, limitation | compare, side-by-side, table, note |

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Synthesize these two sources into related-work style notes: explain the main approaches, how they relate, the shared research direction, and what remains unresolved across them. I want an integrated synthesis, not a side-by-side comparison table.
- Positive-fit instruction after negation cleanup: Synthesize these two sources into related-work style notes: explain the main approaches, how they relate, the shared research direction, and what remains unresolved across them. I want an integrated synthesis, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `related-work-synthesiser` | 0.1821 | 0.1821 | 0.0825 | related-work, style, note, explain, main, approache, relate, shar | note, main, side-by-side, compare, table |
| `citation-note-extractor` | 0.0356 | 0.0356 | 0.0315 | note, main, research, synthesi | related-work, acros, compare |
| `paper-summariser` | 0.0344 | 0.0344 | 0.1190 | note, main, research, synthesi | related-work, note, main |
| `multi-source-comparison-builder` | 0.0222 | 0.0222 | 0.0653 | two, note, research, them, synthesi | related-work, note, main |

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Draft a respectful academic email reply to this message from my professor, including availability and a polite tone suitable for a supervisor relationship: 'Hi Jacky, thanks for your update. Would you be available to meet next Tuesday afternoon to discuss the revised thesis scope? Please let me know what time suits you best.'
- Positive-fit instruction after negation cleanup: Draft a respectful academic email reply to this message from my professor, including availability and a polite tone suitable for a supervisor relationship: 'Hi Jacky, thanks for your update. Would you be available to meet next Tuesday afternoon to discuss the revised thesis scope? Please let me know what time suits you best.'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `professor-email-reply` | 0.1357 | 0.1357 | 0.0318 | draft, respectful, academic, email, reply, message, professor, polite | draft, reply |
| `reply-drafter` | 0.0537 | 0.0537 | 0.0492 | draft, academic, email, reply, message, tone | draft, reply, message, availability, tone |
| `reply-polisher` | 0.0530 | 0.0530 | 0.0155 | draft, academic, email, reply, message, tone | reply, message |

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Edit this already-written message only. Keep the same meaning, availability, and commitments, but improve flow, phrasing, tone, and readability. Return the refined version of this message.
- Positive-fit instruction after negation cleanup: Edit this already-written message only. Keep the same meaning, availability, and commitments, but improve flow, phrasing, tone, and readability. Return the refined version of this message.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `reply-polisher` | 0.2128 | 0.2128 | 0.0303 | message, edit, already-written, only, keep, same, mean, commitment | message, only |
| `reply-drafter` | 0.0645 | 0.0645 | 0.2769 | message, edit, already-written, only, keep, commitment, but, tone | message, edit, already-written, only, keep, same, mean, availability |
| `professor-email-reply` | 0.0311 | 0.0311 | 0.0753 | message, only, keep, commitment, phras, tone, return | edit, already-written, only, same, commitment, refin, version |

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Draft a reply to these teammates about shared project coordination. The reply should clarify what I can take ownership of, confirm the deadline situation, and help the group move the work forward: 'Hey everyone, we need to lock in who is doing the slides, who is writing the report section, and whether we can still meet the Friday deadline. Can each of you confirm what you can finish by tomorrow?'
- Positive-fit instruction after negation cleanup: Draft a reply to these teammates about shared project coordination. The reply should clarify what I can take ownership of, confirm the deadline situation, and help the group move the work forward: 'Hey everyone, we need to lock in who is doing the slides, who is writing the report section, and whether we can still meet the Friday deadline. Can each of you confirm what you can finish by tomorrow?'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `groupwork-reply` | 0.1625 | 0.1625 | 0.0419 | reply, deadline, who, draft, teammate, shar, project, coordination | reply, coordination, group |
| `followup-reply-writer` | 0.0645 | 0.0645 | 0.0232 | reply, confirm, draft, coordination, clarify, group, whether, meet | reply, draft |
| `reply-drafter` | 0.0566 | 0.0566 | 0.0510 | reply, deadline, draft, coordination, group, whether | reply, deadline, draft, writ |

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write a response whose main purpose is to state my next actions clearly
- Positive-fit instruction after negation cleanup: Write a response whose main purpose is to state my next actions clearly

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `followup-reply-writer` | 0.0683 | 0.0683 | 0.0194 | reply, main, state, next, action, clearly | reply, clearly |
| `reply-drafter` | 0.0353 | 0.0353 | 0.0134 | reply, main, clearly | reply, clearly |
| `groupwork-reply` | 0.0181 | 0.0181 | 0.0324 | reply, main, next, action, clearly | reply, main |

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compose a concise new response from the source message only, confirming that I can send the requested file tomorrow. There is no existing reply text to polish, and I do not need a detailed action plan: 'Thanks for the update. Could you send me the file by tomorrow if possible?'
- Positive-fit instruction after negation cleanup: Compose a concise new response from the source message only, confirming that I can send the requested file tomorrow. There is : 'Thanks for the update. Could you send me the file by tomorrow if possible?'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `reply-drafter` | 0.0595 | 0.0595 | 0.0431 | concise, new, reply, message, only | reply, message, only, exist, polish |
| `followup-reply-writer` | 0.0220 | 0.0220 | 0.0122 | concise, reply, message, only, confirm | reply |
| `reply-polisher` | 0.0110 | 0.0110 | 0.0459 | send, new, reply, message, only, request | reply, message, only, action |

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: We are designing a new file-sharing feature where users can invite collaborators by email, generate public links, and revoke access later. Before implementation, reason across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.
- Positive-fit instruction after negation cleanup: We are designing a new file-sharing feature where users can invite collaborators by email, generate public links, and revoke access later. Before implementation, reason across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `security-threat-modeler` | 0.1797 | 0.1797 | 0.0068 | design, feature, user, implementation, reason, asset, external, actor | risk |
| `auth-flow-reviewer` | 0.0522 | 0.0522 | 0.2344 | design, feature, user, acces, protect, actor, boundarie, scenario | design, acces, implementation, acros, protect, asset, external, actor |
| `privacy-risk-reviewer` | 0.0454 | 0.0454 | 0.2569 | design, feature, user, security, mitigation, risk | design, acros, protect, asset, external, actor, component, boundarie |
| `security-code-reviewer` | 0.0207 | 0.0207 | 0.3216 | design, feature, user, implementation, boundarie, security, risk | design, reason, acros, protect, asset, external, actor, component |

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this single API handler for concrete code-level security vulnerabilities and fixes tied to the implementation. It accepts `redirectUrl` from the request body, checks the current user, updates the user's profile, and redirects. Focus on handler-level flaws such as open redirects, unsafe validation, and incorrect access checks in this function.
- Positive-fit instruction after negation cleanup: Review this single API handler for concrete code-level security vulnerabilities and fixes tied to the implementation. It accepts `redirectUrl` from the request body, checks the current user, updates the user's profile, and redirects. Focus on handler-level flaws such as open redirects, unsafe validation, and incorrect access checks in this function.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `security-code-reviewer` | 0.1777 | 0.1777 | 0.0351 | check, redirect, review, handler, concrete, code-level, security, vulnerabilitie | review, security |
| `security-threat-modeler` | 0.0621 | 0.0621 | 0.0305 | check, review, concrete, code-level, security, implementation, user, open | check, review, concrete, vulnerabilitie |
| `code-reviewer` | 0.0501 | 0.0501 | 0.0360 | check, review, fixe, implementation, request, user | check, review, request |
| `auth-flow-reviewer` | 0.0475 | 0.0475 | 0.2978 | check, review, handler, security, user, open, acces | check, redirect, review, api, handler, concrete, code-level, security |

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check the risk of adding this new npm package. It has a broad dependency tree, a postinstall script, and the lockfile pulls in several old transitive packages. I need a dependency and supply-chain risk assessment.
- Positive-fit instruction after negation cleanup: Check the risk of adding this new npm package. It has a broad dependency tree, a postinstall script, and the lockfile pulls in several old transitive packages. I need a dependency and supply-chain risk assessment.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `dependency-risk-auditor` | 0.1705 | 0.1705 | 0.0385 | risk, package, dependency, check, script, lockfile, transitive, supply-chain | risk, broad |
| `security-code-reviewer` | 0.0140 | 0.0140 | 0.0512 | risk, dependency, check | risk, dependency, supply-chain |
| `secret-leak-scanner` | 0.0130 | 0.0130 | 0.0816 | risk, dependency, check | risk, dependency, assessment |
| `ci-failure-debugger` | 0.0116 | 0.0116 | 0.0308 | dependency, check, broad | check, new |

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Look at this diff and tell me if I accidentally exposed anything sensitive: it adds `.env.example`, updates a deployment log, and includes strings that look like `sk_live_...`, a database URL, and a webhook signing secret.
- Positive-fit instruction after negation cleanup: Look at this diff and tell me if I accidentally exposed anything sensitive: it adds `.env.example`, updates a deployment log, and includes strings that look like `sk_live_...`, a database URL, and a webhook signing secret.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `secret-leak-scanner` | 0.0759 | 0.0759 | 0.0124 | diff, expos, sensitive, env, log, string, secret | secret |
| `security-code-reviewer` | 0.0105 | 0.0105 | 0.0000 | diff, sensitive, secret | look, secret |
| `dependency-risk-auditor` | 0.0078 | 0.0078 | 0.0000 | diff, update, secret | secret |
| `privacy-risk-reviewer` | 0.0076 | 0.0076 | 0.0061 | diff, expos, sensitive, secret | secret |

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check whether this account-access change is safe. Users can refresh expired sessions, reset passwords by email link, and switch between workspace roles. I care about bypasses, stale permissions, and privilege escalation.
- Positive-fit instruction after negation cleanup: Check whether this account-access change is safe. Users can refresh expired sessions, reset passwords by email link, and switch between workspace roles. I care about bypasses, stale permissions, and privilege escalation.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `auth-flow-reviewer` | 0.1383 | 0.1383 | 0.0158 | check, whether, account-acces, safe, user, refresh, session, reset | check |
| `privacy-risk-reviewer` | 0.0063 | 0.0063 | 0.0000 | check, whether, user | - |
| `security-code-reviewer` | 0.0062 | 0.0062 | 0.0000 | check, whether, user, permission | - |
| `security-threat-modeler` | 0.0037 | 0.0037 | 0.0000 | check, whether, user | check |

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Assess the data-protection concerns in this analytics change. We want to log search queries, account region, user role, clicked filters, and partial email domains for 18 months so the product team can study usage patterns.
- Positive-fit instruction after negation cleanup: Assess the data-protection concerns in this analytics change. We want to log search queries, account region, user role, clicked filters, and partial email domains for 18 months so the product team can study usage patterns.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `privacy-risk-reviewer` | 0.0378 | 0.0378 | 0.0117 | concern, analytic, user | concern |
| `auth-flow-reviewer` | 0.0165 | 0.0165 | 0.0000 | concern, user, role | concern |
| `secret-leak-scanner` | 0.0117 | 0.0117 | 0.0118 | concern, log, user | - |
| `security-threat-modeler` | 0.0095 | 0.0095 | 0.0000 | concern, user | - |

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before I make anything new, search my existing capability library, shortlist available entries, assess fit and confidence, and decide whether one of them covers a workflow for turning messy meeting notes into action items and follow-up messages. I only want a reuse recommendation, not creation.
- Positive-fit instruction after negation cleanup: Before I make anything new, search my existing capability library, shortlist available entries, assess fit and confidence, and decide whether one of them covers a workflow for turning messy meeting notes into action items and follow-up messages. I only want a reuse recommendation, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-finder` | 0.0822 | 0.0822 | 0.0163 | anyth, new, search, exist, library, shortlist, available, fit | new, exist |
| `skill-creator` | 0.0459 | 0.0459 | 0.1074 | new, exist, capability, library, decide, whether, workflow, note | new, exist, capability, shortlist, entrie, fit, confidence, whether |
| `skill-editor` | 0.0313 | 0.0313 | 0.1109 | new, exist, library, whether, workflow | exist, capability, shortlist, entrie, workflow, reuse, recommendation |
| `skill-installer` | 0.0159 | 0.0159 | 0.0057 | exist, library, available, whether | new, search |

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I found an existing spreadsheet-analysis capability in a public catalog and want it added to my active local library. Please fetch or prepare the package, verify the expected files, and report the source, local path, setup result, and any activation caveats.
- Positive-fit instruction after negation cleanup: I found an existing spreadsheet-analysis capability in a public catalog and want it added to my active local library. Please fetch or prepare the package, verify the expected files, and report the source, local path, setup result, and any activation caveats.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-installer` | 0.1697 | 0.1697 | 0.0000 | local, exist, public, catalog, active, library, fetch, prepare | - |
| `skill-packager` | 0.0422 | 0.0422 | 0.4001 | exist, public, library, prepare, package, check, file, report | local, capability, public, catalog, active, library, fetch, package |
| `skill-finder` | 0.0254 | 0.0254 | 0.0294 | exist, public, library, package | exist |
| `skill-creator` | 0.0198 | 0.0198 | 0.0447 | exist, capability, public, add, library, package, check, expect | exist, capability |

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a new atomic skill for a repeated workflow: I often need to turn supervisor meeting notes into a thesis action list with owners, deadlines, and open questions. There is no existing skill for this exact workflow.
- Positive-fit instruction after negation cleanup: Create a new atomic skill for a repeated workflow: I often need to turn supervisor meeting notes into a thesis action list with owners, deadlines, and open questions. There is .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-creator` | 0.1764 | 0.1764 | 0.1083 | create, new, atomic, skill, repeat, workflow, note | skill, new, exist |
| `skill-finder` | 0.0530 | 0.0530 | 0.0967 | create, new, skill, workflow, note | skill, new, exist |
| `skill-editor` | 0.0524 | 0.0524 | 0.0902 | create, new, skill, workflow | skill, workflow, exist |
| `skill-packager` | 0.0251 | 0.0251 | 0.0182 | create, skill | skill |

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: This existing skill's description is too broad and it keeps triggering for document summaries when it should only handle structured field extraction. Please revise the skill so its selection boundary is clearer.
- Positive-fit instruction after negation cleanup: This existing skill's description is too broad and it keeps triggering for document summaries when it should only handle structured field extraction. Please revise the skill so its selection boundary is clearer.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-editor` | 0.1247 | 0.1247 | 0.0561 | exist, skill', description, broad, keep, summary, revise, skill | exist, skill |
| `skill-creator` | 0.0957 | 0.0957 | 0.1308 | exist, skill', description, broad, keep, trigger, only, skill | exist, skill |
| `skill-evaluator` | 0.0663 | 0.0663 | 0.0745 | exist, skill', description, trigger, structur, skill, selection, boundary | skill |
| `skill-packager` | 0.0573 | 0.0573 | 0.0209 | exist, keep, only, structur, skill | skill', skill |

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Test whether my `reply-polisher` skill actually triggers only when there is already a draft reply. I want an evaluation with realistic near-boundary prompts before deciding whether to edit it.
- Positive-fit instruction after negation cleanup: Test whether my `reply-polisher` skill actually triggers only when there is already a draft reply. I want an evaluation with realistic near-boundary prompts before deciding whether to edit it.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-evaluator` | 0.1320 | 0.1320 | 0.0367 | whether, test, skill, trigger, evaluation, realistic, near-boundary, prompt | test, skill, edit |
| `skill-editor` | 0.0388 | 0.0388 | 0.0207 | whether, skill, edit | skill, edit |
| `skill-creator` | 0.0350 | 0.0350 | 0.0211 | whether, skill, trigger, only, edit | whether, test, skill, already, edit |
| `skill-finder` | 0.0337 | 0.0337 | 0.0340 | whether, skill, already, edit | test, skill, edit |

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I finished an existing `paper-summariser` skill and want to share it with someone else. Check the folder shape, metadata, resource links, and unnecessary files so it is package-ready.
- Positive-fit instruction after negation cleanup: I finished an existing `paper-summariser` skill and want to share it with someone else. Check the folder shape, metadata, resource links, and unnecessary files so it is package-ready.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-packager` | 0.1696 | 0.1696 | 0.0305 | exist, skill, share, check, folder, shape, metadata, resource | skill, check, file |
| `skill-editor` | 0.0703 | 0.0703 | 0.0353 | exist, skill, metadata, resource | exist, skill |
| `skill-installer` | 0.0659 | 0.0659 | 0.0213 | exist, skill, check, file | skill |
| `skill-creator` | 0.0497 | 0.0497 | 0.0616 | exist, skill, check, folder, resource | exist, skill |

