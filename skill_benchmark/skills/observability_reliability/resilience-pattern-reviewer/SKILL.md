---
name: resilience-pattern-reviewer
description: "Reviews service code or configuration for retries, timeouts, circuit breakers, fallbacks, backoff, and failure containment."
---

# Resilience Pattern Reviewer

Checks whether service behavior handles failures safely.

## Use when

- The user asks about resilience patterns in code or config.
- Retries, timeouts, fallback, or circuit breakers are relevant.

## Not for

- Investigating trace output.
- Writing SLO narratives.
- Building dashboards.

## Preconditions

- Code/config or architecture notes are available.
- Failure containment is the review objective.

## Workflow

1. Identify external calls and failure modes.
2. Check timeouts/retries/backoff/fallbacks.
3. Assess cascading-failure risk.
4. Return prioritized fixes and tests.

## Writing rules

- Do not recommend infinite retries.
- Tie patterns to concrete failure modes.

## Default shape

- Call/failure mode
- Current risk
- Recommended pattern
- Test
