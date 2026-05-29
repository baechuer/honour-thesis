---
name: thesis-ops-resource-linker
description: Links thesis research operations work to relevant resources, references, files, systems, or supporting evidence.
---

# Thesis Ops Resource Linker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

thesis research operations procedure over thesis notes, supervisor feedback, proposal draft, experiment log; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- research question
- supervisor note
- method plan
- literature notes
- task-specific constraints

## Resource And Structure Signals

- research question
- methodology
- proposal
- evaluation
- timeline
- resource linker

## Use when

- The user wants resource mapping for thesis research operations rather than completing the task itself.
- Candidate resources, references, or system links are available or named.
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

Resource map with purpose, relevance, owner, and usage notes.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
