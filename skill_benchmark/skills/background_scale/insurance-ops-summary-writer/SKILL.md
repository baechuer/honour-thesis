---
name: insurance-ops-summary-writer
description: Summarizes insurance claims operations material into concise takeaways, decisions, open questions, and evidence limits.
---

# Insurance Ops Summary Writer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

insurance claims operations procedure over claim form, policy wording, incident evidence, assessor notes; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Resource And Structure Signals

- claims
- coverage
- policy
- evidence
- settlement
- summary writer

## Use when

- The user wants a readable summary of claim form, policy wording, incident evidence, assessor notes rather than structured extraction.
- The source is long enough that condensation is useful and the audience is known.
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

Concise summary with key points, caveats, and action-relevant details.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
