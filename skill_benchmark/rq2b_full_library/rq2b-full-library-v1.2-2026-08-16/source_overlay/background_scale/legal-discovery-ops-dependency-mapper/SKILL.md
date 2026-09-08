---
name: legal-discovery-ops-dependency-mapper
description: Maps dependencies, prerequisites, resources, owners, and downstream effects in legal discovery operations work.
---

# Legal Discovery Ops Dependency Mapper

## Use when

- The user wants dependency structure rather than content summarization.

## Input and preconditions

- Inputs mention resources, owners, tools, dates, systems, or prerequisite actions.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Identify prerequisites, dependent items, resources, owners, and downstream effects.
2. Connect each dependency to the evidence that establishes it.
3. Flag cycles, missing owners, and high-risk dependencies.
4. Return the dependency map with risk notes.

## Output

Dependency map with prerequisite, dependent item, owner, and risk notes.
