---
name: meeting-followup-extractor
description: Extracts follow-up actions, owners, deadlines, and next steps from a completed meeting. Use when the user needs an operational action list rather than a narrative summary.
---

# Meeting Follow-Up Extractor

Pulls out concrete next steps from a completed meeting.

## Use when

- The meeting has already happened.
- The user wants to know what needs to happen next.
- The main output should be actions, owners, timing, and dependencies.

## Not for

- Preparing an agenda before the meeting.
- Writing a general summary of the discussion.
- Building a full weekly plan from broader obligations.
- Extracting tasks from unrelated rough notes.

## Preconditions

- The user provides notes, obligations, tasks, meeting context, or planning constraints.
- The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.

## Workflow

1. Read the meeting notes, transcript, or summary for explicit and implied next steps.
2. Separate action items from general discussion.
3. Extract owners, deadlines, dependencies, and open questions.
4. Mark uncertainty clearly when ownership or timing is not explicit.
5. Present the result in a compact, operational form.

## Output pattern

- Follow-up actions.
- Owners, deadlines, and dependencies.
- Open questions and next check-in points.

## Writing rules

- Prefer concrete actions over general observations.
- Distinguish confirmed deadlines from inferred urgency.
- Do not invent owners or due dates.
- Return the extracted follow-up items only unless the user asks for more explanation.
