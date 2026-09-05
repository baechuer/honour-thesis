# Semantic Confusability Report

This report implements Step 3 of the benchmark rubric: listed alternatives and recorded acceptable equivalents should be semantically plausible neighbours, not random unrelated distractors.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.

## Overall Status

- Step 3 status: **PASS**
- Prompts with at least two plausible listed alternatives: 243/245 (99.2%)
- Gold/alternative pairs marked plausible: 666/830 (80.2%)
- Gold skill ranked top-1 among all skills by this backend: 104/245 (42.4%)

Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, whose skill card is similar to the gold skill card, or whose acceptable-equivalent status has already been manually recorded.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |
|---|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 4/6 |
| api_mcp_tooling | 6 | 6/6 | 3/6 |
| browser_web_automation | 6 | 6/6 | 2/6 |
| code_github_workflow | 6 | 6/6 | 1/6 |
| controlled_expansion_clear | 20 | 20/20 | 9/20 |
| data_spreadsheet | 7 | 7/7 | 1/7 |
| deployment_browser_qa | 6 | 6/6 | 2/6 |
| documents_files | 7 | 7/7 | 1/7 |
| github_ci_maintenance | 6 | 6/6 | 3/6 |
| huggingface_ml_workflows | 6 | 6/6 | 3/6 |
| implicit_field_stress | 10 | 10/10 | 2/10 |
| metrics_observability | 6 | 4/6 | 3/6 |
| news_monitoring | 5 | 5/5 | 3/5 |
| observability_reliability | 6 | 6/6 | 5/6 |
| office_artifact_workflows | 6 | 6/6 | 5/6 |
| office_business_automation | 6 | 6/6 | 5/6 |
| pdf_document_operations | 6 | 6/6 | 5/6 |
| planning_meetings | 5 | 5/5 | 3/5 |
| public_like_extra_controlled | 24 | 24/24 | 3/24 |
| public_style_controlled | 64 | 64/64 | 23/64 |
| reading_research | 8 | 8/8 | 5/8 |
| reply_messaging | 5 | 5/5 | 4/5 |
| security_appsec | 6 | 6/6 | 4/6 |
| skill_lifecycle | 6 | 6/6 | 1/6 |
| skill_representation_analysis | 6 | 6/6 | 4/6 |

## Weak Semantic-Confusability Prompts

| Prompt | Gold | Plausible alternatives | Gold all-skill rank |
|---|---|---:|---:|
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 1 | 1 |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 0 | 1 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | no | 0.6807 | 0.4831 | 0.5703 | yes | api, pagination | endpoint, pagination |
| `webhook-contract-planner` | no | 0.6807 | 0.3211 | 0.4641 | no | contract, behavior | contract, behavior |
| `architecture-boundary-reviewer` | no | 0.6807 | 0.3932 | 0.6497 | yes | review | review |

Top similarity neighbours: `openapi-contract-reviewer` (0.681), `openapi-contract-tester` (0.541), `external-api-integration-planner` (0.483), `api-ops-summary-writer` (0.472), `api-integration-planner` (0.455)

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | no | 0.4263 | 0.3312 | 0.5703 | yes | endpoint, behavior | endpoint, pagination |
| `webhook-contract-planner` | no | 0.4263 | 0.2865 | 0.5934 | yes | behavior, verification | payload, retrie |
| `service-dependency-mapper` | no | 0.4263 | 0.2836 | 0.4545 | no | - | failure |

Top similarity neighbours: `api-integration-planner` (0.479), `auth-flow-reviewer` (0.440), `external-api-integration-planner` (0.426), `auth-flow-integrator` (0.422), `public-office-subscription-management` (0.396)

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | no | 0.4632 | 0.3154 | 0.5934 | yes | - | payload, retrie |
| `openapi-contract-reviewer` | no | 0.4632 | 0.3279 | 0.4641 | no | behavior | contract, behavior |
| `public-office-webhook-automation` | no | 0.4632 | 0.3008 | 0.6091 | yes | event | event |
| `public-api-design-principles` | no | 0.4632 | 0.3203 | 0.4039 | no | design | design |

Top similarity neighbours: `webhook-contract-planner` (0.463), `events-ops-acceptance-test-builder` (0.423), `events-ops-intake-classifier` (0.420), `invoice-payment-checker` (0.398), `customer-success-ops-intake-classifier` (0.396)

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `service-dependency-mapper` | no | 0.7248 | 0.4438 | 0.4242 | no | - | service |
| `openapi-contract-reviewer` | no | 0.7248 | 0.4497 | 0.6497 | yes | review | review |
| `database-migration-risk-assessor` | no | 0.7248 | 0.4403 | 0.5922 | yes | - | risk |

Top similarity neighbours: `architecture-boundary-reviewer` (0.725), `public-architecture-patterns` (0.511), `public-addy-agent-api-and-interface-design` (0.485), `public-mattpocock-improve-codebase-architecture` (0.469), `openapi-contract-reviewer` (0.450)

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | no | 0.6735 | 0.3530 | 0.5922 | yes | risk | risk |
| `service-dependency-mapper` | no | 0.6735 | 0.2395 | 0.3664 | no | - | data |
| `public-office-database-sync` | no | 0.6735 | 0.4358 | 0.4213 | no | - | database, migration, data |
| `public-architecture-patterns` | no | 0.6735 | 0.2024 | 0.2951 | no | - | - |
| `deployment-rollback-planner` | no | 0.6735 | 0.5784 | 0.5408 | yes | plan, compatibility, rollback, verification | plan, data, compatibility, rollback, deployment, verification |
| `database-backup-planner` | no | 0.6735 | 0.4688 | 0.5547 | yes | plan, verification | database, plan, verification |

Top similarity neighbours: `database-migration-risk-assessor` (0.673), `migration-risk-auditor` (0.616), `deployment-rollback-planner` (0.578), `public-oh-my-changelog-maintenance` (0.498), `public-office-subscription-management` (0.487)

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 228

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | no | 0.3585 | 0.3129 | 0.4242 | yes | service, direction | service |
| `external-api-integration-planner` | no | 0.3585 | 0.2769 | 0.4545 | no | failure | failure |
| `public-architecture-patterns` | no | 0.3585 | 0.2497 | 0.3361 | no | - | - |
| `public-api-design-principles` | no | 0.3585 | 0.2885 | 0.3776 | yes | - | - |

Top similarity neighbours: `public-swebench-distributed-tracing` (0.505), `distributed-trace-investigator` (0.479), `customer-feedback-analyser` (0.477), `analytics-ops-compliance-checker` (0.474), `dashboard-ops-compliance-checker` (0.468)

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Family: `api_mcp_tooling`
- Gold skill: `rest-api-contract-designer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `mcp-server-builder` | no | 0.4639 | 0.4944 | 0.5983 | yes | resource, example, mcp | resource, schema |
| `webhook-integration-planner` | no | 0.4639 | 0.4413 | 0.4814 | yes | subscription | - |
| `auth-flow-integrator` | no | 0.4639 | 0.3778 | 0.4651 | no | - | api |
| `api-documentation-writer` | no | 0.4639 | 0.3950 | 0.6470 | yes | includ, error, example | api, error |

Top similarity neighbours: `mcp-server-builder` (0.494), `public-anthropic-mcp-builder` (0.469), `rest-api-contract-designer` (0.464), `public-swebench-mcp-builder` (0.445), `webhook-integration-planner` (0.441)

### `api_mcp_tooling_p2_mcp_server_builder`

- Family: `api_mcp_tooling`
- Gold skill: `mcp-server-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | no | 0.4716 | 0.4688 | 0.5983 | yes | design, schema, resource, rest, api | resource, schema |
| `webhook-integration-planner` | no | 0.4716 | 0.3143 | 0.4079 | no | - | - |
| `auth-flow-integrator` | no | 0.4716 | 0.3316 | 0.5342 | yes | api | - |
| `api-documentation-writer` | no | 0.4716 | 0.3305 | 0.5697 | yes | api | example |

Top similarity neighbours: `mcp-server-builder` (0.472), `rest-api-contract-designer` (0.469), `public-anthropic-mcp-builder` (0.431), `api-security-threat-reviewer` (0.417), `public-swebench-mcp-builder` (0.407)

### `api_mcp_tooling_p3_webhook_integration_planner`

- Family: `api_mcp_tooling`
- Gold skill: `webhook-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-webhook-automation` | no | 0.6572 | 0.7009 | 0.6843 | yes | event, integration, api | event |
| `webhook-contract-planner` | no | 0.6572 | 0.6442 | 0.8732 | yes | event, webhook, design, contract, signature, idempotency, behavior, order | webhook, event, signature, verification, idempotency, retrie, order, dead-letter |
| `rest-api-contract-designer` | no | 0.6572 | 0.3112 | 0.4814 | no | design, schema, behavior, endpoint, api | - |
| `mcp-server-builder` | no | 0.6572 | 0.2288 | 0.4079 | no | schema | - |

Top similarity neighbours: `public-office-webhook-automation` (0.701), `webhook-integration-planner` (0.657), `webhook-contract-planner` (0.644), `webhook-setup-planner` (0.644), `public-swebench-gitops-workflow` (0.443)

### `api_mcp_tooling_p4_auth_flow_integrator`

- Family: `api_mcp_tooling`
- Gold skill: `auth-flow-integrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 9

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | no | 0.4306 | 0.2437 | 0.4651 | no | - | api |
| `mcp-server-builder` | no | 0.4306 | 0.1473 | 0.5342 | yes | - | - |
| `webhook-integration-planner` | no | 0.4306 | 0.5706 | 0.4428 | yes | webhook | keys |
| `api-documentation-writer` | no | 0.4306 | 0.2529 | 0.5531 | yes | - | api |

Top similarity neighbours: `webhook-setup-planner` (0.637), `public-office-webhook-automation` (0.606), `webhook-integration-planner` (0.571), `api-integration-planner` (0.507), `webhook-contract-planner` (0.506)

### `api_mcp_tooling_p5_api_documentation_writer`

- Family: `api_mcp_tooling`
- Gold skill: `api-documentation-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | no | 0.5326 | 0.3091 | 0.6470 | yes | api, error | api, error |
| `mcp-server-builder` | no | 0.5326 | 0.1589 | 0.5697 | yes | example | example |
| `webhook-integration-planner` | no | 0.5326 | 0.2725 | 0.4905 | no | - | - |
| `auth-flow-integrator` | no | 0.5326 | 0.2664 | 0.5531 | yes | api | api |

Top similarity neighbours: `api-documentation-writer` (0.533), `public-office-stripe-payments` (0.417), `public-office-quickbooks-automation` (0.403), `invoice-payment-checker` (0.365), `openapi-contract-reviewer` (0.347)

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Family: `api_mcp_tooling`
- Gold skill: `api-security-threat-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-security-threat-model` | no | 0.6196 | 0.3646 | 0.4402 | no | abuse | review, design, abuse |
| `public-openai-security-best-practices` | no | 0.6196 | 0.3898 | 0.4099 | no | security | review |
| `security-threat-modeler` | no | 0.6196 | 0.3398 | 0.4828 | no | data, abuse, security | design, data, abuse, case |
| `rest-api-contract-designer` | no | 0.6196 | 0.2638 | 0.5537 | yes | api | api, design |
| `api-ops-risk-reviewer` | no | 0.6196 | 0.5706 | 0.6985 | yes | api, risk, security | review, api |
| `privacy-risk-reviewer` | no | 0.6196 | 0.5619 | 0.6276 | yes | data, exposure, risk | review, data, exposure |

Top similarity neighbours: `api-security-threat-reviewer` (0.620), `api-ops-risk-reviewer` (0.571), `privacy-risk-reviewer` (0.562), `auth-flow-reviewer` (0.530), `identity-ops-risk-reviewer` (0.511)

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.4183 | 0.3207 | 0.6353 | yes | interaction, test | web, interaction, test |
| `web-data-extractor` | no | 0.4183 | 0.0477 | 0.5152 | yes | page | page, web |
| `frontend-debugger` | no | 0.4183 | 0.2490 | 0.4908 | no | state, observation | state |

Top similarity neighbours: `visual-regression-checker` (0.445), `web-page-snapshotter` (0.418), `psc-visual-screenshot-reviewer` (0.415), `psc-devtools-runtime-diagnoser` (0.387), `psc-playwright-regression-suite` (0.383)

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.3930 | 0.4330 | 0.6349 | yes | report, flow, test | interaction, flow |
| `web-page-snapshotter` | no | 0.3930 | 0.2713 | 0.5743 | yes | test | perform, interaction |
| `frontend-debugger` | no | 0.3930 | 0.2425 | 0.4170 | no | - | - |

Top similarity neighbours: `web-ui-tester` (0.433), `identity-ops-acceptance-test-builder` (0.419), `web-form-filler` (0.393), `marketing-ops-acceptance-test-builder` (0.390), `web-ops-acceptance-test-builder` (0.388)

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 123

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-form-filler` | no | 0.2394 | 0.1152 | 0.6349 | yes | - | interaction, flow |
| `frontend-debugger` | no | 0.2394 | 0.1624 | 0.6468 | yes | behavior | behavior |
| `web-page-snapshotter` | no | 0.2394 | 0.1396 | 0.6353 | yes | test, page | test, web, interaction |

Top similarity neighbours: `email-ops-acceptance-test-builder` (0.380), `facilities-ops-acceptance-test-builder` (0.375), `contract-ops-acceptance-test-builder` (0.360), `grant-ops-acceptance-test-builder` (0.356), `crm-ops-acceptance-test-builder` (0.356)

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-page-snapshotter` | no | 0.4932 | 0.2532 | 0.5152 | yes | page, screenshot | web, page |
| `web-ui-tester` | no | 0.4932 | 0.0278 | 0.4455 | no | - | web |
| `frontend-debugger` | no | 0.4932 | -0.0330 | 0.2881 | no | - | - |
| `product-ops-field-extractor` | no | 0.4932 | 0.4253 | 0.3555 | yes | product, extract, structur | extract, structur |
| `document-extractor` | no | 0.4932 | 0.3336 | 0.5551 | yes | extract, structur | extract, structur, information |

Top similarity neighbours: `web-data-extractor` (0.493), `pdf-layout-table-extractor` (0.443), `product-ops-field-extractor` (0.425), `receipt-extractor` (0.377), `implicit-pdf-table-reconstructor` (0.373)

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.3846 | 0.1565 | 0.6468 | yes | - | behavior |
| `web-page-snapshotter` | no | 0.3846 | 0.1277 | 0.4908 | no | page, open, evidence, inspect, state | state |
| `code-reviewer` | no | 0.3846 | 0.0709 | 0.1042 | no | code | code |
| `playwright-flow-debugger` | no | 0.3846 | 0.2784 | 0.5379 | yes | console, evidence | broken, console, network |
| `psc-devtools-runtime-diagnoser` | no | 0.3846 | 0.1788 | 0.5294 | yes | page, console, evidence, state | diagnose, broken, console, error, network, state, dom, clue |
| `web-ops-failure-diagnoser` | no | 0.3846 | 0.2535 | 0.6354 | yes | - | diagnose |

Top similarity neighbours: `frontend-debugger` (0.385), `api-ops-failure-diagnoser` (0.329), `public-oh-my-game-performance-profiler` (0.312), `publishing-ops-failure-diagnoser` (0.282), `property-ops-failure-diagnoser` (0.281)

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.4781 | 0.2751 | 0.6539 | yes | whether | check, web |
| `frontend-debugger` | no | 0.4781 | 0.2559 | 0.5092 | yes | error | - |
| `web-page-snapshotter` | no | 0.4781 | 0.2410 | 0.5908 | yes | - | web |

Top similarity neighbours: `accessibility-interaction-auditor` (0.519), `accessibility-checker` (0.478), `psc-accessibility-interaction-auditor` (0.469), `public-addy-web-accessibility` (0.438), `meeting-notes-action-extractor` (0.342)

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | no | 0.3028 | 0.1964 | 0.8192 | yes | review, risk | review, file, risk |
| `review-comment-resolver` | no | 0.3028 | 0.2309 | 0.7433 | yes | change, review | review, code, change |
| `ci-failure-debugger` | no | 0.3028 | 0.1891 | 0.5839 | yes | test | test |

Top similarity neighbours: `public-swebench-springboot-tdd` (0.324), `email-ops-acceptance-test-builder` (0.318), `code-reviewer` (0.303), `localization-ops-acceptance-test-builder` (0.300), `repo-ops-acceptance-test-builder` (0.282)

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `code-reviewer` | no | 0.4772 | 0.3537 | 0.8192 | yes | review, change, test | review, file, risk |
| `review-comment-resolver` | no | 0.4772 | 0.3178 | 0.7200 | yes | review, request, change | review, request |
| `ci-failure-debugger` | no | 0.4772 | 0.3272 | 0.5825 | yes | test | check |

Top similarity neighbours: `auth-flow-reviewer` (0.511), `pr-review-comment-resolver` (0.499), `pr-reviewer` (0.477), `auth-flow-integrator` (0.432), `pr-description-writer` (0.431)

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | no | 0.4949 | 0.4239 | 0.7200 | yes | review, request | review, request |
| `code-reviewer` | no | 0.4949 | 0.3743 | 0.7433 | yes | review, test, code, change, miss, implementation | review, code, change |
| `ci-failure-debugger` | no | 0.4949 | 0.4165 | 0.5068 | yes | test, need | - |

Top similarity neighbours: `pr-review-comment-resolver` (0.555), `review-comment-resolver` (0.495), `resilience-pattern-reviewer` (0.463), `repo-code-reviewer` (0.430), `pr-reviewer` (0.424)

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `code-reviewer` | no | 0.4968 | 0.1155 | 0.5839 | yes | commit, test, change | test |
| `pr-reviewer` | no | 0.4968 | 0.1319 | 0.5825 | yes | - | check |
| `review-comment-resolver` | no | 0.4968 | 0.1175 | 0.5068 | yes | change | - |

Top similarity neighbours: `ci-failure-debugger` (0.497), `ci-log-root-cause-debugger` (0.467), `psc-ci-log-first-failure-reader` (0.421), `api-ops-failure-diagnoser` (0.340), `implicit-ci-failure-reader` (0.330)

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `release-note-writer` | no | 0.4319 | 0.4941 | 0.6622 | yes | change, turn, complet, user-fac, release, note | change, complet |
| `pr-reviewer` | no | 0.4319 | 0.2715 | 0.5997 | yes | - | - |
| `code-reviewer` | no | 0.4319 | 0.3001 | 0.6328 | yes | change, test | change |

Top similarity neighbours: `release-changelog-generator` (0.547), `psc-release-communication-packager` (0.501), `release-note-writer` (0.494), `public-oh-my-changelog-maintenance` (0.482), `public-swebench-changelog-automation` (0.475)

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 186

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `changelog-writer` | no | 0.2149 | 0.0907 | 0.6622 | yes | change | complet, change |
| `pr-reviewer` | no | 0.2149 | 0.0435 | 0.5767 | yes | request | chang |
| `code-reviewer` | no | 0.2149 | 0.0676 | 0.6242 | yes | change | change |

Top similarity neighbours: `identity-ops-failure-diagnoser` (0.397), `auth-flow-reviewer` (0.394), `identity-ops-timeline-builder` (0.351), `security-ops-failure-diagnoser` (0.339), `identity-ops-monitoring-plan-builder` (0.336)

### `clear_exp_p01_openapi_backward_compatibility`

- Family: `controlled_expansion_clear`
- Gold skill: `openapi-contract-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | no | 0.7448 | 0.5676 | 0.5703 | yes | pagination, plan, api | endpoint, pagination |
| `webhook-contract-planner` | no | 0.7448 | 0.3468 | 0.4641 | no | - | contract, behavior |
| `architecture-boundary-reviewer` | no | 0.7448 | 0.4595 | 0.6497 | yes | review, risk | review |

Top similarity neighbours: `openapi-contract-reviewer` (0.745), `openapi-contract-tester` (0.618), `external-api-integration-planner` (0.568), `api-ops-summary-writer` (0.533), `api-ops-scenario-planner` (0.526)

### `clear_exp_p02_external_api_rate_limit_plan`

- Family: `controlled_expansion_clear`
- Gold skill: `external-api-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | no | 0.5561 | 0.6324 | 0.5703 | yes | auth, endpoint, pagination, review, openapi, contract | endpoint, pagination |
| `webhook-contract-planner` | no | 0.5561 | 0.3676 | 0.5934 | yes | retrie, idempotency, verification, contract | payload, retrie |
| `service-dependency-mapper` | no | 0.5561 | 0.3637 | 0.4545 | no | call, contract | failure |

Top similarity neighbours: `openapi-contract-reviewer` (0.632), `api-integration-planner` (0.583), `external-api-integration-planner` (0.556), `openapi-contract-tester` (0.498), `auth-flow-integrator` (0.487)

### `clear_exp_p03_webhook_retry_contract`

- Family: `controlled_expansion_clear`
- Gold skill: `webhook-contract-planner`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | no | 0.7833 | 0.5051 | 0.5934 | yes | handl, api, integration | payload, retrie |
| `openapi-contract-reviewer` | no | 0.7833 | 0.4386 | 0.4641 | no | contract, behavior | contract, behavior |
| `architecture-boundary-reviewer` | no | 0.7833 | 0.3019 | 0.3734 | no | - | - |
| `webhook-integration-planner` | no | 0.7833 | 0.7497 | 0.8732 | yes | subscription, webhook, event, signature, verification, idempotency, keys, dead-letter | webhook, event, signature, verification, idempotency, retrie, order, dead-letter |
| `webhook-setup-planner` | no | 0.7833 | 0.6650 | 0.7875 | yes | webhook, event, signature, verification, idempotency, retry, behavior, handl | webhook, event, selection, signature, verification, idempotency, behavior |
| `public-office-webhook-automation` | no | 0.7833 | 0.6158 | 0.6091 | yes | event, api, integration | event |

