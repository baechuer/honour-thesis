---
name: skill-hierarchy-flattener
description: "Converts broad or hierarchical skills into atomic child skills while preserving links, shared resources, and routing boundaries."
---

# Skill Hierarchy Flattener

Atomizes broad skills for evaluation or retrieval.

## Use when

- A skill contains multiple subskills or internal routing.
- The output should be atomic skill definitions.

## Not for

- Installing a skill unchanged.
- Evaluating retrieval results.
- Writing a new unrelated skill.

## Preconditions

- A broad skill or linked-skill set is available.
- Atomic evaluation or retrieval is the target.

## Workflow

1. Identify subprocedures and shared resources.
2. Split into atomic skills.
3. Preserve cross-links and boundaries.
4. Return child skill set.

## Writing rules

- Do not hide domain routing inside one broad skill.
- Keep shared resources referenced explicitly.

## Default shape

- Parent scope
- Child skills
- Shared resources
- Routing boundaries
