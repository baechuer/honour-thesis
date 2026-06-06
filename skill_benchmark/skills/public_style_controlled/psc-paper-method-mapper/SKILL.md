---
name: psc-paper-method-mapper
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Extract a paper's method design, data, baselines, experimental setup, assumptions, and evaluation limitations."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Paper Method Mapper

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

## When to use

Use when the user cares about how a paper was carried out rather than only its conclusion.

## Requirements

- Paper or method excerpt
- Need for experiment/setup detail

## Instructions

- Identify method components, data, baselines, metrics, and assumptions.
- Separate reported results from evaluation design.
- List limitations.

## Deliverables

- Method map
- Evaluation setup
- Assumptions
- Limitations

## When not to use

Not a general summary, citation support audit, or multi-paper synthesis.

## External dependencies to preserve

- Paper text

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
