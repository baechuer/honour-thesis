---
name: risk-ops-quality-auditor
description: Audits risk management operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Risk Ops Quality Auditor

## Use when

- The user wants quality assurance over risk register, control report, incident note, mitigation plan before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: risk register, control report, incident note, mitigation plan.

## Dependencies and resources

- risk taxonomy
- control evidence
- owner map
- impact scale
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
