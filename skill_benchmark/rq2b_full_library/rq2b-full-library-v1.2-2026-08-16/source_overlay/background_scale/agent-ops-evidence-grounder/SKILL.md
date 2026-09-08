---
name: agent-ops-evidence-grounder
description: Grounds agent and skill operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Agent Ops Evidence Grounder

## Use when

- The user wants claims checked against agent traces, tool specs, skill cards, evaluation notes rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: agent traces, tool specs, skill cards, evaluation notes.

## Dependencies and resources

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
