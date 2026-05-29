---
name: document-extractor
description: Extracts structured facts, fields, claims, or other targeted information from a source into an explicit, easy-to-scan output.
---

# Document Extractor

Pulls structured information out of a source.

## Use when

- The user wants specific information pulled out rather than a normal recap.
- The task is to identify facts, fields, dates, metrics, entities, claims, sections, datasets, methods, or other targeted elements.
- The output should be more explicit and structured than a summary.

## Not for

- Producing a narrative summary.
- Writing citation-ready notes.
- Focusing only on method comparison.
- Synthesizing related work prose.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the kind of information the user needs.
2. Read the source for explicit, relevant material.
3. Separate extracted information from background narrative.
4. Preserve uncertainty when the source is incomplete or ambiguous.
5. Present the result in a compact structured form.

## Writing rules

- Prefer explicit extraction over narrative paraphrase.
- Do not invent missing fields or values.
- Keep the output easy to scan.
- Return only the extracted information unless the user asks for explanation.

## Default shape

Use this shape unless the user asks for something else:

- Field or category
- Extracted value or content
- Source wording or qualifier if needed

## Example patterns

### Example 1

User ask:

`Extract the datasets, evaluation metrics, and limitations from this paper.`

Good output style:

- Datasets
- Evaluation metrics
- Limitations

### Example 2

User ask:

`Pull out the key claims and named systems from this report.`

Good output style:

- Claims
- Named systems
- Important qualifiers
