# Procedural Requirement Alignment Report

This is the stricter Step 2 check. Instead of only asking whether skill fields are textually different, it asks whether the prompt-specific requirement aligns better with the gold skill than with each listed alternative.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Method: the script strips long source text where possible, removes local negated spans before scoring positive procedural fit, and still uses the full instruction when matching an alternative's `not_for` boundary. This prevents phrases such as `not a calendar plan` from positively boosting calendar-planning skills while preserving boundary evidence.

## Overall Status

- Step 2 requirement-alignment status: **PASS**
- Prompts where every alternative is beaten by gold or rejected by its boundary: 182/201 (90.5%)
- Gold/alternative pairs passing requirement alignment: 618/641 (96.4%)
- Gold skill ranked first among gold + listed alternatives: 183/201 (91.0%)

Pass rule used here: for each gold/alternative pair, the gold skill must either score above the alternative by the backend-specific margin threshold, or the prompt must strongly activate the alternative's `not_for` boundary. Current thresholds are stored in the JSON report for each pair.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 |
|---|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 |
| api_mcp_tooling | 6 | 5/6 | 6/6 |
| browser_web_automation | 6 | 6/6 | 6/6 |
| code_github_workflow | 6 | 6/6 | 6/6 |
| data_spreadsheet | 7 | 7/7 | 6/7 |
| deployment_browser_qa | 6 | 5/6 | 5/6 |
| documents_files | 7 | 7/7 | 7/7 |
| github_ci_maintenance | 6 | 6/6 | 6/6 |
| huggingface_ml_workflows | 6 | 5/6 | 5/6 |
| implicit_field_stress | 10 | 3/10 | 4/10 |
| metrics_observability | 6 | 6/6 | 5/6 |
| news_monitoring | 5 | 5/5 | 5/5 |
| observability_reliability | 6 | 6/6 | 6/6 |
| office_artifact_workflows | 6 | 5/6 | 5/6 |
| office_business_automation | 6 | 6/6 | 6/6 |
| pdf_document_operations | 6 | 5/6 | 6/6 |
| planning_meetings | 5 | 5/5 | 4/5 |
| public_style_controlled | 64 | 60/64 | 60/64 |
| reading_research | 8 | 8/8 | 8/8 |
| reply_messaging | 5 | 5/5 | 5/5 |
| security_appsec | 6 | 5/6 | 4/6 |
| skill_lifecycle | 6 | 5/6 | 6/6 |
| skill_representation_analysis | 6 | 5/6 | 6/6 |

## Weak Requirement Pairs

| Prompt | Gold | Alternative | Margin | Reason |
|---|---|---|---:|---|
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | `webhook-contract-planner` | 0.0376 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `deploy_p5_release_verification` | `deployment-release-verifier` | `public-netlify-deploy` | -0.1526 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `huggingface_ml_workflows_p2_hf_local_model_selector` | `hf-local-model-selector` | `public-huggingface-huggingface-local-models` | -0.0025 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p1_pdf_answer` | `implicit-pdf-evidence-answerer` | `implicit-pdf-table-reconstructor` | 0.0277 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p4_visual_diff` | `implicit-visual-diff-reviewer` | `visual-regression-checker` | -0.0328 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p6_review_comments` | `implicit-review-comment-planner` | `pr-review-comment-resolver` | -0.0650 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p7_hf_dataset` | `implicit-hf-dataset-inspector` | `hf-dataset-viewer-inspector` | -0.0768 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p8_hf_model` | `implicit-hf-local-model-chooser` | `hf-local-model-selector` | -0.1217 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p9_alert_rule` | `implicit-slo-alert-author` | `prometheus-alert-rule-writer` | 0.0134 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `implicit_p10_trace_path` | `implicit-trace-path-diagnoser` | `distributed-trace-investigator` | -0.1079 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | `public-xlsx` | 0.0108 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `office_p4_formula_audit` | `spreadsheet-formula-auditor` | `public-office-xlsx-manipulation` | -0.0328 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `pdf_document_operations_p1_pdf_question_answerer` | `pdf-question-answerer` | `pdf-redaction-reviewer` | 0.0354 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa` | `psc-pdf-evidence-qa` | `psc-pdf-redaction-pass` | 0.0073 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_browser_quality_p02_1_psc_playwright_regression_suite` | `psc-playwright-regression-suite` | `psc-devtools-runtime-diagnoser` | -0.0686 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_browser_quality_p02_1_psc_playwright_regression_suite` | `psc-playwright-regression-suite` | `psc-visual-screenshot-reviewer` | 0.0245 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_browser_quality_p02_1_psc_playwright_regression_suite` | `psc-playwright-regression-suite` | `psc-accessibility-interaction-auditor` | 0.0146 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_security_appsec_p01_1_psc_feature_threat_modeler` | `psc-feature-threat-modeler` | `psc-privacy-telemetry-reviewer` | -0.0036 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `psc_skill_representation_p03_2_psc_skill_routing_budget_planner` | `psc-skill-routing-budget-planner` | `psc-retrieval-result-adjudicator` | -0.0112 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `sec_p1_threat_model` | `security-threat-modeler` | `auth-flow-reviewer` | -0.0236 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `sec_p1_threat_model` | `security-threat-modeler` | `privacy-risk-reviewer` | -0.1471 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `skill_p2_install_existing` | `skill-installer` | `skill-packager` | 0.0166 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |
| `skill_representation_analysis_p2_skill_authoring_guide` | `skill-authoring-guide` | `skill-installer-wrapper` | 0.0294 | gold does not clearly outrank alternative and alternative not-for boundary is not strongly activated |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review billing_openapi.yaml as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.
- Positive-fit instruction after negation cleanup: Please review billing_openapi.yaml as an API contract. I need endpoint-level issues around schemas, examples, status codes, auth behavior, pagination, and client compatibility.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `openapi-contract-reviewer` | 0.7055 | 0.7055 | 0.4081 | review, api, contract, endpoint-level, issue, schema, example, statu | review, api, behavior |
| `external-api-integration-planner` | 0.5411 | 0.5411 | 0.5870 | review, api, contract, example, auth, behavior, pagination | review, api, contract |
| `webhook-contract-planner` | 0.2963 | 0.2963 | 0.6130 | contract, schema, example, auth, behavior | review, api |
| `architecture-boundary-reviewer` | 0.2832 | 0.2832 | 0.6995 | review, contract | review, api, schema, auth |

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.
- Positive-fit instruction after negation cleanup: Please plan how our app should connect to the Acme Billing API. Cover authentication, endpoint choices, request/response mapping, provider throttling, recovery behavior, page-through results, secrets, and verification tests.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `external-api-integration-planner` | 0.4996 | 0.4996 | 0.3090 | plan, connect, api, authentication, endpoint, request, reply, mapp | api, mapp |
| `openapi-contract-reviewer` | 0.3376 | 0.3376 | 0.3482 | api, endpoint, request, reply, behavior | plan, api, behavior |
| `webhook-contract-planner` | 0.2820 | 0.2820 | 0.3481 | plan, endpoint, provider, behavior, secret, verification, test | api, endpoint |
| `service-dependency-mapper` | 0.2043 | 0.2043 | 0.2389 | plan, reply | - |

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.
- Positive-fit instruction after negation cleanup: A payment provider will send event callbacks into our app. Please design the receiver behavior: which events to accept, how to validate the body, how to check signatures, how to handle duplicate deliveries, retry timing, ordering assumptions, and failed-message storage.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `webhook-contract-planner` | 0.4963 | 0.4963 | 0.2899 | event, check, provider, design, receiver, behavior, signature, duplicate | - |
| `external-api-integration-planner` | 0.3462 | 0.3462 | 0.3047 | provider, behavior | design, receiver |
| `openapi-contract-reviewer` | 0.3013 | 0.3013 | 0.3389 | check, behavior, assumption | design, behavior, retry |
| `public-office-webhook-automation` | 0.1857 | 0.1857 | 0.0944 | event | - |
| `public-api-design-principles` | 0.1805 | 0.1805 | 0.0944 | design, behavior | - |

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review service_modules.md for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.
- Positive-fit instruction after negation cleanup: Please review service_modules.md for backend architecture boundaries. I care about module ownership, dependency direction, coupling, misplaced responsibilities, and a safe refactoring sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `architecture-boundary-reviewer` | 0.6578 | 0.6578 | 0.4148 | review, backend, architecture, boundarie, module, ownership, dependency, direction | review |
| `openapi-contract-reviewer` | 0.4368 | 0.4368 | 0.3329 | review, architecture | review, architecture, boundarie |
| `service-dependency-mapper` | 0.4114 | 0.4114 | 0.3094 | architecture, ownership, dependency, direction | review |
| `database-migration-risk-assessor` | 0.3494 | 0.3494 | 0.5432 | safe | review, architecture |

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please assess add_subscription_status_migration.sql before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.
- Positive-fit instruction after negation cleanup: Please assess add_subscription_status_migration.sql before production rollout. I need locking risk, backfill plan, compatibility with old app versions, rollback path, and verification queries.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `database-migration-risk-assessor` | 0.7223 | 0.7223 | 0.3295 | sql, production, rollout, lock, risk, backfill, plan, compatibility | plan |
| `architecture-boundary-reviewer` | 0.3517 | 0.3517 | 0.5741 | risk, verification | rollout, risk, plan |
| `public-office-database-sync` | 0.3074 | 0.3074 | 0.0488 | sql, production, path | - |
| `service-dependency-mapper` | 0.2691 | 0.2691 | 0.4160 | risk, plan, path | - |
| `public-architecture-patterns` | 0.2170 | 0.2170 | 0.0488 | - | - |

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please trace how the billing, notification, account, and analytics services rely on each other using service_trace_notes.md. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.
- Positive-fit instruction after negation cleanup: Please trace how the billing, notification, account, and analytics services rely on each other using service_trace_notes.md. Include call direction, responsible teams, shared data promises, ways failures propagate, and evidence gaps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `service-dependency-mapper` | 0.4562 | 0.4562 | 0.2876 | trace, service, call, direction, data, failure, evidence, gaps | - |
| `external-api-integration-planner` | 0.3406 | 0.3406 | 0.2980 | call, data, failure | service |
| `public-api-design-principles` | 0.2785 | 0.2785 | 0.0457 | - | - |
| `architecture-boundary-reviewer` | 0.2778 | 0.2778 | 0.3297 | service, each, call, direction, evidence | call |
| `public-architecture-patterns` | 0.1894 | 0.1894 | 0.0457 | direction | - |

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Family: `api_mcp_tooling`
- Gold skill: `rest-api-contract-designer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Specify a new client-facing HTTP interface for subscription invoices, including resources, endpoints, request and response shapes, status codes, pagination, and error examples. This is not an MCP wrapper.
- Positive-fit instruction after negation cleanup: Specify a new client-facing HTTP interface for subscription invoices, including resources, endpoints, request and response shapes, status codes, pagination, and error examples. This is .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `rest-api-contract-designer` | 0.4664 | 0.4664 | 0.5126 | specify, new, resource, endpoint, request, reply, statu, code | mcp |
| `webhook-integration-planner` | 0.4132 | 0.4132 | 0.5312 | subscription | endpoint, mcp |
| `api-documentation-writer` | 0.3760 | 0.3760 | 0.3488 | includ, endpoint, error, example | mcp |
| `auth-flow-integrator` | 0.2489 | 0.2489 | 0.4678 | - | mcp |
| `mcp-server-builder` | 0.2107 | 0.2107 | 0.3387 | specify, resource, example | - |

### `api_mcp_tooling_p2_mcp_server_builder`

- Family: `api_mcp_tooling`
- Gold skill: `mcp-server-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create an MCP server design that exposes two local file-inspection tools with narrow schemas and resource boundaries. Do not design a public REST API.
- Positive-fit instruction after negation cleanup: Create an MCP server design that exposes two local file-inspection tools with narrow schemas and resource boundaries. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `mcp-server-builder` | 0.5679 | 0.5679 | 0.3742 | mcp, server, expose, local, tool, narrow, schema, resource | design, rest, api |
| `webhook-integration-planner` | 0.2035 | 0.2035 | 0.6371 | - | design, mcp, server, rest, api |
| `rest-api-contract-designer` | 0.1829 | 0.1829 | 0.4681 | design, schema, resource | mcp, server, api |
| `api-documentation-writer` | 0.1466 | 0.1466 | 0.5148 | create, schema | design, mcp, server, api |
| `auth-flow-integrator` | 0.1432 | 0.1432 | 0.4380 | boundarie | mcp, tool, api |

### `api_mcp_tooling_p3_webhook_integration_planner`

- Family: `api_mcp_tooling`
- Gold skill: `webhook-integration-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Plan webhook handling for payment events: accepted event types, signature checks, idempotency, retry behavior, ordering, and dead-letter storage.
- Positive-fit instruction after negation cleanup: Plan webhook handling for payment events: accepted event types, signature checks, idempotency, retry behavior, ordering, and dead-letter storage.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `webhook-integration-planner` | 0.8204 | 0.8204 | 0.3518 | event, plan, webhook, handl, type, signature, check, idempotency | - |
| `webhook-contract-planner` | 0.7828 | 0.7828 | 0.2820 | event, plan, webhook, handl, type, signature, check, idempotency | - |
| `public-office-webhook-automation` | 0.5596 | 0.5596 | 0.1009 | event, webhook, type | - |
| `rest-api-contract-designer` | 0.3110 | 0.3110 | 0.5551 | behavior | plan, webhook |
| `mcp-server-builder` | 0.1133 | 0.1133 | 0.5553 | - | plan, webhook |

### `api_mcp_tooling_p4_auth_flow_integrator`

