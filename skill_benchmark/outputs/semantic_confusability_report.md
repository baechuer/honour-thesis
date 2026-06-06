# Semantic Confusability Report

This report implements Step 3 of the benchmark rubric: listed alternatives should be semantically plausible neighbours, not random unrelated distractors.

Similarity backend: **embedding** using `sentence-transformers/all-MiniLM-L6-v2`.

Interpretation: this is an offline similarity diagnostic. It is enough to flag obviously non-confusable pairs, but final thesis evidence should still report actual selector results for M1-M6.

## Overall Status

- Step 3 status: **PASS**
- Prompts with at least two plausible listed alternatives: 180/201 (89.6%)
- Gold/alternative pairs marked plausible: 509/641 (79.4%)
- Gold skill ranked top-1 among all skills by this backend: 89/201 (44.3%)

Pass rule used here: each prompt should have at least two alternatives whose description-card score is close to the gold prompt score, or whose skill card is similar to the gold skill card.

## Family Summary

| Family | Prompts | Prompt pass | Gold top-1 by similarity backend |
|---|---:|---:|---:|
| api_backend_design | 6 | 5/6 | 4/6 |
| api_mcp_tooling | 6 | 5/6 | 4/6 |
| browser_web_automation | 6 | 4/6 | 2/6 |
| code_github_workflow | 6 | 6/6 | 1/6 |
| data_spreadsheet | 7 | 7/7 | 1/7 |
| deployment_browser_qa | 6 | 4/6 | 2/6 |
| documents_files | 7 | 7/7 | 1/7 |
| github_ci_maintenance | 6 | 5/6 | 3/6 |
| huggingface_ml_workflows | 6 | 5/6 | 3/6 |
| implicit_field_stress | 10 | 9/10 | 3/10 |
| metrics_observability | 6 | 2/6 | 3/6 |
| news_monitoring | 5 | 5/5 | 3/5 |
| observability_reliability | 6 | 2/6 | 5/6 |
| office_artifact_workflows | 6 | 5/6 | 4/6 |
| office_business_automation | 6 | 4/6 | 5/6 |
| pdf_document_operations | 6 | 5/6 | 5/6 |
| planning_meetings | 5 | 5/5 | 3/5 |
| public_style_controlled | 64 | 64/64 | 19/64 |
| reading_research | 8 | 8/8 | 5/8 |
| reply_messaging | 5 | 5/5 | 4/5 |
| security_appsec | 6 | 6/6 | 4/6 |
| skill_lifecycle | 6 | 6/6 | 1/6 |
| skill_representation_analysis | 6 | 6/6 | 4/6 |

## Weak Semantic-Confusability Prompts

| Prompt | Gold | Plausible alternatives | Gold all-skill rank |
|---|---|---:|---:|
| `api_p5_database_migration_risk` | `database-migration-risk-assessor` | 1 | 1 |
| `api_mcp_tooling_p6_api_security_threat_reviewer` | `api-security-threat-reviewer` | 1 | 1 |
| `web_p4_data_extraction` | `web-data-extractor` | 1 | 1 |
| `web_p5_frontend_debugging` | `frontend-debugger` | 1 | 1 |
| `deploy_p2_visual_regression` | `visual-regression-checker` | 0 | 1 |
| `deploy_p3_accessibility_interaction` | `accessibility-interaction-auditor` | 0 | 1 |
| `github_ci_maintenance_p6_git_safety_guardrail_installer` | `git-safety-guardrail-installer` | 1 | 1 |
| `huggingface_ml_workflows_p3_sentence_transformer_finetuner` | `sentence-transformer-finetuner` | 1 | 1 |
| `implicit_p5_ci_failure` | `implicit-ci-failure-reader` | 1 | 1 |
| `obs_p2_latency_anomaly` | `latency-anomaly-detector` | 0 | 1 |
| `obs_p4_capacity_risk` | `capacity-risk-forecaster` | 0 | 1 |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | 1 | 3 |
| `obs_p6_incident_summary` | `incident-summary-writer` | 1 | 6 |
| `observability_reliability_p2_grafana_dashboard_builder` | `grafana-dashboard-builder` | 1 | 1 |
| `observability_reliability_p3_distributed_trace_investigator` | `distributed-trace-investigator` | 1 | 3 |
| `observability_reliability_p5_resilience_pattern_reviewer` | `resilience-pattern-reviewer` | 1 | 1 |
| `observability_reliability_p6_service_mesh_traffic_debugger` | `service-mesh-traffic-debugger` | 1 | 1 |
| `office_p1_pdf_layout_review` | `pdf-layout-reviewer` | 1 | 2 |
| `office_business_automation_p1_xlsx_formula_model_builder` | `xlsx-formula-model-builder` | 1 | 1 |
| `office_business_automation_p6_email_classification_router` | `email-classification-router` | 1 | 1 |
| `pdf_document_operations_p5_pdf_redaction_reviewer` | `pdf-redaction-reviewer` | 1 | 1 |

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | 0.6807 | 0.4831 | 0.5703 | yes | api, pagination | endpoint, pagination |
| `webhook-contract-planner` | 0.6807 | 0.3211 | 0.4641 | no | contract, behavior | contract, behavior |
| `architecture-boundary-reviewer` | 0.6807 | 0.3932 | 0.6497 | yes | review | review |

Top similarity neighbours: `openapi-contract-reviewer` (0.681), `openapi-contract-tester` (0.541), `external-api-integration-planner` (0.483), `api-ops-summary-writer` (0.472), `api-integration-planner` (0.455)

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `openapi-contract-reviewer` | 0.4263 | 0.3312 | 0.5703 | yes | endpoint, behavior | endpoint, pagination |
| `webhook-contract-planner` | 0.4263 | 0.2865 | 0.5934 | yes | behavior, verification | payload, retrie |
| `service-dependency-mapper` | 0.4263 | 0.2836 | 0.4545 | no | - | failure |

Top similarity neighbours: `api-integration-planner` (0.479), `auth-flow-reviewer` (0.440), `external-api-integration-planner` (0.426), `auth-flow-integrator` (0.422), `public-office-subscription-management` (0.396)

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `external-api-integration-planner` | 0.4632 | 0.3154 | 0.5934 | yes | - | payload, retrie |
| `openapi-contract-reviewer` | 0.4632 | 0.3279 | 0.4641 | no | behavior | contract, behavior |
| `public-office-webhook-automation` | 0.4632 | 0.3008 | 0.6091 | yes | event | event |
| `public-api-design-principles` | 0.4632 | 0.3203 | 0.4039 | no | design | design |

Top similarity neighbours: `webhook-contract-planner` (0.463), `events-ops-acceptance-test-builder` (0.423), `events-ops-intake-classifier` (0.420), `invoice-payment-checker` (0.398), `customer-success-ops-intake-classifier` (0.396)

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `service-dependency-mapper` | 0.7248 | 0.4438 | 0.4242 | no | - | service |
| `openapi-contract-reviewer` | 0.7248 | 0.4497 | 0.6497 | yes | review | review |
| `database-migration-risk-assessor` | 0.7248 | 0.4403 | 0.5922 | yes | - | risk |

Top similarity neighbours: `architecture-boundary-reviewer` (0.725), `public-architecture-patterns` (0.511), `public-addy-agent-api-and-interface-design` (0.485), `public-mattpocock-improve-codebase-architecture` (0.469), `openapi-contract-reviewer` (0.450)

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | 0.6735 | 0.3530 | 0.5922 | yes | risk | risk |
| `service-dependency-mapper` | 0.6735 | 0.2395 | 0.3664 | no | - | data |
| `public-office-database-sync` | 0.6735 | 0.4358 | 0.4213 | no | - | database, migration, data |
| `public-architecture-patterns` | 0.6735 | 0.2024 | 0.2951 | no | - | - |

Top similarity neighbours: `database-migration-risk-assessor` (0.673), `migration-risk-auditor` (0.616), `deployment-rollback-planner` (0.578), `public-oh-my-changelog-maintenance` (0.498), `public-office-subscription-management` (0.487)

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 228

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `architecture-boundary-reviewer` | 0.3585 | 0.3129 | 0.4242 | yes | service, direction | service |
| `external-api-integration-planner` | 0.3585 | 0.2769 | 0.4545 | no | failure | failure |
| `public-architecture-patterns` | 0.3585 | 0.2497 | 0.3361 | no | - | - |
| `public-api-design-principles` | 0.3585 | 0.2885 | 0.3776 | yes | - | - |

Top similarity neighbours: `public-swebench-distributed-tracing` (0.505), `distributed-trace-investigator` (0.479), `customer-feedback-analyser` (0.477), `analytics-ops-compliance-checker` (0.474), `dashboard-ops-compliance-checker` (0.468)

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Family: `api_mcp_tooling`
- Gold skill: `rest-api-contract-designer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `mcp-server-builder` | 0.4639 | 0.4944 | 0.5983 | yes | resource, example, mcp | resource, schema |
| `webhook-integration-planner` | 0.4639 | 0.4413 | 0.4814 | yes | subscription | - |
| `auth-flow-integrator` | 0.4639 | 0.3778 | 0.4651 | no | - | api |
| `api-documentation-writer` | 0.4639 | 0.3950 | 0.6470 | yes | includ, error, example | api, error |

Top similarity neighbours: `mcp-server-builder` (0.494), `public-anthropic-mcp-builder` (0.469), `rest-api-contract-designer` (0.464), `public-swebench-mcp-builder` (0.445), `webhook-integration-planner` (0.441)

### `api_mcp_tooling_p2_mcp_server_builder`

- Family: `api_mcp_tooling`
- Gold skill: `mcp-server-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | 0.4716 | 0.4688 | 0.5983 | yes | design, schema, resource, rest, api | resource, schema |
| `webhook-integration-planner` | 0.4716 | 0.3143 | 0.4079 | no | - | - |
| `auth-flow-integrator` | 0.4716 | 0.3316 | 0.5342 | yes | api | - |
| `api-documentation-writer` | 0.4716 | 0.3305 | 0.5697 | yes | api | example |

Top similarity neighbours: `mcp-server-builder` (0.472), `rest-api-contract-designer` (0.469), `public-anthropic-mcp-builder` (0.431), `api-security-threat-reviewer` (0.417), `public-swebench-mcp-builder` (0.407)

### `api_mcp_tooling_p3_webhook_integration_planner`

- Family: `api_mcp_tooling`
- Gold skill: `webhook-integration-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-webhook-automation` | 0.7807 | 0.6127 | 0.6843 | yes | event | event |
| `webhook-contract-planner` | 0.7807 | 0.7681 | 0.8732 | yes | event, webhook, signature, idempotency, behavior, order, dead-letter | webhook, event, signature, verification, idempotency, retrie, order, dead-letter |
| `rest-api-contract-designer` | 0.7807 | 0.3138 | 0.4814 | no | behavior | - |
| `mcp-server-builder` | 0.7807 | 0.1382 | 0.4079 | no | - | - |

Top similarity neighbours: `webhook-integration-planner` (0.781), `webhook-contract-planner` (0.768), `webhook-setup-planner` (0.739), `public-office-webhook-automation` (0.613), `web-ops-scenario-planner` (0.439)

### `api_mcp_tooling_p4_auth_flow_integrator`

- Family: `api_mcp_tooling`
- Gold skill: `auth-flow-integrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 9

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | 0.4306 | 0.2437 | 0.4651 | no | - | api |
| `mcp-server-builder` | 0.4306 | 0.1473 | 0.5342 | yes | - | - |
| `webhook-integration-planner` | 0.4306 | 0.5706 | 0.4428 | yes | webhook | keys |
| `api-documentation-writer` | 0.4306 | 0.2529 | 0.5531 | yes | - | api |

Top similarity neighbours: `webhook-setup-planner` (0.637), `public-office-webhook-automation` (0.606), `webhook-integration-planner` (0.571), `api-integration-planner` (0.507), `webhook-contract-planner` (0.506)

### `api_mcp_tooling_p5_api_documentation_writer`

- Family: `api_mcp_tooling`
- Gold skill: `api-documentation-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `rest-api-contract-designer` | 0.5326 | 0.3091 | 0.6470 | yes | api, error | api, error |
| `mcp-server-builder` | 0.5326 | 0.1589 | 0.5697 | yes | example | example |
| `webhook-integration-planner` | 0.5326 | 0.2725 | 0.4905 | no | - | - |
| `auth-flow-integrator` | 0.5326 | 0.2664 | 0.5531 | yes | api | api |

Top similarity neighbours: `api-documentation-writer` (0.533), `public-office-stripe-payments` (0.417), `public-office-quickbooks-automation` (0.403), `invoice-payment-checker` (0.365), `openapi-contract-reviewer` (0.347)

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Family: `api_mcp_tooling`
- Gold skill: `api-security-threat-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-security-threat-model` | 0.6196 | 0.3646 | 0.4402 | no | abuse | review, design, abuse |
| `public-openai-security-best-practices` | 0.6196 | 0.3898 | 0.4099 | no | security | review |
| `security-threat-modeler` | 0.6196 | 0.3398 | 0.4828 | no | data, abuse, security | design, data, abuse, case |
| `rest-api-contract-designer` | 0.6196 | 0.2638 | 0.5537 | yes | api | api, design |

Top similarity neighbours: `api-security-threat-reviewer` (0.620), `api-ops-risk-reviewer` (0.571), `privacy-risk-reviewer` (0.562), `auth-flow-reviewer` (0.530), `identity-ops-risk-reviewer` (0.511)

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.4183 | 0.3207 | 0.6353 | yes | interaction, test | web, interaction, test |
| `web-data-extractor` | 0.4183 | 0.0477 | 0.5152 | yes | page | page, web |
| `frontend-debugger` | 0.4183 | 0.2490 | 0.4908 | no | state, observation | state |

Top similarity neighbours: `visual-regression-checker` (0.445), `web-page-snapshotter` (0.418), `psc-visual-screenshot-reviewer` (0.415), `psc-devtools-runtime-diagnoser` (0.387), `psc-playwright-regression-suite` (0.383)

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.3930 | 0.4330 | 0.6349 | yes | report, flow, test | interaction, flow |
| `web-page-snapshotter` | 0.3930 | 0.2713 | 0.5743 | yes | test | perform, interaction |
| `frontend-debugger` | 0.3930 | 0.2425 | 0.4170 | no | - | - |

Top similarity neighbours: `web-ui-tester` (0.433), `identity-ops-acceptance-test-builder` (0.419), `web-form-filler` (0.393), `marketing-ops-acceptance-test-builder` (0.390), `web-ops-acceptance-test-builder` (0.388)

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 123

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-form-filler` | 0.2394 | 0.1152 | 0.6349 | yes | - | interaction, flow |
| `frontend-debugger` | 0.2394 | 0.1624 | 0.6468 | yes | behavior | behavior |
| `web-page-snapshotter` | 0.2394 | 0.1396 | 0.6353 | yes | test, page | test, web, interaction |

Top similarity neighbours: `email-ops-acceptance-test-builder` (0.380), `facilities-ops-acceptance-test-builder` (0.375), `contract-ops-acceptance-test-builder` (0.360), `grant-ops-acceptance-test-builder` (0.356), `crm-ops-acceptance-test-builder` (0.356)

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-page-snapshotter` | 0.4932 | 0.2532 | 0.5152 | yes | page, screenshot | web, page |
| `web-ui-tester` | 0.4932 | 0.0278 | 0.4455 | no | - | web |
| `frontend-debugger` | 0.4932 | -0.0330 | 0.2881 | no | - | - |

Top similarity neighbours: `web-data-extractor` (0.493), `pdf-layout-table-extractor` (0.443), `product-ops-field-extractor` (0.425), `receipt-extractor` (0.377), `implicit-pdf-table-reconstructor` (0.373)

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.3846 | 0.1565 | 0.6468 | yes | - | behavior |
| `web-page-snapshotter` | 0.3846 | 0.1277 | 0.4908 | no | page, open, evidence, inspect, state | state |
| `code-reviewer` | 0.3846 | 0.0709 | 0.1042 | no | code | code |

Top similarity neighbours: `frontend-debugger` (0.385), `api-ops-failure-diagnoser` (0.329), `public-oh-my-game-performance-profiler` (0.312), `publishing-ops-failure-diagnoser` (0.282), `property-ops-failure-diagnoser` (0.281)

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `web-ui-tester` | 0.4781 | 0.2751 | 0.6539 | yes | whether | check, web |
| `frontend-debugger` | 0.4781 | 0.2559 | 0.5092 | yes | error | - |
| `web-page-snapshotter` | 0.4781 | 0.2410 | 0.5908 | yes | - | web |

Top similarity neighbours: `accessibility-interaction-auditor` (0.519), `accessibility-checker` (0.478), `psc-accessibility-interaction-auditor` (0.469), `public-addy-web-accessibility` (0.438), `meeting-notes-action-extractor` (0.342)

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | 0.3028 | 0.1964 | 0.8192 | yes | review, risk | review, file, risk |
| `review-comment-resolver` | 0.3028 | 0.2309 | 0.7433 | yes | change, review | review, code, change |
| `ci-failure-debugger` | 0.3028 | 0.1891 | 0.5839 | yes | test | test |

