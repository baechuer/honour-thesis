---
name: psc-ci-log-first-failure-reader
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Read CI logs to find the first meaningful failure, likely root cause, minimal fix, and rerun path."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Ci Log First Failure Reader

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

## When to use

Use when the starting artifact is a failed build or test log.

## Requirements

- Failed job output
- Need for first meaningful error
- Rerun or fix sequence

## Instructions

- Ignore cascading failures until the first root error is found.
- Quote log evidence.
- Map the error to dependency, config, test, or code cause.

## Deliverables

- Failing job
- Root-cause hypothesis
- Evidence
- Fix/rerun plan

## When not to use

Not a fresh code review, PR-comment resolver, or changelog writer.

## External dependencies to preserve

- CI logs
- GitHub Actions or equivalent CI

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
