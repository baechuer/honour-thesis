---
name: travel-ops-evidence-grounder
description: Grounds travel planning operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Travel Ops Evidence Grounder

## Use when

- The user wants claims checked against itinerary, booking email, visa note, travel constraint list rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: itinerary, booking email, visa note, travel constraint list.

## Dependencies and resources

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