Top similarity neighbours: `webhook-contract-planner` (0.783), `webhook-integration-planner` (0.750), `webhook-setup-planner` (0.665), `public-office-webhook-automation` (0.616), `external-api-integration-planner` (0.505)

### `clear_exp_p04_visual_snapshot_only`

- Family: `controlled_expansion_clear`
- Gold skill: `web-page-snapshotter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.4450 | 0.3509 | 0.6353 | yes | test, behavior | web, interaction, test |
| `web-data-extractor` | no | 0.4450 | 0.1410 | 0.5152 | yes | page | page, web |
| `frontend-debugger` | no | 0.4450 | 0.3076 | 0.4908 | no | state, dom, behavior, code | state |

Top similarity neighbours: `web-page-snapshotter` (0.445), `dashboard-ops-acceptance-test-builder` (0.422), `dashboard-ops-risk-reviewer` (0.413), `psc-visual-screenshot-reviewer` (0.407), `grafana-dashboard-builder` (0.402)

### `clear_exp_p05_form_submission_delegate`

- Family: `controlled_expansion_clear`
- Gold skill: `web-form-filler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 742

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | no | 0.1954 | 0.2122 | 0.6349 | yes | regression, test | interaction, flow |
| `web-page-snapshotter` | no | 0.1954 | 0.1132 | 0.5743 | yes | test, page | perform, interaction |
| `web-data-extractor` | no | 0.1954 | 0.1342 | 0.5444 | yes | page | - |

Top similarity neighbours: `vendor-ops-acceptance-test-builder` (0.487), `vendor-ops-compliance-checker` (0.430), `procurement-ops-acceptance-test-builder` (0.425), `vendor-ops-risk-reviewer` (0.413), `vendor-ops-quality-auditor` (0.408)

### `clear_exp_p06_ui_regression_pass_fail`

- Family: `controlled_expansion_clear`
- Gold skill: `web-ui-tester`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 174

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `web-form-filler` | no | 0.2834 | 0.0904 | 0.6349 | yes | flow | interaction, flow |
| `web-page-snapshotter` | no | 0.2834 | 0.1340 | 0.6353 | yes | test, evidence | test, web, interaction |
| `frontend-debugger` | no | 0.2834 | 0.2325 | 0.6468 | yes | behavior, fix, frontend, code | behavior |

Top similarity neighbours: `customer-success-ops-acceptance-test-builder` (0.431), `travel-ops-acceptance-test-builder` (0.419), `marketing-ops-acceptance-test-builder` (0.402), `grant-ops-acceptance-test-builder` (0.399), `support-ops-acceptance-test-builder` (0.399)

### `clear_exp_p07_data_trust_audit`

- Family: `controlled_expansion_clear`
- Gold skill: `data-analysis-with-validation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-with-anomaly-focus` | no | 0.6532 | 0.4443 | 0.5074 | yes | spreadsheet, data, value | surfac, data |
| `data-analysis-overview` | no | 0.6532 | 0.4792 | 0.6048 | yes | spreadsheet | - |
| `data-analysis-for-reporting` | no | 0.6532 | 0.4989 | 0.6210 | yes | spreadsheet | - |

Top similarity neighbours: `data-analysis-with-validation` (0.653), `psc-data-trust-auditor` (0.587), `data-analysis-for-reporting` (0.499), `data-analysis-overview` (0.479), `psc-anomaly-watchlist-builder` (0.457)

### `clear_exp_p08_anomaly_watchlist_only`

- Family: `controlled_expansion_clear`
- Gold skill: `data-analysis-with-anomaly-focus`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-with-validation` | no | 0.5282 | 0.1022 | 0.5074 | yes | - | data, surfac |
| `data-analysis-for-root-cause-diagnosis` | no | 0.5282 | 0.2502 | 0.5533 | yes | evidence | spreadsheet |
| `data-analysis-for-reporting` | no | 0.5282 | 0.1984 | 0.4582 | no | evidence | spreadsheet |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.562), `latency-anomaly-detector` (0.551), `data-analysis-with-anomaly-focus` (0.528), `k8s-ops-failure-diagnoser` (0.381), `k8s-ops-monitoring-plan-builder` (0.375)

### `clear_exp_p09_targeted_document_fields`

- Family: `controlled_expansion_clear`
- Gold skill: `document-field-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 12

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-summariser` | no | 0.3634 | 0.2639 | 0.5776 | yes | summary, contract | document |
| `document-normaliser` | no | 0.3634 | 0.1735 | 0.5342 | yes | - | document |
| `multi-document-comparison-preparer` | no | 0.3634 | 0.1404 | 0.4787 | no | clause | field, clause, document |

Top similarity neighbours: `clause-obligation-extractor` (0.539), `receipt-extractor` (0.469), `meeting-notes-action-extractor` (0.415), `contract-ops-compliance-checker` (0.397), `contract-ops-quality-auditor` (0.395)

### `clear_exp_p10_multi_doc_comparison_matrix`

- Family: `controlled_expansion_clear`
- Gold skill: `multi-document-comparison-preparer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 11

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-field-extractor` | no | 0.4533 | 0.1753 | 0.4787 | no | output, document | document, field, clause |
| `document-summariser` | no | 0.4533 | 0.2576 | 0.5780 | yes | contract, document | document, key, detail |
| `document-normaliser` | no | 0.4533 | 0.1704 | 0.5582 | yes | document | document, section, structure |

Top similarity neighbours: `vendor-ops-comparison-builder` (0.562), `vendor-ops-summary-writer` (0.548), `vendor-ops-scenario-planner` (0.518), `vendor-ops-risk-reviewer` (0.488), `procurement-risk-summariser` (0.483)

### `clear_exp_p11_ci_first_error_triage`

- Family: `controlled_expansion_clear`
- Gold skill: `ci-log-root-cause-debugger`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `repo-code-reviewer` | no | 0.4740 | 0.3724 | 0.5790 | yes | review | test |
| `pr-review-comment-resolver` | no | 0.4740 | 0.3389 | 0.4363 | no | code, review | - |
| `github-issue-triager` | no | 0.4740 | 0.4769 | 0.5975 | yes | github, issue | - |

Top similarity neighbours: `psc-ci-log-first-failure-reader` (0.658), `ci-failure-debugger` (0.637), `public-swebench-analyze-ci` (0.596), `pr-reviewer` (0.501), `github-issue-triager` (0.477)

### `clear_exp_p12_review_comment_resolution_plan`

- Family: `controlled_expansion_clear`
- Gold skill: `pr-review-comment-resolver`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `repo-code-reviewer` | no | 0.7356 | 0.5115 | 0.6830 | yes | review | review |
| `ci-log-root-cause-debugger` | no | 0.7356 | 0.4321 | 0.4363 | no | fail | - |
| `release-changelog-generator` | no | 0.7356 | 0.3680 | 0.5882 | yes | - | extract, request |

Top similarity neighbours: `pr-review-comment-resolver` (0.736), `repo-code-reviewer` (0.511), `psc-pr-thread-fix-planner` (0.510), `review-comment-resolver` (0.509), `pr-reviewer` (0.483)

### `clear_exp_p13_hf_dataset_viewer_schema`

- Family: `controlled_expansion_clear`
- Gold skill: `hf-dataset-viewer-inspector`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `hf-local-model-selector` | no | 0.6382 | 0.4337 | 0.6257 | yes | hugg, face, local, model | hugg, face |
| `sentence-transformer-finetuner` | no | 0.6382 | 0.2944 | 0.3604 | no | split | split |
| `hf-community-eval-runner` | no | 0.6382 | 0.4861 | 0.6789 | yes | hugg, face, model | hugg, face |

Top similarity neighbours: `public-huggingface-datasets` (0.700), `hf-dataset-viewer-inspector` (0.638), `psc-hf-dataset-card-inspector` (0.595), `public-huggingface-huggingface-community-evals` (0.508), `psc-local-model-fit-selector` (0.502)

### `clear_exp_p14_sentence_embedding_finetune`

- Family: `controlled_expansion_clear`
- Gold skill: `sentence-transformer-finetuner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | no | 0.7307 | 0.2896 | 0.3604 | no | dataset, split | split |
| `hf-local-model-selector` | no | 0.7307 | 0.1578 | 0.3117 | no | - | - |
| `hf-community-eval-runner` | no | 0.7307 | 0.2594 | 0.4427 | no | evaluation, metric | plan, evaluation |
| `psc-sentence-embedding-trainer` | no | 0.7307 | 0.4632 | 0.6318 | yes | dataset, fine-tun, retrieval, pair, loss, choice, split, train | plan, fine-tun, retrieval, train, pair, evaluation, split, embedd |
| `public-huggingface-train-sentence-transformers` | no | 0.7307 | 0.6132 | 0.7465 | yes | sentence-transformer, retrieval, pair, loss, train | sentence-transformer, retrieval, similarity, train, pair, embedd |
| `psc-retrieval-result-adjudicator` | no | 0.7307 | 0.4682 | 0.3993 | no | retrieval, evaluation | retrieval, evaluation |

Top similarity neighbours: `sentence-transformer-finetuner` (0.731), `public-huggingface-train-sentence-transformers` (0.613), `psc-retrieval-result-adjudicator` (0.468), `psc-sentence-embedding-trainer` (0.463), `skill-benchmark-evaluator` (0.436)

### `clear_exp_p15_pdf_redaction_safety_review`

- Family: `controlled_expansion_clear`
- Gold skill: `pdf-redaction-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-layout-table-extractor` | no | 0.6456 | 0.3745 | 0.4572 | no | - | evidence |
| `pdf-question-answerer` | no | 0.6456 | 0.5100 | 0.5762 | yes | pdf, answer, content, question | pdf, content, evidence |
| `pdf-ocr-cleaner` | no | 0.6456 | 0.4698 | 0.4566 | no | text, region | - |
| `privacy-risk-reviewer` | no | 0.6456 | 0.2777 | 0.4973 | no | review, shar | review, risk |
| `public-office-chat-with-pdf` | no | 0.6456 | 0.5667 | 0.5353 | yes | pdf, answer, content, question | pdf, content, information |
| `psc-pdf-evidence-qa` | no | 0.6456 | 0.5389 | 0.6436 | yes | pdf, external, shar, answer, question | pdf, redaction, evidence |

Top similarity neighbours: `psc-pdf-redaction-pass` (0.667), `pdf-redaction-reviewer` (0.646), `public-office-chat-with-pdf` (0.567), `psc-pdf-scan-ocr-recovery` (0.540), `psc-pdf-evidence-qa` (0.539)

### `clear_exp_p16_pdf_form_completion`

- Family: `controlled_expansion_clear`
- Gold skill: `pdf-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-field-extractor` | no | 0.5623 | 0.3396 | 0.3294 | no | field, extract | field |
| `pdf-layout-table-extractor` | no | 0.5623 | 0.3903 | 0.4926 | no | field, extract | field |
| `pdf-to-docx-converter` | no | 0.5623 | 0.4117 | 0.4258 | no | pdf, convert | pdf |
| `pdf-question-answerer` | no | 0.5623 | 0.3398 | 0.5017 | yes | pdf | pdf |
| `implicit-pdf-evidence-answerer` | no | 0.5623 | 0.3157 | 0.5077 | yes | pdf, convert, extract | pdf |

Top similarity neighbours: `pdf-form-filler` (0.562), `public-office-pdf-form-filler` (0.516), `grant-ops-summary-writer` (0.448), `grant-ops-field-extractor` (0.417), `pdf-to-docx-converter` (0.412)

### `clear_exp_p17_claim_support_audit`

- Family: `controlled_expansion_clear`
- Gold skill: `citation-grounding-helper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | no | 0.4388 | 0.3529 | 0.7106 | yes | claim, support | claim, note, support |
| `paper-summariser` | no | 0.4388 | 0.2724 | 0.4244 | no | paper, summary | - |
| `related-work-synthesiser` | no | 0.4388 | 0.0883 | 0.3904 | no | paper | - |
| `identity-ops-evidence-grounder` | no | 0.4388 | 0.3986 | 0.4235 | yes | claim, evidence | claim, note, ground |
| `contract-ops-evidence-grounder` | no | 0.4388 | 0.3606 | 0.4587 | yes | claim, evidence | claim, note, ground |

Top similarity neighbours: `citation-grounding-helper` (0.439), `identity-ops-evidence-grounder` (0.399), `insurance-ops-evidence-grounder` (0.392), `legal-discovery-ops-evidence-grounder` (0.378), `legal-ops-evidence-grounder` (0.378)

### `clear_exp_p18_related_work_synthesis`

- Family: `controlled_expansion_clear`
- Gold skill: `related-work-synthesiser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `paper-summariser` | no | 0.5470 | 0.4305 | 0.5469 | yes | paper | paper, question |
| `multi-source-comparison-builder` | no | 0.5470 | 0.3382 | 0.5379 | yes | paper | multiple, paper |
| `citation-note-extractor` | no | 0.5470 | 0.2900 | 0.4848 | no | - | - |

Top similarity neighbours: `skill-authoring-guide` (0.667), `skill-editor` (0.581), `skill-benchmark-evaluator` (0.563), `agent-ops-summary-writer` (0.552), `skill-finder` (0.551)

### `clear_exp_p19_auth_flow_review`

- Family: `controlled_expansion_clear`
- Gold skill: `auth-flow-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `security-threat-modeler` | no | 0.6815 | 0.4365 | 0.5270 | yes | flow, security, architecture, threat, model | flow, security |
| `security-code-reviewer` | no | 0.6815 | 0.3925 | 0.6944 | yes | review, security | review, authorization, security |
| `privacy-risk-reviewer` | no | 0.6815 | 0.3946 | 0.7290 | yes | review, handl | review, risk |

Top similarity neighbours: `auth-flow-reviewer` (0.681), `api-security-threat-reviewer` (0.475), `security-threat-modeler` (0.436), `psc-handler-vulnerability-reviewer` (0.430), `auth-flow-integrator` (0.427)

### `clear_exp_p20_skill_router_policy`

- Family: `controlled_expansion_clear`
- Gold skill: `skill-router-policy-designer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 592

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.2477 | 0.3316 | 0.5384 | yes | - | - |
| `skill-benchmark-evaluator` | no | 0.2477 | 0.3265 | 0.5846 | yes | retrieval | - |
| `skill-authoring-guide` | no | 0.2477 | 0.2577 | 0.6061 | yes | procedural | - |

Top similarity neighbours: `search-ops-evidence-grounder` (0.523), `search-ops-summary-writer` (0.487), `search-ops-compliance-checker` (0.470), `search-ops-risk-reviewer` (0.458), `docs-ops-compliance-checker` (0.457)

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-for-reporting` | no | 0.4319 | 0.3990 | 0.6943 | yes | turn | spreadsheet |
| `data-analysis-with-anomaly-focus` | no | 0.4319 | 0.2330 | 0.6496 | yes | pattern | produce, spreadsheet, pattern |
| `data-analysis-with-validation` | no | 0.4319 | 0.1587 | 0.6048 | yes | need, most | - |

Top similarity neighbours: `psc-executive-metric-narrator` (0.467), `data-analysis-overview` (0.432), `news-briefing-writer` (0.422), `news-theme-extractor` (0.405), `dashboard-ops-summary-writer` (0.399)

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | no | 0.5460 | 0.2475 | 0.6496 | yes | - | produce, spreadsheet, pattern |
| `data-analysis-for-root-cause-diagnosis` | no | 0.5460 | 0.2833 | 0.5533 | yes | - | spreadsheet |
| `data-analysis-with-validation` | no | 0.5460 | 0.1447 | 0.5074 | yes | most | data, surfac |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.571), `data-analysis-with-anomaly-focus` (0.546), `latency-anomaly-detector` (0.520), `debugging-root-cause-helper` (0.395), `churn-risk-analyser` (0.361)

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 43

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | no | 0.4354 | 0.2458 | 0.6048 | yes | - | - |
| `data-analysis-with-anomaly-focus` | no | 0.4354 | 0.3766 | 0.5074 | yes | value, issue | surfac, data |
| `data-analysis-for-root-cause-diagnosis` | no | 0.4354 | 0.2396 | 0.6074 | yes | - | - |

Top similarity neighbours: `psc-data-trust-auditor` (0.550), `psc-anomaly-watchlist-builder` (0.508), `dataset-ops-quality-auditor` (0.495), `incident-ops-quality-auditor` (0.490), `database-ops-quality-auditor` (0.489)

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 91

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-with-anomaly-focus` | no | 0.2298 | 0.2016 | 0.5533 | yes | data | spreadsheet |
| `data-analysis-overview` | no | 0.2298 | 0.1794 | 0.6533 | yes | - | spreadsheet |
| `data-analysis-with-validation` | no | 0.2298 | 0.0900 | 0.6074 | yes | data, most | - |

Top similarity neighbours: `metrics-root-cause-diagnoser` (0.375), `latency-anomaly-detector` (0.366), `media-ops-failure-diagnoser` (0.343), `implicit-trace-path-diagnoser` (0.333), `public-swebench-vector-index-tuning` (0.328)

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | no | 0.5076 | 0.3474 | 0.6943 | yes | broad | spreadsheet |
| `data-analysis-for-root-cause-diagnosis` | no | 0.5076 | 0.2447 | 0.6575 | yes | - | spreadsheet, evidence |
| `data-analysis-with-anomaly-focus` | no | 0.5076 | 0.2103 | 0.4582 | no | - | spreadsheet |

Top similarity neighbours: `psc-executive-metric-narrator` (0.518), `data-analysis-for-reporting` (0.508), `dashboard-ops-summary-writer` (0.500), `news-briefing-writer` (0.493), `media-ops-summary-writer` (0.471)

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | no | 0.4886 | 0.1578 | 0.6940 | yes | pattern | spreadsheet, pattern, produce |
| `data-analysis-for-root-cause-diagnosis` | no | 0.4886 | 0.1666 | 0.6062 | yes | evidence | uses, spreadsheet |
| `data-analysis-with-anomaly-focus` | no | 0.4886 | 0.1897 | 0.5688 | yes | pattern | spreadsheet, pattern, produce |

Top similarity neighbours: `data-analysis-for-forecasting` (0.489), `deadline-reminder-planner` (0.331), `capacity-risk-forecaster` (0.321), `tech-news-trend-extractor` (0.309), `psc-anomaly-watchlist-builder` (0.302)

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 32

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | no | 0.4430 | 0.2180 | 0.7161 | yes | broad | spreadsheet, produce, strongest |
| `data-analysis-for-reporting` | no | 0.4430 | 0.2387 | 0.5776 | yes | - | spreadsheet |
| `data-analysis-for-forecasting` | no | 0.4430 | 0.2792 | 0.5718 | yes | forecast | spreadsheet, produce |

Top similarity neighbours: `priority-sorter` (0.568), `travel-ops-priority-ranker` (0.502), `risk-ops-priority-ranker` (0.495), `robotics-ops-priority-ranker` (0.486), `decision-matrix-builder` (0.486)

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | no | 0.3205 | 0.1491 | 0.4188 | no | identify | screenshot |
| `accessibility-interaction-auditor` | no | 0.3205 | 0.0241 | 0.3560 | no | interaction, clue | interaction |
| `public-playwright-interactive` | no | 0.3205 | 0.1422 | 0.6408 | yes | interaction, browser | browser, interaction |
| `public-openai-playwright` | no | 0.3205 | 0.0960 | 0.5178 | yes | browser | browser, screenshot |

Top similarity neighbours: `frontend-debugger` (0.350), `ecommerce-ops-failure-diagnoser` (0.345), `ads-ops-failure-diagnoser` (0.325), `playwright-flow-debugger` (0.321), `grant-ops-failure-diagnoser` (0.320)

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `playwright-flow-debugger` | no | 0.6127 | 0.0964 | 0.4188 | no | screenshot | screenshot |
| `accessibility-interaction-auditor` | no | 0.6127 | 0.2762 | 0.4608 | no | contrast | contrast |
| `public-openai-screenshot` | no | 0.6127 | 0.2456 | 0.3397 | no | screenshot, need | screenshot |
| `public-anthropic-webapp-testing` | no | 0.6127 | 0.1843 | 0.3651 | no | screenshot | screenshot |
| `implicit-visual-diff-reviewer` | yes | 0.6127 | 0.5148 | 0.6475 | yes | compare, current, screenshot, visual, regression | compare, current, screenshot, acros, viewport, visual, regression, layout |
| `psc-visual-screenshot-reviewer` | no | 0.6127 | 0.5221 | 0.6025 | yes | compare, screenshot, visual, regression, clipp, spac, shift | compare, screenshot, visual, regression, layout, shift, clipp |

