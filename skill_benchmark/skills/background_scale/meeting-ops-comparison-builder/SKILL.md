---
name: meeting-ops-comparison-builder
description: Compares multiple meeting and planning operations items by criteria, differences, conflicts, tradeoffs, and decision relevance.
---

# Meeting Ops Comparison Builder

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
- comparison builder

## Use when

- The user wants comparison across two or more meeting and planning operations sources or options.
- At least two comparable items and evaluation criteria are available.
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

Comparison table with criteria, differences, tradeoffs, and recommendation caveats.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
