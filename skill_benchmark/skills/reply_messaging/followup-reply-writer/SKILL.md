---
name: followup-reply-writer
description: Drafts reply messages that emphasize next actions, commitments, clarifications, or follow-up steps. Use when the main value of the response is to state what will happen next.
---

# Follow-Up Reply Writer

Writes replies whose main value is clear next actions and commitments.

## Use when

- The user needs to reply with what they will do next.
- The response should clarify responsibilities, timing, or follow-up actions.
- The context comes from email, chat, or meeting follow-up.

## Not for

- General replies where no explicit follow-up commitment is needed.
- Pure summarization of a thread.
- Task extraction without drafting a reply.
- Recipient-specific etiquette cases where a more specialized reply skill is clearly better.

## Preconditions

- The user provides message context, recipient context, or an existing draft reply.
- The user indicates whether the goal is a fresh draft, refinement, academic reply, group coordination, or follow-up commitment.

## Workflow

1. Identify what must be confirmed, clarified, or committed to.
2. Extract the next-step content that matters most.
3. Draft a reply that states actions, owners, and timing clearly.
4. Make dependencies or uncertainties explicit when relevant.
5. Keep the message concise and easy for the recipient to act on.

## Output pattern

- Reply message.
- Explicit next action or commitment.
- Timing, clarification, or owner when relevant.

## Writing rules

- Prefer explicit commitments over vague intent.
- Include dates or sequencing when known.
- Do not fabricate certainty if the user has not committed yet.
- Return only the final reply unless the user asks for multiple versions.