Top similarity neighbours: `visual-regression-checker` (0.613), `psc-visual-screenshot-reviewer` (0.522), `implicit-visual-diff-reviewer` (0.515), `mobile-ops-comparison-builder` (0.419), `dashboard-ops-comparison-builder` (0.403)

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | no | 0.5996 | 0.3422 | 0.4608 | no | - | contrast |
| `playwright-flow-debugger` | no | 0.5996 | 0.2623 | 0.3560 | no | interaction | interaction |
| `web-ui-tester` | no | 0.5996 | 0.2634 | 0.4484 | no | interaction, whether | interaction, web |
| `public-anthropic-webapp-testing` | no | 0.5996 | 0.0951 | 0.4195 | no | - | web |
| `accessibility-checker` | yes | 0.5996 | 0.4839 | 0.7383 | yes | focu, keyboard, screen-reader, order | keyboard, focu, order, contrast, accessibility, web, interface |
| `public-addy-web-accessibility` | yes | 0.5996 | 0.4475 | 0.6544 | yes | audit, keyboard, accessible | audit, keyboard, navigation, accessible, accessibility, web |

Top similarity neighbours: `accessibility-interaction-auditor` (0.600), `psc-accessibility-interaction-auditor` (0.518), `accessibility-checker` (0.484), `public-addy-web-accessibility` (0.448), `implicit-browser-flow-investigator` (0.373)

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `deployment-release-verifier` | no | 0.4102 | 0.2192 | 0.7033 | yes | - | deployment, environment, version |
| `playwright-flow-debugger` | no | 0.4102 | 0.1925 | 0.5050 | yes | - | failure |
| `web-performance-budget-checker` | no | 0.4102 | 0.0797 | 0.4783 | no | - | - |

Top similarity neighbours: `public-netlify-deploy` (0.518), `deployment-build-triager` (0.410), `ci-failure-debugger` (0.340), `ci-log-root-cause-debugger` (0.315), `devops-ops-failure-diagnoser` (0.313)

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `deployment-build-triager` | no | 0.5144 | 0.4090 | 0.7033 | yes | version, environment, deployment | deployment, environment, version |
| `visual-regression-checker` | no | 0.5144 | 0.2407 | 0.4684 | no | - | - |
| `public-netlify-deploy` | no | 0.5144 | 0.6062 | 0.3772 | yes | production, deploy, publish, netlify | - |
| `public-openai-vercel-deploy` | no | 0.5144 | 0.5461 | 0.4486 | yes | deploy, live, app, create, vercel, deployment | deployment |

Top similarity neighbours: `public-netlify-deploy` (0.606), `public-openai-vercel-deploy` (0.546), `deployment-release-verifier` (0.514), `deployment-build-triager` (0.409), `public-openai-render-deploy` (0.379)

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | no | 0.4529 | 0.2864 | 0.5280 | yes | - | - |
| `deployment-release-verifier` | no | 0.4529 | 0.1923 | 0.5508 | yes | - | load, evidence |
| `accessibility-interaction-auditor` | no | 0.4529 | 0.2616 | 0.4428 | no | - | web, clue |

Top similarity neighbours: `public-swebench-distributed-tracing` (0.465), `mobile-ops-summary-writer` (0.463), `web-performance-budget-checker` (0.453), `mobile-ops-quality-auditor` (0.447), `mobile-ops-resource-linker` (0.440)

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 694

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-normaliser` | no | 0.1591 | 0.0916 | 0.6437 | yes | - | document |
| `document-field-extractor` | no | 0.1591 | 0.1063 | 0.5776 | yes | - | document |
| `document-converter` | no | 0.1591 | 0.0856 | 0.5798 | yes | - | document, such, memo, form |

Top similarity neighbours: `travel-ops-summary-writer` (0.457), `travel-ops-risk-reviewer` (0.416), `travel-ops-compliance-checker` (0.385), `travel-ops-dependency-mapper` (0.381), `travel-ops-rewrite-editor` (0.366)

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 9

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-normaliser` | no | 0.4312 | 0.3998 | 0.6511 | yes | document, mean | document, structure, preserv, mean, content |
| `document-summariser` | no | 0.4312 | 0.4204 | 0.5124 | yes | document, form | document |
| `document-converter` | no | 0.4312 | 0.3733 | 0.5581 | yes | document, form | document |

Top similarity neighbours: `travel-ops-rewrite-editor` (0.574), `travel-ops-summary-writer` (0.507), `method-note-builder` (0.484), `travel-ops-handoff-brief-writer` (0.441), `citation-note-extractor` (0.437)

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-rewriter` | no | 0.4543 | 0.4257 | 0.6511 | yes | document, structure, rewrite | document, structure, preserv, content, mean |
| `document-converter` | no | 0.4543 | 0.3542 | 0.6476 | yes | document, layout | document |
| `document-summariser` | no | 0.4543 | 0.3323 | 0.6437 | yes | document | document |

Top similarity neighbours: `travel-ops-rewrite-editor` (0.515), `document-normaliser` (0.454), `method-note-builder` (0.435), `public-office-meeting-notes` (0.432), `facilities-ops-rewrite-editor` (0.429)

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 12

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-summariser` | no | 0.4059 | 0.2788 | 0.5776 | yes | detail, summary | document |
| `multi-document-comparison-preparer` | no | 0.4059 | 0.2475 | 0.4787 | no | field, detail | field, clause, document |
| `layout-preserving-converter` | no | 0.4059 | 0.2516 | 0.5100 | yes | table | document |

Top similarity neighbours: `receipt-extractor` (0.536), `public-office-invoice-organizer` (0.440), `procurement-ops-field-extractor` (0.439), `finance-ops-artifact-packager` (0.435), `public-office-invoice-generator` (0.434)

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-field-extractor` | no | 0.4703 | 0.1817 | 0.4787 | no | - | document, field, clause |
| `document-normaliser` | no | 0.4703 | 0.2314 | 0.5582 | yes | section | document, section, structure |
| `document-converter` | no | 0.4703 | 0.2290 | 0.5213 | yes | - | document |

Top similarity neighbours: `privacy-policy-drafter` (0.488), `multi-document-comparison-preparer` (0.470), `writing-ops-comparison-builder` (0.400), `public-mattpocock-review` (0.400), `legal-ops-comparison-builder` (0.392)

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-normaliser` | no | 0.4129 | 0.3192 | 0.6476 | yes | clean, content | document |
| `layout-preserving-converter` | no | 0.4129 | 0.4006 | 0.8143 | yes | convert, preserve, label, layout | convert, document, another, format, layout |
| `document-summariser` | no | 0.4129 | 0.2535 | 0.5798 | yes | form | document, such, memo, form |

Top similarity neighbours: `public-markitdown` (0.428), `document-converter` (0.413), `layout-preserving-converter` (0.401), `office-to-markdown-converter` (0.399), `public-office-form-builder` (0.390)

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-converter` | no | 0.4243 | 0.3707 | 0.8143 | yes | layout, markdown, priority, fidelity, note | convert, document, another, format, layout |
| `document-field-extractor` | no | 0.4243 | 0.2174 | 0.5100 | yes | field | document |
| `document-normaliser` | no | 0.4243 | 0.2946 | 0.6219 | yes | preserv | document, section |

Top similarity neighbours: `layout-preserving-converter` (0.424), `method-note-builder` (0.397), `public-mattpocock-writing-shape` (0.377), `public-office-form-builder` (0.372), `document-converter` (0.371)

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Family: `github_ci_maintenance`
- Gold skill: `ci-log-root-cause-debugger`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pr-review-comment-resolver` | no | 0.6584 | 0.2368 | 0.4363 | no | - | - |
| `repo-code-reviewer` | no | 0.6584 | 0.2812 | 0.5790 | yes | - | test |
| `github-issue-triager` | no | 0.6584 | 0.3240 | 0.5975 | yes | - | - |
| `release-changelog-generator` | no | 0.6584 | 0.2707 | 0.5265 | yes | - | - |

Top similarity neighbours: `ci-log-root-cause-debugger` (0.658), `implicit-ci-failure-reader` (0.607), `ci-failure-debugger` (0.534), `psc-ci-log-first-failure-reader` (0.529), `debugging-root-cause-helper` (0.366)

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Family: `github_ci_maintenance`
- Gold skill: `pr-review-comment-resolver`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-openai-gh-address-comments` | no | 0.5911 | 0.3491 | 0.4251 | no | review, comment | review, comment |
| `review-comment-resolver` | no | 0.5911 | 0.5076 | 0.7327 | yes | review, comment, code | request, review, comment, code, change |
| `ci-log-root-cause-debugger` | no | 0.5911 | 0.1962 | 0.4363 | no | - | - |
| `repo-code-reviewer` | no | 0.5911 | 0.4752 | 0.6830 | yes | review | review |

Top similarity neighbours: `pr-review-comment-resolver` (0.591), `review-comment-resolver` (0.508), `public-mattpocock-review` (0.502), `pr-reviewer` (0.498), `repo-code-reviewer` (0.475)

### `github_ci_maintenance_p3_repo_code_reviewer`

- Family: `github_ci_maintenance`
- Gold skill: `repo-code-reviewer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | no | 0.4778 | 0.5750 | 0.5790 | yes | test | test |
| `pr-review-comment-resolver` | no | 0.4778 | 0.3455 | 0.6830 | yes | review, code | review |
| `github-issue-triager` | no | 0.4778 | 0.3897 | 0.6512 | yes | miss | miss |
| `release-changelog-generator` | no | 0.4778 | 0.3552 | 0.5796 | yes | - | - |

Top similarity neighbours: `ci-log-root-cause-debugger` (0.575), `ci-failure-debugger` (0.496), `repo-code-reviewer` (0.478), `implicit-ci-failure-reader` (0.449), `debugging-root-cause-helper` (0.436)

### `github_ci_maintenance_p4_github_issue_triager`

- Family: `github_ci_maintenance`
- Gold skill: `github-issue-triager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 7

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | no | 0.3987 | 0.2183 | 0.5975 | yes | - | - |
| `pr-review-comment-resolver` | no | 0.3987 | 0.2736 | 0.4698 | no | - | - |
| `repo-code-reviewer` | no | 0.3987 | 0.3168 | 0.6512 | yes | miss | miss |
| `release-changelog-generator` | no | 0.3987 | 0.2561 | 0.5451 | yes | - | - |

Top similarity neighbours: `public-mattpocock-setup-matt-pocock-skills` (0.476), `public-oh-my-changelog-maintenance` (0.443), `partnerships-ops-failure-diagnoser` (0.427), `real-estate-ops-failure-diagnoser` (0.411), `property-ops-failure-diagnoser` (0.409)

### `github_ci_maintenance_p5_release_changelog_generator`

- Family: `github_ci_maintenance`
- Gold skill: `release-changelog-generator`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 7

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | no | 0.4104 | 0.1679 | 0.5265 | yes | - | - |
| `pr-review-comment-resolver` | no | 0.4104 | 0.3870 | 0.5882 | yes | turn, change, review, code | extract, request |
| `repo-code-reviewer` | no | 0.4104 | 0.3571 | 0.5796 | yes | review | - |
| `github-issue-triager` | no | 0.4104 | 0.3420 | 0.5451 | yes | - | - |

Top similarity neighbours: `psc-release-communication-packager` (0.489), `public-mattpocock-review` (0.438), `release-note-writer` (0.437), `public-office-changelog-generator` (0.428), `pr-reviewer` (0.424)

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Family: `github_ci_maintenance`
- Gold skill: `git-safety-guardrail-installer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-mattpocock-git-guardrails-claude-code` | no | 0.6705 | 0.6171 | 0.6530 | yes | block, git, push, reset, hard, hook | hook, prevent, dangerou, git, operation, command |
| `public-mattpocock-setup-pre-commit` | no | 0.6705 | 0.4226 | 0.3537 | no | hook | configure, hook |
| `ci-log-root-cause-debugger` | no | 0.6705 | 0.2046 | 0.4432 | no | - | command |
| `pr-review-comment-resolver` | no | 0.6705 | 0.3834 | 0.4113 | no | step, verification | - |
| `psc-repo-guardrail-hook-installer` | no | 0.6705 | 0.6527 | 0.7527 | yes | repository, guardrail, secret, hook, verification | repository, hook, guardrail, secret, workflow, command |
| `public-oh-my-git-guardrails-claude-code` | no | 0.6705 | 0.4141 | 0.4607 | no | - | - |

Top similarity neighbours: `git-safety-guardrail-installer` (0.670), `psc-repo-guardrail-hook-installer` (0.653), `public-mattpocock-git-guardrails-claude-code` (0.617), `psc-pr-thread-fix-planner` (0.452), `psc-release-communication-packager` (0.437)

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-dataset-viewer-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-datasets` | no | 0.4339 | 0.3715 | 0.7311 | yes | dataset, subset, split | hugg, face, dataset, metadata, split, subset |
| `public-huggingface-huggingface-tool-builder` | no | 0.4339 | 0.1035 | 0.5321 | yes | - | hugg, face |
| `hf-local-model-selector` | no | 0.4339 | 0.2342 | 0.6257 | yes | model | hugg, face |
| `sentence-transformer-finetuner` | no | 0.4339 | 0.2130 | 0.3604 | no | split | split |

Top similarity neighbours: `hf-dataset-viewer-inspector` (0.434), `implicit-hf-dataset-inspector` (0.417), `dataset-ops-acceptance-test-builder` (0.391), `dataset-ops-quality-auditor` (0.379), `dataset-ops-risk-reviewer` (0.375)

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-local-model-selector`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-local-models` | yes | 0.4917 | 0.5127 | 0.6159 | yes | local, model, mac, gguf | select, gguf, model, local |
| `public-huggingface-huggingface-best` | no | 0.4917 | 0.1741 | 0.3226 | no | - | - |
| `hf-dataset-viewer-inspector` | no | 0.4917 | 0.3117 | 0.6257 | yes | hugg, face, dataset | hugg, face |
| `sentence-transformer-finetuner` | no | 0.4917 | 0.2278 | 0.3117 | no | train | - |

Top similarity neighbours: `psc-local-model-fit-selector` (0.513), `public-huggingface-huggingface-local-models` (0.513), `hf-local-model-selector` (0.492), `public-huggingface-huggingface-vision-trainer` (0.457), `public-huggingface-huggingface-llm-trainer` (0.449)

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Family: `huggingface_ml_workflows`
- Gold skill: `sentence-transformer-finetuner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-huggingface-train-sentence-transformers` | yes | 0.6170 | 0.4697 | 0.7465 | yes | pair, sentence-transformer, retrieval | sentence-transformer, retrieval, similarity, train, pair, embedd |
| `public-swebench-similarity-search-patterns` | no | 0.6170 | 0.3032 | 0.3704 | no | retrieval | retrieval, similarity |
| `hf-dataset-viewer-inspector` | no | 0.6170 | 0.1386 | 0.3604 | no | split | split |
| `hf-local-model-selector` | no | 0.6170 | 0.1226 | 0.3117 | no | - | - |
| `psc-sentence-embedding-trainer` | no | 0.6170 | 0.3669 | 0.6318 | yes | pair, hard, negative, plan, fine-tun, split, retrieval, metric | plan, fine-tun, retrieval, train, pair, evaluation, split, embedd |
| `psc-retrieval-result-adjudicator` | no | 0.6170 | 0.5335 | 0.3993 | yes | rout, retrieval | retrieval, evaluation |

Top similarity neighbours: `sentence-transformer-finetuner` (0.617), `psc-retrieval-result-adjudicator` (0.533), `skill-authoring-guide` (0.529), `skill-router-policy-designer` (0.520), `agent-ops-summary-writer` (0.511)

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Family: `huggingface_ml_workflows`
- Gold skill: `gradio-demo-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 259

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | no | 0.2475 | 0.1970 | 0.4544 | yes | - | dataset, example |
| `hf-local-model-selector` | no | 0.2475 | 0.1764 | 0.4465 | yes | model | model |
| `sentence-transformer-finetuner` | no | 0.2475 | 0.2716 | 0.2751 | yes | plan, check, fine-tun | - |
| `hf-zerogpu-space-deployer` | no | 0.2475 | 0.0720 | 0.4229 | no | - | constraint |

Top similarity neighbours: `public-huggingface-huggingface-trackio` (0.450), `web-ops-scenario-planner` (0.443), `support-ticket-triager` (0.418), `web-ui-tester` (0.406), `webhook-setup-planner` (0.374)

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-zerogpu-space-deployer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | no | 0.6624 | 0.3331 | 0.5148 | yes | hugg, face | hugg, face |
| `hf-local-model-selector` | no | 0.6624 | 0.4501 | 0.6089 | yes | hugg, face | hugg, face |
| `sentence-transformer-finetuner` | no | 0.6624 | 0.2067 | 0.2329 | no | - | - |
| `gradio-demo-builder` | no | 0.6624 | 0.4996 | 0.4229 | no | gradio, constraint | constraint |

Top similarity neighbours: `public-huggingface-huggingface-zerogpu` (0.692), `hf-zerogpu-space-deployer` (0.662), `public-huggingface-huggingface-llm-trainer` (0.553), `public-huggingface-huggingface-vision-trainer` (0.535), `gradio-demo-builder` (0.500)

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-community-eval-runner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | no | 0.5127 | 0.3708 | 0.6789 | yes | hugg, face, dataset | hugg, face |
| `hf-local-model-selector` | no | 0.5127 | 0.3325 | 0.7039 | yes | hugg, face | hugg, face, model, hardware |
| `sentence-transformer-finetuner` | no | 0.5127 | 0.2601 | 0.4427 | no | evaluation, plan | plan, evaluation |
| `gradio-demo-builder` | no | 0.5127 | 0.3374 | 0.4945 | no | dataset, gradio | model |

Top similarity neighbours: `hf-community-eval-runner` (0.513), `public-huggingface-huggingface-vision-trainer` (0.488), `psc-hf-dataset-card-inspector` (0.476), `public-huggingface-datasets` (0.469), `public-huggingface-huggingface-llm-trainer` (0.466)

### `implicit_p10_trace_path`

- Family: `implicit_field_stress`
- Gold skill: `implicit-trace-path-diagnoser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-slo-alert-author` | no | 0.4729 | 0.1763 | 0.5090 | yes | - | - |
| `distributed-trace-investigator` | yes | 0.4729 | 0.5669 | 0.5327 | yes | distribut, trace, span, locate, latency | distribut, trace, span, locate, latency, fail, call, dependency |
| `prometheus-alert-rule-writer` | no | 0.4729 | 0.2686 | 0.3596 | no | - | - |

Top similarity neighbours: `distributed-trace-investigator` (0.567), `public-swebench-distributed-tracing` (0.546), `latency-anomaly-detector` (0.504), `implicit-trace-path-diagnoser` (0.473), `service-mesh-traffic-debugger` (0.446)

### `implicit_p1_pdf_answer`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-evidence-answerer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 29

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-pdf-table-reconstructor` | no | 0.3072 | 0.2618 | 0.7402 | yes | pdf, packet, page | work, pdf, packet, page |
| `pdf-question-answerer` | no | 0.3072 | 0.2871 | 0.6298 | yes | answer, pdf, question, page, evidence | pdf, answer, page, evidence |
| `pdf-layout-table-extractor` | no | 0.3072 | 0.2616 | 0.5207 | yes | page, evidence, table, field, extract, layout | page, evidence, extract |

Top similarity neighbours: `travel-ops-risk-reviewer` (0.419), `travel-ops-summary-writer` (0.417), `travel-ops-compliance-checker` (0.376), `travel-ops-dependency-mapper` (0.370), `travel-ops-quality-auditor` (0.370)

### `implicit_p2_pdf_table`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-table-reconstructor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-pdf-evidence-answerer` | no | 0.4841 | 0.4931 | 0.7402 | yes | extract, pdf, page, answer | work, pdf, packet, page |
| `pdf-layout-table-extractor` | yes | 0.4841 | 0.5707 | 0.6568 | yes | row, extract, page, column | row, column, page |
| `pdf-question-answerer` | no | 0.4841 | 0.5532 | 0.3658 | yes | pdf, page, answer | pdf, page |

Top similarity neighbours: `pdf-layout-table-extractor` (0.571), `pdf-question-answerer` (0.553), `public-office-invoice-template` (0.540), `implicit-pdf-evidence-answerer` (0.493), `public-office-pdf-extraction` (0.492)

### `implicit_p3_browser_flow`

- Family: `implicit_field_stress`
- Gold skill: `implicit-browser-flow-investigator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 395

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-visual-diff-reviewer` | no | 0.0743 | -0.0380 | 0.5147 | yes | - | state, screenshot |
| `playwright-flow-debugger` | no | 0.0743 | 0.1475 | 0.4990 | yes | reproduce, console, network, evidence, failure | interaction, console, network, screenshot |
| `visual-regression-checker` | no | 0.0743 | 0.0563 | 0.3970 | yes | - | screenshot |

Top similarity neighbours: `ads-ops-failure-diagnoser` (0.304), `fundraising-ops-failure-diagnoser` (0.289), `frontend-debugger` (0.270), `sales-ops-failure-diagnoser` (0.268), `ecommerce-ops-failure-diagnoser` (0.263)

### `implicit_p4_visual_diff`

- Family: `implicit_field_stress`
- Gold skill: `implicit-visual-diff-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-browser-flow-investigator` | no | 0.5356 | 0.3078 | 0.5147 | yes | screenshot | state, screenshot |
| `visual-regression-checker` | yes | 0.5356 | 0.5937 | 0.6475 | yes | compare, baseline, screenshot, layout, shift, clipp, acros | compare, current, visual, acros, screenshot, viewport, layout, regression |
| `playwright-flow-debugger` | no | 0.5356 | 0.2457 | 0.2597 | no | screenshot | screenshot |

Top similarity neighbours: `visual-regression-checker` (0.594), `psc-visual-screenshot-reviewer` (0.552), `implicit-visual-diff-reviewer` (0.536), `mobile-ops-rewrite-editor` (0.499), `mobile-ops-summary-writer` (0.470)

### `implicit_p5_ci_failure`

