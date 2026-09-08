---
name: geospatial-ops-evidence-grounder
description: Grounds geospatial analysis operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Geospatial Ops Evidence Grounder

## Use when

- The user wants claims checked against map layer, coordinate table, spatial query, GIS project note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: map layer, coordinate table, spatial query, GIS project note.

## Dependencies and resources

- spatial data
- coordinate reference system
- map layers
- analysis boundary
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
