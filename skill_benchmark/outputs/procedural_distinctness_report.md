# Procedural Distinctness Report

This report implements Step 2 of the benchmark rubric: each gold skill should be procedurally distinguishable from its closest alternatives before we test semantic confusability or retrieval accuracy.

Important interpretation: `not_for` boundaries are treated as supporting evidence, not as a primary reason by themselves. This prevents the benchmark from passing only because a skill contains a negated rule.

## Overall Status

- Step 2 status: **PASS**
- Prompts with at least one primary procedural differentiator for every alternative: 201/201 (100.0%)
- Gold/alternative pairs with at least one primary differentiator: 641/641 (100.0%)
- Gold/alternative pairs with two or more primary differentiators: 641/641 (100.0%)
- Prompts where all listed alternatives differ on two or more primary axes: 201/201 (100.0%)

Pass rule used here: every pair needs at least one primary procedural axis; the benchmark is considered strong when at least 80% of pairs have two or more primary axes.

What this proves: the current controlled skills expose positive procedural differences in their structured fields. What it does not prove yet: that flat metadata, embeddings, tree routing, graph retrieval, or rerankers will recover those differences under semantic similarity and scale. That is tested in later rubric steps.

Why Step 2 was previously unresolved: the coverage report showed that fields existed, but it did not compare each gold skill against its listed near alternatives. This report performs that pair-level check.

## Axis Frequency

| Primary axis | Pair count |
|---|---:|
| input/precondition | 641 |
| output artifact | 641 |
| workflow | 641 |
| success criterion | 641 |
| dependency/resource | 364 |

| Supporting boundary axis | Pair count |
|---|---:|
| avoid/not-for boundary | 640 |

## Family Summary

| Family | Prompts | Prompt pass | Strong prompts | Weak pairs |
|---|---:|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 | 0/21 |
| api_mcp_tooling | 6 | 6/6 | 6/6 | 0/24 |
| browser_web_automation | 6 | 6/6 | 6/6 | 0/18 |
| code_github_workflow | 6 | 6/6 | 6/6 | 0/18 |
| data_spreadsheet | 7 | 7/7 | 7/7 | 0/21 |
| deployment_browser_qa | 6 | 6/6 | 6/6 | 0/22 |
| documents_files | 7 | 7/7 | 7/7 | 0/21 |
| github_ci_maintenance | 6 | 6/6 | 6/6 | 0/24 |
| huggingface_ml_workflows | 6 | 6/6 | 6/6 | 0/24 |
| implicit_field_stress | 10 | 10/10 | 10/10 | 0/30 |
| metrics_observability | 6 | 6/6 | 6/6 | 0/18 |
| news_monitoring | 5 | 5/5 | 5/5 | 0/10 |
| observability_reliability | 6 | 6/6 | 6/6 | 0/24 |
| office_artifact_workflows | 6 | 6/6 | 6/6 | 0/22 |
| office_business_automation | 6 | 6/6 | 6/6 | 0/24 |
| pdf_document_operations | 6 | 6/6 | 6/6 | 0/24 |
| planning_meetings | 5 | 5/5 | 5/5 | 0/10 |
| public_style_controlled | 64 | 64/64 | 64/64 | 0/192 |
| reading_research | 8 | 8/8 | 8/8 | 0/24 |
| reply_messaging | 5 | 5/5 | 5/5 | 0/10 |
| security_appsec | 6 | 6/6 | 6/6 | 0/18 |
| skill_lifecycle | 6 | 6/6 | 6/6 | 0/18 |
| skill_representation_analysis | 6 | 6/6 | 6/6 | 0/24 |

## Weak Or Review-Worthy Pairs

- No weak pairs under the current heuristic.

## Prompt Detail

### `api_p1_openapi_contract_review`

- Family: `api_backend_design`
- Gold skill: `openapi-contract-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `external-api-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.15, output artifact=0.06, workflow=0.14, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `webhook-contract-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.06, workflow=0.10, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `architecture-boundary-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.07, workflow=0.03, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.11 |

### `api_p2_external_api_integration`

- Family: `api_backend_design`
- Gold skill: `external-api-integration-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `openapi-contract-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.15, output artifact=0.06, workflow=0.14, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `webhook-contract-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.16, output artifact=0.00, workflow=0.12, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `service-dependency-mapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.06, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |

### `api_p3_webhook_contract`

- Family: `api_backend_design`
- Gold skill: `webhook-contract-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `external-api-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.16, output artifact=0.00, workflow=0.12, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `openapi-contract-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.06, workflow=0.10, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `public-office-webhook-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-api-design-principles` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `api_p4_architecture_boundary`

- Family: `api_backend_design`
- Gold skill: `architecture-boundary-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `service-dependency-mapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.07, workflow=0.11, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `openapi-contract-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.07, workflow=0.03, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.11 |
| `database-migration-risk-assessor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.03, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.18 |

### `api_p5_database_migration_risk`

- Family: `api_backend_design`
- Gold skill: `database-migration-risk-assessor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `architecture-boundary-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.03, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `service-dependency-mapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.10 |
| `public-office-database-sync` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-architecture-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `architecture-boundary-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.07, workflow=0.11, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `external-api-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.06, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `public-architecture-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-api-design-principles` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `api_mcp_tooling_p1_rest_api_contract_designer`

- Family: `api_mcp_tooling`
- Gold skill: `rest-api-contract-designer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `mcp-server-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.33, workflow=0.26, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `webhook-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.31 |
| `auth-flow-integrator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.50 |
| `api-documentation-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.16, output artifact=0.22, workflow=0.13, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.25 |

### `api_mcp_tooling_p2_mcp_server_builder`

- Family: `api_mcp_tooling`
- Gold skill: `mcp-server-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `rest-api-contract-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.33, workflow=0.26, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `webhook-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.16 |
| `auth-flow-integrator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.11, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.38 |
| `api-documentation-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.08, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.10 |

### `api_mcp_tooling_p3_webhook_integration_planner`

- Family: `api_mcp_tooling`
- Gold skill: `webhook-integration-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-webhook-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `webhook-contract-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.22, output artifact=0.00, workflow=0.22, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.04 |
| `rest-api-contract-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.31 |
| `mcp-server-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.16 |

### `api_mcp_tooling_p4_auth_flow_integrator`

- Family: `api_mcp_tooling`
- Gold skill: `auth-flow-integrator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `rest-api-contract-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.50 |
| `mcp-server-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.11, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.38 |
| `webhook-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.09, workflow=0.07, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `api-documentation-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.19 |

### `api_mcp_tooling_p5_api_documentation_writer`

- Family: `api_mcp_tooling`
- Gold skill: `api-documentation-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `rest-api-contract-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.16, output artifact=0.22, workflow=0.13, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `mcp-server-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.08, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.10 |
| `webhook-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.36 |
| `auth-flow-integrator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.19 |

### `api_mcp_tooling_p6_api_security_threat_reviewer`

- Family: `api_mcp_tooling`
- Gold skill: `api-security-threat-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-security-threat-model` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-security-best-practices` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `security-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.05, workflow=0.18, success criterion=0.09, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `rest-api-contract-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `web_p1_page_snapshot`

- Family: `browser_web_automation`
- Gold skill: `web-page-snapshotter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.41, output artifact=0.05, workflow=0.09, success criterion=0.07, dependency/resource=0.33, avoid/not-for boundary=0.26 |
| `web-data-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.00, workflow=0.11, success criterion=0.09, dependency/resource=0.00, avoid/not-for boundary=0.15 |
| `frontend-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.05, workflow=0.07, success criterion=0.13, dependency/resource=0.33, avoid/not-for boundary=0.18 |

### `web_p2_form_filling`

