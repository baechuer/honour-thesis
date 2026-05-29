# Procedural Distinctness Report

This report implements Step 2 of the benchmark rubric: each gold skill should be procedurally distinguishable from its closest alternatives before we test semantic confusability or retrieval accuracy.

Important interpretation: `not_for` boundaries are treated as supporting evidence, not as a primary reason by themselves. This prevents the benchmark from passing only because a skill contains a negated rule.

## Overall Status

- Step 2 status: **PASS**
- Prompts with at least one primary procedural differentiator for every alternative: 85/85 (100.0%)
- Gold/alternative pairs with at least one primary differentiator: 251/251 (100.0%)
- Gold/alternative pairs with two or more primary differentiators: 251/251 (100.0%)
- Prompts where all listed alternatives differ on two or more primary axes: 85/85 (100.0%)

Pass rule used here: every pair needs at least one primary procedural axis; the benchmark is considered strong when at least 80% of pairs have two or more primary axes.

What this proves: the current controlled skills expose positive procedural differences in their structured fields. What it does not prove yet: that flat metadata, embeddings, tree routing, graph retrieval, or rerankers will recover those differences under semantic similarity and scale. That is tested in later rubric steps.

Why Step 2 was previously unresolved: the coverage report showed that fields existed, but it did not compare each gold skill against its listed near alternatives. This report performs that pair-level check.

## Axis Frequency

| Primary axis | Pair count |
|---|---:|
| input/precondition | 251 |
| output artifact | 251 |
| workflow | 251 |
| success criterion | 251 |
| dependency/resource | 127 |

| Supporting boundary axis | Pair count |
|---|---:|
| avoid/not-for boundary | 251 |

## Family Summary

| Family | Prompts | Prompt pass | Strong prompts | Weak pairs |
|---|---:|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 | 0/21 |
| browser_web_automation | 6 | 6/6 | 6/6 | 0/18 |
| code_github_workflow | 6 | 6/6 | 6/6 | 0/18 |
| data_spreadsheet | 7 | 7/7 | 7/7 | 0/21 |
| deployment_browser_qa | 6 | 6/6 | 6/6 | 0/22 |
| documents_files | 7 | 7/7 | 7/7 | 0/21 |
| metrics_observability | 6 | 6/6 | 6/6 | 0/18 |
| news_monitoring | 5 | 5/5 | 5/5 | 0/10 |
| office_artifact_workflows | 6 | 6/6 | 6/6 | 0/22 |
| planning_meetings | 5 | 5/5 | 5/5 | 0/10 |
| reading_research | 8 | 8/8 | 8/8 | 0/24 |
| reply_messaging | 5 | 5/5 | 5/5 | 0/10 |
| security_appsec | 6 | 6/6 | 6/6 | 0/18 |
| skill_lifecycle | 6 | 6/6 | 6/6 | 0/18 |

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
| `public-office-webhook-automation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-api-design-principles` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

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
| `public-office-database-sync` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-architecture-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `api_p6_service_dependency_map`

- Family: `api_backend_design`
- Gold skill: `service-dependency-mapper`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `architecture-boundary-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.07, workflow=0.11, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `external-api-integration-planner` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.06, workflow=0.05, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.29 |
| `public-architecture-patterns` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-api-design-principles` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.04, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

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
| `public-playwright-interactive` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-playwright` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.02, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p2_visual_regression`

- Family: `deployment_browser_qa`
- Gold skill: `visual-regression-checker`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.07, workflow=0.05, success criterion=0.14, dependency/resource=1.00, avoid/not-for boundary=0.04 |
| `accessibility-interaction-auditor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.07, workflow=0.02, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `public-openai-screenshot` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `deploy_p3_accessibility_interaction`

- Family: `deployment_browser_qa`
- Gold skill: `accessibility-interaction-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `visual-regression-checker` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.07, workflow=0.02, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `playwright-flow-debugger` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.11, output artifact=0.15, workflow=0.08, success criterion=0.11, dependency/resource=1.00, avoid/not-for boundary=0.09 |
| `web-ui-tester` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.16, output artifact=0.00, workflow=0.05, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-anthropic-webapp-testing` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

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
| `public-netlify-deploy` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-openai-vercel-deploy` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

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

### `office_p1_pdf_layout_review`

- Family: `office_artifact_workflows`
- Gold skill: `pdf-layout-reviewer`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-ocr-extractor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.08, output artifact=0.06, workflow=0.04, success criterion=0.05, dependency/resource=1.00, avoid/not-for boundary=0.12 |
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `public-office-pdf-extraction` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-pdf` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

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
| `public-docx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-docx-manipulation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p4_formula_audit`

- Family: `office_artifact_workflows`
- Gold skill: `spreadsheet-formula-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.03, output artifact=0.00, workflow=0.02, success criterion=0.00, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `data-analysis-with-validation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.07, output artifact=0.05, workflow=0.09, success criterion=0.04, dependency/resource=0.00, avoid/not-for boundary=0.04 |
| `public-xlsx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-xlsx-manipulation` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p5_slide_visual_audit`

- Family: `office_artifact_workflows`
- Gold skill: `slide-deck-visual-auditor`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `office-to-markdown-converter` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.07, output artifact=0.00, workflow=0.04, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `pdf-layout-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.06, output artifact=0.13, workflow=0.05, success criterion=0.10, dependency/resource=1.00, avoid/not-for boundary=0.08 |
| `public-pptx` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |
| `public-office-ppt-visual` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.00, output artifact=0.00, workflow=0.00, success criterion=0.00, dependency/resource=0.00, avoid/not-for boundary=0.00 |

### `office_p6_office_to_markdown`

- Family: `office_artifact_workflows`
- Gold skill: `office-to-markdown-converter`
- Status: PASS; strong

| Alternative | Primary axes | Supporting axes | Axis similarities |
|---|---|---|---|
| `pdf-layout-reviewer` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.12, output artifact=0.00, workflow=0.04, success criterion=0.02, dependency/resource=1.00, avoid/not-for boundary=0.00 |
| `docx-redline-editor` | input/precondition, output artifact, workflow, success criterion | avoid/not-for boundary | input/precondition=0.10, output artifact=0.00, workflow=0.09, success criterion=0.03, dependency/resource=1.00, avoid/not-for boundary=0.22 |
| `document-converter` | input/precondition, output artifact, workflow, success criterion, dependency/resource | avoid/not-for boundary | input/precondition=0.13, output artifact=0.00, workflow=0.13, success criterion=0.02, dependency/resource=0.00, avoid/not-for boundary=0.08 |

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

