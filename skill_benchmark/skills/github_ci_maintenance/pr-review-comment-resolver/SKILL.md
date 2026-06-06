---
name: pr-review-comment-resolver
description: "Turns pull request review comments into specific code changes, reply points, and verification steps."
---

# Pr Review Comment Resolver

Acts on reviewer feedback rather than conducting a fresh review.

## Use when

- The user provides PR review comments.
- The task is to resolve requested changes and prepare replies.

## Not for

- Finding CI root cause.
- Writing changelog entries.
- Installing git safety hooks.

## Preconditions

- Review comments and relevant code context are available.
- The user wants implementation or response planning.

## Workflow

1. Group comments by required change.
2. Map each comment to file/code action.
3. Identify disagreements or questions.
4. Return patch plan and response summary.

## Writing rules

- Do not ignore unresolved reviewer requests.
- Separate actioned comments from clarification needed.

## Default shape

- Comment
- Required action
- Verification
- Reply
