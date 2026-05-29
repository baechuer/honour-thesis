---
name: security-threat-modeler
description: Builds a security threat model for a feature, architecture, data flow, or system design by identifying assets, trust boundaries, attackers, abuse cases, and mitigations.
---

# Security Threat Modeler

Creates architecture-level security threat models.

## Use when

- The user wants to reason about security risks in a feature, service, architecture, or data flow.
- The task involves pre-implementation assets, trust boundaries, threat actors, abuse paths, mitigations, or residual risk.
- The output is design-level threat modeling for a feature or architecture, not implementation bug finding.
- The output should be a structured threat model rather than a code-level bug review.

## Not for

- Reviewing source code for concrete vulnerabilities.
- Checking dependency or supply-chain risk.
- Looking only for leaked secrets.
- Reviewing privacy compliance as the main task.

## Preconditions

- The user provides a feature design, code path, dependency context, diff, auth flow, logs, or data-handling description.
- The user indicates whether the concern is threat modeling, code vulnerability, dependency risk, secrets, auth, or privacy.

## Workflow

1. Identify the feature, assets, users, external systems, and trust boundaries.
2. Map likely attackers, abuse paths, and security assumptions.
3. Prioritize threats by impact and likelihood.
4. Propose mitigations, detection, and validation checks.
5. State residual risk and open questions.

## Output pattern

- Assets, actors, and trust boundaries.
- Abuse cases and threat scenarios.
- Mitigations, detection, residual risk, and open questions.

## Writing rules

- Keep the analysis grounded in the described system.
- Distinguish design risk from implementation bug.
- Avoid generic security advice when a concrete abuse path is possible.
- Use `references/threat_model_axes.md` for structured coverage when useful.
