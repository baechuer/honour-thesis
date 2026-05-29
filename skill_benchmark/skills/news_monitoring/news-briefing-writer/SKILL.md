---
name: news-briefing-writer
description: Turns one or more provided news items into a concise briefing with the main developments, why they matter, and the current state of play. Use when the user needs a readable briefing rather than a raw summary, theme list, or source-grounded extraction.
---

# News Briefing Writer

Builds a concise briefing from provided news material.

## Use when

- The user provides one or more news items, links, excerpts, or notes.
- The user wants a short briefing they can read quickly, often with sections such as what happened, why it matters, who is affected, and what to watch next.
- The output should support decision awareness rather than just recap the article chronologically.
- The output should explain the key developments and why they matter.

## Not for

- Summarizing a single source as plainly as possible without briefing structure.
- Extracting only themes across multiple articles.
- Listing only source-grounded claims or facts.
- Judging whether a news topic is an emerging long-term trend.

## Preconditions

- The user provides one or more news items, snippets, articles, or source summaries.
- The user indicates whether they need recap, briefing, grounded facts, themes, or trend signal.

## Workflow

1. Identify the main development or developments across the provided material.
2. Distinguish the most important points from background detail.
3. Explain why the development matters now.
4. Note uncertainty, open questions, or what to watch next if relevant.
5. Present the result in a concise briefing format.

## Writing rules

- Keep the briefing easy to scan.
- Prefer current significance over background detail.
- Preserve important source qualifications and uncertainty.
- Return only the briefing unless the user asks for commentary.

## Output pattern

Use this shape unless the user asks for a different format:

- Headline or topic
- Key development
- Why it matters
- What to watch next

## Examples

For concrete input/output examples, see [examples.md](examples.md).
