---
name: incident-ops-quality-auditor
description: Audits incident and reliability operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Incident Ops Quality Auditor

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
- quality auditor

## Use when

- The user wants quality assurance over incident timeline, logs, alerts, postmortem notes before the artifact is used downstream.
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
