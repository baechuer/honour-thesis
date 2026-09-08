---
name: bioinformatics-ops-summary-writer
description: Summarizes bioinformatics operations material into concise takeaways, decisions, open questions, and evidence limits.
---

# Bioinformatics Ops Summary Writer

## Use when

- The user wants a readable summary of sequence file, variant table, pipeline log, sample metadata rather than structured extraction.

## Input and preconditions

- The source is long enough that condensation is useful and the audience is known.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. Read the supplied material for decisions, facts, open questions, and caveats.
2. Group the most consequential points for the named audience.
3. Separate confirmed information from assumptions and gaps.
4. Write a concise summary with action-relevant detail.

## Output

Concise summary with key points, caveats, and action-relevant details.
