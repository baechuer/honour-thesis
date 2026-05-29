---
name: iot-ops-priority-ranker
description: Ranks IoT operations items by urgency, impact, effort, dependency, evidence strength, or stakeholder importance.
---

# Iot Ops Priority Ranker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

IoT operations procedure over device telemetry, firmware note, sensor log, provisioning record; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Resource And Structure Signals

- devices
- telemetry
- firmware
- sensors
- provisioning
- priority ranker

## Use when

- The user wants prioritization among candidate IoT operations items rather than a summary.
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
