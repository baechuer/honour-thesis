# Final Representation Field Taxonomy - Draft

Date: 2026-05-29

Purpose: freeze the current thesis interpretation of what information a scalable skill representation should preserve.

This taxonomy is based on:

- the 2089-skill benchmark;
- the 200 public-skill field audit;
- DeepSeek model-assisted verification of public skill fields;
- targeted disagreement adjudication;
- Step 7 field-ablation results.

## Main Thesis Claim

The thesis should not claim that every public skill already contains a clean schema.

The stronger and more defensible claim is:

> Skill artifacts often contain procedural signals, but these signals are unevenly expressed. A retrieval representation layer should extract and normalize the signals that help distinguish semantically similar but procedurally different skills.

## Final Field Categories

| Field | Status | Retrieval Role | Current Evidence |
|---|---|---|---|
| `description/topic` | Observed | First-stage broad recall only | Present in public skills, but description-only methods degrade at scale. |
| `use_when` / routing intent | Observed/extractable | Strong positive selector field | Largest early field-ablation gain; must be separated from generic description. |
| `output_artifact` | Observed/extractable | Strong positive selector field | Field ablation shows major top-1 improvement after adding outputs. |
| `workflow_procedure` | Observed/extractable | Strong positive selector/reranking field | BM25 peak occurs after workflow is included; supports procedural distinction. |
| `input_precondition` | Extractable | Moderate selector and feasibility field | Helps reduce non-core false positives, but public skills often imply it rather than label it. |
| `constraints_boundaries` / `not_for` | Definition-sensitive | Penalty, filter, or boundary check | Useful conceptually, but naive text concatenation hurts top-1. |
| `dependencies_tools` | Observed | Feasibility/reranking field, not raw positive text | Strong public-skill evidence, but dependency text can attract irrelevant same-tool skills. |
| `resources_references` | Observed/extractable | Context-loading and hierarchy field | Common in public skills, but should mean concrete files/links/scripts, not inline templates. |
| `examples_tests` | Observed/extractable | Downstream execution and validation support | Common in public skills; less central for first-stage selection. |
| `portability_environment` | Observed/extractable | Feasibility and execution-risk field | Useful for execution planning, especially local/runtime-dependent skills. |
| `hierarchy_links` | Partially observed | Skill expansion/delegation field | Real public skills can be hierarchical, but controlled benchmark core should stay atomic. |
| `safety_side_effects` | Weakly observed/proposed | Guardrail and downstream validation field | Sparse in public skills; keep as a quality/reliability field, not a mature authoring convention. |

## Recommended Retrieval Usage

Primary retrieval should preserve these fields:

- `use_when`
- `output_artifact`
- `workflow_procedure`
- `input_precondition`

These fields are most directly tied to distinguishing near-neighbour skills.

Secondary reranking or feasibility checks should use:

- `constraints_boundaries`
- `not_for`
- `dependencies_tools`
- `resources_references`
- `portability_environment`
- `hierarchy_links`
- `safety_side_effects`

These should not simply be appended as plain retrieval text because they can introduce false positives.

## Method Set For Thesis Comparison

Keep the final comparison focused on representation classes, not provider trivia:

| Method | Purpose |
|---|---|
| M0 progressive disclosure | Historical/context baseline: load all compact descriptions when possible, then choose full docs. |
| M1 flat lexical retrieval | Scalable flat-card baseline over name/description/tags. |
| M2 dense semantic retrieval | Scalable semantic candidate generator over full skill text or description cards. |
| M3 structured procedural retrieval | Tests whether normalized procedural fields improve selection. |
| M6/M8 hybrid retrieval + schema reranking | Tests whether broad semantic recall plus procedural reranking gives the best practical trade-off. |

Provider-specific variants, such as Qwen embedding or Qwen reranking, should be presented as implementations of the dense/hybrid classes, not as the main intellectual contribution.

## Current Interpretation To Carry Into Writing

- Strong embedding retrieval is useful for first-stage filtering.
- Generic reranking helps, but procedural schema reranking is better aligned with this benchmark.
- Structure-aware representation is not just "more text"; the useful fields are selective.
- `use_when`, `output_artifact`, and `workflow_procedure` are the strongest current evidence fields.
- `not_for`, dependency, and resource information should be handled with field-aware logic, not naive concatenation.
- Public skills validate the existence of many procedural signals, but also show that extraction/normalization is the representation layer's responsibility.

## Still To Decide

- Final candidate budget: top-50 or top-100.
- Whether Qwen R1/R2 provider variants need to be rerun at 2089 scale, or whether local R1/M1 plus Qwen full-skill is enough.
- Final downstream sample and grading protocol.

## Public-Skill Expansion Rule

Additional public skills can be used to validate this taxonomy and increase background pressure, but they should not automatically become evaluated gold skills.

Use imported public skills in two ways:

- **Background skills**: realistic distractors and scale pressure. These test whether the target skill remains retrievable when many unrelated or weakly related skills exist.
- **Taxonomy evidence**: external artifacts for checking whether fields such as inputs, outputs, workflows, dependencies, resources, and boundaries are observed, extractable, or proposed.

Only promote a public skill into the controlled evaluated set if it has been:

- atomized into one clear procedural capability;
- assigned a gold prompt and plausible alternatives;
- checked for semantic confusability;
- checked for leakage and acceptable alternatives;
- included in the normal Step 1-4 benchmark validation loop.
