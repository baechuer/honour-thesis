---
name: facilities-ops-timeline-builder
description: Builds a timeline for facilities operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Facilities Ops Timeline Builder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

facilities operations procedure over maintenance request, space plan, safety report, vendor schedule; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- facility map
- maintenance log
- safety policy
- vendor contact
- task-specific constraints

## Resource And Structure Signals

- maintenance
- facility
- space
- safety
- vendor
- timeline builder

## Use when

- The user wants sequence reconstruction or schedule structure from maintenance request, space plan, safety report, vendor schedule.
- The source contains dates, order cues, event descriptions, or dependency markers.
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

Timeline with dates, event descriptions, dependencies, and unresolved gaps.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
