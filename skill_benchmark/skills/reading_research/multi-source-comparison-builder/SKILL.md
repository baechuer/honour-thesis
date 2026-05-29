---
name: multi-source-comparison-builder
description: Compares multiple papers or sources along important dimensions such as methods, findings, assumptions, scope, or evaluation setup.
---

# Multi-Source Comparison Builder

Builds a structured comparison across sources.

## Use when

- The user provides two or more papers or sources.
- The task is to compare them along explicit or implicit dimensions.
- The output should make similarities and differences easy to inspect.

## Not for

- Summarizing one paper.
- Writing polished related-work prose as the main output.
- Extracting citation notes only.
- Checking one claim against one source.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the sources and useful comparison dimensions.
2. Extract comparable information from each source.
3. Align similarities, differences, and gaps.
4. Preserve scope differences, caveats, and incompatible assumptions.
5. Present the result in a structured comparison format.

## Writing rules

- Prefer side-by-side comparability over narrative flow.
- Make the comparison dimensions explicit.
- Preserve meaningful differences instead of smoothing them away.
- Return only the comparison unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Comparison dimensions
- Source A
- Source B
- Similarities
- Differences
- Key takeaway

For worked examples, see `examples.md`.