- Family: `browser_web_automation`
- Gold skill: `web-form-filler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.04, workflow=0.08, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.21 |
| `web-page-snapshotter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.05, workflow=0.06, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.22 |
| `frontend-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.22, output artifact=0.00, workflow=0.02, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.10 |

### `web_p3_ui_test`

- Family: `browser_web_automation`
- Gold skill: `web-ui-tester`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-form-filler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.04, workflow=0.08, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.21 |
| `frontend-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.04, workflow=0.14, success criterion=0.03, dependency/resource=0.33, avoid/not-for boundary=0.18 |
| `web-page-snapshotter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.41, output artifact=0.05, workflow=0.09, success criterion=0.07, dependency/resource=0.33, avoid/not-for boundary=0.26 |

### `web_p4_data_extraction`

- Family: `browser_web_automation`
- Gold skill: `web-data-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-page-snapshotter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.00, workflow=0.11, success criterion=0.09, dependency/resource=0.00, avoid/not-for boundary=0.15 |
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.19 |
| `frontend-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.26, output artifact=0.00, workflow=0.04, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.25 |

### `web_p5_frontend_debugging`

- Family: `browser_web_automation`
- Gold skill: `frontend-debugger`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.04, workflow=0.14, success criterion=0.03, dependency/resource=0.33, avoid/not-for boundary=0.18 |
| `web-page-snapshotter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.05, workflow=0.07, success criterion=0.13, dependency/resource=0.33, avoid/not-for boundary=0.18 |
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.09, workflow=0.07, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.06 |

### `web_p6_accessibility_check`

- Family: `browser_web_automation`
- Gold skill: `accessibility-checker`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.00, workflow=0.06, success criterion=0.02, dependency/resource=0.33, avoid/not-for boundary=0.09 |
| `frontend-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.26, output artifact=0.10, workflow=0.08, success criterion=0.06, dependency/resource=0.33, avoid/not-for boundary=0.12 |
| `web-page-snapshotter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.00, workflow=0.07, success criterion=0.06, dependency/resource=0.33, avoid/not-for boundary=0.12 |

### `code_p1_local_code_review`

- Family: `code_github_workflow`
- Gold skill: `code-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.25, workflow=0.31, success criterion=0.21, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.10, workflow=0.10, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.30 |
| `ci-failure-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.29, output artifact=0.00, workflow=0.07, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.20 |

### `code_p2_pr_review`

- Family: `code_github_workflow`
- Gold skill: `pr-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.25, workflow=0.31, success criterion=0.21, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.04, workflow=0.08, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.19 |
| `ci-failure-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.00, workflow=0.05, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.21 |

### `code_p3_review_comment_resolution`

- Family: `code_github_workflow`
- Gold skill: `review-comment-resolver`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.04, workflow=0.08, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.19 |
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.10, workflow=0.10, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.30 |
| `ci-failure-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=0.05, workflow=0.10, success criterion=0.03, dependency/resource=0.00, avoid/not-for boundary=0.23 |

### `code_p4_ci_failure_debugging`

- Family: `code_github_workflow`
- Gold skill: `ci-failure-debugger`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.29, output artifact=0.00, workflow=0.07, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.20 |
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.00, workflow=0.05, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.21 |
| `review-comment-resolver` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=0.05, workflow=0.10, success criterion=0.03, dependency/resource=0.00, avoid/not-for boundary=0.23 |

### `code_p5_changelog_entry`

- Family: `code_github_workflow`
- Gold skill: `changelog-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `release-note-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.43, output artifact=0.04, workflow=0.13, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.37, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.18 |

### `code_p6_release_notes`

- Family: `code_github_workflow`
- Gold skill: `release-note-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `changelog-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.43, output artifact=0.04, workflow=0.13, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `pr-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.34, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.00, workflow=0.04, success criterion=0.06, dependency/resource=1.00, avoid/not-for boundary=0.26 |

### `data_p1_overview`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-overview`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-for-reporting` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.19, workflow=0.10, success criterion=0.24, dependency/resource=0.33, avoid/not-for boundary=0.07 |
| `data-analysis-with-anomaly-focus` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.18, workflow=0.07, success criterion=0.12, dependency/resource=0.40, avoid/not-for boundary=0.13 |
| `data-analysis-with-validation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.19, workflow=0.11, success criterion=0.16, dependency/resource=0.50, avoid/not-for boundary=0.16 |

### `data_p2_anomaly_focus`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-anomaly-focus`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.18, workflow=0.07, success criterion=0.12, dependency/resource=0.40, avoid/not-for boundary=0.13 |
| `data-analysis-for-root-cause-diagnosis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.26, workflow=0.10, success criterion=0.18, dependency/resource=0.40, avoid/not-for boundary=0.13 |
| `data-analysis-with-validation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.29, workflow=0.10, success criterion=0.18, dependency/resource=0.40, avoid/not-for boundary=0.13 |

### `data_p3_validation`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-with-validation`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.19, workflow=0.11, success criterion=0.16, dependency/resource=0.50, avoid/not-for boundary=0.16 |
| `data-analysis-with-anomaly-focus` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.29, workflow=0.10, success criterion=0.18, dependency/resource=0.40, avoid/not-for boundary=0.13 |
| `data-analysis-for-root-cause-diagnosis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.30, output artifact=0.33, workflow=0.06, success criterion=0.25, dependency/resource=0.50, avoid/not-for boundary=0.12 |

### `data_p4_root_cause`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-root-cause-diagnosis`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-with-anomaly-focus` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.26, workflow=0.10, success criterion=0.18, dependency/resource=0.40, avoid/not-for boundary=0.13 |
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.17, workflow=0.11, success criterion=0.16, dependency/resource=0.50, avoid/not-for boundary=0.25 |
| `data-analysis-with-validation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.30, output artifact=0.33, workflow=0.06, success criterion=0.25, dependency/resource=0.50, avoid/not-for boundary=0.12 |

### `data_p5_reporting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-reporting`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.19, workflow=0.10, success criterion=0.24, dependency/resource=0.33, avoid/not-for boundary=0.07 |
| `data-analysis-for-root-cause-diagnosis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.24, output artifact=0.22, workflow=0.06, success criterion=0.23, dependency/resource=0.33, avoid/not-for boundary=0.00 |
| `data-analysis-with-anomaly-focus` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.17, workflow=0.04, success criterion=0.13, dependency/resource=0.25, avoid/not-for boundary=0.16 |

### `data_p6_forecasting`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-forecasting`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.29, output artifact=0.17, workflow=0.08, success criterion=0.12, dependency/resource=0.50, avoid/not-for boundary=0.12 |
| `data-analysis-for-root-cause-diagnosis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=0.35, workflow=0.11, success criterion=0.19, dependency/resource=0.50, avoid/not-for boundary=0.08 |
| `data-analysis-with-anomaly-focus` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.20, workflow=0.12, success criterion=0.14, dependency/resource=0.40, avoid/not-for boundary=0.14 |

### `data_p7_ranking_selection`

- Family: `data_spreadsheet`
- Gold skill: `data-analysis-for-ranking-selection`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `data-analysis-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.18, workflow=0.04, success criterion=0.10, dependency/resource=0.50, avoid/not-for boundary=0.07 |
| `data-analysis-for-reporting` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.17, workflow=0.07, success criterion=0.12, dependency/resource=0.33, avoid/not-for boundary=0.20 |
| `data-analysis-for-forecasting` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=0.20, workflow=0.12, success criterion=0.10, dependency/resource=0.50, avoid/not-for boundary=0.08 |

### `deploy_p1_playwright_flow_debug`

- Family: `deployment_browser_qa`
- Gold skill: `playwright-flow-debugger`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.07, workflow=0.05, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.04 |
| `accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.15, workflow=0.08, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `public-playwright-interactive` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.04, success criterion=0.06, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-playwright` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.07, workflow=0.05, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.04 |
| `accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.07, workflow=0.02, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `public-openai-screenshot` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.07, workflow=0.02, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.15, workflow=0.08, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.16, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p4_build_log_triage`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-build-triager`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `deployment-release-verifier` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.09, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.12, workflow=0.07, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.23 |
| `web-performance-budget-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.13, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.05 |

