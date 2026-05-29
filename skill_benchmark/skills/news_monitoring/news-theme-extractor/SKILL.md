---
name: news-theme-extractor
description: Extracts recurring themes, topics, and patterns across provided news items. Use when the user wants to know what topics are appearing across multiple sources rather than a single-source summary or a full briefing.
---

# News Theme Extractor

Finds recurring topics and patterns across provided news items.

## Use when

- The user provides multiple news items, excerpts, or links.
- The main task is to identify common topics or repeated signals.
- The output should emphasize themes rather than a narrative recap.

## Not for

- Summarizing a single article in straightforward form.
- Writing a briefing with a strong narrative arc.
- Extracting only source-grounded factual claims.
- Making a stronger trend judgment about what is durable, hype-driven, or strategically important.

## Preconditions

- The user provides one or more news items, snippets, articles, or source summaries.
- The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.

## Workflow

1. Review the provided items together rather than one by one in isolation.
2. Identify repeated topics, actors, events, or concerns.
3. Group related observations into themes.
4. Distinguish major themes from minor noise.
5. Present the themes in a compact, clear list.

## Output pattern

- Recurring themes or topics across sources.
- Evidence snippets for each theme.
- Scope limits or weak signals.

## Writing rules

- Prefer cross-source patterns over article-by-article recap.
- Make the grouping logic clear.
- Avoid overstating a theme if it is weakly supported.
- Return only the extracted themes unless the user asks for further commentary.
