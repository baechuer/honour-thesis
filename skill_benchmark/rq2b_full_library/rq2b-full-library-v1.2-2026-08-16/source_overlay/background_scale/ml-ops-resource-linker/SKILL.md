---
name: ml-ops-resource-linker
description: Links machine learning operations work to relevant resources, references, files, systems, or supporting evidence.
---

# Ml Ops Resource Linker

## Use when

- The user wants resource mapping for machine learning operations rather than completing the task itself.

## Input and preconditions

- Candidate resources, references, or system links are available or named.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. Identify resources, references, files, systems, and evidence relevant to the task.
2. Explain the purpose and limits of each selected resource.
3. Associate an owner or usage note where available.
4. Return the resource map.

## Output

Resource map with purpose, relevance, owner, and usage notes.
