---
name: web-form-filler
description: Performs step-by-step browser interactions such as filling forms, clicking controls, navigating flows, uploading files, or submitting user-provided input.
---

# Web Form Filler

Carries out browser interactions on behalf of the user.

## Use when

- The user wants a form, checkout, signup, booking, survey, or admin flow completed.
- The task involves controlled data entry: entering provided values, clicking controls, choosing options, or navigating a web flow on the user's behalf.
- The success criterion is completed form progress or a clear stop-before-submit checkpoint, not a pass/fail validation result.
- The output should report what was done and any step that needs user confirmation.

## Not for

- Merely capturing a screenshot or page state.
- Testing whether a UI is correct without actually completing a requested flow.
- Extracting structured data from a page.
- Diagnosing frontend code as the main task.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Identify the target page and the user-provided values or choices.
2. Navigate the flow step by step.
3. Fill only fields that the user has authorized or clearly specified.
4. Pause before irreversible submissions, payments, destructive actions, or sensitive changes.
5. Report completed steps, blockers, and any required confirmation.

## Output pattern

- Completed interaction steps.
- Values entered or choices made.
- Blockers or confirmations required before submission.

## Writing rules

- Do not invent personal data or credentials.
- Do not submit irreversible actions without confirmation.
- Keep the user informed about blockers and required inputs.
- Distinguish successful interaction from validation or test coverage.
