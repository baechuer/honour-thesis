---
name: agent-ops-quality-auditor
description: Audits agent and skill operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Agent Ops Quality Auditor

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

agent and skill operations procedure over agent traces, tool specs, skill cards, evaluation notes; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Resource And Structure Signals

- skills
- tools
- routing
- traces
- evaluation
- quality auditor

## Use when

- The user wants quality assurance over agent traces, tool specs, skill cards, evaluation notes before the artifact is used downstream.
- Expected quality criteria or artifact shape is available.
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

Quality findings, missing elements, inconsistent details, and correction checklist.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
