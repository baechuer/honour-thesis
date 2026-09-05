---
name: psc-privacy-telemetry-reviewer
description: "Application-security workflow involving risks, code, features, dependencies, privacy, data handling, and mitigations. Review data collection or telemetry plans for privacy, retention, minimization, consent, re-identification, and compliance concerns."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-security-appsec
metadata:
  source_style: public_style_controlled
  cluster_id: psc_security_appsec
---

# Privacy Telemetry Reviewer

## Capability

Review data collection or telemetry plans for privacy, retention, minimization, consent, re-identification, and compliance concerns. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Security workflows where threat modeling, code review, dependency auditing, and privacy review all look like risk analysis.

The important distinction is not just the file type or tool name. Route here when the user is asking for privacy risks and the request depends on data fields to collect, and retention/sharing plan. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use when the risk is personal data handling rather than code exploitability. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Data fields to collect | Privacy risks |
| Retention/sharing plan | Data-field table |
| Purpose and user context | Mitigations |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Classify data sensitivity.
2. Check minimization, retention, consent, access, and re-identification risk.
3. Recommend safer collection boundaries.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Data fields to collect", "Retention/sharing plan"]
  returns: ["Privacy risks", "Data-field table"]
  tools: ["Telemetry/data-flow description"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include privacy risks, data-field table, mitigations, and retention/access notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Privacy risks
- Data-field table
- Mitigations
- Retention/access notes

## Boundaries

Not for generic security threat modeling or dependency risk. Nearby skills in this cluster include `psc-feature-threat-modeler`, `psc-handler-vulnerability-reviewer`, `psc-dependency-supply-chain-auditor`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with telemetry/data-flow description. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Data fields to collect. Retention/sharing plan. Purpose and user context.

## Samples

- Review the analytics plan that logs search queries, account region, role, clicked filters, and partial email domains for 18 months.
- Assess privacy risk for a telemetry change: data minimization, retention, consent, access controls, and re-identification. Do not focus on code exploits.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants privacy risks or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces privacy risks.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