Top similarity neighbours: `public-swebench-springboot-tdd` (0.324), `email-ops-acceptance-test-builder` (0.318), `code-reviewer` (0.303), `localization-ops-acceptance-test-builder` (0.300), `repo-ops-acceptance-test-builder` (0.282)

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.4772 | 0.3537 | 0.8192 | yes | review, change, test | review, file, risk |
| `review-comment-resolver` | 0.4772 | 0.3178 | 0.7200 | yes | review, request, change | review, request |
| `ci-failure-debugger` | 0.4772 | 0.3272 | 0.5825 | yes | test | check |

Top similarity neighbours: `auth-flow-reviewer` (0.511), `pr-review-comment-resolver` (0.499), `pr-reviewer` (0.477), `auth-flow-integrator` (0.432), `pr-description-writer` (0.431)

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pr-reviewer` | 0.4949 | 0.4239 | 0.7200 | yes | review, request | review, request |
| `code-reviewer` | 0.4949 | 0.3743 | 0.7433 | yes | review, test, code, change, miss, implementation | review, code, change |
| `ci-failure-debugger` | 0.4949 | 0.4165 | 0.5068 | yes | test, need | - |

Top similarity neighbours: `pr-review-comment-resolver` (0.555), `review-comment-resolver` (0.495), `resilience-pattern-reviewer` (0.463), `repo-code-reviewer` (0.430), `pr-reviewer` (0.424)

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.4968 | 0.1155 | 0.5839 | yes | commit, test, change | test |
| `pr-reviewer` | 0.4968 | 0.1319 | 0.5825 | yes | - | check |
| `review-comment-resolver` | 0.4968 | 0.1175 | 0.5068 | yes | change | - |

Top similarity neighbours: `ci-failure-debugger` (0.497), `ci-log-root-cause-debugger` (0.467), `psc-ci-log-first-failure-reader` (0.421), `api-ops-failure-diagnoser` (0.340), `implicit-ci-failure-reader` (0.330)

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `release-note-writer` | 0.4319 | 0.4941 | 0.6622 | yes | change, turn, complet, user-fac, release, note | change, complet |
| `pr-reviewer` | 0.4319 | 0.2715 | 0.5997 | yes | - | - |
| `code-reviewer` | 0.4319 | 0.3001 | 0.6328 | yes | change, test | change |

Top similarity neighbours: `release-changelog-generator` (0.547), `psc-release-communication-packager` (0.501), `release-note-writer` (0.494), `public-oh-my-changelog-maintenance` (0.482), `public-swebench-changelog-automation` (0.475)

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 186

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `changelog-writer` | 0.2149 | 0.0907 | 0.6622 | yes | change | complet, change |
| `pr-reviewer` | 0.2149 | 0.0435 | 0.5767 | yes | request | chang |
| `code-reviewer` | 0.2149 | 0.0676 | 0.6242 | yes | change | change |

Top similarity neighbours: `identity-ops-failure-diagnoser` (0.397), `auth-flow-reviewer` (0.394), `identity-ops-timeline-builder` (0.351), `security-ops-failure-diagnoser` (0.339), `identity-ops-monitoring-plan-builder` (0.336)

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-for-reporting` | 0.4319 | 0.3990 | 0.6943 | yes | turn | spreadsheet |
| `data-analysis-with-anomaly-focus` | 0.4319 | 0.2330 | 0.6496 | yes | pattern | produce, spreadsheet, pattern |
| `data-analysis-with-validation` | 0.4319 | 0.1587 | 0.6048 | yes | need, most | - |

Top similarity neighbours: `psc-executive-metric-narrator` (0.467), `data-analysis-overview` (0.432), `news-briefing-writer` (0.422), `news-theme-extractor` (0.405), `dashboard-ops-summary-writer` (0.399)

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.5460 | 0.2475 | 0.6496 | yes | - | produce, spreadsheet, pattern |
| `data-analysis-for-root-cause-diagnosis` | 0.5460 | 0.2833 | 0.5533 | yes | - | spreadsheet |
| `data-analysis-with-validation` | 0.5460 | 0.1447 | 0.5074 | yes | most | data, surfac |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.571), `data-analysis-with-anomaly-focus` (0.546), `latency-anomaly-detector` (0.520), `debugging-root-cause-helper` (0.395), `churn-risk-analyser` (0.361)

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 23

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.3195 | 0.2293 | 0.6048 | yes | - | - |
| `data-analysis-with-anomaly-focus` | 0.3195 | 0.3377 | 0.5074 | yes | value, issue | surfac, data |
| `data-analysis-for-root-cause-diagnosis` | 0.3195 | 0.1844 | 0.6074 | yes | - | - |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.466), `psc-data-trust-auditor` (0.440), `latency-anomaly-detector` (0.399), `real-estate-ops-failure-diagnoser` (0.358), `dataset-ops-quality-auditor` (0.351)

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 91

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-with-anomaly-focus` | 0.2298 | 0.2016 | 0.5533 | yes | data | spreadsheet |
| `data-analysis-overview` | 0.2298 | 0.1794 | 0.6533 | yes | - | spreadsheet |
| `data-analysis-with-validation` | 0.2298 | 0.0900 | 0.6074 | yes | data, most | - |

Top similarity neighbours: `metrics-root-cause-diagnoser` (0.375), `latency-anomaly-detector` (0.366), `media-ops-failure-diagnoser` (0.343), `implicit-trace-path-diagnoser` (0.333), `public-swebench-vector-index-tuning` (0.328)

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.5076 | 0.3474 | 0.6943 | yes | broad | spreadsheet |
| `data-analysis-for-root-cause-diagnosis` | 0.5076 | 0.2447 | 0.6575 | yes | - | spreadsheet, evidence |
| `data-analysis-with-anomaly-focus` | 0.5076 | 0.2103 | 0.4582 | no | - | spreadsheet |

Top similarity neighbours: `psc-executive-metric-narrator` (0.518), `data-analysis-for-reporting` (0.508), `dashboard-ops-summary-writer` (0.500), `news-briefing-writer` (0.493), `media-ops-summary-writer` (0.471)

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.4886 | 0.1578 | 0.6940 | yes | pattern | spreadsheet, pattern, produce |
| `data-analysis-for-root-cause-diagnosis` | 0.4886 | 0.1666 | 0.6062 | yes | evidence | uses, spreadsheet |
| `data-analysis-with-anomaly-focus` | 0.4886 | 0.1897 | 0.5688 | yes | pattern | spreadsheet, pattern, produce |

Top similarity neighbours: `data-analysis-for-forecasting` (0.489), `deadline-reminder-planner` (0.331), `capacity-risk-forecaster` (0.321), `tech-news-trend-extractor` (0.309), `psc-anomaly-watchlist-builder` (0.302)

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 32

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `data-analysis-overview` | 0.4430 | 0.2180 | 0.7161 | yes | broad | spreadsheet, produce, strongest |
| `data-analysis-for-reporting` | 0.4430 | 0.2387 | 0.5776 | yes | - | spreadsheet |
| `data-analysis-for-forecasting` | 0.4430 | 0.2792 | 0.5718 | yes | forecast | spreadsheet, produce |

Top similarity neighbours: `priority-sorter` (0.568), `travel-ops-priority-ranker` (0.502), `risk-ops-priority-ranker` (0.495), `robotics-ops-priority-ranker` (0.486), `decision-matrix-builder` (0.486)

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.3205 | 0.1491 | 0.4188 | no | identify | screenshot |
| `accessibility-interaction-auditor` | 0.3205 | 0.0241 | 0.3560 | no | interaction, clue | interaction |
| `public-playwright-interactive` | 0.3205 | 0.1422 | 0.6408 | yes | interaction, browser | browser, interaction |
| `public-openai-playwright` | 0.3205 | 0.0960 | 0.5178 | yes | browser | browser, screenshot |

Top similarity neighbours: `frontend-debugger` (0.350), `ecommerce-ops-failure-diagnoser` (0.345), `ads-ops-failure-diagnoser` (0.325), `playwright-flow-debugger` (0.321), `grant-ops-failure-diagnoser` (0.320)

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `playwright-flow-debugger` | 0.6127 | 0.0964 | 0.4188 | no | screenshot | screenshot |
| `accessibility-interaction-auditor` | 0.6127 | 0.2762 | 0.4608 | no | contrast | contrast |
| `public-openai-screenshot` | 0.6127 | 0.2456 | 0.3397 | no | screenshot, need | screenshot |
| `public-anthropic-webapp-testing` | 0.6127 | 0.1843 | 0.3651 | no | screenshot | screenshot |

Top similarity neighbours: `visual-regression-checker` (0.613), `psc-visual-screenshot-reviewer` (0.522), `implicit-visual-diff-reviewer` (0.515), `mobile-ops-comparison-builder` (0.419), `dashboard-ops-comparison-builder` (0.403)

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.5996 | 0.3422 | 0.4608 | no | - | contrast |
| `playwright-flow-debugger` | 0.5996 | 0.2623 | 0.3560 | no | interaction | interaction |
| `web-ui-tester` | 0.5996 | 0.2634 | 0.4484 | no | interaction, whether | interaction, web |
| `public-anthropic-webapp-testing` | 0.5996 | 0.0951 | 0.4195 | no | - | web |

Top similarity neighbours: `accessibility-interaction-auditor` (0.600), `psc-accessibility-interaction-auditor` (0.518), `accessibility-checker` (0.484), `public-addy-web-accessibility` (0.448), `implicit-browser-flow-investigator` (0.373)

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `deployment-release-verifier` | 0.4102 | 0.2192 | 0.7033 | yes | - | deployment, environment, version |
| `playwright-flow-debugger` | 0.4102 | 0.1925 | 0.5050 | yes | - | failure |
| `web-performance-budget-checker` | 0.4102 | 0.0797 | 0.4783 | no | - | - |

Top similarity neighbours: `public-netlify-deploy` (0.518), `deployment-build-triager` (0.410), `ci-failure-debugger` (0.340), `ci-log-root-cause-debugger` (0.315), `devops-ops-failure-diagnoser` (0.313)

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `deployment-build-triager` | 0.4835 | 0.4641 | 0.7033 | yes | version, environment | deployment, environment, version |
| `visual-regression-checker` | 0.4835 | 0.2861 | 0.4684 | no | - | - |
| `public-netlify-deploy` | 0.4835 | 0.6322 | 0.3772 | yes | production, deploy, netlify | - |
| `public-openai-vercel-deploy` | 0.4835 | 0.3599 | 0.4486 | no | deploy, live, app | deployment |

Top similarity neighbours: `public-netlify-deploy` (0.632), `deployment-release-verifier` (0.483), `deployment-build-triager` (0.464), `public-openai-vercel-deploy` (0.360), `publishing-ops-failure-diagnoser` (0.340)

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `visual-regression-checker` | 0.4529 | 0.2864 | 0.5280 | yes | - | - |
| `deployment-release-verifier` | 0.4529 | 0.1923 | 0.5508 | yes | - | load, evidence |
| `accessibility-interaction-auditor` | 0.4529 | 0.2616 | 0.4428 | no | - | web, clue |

Top similarity neighbours: `public-swebench-distributed-tracing` (0.465), `mobile-ops-summary-writer` (0.463), `web-performance-budget-checker` (0.453), `mobile-ops-quality-auditor` (0.447), `mobile-ops-resource-linker` (0.440)

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 694

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.1591 | 0.0916 | 0.6437 | yes | - | document |
| `document-field-extractor` | 0.1591 | 0.1063 | 0.5776 | yes | - | document |
| `document-converter` | 0.1591 | 0.0856 | 0.5798 | yes | - | document, such, memo, form |

Top similarity neighbours: `travel-ops-summary-writer` (0.457), `travel-ops-risk-reviewer` (0.416), `travel-ops-compliance-checker` (0.385), `travel-ops-dependency-mapper` (0.381), `travel-ops-rewrite-editor` (0.366)

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 9

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.4312 | 0.3998 | 0.6511 | yes | document, mean | document, structure, preserv, mean, content |
| `document-summariser` | 0.4312 | 0.4204 | 0.5124 | yes | document, form | document |
| `document-converter` | 0.4312 | 0.3733 | 0.5581 | yes | document, form | document |

Top similarity neighbours: `travel-ops-rewrite-editor` (0.574), `travel-ops-summary-writer` (0.507), `method-note-builder` (0.484), `travel-ops-handoff-brief-writer` (0.441), `citation-note-extractor` (0.437)

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-rewriter` | 0.4543 | 0.4257 | 0.6511 | yes | document, structure, rewrite | document, structure, preserv, content, mean |
| `document-converter` | 0.4543 | 0.3542 | 0.6476 | yes | document, layout | document |
| `document-summariser` | 0.4543 | 0.3323 | 0.6437 | yes | document | document |

Top similarity neighbours: `travel-ops-rewrite-editor` (0.515), `document-normaliser` (0.454), `method-note-builder` (0.435), `public-office-meeting-notes` (0.432), `facilities-ops-rewrite-editor` (0.429)

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 12

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-summariser` | 0.4059 | 0.2788 | 0.5776 | yes | detail, summary | document |
| `multi-document-comparison-preparer` | 0.4059 | 0.2475 | 0.4787 | no | field, detail | field, clause, document |
| `layout-preserving-converter` | 0.4059 | 0.2516 | 0.5100 | yes | table | document |

Top similarity neighbours: `receipt-extractor` (0.536), `public-office-invoice-organizer` (0.440), `procurement-ops-field-extractor` (0.439), `finance-ops-artifact-packager` (0.435), `public-office-invoice-generator` (0.434)

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-field-extractor` | 0.4703 | 0.1817 | 0.4787 | no | - | document, field, clause |
| `document-normaliser` | 0.4703 | 0.2314 | 0.5582 | yes | section | document, section, structure |
| `document-converter` | 0.4703 | 0.2290 | 0.5213 | yes | - | document |

Top similarity neighbours: `privacy-policy-drafter` (0.488), `multi-document-comparison-preparer` (0.470), `writing-ops-comparison-builder` (0.400), `public-mattpocock-review` (0.400), `legal-ops-comparison-builder` (0.392)

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-normaliser` | 0.4129 | 0.3192 | 0.6476 | yes | clean, content | document |
| `layout-preserving-converter` | 0.4129 | 0.4006 | 0.8143 | yes | convert, preserve, label, layout | convert, document, another, format, layout |
| `document-summariser` | 0.4129 | 0.2535 | 0.5798 | yes | form | document, such, memo, form |

Top similarity neighbours: `public-markitdown` (0.428), `document-converter` (0.413), `layout-preserving-converter` (0.401), `office-to-markdown-converter` (0.399), `public-office-form-builder` (0.390)

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-converter` | 0.4243 | 0.3707 | 0.8143 | yes | layout, markdown, priority, fidelity, note | convert, document, another, format, layout |
| `document-field-extractor` | 0.4243 | 0.2174 | 0.5100 | yes | field | document |
| `document-normaliser` | 0.4243 | 0.2946 | 0.6219 | yes | preserv | document, section |

Top similarity neighbours: `layout-preserving-converter` (0.424), `method-note-builder` (0.397), `public-mattpocock-writing-shape` (0.377), `public-office-form-builder` (0.372), `document-converter` (0.371)

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Family: `github_ci_maintenance`
- Gold skill: `ci-log-root-cause-debugger`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pr-review-comment-resolver` | 0.6584 | 0.2368 | 0.4363 | no | - | - |
| `repo-code-reviewer` | 0.6584 | 0.2812 | 0.5790 | yes | - | test |
| `github-issue-triager` | 0.6584 | 0.3240 | 0.5975 | yes | - | - |
| `release-changelog-generator` | 0.6584 | 0.2707 | 0.5265 | yes | - | - |

Top similarity neighbours: `ci-log-root-cause-debugger` (0.658), `implicit-ci-failure-reader` (0.607), `ci-failure-debugger` (0.534), `psc-ci-log-first-failure-reader` (0.529), `debugging-root-cause-helper` (0.366)

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Family: `github_ci_maintenance`
- Gold skill: `pr-review-comment-resolver`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-openai-gh-address-comments` | 0.5911 | 0.3491 | 0.4251 | no | review, comment | review, comment |
| `review-comment-resolver` | 0.5911 | 0.5076 | 0.7327 | yes | review, comment, code | request, review, comment, code, change |
| `ci-log-root-cause-debugger` | 0.5911 | 0.1962 | 0.4363 | no | - | - |
| `repo-code-reviewer` | 0.5911 | 0.4752 | 0.6830 | yes | review | review |

Top similarity neighbours: `pr-review-comment-resolver` (0.591), `review-comment-resolver` (0.508), `public-mattpocock-review` (0.502), `pr-reviewer` (0.498), `repo-code-reviewer` (0.475)

### `github_ci_maintenance_p3_repo_code_reviewer`

