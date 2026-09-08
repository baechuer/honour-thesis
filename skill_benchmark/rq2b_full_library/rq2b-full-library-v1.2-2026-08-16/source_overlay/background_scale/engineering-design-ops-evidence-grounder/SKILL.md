---
name: engineering-design-ops-evidence-grounder
description: Grounds engineering design operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Engineering Design Ops Evidence Grounder

## Use when

- The user wants claims checked against design specification, calculation note, review comment, requirement list rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: design specification, calculation note, review comment, requirement list.

## Dependencies and resources

- specification
- requirement set
- calculation record
- review standard
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
