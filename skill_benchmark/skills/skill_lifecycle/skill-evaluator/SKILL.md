---
name: skill-evaluator
description: Tests or reviews an existing skill's behavior, trigger description, outputs, and failure modes using realistic tasks before deciding whether to edit or rely on it.
---

# Skill Evaluator

Evaluates whether a skill works as intended.

## Use when

- The user wants to test, audit, benchmark, or compare a skill's behavior.
- The task is to identify whether a skill triggers correctly and produces suitable outputs.
- The output should be an evaluation result, not an immediate edit.

## Not for

- Creating a new skill.
- Installing a skill.
- Editing a skill as the primary task.
- Searching for a skill without testing behavior.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Identify the skill and the expected behavior.
2. Choose realistic test tasks, including near-boundary cases.
3. Inspect trigger fit, workflow fit, output quality, and failure modes.
4. Separate selection problems from execution problems.
5. Return findings and recommend whether editing is needed.

## Output pattern

- Evaluation findings.
- Trigger fit, boundary fit, workflow fit, output fit, and failure modes.
- Recommendation on whether editing is needed.

## Writing rules

- Do not leak the intended answer into evaluation prompts.
- Prefer concrete examples, traces, or outputs over vague judgments.
- Use `references/skill_test_axes.md` when a structured evaluation checklist is useful.
