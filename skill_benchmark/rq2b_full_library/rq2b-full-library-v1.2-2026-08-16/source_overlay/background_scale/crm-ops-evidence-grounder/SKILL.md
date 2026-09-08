---
name: crm-ops-evidence-grounder
description: Grounds CRM and sales operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Crm Ops Evidence Grounder

## Use when

- The user wants claims checked against CRM records, account notes, opportunity fields, email history rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: CRM records, account notes, opportunity fields, email history.

## Dependencies and resources

- CRM export
- account stage
- contact fields
- activity history
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
