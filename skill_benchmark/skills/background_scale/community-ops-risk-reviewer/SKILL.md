---
name: community-ops-risk-reviewer
description: Reviews community management operations material for operational, compliance, security, quality, or delivery risk.
---

# Community Ops Risk Reviewer

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
- risk reviewer

## Use when

- The user wants risk findings from forum post, moderation queue, announcement draft, user feedback thread rather than extraction or formatting.
- The task includes enough context to identify impact, likelihood, and mitigation.
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

Risk register with severity, evidence, mitigation, and owner questions.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
