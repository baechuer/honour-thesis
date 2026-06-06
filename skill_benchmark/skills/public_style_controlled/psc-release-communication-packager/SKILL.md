---
name: psc-release-communication-packager
description: "GitHub repository maintenance workflow involving CI, pull requests, review threads, hooks, releases, changed code, and verification. Turn merged changes into audience-appropriate release notes, changelog sections, upgrade notes, and breaking-change warnings."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_github_maintenance
---

# Release Communication Packager

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: GitHub maintenance where CI failure, review resolution, guardrail installation, and release communication share repository language.

## When to use

Use after changes are merged or ready to ship and the user needs release communication.

## Requirements

- Merged PRs, commits, or change list
- Audience
- Release categories

## Instructions

- Group features, fixes, breaking changes, and migrations.
- Adjust language to user/developer audience.
- Keep implementation details only when useful.

## Deliverables

- Release notes
- Changelog bullets
- Upgrade caveats

## When not to use

Not for code review, review-thread resolution, or CI failure debugging.

## External dependencies to preserve

- Commit or PR summary

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
