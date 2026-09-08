---
name: knowledge-ops-dependency-mapper
description: Maps dependencies, prerequisites, resources, owners, and downstream effects in knowledge management operations work.
---

# Knowledge Ops Dependency Mapper

## Use when

- The user wants dependency structure rather than content summarization.

## Input and preconditions

- Inputs mention resources, owners, tools, dates, systems, or prerequisite actions.
- Relevant material: notes, wiki pages, knowledge base articles, taxonomy.

## Dependencies and resources

- note corpus
- taxonomy
- source links
- owner context
- task-specific constraints

## Procedure

1. Identify prerequisites, dependent items, resources, owners, and downstream effects.
2. Connect each dependency to the evidence that establishes it.
3. Flag cycles, missing owners, and high-risk dependencies.
4. Return the dependency map with risk notes.

## Output

Dependency map with prerequisite, dependent item, owner, and risk notes.
