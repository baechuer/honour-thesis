---
name: course-ops-evidence-grounder
description: Grounds course and learning operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Course Ops Evidence Grounder

## Use when

- The user wants claims checked against lecture notes, assignment brief, rubric, study material rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: lecture notes, assignment brief, rubric, study material.

## Dependencies and resources

- course material
- rubric
- deadline
- learning objective
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
