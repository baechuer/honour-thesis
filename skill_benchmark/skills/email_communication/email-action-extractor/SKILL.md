---
name: email-action-extractor
description: Extracts concrete actions, owners, deadlines, and follow-up items from email content or threads. Use when the user needs operational next steps from email rather than a drafted response.
---

# Email Action Extractor

Pulls out actionable next steps from an email or thread.

## Use when

- The user wants to know what needs to be done after reading an email or thread.
- The task is to identify actions, owners, due dates, blockers, or follow-up points.
- The main output should be an action list rather than a drafted email.

## Not for

- Writing a new email.
- Polishing an email draft.
- Producing a narrative summary of a thread when the user mainly needs a recap.
- Replying to the sender.

## Workflow

1. Read the email or thread for explicit and implied requests.
2. Separate informational content from actionable content.
3. Extract actions, owners, deadlines, dependencies, and open questions.
4. Make uncertainty explicit when ownership or timing is unclear.
5. Present the result in a compact, operational form.

## Writing rules

- Prefer concrete actions over generic summaries.
- Distinguish confirmed deadlines from inferred urgency.
- Do not fabricate owners or due dates when they are not present.
- Return the extracted actions only unless the user asks for extra explanation.
