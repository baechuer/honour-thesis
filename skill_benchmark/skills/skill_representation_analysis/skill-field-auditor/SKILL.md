---
name: skill-field-auditor
description: "Extracts representation fields from existing skills, including triggers, inputs, outputs, workflow, constraints, dependencies, resources, and examples."
---

# Skill Field Auditor

Audits what information a skill artifact contains.

## Use when

- The user provides existing skill files.
- The output should be a field audit or extraction table.

## Not for

- Writing a new skill from scratch.
- Installing a public skill.
- Evaluating retrieval accuracy.

## Preconditions

- One or more skill artifacts are available.
- The target field taxonomy is known.

## Workflow

1. Read each skill artifact.
2. Extract explicit and implicit fields.
3. Mark evidence and confidence.
4. Return structured audit.

## Writing rules

- Do not assume missing fields are present.
- Quote evidence where possible.

## Default shape

- Skill
- Field
- Evidence
- Explicit/implicit/missing
