---
name: customer-success-ops-evidence-grounder
description: Grounds customer success operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Customer Success Ops Evidence Grounder

## Use when

- The user wants claims checked against account health note, renewal plan, usage report, success plan rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: account health note, renewal plan, usage report, success plan.

## Dependencies and resources

- account profile
- usage data
- renewal date
- success criteria
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