- Family: `github_ci_maintenance`
- Gold skill: `repo-code-reviewer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | 0.4778 | 0.5750 | 0.5790 | yes | test | test |
| `pr-review-comment-resolver` | 0.4778 | 0.3455 | 0.6830 | yes | review, code | review |
| `github-issue-triager` | 0.4778 | 0.3897 | 0.6512 | yes | miss | miss |
| `release-changelog-generator` | 0.4778 | 0.3552 | 0.5796 | yes | - | - |

Top similarity neighbours: `ci-log-root-cause-debugger` (0.575), `ci-failure-debugger` (0.496), `repo-code-reviewer` (0.478), `implicit-ci-failure-reader` (0.449), `debugging-root-cause-helper` (0.436)

### `github_ci_maintenance_p4_github_issue_triager`

- Family: `github_ci_maintenance`
- Gold skill: `github-issue-triager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | 0.3987 | 0.2183 | 0.5975 | yes | - | - |
| `pr-review-comment-resolver` | 0.3987 | 0.2736 | 0.4698 | no | - | - |
| `repo-code-reviewer` | 0.3987 | 0.3168 | 0.6512 | yes | miss | miss |
| `release-changelog-generator` | 0.3987 | 0.2561 | 0.5451 | yes | - | - |

Top similarity neighbours: `public-mattpocock-setup-matt-pocock-skills` (0.476), `public-oh-my-changelog-maintenance` (0.443), `partnerships-ops-failure-diagnoser` (0.427), `real-estate-ops-failure-diagnoser` (0.411), `property-ops-failure-diagnoser` (0.409)

### `github_ci_maintenance_p5_release_changelog_generator`

- Family: `github_ci_maintenance`
- Gold skill: `release-changelog-generator`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `ci-log-root-cause-debugger` | 0.4104 | 0.1679 | 0.5265 | yes | - | - |
| `pr-review-comment-resolver` | 0.4104 | 0.3870 | 0.5882 | yes | turn, change, review, code | extract, request |
| `repo-code-reviewer` | 0.4104 | 0.3571 | 0.5796 | yes | review | - |
| `github-issue-triager` | 0.4104 | 0.3420 | 0.5451 | yes | - | - |

Top similarity neighbours: `psc-release-communication-packager` (0.489), `public-mattpocock-review` (0.438), `release-note-writer` (0.437), `public-office-changelog-generator` (0.428), `pr-reviewer` (0.424)

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Family: `github_ci_maintenance`
- Gold skill: `git-safety-guardrail-installer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-mattpocock-git-guardrails-claude-code` | 0.6705 | 0.6171 | 0.6530 | yes | block, git, push, reset, hard, hook | hook, prevent, dangerou, git, operation, command |
| `public-mattpocock-setup-pre-commit` | 0.6705 | 0.4226 | 0.3537 | no | hook | configure, hook |
| `ci-log-root-cause-debugger` | 0.6705 | 0.2046 | 0.4432 | no | - | command |
| `pr-review-comment-resolver` | 0.6705 | 0.3834 | 0.4113 | no | step, verification | - |

Top similarity neighbours: `git-safety-guardrail-installer` (0.670), `psc-repo-guardrail-hook-installer` (0.653), `public-mattpocock-git-guardrails-claude-code` (0.617), `psc-pr-thread-fix-planner` (0.452), `psc-release-communication-packager` (0.437)

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-dataset-viewer-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-datasets` | 0.4339 | 0.3715 | 0.7311 | yes | dataset, subset, split | hugg, face, dataset, metadata, split, subset |
| `public-huggingface-huggingface-tool-builder` | 0.4339 | 0.1035 | 0.5321 | yes | - | hugg, face |
| `hf-local-model-selector` | 0.4339 | 0.2342 | 0.6257 | yes | model | hugg, face |
| `sentence-transformer-finetuner` | 0.4339 | 0.2130 | 0.3604 | no | split | split |

Top similarity neighbours: `hf-dataset-viewer-inspector` (0.434), `implicit-hf-dataset-inspector` (0.417), `dataset-ops-acceptance-test-builder` (0.391), `dataset-ops-quality-auditor` (0.379), `dataset-ops-risk-reviewer` (0.375)

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-local-model-selector`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 5

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-huggingface-local-models` | 0.4646 | 0.4859 | 0.6159 | yes | local, model, mac, gguf | select, gguf, model, local |
| `public-huggingface-huggingface-best` | 0.4646 | 0.2252 | 0.3226 | no | - | - |
| `hf-dataset-viewer-inspector` | 0.4646 | 0.3632 | 0.6257 | yes | hugg, face, dataset | hugg, face |
| `sentence-transformer-finetuner` | 0.4646 | 0.1957 | 0.3117 | no | - | - |

Top similarity neighbours: `public-huggingface-huggingface-local-models` (0.486), `psc-local-model-fit-selector` (0.481), `psc-hf-dataset-card-inspector` (0.473), `public-huggingface-huggingface-vision-trainer` (0.469), `hf-local-model-selector` (0.465)

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Family: `huggingface_ml_workflows`
- Gold skill: `sentence-transformer-finetuner`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-huggingface-train-sentence-transformers` | 0.6170 | 0.4697 | 0.7465 | yes | pair, sentence-transformer, retrieval | sentence-transformer, retrieval, similarity, train, pair, embedd |
| `public-swebench-similarity-search-patterns` | 0.6170 | 0.3032 | 0.3704 | no | retrieval | retrieval, similarity |
| `hf-dataset-viewer-inspector` | 0.6170 | 0.1386 | 0.3604 | no | split | split |
| `hf-local-model-selector` | 0.6170 | 0.1226 | 0.3117 | no | - | - |

Top similarity neighbours: `sentence-transformer-finetuner` (0.617), `psc-retrieval-result-adjudicator` (0.533), `skill-authoring-guide` (0.529), `skill-router-policy-designer` (0.520), `agent-ops-summary-writer` (0.511)

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Family: `huggingface_ml_workflows`
- Gold skill: `gradio-demo-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 259

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | 0.2475 | 0.1970 | 0.4544 | yes | - | dataset, example |
| `hf-local-model-selector` | 0.2475 | 0.1764 | 0.4465 | yes | model | model |
| `sentence-transformer-finetuner` | 0.2475 | 0.2716 | 0.2751 | yes | plan, check, fine-tun | - |
| `hf-zerogpu-space-deployer` | 0.2475 | 0.0720 | 0.4229 | no | - | constraint |

Top similarity neighbours: `public-huggingface-huggingface-trackio` (0.450), `web-ops-scenario-planner` (0.443), `support-ticket-triager` (0.418), `web-ui-tester` (0.406), `webhook-setup-planner` (0.374)

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-zerogpu-space-deployer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | 0.6624 | 0.3331 | 0.5148 | yes | hugg, face | hugg, face |
| `hf-local-model-selector` | 0.6624 | 0.4501 | 0.6089 | yes | hugg, face | hugg, face |
| `sentence-transformer-finetuner` | 0.6624 | 0.2067 | 0.2329 | no | - | - |
| `gradio-demo-builder` | 0.6624 | 0.4996 | 0.4229 | no | gradio, constraint | constraint |

Top similarity neighbours: `public-huggingface-huggingface-zerogpu` (0.692), `hf-zerogpu-space-deployer` (0.662), `public-huggingface-huggingface-llm-trainer` (0.553), `public-huggingface-huggingface-vision-trainer` (0.535), `gradio-demo-builder` (0.500)

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-community-eval-runner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `hf-dataset-viewer-inspector` | 0.5127 | 0.3708 | 0.6789 | yes | hugg, face, dataset | hugg, face |
| `hf-local-model-selector` | 0.5127 | 0.3325 | 0.7039 | yes | hugg, face | hugg, face, model, hardware |
| `sentence-transformer-finetuner` | 0.5127 | 0.2601 | 0.4427 | no | evaluation, plan | plan, evaluation |
| `gradio-demo-builder` | 0.5127 | 0.3374 | 0.4945 | no | dataset, gradio | model |

Top similarity neighbours: `hf-community-eval-runner` (0.513), `public-huggingface-huggingface-vision-trainer` (0.488), `psc-hf-dataset-card-inspector` (0.476), `public-huggingface-datasets` (0.469), `public-huggingface-huggingface-llm-trainer` (0.466)

### `implicit_p10_trace_path`

- Family: `implicit_field_stress`
- Gold skill: `implicit-trace-path-diagnoser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-slo-alert-author` | 0.4729 | 0.1763 | 0.5090 | yes | - | - |
| `distributed-trace-investigator` | 0.4729 | 0.5669 | 0.5327 | yes | distribut, trace, span, locate, latency | distribut, trace, span, locate, latency, fail, call, dependency |
| `prometheus-alert-rule-writer` | 0.4729 | 0.2686 | 0.3596 | no | - | - |

Top similarity neighbours: `distributed-trace-investigator` (0.567), `public-swebench-distributed-tracing` (0.546), `latency-anomaly-detector` (0.504), `implicit-trace-path-diagnoser` (0.473), `service-mesh-traffic-debugger` (0.446)

### `implicit_p1_pdf_answer`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-evidence-answerer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 69

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-pdf-table-reconstructor` | 0.1974 | 0.2575 | 0.7402 | yes | pdf, packet, page, reconstruct | work, pdf, packet, page |
| `pdf-question-answerer` | 0.1974 | 0.1818 | 0.6298 | yes | answer, pdf, page, evidence | pdf, answer, page, evidence |
| `pdf-layout-table-extractor` | 0.1974 | 0.2575 | 0.5207 | yes | page, evidence, table | page, evidence, extract |

Top similarity neighbours: `travel-ops-dependency-mapper` (0.312), `travel-ops-summary-writer` (0.309), `travel-ops-artifact-packager` (0.286), `logistics-ops-dependency-mapper` (0.282), `travel-ops-evidence-grounder` (0.281)

### `implicit_p2_pdf_table`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-table-reconstructor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-pdf-evidence-answerer` | 0.4901 | 0.4721 | 0.7402 | yes | extract, pdf, page, answer | work, pdf, packet, page |
| `pdf-layout-table-extractor` | 0.4901 | 0.6111 | 0.6568 | yes | extract, page, row | row, column, page |
| `pdf-question-answerer` | 0.4901 | 0.5503 | 0.3658 | yes | pdf, page, answer | pdf, page |

Top similarity neighbours: `pdf-layout-table-extractor` (0.611), `public-office-invoice-template` (0.574), `pdf-question-answerer` (0.550), `public-office-pdf-extraction` (0.526), `public-office-pdf-form-filler` (0.496)

### `implicit_p3_browser_flow`

- Family: `implicit_field_stress`
- Gold skill: `implicit-browser-flow-investigator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 395

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-visual-diff-reviewer` | 0.0743 | -0.0380 | 0.5147 | yes | - | state, screenshot |
| `playwright-flow-debugger` | 0.0743 | 0.1475 | 0.4990 | yes | reproduce, console, network, evidence, failure | interaction, console, network, screenshot |
| `visual-regression-checker` | 0.0743 | 0.0563 | 0.3970 | yes | - | screenshot |

Top similarity neighbours: `ads-ops-failure-diagnoser` (0.304), `fundraising-ops-failure-diagnoser` (0.289), `frontend-debugger` (0.270), `sales-ops-failure-diagnoser` (0.268), `ecommerce-ops-failure-diagnoser` (0.263)

### `implicit_p4_visual_diff`

- Family: `implicit_field_stress`
- Gold skill: `implicit-visual-diff-reviewer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-browser-flow-investigator` | 0.5356 | 0.3078 | 0.5147 | yes | screenshot | state, screenshot |
| `visual-regression-checker` | 0.5356 | 0.5937 | 0.6475 | yes | compare, baseline, screenshot, layout, shift, clipp, acros | compare, current, visual, acros, screenshot, viewport, layout, regression |
| `playwright-flow-debugger` | 0.5356 | 0.2457 | 0.2597 | no | screenshot | screenshot |

Top similarity neighbours: `visual-regression-checker` (0.594), `psc-visual-screenshot-reviewer` (0.552), `implicit-visual-diff-reviewer` (0.536), `mobile-ops-rewrite-editor` (0.499), `mobile-ops-summary-writer` (0.470)

### `implicit_p5_ci_failure`

- Family: `implicit_field_stress`
- Gold skill: `implicit-ci-failure-reader`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-review-comment-planner` | 0.5801 | 0.0984 | 0.3685 | no | - | - |
| `ci-log-root-cause-debugger` | 0.5801 | 0.4804 | 0.5365 | yes | error | failure |
| `repo-code-reviewer` | 0.5801 | 0.2345 | 0.3040 | no | - | - |

Top similarity neighbours: `implicit-ci-failure-reader` (0.580), `ci-failure-debugger` (0.503), `psc-ci-log-first-failure-reader` (0.495), `ci-log-root-cause-debugger` (0.480), `bioinformatics-ops-failure-diagnoser` (0.412)

### `implicit_p6_review_comments`

- Family: `implicit_field_stress`
- Gold skill: `implicit-review-comment-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 36

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-ci-failure-reader` | 0.2904 | 0.1704 | 0.3685 | no | - | - |
| `pr-review-comment-resolver` | 0.2904 | 0.4576 | 0.4949 | yes | code, review | turn, review, comment |
| `repo-code-reviewer` | 0.2904 | 0.5145 | 0.3593 | yes | review | review |

Top similarity neighbours: `review-comment-resolver` (0.560), `code-reviewer` (0.517), `repo-code-reviewer` (0.514), `pr-review-comment-resolver` (0.458), `pr-reviewer` (0.455)

### `implicit_p7_hf_dataset`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-dataset-inspector`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-hf-local-model-chooser` | 0.6150 | 0.2231 | 0.6244 | yes | - | - |
| `hf-dataset-viewer-inspector` | 0.6150 | 0.6101 | 0.6948 | yes | inspect, dataset, split, row, example, schema | inspect, dataset, split, subset, example, schema |
| `hf-local-model-selector` | 0.6150 | 0.2412 | 0.4445 | no | - | - |

Top similarity neighbours: `implicit-hf-dataset-inspector` (0.615), `hf-dataset-viewer-inspector` (0.610), `data-analysis-overview` (0.530), `dataset-ops-risk-reviewer` (0.486), `dataset-ops-summary-writer` (0.479)

### `implicit_p8_hf_model`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-local-model-chooser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 407

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-hf-dataset-inspector` | 0.1650 | 0.1681 | 0.6244 | yes | - | - |
| `hf-local-model-selector` | 0.1650 | 0.2938 | 0.7390 | yes | local, model, quantization | local, hugg, face, gguf, model, memory, quantization, latency |
| `hf-dataset-viewer-inspector` | 0.1650 | 0.1407 | 0.4489 | yes | - | hugg, face |

Top similarity neighbours: `support-ticket-triager` (0.365), `psc-local-model-fit-selector` (0.331), `public-huggingface-huggingface-vision-trainer` (0.322), `public-swebench-vector-index-tuning` (0.314), `ml-ops-scenario-planner` (0.311)

### `implicit_p9_alert_rule`

- Family: `implicit_field_stress`
- Gold skill: `implicit-slo-alert-author`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `implicit-trace-path-diagnoser` | 0.5679 | 0.1767 | 0.5090 | yes | - | - |
| `prometheus-alert-rule-writer` | 0.5679 | 0.5634 | 0.6465 | yes | alert, rule, metric, window, severity, label | alert, rule, slos, metric, name, window, label, severity |
| `distributed-trace-investigator` | 0.5679 | 0.2228 | 0.1912 | no | - | - |

Top similarity neighbours: `implicit-slo-alert-author` (0.568), `prometheus-alert-rule-writer` (0.563), `slo-breach-checker` (0.508), `support-ops-acceptance-test-builder` (0.425), `customer-success-ops-acceptance-test-builder` (0.425)

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `incident-summary-writer` | 0.4676 | 0.3133 | 0.6402 | yes | - | summary, metric, operational |
| `metrics-root-cause-diagnoser` | 0.4676 | 0.2161 | 0.6323 | yes | - | current, operational |
| `latency-anomaly-detector` | 0.4676 | 0.2790 | 0.4758 | no | service | metric, service |

Top similarity neighbours: `public-swebench-service-mesh-observability` (0.516), `service-mesh-traffic-debugger` (0.472), `metrics-overview` (0.468), `public-swebench-distributed-tracing` (0.460), `public-swebench-slo-implementation` (0.443)

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `metrics-root-cause-diagnoser` | 0.6057 | 0.2645 | 0.4881 | no | identify | regression |
| `metrics-overview` | 0.6057 | 0.4380 | 0.4758 | no | service, snapshot, metric | metric, service |
| `slo-breach-checker` | 0.6057 | 0.3682 | 0.4578 | no | service, whether, metric | metric, service |

Top similarity neighbours: `latency-anomaly-detector` (0.606), `public-swebench-distributed-tracing` (0.598), `cloud-ops-quality-auditor` (0.467), `cloud-ops-failure-diagnoser` (0.453), `cloud-ops-intake-classifier` (0.449)

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `capacity-risk-forecaster` | 0.5644 | 0.3104 | 0.3837 | no | risk | risk |
| `metrics-overview` | 0.5644 | 0.4863 | 0.6004 | yes | service, snapshot | service, metric |
| `metrics-root-cause-diagnoser` | 0.5644 | 0.3178 | 0.5532 | yes | - | - |

Top similarity neighbours: `slo-breach-checker` (0.564), `resilience-pattern-reviewer` (0.495), `service-mesh-traffic-debugger` (0.487), `metrics-overview` (0.486), `sre-ops-risk-reviewer` (0.475)

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Plausible listed alternatives: 0
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `slo-breach-checker` | 0.5465 | 0.4465 | 0.3837 | no | risk, service, slo | risk |
| `metrics-root-cause-diagnoser` | 0.5465 | 0.2580 | 0.3033 | no | likely, operational, current, cause | likely |
| `metrics-overview` | 0.5465 | 0.2328 | 0.3813 | no | service, snapshot, focu, operational, current | signal |