### `deploy_p5_release_verification`

- Family: `deployment_browser_qa`
- Gold skill: `deployment-release-verifier`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `deployment-build-triager` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.09, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.02, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `public-netlify-deploy` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-vercel-deploy` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p6_performance_budget`

- Family: `deployment_browser_qa`
- Gold skill: `web-performance-budget-checker`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.15, workflow=0.04, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.14 |
| `deployment-release-verifier` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.08, workflow=0.02, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.10 |
| `accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.17, workflow=0.05, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.25 |

### `doc_p1_document_summary`

- Family: `documents_files`
- Gold skill: `document-summariser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-normaliser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.08, workflow=0.11, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.26 |
| `document-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.28, workflow=0.09, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.14 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.12, workflow=0.05, success criterion=0.12, dependency/resource=0.00, avoid/not-for boundary=0.26 |

### `doc_p2_document_rewriter`

- Family: `documents_files`
- Gold skill: `document-rewriter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-normaliser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.21, workflow=0.16, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `document-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.29, output artifact=0.14, workflow=0.18, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.18 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.35, output artifact=0.27, workflow=0.09, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.12 |

### `doc_p3_document_normaliser`

- Family: `documents_files`
- Gold skill: `document-normaliser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-rewriter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.21, workflow=0.16, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.40, output artifact=0.24, workflow=0.15, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `document-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.08, workflow=0.11, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.26 |

### `doc_p4_field_extraction`

- Family: `documents_files`
- Gold skill: `document-field-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.28, workflow=0.09, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.14 |
| `multi-document-comparison-preparer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.20, workflow=0.08, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `layout-preserving-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.07, workflow=0.09, success criterion=0.06, dependency/resource=0.33, avoid/not-for boundary=0.22 |

### `doc_p5_comparison_preparation`

- Family: `documents_files`
- Gold skill: `multi-document-comparison-preparer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-field-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.20, workflow=0.08, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `document-normaliser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.21, workflow=0.14, success criterion=0.15, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.38, output artifact=0.22, workflow=0.12, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.04 |

### `doc_p6_conversion`

- Family: `documents_files`
- Gold skill: `document-converter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-normaliser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.40, output artifact=0.24, workflow=0.15, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `layout-preserving-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.22, workflow=0.24, success criterion=0.16, dependency/resource=0.33, avoid/not-for boundary=0.12 |
| `document-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.12, workflow=0.05, success criterion=0.12, dependency/resource=0.00, avoid/not-for boundary=0.26 |

### `doc_p7_layout_preserving_conversion`

- Family: `documents_files`
- Gold skill: `layout-preserving-converter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.22, workflow=0.24, success criterion=0.16, dependency/resource=0.33, avoid/not-for boundary=0.12 |
| `document-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.07, workflow=0.09, success criterion=0.06, dependency/resource=0.33, avoid/not-for boundary=0.22 |
| `document-normaliser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.43, output artifact=0.17, workflow=0.15, success criterion=0.30, dependency/resource=0.33, avoid/not-for boundary=0.12 |

### `github_ci_maintenance_p1_ci_log_root_cause_debugger`

- Family: `github_ci_maintenance`
- Gold skill: `ci-log-root-cause-debugger`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.05 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.17, workflow=0.00, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `github-issue-triager` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `release-changelog-generator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.33 |

### `github_ci_maintenance_p2_pr_review_comment_resolver`

- Family: `github_ci_maintenance`
- Gold skill: `pr-review-comment-resolver`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-openai-gh-address-comments` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.18, output artifact=0.07, workflow=0.14, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.05 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=0.00, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `github_ci_maintenance_p3_repo_code_reviewer`

- Family: `github_ci_maintenance`
- Gold skill: `repo-code-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.17, workflow=0.00, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=0.00, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `github-issue-triager` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.12, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.13 |
| `release-changelog-generator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |

### `github_ci_maintenance_p4_github_issue_triager`

- Family: `github_ci_maintenance`
- Gold skill: `github-issue-triager`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.10, workflow=0.03, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.12, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.13 |
| `release-changelog-generator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |

### `github_ci_maintenance_p5_release_changelog_generator`

- Family: `github_ci_maintenance`
- Gold skill: `release-changelog-generator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `github-issue-triager` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |

### `github_ci_maintenance_p6_git_safety_guardrail_installer`

- Family: `github_ci_maintenance`
- Gold skill: `git-safety-guardrail-installer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-mattpocock-git-guardrails-claude-code` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-mattpocock-setup-pre-commit` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.20, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.07 |

### `huggingface_ml_workflows_p1_hf_dataset_viewer_inspector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-dataset-viewer-inspector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-datasets` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-tool-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |
| `sentence-transformer-finetuner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.08, workflow=0.03, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.18 |

### `huggingface_ml_workflows_p2_hf_local_model_selector`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-local-model-selector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-huggingface-local-models` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-huggingface-huggingface-best` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |
| `sentence-transformer-finetuner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.08, workflow=0.06, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.12 |

### `huggingface_ml_workflows_p3_sentence_transformer_finetuner`

- Family: `huggingface_ml_workflows`
- Gold skill: `sentence-transformer-finetuner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-huggingface-train-sentence-transformers` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-similarity-search-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.08, workflow=0.03, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.08, workflow=0.06, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.12 |

### `huggingface_ml_workflows_p4_gradio_demo_builder`

- Family: `huggingface_ml_workflows`
- Gold skill: `gradio-demo-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.08, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.06, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.31 |
| `sentence-transformer-finetuner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.07, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.06 |
| `hf-zerogpu-space-deployer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.12 |

### `huggingface_ml_workflows_p5_hf_zerogpu_space_deployer`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-zerogpu-space-deployer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.08, workflow=0.06, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.06 |
| `sentence-transformer-finetuner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `gradio-demo-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.12 |

### `huggingface_ml_workflows_p6_hf_community_eval_runner`

- Family: `huggingface_ml_workflows`
- Gold skill: `hf-community-eval-runner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.13 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.08, workflow=0.07, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.23 |
| `sentence-transformer-finetuner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.10, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `gradio-demo-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.03, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p10_trace_path`

- Family: `implicit_field_stress`
- Gold skill: `implicit-trace-path-diagnoser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-slo-alert-author` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `distributed-trace-investigator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.12, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |

### `implicit_p1_pdf_answer`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-evidence-answerer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-pdf-table-reconstructor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.19, output artifact=0.00, workflow=0.06, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.19, output artifact=0.20, workflow=0.18, success criterion=0.19, dependency/resource=1.00, avoid/not-for boundary=0.10 |
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.05 |

### `implicit_p2_pdf_table`

- Family: `implicit_field_stress`
- Gold skill: `implicit-pdf-table-reconstructor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-pdf-evidence-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.19, output artifact=0.00, workflow=0.06, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.10, success criterion=0.19, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p3_browser_flow`

- Family: `implicit_field_stress`
- Gold skill: `implicit-browser-flow-investigator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-visual-diff-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.02, output artifact=0.25, workflow=0.31, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.10 |
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.09, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p4_visual_diff`

- Family: `implicit_field_stress`
- Gold skill: `implicit-visual-diff-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-browser-flow-investigator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.07, workflow=0.20, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.00, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p5_ci_failure`

- Family: `implicit_field_stress`
- Gold skill: `implicit-ci-failure-reader`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-review-comment-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `ci-log-root-cause-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.15, workflow=0.23, success criterion=0.23, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p6_review_comments`

- Family: `implicit_field_stress`
- Gold skill: `implicit-review-comment-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-ci-failure-reader` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pr-review-comment-resolver` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.30, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `repo-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |

### `implicit_p7_hf_dataset`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-dataset-inspector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-hf-local-model-chooser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.10, workflow=0.20, success criterion=0.06, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |

### `implicit_p8_hf_model`

- Family: `implicit_field_stress`
- Gold skill: `implicit-hf-local-model-chooser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-hf-dataset-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `hf-local-model-selector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.17, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `hf-dataset-viewer-inspector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `implicit_p9_alert_rule`

