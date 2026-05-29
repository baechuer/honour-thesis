---
name: paper-summariser
description: Summarises an academic paper into a concise research-oriented recap that foregrounds the paper's question, approach, findings, and limits.
---

# Paper Summariser

Summarises an academic paper into a concise research-oriented recap.

## Use when

- The user gives you a paper, preprint, workshop paper, journal article, or thesis chapter and wants to understand it quickly.
- The user wants the source read as a research contribution rather than just a generic piece of text.
- The output should help someone remember what the paper was trying to do, how it did it, what it found, and what its limits are.

## Not for

- Extracting citation-ready notes as the main output.
- Building method-comparison notes.
- Checking whether a claim is grounded by the source.
- Synthesizing multiple sources into related-work prose.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the paper's research question, goal, or contribution.
2. Find the main approach, method, or argument structure.
3. Pull out the most important findings, claims, or results.
4. Note meaningful scope conditions, assumptions, and limitations.
5. Present the paper as a compact research-oriented recap.

## Writing rules

- Center the summary on the paper's contribution and research role.
- Preserve important qualifiers, uncertainty, and limits.
- Keep background detail brief unless it is necessary to understand the contribution.
- Keep the output concise and readable.
- Return only the summary unless the user asks for another format.

## Default shape

Use this shape unless the user asks for something else:

- Research question or goal
- Approach or method
- Main findings
- Important limitations or caveats

## Example patterns

### Example 1

User ask:

`Summarise this paper for me so I can understand the main idea quickly.`

Good output style:

- Research question: what problem the paper is addressing
- Approach: how the authors tackled it
- Main findings: the core result
- Limitations: what to be careful about

### Example 2

User ask:

`Give me a short summary of this paper for my thesis notes.`

Good output style:

- Focus on contribution, method, and result
- Keep the paper framed as research work
- Include at least one limit or scope note when available