- Family: `implicit_field_stress`
- Gold skill: `implicit-ci-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-review-comment-planner` | no | 0.5801 | 0.0984 | 0.3685 | no | - | - |
| `ci-log-root-cause-debugger` | no | 0.5801 | 0.4804 | 0.5365 | yes | error | failure |
| `repo-code-reviewer` | no | 0.5801 | 0.2345 | 0.3040 | no | - | - |
| `ci-failure-debugger` | no | 0.5801 | 0.5029 | 0.4922 | yes | error, smallest, fix | failure, fix |
| `psc-ci-log-first-failure-reader` | no | 0.5801 | 0.4951 | 0.4971 | yes | find, first, meaningful, fix, rerun | read, first, meaningful, failure, likely, root, cause, rerun |

Top similarity neighbours: `implicit-ci-failure-reader` (0.580), `ci-failure-debugger` (0.503), `psc-ci-log-first-failure-reader` (0.495), `ci-log-root-cause-debugger` (0.480), `bioinformatics-ops-failure-diagnoser` (0.412)

### `implicit_p6_review_comments`

- Family: `implicit_field_stress`
- Gold skill: `implicit-review-comment-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 48

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-ci-failure-reader` | no | 0.3358 | 0.3826 | 0.3685 | yes | - | - |
| `pr-review-comment-resolver` | yes | 0.3358 | 0.6202 | 0.4949 | yes | review, code | turn, review, comment |
| `repo-code-reviewer` | no | 0.3358 | 0.6047 | 0.3593 | yes | review | review |

Top similarity neighbours: `pr-review-comment-resolver` (0.620), `repo-code-reviewer` (0.605), `psc-pr-thread-fix-planner` (0.559), `pr-reviewer` (0.539), `psc-ci-log-first-failure-reader` (0.530)

### `implicit_p7_hf_dataset`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-dataset-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 14

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-hf-local-model-chooser` | no | 0.4740 | 0.4609 | 0.6244 | yes | hugg, face, choose, local, model | - |
| `hf-dataset-viewer-inspector` | yes | 0.4740 | 0.6314 | 0.6948 | yes | inspect, hugg, face, dataset, split, row, example, schema | inspect, dataset, split, subset, example, schema |
| `hf-local-model-selector` | no | 0.4740 | 0.4727 | 0.4445 | yes | hugg, face, local, model | - |

Top similarity neighbours: `psc-hf-dataset-card-inspector` (0.689), `public-huggingface-datasets` (0.667), `hf-dataset-viewer-inspector` (0.631), `psc-local-model-fit-selector` (0.579), `psc-sentence-embedding-trainer` (0.570)

### `implicit_p8_hf_model`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-local-model-chooser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 27

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-hf-dataset-inspector` | no | 0.3012 | 0.2630 | 0.6244 | yes | inspect, dataset | - |
| `hf-local-model-selector` | yes | 0.3012 | 0.3902 | 0.7390 | yes | hugg, face, gguf, quantization | local, hugg, face, gguf, model, memory, quantization, latency |
| `hf-dataset-viewer-inspector` | no | 0.3012 | 0.3660 | 0.4489 | yes | hugg, face, inspect, dataset | hugg, face |

Top similarity neighbours: `public-huggingface-huggingface-llm-trainer` (0.575), `public-huggingface-huggingface-vision-trainer` (0.565), `psc-hf-dataset-card-inspector` (0.538), `psc-sentence-embedding-trainer` (0.513), `psc-local-model-fit-selector` (0.491)

### `implicit_p9_alert_rule`

- Family: `implicit_field_stress`
- Gold skill: `implicit-slo-alert-author`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `implicit-trace-path-diagnoser` | no | 0.5679 | 0.1767 | 0.5090 | yes | - | - |
| `prometheus-alert-rule-writer` | yes | 0.5679 | 0.5634 | 0.6465 | yes | alert, rule, metric, window, severity, label | alert, rule, slos, metric, name, window, label, severity |
| `distributed-trace-investigator` | no | 0.5679 | 0.2228 | 0.1912 | no | - | - |

Top similarity neighbours: `implicit-slo-alert-author` (0.568), `prometheus-alert-rule-writer` (0.563), `slo-breach-checker` (0.508), `support-ops-acceptance-test-builder` (0.425), `customer-success-ops-acceptance-test-builder` (0.425)

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `incident-summary-writer` | no | 0.4676 | 0.3133 | 0.6402 | yes | - | summary, metric, operational |
| `metrics-root-cause-diagnoser` | no | 0.4676 | 0.2161 | 0.6323 | yes | - | current, operational |
| `latency-anomaly-detector` | no | 0.4676 | 0.2790 | 0.4758 | no | service | metric, service |

Top similarity neighbours: `public-swebench-service-mesh-observability` (0.516), `service-mesh-traffic-debugger` (0.472), `metrics-overview` (0.468), `public-swebench-distributed-tracing` (0.460), `public-swebench-slo-implementation` (0.443)

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `metrics-root-cause-diagnoser` | no | 0.6057 | 0.2645 | 0.4881 | no | identify | regression |
| `metrics-overview` | no | 0.6057 | 0.4380 | 0.4758 | no | service, snapshot, metric | metric, service |
| `slo-breach-checker` | no | 0.6057 | 0.3682 | 0.4578 | no | service, whether, metric | metric, service |
| `public-swebench-distributed-tracing` | no | 0.6057 | 0.5984 | 0.4235 | yes | identify, performance, request | - |
| `web-performance-budget-checker` | no | 0.6057 | 0.4467 | 0.2279 | no | performance, metric | metric |
| `public-swebench-service-mesh-observability` | no | 0.6057 | 0.4490 | 0.4003 | no | service, metric | latency, metric, service, includ |

Top similarity neighbours: `latency-anomaly-detector` (0.606), `public-swebench-distributed-tracing` (0.598), `cloud-ops-quality-auditor` (0.467), `cloud-ops-failure-diagnoser` (0.453), `cloud-ops-intake-classifier` (0.449)

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `capacity-risk-forecaster` | no | 0.5644 | 0.3104 | 0.3837 | no | risk | risk |
| `metrics-overview` | no | 0.5644 | 0.4863 | 0.6004 | yes | service, snapshot | service, metric |
| `metrics-root-cause-diagnoser` | no | 0.5644 | 0.3178 | 0.5532 | yes | - | - |

Top similarity neighbours: `slo-breach-checker` (0.564), `resilience-pattern-reviewer` (0.495), `service-mesh-traffic-debugger` (0.487), `metrics-overview` (0.486), `sre-ops-risk-reviewer` (0.475)

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `slo-breach-checker` | no | 0.5465 | 0.4465 | 0.3837 | no | risk, service, slo | risk |
| `metrics-root-cause-diagnoser` | no | 0.5465 | 0.2580 | 0.3033 | no | likely, operational, current, cause | likely |
| `metrics-overview` | no | 0.5465 | 0.2328 | 0.3813 | no | service, snapshot, focu, operational, current | signal |
| `slo-breach-narrative-writer` | no | 0.5465 | 0.4282 | 0.2761 | no | slo, breach | - |
| `public-swebench-slo-implementation` | no | 0.5465 | 0.4037 | 0.2054 | no | service | - |
| `cloud-ops-scenario-planner` | no | 0.5465 | 0.4220 | 0.3419 | no | risk | risk |

Top similarity neighbours: `capacity-risk-forecaster` (0.546), `slo-breach-checker` (0.447), `slo-breach-narrative-writer` (0.428), `risk-ops-failure-diagnoser` (0.427), `cloud-ops-scenario-planner` (0.422)

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `latency-anomaly-detector` | no | 0.5291 | 0.5522 | 0.4881 | yes | service, latency | regression |
| `capacity-risk-forecaster` | no | 0.5291 | 0.3616 | 0.3033 | no | queue, pressure, capacity | likely |
| `incident-summary-writer` | no | 0.5291 | 0.2773 | 0.4900 | no | incident, statu | operational, incident |
| `cloud-ops-failure-diagnoser` | no | 0.5291 | 0.4943 | 0.4128 | yes | - | diagnose |
| `service-mesh-traffic-debugger` | no | 0.5291 | 0.4902 | 0.4282 | yes | service | - |

Top similarity neighbours: `latency-anomaly-detector` (0.552), `metrics-root-cause-diagnoser` (0.529), `cloud-ops-failure-diagnoser` (0.494), `service-mesh-traffic-debugger` (0.490), `public-swebench-distributed-tracing` (0.489)

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `metrics-overview` | no | 0.3814 | 0.2466 | 0.6402 | yes | service, snapshot | metric, operational, summary |
| `metrics-root-cause-diagnoser` | no | 0.3814 | 0.1205 | 0.4900 | no | incident | incident, operational |
| `slo-breach-checker` | no | 0.3814 | 0.1892 | 0.4430 | no | service | metric |
| `incident-ops-summary-writer` | yes | 0.3814 | 0.4126 | 0.7471 | yes | incident | incident, concise, summary |

Top similarity neighbours: `incident-ops-summary-writer` (0.413), `incident-ops-failure-diagnoser` (0.409), `incident-ops-resource-linker` (0.394), `incident-ops-timeline-builder` (0.388), `public-office-microsoft-teams` (0.386)

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `news-briefing-writer` | no | 0.5028 | 0.4618 | 0.7463 | yes | summary, news | news, summary, provid, item, theme, brief |
| `source-grounding-extractor` | no | 0.5028 | 0.4106 | 0.5870 | yes | summary, news | news, summary, provid, content |

Top similarity neighbours: `news-summariser` (0.503), `news-briefing-writer` (0.462), `paper-summariser` (0.449), `general-source-summariser` (0.434), `journalism-ops-summary-writer` (0.426)

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `news-summariser` | no | 0.4626 | 0.3106 | 0.7463 | yes | summary | brief, provid, news, item, summary, theme |
| `tech-news-trend-extractor` | no | 0.4626 | 0.2272 | 0.6218 | yes | signal, just | provid, news |

Top similarity neighbours: `events-ops-summary-writer` (0.498), `news-briefing-writer` (0.463), `events-ops-priority-ranker` (0.441), `incident-summary-writer` (0.432), `events-ops-handoff-brief-writer` (0.423)

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 24

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `news-summariser` | no | 0.3918 | 0.1907 | 0.5870 | yes | - | provid, news, content, summary |
| `news-briefing-writer` | no | 0.3918 | 0.2090 | 0.5504 | yes | - | extract, source-ground, provid, news, need, summary |

Top similarity neighbours: `product-ops-evidence-grounder` (0.545), `vendor-ops-evidence-grounder` (0.477), `marketing-ops-evidence-grounder` (0.476), `ads-ops-evidence-grounder` (0.471), `manufacturing-ops-evidence-grounder` (0.454)

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `tech-news-trend-extractor` | no | 0.6440 | 0.5699 | 0.6820 | yes | acros, tech, news | topic, acros, provid, news, know, appear |
| `news-briefing-writer` | no | 0.6440 | 0.4330 | 0.7072 | yes | extract, theme, news | extract, theme, provid, news, item, summary, brief |

Top similarity neighbours: `news-theme-extractor` (0.644), `tech-news-trend-extractor` (0.570), `news-summariser` (0.455), `related-work-synthesiser` (0.449), `news-briefing-writer` (0.433)

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `news-theme-extractor` | no | 0.7194 | 0.4448 | 0.6820 | yes | pattern, acros, news | news, provid, topic, know, appear, acros |
| `news-briefing-writer` | no | 0.7194 | 0.4735 | 0.6218 | yes | news, why, they, matter | news, provid |

Top similarity neighbours: `tech-news-trend-extractor` (0.719), `news-briefing-writer` (0.473), `social-ops-summary-writer` (0.447), `news-theme-extractor` (0.445), `public-office-news-monitor` (0.438)

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Family: `observability_reliability`
- Gold skill: `prometheus-alert-rule-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-prometheus-configuration` | no | 0.5214 | 0.4248 | 0.5602 | yes | alert, metric | prometheu, alert, metric |
| `slo-breach-checker` | no | 0.5214 | 0.4433 | 0.6031 | yes | metric | metric |
| `grafana-dashboard-builder` | no | 0.5214 | 0.3908 | 0.3794 | no | querie, build, dashboard | threshold |
| `distributed-trace-investigator` | no | 0.5214 | 0.3192 | 0.4400 | no | latency | - |

Top similarity neighbours: `prometheus-alert-rule-writer` (0.521), `ecommerce-ops-monitoring-plan-builder` (0.467), `dashboard-ops-acceptance-test-builder` (0.462), `metrics-overview` (0.453), `dashboard-ops-scenario-planner` (0.451)

### `observability_reliability_p2_grafana_dashboard_builder`

- Family: `observability_reliability`
- Gold skill: `grafana-dashboard-builder`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-grafana-dashboards` | no | 0.7131 | 0.6093 | 0.6667 | yes | grafana, dashboard | build, grafana, dashboard |
| `public-swebench-python-observability` | no | 0.7131 | 0.2322 | 0.2812 | no | - | - |
| `metrics-overview` | no | 0.7131 | 0.4249 | 0.4927 | no | dashboard, service, health | dashboard |
| `prometheus-alert-rule-writer` | no | 0.7131 | 0.4334 | 0.3794 | no | threshold | threshold |
| `dashboard-ops-quality-auditor` | no | 0.7131 | 0.4456 | 0.5019 | yes | dashboard | dashboard |
| `dashboard-ops-monitoring-plan-builder` | no | 0.7131 | 0.4250 | 0.4565 | no | dashboard, threshold | build, dashboard, threshold |

Top similarity neighbours: `grafana-dashboard-builder` (0.713), `public-swebench-grafana-dashboards` (0.609), `dashboard-ops-risk-reviewer` (0.460), `dashboard-ops-compliance-checker` (0.455), `dashboard-ops-quality-auditor` (0.446)

### `observability_reliability_p3_distributed_trace_investigator`

- Family: `observability_reliability`
- Gold skill: `distributed-trace-investigator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-distributed-tracing` | no | 0.4696 | 0.4360 | 0.5285 | yes | acros | distribut |
| `public-swebench-python-observability` | no | 0.4696 | 0.2936 | 0.4399 | no | - | distribut |
| `metrics-root-cause-diagnoser` | no | 0.4696 | 0.2941 | 0.4572 | no | - | - |
| `prometheus-alert-rule-writer` | no | 0.4696 | 0.3218 | 0.4400 | no | - | - |
| `service-mesh-traffic-debugger` | no | 0.4696 | 0.4403 | 0.4770 | yes | service | retrie |
| `latency-anomaly-detector` | no | 0.4696 | 0.4758 | 0.4585 | yes | latency, service | latency |

Top similarity neighbours: `latency-anomaly-detector` (0.476), `implicit-trace-path-diagnoser` (0.471), `distributed-trace-investigator` (0.470), `service-mesh-traffic-debugger` (0.440), `public-swebench-distributed-tracing` (0.436)

### `observability_reliability_p4_slo_breach_narrative_writer`

- Family: `observability_reliability`
- Gold skill: `slo-breach-narrative-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `incident-summary-writer` | no | 0.6331 | 0.6156 | 0.5918 | yes | timeline, impact, action | timeline, impact, action |
| `slo-breach-checker` | no | 0.6331 | 0.3835 | 0.6714 | yes | slo | slo |
| `prometheus-alert-rule-writer` | no | 0.6331 | 0.3490 | 0.5079 | yes | write | write |
| `grafana-dashboard-builder` | no | 0.6331 | 0.1115 | 0.3412 | no | - | - |

Top similarity neighbours: `slo-breach-narrative-writer` (0.633), `incident-summary-writer` (0.616), `incident-ops-summary-writer` (0.547), `meeting-notes-action-extractor` (0.493), `public-oh-my-changelog-maintenance` (0.462)

### `observability_reliability_p5_resilience_pattern_reviewer`

- Family: `observability_reliability`
- Gold skill: `resilience-pattern-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-python-resilience` | no | 0.4603 | 0.4378 | 0.5768 | yes | retry, timeout, backoff | service, retrie, timeout, backoff, failure |
| `dependency-risk-auditor` | no | 0.4603 | 0.2928 | 0.4152 | no | review, risk | review |
| `prometheus-alert-rule-writer` | no | 0.4603 | 0.3162 | 0.4644 | no | - | - |
| `grafana-dashboard-builder` | no | 0.4603 | 0.2133 | 0.4749 | no | - | - |
| `api-security-threat-reviewer` | no | 0.4603 | 0.4060 | 0.4160 | yes | review | review |
| `contract-risk-reviewer` | no | 0.4603 | 0.4002 | 0.4270 | yes | review | review |

Top similarity neighbours: `resilience-pattern-reviewer` (0.460), `public-swebench-python-resilience` (0.438), `api-security-threat-reviewer` (0.406), `contract-risk-reviewer` (0.400), `api-ops-risk-reviewer` (0.387)

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Family: `observability_reliability`
- Gold skill: `service-mesh-traffic-debugger`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-swebench-service-mesh-observability` | no | 0.7188 | 0.4590 | 0.6549 | yes | debug | debug, service, mesh |
| `public-swebench-istio-traffic-management` | no | 0.7188 | 0.4448 | 0.4873 | no | rout, traffic | traffic, service, mesh, rout |
| `public-swebench-linkerd-patterns` | no | 0.7188 | 0.4371 | 0.4581 | no | traffic | traffic, service, mesh |
| `prometheus-alert-rule-writer` | no | 0.7188 | 0.2509 | 0.4411 | no | rule | rule |
| `service-dependency-mapper` | no | 0.7188 | 0.3853 | 0.5218 | yes | - | service |
| `resilience-pattern-reviewer` | no | 0.7188 | 0.2000 | 0.5036 | yes | retrie | service, retrie, configuration |

Top similarity neighbours: `service-mesh-traffic-debugger` (0.719), `public-swebench-service-mesh-observability` (0.459), `public-swebench-istio-traffic-management` (0.445), `public-swebench-linkerd-patterns` (0.437), `service-dependency-mapper` (0.385)

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-ocr-extractor` | no | 0.5425 | 0.4491 | 0.6087 | yes | extract | page |
| `office-to-markdown-converter` | no | 0.5425 | 0.2439 | 0.4780 | no | table | table |
| `public-office-pdf-extraction` | no | 0.5425 | 0.4342 | 0.3743 | no | table, extract | table |
| `public-pdf` | no | 0.5425 | 0.3781 | 0.4328 | no | pdf, table, anyth, form, read, extract | page, pdf, form, table, read |
| `pdf-layout-table-extractor` | no | 0.5425 | 0.5693 | 0.5890 | yes | layout, table, extract, field | page, layout, table |
| `implicit-pdf-table-reconstructor` | no | 0.5425 | 0.4461 | 0.4193 | no | pdf | page, pdf |

Top similarity neighbours: `pdf-layout-table-extractor` (0.569), `pdf-layout-reviewer` (0.542), `public-office-pdf-watermark` (0.489), `psc-pdf-native-extraction-pack` (0.468), `public-office-pdf-form-filler` (0.466)

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | no | 0.6417 | 0.3919 | 0.6087 | yes | pdf, page | page |
| `office-to-markdown-converter` | no | 0.6417 | 0.2515 | 0.5097 | yes | - | preserv |
| `document-field-extractor` | no | 0.6417 | 0.2501 | 0.4120 | no | - | extract |

Top similarity neighbours: `pdf-ocr-extractor` (0.642), `pdf-ocr-cleaner` (0.638), `public-office-pdf-ocr` (0.571), `psc-pdf-scan-ocr-recovery` (0.556), `public-office-smart-ocr` (0.518)

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | no | 0.6431 | 0.3573 | 0.5942 | yes | document | document, preserv |
| `document-rewriter` | no | 0.6431 | 0.4280 | 0.4779 | no | document, substantive | document, preserv, structure |
| `public-docx` | no | 0.6431 | 0.5139 | 0.5794 | yes | docx, word, document, edit, comment, change | document, track, change, comment, word, edit |
| `public-office-docx-manipulation` | no | 0.6431 | 0.4314 | 0.5587 | yes | word, document, edit | document, word, edit |

Top similarity neighbours: `docx-redline-editor` (0.643), `vendor-ops-rewrite-editor` (0.561), `pdf-layout-reviewer` (0.532), `docs-ops-risk-reviewer` (0.531), `pdf-redaction-reviewer` (0.523)

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | no | 0.6680 | 0.2227 | 0.3666 | no | - | spreadsheet |
| `data-analysis-with-validation` | no | 0.6680 | 0.5663 | 0.5297 | yes | assumption, whether | assumption |
| `public-xlsx` | no | 0.6680 | 0.5549 | 0.4351 | no | xlsx, formula, edit, sheet | spreadsheet, formula, reference, sheet |
| `public-office-xlsx-manipulation` | no | 0.6680 | 0.3841 | 0.2712 | no | edit | spreadsheet |
| `psc-data-trust-auditor` | no | 0.6680 | 0.5334 | 0.5952 | yes | audit, assumption, range, whether | audit, spreadsheet, assumption, calculation, analysi |

Top similarity neighbours: `spreadsheet-formula-auditor` (0.668), `xlsx-formula-model-builder` (0.645), `data-analysis-with-validation` (0.566), `public-xlsx` (0.555), `psc-data-trust-auditor` (0.533)

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | no | 0.6682 | 0.2089 | 0.4661 | no | hierarchy | slide, hierarchy |
| `pdf-layout-reviewer` | no | 0.6682 | 0.4179 | 0.6589 | yes | review, visual, alignment | review, visual, alignment |
| `public-pptx` | no | 0.6682 | 0.4032 | 0.4232 | no | pptx, presentation, need, text | presentation, slide, text |
| `public-office-ppt-visual` | no | 0.6682 | 0.5828 | 0.6293 | yes | presentation, visual | presentation, slide, visual |

