---
name: psc-source-field-table-extractor
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Extract specific fields from sources into a structured table for later comparison or coding."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Source Field Table Extractor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

## When to use

Use when the user wants reusable fields, not prose summary.

## Requirements

- Source text
- Field list or extraction schema
- Need for structured output

## Instructions

- Identify requested fields.
- Extract values with evidence snippets.
- Mark missing or ambiguous fields.
- Return a table.

## Deliverables

- Field-value table
- Evidence snippets
- Missing-field notes

## When not to use

Not for broad synthesis, citation support, or method-only reading unless those are requested fields.

## External dependencies to preserve

- Source text and field schema

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