Top similarity neighbours: `capacity-risk-forecaster` (0.546), `slo-breach-checker` (0.447), `slo-breach-narrative-writer` (0.428), `risk-ops-failure-diagnoser` (0.427), `cloud-ops-scenario-planner` (0.422)

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `latency-anomaly-detector` | 0.4856 | 0.4443 | 0.4881 | yes | service, latency | regression |
| `capacity-risk-forecaster` | 0.4856 | 0.2928 | 0.3033 | no | queue, pressure | likely |
| `incident-summary-writer` | 0.4856 | 0.2018 | 0.4900 | no | - | operational, incident |

Top similarity neighbours: `service-mesh-traffic-debugger` (0.508), `public-swebench-distributed-tracing` (0.502), `metrics-root-cause-diagnoser` (0.486), `support-ops-failure-diagnoser` (0.465), `cloud-ops-failure-diagnoser` (0.461)

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `metrics-overview` | 0.3814 | 0.2466 | 0.6402 | yes | service, snapshot | metric, operational, summary |
| `metrics-root-cause-diagnoser` | 0.3814 | 0.1205 | 0.4900 | no | incident | incident, operational |
| `slo-breach-checker` | 0.3814 | 0.1892 | 0.4430 | no | service | metric |

Top similarity neighbours: `incident-ops-summary-writer` (0.413), `incident-ops-failure-diagnoser` (0.409), `incident-ops-resource-linker` (0.394), `incident-ops-timeline-builder` (0.388), `public-office-microsoft-teams` (0.386)

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-briefing-writer` | 0.5028 | 0.4618 | 0.7463 | yes | summary, news | news, summary, provid, item, theme, brief |
| `source-grounding-extractor` | 0.5028 | 0.4106 | 0.5870 | yes | summary, news | news, summary, provid, content |

Top similarity neighbours: `news-summariser` (0.503), `news-briefing-writer` (0.462), `paper-summariser` (0.449), `general-source-summariser` (0.434), `journalism-ops-summary-writer` (0.426)

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-summariser` | 0.4626 | 0.3106 | 0.7463 | yes | summary | brief, provid, news, item, summary, theme |
| `tech-news-trend-extractor` | 0.4626 | 0.2272 | 0.6218 | yes | signal, just | provid, news |

Top similarity neighbours: `events-ops-summary-writer` (0.498), `news-briefing-writer` (0.463), `events-ops-priority-ranker` (0.441), `incident-summary-writer` (0.432), `events-ops-handoff-brief-writer` (0.423)

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 24

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-summariser` | 0.3918 | 0.1907 | 0.5870 | yes | - | provid, news, content, summary |
| `news-briefing-writer` | 0.3918 | 0.2090 | 0.5504 | yes | - | extract, source-ground, provid, news, need, summary |

Top similarity neighbours: `product-ops-evidence-grounder` (0.545), `vendor-ops-evidence-grounder` (0.477), `marketing-ops-evidence-grounder` (0.476), `ads-ops-evidence-grounder` (0.471), `manufacturing-ops-evidence-grounder` (0.454)

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `tech-news-trend-extractor` | 0.6440 | 0.5699 | 0.6820 | yes | acros, tech, news | topic, acros, provid, news, know, appear |
| `news-briefing-writer` | 0.6440 | 0.4330 | 0.7072 | yes | extract, theme, news | extract, theme, provid, news, item, summary, brief |

Top similarity neighbours: `news-theme-extractor` (0.644), `tech-news-trend-extractor` (0.570), `news-summariser` (0.455), `related-work-synthesiser` (0.449), `news-briefing-writer` (0.433)

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `news-theme-extractor` | 0.7194 | 0.4448 | 0.6820 | yes | pattern, acros, news | news, provid, topic, know, appear, acros |
| `news-briefing-writer` | 0.7194 | 0.4735 | 0.6218 | yes | news, why, they, matter | news, provid |

Top similarity neighbours: `tech-news-trend-extractor` (0.719), `news-briefing-writer` (0.473), `social-ops-summary-writer` (0.447), `news-theme-extractor` (0.445), `public-office-news-monitor` (0.438)

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Family: `observability_reliability`
- Gold skill: `prometheus-alert-rule-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-prometheus-configuration` | 0.5214 | 0.4248 | 0.5602 | yes | alert, metric | prometheu, alert, metric |
| `slo-breach-checker` | 0.5214 | 0.4433 | 0.6031 | yes | metric | metric |
| `grafana-dashboard-builder` | 0.5214 | 0.3908 | 0.3794 | no | querie, build, dashboard | threshold |
| `distributed-trace-investigator` | 0.5214 | 0.3192 | 0.4400 | no | latency | - |

Top similarity neighbours: `prometheus-alert-rule-writer` (0.521), `ecommerce-ops-monitoring-plan-builder` (0.467), `dashboard-ops-acceptance-test-builder` (0.462), `metrics-overview` (0.453), `dashboard-ops-scenario-planner` (0.451)

### `observability_reliability_p2_grafana_dashboard_builder`

- Family: `observability_reliability`
- Gold skill: `grafana-dashboard-builder`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-grafana-dashboards` | 0.7131 | 0.6093 | 0.6667 | yes | grafana, dashboard | build, grafana, dashboard |
| `public-swebench-python-observability` | 0.7131 | 0.2322 | 0.2812 | no | - | - |
| `metrics-overview` | 0.7131 | 0.4249 | 0.4927 | no | dashboard, service, health | dashboard |
| `prometheus-alert-rule-writer` | 0.7131 | 0.4334 | 0.3794 | no | threshold | threshold |

Top similarity neighbours: `grafana-dashboard-builder` (0.713), `public-swebench-grafana-dashboards` (0.609), `dashboard-ops-risk-reviewer` (0.460), `dashboard-ops-compliance-checker` (0.455), `dashboard-ops-quality-auditor` (0.446)

### `observability_reliability_p3_distributed_trace_investigator`

- Family: `observability_reliability`
- Gold skill: `distributed-trace-investigator`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-distributed-tracing` | 0.4696 | 0.4360 | 0.5285 | yes | acros | distribut |
| `public-swebench-python-observability` | 0.4696 | 0.2936 | 0.4399 | no | - | distribut |
| `metrics-root-cause-diagnoser` | 0.4696 | 0.2941 | 0.4572 | no | - | - |
| `prometheus-alert-rule-writer` | 0.4696 | 0.3218 | 0.4400 | no | - | - |

Top similarity neighbours: `latency-anomaly-detector` (0.476), `implicit-trace-path-diagnoser` (0.471), `distributed-trace-investigator` (0.470), `service-mesh-traffic-debugger` (0.440), `public-swebench-distributed-tracing` (0.436)

### `observability_reliability_p4_slo_breach_narrative_writer`

- Family: `observability_reliability`
- Gold skill: `slo-breach-narrative-writer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `incident-summary-writer` | 0.6331 | 0.6156 | 0.5918 | yes | timeline, impact, action | timeline, impact, action |
| `slo-breach-checker` | 0.6331 | 0.3835 | 0.6714 | yes | slo | slo |
| `prometheus-alert-rule-writer` | 0.6331 | 0.3490 | 0.5079 | yes | write | write |
| `grafana-dashboard-builder` | 0.6331 | 0.1115 | 0.3412 | no | - | - |

Top similarity neighbours: `slo-breach-narrative-writer` (0.633), `incident-summary-writer` (0.616), `incident-ops-summary-writer` (0.547), `meeting-notes-action-extractor` (0.493), `public-oh-my-changelog-maintenance` (0.462)

### `observability_reliability_p5_resilience_pattern_reviewer`

- Family: `observability_reliability`
- Gold skill: `resilience-pattern-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-python-resilience` | 0.4603 | 0.4378 | 0.5768 | yes | retry, timeout, backoff | service, retrie, timeout, backoff, failure |
| `dependency-risk-auditor` | 0.4603 | 0.2928 | 0.4152 | no | review, risk | review |
| `prometheus-alert-rule-writer` | 0.4603 | 0.3162 | 0.4644 | no | - | - |
| `grafana-dashboard-builder` | 0.4603 | 0.2133 | 0.4749 | no | - | - |

Top similarity neighbours: `resilience-pattern-reviewer` (0.460), `public-swebench-python-resilience` (0.438), `api-security-threat-reviewer` (0.406), `contract-risk-reviewer` (0.400), `api-ops-risk-reviewer` (0.387)

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Family: `observability_reliability`
- Gold skill: `service-mesh-traffic-debugger`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-swebench-service-mesh-observability` | 0.7188 | 0.4590 | 0.6549 | yes | debug | debug, service, mesh |
| `public-swebench-istio-traffic-management` | 0.7188 | 0.4448 | 0.4873 | no | rout, traffic | traffic, service, mesh, rout |
| `public-swebench-linkerd-patterns` | 0.7188 | 0.4371 | 0.4581 | no | traffic | traffic, service, mesh |
| `prometheus-alert-rule-writer` | 0.7188 | 0.2509 | 0.4411 | no | rule | rule |

Top similarity neighbours: `service-mesh-traffic-debugger` (0.719), `public-swebench-service-mesh-observability` (0.459), `public-swebench-istio-traffic-management` (0.445), `public-swebench-linkerd-patterns` (0.437), `service-dependency-mapper` (0.385)

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-ocr-extractor` | 0.5425 | 0.4491 | 0.6087 | yes | extract | page |
| `office-to-markdown-converter` | 0.5425 | 0.2439 | 0.4780 | no | table | table |
| `public-office-pdf-extraction` | 0.5425 | 0.4342 | 0.3743 | no | table, extract | table |
| `public-pdf` | 0.5425 | 0.3781 | 0.4328 | no | pdf, table, anyth, form, read, extract | page, pdf, form, table, read |

Top similarity neighbours: `pdf-layout-table-extractor` (0.569), `pdf-layout-reviewer` (0.542), `public-office-pdf-watermark` (0.489), `psc-pdf-native-extraction-pack` (0.468), `public-office-pdf-form-filler` (0.466)

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | 0.6417 | 0.3919 | 0.6087 | yes | pdf, page | page |
| `office-to-markdown-converter` | 0.6417 | 0.2515 | 0.5097 | yes | - | preserv |
| `document-field-extractor` | 0.6417 | 0.2501 | 0.4120 | no | - | extract |

Top similarity neighbours: `pdf-ocr-extractor` (0.642), `pdf-ocr-cleaner` (0.638), `public-office-pdf-ocr` (0.571), `psc-pdf-scan-ocr-recovery` (0.556), `public-office-smart-ocr` (0.518)

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.6431 | 0.3573 | 0.5942 | yes | document | document, preserv |
| `document-rewriter` | 0.6431 | 0.4280 | 0.4779 | no | document, substantive | document, preserv, structure |
| `public-docx` | 0.6431 | 0.5139 | 0.5794 | yes | docx, word, document, edit, comment, change | document, track, change, comment, word, edit |
| `public-office-docx-manipulation` | 0.6431 | 0.4314 | 0.5587 | yes | word, document, edit | document, word, edit |

Top similarity neighbours: `docx-redline-editor` (0.643), `vendor-ops-rewrite-editor` (0.561), `pdf-layout-reviewer` (0.532), `docs-ops-risk-reviewer` (0.531), `pdf-redaction-reviewer` (0.523)

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.5114 | 0.1621 | 0.3666 | no | - | spreadsheet |
| `data-analysis-with-validation` | 0.5114 | 0.3939 | 0.5297 | yes | check, assumption, whether | assumption |
| `public-xlsx` | 0.5114 | 0.4785 | 0.4351 | yes | xlsx | spreadsheet, formula, reference, sheet |
| `public-office-xlsx-manipulation` | 0.5114 | 0.4145 | 0.2712 | no | - | spreadsheet |

Top similarity neighbours: `xlsx-formula-model-builder` (0.612), `spreadsheet-formula-auditor` (0.511), `public-xlsx` (0.478), `public-swebench-xlsx` (0.456), `public-office-xlsx-manipulation` (0.414)

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `office-to-markdown-converter` | 0.6682 | 0.2089 | 0.4661 | no | hierarchy | slide, hierarchy |
| `pdf-layout-reviewer` | 0.6682 | 0.4179 | 0.6589 | yes | review, visual, alignment | review, visual, alignment |
| `public-pptx` | 0.6682 | 0.4032 | 0.4232 | no | pptx, presentation, need, text | presentation, slide, text |
| `public-office-ppt-visual` | 0.6682 | 0.5828 | 0.6293 | yes | presentation, visual | presentation, slide, visual |

Top similarity neighbours: `slide-deck-visual-auditor` (0.668), `public-office-ppt-visual` (0.583), `psc-visual-screenshot-reviewer` (0.434), `slide-outline-builder` (0.434), `psc-related-work-synthesizer` (0.420)

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-layout-reviewer` | 0.5433 | 0.3664 | 0.4780 | no | table, layout | table |
| `docx-redline-editor` | 0.5433 | 0.5413 | 0.5942 | yes | track, change | document, preserv |
| `document-converter` | 0.5433 | 0.3757 | 0.6259 | yes | convert, markdown, layout | convert, document, markdown |

Top similarity neighbours: `office-to-markdown-converter` (0.543), `docx-redline-editor` (0.541), `public-markitdown` (0.446), `layout-preserving-converter` (0.444), `public-docx` (0.443)

### `office_business_automation_p1_xlsx_formula_model_builder`

- Family: `office_business_automation`
- Gold skill: `xlsx-formula-model-builder`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-xlsx-manipulation` | 0.6088 | 0.2040 | 0.4294 | no | spreadsheet | spreadsheet |
| `public-swebench-xlsx` | 0.6088 | 0.2887 | 0.4764 | no | formula, spreadsheet | formula, spreadsheet, input, output, sheet |
| `public-office-data-analysis` | 0.6088 | 0.2945 | 0.4398 | no | build, spreadsheet | build, spreadsheet |
| `airtable-workflow-automator` | 0.6088 | 0.4446 | 0.5053 | yes | airtable, automation | - |

Top similarity neighbours: `xlsx-formula-model-builder` (0.609), `spreadsheet-formula-auditor` (0.488), `airtable-workflow-automator` (0.445), `public-office-airtable-automation` (0.435), `public-office-dcf-valuation` (0.399)

### `office_business_automation_p2_airtable_workflow_automator`

- Family: `office_business_automation`
- Gold skill: `airtable-workflow-automator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-airtable-automation` | 0.7116 | 0.6708 | 0.8337 | yes | airtable, automation, view, trigger | airtable, view, automation, trigger, integration, workflow |
| `public-office-crm-automation` | 0.7116 | 0.3413 | 0.4674 | no | automation | automation, workflow |
| `xlsx-formula-model-builder` | 0.7116 | 0.2794 | 0.5053 | yes | - | - |
| `notion-research-database-builder` | 0.7116 | 0.3354 | 0.5111 | yes | field | field, workflow |

Top similarity neighbours: `airtable-workflow-automator` (0.712), `public-office-airtable-automation` (0.671), `public-office-intercom-automation` (0.404), `public-office-linear-automation` (0.377), `partnerships-ops-acceptance-test-builder` (0.369)

### `office_business_automation_p3_notion_research_database_builder`

- Family: `office_business_automation`
- Gold skill: `notion-research-database-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-notion-automation` | 0.6945 | 0.4183 | 0.6671 | yes | notion, database, template | notion, database, template, workflow |
| `public-openai-notion-research-documentation` | 0.6945 | 0.5308 | 0.5366 | yes | notion, research | notion, research |
| `xlsx-formula-model-builder` | 0.6945 | 0.2361 | 0.4496 | no | structure | - |
| `airtable-workflow-automator` | 0.6945 | 0.2830 | 0.5111 | yes | - | field, workflow |

Top similarity neighbours: `notion-research-database-builder` (0.695), `thesis-ops-normalizer` (0.540), `public-openai-notion-research-documentation` (0.531), `thesis-ops-summary-writer` (0.499), `thesis-ops-resource-linker` (0.497)

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Family: `office_business_automation`
- Gold skill: `calendar-scheduling-optimizer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-calendar-automation` | 0.4597 | 0.3807 | 0.7150 | yes | meet, schedul | time, calendar, meet, block |
| `meeting-agenda-builder` | 0.4597 | 0.4570 | 0.4181 | yes | note, meet | meet |
| `xlsx-formula-model-builder` | 0.4597 | 0.0472 | 0.3532 | no | - | - |
| `airtable-workflow-automator` | 0.4597 | 0.1876 | 0.3932 | no | - | - |

Top similarity neighbours: `meeting-scheduler` (0.535), `meeting-summary-writer` (0.477), `calendar-scheduling-optimizer` (0.460), `meeting-agenda-builder` (0.457), `meeting-notes-action-extractor` (0.456)

### `office_business_automation_p5_meeting_notes_action_extractor`

