---
name: marketing-ops-intake-classifier
description: Classifies marketing campaign operations requests by input type, expected artifact, routing owner, urgency, and missing context.
---

# Marketing Ops Intake Classifier

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

marketing campaign operations procedure over campaign brief, ad copy, audience segment, performance report; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- campaign goal
- audience data
- creative assets
- performance metrics
- task-specific constraints

## Resource And Structure Signals

- campaign
- audience
- copy
- conversion
- creative
- intake classifier

## Use when

- The user needs classification or routing for marketing campaign operations material before deeper work begins.
- There is enough task context to decide category, owner, urgency, and next action.
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

Classification labels, routing decision, missing-context list, and next-step recommendation.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
