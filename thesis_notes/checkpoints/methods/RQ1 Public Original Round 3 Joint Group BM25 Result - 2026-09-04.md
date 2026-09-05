# RQ1 Public Original Round 3 Joint Group BM25 Result

Date: 2026-09-04  
Status: `COMPLETE / MECHANICALLY AND SOURCE VALIDATED / RESEARCHER REVIEWED WITH EDITS VISIBLE / INTEGRATED INTO THESIS`

## What Was Tested

This supporting RQ1 extension compares each exact public original skill source
with the same source after a coherent group of already verified Round-3 lines
is deleted. The document may be incomplete after deletion: the measurement is
routing support, not skill executability. It is distinct from the earlier
field-card group study and does not pool results across the groups.

| Group | Component fields | Families | Compositions | Ranking rows |
| --- | --- | ---: | ---: | ---: |
| Task specification | use; input; output | 99 | 37 | 396 |
| Execution/verification | workflow; success | 138 | 51 | 552 |
| Applicability/capability | boundary; dependency | 132 | 50 | 528 |

Each group mask is the exact union of blanked source lines in its component
Round-3 masks. Every component candidate had an existing `CLEAR` decision, and
the exact-union validator confirmed that the group did not change any other
line or reintroduce a removed component value.

## Integrity

- Freeze SHA-256: `7a73a3d4026ffa32b855ae3844cf3d63046aff9535435294a2cf742f84cc9062`
- BM25 result SHA-256: `3eb649a71770c9e24f800b3f07479bcedecc2efa5e768cdbf66210e1e1a46e14`
- BM25 analysis SHA-256: `2ef74203c46bdb9ce824eb0c8f23e95a5f0f6852c70bc410eee404ea822dfcb8`
- 1,476/1,476 rows passed identity, candidate, prompt, rank, pair-coverage and
  checksum validation.
- Local BM25 only; no external text transfer, query rewrite or reranker.

## Result

Primary estimates average direct/paraphrase observations within routing family,
families within composition, then use 10,000 seeded composition-clustered
paired bootstrap resamples. Positive effects mean the full document routed
better than the version with the whole group deleted.

| Group | Full Hit@1 | Removed Hit@1 | Hit@1 delta [95% CI] | MRR delta [95% CI] | Native margin delta [95% CI] |
| --- | ---: | ---: | ---: | ---: | ---: |
| Task specification | 0.784 | 0.518 | +0.266 [+0.196, +0.336] | +0.156 [+0.116, +0.198] | +4.645 [+3.403, +5.996] |
| Execution/verification | 0.790 | 0.614 | +0.176 [+0.094, +0.262] | +0.114 [+0.065, +0.164] | +4.272 [+2.771, +5.859] |
| Applicability/capability | 0.780 | 0.644 | +0.136 [+0.087, +0.186] | +0.083 [+0.055, +0.112] | +2.547 [+1.805, +3.309] |

Descriptively, full-correct-to-removed-wrong prompt transitions outnumbered
reverse transitions in every group: task 57 vs 3, execution 63 vs 12, and
applicability 46 vs 5. They are not used as the primary unit of inference.

## Interpretation

For these strict public-source cases and local BM25, removing each tested
combination of documented information weakens routing. The result says nothing
about which individual field inside a group was decisive, whether effects are
additive, or whether a different retriever will behave the same way. Qwen has
not run. The next bounded step is a local-only cache-aware Qwen preflight;
executing it requires a fresh, exact external-text authorisation.

## Canonical Artifacts

- SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md`
- Freeze: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_freeze/`
- Result: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_bm25_results/bm25_results.json`
- Analysis: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_bm25_results/analysis/bm25_paired_analysis.json`

No thesis LaTeX or PDF file was modified.