- Family: `office_business_automation`
- Gold skill: `meeting-notes-action-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-meeting-notes` | 0.6555 | 0.4303 | 0.5451 | yes | - | - |
| `meeting-followup-extractor` | 0.6555 | 0.5992 | 0.7336 | yes | extract, action, owner | extract, action, owner, follow-up, meet |
| `xlsx-formula-model-builder` | 0.6555 | 0.2451 | 0.3643 | no | - | - |
| `airtable-workflow-automator` | 0.6555 | 0.2609 | 0.4419 | no | - | - |

Top similarity neighbours: `meeting-notes-action-extractor` (0.655), `meeting-followup-extractor` (0.599), `weekly-planner` (0.583), `meeting-summary-writer` (0.539), `meeting-agenda-builder` (0.536)

### `office_business_automation_p6_email_classification_router`

- Family: `office_business_automation`
- Gold skill: `email-classification-router`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-email-classifier` | 0.6775 | 0.4772 | 0.6024 | yes | email, priority | email, priority, requir, action |
| `public-office-gmail-workflows` | 0.6775 | 0.2673 | 0.3930 | no | email | email |
| `public-office-suspicious-email` | 0.6775 | 0.4335 | 0.4373 | no | email | email |
| `xlsx-formula-model-builder` | 0.6775 | 0.0971 | 0.2803 | no | - | - |

Top similarity neighbours: `email-classification-router` (0.677), `email-ops-priority-ranker` (0.496), `email-action-extractor` (0.493), `professor-email-reply` (0.489), `email-ops-risk-reviewer` (0.488)

### `pdf_document_operations_p1_pdf_question_answerer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-question-answerer`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 219

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-layout-table-extractor` | 0.2043 | 0.1461 | 0.5035 | yes | evidence, page | page, evidence |
| `pdf-ocr-cleaner` | 0.2043 | 0.0457 | 0.5054 | yes | page | page |
| `pdf-form-filler` | 0.2043 | 0.1024 | 0.5017 | yes | pdf | pdf |
| `pdf-redaction-reviewer` | 0.2043 | 0.2242 | 0.5762 | yes | evidence, pdf | pdf, content, evidence |

Top similarity neighbours: `travel-ops-evidence-grounder` (0.378), `travel-ops-summary-writer` (0.333), `supply-chain-ops-evidence-grounder` (0.322), `compliance-ops-evidence-grounder` (0.320), `travel-ops-compliance-checker` (0.318)

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Family: `pdf_document_operations`
- Gold skill: `pdf-layout-table-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | 0.5897 | 0.4106 | 0.5035 | yes | pdf, page, answer, question | page, evidence |
| `pdf-ocr-cleaner` | 0.5897 | 0.3307 | 0.6220 | yes | page, anchor | pdfs, page |
| `pdf-form-filler` | 0.5897 | 0.3532 | 0.4926 | no | pdf | field |
| `pdf-redaction-reviewer` | 0.5897 | 0.2891 | 0.4572 | no | pdf | evidence |

Top similarity neighbours: `pdf-layout-table-extractor` (0.590), `public-office-invoice-template` (0.528), `public-office-pdf-extraction` (0.508), `implicit-pdf-table-reconstructor` (0.479), `public-office-pdf-form-filler` (0.440)

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Family: `pdf_document_operations`
- Gold skill: `pdf-ocr-cleaner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | 0.7429 | 0.4168 | 0.5054 | yes | page, pdf | page |
| `pdf-layout-table-extractor` | 0.7429 | 0.6270 | 0.6220 | yes | page, table, extract | pdfs, page |
| `pdf-form-filler` | 0.7429 | 0.3238 | 0.4451 | no | pdf | - |
| `pdf-redaction-reviewer` | 0.7429 | 0.3919 | 0.4566 | no | pdf | - |

Top similarity neighbours: `pdf-ocr-cleaner` (0.743), `pdf-ocr-extractor` (0.698), `psc-pdf-scan-ocr-recovery` (0.648), `pdf-layout-table-extractor` (0.627), `public-office-pdf-ocr` (0.626)

### `pdf_document_operations_p4_pdf_form_filler`

- Family: `pdf_document_operations`
- Gold skill: `pdf-form-filler`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `public-office-pdf-form-filler` | 0.4894 | 0.4535 | 0.6335 | yes | pdf | fill, pdf, form |
| `document-field-extractor` | 0.4894 | 0.2915 | 0.3294 | no | - | field |
| `pdf-question-answerer` | 0.4894 | 0.2822 | 0.5017 | yes | pdf | pdf |
| `pdf-layout-table-extractor` | 0.4894 | 0.3075 | 0.4926 | no | - | field |

Top similarity neighbours: `pdf-form-filler` (0.489), `public-office-pdf-form-filler` (0.454), `public-office-expense-tracker` (0.449), `receipt-extractor` (0.428), `invoice-payment-checker` (0.423)

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-redaction-reviewer`
- Plausible listed alternatives: 1
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `privacy-risk-reviewer` | 0.5848 | 0.2339 | 0.4973 | no | - | review, risk |
| `public-office-contract-review` | 0.5848 | 0.4120 | 0.4852 | no | - | risk |
| `public-openai-pdf` | 0.5848 | 0.3511 | 0.3958 | no | pdf, such | review, pdf |
| `pdf-question-answerer` | 0.5848 | 0.4262 | 0.5762 | yes | pdf | pdf, content, evidence |

Top similarity neighbours: `pdf-redaction-reviewer` (0.585), `psc-pdf-redaction-pass` (0.547), `psc-pdf-evidence-qa` (0.442), `pdf-layout-reviewer` (0.442), `public-office-pdf-watermark` (0.440)

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Family: `pdf_document_operations`
- Gold skill: `pdf-to-docx-converter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `pdf-question-answerer` | 0.6068 | 0.3637 | 0.4143 | no | pdf, answer, question | pdf |
| `pdf-layout-table-extractor` | 0.6068 | 0.5387 | 0.5832 | yes | table, preserv | preserv, table |
| `pdf-ocr-cleaner` | 0.6068 | 0.3279 | 0.5004 | yes | - | - |
| `pdf-form-filler` | 0.6068 | 0.3483 | 0.4258 | no | pdf | pdf |

Top similarity neighbours: `pdf-to-docx-converter` (0.607), `pdf-layout-table-extractor` (0.539), `layout-preserving-converter` (0.496), `implicit-pdf-table-reconstructor` (0.474), `public-office-pdf-extraction` (0.434)

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `weekly-planner` | 0.6178 | 0.4975 | 0.6665 | yes | need, week, extract | note, need, structur, plan |
| `task-extractor` | 0.6178 | 0.5337 | 0.6002 | yes | need, extract | note, need, plan, summary |

Top similarity neighbours: `meeting-agenda-builder` (0.618), `task-extractor` (0.534), `meeting-summary-writer` (0.526), `meeting-ops-summary-writer` (0.515), `meeting-followup-extractor` (0.513)

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `meeting-followup-extractor` | 0.6305 | 0.4959 | 0.6969 | yes | meet, summary | summary, complet, meet, need, list |
| `task-extractor` | 0.6305 | 0.4663 | 0.6053 | yes | summary, note | summary, need, plan |

Top similarity neighbours: `meeting-summary-writer` (0.630), `meeting-notes-action-extractor` (0.589), `meeting-ops-summary-writer` (0.584), `meeting-agenda-builder` (0.530), `meeting-ops-rewrite-editor` (0.520)

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 7

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `meeting-summary-writer` | 0.4765 | 0.5250 | 0.6969 | yes | need, meet, happen | complet, meet, need, list, summary |
| `task-extractor` | 0.4765 | 0.4417 | 0.6783 | yes | need, note | extract, need, summary |

Top similarity neighbours: `meeting-notes-action-extractor` (0.576), `meeting-summary-writer` (0.525), `meeting-ops-summary-writer` (0.521), `meeting-agenda-builder` (0.484), `public-office-meeting-notes` (0.484)

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `weekly-planner` | 0.5491 | 0.5707 | 0.6026 | yes | note, schedul, week | plan, extract, note, need, schedul, weekly |
| `meeting-followup-extractor` | 0.5491 | 0.4481 | 0.6783 | yes | list, complet, meet | extract, need, summary |

Top similarity neighbours: `weekly-planner` (0.571), `meeting-notes-action-extractor` (0.557), `task-extractor` (0.549), `meeting-summary-writer` (0.481), `meeting-followup-extractor` (0.448)

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `task-extractor` | 0.6423 | 0.4257 | 0.6026 | yes | plan, need, summary, extract | weekly, plan, need, schedul, extract, note |
| `meeting-agenda-builder` | 0.6423 | 0.4537 | 0.6665 | yes | meet, plan, need, summary, agenda | plan, need, structur, note |

Top similarity neighbours: `weekly-planner` (0.642), `meeting-ops-scenario-planner` (0.499), `ux-ops-scenario-planner` (0.483), `thesis-ops-scenario-planner` (0.483), `repo-ops-scenario-planner` (0.466)

### `psc_browser_quality_p01_1_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 20

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-playwright-regression-suite` | 0.1674 | 0.1082 | 0.7628 | yes | browser, evidence | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-visual-screenshot-reviewer` | 0.1674 | 0.1052 | 0.7625 | yes | browser, evidence, state | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-accessibility-interaction-auditor` | 0.1674 | 0.1135 | 0.7410 | yes | browser, evidence, state | web, interaction, screenshot, runtime, browser, quality, workflow, involv |

Top similarity neighbours: `frontend-debugger` (0.290), `web-ui-tester` (0.265), `ads-ops-failure-diagnoser` (0.229), `implicit-browser-flow-investigator` (0.218), `ads-ops-acceptance-test-builder` (0.214)

### `psc_browser_quality_p01_2_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-playwright-regression-suite` | 0.4944 | 0.4989 | 0.7628 | yes | evidence, interaction, failure, screenshot, playwright, assertion | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-visual-screenshot-reviewer` | 0.4944 | 0.3275 | 0.7625 | yes | evidence, interaction, state, screenshot | web, interaction, screenshot, runtime, browser, quality, workflow, involv |
| `psc-accessibility-interaction-auditor` | 0.4944 | 0.3670 | 0.7410 | yes | evidence, interaction, state, screenshot | web, interaction, screenshot, runtime, browser, quality, workflow, involv |

Top similarity neighbours: `playwright-flow-debugger` (0.625), `frontend-debugger` (0.508), `psc-playwright-regression-suite` (0.499), `psc-devtools-runtime-diagnoser` (0.494), `public-addy-agent-browser-testing-with-devtools` (0.480)

### `psc_browser_quality_p02_1_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 114

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.2564 | 0.2638 | 0.7628 | yes | browser, regression, check, evidence | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-visual-screenshot-reviewer` | 0.2564 | 0.2883 | 0.7518 | yes | browser, regression, check, evidence | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-accessibility-interaction-auditor` | 0.2564 | 0.2813 | 0.6817 | yes | browser, regression, check, evidence | interaction, screenshot, browser, quality, workflow, involv, web, page |

Top similarity neighbours: `ecommerce-ops-acceptance-test-builder` (0.364), `fundraising-ops-acceptance-test-builder` (0.363), `ads-ops-acceptance-test-builder` (0.357), `invoice-payment-checker` (0.353), `customer-success-ops-acceptance-test-builder` (0.352)

### `psc_browser_quality_p02_2_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.5230 | 0.3799 | 0.7628 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-visual-screenshot-reviewer` | 0.5230 | 0.3444 | 0.7518 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |
| `psc-accessibility-interaction-auditor` | 0.5230 | 0.2764 | 0.6817 | yes | screenshot, regression | interaction, screenshot, browser, quality, workflow, involv, web, page |

Top similarity neighbours: `psc-playwright-regression-suite` (0.523), `sales-ops-acceptance-test-builder` (0.472), `contract-ops-acceptance-test-builder` (0.471), `ads-ops-acceptance-test-builder` (0.470), `procurement-ops-acceptance-test-builder` (0.470)

### `psc_browser_quality_p03_1_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.5190 | 0.2735 | 0.7625 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-playwright-regression-suite` | 0.5190 | 0.3277 | 0.7518 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-accessibility-interaction-auditor` | 0.5190 | 0.3759 | 0.8210 | yes | screenshot, regression | page, screenshot, regression, browser, quality, workflow, involv, web |

Top similarity neighbours: `psc-visual-screenshot-reviewer` (0.519), `visual-regression-checker` (0.519), `implicit-visual-diff-reviewer` (0.489), `pdf-layout-reviewer` (0.444), `mobile-ops-rewrite-editor` (0.442)

### `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.6051 | 0.4138 | 0.7625 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-playwright-regression-suite` | 0.6051 | 0.4394 | 0.7518 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |
| `psc-accessibility-interaction-auditor` | 0.6051 | 0.4639 | 0.8210 | yes | regression, screenshot, browser, interaction | page, screenshot, regression, browser, quality, workflow, involv, web |

Top similarity neighbours: `visual-regression-checker` (0.712), `implicit-visual-diff-reviewer` (0.688), `psc-visual-screenshot-reviewer` (0.605), `psc-accessibility-interaction-auditor` (0.464), `psc-playwright-regression-suite` (0.439)

### `psc_browser_quality_p04_1_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.4894 | 0.2972 | 0.7410 | yes | error | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-playwright-regression-suite` | 0.4894 | 0.2501 | 0.6817 | yes | navigation, form | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-visual-screenshot-reviewer` | 0.4894 | 0.3659 | 0.8210 | yes | - | web, interaction, browser, quality, workflow, involv, page, screenshot |

Top similarity neighbours: `accessibility-interaction-auditor` (0.509), `psc-accessibility-interaction-auditor` (0.489), `writing-ops-quality-auditor` (0.454), `public-addy-web-accessibility` (0.439), `email-ops-quality-auditor` (0.421)

### `psc_browser_quality_p04_2_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-devtools-runtime-diagnoser` | 0.6815 | 0.3769 | 0.7410 | yes | web, accessibility, interaction, quality, state, error | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-playwright-regression-suite` | 0.6815 | 0.3849 | 0.6817 | yes | web, form, accessibility, interaction, quality | web, interaction, browser, quality, workflow, involv, page, screenshot |
| `psc-visual-screenshot-reviewer` | 0.6815 | 0.4670 | 0.8210 | yes | web, accessibility, interaction, quality, state | web, interaction, browser, quality, workflow, involv, page, screenshot |

Top similarity neighbours: `accessibility-interaction-auditor` (0.759), `accessibility-checker` (0.691), `psc-accessibility-interaction-auditor` (0.681), `public-addy-web-accessibility` (0.549), `psc-visual-screenshot-reviewer` (0.467)

### `psc_data_analysis_intent_p01_1_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-anomaly-watchlist-builder` | 0.3965 | 0.3782 | 0.7577 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-decision-ranking-analyst` | 0.3965 | 0.2397 | 0.7717 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-executive-metric-narrator` | 0.3965 | 0.1982 | 0.7399 | yes | decision, csv, data | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |

Top similarity neighbours: `psc-data-trust-auditor` (0.397), `data-analysis-with-validation` (0.387), `psc-anomaly-watchlist-builder` (0.378), `dataset-ops-failure-diagnoser` (0.329), `real-estate-ops-failure-diagnoser` (0.324)

### `psc_data_analysis_intent_p01_2_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-anomaly-watchlist-builder` | 0.7167 | 0.5013 | 0.7577 | yes | data, quality, rank | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-decision-ranking-analyst` | 0.7167 | 0.5559 | 0.7717 | yes | data, quality, rank, recommendation | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |
| `psc-executive-metric-narrator` | 0.7167 | 0.4916 | 0.7399 | yes | data, quality, rank, executive | data, spreadsheet, analysi, workflow, involv, csv, metric, quality |

Top similarity neighbours: `psc-data-trust-auditor` (0.717), `data-analysis-with-validation` (0.653), `psc-decision-ranking-analyst` (0.556), `spreadsheet-formula-auditor` (0.555), `dashboard-ops-quality-auditor` (0.529)

### `psc_data_analysis_intent_p02_1_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.4951 | 0.2599 | 0.7577 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | 0.4951 | 0.2317 | 0.6996 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-executive-metric-narrator` | 0.4951 | 0.2418 | 0.6756 | yes | metric | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `latency-anomaly-detector` (0.542), `psc-anomaly-watchlist-builder` (0.495), `search-ops-monitoring-plan-builder` (0.431), `library-ops-monitoring-plan-builder` (0.425), `publishing-ops-monitoring-plan-builder` (0.414)

### `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.6858 | 0.4093 | 0.7577 | yes | csv, report | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | 0.6858 | 0.3282 | 0.6996 | yes | csv, evidence, report | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-executive-metric-narrator` | 0.6858 | 0.3855 | 0.6756 | yes | csv, turn, report, brief | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-anomaly-watchlist-builder` (0.686), `data-analysis-with-anomaly-focus` (0.587), `incident-summary-writer` (0.499), `events-ops-quality-auditor` (0.492), `latency-anomaly-detector` (0.467)

### `psc_data_analysis_intent_p03_1_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 133

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.3366 | 0.1682 | 0.7717 | yes | rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-anomaly-watchlist-builder` | 0.3366 | 0.1100 | 0.6996 | yes | rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-executive-metric-narrator` | 0.3366 | 0.2207 | 0.7614 | yes | rank, risk | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |

Top similarity neighbours: `risk-ops-comparison-builder` (0.476), `travel-ops-comparison-builder` (0.474), `travel-ops-priority-ranker` (0.474), `risk-ops-priority-ranker` (0.462), `robotics-ops-priority-ranker` (0.430)

### `psc_data_analysis_intent_p03_2_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.5147 | 0.2807 | 0.7717 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-anomaly-watchlist-builder` | 0.5147 | 0.2473 | 0.6996 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |
| `psc-executive-metric-narrator` | 0.5147 | 0.3643 | 0.7614 | yes | decision, rank | data, rank, spreadsheet, analysi, workflow, involv, csv, metric |

Top similarity neighbours: `data-analysis-for-ranking-selection` (0.609), `psc-decision-ranking-analyst` (0.515), `dataset-ops-priority-ranker` (0.451), `decision-matrix-builder` (0.437), `priority-sorter` (0.429)

### `psc_data_analysis_intent_p04_1_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.5239 | 0.2640 | 0.7399 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-anomaly-watchlist-builder` | 0.5239 | 0.3190 | 0.6756 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | 0.5239 | 0.3829 | 0.7614 | yes | - | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-executive-metric-narrator` (0.524), `meeting-ops-priority-ranker` (0.453), `meeting-ops-summary-writer` (0.447), `risk-ops-summary-writer` (0.438), `data-analysis-for-reporting` (0.436)

### `psc_data_analysis_intent_p04_2_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-data-trust-auditor` | 0.6677 | 0.4719 | 0.7399 | yes | metric, spreadsheet, busines, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-anomaly-watchlist-builder` | 0.6677 | 0.4475 | 0.6756 | yes | metric, spreadsheet, busines, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |
| `psc-decision-ranking-analyst` | 0.6677 | 0.4188 | 0.7614 | yes | metric, spreadsheet, busines, action, data | data, metric, spreadsheet, analysi, workflow, involv, csv, quality |

Top similarity neighbours: `psc-executive-metric-narrator` (0.668), `operations-ops-summary-writer` (0.608), `personal-ops-summary-writer` (0.578), `dashboard-ops-summary-writer` (0.569), `finance-ops-summary-writer` (0.561)

### `psc_github_maintenance_p01_1_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pr-thread-fix-planner` | 0.4716 | 0.2467 | 0.7282 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-repo-guardrail-hook-installer` | 0.4716 | 0.1062 | 0.6133 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-release-communication-packager` | 0.4716 | 0.1806 | 0.6780 | yes | - | github, repository, maintenance, workflow, involv, extract, request, review |

Top similarity neighbours: `ci-failure-debugger` (0.517), `implicit-ci-failure-reader` (0.488), `psc-ci-log-first-failure-reader` (0.472), `ci-log-root-cause-debugger` (0.455), `construction-ops-failure-diagnoser` (0.429)

### `psc_github_maintenance_p01_2_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pr-thread-fix-planner` | 0.7010 | 0.4783 | 0.7282 | yes | github, review, release, note | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-repo-guardrail-hook-installer` | 0.7010 | 0.3927 | 0.6133 | yes | github, review, release | github, repository, maintenance, workflow, involv, extract, request, review |
| `psc-release-communication-packager` | 0.7010 | 0.4639 | 0.6780 | yes | github, turn, review, release, note | github, repository, maintenance, workflow, involv, extract, request, review |

Top similarity neighbours: `psc-ci-log-first-failure-reader` (0.701), `ci-failure-debugger` (0.635), `public-swebench-analyze-ci` (0.619), `pr-reviewer` (0.599), `github-issue-triager` (0.534)

### `psc_github_maintenance_p02_1_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.5172 | 0.3017 | 0.7282 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |
| `psc-repo-guardrail-hook-installer` | 0.5172 | 0.3374 | 0.7902 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |
| `psc-release-communication-packager` | 0.5172 | 0.3613 | 0.8423 | yes | review, thread | extract, request, review, thread, code, verification, github, repository |

Top similarity neighbours: `implicit-review-comment-planner` (0.552), `pr-review-comment-resolver` (0.525), `psc-pr-thread-fix-planner` (0.517), `public-mattpocock-review` (0.477), `pr-reviewer` (0.432)

### `psc_github_maintenance_p02_2_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 5

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.6220 | 0.5321 | 0.7282 | yes | review, github, thread, code | extract, request, review, thread, code, verification, github, repository |
| `psc-repo-guardrail-hook-installer` | 0.6220 | 0.4584 | 0.7902 | yes | review, github, thread, code | extract, request, review, thread, code, verification, github, repository |
| `psc-release-communication-packager` | 0.6220 | 0.5301 | 0.8423 | yes | review, github, thread, code, change | extract, request, review, thread, code, verification, github, repository |

Top similarity neighbours: `pr-review-comment-resolver` (0.711), `pr-reviewer` (0.704), `review-comment-resolver` (0.673), `repo-code-reviewer` (0.636), `psc-pr-thread-fix-planner` (0.622)

### `psc_github_maintenance_p03_1_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.5622 | 0.3737 | 0.6133 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-pr-thread-fix-planner` | 0.5622 | 0.4295 | 0.7902 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-release-communication-packager` | 0.5622 | 0.4965 | 0.7938 | yes | repository | repository, hook, verification, github, maintenance, workflow, involv, extract |

Top similarity neighbours: `git-safety-guardrail-installer` (0.621), `psc-repo-guardrail-hook-installer` (0.562), `public-mattpocock-git-guardrails-claude-code` (0.504), `psc-release-communication-packager` (0.496), `public-openai-security-ownership-map` (0.496)

### `psc_github_maintenance_p03_2_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.6767 | 0.3873 | 0.6133 | yes | hook, verification | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-pr-thread-fix-planner` | 0.6767 | 0.5025 | 0.7902 | yes | hook, verification, step | repository, hook, verification, github, maintenance, workflow, involv, extract |
| `psc-release-communication-packager` | 0.6767 | 0.4810 | 0.7938 | yes | hook, verification | repository, hook, verification, github, maintenance, workflow, involv, extract |

Top similarity neighbours: `git-safety-guardrail-installer` (0.730), `psc-repo-guardrail-hook-installer` (0.677), `public-mattpocock-git-guardrails-claude-code` (0.665), `version-control-helper` (0.504), `psc-pr-thread-fix-planner` (0.502)

### `psc_github_maintenance_p04_1_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.5738 | 0.2799 | 0.6780 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |
| `psc-pr-thread-fix-planner` | 0.5738 | 0.4353 | 0.8423 | yes | note, release, change | release, note, github, repository, maintenance, workflow, involv, extract |
| `psc-repo-guardrail-hook-installer` | 0.5738 | 0.3194 | 0.7938 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |

Top similarity neighbours: `psc-release-communication-packager` (0.574), `release-note-writer` (0.550), `public-office-changelog-generator` (0.542), `release-changelog-generator` (0.536), `public-oh-my-changelog-maintenance` (0.485)

### `psc_github_maintenance_p04_2_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-ci-log-first-failure-reader` | 0.6244 | 0.3632 | 0.6780 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |
| `psc-pr-thread-fix-planner` | 0.6244 | 0.4766 | 0.8423 | yes | release, change, note | release, note, github, repository, maintenance, workflow, involv, extract |
| `psc-repo-guardrail-hook-installer` | 0.6244 | 0.3773 | 0.7938 | yes | release | release, github, repository, maintenance, workflow, involv, extract, request |

Top similarity neighbours: `release-changelog-generator` (0.724), `public-oh-my-changelog-maintenance` (0.663), `psc-release-communication-packager` (0.624), `release-note-writer` (0.618), `public-swebench-changelog-automation` (0.614)

### `psc_huggingface_workflow_p01_1_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-local-model-fit-selector` | 0.6053 | 0.4097 | 0.8221 | yes | hugg, face, dataset, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-sentence-embedding-trainer` | 0.6053 | 0.4318 | 0.7333 | yes | hugg, face, dataset, split, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-hf-space-deployment-preparer` | 0.6053 | 0.4034 | 0.8565 | yes | hugg, face, dataset, model | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |

Top similarity neighbours: `psc-hf-dataset-card-inspector` (0.605), `public-huggingface-datasets` (0.604), `hf-dataset-viewer-inspector` (0.590), `public-huggingface-huggingface-vision-trainer` (0.493), `hf-community-eval-runner` (0.480)

### `psc_huggingface_workflow_p01_2_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-local-model-fit-selector` | 0.4505 | 0.2521 | 0.8221 | yes | train, dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-sentence-embedding-trainer` | 0.4505 | 0.2728 | 0.7333 | yes | train, dataset, split | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |
| `psc-hf-space-deployment-preparer` | 0.4505 | 0.2876 | 0.8565 | yes | train, dataset | hugg, face, dataset, machine-learn, workflow, involv, model, embedd |

Top similarity neighbours: `dataset-ops-risk-reviewer` (0.466), `dataset-ops-acceptance-test-builder` (0.459), `psc-hf-dataset-card-inspector` (0.451), `dataset-ops-compliance-checker` (0.448), `training-ops-quality-auditor` (0.443)

### `psc_huggingface_workflow_p02_1_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.3572 | 0.3018 | 0.8221 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-sentence-embedding-trainer` | 0.3572 | 0.2453 | 0.7528 | yes | model, choice | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-hf-space-deployment-preparer` | 0.3572 | 0.3165 | 0.8111 | yes | model | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |

Top similarity neighbours: `support-ticket-triager` (0.410), `psc-local-model-fit-selector` (0.357), `support-ops-intake-classifier` (0.351), `public-huggingface-huggingface-trackio` (0.344), `public-huggingface-huggingface-local-models` (0.344)

### `psc_huggingface_workflow_p02_2_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.5557 | 0.5221 | 0.8221 | yes | hugg, face, model, dataset, card | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-sentence-embedding-trainer` | 0.5557 | 0.4106 | 0.7528 | yes | hugg, face, model, dataset | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |
| `psc-hf-space-deployment-preparer` | 0.5557 | 0.4565 | 0.8111 | yes | hugg, face, model, dataset | model, hugg, face, machine-learn, workflow, involv, dataset, embedd |

Top similarity neighbours: `public-huggingface-huggingface-local-models` (0.584), `hf-local-model-selector` (0.562), `psc-local-model-fit-selector` (0.556), `public-huggingface-huggingface-vision-trainer` (0.535), `psc-hf-dataset-card-inspector` (0.522)

### `psc_huggingface_workflow_p03_1_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 34

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.3392 | 0.2252 | 0.7333 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-local-model-fit-selector` | 0.3392 | 0.2112 | 0.7528 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-hf-space-deployment-preparer` | 0.3392 | 0.1896 | 0.6647 | yes | embedd, evaluation | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |

Top similarity neighbours: `skill-benchmark-evaluator` (0.713), `psc-retrieval-result-adjudicator` (0.637), `skill-router-policy-designer` (0.618), `skill-finder` (0.583), `psc-skill-routing-budget-planner` (0.557)

### `psc_huggingface_workflow_p03_2_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.5020 | 0.2137 | 0.7333 | yes | split, model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-local-model-fit-selector` | 0.5020 | 0.2608 | 0.7528 | yes | choose, local, model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |
| `psc-hf-space-deployment-preparer` | 0.5020 | 0.2101 | 0.6647 | yes | model | embedd, hugg, face, machine-learn, workflow, involv, dataset, model |

Top similarity neighbours: `sentence-transformer-finetuner` (0.651), `public-huggingface-train-sentence-transformers` (0.572), `psc-sentence-embedding-trainer` (0.502), `speaker-notes-writer` (0.431), `public-office-transcription-automation` (0.409)

### `psc_huggingface_workflow_p04_1_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.6606 | 0.5684 | 0.8565 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-local-model-fit-selector` | 0.6606 | 0.5710 | 0.8111 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-sentence-embedding-trainer` | 0.6606 | 0.4744 | 0.6647 | yes | demo, hugg, face, space | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |

Top similarity neighbours: `psc-hf-space-deployment-preparer` (0.661), `public-huggingface-huggingface-vision-trainer` (0.595), `psc-local-model-fit-selector` (0.571), `psc-hf-dataset-card-inspector` (0.568), `public-huggingface-huggingface-community-evals` (0.547)

### `psc_huggingface_workflow_p04_2_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-hf-dataset-card-inspector` | 0.5726 | 0.3742 | 0.8565 | yes | model, demo, deployment, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-local-model-fit-selector` | 0.5726 | 0.3863 | 0.8111 | yes | model, demo, deployment, runtime, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |
| `psc-sentence-embedding-trainer` | 0.5726 | 0.2687 | 0.6647 | yes | model, demo, deployment, train | hugg, face, space, deployment, machine-learn, workflow, involv, dataset |

Top similarity neighbours: `psc-hf-space-deployment-preparer` (0.573), `hf-zerogpu-space-deployer` (0.551), `training-ops-artifact-packager` (0.524), `ml-ops-artifact-packager` (0.503), `platform-ops-dependency-mapper` (0.494)

### `psc_pdf_document_work_p01_1_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-scan-ocr-recovery` | 0.5694 | 0.4868 | 0.8519 | yes | text, packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-evidence-qa` | 0.5694 | 0.4741 | 0.8106 | yes | packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-redaction-pass` | 0.5694 | 0.4463 | 0.8384 | yes | packet, pdf, extract, document, page, anchor | pdf, document, extract, anchor, workflow, involv, ocr, recovery |

Top similarity neighbours: `pdf-layout-table-extractor` (0.661), `implicit-pdf-table-reconstructor` (0.590), `psc-pdf-native-extraction-pack` (0.569), `public-office-pdf-extraction` (0.534), `pdf-ocr-extractor` (0.517)

### `psc_pdf_document_work_p01_2_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-scan-ocr-recovery` | 0.6615 | 0.5483 | 0.8519 | yes | extract, workflow, packet, text, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-evidence-qa` | 0.6615 | 0.4808 | 0.8106 | yes | extract, workflow, packet, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |
| `psc-pdf-redaction-pass` | 0.6615 | 0.4808 | 0.8384 | yes | extract, workflow, packet, page, anchor, ocr, answer | pdf, document, extract, anchor, workflow, involv, ocr, recovery |

Top similarity neighbours: `public-office-pdf-extraction` (0.675), `psc-pdf-native-extraction-pack` (0.661), `pdf-ocr-extractor` (0.661), `pdf-layout-table-extractor` (0.653), `pdf-ocr-cleaner` (0.560)

### `psc_pdf_document_work_p02_1_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.6033 | 0.4752 | 0.8519 | yes | page, pdf, packet, text | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-evidence-qa` | 0.6033 | 0.4501 | 0.8227 | yes | page, pdf, packet | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-redaction-pass` | 0.6033 | 0.4296 | 0.8428 | yes | page, pdf, packet | pdf, document, page, workflow, involv, extract, ocr, recovery |

Top similarity neighbours: `pdf-ocr-cleaner` (0.663), `pdf-ocr-extractor` (0.641), `psc-pdf-scan-ocr-recovery` (0.603), `public-office-pdf-ocr` (0.532), `psc-pdf-native-extraction-pack` (0.475)

### `psc_pdf_document_work_p02_2_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.6806 | 0.5510 | 0.8519 | yes | ocr, recovery, workflow, pdf, page, born-digital, table, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-evidence-qa` | 0.6806 | 0.4592 | 0.8227 | yes | ocr, recovery, workflow, pdf, page, note, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |
| `psc-pdf-redaction-pass` | 0.6806 | 0.4536 | 0.8428 | yes | ocr, recovery, workflow, pdf, page, extract | pdf, document, page, workflow, involv, extract, ocr, recovery |

Top similarity neighbours: `pdf-ocr-extractor` (0.715), `pdf-ocr-cleaner` (0.709), `psc-pdf-scan-ocr-recovery` (0.681), `pdf-layout-table-extractor` (0.623), `public-office-pdf-ocr` (0.620)

### `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 105

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.1815 | 0.1030 | 0.8106 | yes | pdf, page, evidence, answer | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | 0.1815 | 0.0987 | 0.8227 | yes | pdf, page, evidence, answer | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-redaction-pass` | 0.1815 | 0.1790 | 0.8734 | yes | pdf, page, evidence, answer | pdf, document, evidence, answer, workflow, involv, extract, ocr |

Top similarity neighbours: `travel-ops-dependency-mapper` (0.291), `travel-ops-scenario-planner` (0.285), `travel-ops-summary-writer` (0.283), `travel-ops-intake-classifier` (0.280), `travel-ops-risk-reviewer` (0.277)

### `psc_pdf_document_work_p03_2_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.5052 | 0.4116 | 0.8106 | yes | answer, pdf, page, evidence, document, extract, table | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | 0.5052 | 0.3550 | 0.8227 | yes | answer, pdf, page, evidence, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |
| `psc-pdf-redaction-pass` | 0.5052 | 0.3540 | 0.8734 | yes | answer, pdf, page, evidence, document, extract | pdf, document, evidence, answer, workflow, involv, extract, ocr |

Top similarity neighbours: `pdf-question-answerer` (0.584), `implicit-pdf-evidence-answerer` (0.512), `psc-pdf-evidence-qa` (0.505), `pdf-layout-table-extractor` (0.484), `pdf-ocr-extractor` (0.424)