- Family: `api_mcp_tooling`
- Gold skill: `auth-flow-integrator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Integrate OAuth login for a dashboard app, covering scopes, token refresh, secret storage, logout, and authorization checks. Do not turn it into webhook planning.
- Positive-fit instruction after negation cleanup: Integrate OAuth login for a dashboard app, covering scopes, token refresh, secret storage, logout, and authorization checks. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `auth-flow-integrator` | 0.6085 | 0.6085 | 0.6469 | integrate, oauth, app, scope, token, refresh, secret, storage | webhook, plan |
| `api-documentation-writer` | 0.3356 | 0.3356 | 0.3943 | - | - |
| `webhook-integration-planner` | 0.2474 | 0.2474 | 0.3449 | storage, check | - |
| `rest-api-contract-designer` | 0.2363 | 0.2363 | 0.5380 | - | webhook, plan |
| `mcp-server-builder` | 0.1029 | 0.1029 | 0.6725 | - | webhook, plan |

### `api_mcp_tooling_p5_api_documentation_writer`

- Family: `api_mcp_tooling`
- Gold skill: `api-documentation-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write developer docs for the existing billing API contract in billing_contract.yaml, including quickstart, examples, auth notes, and errors.
- Positive-fit instruction after negation cleanup: Write developer docs for the existing billing API contract in billing_contract.yaml, including quickstart, examples, auth notes, and errors.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `api-documentation-writer` | 0.6245 | 0.6245 | 0.2672 | write, developer, docs, exist, api, contract, includ, quickstart | api |
| `rest-api-contract-designer` | 0.3245 | 0.3245 | 0.3151 | api, contract, example, error | developer, exist, api |
| `auth-flow-integrator` | 0.2235 | 0.2235 | 0.2625 | api, auth | api |
| `webhook-integration-planner` | 0.2036 | 0.2036 | 0.3250 | contract | exist, api |
| `mcp-server-builder` | 0.0941 | 0.0941 | 0.3426 | example, auth | docs, api, auth |

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Family: `api_mcp_tooling`
- Gold skill: `api-security-threat-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Threat-review the billing API for authorization gaps, sensitive data exposure, rate-limit abuse, and validation risks. I need security findings, not user-facing docs.
- Positive-fit instruction after negation cleanup: Threat-review the billing API for authorization gaps, sensitive data exposure, rate-limit abuse, and validation risks. I need security findings, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `api-security-threat-reviewer` | 0.7048 | 0.7048 | 0.3573 | api, authorization, sensitive, data, exposure, rate-limit, abuse, check | security, docs |
| `security-threat-modeler` | 0.4391 | 0.4391 | 0.5474 | data, abuse, check, risk, security | check, risk |
| `public-security-threat-model` | 0.3412 | 0.3412 | 0.3037 | data, exposure, abuse, check, risk | - |
| `public-openai-security-best-practices` | 0.3015 | 0.3015 | 0.1021 | check, risk, security | - |
| `rest-api-contract-designer` | 0.2569 | 0.2569 | 0.3205 | api | api |

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Open the staging dashboard and capture a page snapshot of what the user sees on the account settings page right now. I need the visible state, screenshot-style observations, and any obvious rendering issue; do not click through a full interaction test.
- Positive-fit instruction after negation cleanup: Open the staging dashboard and capture a page snapshot of what the user sees on the account settings page right now. I need the visible state, screenshot-style observations, and any obvious rendering issue; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-page-snapshotter` | 0.4833 | 0.4833 | 0.3344 | page, open, capture, user, visible, state, observation, render | page, test |
| `web-ui-tester` | 0.3115 | 0.3115 | 0.3540 | page, open, user, state, observation, render | page |
| `frontend-debugger` | 0.2856 | 0.2856 | 0.5012 | page, open, user, visible, state, observation, render, issue | page, user, test |
| `web-data-extractor` | 0.1777 | 0.1777 | 0.4489 | page, open, user, visible, observation | page, test |

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Go through the demo signup flow and fill in the form fields with the sample details I provided. Report which fields were entered and pause before final submission if it would create a real account. This is delegated browser form completion, not expected-versus-actual UI validation or a general test report.
- Positive-fit instruction after negation cleanup: Go through the demo signup flow and fill in the form fields with the sample details I provided. Report which fields were entered and pause before final submission if it would create a real account. This is delegated browser form completion, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-form-filler` | 0.5477 | 0.5477 | 0.4165 | form, field, signup, flow, fill, provid, report, enter | flow, test |
| `web-ui-tester` | 0.3497 | 0.3497 | 0.3979 | flow, report, real | form, fill, real |
| `web-page-snapshotter` | 0.2765 | 0.2765 | 0.4040 | form, flow, report | form, fill, browser, test |
| `frontend-debugger` | 0.2239 | 0.2239 | 0.5123 | flow, report, browser | form, fill, browser, test |

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Test whether the checkout page correctly shows a validation message when the postcode field is empty, and report the expected versus actual behavior.
- Positive-fit instruction after negation cleanup: Test whether the checkout page correctly shows a validation message when the postcode field is empty, and report the expected versus actual behavior.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-ui-tester` | 0.3213 | 0.3213 | 0.1458 | test, whether, page, correctly, check, message, report, expect | page |
| `web-form-filler` | 0.2647 | 0.2647 | 0.3331 | test, whether, checkout, page, check, field, report | test, whether, page |
| `frontend-debugger` | 0.2463 | 0.2463 | 0.3653 | test, whether, page, check, report, behavior | test, page |
| `web-page-snapshotter` | 0.2198 | 0.2198 | 0.2555 | test, whether, page, show, report, behavior | test, page |

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From this product listing page, extract the product names, prices, availability labels, and detail-page links into a structured table. I do not need a screenshot.
- Positive-fit instruction after negation cleanup: From this product listing page, extract the product names, prices, availability labels, and detail-page links into a structured table. I .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-data-extractor` | 0.5382 | 0.5382 | 0.2507 | list, page, extract, name, price, label, link, structur | page |
| `web-page-snapshotter` | 0.1500 | 0.1500 | 0.2650 | page, extract, structur | page, extract, structur |
| `web-ui-tester` | 0.0492 | 0.0492 | 0.1624 | page, extract | page, extract |
| `frontend-debugger` | -0.0214 | -0.0214 | 0.0562 | page, extract | page |

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The settings page opens but clicking Save does nothing, and the console shows `Cannot read properties of undefined (reading 'id')` after the profile API call. Use the UI symptom as evidence, then inspect the frontend event handler, state update path, and API response contract. The deliverable is the likely source-level cause plus the smallest code patch.
- Positive-fit instruction after negation cleanup: The settings page opens but clicking Save does nothing, and the console shows `Cannot read properties of undefined (reading 'id')` after the profile API call. Use the UI symptom as evidence, then inspect the frontend event handler, state update path, and API response contract. The deliverable is the likely source-level cause plus the smallest code patch.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `frontend-debugger` | 0.3154 | 0.3154 | 0.2348 | api, page, open, console, symptom, evidence, inspect, frontend | page, code |
| `web-ui-tester` | 0.2291 | 0.2291 | 0.2342 | page, open, console, evidence, state, path | page, frontend, source-level, cause, code, patch |
| `web-page-snapshotter` | 0.1547 | 0.1547 | 0.3356 | page, open, show, evidence, inspect, state, code | page, frontend, cause |
| `code-reviewer` | 0.1070 | 0.1070 | 0.1483 | evidence, path, likely, code | - |

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Evaluate the signup form for keyboard navigation, input labels, focus order, and whether screen-reader users can understand the error messages.
- Positive-fit instruction after negation cleanup: Evaluate the signup form for keyboard navigation, input labels, focus order, and whether screen-reader users can understand the error messages.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `accessibility-checker` | 0.5011 | 0.5011 | 0.4697 | keyboard, label, focu, order, whether, screen-reader, user | form, user |
| `frontend-debugger` | 0.3576 | 0.3576 | 0.3887 | whether, user, error | form, user |
| `web-ui-tester` | 0.3313 | 0.3313 | 0.3645 | navigation, input, whether, user, error, message | form |
| `web-page-snapshotter` | 0.3296 | 0.3296 | 0.3867 | form, whether, user | form |

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this local change before I commit it. The patch updates the cache key from `user.id` to `user.email`, adds a fallback for missing names, and changes the unit test fixture. I want to know if this could introduce bugs or missing-test risk, not have you rewrite it yet.
- Positive-fit instruction after negation cleanup: Review this local change before I commit it. The patch updates the cache key from `user.id` to `user.email`, adds a fallback for missing names, and changes the unit test fixture. I want to know if this could introduce bugs or missing-test risk, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `code-reviewer` | 0.2810 | 0.2810 | 0.1853 | change, user, review, local, commit, miss, test, bugs | change, review |
| `ci-failure-debugger` | 0.2236 | 0.2236 | 0.2216 | user, review, test | review, test |
| `pr-reviewer` | 0.2213 | 0.2213 | 0.2293 | user, review, commit, test, risk | change, review, local |
| `review-comment-resolver` | 0.1631 | 0.1631 | 0.1514 | change, user, review, test | review |

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Can you review this pull request as if you were leaving PR feedback? It changes the auth middleware, adds a migration, updates two API tests, and the PR discussion says the branch is meant to preserve backward compatibility.
- Positive-fit instruction after negation cleanup: Can you review this pull request as if you were leaving PR feedback? It changes the auth middleware, adds a migration, updates two API tests, and the PR discussion says the branch is meant to preserve backward compatibility.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pr-reviewer` | 0.3789 | 0.3789 | 0.2941 | review, extract, request, migration, test, discussion, branch, compatibility | review, change |
| `ci-failure-debugger` | 0.2542 | 0.2542 | 0.2752 | review, request, test | review, test |
| `code-reviewer` | 0.2240 | 0.2240 | 0.5188 | review, request, change, test | review, extract, request, change |
| `review-comment-resolver` | 0.1728 | 0.1728 | 0.3383 | review, request, change, test, preserve | review, extract, request |

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I already got review comments on this branch. Please address this specific reviewer request by planning and making the requested code/test change: `The retry loop can spin forever if the response is 429 and Retry-After is missing. Please add a cap and a test.` I need the existing comment resolved with an implementation response, not a fresh PR review or CI debugging.
- Positive-fit instruction after negation cleanup: I already got review comments on this branch. Please address this specific reviewer request by planning and making the requested code/test change: `The retry loop can spin forever if the response is 429 and Retry-After is missing. Please add a cap and a test.` I need the existing comment resolved with an implementation response, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `review-comment-resolver` | 0.4621 | 0.4621 | 0.5097 | comment, request, test, reply, already, review, addres, plan | review, comment, request, addres, specific, code, fresh, debug |
| `ci-failure-debugger` | 0.3970 | 0.3970 | 0.5052 | comment, request, test, review, code | review, comment, test, plan, code |
| `code-reviewer` | 0.3961 | 0.3961 | 0.4976 | comment, request, test, review, code, change, miss, implementation | review, comment, request, change, debug |
| `pr-reviewer` | 0.3828 | 0.3828 | 0.4664 | comment, request, test, review, branch, code | review, code, change, debug |

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The CI run failed after my last commit. The failing job is `unit-tests`, and the first useful error says `Expected status 200, received 401` in `auth.middleware.test.ts` after the token refresh change. Help me find the cause and the smallest fix.
- Positive-fit instruction after negation cleanup: The CI run failed after my last commit. The failing job is `unit-tests`, and the first useful error says `Expected status 200, received 401` in `auth.middleware.test.ts` after the token refresh change. Help me find the cause and the smallest fix.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `ci-failure-debugger` | 0.4860 | 0.4860 | 0.3947 | fail, run, job, first, useful, error, test, cause | fail, test |
| `code-reviewer` | 0.1564 | 0.1564 | 0.2406 | commit, test, change | fail, run, change |
| `pr-reviewer` | 0.1518 | 0.1518 | 0.2683 | commit, first, test | fail, job, change |
| `review-comment-resolver` | 0.0994 | 0.0994 | 0.3090 | run, receiv, test, change, smallest | - |

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn these completed changes into a concise internal changelog entry for the repository changelog, grouped by change type if useful: fixed retry timeout handling, added token-refresh tests, improved cache invalidation for renamed users, and removed an unused feature flag. Do not write user-facing release notes.
- Positive-fit instruction after negation cleanup: Turn these completed changes into a concise internal changelog entry for the repository changelog, grouped by change type if useful: fixed retry timeout handling, added token-refresh tests, improved cache invalidation for renamed users, and removed an unused feature flag. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `changelog-writer` | 0.5204 | 0.5204 | 0.4216 | change, changelog, complet, concise, internal, entry, group, type | change, release, note |
| `release-note-writer` | 0.4630 | 0.4630 | 0.5652 | change, changelog, turn, complet, useful, user | change, changelog, internal, release |
| `pr-reviewer` | 0.3460 | 0.3460 | 0.3045 | changelog, concise, test, user | change, changelog, release, note |
| `code-reviewer` | 0.3310 | 0.3310 | 0.4049 | change, changelog, concise, test, user | change, changelog |

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write user-facing release notes for this update. We improved sign-in reliability when sessions expire, made profile changes appear faster across devices, and fixed a retry issue that could delay requests during temporary service pressure.
- Positive-fit instruction after negation cleanup: Write user-facing release notes for this update. We improved sign-in reliability when sessions expire, made profile changes appear faster across devices, and fixed a retry issue that could delay requests during temporary service pressure.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `release-note-writer` | 0.2885 | 0.2885 | 0.2564 | user-fac, release, note, update, change, request | release, change, request |
| `changelog-writer` | 0.2081 | 0.2081 | 0.2367 | write, user-fac, release, note, change, request | release, note, change |
| `pr-reviewer` | 0.1370 | 0.1370 | 0.1107 | user-fac, release, note, issue, request | release, note, change |
| `code-reviewer` | 0.1136 | 0.1136 | 0.1645 | release, note, change, issue, request | change, request |

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. I need a broad exploratory orientation: what the sheet contains, the overall picture, the main patterns, the most useful caveats, and a few sensible next questions. Do not turn it into an executive report, forecast, ranking recommendation, or diagnosis of one specific problem yet.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. I need a broad exploratory orientation: what the sheet contains, the overall picture, the main patterns, the most useful caveats, and a few sensible next questions. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-overview` | 0.4625 | 0.4625 | 0.3599 | csv, broad, overall, picture, main, pattern, most | report, forecast, rank, recommendation, specific |
| `data-analysis-for-reporting` | 0.3918 | 0.3918 | 0.4640 | csv, main, most, useful, caveat, question | main, forecast, rank |
| `data-analysis-with-anomaly-focus` | 0.3251 | 0.3251 | 0.3298 | csv, broad, pattern | pattern, report, forecast |
| `data-analysis-with-validation` | 0.2399 | 0.2399 | 0.3840 | csv, main, most, next | broad, report, rank |

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Build an anomaly watchlist: which spikes, dips, outliers, or concentrated deviations look most worth worrying about, and how confident should I be that each one is real? Do not explain root cause yet.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Build an anomaly watchlist: which spikes, dips, outliers, or concentrated deviations look most worth worrying about, and how confident should I be that each one is real? .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-with-anomaly-focus` | 0.6271 | 0.6271 | 0.4897 | csv, anomaly, watchlist, spike, dips, outlier, concentrat, deviation | anomaly, explain, root, cause |
| `data-analysis-overview` | 0.3874 | 0.3874 | 0.4279 | csv, anomaly, most | spike, explain, cause |
| `data-analysis-for-root-cause-diagnosis` | 0.3383 | 0.3383 | 0.3524 | csv, anomaly, look, most | look |
| `data-analysis-with-validation` | 0.2825 | 0.2825 | 0.2858 | csv, anomaly, most | explain, cause |

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Please read channel_performance_weekly.csv. Before I react to it, audit whether the numbers are trustworthy: check for missing values, inconsistent rows, suspicious outliers, denominator issues, or measurement artifacts that could make a genuine problem look worse than it is.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Before I react to it, audit whether the numbers are trustworthy: check for missing values, inconsistent rows, suspicious outliers, denominator issues, or measurement artifacts that could make a genuine problem look worse than it is.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-with-anomaly-focus` | 0.3491 | 0.3491 | 0.4401 | csv, check, value, outlier, issue, look, than | check |
| `data-analysis-with-validation` | 0.3473 | 0.3473 | 0.2153 | csv, whether, check, miss, value, inconsistent, issue, problem | - |
| `data-analysis-overview` | 0.2926 | 0.2926 | 0.4180 | csv, check, miss, value, rows | whether |
| `data-analysis-for-root-cause-diagnosis` | 0.2892 | 0.2892 | 0.3696 | csv, check, issue, problem, look, than | whether, look |

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. This seems to be getting worse. Assume the data is usable enough for analysis and trace the most likely driver: which channel, metric, or segment appears to explain the degradation, and what evidence supports that diagnosis?
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. This seems to be getting worse. Assume the data is usable enough for analysis and trace the most likely driver: which channel, metric, or segment appears to explain the degradation, and what evidence supports that diagnosis?

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-root-cause-diagnosis` | 0.3128 | 0.3128 | 0.2281 | csv, data, analysi, most, likely, driver, channel, metric | data |
| `data-analysis-with-anomaly-focus` | 0.2354 | 0.2354 | 0.2537 | csv, data, analysi, segment, appear, explain, evidence, diagnosi | data, explain |
| `data-analysis-overview` | 0.2273 | 0.2273 | 0.2426 | csv, data, analysi, most, diagnosi | data, explain |
| `data-analysis-with-validation` | 0.1910 | 0.1910 | 0.2062 | csv, data, analysi, most, support, diagnosi | likely, explain |

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Turn this into an upward-facing reporting brief: a headline, two or three executive takeaways, the clearest supporting numbers, and one caveat. Do not give me a broad exploratory analysis.
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Turn this into an upward-facing reporting brief: a headline, two or three executive takeaways, the clearest supporting numbers, and one caveat. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-reporting` | 0.5273 | 0.5273 | 0.3493 | csv, turn, upward-fac, report, headline, executive, takeaway, support | - |
| `data-analysis-overview` | 0.3977 | 0.3977 | 0.3875 | csv, report, takeaway | report |
| `data-analysis-for-root-cause-diagnosis` | 0.3412 | 0.3412 | 0.4107 | csv, report, support | report, broad |
| `data-analysis-with-anomaly-focus` | 0.2881 | 0.2881 | 0.3682 | csv, report | report |

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read channel_performance_weekly.csv. Forecast the likely next direction if the current pattern keeps going: what seems likely to happen next, what evidence supports that continuation, and how much should I trust the forecast?
- Positive-fit instruction after negation cleanup: Please read channel_performance_weekly.csv. Forecast the likely next direction if the current pattern keeps going: what seems likely to happen next, what evidence supports that continuation, and how much should I trust the forecast?

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-forecasting` | 0.5468 | 0.5468 | 0.1054 | forecast, likely, next, csv, direction, current, pattern, happen | current, happen |
| `data-analysis-for-root-cause-diagnosis` | 0.2621 | 0.2621 | 0.2135 | forecast, likely, next, csv, pattern, evidence, support | forecast |
| `data-analysis-with-anomaly-focus` | 0.2506 | 0.2506 | 0.2971 | forecast, csv, pattern, evidence | forecast, pattern |
| `data-analysis-overview` | 0.1957 | 0.1957 | 0.2668 | forecast, csv, pattern, keep | forecast, trust |

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read pilot_priority_options.csv. Compare the options, rank them for action now, recommend the first choice, explain the decision criteria and trade-offs behind that ordering, and say what follow-up check would reduce decision risk. This is a selection task, not a forecast of one metric or a broad overview.
- Positive-fit instruction after negation cleanup: Please read pilot_priority_options.csv. Compare the options, rank them for action now, recommend the first choice, explain the decision criteria and trade-offs behind that ordering, and say what follow-up check would reduce decision risk. This is a selection task, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `data-analysis-for-ranking-selection` | 0.5682 | 0.5682 | 0.4504 | decision, csv, compare, option, rank, recommend, choice, criteria | decision, option, selection, forecast, broad, overview |
| `data-analysis-for-forecasting` | 0.3058 | 0.3058 | 0.2730 | csv, compare, option, rank, explain, check, risk, task | rank, explain |
| `data-analysis-overview` | 0.2984 | 0.2984 | 0.2977 | csv, rank, check, task | rank, explain, forecast |
| `data-analysis-for-reporting` | 0.2588 | 0.2588 | 0.4333 | csv, rank, them, check, risk, task | decision, option, rank, selection, forecast |

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.
- Positive-fit instruction after negation cleanup: The checkout flow at `http://localhost:4173/checkout` fails after I click Apply coupon. Please reproduce the interaction with browser evidence, capture console or network clues, and identify why the flow breaks.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `playwright-flow-debugger` | 0.2499 | 0.2499 | 0.1125 | flow, fail, reproduce, interaction, browser, evidence, capture, console | interaction |
| `public-playwright-interactive` | 0.0934 | 0.0934 | 0.0676 | interaction, browser, evidence, capture, console | - |
| `public-openai-playwright` | 0.0467 | 0.0467 | 0.0676 | flow, interaction, browser, evidence | - |
| `visual-regression-checker` | 0.0393 | 0.0393 | 0.2462 | flow, evidence, capture, identify | fail, click, why |
| `accessibility-interaction-auditor` | -0.0133 | -0.0133 | 0.0080 | flow, interaction, evidence, clue, identify | - |

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please compare the baseline and current screenshots for pricing_page_desktop.png and pricing_page_mobile.png. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.
- Positive-fit instruction after negation cleanup: Please compare the baseline and current screenshots for pricing_page_desktop.png and pricing_page_mobile.png. I need visual regressions like clipping, spacing shifts, text overflow, and contrast changes.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `visual-regression-checker` | 0.6520 | 0.6520 | 0.0783 | compare, baseline, current, screenshot, visual, regression, clipp, spac | - |
| `accessibility-interaction-auditor` | 0.2576 | 0.2576 | 0.5062 | visual, contrast, change | compare, visual, regression |
| `public-openai-screenshot` | 0.2387 | 0.2387 | 0.1069 | compare, screenshot, visual | - |
| `playwright-flow-debugger` | 0.2006 | 0.2006 | 0.4653 | screenshot, visual | compare, screenshot, visual |
| `public-anthropic-webapp-testing` | 0.1771 | 0.1771 | 0.1069 | screenshot, visual | - |

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.
- Positive-fit instruction after negation cleanup: Please audit the account-settings modal for keyboard and screen-reader interaction. Focus on tab order, focus trapping, accessible names, ARIA state, and whether form errors are announced.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `accessibility-interaction-auditor` | 0.6121 | 0.6121 | 0.1641 | focu, audit, modal, keyboard, screen-reader, interaction, order, accessible | - |
| `playwright-flow-debugger` | 0.3668 | 0.3668 | 0.2476 | interaction, state, whether | interaction |
| `visual-regression-checker` | 0.3613 | 0.3613 | 0.2833 | name, state | audit |
| `web-ui-tester` | 0.2756 | 0.2756 | 0.3633 | interaction, state, whether, error | form |
| `public-anthropic-webapp-testing` | 0.1394 | 0.1394 | 0.0888 | interaction, state | - |

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The Netlify deploy for build_log.txt failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.
- Positive-fit instruction after negation cleanup: The Netlify deploy for build_log.txt failed. Please inspect the build log and identify the likely root cause, missing env/config assumptions, and the smallest rerun sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `deployment-build-triager` | 0.3902 | 0.3902 | 0.1827 | deploy, fail, build, identify, likely, root, cause, miss | deploy, build |
| `deployment-release-verifier` | 0.2347 | 0.2347 | 0.3739 | deploy, fail, build, config | fail, build, log |
| `web-performance-budget-checker` | 0.0885 | 0.0885 | -0.0016 | identify, assumption | - |
| `playwright-flow-debugger` | 0.0687 | 0.0687 | 0.1082 | fail, identify | build |

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Gold rank among listed candidates: 2
- Instruction used for scoring: The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.
- Positive-fit instruction after negation cleanup: The production deploy is live at `https://example-release.netlify.app`. Please verify release readiness with URL smoke checks, version evidence, asset loading, critical routes, environment sanity, and rollback notes.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-netlify-deploy` | 0.6129 | 0.6129 | 0.0880 | check, production, deploy, live, http, netlify, app, url | - |
| `deployment-release-verifier` | 0.4603 | 0.4603 | 0.3178 | check, deploy, release, readines, url, smoke, version, evidence | - |
| `deployment-build-triager` | 0.3946 | 0.3946 | 0.3727 | check, deploy, release, version, evidence, environment | check, deploy, url |
| `public-openai-vercel-deploy` | 0.2851 | 0.2851 | 0.0880 | check, deploy, live, app, url, environment | - |
| `visual-regression-checker` | 0.1219 | 0.1219 | 0.3511 | check, evidence | smoke |

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review lighthouse_trace_summary.txt against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.
- Positive-fit instruction after negation cleanup: Please review lighthouse_trace_summary.txt against a mobile performance budget. I care about LCP, blocking scripts, network weight, image size, and which fixes matter most.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `web-performance-budget-checker` | 0.5212 | 0.5212 | 0.2677 | review, against, performance, budget, block, network, weight, image | - |
| `visual-regression-checker` | 0.3194 | 0.3194 | 0.1197 | image, size | - |
| `deployment-release-verifier` | 0.2475 | 0.2475 | 0.2700 | block | - |
| `accessibility-interaction-auditor` | 0.2406 | 0.2406 | 0.2887 | - | review |

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read internal_travel_policy_update.txt and help me make sense of it quickly. I want the main point, the most important details, and anything I should pay attention to.
- Positive-fit instruction after negation cleanup: Please read internal_travel_policy_update.txt and help me make sense of it quickly. I want the main point, the most important details, and anything I should pay attention to.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-summariser` | 0.2300 | 0.2300 | 0.1477 | read, quickly, main, point, most, important, detail | - |
| `document-field-extractor` | 0.1414 | 0.1414 | 0.1356 | read, important | main |
| `document-converter` | 0.1227 | 0.1227 | 0.0895 | main, most, important, detail | - |
| `document-normaliser` | 0.1171 | 0.1171 | 0.1217 | important | main |

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read travel_request_note_raw.txt and produce a revised full prose version for a human reader. Keep it as continuous paragraphs in the same document form, improve wording, flow, and polish, and preserve the same meaning and commitments.
- Positive-fit instruction after negation cleanup: Please read travel_request_note_raw.txt and produce a revised full prose version for a human reader. Keep it as continuous paragraphs in the same document form, improve wording, flow, and polish, and preserve the same meaning and commitments.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-rewriter` | 0.5785 | 0.5785 | 0.4123 | same, revis, prose, version, human, reader, keep, document | - |
| `document-converter` | 0.5292 | 0.5292 | 0.4180 | keep, document, form, preserve, mean | document |
| `document-summariser` | 0.5103 | 0.5103 | 0.4340 | read, document, form, preserve | document, polish |
| `document-normaliser` | 0.4772 | 0.4772 | 0.4896 | version, keep, document, form, word, preserve, mean | document, mean |

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read travel_request_note_raw.txt and normalise the document structure: keep the original wording and order as much as possible, but fix inconsistent headings, spacing, list style, and layout noise. Do not substantially rewrite the prose.
- Positive-fit instruction after negation cleanup: Please read travel_request_note_raw.txt and normalise the document structure: keep the original wording and order as much as possible, but fix inconsistent headings, spacing, list style, and layout noise. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-normaliser` | 0.5602 | 0.5602 | 0.4387 | normalize, document, structure, keep, original, word, order, possible | document, layout |
| `document-converter` | 0.4501 | 0.4501 | 0.4151 | document, structure, keep, layout, noise | document, layout, rewrite |
| `document-rewriter` | 0.4334 | 0.4334 | 0.3859 | document, structure, keep, original, word | normalize, noise, rewrite |
| `document-summariser` | 0.3965 | 0.3965 | 0.3566 | read, document | document, layout, rewrite |

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read invoice_northbridge_supplies.txt and extract the reusable fields into a structured table, including supplier, invoice number, dates, line items, totals, and payment details. Do not write a narrative summary.
- Positive-fit instruction after negation cleanup: Please read invoice_northbridge_supplies.txt and extract the reusable fields into a structured table, including supplier, invoice number, dates, line items, totals, and payment details. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-field-extractor` | 0.4346 | 0.4346 | 0.3466 | read, extract, field, structur, invoice, date, item, total | narrative, summary |
| `document-summariser` | 0.3306 | 0.3306 | 0.3638 | read, extract, structur, invoice, detail | extract, field, date |
| `layout-preserving-converter` | 0.3278 | 0.3278 | 0.4124 | extract, field, structur, table, invoice | extract, field, narrative, summary |
| `multi-document-comparison-preparer` | 0.3202 | 0.3202 | 0.2857 | extract, field, structur, invoice, detail | extract, summary |

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read policy_draft_a.txt and policy_draft_b.txt, then prepare a side-by-side comparison matrix so I can quickly see matching sections, changed wording, additions, removals, and unresolved differences.
- Positive-fit instruction after negation cleanup: Please read policy_draft_a.txt and policy_draft_b.txt, then prepare a side-by-side comparison matrix so I can quickly see matching sections, changed wording, additions, removals, and unresolved differences.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `multi-document-comparison-preparer` | 0.5349 | 0.5349 | 0.3378 | prepare, compare, see, match, section, difference | chang |
| `document-normaliser` | 0.3421 | 0.3421 | 0.2425 | compare, see, section, word | chang |
| `document-converter` | 0.3235 | 0.3235 | 0.3590 | compare, see, section | - |
| `document-field-extractor` | 0.2796 | 0.2796 | 0.2521 | read, compare, see | compare |

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read request_form.txt and convert the whole form into clean markdown notes I can drop into my repo. Preserve the content and labels, but simplify the source formatting rather than keeping the exact visual layout.
- Positive-fit instruction after negation cleanup: Please read request_form.txt and convert the whole form into clean markdown notes I can drop into my repo. Preserve the content and labels, but simplify the source formatting .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-converter` | 0.5454 | 0.5454 | 0.3915 | convert, form, markdown, note, preserve, content, label, simplify | content, layout |
| `document-normaliser` | 0.4530 | 0.4530 | 0.3989 | convert, form, clean, preserve, content, label, formatt | convert, content, layout |
| `layout-preserving-converter` | 0.3914 | 0.3914 | 0.3549 | convert, form, preserve, content, label, but, formatt | convert, content, layout |
| `document-summariser` | 0.3316 | 0.3316 | 0.2851 | read, convert, form, note, preserve | convert, layout |

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please read request_form.txt and turn it into markdown while preserving the layout cues: headings, labels, rows, and grouped fields should remain recognizable. The priority is layout fidelity, not just simplified notes.
- Positive-fit instruction after negation cleanup: Please read request_form.txt and turn it into markdown while preserving the layout cues: headings, labels, rows, and grouped fields should remain recognizable. The priority is layout fidelity, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `layout-preserving-converter` | 0.4111 | 0.4111 | 0.3099 | layout, preserv, cues, heading, label, rows, group, field | layout, field |
| `document-normaliser` | 0.3427 | 0.3427 | 0.3847 | preserv, heading, label | layout, preserv, field |
| `document-converter` | 0.3355 | 0.3355 | 0.4941 | layout, turn, markdown, preserv, label, priority, fidelity | layout, preserv, field, fidelity |
| `document-field-extractor` | 0.2181 | 0.2181 | 0.2130 | read, field | - |

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Family: `github_ci_maintenance`
- Gold skill: `ci-log-root-cause-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Inspect ci_log.txt and identify the CI root cause, the first meaningful error, and the smallest rerun sequence.
- Positive-fit instruction after negation cleanup: Inspect ci_log.txt and identify the CI root cause, the first meaningful error, and the smallest rerun sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `ci-log-root-cause-debugger` | 0.6964 | 0.6964 | 0.3463 | identify, root, cause, first, meaningful, error, smallest, rerun | - |
| `repo-code-reviewer` | 0.2116 | 0.2116 | 0.5164 | inspect, identify | - |
| `github-issue-triager` | 0.1979 | 0.1979 | 0.2630 | identify, root, cause | - |
| `pr-review-comment-resolver` | 0.1827 | 0.1827 | 0.6027 | identify | root, cause |
| `release-changelog-generator` | 0.1645 | 0.1645 | 0.5724 | identify | - |

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Family: `github_ci_maintenance`
- Gold skill: `pr-review-comment-resolver`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use pr_review_comments.md to plan how to resolve the review comments and what response to leave. Do not perform a general code review.
- Positive-fit instruction after negation cleanup: Use pr_review_comments.md to plan how to resolve the review comments and what response to leave. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pr-review-comment-resolver` | 0.6163 | 0.6163 | 0.2274 | plan, resolve, review, comment, reply | - |
| `review-comment-resolver` | 0.5654 | 0.5654 | 0.4896 | plan, review, comment, reply | review, comment, perform, code |
| `repo-code-reviewer` | 0.4411 | 0.4411 | 0.5173 | review, comment | review, comment |
| `public-openai-gh-address-comments` | 0.4268 | 0.4268 | 0.0113 | review, comment | - |
| `ci-log-root-cause-debugger` | 0.1661 | 0.1661 | 0.4795 | - | review, code |

