---
name: database-migration-risk-assessor
description: "Assesses database migration plans for locking, data backfill, compatibility, rollback, deployment ordering, and verification risk."
---

# Database Migration Risk Assessor

Reviews schema/data changes as operational rollout risks.

## Use when

- The user provides a migration file, schema change, rollout plan, or backfill task.
- The concern is production safety, locking, rollback, compatibility, or verification.
- The output should be migration risk findings and a safer rollout plan.

## Not for

- General service architecture review.
- OpenAPI contract documentation review.
- External API integration planning.

## Preconditions

- Migration SQL, ORM migration, schema diff, or rollout notes are available.
- Database type, table size, or deployment constraints are stated or inferable.
- The user needs risk assessment before applying the change.

## Workflow

1. Identify schema changes, data changes, indexes, constraints, and backfills.
2. Check locking, long-running operations, compatibility with old and new app versions, and rollback path.
3. Plan deployment ordering and feature-flag or dual-write needs.
4. Define verification queries and failure recovery steps.
5. Return a risk-ranked rollout recommendation.

## Writing rules

- Do not assume migrations are safe because they are syntactically valid.
- Separate pre-deploy, deploy, backfill, and post-deploy checks.
- Call out missing production-size or database-engine context.

## Default shape

- Migration element
- Risk
- Why it matters
- Safer rollout or verification