- Family: `implicit_field_stress`
- Gold skill: `implicit-slo-alert-author`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `implicit-trace-path-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.27, output artifact=0.38, workflow=0.00, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.14 |
| `distributed-trace-investigator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |

### `obs_p1_metrics_overview`

- Family: `metrics_observability`
- Gold skill: `metrics-overview`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `incident-summary-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.53, output artifact=0.18, workflow=0.13, success criterion=0.15, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.19, workflow=0.16, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.33 |
| `latency-anomaly-detector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.43, output artifact=0.21, workflow=0.14, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.20 |

### `obs_p2_latency_anomaly`

- Family: `metrics_observability`
- Gold skill: `latency-anomaly-detector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.15, workflow=0.09, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.16 |
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.43, output artifact=0.21, workflow=0.14, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `slo-breach-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.45, output artifact=0.23, workflow=0.18, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.15 |

### `obs_p3_slo_breach`

- Family: `metrics_observability`
- Gold skill: `slo-breach-checker`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `capacity-risk-forecaster` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.40, workflow=0.03, success criterion=0.19, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.17, workflow=0.14, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.42 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.38, output artifact=0.26, workflow=0.07, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.33 |

### `obs_p4_capacity_risk`

- Family: `metrics_observability`
- Gold skill: `capacity-risk-forecaster`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `slo-breach-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.40, workflow=0.03, success criterion=0.19, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.32, output artifact=0.29, workflow=0.10, success criterion=0.22, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.37, output artifact=0.25, workflow=0.11, success criterion=0.16, dependency/resource=1.00, avoid/not-for boundary=0.29 |

### `obs_p5_root_cause`

- Family: `metrics_observability`
- Gold skill: `metrics-root-cause-diagnoser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `latency-anomaly-detector` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.15, workflow=0.09, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.16 |
| `capacity-risk-forecaster` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.32, output artifact=0.29, workflow=0.10, success criterion=0.22, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `incident-summary-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.21, workflow=0.08, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.22 |

### `obs_p6_incident_summary`

- Family: `metrics_observability`
- Gold skill: `incident-summary-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.53, output artifact=0.18, workflow=0.13, success criterion=0.15, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.21, workflow=0.08, success criterion=0.13, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `slo-breach-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.24, workflow=0.09, success criterion=0.23, dependency/resource=1.00, avoid/not-for boundary=0.09 |

### `news_p1_plain_summary`

- Family: `news_monitoring`
- Gold skill: `news-summariser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `news-briefing-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.20, success criterion=0.08, dependency/resource=0.00, avoid/not-for boundary=0.18 |
| `source-grounding-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.50, output artifact=0.06, workflow=0.10, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.14 |

### `news_p2_briefing`

- Family: `news_monitoring`
- Gold skill: `news-briefing-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `news-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.20, success criterion=0.08, dependency/resource=0.00, avoid/not-for boundary=0.18 |
| `tech-news-trend-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.34, output artifact=0.18, workflow=0.16, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.28 |

### `news_p3_grounded_claims`

- Family: `news_monitoring`
- Gold skill: `source-grounding-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `news-summariser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.50, output artifact=0.06, workflow=0.10, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.14 |
| `news-briefing-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.35, output artifact=0.00, workflow=0.11, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.15 |

### `news_p4_theme_extraction`

- Family: `news_monitoring`
- Gold skill: `news-theme-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `tech-news-trend-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.50, output artifact=0.11, workflow=0.20, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.26 |
| `news-briefing-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.00, workflow=0.09, success criterion=0.08, dependency/resource=0.00, avoid/not-for boundary=0.19 |

### `news_p5_trend_signal`

- Family: `news_monitoring`
- Gold skill: `tech-news-trend-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `news-theme-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.50, output artifact=0.11, workflow=0.20, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.26 |
| `news-briefing-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.34, output artifact=0.18, workflow=0.16, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.28 |

### `observability_reliability_p1_prometheus_alert_rule_writer`

- Family: `observability_reliability`
- Gold skill: `prometheus-alert-rule-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-prometheus-configuration` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `slo-breach-checker` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.05, workflow=0.04, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.10 |
| `grafana-dashboard-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `distributed-trace-investigator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `observability_reliability_p2_grafana_dashboard_builder`

- Family: `observability_reliability`
- Gold skill: `grafana-dashboard-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-grafana-dashboards` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-python-observability` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `metrics-overview` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.04 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.25 |

### `observability_reliability_p3_distributed_trace_investigator`

- Family: `observability_reliability`
- Gold skill: `distributed-trace-investigator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-distributed-tracing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-python-observability` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `metrics-root-cause-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.04, workflow=0.04, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.05 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `observability_reliability_p4_slo_breach_narrative_writer`

- Family: `observability_reliability`
- Gold skill: `slo-breach-narrative-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `incident-summary-writer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.10, workflow=0.14, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `slo-breach-checker` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.00, workflow=0.02, success criterion=0.03, dependency/resource=0.00, avoid/not-for boundary=0.04 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.23 |
| `grafana-dashboard-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.36 |

### `observability_reliability_p5_resilience_pattern_reviewer`

- Family: `observability_reliability`
- Gold skill: `resilience-pattern-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-python-resilience` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `dependency-risk-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.10, workflow=0.06, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.00, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `grafana-dashboard-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |

### `observability_reliability_p6_service_mesh_traffic_debugger`

- Family: `observability_reliability`
- Gold skill: `service-mesh-traffic-debugger`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-swebench-service-mesh-observability` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-istio-traffic-management` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-linkerd-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `prometheus-alert-rule-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.08, workflow=0.03, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.23 |

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-ocr-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.06, workflow=0.04, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `public-office-pdf-extraction` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-pdf` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p2_scanned_pdf_ocr`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-ocr-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-layout-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.06, workflow=0.04, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.06, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `document-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.05, workflow=0.09, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.08 |

### `office_p3_docx_redline`

- Family: `office_artifact_workflows`
- Gold skill: `docx-redline-editor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.09, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `document-rewriter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.05 |
| `public-docx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-docx-manipulation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `data-analysis-with-validation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.05, workflow=0.09, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.04 |
| `public-xlsx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.03, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-xlsx-manipulation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.04, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-layout-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.13, workflow=0.05, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `public-pptx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.06, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-ppt-visual` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.06, output artifact=0.10, workflow=0.04, success criterion=0.06, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-layout-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `docx-redline-editor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.09, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.13, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.08 |

### `office_business_automation_p1_xlsx_formula_model_builder`

- Family: `office_business_automation`
- Gold skill: `xlsx-formula-model-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-xlsx-manipulation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-swebench-xlsx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.04, workflow=0.02, success criterion=0.03, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-data-analysis` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.01, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `airtable-workflow-automator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.04, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `office_business_automation_p2_airtable_workflow_automator`

- Family: `office_business_automation`
- Gold skill: `airtable-workflow-automator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-airtable-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-crm-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `xlsx-formula-model-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.04, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `notion-research-database-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.15, output artifact=0.09, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `office_business_automation_p3_notion_research_database_builder`

- Family: `office_business_automation`
- Gold skill: `notion-research-database-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-notion-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-notion-research-documentation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `xlsx-formula-model-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.06 |
| `airtable-workflow-automator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.15, output artifact=0.09, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `office_business_automation_p4_calendar_scheduling_optimizer`

