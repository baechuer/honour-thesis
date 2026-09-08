---
name: repo-ops-evidence-grounder
description: Grounds repository and engineering workflow claims in specific evidence snippets, source locations, and confidence notes.
---

# Repo Ops Evidence Grounder

## Use when

- The user wants claims checked against pull request, diff, CI logs, issue description rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: pull request, diff, CI logs, issue description.

## Dependencies and resources

- repository diff
- test output
- issue context
- review policy
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
