---
name: k8s-ops-quality-auditor
description: Audits Kubernetes platform operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# K8s Ops Quality Auditor

## Use when

- The user wants quality assurance over manifest, pod log, deployment event, cluster configuration before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
