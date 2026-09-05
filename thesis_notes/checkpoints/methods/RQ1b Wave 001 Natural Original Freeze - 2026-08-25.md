# RQ1b Wave 001 Natural-Original Freeze

Date: 2026-08-25  
Status: `FROZEN / NOT EXECUTED / NO EXTERNAL TEXT TRANSFER`

## Purpose

This checkpoint closes the first RQ1b naturalistic-public-skill curation wave.
It creates a valid natural-original selection dataset, not a retrieval result,
human-label study, causal field-masking study, or extension of RQ2.

## Frozen Data

- `62` valid source-disjoint clusters, exceeding the protocol minimum of `50`.
- `129` distinct preserved original candidate artifacts.
- `2` task prompts per cluster: a direct operational request and an
  independently phrased prompt.
- Field counts: use condition `17`, output artifact `20`, dependency/resource
  `6`, input/precondition `7`, workflow/procedure `6`, boundary/not-for `4`,
  success/verification `2`.
- All entries are `VALID_CLUSTER_ORIGINAL_ONLY`; there are `0`
  mask-eligible entries.

The low-count boundary/not-for and success/verification groups are exploratory
only. They cannot support a stable field ranking.

## Gates Passed

1. Preserved source path and SHA-256 revalidation for every candidate.
2. Source-disjoint frozen candidate sets.
3. Two task-like prompts per cluster.
4. Literal prompt audit: `0` candidate-name matches and `0` copied three- or
   four-token source phrases. The `143` remaining short-line hits are retained
   as audit evidence rather than treated as a clean semantic-leakage proof.
5. Exact source-evidence/residual map for every candidate and all relevant
   natural-document surfaces.
6. Two independent internal Codex blinded-review tables per cluster, both
   prompts, with an agreed singleton acceptable first skill in `62/62`
   clusters; no third adjudication was required.
7. Raw reviewer response tables recovered from local sessions and verified
   against their stored hashes.

## Evidence

- Frozen manifest:
  `skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_001_frozen_manifest.jsonl`
- Validation certificate:
  `skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_001_freeze_certificate.json`
- Source/residual evidence map:
  `skill_benchmark/rq1b_naturalistic_public_replication/review/wave_001/SOURCE_EVIDENCE_AND_RESIDUAL_MAP.md`
- Prompt-overlap audit:
  `skill_benchmark/rq1b_naturalistic_public_replication/review/wave_001/prompt_overlap_audit.json`
- Blinded-review response manifest:
  `skill_benchmark/rq1b_naturalistic_public_replication/review/wave_001/blind_review_response_manifest.json`
- Freeze validator:
  `skill_benchmark/scripts/freeze_rq1b_wave.py`

## Interpretation Boundary

Natural public artifacts express operational facts jointly. The target
distinction appears in titles, workflows, examples, and resources as well as
the declared primary field. Consequently, this frozen wave may later test
selection over unmodified natural artifacts, but it may not report a causal
effect of deleting one declared field. The blinded review is model-assisted
curation evidence, not human annotation. No BM25, embedding, reranker,
external API, hosted compute, or external text transfer has occurred.

## Next Gate

Any selector experiment requires a separately stated execution plan. A future
natural-original selector run must keep the frozen manifest unchanged, report
cluster-level acceptable metrics, and preserve the distinction between RQ1a
controlled field sufficiency and RQ1b natural-artifact selection.

