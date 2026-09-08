---
name: logistics-ops-evidence-grounder
description: Grounds logistics and shipment operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Logistics Ops Evidence Grounder

## Use when

- The user wants claims checked against shipment manifest, tracking update, carrier note, customs form rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: shipment manifest, tracking update, carrier note, customs form.

## Dependencies and resources

- shipment manifest
- carrier data
- delivery window
- customs details
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
