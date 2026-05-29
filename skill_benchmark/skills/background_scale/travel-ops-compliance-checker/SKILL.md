---
name: travel-ops-compliance-checker
description: Checks travel planning operations material against policy, requirements, acceptance criteria, or required procedure.
---

# Travel Ops Compliance Checker

Background scale skill used to create realistic retrieval pressure in the benchmark.

## Dependency Profile

travel planning operations procedure over itinerary, booking email, visa note, travel constraint list; requires preserving the procedure-specific input state and output artifact.

## External Dependencies To Preserve

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Resource And Structure Signals

- itinerary
- booking
- visa
- schedule
- travel risk
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
