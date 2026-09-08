---
name: risk-ops-evidence-grounder
description: Grounds risk management operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Risk Ops Evidence Grounder

## Use when

- The user wants claims checked against risk register, control report, incident note, mitigation plan rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: risk register, control report, incident note, mitigation plan.

## Dependencies and resources

- risk taxonomy
- control evidence
- owner map
- impact scale
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