### `github_ci_maintenance_p3_repo_code_reviewer`

- Family: `github_ci_maintenance`
- Gold skill: `repo-code-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review the diff described in payment_diff.patch for bugs and missing tests. This is a fresh code review, not a CI log diagnosis.
- Positive-fit instruction after negation cleanup: Review the diff described in payment_diff.patch for bugs and missing tests. This is a fresh code review, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `repo-code-reviewer` | 0.4470 | 0.4470 | 0.5816 | review, diff, bugs, miss, test | review |
| `github-issue-triager` | 0.2394 | 0.2394 | 0.4050 | miss | review, diff, code |
| `pr-review-comment-resolver` | 0.2391 | 0.2391 | 0.5047 | review, patch, code | - |
| `ci-log-root-cause-debugger` | 0.2243 | 0.2243 | 0.4664 | test | review, code |
| `release-changelog-generator` | 0.1765 | 0.1765 | 0.6070 | - | review, code |

### `github_ci_maintenance_p4_github_issue_triager`

- Family: `github_ci_maintenance`
- Gold skill: `github-issue-triager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Triage the issues in issues.md into bug/feature/support labels, priority, owner guess, and missing reproduction details.
- Positive-fit instruction after negation cleanup: Triage the issues in issues.md into bug/feature/support labels, priority, owner guess, and missing reproduction details.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `github-issue-triager` | 0.4878 | 0.4878 | 0.3597 | issue, triage, label, priority, owner, miss, reproduction, detail | - |
| `repo-code-reviewer` | 0.3287 | 0.3287 | 0.3337 | miss | - |
| `pr-review-comment-resolver` | 0.3143 | 0.3143 | 0.3120 | - | - |
| `release-changelog-generator` | 0.2721 | 0.2721 | 0.3435 | - | issue, triage |
| `ci-log-root-cause-debugger` | 0.2264 | 0.2264 | 0.3501 | - | issue, triage |

### `github_ci_maintenance_p5_release_changelog_generator`

- Family: `github_ci_maintenance`
- Gold skill: `release-changelog-generator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn merged_prs.md into release notes grouped by features, fixes, and breaking changes. Do not review the code.
- Positive-fit instruction after negation cleanup: Turn merged_prs.md into release notes grouped by features, fixes, and breaking changes. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `release-changelog-generator` | 0.5439 | 0.5439 | 0.2499 | release, note, group, fixe, break, change | review, code |
| `pr-review-comment-resolver` | 0.4447 | 0.4447 | 0.2799 | turn, group, change | - |
| `repo-code-reviewer` | 0.4126 | 0.4126 | 0.3631 | - | release, note, review |
| `github-issue-triager` | 0.3907 | 0.3907 | 0.4835 | - | note, review, code |
| `ci-log-root-cause-debugger` | 0.2035 | 0.2035 | 0.3022 | - | release, note, review, code |

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Family: `github_ci_maintenance`
- Gold skill: `git-safety-guardrail-installer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design repository guardrails to block accidental `git push`, `reset --hard`, and secret commits. I need hook/config steps and verification, not issue triage.
- Positive-fit instruction after negation cleanup: Design repository guardrails to block accidental `git push`, `reset --hard`, and secret commits. I need hook/config steps and verification, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `git-safety-guardrail-installer` | 0.7483 | 0.7483 | 0.2277 | repository, guardrail, block, git, secret, commit, hook, config | issue |
| `public-mattpocock-git-guardrails-claude-code` | 0.5411 | 0.5411 | 0.0369 | guardrail, block, git, push, reset, hard, hook | - |
| `pr-review-comment-resolver` | 0.3844 | 0.3844 | 0.4119 | step, verification | git, hook |
| `public-mattpocock-setup-pre-commit` | 0.3828 | 0.3828 | 0.0369 | commit, hook | - |
| `ci-log-root-cause-debugger` | 0.2145 | 0.2145 | 0.2573 | repository | issue, triage |

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-dataset-viewer-inspector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: For the dataset described in customer_tickets_dataset.md, inspect expected subsets, splits, columns, and row examples before we choose any model.
- Positive-fit instruction after negation cleanup: For the dataset described in customer_tickets_dataset.md, inspect expected subsets, splits, columns, and row examples before we choose any model.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `hf-dataset-viewer-inspector` | 0.5779 | 0.5779 | 0.0906 | dataset, inspect, expect, subset, split, column, row, example | model |
| `public-huggingface-datasets` | 0.3934 | 0.3934 | 0.0948 | dataset, subset, split | - |
| `hf-local-model-selector` | 0.2472 | 0.2472 | 0.4546 | choose, model | dataset, inspect, model |
| `sentence-transformer-finetuner` | 0.1866 | 0.1866 | 0.3242 | split, example, choose, model | dataset, inspect, column |
| `public-huggingface-huggingface-tool-builder` | 0.0881 | 0.0881 | 0.0948 | example, model | - |

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-local-model-selector`
- Gold rank among listed candidates: 2
- Instruction used for scoring: I need a local model for classifying support tickets on an 8 GB Mac. Choose realistic Hugging Face/GGUF candidates and quantization options; do not design a dataset audit.
- Positive-fit instruction after negation cleanup: I need a local model for classifying support tickets on an 8 GB Mac. Choose realistic Hugging Face/GGUF candidates and quantization options; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-huggingface-huggingface-local-models` | 0.4486 | 0.4486 | 0.1427 | local, model, mac, realistic, gguf | - |
| `hf-local-model-selector` | 0.4461 | 0.4461 | 0.2917 | local, model, choose, hugg, face, gguf, candidate, quantization | model, dataset |
| `hf-dataset-viewer-inspector` | 0.2853 | 0.2853 | 0.3137 | model, hugg, face | local, model |
| `public-huggingface-huggingface-best` | 0.2126 | 0.2126 | 0.1427 | realistic | - |
| `sentence-transformer-finetuner` | 0.1727 | 0.1727 | 0.2747 | model, choose | local, dataset |

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Family: `huggingface_ml_workflows`
- Gold skill: `sentence-transformer-finetuner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: We have labelled skill-query pairs and hard negatives for agent skill routing. Plan a sentence-transformer fine-tuning setup with losses, splits, and retrieval metrics.
- Positive-fit instruction after negation cleanup: We have labelled skill-query pairs and hard negatives for agent skill routing. Plan a sentence-transformer fine-tuning setup with losses, splits, and retrieval metrics.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `sentence-transformer-finetuner` | 0.6528 | 0.6528 | 0.1694 | pair, hard, negative, plan, sentence-transformer, fine-tun, losse, split | - |
| `public-huggingface-train-sentence-transformers` | 0.5184 | 0.5184 | 0.3599 | pair, skill, sentence-transformer, retrieval | skill |
| `public-swebench-similarity-search-patterns` | 0.4131 | 0.4131 | 0.0702 | skill, retrieval | - |
| `hf-dataset-viewer-inspector` | 0.1953 | 0.1953 | 0.4274 | split | - |
| `hf-local-model-selector` | 0.1597 | 0.1597 | 0.3288 | setup | fine-tun |

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Family: `huggingface_ml_workflows`
- Gold skill: `gradio-demo-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a small Python web UI plan for a ticket classifier with a text box, confidence display, sample inputs, and launch checks. We already have the model; do not discuss fine-tuning.
- Positive-fit instruction after negation cleanup: Create a small Python web UI plan for a ticket classifier with a text box, confidence display, sample inputs, and launch checks. We already have the model; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `gradio-demo-builder` | 0.3695 | 0.3695 | 0.1541 | web, plan, display, input, launch, check, model | model |
| `hf-dataset-viewer-inspector` | 0.2662 | 0.2662 | 0.2728 | check, model | model |
| `sentence-transformer-finetuner` | 0.2457 | 0.2457 | 0.1872 | plan, check, model | - |
| `hf-local-model-selector` | 0.2157 | 0.2157 | 0.2283 | check, model | model, fine-tun |
| `hf-zerogpu-space-deployer` | 0.0766 | 0.0766 | 0.3291 | plan, check | model |

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-zerogpu-space-deployer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare our Gradio classifier for Hugging Face ZeroGPU Spaces. Focus on dependency files, GPU queue behavior, sleep constraints, and deployment verification.
- Positive-fit instruction after negation cleanup: Prepare our Gradio classifier for Hugging Face ZeroGPU Spaces. Focus on dependency files, GPU queue behavior, sleep constraints, and deployment verification.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `hf-zerogpu-space-deployer` | 0.6800 | 0.6800 | 0.2883 | prepare, hugg, face, zerogpu, space, dependency, file, gpu | - |
| `gradio-demo-builder` | 0.3958 | 0.3958 | 0.2056 | gradio, behavior, constraint | - |
| `hf-local-model-selector` | 0.3284 | 0.3284 | 0.2365 | hugg, face, constraint, verification | - |
| `hf-dataset-viewer-inspector` | 0.2690 | 0.2690 | 0.4046 | hugg, face, constraint, deployment | gradio |
| `sentence-transformer-finetuner` | 0.1640 | 0.1640 | 0.4452 | - | gradio |

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-community-eval-runner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compare two Hugging Face classifiers on a held-out ticket dataset using reproducible metrics. I need an evaluation plan and result table, not a Gradio app.
- Positive-fit instruction after negation cleanup: Compare two Hugging Face classifiers on a held-out ticket dataset using reproducible metrics. I need an evaluation plan and result table, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `hf-community-eval-runner` | 0.4833 | 0.4833 | 0.3033 | hugg, face, dataset, reproducible, metric, evaluation, plan, result | dataset |
| `hf-dataset-viewer-inspector` | 0.3359 | 0.3359 | 0.2306 | hugg, face, dataset | gradio |
| `sentence-transformer-finetuner` | 0.2501 | 0.2501 | 0.4148 | metric, evaluation, plan | dataset, gradio |
| `hf-local-model-selector` | 0.1983 | 0.1983 | 0.2733 | compare, hugg, face | dataset |
| `gradio-demo-builder` | 0.0899 | 0.0899 | 0.0425 | dataset, plan | - |

### `implicit_p10_trace_path`

- Family: `implicit_field_stress`
- Gold skill: `implicit-trace-path-diagnoser`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Use these distributed trace spans to locate where checkout latency is introduced across services.
- Positive-fit instruction after negation cleanup: Use these distributed trace spans to locate where checkout latency is introduced across services.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `distributed-trace-investigator` | 0.7035 | 0.7035 | 0.2439 | distribut, trace, span, locate, latency, acros, service | trace |
| `implicit-trace-path-diagnoser` | 0.5956 | 0.5956 | 0.2231 | distribut, trace, span, locate, latency, acros, service | - |
| `prometheus-alert-rule-writer` | 0.2983 | 0.2983 | 0.1545 | - | trace |
| `implicit-slo-alert-author` | 0.1985 | 0.1985 | 0.2493 | - | trace |

### `implicit_p1_pdf_answer`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-evidence-answerer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Read the PDF packet and answer whether travel meals after a delay are reimbursable. I need the answer and page evidence, not a reconstructed table.
- Positive-fit instruction after negation cleanup: Read the PDF packet and answer whether travel meals after a delay are reimbursable. I need the answer and page evidence, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `implicit-pdf-evidence-answerer` | 0.2379 | 0.2379 | 0.1960 | answer, read, pdf, packet, page, evidence | table |
| `implicit-pdf-table-reconstructor` | 0.2102 | 0.2102 | -0.0105 | pdf, packet, page | - |
| `pdf-question-answerer` | 0.1678 | 0.1678 | 0.2228 | answer, pdf, page, evidence | pdf, table |
| `pdf-layout-table-extractor` | 0.0984 | 0.0984 | 0.1328 | pdf, page, evidence | answer, pdf |

### `implicit_p2_pdf_table`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-table-reconstructor`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Pull the invoice rows from the PDF with page and row anchors. Keep it as structured data rather than a prose answer.
- Positive-fit instruction after negation cleanup: Pull the invoice rows from the PDF with page and row anchors. Keep it as structured data .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-layout-table-extractor` | 0.6566 | 0.6566 | 0.5082 | extract, invoice, rows, pdf, page, row, anchor, structur | pdf, prose, answer |
| `implicit-pdf-table-reconstructor` | 0.5743 | 0.5743 | 0.0913 | rows, pdf, page, row, structur, data | - |
| `pdf-question-answerer` | 0.4879 | 0.4879 | 0.6056 | extract, pdf, page, anchor, keep | extract, pdf |
| `implicit-pdf-evidence-answerer` | 0.4543 | 0.4543 | 0.1973 | extract, pdf, page, anchor | - |

### `implicit_p3_browser_flow`

- Family: `implicit_field_stress`
- Gold skill: `implicit-browser-flow-investigator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The checkout button stops working after a coupon is applied. Reproduce the click path and use console or network evidence to explain the failure.
- Positive-fit instruction after negation cleanup: The checkout button stops working after a coupon is applied. Reproduce the click path and use console or network evidence to explain the failure.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `implicit-browser-flow-investigator` | 0.1804 | 0.1804 | 0.0569 | click, path, console, network, evidence, failure | - |
| `playwright-flow-debugger` | 0.1397 | 0.1397 | 0.0871 | reproduce, path, console, network, evidence, explain, failure | failure |
| `implicit-visual-diff-reviewer` | 0.0078 | 0.0078 | 0.0561 | - | - |
| `visual-regression-checker` | -0.0165 | -0.0165 | 0.4389 | evidence | button, click |

### `implicit_p4_visual_diff`

- Family: `implicit_field_stress`
- Gold skill: `implicit-visual-diff-reviewer`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Compare the baseline and new screenshots for layout shifts, clipping, spacing, and text overflow across desktop and mobile.
- Positive-fit instruction after negation cleanup: Compare the baseline and new screenshots for layout shifts, clipping, spacing, and text overflow across desktop and mobile.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `visual-regression-checker` | 0.6596 | 0.6596 | 0.1019 | compare, baseline, screenshot, layout, shift, clipp, spac, text | - |
| `implicit-visual-diff-reviewer` | 0.6268 | 0.6268 | 0.1026 | compare, screenshot, layout, clipp, spac, text, overflow, acros | - |
| `implicit-browser-flow-investigator` | 0.3120 | 0.3120 | 0.2335 | screenshot | - |
| `playwright-flow-debugger` | 0.3096 | 0.3096 | 0.4591 | screenshot | compare, screenshot |

### `implicit_p5_ci_failure`

- Family: `implicit_field_stress`
- Gold skill: `implicit-ci-failure-reader`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Look at the CI log and find the first meaningful error plus the smallest fix and rerun sequence.
- Positive-fit instruction after negation cleanup: Look at the CI log and find the first meaningful error plus the smallest fix and rerun sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `implicit-ci-failure-reader` | 0.7248 | 0.7248 | 0.0197 | look, log, first, meaningful, error, smallest, fix, rerun | - |
| `ci-log-root-cause-debugger` | 0.5333 | 0.5333 | 0.2634 | log, find, first, meaningful, error, smallest, fix, rerun | - |
| `repo-code-reviewer` | 0.1726 | 0.1726 | 0.4460 | find, fix | - |
| `implicit-review-comment-planner` | 0.0832 | 0.0832 | 0.2256 | - | - |

### `implicit_p6_review_comments`

- Family: `implicit_field_stress`
- Gold skill: `implicit-review-comment-planner`
- Gold rank among listed candidates: 3
- Instruction used for scoring: Use the existing reviewer feedback to group required fixes, note any questions, and prepare responses for each thread; do not do a fresh code review.
- Positive-fit instruction after negation cleanup: Use the existing reviewer feedback to group required fixes, note any questions, and prepare responses for each thread; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pr-review-comment-resolver` | 0.5098 | 0.5098 | 0.2591 | reviewer, group, requir, question, prepare, reply, each | - |
| `repo-code-reviewer` | 0.4677 | 0.4677 | 0.4323 | - | exist, note, review |
| `implicit-review-comment-planner` | 0.4448 | 0.4448 | 0.4681 | exist, reviewer, feedback, group, requir, question, prepare, reply | fresh, code, review |
| `implicit-ci-failure-reader` | 0.1662 | 0.1662 | 0.0783 | - | - |

### `implicit_p7_hf_dataset`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-dataset-inspector`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Before modelling, inspect the dataset splits, columns, row examples, labels, and schema caveats.
- Positive-fit instruction after negation cleanup: Before modelling, inspect the dataset splits, columns, row examples, labels, and schema caveats.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `hf-dataset-viewer-inspector` | 0.7485 | 0.7485 | 0.2541 | inspect, dataset, split, column, row, example, schema, caveat | - |
| `implicit-hf-dataset-inspector` | 0.6717 | 0.6717 | 0.2575 | modell, inspect, dataset, split, column, example, label, schema | - |
| `hf-local-model-selector` | 0.2916 | 0.2916 | 0.6049 | - | inspect, dataset |
| `implicit-hf-local-model-chooser` | 0.2579 | 0.2579 | 0.0006 | - | - |

### `implicit_p8_hf_model`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-local-model-chooser`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Choose a local model and quantization that can run on an 8 GB laptop for ticket classification.
- Positive-fit instruction after negation cleanup: Choose a local model and quantization that can run on an 8 GB laptop for ticket classification.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `hf-local-model-selector` | 0.4435 | 0.4435 | 0.2666 | choose, local, model, quantization | model |
| `implicit-hf-local-model-chooser` | 0.3218 | 0.3218 | 0.0712 | choose, local, model, quantization | - |
| `implicit-hf-dataset-inspector` | 0.3012 | 0.3012 | 0.5248 | model, quantization, laptop | model, quantization, laptop |
| `hf-dataset-viewer-inspector` | 0.2358 | 0.2358 | 0.3798 | model | local, model |

### `implicit_p9_alert_rule`