Top similarity neighbours: `slide-deck-visual-auditor` (0.668), `public-office-ppt-visual` (0.583), `psc-visual-screenshot-reviewer` (0.434), `slide-outline-builder` (0.434), `psc-related-work-synthesizer` (0.420)

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | no | 0.5433 | 0.3664 | 0.4780 | no | table, layout | table |
| `docx-redline-editor` | no | 0.5433 | 0.5413 | 0.5942 | yes | track, change | document, preserv |
| `document-converter` | no | 0.5433 | 0.3757 | 0.6259 | yes | convert, markdown, layout | convert, document, markdown |

Top similarity neighbours: `office-to-markdown-converter` (0.543), `docx-redline-editor` (0.541), `public-markitdown` (0.446), `layout-preserving-converter` (0.444), `public-docx` (0.443)

### `office_business_automation_p1_xlsx_formula_model_builder`

- Family: `office_business_automation`
- Gold skill: `xlsx-formula-model-builder`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-xlsx-manipulation` | no | 0.6088 | 0.2040 | 0.4294 | no | spreadsheet | spreadsheet |
| `public-swebench-xlsx` | no | 0.6088 | 0.2887 | 0.4764 | no | formula, spreadsheet | formula, spreadsheet, input, output, sheet |
| `public-office-data-analysis` | no | 0.6088 | 0.2945 | 0.4398 | no | build, spreadsheet | build, spreadsheet |
| `airtable-workflow-automator` | no | 0.6088 | 0.4446 | 0.5053 | yes | airtable, automation | - |
| `spreadsheet-formula-auditor` | no | 0.6088 | 0.4876 | 0.6240 | yes | formula, spreadsheet | formula, spreadsheet, assumption, sheet |
| `public-office-airtable-automation` | no | 0.6088 | 0.4349 | 0.4236 | no | airtable, automation | - |

Top similarity neighbours: `xlsx-formula-model-builder` (0.609), `spreadsheet-formula-auditor` (0.488), `airtable-workflow-automator` (0.445), `public-office-airtable-automation` (0.435), `public-office-dcf-valuation` (0.399)

### `office_business_automation_p2_airtable_workflow_automator`

- Family: `office_business_automation`
- Gold skill: `airtable-workflow-automator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-airtable-automation` | no | 0.7116 | 0.6708 | 0.8337 | yes | airtable, automation, view, trigger | airtable, view, automation, trigger, integration, workflow |
| `public-office-crm-automation` | no | 0.7116 | 0.3413 | 0.4674 | no | automation | automation, workflow |
| `xlsx-formula-model-builder` | no | 0.7116 | 0.2794 | 0.5053 | yes | - | - |
| `notion-research-database-builder` | no | 0.7116 | 0.3354 | 0.5111 | yes | field | field, workflow |

Top similarity neighbours: `airtable-workflow-automator` (0.712), `public-office-airtable-automation` (0.671), `public-office-intercom-automation` (0.404), `public-office-linear-automation` (0.377), `partnerships-ops-acceptance-test-builder` (0.369)

### `office_business_automation_p3_notion_research_database_builder`

- Family: `office_business_automation`
- Gold skill: `notion-research-database-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | no | 0.6945 | 0.4183 | 0.6671 | yes | notion, database, template | notion, database, template, workflow |
| `public-openai-notion-research-documentation` | no | 0.6945 | 0.5308 | 0.5366 | yes | notion, research | notion, research |
| `xlsx-formula-model-builder` | no | 0.6945 | 0.2361 | 0.4496 | no | structure | - |
| `airtable-workflow-automator` | no | 0.6945 | 0.2830 | 0.5111 | yes | - | field, workflow |

Top similarity neighbours: `notion-research-database-builder` (0.695), `thesis-ops-normalizer` (0.540), `public-openai-notion-research-documentation` (0.531), `thesis-ops-summary-writer` (0.499), `thesis-ops-resource-linker` (0.497)

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Family: `office_business_automation`
- Gold skill: `calendar-scheduling-optimizer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-calendar-automation` | no | 0.4597 | 0.3807 | 0.7150 | yes | meet, schedul | time, calendar, meet, block |
| `meeting-agenda-builder` | no | 0.4597 | 0.4570 | 0.4181 | yes | note, meet | meet |
| `xlsx-formula-model-builder` | no | 0.4597 | 0.0472 | 0.3532 | no | - | - |
| `airtable-workflow-automator` | no | 0.4597 | 0.1876 | 0.3932 | no | - | - |

Top similarity neighbours: `meeting-scheduler` (0.535), `meeting-summary-writer` (0.477), `calendar-scheduling-optimizer` (0.460), `meeting-agenda-builder` (0.457), `meeting-notes-action-extractor` (0.456)

### `office_business_automation_p5_meeting_notes_action_extractor`

- Family: `office_business_automation`
- Gold skill: `meeting-notes-action-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-meeting-notes` | no | 0.6555 | 0.4303 | 0.5451 | yes | - | - |
| `meeting-followup-extractor` | no | 0.6555 | 0.5992 | 0.7336 | yes | extract, action, owner | extract, action, owner, follow-up, meet |
| `xlsx-formula-model-builder` | no | 0.6555 | 0.2451 | 0.3643 | no | - | - |
| `airtable-workflow-automator` | no | 0.6555 | 0.2609 | 0.4419 | no | - | - |

Top similarity neighbours: `meeting-notes-action-extractor` (0.655), `meeting-followup-extractor` (0.599), `weekly-planner` (0.583), `meeting-summary-writer` (0.539), `meeting-agenda-builder` (0.536)

### `office_business_automation_p6_email_classification_router`

- Family: `office_business_automation`
- Gold skill: `email-classification-router`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-email-classifier` | no | 0.6775 | 0.4772 | 0.6024 | yes | email, priority | email, priority, requir, action |
| `public-office-gmail-workflows` | no | 0.6775 | 0.2673 | 0.3930 | no | email | email |
| `public-office-suspicious-email` | no | 0.6775 | 0.4335 | 0.4373 | no | email | email |
| `xlsx-formula-model-builder` | no | 0.6775 | 0.0971 | 0.2803 | no | - | - |
| `email-ops-priority-ranker` | no | 0.6775 | 0.4962 | 0.5299 | yes | email | email |
| `email-action-extractor` | no | 0.6775 | 0.4931 | 0.4894 | no | email | email, action |

Top similarity neighbours: `email-classification-router` (0.677), `email-ops-priority-ranker` (0.496), `email-action-extractor` (0.493), `professor-email-reply` (0.489), `email-ops-risk-reviewer` (0.488)

### `pdf_document_operations_p1_pdf_question_answerer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-question-answerer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 9

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-layout-table-extractor` | no | 0.3983 | 0.2864 | 0.5035 | yes | evidence, page, extract, table, field | page, evidence |
| `pdf-ocr-cleaner` | no | 0.3983 | 0.2021 | 0.5054 | yes | page, ocr, mark | page |
| `pdf-form-filler` | no | 0.3983 | 0.2459 | 0.5017 | yes | pdf, fill, form, field | pdf |
| `pdf-redaction-reviewer` | no | 0.3983 | 0.4215 | 0.5762 | yes | evidence, pdf, redaction, review, sensitive | pdf, content, evidence |

Top similarity neighbours: `psc-pdf-evidence-qa` (0.477), `implicit-pdf-evidence-answerer` (0.465), `travel-ops-compliance-checker` (0.430), `travel-ops-evidence-grounder` (0.429), `compliance-ops-evidence-grounder` (0.426)

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Family: `pdf_document_operations`
- Gold skill: `pdf-layout-table-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | no | 0.5897 | 0.4106 | 0.5035 | yes | pdf, page, answer, question | page, evidence |
| `pdf-ocr-cleaner` | no | 0.5897 | 0.3307 | 0.6220 | yes | page, anchor | pdfs, page |
| `pdf-form-filler` | no | 0.5897 | 0.3532 | 0.4926 | no | pdf | field |
| `pdf-redaction-reviewer` | no | 0.5897 | 0.2891 | 0.4572 | no | pdf | evidence |

Top similarity neighbours: `pdf-layout-table-extractor` (0.590), `public-office-invoice-template` (0.528), `public-office-pdf-extraction` (0.508), `implicit-pdf-table-reconstructor` (0.479), `public-office-pdf-form-filler` (0.440)

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Family: `pdf_document_operations`
- Gold skill: `pdf-ocr-cleaner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | no | 0.7429 | 0.4168 | 0.5054 | yes | page, pdf | page |
| `pdf-layout-table-extractor` | no | 0.7429 | 0.6270 | 0.6220 | yes | page, table, extract | pdfs, page |
| `pdf-form-filler` | no | 0.7429 | 0.3238 | 0.4451 | no | pdf | - |
| `pdf-redaction-reviewer` | no | 0.7429 | 0.3919 | 0.4566 | no | pdf | - |

Top similarity neighbours: `pdf-ocr-cleaner` (0.743), `pdf-ocr-extractor` (0.698), `psc-pdf-scan-ocr-recovery` (0.648), `pdf-layout-table-extractor` (0.627), `public-office-pdf-ocr` (0.626)

### `pdf_document_operations_p4_pdf_form_filler`

- Family: `pdf_document_operations`
- Gold skill: `pdf-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `public-office-pdf-form-filler` | no | 0.4894 | 0.4535 | 0.6335 | yes | pdf | fill, pdf, form |
| `document-field-extractor` | no | 0.4894 | 0.2915 | 0.3294 | no | - | field |
| `pdf-question-answerer` | no | 0.4894 | 0.2822 | 0.5017 | yes | pdf | pdf |
| `pdf-layout-table-extractor` | no | 0.4894 | 0.3075 | 0.4926 | no | - | field |

Top similarity neighbours: `pdf-form-filler` (0.489), `public-office-pdf-form-filler` (0.454), `public-office-expense-tracker` (0.449), `receipt-extractor` (0.428), `invoice-payment-checker` (0.423)

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-redaction-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `privacy-risk-reviewer` | no | 0.5848 | 0.2339 | 0.4973 | no | - | review, risk |
| `public-office-contract-review` | no | 0.5848 | 0.4120 | 0.4852 | no | - | risk |
| `public-openai-pdf` | no | 0.5848 | 0.3511 | 0.3958 | no | pdf, such | review, pdf |
| `pdf-question-answerer` | no | 0.5848 | 0.4262 | 0.5762 | yes | pdf | pdf, content, evidence |
| `pdf-layout-reviewer` | no | 0.5848 | 0.4419 | 0.6378 | yes | pdf | review, pdf, risk |

Top similarity neighbours: `pdf-redaction-reviewer` (0.585), `psc-pdf-redaction-pass` (0.547), `psc-pdf-evidence-qa` (0.442), `pdf-layout-reviewer` (0.442), `public-office-pdf-watermark` (0.440)

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Family: `pdf_document_operations`
- Gold skill: `pdf-to-docx-converter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | no | 0.6068 | 0.3637 | 0.4143 | no | pdf, answer, question | pdf |
| `pdf-layout-table-extractor` | no | 0.6068 | 0.5387 | 0.5832 | yes | table, preserv | preserv, table |
| `pdf-ocr-cleaner` | no | 0.6068 | 0.3279 | 0.5004 | yes | - | - |
| `pdf-form-filler` | no | 0.6068 | 0.3483 | 0.4258 | no | pdf | pdf |

Top similarity neighbours: `pdf-to-docx-converter` (0.607), `pdf-layout-table-extractor` (0.539), `layout-preserving-converter` (0.496), `implicit-pdf-table-reconstructor` (0.474), `public-office-pdf-extraction` (0.434)

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `weekly-planner` | no | 0.6178 | 0.4975 | 0.6665 | yes | need, week, extract | note, need, structur, plan |
| `task-extractor` | no | 0.6178 | 0.5337 | 0.6002 | yes | need, extract | note, need, plan, summary |

Top similarity neighbours: `meeting-agenda-builder` (0.618), `task-extractor` (0.534), `meeting-summary-writer` (0.526), `meeting-ops-summary-writer` (0.515), `meeting-followup-extractor` (0.513)

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `meeting-followup-extractor` | no | 0.6305 | 0.4959 | 0.6969 | yes | meet, summary | summary, complet, meet, need, list |
| `task-extractor` | no | 0.6305 | 0.4663 | 0.6053 | yes | summary, note | summary, need, plan |

Top similarity neighbours: `meeting-summary-writer` (0.630), `meeting-notes-action-extractor` (0.589), `meeting-ops-summary-writer` (0.584), `meeting-agenda-builder` (0.530), `meeting-ops-rewrite-editor` (0.520)

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `meeting-summary-writer` | no | 0.6518 | 0.4745 | 0.6969 | yes | meet | complet, meet, need, list, summary |
| `task-extractor` | no | 0.6518 | 0.5136 | 0.6783 | yes | extract, note | extract, need, summary |

Top similarity neighbours: `meeting-notes-action-extractor` (0.654), `meeting-followup-extractor` (0.652), `task-extractor` (0.514), `public-office-meeting-notes` (0.482), `meeting-agenda-builder` (0.476)

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `weekly-planner` | no | 0.5491 | 0.5707 | 0.6026 | yes | note, schedul, week | plan, extract, note, need, schedul, weekly |
| `meeting-followup-extractor` | no | 0.5491 | 0.4481 | 0.6783 | yes | list, complet, meet | extract, need, summary |

Top similarity neighbours: `weekly-planner` (0.571), `meeting-notes-action-extractor` (0.557), `task-extractor` (0.549), `meeting-summary-writer` (0.481), `meeting-followup-extractor` (0.448)

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `task-extractor` | no | 0.6423 | 0.4257 | 0.6026 | yes | plan, need, summary, extract | weekly, plan, need, schedul, extract, note |
| `meeting-agenda-builder` | no | 0.6423 | 0.4537 | 0.6665 | yes | meet, plan, need, summary, agenda | plan, need, structur, note |

Top similarity neighbours: `weekly-planner` (0.642), `meeting-ops-scenario-planner` (0.499), `ux-ops-scenario-planner` (0.483), `thesis-ops-scenario-planner` (0.483), `repo-ops-scenario-planner` (0.466)

### `public_like_extra_p01_pdf_invoice_rows`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 22

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-scan-ocr-recovery` | no | 0.4195 | 0.3684 | 0.8519 | yes | pdf, text, extract, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.4195 | 0.3759 | 0.8106 | yes | pdf, extract, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.4195 | 0.3495 | 0.8384 | yes | pdf, extract, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |

Top similarity neighbours: `procurement-ops-summary-writer` (0.532), `procurement-risk-summariser` (0.506), `vendor-ops-summary-writer` (0.495), `procurement-ops-quality-auditor` (0.486), `procurement-ops-risk-reviewer` (0.481)

### `public_like_extra_p02_scanned_appendix_recovery`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.5131 | 0.3527 | 0.8519 | yes | page, text | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.5131 | 0.3606 | 0.8227 | yes | page | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.5131 | 0.3427 | 0.8428 | yes | page | pdf, document, page, workflow, involv, extract, ocr, recovery |

Top similarity neighbours: `pdf-ocr-cleaner` (0.548), `pdf-ocr-extractor` (0.546), `psc-pdf-scan-ocr-recovery` (0.513), `pdf-layout-reviewer` (0.398), `public-office-smart-ocr` (0.392)

### `public_like_extra_p03_pdf_claim_answer`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 15

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.3942 | 0.4182 | 0.8106 | yes | answer, pdf, page, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.3942 | 0.4116 | 0.8227 | yes | answer, pdf, page, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-redaction-pass` | no | 0.3942 | 0.3593 | 0.8734 | yes | answer, pdf, page, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |

Top similarity neighbours: `insurance-ops-artifact-packager` (0.426), `pdf-ocr-extractor` (0.424), `legal-ops-artifact-packager` (0.419), `psc-pdf-native-extraction-pack` (0.418), `legal-discovery-ops-artifact-packager` (0.415)

### `public_like_extra_p04_pdf_hidden_redaction_check`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.5221 | 0.4366 | 0.8384 | yes | shar, pdf, metadata, text | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.5221 | 0.4256 | 0.8428 | yes | shar, pdf, text | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-evidence-qa` | no | 0.5221 | 0.4193 | 0.8734 | yes | shar, pdf | document, external, shar, pdf, workflow, involv, extract, ocr |

Top similarity neighbours: `psc-pdf-redaction-pass` (0.522), `public-office-chat-with-pdf` (0.515), `public-pdf` (0.490), `public-office-pdf-watermark` (0.473), `public-office-pdf-ocr` (0.471)

### `public_like_extra_p05_source_claim_table`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-related-work-synthesizer` | no | 0.4892 | 0.2567 | 0.7491 | yes | claim | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-paper-method-mapper` | no | 0.4892 | 0.2916 | 0.7904 | yes | claim | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-source-field-table-extractor` | no | 0.4892 | 0.2919 | 0.8030 | yes | claim | claim, evidence, research-read, workflow, involv, paper, method, compare |

Top similarity neighbours: `citation-grounding-helper` (0.583), `psc-citation-claim-support-auditor` (0.489), `citation-note-extractor` (0.420), `source-grounding-extractor` (0.368), `publishing-ops-evidence-grounder` (0.366)

### `public_like_extra_p06_method_design_map`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-paper-method-mapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 55

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | no | 0.2961 | 0.1352 | 0.7904 | yes | paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-related-work-synthesizer` | no | 0.2961 | 0.2071 | 0.8210 | yes | paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-source-field-table-extractor` | no | 0.2961 | 0.1867 | 0.8221 | yes | paper | method, research-read, workflow, involv, paper, claim, evidence, compare |

Top similarity neighbours: `lab-ops-summary-writer` (0.450), `lab-ops-dependency-mapper` (0.411), `lab-ops-rewrite-editor` (0.406), `lab-ops-intake-classifier` (0.400), `lab-ops-artifact-packager` (0.389)

### `public_like_extra_p07_related_work_theme_draft`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | no | 0.4767 | 0.3420 | 0.7491 | yes | paper | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-paper-method-mapper` | no | 0.4767 | 0.4100 | 0.8210 | yes | paper | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-source-field-table-extractor` | no | 0.4767 | 0.4321 | 0.8039 | yes | paper | paper, thesi, research-read, workflow, involv, claim, method, evidence |

Top similarity neighbours: `related-work-synthesiser` (0.605), `method-note-builder` (0.600), `note-linker` (0.530), `citation-note-extractor` (0.514), `paper-summariser` (0.498)

### `public_like_extra_p08_source_fact_table`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 22

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | no | 0.3920 | 0.2476 | 0.8030 | yes | paper | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-paper-method-mapper` | no | 0.3920 | 0.3558 | 0.8221 | yes | extract, evaluation, paper | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-related-work-synthesizer` | no | 0.3920 | 0.2238 | 0.8039 | yes | paper, synthesize | compare, research-read, workflow, involv, paper, claim, method, evidence |

Top similarity neighbours: `public-office-data-analysis` (0.470), `psc-executive-metric-narrator` (0.469), `skill-benchmark-evaluator` (0.458), `psc-decision-ranking-analyst` (0.448), `dataset-ops-risk-reviewer` (0.447)

### `public_like_extra_p09_data_quality_gate`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-data-trust-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 34

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-anomaly-watchlist-builder` | no | 0.3680 | 0.3570 | 0.7577 | yes | report | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-decision-ranking-analyst` | no | 0.3680 | 0.2628 | 0.7717 | yes | report | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-executive-metric-narrator` | no | 0.3680 | 0.2477 | 0.7399 | yes | report | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |

Top similarity neighbours: `k8s-ops-quality-auditor` (0.484), `k8s-ops-failure-diagnoser` (0.462), `manufacturing-ops-failure-diagnoser` (0.409), `dataset-ops-quality-auditor` (0.406), `warehouse-ops-quality-auditor` (0.404)

### `public_like_extra_p10_anomaly_watchlist_export`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.5128 | 0.2589 | 0.7577 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.5128 | 0.2632 | 0.6996 | yes | evidence | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-executive-metric-narrator` | no | 0.5128 | 0.2936 | 0.6756 | yes | executive | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.513), `operations-ops-summary-writer` (0.487), `finance-ops-failure-diagnoser` (0.484), `operations-ops-failure-diagnoser` (0.475), `public-oh-my-changelog-maintenance` (0.472)

### `public_like_extra_p11_vendor_decision_ranking`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 21

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.4676 | 0.2406 | 0.7717 | yes | value, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-anomaly-watchlist-builder` | no | 0.4676 | 0.2253 | 0.6996 | yes | rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-executive-metric-narrator` | no | 0.4676 | 0.2622 | 0.7614 | yes | risk, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |

Top similarity neighbours: `vendor-ops-priority-ranker` (0.640), `vendor-ops-comparison-builder` (0.575), `vendor-ops-risk-reviewer` (0.545), `procurement-ops-priority-ranker` (0.526), `vendor-ops-summary-writer` (0.524)

### `public_like_extra_p12_board_metric_story`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.4518 | 0.2900 | 0.7399 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-anomaly-watchlist-builder` | no | 0.4518 | 0.2362 | 0.6756 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.4518 | 0.3079 | 0.7614 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-executive-metric-narrator` (0.452), `k8s-ops-summary-writer` (0.414), `knowledge-ops-summary-writer` (0.400), `k8s-ops-quality-auditor` (0.388), `k8s-ops-risk-reviewer` (0.370)

