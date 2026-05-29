---
name: community-ops-acceptance-test-builder
description: Builds acceptance tests or review checks for community management operations outputs against expected behavior and constraints.
---

# Community Ops Acceptance Test Builder

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

community management operations procedure over forum post, moderation queue, announcement draft, user feedback thread; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- community guidelines
- thread context
- user history
- announcement goal
- task-specific constraints

## Resource And Structure Signals

- posts
- moderation
- announcements
- feedback
- guidelines
- acceptance test builder

## Use when

- The user wants testable checks for community management operations deliverables or workflows.
- Success criteria, expected artifact shape, or user acceptance conditions are available.
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

Acceptance tests with inputs, expected results, edge cases, and verification notes.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
