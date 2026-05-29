---
name: product-ops-priority-ranker
description: Ranks product management operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Product Ops Priority Ranker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

product management operations procedure over feature brief, roadmap item, user feedback, acceptance criteria; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- feature brief
- user feedback
- roadmap context
- acceptance criteria
- task-specific constraints

## Resource And Structure Signals

- features
- roadmap
- users
- acceptance criteria
- priorities
- priority ranker

## Use when

- The user wants prioritization among candidate product management operations items rather than a summary.
- Items and ranking criteria are explicit or inferable from the task context.
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

Ranked list with scoring criteria, rationale, and sensitivity notes.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
