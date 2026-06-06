# Representation Coverage Report

This report checks whether exported representation fields are populated enough to support the benchmark methodology rubric.

- Skills in structured export: 2433
- Main evaluated skills: 169
- Background/public/support skills: 2264

## Structured Field Coverage

| Field | Main coverage | Threshold | Status |
|---|---:|---:|---|
| `use_when` | 167/169 (98.8%) | 100% | WARN |
| `not_for` | 166/169 (98.2%) | 80% | PASS |
| `preconditions` | 164/169 (97.0%) | 30% | PASS |
| `workflow` | 168/169 (99.4%) | 100% | WARN |
| `output_shape` | 167/169 (98.8%) | 80% | PASS |
| `writing_rules` | 131/169 (77.5%) | 90% | WARN |

## Main Family Coverage

| Family | Skills | Use when | Not for | Workflow | Output |
|---|---:|---:|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| api_mcp_tooling | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| browser_web_automation | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| code_github_workflow | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| data_spreadsheet | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| deployment_browser_qa | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| documents_files | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| github_ci_maintenance | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| huggingface_ml_workflows | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| implicit_field_stress | 10 | 8/10 | 7/10 | 9/10 | 8/10 |
| metrics_observability | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| news_monitoring | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| observability_reliability | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| office_artifact_workflows | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| office_business_automation | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| pdf_document_operations | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| planning_meetings | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| public_style_controlled | 32 | 32/32 | 32/32 | 32/32 | 32/32 |
| reading_research | 8 | 8/8 | 8/8 | 8/8 | 8/8 |
| reply_messaging | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| security_appsec | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| skill_lifecycle | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| skill_representation_analysis | 6 | 6/6 | 6/6 | 6/6 | 6/6 |

## Dependency / Resource Coverage

| Slice | Skills | Dependency signal | Resource signal | Status |
|---|---:|---:|---:|---|
| public imported background | 460 | 460/460 (100.0%) | 460/460 (100.0%) | PASS |
| main tool-heavy clusters | 18 | 9/18 (50.0%) | not required | PASS |

## Graph Edge Coverage

- Skills represented in graph: 2433
- Total edges: 63725

| Edge type | Count |
|---|---:|
| `avoid_when` | 2803 |
| `belongs_to_family` | 2433 |
| `derived_from_public_skill` | 460 |
| `follows_writing_rule` | 4345 |
| `has_precondition` | 5230 |
| `has_resource_signal` | 12017 |
| `has_workflow_step` | 13872 |
| `produces_output` | 2887 |
| `requires_dependency` | 10142 |
| `triggered_by` | 8535 |
| `uses_resource` | 1001 |

## Highest Priority Gaps

| Family | Skill | Missing fields |
|---|---|---|
| implicit_field_stress | `implicit-browser-flow-investigator` | preconditions |
| implicit_field_stress | `implicit-ci-failure-reader` | not_for, preconditions |
| implicit_field_stress | `implicit-hf-local-model-chooser` | not_for, output_shape |
| implicit_field_stress | `implicit-pdf-table-reconstructor` | preconditions |
| implicit_field_stress | `implicit-review-comment-planner` | output_shape, preconditions |
| implicit_field_stress | `implicit-trace-path-diagnoser` | preconditions |
| implicit_field_stress | `implicit-visual-diff-reviewer` | not_for |
