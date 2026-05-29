---
name: product-ops-dependency-mapper
description: Maps dependencies, prerequisites, resources, owners, and downstream effects in product management operations work.
---

# Product Ops Dependency Mapper

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

product management operations procedure over feature brief, roadmap item, user feedback, acceptance criteria; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- feature brief
- user feedback
- roadmap context
- acceptance criteria
- task-specific constraints

## Resource And Structure Signals

- features
- roadmap
- users
- acceptance criteria
- priorities
- dependency mapper

## Use when

- The user wants dependency structure rather than content summarization.
- Inputs mention resources, owners, tools, dates, systems, or prerequisite actions.
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

Dependency map with prerequisite, dependent item, owner, and risk notes.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