- Family: `implicit_field_stress`
- Gold skill: `implicit-slo-alert-author`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create alert rules from these checkout SLO metrics with windows, severity labels, and verification queries.
- Positive-fit instruction after negation cleanup: Create alert rules from these checkout SLO metrics with windows, severity labels, and verification queries.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `implicit-slo-alert-author` | 0.6730 | 0.6730 | 0.3286 | alert, rule, metric, window, severity, label, verification | - |
| `prometheus-alert-rule-writer` | 0.6596 | 0.6596 | 0.1672 | alert, rule, slo, metric, window, severity, label, verification | - |
| `implicit-trace-path-diagnoser` | 0.2621 | 0.2621 | 0.4149 | - | alert, rule |
| `distributed-trace-investigator` | 0.2463 | 0.2463 | 0.4122 | - | alert |

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Give me a triage overview of this service snapshot
- Positive-fit instruction after negation cleanup: Give me a triage overview of this service snapshot

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `metrics-overview` | 0.4828 | 0.4828 | 0.3129 | overview, service, snapshot | - |
| `incident-summary-writer` | 0.3975 | 0.3975 | 0.3015 | overview, service | - |
| `latency-anomaly-detector` | 0.3290 | 0.3290 | 0.3030 | service, snapshot | overview |
| `metrics-root-cause-diagnoser` | 0.2690 | 0.2690 | 0.3669 | service | - |

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Run an anomaly-focused readout on this service snapshot. Identify unusual performance behavior, especially tail-latency spikes, outliers, and whether the deviation is broad or concentrated in a smaller slice of requests. Do not give only a general metrics overview
- Positive-fit instruction after negation cleanup: Run an anomaly-focused readout on this service snapshot. Identify unusual performance behavior, especially tail-latency spikes, outliers, and whether the deviation is broad or concentrated in a smaller slice of requests.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `latency-anomaly-detector` | 0.6334 | 0.6334 | 0.2978 | anomaly-focus, service, snapshot, identify, unusual, performance, behavior, spike | broad, only, overview |
| `metrics-overview` | 0.5063 | 0.5063 | 0.3527 | readout, service, snapshot, identify, whether | whether |
| `slo-breach-checker` | 0.4158 | 0.4158 | 0.3295 | service, snapshot, identify, whether | - |
| `metrics-root-cause-diagnoser` | 0.3750 | 0.3750 | 0.3660 | service, identify, performance, whether | only |

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check this service snapshot against a reliability-objective risk frame
- Positive-fit instruction after negation cleanup: Check this service snapshot against a reliability-objective risk frame

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `slo-breach-checker` | 0.5663 | 0.5663 | 0.3247 | check, service, snapshot, risk | risk |
| `metrics-overview` | 0.4527 | 0.4527 | 0.3647 | service, snapshot | risk |
| `capacity-risk-forecaster` | 0.3630 | 0.3630 | 0.2903 | service, risk | check, against |
| `metrics-root-cause-diagnoser` | 0.3203 | 0.3203 | 0.3646 | check, service, against | check, risk |

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Forecast capacity risk from this service snapshot if the pattern keeps going. Focus on future pressure, saturation risk, queue growth, headroom, and likely bottlenecks that could turn into a bigger operational problem. Do not decide current SLO breach or root cause
- Positive-fit instruction after negation cleanup: Forecast capacity risk from this service snapshot if the pattern keeps going. Focus on future pressure, saturation risk, queue growth, headroom, and likely bottlenecks that could turn into a bigger operational problem.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `capacity-risk-forecaster` | 0.6418 | 0.6418 | 0.3968 | risk, forecast, capacity, service, pattern, focu, future, pressure | current, slo, breach, root, cause |
| `metrics-overview` | 0.3751 | 0.3751 | 0.6417 | forecast, service, snapshot, keep, focu, saturation, queue, operational | risk, forecast, capacity, future, slo, breach, root, cause |
| `slo-breach-checker` | 0.3352 | 0.3352 | 0.3806 | risk, forecast, service, snapshot, operational | risk, forecast, capacity, root, cause |
| `metrics-root-cause-diagnoser` | 0.2779 | 0.2779 | 0.5609 | forecast, service, saturation, likely, operational, problem | risk, forecast, capacity, future, slo |

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Do a root-cause diagnosis for this service snapshot. Compare hypotheses such as downstream dependency latency, queue buildup, CPU pressure, and request mix; identify the most plausible driver of the degradation; and tie the diagnosis to evidence. Snapshot data
- Positive-fit instruction after negation cleanup: Do a root-cause diagnosis for this service snapshot. Compare hypotheses such as downstream dependency latency, queue buildup, CPU pressure, and request mix; identify the most plausible driver of the degradation; and tie the diagnosis to evidence. Snapshot data

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `latency-anomaly-detector` | 0.5137 | 0.5137 | 0.5233 | snapshot, service, compare, latency, identify, driver, evidence | compare, hypothese, most, plausible, driver, degradation |
| `metrics-root-cause-diagnoser` | 0.4798 | 0.4798 | 0.3156 | diagnosi, service, compare, hypothese, dependency, latency, identify, most | - |
| `capacity-risk-forecaster` | 0.4369 | 0.4369 | 0.3794 | service, queue, buildup, cpu, pressure, identify, most, plausible | compare, hypothese, driver, degradation, evidence |
| `incident-summary-writer` | 0.3761 | 0.3761 | 0.4076 | diagnosi, service, identify, most, degradation | root-cause |

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn this service snapshot into an incident update I could quickly share with the team
- Positive-fit instruction after negation cleanup: Turn this service snapshot into an incident update I could quickly share with the team

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `incident-summary-writer` | 0.4794 | 0.4794 | 0.2551 | turn, service, incident, quickly | - |
| `slo-breach-checker` | 0.4150 | 0.4150 | 0.1934 | service, snapshot, incident | incident |
| `metrics-overview` | 0.3657 | 0.3657 | 0.2714 | service, snapshot, incident | incident, update |
| `metrics-root-cause-diagnoser` | 0.2666 | 0.2666 | 0.3094 | service, incident | incident |

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise this news article in a straightforward neutral recap
- Positive-fit instruction after negation cleanup: Summarise this news article in a straightforward neutral recap

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-summariser` | 0.5278 | 0.5278 | 0.3718 | summary, news, article, straightforward, recap | news |
| `news-briefing-writer` | 0.4150 | 0.4150 | 0.5118 | summary, news, article, recap | summary, news, article |
| `source-grounding-extractor` | 0.3274 | 0.3274 | 0.3547 | summary, news, article, recap | summary |

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn this article into a short decision memo with clear sections for the key event, current state of play, significance now, affected parties, and follow-up signals. The output should support quick situation awareness, not just summarize the article chronologically
- Positive-fit instruction after negation cleanup: Turn this article into a short decision memo with clear sections for the key event, current state of play, significance now, affected parties, and follow-up signals. The output should support quick situation awareness,

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-briefing-writer` | 0.4603 | 0.4603 | 0.3692 | turn, article, short, decision, section, key, current, state | article, summary |
| `news-summariser` | 0.3767 | 0.3767 | 0.6242 | article, event, signal, output, support | decision, memo, current, state, play, significance, now, affect |
| `tech-news-trend-extractor` | 0.3145 | 0.3145 | 0.3317 | article, clear, significance, now, signal, output, support | summary |

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From this article, identify the source-backed claims and facts, including important product details, named companies or people, and any figures or stated plans
- Positive-fit instruction after negation cleanup: From this article, identify the source-backed claims and facts, including important product details, named companies or people, and any figures or stated plans

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `source-grounding-extractor` | 0.3362 | 0.3362 | 0.2452 | article, identify, claim, fact, nam, figure, plan | - |
| `news-summariser` | 0.2256 | 0.2256 | 0.2381 | article, identify, fact, important, detail | claim |
| `news-briefing-writer` | 0.1211 | 0.1211 | 0.3842 | article, identify, fact, important, detail | article, claim, fact |

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Extract the recurring themes across these three tech news snippets, grouping repeated ideas without forecasting market direction. Snippet 1
- Positive-fit instruction after negation cleanup: Extract the recurring themes across these three tech news snippets, grouping repeated ideas . Snippet 1

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `news-theme-extractor` | 0.6971 | 0.6971 | 0.3752 | snippet, extract, recurr, theme, acros, news, group, repeat | extract |
| `tech-news-trend-extractor` | 0.5681 | 0.5681 | 0.5788 | snippet, theme, acros, tech, news, repeat | extract, theme |
| `news-briefing-writer` | 0.4541 | 0.4541 | 0.5718 | snippet, extract, theme, acros, news | extract, theme, acros, news |

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Identify which patterns across these three tech news snippets look like actionable tech trend signals right now, why they matter strategically, and what evidence would confirm or weaken the trend. Snippet 1
- Positive-fit instruction after negation cleanup: Identify which patterns across these three tech news snippets look like actionable tech trend signals right now, why they matter strategically, and what evidence would confirm or weaken the trend. Snippet 1

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `tech-news-trend-extractor` | 0.6801 | 0.6801 | 0.4403 | tech, snippet, trend, identify, acros, news, signal, now | trend |
| `news-theme-extractor` | 0.4269 | 0.4269 | 0.3259 | snippet, trend, identify, pattern, acros, news, signal, they | trend, strategically |
| `news-briefing-writer` | 0.4216 | 0.4216 | 0.4514 | snippet, trend, identify, acros, news, signal, now, why | trend, acros, news |

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Family: `observability_reliability`
- Gold skill: `prometheus-alert-rule-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Produce PromQL alerting expressions for checkout latency and error-budget burn using metrics.md. Include windows, labels, severity, and verification queries; do not build a dashboard.
- Positive-fit instruction after negation cleanup: Produce PromQL alerting expressions for checkout latency and error-budget burn using metrics.md. Include windows, labels, severity, and verification queries; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `prometheus-alert-rule-writer` | 0.6222 | 0.6222 | 0.2911 | alert, expression, metric, window, label, severity, verification | build, dashboard |
| `slo-breach-checker` | 0.4599 | 0.4599 | 0.2755 | metric, window | - |
| `public-swebench-prometheus-configuration` | 0.4110 | 0.4110 | 0.0508 | alert, metric | - |
| `distributed-trace-investigator` | 0.3614 | 0.3614 | 0.4373 | latency | alert, build, dashboard |
| `grafana-dashboard-builder` | 0.2485 | 0.2485 | 0.3652 | metric, querie | alert |

### `observability_reliability_p2_grafana_dashboard_builder`

- Family: `observability_reliability`
- Gold skill: `grafana-dashboard-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design a Grafana dashboard for checkout service health with panels, variables, queries, thresholds, and operator layout. This is not an alert-rule task.
- Positive-fit instruction after negation cleanup: Design a Grafana dashboard for checkout service health with panels, variables, queries, thresholds, and operator layout. This is .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `grafana-dashboard-builder` | 0.8023 | 0.8023 | 0.3382 | design, grafana, dashboard, service, panel, variable, querie, threshold | - |
| `public-swebench-grafana-dashboards` | 0.5567 | 0.5567 | 0.1303 | grafana, dashboard | - |
| `metrics-overview` | 0.4246 | 0.4246 | 0.2033 | dashboard, service, health, threshold | - |
| `prometheus-alert-rule-writer` | 0.2977 | 0.2977 | 0.5720 | threshold | grafana, dashboard |
| `public-swebench-python-observability` | 0.1388 | 0.1388 | 0.1303 | - | - |

### `observability_reliability_p3_distributed_trace_investigator`

- Family: `observability_reliability`
- Gold skill: `distributed-trace-investigator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use checkout_trace.json to find where checkout latency is introduced across services. I need trace-based diagnosis, not a dashboard.
- Positive-fit instruction after negation cleanup: Use checkout_trace.json to find where checkout latency is introduced across services. I need trace-based diagnosis, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `distributed-trace-investigator` | 0.6105 | 0.6105 | 0.2966 | latency, acros, service, diagnosi | dashboard |
| `public-swebench-distributed-tracing` | 0.4601 | 0.4601 | -0.0055 | json, latency, acros, service | - |
| `prometheus-alert-rule-writer` | 0.3418 | 0.3418 | 0.2319 | - | dashboard |
| `metrics-root-cause-diagnoser` | 0.2799 | 0.2799 | 0.2022 | latency, acros, service, diagnosi | - |
| `public-swebench-python-observability` | 0.2536 | 0.2536 | -0.0055 | json | - |

### `observability_reliability_p4_slo_breach_narrative_writer`

- Family: `observability_reliability`
- Gold skill: `slo-breach-narrative-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Using incident_notes.md, write an SLO breach narrative with timeline, user impact, mitigation, and follow-up actions.
- Positive-fit instruction after negation cleanup: Using incident_notes.md, write an SLO breach narrative with timeline, user impact, mitigation, and follow-up actions.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `slo-breach-narrative-writer` | 0.8253 | 0.8253 | 0.3969 | write, slo, breach, timeline, user, impact, mitigation, follow-up | - |
| `incident-summary-writer` | 0.7159 | 0.7159 | 0.4170 | slo, timeline, user, impact, mitigation, action | slo |
| `slo-breach-checker` | 0.6025 | 0.6025 | 0.3807 | slo, breach, user | - |
| `prometheus-alert-rule-writer` | 0.3673 | 0.3673 | 0.3886 | write, slo, user | narrative |
| `grafana-dashboard-builder` | 0.1487 | 0.1487 | 0.5553 | user | narrative |

### `observability_reliability_p5_resilience_pattern_reviewer`

- Family: `observability_reliability`
- Gold skill: `resilience-pattern-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review payment_client.py for retry, timeout, backoff, fallback, and cascading-failure risks.
- Positive-fit instruction after negation cleanup: Review payment_client.py for retry, timeout, backoff, fallback, and cascading-failure risks.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `resilience-pattern-reviewer` | 0.4858 | 0.4858 | 0.0858 | review, timeout, backoff, fallback, cascading-failure, risk | - |
| `public-swebench-python-resilience` | 0.3926 | 0.3926 | 0.0796 | retry, timeout, backoff | - |
| `dependency-risk-auditor` | 0.3210 | 0.3210 | 0.2385 | review, risk | review, risk |
| `prometheus-alert-rule-writer` | 0.2353 | 0.2353 | 0.1446 | risk | - |
| `grafana-dashboard-builder` | 0.1043 | 0.1043 | 0.2029 | - | - |

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Family: `observability_reliability`
- Gold skill: `service-mesh-traffic-debugger`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Debug the service-mesh routing notes in mesh_config.yaml, focusing on traffic split, mTLS, retries, and destination rules.
- Positive-fit instruction after negation cleanup: Debug the service-mesh routing notes in mesh_config.yaml, focusing on traffic split, mTLS, retries, and destination rules.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `service-mesh-traffic-debugger` | 0.7661 | 0.7661 | 0.2225 | debug, rout, traffic, split, mtls, retrie, destination, rule | retrie |
| `public-swebench-service-mesh-observability` | 0.4253 | 0.4253 | 0.0392 | debug | - |
| `public-swebench-istio-traffic-management` | 0.3688 | 0.3688 | 0.0392 | rout, traffic | - |
| `public-swebench-linkerd-patterns` | 0.3385 | 0.3385 | 0.0392 | traffic | - |
| `prometheus-alert-rule-writer` | 0.2596 | 0.2596 | 0.1269 | rout, rule | - |

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please inspect grant_application_packet.pdf as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. Do not just extract the fields.
- Positive-fit instruction after negation cleanup: Please inspect grant_application_packet.pdf as a rendered PDF. I need page-by-page layout issues: cropped tables, broken headers, missing signature areas, and anything that would make the form hard to read. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-layout-reviewer` | 0.5759 | 0.5759 | 0.3877 | pdf, inspect, render, layout, issue, cropp, table, header | table, extract, field |
| `public-pdf` | 0.4240 | 0.4240 | 0.0338 | pdf, render, layout, table, anyth, form, read | - |
| `public-office-pdf-extraction` | 0.4212 | 0.4212 | 0.0338 | pdf, render, layout, table | - |
| `pdf-ocr-extractor` | 0.3779 | 0.3779 | 0.4871 | pdf, area | pdf, render, layout |
| `office-to-markdown-converter` | 0.3244 | 0.3244 | 0.3774 | layout, table | pdf, render |

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please recover the text from scanned_receipts_packet.pdf. It looks like image scans, so keep page numbers and mark uncertain OCR text instead of pretending every amount is reliable.
- Positive-fit instruction after negation cleanup: Please recover the text from scanned_receipts_packet.pdf. It looks like image scans, so keep page numbers and mark uncertain OCR text .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-ocr-extractor` | 0.6048 | 0.6048 | 0.4548 | text, recover, pdf, image, keep, page, number, mark | pdf, ocr |
| `pdf-layout-reviewer` | 0.3586 | 0.3586 | 0.5125 | pdf, page | page, ocr |
| `document-field-extractor` | 0.3016 | 0.3016 | 0.1497 | scan, keep | - |
| `office-to-markdown-converter` | 0.2892 | 0.2892 | 0.3718 | text, keep, page, mark, uncertain | pdf, page |

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review vendor_agreement_draft.docx as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.
- Positive-fit instruction after negation cleanup: Please review vendor_agreement_draft.docx as a Word document and prepare redline-style edits with short reviewer comments. Preserve sections and explain any substantive change.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `docx-redline-editor` | 0.7222 | 0.7222 | 0.4291 | review, word, document, prepare, redline-style, edit, reviewer, comment | document |
| `public-docx` | 0.5472 | 0.5472 | 0.1114 | docx, word, document, edit, short, comment, preserve, section | - |
| `public-office-docx-manipulation` | 0.5108 | 0.5108 | 0.1114 | docx, word, document, edit, comment, change | - |
| `document-rewriter` | 0.4835 | 0.4835 | 0.3357 | word, document, edit, preserve, substantive | substantive |
| `office-to-markdown-converter` | 0.4020 | 0.4020 | 0.4177 | review, document, preserve, section | word, document, change |

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Please check pricing_model.xlsx for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.
- Positive-fit instruction after negation cleanup: Please check pricing_model.xlsx for calculation and assumption risks. I care about wrong cell links, mismatched copied ranges, embedded constants, and whether the summary tab traces back correctly.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `public-office-xlsx-manipulation` | 0.5167 | 0.5167 | 0.0162 | xlsx, link, summary | - |
| `spreadsheet-formula-auditor` | 0.4839 | 0.4839 | 0.3395 | check, calculation, assumption, risk, cell, link, range, whether | summary |
| `public-xlsx` | 0.4731 | 0.4731 | 0.0162 | check, xlsx, calculation, assumption, wrong, cell, link, range | - |
| `data-analysis-with-validation` | 0.3147 | 0.3147 | 0.1451 | check, assumption, whether, summary | - |
| `office-to-markdown-converter` | 0.1919 | 0.1919 | 0.3148 | embedd, summary | check |

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please review thesis_proposal_deck.pptx for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.
- Positive-fit instruction after negation cleanup: Please review thesis_proposal_deck.pptx for presentation readiness. I need slide-level feedback on visual hierarchy, text overflow, alignment, theme consistency, and speaker-note fit.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `slide-deck-visual-auditor` | 0.7504 | 0.7504 | 0.4209 | review, presentation, readines, slide-level, feedback, visual, hierarchy, text | presentation |
| `public-office-ppt-visual` | 0.6367 | 0.6367 | 0.0531 | presentation, visual, text, theme | - |
| `public-pptx` | 0.4530 | 0.4530 | 0.0952 | pptx, presentation, visual, text, theme | - |
| `pdf-layout-reviewer` | 0.3937 | 0.3937 | 0.1739 | review, visual, alignment | - |
| `office-to-markdown-converter` | 0.2550 | 0.2550 | 0.2554 | review, visual, hierarchy, text | - |

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please convert project_brief.docx into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but do not create tracked changes or a layout audit.
- Positive-fit instruction after negation cleanup: Please convert project_brief.docx into clean Markdown for a repository. Preserve headings, tables, labels, and source traceability, but .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `office-to-markdown-converter` | 0.5532 | 0.5532 | 0.3745 | convert, clean, markdown, preserve, heading, table, label, traceability | track, change, audit |
| `docx-redline-editor` | 0.4744 | 0.4744 | 0.4591 | preserve, heading | convert, markdown, layout, audit |
| `document-converter` | 0.4545 | 0.4545 | 0.4074 | convert, markdown, preserve, label | layout |
| `pdf-layout-reviewer` | 0.2595 | 0.2595 | 0.3334 | table | convert, markdown, table |

### `office_business_automation_p1_xlsx_formula_model_builder`

- Family: `office_business_automation`
- Gold skill: `xlsx-formula-model-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build a spreadsheet formula model for subscription revenue using revenue_assumptions.md. I need formulas and validation checks, not Airtable automation.
- Positive-fit instruction after negation cleanup: Build a spreadsheet formula model for subscription revenue using revenue_assumptions.md. I need formulas and validation checks, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `xlsx-formula-model-builder` | 0.6169 | 0.6169 | 0.2764 | formula, check, build, spreadsheet, model | airtable |
| `public-office-xlsx-manipulation` | 0.3204 | 0.3204 | 0.0452 | formula, spreadsheet | - |
| `airtable-workflow-automator` | 0.3103 | 0.3103 | 0.4232 | formula, spreadsheet | formula, build |
| `public-swebench-xlsx` | 0.2584 | 0.2584 | 0.0452 | formula, check, build, spreadsheet, model, revenue | - |
| `public-office-data-analysis` | 0.2272 | 0.2272 | 0.0452 | formula, build, spreadsheet, model, revenue | - |

### `office_business_automation_p2_airtable_workflow_automator`

