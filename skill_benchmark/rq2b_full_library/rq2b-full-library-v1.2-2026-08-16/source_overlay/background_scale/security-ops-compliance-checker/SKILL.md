---
name: security-ops-compliance-checker
description: Checks application security operations material against policy, requirements, acceptance criteria, or required procedure.
---

# Security Ops Compliance Checker

## Use when

- The user wants compliance or requirement fit checked rather than a general review.

## Input and preconditions

- The relevant policy, checklist, acceptance criteria, or rule set is available.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Map the supplied material to the stated policy, rule set, or acceptance criteria.
2. Mark each requirement as met, unmet, unclear, or unsupported.
3. Attach evidence and remediation detail to each failure.
4. Return compliance status and the correction list.

## Output

Compliance status, failed requirements, evidence, and remediation steps.
