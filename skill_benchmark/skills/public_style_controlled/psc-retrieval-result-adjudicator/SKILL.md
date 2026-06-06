---
name: psc-retrieval-result-adjudicator
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Adjudicate skill retrieval results with strict gold labels, acceptable alternatives, failure categories, top-k, MRR, and non-core false positives."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Retrieval Result Adjudicator

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

## When to use

Use after retrieval has already produced rankings and the task is evaluation.

## Requirements

- Prompt/gold set
- Ranked retrieval output
- Acceptable alternative policy

## Instructions

- Score strict and acceptable labels separately.
- Compute top-k and MRR.
- Classify failures by candidate miss, reranker ordering, ambiguity, or better-than-gold.

## Deliverables

- Metrics
- Failure categories
- Adjudication notes
- Revision queue

## When not to use

Not for designing a router policy from scratch or extracting fields from raw skills.

## External dependencies to preserve

- Retrieval result JSON
- Gold labels

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