- Family: `office_business_automation`
- Gold skill: `calendar-scheduling-optimizer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-calendar-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `meeting-agenda-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.14 |
| `xlsx-formula-model-builder` | input/precondition, output artifact, workflow, success criterion | - | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.89 |
| `airtable-workflow-automator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.00 |

### `office_business_automation_p5_meeting_notes_action_extractor`

- Family: `office_business_automation`
- Gold skill: `meeting-notes-action-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-meeting-notes` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `meeting-followup-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.19, output artifact=0.06, workflow=0.16, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.04 |
| `xlsx-formula-model-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.23 |
| `airtable-workflow-automator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `office_business_automation_p6_email_classification_router`

- Family: `office_business_automation`
- Gold skill: `email-classification-router`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-email-classifier` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-gmail-workflows` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.01, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-suspicious-email` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `xlsx-formula-model-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.20 |

### `pdf_document_operations_p1_pdf_question_answerer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-question-answerer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.12, workflow=0.06, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.05 |
| `pdf-ocr-cleaner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.17, workflow=0.16, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.31 |
| `pdf-form-filler` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.08, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.36 |
| `pdf-redaction-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.15, workflow=0.09, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.36 |

### `pdf_document_operations_p2_pdf_layout_table_extractor`

- Family: `pdf_document_operations`
- Gold skill: `pdf-layout-table-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.12, workflow=0.06, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.05 |
| `pdf-ocr-cleaner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.06, workflow=0.11, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-form-filler` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=0.13, workflow=0.03, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.13 |
| `pdf-redaction-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.06, workflow=0.06, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.13 |

### `pdf_document_operations_p3_pdf_ocr_cleaner`

- Family: `pdf_document_operations`
- Gold skill: `pdf-ocr-cleaner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.17, workflow=0.16, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.31 |
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.06, workflow=0.11, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-form-filler` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `pdf-redaction-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.07, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.29 |

### `pdf_document_operations_p4_pdf_form_filler`

- Family: `pdf_document_operations`
- Gold skill: `pdf-form-filler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `public-office-pdf-form-filler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.08, success criterion=0.05, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `document-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.13, workflow=0.02, success criterion=0.15, dependency/resource=0.00, avoid/not-for boundary=0.05 |
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.08, workflow=0.03, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.36 |
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.17, output artifact=0.13, workflow=0.03, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.13 |

### `pdf_document_operations_p5_pdf_redaction_reviewer`

- Family: `pdf_document_operations`
- Gold skill: `pdf-redaction-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `privacy-risk-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.06, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-contract-review` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.04 |
| `public-openai-pdf` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.15, workflow=0.09, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.36 |

### `pdf_document_operations_p6_pdf_to_docx_converter`

- Family: `pdf_document_operations`
- Gold skill: `pdf-to-docx-converter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-question-answerer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.19 |
| `pdf-layout-table-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.06, workflow=0.09, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.13 |
| `pdf-ocr-cleaner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.00, workflow=0.11, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.20 |
| `pdf-form-filler` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.23 |

### `plan_p1_meeting_agenda`

- Family: `planning_meetings`
- Gold skill: `meeting-agenda-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `weekly-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.08, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.44 |
| `task-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.00, workflow=0.00, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.29 |

### `plan_p2_meeting_summary`

- Family: `planning_meetings`
- Gold skill: `meeting-summary-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `meeting-followup-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.50, output artifact=0.05, workflow=0.09, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.35 |
| `task-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.00, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.22 |

### `plan_p3_meeting_followup`

- Family: `planning_meetings`
- Gold skill: `meeting-followup-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `meeting-summary-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.50, output artifact=0.05, workflow=0.09, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.35 |
| `task-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.46, output artifact=0.00, workflow=0.21, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `plan_p4_task_extractor`

- Family: `planning_meetings`
- Gold skill: `task-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `weekly-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.40, output artifact=0.00, workflow=0.08, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.35 |
| `meeting-followup-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.46, output artifact=0.00, workflow=0.21, success criterion=0.12, dependency/resource=1.00, avoid/not-for boundary=0.21 |

### `plan_p5_weekly_planner`

- Family: `planning_meetings`
- Gold skill: `weekly-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `task-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.40, output artifact=0.00, workflow=0.08, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.35 |
| `meeting-agenda-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.08, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.44 |

### `psc_browser_quality_p01_1_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.13, workflow=0.04, success criterion=0.13, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.08 |

### `psc_browser_quality_p01_2_psc_devtools_runtime_diagnoser`

- Family: `public_style_controlled`
- Gold skill: `psc-devtools-runtime-diagnoser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.13, workflow=0.04, success criterion=0.13, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.08 |

### `psc_browser_quality_p02_1_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.13, workflow=0.04, success criterion=0.13, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.40, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |

### `psc_browser_quality_p02_2_psc_playwright_regression_suite`

- Family: `public_style_controlled`
- Gold skill: `psc-playwright-regression-suite`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.13, workflow=0.04, success criterion=0.13, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.40, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |

### `psc_browser_quality_p03_1_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.40, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.07, workflow=0.07, success criterion=0.07, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_browser_quality_p03_2_psc_visual_screenshot_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-visual-screenshot-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.40, avoid/not-for boundary=0.00 |
| `psc-accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.07, workflow=0.07, success criterion=0.07, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_browser_quality_p04_1_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.08 |
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.07, workflow=0.07, success criterion=0.07, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_browser_quality_p04_2_psc_accessibility_interaction_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-accessibility-interaction-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-devtools-runtime-diagnoser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.08 |
| `psc-playwright-regression-suite` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-visual-screenshot-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.07, workflow=0.07, success criterion=0.07, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_data_analysis_intent_p01_1_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.08, success criterion=0.07, dependency/resource=0.29, avoid/not-for boundary=0.15 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.43, avoid/not-for boundary=0.07 |

### `psc_data_analysis_intent_p01_2_psc_data_trust_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-data-trust-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.08, success criterion=0.07, dependency/resource=0.29, avoid/not-for boundary=0.15 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.43, avoid/not-for boundary=0.07 |

### `psc_data_analysis_intent_p02_1_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.08, success criterion=0.07, dependency/resource=0.29, avoid/not-for boundary=0.15 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_data_analysis_intent_p02_2_psc_anomaly_watchlist_builder`

- Family: `public_style_controlled`
- Gold skill: `psc-anomaly-watchlist-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.03, output artifact=0.07, workflow=0.08, success criterion=0.07, dependency/resource=0.29, avoid/not-for boundary=0.15 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_data_analysis_intent_p03_1_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |

### `psc_data_analysis_intent_p03_2_psc_decision_ranking_analyst`

- Family: `public_style_controlled`
- Gold skill: `psc-decision-ranking-analyst`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-executive-metric-narrator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |

### `psc_data_analysis_intent_p04_1_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.43, avoid/not-for boundary=0.07 |
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |

### `psc_data_analysis_intent_p04_2_psc_executive_metric_narrator`

- Family: `public_style_controlled`
- Gold skill: `psc-executive-metric-narrator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-data-trust-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.43, avoid/not-for boundary=0.07 |
| `psc-anomaly-watchlist-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |
| `psc-decision-ranking-analyst` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |

### `psc_github_maintenance_p01_1_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.10, success criterion=0.07, dependency/resource=0.38, avoid/not-for boundary=0.27 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.15, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.18 |

### `psc_github_maintenance_p01_2_psc_ci_log_first_failure_reader`

- Family: `public_style_controlled`
- Gold skill: `psc-ci-log-first-failure-reader`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.10, success criterion=0.07, dependency/resource=0.38, avoid/not-for boundary=0.27 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.15, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.18 |

### `psc_github_maintenance_p02_1_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.10, success criterion=0.07, dependency/resource=0.38, avoid/not-for boundary=0.27 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.23, workflow=0.00, success criterion=0.23, dependency/resource=0.17, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.07, success criterion=0.08, dependency/resource=0.29, avoid/not-for boundary=0.18 |