### `public_like_extra_p13_ci_failure_first_cause`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pr-thread-fix-planner` | no | 0.5269 | 0.2797 | 0.7282 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-repo-guardrail-hook-installer` | no | 0.5269 | 0.1244 | 0.6133 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-release-communication-packager` | no | 0.5269 | 0.1579 | 0.6780 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |

Top similarity neighbours: `implicit-ci-failure-reader` (0.569), `ci-log-root-cause-debugger` (0.553), `psc-ci-log-first-failure-reader` (0.527), `ci-failure-debugger` (0.514), `manufacturing-ops-failure-diagnoser` (0.449)

### `public_like_extra_p14_review_thread_patch_plan`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.5022 | 0.3415 | 0.7282 | yes | request | extract, request, review, thread, code, verification, github, repository |
| `psc-repo-guardrail-hook-installer` | no | 0.5022 | 0.4461 | 0.7902 | yes | request | extract, request, review, thread, code, verification, github, repository |
| `psc-release-communication-packager` | no | 0.5022 | 0.4559 | 0.8423 | yes | request, change | extract, request, review, thread, code, verification, github, repository |

Top similarity neighbours: `pr-review-comment-resolver` (0.511), `psc-pr-thread-fix-planner` (0.502), `psc-release-communication-packager` (0.456), `public-oh-my-file-organization` (0.447), `psc-repo-guardrail-hook-installer` (0.446)

### `public_like_extra_p15_repo_hook_guardrail`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.4907 | 0.2595 | 0.6133 | yes | verification | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-pr-thread-fix-planner` | no | 0.4907 | 0.2943 | 0.7902 | yes | verification | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-release-communication-packager` | no | 0.4907 | 0.2900 | 0.7938 | yes | verification | repository, hook, verification, github, maintenance, workflow, involv, extract |

Top similarity neighbours: `git-safety-guardrail-installer` (0.576), `psc-repo-guardrail-hook-installer` (0.491), `public-oh-my-setup-pre-commit` (0.452), `public-mattpocock-git-guardrails-claude-code` (0.449), `public-mattpocock-setup-pre-commit` (0.427)

### `public_like_extra_p16_release_note_packaging`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-release-communication-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.6004 | 0.3976 | 0.6780 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |
| `psc-pr-thread-fix-planner` | no | 0.6004 | 0.4342 | 0.8423 | yes | release, change, note | release, note, github, repository, maintenance, workflow, involv, extract |
| `psc-repo-guardrail-hook-installer` | no | 0.6004 | 0.3654 | 0.7938 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |

Top similarity neighbours: `release-changelog-generator` (0.660), `psc-release-communication-packager` (0.600), `release-note-writer` (0.522), `public-office-changelog-generator` (0.512), `pr-review-comment-resolver` (0.508)

### `public_like_extra_p17_hf_dataset_card_check`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 11

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-local-model-fit-selector` | no | 0.3882 | 0.1764 | 0.8221 | yes | dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-sentence-embedding-trainer` | no | 0.3882 | 0.2258 | 0.7333 | yes | dataset, split, retrieval | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.3882 | 0.1998 | 0.8565 | yes | dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |

Top similarity neighbours: `hf-dataset-viewer-inspector` (0.525), `implicit-hf-dataset-inspector` (0.482), `public-huggingface-datasets` (0.474), `dataset-ops-artifact-packager` (0.442), `context-retriever` (0.427)

### `public_like_extra_p18_local_model_constraints`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 108

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.2197 | 0.1861 | 0.8221 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-sentence-embedding-trainer` | no | 0.2197 | 0.3027 | 0.7528 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.2197 | 0.2007 | 0.8111 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |

Top similarity neighbours: `public-swebench-v3-performance-optimization` (0.368), `web-performance-budget-checker` (0.360), `public-swebench-llm-evaluation` (0.354), `public-swebench-vector-index-tuning` (0.346), `public-swebench-python-performance-optimization` (0.333)

### `public_like_extra_p19_embedding_training_run`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.4599 | 0.1115 | 0.7333 | yes | train, split | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-local-model-fit-selector` | no | 0.4599 | 0.0670 | 0.7528 | yes | train | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-hf-space-deployment-preparer` | no | 0.4599 | 0.0832 | 0.6647 | yes | train | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |

Top similarity neighbours: `sentence-transformer-finetuner` (0.572), `public-huggingface-train-sentence-transformers` (0.476), `psc-sentence-embedding-trainer` (0.460), `search-ops-rewrite-editor` (0.352), `search-ops-summary-writer` (0.340)

### `public_like_extra_p20_space_deploy_readiness`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 52

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.3305 | 0.1920 | 0.8565 | yes | demo, deployment, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-local-model-fit-selector` | no | 0.3305 | 0.1459 | 0.8111 | yes | demo, deployment, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-sentence-embedding-trainer` | no | 0.3305 | 0.0935 | 0.6647 | yes | demo, deployment, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |

Top similarity neighbours: `public-huggingface-huggingface-gradio` (0.614), `gradio-demo-builder` (0.611), `deployment-release-verifier` (0.455), `deployment-build-triager` (0.411), `public-swebench-springboot-tdd` (0.404)

### `public_like_extra_p21_feature_threat_model`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-privacy-telemetry-reviewer` | no | 0.5592 | 0.3033 | 0.6551 | yes | feature, mitigation, risk, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-dependency-supply-chain-auditor` | no | 0.5592 | 0.4564 | 0.7333 | yes | feature, mitigation, risk, dependency | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-handler-vulnerability-reviewer` | no | 0.5592 | 0.4647 | 0.7716 | yes | feature, path, mitigation, risk, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |

Top similarity neighbours: `public-security-threat-model` (0.619), `security-threat-modeler` (0.575), `psc-feature-threat-modeler` (0.559), `security-ops-dependency-mapper` (0.500), `security-ops-resource-linker` (0.482)

### `public_like_extra_p22_privacy_telemetry_review`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 14

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.4711 | 0.2770 | 0.6551 | yes | data | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-dependency-supply-chain-auditor` | no | 0.4711 | 0.2463 | 0.6273 | yes | data | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-handler-vulnerability-reviewer` | no | 0.4711 | 0.2684 | 0.6960 | yes | review, data, path | privacy, data, application-security, workflow, involv, risk, code, feature |

Top similarity neighbours: `privacy-risk-reviewer` (0.577), `analytics-ops-risk-reviewer` (0.558), `analytics-ops-summary-writer` (0.531), `analytics-ops-compliance-checker` (0.517), `privacy-ops-summary-writer` (0.504)

### `public_like_extra_p23_supply_chain_audit`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.5654 | 0.4201 | 0.7333 | yes | threat-model, feature | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.5654 | 0.2071 | 0.6273 | yes | feature | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-handler-vulnerability-reviewer` | no | 0.5654 | 0.3665 | 0.7442 | yes | feature | risk, dependencie, application-security, workflow, involv, code, feature, privacy |

Top similarity neighbours: `dependency-risk-auditor` (0.656), `psc-dependency-supply-chain-auditor` (0.565), `risk-ops-artifact-packager` (0.560), `security-ops-artifact-packager` (0.525), `product-ops-artifact-packager` (0.481)

### `public_like_extra_p24_handler_vulnerability_review`

- Family: `public_like_extra_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.3662 | 0.1649 | 0.7716 | yes | abuse | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.3662 | 0.1935 | 0.6960 | yes | review | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-dependency-supply-chain-auditor` | no | 0.3662 | 0.1572 | 0.7442 | yes | - | code, application-security, workflow, involv, risk, feature, dependencie, privacy |

Top similarity neighbours: `security-code-reviewer` (0.366), `psc-handler-vulnerability-reviewer` (0.366), `security-ops-resource-linker` (0.347), `security-ops-rewrite-editor` (0.345), `secret-leak-scanner` (0.338)

### `psc_browser_quality_p01_1_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 20

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-playwright-regression-suite` | no | 0.1674 | 0.1082 | 0.7628 | yes | browser, evidence | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-visual-screenshot-reviewer` | no | 0.1674 | 0.1052 | 0.7625 | yes | browser, evidence, state | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-accessibility-interaction-auditor` | no | 0.1674 | 0.1135 | 0.7410 | yes | browser, evidence, state | web, interaction, screenshot, runtime, browser, quality, workflow, involv |

Top similarity neighbours: `frontend-debugger` (0.290), `web-ui-tester` (0.265), `ads-ops-failure-diagnoser` (0.229), `implicit-browser-flow-investigator` (0.218), `ads-ops-acceptance-test-builder` (0.214)

### `psc_browser_quality_p01_2_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-playwright-regression-suite` | no | 0.4944 | 0.4989 | 0.7628 | yes | evidence, interaction, failure, screenshot, playwright, assertion | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-visual-screenshot-reviewer` | no | 0.4944 | 0.3275 | 0.7625 | yes | evidence, interaction, state, screenshot | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-accessibility-interaction-auditor` | no | 0.4944 | 0.3670 | 0.7410 | yes | evidence, interaction, state, screenshot | web, interaction, screenshot, runtime, browser, quality, workflow, involv |

Top similarity neighbours: `playwright-flow-debugger` (0.625), `frontend-debugger` (0.508), `psc-playwright-regression-suite` (0.499), `psc-devtools-runtime-diagnoser` (0.494), `public-addy-agent-browser-testing-with-devtools` (0.480)

### `psc_browser_quality_p02_1_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.5970 | 0.4079 | 0.7628 | yes | browser, regression, evidence, runtime, console, error, screenshot, accessibility | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-visual-screenshot-reviewer` | no | 0.5970 | 0.4098 | 0.7518 | yes | browser, regression, evidence, runtime, screenshot, accessibility | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-accessibility-interaction-auditor` | no | 0.5970 | 0.4035 | 0.6817 | yes | browser, regression, evidence, runtime, screenshot, audit, accessibility | interaction, screenshot, browser, quality, workflow, involv, web, page |

Top similarity neighbours: `psc-playwright-regression-suite` (0.597), `ecommerce-ops-acceptance-test-builder` (0.457), `fundraising-ops-acceptance-test-builder` (0.452), `ads-ops-acceptance-test-builder` (0.452), `sales-ops-acceptance-test-builder` (0.438)

### `psc_browser_quality_p02_2_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.5230 | 0.3799 | 0.7628 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-visual-screenshot-reviewer` | no | 0.5230 | 0.3444 | 0.7518 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-accessibility-interaction-auditor` | no | 0.5230 | 0.2764 | 0.6817 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |

Top similarity neighbours: `psc-playwright-regression-suite` (0.523), `sales-ops-acceptance-test-builder` (0.472), `contract-ops-acceptance-test-builder` (0.471), `ads-ops-acceptance-test-builder` (0.470), `procurement-ops-acceptance-test-builder` (0.470)

### `psc_browser_quality_p03_1_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.5190 | 0.2735 | 0.7625 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-playwright-regression-suite` | no | 0.5190 | 0.3277 | 0.7518 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-accessibility-interaction-auditor` | no | 0.5190 | 0.3759 | 0.8210 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |

Top similarity neighbours: `psc-visual-screenshot-reviewer` (0.519), `visual-regression-checker` (0.519), `implicit-visual-diff-reviewer` (0.489), `pdf-layout-reviewer` (0.444), `mobile-ops-rewrite-editor` (0.442)

### `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.6051 | 0.4138 | 0.7625 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-playwright-regression-suite` | no | 0.6051 | 0.4394 | 0.7518 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-accessibility-interaction-auditor` | no | 0.6051 | 0.4639 | 0.8210 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |

Top similarity neighbours: `visual-regression-checker` (0.712), `implicit-visual-diff-reviewer` (0.688), `psc-visual-screenshot-reviewer` (0.605), `psc-accessibility-interaction-auditor` (0.464), `psc-playwright-regression-suite` (0.439)

### `psc_browser_quality_p04_1_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.4894 | 0.2972 | 0.7410 | yes | error | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-playwright-regression-suite` | no | 0.4894 | 0.2501 | 0.6817 | yes | navigation, form | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-visual-screenshot-reviewer` | no | 0.4894 | 0.3659 | 0.8210 | yes | - | web, interaction, browser, quality, workflow, involv, page, screenshot |

Top similarity neighbours: `accessibility-interaction-auditor` (0.509), `psc-accessibility-interaction-auditor` (0.489), `writing-ops-quality-auditor` (0.454), `public-addy-web-accessibility` (0.439), `email-ops-quality-auditor` (0.421)

### `psc_browser_quality_p04_2_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | no | 0.6815 | 0.3769 | 0.7410 | yes | web, accessibility, interaction, quality, state, error | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-playwright-regression-suite` | no | 0.6815 | 0.3849 | 0.6817 | yes | web, form, accessibility, interaction, quality | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-visual-screenshot-reviewer` | no | 0.6815 | 0.4670 | 0.8210 | yes | web, accessibility, interaction, quality, state | web, interaction, browser, quality, workflow, involv, page, screenshot |

Top similarity neighbours: `accessibility-interaction-auditor` (0.759), `accessibility-checker` (0.691), `psc-accessibility-interaction-auditor` (0.681), `public-addy-web-accessibility` (0.549), `psc-visual-screenshot-reviewer` (0.467)

### `psc_data_analysis_intent_p01_1_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-anomaly-watchlist-builder` | no | 0.3965 | 0.3782 | 0.7577 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-decision-ranking-analyst` | no | 0.3965 | 0.2397 | 0.7717 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-executive-metric-narrator` | no | 0.3965 | 0.1982 | 0.7399 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |

Top similarity neighbours: `psc-data-trust-auditor` (0.397), `data-analysis-with-validation` (0.387), `psc-anomaly-watchlist-builder` (0.378), `dataset-ops-failure-diagnoser` (0.329), `real-estate-ops-failure-diagnoser` (0.324)

### `psc_data_analysis_intent_p01_2_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-anomaly-watchlist-builder` | no | 0.7167 | 0.5013 | 0.7577 | yes | data, quality, rank | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-decision-ranking-analyst` | no | 0.7167 | 0.5559 | 0.7717 | yes | data, quality, rank, recommendation | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-executive-metric-narrator` | no | 0.7167 | 0.4916 | 0.7399 | yes | data, quality, rank, executive | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |

Top similarity neighbours: `psc-data-trust-auditor` (0.717), `data-analysis-with-validation` (0.653), `psc-decision-ranking-analyst` (0.556), `spreadsheet-formula-auditor` (0.555), `dashboard-ops-quality-auditor` (0.529)

### `psc_data_analysis_intent_p02_1_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.4951 | 0.2599 | 0.7577 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.4951 | 0.2317 | 0.6996 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-executive-metric-narrator` | no | 0.4951 | 0.2418 | 0.6756 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `latency-anomaly-detector` (0.542), `psc-anomaly-watchlist-builder` (0.495), `search-ops-monitoring-plan-builder` (0.431), `library-ops-monitoring-plan-builder` (0.425), `publishing-ops-monitoring-plan-builder` (0.414)

### `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.6858 | 0.4093 | 0.7577 | yes | csv, report | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.6858 | 0.3282 | 0.6996 | yes | csv, evidence, report | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-executive-metric-narrator` | no | 0.6858 | 0.3855 | 0.6756 | yes | csv, turn, report, brief | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.686), `data-analysis-with-anomaly-focus` (0.587), `incident-summary-writer` (0.499), `events-ops-quality-auditor` (0.492), `latency-anomaly-detector` (0.467)

### `psc_data_analysis_intent_p03_1_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 133

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.3366 | 0.1682 | 0.7717 | yes | rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-anomaly-watchlist-builder` | no | 0.3366 | 0.1100 | 0.6996 | yes | rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-executive-metric-narrator` | no | 0.3366 | 0.2207 | 0.7614 | yes | rank, risk | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |

Top similarity neighbours: `risk-ops-comparison-builder` (0.476), `travel-ops-comparison-builder` (0.474), `travel-ops-priority-ranker` (0.474), `risk-ops-priority-ranker` (0.462), `robotics-ops-priority-ranker` (0.430)

### `psc_data_analysis_intent_p03_2_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.5147 | 0.2807 | 0.7717 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-anomaly-watchlist-builder` | no | 0.5147 | 0.2473 | 0.6996 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-executive-metric-narrator` | no | 0.5147 | 0.3643 | 0.7614 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |

Top similarity neighbours: `data-analysis-for-ranking-selection` (0.609), `psc-decision-ranking-analyst` (0.515), `dataset-ops-priority-ranker` (0.451), `decision-matrix-builder` (0.437), `priority-sorter` (0.429)

### `psc_data_analysis_intent_p04_1_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.5239 | 0.2640 | 0.7399 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-anomaly-watchlist-builder` | no | 0.5239 | 0.3190 | 0.6756 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.5239 | 0.3829 | 0.7614 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-executive-metric-narrator` (0.524), `meeting-ops-priority-ranker` (0.453), `meeting-ops-summary-writer` (0.447), `risk-ops-summary-writer` (0.438), `data-analysis-for-reporting` (0.436)

### `psc_data_analysis_intent_p04_2_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | no | 0.6677 | 0.4719 | 0.7399 | yes | metric, spreadsheet, busines, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-anomaly-watchlist-builder` | no | 0.6677 | 0.4475 | 0.6756 | yes | metric, spreadsheet, busines, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | no | 0.6677 | 0.4188 | 0.7614 | yes | metric, spreadsheet, busines, action, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-executive-metric-narrator` (0.668), `operations-ops-summary-writer` (0.608), `personal-ops-summary-writer` (0.578), `dashboard-ops-summary-writer` (0.569), `finance-ops-summary-writer` (0.561)

### `psc_github_maintenance_p01_1_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pr-thread-fix-planner` | no | 0.4716 | 0.2467 | 0.7282 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-repo-guardrail-hook-installer` | no | 0.4716 | 0.1062 | 0.6133 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-release-communication-packager` | no | 0.4716 | 0.1806 | 0.6780 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |

Top similarity neighbours: `ci-failure-debugger` (0.517), `implicit-ci-failure-reader` (0.488), `psc-ci-log-first-failure-reader` (0.472), `ci-log-root-cause-debugger` (0.455), `construction-ops-failure-diagnoser` (0.429)

### `psc_github_maintenance_p01_2_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pr-thread-fix-planner` | no | 0.7010 | 0.4783 | 0.7282 | yes | github, review, release, note | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-repo-guardrail-hook-installer` | no | 0.7010 | 0.3927 | 0.6133 | yes | github, review, release | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-release-communication-packager` | no | 0.7010 | 0.4639 | 0.6780 | yes | github, turn, review, release, note | github, repository, maintenance, workflow, involv, extract, request, review |

Top similarity neighbours: `psc-ci-log-first-failure-reader` (0.701), `ci-failure-debugger` (0.635), `public-swebench-analyze-ci` (0.619), `pr-reviewer` (0.599), `github-issue-triager` (0.534)

### `psc_github_maintenance_p02_1_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.5172 | 0.3017 | 0.7282 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |
| `psc-repo-guardrail-hook-installer` | no | 0.5172 | 0.3374 | 0.7902 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |
| `psc-release-communication-packager` | no | 0.5172 | 0.3613 | 0.8423 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |

Top similarity neighbours: `implicit-review-comment-planner` (0.552), `pr-review-comment-resolver` (0.525), `psc-pr-thread-fix-planner` (0.517), `public-mattpocock-review` (0.477), `pr-reviewer` (0.432)

### `psc_github_maintenance_p02_2_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 5

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.6220 | 0.5321 | 0.7282 | yes | review, github, thread, code | extract, request, review, thread, code, verification, github, repository |
| `psc-repo-guardrail-hook-installer` | no | 0.6220 | 0.4584 | 0.7902 | yes | review, github, thread, code | extract, request, review, thread, code, verification, github, repository |
| `psc-release-communication-packager` | no | 0.6220 | 0.5301 | 0.8423 | yes | review, github, thread, code, change | extract, request, review, thread, code, verification, github, repository |

Top similarity neighbours: `pr-review-comment-resolver` (0.711), `pr-reviewer` (0.704), `review-comment-resolver` (0.673), `repo-code-reviewer` (0.636), `psc-pr-thread-fix-planner` (0.622)

### `psc_github_maintenance_p03_1_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.5622 | 0.3737 | 0.6133 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-pr-thread-fix-planner` | no | 0.5622 | 0.4295 | 0.7902 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-release-communication-packager` | no | 0.5622 | 0.4965 | 0.7938 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |

Top similarity neighbours: `git-safety-guardrail-installer` (0.621), `psc-repo-guardrail-hook-installer` (0.562), `public-mattpocock-git-guardrails-claude-code` (0.504), `psc-release-communication-packager` (0.496), `public-openai-security-ownership-map` (0.496)

### `psc_github_maintenance_p03_2_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.6767 | 0.3873 | 0.6133 | yes | hook, verification | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-pr-thread-fix-planner` | no | 0.6767 | 0.5025 | 0.7902 | yes | hook, verification, step | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-release-communication-packager` | no | 0.6767 | 0.4810 | 0.7938 | yes | hook, verification | repository, hook, verification, github, maintenance, workflow, involv, extract |

Top similarity neighbours: `git-safety-guardrail-installer` (0.730), `psc-repo-guardrail-hook-installer` (0.677), `public-mattpocock-git-guardrails-claude-code` (0.665), `version-control-helper` (0.504), `psc-pr-thread-fix-planner` (0.502)

