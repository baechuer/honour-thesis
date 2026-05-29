---
name: citation-note-extractor
description: Turns a source into concise citation-ready notes that capture useful claims, supporting detail, possible use in writing, and important cautions.
---

# Citation Note Extractor

Builds concise citation-ready notes from a source.

## Use when

- The user is reading for later writing, citation, or literature review work.
- The task is to capture reusable notes rather than produce a full summary.
- The output should help the user remember what the source can support in future writing.

## Not for

- Producing a broad paper summary.
- Comparing methods across papers.
- Checking a user's already-written claim for support.
- Writing related-work prose directly.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the source's most reusable claims, findings, or ideas.
2. Note what kind of point the source could support later.
3. Capture a useful supporting detail, result, or observation.
4. Preserve important limits, qualifiers, and scope conditions.
5. Present the result as compact citation-oriented notes.

## Writing rules

- Prefer reusable notes over long narrative prose.
- Preserve what the source can support and where its limits are.
- Keep notes compact enough to be useful during later writing.
- Return only the notes unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Main point
- Useful supporting detail
- Possible use in writing
- Limitation or caution

For worked examples, see `examples.md`.
