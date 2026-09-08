---
name: legal-discovery-ops-evidence-grounder
description: Grounds legal discovery operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Legal Discovery Ops Evidence Grounder

## Use when

- The user wants claims checked against document production, privilege log, deposition note, evidence request rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
