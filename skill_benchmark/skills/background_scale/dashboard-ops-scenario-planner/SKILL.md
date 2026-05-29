---
name: dashboard-ops-scenario-planner
description: Plans alternative scenarios for dashboard and metric reporting decisions under changing assumptions, constraints, or risks.
---

# Dashboard Ops Scenario Planner

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
- scenario planner

## Use when

- The user wants scenario planning for dashboard and metric reporting rather than a single recommendation.
- Key assumptions, decision options, or uncertainty drivers are available.
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

Scenario table with assumptions, expected outcomes, risks, and decision triggers.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