- Family: `office_business_automation`
- Gold skill: `airtable-workflow-automator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design an Airtable automation for inbound partner requests: fields, views, trigger conditions, Slack notification, and testing steps.
- Positive-fit instruction after negation cleanup: Design an Airtable automation for inbound partner requests: fields, views, trigger conditions, Slack notification, and testing steps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `airtable-workflow-automator` | 0.6711 | 0.6711 | 0.2870 | design, airtable, automation, field, view, trigger, condition, test | - |
| `public-office-airtable-automation` | 0.5331 | 0.5331 | 0.0653 | airtable, automation, request, view, trigger | - |
| `public-office-crm-automation` | 0.3155 | 0.3155 | 0.0653 | automation, request | - |
| `notion-research-database-builder` | 0.2778 | 0.2778 | 0.6009 | design, field, view | airtable, automation |
| `xlsx-formula-model-builder` | 0.2416 | 0.2416 | 0.4938 | design | airtable |

### `office_business_automation_p3_notion_research_database_builder`

- Family: `office_business_automation`
- Gold skill: `notion-research-database-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a Notion research database structure for thesis papers with properties, relations, review status, tags, and capture templates.
- Positive-fit instruction after negation cleanup: Create a Notion research database structure for thesis papers with properties, relations, review status, tags, and capture templates.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `notion-research-database-builder` | 0.7547 | 0.7547 | 0.2996 | create, notion, research, database, structure, propertie, relation, review | paper |
| `public-openai-notion-research-documentation` | 0.4523 | 0.4523 | -0.0513 | create, notion, research, database, statu, template | - |
| `public-office-notion-automation` | 0.3678 | 0.3678 | -0.0513 | notion, database, propertie, statu, template | - |
| `airtable-workflow-automator` | 0.3020 | 0.3020 | 0.5487 | - | notion, research, database |
| `xlsx-formula-model-builder` | 0.2494 | 0.2494 | 0.2535 | structure | - |

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Family: `office_business_automation`
- Gold skill: `calendar-scheduling-optimizer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use these availability notes to propose two meeting slots with buffers and conflict tradeoffs. This is scheduling, not meeting-note extraction.
- Positive-fit instruction after negation cleanup: Use these availability notes to propose two meeting slots with buffers and conflict tradeoffs. This is scheduling, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `calendar-scheduling-optimizer` | 0.5875 | 0.5875 | 0.4207 | availability, note, propose, meet, slot, buffer, conflict, tradeoff | note, meet, extract |
| `meeting-agenda-builder` | 0.4126 | 0.4126 | 0.5851 | note, meet | note, meet, extract |
| `public-office-calendar-automation` | 0.3825 | 0.3825 | 0.0426 | meet, schedul | - |
| `airtable-workflow-automator` | 0.1978 | 0.1978 | 0.3164 | - | schedul |
| `xlsx-formula-model-builder` | 0.1179 | 0.1179 | 0.3721 | - | meet, extract |

### `office_business_automation_p5_meeting_notes_action_extractor`

- Family: `office_business_automation`
- Gold skill: `meeting-notes-action-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From meeting_notes.md, extract decisions, actions, owners, due dates, and open questions. Do not draft a calendar schedule.
- Positive-fit instruction after negation cleanup: From meeting_notes.md, extract decisions, actions, owners, due dates, and open questions. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-notes-action-extractor` | 0.7857 | 0.7857 | 0.5379 | extract, decision, action, owner, due, date, open, question | - |
| `meeting-followup-extractor` | 0.6424 | 0.6424 | 0.5940 | extract, action, owner, due, date, open, question | extract |
| `public-office-meeting-notes` | 0.5602 | 0.5602 | 0.0748 | extract, decision, action | - |
| `xlsx-formula-model-builder` | 0.2868 | 0.2868 | 0.4574 | - | extract, action |
| `airtable-workflow-automator` | 0.2661 | 0.2661 | 0.3786 | action | - |

### `office_business_automation_p6_email_classification_router`

- Family: `office_business_automation`
- Gold skill: `email-classification-router`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Classify the emails in inbox_sample.md by category, priority, routing destination, and escalation risk. Do not write replies.
- Positive-fit instruction after negation cleanup: Classify the emails in inbox_sample.md by category, priority, routing destination, and escalation risk. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `email-classification-router` | 0.7729 | 0.7729 | 0.4198 | classify, email, category, priority, rout, destination, escalation, risk | email |
| `public-office-email-classifier` | 0.5560 | 0.5560 | 0.0806 | classify, email, category, priority | - |
| `public-office-suspicious-email` | 0.5258 | 0.5258 | 0.0806 | email, risk | - |
| `public-office-gmail-workflows` | 0.2993 | 0.2993 | 0.0806 | email, priority | - |
| `xlsx-formula-model-builder` | 0.1414 | 0.1414 | 0.4945 | - | classify, email |

### `pdf_document_operations_p1_pdf_question_answerer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-question-answerer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Please answer this from sample_packet.pdf: what evidence does the policy give for reimbursing delayed travel meals? Cite the page or section evidence rather than converting the whole document.
- Positive-fit instruction after negation cleanup: Please answer this from sample_packet.pdf: what evidence does the policy give for reimbursing delayed travel meals? Cite the page or section evidence .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-question-answerer` | 0.1727 | 0.1727 | 0.1176 | evidence, answer, pdf, page, section | pdf, convert |
| `pdf-redaction-reviewer` | 0.1373 | 0.1373 | -0.0043 | evidence, pdf, page, section | pdf, document |
| `pdf-layout-table-extractor` | 0.0758 | 0.0758 | 0.1072 | evidence, pdf, page | answer, pdf |
| `pdf-form-filler` | 0.0704 | 0.0704 | 0.0962 | pdf | answer, pdf, convert |
| `pdf-ocr-cleaner` | 0.0110 | 0.0110 | 0.1255 | pdf, page | - |

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Family: `pdf_document_operations`
- Gold skill: `pdf-layout-table-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From vendor_statement.pdf, extract the invoice table into structured rows with invoice id, date, subtotal, tax, total, and page/row anchors. Do not answer it as a general PDF question.
- Positive-fit instruction after negation cleanup: From vendor_statement.pdf, extract the invoice table into structured rows with invoice id, date, subtotal, tax, total, and page/row anchors. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-layout-table-extractor` | 0.6041 | 0.6041 | 0.3159 | invoice, pdf, extract, table, structur, rows, page, row | pdf, answer, question |
| `pdf-question-answerer` | 0.3331 | 0.3331 | 0.5964 | pdf, extract, page, anchor | pdf, extract, table |
| `pdf-form-filler` | 0.3133 | 0.3133 | 0.6335 | pdf | pdf, invoice, extract, answer, question |
| `pdf-ocr-cleaner` | 0.2906 | 0.2906 | 0.2421 | pdf, page, anchor | extract, table |
| `pdf-redaction-reviewer` | 0.2374 | 0.2374 | 0.4775 | pdf, extract, page, anchor | pdf, extract |

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Family: `pdf_document_operations`
- Gold skill: `pdf-ocr-cleaner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The file scanned_receipts.pdf is mostly images. Recover the text page by page and mark uncertain OCR regions; do not treat it as a normal digital table extraction.
- Positive-fit instruction after negation cleanup: The file scanned_receipts.pdf is mostly images. Recover the text page by page and mark uncertain OCR regions; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-ocr-cleaner` | 0.7347 | 0.7347 | 0.3787 | page, pdf, image, recover, text, mark, uncertain, ocr | table, extract |
| `pdf-layout-table-extractor` | 0.4845 | 0.4845 | 0.5364 | page, pdf, mark, uncertain | pdf, ocr |
| `pdf-question-answerer` | 0.3801 | 0.3801 | 0.5928 | page, pdf, text | pdf, table, extract |
| `pdf-redaction-reviewer` | 0.3775 | 0.3775 | 0.4973 | page, pdf, text | file, pdf, extract |
| `pdf-form-filler` | 0.3736 | 0.3736 | 0.4621 | pdf | pdf, extract |

### `pdf_document_operations_p4_pdf_form_filler`

- Family: `pdf_document_operations`
- Gold skill: `pdf-form-filler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use reimbursement_form.pdf and the supplied employee details to prepare a field-entry checklist for the reimbursement packet. Identify required blanks that still need values; do not summarize the packet.
- Positive-fit instruction after negation cleanup: Use reimbursement_form.pdf and the supplied employee details to prepare a field-entry checklist for the reimbursement packet. Identify required blanks that still need values; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-form-filler` | 0.5876 | 0.5876 | 0.4189 | pdf, suppli, prepare, checklist, requir, value | pdf |
| `public-office-pdf-form-filler` | 0.5241 | 0.5241 | -0.0598 | pdf, requir, value | - |
| `document-field-extractor` | 0.3909 | 0.3909 | 0.1368 | identify, value | summary |
| `pdf-layout-table-extractor` | 0.3893 | 0.3893 | 0.2729 | pdf, value | pdf |
| `pdf-question-answerer` | 0.2844 | 0.2844 | 0.4207 | pdf, identify | pdf |

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-redaction-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before we send client_contract.pdf to an external vendor, identify page-specific redaction targets such as IDs, addresses, pricing, and confidential clauses.
- Positive-fit instruction after negation cleanup: Before we send client_contract.pdf to an external vendor, identify page-specific redaction targets such as IDs, addresses, pricing, and confidential clauses.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-redaction-reviewer` | 0.5974 | 0.5974 | 0.3005 | pdf, identify, redaction, target, ids, addresse, confidential, clause | pdf |
| `public-office-contract-review` | 0.4397 | 0.4397 | 0.4188 | pdf, external, addresse, clause | pdf, identify |
| `pdf-question-answerer` | 0.4297 | 0.4297 | 0.3465 | pdf, identify | pdf |
| `public-openai-pdf` | 0.4058 | 0.4058 | 0.0156 | pdf, external, such | - |
| `privacy-risk-reviewer` | 0.2568 | 0.2568 | 0.2861 | identify | external |

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Family: `pdf_document_operations`
- Gold skill: `pdf-to-docx-converter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Convert training_manual.pdf into an editable DOCX-style structure with headings and tables preserved. Do not just answer questions from it.
- Positive-fit instruction after negation cleanup: Convert training_manual.pdf into an editable DOCX-style structure with headings and tables preserved. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `pdf-to-docx-converter` | 0.7022 | 0.7022 | 0.3833 | convert, pdf, editable, docx-style, structure, heading, table, preserv | pdf, answer, question |
| `pdf-layout-table-extractor` | 0.5598 | 0.5598 | 0.3956 | pdf, table, preserv | pdf, answer, question |
| `pdf-form-filler` | 0.3639 | 0.3639 | 0.5162 | pdf | convert, pdf, answer, question |
| `pdf-ocr-cleaner` | 0.3589 | 0.3589 | 0.2758 | pdf, preserv | table |
| `pdf-question-answerer` | 0.3070 | 0.3070 | 0.6428 | pdf | convert, pdf, table |

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I have a short group project meeting tomorrow for a class presentation on AI study assistants. Please turn these topics into an agenda for that upcoming meeting: who will cover the demo, who will finish the slides, what risks could delay us before Friday, and what we need to prepare before the next check-in. The output should guide the meeting discussion, not schedule my whole week or only extract tasks.
- Positive-fit instruction after negation cleanup: I have a short group project meeting tomorrow for a class presentation on AI study assistants. Please turn these topics into an agenda for that upcoming meeting: who will cover the demo, who will finish the slides, what risks could delay us before Friday, and what we need to prepare before the next check-in. The output should guide the meeting discussion, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-agenda-builder` | 0.6533 | 0.6533 | 0.6255 | meet, group, turn, topic, agenda, upcom, output, guide | meet, discussion, extract, task |
| `weekly-planner` | 0.4403 | 0.4403 | 0.5427 | meet, group, risk, output | meet, agenda, only, extract, task |
| `task-extractor` | 0.4373 | 0.4373 | 0.6619 | meet, output | meet, agenda, schedule, extract |

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise these meeting notes into a clean meeting recap
- Positive-fit instruction after negation cleanup: Summarise these meeting notes into a clean meeting recap

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-summary-writer` | 0.6977 | 0.6977 | 0.6518 | meet, summary, note, recap | meet, note |
| `meeting-followup-extractor` | 0.4801 | 0.4801 | 0.6268 | meet, summary, note | meet, summary, note |
| `task-extractor` | 0.4731 | 0.4731 | 0.4815 | meet, summary, note | meet, summary |

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Gold rank among listed candidates: 3
- Instruction used for scoring: I need something clean from these meeting notes so I can quickly see what needs to happen next and what still needs attention
- Positive-fit instruction after negation cleanup: I need something clean from these meeting notes so I can quickly see what needs to happen next and what still needs attention

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `meeting-summary-writer` | 0.6229 | 0.6229 | 0.6083 | meet, note, happen | meet, note |
| `task-extractor` | 0.5398 | 0.5398 | 0.4393 | meet, note | meet |
| `meeting-followup-extractor` | 0.5147 | 0.5147 | 0.5903 | meet, note, happen, next | meet, note |

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn these rough notes into a plain action-item list without scheduling the week and without treating them as completed meeting notes
- Positive-fit instruction after negation cleanup: Turn these rough notes into a plain action-item list

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `task-extractor` | 0.5060 | 0.5060 | 0.4800 | rough, note, list | complet, meet |
| `meeting-followup-extractor` | 0.2700 | 0.2700 | 0.5740 | note, list | note, rough, meet |
| `weekly-planner` | 0.1969 | 0.1969 | 0.7103 | note, list | note, rough, complet, meet |

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Help me make a realistic week-level plan with sequencing and time buffers. I need to finish the planning skill family, revise prompts for the reply cluster, prepare for a Tuesday project meeting about collaborating on a prototype and brainstorming test cases for a multi-agent system, review two papers, send my supervisor a grounded summary by Thursday, and leave time for benchmark testing. I also have classes on Tuesday and Thursday afternoon. Do not just extract a raw task list or prepare a single meeting agenda.
- Positive-fit instruction after negation cleanup: Help me make a realistic week-level plan with sequencing and time buffers. I need to finish the planning skill family, revise prompts for the reply cluster, prepare for a Tuesday project meeting about collaborating on a prototype and brainstorming test cases for a multi-agent system, review two papers, send my supervisor a grounded summary by Thursday, and leave time for benchmark testing. I also have classes on Tuesday and Thursday afternoon. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `weekly-planner` | 0.6978 | 0.6978 | 0.3683 | plan, time, realistic, week-level, sequenc, buffer, meet | meet, summary, extract, task, agenda |
| `meeting-agenda-builder` | 0.4904 | 0.4904 | 0.4909 | plan, time, week-level, prompt, meet, summary | plan, meet, summary, extract, task |
| `task-extractor` | 0.3988 | 0.3988 | 0.5863 | plan, week-level, meet, summary | plan, meet, week-level, summary, extract, agenda |

### `psc_browser_quality_p01_1_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The checkout Apply Coupon button stops responding after the first click. Reproduce the path and use browser evidence to explain whether it is DOM state, network, or JavaScript logic.
- Positive-fit instruction after negation cleanup: The checkout Apply Coupon button stops responding after the first click. Reproduce the path and use browser evidence to explain whether it is DOM state, network, or JavaScript logic.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-devtools-runtime-diagnoser` | 0.2357 | 0.2357 | -0.0216 | reproduce, browser, evidence, dom, state, network, javascript | - |
| `psc-playwright-regression-suite` | 0.1067 | 0.1067 | -0.1013 | path, browser, evidence | - |
| `psc-accessibility-interaction-auditor` | 0.1062 | 0.1062 | -0.0331 | path, browser, evidence, state | - |
| `psc-visual-screenshot-reviewer` | 0.0490 | 0.0490 | 0.1685 | browser, evidence, state | browser, dom, network |

### `psc_browser_quality_p01_2_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use Chrome DevTools-style evidence for the broken checkout interaction: console errors, network failures, DOM state, and screenshots. Do not only write Playwright assertions.
- Positive-fit instruction after negation cleanup: Use Chrome DevTools-style evidence for the broken checkout interaction: console errors, network failures, DOM state, and screenshots. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-devtools-runtime-diagnoser` | 0.5382 | 0.5382 | 0.2148 | evidence, broken, interaction, console, error, network, failure, dom | screenshot |
| `psc-accessibility-interaction-auditor` | 0.3926 | 0.3926 | 0.1244 | evidence, interaction, error, state, screenshot | screenshot, only |
| `psc-playwright-regression-suite` | 0.2991 | 0.2991 | 0.2963 | evidence, interaction, failure, screenshot | - |
| `psc-visual-screenshot-reviewer` | 0.2907 | 0.2907 | 0.4338 | evidence, interaction, state, screenshot | network, dom, screenshot |

### `psc_browser_quality_p02_1_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Build a repeatable browser regression check for the checkout form: navigate, fill fields, apply the coupon, assert the discount message, and capture failure evidence.
- Positive-fit instruction after negation cleanup: Build a repeatable browser regression check for the checkout form: navigate, fill fields, apply the coupon, assert the discount message, and capture failure evidence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-devtools-runtime-diagnoser` | 0.3257 | 0.3257 | 0.2590 | browser, regression, check, failure, evidence | regression, capture |
| `psc-playwright-regression-suite` | 0.2571 | 0.2571 | 0.1280 | browser, regression, check, form, capture, failure, evidence | - |
| `psc-accessibility-interaction-auditor` | 0.2425 | 0.2425 | 0.1606 | browser, regression, check, evidence | - |
| `psc-visual-screenshot-reviewer` | 0.2326 | 0.2326 | 0.2106 | browser, regression, check, evidence | browser |

### `psc_browser_quality_p02_2_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write a Playwright test for the checkout coupon flow with assertions and screenshots. I need reusable regression coverage, not just a manual DevTools diagnosis.
- Positive-fit instruction after negation cleanup: Write a Playwright test for the checkout coupon flow with assertions and screenshots. I need reusable regression coverage, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-playwright-regression-suite` | 0.5249 | 0.5249 | 0.3066 | playwright, test, flow, assertion, screenshot, regression | manual, devtool |
| `psc-visual-screenshot-reviewer` | 0.3272 | 0.3272 | 0.2874 | screenshot, regression | test, screenshot, diagnosi |
| `psc-devtools-runtime-diagnoser` | 0.3229 | 0.3229 | 0.3574 | flow, screenshot, regression | screenshot, regression, just |
| `psc-accessibility-interaction-auditor` | 0.2139 | 0.2139 | 0.2945 | flow, screenshot, regression | test, screenshot |

### `psc_browser_quality_p03_1_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compare the old and new pricing-page screenshots and call out visible layout regressions, spacing changes, clipped content, and mobile text overflow.
- Positive-fit instruction after negation cleanup: Compare the old and new pricing-page screenshots and call out visible layout regressions, spacing changes, clipped content, and mobile text overflow.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-visual-screenshot-reviewer` | 0.5130 | 0.5130 | 0.1976 | compare, screenshot, layout, regression, spac, clipp, text, overflow | screenshot |
| `psc-accessibility-interaction-auditor` | 0.3423 | 0.3423 | 0.4339 | screenshot, regression | compare, screenshot |
| `psc-playwright-regression-suite` | 0.2698 | 0.2698 | 0.2124 | screenshot, regression | - |
| `psc-devtools-runtime-diagnoser` | 0.2535 | 0.2535 | 0.4304 | screenshot, regression | screenshot, regression |

### `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Do a visual regression review from screenshot pairs across desktop and mobile. I need layout differences and severity, not browser interaction debugging.
- Positive-fit instruction after negation cleanup: Do a visual regression review from screenshot pairs across desktop and mobile. I need layout differences and severity, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-visual-screenshot-reviewer` | 0.6534 | 0.6534 | 0.3553 | visual, regression, screenshot, layout, difference, severity | screenshot, browser |
| `psc-accessibility-interaction-auditor` | 0.4005 | 0.4005 | 0.5691 | visual, regression, screenshot, severity | screenshot |
| `psc-playwright-regression-suite` | 0.3452 | 0.3452 | 0.5030 | regression, screenshot | visual, review, debug |
| `psc-devtools-runtime-diagnoser` | 0.3022 | 0.3022 | 0.6446 | regression, screenshot | regression, review, screenshot |

### `psc_browser_quality_p04_1_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit the account settings modal for keyboard navigation, focus trapping, labels, contrast, and whether form errors are announced clearly.
- Positive-fit instruction after negation cleanup: Audit the account settings modal for keyboard navigation, focus trapping, labels, contrast, and whether form errors are announced clearly.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-accessibility-interaction-auditor` | 0.5843 | 0.5843 | 0.3003 | audit, keyboard, focu, label, contrast, error | - |
| `psc-visual-screenshot-reviewer` | 0.3946 | 0.3946 | 0.2600 | contrast | - |
| `psc-devtools-runtime-diagnoser` | 0.3683 | 0.3683 | 0.3912 | error | - |
| `psc-playwright-regression-suite` | 0.2100 | 0.2100 | 0.4404 | navigation, form | audit |

### `psc_browser_quality_p04_2_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this web form specifically for accessibility interaction quality: keyboard path, accessible names, ARIA state, focus order, and screen-reader error feedback.
- Positive-fit instruction after negation cleanup: Review this web form specifically for accessibility interaction quality: keyboard path, accessible names, ARIA state, focus order, and screen-reader error feedback.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-accessibility-interaction-auditor` | 0.7632 | 0.7632 | 0.3460 | web, accessibility, interaction, quality, keyboard, path, aria, state | - |
| `psc-visual-screenshot-reviewer` | 0.4961 | 0.4961 | 0.3396 | web, accessibility, interaction, quality, state | - |
| `psc-devtools-runtime-diagnoser` | 0.3813 | 0.3813 | 0.5310 | web, accessibility, interaction, quality, state, error | review, accessibility |
| `psc-playwright-regression-suite` | 0.3155 | 0.3155 | 0.4135 | web, form, accessibility, interaction, quality, path | review |

### `psc_data_analysis_intent_p01_1_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before we make a decision from this weekly channel CSV, check whether the data is trustworthy: missing values, duplicate rows, invalid ranges, and schema issues.
- Positive-fit instruction after negation cleanup: Before we make a decision from this weekly channel CSV, check whether the data is trustworthy: missing values, duplicate rows, invalid ranges, and schema issues.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-data-trust-auditor` | 0.4674 | 0.4674 | 0.1493 | decision, csv, check, whether, data, trustworthy, miss, value | - |
| `psc-anomaly-watchlist-builder` | 0.3921 | 0.3921 | 0.2727 | decision, csv, check, data, value | data |
| `psc-decision-ranking-analyst` | 0.2301 | 0.2301 | 0.2994 | decision, csv, data | decision, check, data |
| `psc-executive-metric-narrator` | 0.2087 | 0.2087 | 0.2976 | decision, csv, data | - |

### `psc_data_analysis_intent_p01_2_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit the spreadsheet's data quality and assumptions. I need trustworthiness checks, not a ranking recommendation or executive summary.
- Positive-fit instruction after negation cleanup: Audit the spreadsheet's data quality and assumptions. I need trustworthiness checks, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-data-trust-auditor` | 0.7538 | 0.7538 | 0.4321 | audit, data, quality, assumption, check | rank, executive |
| `psc-anomaly-watchlist-builder` | 0.4504 | 0.4504 | 0.5093 | data, quality, check | audit, data, executive |
| `psc-executive-metric-narrator` | 0.3971 | 0.3971 | 0.4515 | data, quality | audit, rank |
| `psc-decision-ranking-analyst` | 0.3651 | 0.3651 | 0.4616 | data, quality | data, quality, check |

