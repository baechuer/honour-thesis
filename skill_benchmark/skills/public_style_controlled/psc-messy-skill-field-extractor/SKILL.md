---
name: psc-messy-skill-field-extractor
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Extract triggers, inputs, outputs, workflow, dependencies, resources, examples, and boundaries from messy public-style skill files."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Messy Skill Field Extractor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

## When to use

Use when the source is an existing skill artifact and the output is a field audit.

## Requirements

- One or more skill files
- Field taxonomy
- Need for evidence spans

## Instructions

- Read the raw skill body.
- Extract explicit and implicit fields.
- Quote evidence and mark missing fields.
- Separate artifact fields from inferred selector fields.

## Deliverables

- Field audit
- Evidence spans
- Explicit/implicit/missing labels

## When not to use

Not for authoring a new skill, installing a package, or evaluating retrieval results.

## External dependencies to preserve

- Raw skill artifacts

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
