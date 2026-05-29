---
name: task-extractor
description: Extracts concrete tasks from rough notes, plans, or mixed text. Use when the user needs actionable tasks identified from unstructured material rather than a meeting-specific summary or a scheduled weekly plan.
---

# Task Extractor

Turns rough notes or mixed text into a clearer task list.

## Use when

- The user has rough notes, bullets, reminders, or mixed text.
- The task is to identify what actions are implied or required.
- The output should be a cleaned-up list of tasks.

## Not for

- Building a week-level schedule or prioritised plan.
- Preparing a meeting agenda.
- Summarising a completed meeting.
- Extracting meeting follow-up items when meeting structure and ownership are the main concern.

## Preconditions

- The user provides notes, obligations, tasks, meeting context, or planning constraints.
- The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.

## Workflow

1. Read the source notes for explicit and implied actions.
2. Separate tasks from background information.
3. Rewrite vague notes into clearer task statements.
4. Preserve known deadlines, dependencies, or constraints.
5. Present a compact task list the user can act on.

## Output pattern

- Actionable task list.
- Owner or context when available.
- Deadline, priority, or missing detail when relevant.

## Writing rules

- Prefer actionable task phrasing.
- Keep related context only when needed to understand the task.
- Do not invent deadlines or owners that are not present.
- Return the task list only unless the user asks for more structure.
