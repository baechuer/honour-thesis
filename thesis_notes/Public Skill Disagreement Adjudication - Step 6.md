# Public Skill Disagreement Adjudication - Step 6

Date: 2026-05-29

Purpose: targeted pattern-level adjudication of heuristic/model disagreements from the 200 public-skill field audit.

Source files:

- `skill_benchmark/outputs/public_skill_field_agreement_report.md`
- `skill_benchmark/outputs/public_skill_field_disagreement_review_packet.md`
- `thesis_notes/Public Skill Model Verification Checkpoint - 200 Skills.md`

This is not a second full gold annotation pass. It is a manual review of disagreement patterns used to refine field definitions before final thesis claims.

## Main Decision

The public-skill audit supports the broad claim that real skills often contain procedural retrieval signals, but the fields must be split into three categories:

1. **Observed and retrieval-useful**: use/routing intent, workflow/procedure, output artifact, dependencies/tools, examples/tests, portability/environment.
2. **Often extractable but definition-sensitive**: input/preconditions, constraints/boundaries, resources/references, hierarchy/links.
3. **Weakly observed or proposed quality field**: safety/side effects.

This means the thesis should not claim that public skills already expose a clean schema. The stronger claim is:

> Public skill artifacts contain many procedural signals, but these signals are unevenly expressed. A retrieval representation layer can normalize them into fields that improve skill selection.

## Field Decisions

| Field | Disagreement Pattern | Manual Decision | Thesis Impact |
|---|---|---|---|
| `routing_trigger` | Heuristic counted broad description/frontmatter as explicit trigger; model often marked missing. | Definition needs refinement. Broad descriptions count as weak routing cues, not high-quality invocation conditions. | Keep as essential, but separate `description/topic` from `use_when/trigger`. |
| `resources_references` | Heuristic counted `related_skills`, inline templates, headings, and frontmatter as resources; model required concrete files/links/scripts. | Model definition is stronger for thesis. Count concrete file paths, URLs, bundled references, scripts, linked docs, or delegated skill documents. Inline templates should be examples/templates, not external resources. | Treat resources as a field-aware signal, not plain text. |
| `safety_side_effects` | Heuristic overcounted words like risk, security, and churn risk when they were task content, not execution risk. Model found some real guardrails such as secrets, read-only operations, copyright, and auth. | Sparse but important. Count only permissions, privacy, destructive actions, auth/secrets, data mutation, copyright/legal, or explicit side effects. | Classify as proposed/weakly observed. Useful for reliability, but not a mature public-skill convention. |
| `constraints_boundaries` | Heuristic overcounted generic rules, slogans, validation headings, and business constraints. Model sometimes undercounted technical guardrails. | Count scope limits, not-for conditions, supported/unsupported formats, rate/page limits, read-only boundaries, and hard guardrails. Do not count generic best-practice rules unless they restrict applicability. | Keep, but score carefully. Naive text concatenation already hurts retrieval. |
| `input_precondition` | Heuristic overcounted examples, sample schemas, quick-start snippets, and illustrative inputs. Model sometimes missed implicit required artifacts. | Count user-provided artifacts, available environment state, existing project/app, required credentials, required data, or clear prerequisite state. Do not count generic examples as preconditions. | Important but should be normalized, because public skills often imply rather than label preconditions. |
| `dependencies_tools` | High agreement, with model catching implicit tool/library mentions. | Observed and reliable. Include tools, APIs, CLIs, libraries, models, scripts, integrations, and runtimes. | Strong evidence that dependency/tool signals are real in public skills. |
| `workflow_procedure` | High agreement, though heuristic can miss implicit procedures and model can overcount conceptual frameworks. | Count ordered steps, methods, required phases, checklists, or concrete procedural templates. Do not count only conceptual background. | Strong core retrieval field. Field ablation supports this. |
| `output_artifact` | High agreement, with model catching implicit deliverables. | Count concrete or inferable deliverables: code, report, deck, HTML, screenshot, config, plan, dataset, API response, etc. | Strong core retrieval field. Field ablation supports this. |
| `examples_tests` | High agreement, but heuristic can count generic illustrative text too broadly. | Count example prompts, examples, test commands, validation checks, expected outputs, verification steps, and sample artifacts. | Useful public-skill field; likely more useful for downstream execution than first-stage retrieval. |
| `hierarchy_links` | Good agreement but definition-sensitive. | Count explicit linked skills, delegated workflows, bundled subdocuments, reference docs, and "load as needed" paths. | Supports the idea that hierarchical skills exist in the wild, but benchmark core should remain atomic for clean evaluation. |

## Concrete Corrections To Use In The Thesis

- Do not say public skills already contain a clean procedural schema.
- Say public skills contain recoverable procedural signals, but the representation layer has to extract and normalize them.
- Do not treat `not_for`, `constraints`, or safety text as simple positive retrieval text.
- Use `not_for` and safety fields as penalties, filters, or post-retrieval feasibility checks.
- Treat dependencies/resources as useful for procedural suitability, but risky as raw concatenated retrieval text because they can attract irrelevant skills with similar tools.

## Link To Step 7 Field Ablation

The field-ablation results fit this manual adjudication:

- `use_when` gives the largest early gain.
- `output_artifact` and `workflow_procedure` produce the strongest additional top-1/MRR gains.
- `preconditions` help modestly and reduce non-core false positives.
- Naive `not_for` and dependency/resource concatenation can reduce top-1 or add noise.

This supports the final thesis framing: the important contribution is not "more metadata is always better." The contribution is identifying which procedural information should be preserved and how it should be used in retrieval.

## Remaining Optional Work

If the thesis needs a stricter appendix, manually label the 50 rows in `public_skill_field_disagreement_review_packet.md` with one of:

- `heuristic_correct`
- `model_correct`
- `both_partly_correct`
- `both_wrong_or_unclear`
- `definition_needs_refinement`

For the main thesis, the pattern-level adjudication is sufficient to refine the field taxonomy and prevent overclaiming.