### `psc_data_analysis_intent_p02_1_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Scan the weekly channel metrics for unusual spikes, drops, outliers, or concentrated deviations that deserve follow-up.
- Positive-fit instruction after negation cleanup: Scan the weekly channel metrics for unusual spikes, drops, outliers, or concentrated deviations that deserve follow-up.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-anomaly-watchlist-builder` | 0.5473 | 0.5473 | 0.2078 | metric, unusual, spike, drop, outlier, follow-up | - |
| `psc-data-trust-auditor` | 0.3098 | 0.3098 | 0.1694 | metric | - |
| `psc-executive-metric-narrator` | 0.2662 | 0.2662 | 0.4984 | metric | - |
| `psc-decision-ranking-analyst` | 0.2090 | 0.2090 | 0.3382 | metric | - |

### `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Build an anomaly watchlist from the CSV with evidence windows and priorities. Do not turn it into a broad reporting brief.
- Positive-fit instruction after negation cleanup: Build an anomaly watchlist from the CSV with evidence windows and priorities. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-anomaly-watchlist-builder` | 0.7311 | 0.7311 | 0.2861 | anomaly, watchlist, csv, evidence, window | - |
| `psc-data-trust-auditor` | 0.4884 | 0.4884 | 0.1938 | csv | - |
| `psc-executive-metric-narrator` | 0.3379 | 0.3379 | 0.5409 | csv | anomaly |
| `psc-decision-ranking-analyst` | 0.3045 | 0.3045 | 0.3982 | csv, evidence | anomaly |

### `psc_data_analysis_intent_p03_1_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compare the pilot options and rank which one we should act on first, using cost, impact, risk, confidence, and time-to-value.
- Positive-fit instruction after negation cleanup: Compare the pilot options and rank which one we should act on first, using cost, impact, risk, confidence, and time-to-value.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-decision-ranking-analyst` | 0.4164 | 0.4164 | 0.1892 | compare, option, rank, first, confidence | - |
| `psc-executive-metric-narrator` | 0.3067 | 0.3067 | 0.2298 | rank, risk | option, rank |
| `psc-anomaly-watchlist-builder` | 0.2368 | 0.2368 | 0.1895 | compare, rank, confidence | - |
| `psc-data-trust-auditor` | 0.2164 | 0.2164 | 0.3474 | rank, act | option, rank |

### `psc_data_analysis_intent_p03_2_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the option table to produce a decision ranking with criteria, tradeoffs, and first-choice recommendation. Do not just summarize the dataset.
- Positive-fit instruction after negation cleanup: Use the option table to produce a decision ranking with criteria, tradeoffs, and first-choice recommendation. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-decision-ranking-analyst` | 0.6222 | 0.6222 | 0.2231 | option, table, decision, rank, criteria, tradeoff, recommendation | decision |
| `psc-executive-metric-narrator` | 0.3251 | 0.3251 | 0.2957 | table, decision, rank | option, rank |
| `psc-anomaly-watchlist-builder` | 0.2849 | 0.2849 | 0.1656 | table, decision, rank | - |
| `psc-data-trust-auditor` | 0.2530 | 0.2530 | 0.3293 | decision, rank | option, rank |

### `psc_data_analysis_intent_p04_1_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn the weekly performance table into a leadership-ready brief: headline, key movements, risks, and two recommended next steps.
- Positive-fit instruction after negation cleanup: Turn the weekly performance table into a leadership-ready brief: headline, key movements, risks, and two recommended next steps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-executive-metric-narrator` | 0.5819 | 0.5819 | 0.1169 | turn, table, brief, headline, key, movement, risk, recommend | - |
| `psc-anomaly-watchlist-builder` | 0.4011 | 0.4011 | 0.2761 | table, next | - |
| `psc-decision-ranking-analyst` | 0.3611 | 0.3611 | -0.0146 | table, recommend | - |
| `psc-data-trust-auditor` | 0.2829 | 0.2829 | 0.2964 | - | - |

### `psc_data_analysis_intent_p04_2_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write an executive metric narrative from the spreadsheet. I need business takeaways and actions, not data validation or anomaly hunting.
- Positive-fit instruction after negation cleanup: Write an executive metric narrative from the spreadsheet. I need business takeaways and actions, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-executive-metric-narrator` | 0.7484 | 0.7484 | 0.3209 | executive, metric, narrative, spreadsheet, busines, takeaway, action | anomaly |
| `psc-data-trust-auditor` | 0.4286 | 0.4286 | 0.4944 | metric, spreadsheet, busines | executive |
| `psc-anomaly-watchlist-builder` | 0.3535 | 0.3535 | 0.5925 | metric, spreadsheet, busines | executive, narrative, data |
| `psc-decision-ranking-analyst` | 0.3313 | 0.3313 | 0.2563 | metric, spreadsheet, busines, action | data, check, anomaly |

### `psc_github_maintenance_p01_1_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The build failed after the last push. Read the CI output, identify the first real error, explain the likely cause, and give the smallest rerun sequence.
- Positive-fit instruction after negation cleanup: The build failed after the last push. Read the CI output, identify the first real error, explain the likely cause, and give the smallest rerun sequence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-ci-log-first-failure-reader` | 0.5177 | 0.5177 | 0.2833 | build, fail, read, output, first, error, likely, cause | - |
| `psc-pr-thread-fix-planner` | 0.2437 | 0.2437 | 0.2804 | - | - |
| `psc-release-communication-packager` | 0.1866 | 0.1866 | 0.3130 | - | - |
| `psc-repo-guardrail-hook-installer` | 0.1420 | 0.1420 | 0.2861 | output | - |

### `psc_github_maintenance_p01_2_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Analyze the failed GitHub Actions log for the first meaningful failure and minimal fix path. Do not turn this into a PR review or release note.
- Positive-fit instruction after negation cleanup: Analyze the failed GitHub Actions log for the first meaningful failure and minimal fix path. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-ci-log-first-failure-reader` | 0.6047 | 0.6047 | 0.3768 | fail, github, action, log, first, meaningful, failure, minimal | review |
| `psc-repo-guardrail-hook-installer` | 0.3995 | 0.3995 | 0.2094 | analysi, github, action, failure | analysi, release, note |
| `psc-pr-thread-fix-planner` | 0.3883 | 0.3883 | 0.2238 | github, action | log, review |
| `psc-release-communication-packager` | 0.3499 | 0.3499 | 0.2671 | github | failure, review |

### `psc_github_maintenance_p02_1_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use the review threads on this PR to plan the required fixes, tests, and replies. The comments already exist; I need an action map.
- Positive-fit instruction after negation cleanup: Use the review threads on this PR to plan the required fixes, tests, and replies. The comments already exist; I need an action map.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pr-thread-fix-planner` | 0.6990 | 0.6990 | 0.3773 | review, thread, plan, requir, fixe, test, comment, already | review, comment |
| `psc-release-communication-packager` | 0.4097 | 0.4097 | 0.4267 | review, thread, fixe | review |
| `psc-repo-guardrail-hook-installer` | 0.3995 | 0.3995 | 0.2799 | review, thread, plan, action | - |
| `psc-ci-log-first-failure-reader` | 0.3715 | 0.3715 | 0.4557 | review, thread, plan, test, action, map | review |

### `psc_github_maintenance_p02_2_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Address unresolved GitHub PR review comments by mapping each thread to code/test changes and response text. Do not perform a fresh review from scratch.
- Positive-fit instruction after negation cleanup: Address unresolved GitHub PR review comments by mapping each thread to code/test changes and response text. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pr-thread-fix-planner` | 0.6910 | 0.6910 | 0.4043 | addres, github, review, comment, mapp, each, thread, code | review, comment, code, fresh |
| `psc-release-communication-packager` | 0.4775 | 0.4775 | 0.4537 | github, review, thread, code, change | review, code |
| `psc-repo-guardrail-hook-installer` | 0.4308 | 0.4308 | 0.2231 | github, review, thread, code | - |
| `psc-ci-log-first-failure-reader` | 0.4287 | 0.4287 | 0.5298 | github, review, thread, code, test | review, code, fresh |

### `psc_github_maintenance_p03_1_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Set up repository safeguards so contributors cannot accidentally commit secrets or run destructive git operations without confirmation.
- Positive-fit instruction after negation cleanup: Set up repository safeguards so contributors cannot accidentally commit secrets or run destructive git operations .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-repo-guardrail-hook-installer` | 0.5305 | 0.5305 | 0.2870 | set, repository, secret, git, operation | - |
| `psc-release-communication-packager` | 0.4542 | 0.4542 | 0.2196 | repository, commit | - |
| `psc-pr-thread-fix-planner` | 0.3229 | 0.3229 | 0.1516 | repository | - |
| `psc-ci-log-first-failure-reader` | 0.2679 | 0.2679 | 0.1745 | repository | - |

### `psc_github_maintenance_p03_2_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design git hook guardrails for secret commits, force pushes, reset --hard, branch deletion, and unsafe clean commands, including verification steps.
- Positive-fit instruction after negation cleanup: Design git hook guardrails for secret commits, force pushes, reset --hard, branch deletion, and unsafe clean commands, including verification steps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-repo-guardrail-hook-installer` | 0.7207 | 0.7207 | 0.1993 | git, hook, guardrail, secret, command, verification | - |
| `psc-pr-thread-fix-planner` | 0.4483 | 0.4483 | 0.2131 | hook, verification, step | - |
| `psc-release-communication-packager` | 0.4459 | 0.4459 | 0.2389 | hook, commit, verification | - |
| `psc-ci-log-first-failure-reader` | 0.3768 | 0.3768 | 0.2506 | hook, verification | - |

### `psc_github_maintenance_p04_1_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn the merged PR list into release notes grouped by features, fixes, and breaking changes, with upgrade notes where needed.
- Positive-fit instruction after negation cleanup: Turn the merged PR list into release notes grouped by features, fixes, and breaking changes, with upgrade notes where needed.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-release-communication-packager` | 0.6994 | 0.6994 | 0.1656 | note, turn, merg, list, release, group, feature, fixe | - |
| `psc-pr-thread-fix-planner` | 0.4938 | 0.4938 | 0.2143 | note, release, group, fixe, change | - |
| `psc-repo-guardrail-hook-installer` | 0.3357 | 0.3357 | 0.3189 | note, release | note, release |
| `psc-ci-log-first-failure-reader` | 0.2998 | 0.2998 | 0.3970 | release | - |

### `psc_github_maintenance_p04_2_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare user-facing release communication from completed changes. I need release notes/changelog language, not bug-finding or CI triage.
- Positive-fit instruction after negation cleanup: Prepare user-facing release communication from completed changes. I need release notes/changelog language, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-release-communication-packager` | 0.7239 | 0.7239 | 0.3775 | release, communication, change, note, changelog, language | - |
| `psc-pr-thread-fix-planner` | 0.4894 | 0.4894 | 0.3555 | release, prepare, change, note | - |
| `psc-repo-guardrail-hook-installer` | 0.3953 | 0.3953 | 0.5538 | release, note | release, note |
| `psc-ci-log-first-failure-reader` | 0.3502 | 0.3502 | 0.4506 | release | changelog |

### `psc_huggingface_workflow_p01_1_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use Hugging Face dataset information to inspect the ticket dataset's splits, columns, labels, row examples, and licensing caveats before we model it.
- Positive-fit instruction after negation cleanup: Use Hugging Face dataset information to inspect the ticket dataset's splits, columns, labels, row examples, and licensing caveats before we model it.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-hf-dataset-card-inspector` | 0.6393 | 0.6393 | 0.1814 | hugg, face, dataset, inspect, split, column, label, row | model |
| `psc-sentence-embedding-trainer` | 0.4141 | 0.4141 | 0.1686 | hugg, face, dataset, split, label, model | - |
| `psc-local-model-fit-selector` | 0.3818 | 0.3818 | 0.4383 | hugg, face, dataset, model | dataset |
| `psc-hf-space-deployment-preparer` | 0.3514 | 0.3514 | 0.3427 | hugg, face, dataset, model | dataset, model |

### `psc_huggingface_workflow_p01_2_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before training anything, audit the dataset card: subsets, train/validation/test split, feature schema, example rows, labels, and data caveats.
- Positive-fit instruction after negation cleanup: Before training anything, audit the dataset card: subsets, train/validation/test split, feature schema, example rows, labels, and data caveats.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-hf-dataset-card-inspector` | 0.6041 | 0.6041 | 0.2038 | train, dataset, card, subset, check, split, feature, schema | - |
| `psc-sentence-embedding-trainer` | 0.3805 | 0.3805 | 0.1252 | train, dataset, split, label, data | - |
| `psc-hf-space-deployment-preparer` | 0.3348 | 0.3348 | 0.4634 | train, dataset, check | train, dataset |
| `psc-local-model-fit-selector` | 0.3135 | 0.3135 | 0.4735 | train, dataset, check | dataset, schema |

### `psc_huggingface_workflow_p02_1_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I need a support-ticket classifier that can run locally on an 8 GB laptop. Shortlist realistic model sizes, quantization choices, and latency tradeoffs.
- Positive-fit instruction after negation cleanup: I need a support-ticket classifier that can run locally on an 8 GB laptop. Shortlist realistic model sizes, quantization choices, and latency tradeoffs.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-local-model-fit-selector` | 0.4521 | 0.4521 | 0.1985 | shortlist, model, size, quantization, choice, latency, tradeoff | - |
| `psc-hf-space-deployment-preparer` | 0.3256 | 0.3256 | 0.2704 | model, choice | model |
| `psc-hf-dataset-card-inspector` | 0.3152 | 0.3152 | 0.2355 | model | model |
| `psc-sentence-embedding-trainer` | 0.2642 | 0.2642 | 0.3014 | model, choice | - |

### `psc_huggingface_workflow_p02_2_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Choose Hugging Face or GGUF local model candidates for an 8 GB Mac. I need memory-fit and quantization reasoning, not a dataset card audit.
- Positive-fit instruction after negation cleanup: Choose Hugging Face or GGUF local model candidates for an 8 GB Mac. I need memory-fit and quantization reasoning, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-local-model-fit-selector` | 0.5762 | 0.5762 | 0.2421 | choose, hugg, face, gguf, local, model, candidate, quantization | dataset |
| `psc-hf-space-deployment-preparer` | 0.4498 | 0.4498 | 0.3036 | hugg, face, model | model, dataset |
| `psc-hf-dataset-card-inspector` | 0.4155 | 0.4155 | 0.2895 | hugg, face, model | local, model |
| `psc-sentence-embedding-trainer` | 0.2831 | 0.2831 | 0.3031 | choose, hugg, face, model | local |

### `psc_huggingface_workflow_p03_1_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: We have labelled skill queries, gold skills, and hard negatives. Design the embedding fine-tuning setup and retrieval evaluation for a skill router.
- Positive-fit instruction after negation cleanup: We have labelled skill queries, gold skills, and hard negatives. Design the embedding fine-tuning setup and retrieval evaluation for a skill router.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-sentence-embedding-trainer` | 0.4845 | 0.4845 | 0.2049 | labell, hard, negative, embedd, fine-tun, setup, retrieval, evaluation | - |
| `psc-local-model-fit-selector` | 0.2897 | 0.2897 | 0.2463 | embedd, setup, evaluation | fine-tun |
| `psc-hf-dataset-card-inspector` | 0.2881 | 0.2881 | 0.2531 | embedd, evaluation | fine-tun |
| `psc-hf-space-deployment-preparer` | 0.1820 | 0.1820 | 0.3005 | embedd, evaluation | - |

### `psc_huggingface_workflow_p03_2_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Plan a SentenceTransformer fine-tuning run with positives, hard negatives, loss function, splits, top-k recall, and MRR. Do not choose a local chatbot model.
- Positive-fit instruction after negation cleanup: Plan a SentenceTransformer fine-tuning run with positives, hard negatives, loss function, splits, top-k recall, and MRR. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-sentence-embedding-trainer` | 0.6595 | 0.6595 | 0.2584 | plan, fine-tun, positive, hard, negative, loss, split, top-k | local |
| `psc-local-model-fit-selector` | 0.3070 | 0.3070 | 0.1843 | - | plan, fine-tun |
| `psc-hf-dataset-card-inspector` | 0.2995 | 0.2995 | 0.2224 | split | fine-tun, local, model |
| `psc-hf-space-deployment-preparer` | 0.2360 | 0.2360 | 0.2076 | plan | model |

### `psc_huggingface_workflow_p04_1_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare the classifier demo for Hugging Face Spaces with requirements, app entrypoint, secrets, hardware tier, queue behavior, and verification after launch.
- Positive-fit instruction after negation cleanup: Prepare the classifier demo for Hugging Face Spaces with requirements, app entrypoint, secrets, hardware tier, queue behavior, and verification after launch.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-hf-space-deployment-preparer` | 0.6680 | 0.6680 | 0.2017 | prepare, demo, hugg, face, space, requirement, app, entrypoint | - |
| `psc-hf-dataset-card-inspector` | 0.5239 | 0.5239 | 0.2804 | demo, hugg, face, space | space |
| `psc-local-model-fit-selector` | 0.5097 | 0.5097 | 0.2795 | demo, hugg, face, space, hardware | demo |
| `psc-sentence-embedding-trainer` | 0.3936 | 0.3936 | 0.3242 | demo, hugg, face, space | demo |

### `psc_huggingface_workflow_p04_2_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Package this model demo for a hosted Space-style deployment. Focus on runtime files, dependency pins, GPU/queue assumptions, and launch checks rather than training.
- Positive-fit instruction after negation cleanup: Package this model demo for a hosted Space-style deployment. Focus on runtime files, dependency pins, GPU/queue assumptions, and launch checks .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-hf-space-deployment-preparer` | 0.6470 | 0.6470 | 0.1835 | model, demo, deployment, runtime, file, gpu, queue, assumption | model, train |
| `psc-local-model-fit-selector` | 0.3763 | 0.3763 | 0.4026 | model, demo, deployment, runtime, check | demo, host, deployment |
| `psc-hf-dataset-card-inspector` | 0.3331 | 0.3331 | 0.3416 | model, demo, deployment, check | model, deployment |
| `psc-sentence-embedding-trainer` | 0.1388 | 0.1388 | 0.3495 | model, demo, deployment | demo |

### `psc_pdf_document_work_p01_1_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Gold rank among listed candidates: 1
- Instruction used for scoring: The vendor packet PDF has selectable text and tables. Pull out the document metadata, section text, and invoice rows into structured JSON with page anchors.
- Positive-fit instruction after negation cleanup: The vendor packet PDF has selectable text and tables. Pull out the document metadata, section text, and invoice rows into structured JSON with page anchors.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-native-extraction-pack` | 0.6853 | 0.6853 | 0.4369 | text, packet, pdf, selectable, table, extract, document, metadata | pdf |
| `psc-pdf-evidence-qa` | 0.4976 | 0.4976 | 0.5591 | text, packet, pdf, extract, document, section, page, anchor | pdf, table, extract |
| `psc-pdf-scan-ocr-recovery` | 0.4696 | 0.4696 | 0.3974 | text, packet, pdf, selectable, extract, document, page, anchor | text, table, extract |
| `psc-pdf-redaction-pass` | 0.4639 | 0.4639 | 0.2205 | text, packet, pdf, extract, document, section, invoice, page | table, extract |

### `psc_pdf_document_work_p01_2_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use a pdfplumber-style native extraction workflow on the vendor packet. I need embedded text, table cells, metadata, and page anchors, not OCR or a prose answer.
- Positive-fit instruction after negation cleanup: Use a pdfplumber-style native extraction workflow on the vendor packet. I need embedded text, table cells, metadata, and page anchors, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-native-extraction-pack` | 0.7313 | 0.7313 | 0.5135 | native, extract, workflow, packet, embedd, text, table, cell | ocr, prose, answer |
| `psc-pdf-scan-ocr-recovery` | 0.4924 | 0.4924 | 0.4623 | extract, workflow, packet, text, page, anchor | native, extract, text, table |
| `psc-pdf-redaction-pass` | 0.4822 | 0.4822 | 0.3477 | extract, workflow, packet, text, page, anchor | native, extract, table, answer |
| `psc-pdf-evidence-qa` | 0.4653 | 0.4653 | 0.5840 | extract, workflow, packet, text, page, anchor | extract, table, ocr, answer |

### `psc_pdf_document_work_p02_1_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Gold rank among listed candidates: 1
- Instruction used for scoring: This signed PDF packet looks like photographed scans. Recover the readable text page by page and flag uncertain handwriting or blurred regions.
- Positive-fit instruction after negation cleanup: This signed PDF packet looks like photographed scans. Recover the readable text page by page and flag uncertain handwriting or blurred regions.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-scan-ocr-recovery` | 0.6474 | 0.6474 | 0.1536 | page, pdf, packet, photograph, recover, text, uncertain, handwrit | text |
| `psc-pdf-native-extraction-pack` | 0.4432 | 0.4432 | 0.6005 | page, pdf, packet, text | pdf |
| `psc-pdf-evidence-qa` | 0.4366 | 0.4366 | 0.4772 | page, pdf, packet, readable, text, flag, uncertain | pdf |
| `psc-pdf-redaction-pass` | 0.4223 | 0.4223 | 0.1096 | page, pdf, packet, look, scan, text | - |

### `psc_pdf_document_work_p02_2_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Run an OCR recovery workflow for the scanned receipt PDF. Preserve page order and confidence notes instead of treating it as a born-digital table extraction.
- Positive-fit instruction after negation cleanup: Run an OCR recovery workflow for the scanned receipt PDF. Preserve page order and confidence notes .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-scan-ocr-recovery` | 0.7413 | 0.7413 | 0.4131 | run, ocr, recovery, workflow, scann, pdf, page, order | table, extract |
| `psc-pdf-native-extraction-pack` | 0.5178 | 0.5178 | 0.6007 | ocr, recovery, workflow, pdf, page, note | ocr, pdf |
| `psc-pdf-evidence-qa` | 0.4586 | 0.4586 | 0.7041 | ocr, recovery, workflow, pdf, page, note | ocr, pdf, table, extract |
| `psc-pdf-redaction-pass` | 0.4458 | 0.4458 | 0.2738 | ocr, recovery, workflow, pdf, page, note | table, extract |

### `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Gold rank among listed candidates: 1
- Instruction used for scoring: From the policy PDF, tell me whether delayed-travel meals are reimbursable and point to the page evidence that supports the answer.
- Positive-fit instruction after negation cleanup: From the policy PDF, tell me whether delayed-travel meals are reimbursable and point to the page evidence that supports the answer.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-evidence-qa` | 0.1705 | 0.1705 | 0.0477 | pdf, point, page, evidence, support, answer | pdf, answer |
| `psc-pdf-redaction-pass` | 0.1632 | 0.1632 | 0.1834 | pdf, page, evidence, answer | policy, answer |
| `psc-pdf-native-extraction-pack` | 0.1041 | 0.1041 | 0.0614 | pdf, whether, page, evidence, answer | pdf, answer |
| `psc-pdf-scan-ocr-recovery` | 0.0712 | 0.0712 | 0.1550 | pdf, page, evidence, answer | - |

### `psc_pdf_document_work_p03_2_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Answer a narrow question from the PDF with cited page evidence. I only need the supported answer and uncertainty notes, not a converted document or extracted table.
- Positive-fit instruction after negation cleanup: Answer a narrow question from the PDF with cited page evidence. I only need the supported answer and uncertainty notes, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-evidence-qa` | 0.4734 | 0.4734 | 0.5727 | answer, question, pdf, page, evidence, support, uncertainty, note | answer, question, pdf, convert, extract, table |
| `psc-pdf-redaction-pass` | 0.2597 | 0.2597 | 0.4206 | answer, pdf, page, evidence, note | answer, question, extract, table |
| `psc-pdf-native-extraction-pack` | 0.2562 | 0.2562 | 0.3764 | answer, pdf, page, evidence, uncertainty, note | answer, question, pdf |
| `psc-pdf-scan-ocr-recovery` | 0.2499 | 0.2499 | 0.3268 | answer, pdf, page, evidence, uncertainty | extract, table |

### `psc_pdf_document_work_p04_1_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before I send this contract PDF to a vendor, identify the page-level items that should be hidden, including names, addresses, pricing, IDs, and confidential clauses.
- Positive-fit instruction after negation cleanup: Before I send this contract PDF to a vendor, identify the page-level items that should be hidden, including names, addresses, pricing, IDs, and confidential clauses.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-redaction-pass` | 0.5897 | 0.5897 | 0.2484 | send, contract, pdf, name, addresse, pric, ids, confidential | - |
| `psc-pdf-native-extraction-pack` | 0.5016 | 0.5016 | 0.3728 | pdf | pdf |
| `psc-pdf-evidence-qa` | 0.4804 | 0.4804 | 0.4141 | pdf, identify | pdf |
| `psc-pdf-scan-ocr-recovery` | 0.4608 | 0.4608 | 0.2802 | pdf | - |

### `psc_pdf_document_work_p04_2_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Prepare a PDF redaction checklist for external sharing. I need sensitive targets with page anchors, not a summary or field extraction table.
- Positive-fit instruction after negation cleanup: Prepare a PDF redaction checklist for external sharing. I need sensitive targets with page anchors, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-pdf-redaction-pass` | 0.6561 | 0.6561 | 0.3606 | pdf, redaction, checklist, external, shar, sensitive, target, page | extract, table |
| `psc-pdf-evidence-qa` | 0.5207 | 0.5207 | 0.4085 | pdf, redaction, external, shar, page, anchor | pdf, extract, table |
| `psc-pdf-native-extraction-pack` | 0.4597 | 0.4597 | 0.4148 | pdf, redaction, external, shar, page, anchor | pdf, redaction |
| `psc-pdf-scan-ocr-recovery` | 0.3996 | 0.3996 | 0.3788 | pdf, redaction, external, shar, page, anchor | redaction, extract, table |

### `psc_research_reading_p01_1_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: For this paper, map how the study was carried out: data, method components, baselines, metrics, assumptions, and evaluation limits.
- Positive-fit instruction after negation cleanup: For this paper, map how the study was carried out: data, method components, baselines, metrics, assumptions, and evaluation limits.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-paper-method-mapper` | 0.5956 | 0.5956 | 0.3875 | paper, map, was, carri, data, method, component, baseline | - |
| `psc-citation-claim-support-auditor` | 0.3476 | 0.3476 | 0.3566 | paper, method | paper, method |
| `psc-related-work-synthesizer` | 0.2785 | 0.2785 | 0.2321 | paper, method, assumption | method |
| `psc-source-field-table-extractor` | 0.2637 | 0.2637 | 0.2177 | paper, method | - |

### `psc_research_reading_p01_2_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Extract method and evaluation details from the paper. I need setup, baselines, metrics, assumptions, and limitations, not a broad summary.
- Positive-fit instruction after negation cleanup: Extract method and evaluation details from the paper. I need setup, baselines, metrics, assumptions, and limitations, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-paper-method-mapper` | 0.5875 | 0.5875 | 0.5081 | extract, method, evaluation, detail, paper, setup, baseline, metric | summary |
| `psc-source-field-table-extractor` | 0.3662 | 0.3662 | 0.2954 | extract, method, paper | broad |
| `psc-citation-claim-support-auditor` | 0.3398 | 0.3398 | 0.6072 | method, paper | extract, method, paper, summary |
| `psc-related-work-synthesizer` | 0.2686 | 0.2686 | 0.4381 | method, paper, assumption | extract, method |

### `psc_research_reading_p02_1_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check whether this source really supports my sentence about skill libraries improving agent reliability, and suggest safer wording if it overclaims.
- Positive-fit instruction after negation cleanup: Check whether this source really supports my sentence about skill libraries improving agent reliability, and suggest safer wording if it overclaims.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-citation-claim-support-auditor` | 0.4728 | 0.4728 | 0.2690 | check, whether, support, safer, word, overclaim | - |
| `psc-paper-method-mapper` | 0.2962 | 0.2962 | 0.2921 | - | support |
| `psc-source-field-table-extractor` | 0.2944 | 0.2944 | 0.3190 | - | support |
| `psc-related-work-synthesizer` | 0.2504 | 0.2504 | 0.3792 | - | check |

### `psc_research_reading_p02_2_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Perform a citation-grounding audit for one draft claim: support strength, exact evidence, caveats, and revised claim wording.
- Positive-fit instruction after negation cleanup: Perform a citation-grounding audit for one draft claim: support strength, exact evidence, caveats, and revised claim wording.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-citation-claim-support-auditor` | 0.7198 | 0.7198 | 0.2236 | claim, draft, support, strength, evidence, caveat, word | - |
| `psc-paper-method-mapper` | 0.4011 | 0.4011 | 0.5616 | claim, evidence | audit, support |
| `psc-source-field-table-extractor` | 0.3536 | 0.3536 | 0.3349 | claim, evidence | support |
| `psc-related-work-synthesizer` | 0.3329 | 0.3329 | 0.5056 | claim, evidence | - |

### `psc_research_reading_p03_1_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Use these three papers to write related-work notes that compare approaches, show where they agree or diverge, and identify the gap my thesis targets.
- Positive-fit instruction after negation cleanup: Use these three papers to write related-work notes that compare approaches, show where they agree or diverge, and identify the gap my thesis targets.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-related-work-synthesizer` | 0.5196 | 0.5196 | 0.3264 | paper, write, related-work, note, compare, approache, identify, gap | - |
| `psc-paper-method-mapper` | 0.3927 | 0.3927 | 0.3919 | paper, compare, identify, thesi | - |
| `psc-citation-claim-support-auditor` | 0.3180 | 0.3180 | 0.3645 | paper, compare, identify, thesi | paper |
| `psc-source-field-table-extractor` | 0.2617 | 0.2617 | 0.2055 | paper, note, compare, identify, thesi | - |

### `psc_research_reading_p03_2_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Synthesize multiple sources into a related-work argument with themes, contrasts, unresolved limitations, and thesis positioning.
- Positive-fit instruction after negation cleanup: Synthesize multiple sources into a related-work argument with themes, contrasts, unresolved limitations, and thesis positioning.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-related-work-synthesizer` | 0.6657 | 0.6657 | 0.2345 | synthesize, multiple, related-work, argument, theme, contrast, unresolv, thesi | - |
| `psc-citation-claim-support-auditor` | 0.3656 | 0.3656 | 0.2933 | thesi | - |
| `psc-source-field-table-extractor` | 0.3484 | 0.3484 | 0.3827 | thesi | - |
| `psc-paper-method-mapper` | 0.2984 | 0.2984 | 0.3617 | limitation, thesi | - |

### `psc_research_reading_p04_1_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Extract each paper's dataset, task, model, baseline, metric, result, and limitation into a comparison table with source evidence.
- Positive-fit instruction after negation cleanup: Extract each paper's dataset, task, model, baseline, metric, result, and limitation into a comparison table with source evidence.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-paper-method-mapper` | 0.5496 | 0.5496 | 0.4380 | extract, paper', baseline, metric, result, limitation, compare, evidence | - |
| `psc-source-field-table-extractor` | 0.5409 | 0.5409 | 0.3052 | extract, compare, table, evidence | - |
| `psc-citation-claim-support-auditor` | 0.4619 | 0.4619 | 0.4758 | compare, evidence | extract |
| `psc-related-work-synthesizer` | 0.4321 | 0.4321 | 0.4181 | compare, evidence | extract |

