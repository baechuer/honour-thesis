---
name: insurance-ops-evidence-grounder
description: Grounds insurance claims operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Insurance Ops Evidence Grounder

## Use when

- The user wants claims checked against claim form, policy wording, incident evidence, assessor notes rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: claim form, policy wording, incident evidence, assessor notes.

## Dependencies and resources

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
