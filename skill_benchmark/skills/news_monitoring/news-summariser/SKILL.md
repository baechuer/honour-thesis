---
name: news-summariser
description: Summarises provided news content into the main points of the source. Use when the user wants a straightforward recap of one or more news items without theme clustering, briefing structure, or trend inference.
---

# News Summariser

Summarises provided news content into a concise recap.

## Use when

- The user provides a news article, excerpt, transcript, or a small set of news items.
- The main task is to explain what the source says.
- The output should stay close to the source content.

## Not for

- Writing a briefing-style synthesis.
- Producing a decision memo for situation awareness with current state of play, significance now, affected parties, and follow-up signals.
- Extracting themes across multiple news items.
- Extracting only source-grounded claims with explicit provenance.
- Deciding whether something represents a broader trend.

## Preconditions

- The user provides one or more news items, snippets, articles, or source summaries.
- The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.

## Workflow

1. Identify the core event, announcement, or update.
2. Extract the main points from the provided material.
3. Remove repetition and side detail.
4. Preserve important qualifiers, dates, and uncertainty.
5. Return a concise summary of the source.

## Output pattern

- Straightforward recap of the source.
- Main announcement or event.
- Important supporting details and caveats.

## Writing rules

- Stay close to what the provided source actually says.
- Do not infer broader trend implications unless asked.
- Keep the output concise and readable.
- Return only the summary unless the user asks for another format.
