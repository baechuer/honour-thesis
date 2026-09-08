---
name: real-estate-ops-evidence-grounder
description: Grounds real estate transaction operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Real Estate Ops Evidence Grounder

## Use when

- The user wants claims checked against listing brief, offer terms, inspection note, settlement timeline rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: listing brief, offer terms, inspection note, settlement timeline.

## Dependencies and resources

- listing details
- buyer criteria
- offer terms
- inspection evidence
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
