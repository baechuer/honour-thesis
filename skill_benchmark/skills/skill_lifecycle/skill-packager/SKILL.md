---
name: skill-packager
description: Prepares an existing skill for sharing, distribution, or reuse by checking required files, metadata, resource references, packaging shape, and portability.
---

# Skill Packager

Packages an existing skill for distribution.

## Use when

- The user wants to package, share, publish, export, or distribute a skill.
- The skill already exists and needs final structural checks.
- The output should be a package-ready skill folder or packaging checklist.

## Not for

- Creating the skill from scratch.
- Installing a skill into the local library.
- Fetching or preparing a public catalog package for active local setup, verification, and activation.
- Fetching or preparing a public catalog capability for active local library setup, verifying expected files, and reporting source, local path, setup result, or activation caveats.
- Editing the skill's core behavior unless packaging requires a small fix.
- Testing task performance as the main goal.

## Preconditions

- The user provides a skill need, existing skill, public source, installed library, or packaging target.
- The user indicates whether the operation is find, install, create, edit, evaluate, or package.

## Workflow

1. Identify the skill folder and intended distribution target.
2. Check required files, frontmatter, resource paths, and unnecessary clutter.
3. Confirm that scripts, references, and assets are included only when needed.
4. Make or recommend small packaging fixes.
5. Report package readiness and remaining blockers.

## Output pattern

- Packaging readiness report.
- Required files, metadata, resource links, and clutter checks.
- Remaining blockers before sharing.

## Writing rules

- Keep packaging separate from behavior redesign.
- Preserve license, attribution, and source details when present.
- Use `references/package_checklist.md` for a structured packaging pass.