### `psc_pdf_document_work_p04_1_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.4958 | 0.4263 | 0.8384 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | 0.4958 | 0.4217 | 0.8428 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-evidence-qa` | 0.4958 | 0.4368 | 0.8734 | yes | pdf | document, external, shar, pdf, workflow, involv, extract, ocr |

Top similarity neighbours: `pdf-redaction-reviewer` (0.511), `psc-pdf-redaction-pass` (0.496), `pdf-layout-reviewer` (0.473), `pdf-layout-table-extractor` (0.466), `psc-pdf-evidence-qa` (0.437)

### `psc_pdf_document_work_p04_2_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-pdf-native-extraction-pack` | 0.5959 | 0.4849 | 0.8384 | yes | pdf, redaction, external, shar, page, anchor, extract, table | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-scan-ocr-recovery` | 0.5959 | 0.4544 | 0.8428 | yes | pdf, redaction, external, shar, page, anchor, extract | document, external, shar, pdf, workflow, involv, extract, ocr |
| `psc-pdf-evidence-qa` | 0.5959 | 0.4879 | 0.8734 | yes | pdf, redaction, external, shar, page, anchor, extract | document, external, shar, pdf, workflow, involv, extract, ocr |

Top similarity neighbours: `psc-pdf-redaction-pass` (0.596), `pdf-redaction-reviewer` (0.570), `public-office-pdf-watermark` (0.494), `psc-pdf-evidence-qa` (0.488), `pdf-layout-table-extractor` (0.487)

### `psc_research_reading_p01_1_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | 0.5081 | 0.3655 | 0.7904 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-related-work-synthesizer` | 0.5081 | 0.2823 | 0.8210 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-source-field-table-extractor` | 0.5081 | 0.3371 | 0.8221 | yes | paper, method | method, research-read, workflow, involv, paper, claim, evidence, compare |

Top similarity neighbours: `research-ops-dependency-mapper` (0.516), `psc-paper-method-mapper` (0.508), `customer-success-ops-dependency-mapper` (0.489), `thesis-ops-dependency-mapper` (0.488), `metrics-overview` (0.486)

### `psc_research_reading_p01_2_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 4

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-citation-claim-support-auditor` | 0.4714 | 0.3456 | 0.7904 | yes | method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-related-work-synthesizer` | 0.4714 | 0.2438 | 0.8210 | yes | method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |
| `psc-source-field-table-extractor` | 0.4714 | 0.3642 | 0.8221 | yes | extract, method, paper | method, research-read, workflow, involv, paper, claim, evidence, compare |

Top similarity neighbours: `method-note-builder` (0.534), `paper-summariser` (0.520), `document-extractor` (0.501), `psc-paper-method-mapper` (0.471), `multi-source-comparison-builder` (0.435)

### `psc_research_reading_p02_1_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 32

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.3999 | 0.2727 | 0.7904 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-related-work-synthesizer` | 0.3999 | 0.2550 | 0.7491 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-source-field-table-extractor` | 0.3999 | 0.3180 | 0.8030 | yes | - | claim, evidence, research-read, workflow, involv, paper, method, compare |

Top similarity neighbours: `skill-authoring-guide` (0.566), `skill-finder` (0.533), `agent-ops-evidence-grounder` (0.520), `agent-ops-risk-reviewer` (0.505), `agent-ops-summary-writer` (0.500)

### `psc_research_reading_p02_2_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.6402 | 0.3725 | 0.7904 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-related-work-synthesizer` | 0.6402 | 0.2890 | 0.7491 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |
| `psc-source-field-table-extractor` | 0.6402 | 0.3441 | 0.8030 | yes | claim, evidence | claim, evidence, research-read, workflow, involv, paper, method, compare |

Top similarity neighbours: `citation-grounding-helper` (0.651), `psc-citation-claim-support-auditor` (0.640), `research-ops-evidence-grounder` (0.633), `qa-ops-evidence-grounder` (0.603), `legal-ops-evidence-grounder` (0.596)

### `psc_research_reading_p03_1_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.4337 | 0.4010 | 0.8210 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-citation-claim-support-auditor` | 0.4337 | 0.3361 | 0.7491 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-source-field-table-extractor` | 0.4337 | 0.3003 | 0.8039 | yes | paper, compare, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |

Top similarity neighbours: `related-work-synthesiser` (0.527), `paper-summariser` (0.523), `multi-source-comparison-builder` (0.471), `thesis-ops-summary-writer` (0.466), `method-note-builder` (0.466)

### `psc_research_reading_p03_2_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.6021 | 0.3773 | 0.8210 | yes | limitation, thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-citation-claim-support-auditor` | 0.6021 | 0.3987 | 0.7491 | yes | thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |
| `psc-source-field-table-extractor` | 0.6021 | 0.4299 | 0.8039 | yes | thesi | paper, thesi, research-read, workflow, involv, claim, method, evidence |

Top similarity neighbours: `related-work-synthesiser` (0.747), `psc-related-work-synthesizer` (0.602), `thesis-ops-rewrite-editor` (0.547), `thesis-ops-summary-writer` (0.542), `thesis-ops-resource-linker` (0.499)

### `psc_research_reading_p04_1_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.5171 | 0.4869 | 0.8221 | yes | extract, paper', baseline, limitation, compare, evidence | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-citation-claim-support-auditor` | 0.5171 | 0.4478 | 0.8030 | yes | compare, evidence | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-related-work-synthesizer` | 0.5171 | 0.3611 | 0.8039 | yes | compare, evidence | compare, research-read, workflow, involv, paper, claim, method, evidence |

Top similarity neighbours: `multi-source-comparison-builder` (0.582), `research-ops-comparison-builder` (0.536), `psc-source-field-table-extractor` (0.517), `document-extractor` (0.516), `research-ops-summary-writer` (0.508)

### `psc_research_reading_p04_2_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-paper-method-mapper` | 0.6554 | 0.3696 | 0.8221 | yes | evidence, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-citation-claim-support-auditor` | 0.6554 | 0.4830 | 0.8030 | yes | evidence, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |
| `psc-related-work-synthesizer` | 0.6554 | 0.3723 | 0.8039 | yes | evidence, related-work, synthesi | compare, research-read, workflow, involv, paper, claim, method, evidence |

Top similarity neighbours: `psc-source-field-table-extractor` (0.655), `research-ops-field-extractor` (0.563), `document-extractor` (0.538), `document-field-extractor` (0.537), `legal-discovery-ops-field-extractor` (0.532)

### `psc_security_appsec_p01_1_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 10

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-handler-vulnerability-reviewer` | 0.3528 | 0.3564 | 0.7716 | yes | - | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-dependency-supply-chain-auditor` | 0.3528 | 0.3321 | 0.7333 | yes | - | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-privacy-telemetry-reviewer` | 0.3528 | 0.3662 | 0.6551 | yes | - | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |

Top similarity neighbours: `privacy-risk-reviewer` (0.403), `public-openai-security-ownership-map` (0.398), `auth-flow-reviewer` (0.385), `public-swebench-linkerd-patterns` (0.372), `public-addy-agent-security-and-hardening` (0.369)

### `psc_security_appsec_p01_2_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-handler-vulnerability-reviewer` | 0.5322 | 0.4685 | 0.7716 | yes | feature, path, mitigation, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-dependency-supply-chain-auditor` | 0.5322 | 0.3882 | 0.7333 | yes | feature, mitigation | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |
| `psc-privacy-telemetry-reviewer` | 0.5322 | 0.2990 | 0.6551 | yes | feature, mitigation, review | feature, mitigation, application-security, workflow, involv, risk, code, dependencie |

Top similarity neighbours: `psc-feature-threat-modeler` (0.532), `public-security-threat-model` (0.494), `security-threat-modeler` (0.484), `api-security-threat-reviewer` (0.482), `psc-handler-vulnerability-reviewer` (0.469)

### `psc_security_appsec_p02_1_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 5

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.3914 | 0.1666 | 0.7716 | yes | - | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-dependency-supply-chain-auditor` | 0.3914 | 0.1206 | 0.7442 | yes | - | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-privacy-telemetry-reviewer` | 0.3914 | 0.1893 | 0.6960 | yes | review | code, application-security, workflow, involv, risk, feature, dependencie, privacy |

Top similarity neighbours: `auth-flow-reviewer` (0.445), `security-ops-rewrite-editor` (0.424), `public-n-skills-dev-browser` (0.399), `api-security-threat-reviewer` (0.393), `psc-handler-vulnerability-reviewer` (0.391)

### `psc_security_appsec_p02_2_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.6036 | 0.4708 | 0.7716 | yes | code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-dependency-supply-chain-auditor` | 0.6036 | 0.3502 | 0.7442 | yes | code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |
| `psc-privacy-telemetry-reviewer` | 0.6036 | 0.3219 | 0.6960 | yes | review, code | code, application-security, workflow, involv, risk, feature, dependencie, privacy |

Top similarity neighbours: `api-security-threat-reviewer` (0.633), `psc-handler-vulnerability-reviewer` (0.604), `api-ops-risk-reviewer` (0.566), `security-code-reviewer` (0.520), `security-threat-modeler` (0.517)

### `psc_security_appsec_p03_1_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.5690 | 0.2508 | 0.7333 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-handler-vulnerability-reviewer` | 0.5690 | 0.2736 | 0.7442 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-privacy-telemetry-reviewer` | 0.5690 | 0.1328 | 0.6273 | yes | dependencie, risk, mitigation | risk, dependencie, application-security, workflow, involv, code, feature, privacy |

Top similarity neighbours: `psc-dependency-supply-chain-auditor` (0.569), `supply-chain-ops-dependency-mapper` (0.512), `supply-chain-ops-artifact-packager` (0.508), `risk-ops-artifact-packager` (0.506), `risk-ops-dependency-mapper` (0.473)

### `psc_security_appsec_p03_2_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.6443 | 0.2596 | 0.7333 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-handler-vulnerability-reviewer` | 0.6443 | 0.3121 | 0.7442 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |
| `psc-privacy-telemetry-reviewer` | 0.6443 | 0.2453 | 0.6273 | yes | risk | risk, dependencie, application-security, workflow, involv, code, feature, privacy |

Top similarity neighbours: `dependency-risk-auditor` (0.672), `psc-dependency-supply-chain-auditor` (0.644), `risk-ops-artifact-packager` (0.490), `public-addy-agent-source-driven-development` (0.479), `public-addy-web-best-practices` (0.458)

### `psc_security_appsec_p04_1_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 270

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.2354 | 0.0898 | 0.6551 | yes | - | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-handler-vulnerability-reviewer` | 0.2354 | 0.0799 | 0.6960 | yes | review | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-dependency-supply-chain-auditor` | 0.2354 | 0.1373 | 0.6273 | yes | - | privacy, data, application-security, workflow, involv, risk, code, feature |

Top similarity neighbours: `email-ops-quality-auditor` (0.426), `analytics-ops-quality-auditor` (0.416), `search-ops-monitoring-plan-builder` (0.406), `email-ops-monitoring-plan-builder` (0.398), `seo-ops-monitoring-plan-builder` (0.394)

### `psc_security_appsec_p04_2_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-feature-threat-modeler` | 0.6428 | 0.2937 | 0.6551 | yes | privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-handler-vulnerability-reviewer` | 0.6428 | 0.3151 | 0.6960 | yes | privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |
| `psc-dependency-supply-chain-auditor` | 0.6428 | 0.2569 | 0.6273 | yes | asses, privacy, risk, data, code | privacy, data, application-security, workflow, involv, risk, code, feature |

Top similarity neighbours: `psc-privacy-telemetry-reviewer` (0.643), `privacy-ops-scenario-planner` (0.521), `privacy-risk-reviewer` (0.508), `privacy-ops-risk-reviewer` (0.506), `privacy-policy-drafter` (0.493)

### `psc_skill_representation_p01_1_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 290

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-public-skill-atomizer` | 0.3298 | 0.2269 | 0.8264 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | 0.3298 | 0.2626 | 0.7959 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | 0.3298 | 0.2488 | 0.7727 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `warehouse-ops-artifact-packager` (0.486), `retail-ops-artifact-packager` (0.464), `manufacturing-ops-artifact-packager` (0.461), `procurement-ops-artifact-packager` (0.456), `supply-chain-ops-artifact-packager` (0.446)

### `psc_skill_representation_p01_2_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 18

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-public-skill-atomizer` | 0.4920 | 0.3705 | 0.8264 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | 0.4920 | 0.3787 | 0.7959 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | 0.4920 | 0.4885 | 0.7727 | yes | artifact | workflow, skill-library, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-editor` (0.676), `skill-field-auditor` (0.672), `skill-finder` (0.622), `skill-authoring-guide` (0.604), `skill-evaluator` (0.592)

### `psc_skill_representation_p02_1_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.6243 | 0.5417 | 0.8264 | yes | file, candidate, resource | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-skill-routing-budget-planner` | 0.6243 | 0.5273 | 0.8222 | yes | candidate | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-retrieval-result-adjudicator` | 0.6243 | 0.4639 | 0.7525 | yes | candidate | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |

Top similarity neighbours: `psc-public-skill-atomizer` (0.624), `skill-installer-wrapper` (0.591), `psc-messy-skill-field-extractor` (0.542), `psc-skill-routing-budget-planner` (0.527), `skill-hierarchy-flattener` (0.525)

### `psc_skill_representation_p02_2_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.5912 | 0.4836 | 0.8264 | yes | resource, rout, boundarie | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-skill-routing-budget-planner` | 0.5912 | 0.5484 | 0.8222 | yes | rout | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |
| `psc-retrieval-result-adjudicator` | 0.5912 | 0.4144 | 0.7525 | yes | rout | rout, candidate, skill-library, workflow, involv, artifact, field, atomization |

Top similarity neighbours: `skill-hierarchy-flattener` (0.776), `psc-public-skill-atomizer` (0.591), `skill-router-policy-designer` (0.582), `psc-skill-routing-budget-planner` (0.548), `skill-installer-wrapper` (0.521)

### `psc_skill_representation_p03_1_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.7439 | 0.4636 | 0.7959 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | 0.7439 | 0.5394 | 0.8222 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | 0.7439 | 0.4674 | 0.7298 | yes | rout, candidate, field | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-router-policy-designer` (0.791), `psc-skill-routing-budget-planner` (0.744), `psc-public-skill-atomizer` (0.539), `skill-hierarchy-flattener` (0.520), `skill-finder` (0.478)

### `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 3

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.5267 | 0.4611 | 0.7959 | yes | evaluation | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | 0.5267 | 0.4462 | 0.8222 | yes | evaluation | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-retrieval-result-adjudicator` | 0.5267 | 0.6116 | 0.7298 | yes | retrieval, top-k, evaluation | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-benchmark-evaluator` (0.687), `psc-retrieval-result-adjudicator` (0.612), `psc-skill-routing-budget-planner` (0.527), `skill-finder` (0.522), `search-ops-priority-ranker` (0.515)

### `psc_skill_representation_p04_1_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.6498 | 0.3955 | 0.7727 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | 0.6498 | 0.3665 | 0.7525 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | 0.6498 | 0.4031 | 0.7298 | yes | - | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `skill-benchmark-evaluator` (0.763), `psc-retrieval-result-adjudicator` (0.650), `skill-evaluator` (0.513), `search-ops-priority-ranker` (0.508), `training-ops-priority-ranker` (0.473)

### `psc_skill_representation_p04_2_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `psc-messy-skill-field-extractor` | 0.6576 | 0.2640 | 0.7727 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-public-skill-atomizer` | 0.6576 | 0.2775 | 0.7525 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |
| `psc-skill-routing-budget-planner` | 0.6576 | 0.2897 | 0.7298 | yes | candidate | skill-library, workflow, involv, artifact, rout, field, atomization, benchmark |

Top similarity neighbours: `psc-retrieval-result-adjudicator` (0.658), `skill-benchmark-evaluator` (0.551), `search-ops-summary-writer` (0.522), `search-ops-priority-ranker` (0.520), `search-ops-comparison-builder` (0.486)

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `general-source-summariser` | 0.6689 | 0.4840 | 0.6950 | yes | recap, summary | summary, recap |
| `method-note-builder` | 0.6689 | 0.3943 | 0.5489 | yes | paper, note | paper |
| `citation-note-extractor` | 0.6689 | 0.4355 | 0.5684 | yes | citation-ready, note | concise |

Top similarity neighbours: `paper-summariser` (0.669), `general-source-summariser` (0.484), `research-ops-summary-writer` (0.439), `citation-note-extractor` (0.435), `multi-source-comparison-builder` (0.430)

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `paper-summariser` | 0.4982 | 0.4710 | 0.6950 | yes | summary, academic, paper, limit | summary, recap |
| `document-extractor` | 0.4982 | 0.3338 | 0.5553 | yes | - | - |
| `citation-note-extractor` | 0.4982 | 0.4066 | 0.6566 | yes | - | important |

Top similarity neighbours: `research-ops-evidence-grounder` (0.504), `general-source-summariser` (0.498), `paper-summariser` (0.471), `thesis-ops-evidence-grounder` (0.470), `research-ops-summary-writer` (0.447)

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `document-extractor` | 0.7176 | 0.4348 | 0.7283 | yes | - | claim |
| `paper-summariser` | 0.7176 | 0.3786 | 0.5684 | yes | - | concise |
| `citation-grounding-helper` | 0.7176 | 0.5656 | 0.7106 | yes | note | note, claim, support |

