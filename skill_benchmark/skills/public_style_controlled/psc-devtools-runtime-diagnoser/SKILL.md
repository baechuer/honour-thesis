---
name: psc-devtools-runtime-diagnoser
description: "Browser quality workflow involving web pages, interactions, screenshots, accessibility, runtime evidence, and regression checks. Diagnose broken web interactions using DOM state, console errors, network requests, screenshots, and runtime clues."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_browser_quality
---

# Devtools Runtime Diagnoser

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Browser tasks where testing, visual inspection, DevTools diagnosis, and accessibility are easy to confuse.

## When to use

Use this when an interaction fails and browser evidence is needed to identify likely cause.

## Requirements

- A target page or flow
- Symptom to reproduce
- Access to browser/runtime evidence

## Instructions

- Reproduce the interaction.
- Collect console, network, DOM, and screenshot evidence.
- Separate UI state, API, timing, and JavaScript failure hypotheses.

## Deliverables

- Reproduction trace
- Evidence packet
- Likely cause
- Verification step

## When not to use

Not just screenshot capture, accessibility review, or a scripted regression suite.

## External dependencies to preserve

- Browser DevTools or equivalent runtime inspector

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
