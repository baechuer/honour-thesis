---
name: source-grounding-extractor
description: Extracts source-grounded claims, facts, and statements from provided news content with explicit linkage to the source material. Use when the user needs grounded information rather than a broader summary or synthesis.
---

# Source Grounding Extractor

Pulls out grounded claims from provided news material.

## Use when

- The user provides one or more news sources.
- The task is to identify what can be directly grounded in the source text.
- The output should preserve provenance rather than broad synthesis.

## Not for

- Writing a readable summary for general consumption.
- Extracting recurring themes across multiple items.
- Writing a short briefing.
- Making trend judgments or strategic interpretations.

## Preconditions

- The user provides one or more news items, snippets, articles, or source summaries.
- The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.

## Workflow

1. Read the provided source carefully for explicit claims and supported facts.
2. Separate grounded claims from interpretation or implication.
3. Extract the most relevant facts, statements, dates, or numbers.
4. Preserve attribution or source linkage where useful.
5. Present the result in a compact grounded format.

## Output pattern

- Grounded claims or facts.
- Source linkage or supporting wording.
- Named entities, figures, plans, and qualifiers.

## Writing rules

- Prefer directly supported claims over inferred conclusions.
- Preserve source uncertainty and attribution.
- Avoid broad interpretive synthesis unless explicitly requested.
- Return the grounded extraction only unless the user asks for more.
