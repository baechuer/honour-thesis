---
name: agent-ops-risk-reviewer
description: Reviews agent and skill operations material for operational, compliance, security, quality, or delivery risk.
---

# Agent Ops Risk Reviewer

## Use when

- The user wants risk findings from agent traces, tool specs, skill cards, evaluation notes rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: agent traces, tool specs, skill cards, evaluation notes.

## Dependencies and resources

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