### `psc_github_maintenance_p04_1_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.5738 | 0.2799 | 0.6780 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |
| `psc-pr-thread-fix-planner` | no | 0.5738 | 0.4353 | 0.8423 | yes | note, release, change | release, note, github, repository, maintenance, workflow, involv, extract |
| `psc-repo-guardrail-hook-installer` | no | 0.5738 | 0.3194 | 0.7938 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |

Top similarity neighbours: `psc-release-communication-packager` (0.574), `release-note-writer` (0.550), `public-office-changelog-generator` (0.542), `release-changelog-generator` (0.536), `public-oh-my-changelog-maintenance` (0.485)

### `psc_github_maintenance_p04_2_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | no | 0.6244 | 0.3632 | 0.6780 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |
| `psc-pr-thread-fix-planner` | no | 0.6244 | 0.4766 | 0.8423 | yes | release, change, note | release, note, github, repository, maintenance, workflow, involv, extract |
| `psc-repo-guardrail-hook-installer` | no | 0.6244 | 0.3773 | 0.7938 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |

Top similarity neighbours: `release-changelog-generator` (0.724), `public-oh-my-changelog-maintenance` (0.663), `psc-release-communication-packager` (0.624), `release-note-writer` (0.618), `public-swebench-changelog-automation` (0.614)

### `psc_huggingface_workflow_p01_1_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-local-model-fit-selector` | no | 0.6053 | 0.4097 | 0.8221 | yes | hugg, face, dataset, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-sentence-embedding-trainer` | no | 0.6053 | 0.4318 | 0.7333 | yes | hugg, face, dataset, split, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.6053 | 0.4034 | 0.8565 | yes | hugg, face, dataset, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |

Top similarity neighbours: `psc-hf-dataset-card-inspector` (0.605), `public-huggingface-datasets` (0.604), `hf-dataset-viewer-inspector` (0.590), `public-huggingface-huggingface-vision-trainer` (0.493), `hf-community-eval-runner` (0.480)

### `psc_huggingface_workflow_p01_2_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-local-model-fit-selector` | no | 0.4505 | 0.2521 | 0.8221 | yes | train, dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-sentence-embedding-trainer` | no | 0.4505 | 0.2728 | 0.7333 | yes | train, dataset, split | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.4505 | 0.2876 | 0.8565 | yes | train, dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |

Top similarity neighbours: `dataset-ops-risk-reviewer` (0.466), `dataset-ops-acceptance-test-builder` (0.459), `psc-hf-dataset-card-inspector` (0.451), `dataset-ops-compliance-checker` (0.448), `training-ops-quality-auditor` (0.443)

### `psc_huggingface_workflow_p02_1_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.3572 | 0.3018 | 0.8221 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-sentence-embedding-trainer` | no | 0.3572 | 0.2453 | 0.7528 | yes | model, choice | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.3572 | 0.3165 | 0.8111 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |

Top similarity neighbours: `support-ticket-triager` (0.410), `psc-local-model-fit-selector` (0.357), `support-ops-intake-classifier` (0.351), `public-huggingface-huggingface-trackio` (0.344), `public-huggingface-huggingface-local-models` (0.344)

### `psc_huggingface_workflow_p02_2_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.5557 | 0.5221 | 0.8221 | yes | hugg, face, model, dataset, card | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-sentence-embedding-trainer` | no | 0.5557 | 0.4106 | 0.7528 | yes | hugg, face, model, dataset | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-hf-space-deployment-preparer` | no | 0.5557 | 0.4565 | 0.8111 | yes | hugg, face, model, dataset | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |

Top similarity neighbours: `public-huggingface-huggingface-local-models` (0.584), `hf-local-model-selector` (0.562), `psc-local-model-fit-selector` (0.556), `public-huggingface-huggingface-vision-trainer` (0.535), `psc-hf-dataset-card-inspector` (0.522)

### `psc_huggingface_workflow_p03_1_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 34

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.3392 | 0.2252 | 0.7333 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-local-model-fit-selector` | no | 0.3392 | 0.2112 | 0.7528 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-hf-space-deployment-preparer` | no | 0.3392 | 0.1896 | 0.6647 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |

Top similarity neighbours: `skill-benchmark-evaluator` (0.713), `psc-retrieval-result-adjudicator` (0.637), `skill-router-policy-designer` (0.618), `skill-finder` (0.583), `psc-skill-routing-budget-planner` (0.557)

### `psc_huggingface_workflow_p03_2_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.5020 | 0.2137 | 0.7333 | yes | split, model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-local-model-fit-selector` | no | 0.5020 | 0.2608 | 0.7528 | yes | choose, local, model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-hf-space-deployment-preparer` | no | 0.5020 | 0.2101 | 0.6647 | yes | model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |

Top similarity neighbours: `sentence-transformer-finetuner` (0.651), `public-huggingface-train-sentence-transformers` (0.572), `psc-sentence-embedding-trainer` (0.502), `speaker-notes-writer` (0.431), `public-office-transcription-automation` (0.409)

### `psc_huggingface_workflow_p04_1_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.6606 | 0.5684 | 0.8565 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-local-model-fit-selector` | no | 0.6606 | 0.5710 | 0.8111 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-sentence-embedding-trainer` | no | 0.6606 | 0.4744 | 0.6647 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |

Top similarity neighbours: `psc-hf-space-deployment-preparer` (0.661), `public-huggingface-huggingface-vision-trainer` (0.595), `psc-local-model-fit-selector` (0.571), `psc-hf-dataset-card-inspector` (0.568), `public-huggingface-huggingface-community-evals` (0.547)

### `psc_huggingface_workflow_p04_2_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | no | 0.5726 | 0.3742 | 0.8565 | yes | model, demo, deployment, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-local-model-fit-selector` | no | 0.5726 | 0.3863 | 0.8111 | yes | model, demo, deployment, runtime, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-sentence-embedding-trainer` | no | 0.5726 | 0.2687 | 0.6647 | yes | model, demo, deployment, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |

Top similarity neighbours: `psc-hf-space-deployment-preparer` (0.573), `hf-zerogpu-space-deployer` (0.551), `training-ops-artifact-packager` (0.524), `ml-ops-artifact-packager` (0.503), `platform-ops-dependency-mapper` (0.494)

### `psc_pdf_document_work_p01_1_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-scan-ocr-recovery` | no | 0.5694 | 0.4868 | 0.8519 | yes | text, packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.5694 | 0.4741 | 0.8106 | yes | packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.5694 | 0.4463 | 0.8384 | yes | packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |

Top similarity neighbours: `pdf-layout-table-extractor` (0.661), `implicit-pdf-table-reconstructor` (0.590), `psc-pdf-native-extraction-pack` (0.569), `public-office-pdf-extraction` (0.534), `pdf-ocr-extractor` (0.517)

### `psc_pdf_document_work_p01_2_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-scan-ocr-recovery` | no | 0.6615 | 0.5483 | 0.8519 | yes | extract, workflow, packet, text, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.6615 | 0.4808 | 0.8106 | yes | extract, workflow, packet, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.6615 | 0.4808 | 0.8384 | yes | extract, workflow, packet, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |

Top similarity neighbours: `public-office-pdf-extraction` (0.675), `psc-pdf-native-extraction-pack` (0.661), `pdf-ocr-extractor` (0.661), `pdf-layout-table-extractor` (0.653), `pdf-ocr-cleaner` (0.560)

### `psc_pdf_document_work_p02_1_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.6033 | 0.4752 | 0.8519 | yes | page, pdf, packet, text | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.6033 | 0.4501 | 0.8227 | yes | page, pdf, packet | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.6033 | 0.4296 | 0.8428 | yes | page, pdf, packet | pdf, document, page, workflow, involv, extract, ocr, recovery |

Top similarity neighbours: `pdf-ocr-cleaner` (0.663), `pdf-ocr-extractor` (0.641), `psc-pdf-scan-ocr-recovery` (0.603), `public-office-pdf-ocr` (0.532), `psc-pdf-native-extraction-pack` (0.475)

### `psc_pdf_document_work_p02_2_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.6806 | 0.5510 | 0.8519 | yes | ocr, recovery, workflow, pdf, page, born-digital, table, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-evidence-qa` | no | 0.6806 | 0.4592 | 0.8227 | yes | ocr, recovery, workflow, pdf, page, note, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-redaction-pass` | no | 0.6806 | 0.4536 | 0.8428 | yes | ocr, recovery, workflow, pdf, page, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |

Top similarity neighbours: `pdf-ocr-extractor` (0.715), `pdf-ocr-cleaner` (0.709), `psc-pdf-scan-ocr-recovery` (0.681), `pdf-layout-table-extractor` (0.623), `public-office-pdf-ocr` (0.620)

### `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.4852 | 0.3472 | 0.8106 | yes | answer, pdf, page, evidence, extract, table, ocr, document | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.4852 | 0.3687 | 0.8227 | yes | answer, pdf, page, evidence, extract, ocr, document | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-redaction-pass` | no | 0.4852 | 0.4347 | 0.8734 | yes | answer, pdf, page, evidence, extract, ocr, document | pdf, document, evidence, answer, workflow, involv, extract, ocr |

Top similarity neighbours: `psc-pdf-evidence-qa` (0.485), `pdf-redaction-reviewer` (0.438), `psc-pdf-redaction-pass` (0.435), `travel-ops-risk-reviewer` (0.414), `implicit-pdf-evidence-answerer` (0.410)

### `psc_pdf_document_work_p03_2_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.5052 | 0.4116 | 0.8106 | yes | answer, pdf, page, evidence, document, extract, table | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.5052 | 0.3550 | 0.8227 | yes | answer, pdf, page, evidence, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-redaction-pass` | no | 0.5052 | 0.3540 | 0.8734 | yes | answer, pdf, page, evidence, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |

Top similarity neighbours: `pdf-question-answerer` (0.584), `implicit-pdf-evidence-answerer` (0.512), `psc-pdf-evidence-qa` (0.505), `pdf-layout-table-extractor` (0.484), `pdf-ocr-extractor` (0.424)

### `psc_pdf_document_work_p04_1_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.4958 | 0.4263 | 0.8384 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.4958 | 0.4217 | 0.8428 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-evidence-qa` | no | 0.4958 | 0.4368 | 0.8734 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |

Top similarity neighbours: `pdf-redaction-reviewer` (0.511), `psc-pdf-redaction-pass` (0.496), `pdf-layout-reviewer` (0.473), `pdf-layout-table-extractor` (0.466), `psc-pdf-evidence-qa` (0.437)

### `psc_pdf_document_work_p04_2_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | no | 0.5959 | 0.4849 | 0.8384 | yes | pdf, redaction, external, shar, page, anchor, extract, table | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | no | 0.5959 | 0.4544 | 0.8428 | yes | pdf, redaction, external, shar, page, anchor, extract | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-evidence-qa` | no | 0.5959 | 0.4879 | 0.8734 | yes | pdf, redaction, external, shar, page, anchor, extract | document, external, shar, pdf, workflow, involv, extract, ocr |

Top similarity neighbours: `psc-pdf-redaction-pass` (0.596), `pdf-redaction-reviewer` (0.570), `public-office-pdf-watermark` (0.494), `psc-pdf-evidence-qa` (0.488), `pdf-layout-table-extractor` (0.487)

### `psc_research_reading_p01_1_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | no | 0.5081 | 0.3655 | 0.7904 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-related-work-synthesizer` | no | 0.5081 | 0.2823 | 0.8210 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-source-field-table-extractor` | no | 0.5081 | 0.3371 | 0.8221 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |

Top similarity neighbours: `research-ops-dependency-mapper` (0.516), `psc-paper-method-mapper` (0.508), `customer-success-ops-dependency-mapper` (0.489), `thesis-ops-dependency-mapper` (0.488), `metrics-overview` (0.486)

### `psc_research_reading_p01_2_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | no | 0.4714 | 0.3456 | 0.7904 | yes | method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-related-work-synthesizer` | no | 0.4714 | 0.2438 | 0.8210 | yes | method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-source-field-table-extractor` | no | 0.4714 | 0.3642 | 0.8221 | yes | extract, method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |

Top similarity neighbours: `method-note-builder` (0.534), `paper-summariser` (0.520), `document-extractor` (0.501), `psc-paper-method-mapper` (0.471), `multi-source-comparison-builder` (0.435)

### `psc_research_reading_p02_1_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 32

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.3999 | 0.2727 | 0.7904 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-related-work-synthesizer` | no | 0.3999 | 0.2550 | 0.7491 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-source-field-table-extractor` | no | 0.3999 | 0.3180 | 0.8030 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |

Top similarity neighbours: `skill-authoring-guide` (0.566), `skill-finder` (0.533), `agent-ops-evidence-grounder` (0.520), `agent-ops-risk-reviewer` (0.505), `agent-ops-summary-writer` (0.500)

### `psc_research_reading_p02_2_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.6402 | 0.3725 | 0.7904 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-related-work-synthesizer` | no | 0.6402 | 0.2890 | 0.7491 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-source-field-table-extractor` | no | 0.6402 | 0.3441 | 0.8030 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |

Top similarity neighbours: `citation-grounding-helper` (0.651), `psc-citation-claim-support-auditor` (0.640), `research-ops-evidence-grounder` (0.633), `qa-ops-evidence-grounder` (0.603), `legal-ops-evidence-grounder` (0.596)

### `psc_research_reading_p03_1_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.4337 | 0.4010 | 0.8210 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-citation-claim-support-auditor` | no | 0.4337 | 0.3361 | 0.7491 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-source-field-table-extractor` | no | 0.4337 | 0.3003 | 0.8039 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |

Top similarity neighbours: `related-work-synthesiser` (0.527), `paper-summariser` (0.523), `multi-source-comparison-builder` (0.471), `thesis-ops-summary-writer` (0.466), `method-note-builder` (0.466)

### `psc_research_reading_p03_2_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.6021 | 0.3773 | 0.8210 | yes | limitation, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-citation-claim-support-auditor` | no | 0.6021 | 0.3987 | 0.7491 | yes | thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-source-field-table-extractor` | no | 0.6021 | 0.4299 | 0.8039 | yes | thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |

Top similarity neighbours: `related-work-synthesiser` (0.747), `psc-related-work-synthesizer` (0.602), `thesis-ops-rewrite-editor` (0.547), `thesis-ops-summary-writer` (0.542), `thesis-ops-resource-linker` (0.499)

### `psc_research_reading_p04_1_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.6124 | 0.5314 | 0.8221 | yes | extract, paper', baseline, limitation, compare, evidence, method | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-citation-claim-support-auditor` | no | 0.6124 | 0.5306 | 0.8030 | yes | compare, evidence, method, citation | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-related-work-synthesizer` | no | 0.6124 | 0.4064 | 0.8039 | yes | compare, evidence, method, synthesize, related-work | compare, research-read, workflow, involv, paper, claim, method, evidence |

Top similarity neighbours: `psc-source-field-table-extractor` (0.612), `multi-source-comparison-builder` (0.597), `document-extractor` (0.572), `research-ops-field-extractor` (0.570), `research-ops-comparison-builder` (0.566)

### `psc_research_reading_p04_2_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | no | 0.6554 | 0.3696 | 0.8221 | yes | evidence, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-citation-claim-support-auditor` | no | 0.6554 | 0.4830 | 0.8030 | yes | evidence, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-related-work-synthesizer` | no | 0.6554 | 0.3723 | 0.8039 | yes | evidence, related-work, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |

Top similarity neighbours: `psc-source-field-table-extractor` (0.655), `research-ops-field-extractor` (0.563), `document-extractor` (0.538), `document-field-extractor` (0.537), `legal-discovery-ops-field-extractor` (0.532)

### `psc_security_appsec_p01_1_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-handler-vulnerability-reviewer` | no | 0.5295 | 0.4487 | 0.7716 | yes | feature, risk, privacy, review, fixe | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-dependency-supply-chain-auditor` | no | 0.5295 | 0.3805 | 0.7333 | yes | feature, risk, privacy | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-privacy-telemetry-reviewer` | no | 0.5295 | 0.4943 | 0.6551 | yes | feature, risk, telemetry, privacy, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |

Top similarity neighbours: `psc-feature-threat-modeler` (0.529), `public-security-threat-model` (0.501), `psc-privacy-telemetry-reviewer` (0.494), `privacy-risk-reviewer` (0.491), `security-threat-modeler` (0.482)

### `psc_security_appsec_p01_2_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-handler-vulnerability-reviewer` | no | 0.5322 | 0.4685 | 0.7716 | yes | feature, path, mitigation, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-dependency-supply-chain-auditor` | no | 0.5322 | 0.3882 | 0.7333 | yes | feature, mitigation | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-privacy-telemetry-reviewer` | no | 0.5322 | 0.2990 | 0.6551 | yes | feature, mitigation, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |

Top similarity neighbours: `psc-feature-threat-modeler` (0.532), `public-security-threat-model` (0.494), `security-threat-modeler` (0.484), `api-security-threat-reviewer` (0.482), `psc-handler-vulnerability-reviewer` (0.469)

### `psc_security_appsec_p02_1_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 5

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.3914 | 0.1666 | 0.7716 | yes | - | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-dependency-supply-chain-auditor` | no | 0.3914 | 0.1206 | 0.7442 | yes | - | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.3914 | 0.1893 | 0.6960 | yes | review | code, application-security, workflow, involv, risk, feature, dependencie, privacy |

Top similarity neighbours: `auth-flow-reviewer` (0.445), `security-ops-rewrite-editor` (0.424), `public-n-skills-dev-browser` (0.399), `api-security-threat-reviewer` (0.393), `psc-handler-vulnerability-reviewer` (0.391)

### `psc_security_appsec_p02_2_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.6036 | 0.4708 | 0.7716 | yes | code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-dependency-supply-chain-auditor` | no | 0.6036 | 0.3502 | 0.7442 | yes | code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.6036 | 0.3219 | 0.6960 | yes | review, code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |

Top similarity neighbours: `api-security-threat-reviewer` (0.633), `psc-handler-vulnerability-reviewer` (0.604), `api-ops-risk-reviewer` (0.566), `security-code-reviewer` (0.520), `security-threat-modeler` (0.517)

### `psc_security_appsec_p03_1_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.5690 | 0.2508 | 0.7333 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-handler-vulnerability-reviewer` | no | 0.5690 | 0.2736 | 0.7442 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.5690 | 0.1328 | 0.6273 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |

Top similarity neighbours: `psc-dependency-supply-chain-auditor` (0.569), `supply-chain-ops-dependency-mapper` (0.512), `supply-chain-ops-artifact-packager` (0.508), `risk-ops-artifact-packager` (0.506), `risk-ops-dependency-mapper` (0.473)

### `psc_security_appsec_p03_2_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.6443 | 0.2596 | 0.7333 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-handler-vulnerability-reviewer` | no | 0.6443 | 0.3121 | 0.7442 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-privacy-telemetry-reviewer` | no | 0.6443 | 0.2453 | 0.6273 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |

Top similarity neighbours: `dependency-risk-auditor` (0.672), `psc-dependency-supply-chain-auditor` (0.644), `risk-ops-artifact-packager` (0.490), `public-addy-agent-source-driven-development` (0.479), `public-addy-web-best-practices` (0.458)

### `psc_security_appsec_p04_1_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 270

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.2354 | 0.0898 | 0.6551 | yes | - | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-handler-vulnerability-reviewer` | no | 0.2354 | 0.0799 | 0.6960 | yes | review | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-dependency-supply-chain-auditor` | no | 0.2354 | 0.1373 | 0.6273 | yes | - | privacy, data, application-security, workflow, involv, risk, code, feature |

Top similarity neighbours: `email-ops-quality-auditor` (0.426), `analytics-ops-quality-auditor` (0.416), `search-ops-monitoring-plan-builder` (0.406), `email-ops-monitoring-plan-builder` (0.398), `seo-ops-monitoring-plan-builder` (0.394)

### `psc_security_appsec_p04_2_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | no | 0.6428 | 0.2937 | 0.6551 | yes | privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-handler-vulnerability-reviewer` | no | 0.6428 | 0.3151 | 0.6960 | yes | privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-dependency-supply-chain-auditor` | no | 0.6428 | 0.2569 | 0.6273 | yes | asses, privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |

Top similarity neighbours: `psc-privacy-telemetry-reviewer` (0.643), `privacy-ops-scenario-planner` (0.521), `privacy-risk-reviewer` (0.508), `privacy-ops-risk-reviewer` (0.506), `privacy-policy-drafter` (0.493)

### `psc_skill_representation_p01_1_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 290

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-public-skill-atomizer` | no | 0.3298 | 0.2269 | 0.8264 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | no | 0.3298 | 0.2626 | 0.7959 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | no | 0.3298 | 0.2488 | 0.7727 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `warehouse-ops-artifact-packager` (0.486), `retail-ops-artifact-packager` (0.464), `manufacturing-ops-artifact-packager` (0.461), `procurement-ops-artifact-packager` (0.456), `supply-chain-ops-artifact-packager` (0.446)

### `psc_skill_representation_p01_2_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 18

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-public-skill-atomizer` | no | 0.4920 | 0.3705 | 0.8264 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | no | 0.4920 | 0.3787 | 0.7959 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | no | 0.4920 | 0.4885 | 0.7727 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-editor` (0.676), `skill-field-auditor` (0.672), `skill-finder` (0.622), `skill-authoring-guide` (0.604), `skill-evaluator` (0.592)

