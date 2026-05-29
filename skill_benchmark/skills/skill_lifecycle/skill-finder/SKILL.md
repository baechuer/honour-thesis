---
name: skill-finder
description: Searches or inspects an existing skill library to determine whether a suitable skill already exists for a user's task before creating or installing anything new.
---

# Skill Finder

Finds an existing skill that may fit a task.

## Use when

- The user asks whether there is already a skill for a workflow or task.
- The goal is discovery, comparison, or shortlisting existing skills.
- The output should identify candidate skills and why they may or may not fit.

## Not for

- Creating a new skill artifact.
- Editing an existing skill.
- Installing a skill from an external source.
- Testing a skill's behavior in depth.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Clarify the task need from the user's request.
2. Search available skill names, descriptions, and relevant bodies when necessary.
3. Shortlist plausible matches and note scope boundaries.
4. Explain whether an existing skill is sufficient or a new skill may be needed.
5. Return candidates with confidence and next step.

## Output pattern

- Candidate existing skills.
- Fit assessment and confidence.
- Recommendation to use, reject, edit, install, or create.

## Writing rules

- Do not create or modify skills during discovery.
- Prefer specific matches over broad nearby skills.
- State when no existing skill is a clean fit.