Top similarity neighbours: `citation-note-extractor` (0.718), `citation-grounding-helper` (0.566), `method-note-builder` (0.519), `psc-citation-claim-support-auditor` (0.507), `general-source-summariser` (0.502)

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | 0.5590 | 0.3442 | 0.7283 | yes | detail | claim |
| `method-note-builder` | 0.5590 | 0.2255 | 0.5104 | yes | extract | extract |
| `paper-summariser` | 0.5590 | 0.1743 | 0.5425 | yes | - | - |

Top similarity neighbours: `document-field-extractor` (0.592), `document-extractor` (0.559), `psc-source-field-table-extractor` (0.510), `finance-ops-field-extractor` (0.501), `database-ops-field-extractor` (0.482)

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 15

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `paper-summariser` | 0.3833 | 0.3953 | 0.5489 | yes | - | paper |
| `document-extractor` | 0.3833 | 0.3599 | 0.5104 | yes | - | extract |
| `citation-note-extractor` | 0.3833 | 0.3185 | 0.6449 | yes | - | note |

Top similarity neighbours: `manufacturing-ops-summary-writer` (0.415), `energy-ops-summary-writer` (0.411), `thesis-ops-summary-writer` (0.408), `hr-ops-summary-writer` (0.402), `ux-ops-summary-writer` (0.400)

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `citation-note-extractor` | 0.4869 | 0.4518 | 0.7106 | yes | support | claim, note, support |
| `paper-summariser` | 0.4869 | 0.3984 | 0.4244 | no | - | - |
| `document-extractor` | 0.4869 | 0.4048 | 0.5536 | yes | explicit | claim |

Top similarity neighbours: `citation-grounding-helper` (0.487), `agent-ops-summary-writer` (0.460), `citation-note-extractor` (0.452), `qa-ops-summary-writer` (0.440), `incident-ops-rewrite-editor` (0.440)

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `related-work-synthesiser` | 0.5742 | 0.4958 | 0.5379 | yes | related-work | multiple, paper |
| `method-note-builder` | 0.5742 | 0.3942 | 0.5466 | yes | evaluation, note | paper, assumption, evaluation, setup |
| `citation-note-extractor` | 0.5742 | 0.5160 | 0.5837 | yes | turn, note | important |

Top similarity neighbours: `multi-source-comparison-builder` (0.574), `citation-note-extractor` (0.516), `research-ops-comparison-builder` (0.496), `related-work-synthesiser` (0.496), `citation-grounding-helper` (0.483)

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `multi-source-comparison-builder` | 0.7327 | 0.4915 | 0.5379 | yes | compare | multiple, paper |
| `citation-note-extractor` | 0.7327 | 0.4328 | 0.4848 | no | note | - |
| `paper-summariser` | 0.7327 | 0.3974 | 0.5469 | yes | - | paper, question |

Top similarity neighbours: `related-work-synthesiser` (0.733), `psc-related-work-synthesizer` (0.548), `psc-source-field-table-extractor` (0.508), `multi-source-comparison-builder` (0.491), `general-source-summariser` (0.490)

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.5758 | 0.4369 | 0.6945 | yes | draft, email, reply, message | draft, reply, email, context |
| `reply-polisher` | 0.5758 | 0.4410 | 0.6370 | yes | email, reply, message, tone | reply, email |

Top similarity neighbours: `professor-email-reply` (0.576), `reply-polisher` (0.441), `reply-drafter` (0.437), `email-drafter` (0.428), `groupwork-reply` (0.412)

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `professor-email-reply` | 0.4806 | 0.2795 | 0.6370 | yes | - | reply, email |
| `reply-drafter` | 0.4806 | 0.3891 | 0.6908 | yes | message | reply, message, email |

Top similarity neighbours: `reply-polisher` (0.481), `followup-reply-writer` (0.461), `partnerships-ops-rewrite-editor` (0.438), `email-polisher` (0.432), `groupwork-reply` (0.398)

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.5182 | 0.2437 | 0.7078 | yes | reply, draft, need | reply, draft, message |
| `followup-reply-writer` | 0.5182 | 0.3361 | 0.6648 | yes | reply, draft | reply, draft, message |

Top similarity neighbours: `groupwork-reply` (0.518), `meeting-ops-summary-writer` (0.381), `meeting-summary-writer` (0.378), `partnerships-ops-handoff-brief-writer` (0.371), `partnerships-ops-failure-diagnoser` (0.355)

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-drafter` | 0.6173 | 0.3860 | 0.7056 | yes | - | draft, reply, message |
| `groupwork-reply` | 0.6173 | 0.4311 | 0.6648 | yes | - | draft, reply, message |

Top similarity neighbours: `followup-reply-writer` (0.617), `email-action-extractor` (0.464), `reply-polisher` (0.444), `groupwork-reply` (0.431), `meeting-followup-extractor` (0.410)

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `reply-polisher` | 0.5525 | 0.6040 | 0.6908 | yes | message, reply, polish | reply, message, email |
| `followup-reply-writer` | 0.5525 | 0.5293 | 0.7056 | yes | response, message, reply, action | draft, reply, message |

Top similarity neighbours: `reply-polisher` (0.604), `reply-drafter` (0.552), `email-polisher` (0.541), `followup-reply-writer` (0.529), `groupwork-reply` (0.490)

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 15

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.3366 | 0.3427 | 0.6276 | yes | security | security |
| `auth-flow-reviewer` | 0.3366 | 0.3770 | 0.5270 | yes | security, risk | security, flow |
| `privacy-risk-reviewer` | 0.3366 | 0.4133 | 0.5166 | yes | risk | data |

Top similarity neighbours: `public-openai-security-ownership-map` (0.428), `privacy-risk-reviewer` (0.413), `auth-flow-reviewer` (0.377), `identity-ops-resource-linker` (0.374), `psc-pdf-redaction-pass` (0.370)

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `code-reviewer` | 0.4008 | 0.2002 | 0.5156 | yes | review, implementation | review, code |
| `auth-flow-reviewer` | 0.4008 | 0.4319 | 0.6944 | yes | review, security | review, security, authorization |
| `security-threat-modeler` | 0.4008 | 0.2826 | 0.6276 | yes | security | security |

Top similarity neighbours: `api-security-threat-reviewer` (0.466), `api-ops-rewrite-editor` (0.440), `psc-handler-vulnerability-reviewer` (0.438), `auth-flow-reviewer` (0.432), `security-ops-rewrite-editor` (0.403)

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Plausible listed alternatives: 2
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.5351 | 0.1974 | 0.6562 | yes | - | review |
| `secret-leak-scanner` | 0.5351 | 0.2172 | 0.5770 | yes | - | - |
| `ci-failure-debugger` | 0.5351 | 0.1208 | 0.2660 | no | check, need | - |

Top similarity neighbours: `dependency-risk-auditor` (0.535), `psc-dependency-supply-chain-auditor` (0.522), `risk-ops-artifact-packager` (0.480), `risk-ops-dependency-mapper` (0.470), `supply-chain-ops-risk-reviewer` (0.391)

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `dependency-risk-auditor` | 0.4699 | 0.3471 | 0.5770 | yes | update | - |
| `security-code-reviewer` | 0.4699 | 0.3973 | 0.6436 | yes | diff | diff, unsafe |
| `privacy-risk-reviewer` | 0.4699 | 0.3400 | 0.5534 | yes | - | - |

Top similarity neighbours: `secret-leak-scanner` (0.470), `environment-config-auditor` (0.463), `security-ops-rewrite-editor` (0.427), `public-oh-my-changelog-maintenance` (0.419), `deployment-build-triager` (0.401)

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-code-reviewer` | 0.3801 | 0.1072 | 0.6944 | yes | - | review, authorization, security |
| `security-threat-modeler` | 0.3801 | 0.0842 | 0.5270 | yes | - | flow, security |
| `privacy-risk-reviewer` | 0.3801 | 0.2003 | 0.7290 | yes | - | review, risk |

Top similarity neighbours: `auth-flow-reviewer` (0.380), `identity-ops-failure-diagnoser` (0.284), `identity-ops-summary-writer` (0.252), `identity-ops-resource-linker` (0.232), `identity-ops-risk-reviewer` (0.220)

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `security-threat-modeler` | 0.4925 | 0.2250 | 0.5166 | yes | - | data |
| `secret-leak-scanner` | 0.4925 | 0.2724 | 0.5534 | yes | - | - |
| `auth-flow-reviewer` | 0.4925 | 0.3161 | 0.7290 | yes | - | review, risk |

Top similarity neighbours: `privacy-risk-reviewer` (0.492), `analytics-ops-compliance-checker` (0.469), `analytics-ops-risk-reviewer` (0.462), `analytics-ops-quality-auditor` (0.447), `dataset-ops-compliance-checker` (0.415)

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.4128 | 0.3250 | 0.6937 | yes | new, workflow | new |
| `skill-installer` | 0.4128 | 0.2942 | 0.8188 | yes | exist, library | exist, library, user', install |
| `skill-editor` | 0.4128 | 0.3765 | 0.7289 | yes | new, exist, workflow | exist, creat, new |

Top similarity neighbours: `meeting-notes-action-extractor` (0.544), `meeting-followup-extractor` (0.458), `method-note-builder` (0.445), `public-anthropic-doc-coauthoring` (0.436), `meeting-summary-writer` (0.435)

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 236

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-finder` | 0.2438 | 0.2277 | 0.8188 | yes | exist, library | install, exist, user', library |
| `skill-creator` | 0.2438 | 0.0283 | 0.6487 | yes | - | - |
| `skill-packager` | 0.2438 | 0.1780 | 0.7879 | yes | exist, prepare, check, file | prepare, exist |

Top similarity neighbours: `public-office-data-analysis` (0.609), `public-office-sheets-automation` (0.497), `data-analysis-for-reporting` (0.479), `public-swebench-xlsx` (0.462), `data-analysis-overview` (0.459)

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-editor` | 0.5725 | 0.4982 | 0.7846 | yes | workflow, new, exist | workflow, new, artifact, description, boundarie, resource |
| `skill-finder` | 0.5725 | 0.4275 | 0.6937 | yes | new, exist | new |
| `skill-packager` | 0.5725 | 0.3585 | 0.6525 | yes | exist | resource |

Top similarity neighbours: `skill-creator` (0.573), `skill-editor` (0.498), `skill-authoring-guide` (0.447), `psc-public-skill-atomizer` (0.446), `task-extractor` (0.438)

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 78

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.4342 | 0.3479 | 0.7846 | yes | description, trigger | artifact, description, workflow, boundarie, resource, new |
| `skill-evaluator` | 0.4342 | 0.3313 | 0.6445 | yes | exist, skill', description, trigger | exist, description, behavior |
| `skill-packager` | 0.4342 | 0.3111 | 0.6374 | yes | exist | exist, resource |

Top similarity neighbours: `document-field-extractor` (0.616), `course-ops-field-extractor` (0.559), `docs-ops-field-extractor` (0.558), `skill-field-auditor` (0.557), `writing-ops-field-extractor` (0.554)

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 8

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-editor` | 0.3869 | 0.3028 | 0.6445 | yes | - | exist, behavior, description |
| `skill-finder` | 0.3869 | 0.2673 | 0.6822 | yes | whether, already | exist, whether |
| `skill-creator` | 0.3869 | 0.2153 | 0.5384 | yes | trigger | trigger, description |

Top similarity neighbours: `reply-polisher` (0.601), `reply-drafter` (0.576), `email-polisher` (0.528), `followup-reply-writer` (0.494), `email-drafter` (0.440)

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 6

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-creator` | 0.3880 | 0.2272 | 0.6525 | yes | resource | resource |
| `skill-installer` | 0.3880 | 0.2697 | 0.7879 | yes | exist | prepare, exist |
| `skill-editor` | 0.3880 | 0.2195 | 0.6374 | yes | exist, resource | exist, resource |

Top similarity neighbours: `public-anthropic-doc-coauthoring` (0.475), `document-summariser` (0.430), `public-office-content-writer` (0.422), `docs-ops-summary-writer` (0.397), `public-skill-installer` (0.392)

### `skill_representation_analysis_p1_skill_field_auditor`

- Family: `skill_representation_analysis`
- Gold skill: `skill-field-auditor`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-authoring-guide` | 0.6763 | 0.5141 | 0.6900 | yes | trigger, resource, example | trigger, constraint, resource, example |
| `skill-router-policy-designer` | 0.6763 | 0.3289 | 0.5384 | yes | - | - |
| `skill-hierarchy-flattener` | 0.6763 | 0.2493 | 0.5194 | yes | resource | resource |
| `skill-installer-wrapper` | 0.6763 | 0.5400 | 0.6281 | yes | resource | resource |

Top similarity neighbours: `skill-field-auditor` (0.676), `training-ops-quality-auditor` (0.578), `psc-messy-skill-field-extractor` (0.558), `writing-ops-quality-auditor` (0.546), `course-ops-quality-auditor` (0.544)

### `skill_representation_analysis_p2_skill_authoring_guide`

- Family: `skill_representation_analysis`
- Gold skill: `skill-authoring-guide`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 12

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | 0.5022 | 0.5549 | 0.6900 | yes | includ, trigger, workflow, dependencie, example, exist | trigger, resource, constraint, example |
| `skill-router-policy-designer` | 0.5022 | 0.3856 | 0.6061 | yes | - | - |
| `skill-hierarchy-flattener` | 0.5022 | 0.4138 | 0.5291 | yes | atomic, boundarie | resource |
| `skill-installer-wrapper` | 0.5022 | 0.5098 | 0.6144 | yes | - | resource |

Top similarity neighbours: `migration-risk-auditor` (0.599), `skill-editor` (0.558), `skill-field-auditor` (0.555), `skill-creator` (0.542), `database-migration-risk-assessor` (0.535)

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Family: `skill_representation_analysis`
- Gold skill: `skill-router-policy-designer`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | 0.8082 | 0.4291 | 0.5384 | yes | includ, representation, field | - |
| `skill-authoring-guide` | 0.8082 | 0.4935 | 0.6061 | yes | - | - |
| `skill-hierarchy-flattener` | 0.8082 | 0.5538 | 0.6309 | yes | rout | rout |
| `skill-installer-wrapper` | 0.8082 | 0.4621 | 0.4956 | no | - | - |

Top similarity neighbours: `skill-router-policy-designer` (0.808), `psc-skill-routing-budget-planner` (0.736), `skill-hierarchy-flattener` (0.554), `psc-public-skill-atomizer` (0.539), `skill-finder` (0.530)

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Family: `skill_representation_analysis`
- Gold skill: `skill-hierarchy-flattener`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | 0.8028 | 0.4947 | 0.5194 | yes | resource | resource |
| `skill-authoring-guide` | 0.8028 | 0.5745 | 0.5291 | yes | resource | resource |
| `skill-router-policy-designer` | 0.8028 | 0.6226 | 0.6309 | yes | rout | rout |
| `skill-installer-wrapper` | 0.8028 | 0.6353 | 0.5982 | yes | preserv, resource | preserv, resource |

Top similarity neighbours: `skill-hierarchy-flattener` (0.803), `psc-public-skill-atomizer` (0.670), `skill-installer-wrapper` (0.635), `skill-router-policy-designer` (0.623), `skill-creator` (0.622)

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Family: `skill_representation_analysis`
- Gold skill: `skill-installer-wrapper`
- Plausible listed alternatives: 3
- Gold rank among all skills by similarity backend: 2

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | 0.6577 | 0.3312 | 0.6281 | yes | resource | resource |
| `skill-authoring-guide` | 0.6577 | 0.3540 | 0.6144 | yes | resource | resource |
| `skill-router-policy-designer` | 0.6577 | 0.2096 | 0.4956 | no | - | - |
| `skill-hierarchy-flattener` | 0.6577 | 0.2687 | 0.5982 | yes | preserv, resource | preserv, resource |

Top similarity neighbours: `public-skill-installer` (0.689), `skill-installer-wrapper` (0.658), `public-vercel-find-skills` (0.551), `public-oh-my-agentic-skills` (0.549), `public-skill-creator` (0.548)

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Family: `skill_representation_analysis`
- Gold skill: `skill-benchmark-evaluator`
- Plausible listed alternatives: 4
- Gold rank among all skills by similarity backend: 1

| Alternative | Prompt-gold | Prompt-alt | Gold-alt skill-card | Plausible? | Shared prompt/alt terms | Shared gold/alt terms |
|---|---:|---:|---:|---|---|---|
| `skill-field-auditor` | 0.4785 | 0.1974 | 0.6460 | yes | - | - |
| `skill-authoring-guide` | 0.4785 | 0.1415 | 0.5925 | yes | - | - |
| `skill-router-policy-designer` | 0.4785 | 0.1811 | 0.5846 | yes | - | - |
| `skill-hierarchy-flattener` | 0.4785 | 0.1847 | 0.5722 | yes | - | - |

Top similarity neighbours: `skill-benchmark-evaluator` (0.478), `psc-retrieval-result-adjudicator` (0.428), `rag-failure-diagnoser` (0.417), `search-ops-risk-reviewer` (0.405), `search-ops-priority-ranker` (0.400)

