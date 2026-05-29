---
name: construction-ops-monitoring-plan-builder
description: Builds a monitoring plan for construction project operations with signals, thresholds, review cadence, and escalation owners.
---

# Construction Ops Monitoring Plan Builder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

construction project operations procedure over site report, change order, drawing register, safety observation; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- site records
- drawing set
- contract scope
- safety plan
- task-specific constraints

## Resource And Structure Signals

- site
- drawings
- change order
- safety
- schedule
- monitoring plan builder

## Use when

- The user wants ongoing monitoring or follow-up design for construction project operations.
- Relevant signals, owners, and decision thresholds can be defined.
- The task needs this specific procedure rather than a neighboring confusable skill.
- The output should match the expected artifact below.

## Not for

- Replacing a gold-label core benchmark skill when that core skill is procedurally more specific.
- Broad internal routing across unrelated domains.
- Acting on missing context without asking for or identifying the needed input.

## Workflow

1. Identify the user's intended input and desired artifact.
2. Confirm this skill's procedure is the best fit rather than a neighboring skill.
3. Extract the relevant constraints, evidence, or requirements.
4. Produce the expected output in a compact and reusable form.
5. State uncertainty or required follow-up when the input is incomplete.

## Expected output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
