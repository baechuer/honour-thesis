---
name: review-comment-resolver
description: Implements or proposes fixes for existing review comments on code, focusing on satisfying requested changes while preserving the current design.
---

# Review Comment Resolver

Turns review feedback into concrete code changes.

## Use when

- The user has already received review comments or requested changes.
- The task is to address, implement, or respond to those comments.
- The output should be changed code, a resolution plan, or a response explaining how the comment was handled.

## Not for

- Performing a fresh code review from scratch.
- Reviewing an entire pull request without specific comments to address.
- Debugging CI failure logs unless the failure is part of a review comment.
- Writing changelog or release text.

## Preconditions

- The user provides code, a diff, PR context, CI output, review comments, or a completed-change summary.
- The requested artifact is clear: review findings, fixes, debugging notes, changelog text, or release notes.

## Workflow

1. Identify each review comment and the code it refers to.
2. Separate required fixes from optional suggestions or misunderstandings.
3. Modify the smallest relevant code surface.
4. Run or describe focused verification where possible.
5. Summarize how each comment was resolved.

## Output pattern

- Resolved review comments.
- Code changes or proposed fixes.
- Verification performed or still needed.

## Writing rules

- Preserve the existing design unless the comment requires a redesign.
- Do not silently ignore a requested change.
- If a comment is invalid or ambiguous, explain the reason and propose a safe response.
- Keep the final answer focused on resolved comments and tests.
