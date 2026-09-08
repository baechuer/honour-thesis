---
name: repo-ops-rewrite-editor
description: Rewrites repository and engineering workflow text for clarity, audience fit, tone, structure, and constraint preservation.
---

# Repo Ops Rewrite Editor

## Use when

- The user wants improved wording for existing repository and engineering workflow text rather than analysis.

## Input and preconditions

- A draft or source text exists and the desired audience or tone is stated.
- Relevant material: pull request, diff, CI logs, issue description.

## Dependencies and resources

- repository diff
- test output
- issue context
- review policy
- task-specific constraints

## Procedure

1. Identify the intended audience, tone, and non-negotiable constraints in the draft.
2. Revise wording and structure while preserving the source meaning.
3. Check that factual claims and constraints remain intact.
4. Return the revised text and material preservation notes.

## Output

Rewritten text plus a compact list of changed assumptions or preserved constraints.
