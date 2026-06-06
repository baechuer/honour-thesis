---
name: psc-public-skill-atomizer
description: "Skill-library workflow involving skill artifacts, routing, fields, atomization, benchmark results, candidates, and evaluation. Split broad or hierarchical public skills into atomic skill candidates while preserving shared resources and routing boundaries."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_skill_representation
---

# Public Skill Atomizer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Skill-library maintenance where field extraction, atomization, routing policy, and result adjudication are easily conflated.

## When to use

Use when one public skill contains multiple internal workflows or domain branches.

## Requirements

- Broad skill artifact
- Subworkflow boundaries
- Shared resources or links

## Instructions

- Identify internal branches.
- Create atomic child-skill candidates.
- Preserve shared resources and parent links.
- State routing boundaries.

## Deliverables

- Atomic skill list
- Shared resources
- Parent/child mapping
- Boundary notes

## When not to use

Not for simple field extraction or retrieval-result scoring.

## External dependencies to preserve

- Broad skill file and linked resources

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
