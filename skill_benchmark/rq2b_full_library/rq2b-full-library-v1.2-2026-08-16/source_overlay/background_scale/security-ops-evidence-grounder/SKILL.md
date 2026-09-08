---
name: security-ops-evidence-grounder
description: Grounds application security operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Security Ops Evidence Grounder

## Use when

- The user wants claims checked against repository files, threat notes, scan findings, architecture description rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
