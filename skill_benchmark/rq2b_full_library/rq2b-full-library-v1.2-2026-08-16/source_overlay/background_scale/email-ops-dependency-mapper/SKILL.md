---
name: email-ops-dependency-mapper
description: Maps dependencies, prerequisites, resources, owners, and downstream effects in email and messaging operations work.
---

# Email Ops Dependency Mapper

## Use when

- The user wants dependency structure rather than content summarization.

## Input and preconditions

- Inputs mention resources, owners, tools, dates, systems, or prerequisite actions.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. Identify prerequisites, dependent items, resources, owners, and downstream effects.
2. Connect each dependency to the evidence that establishes it.
3. Flag cycles, missing owners, and high-risk dependencies.
4. Return the dependency map with risk notes.

## Output

Dependency map with prerequisite, dependent item, owner, and risk notes.
