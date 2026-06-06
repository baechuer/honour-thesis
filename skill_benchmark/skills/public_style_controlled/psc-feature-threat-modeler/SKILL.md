---
name: psc-feature-threat-modeler
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Threat-model a planned feature by identifying assets, actors, trust boundaries, abuse cases, and mitigations before implementation."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Feature Threat Modeler

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

## When to use

Use during design, before code exists or before implementation choices are fixed.

## Requirements

- Feature design
- Actors/assets
- Trust boundaries or data flows

## Instructions

- Identify assets, actors, boundaries, entry points, and misuse cases.
- Prioritize threats and mitigations.
- List assumptions and follow-up checks.

## Deliverables

- Threat model
- Abuse cases
- Mitigations
- Assumptions

## When not to use

Not for reviewing one code handler, dependency supply-chain risk, or data-retention policy.

## External dependencies to preserve

- Feature notes or architecture sketch

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
