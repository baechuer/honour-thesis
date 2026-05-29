---
name: course-ops-evidence-grounder
description: Grounds course and learning operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Course Ops Evidence Grounder

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
- evidence grounder

## Use when

- The user wants claims checked against lecture notes, assignment brief, rubric, study material rather than rewritten or summarized.
- Source material is available and claims can be linked to evidence spans.
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

Claim-evidence map with supported, unsupported, and uncertain claims.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
