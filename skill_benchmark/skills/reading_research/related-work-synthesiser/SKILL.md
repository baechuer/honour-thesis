---
name: related-work-synthesiser
description: Synthesises multiple papers or sources into a related-work style overview with themes, contrasts, gaps, and open questions.
---

# Related Work Synthesiser

Builds a narrative synthesis across multiple sources.

## Use when

- The user provides multiple papers or sources.
- The goal is to explain how the sources relate to each other.
- The output should read like a related-work or literature-review style synthesis.

## Not for

- Summarizing one source in isolation.
- Extracting fields or citation notes only.
- Producing side-by-side comparison table as the main output.
- Checking a single claim's source support.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the shared topic, problem, or framing connecting the sources.
2. Group the sources into themes, approaches, or positions.
3. Highlight similarities, contrasts, and tensions across the set.
4. Note gaps, limitations, or unresolved questions.
5. Present the result as a coherent synthesis rather than isolated mini-summaries.

## Writing rules

- Prioritise synthesis over article-by-article recap.
- Make thematic structure visible.
- Preserve meaningful disagreement, scope differences, and uncertainty.
- Return only the synthesis unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Main theme or framing
- Supporting source groupings or positions
- Key contrast or tension
- Gap, limitation, or open question

For worked examples, see `examples.md`.
