---
name: accessibility-interaction-auditor
description: "Audits keyboard navigation, focus order, accessible names, ARIA state, contrast clues, and interaction accessibility for a web interface."
---

# Accessibility Interaction Auditor

Checks whether a UI can be operated and understood through accessible interactions.

## Use when

- The user asks about keyboard use, focus traps, screen-reader labels, ARIA state, or interaction accessibility.
- The interface has forms, modals, menus, controls, or dynamic state changes.
- The output should list accessibility barriers and verification steps.

## Not for

- General visual regression comparison.
- Deployment log triage.
- PDF layout review.

## Preconditions

- A target page or UI state is available.
- The relevant controls, flow, or accessibility concern is stated.
- Keyboard, accessibility tree, or DOM evidence can be inspected.

## Workflow

1. Identify the target flow and interactive controls.
2. Check keyboard reachability, focus order, focus visibility, and escape paths.
3. Inspect accessible names, roles, states, labels, and error messages.
4. Assess contrast or visual cues where they affect interaction.
5. Return barriers with concrete verification steps.

## Writing rules

- Tie findings to user tasks, not abstract compliance only.
- Do not conflate visual polish with accessibility failure.
- Include retest instructions for each serious issue.

## Default shape

- Control or flow
- Accessibility issue
- User impact
- Verification and fix