### `psc_github_maintenance_p02_2_psc_pr_thread_fix_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-pr-thread-fix-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.07, workflow=0.10, success criterion=0.07, dependency/resource=0.38, avoid/not-for boundary=0.27 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.23, workflow=0.00, success criterion=0.23, dependency/resource=0.17, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.07, success criterion=0.08, dependency/resource=0.29, avoid/not-for boundary=0.18 |

### `psc_github_maintenance_p03_1_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.15, avoid/not-for boundary=0.00 |
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.23, workflow=0.00, success criterion=0.23, dependency/resource=0.17, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.18, avoid/not-for boundary=0.00 |

### `psc_github_maintenance_p03_2_psc_repo_guardrail_hook_installer`

- Family: `public_style_controlled`
- Gold skill: `psc-repo-guardrail-hook-installer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.15, avoid/not-for boundary=0.00 |
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.23, workflow=0.00, success criterion=0.23, dependency/resource=0.17, avoid/not-for boundary=0.00 |
| `psc-release-communication-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.18, avoid/not-for boundary=0.00 |

### `psc_github_maintenance_p04_1_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.18 |
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.07, success criterion=0.08, dependency/resource=0.29, avoid/not-for boundary=0.18 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.18, avoid/not-for boundary=0.00 |

### `psc_github_maintenance_p04_2_psc_release_communication_packager`

- Family: `public_style_controlled`
- Gold skill: `psc-release-communication-packager`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-ci-log-first-failure-reader` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.18 |
| `psc-pr-thread-fix-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.07, success criterion=0.08, dependency/resource=0.29, avoid/not-for boundary=0.18 |
| `psc-repo-guardrail-hook-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.18, avoid/not-for boundary=0.00 |

### `psc_huggingface_workflow_p01_1_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.15 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.17, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.36, avoid/not-for boundary=0.18 |

### `psc_huggingface_workflow_p01_2_psc_hf_dataset_card_inspector`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-dataset-card-inspector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.15 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.17, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.36, avoid/not-for boundary=0.18 |

### `psc_huggingface_workflow_p02_1_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.15 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.06, workflow=0.04, success criterion=0.06, dependency/resource=0.13, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.12, avoid/not-for boundary=0.17 |

### `psc_huggingface_workflow_p02_2_psc_local_model_fit_selector`

- Family: `public_style_controlled`
- Gold skill: `psc-local-model-fit-selector`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.13, avoid/not-for boundary=0.15 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.06, workflow=0.04, success criterion=0.06, dependency/resource=0.13, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.12, avoid/not-for boundary=0.17 |

### `psc_huggingface_workflow_p03_1_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.17, avoid/not-for boundary=0.08 |
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.06, workflow=0.04, success criterion=0.06, dependency/resource=0.13, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.15, avoid/not-for boundary=0.00 |

### `psc_huggingface_workflow_p03_2_psc_sentence_embedding_trainer`

- Family: `public_style_controlled`
- Gold skill: `psc-sentence-embedding-trainer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.17, avoid/not-for boundary=0.08 |
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.06, workflow=0.04, success criterion=0.06, dependency/resource=0.13, avoid/not-for boundary=0.08 |
| `psc-hf-space-deployment-preparer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.15, avoid/not-for boundary=0.00 |

### `psc_huggingface_workflow_p04_1_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.36, avoid/not-for boundary=0.18 |
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.12, avoid/not-for boundary=0.17 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.15, avoid/not-for boundary=0.00 |

### `psc_huggingface_workflow_p04_2_psc_hf_space_deployment_preparer`

- Family: `public_style_controlled`
- Gold skill: `psc-hf-space-deployment-preparer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-hf-dataset-card-inspector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.03, success criterion=0.00, dependency/resource=0.36, avoid/not-for boundary=0.18 |
| `psc-local-model-fit-selector` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.20, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.12, avoid/not-for boundary=0.17 |
| `psc-sentence-embedding-trainer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.15, avoid/not-for boundary=0.00 |

### `psc_pdf_document_work_p01_1_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=0.15, workflow=0.03, success criterion=0.15, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.14, workflow=0.03, success criterion=0.10, dependency/resource=0.27, avoid/not-for boundary=0.18 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.12, workflow=0.03, success criterion=0.09, dependency/resource=0.25, avoid/not-for boundary=0.19 |

### `psc_pdf_document_work_p01_2_psc_pdf_native_extraction_pack`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-native-extraction-pack`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=0.15, workflow=0.03, success criterion=0.15, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.14, workflow=0.03, success criterion=0.10, dependency/resource=0.27, avoid/not-for boundary=0.18 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.12, workflow=0.03, success criterion=0.09, dependency/resource=0.25, avoid/not-for boundary=0.19 |

### `psc_pdf_document_work_p02_1_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=0.15, workflow=0.03, success criterion=0.15, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.07, workflow=0.03, success criterion=0.05, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.03, success criterion=0.10, dependency/resource=0.17, avoid/not-for boundary=0.19 |

### `psc_pdf_document_work_p02_2_psc_pdf_scan_ocr_recovery`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-scan-ocr-recovery`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.18, output artifact=0.15, workflow=0.03, success criterion=0.15, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.07, workflow=0.03, success criterion=0.05, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.03, success criterion=0.10, dependency/resource=0.17, avoid/not-for boundary=0.19 |

### `psc_pdf_document_work_p03_1_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.14, workflow=0.03, success criterion=0.10, dependency/resource=0.27, avoid/not-for boundary=0.18 |
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.07, workflow=0.03, success criterion=0.05, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.12, workflow=0.03, success criterion=0.07, dependency/resource=0.36, avoid/not-for boundary=0.12 |

### `psc_pdf_document_work_p03_2_psc_pdf_evidence_qa`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-evidence-qa`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.14, output artifact=0.14, workflow=0.03, success criterion=0.10, dependency/resource=0.27, avoid/not-for boundary=0.18 |
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.11, output artifact=0.07, workflow=0.03, success criterion=0.05, dependency/resource=0.18, avoid/not-for boundary=0.05 |
| `psc-pdf-redaction-pass` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.12, workflow=0.03, success criterion=0.07, dependency/resource=0.36, avoid/not-for boundary=0.12 |

### `psc_pdf_document_work_p04_1_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.12, workflow=0.03, success criterion=0.09, dependency/resource=0.25, avoid/not-for boundary=0.19 |
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.03, success criterion=0.10, dependency/resource=0.17, avoid/not-for boundary=0.19 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.12, workflow=0.03, success criterion=0.07, dependency/resource=0.36, avoid/not-for boundary=0.12 |

### `psc_pdf_document_work_p04_2_psc_pdf_redaction_pass`

- Family: `public_style_controlled`
- Gold skill: `psc-pdf-redaction-pass`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-pdf-native-extraction-pack` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.12, workflow=0.03, success criterion=0.09, dependency/resource=0.25, avoid/not-for boundary=0.19 |
| `psc-pdf-scan-ocr-recovery` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.13, workflow=0.03, success criterion=0.10, dependency/resource=0.17, avoid/not-for boundary=0.19 |
| `psc-pdf-evidence-qa` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.12, workflow=0.03, success criterion=0.07, dependency/resource=0.36, avoid/not-for boundary=0.12 |

### `psc_research_reading_p01_1_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.33, avoid/not-for boundary=0.08 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.25 |

### `psc_research_reading_p01_2_psc_paper_method_mapper`

- Family: `public_style_controlled`
- Gold skill: `psc-paper-method-mapper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.33, avoid/not-for boundary=0.08 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.25 |

### `psc_research_reading_p02_1_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.09, workflow=0.17, success criterion=0.09, dependency/resource=0.43, avoid/not-for boundary=0.00 |

### `psc_research_reading_p02_2_psc_citation_claim_support_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-citation-claim-support-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.09, workflow=0.17, success criterion=0.09, dependency/resource=0.43, avoid/not-for boundary=0.00 |

