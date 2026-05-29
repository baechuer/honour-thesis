---
name: service-dependency-mapper
description: "Maps service dependencies, upstream and downstream calls, owners, data contracts, failure modes, and operational handoff points."
---

# Service Dependency Mapper

Creates a dependency view of a system rather than evaluating one API or migration.

## Use when

- The user wants to understand service dependencies, owners, call paths, or failure propagation.
- The task involves multiple services, queues, APIs, databases, or external systems.
- The output should be a dependency map with risks and evidence gaps.

## Not for

- Designing one webhook receiver contract.
- Reviewing one OpenAPI spec for schema correctness.
- Auditing one database migration.

## Preconditions

- Service names, architecture notes, traces, logs, or repository evidence are available.
- The user wants system relationships rather than a single component fix.
- Owners, call directions, or data contracts can be identified or marked unknown.

## Workflow

1. Identify services, data stores, queues, APIs, and external dependencies.
2. Map upstream/downstream relationships and ownership.
3. Record data contracts, critical paths, failure modes, and missing evidence.
4. Highlight dependency risks and coordination points.
5. Return a compact map and next evidence to collect.

## Writing rules

- Do not invent dependency edges without evidence.
- Mark unknown owners or contracts explicitly.
- Keep the map operationally useful for planning or incident response.

## Default shape

- Dependency edge
- Owner or contract
- Failure mode
- Evidence or follow-up
