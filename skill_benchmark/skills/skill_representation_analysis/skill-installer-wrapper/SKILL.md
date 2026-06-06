---
name: skill-installer-wrapper
description: "Installs public skills into a local skill directory, preserving source metadata, files, resources, and compatibility checks."
---

# Skill Installer Wrapper

Moves a public skill into the local library.

## Use when

- The user provides a public skill source or repository.
- The output is an installed skill with import metadata and compatibility notes.

## Not for

- Auditing fields without installing.
- Designing router policy.
- Evaluating benchmark accuracy.

## Preconditions

- Source URL/path and target skill directory are known.
- Licensing/tool assumptions or compatibility need checking.

## Workflow

1. Inspect source layout.
2. Copy skill files and resources.
3. Record source metadata.
4. Check compatibility and missing dependencies.

## Writing rules

- Do not silently drop resources.
- Keep source provenance.

## Default shape

- Installed path
- Copied files
- Source metadata
- Compatibility notes
