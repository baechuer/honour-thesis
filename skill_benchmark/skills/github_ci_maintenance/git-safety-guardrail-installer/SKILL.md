---
name: git-safety-guardrail-installer
description: "Configures repository hooks or guardrails that prevent dangerous git operations, secret commits, or unsafe workflow commands."
---

# Git Safety Guardrail Installer

Adds workflow safety controls to a repository.

## Use when

- The user wants hooks or safeguards against risky git commands.
- The output is a guardrail setup plan or config.

## Not for

- Writing changelogs.
- Reviewing code.
- Triaging issues.

## Preconditions

- Repository tooling and desired blocked operations are known.
- The user accepts local workflow configuration changes.

## Workflow

1. Identify risky operations and repo tooling.
2. Choose hook/guardrail mechanism.
3. Define blocked commands or secret checks.
4. Return setup and verification commands.

## Writing rules

- Do not install destructive guardrails without explaining impact.
- Keep bypass procedure explicit.

## Default shape

- Guardrail
- Config/action
- Verification
- Bypass or maintenance note
