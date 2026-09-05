---
name: psc-dependency-supply-chain-auditor
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Assess third-party dependency risk from package metadata, maintainer signals, install scripts, transitive dependencies, and version history."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-security-appsec
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Dependency Supply Chain Auditor

## About

Assess third-party dependency risk from package metadata, maintainer signals, install scripts, transitive dependencies, and version history. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

The important distinction is not just the file type or tool name. Route here when the user is asking for dependency risk summary and the request depends on package name/version or lockfile diff, and dependency tree. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Use it for

Use before adding or upgrading packages where supply-chain risk matters. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Package name/version or lockfile diff | Dependency risk summary |
| Dependency tree | Risk evidence |
| Risk tolerance | Mitigation or alternative |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Process

A normal run is usually:

1. Check package purpose, maintainers, scripts, permissions, old transitive dependencies, and update cadence.
2. Return risk level and mitigation.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Package name/version or lockfile diff", "Dependency tree"]
  returns: ["Dependency risk summary", "Risk evidence"]
  tools: ["Package registry, lockfile, dependency tree"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Expected artifacts

The handoff is usually a compact artifact rather than a long essay. Include dependency risk summary, risk evidence, and mitigation or alternative when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Dependency risk summary
- Risk evidence
- Mitigation or alternative

## Do not use for

Not for reviewing first-party code logic or privacy data collection. Nearby skills in this cluster include `psc-feature-threat-modeler`, `psc-handler-vulnerability-reviewer`, `psc-privacy-telemetry-reviewer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Runtime assumptions

This workflow can be carried out with package registry, lockfile, dependency tree. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Package name/version or lockfile diff. Dependency tree. Risk tolerance.

## Examples

- We are about to add an npm package with a postinstall script and many transitive dependencies. Assess the supply-chain risk and mitigation options.
- Audit a third-party dependency before adoption: maintainer health, install scripts, transitive risk, old packages, and safer alternatives.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants dependency risk summary or a neighbouring artifact, then ask one clarifying question if needed.

## Acceptance

- The response clearly produces dependency risk summary.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
