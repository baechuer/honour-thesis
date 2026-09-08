---
name: construction-ops-evidence-grounder
description: Grounds construction project operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Construction Ops Evidence Grounder

## Use when

- The user wants claims checked against site report, change order, drawing register, safety observation rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: site report, change order, drawing register, safety observation.

## Dependencies and resources

- site records
- drawing set
- contract scope
- safety plan
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
