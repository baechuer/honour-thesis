---
name: procurement-ops-evidence-grounder
description: Grounds procurement operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Procurement Ops Evidence Grounder

## Use when

- The user wants claims checked against purchase request, vendor quote, RFP response, approval note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: purchase request, vendor quote, RFP response, approval note.

## Dependencies and resources

- purchase request
- vendor quote
- budget code
- approval policy
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
