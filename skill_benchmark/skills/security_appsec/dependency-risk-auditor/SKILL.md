---
name: dependency-risk-auditor
description: Reviews package dependencies, versions, lockfiles, licenses, update history, and supply-chain signals to identify dependency or third-party risk.
---

# Dependency Risk Auditor

Audits dependency and supply-chain risk.

## Use when

- The user asks about package, dependency, library, lockfile, supply-chain, license, or version risk.
- The task is to assess third-party components rather than the user's own code logic.
- The output should explain dependency risk and practical mitigation.

## Not for

- Reviewing application code for vulnerabilities.
- Creating a broad system threat model.
- Scanning only for hardcoded secrets.
- Reviewing privacy risk in data handling as the main task.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Identify direct and relevant transitive dependencies.
2. Check version age, known vulnerabilities, maintenance signals, license concerns, and risky install scripts when information is available.
3. Distinguish confirmed issues from items needing external verification.
4. Prioritize updates, removals, pins, or monitoring actions.
5. Return a risk-focused dependency assessment.

## Output pattern

- Dependency risk assessment.
- Confirmed versus unverified package concerns.
- Recommended update, removal, pinning, or monitoring actions.

## Writing rules

- Do not invent vulnerability IDs.
- Be clear when live vulnerability data is unavailable.
- Prefer specific package-level recommendations.
- Use `references/dependency_risk_axes.md` for a structured audit.
