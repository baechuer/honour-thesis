---
name: psc-citation-claim-support-auditor
description: "Research-reading workflow involving papers, sources, claims, methods, evidence, comparison, synthesis, and thesis writing. Check whether a draft claim is supported by a source and record quoted/paraphrased evidence, caveats, and citation risk."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_research_reading
---

# Citation Claim Support Auditor

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Research reading tasks where summary, method extraction, citation grounding, and synthesis share academic language.

## When to use

Use when the user has a claim and needs to know whether the source supports it.

## Requirements

- Draft claim
- Source text
- Need for support/caveat judgment

## Instructions

- Locate source evidence.
- Judge support strength.
- Identify overclaiming or missing caveats.
- Return safe wording.

## Deliverables

- Support verdict
- Evidence
- Caveat
- Safer wording

## When not to use

Not for summarizing the whole paper or extracting all methods.

## External dependencies to preserve

- Source text and draft claim

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
