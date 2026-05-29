# Step 8 Downstream Candidate-Subset Validation Plan

Status: planned, not yet executed.

Purpose: test whether candidate subsetting improves the final task artifact, not only whether the selector ranks the gold skill highly.

## Conditions To Compare

Use the same prompt text across all conditions.

| Condition | What the main agent sees | Purpose |
|---|---|---|
| `oracle_gold` | Only the gold full `SKILL.md` | Checks whether the prompt and skill can produce a correct artifact when retrieval is solved. |
| `m0_progressive_core` | Normal progressive disclosure over the 67 controlled core skills | Baseline for current main-agent skill selection behavior. |
| `m1_flat_top5` | Top-5 candidates from flat metadata selector | Tests scalable compressed metadata subsetting. |
| `m2b_full_skill_top5` | Top-5 candidates from full-skill embedding selector | Tests whether full skill text improves candidate recall. |
| `m3_schema_top5` | Top-5 candidates from schema/procedural selector | Tests whether procedural fields improve downstream task success. |
| `m6_minilm_schema_rerank_top5` | Top-5 candidates from MiniLM full-skill retrieval plus schema-aware reranking | Tests the strongest current local retrieve-and-rerank method. |

Optional negative control: expose the top wrong candidate from `m2a_minilm_description` for selected prompts where it confidently retrieves a semantically plausible but procedurally wrong skill.

## Candidate Budget

- First validation budget: top-5.
- Record whether gold or an acceptable alternative is in the candidate set before downstream execution.
- If gold/acceptable is absent, label the downstream failure as retrieval failure, not main-agent execution failure.

## Representative Prompt Sample

The first downstream sample should include easy-success cases, semantic near-neighbor cases, no-skill M0 cases, and wrong-skill M0 cases.

| Prompt | Family | Why include it |
|---|---|---|
| `reply_p2_polish_supervisor` | reply_messaging | Easy M0 success; checks that simple cases remain stable. |
| `doc_p2_document_rewriter` | documents_files | Acceptable-alternative edge case; rewrite vs summary/polish confusion. |
| `doc_p4_field_extraction` | documents_files | M0 no-skill case; output schema is easy to grade. |
| `doc_p6_conversion` | documents_files | Public acceptable alternative exists; tests acceptable scoring. |
| `data_p3_validation` | data_spreadsheet | M0 no-skill case; validates whether procedural audit fields matter. |
| `obs_p5_root_cause` | metrics_observability | Core semantic-neighbor case; root cause vs anomaly/capacity confusion. |
| `news_p2_briefing` | news_monitoring | M0 wrong top-1 case; tests artifact type distinction. |
| `read_p2_general_source_summary` | reading_research | M0 wrong top-1 but gold any-hit; useful for downstream recovery analysis. |
| `read_p7_multi_source_comparison` | reading_research | M0 no-skill but task is answerable; tests skill-use necessity. |
| `sec_p2_security_code_review` | security_appsec | M0 no-skill case; code-level security vs broad auth/threat review. |
| `skill_p4_edit_existing` | skill_lifecycle | M0 wrong top-1 case; skill edit vs finding/extraction confusion. |
| `skill_p6_package_existing` | skill_lifecycle | M0 wrong top-1 but gold any-hit; tests multi-skill recovery. |

Browser-heavy prompts can be added later after browser execution is available in the downstream environment; otherwise they should remain retrieval-only cases.

## Artifact Grading Rubric

Score each final output on a 10-point scale.

| Criterion | Points | What counts |
|---|---:|---|
| Correct artifact type | 2 | Output format matches the requested task, such as brief, comparison table, extraction schema, review memo, or rewrite. |
| Required fields included | 2 | Includes all prompt-required sections, fields, constraints, or comparison axes. |
| Procedural workflow followed | 2 | Performs the intended operation, not a neighboring one. For example, validates data instead of summarizing it. |
| Evidence/resource handling | 1 | Uses provided source, file, metrics, code, or dependency information correctly when required. |
| Constraint compliance | 1 | Avoids forbidden behavior such as submitting forms, inventing evidence, changing meaning, or producing the wrong level of detail. |
| Completeness and usability | 2 | Final artifact is specific enough to be useful without major missing pieces. |

Pass thresholds:

- `8-10`: downstream success
- `6-7`: partial success; inspect whether failure came from retrieval, skill execution, or prompt ambiguity
- `0-5`: downstream failure

## Step 8 Pass Criteria

- At least 12 prompts are evaluated.
- `oracle_gold` reaches at least 80% downstream success; otherwise the prompt or skill set is not stable enough for downstream claims.
- For each non-oracle selector, report candidate recall before artifact success.
- A method is only credited for downstream success if the selected/used skill is gold or documented acceptable.
- Failures are labelled as one of: retrieval failure, wrong-skill execution, no-skill/direct-answer behavior, environment/tool failure, or prompt ambiguity.

## Expected Use

This step should be run after stronger embedding and reranking baselines are added, but the sample above is already suitable for an initial local dry run using the current M1/M2/M3 selectors.
