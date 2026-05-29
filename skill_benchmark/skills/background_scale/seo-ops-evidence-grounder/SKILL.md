---
name: seo-ops-evidence-grounder
description: Grounds search engine optimization operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Seo Ops Evidence Grounder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

search engine optimization operations procedure over keyword list, page audit, ranking report, content brief; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- target page
- keyword data
- search intent
- ranking baseline
- task-specific constraints

## Resource And Structure Signals

- keywords
- rankings
- content
- search intent
- metadata
- evidence grounder

## Use when

- The user wants claims checked against keyword list, page audit, ranking report, content brief rather than rewritten or summarized.
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