### `psc_skill_representation_p02_1_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.6243 | 0.5417 | 0.8264 | yes | file, candidate, resource | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-skill-routing-budget-planner` | no | 0.6243 | 0.5273 | 0.8222 | yes | candidate | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-retrieval-result-adjudicator` | no | 0.6243 | 0.4639 | 0.7525 | yes | candidate | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |

Top similarity neighbours: `psc-public-skill-atomizer` (0.624), `skill-installer-wrapper` (0.591), `psc-messy-skill-field-extractor` (0.542), `psc-skill-routing-budget-planner` (0.527), `skill-hierarchy-flattener` (0.525)

### `psc_skill_representation_p02_2_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.5912 | 0.4836 | 0.8264 | yes | resource, rout, boundarie | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-skill-routing-budget-planner` | no | 0.5912 | 0.5484 | 0.8222 | yes | rout | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-retrieval-result-adjudicator` | no | 0.5912 | 0.4144 | 0.7525 | yes | rout | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |

Top similarity neighbours: `skill-hierarchy-flattener` (0.776), `psc-public-skill-atomizer` (0.591), `skill-router-policy-designer` (0.582), `psc-skill-routing-budget-planner` (0.548), `skill-installer-wrapper` (0.521)

### `psc_skill_representation_p03_1_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.7439 | 0.4636 | 0.7959 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | no | 0.7439 | 0.5394 | 0.8222 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | no | 0.7439 | 0.4674 | 0.7298 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-router-policy-designer` (0.791), `psc-skill-routing-budget-planner` (0.744), `psc-public-skill-atomizer` (0.539), `skill-hierarchy-flattener` (0.520), `skill-finder` (0.478)

### `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.6160 | 0.5381 | 0.7959 | yes | candidate, evaluation, output, rout, extract, field, messy, atomization | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | no | 0.6160 | 0.5174 | 0.8222 | yes | candidate, evaluation, rout, field, atomization, public | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | no | 0.6160 | 0.6633 | 0.7298 | yes | retrieval, top-k, candidate, evaluation, rout, field, atomization | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `psc-retrieval-result-adjudicator` (0.663), `skill-benchmark-evaluator` (0.636), `psc-skill-routing-budget-planner` (0.616), `psc-messy-skill-field-extractor` (0.538), `skill-router-policy-designer` (0.538)

### `psc_skill_representation_p04_1_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.6498 | 0.3955 | 0.7727 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | no | 0.6498 | 0.3665 | 0.7525 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | no | 0.6498 | 0.4031 | 0.7298 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-benchmark-evaluator` (0.763), `psc-retrieval-result-adjudicator` (0.650), `skill-evaluator` (0.513), `search-ops-priority-ranker` (0.508), `training-ops-priority-ranker` (0.473)

### `psc_skill_representation_p04_2_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | no | 0.6576 | 0.2640 | 0.7727 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | no | 0.6576 | 0.2775 | 0.7525 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | no | 0.6576 | 0.2897 | 0.7298 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `psc-retrieval-result-adjudicator` (0.658), `skill-benchmark-evaluator` (0.551), `search-ops-summary-writer` (0.522), `search-ops-priority-ranker` (0.520), `search-ops-comparison-builder` (0.486)

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `general-source-summariser` | no | 0.6689 | 0.4840 | 0.6950 | yes | recap, summary | summary, recap |
| `method-note-builder` | no | 0.6689 | 0.3943 | 0.5489 | yes | paper, note | paper |
| `citation-note-extractor` | no | 0.6689 | 0.4355 | 0.5684 | yes | citation-ready, note | concise |

Top similarity neighbours: `paper-summariser` (0.669), `general-source-summariser` (0.484), `research-ops-summary-writer` (0.439), `citation-note-extractor` (0.435), `multi-source-comparison-builder` (0.430)

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `paper-summariser` | no | 0.4982 | 0.4710 | 0.6950 | yes | summary, academic, paper, limit | summary, recap |
| `document-extractor` | no | 0.4982 | 0.3338 | 0.5553 | yes | - | - |
| `citation-note-extractor` | no | 0.4982 | 0.4066 | 0.6566 | yes | - | important |

Top similarity neighbours: `research-ops-evidence-grounder` (0.504), `general-source-summariser` (0.498), `paper-summariser` (0.471), `thesis-ops-evidence-grounder` (0.470), `research-ops-summary-writer` (0.447)

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `document-extractor` | no | 0.7176 | 0.4348 | 0.7283 | yes | - | claim |
| `paper-summariser` | no | 0.7176 | 0.3786 | 0.5684 | yes | - | concise |
| `citation-grounding-helper` | no | 0.7176 | 0.5656 | 0.7106 | yes | note | note, claim, support |

Top similarity neighbours: `citation-note-extractor` (0.718), `citation-grounding-helper` (0.566), `method-note-builder` (0.519), `psc-citation-claim-support-auditor` (0.507), `general-source-summariser` (0.502)

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | no | 0.5590 | 0.3442 | 0.7283 | yes | detail | claim |
| `method-note-builder` | no | 0.5590 | 0.2255 | 0.5104 | yes | extract | extract |
| `paper-summariser` | no | 0.5590 | 0.1743 | 0.5425 | yes | - | - |

Top similarity neighbours: `document-field-extractor` (0.592), `document-extractor` (0.559), `psc-source-field-table-extractor` (0.510), `finance-ops-field-extractor` (0.501), `database-ops-field-extractor` (0.482)

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 15

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `paper-summariser` | no | 0.3833 | 0.3953 | 0.5489 | yes | - | paper |
| `document-extractor` | no | 0.3833 | 0.3599 | 0.5104 | yes | - | extract |
| `citation-note-extractor` | no | 0.3833 | 0.3185 | 0.6449 | yes | - | note |

Top similarity neighbours: `manufacturing-ops-summary-writer` (0.415), `energy-ops-summary-writer` (0.411), `thesis-ops-summary-writer` (0.408), `hr-ops-summary-writer` (0.402), `ux-ops-summary-writer` (0.400)

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | no | 0.4869 | 0.4518 | 0.7106 | yes | support | claim, note, support |
| `paper-summariser` | no | 0.4869 | 0.3984 | 0.4244 | no | - | - |
| `document-extractor` | no | 0.4869 | 0.4048 | 0.5536 | yes | explicit | claim |

Top similarity neighbours: `citation-grounding-helper` (0.487), `agent-ops-summary-writer` (0.460), `citation-note-extractor` (0.452), `qa-ops-summary-writer` (0.440), `incident-ops-rewrite-editor` (0.440)

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `related-work-synthesiser` | no | 0.5742 | 0.4958 | 0.5379 | yes | related-work | multiple, paper |
| `method-note-builder` | no | 0.5742 | 0.3942 | 0.5466 | yes | evaluation, note | paper, assumption, evaluation, setup |
| `citation-note-extractor` | no | 0.5742 | 0.5160 | 0.5837 | yes | turn, note | important |

Top similarity neighbours: `multi-source-comparison-builder` (0.574), `citation-note-extractor` (0.516), `research-ops-comparison-builder` (0.496), `related-work-synthesiser` (0.496), `citation-grounding-helper` (0.483)

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `multi-source-comparison-builder` | no | 0.7327 | 0.4915 | 0.5379 | yes | compare | multiple, paper |
| `citation-note-extractor` | no | 0.7327 | 0.4328 | 0.4848 | no | note | - |
| `paper-summariser` | no | 0.7327 | 0.3974 | 0.5469 | yes | - | paper, question |

Top similarity neighbours: `related-work-synthesiser` (0.733), `psc-related-work-synthesizer` (0.548), `psc-source-field-table-extractor` (0.508), `multi-source-comparison-builder` (0.491), `general-source-summariser` (0.490)

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `reply-drafter` | no | 0.5758 | 0.4369 | 0.6945 | yes | draft, email, reply, message | draft, reply, email, context |
| `reply-polisher` | no | 0.5758 | 0.4410 | 0.6370 | yes | email, reply, message, tone | reply, email |

Top similarity neighbours: `professor-email-reply` (0.576), `reply-polisher` (0.441), `reply-drafter` (0.437), `email-drafter` (0.428), `groupwork-reply` (0.412)

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `professor-email-reply` | no | 0.4806 | 0.2795 | 0.6370 | yes | - | reply, email |
| `reply-drafter` | no | 0.4806 | 0.3891 | 0.6908 | yes | message | reply, message, email |

Top similarity neighbours: `reply-polisher` (0.481), `followup-reply-writer` (0.461), `partnerships-ops-rewrite-editor` (0.438), `email-polisher` (0.432), `groupwork-reply` (0.398)

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `reply-drafter` | no | 0.5182 | 0.2437 | 0.7078 | yes | reply, draft, need | reply, draft, message |
| `followup-reply-writer` | no | 0.5182 | 0.3361 | 0.6648 | yes | reply, draft | reply, draft, message |

Top similarity neighbours: `groupwork-reply` (0.518), `meeting-ops-summary-writer` (0.381), `meeting-summary-writer` (0.378), `partnerships-ops-handoff-brief-writer` (0.371), `partnerships-ops-failure-diagnoser` (0.355)

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `reply-drafter` | no | 0.6173 | 0.3860 | 0.7056 | yes | - | draft, reply, message |
| `groupwork-reply` | no | 0.6173 | 0.4311 | 0.6648 | yes | - | draft, reply, message |

Top similarity neighbours: `followup-reply-writer` (0.617), `email-action-extractor` (0.464), `reply-polisher` (0.444), `groupwork-reply` (0.431), `meeting-followup-extractor` (0.410)

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `reply-polisher` | no | 0.5525 | 0.6040 | 0.6908 | yes | message, reply, polish | reply, message, email |
| `followup-reply-writer` | no | 0.5525 | 0.5293 | 0.7056 | yes | response, message, reply, action | draft, reply, message |

Top similarity neighbours: `reply-polisher` (0.604), `reply-drafter` (0.552), `email-polisher` (0.541), `followup-reply-writer` (0.529), `groupwork-reply` (0.490)

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | no | 0.4394 | 0.3827 | 0.6276 | yes | security, review | security |
| `auth-flow-reviewer` | no | 0.4394 | 0.4755 | 0.5270 | yes | security, risk, review | security, flow |
| `privacy-risk-reviewer` | no | 0.4394 | 0.4675 | 0.5166 | yes | risk, review, privacy | data |

Top similarity neighbours: `auth-flow-reviewer` (0.475), `privacy-risk-reviewer` (0.468), `psc-feature-threat-modeler` (0.466), `security-threat-modeler` (0.439), `public-security-threat-model` (0.437)

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `code-reviewer` | no | 0.4879 | 0.2611 | 0.5156 | yes | review, implementation | review, code |
| `auth-flow-reviewer` | no | 0.4879 | 0.5727 | 0.6944 | yes | review, security, authorization | review, security, authorization |
| `security-threat-modeler` | no | 0.4879 | 0.3796 | 0.6276 | yes | security, architecture, threat, model | security |

Top similarity neighbours: `auth-flow-reviewer` (0.573), `api-security-threat-reviewer` (0.557), `psc-handler-vulnerability-reviewer` (0.518), `security-code-reviewer` (0.488), `auth-flow-integrator` (0.466)

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | no | 0.5351 | 0.1974 | 0.6562 | yes | - | review |
| `secret-leak-scanner` | no | 0.5351 | 0.2172 | 0.5770 | yes | - | - |
| `ci-failure-debugger` | no | 0.5351 | 0.1208 | 0.2660 | no | check, need | - |

Top similarity neighbours: `dependency-risk-auditor` (0.535), `psc-dependency-supply-chain-auditor` (0.522), `risk-ops-artifact-packager` (0.480), `risk-ops-dependency-mapper` (0.470), `supply-chain-ops-risk-reviewer` (0.391)

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `dependency-risk-auditor` | no | 0.4699 | 0.3471 | 0.5770 | yes | update | - |
| `security-code-reviewer` | no | 0.4699 | 0.3973 | 0.6436 | yes | diff | diff, unsafe |
| `privacy-risk-reviewer` | no | 0.4699 | 0.3400 | 0.5534 | yes | - | - |

Top similarity neighbours: `secret-leak-scanner` (0.470), `environment-config-auditor` (0.463), `security-ops-rewrite-editor` (0.427), `public-oh-my-changelog-maintenance` (0.419), `deployment-build-triager` (0.401)

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | no | 0.3801 | 0.1072 | 0.6944 | yes | - | review, authorization, security |
| `security-threat-modeler` | no | 0.3801 | 0.0842 | 0.5270 | yes | - | flow, security |
| `privacy-risk-reviewer` | no | 0.3801 | 0.2003 | 0.7290 | yes | - | review, risk |

Top similarity neighbours: `auth-flow-reviewer` (0.380), `identity-ops-failure-diagnoser` (0.284), `identity-ops-summary-writer` (0.252), `identity-ops-resource-linker` (0.232), `identity-ops-risk-reviewer` (0.220)

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `security-threat-modeler` | no | 0.4925 | 0.2250 | 0.5166 | yes | - | data |
| `secret-leak-scanner` | no | 0.4925 | 0.2724 | 0.5534 | yes | - | - |
| `auth-flow-reviewer` | no | 0.4925 | 0.3161 | 0.7290 | yes | - | review, risk |

Top similarity neighbours: `privacy-risk-reviewer` (0.492), `analytics-ops-compliance-checker` (0.469), `analytics-ops-risk-reviewer` (0.462), `analytics-ops-quality-auditor` (0.447), `dataset-ops-compliance-checker` (0.415)

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-creator` | no | 0.4128 | 0.3250 | 0.6937 | yes | new, workflow | new |
| `skill-installer` | no | 0.4128 | 0.2942 | 0.8188 | yes | exist, library | exist, library, user', install |
| `skill-editor` | no | 0.4128 | 0.3765 | 0.7289 | yes | new, exist, workflow | exist, creat, new |

Top similarity neighbours: `meeting-notes-action-extractor` (0.544), `meeting-followup-extractor` (0.458), `method-note-builder` (0.445), `public-anthropic-doc-coauthoring` (0.436), `meeting-summary-writer` (0.435)

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 237

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-finder` | no | 0.2566 | 0.2283 | 0.8188 | yes | exist, library, new | install, exist, user', library |
| `skill-creator` | no | 0.2566 | 0.0715 | 0.6487 | yes | new | - |
| `skill-packager` | no | 0.2566 | 0.2736 | 0.7879 | yes | exist, check, file, prepare, distribution | prepare, exist |

Top similarity neighbours: `public-office-data-analysis` (0.543), `public-office-sheets-automation` (0.482), `data-analysis-overview` (0.463), `data-analysis-for-reporting` (0.458), `public-swebench-xlsx` (0.430)

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-editor` | no | 0.5725 | 0.4982 | 0.7846 | yes | workflow, new, exist | workflow, new, artifact, description, boundarie, resource |
| `skill-finder` | no | 0.5725 | 0.4275 | 0.6937 | yes | new, exist | new |
| `skill-packager` | no | 0.5725 | 0.3585 | 0.6525 | yes | exist | resource |

Top similarity neighbours: `skill-creator` (0.573), `skill-editor` (0.498), `skill-authoring-guide` (0.447), `psc-public-skill-atomizer` (0.446), `task-extractor` (0.438)

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 78

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-creator` | no | 0.4342 | 0.3479 | 0.7846 | yes | description, trigger | artifact, description, workflow, boundarie, resource, new |
| `skill-evaluator` | no | 0.4342 | 0.3313 | 0.6445 | yes | exist, skill', description, trigger | exist, description, behavior |
| `skill-packager` | no | 0.4342 | 0.3111 | 0.6374 | yes | exist | exist, resource |

Top similarity neighbours: `document-field-extractor` (0.616), `course-ops-field-extractor` (0.559), `docs-ops-field-extractor` (0.558), `skill-field-auditor` (0.557), `writing-ops-field-extractor` (0.554)

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-editor` | no | 0.3869 | 0.3028 | 0.6445 | yes | - | exist, behavior, description |
| `skill-finder` | no | 0.3869 | 0.2673 | 0.6822 | yes | whether, already | exist, whether |
| `skill-creator` | no | 0.3869 | 0.2153 | 0.5384 | yes | trigger | trigger, description |

Top similarity neighbours: `reply-polisher` (0.601), `reply-drafter` (0.576), `email-polisher` (0.528), `followup-reply-writer` (0.494), `email-drafter` (0.440)

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-creator` | no | 0.3880 | 0.2272 | 0.6525 | yes | resource | resource |
| `skill-installer` | no | 0.3880 | 0.2697 | 0.7879 | yes | exist | prepare, exist |
| `skill-editor` | no | 0.3880 | 0.2195 | 0.6374 | yes | exist, resource | exist, resource |

Top similarity neighbours: `public-anthropic-doc-coauthoring` (0.475), `document-summariser` (0.430), `public-office-content-writer` (0.422), `docs-ops-summary-writer` (0.397), `public-skill-installer` (0.392)

### `skill_representation_analysis_p1_skill_field_auditor`

- Family: `skill_representation_analysis`
- Gold skill: `skill-field-auditor`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-authoring-guide` | no | 0.6763 | 0.5141 | 0.6900 | yes | trigger, resource, example | trigger, constraint, resource, example |
| `skill-router-policy-designer` | no | 0.6763 | 0.3289 | 0.5384 | yes | - | - |
| `skill-hierarchy-flattener` | no | 0.6763 | 0.2493 | 0.5194 | yes | resource | resource |
| `skill-installer-wrapper` | no | 0.6763 | 0.5400 | 0.6281 | yes | resource | resource |

Top similarity neighbours: `skill-field-auditor` (0.676), `training-ops-quality-auditor` (0.578), `psc-messy-skill-field-extractor` (0.558), `writing-ops-quality-auditor` (0.546), `course-ops-quality-auditor` (0.544)

### `skill_representation_analysis_p2_skill_authoring_guide`

- Family: `skill_representation_analysis`
- Gold skill: `skill-authoring-guide`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 9

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.5003 | 0.4702 | 0.6900 | yes | includ, trigger, workflow, dependencie, example, exist | trigger, resource, constraint, example |
| `skill-router-policy-designer` | no | 0.5003 | 0.3619 | 0.6061 | yes | - | - |
| `skill-hierarchy-flattener` | no | 0.5003 | 0.4116 | 0.5291 | yes | atomic, boundarie | resource |
| `skill-installer-wrapper` | no | 0.5003 | 0.5161 | 0.6144 | yes | install | resource |

Top similarity neighbours: `skill-creator` (0.624), `skill-editor` (0.554), `migration-risk-auditor` (0.523), `skill-installer-wrapper` (0.516), `database-migration-risk-assessor` (0.514)

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Family: `skill_representation_analysis`
- Gold skill: `skill-router-policy-designer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.8082 | 0.4291 | 0.5384 | yes | includ, representation, field | - |
| `skill-authoring-guide` | no | 0.8082 | 0.4935 | 0.6061 | yes | - | - |
| `skill-hierarchy-flattener` | no | 0.8082 | 0.5538 | 0.6309 | yes | rout | rout |
| `skill-installer-wrapper` | no | 0.8082 | 0.4621 | 0.4956 | no | - | - |

Top similarity neighbours: `skill-router-policy-designer` (0.808), `psc-skill-routing-budget-planner` (0.736), `skill-hierarchy-flattener` (0.554), `psc-public-skill-atomizer` (0.539), `skill-finder` (0.530)

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Family: `skill_representation_analysis`
- Gold skill: `skill-hierarchy-flattener`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.8028 | 0.4947 | 0.5194 | yes | resource | resource |
| `skill-authoring-guide` | no | 0.8028 | 0.5745 | 0.5291 | yes | resource | resource |
| `skill-router-policy-designer` | no | 0.8028 | 0.6226 | 0.6309 | yes | rout | rout |
| `skill-installer-wrapper` | no | 0.8028 | 0.6353 | 0.5982 | yes | preserv, resource | preserv, resource |

Top similarity neighbours: `skill-hierarchy-flattener` (0.803), `psc-public-skill-atomizer` (0.670), `skill-installer-wrapper` (0.635), `skill-router-policy-designer` (0.623), `skill-creator` (0.622)

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Family: `skill_representation_analysis`
- Gold skill: `skill-installer-wrapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.6577 | 0.3312 | 0.6281 | yes | resource | resource |
| `skill-authoring-guide` | no | 0.6577 | 0.3540 | 0.6144 | yes | resource | resource |
| `skill-router-policy-designer` | no | 0.6577 | 0.2096 | 0.4956 | no | - | - |
| `skill-hierarchy-flattener` | no | 0.6577 | 0.2687 | 0.5982 | yes | preserv, resource | preserv, resource |

Top similarity neighbours: `public-skill-installer` (0.689), `skill-installer-wrapper` (0.658), `public-vercel-find-skills` (0.551), `public-oh-my-agentic-skills` (0.549), `public-skill-creator` (0.548)

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Family: `skill_representation_analysis`
- Gold skill: `skill-benchmark-evaluator`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Acceptable? | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | no | 0.4785 | 0.1974 | 0.6460 | yes | - | - |
| `skill-authoring-guide` | no | 0.4785 | 0.1415 | 0.5925 | yes | - | - |
| `skill-router-policy-designer` | no | 0.4785 | 0.1811 | 0.5846 | yes | - | - |
| `skill-hierarchy-flattener` | no | 0.4785 | 0.1847 | 0.5722 | yes | - | - |

Top similarity neighbours: `skill-benchmark-evaluator` (0.478), `psc-retrieval-result-adjudicator` (0.428), `rag-failure-diagnoser` (0.417), `search-ops-risk-reviewer` (0.405), `search-ops-priority-ranker` (0.400)

