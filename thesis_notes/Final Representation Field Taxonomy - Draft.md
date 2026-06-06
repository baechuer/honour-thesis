# Final Representation Field Taxonomy - Draft

Date: 2026-06-01

Purpose: freeze the current thesis interpretation of what information a scalable skill representation should preserve.

This taxonomy is based on:

- the 2349-skill benchmark;
- the 460 public-skill field audit;
- DeepSeek model-assisted verification of 460 public skill fields;
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
| `use_when` / routing intent | Observed/extractable | Strong positive selector field | Model audit: 394/460 public skills present. Largest early field-ablation gain; must be separated from generic description. |
| `output_artifact` | Observed/extractable | Strong positive selector field | Model audit: 369/460 present. Field ablation shows major top-1 improvement after adding outputs. |
| `workflow_procedure` | Observed/extractable | Strong positive selector/reranking field | Model audit: 416/460 present. BM25 peak occurs after workflow is included; supports procedural distinction. |
| `input_precondition` | Extractable | Moderate selector and feasibility field | Model audit: 314/460 present. Helps reduce non-core false positives, but public skills often imply it rather than label it. |
| `constraints_boundaries` / `not_for` | Definition-sensitive | Penalty, filter, or boundary check | Useful conceptually, but naive text concatenation hurts top-1. |
| `dependencies_tools` | Observed | Feasibility/reranking field, not raw positive text | Model audit: 412/460 present. Strong public-skill evidence, but dependency text can attract irrelevant same-tool skills. |
| `resources_references` | Observed/extractable | Context-loading and hierarchy field | Model audit: 355/460 present. Common in public skills, but should mean concrete files/links/scripts, not inline templates. |
| `examples_tests` | Observed/extractable | Downstream execution and validation support | Model audit: 403/460 present. Common in public skills; less central for first-stage selection. |
| `portability_environment` | Observed/extractable | Feasibility and execution-risk field | Model audit: 341/460 present. Useful for execution planning, especially local/runtime-dependent skills. |
| `hierarchy_links` | Partially observed | Skill expansion/delegation field | Model audit: 238/460 present. Real public skills can be hierarchical, but controlled benchmark core should stay atomic. |
| `safety_side_effects` | Weakly observed/proposed | Guardrail and downstream validation field | Model audit: 137/460 present. Sparse in public skills; keep as a quality/reliability field, not a mature authoring convention. |

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
| M1 flat lexical control | Scalable flat-card control over name/description/tags; useful for diagnosing lexical cueing. |
| M2 dense semantic retrieval | Scalable semantic candidate generator over R1 flat cards or full skill artifacts. |
| M3 structured procedural retrieval | Tests whether extracted procedural fields help before reranking. |
| M4 generic neural reranking | Tests whether a strong model reranker over dense candidates solves the task without explicit procedural scoring. |
| M6-v0 local schema reranking | Diagnostic current method: weighted lexical overlap over extracted fields; transparent but too crude for final claims. |
| M6-v1 field-aware procedural reranking | Proposed main structure-aware method: parse request fields, compare them to extracted skill fields, and penalize boundary/hierarchy mismatches. |

Provider-specific variants, such as Qwen embedding or Qwen reranking, should be presented as implementations of the dense/hybrid classes, not as the main intellectual contribution.

Detailed method cleanup is recorded in:

- `thesis_notes/Final Method Set and Information-Use Plan.md`

## Current Interpretation To Carry Into Writing

- Strong embedding retrieval is useful for first-stage filtering.
- Generic reranking helps, and the current public-gold results show it can outperform the crude local schema reranker on externally authored skills.
- The current local schema reranker should be described as `M6-v0`: diagnostic evidence that procedural fields can be useful, but not the final method.
- The final method should be `M6-v1`: a field-aware procedural reranker that uses extracted information as fields rather than appending them as plain text.
- Structure-aware representation is not just "more text"; the useful fields are selective.
- `use_when`, `output_artifact`, and `workflow_procedure` are the strongest current evidence fields.
- `not_for`, dependency, and resource information should be handled with field-aware logic, not naive concatenation.
- Public skills validate the existence of many procedural signals, but also show that extraction/normalization is the representation layer's responsibility.
- Step 6 now supports this with full 460-skill model-assisted verification, not only the earlier 200-skill checkpoint.
- Step 6b public-gold manual adjudication supports using public-gold as a separate external-validity stratum after acceptable alternatives and unstable cases are cleaned.

## Still To Decide

- Final candidate budget: top-50 or top-100.
- Exact scoring and calibration for `M6-v1` field-aware procedural reranking.
- Whether to include an optional LLM field-aware reranker as an expensive upper-bound method.
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
