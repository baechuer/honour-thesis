---
name: tech-news-trend-extractor
description: Synthesises provided technology news into emerging trends, hot topics, and likely signal strength. Use when the user wants to know what appears to be gaining momentum across tech news rather than just what each source says.
---

# Tech News Trend Extractor

Turns provided technology news into a trend-oriented view.

## Use when

- The user provides one or more technology news items or excerpts.
- The main task is to identify what appears to be hot, emerging, or repeatedly signaled.
- The output should go beyond summary into trend-level interpretation.

## Not for

- Summarizing a single source in a straightforward way.
- Extracting themes without judging trend strength.
- Extracting only grounded claims.
- Writing a general-purpose briefing without explicit trend emphasis.

## Preconditions

- The user provides one or more news items, snippets, articles, or source summaries.
- The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.

## Workflow

1. Review the provided items for repeated technologies, companies, launches, concerns, or shifts.
2. Identify candidate trends or hot topics.
3. Distinguish stronger signals from one-off items or hype.
4. Explain why a topic appears meaningful now.
5. Present the result as trend candidates with a brief judgment of strength or uncertainty.

## Writing rules

- Make clear what is observed versus inferred.
- Avoid claiming long-term significance without enough support.
- Prefer trend candidates, signals, and watch-points over overconfident predictions.
- Return only the trend-oriented synthesis unless the user asks for more.

## Output pattern

Use this shape unless the user asks for another format:

- Emerging topic
- Supporting signals from the provided sources
- Why it may matter
- Signal strength: strong / medium / weak
- Caution or uncertainty

## Examples

For concrete input/output examples, see [examples.md](examples.md).