### `psc_research_reading_p04_2_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Turn the source into a structured field table. I need field values and evidence snippets, not a narrative summary or related-work synthesis.
- Positive-fit instruction after negation cleanup: Turn the source into a structured field table. I need field values and evidence snippets, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-source-field-table-extractor` | 0.7497 | 0.7497 | 0.4652 | field, structur, table, value, evidence, snippet | field, synthesi |
| `psc-citation-claim-support-auditor` | 0.4554 | 0.4554 | 0.3114 | evidence | summary |
| `psc-related-work-synthesizer` | 0.3305 | 0.3305 | 0.3002 | evidence | - |
| `psc-paper-method-mapper` | 0.2772 | 0.2772 | 0.4444 | evidence | summary, synthesi |

### `psc_security_appsec_p01_1_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Before building invite-by-link file sharing, map what needs protection, who can interact with it, where control changes hands, how it could be abused, and what safeguards we should add.
- Positive-fit instruction after negation cleanup: Before building invite-by-link file sharing, map what needs protection, who can interact with it, where control changes hands, how it could be abused, and what safeguards we should add.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-privacy-telemetry-reviewer` | 0.3759 | 0.3759 | 0.2745 | shar | - |
| `psc-feature-threat-modeler` | 0.3723 | 0.3723 | 0.2570 | - | - |
| `psc-handler-vulnerability-reviewer` | 0.3208 | 0.3208 | 0.2830 | - | - |
| `psc-dependency-supply-chain-auditor` | 0.2988 | 0.2988 | 0.3228 | add | - |

### `psc_security_appsec_p01_2_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a design-stage threat model for the new collaborator-invite feature. I need abuse paths and mitigations, not a code-level vulnerability review.
- Positive-fit instruction after negation cleanup: Create a design-stage threat model for the new collaborator-invite feature. I need abuse paths and mitigations, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-feature-threat-modeler` | 0.5065 | 0.5065 | 0.1797 | threat, model, feature, abuse, mitigation | review |
| `psc-handler-vulnerability-reviewer` | 0.3701 | 0.3701 | 0.3939 | feature, path, mitigation | threat, model, review |
| `psc-dependency-supply-chain-auditor` | 0.3128 | 0.3128 | 0.1740 | feature, mitigation | review |
| `psc-privacy-telemetry-reviewer` | 0.2828 | 0.2828 | 0.4196 | feature, mitigation | threat, model |

### `psc_security_appsec_p02_1_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this redirect handler for concrete security bugs around user input, auth checks, URL validation, and test coverage.
- Positive-fit instruction after negation cleanup: Review this redirect handler for concrete security bugs around user input, auth checks, URL validation, and test coverage.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-handler-vulnerability-reviewer` | 0.3972 | 0.3972 | 0.1779 | check, review, handler, concrete, security, user, input, auth | review |
| `psc-privacy-telemetry-reviewer` | 0.1726 | 0.1726 | 0.1747 | check, review, user | security |
| `psc-feature-threat-modeler` | 0.1547 | 0.1547 | 0.1637 | check | review, handler |
| `psc-dependency-supply-chain-auditor` | 0.0854 | 0.0854 | 0.2225 | check | review |

### `psc_security_appsec_p02_2_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Do an implementation-level security review of the API handler. Focus on exploitable flaws and code fixes, not feature-level threat modeling.
- Positive-fit instruction after negation cleanup: Do an implementation-level security review of the API handler. Focus on exploitable flaws and code fixes, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-handler-vulnerability-reviewer` | 0.5742 | 0.5742 | 0.3370 | implementation-level, security, review, handler, exploitable, flaw, code, fixe | review, threat, model |
| `psc-feature-threat-modeler` | 0.2914 | 0.2914 | 0.3509 | code | review, handler, code |
| `psc-dependency-supply-chain-auditor` | 0.2805 | 0.2805 | 0.2551 | code | review, code |
| `psc-privacy-telemetry-reviewer` | 0.2708 | 0.2708 | 0.4148 | review, code | security, threat, model |

### `psc_security_appsec_p03_1_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: We are about to add an npm package with a postinstall script and many transitive dependencies. Assess the supply-chain risk and mitigation options.
- Positive-fit instruction after negation cleanup: We are about to add an npm package with a postinstall script and many transitive dependencies. Assess the supply-chain risk and mitigation options.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-dependency-supply-chain-auditor` | 0.6561 | 0.6561 | 0.0734 | add, package, script, transitive, dependencie, asses, supply-chain, risk | - |
| `psc-handler-vulnerability-reviewer` | 0.2866 | 0.2866 | 0.1259 | dependencie, risk, mitigation | - |
| `psc-feature-threat-modeler` | 0.2688 | 0.2688 | 0.4816 | dependencie, risk, mitigation | supply-chain, risk |
| `psc-privacy-telemetry-reviewer` | 0.1365 | 0.1365 | 0.3053 | dependencie, risk, mitigation | risk |

### `psc_security_appsec_p03_2_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit a third-party dependency before adoption: maintainer health, install scripts, transitive risk, old packages, and safer alternatives.
- Positive-fit instruction after negation cleanup: Audit a third-party dependency before adoption: maintainer health, install scripts, transitive risk, old packages, and safer alternatives.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-dependency-supply-chain-auditor` | 0.6932 | 0.6932 | 0.2622 | third-party, dependency, maintainer, install, script, transitive, risk, old | - |
| `psc-handler-vulnerability-reviewer` | 0.3503 | 0.3503 | 0.2672 | risk | - |
| `psc-feature-threat-modeler` | 0.2858 | 0.2858 | 0.5703 | risk | dependency, risk |
| `psc-privacy-telemetry-reviewer` | 0.2813 | 0.2813 | 0.3792 | risk, safer | dependency, risk |

### `psc_security_appsec_p04_1_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review the analytics plan that logs search queries, account region, role, clicked filters, and partial email domains for 18 months.
- Positive-fit instruction after negation cleanup: Review the analytics plan that logs search queries, account region, role, clicked filters, and partial email domains for 18 months.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-privacy-telemetry-reviewer` | 0.2861 | 0.2861 | 0.0656 | review, plan | - |
| `psc-feature-threat-modeler` | 0.1324 | 0.1324 | 0.2005 | - | review |
| `psc-handler-vulnerability-reviewer` | 0.1238 | 0.1238 | 0.2747 | review | review |
| `psc-dependency-supply-chain-auditor` | 0.1164 | 0.1164 | 0.2464 | - | review |

### `psc_security_appsec_p04_2_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Assess privacy risk for a telemetry change: data minimization, retention, consent, access controls, and re-identification. Do not focus on code exploits.
- Positive-fit instruction after negation cleanup: Assess privacy risk for a telemetry change: data minimization, retention, consent, access controls, and re-identification. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-privacy-telemetry-reviewer` | 0.7272 | 0.7272 | 0.3118 | privacy, risk, telemetry, data, minimization, retention, consent, acces | risk |
| `psc-feature-threat-modeler` | 0.2522 | 0.2522 | 0.2999 | privacy, risk, data | risk, code |
| `psc-dependency-supply-chain-auditor` | 0.1632 | 0.1632 | 0.4270 | asses, privacy, risk, data | privacy, data, code |
| `psc-handler-vulnerability-reviewer` | 0.1610 | 0.1610 | 0.4486 | privacy, risk, data | privacy, retention |

### `psc_skill_representation_p01_1_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Review this rough capability note and produce a selector-facing inventory: when it should trigger, required inputs, expected artifact, steps, tools, examples, and gaps.
- Positive-fit instruction after negation cleanup: Review this rough capability note and produce a selector-facing inventory: when it should trigger, required inputs, expected artifact, steps, tools, examples, and gaps.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-messy-skill-field-extractor` | 0.4074 | 0.4074 | 0.2983 | trigger, input, artifact, example | - |
| `psc-skill-routing-budget-planner` | 0.3113 | 0.3113 | 0.2299 | inventory, artifact | - |
| `psc-retrieval-result-adjudicator` | 0.2890 | 0.2890 | 0.2458 | note, artifact | - |
| `psc-public-skill-atomizer` | 0.2443 | 0.2443 | 0.1691 | note, artifact | - |

### `psc_skill_representation_p01_2_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Perform a field-taxonomy audit of an existing skill artifact with evidence spans. Do not write or install a new skill.
- Positive-fit instruction after negation cleanup: Perform a field-taxonomy audit of an existing skill artifact with evidence spans. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-messy-skill-field-extractor` | 0.7215 | 0.7215 | 0.5686 | audit, exist, skill, artifact, evidence, span | skill, install, new |
| `psc-retrieval-result-adjudicator` | 0.4623 | 0.4623 | 0.3989 | skill, artifact | skill |
| `psc-public-skill-atomizer` | 0.4074 | 0.4074 | 0.3099 | skill, artifact | - |
| `psc-skill-routing-budget-planner` | 0.4024 | 0.4024 | 0.6874 | skill, artifact | skill, audit |

### `psc_skill_representation_p02_1_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: This public skill has separate finance, document, and research branches inside one file. Split it into atomic skill candidates and keep shared resources linked.
- Positive-fit instruction after negation cleanup: This public skill has separate finance, document, and research branches inside one file. Split it into atomic skill candidates and keep shared resources linked.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-public-skill-atomizer` | 0.6698 | 0.6698 | 0.2580 | skill, public, branche, file, split, atomic, candidate, shar | - |
| `psc-messy-skill-field-extractor` | 0.5295 | 0.5295 | 0.4689 | skill, separate, file, candidate, resource | skill |
| `psc-skill-routing-budget-planner` | 0.4895 | 0.4895 | 0.5109 | skill, candidate, resource | skill |
| `psc-retrieval-result-adjudicator` | 0.3707 | 0.3707 | 0.3761 | skill, candidate, resource | skill |

### `psc_skill_representation_p02_2_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Atomize a broad hierarchical skill into standalone child skills with preserved resource references and routing boundaries.
- Positive-fit instruction after negation cleanup: Atomize a broad hierarchical skill into standalone child skills with preserved resource references and routing boundaries.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-public-skill-atomizer` | 0.6573 | 0.6573 | 0.0842 | skill, broad, hierarchical, child, preserv, resource, rout, boundarie | - |
| `psc-skill-routing-budget-planner` | 0.5648 | 0.5648 | 0.4580 | skill, resource, rout | skill, hierarchical |
| `psc-messy-skill-field-extractor` | 0.4637 | 0.4637 | 0.3227 | skill, resource, rout, boundarie | skill |
| `psc-retrieval-result-adjudicator` | 0.2734 | 0.2734 | 0.4935 | skill, resource, rout | skill |

### `psc_skill_representation_p03_1_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design a routing policy for a 2000-skill library: candidate generation, representation fields, reranking, fallback, and cost controls.
- Positive-fit instruction after negation cleanup: Design a routing policy for a 2000-skill library: candidate generation, representation fields, reranking, fallback, and cost controls.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-skill-routing-budget-planner` | 0.7599 | 0.7599 | 0.3345 | design, rout, policy, library, candidate, representation, field, rerank | field |
| `psc-public-skill-atomizer` | 0.5350 | 0.5350 | 0.1468 | rout, candidate, field | field |
| `psc-messy-skill-field-extractor` | 0.4021 | 0.4021 | 0.3836 | rout, candidate, field | - |
| `psc-retrieval-result-adjudicator` | 0.3848 | 0.3848 | 0.6059 | rout, policy, candidate, field | design, policy, field |

### `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Specify a candidate-subsetting architecture for skill retrieval with top-k budgets, field-aware reranking, fallback, and evaluation metrics.
- Positive-fit instruction after negation cleanup: Specify a candidate-subsetting architecture for skill retrieval with top-k budgets, field-aware reranking, fallback, and evaluation metrics.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-retrieval-result-adjudicator` | 0.5955 | 0.5955 | 0.3141 | skill, retrieval, top-k, evaluation, metric | skill |
| `psc-skill-routing-budget-planner` | 0.5843 | 0.5843 | 0.4498 | specify, skill, retrieval, budget, rerank, fallback, evaluation, metric | skill |
| `psc-messy-skill-field-extractor` | 0.5346 | 0.5346 | 0.5282 | skill, evaluation | skill, retrieval |
| `psc-public-skill-atomizer` | 0.4469 | 0.4469 | 0.4625 | skill, evaluation | - |

### `psc_skill_representation_p04_1_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Evaluate these skill retrieval rankings with strict gold labels, acceptable alternatives, top-1, top-5, MRR, and failure categories.
- Positive-fit instruction after negation cleanup: Evaluate these skill retrieval rankings with strict gold labels, acceptable alternatives, top-1, top-5, MRR, and failure categories.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-retrieval-result-adjudicator` | 0.7302 | 0.7302 | 0.2827 | skill, retrieval, ranking, strict, gold, label, acceptable, alternative | skill |
| `psc-messy-skill-field-extractor` | 0.4824 | 0.4824 | 0.5095 | skill, label | skill, retrieval |
| `psc-skill-routing-budget-planner` | 0.4426 | 0.4426 | 0.3937 | skill, retrieval | skill |
| `psc-public-skill-atomizer` | 0.3719 | 0.3719 | 0.4380 | skill | - |

### `psc_skill_representation_p04_2_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Adjudicate retrieval results: separate strict and acceptable scoring, identify candidate misses versus reranker losses, and flag better-than-gold cases.
- Positive-fit instruction after negation cleanup: Adjudicate retrieval results: separate strict and acceptable scoring, identify candidate misses versus reranker losses, and flag better-than-gold cases.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `psc-retrieval-result-adjudicator` | 0.7430 | 0.7430 | 0.1953 | adjudicate, retrieval, result, strict, acceptable, candidate, reranker, better-than-gold | - |
| `psc-skill-routing-budget-planner` | 0.3490 | 0.3490 | 0.3123 | retrieval, result, candidate | - |
| `psc-messy-skill-field-extractor` | 0.3465 | 0.3465 | 0.4778 | result, separate, candidate | retrieval, result |
| `psc-public-skill-atomizer` | 0.2670 | 0.2670 | 0.5069 | result, identify, candidate | scor |

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Give me a balanced research-oriented recap of this academic paper. I want the research problem, overall approach, main findings, and limitations in one readable summary, not citation-ready notes and not a method-only audit
- Positive-fit instruction after negation cleanup: Give me a balanced research-oriented recap of this academic paper. I want the research problem, overall approach, main findings, and limitations in one readable summary,

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `paper-summariser` | 0.5417 | 0.5417 | 0.4449 | research-orient, recap, academic, paper, research, approach, main, finding | main, citation-ready, note |
| `general-source-summariser` | 0.4125 | 0.4125 | 0.5375 | recap, paper, research, main, readable, summary | research, summary |
| `citation-note-extractor` | 0.3014 | 0.3014 | 0.4572 | paper, research, main, finding, limitation, summary | paper, summary |
| `method-note-builder` | 0.2729 | 0.2729 | 0.4888 | recap, paper, research, problem, limitation, summary | paper, summary, note |

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Summarise this as a general source report rather than an academic paper. I need the context, main observations, practical recommendations, and evidence limits in plain language
- Positive-fit instruction after negation cleanup: Summarise this as a general source report . I need the context, main observations, practical recommendations, and evidence limits in plain language

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `general-source-summariser` | 0.5022 | 0.5022 | 0.4506 | summary, report, context, main, observation, recommendation, evidence, limit | summary |
| `paper-summariser` | 0.4085 | 0.4085 | 0.3889 | summary, main, limit | main |
| `citation-note-extractor` | 0.3717 | 0.3717 | 0.4570 | summary, main, observation, limit | summary, paper |
| `document-extractor` | 0.3595 | 0.3595 | 0.4001 | summary | summary |

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Make this source usable for me later when I'm writing by producing citation-ready notes
- Positive-fit instruction after negation cleanup: Make this source usable for me later when I'm writing by producing citation-ready notes

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `citation-note-extractor` | 0.7184 | 0.7184 | 0.4164 | writ, citation-ready, note | writ, produc |
| `paper-summariser` | 0.4985 | 0.4985 | 0.7076 | note | citation-ready, note |
| `citation-grounding-helper` | 0.4948 | 0.4948 | 0.6754 | note | writ, note |
| `document-extractor` | 0.4427 | 0.4427 | 0.5407 | note | writ, produc, citation-ready, note |

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Extract the specific details from this source into a structured table of fields and values
- Positive-fit instruction after negation cleanup: Extract the specific details from this source into a structured table of fields and values

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `document-extractor` | 0.5717 | 0.5717 | 0.1679 | extract, specific, structur, field, value | - |
| `method-note-builder` | 0.3638 | 0.3638 | 0.2872 | extract, specific, detail, structur, field | extract |
| `citation-note-extractor` | 0.3323 | 0.3323 | 0.1468 | detail | - |
| `paper-summariser` | 0.2805 | 0.2805 | 0.3441 | extract, detail | extract |

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Help me make sense of this source by focusing on how the work was actually carried out, how it was evaluated, and what assumptions or constraints shaped the result
- Positive-fit instruction after negation cleanup: Help me make sense of this source by focusing on how the work was actually carried out, how it was evaluated, and what assumptions or constraints shaped the result

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `method-note-builder` | 0.3892 | 0.3892 | 0.4492 | was, work, carri, assumption, constraint, result | work |
| `paper-summariser` | 0.3451 | 0.3451 | 0.4123 | was, assumption, result | - |
| `document-extractor` | 0.3030 | 0.3030 | 0.3652 | result | focus, work |
| `citation-note-extractor` | 0.2486 | 0.2486 | 0.4325 | work, result | - |

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I wrote this exact sentence from the source: 'Explicit task decomposition reliably improves agent performance in realistic environments.' Perform a citation-grounding support audit: mark which parts of the sentence are supported, overstated, or unsupported, explain the overreach, and give a safer revised sentence if needed.
- Positive-fit instruction after negation cleanup: I wrote this exact sentence from the source: 'Explicit task decomposition reliably improves agent performance in realistic environments.' Perform a citation-grounding support audit: mark which parts of the sentence are supported, overstated, or unsupported, explain the overreach, and give a safer revised sentence if needed.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `citation-grounding-helper` | 0.5216 | 0.5216 | 0.4342 | sentence, support, exact, task, part, overstat, unsupport, explain | - |
| `citation-note-extractor` | 0.4574 | 0.4574 | 0.3834 | support, task | support |
| `document-extractor` | 0.4284 | 0.4284 | 0.4048 | explicit, task | - |
| `paper-summariser` | 0.3453 | 0.3453 | 0.4645 | - | - |

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compare these two sources in a side-by-side table with separate columns for Source A and Source B so I can clearly see how they line up, where they differ, and what each one contributes. Use rows such as approach, evaluation, strengths, limitations, and contribution; do not turn it into a synthesized related-work paragraph, method-only note, or citation-note list.
- Positive-fit instruction after negation cleanup: Compare these two sources in a side-by-side table with separate columns for Source A and Source B so I can clearly see how they line up, where they differ, and what each one contributes. Use rows such as approach, evaluation, strengths, limitations, and contribution; .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `multi-source-comparison-builder` | 0.5997 | 0.5997 | 0.5610 | compare, two, side-by-side, see, each, such, evaluation | related-work, note |
| `related-work-synthesiser` | 0.4436 | 0.4436 | 0.6912 | compare, see, each, limitation | compare, side-by-side, table, note |
| `citation-note-extractor` | 0.3344 | 0.3344 | 0.3733 | compare, see, limitation | compare, related-work |
| `method-note-builder` | 0.2972 | 0.2972 | 0.4465 | compare, see, evaluation, limitation | synthesiz, note |

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Synthesize these two sources into related-work style notes: explain the main approaches, how they relate, the shared research direction, and what remains unresolved across them. I want an integrated synthesis, not a side-by-side comparison table.
- Positive-fit instruction after negation cleanup: Synthesize these two sources into related-work style notes: explain the main approaches, how they relate, the shared research direction, and what remains unresolved across them. I want an integrated synthesis, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `related-work-synthesiser` | 0.7216 | 0.7216 | 0.4768 | related-work, style, note, explain, main, approache, relate, shar | note, main, side-by-side, compare, table |
| `paper-summariser` | 0.4558 | 0.4558 | 0.5587 | note, main, research, synthesi | related-work, note, main |
| `citation-note-extractor` | 0.4476 | 0.4476 | 0.3768 | note, main, research, synthesi | related-work, acros, compare |
| `multi-source-comparison-builder` | 0.4291 | 0.4291 | 0.4982 | two, note, research, them, synthesi | related-work, note, main |

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Draft a respectful academic email reply to this message from my professor, including availability and a polite tone suitable for a supervisor relationship: 'Hi Jacky, thanks for your update. Would you be available to meet next Tuesday afternoon to discuss the revised thesis scope? Please let me know what time suits you best.'
- Positive-fit instruction after negation cleanup: Draft a respectful academic email reply to this message from my professor, including availability and a polite tone suitable for a supervisor relationship: 'Hi Jacky, thanks for your update. Would you be available to meet next Tuesday afternoon to discuss the revised thesis scope? Please let me know what time suits you best.'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `professor-email-reply` | 0.5624 | 0.5624 | 0.2754 | draft, respectful, academic, email, reply, message, professor, polite | draft, reply |
| `reply-drafter` | 0.4254 | 0.4254 | 0.3663 | draft, academic, email, reply, message, tone | draft, reply, message, availability, tone |
| `reply-polisher` | 0.3769 | 0.3769 | 0.3310 | draft, academic, email, reply, message, tone | reply, message |

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Edit this already-written message only. Keep the same meaning, availability, and commitments, but improve flow, phrasing, tone, and readability. Return the refined version of this message.
- Positive-fit instruction after negation cleanup: Edit this already-written message only. Keep the same meaning, availability, and commitments, but improve flow, phrasing, tone, and readability. Return the refined version of this message.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `reply-polisher` | 0.5872 | 0.5872 | 0.4493 | message, edit, already-written, only, keep, same, mean, commitment | message, only |
| `reply-drafter` | 0.5602 | 0.5602 | 0.5262 | message, edit, already-written, only, keep, commitment, but, tone | message, edit, already-written, only, keep, same, mean, availability |
| `professor-email-reply` | 0.4174 | 0.4174 | 0.3302 | message, only, keep, commitment, phras, tone, return | edit, already-written, only, same, commitment, refin, version |

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Draft a reply to these teammates about shared project coordination. The reply should clarify what I can take ownership of, confirm the deadline situation, and help the group move the work forward: 'Hey everyone, we need to lock in who is doing the slides, who is writing the report section, and whether we can still meet the Friday deadline. Can each of you confirm what you can finish by tomorrow?'
- Positive-fit instruction after negation cleanup: Draft a reply to these teammates about shared project coordination. The reply should clarify what I can take ownership of, confirm the deadline situation, and help the group move the work forward: 'Hey everyone, we need to lock in who is doing the slides, who is writing the report section, and whether we can still meet the Friday deadline. Can each of you confirm what you can finish by tomorrow?'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `groupwork-reply` | 0.6194 | 0.6194 | 0.3943 | reply, deadline, who, draft, teammate, shar, project, coordination | reply, coordination, group |
| `followup-reply-writer` | 0.4357 | 0.4357 | 0.3440 | reply, confirm, draft, coordination, clarify, group, whether, meet | reply, draft |
| `reply-drafter` | 0.3486 | 0.3486 | 0.3409 | reply, deadline, draft, coordination, group, whether | reply, deadline, draft, writ |

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Write a response whose main purpose is to state my next actions clearly
- Positive-fit instruction after negation cleanup: Write a response whose main purpose is to state my next actions clearly

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `followup-reply-writer` | 0.6110 | 0.6110 | 0.4964 | reply, main, state, next, action, clearly | reply, clearly |
| `groupwork-reply` | 0.5228 | 0.5228 | 0.4388 | reply, main, next, action, clearly | reply, main |
| `reply-drafter` | 0.5157 | 0.5157 | 0.4259 | reply, main, clearly | reply, clearly |

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Compose a concise new response from the source message only, confirming that I can send the requested file tomorrow. There is no existing reply text to polish, and I do not need a detailed action plan: 'Thanks for the update. Could you send me the file by tomorrow if possible?'
- Positive-fit instruction after negation cleanup: Compose a concise new response from the source message only, confirming that I can send the requested file tomorrow. There is : 'Thanks for the update. Could you send me the file by tomorrow if possible?'

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `reply-drafter` | 0.5198 | 0.5198 | 0.5440 | concise, new, reply, message, only | reply, message, only, exist, polish |
| `followup-reply-writer` | 0.4680 | 0.4680 | 0.4191 | concise, reply, message, only, confirm | reply |
| `reply-polisher` | 0.4158 | 0.4158 | 0.5710 | send, new, reply, message, only, request | reply, message, only, action |

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Gold rank among listed candidates: 3
- Instruction used for scoring: We are designing a new file-sharing feature where users can invite collaborators by email, generate public links, and revoke access later. Before implementation, reason across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.
- Positive-fit instruction after negation cleanup: We are designing a new file-sharing feature where users can invite collaborators by email, generate public links, and revoke access later. Before implementation, reason across protected assets, external actors, component boundaries, abuse scenarios, security assumptions, mitigations, detection ideas, and residual risk.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `privacy-risk-reviewer` | 0.5518 | 0.5518 | 0.4195 | design, feature, user, security, mitigation, risk | design, acros, protect, asset, external, actor, component, boundarie |
| `auth-flow-reviewer` | 0.4283 | 0.4283 | 0.4183 | design, feature, user, acces, protect, actor, boundarie, scenario | design, acces, implementation, acros, protect, asset, external, actor |
| `security-threat-modeler` | 0.4047 | 0.4047 | 0.2787 | design, feature, user, implementation, reason, asset, external, actor | risk |
| `security-code-reviewer` | 0.3822 | 0.3822 | 0.4235 | design, feature, user, implementation, boundarie, security, risk | design, reason, acros, protect, asset, external, actor, component |

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Gold rank among listed candidates: 2
- Instruction used for scoring: Review this single API handler for concrete code-level security vulnerabilities and fixes tied to the implementation. It accepts `redirectUrl` from the request body, checks the current user, updates the user's profile, and redirects. Focus on handler-level flaws such as open redirects, unsafe validation, and incorrect access checks in this function.
- Positive-fit instruction after negation cleanup: Review this single API handler for concrete code-level security vulnerabilities and fixes tied to the implementation. It accepts `redirectUrl` from the request body, checks the current user, updates the user's profile, and redirects. Focus on handler-level flaws such as open redirects, unsafe validation, and incorrect access checks in this function.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `auth-flow-reviewer` | 0.4784 | 0.4784 | 0.5530 | check, review, handler, security, user, open, acces | check, redirect, review, api, handler, concrete, code-level, security |
| `security-code-reviewer` | 0.4722 | 0.4722 | 0.1849 | check, redirect, review, handler, concrete, code-level, security, vulnerabilitie | review, security |
| `security-threat-modeler` | 0.3758 | 0.3758 | 0.2879 | check, review, concrete, code-level, security, implementation, user, open | check, review, concrete, vulnerabilitie |
| `code-reviewer` | 0.1449 | 0.1449 | 0.2401 | check, review, fixe, implementation, request, user | check, review, request |

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check the risk of adding this new npm package. It has a broad dependency tree, a postinstall script, and the lockfile pulls in several old transitive packages. I need a dependency and supply-chain risk assessment.
- Positive-fit instruction after negation cleanup: Check the risk of adding this new npm package. It has a broad dependency tree, a postinstall script, and the lockfile pulls in several old transitive packages. I need a dependency and supply-chain risk assessment.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `dependency-risk-auditor` | 0.5560 | 0.5560 | 0.2297 | risk, package, dependency, check, script, lockfile, transitive, supply-chain | risk, broad |
| `secret-leak-scanner` | 0.2842 | 0.2842 | 0.3944 | risk, dependency, check | risk, dependency, assessment |
| `security-code-reviewer` | 0.2389 | 0.2389 | 0.3992 | risk, dependency, check | risk, dependency, supply-chain |
| `ci-failure-debugger` | 0.1084 | 0.1084 | 0.1112 | dependency, check, broad | check, new |

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Look at this diff and tell me if I accidentally exposed anything sensitive: it adds `.env.example`, updates a deployment log, and includes strings that look like `sk_live_...`, a database URL, and a webhook signing secret.
- Positive-fit instruction after negation cleanup: Look at this diff and tell me if I accidentally exposed anything sensitive: it adds `.env.example`, updates a deployment log, and includes strings that look like `sk_live_...`, a database URL, and a webhook signing secret.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `secret-leak-scanner` | 0.4813 | 0.4813 | 0.2507 | diff, expos, sensitive, env, log, string, secret | secret |
| `security-code-reviewer` | 0.3124 | 0.3124 | 0.2643 | diff, sensitive, secret | look, secret |
| `dependency-risk-auditor` | 0.3050 | 0.3050 | 0.2393 | diff, update, secret | secret |
| `privacy-risk-reviewer` | 0.2612 | 0.2612 | 0.3409 | diff, expos, sensitive, secret | secret |

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Check whether this account-access change is safe. Users can refresh expired sessions, reset passwords by email link, and switch between workspace roles. I care about bypasses, stale permissions, and privilege escalation.
- Positive-fit instruction after negation cleanup: Check whether this account-access change is safe. Users can refresh expired sessions, reset passwords by email link, and switch between workspace roles. I care about bypasses, stale permissions, and privilege escalation.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `auth-flow-reviewer` | 0.4920 | 0.4920 | 0.2814 | check, whether, account-acces, safe, user, refresh, session, reset | check |
| `privacy-risk-reviewer` | 0.2812 | 0.2812 | 0.2523 | check, whether, user | - |
| `security-threat-modeler` | 0.1840 | 0.1840 | 0.1342 | check, whether, user | check |
| `security-code-reviewer` | 0.1747 | 0.1747 | 0.1128 | check, whether, user, permission | - |

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Assess the data-protection concerns in this analytics change. We want to log search queries, account region, user role, clicked filters, and partial email domains for 18 months so the product team can study usage patterns.
- Positive-fit instruction after negation cleanup: Assess the data-protection concerns in this analytics change. We want to log search queries, account region, user role, clicked filters, and partial email domains for 18 months so the product team can study usage patterns.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `privacy-risk-reviewer` | 0.5598 | 0.5598 | 0.4018 | concern, analytic, user | concern |
| `secret-leak-scanner` | 0.3754 | 0.3754 | 0.2580 | concern, log, user | - |
| `auth-flow-reviewer` | 0.3281 | 0.3281 | 0.2919 | concern, user, role | concern |
| `security-threat-modeler` | 0.2962 | 0.2962 | 0.2672 | concern, user | - |

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Before I make anything new, search my existing capability library, shortlist available entries, assess fit and confidence, and decide whether one of them covers a workflow for turning messy meeting notes into action items and follow-up messages. I only want a reuse recommendation, not creation.
- Positive-fit instruction after negation cleanup: Before I make anything new, search my existing capability library, shortlist available entries, assess fit and confidence, and decide whether one of them covers a workflow for turning messy meeting notes into action items and follow-up messages. I only want a reuse recommendation, .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-finder` | 0.4668 | 0.4668 | 0.2712 | anyth, new, search, exist, library, shortlist, available, fit | new, exist |
| `skill-editor` | 0.4466 | 0.4466 | 0.4732 | new, exist, library, whether, workflow | exist, capability, shortlist, entrie, workflow, reuse, recommendation |
| `skill-creator` | 0.4302 | 0.4302 | 0.4487 | new, exist, capability, library, decide, whether, workflow, note | new, exist, capability, shortlist, entrie, fit, confidence, whether |
| `skill-installer` | 0.2892 | 0.2892 | 0.3189 | exist, library, available, whether | new, search |

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I found an existing spreadsheet-analysis capability in a public catalog and want it added to my active local library. Please fetch or prepare the package, verify the expected files, and report the source, local path, setup result, and any activation caveats.
- Positive-fit instruction after negation cleanup: I found an existing spreadsheet-analysis capability in a public catalog and want it added to my active local library. Please fetch or prepare the package, verify the expected files, and report the source, local path, setup result, and any activation caveats.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-installer` | 0.2828 | 0.2828 | 0.2024 | local, exist, public, catalog, active, library, fetch, prepare | - |
| `skill-packager` | 0.2662 | 0.2662 | 0.3362 | exist, public, library, prepare, package, check, file, report | local, capability, public, catalog, active, library, fetch, package |
| `skill-finder` | 0.2253 | 0.2253 | 0.1062 | exist, public, library, package | exist |
| `skill-creator` | 0.1193 | 0.1193 | 0.1846 | exist, capability, public, add, library, package, check, expect | exist, capability |

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Create a new atomic skill for a repeated workflow: I often need to turn supervisor meeting notes into a thesis action list with owners, deadlines, and open questions. There is no existing skill for this exact workflow.
- Positive-fit instruction after negation cleanup: Create a new atomic skill for a repeated workflow: I often need to turn supervisor meeting notes into a thesis action list with owners, deadlines, and open questions. There is .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-creator` | 0.5579 | 0.5579 | 0.4235 | create, new, atomic, skill, repeat, workflow, note | skill, new, exist |
| `skill-editor` | 0.4885 | 0.4885 | 0.5040 | create, new, skill, workflow | skill, workflow, exist |
| `skill-finder` | 0.4231 | 0.4231 | 0.4201 | create, new, skill, workflow, note | skill, new, exist |
| `skill-packager` | 0.2860 | 0.2860 | 0.3527 | create, skill | skill |

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: This existing skill's description is too broad and it keeps triggering for document summaries when it should only handle structured field extraction. Please revise the skill so its selection boundary is clearer.
- Positive-fit instruction after negation cleanup: This existing skill's description is too broad and it keeps triggering for document summaries when it should only handle structured field extraction. Please revise the skill so its selection boundary is clearer.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-editor` | 0.4990 | 0.4990 | 0.3763 | exist, skill', description, broad, keep, summary, revise, skill | exist, skill |
| `skill-creator` | 0.4096 | 0.4096 | 0.3294 | exist, skill', description, broad, keep, trigger, only, skill | exist, skill |
| `skill-evaluator` | 0.3735 | 0.3735 | 0.3601 | exist, skill', description, trigger, structur, skill, selection, boundary | skill |
| `skill-packager` | 0.2467 | 0.2467 | 0.2968 | exist, keep, only, structur, skill | skill', skill |

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Test whether my `reply-polisher` skill actually triggers only when there is already a draft reply. I want an evaluation with realistic near-boundary prompts before deciding whether to edit it.
- Positive-fit instruction after negation cleanup: Test whether my `reply-polisher` skill actually triggers only when there is already a draft reply. I want an evaluation with realistic near-boundary prompts before deciding whether to edit it.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-evaluator` | 0.4638 | 0.4638 | 0.3337 | whether, test, skill, trigger, evaluation, realistic, near-boundary, prompt | test, skill, edit |
| `skill-finder` | 0.3547 | 0.3547 | 0.3323 | whether, skill, already, edit | test, skill, edit |
| `skill-editor` | 0.3418 | 0.3418 | 0.2127 | whether, skill, edit | skill, edit |
| `skill-creator` | 0.3047 | 0.3047 | 0.2727 | whether, skill, trigger, only, edit | whether, test, skill, already, edit |

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Gold rank among listed candidates: 1
- Instruction used for scoring: I finished an existing `paper-summariser` skill and want to share it with someone else. Check the folder shape, metadata, resource links, and unnecessary files so it is package-ready.
- Positive-fit instruction after negation cleanup: I finished an existing `paper-summariser` skill and want to share it with someone else. Check the folder shape, metadata, resource links, and unnecessary files so it is package-ready.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-packager` | 0.4764 | 0.4764 | 0.3726 | exist, skill, share, check, folder, shape, metadata, resource | skill, check, file |
| `skill-installer` | 0.3472 | 0.3472 | 0.2584 | exist, skill, check, file | skill |
| `skill-creator` | 0.3109 | 0.3109 | 0.2549 | exist, skill, check, folder, resource | exist, skill |
| `skill-editor` | 0.2947 | 0.2947 | 0.2774 | exist, skill, metadata, resource | exist, skill |

