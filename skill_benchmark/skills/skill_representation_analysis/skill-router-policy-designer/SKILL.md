---
name: skill-router-policy-designer
description: "Designs skill routing policies, candidate-generation stages, reranking rules, budgets, and fallback behavior."
---

# Skill Router Policy Designer

Specifies how a retriever or selector should choose skills.

## Use when

- The user wants a retrieval or routing policy.
- Candidate budgets, stages, and fallback behavior matter.

## Not for

- Writing a single skill file.
- Installing public skills.
- Evaluating a completed benchmark only.

## Preconditions

- Skill library structure and constraints are known.
- Selection policy is the requested artifact.

## Workflow

1. Define candidate generation.
2. Choose representation fields.
3. Specify reranking and fallback.
4. Return routing policy and metrics.

## Writing rules

- Do not collapse retriever and main agent roles.
- Make candidate budget explicit.

## Default shape

- Stages
- Representation fields
- Budgets
- Fallback/metrics
