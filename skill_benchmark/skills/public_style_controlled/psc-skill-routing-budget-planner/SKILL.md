---
name: psc-skill-routing-budget-planner
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Design candidate-generation, representation, reranking, budget, fallback, and clarification policy for large skill libraries."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Skill Routing Budget Planner

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

## When to use

Use when the requested artifact is a selector or routing policy.

## Requirements

- Skill library scale
- Candidate budget
- Representation/retrieval choices

## Instructions

- Define first-stage retrieval.
- Choose representation fields.
- Set reranking and fallback policy.
- Specify metrics and cost controls.

## Deliverables

- Routing stages
- Budgets
- Representation fields
- Fallback/metrics

## When not to use

Not for auditing one skill's fields or splitting a hierarchical skill.

## External dependencies to preserve

- Skill library inventory or scale assumptions

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