### `skill_representation_analysis_p1_skill_field_auditor`

- Family: `skill_representation_analysis`
- Gold skill: `skill-field-auditor`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Audit public_skill_sample.md and extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and missing fields.
- Positive-fit instruction after negation cleanup: Audit public_skill_sample.md and extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and missing fields.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-field-auditor` | 0.7405 | 0.7405 | 0.5055 | audit, extract, trigger, input, output, workflow, dependencie, resource | - |
| `skill-installer-wrapper` | 0.5252 | 0.5252 | 0.4822 | output, dependencie, resource, miss | audit, field |
| `skill-authoring-guide` | 0.5202 | 0.5202 | 0.5402 | trigger, output, workflow, resource, example | audit |
| `skill-router-policy-designer` | 0.3467 | 0.3467 | 0.5449 | field | - |
| `skill-hierarchy-flattener` | 0.2318 | 0.2318 | 0.4681 | output, resource | - |

### `skill_representation_analysis_p2_skill_authoring_guide`

- Family: `skill_representation_analysis`
- Gold skill: `skill-authoring-guide`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Draft a new atomic skill for reviewing database migrations, including triggers, boundaries, workflow, dependencies, and examples. Do not just audit an existing skill.
- Positive-fit instruction after negation cleanup: Draft a new atomic skill for reviewing database migrations, including triggers, boundaries, workflow, dependencies, and examples. .

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-authoring-guide` | 0.4653 | 0.4653 | 0.5304 | draft, atomic, skill, trigger, boundarie, workflow, example | skill, audit, exist |
| `skill-installer-wrapper` | 0.4359 | 0.4359 | 0.3088 | skill, dependencie | audit |
| `skill-field-auditor` | 0.4164 | 0.4164 | 0.4861 | skill, includ, trigger, workflow, dependencie, example | skill, new |
| `skill-hierarchy-flattener` | 0.3848 | 0.3848 | 0.5625 | atomic, skill, boundarie | skill, new |
| `skill-router-policy-designer` | 0.3586 | 0.3586 | 0.4443 | skill | skill |

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Family: `skill_representation_analysis`
- Gold skill: `skill-router-policy-designer`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Design a two-stage skill routing policy for a 2000-skill library, including candidate budget, representation fields, reranking, and fallback behavior.
- Positive-fit instruction after negation cleanup: Design a two-stage skill routing policy for a 2000-skill library, including candidate budget, representation fields, reranking, and fallback behavior.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-router-policy-designer` | 0.8571 | 0.8571 | 0.4475 | design, skill, rout, policy, library, candidate, budget, representation | skill |
| `skill-hierarchy-flattener` | 0.5525 | 0.5525 | 0.4556 | skill, rout | skill |
| `skill-authoring-guide` | 0.5450 | 0.5450 | 0.5773 | skill, rout | design, skill, policy |
| `skill-installer-wrapper` | 0.4215 | 0.4215 | 0.2473 | skill | design, policy, field |
| `skill-field-auditor` | 0.4124 | 0.4124 | 0.4436 | skill, includ, representation, field | skill |

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Family: `skill_representation_analysis`
- Gold skill: `skill-hierarchy-flattener`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Decompose the broad all-in-one skill in hierarchical_skill.md into atomic standalone skill definitions while preserving cross-references, common resources, and routing boundaries.
- Positive-fit instruction after negation cleanup: Decompose the broad all-in-one skill in hierarchical_skill.md into atomic standalone skill definitions while preserving cross-references, common resources, and routing boundaries.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-hierarchy-flattener` | 0.7983 | 0.7983 | 0.5689 | skill, broad, atomic, definition, preserv, resource, rout, boundarie | skill |
| `skill-authoring-guide` | 0.6706 | 0.6706 | 0.5470 | skill, broad, atomic, resource, rout, boundarie | skill |
| `skill-installer-wrapper` | 0.5905 | 0.5905 | 0.1149 | skill, preserv, resource | - |
| `skill-router-policy-designer` | 0.5894 | 0.5894 | 0.6224 | skill, rout | skill |
| `skill-field-auditor` | 0.5108 | 0.5108 | 0.5265 | skill, resource | skill |

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Family: `skill_representation_analysis`
- Gold skill: `skill-installer-wrapper`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Install the public skill from  into the local library, preserving resources and source metadata.
- Positive-fit instruction after negation cleanup: Install the public skill from into the local library, preserving resources and source metadata.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-installer-wrapper` | 0.6280 | 0.6280 | 0.2183 | install, public, skill, local, preserv, resource, metadata | install |
| `skill-authoring-guide` | 0.4197 | 0.4197 | 0.4639 | skill, local, resource | install, skill |
| `skill-field-auditor` | 0.3924 | 0.3924 | 0.5526 | skill, resource | install, public, skill |
| `skill-hierarchy-flattener` | 0.2693 | 0.2693 | 0.5168 | skill, preserv, resource | install, skill |
| `skill-router-policy-designer` | 0.2586 | 0.2586 | 0.6965 | skill, library | install, public, skill |

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Family: `skill_representation_analysis`
- Gold skill: `skill-benchmark-evaluator`
- Gold rank among listed candidates: 1
- Instruction used for scoring: Evaluate retrieval_results.json with top-1, top-5, MRR, non-core false positives, and failure-mode categories.
- Positive-fit instruction after negation cleanup: Evaluate retrieval_results.json with top-1, top-5, MRR, non-core false positives, and failure-mode categories.

| Candidate | Fit score | Positive | Boundary | Shared positive terms | Shared boundary terms |
|---|---:|---:|---:|---|---|
| `skill-benchmark-evaluator` | 0.5330 | 0.5330 | 0.1273 | evaluate, mrr, false, positive | - |
| `skill-field-auditor` | 0.2000 | 0.2000 | 0.2959 | - | - |
| `skill-router-policy-designer` | 0.1815 | 0.1815 | 0.0722 | - | - |
| `skill-authoring-guide` | 0.1332 | 0.1332 | 0.1118 | - | - |
| `skill-hierarchy-flattener` | 0.1332 | 0.1332 | 0.3253 | - | - |

