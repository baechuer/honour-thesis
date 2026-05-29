# Representation Coverage Report

This report checks whether exported representation fields are populated enough to support the benchmark methodology rubric.

- Skills in structured export: 2349
- Main evaluated skills: 85
- Background/public/support skills: 2264

## Structured Field Coverage

| Field | Main coverage | Threshold | Status |
|---|---:|---:|---|
| `use_when` | 85/85 (100.0%) | 100% | PASS |
| `not_for` | 85/85 (100.0%) | 80% | PASS |
| `preconditions` | 85/85 (100.0%) | 30% | PASS |
| `workflow` | 85/85 (100.0%) | 100% | PASS |
| `output_shape` | 85/85 (100.0%) | 80% | PASS |
| `writing_rules` | 85/85 (100.0%) | 90% | PASS |

## Main Family Coverage

| Family | Skills | Use when | Not for | Workflow | Output |
|---|---:|---:|---:|---:|---:|
| api_backend_design | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| browser_web_automation | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| code_github_workflow | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| data_spreadsheet | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| deployment_browser_qa | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| documents_files | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| metrics_observability | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| news_monitoring | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| office_artifact_workflows | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| planning_meetings | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| reading_research | 8 | 8/8 | 8/8 | 8/8 | 8/8 |
| reply_messaging | 5 | 5/5 | 5/5 | 5/5 | 5/5 |
| security_appsec | 6 | 6/6 | 6/6 | 6/6 | 6/6 |
| skill_lifecycle | 6 | 6/6 | 6/6 | 6/6 | 6/6 |

## Dependency / Resource Coverage

| Slice | Skills | Dependency signal | Resource signal | Status |
|---|---:|---:|---:|---|
| public imported background | 460 | 460/460 (100.0%) | 460/460 (100.0%) | PASS |
| main tool-heavy clusters | 18 | 9/18 (50.0%) | not required | PASS |

## Graph Edge Coverage

- Skills represented in graph: 2349
- Total edges: 52205

| Edge type | Count |
|---|---:|
| `avoid_when` | 2148 |
| `belongs_to_family` | 2349 |
| `derived_from_public_skill` | 460 |
| `follows_writing_rule` | 3936 |
| `has_precondition` | 188 |
| `has_resource_signal` | 12017 |
| `has_workflow_step` | 9456 |
| `produces_output` | 2166 |
| `requires_dependency` | 10105 |
| `triggered_by` | 8411 |
| `uses_resource` | 969 |

## Highest Priority Gaps

- No high-priority gaps found.
