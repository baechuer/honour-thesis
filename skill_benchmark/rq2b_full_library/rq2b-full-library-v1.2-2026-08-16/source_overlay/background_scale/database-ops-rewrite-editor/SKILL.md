---
name: database-ops-rewrite-editor
description: Rewrites database operations text for clarity, audience fit, tone, structure, and constraint preservation.
---

# Database Ops Rewrite Editor

## Use when

- The user wants improved wording for existing database operations text rather than analysis.

## Input and preconditions

- A draft or source text exists and the desired audience or tone is stated.
- Relevant material: schema, migration file, query plan, data quality note.

## Dependencies and resources

- database schema
- migration file
- query plan
- data sample
- task-specific constraints

## Procedure

1. Identify the intended audience, tone, and non-negotiable constraints in the draft.
2. Revise wording and structure while preserving the source meaning.
3. Check that factual claims and constraints remain intact.
4. Return the revised text and material preservation notes.

## Output

Rewritten text plus a compact list of changed assumptions or preserved constraints.
