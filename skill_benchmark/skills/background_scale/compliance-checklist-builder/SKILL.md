---
name: compliance-checklist-builder
description: Creates practical compliance checklists for standards, policies, regulations, audits, or internal governance requirements.
---

# Compliance Checklist Builder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

General background procedure; depends on user-provided task context and the source material named in the request.

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- requested artifact
- input type
- domain-specific constraints

## Use when

- The user wants a checklist for compliance work.
- The user provides enough context to identify the intended input and output artifact.
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

Checklist organized by requirement area.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
