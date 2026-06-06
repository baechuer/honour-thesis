---
name: psc-repo-guardrail-hook-installer
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Set up repository guardrails such as pre-commit hooks, protected commands, secret checks, and verification commands."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Repo Guardrail Hook Installer

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

## When to use

Use when the output is workflow safety configuration rather than analysis of a current failure.

## Requirements

- Repository tooling
- Risky operations to block
- Verification commands

## Instructions

- Choose hook or guardrail mechanism.
- Define blocked operations and checks.
- Document bypass/maintenance policy.
- Verify with safe dry runs.

## Deliverables

- Hook/config plan
- Blocked actions
- Verification
- Maintenance notes

## When not to use

Not for analyzing CI logs or writing release notes.

## External dependencies to preserve

- Git hooks, Husky, pre-commit, or local command wrapper

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
