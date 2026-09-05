# Public Skill Subagent Review Protocol

Status: active Step 6 calibration method.

This protocol defines how to use Codex/subagent review as a human-like calibration layer for the public-skill field audit. It does not replace the deterministic heuristic audit or the model-assisted API audit. It is used to inspect evidence quality, catch overcounts, and create defensible examples for the thesis.

## Purpose

The thesis needs to show that proposed representation fields are not only invented for the controlled benchmark. Public `SKILL.md` artifacts should be checked for whether fields are:

- explicitly present
- implicitly extractable
- missing
- ambiguous because the skill is too broad, underspecified, or hierarchical

Subagent review is useful because it can read a complete skill artifact and judge whether a field is genuinely supported, rather than only matching keywords.

## Review Unit

One review batch should contain 5 to 10 public skills.

Each subagent receives:

- exact file paths
- the fixed field list
- the fixed status set
- the evidence rule
- a single output file path

Do not ask one subagent to review the entire 200-skill corpus. That becomes slow, inconsistent, and hard to audit.

## Fields

Review these fields:

| Field | Meaning |
|---|---|
| `routing_trigger` | When the skill should be selected or invoked. |
| `input_precondition` | Required input artifacts, prerequisites, or prior state. |
| `output_artifact` | Expected result, deliverable, file, report, patch, table, or response format. |
| `workflow_procedure` | Concrete process, ordered steps, method, or execution procedure. |
| `constraints_boundaries` | Scope limits, not-for conditions, do-not-use cases, guardrails, or constraints. |
| `dependencies_tools` | Required tools, APIs, binaries, credentials, platforms, commands, or external services. |
| `resources_references` | Referenced files, scripts, templates, assets, documentation, or supporting resources. |
| `examples_tests` | Examples, sample prompts, expected outputs, tests, verification checks, or evals. |
| `safety_side_effects` | Permissions, privacy, security, mutation risk, destructive actions, or side effects. |
| `portability_environment` | OS, language, model, version, runtime, compatibility, or environment assumptions. |
| `hierarchy_links` | Links to related skills, subskills, delegated workflows, or follow-up skill documents. |

## Status Labels

Use exactly these labels:

- `explicit`: the field is clearly named in frontmatter, a heading, or a directly labelled section.
- `implicit`: the field is supported by body text under different wording.
- `missing`: no direct textual evidence.
- `ambiguous`: the skill is too broad, underspecified, or internally mixed to label confidently.

## Evidence Rule

Every `explicit` or `implicit` label must include a short exact quote from the reviewed `SKILL.md`.

If no short quote can be provided, the field must be `missing` or `ambiguous`.

The reviewer must not infer what a good skill should contain. The reviewer only annotates what the artifact actually says.

## Output Format

Each subagent review file should use this Markdown structure:

```markdown
# Public Skill Review - Agent X

## skill-name

| Field | Status | Evidence | Notes |
|---|---|---|---|
| `routing_trigger` | explicit | "quote" | short reason |

### Skill-Level Judgment

- Atomic/broad/hierarchical:
- Main retrieval-relevant fields:
- Main missing fields:

## Calibration Notes

- Likely heuristic overcounts:
- Likely heuristic undercounts:
- Public-skill design issues:
```

## Recommended Sampling Strategy

Use subagent review for:

- low-coverage skills
- high-coverage skills that may reflect keyword overcounting
- heuristic/model disagreement cases
- public skills that are broad or hierarchical
- public skills with dependencies, external resources, or safety concerns

Initial pilot:

- Agent A reviews low/medium coverage public skills.
- Agent B reviews tool/resource-heavy public skills.

Later calibration:

- Select 20 disagreement-heavy skills after the model-assisted API audit exists.
- Optionally double-code 5 skills with two subagents to estimate reviewer consistency.

## Pass Criteria

The subagent/manual calibration is sufficient when:

- at least 20 public skills have evidence-grounded review
- disagreement cases are prioritized
- each representation field has at least a few positive or negative examples
- systematic heuristic errors are either fixed or documented
- final field classification uses heuristic + model-assisted + subagent/manual evidence

## Fail Conditions

The review is not sufficient if:

- reviewers label fields without evidence quotes
- only easy/highly structured skills are reviewed
- disagreement cases are ignored
- subagent judgments are treated as ground truth without calibration
- the thesis reports heuristic prevalence as if it were manually validated

## Current Pilot

Started on 2026-05-28.

Output folder:

- `skill_benchmark/outputs/subagent_reviews/`

Pilot files:

- `public_skill_review_agent_a.md`
- `public_skill_review_agent_b.md`
