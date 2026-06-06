---
name: psc-privacy-telemetry-reviewer
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Review data collection or telemetry plans for privacy, retention, minimization, consent, re-identification, and compliance concerns."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Privacy Telemetry Reviewer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

## When to use

Use when the risk is personal data handling rather than code exploitability.

## Requirements

- Data fields to collect
- Retention/sharing plan
- Purpose and user context

## Instructions

- Classify data sensitivity.
- Check minimization, retention, consent, access, and re-identification risk.
- Recommend safer collection boundaries.

## Deliverables

- Privacy risks
- Data-field table
- Mitigations
- Retention/access notes

## When not to use

Not for generic security threat modeling or dependency risk.

## External dependencies to preserve

- Telemetry/data-flow description

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
