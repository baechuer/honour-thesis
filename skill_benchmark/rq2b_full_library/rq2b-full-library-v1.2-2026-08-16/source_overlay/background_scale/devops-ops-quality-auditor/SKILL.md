---
name: devops-ops-quality-auditor
description: Audits DevOps pipeline operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Devops Ops Quality Auditor

## Use when

- The user wants quality assurance over pipeline log, build script, deploy config, release checklist before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
