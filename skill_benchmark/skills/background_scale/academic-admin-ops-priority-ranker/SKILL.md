---
name: academic-admin-ops-priority-ranker
description: Ranks academic administration operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Academic Admin Ops Priority Ranker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

academic administration operations procedure over course policy, enrollment note, assessment record, student request; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- institution policy
- student record
- assessment criteria
- deadline
- task-specific constraints

## Resource And Structure Signals

- course
- student
- assessment
- policy
- enrollment
- priority ranker

## Use when

- The user wants prioritization among candidate academic administration operations items rather than a summary.
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
