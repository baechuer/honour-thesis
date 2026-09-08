---
name: training-ops-evidence-grounder
description: Grounds training and enablement operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Training Ops Evidence Grounder

## Use when

- The user wants claims checked against training brief, learner feedback, curriculum outline, assessment result rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: training brief, learner feedback, curriculum outline, assessment result.

## Dependencies and resources

- learning objective
- audience profile
- training materials
- assessment rubric
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
