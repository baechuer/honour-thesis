---
name: skill-editor
description: Revises an existing skill artifact to improve its description, workflow, boundaries, examples, resources, or selection behavior without creating a new skill.
---

# Skill Editor

Improves an existing skill.

## Use when

- The user wants to update, refine, restructure, or repair an existing skill.
- The task changes the skill's metadata, body, examples, resources, or selection boundaries.
- The output should be an edited skill rather than a newly created skill.

## Not for

- Creating a brand-new skill for a workflow.
- Installing a skill from a registry.
- Merely shortlisting existing capability entries or making a reuse recommendation.
- Evaluating a skill without making or proposing edits.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Read the existing skill's name, description, body, and relevant resources.
2. Identify the selection or execution problem being fixed.
3. Make focused edits to metadata, workflow, boundaries, examples, or resources.
4. Preserve useful existing behavior and avoid broad rewrites.
5. Summarize what changed and why.

## Output pattern

- Edited skill changes.
- Updated metadata, workflow, boundaries, examples, or resources.
- Reason the edit improves selection or execution.

## Writing rules

- Respect existing skill scope unless the user asks to change it.
- Do not silently convert an edit into a new skill.
- Keep descriptions concise but discriminative.
- Keep resource references accurate.
