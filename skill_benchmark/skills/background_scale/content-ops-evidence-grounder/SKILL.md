---
name: content-ops-evidence-grounder
description: Grounds content production operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Content Ops Evidence Grounder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

content production operations procedure over content calendar, draft article, brief, editorial feedback; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- content brief
- brand voice
- publication channel
- editorial criteria
- task-specific constraints

## Resource And Structure Signals

- article
- calendar
- editorial
- brand voice
- draft
- evidence grounder

## Use when

- The user wants claims checked against content calendar, draft article, brief, editorial feedback rather than rewritten or summarized.
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
