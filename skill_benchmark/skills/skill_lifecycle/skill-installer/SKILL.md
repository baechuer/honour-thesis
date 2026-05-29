---
name: skill-installer
description: Installs or prepares installation of an existing skill from a registry, repository, catalog, or local package into the user's active skill library.
---

# Skill Installer

Installs an existing skill.

## Use when

- The user has identified a skill or source to install.
- The task is to fetch, install, enable, or prepare a skill package.
- The output should report installation status, source, and any setup caveats.

## Not for

- Searching broadly for possible skills without installing.
- Creating a new skill from scratch.
- Editing the contents of an installed skill.
- Evaluating a skill's behavior after installation unless explicitly requested.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Identify the requested skill and installation source.
2. Check whether the skill is already installed or available locally.
3. Install or prepare the skill using the relevant package, registry, or repository path.
4. Verify that the expected skill files are present.
5. Report what changed and any restart or activation step.

## Output pattern

- Installation status.
- Source and installed skill path.
- Verification result and activation caveats.

## Writing rules

- Do not substitute a different skill without saying so.
- Preserve source attribution and version information when available.
- Keep installation separate from skill editing or evaluation.