### `psc_research_reading_p03_1_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.33, avoid/not-for boundary=0.08 |
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_research_reading_p03_2_psc_related_work_synthesizer`

- Family: `public_style_controlled`
- Gold skill: `psc-related-work-synthesizer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.33, avoid/not-for boundary=0.08 |
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-source-field-table-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_research_reading_p04_1_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.25 |
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.09, workflow=0.17, success criterion=0.09, dependency/resource=0.43, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_research_reading_p04_2_psc_source_field_table_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-source-field-table-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-paper-method-mapper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.50, avoid/not-for boundary=0.25 |
| `psc-citation-claim-support-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.09, workflow=0.17, success criterion=0.09, dependency/resource=0.43, avoid/not-for boundary=0.00 |
| `psc-related-work-synthesizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.10, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.08 |

### `psc_security_appsec_p01_1_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.18, avoid/not-for boundary=0.15 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.08, output artifact=0.08, workflow=0.04, success criterion=0.08, dependency/resource=0.22, avoid/not-for boundary=0.17 |

### `psc_security_appsec_p01_2_psc_feature_threat_modeler`

- Family: `public_style_controlled`
- Gold skill: `psc-feature-threat-modeler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.18, avoid/not-for boundary=0.15 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.08, output artifact=0.08, workflow=0.04, success criterion=0.08, dependency/resource=0.22, avoid/not-for boundary=0.17 |

### `psc_security_appsec_p02_1_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.17 |

### `psc_security_appsec_p02_2_psc_handler_vulnerability_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-handler-vulnerability-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.07 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.17 |

### `psc_security_appsec_p03_1_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.18, avoid/not-for boundary=0.15 |
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_security_appsec_p03_2_psc_dependency_supply_chain_auditor`

- Family: `public_style_controlled`
- Gold skill: `psc-dependency-supply-chain-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.18, avoid/not-for boundary=0.15 |
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.07 |
| `psc-privacy-telemetry-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_security_appsec_p04_1_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.08, output artifact=0.08, workflow=0.04, success criterion=0.08, dependency/resource=0.22, avoid/not-for boundary=0.17 |
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.17 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_security_appsec_p04_2_psc_privacy_telemetry_reviewer`

- Family: `public_style_controlled`
- Gold skill: `psc-privacy-telemetry-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-feature-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.08, output artifact=0.08, workflow=0.04, success criterion=0.08, dependency/resource=0.22, avoid/not-for boundary=0.17 |
| `psc-handler-vulnerability-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.17 |
| `psc-dependency-supply-chain-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=0.20, avoid/not-for boundary=0.00 |

### `psc_skill_representation_p01_1_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |

### `psc_skill_representation_p01_2_psc_messy_skill_field_extractor`

- Family: `public_style_controlled`
- Gold skill: `psc-messy-skill-field-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |

### `psc_skill_representation_p02_1_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.22, avoid/not-for boundary=0.00 |

### `psc_skill_representation_p02_2_psc_public_skill_atomizer`

- Family: `public_style_controlled`
- Gold skill: `psc-public-skill-atomizer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.29, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.22, avoid/not-for boundary=0.00 |

### `psc_skill_representation_p03_1_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.20, avoid/not-for boundary=0.08 |

### `psc_skill_representation_p03_2_psc_skill_routing_budget_planner`

- Family: `public_style_controlled`
- Gold skill: `psc-skill-routing-budget-planner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.05, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-retrieval-result-adjudicator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.20, avoid/not-for boundary=0.08 |

### `psc_skill_representation_p04_1_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.20, avoid/not-for boundary=0.08 |

### `psc_skill_representation_p04_2_psc_retrieval_result_adjudicator`

- Family: `public_style_controlled`
- Gold skill: `psc-retrieval-result-adjudicator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `psc-messy-skill-field-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.25, avoid/not-for boundary=0.00 |
| `psc-public-skill-atomizer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.07, workflow=0.00, success criterion=0.07, dependency/resource=0.22, avoid/not-for boundary=0.00 |
| `psc-skill-routing-budget-planner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.10, output artifact=0.08, workflow=0.00, success criterion=0.08, dependency/resource=0.20, avoid/not-for boundary=0.08 |

### `read_p1_paper_summary`

- Family: `reading_research`
- Gold skill: `paper-summariser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `general-source-summariser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.28, output artifact=0.15, workflow=0.20, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `method-note-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.26, workflow=0.15, success criterion=0.18, dependency/resource=0.00, avoid/not-for boundary=0.33 |
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.10, workflow=0.21, success criterion=0.14, dependency/resource=0.00, avoid/not-for boundary=0.15 |

### `read_p2_general_source_summary`

- Family: `reading_research`
- Gold skill: `general-source-summariser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.28, output artifact=0.15, workflow=0.20, success criterion=0.18, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `document-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.29, output artifact=0.17, workflow=0.11, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.31, output artifact=0.20, workflow=0.20, success criterion=0.18, dependency/resource=0.00, avoid/not-for boundary=0.15 |

### `read_p3_citation_notes`

- Family: `reading_research`
- Gold skill: `citation-note-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `document-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.10, workflow=0.12, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.16 |
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.10, workflow=0.21, success criterion=0.14, dependency/resource=0.00, avoid/not-for boundary=0.15 |
| `citation-grounding-helper` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.10, workflow=0.06, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.15 |

### `read_p4_document_extraction`

- Family: `reading_research`
- Gold skill: `document-extractor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.10, workflow=0.12, success criterion=0.10, dependency/resource=0.00, avoid/not-for boundary=0.16 |
| `method-note-builder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.10, workflow=0.10, success criterion=0.08, dependency/resource=0.00, avoid/not-for boundary=0.24 |
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.26, output artifact=0.11, workflow=0.07, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.17 |

### `read_p5_method_notes`

- Family: `reading_research`
- Gold skill: `method-note-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.28, output artifact=0.26, workflow=0.15, success criterion=0.18, dependency/resource=0.00, avoid/not-for boundary=0.33 |
| `document-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.33, output artifact=0.10, workflow=0.10, success criterion=0.08, dependency/resource=0.00, avoid/not-for boundary=0.24 |
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.28, output artifact=0.19, workflow=0.12, success criterion=0.31, dependency/resource=1.00, avoid/not-for boundary=0.13 |

### `read_p6_grounding_check`

- Family: `reading_research`
- Gold skill: `citation-grounding-helper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.10, workflow=0.06, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.15 |
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.24, output artifact=0.10, workflow=0.02, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `document-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.28, output artifact=0.18, workflow=0.08, success criterion=0.07, dependency/resource=1.00, avoid/not-for boundary=0.08 |

### `read_p7_multi_source_comparison`

- Family: `reading_research`
- Gold skill: `multi-source-comparison-builder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `related-work-synthesiser` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.24, workflow=0.12, success criterion=0.26, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `method-note-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.28, output artifact=0.21, workflow=0.15, success criterion=0.20, dependency/resource=1.00, avoid/not-for boundary=0.38 |
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.22, workflow=0.11, success criterion=0.22, dependency/resource=1.00, avoid/not-for boundary=0.29 |

### `read_p8_related_work_synthesis`

- Family: `reading_research`
- Gold skill: `related-work-synthesiser`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `multi-source-comparison-builder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.24, workflow=0.12, success criterion=0.26, dependency/resource=1.00, avoid/not-for boundary=0.25 |
| `citation-note-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.27, workflow=0.06, success criterion=0.19, dependency/resource=1.00, avoid/not-for boundary=0.11 |
| `paper-summariser` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.34, output artifact=0.12, workflow=0.08, success criterion=0.13, dependency/resource=0.00, avoid/not-for boundary=0.12 |

### `reply_p1_professor_reply`

- Family: `reply_messaging`
- Gold skill: `professor-email-reply`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `reply-drafter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.06, workflow=0.17, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `reply-polisher` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.04, workflow=0.06, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.05 |

### `reply_p2_polish_supervisor`

