---
name: robotics-ops-evidence-grounder
description: Grounds robotics operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Robotics Ops Evidence Grounder

## Use when

- The user wants claims checked against robot log, mission plan, sensor trace, calibration note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
