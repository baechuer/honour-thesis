---
name: platform-ops-risk-reviewer
description: Reviews platform engineering operations material for operational, compliance, security, quality, or delivery risk.
---

# Platform Ops Risk Reviewer

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

platform engineering operations procedure over developer platform request, service catalog, template repo, platform metric; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Resource And Structure Signals

- platform
- templates
- developer workflow
- service catalog
- self-service
- risk reviewer

## Use when

- The user wants risk findings from developer platform request, service catalog, template repo, platform metric rather than extraction or formatting.
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
