---
name: agent-ops-quality-auditor
description: Audits agent and skill operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Agent Ops Quality Auditor

## Use when

- The user wants quality assurance over agent traces, tool specs, skill cards, evaluation notes before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: agent traces, tool specs, skill cards, evaluation notes.

## Dependencies and resources

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
