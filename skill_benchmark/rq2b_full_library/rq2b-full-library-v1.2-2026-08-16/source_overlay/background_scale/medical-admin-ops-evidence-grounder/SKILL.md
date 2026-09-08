---
name: medical-admin-ops-evidence-grounder
description: Grounds medical administration operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Medical Admin Ops Evidence Grounder

## Use when

- The user wants claims checked against appointment note, referral text, intake form, clinic instruction rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: appointment note, referral text, intake form, clinic instruction.

## Dependencies and resources

- patient-provided note
- appointment details
- clinic policy
- form fields
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
