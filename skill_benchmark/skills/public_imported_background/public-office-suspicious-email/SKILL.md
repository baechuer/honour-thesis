---
name: public-office-suspicious-email
description: "Public-source background skill based on `Suspicious Email Analyzer`. Analyze emails for phishing, scam indicators, and security threats Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "Suspicious Email Analyzer"
  public_origin: "claude-office-skills/skills"
  source_url: "https://github.com/claude-office-skills/skills/tree/main/suspicious-email"
  raw_url: "https://raw.githubusercontent.com/claude-office-skills/skills/main/suspicious-email/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for suspicious email; depends on the source artifact and task context named by the user"
---

# Public Imported Background: Suspicious Email Analyzer

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: claude-office-skills/skills
- Source page: https://github.com/claude-office-skills/skills/tree/main/suspicious-email
- Raw artifact: https://raw.githubusercontent.com/claude-office-skills/skills/main/suspicious-email/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for suspicious email; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- security evidence
- system context
- threat or control taxonomy

## Resource And Structure Signals

- suspicious email
- public SKILL.md metadata
- security
- threats
- controls
- risk

## Use when

- The retrieval setting needs realistic public-skill noise around this capability.
- The selector should consider tool requirements, file types, resource links, or external systems as part of skill suitability.
- The task is closer to this public skill's dependency profile than to a controlled core skill.

## Not for

- Replacing a controlled gold-label core skill in the main confusable evaluation.
- Hiding a second routing problem inside the selected skill.
- Treating public-source imports as cleanly annotated gold labels.

## Benchmark Role

This skill is intended for large-library and dependency-aware retrieval settings. It helps test whether skill representations preserve information such as required tools, file formats, repository context, external services, and optional resources.
