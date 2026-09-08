---
name: supply-chain-ops-quality-auditor
description: Audits supply chain operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Supply Chain Ops Quality Auditor

## Use when

- The user wants quality assurance over supplier update, demand forecast, inventory plan, risk note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
