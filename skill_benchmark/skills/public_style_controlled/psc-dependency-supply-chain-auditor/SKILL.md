---
name: psc-dependency-supply-chain-auditor
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Assess third-party dependency risk from package metadata, maintainer signals, install scripts, transitive dependencies, and version history."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Dependency Supply Chain Auditor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

## When to use

Use before adding or upgrading packages where supply-chain risk matters.

## Requirements

- Package name/version or lockfile diff
- Dependency tree
- Risk tolerance

## Instructions

- Check package purpose, maintainers, scripts, permissions, old transitive dependencies, and update cadence.
- Return risk level and mitigation.

## Deliverables

- Dependency risk summary
- Risk evidence
- Mitigation or alternative

## When not to use

Not for reviewing first-party code logic or privacy data collection.

## External dependencies to preserve

- Package registry, lockfile, dependency tree

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
