---
name: dashboard-ops-rewrite-editor
description: Rewrites dashboard and metric reporting text for clarity, audience fit, tone, structure, and constraint preservation.
---

# Dashboard Ops Rewrite Editor

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

dashboard and metric reporting procedure over dashboard screenshots, metric tables, alert notes, KPI definitions; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- dashboard export
- metric glossary
- time window
- owner notes
- task-specific constraints

## Resource And Structure Signals

- charts
- KPIs
- alerts
- thresholds
- trend lines
- rewrite editor

## Use when

- The user wants improved wording for existing dashboard and metric reporting text rather than analysis.
- A draft or source text exists and the desired audience or tone is stated.
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

Rewritten text plus a compact list of changed assumptions or preserved constraints.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
