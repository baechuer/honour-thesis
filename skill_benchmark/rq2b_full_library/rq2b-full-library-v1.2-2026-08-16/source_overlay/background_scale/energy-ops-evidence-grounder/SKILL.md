---
name: energy-ops-evidence-grounder
description: Grounds energy operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Energy Ops Evidence Grounder

## Use when

- The user wants claims checked against usage report, meter reading, sustainability plan, tariff note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: usage report, meter reading, sustainability plan, tariff note.

## Dependencies and resources

- meter data
- tariff schedule
- facility profile
- sustainability target
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
