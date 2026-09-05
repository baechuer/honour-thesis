---
name: psc-decision-ranking-analyst
description: "Spreadsheet analysis workflow involving CSV data, metrics, data quality, anomalies, decision ranking, reporting, and business interpretation. Rank options for action using criteria, tradeoffs, evidence, constraints, and recommendation confidence."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-data-analysis-intent
metadata:
  source_style: public_style_controlled
  cluster_id: psc_data_analysis_intent
---

# Decision Ranking Analyst

## Capability

Rank options for action using criteria, tradeoffs, evidence, constraints, and recommendation confidence. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Same spreadsheet or dataset, different analytical intent: trust audit, anomaly watchlist, decision ranking, or executive narrative.

The important distinction is not just the file type or tool name. Route here when the user is asking for ranked options and the request depends on candidate options, and decision criteria. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Good fit

Use when the dataset represents alternatives and the output should choose or rank options. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Candidate options | Ranked options |
| Decision criteria | Criteria |
| Constraints and tradeoffs | Recommendation |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Playbook

A normal run is usually:

1. Define criteria.
2. Score and compare options.
3. Explain tradeoffs and uncertainty.
4. Recommend first action.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Candidate options", "Decision criteria"]
  returns: ["Ranked options", "Criteria"]
  tools: ["Option table or decision matrix"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Handoff

The handoff is usually a compact artifact rather than a long essay. Include ranked options, criteria, recommendation, and tradeoffs when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Ranked options
- Criteria
- Recommendation
- Tradeoffs

## Boundaries

Not for general data quality checks or anomaly detection unless those affect the decision. Nearby skills in this cluster include `psc-data-trust-auditor`, `psc-anomaly-watchlist-builder`, `psc-executive-metric-narrator`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Tools and files

This workflow can be carried out with option table or decision matrix. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Candidate options. Decision criteria. Constraints and tradeoffs.

## Samples

- Compare the pilot options and rank which one we should act on first, using cost, impact, risk, confidence, and time-to-value.
- Use the option table to produce a decision ranking with criteria, tradeoffs, and first-choice recommendation. Do not just summarize the dataset.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants ranked options or a neighbouring artifact, then ask one clarifying question if needed.

## Checks

- The response clearly produces ranked options.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
