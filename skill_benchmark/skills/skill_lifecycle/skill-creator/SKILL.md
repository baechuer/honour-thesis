---
name: skill-creator
description: Creates a new atomic skill artifact for a repeated workflow, including a focused SKILL.md, clear trigger description, workflow, boundaries, and optional supporting resources.
---

# Skill Creator

Creates a new skill artifact.

## Use when

- The user wants to create a new skill for a repeated workflow or missing capability.
- No existing skill is sufficient for the task.
- The output should be a new skill folder or a complete proposed skill design.

## Not for

- Finding whether an existing skill already fits.
- Shortlisting existing capability entries, assessing fit and confidence, and recommending reuse without creating a new artifact.
- Installing a prebuilt skill from a registry.
- Making small edits to an existing skill.
- Testing an existing skill without creating a new one.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Identify the repeated workflow, trigger conditions, and expected output.
2. Decide the skill's atomic scope and boundaries.
3. Write a concise description that helps future selection.
4. Add workflow steps, constraints, and optional support resources only when useful.
5. Validate that the skill does not hide unrelated internal routing decisions.

## Output pattern

- New skill design or skill folder contents.
- Trigger description, workflow, boundaries, and optional resources.
- Validation notes for atomic scope.

## Writing rules

- Keep the skill atomic and selection-friendly.
- Do not create broad parent skills that route internally to unrelated domains.
- Include "Not for" boundaries when they reduce likely confusion.
- Avoid extra documentation that does not support execution.
