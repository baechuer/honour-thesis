---
name: docs-ops-evidence-grounder
description: Grounds document operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Docs Ops Evidence Grounder

## Use when

- The user wants claims checked against PDF, DOCX, Markdown file, policy draft, extracted text rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: PDF, DOCX, Markdown file, policy draft, extracted text.

## Dependencies and resources

- document file
- layout evidence
- source text
- format target
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
