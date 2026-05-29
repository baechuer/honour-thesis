---
name: web-ops-scenario-planner
description: Plans alternative scenarios for web automation and QA decisions under changing assumptions, constraints, or risks.
---

# Web Ops Scenario Planner

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

web automation and QA procedure over web page, browser state, test flow, screenshot evidence; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Resource And Structure Signals

- DOM
- forms
- screenshots
- interactions
- accessibility
- scenario planner

## Use when

- The user wants scenario planning for web automation and QA rather than a single recommendation.
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
