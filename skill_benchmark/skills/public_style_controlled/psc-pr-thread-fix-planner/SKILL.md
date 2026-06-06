---
name: psc-pr-thread-fix-planner
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Convert existing pull request review threads into required code changes, response notes, and verification steps."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Pr Thread Fix Planner

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

## When to use

Use when reviewer comments already exist and the task is to address them.

## Requirements

- Review comments or PR threads
- Code context
- Need for response/action mapping

## Instructions

- Group comments by requested change.
- Map each thread to code/test action.
- Separate accepted fixes from clarification questions.
- Prepare response notes.

## Deliverables

- Thread action map
- Patch plan
- Verification
- Reply notes

## When not to use

Not for fresh code review or CI log diagnosis unless those are requested in the comments.

## External dependencies to preserve

- GitHub PR review threads

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
