# RQ1 Public Original Round 3 Twin Result and Failure Analysis

Date: 2026-09-04  
Status: `COMPLETE / MECHANICALLY AND SOURCE VALIDATED / RESEARCHER REVIEWED WITH EDITS VISIBLE / INTEGRATED INTO THESIS`

## Scope

This checkpoint records the first-stage retrieval twin from the frozen Round-3
clean-only public-original source frame. It compares an exact public source
document (`FULL_ORIGINAL`) with the exact same document after only one named
information field is removed (`REMOVE_<FIELD>_R3`). The edited document may be
incomplete or non-executable; this is permitted because RQ1 tests routing
information, not execution after deletion.

The candidate set, prompts, candidate order, singleton gold label, original
hashes, masked hashes and clearance decision were held fixed. Each eligible
routing family has one direct and one paraphrase prompt. Those prompt variants
are repeated measurements, not independent observations.

## Frozen Frame and Integrity

- Freeze: 1,078 composition-family cases, 2,156 prompt rows and 4,312 paired
  ranking rows per retriever.
- Eligible composition counts: use 57; input 53; output 49; workflow 63;
  success 59; boundary 69; dependency 52.
- Freeze SHA-256:
  `a87dc0529fad8ee1cf2c19ff762746c7c9affe18b7145b3b98e7f5476c871861`.
- BM25 result SHA-256:
  `010fee2f8f548bcd22c08f2eb8b65bdece0850c2cce231fdad58f178967ee1d3`.
- Qwen preflight payload SHA-256:
  `38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2`.
- Qwen result SHA-256:
  `8c7f058106de376e92b6cd1381fdd0491fbbdb9836ab9b0a759d4efa36637f06`.
- Qwen paired-analysis SHA-256:
  `765421cfd8f309ae38278e7723f71614aa907b3d872b1b511cd897e41e7a4180`.
- Twin-synthesis SHA-256:
  `5f0211cd4e4a337b2d5dcfed446b5bc38ca7d6d69b276ad4bbed37425cb173b1`.

All row-coverage, identity, candidate-cardinality, rank, prompt-pair,
checksum and composition-level analysis validators passed. The Qwen execution
completed under the explicit user authorisation: 1,898 unique cache-miss texts,
190 successful sequential requests, zero retries, no query rewrite and no
reranker. Provider-reported input usage was 2,394,292 tokens. Embeddings are
persisted at
`skill_benchmark/cache/rq1_public_original_round3_qwen_text_embedding_v4_1024/`.

## Primary Result

The primary metric is paired `Hit@1(FULL_ORIGINAL) - Hit@1(REMOVE_FIELD)`.
Within each field, direct/paraphrase observations are averaged within routing
family, families are equally averaged within composition, and 95% CIs use
10,000 composition-clustered paired bootstrap resamples. Each field retains
its own clean-only denominator; fields are not pooled.

| Field | BM25 delta [95% CI] | Qwen delta [95% CI] | Conservative reading |
| --- | --- | --- | --- |
| Use condition | +0.114 [+0.067, +0.167] | +0.058 [+0.031, +0.092] | Stable positive under both. |
| Input/precondition | +0.098 [+0.051, +0.149] | +0.016 [-0.017, +0.052] | BM25 positive; Qwen indeterminate. |
| Output/artifact | +0.122 [+0.065, +0.187] | +0.003 [-0.036, +0.036] | BM25 positive; Qwen indeterminate. |
| Workflow/procedure | +0.151 [+0.086, +0.215] | +0.040 [-0.024, +0.100] | BM25 positive; Qwen indeterminate. |
| Success/verification | +0.117 [+0.059, +0.182] | +0.027 [+0.005, +0.054] | Stable positive under both. |
| Boundary/not-for | +0.024 [-0.014, +0.064] | -0.022 [-0.054, +0.008] | No stable positive Top-1 effect. |
| Dependency/resource | +0.091 [+0.046, +0.139] | +0.013 [-0.048, +0.067] | BM25 positive; Qwen indeterminate. |

## Failure Analysis

The result package separates three phenomena rather than treating every mask
as a failure:

1. `full-correct -> removed-wrong` is an observed strict routing loss
   consistent with removing the named field.
2. `full-wrong -> removed-correct` is a countervailing improvement. It stays
   in the analysis and stops us from claiming that every deletion harms
   selection.
3. A lower native gold-versus-leading-negative margin can show weakening even
   when the top-ranked label does not change. It is diagnostic within a single
   retriever only; BM25 and cosine margins are not put on one scale.

For Qwen, use condition has 27 prompt-row correct-to-wrong transitions versus
8 countervailing improvements, and success/verification has 11 versus 4. This
matches their positive composition-level effects. Boundary/not-for instead has
10 losses and 13 countervailing improvements, matching its non-positive Qwen
Top-1 estimate. Workflow has 29 losses and 11 improvements, but its effect is
heterogeneous across the 63 compositions, so its Qwen confidence interval
still crosses zero. These prompt-row counts are descriptive: the composition
is the statistical unit.

## What This Supports and Does Not Support

Supported: for the reviewed strict public-source compositions and these two
first-stage retrievers, removing some documented field information can weaken
routing. Use condition and success/verification meet the conservative
cross-retriever rule.

Not supported: that all seven fields are equally useful; that a weak/null
effect makes a field generally useless; that the field was the only cue in a
document; that masking preserves executability; or that results automatically
generalise to whole-library search, query rewriting, reranking, graph/tree
retrieval or other models.

## Canonical Artifacts

- SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md`
- Freeze: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/`
- BM25 result: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_bm25_results/`
- Qwen result: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_qwen_results/`
- Cross-retriever synthesis: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_twin_synthesis/`

This checkpoint did not modify the thesis when it was first created. Its current results and limitations are now integrated into the thesis.
