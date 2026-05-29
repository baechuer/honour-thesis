---
name: course-ops-normalizer
description: Normalizes course and learning operations material into a consistent naming, schema, format, or taxonomy.
---

# Course Ops Normalizer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

course and learning operations procedure over lecture notes, assignment brief, rubric, study material; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- course material
- rubric
- deadline
- learning objective
- task-specific constraints

## Resource And Structure Signals

- assignment
- rubric
- study
- lecture
- feedback
- normalizer

## Use when

- The user wants consistency and canonicalization for lecture notes, assignment brief, rubric, study material.
- There is a target schema, naming convention, taxonomy, or example format.
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

Normalized artifact with mapping from original values to canonical values.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