- Family: `reply_messaging`
- Gold skill: `reply-polisher`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `professor-email-reply` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.04, workflow=0.06, success criterion=0.08, dependency/resource=1.00, avoid/not-for boundary=0.05 |
| `reply-drafter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.13, workflow=0.13, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.18 |

### `reply_p3_groupwork_coordination`

- Family: `reply_messaging`
- Gold skill: `groupwork-reply`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `reply-drafter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.29, output artifact=0.12, workflow=0.09, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.15 |
| `followup-reply-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.06, workflow=0.09, success criterion=0.21, dependency/resource=1.00, avoid/not-for boundary=0.06 |

### `reply_p4_followup_commitment`

- Family: `reply_messaging`
- Gold skill: `followup-reply-writer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `reply-drafter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.06, workflow=0.12, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `groupwork-reply` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.36, output artifact=0.06, workflow=0.09, success criterion=0.21, dependency/resource=1.00, avoid/not-for boundary=0.06 |

### `reply_p5_generic_fresh_draft`

- Family: `reply_messaging`
- Gold skill: `reply-drafter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `reply-polisher` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.33, output artifact=0.13, workflow=0.13, success criterion=0.17, dependency/resource=1.00, avoid/not-for boundary=0.18 |
| `followup-reply-writer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.42, output artifact=0.06, workflow=0.12, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.17 |

### `sec_p1_threat_model`

- Family: `security_appsec`
- Gold skill: `security-threat-modeler`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `security-code-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.15, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.19 |
| `auth-flow-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.09, workflow=0.09, success criterion=0.14, dependency/resource=0.33, avoid/not-for boundary=0.12 |
| `privacy-risk-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=0.13, workflow=0.09, success criterion=0.21, dependency/resource=0.33, avoid/not-for boundary=0.04 |

### `sec_p2_security_code_review`

- Family: `security_appsec`
- Gold skill: `security-code-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.09, workflow=0.14, success criterion=0.06, dependency/resource=1.00, avoid/not-for boundary=0.02 |
| `auth-flow-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.10, workflow=0.12, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.35 |
| `security-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.38, output artifact=0.00, workflow=0.15, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.19 |

### `sec_p3_dependency_risk`

- Family: `security_appsec`
- Gold skill: `dependency-risk-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `security-code-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.32, output artifact=0.00, workflow=0.08, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.12 |
| `secret-leak-scanner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.04, workflow=0.03, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.18 |
| `ci-failure-debugger` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.05, success criterion=0.04, dependency/resource=0.33, avoid/not-for boundary=0.08 |

### `sec_p4_secret_leak`

- Family: `security_appsec`
- Gold skill: `secret-leak-scanner`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `dependency-risk-auditor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.04, workflow=0.03, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.18 |
| `security-code-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.31, output artifact=0.00, workflow=0.08, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.15 |
| `privacy-risk-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.24 |

### `sec_p5_auth_flow`

- Family: `security_appsec`
- Gold skill: `auth-flow-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `security-code-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.36, output artifact=0.10, workflow=0.12, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.35 |
| `security-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.37, output artifact=0.09, workflow=0.09, success criterion=0.14, dependency/resource=0.33, avoid/not-for boundary=0.12 |
| `privacy-risk-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.42, output artifact=0.10, workflow=0.10, success criterion=0.12, dependency/resource=0.33, avoid/not-for boundary=0.41 |

### `sec_p6_privacy_review`

- Family: `security_appsec`
- Gold skill: `privacy-risk-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `security-threat-modeler` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.40, output artifact=0.13, workflow=0.09, success criterion=0.21, dependency/resource=0.33, avoid/not-for boundary=0.04 |
| `secret-leak-scanner` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.00, workflow=0.07, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.24 |
| `auth-flow-reviewer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.42, output artifact=0.10, workflow=0.10, success criterion=0.12, dependency/resource=0.33, avoid/not-for boundary=0.41 |

### `skill_p1_find_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-finder`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-creator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.00, workflow=0.04, success criterion=0.06, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `skill-installer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.00, workflow=0.09, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `skill-editor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.38, output artifact=0.04, workflow=0.06, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.13 |

### `skill_p2_install_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-installer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-finder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.00, workflow=0.09, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `skill-creator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.49, output artifact=0.00, workflow=0.04, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `skill-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.45, output artifact=0.00, workflow=0.10, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.14 |

### `skill_p3_create_new`

- Family: `skill_lifecycle`
- Gold skill: `skill-creator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-editor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.09, workflow=0.14, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.36 |
| `skill-finder` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.44, output artifact=0.00, workflow=0.04, success criterion=0.06, dependency/resource=1.00, avoid/not-for boundary=0.21 |
| `skill-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.49, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.10 |

### `skill_p4_edit_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-editor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-creator` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.41, output artifact=0.09, workflow=0.14, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.36 |
| `skill-evaluator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.42, output artifact=0.00, workflow=0.08, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.10 |
| `skill-packager` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.04, workflow=0.04, success criterion=0.06, dependency/resource=0.00, avoid/not-for boundary=0.07 |

### `skill_p5_evaluate_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-evaluator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-editor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.42, output artifact=0.00, workflow=0.08, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.10 |
| `skill-finder` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.49, output artifact=0.10, workflow=0.02, success criterion=0.09, dependency/resource=0.00, avoid/not-for boundary=0.46 |
| `skill-creator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.50, output artifact=0.04, workflow=0.08, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.15 |

### `skill_p6_package_existing`

- Family: `skill_lifecycle`
- Gold skill: `skill-packager`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-creator` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.49, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.10 |
| `skill-installer` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.45, output artifact=0.00, workflow=0.10, success criterion=0.07, dependency/resource=0.00, avoid/not-for boundary=0.14 |
| `skill-editor` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.39, output artifact=0.04, workflow=0.04, success criterion=0.06, dependency/resource=0.00, avoid/not-for boundary=0.07 |

### `skill_representation_analysis_p1_skill_field_auditor`

- Family: `skill_representation_analysis`
- Gold skill: `skill-field-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-authoring-guide` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `skill-router-policy-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.27 |
| `skill-hierarchy-flattener` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.46 |
| `skill-installer-wrapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |

### `skill_representation_analysis_p2_skill_authoring_guide`

- Family: `skill_representation_analysis`
- Gold skill: `skill-authoring-guide`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `skill-router-policy-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `skill-hierarchy-flattener` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.09, workflow=0.10, success criterion=0.25, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `skill-installer-wrapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.56 |

### `skill_representation_analysis_p3_skill_router_policy_designer`

- Family: `skill_representation_analysis`
- Gold skill: `skill-router-policy-designer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.04, success criterion=0.09, dependency/resource=1.00, avoid/not-for boundary=0.27 |
| `skill-authoring-guide` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `skill-hierarchy-flattener` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `skill-installer-wrapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.09 |

### `skill_representation_analysis_p4_skill_hierarchy_flattener`

- Family: `skill_representation_analysis`
- Gold skill: `skill-hierarchy-flattener`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.46 |
| `skill-authoring-guide` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.09, workflow=0.10, success criterion=0.25, dependency/resource=1.00, avoid/not-for boundary=0.07 |
| `skill-router-policy-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.17 |
| `skill-installer-wrapper` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.08 |

### `skill_representation_analysis_p5_skill_installer_wrapper`

- Family: `skill_representation_analysis`
- Gold skill: `skill-installer-wrapper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `skill-authoring-guide` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.56 |
| `skill-router-policy-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `skill-hierarchy-flattener` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.04, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.08 |

### `skill_representation_analysis_p6_skill_benchmark_evaluator`

- Family: `skill_representation_analysis`
- Gold skill: `skill-benchmark-evaluator`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `skill-field-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.09, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.15 |
| `skill-authoring-guide` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.15 |
| `skill-router-policy-designer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.08, workflow=0.00, success criterion=0.04, dependency/resource=1.00, avoid/not-for boundary=0.44 |
| `skill-hierarchy-flattener` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.07 |

