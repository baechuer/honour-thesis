---
name: meeting-ops-artifact-packager
description: Packages meeting and planning operations outputs into a reusable artifact with sections, file naming, dependencies, and delivery notes.
---

# Meeting Ops Artifact Packager

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

meeting and planning operations procedure over meeting transcript, agenda notes, calendar constraints, action list; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- meeting notes
- participant list
- calendar window
- action owners
- task-specific constraints

## Resource And Structure Signals

- agenda
- decisions
- actions
- owners
- timelines
- artifact packager

## Use when

- The user wants a finished deliverable package rather than raw analysis.
- The required output audience, format, and included materials are known.
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

Packaged artifact outline with included files, section order, and delivery checklist.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
