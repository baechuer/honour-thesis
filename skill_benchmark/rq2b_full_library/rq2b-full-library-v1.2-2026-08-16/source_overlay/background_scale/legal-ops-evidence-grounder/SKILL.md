---
name: legal-ops-evidence-grounder
description: Grounds legal and policy operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Legal Ops Evidence Grounder

## Use when

- The user wants claims checked against policy text, legal memo, contract clause, compliance question rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: policy text, legal memo, contract clause, compliance question.

## Dependencies and resources

- legal text
- jurisdiction note
- policy version
- review purpose
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
