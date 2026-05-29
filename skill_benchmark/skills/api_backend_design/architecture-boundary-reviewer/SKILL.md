---
name: architecture-boundary-reviewer
description: "Reviews backend architecture boundaries, dependency direction, module ownership, service responsibilities, and maintainability risks."
---

# Architecture Boundary Reviewer

Checks whether system structure has clear boundaries and sustainable dependency flow.

## Use when

- The user asks whether modules, services, layers, or architecture patterns are well separated.
- The task involves dependency direction, ownership, coupling, or boundary violations.
- The output should be architecture findings and refactoring recommendations.

## Not for

- Reviewing OpenAPI schema details.
- Planning external API auth and endpoint calls.
- Auditing database migration rollout risk only.

## Preconditions

- A codebase map, architecture summary, module list, or dependency evidence is available.
- The user wants structural feedback, not endpoint contract polish.
- Relevant business/domain responsibilities can be identified.

## Workflow

1. Map modules, services, layers, owners, and dependency direction.
2. Identify boundary leaks, cyclic dependencies, misplaced responsibilities, and coupling hotspots.
3. Relate findings to maintainability, testability, and change risk.
4. Recommend refactoring sequence with verification checks.
5. Call out uncertainties where architecture evidence is incomplete.

## Writing rules

- Avoid pattern name-dropping without evidence.
- Tie each recommendation to a boundary or dependency problem.
- Prefer incremental changes over broad rewrites.

## Default shape

- Boundary or dependency
- Observed risk
- Impact
- Refactoring recommendation
