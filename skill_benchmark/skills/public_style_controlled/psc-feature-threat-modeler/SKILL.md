---
name: psc-feature-threat-modeler
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Threat-model a planned feature by identifying assets, actors, trust boundaries, abuse cases, and mitigations before implementation."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-security-appsec
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Feature Threat Modeler

## Capability

Threat-model a planned feature by identifying assets, actors, trust boundaries, abuse cases, and mitigations before implementation. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

The important distinction is not just the file type or tool name. Route here when the user is asking for threat model and the request depends on feature design, and actors/assets. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use during design, before code exists or before implementation choices are fixed. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Feature design | Threat model |
| Actors/assets | Abuse cases |
| Trust boundaries or data flows | Mitigations |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Identify assets, actors, boundaries, entry points, and misuse cases.
2. Prioritize threats and mitigations.
3. List assumptions and follow-up checks.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Feature design", "Actors/assets"]
  returns: ["Threat model", "Abuse cases"]
  tools: ["Feature notes or architecture sketch"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include threat model, abuse cases, mitigations, and assumptions when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Threat model
- Abuse cases
- Mitigations
- Assumptions

## Boundaries

Not for reviewing one code handler, dependency supply-chain risk, or data-retention policy. Nearby skills in this cluster include `psc-handler-vulnerability-reviewer`, `psc-dependency-supply-chain-auditor`, `psc-privacy-telemetry-reviewer`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with feature notes or architecture sketch. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Feature design. Actors/assets. Trust boundaries or data flows.

## Samples

- Before building invite-by-link file sharing, map what needs protection, who can interact with it, where control changes hands, how it could be abused, and what safeguards we should add.
- Create a design-stage threat model for the new collaborator-invite feature. I need abuse paths and mitigations, not a code-level vulnerability review.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants threat model or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces threat model.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
