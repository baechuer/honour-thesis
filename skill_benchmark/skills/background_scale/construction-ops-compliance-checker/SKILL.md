---
name: construction-ops-compliance-checker
description: Checks construction project operations material against policy, requirements, acceptance criteria, or required procedure.
---

# Construction Ops Compliance Checker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

construction project operations procedure over site report, change order, drawing register, safety observation; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- site records
- drawing set
- contract scope
- safety plan
- task-specific constraints

## Resource And Structure Signals

- site
- drawings
- change order
- safety
- schedule
- compliance checker

## Use when

- The user wants compliance or requirement fit checked rather than a general review.
- The relevant policy, checklist, acceptance criteria, or rule set is available.
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

Compliance status, failed requirements, evidence, and remediation steps.

## Writing rules

- Keep the result focused on this skill's procedural role.
- Do not silently switch to a more specific benchmark core skill.
- Preserve important caveats and source limits.
