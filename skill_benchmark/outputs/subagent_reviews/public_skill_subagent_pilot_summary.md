# Public Skill Subagent Review Pilot Summary

Date: 2026-05-28

This pilot tests whether evidence-grounded subagent review can calibrate the public-skill field audit.

## Scope

- Reviewed skills: 10 public `SKILL.original.md` files.
- Reviewers: 2 subagent batches.
- Output files:
  - `public_skill_review_agent_a.md`
  - `public_skill_review_agent_b.md`

Agent A reviewed:

- `public-anthropic-internal-comms`
- `public-anthropic-brand-guidelines`
- `public-anthropic-frontend-design`
- `public-api-design-principles`
- `public-brainstorming`

Agent B reviewed:

- `public-huggingface-datasets`
- `public-markitdown`
- `public-netlify-deploy`
- `public-office-ads-copywriter`
- `public-office-data-analysis`

## Main Calibration Signal

The subagent review supports the core direction of Step 6:

- Public skills often contain routing triggers, workflows, outputs, dependencies, resources, examples, and environment assumptions.
- Several fields are frequently implicit rather than normalized into clean schema fields.
- Safety/side-effect information is sparse and should be treated as weakly observed or proposed unless the skill text explicitly mentions read-only behavior, secrets, costs, approval gates, deployment/network effects, or accuracy risks.

## Likely Heuristic Overcounts

The heuristic audit should be treated cautiously for these fields:

- `resources_references`: ordinary mentions of "resources" or style guidance are not enough; stronger evidence is a named file, URL, directory, bundled reference, or linked skill/document.
- `examples_tests`: examples and tests should not be collapsed too aggressively. Some files provide examples but no evaluation/test logic.
- `output_artifact`: broad phrases such as "apply guidelines" may imply an output, but do not always define a concrete deliverable.
- `workflow_procedure`: principle lists and best-practice sections are weaker than ordered procedures.
- `dependencies_tools`: domain words like API, REST, or GraphQL are not necessarily operational dependencies unless the skill requires a tool, API call, library, CLI, server, credential, or service.

## Likely Heuristic Undercounts

The heuristic may miss:

- implicit workflow stages stated without headings
- side effects expressed through approval gates or "do not proceed" constraints
- hierarchy expressed as navigation tiers, bundled reference escalation, or "use another skill" instructions
- resource dependencies expressed through named local files rather than `resources/` headings

## Field-Level Notes

- `routing_trigger`: usually easy and explicit.
- `input_precondition`: can be explicit in frontmatter, but often appears as task setup or required user context.
- `output_artifact`: strong when a deliverable is named; ambiguous when the skill only changes style or behavior.
- `workflow_procedure`: strong when steps are ordered; weaker in principle-only skills.
- `constraints_boundaries`: usually reliable when "do not", limits, scope, or requirements are explicit.
- `dependencies_tools`: strong in tool/API/deployment skills; gray in conceptual API-design skills.
- `resources_references`: should require concrete files, URLs, folders, examples, references, or linked skills.
- `examples_tests`: examples are common; tests/verifiers are less common.
- `safety_side_effects`: weak overall; mark present only with textual evidence of operational risk, permissions, privacy, security, mutation, or approval.
- `portability_environment`: common in public skills with model/language/platform compatibility metadata.
- `hierarchy_links`: present when related skills, reference escalation, navigation tiers, or subskill handoffs are explicit.

## Thesis Implication

The subagent pilot supports a careful claim:

> Public skills do contain many retrieval-relevant procedural signals, but those signals are inconsistently structured. A representation layer can therefore be framed as normalization/extraction of information that public artifacts often contain implicitly, rather than as assuming authors already provide perfect metadata.

It also strengthens the caveat:

> Safety/side-effect fields and hierarchy fields should not be claimed as universal public-skill conventions. They are better framed as partial public patterns and proposed quality fields.

## Recommended Next Step

Run the model-assisted 20-skill checkpoint after `DEEPSEEK_API_KEY` is added, then compare:

- heuristic labels
- model-assisted labels with evidence spans
- subagent/manual review labels

Manual review should prioritize heuristic/model disagreement cases.
