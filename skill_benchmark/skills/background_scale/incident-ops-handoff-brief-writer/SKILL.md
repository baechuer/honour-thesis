---
name: incident-ops-handoff-brief-writer
description: Writes a handoff brief for incident and reliability operations work with context, decisions, constraints, owners, and next actions.
---

# Incident Ops Handoff Brief Writer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

incident and reliability operations procedure over incident timeline, logs, alerts, postmortem notes; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- timeline
- service logs
- alert history
- owner map
- task-specific constraints

## Resource And Structure Signals

- outage
- timeline
- root cause
- mitigation
- follow-up actions
- handoff brief writer

## Use when

- The user wants another person or agent to continue incident and reliability operations work without losing context.
- Current state, unresolved questions, and expected next owner can be identified.
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

Handoff brief with context, completed work, open issues, owner, and acceptance criteria.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
