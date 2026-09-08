# V7 runner-output and offline-analysis contract

Status: `PRE_OUTCOME_IMPLEMENTATION_CONTRACT_NO_SELECTOR_RESULTS_OBSERVED`.

This package closes the interface between the frozen B36+C6 experiment and the
offline D3 analysis. It does not contain, inspect, or authorise selector output.
The two JSON Schemas are intentionally label-free. The scorer is the first code
allowed to open the frozen label adapter and reviewed-neighbour ledger.

## Materialised outcomes

- B1 persists 12 first-stage cells (`B01-G0` through `B12-G0`): 12 x 1,077 =
  12,924 rows. Every row contains exactly 100 unique source SHA identities and
  scores.
- B2 persists the 24 core GQ/GS conditions plus six new bridge conditions:
  30 x 1,077 = 32,310 rows. Every row binds and permutes exactly the persisted
  Top-20 from its declared B1 source.
- The total is 42 materialised outcomes per prompt and 45,234 outcome rows.
- `C2-Q` and `C2-S` are analysis aliases for `B05-GQ` and `B05-GS`. They cause
  no runner call and have no duplicate input or output row.

## Label-isolation boundary

Runner code may use the label-free runtime queries, source manifest, condition
manifests, and representation artifacts. A runner row cannot contain targets,
gold, A_q/J_q/D_q, acceptable/adequacy/judgement fields, metrics, or review
outcomes. Both schemas use `additionalProperties: false`; the validator also
recursively rejects label/outcome-like keys.

The offline scorer validates the full label-free output first. Only then does it
join:

- `offline_label_adapter.jsonl` for A_q, J_q, lane and strata;
- `dependency_ledger.jsonl` for whole-group resampling;
- `exposure_ledger.jsonl` for the required exposure disclosure; and
- `reviewed_confusable_neighbour_ledger.jsonl` for the sealed D_q diagnostic.

Unjudged candidates are unknown, not errors. Reviewed errors are J_q minus A_q
and are decomposed into partially adequate and inadequate. The acceptable
Known-A endpoint uses all prompts and any member of A_q. The strict endpoint is
the frozen `STRICT` subset, where A_q is a singleton; no strict target is
invented for a multi-acceptable prompt.

## Ranking and cost identity

`top20_binding_sha256` is canonical JSON SHA-256 over the B1 condition, prompt
identity/hash and ordered first 20 source identities. A B2 row must carry that
binding, the identical ordered input identities, a representation-specific
candidate-view hash for every item, and a whole-input hash. Its output must be a
permutation of those same 20 identities with the original input rank retained.

Cost fields record measured latency, calls, tokens, windows, cache hits, retries,
timeouts and failed attempts. A successful row may include retry/failure costs.
An unrecovered outcome must not invent rankings: it yields no scientific row,
and full-scope offline scoring stops until the missing cell is resolved under
the run SOP.

## Offline endpoints and scopes

For every condition the scorer reports Known-A Hit@1, CandidateHit@20,
SetRecall@20, MRR@20, conditional Hit@1, reviewed-error decomposition,
Unjudged@1/@20, and the `[Known-A Hit@1, Hit@1 + Unjudged@1]` identification
interval. It verifies both:

1. `Hit@1 = CandidateHit@20 x ConditionalHit@1` on the same scope; and
2. every B2 CandidateHit@20 equals its bound B1 candidate source.

The primary scope is the 714-prompt `B_NC_FULL_UNION` lane. The 649-prompt
source-native NC stratum is the prespecified sensitivity; the 65 legacy NC, 127
parent-public, and 236 parent-controlled prompts are separate descriptive
strata. Parent rows never enter P1-P5 inference.

D_q is used only where the frozen C* contains at least one A_q and one D_q. The
scorer reports reviewed-neighbour Top-1, acceptable-to-neighbour regression,
neighbour-to-acceptable rescue, relation-rule counts and slice coverage. D_q
does not become a retrieval edge or candidate-generation input.

## P1-P5

The exact comparisons and endpoints are in `analysis_contract.json`. All five
use prompt-weighted paired differences and whole frozen dependency groups as
the resampling/randomisation unit. Every comparison receives a 10,000-replicate
whole-group percentile bootstrap with seed `2026090801` and a descriptive 95%
CI. P1/P3/P4/P5 receive 100,000 whole-group paired sign flips with seed
`2026090802`, two-sided alpha 0.01. P2 passes non-inferiority only when its
one-sided 99% grouped-bootstrap lower bound is strictly greater than -0.03.
Equal-dependency-group-weighted effects are sensitivity estimates, not a
replacement estimand.

## Commands

Validate complete label-free output without loading offline labels:

```bash
python3 -B skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py \
  --b1 /ABSOLUTE/PATH/b1.jsonl \
  --b2 /ABSOLUTE/PATH/b2.jsonl
```

The validator and offline scorer accept either plain `.jsonl` or deterministic
gzip `.jsonl.gz` (`mtime=0`). Compression is a physical storage choice only;
the decompressed JSON rows remain governed by the same schemas and hashes.

Validate an incremental shard (all included B2 rows still require their B1
source rows in the supplied B1 file):

```bash
python3 -B skill_benchmark/scripts/validate_rq2b_v7_runner_outputs.py \
  --b1 /ABSOLUTE/PATH/b1-shard.jsonl \
  --b2 /ABSOLUTE/PATH/b2-shard.jsonl \
  --allow-incomplete
```

Only after the frozen run is complete, perform the offline join and analysis:

```bash
python3 -B skill_benchmark/scripts/analyse_rq2b_v7_offline_outputs.py \
  --b1 /ABSOLUTE/PATH/b1.jsonl \
  --b2 /ABSOLUTE/PATH/b2.jsonl \
  --output /NEW/ABSOLUTE/PATH/v7_offline_analysis.json
```

The output path must not already exist. The analyser has no default selector
result path and performs no retrieval, reranking, provider, or metric update
outside the explicitly requested new JSON.

Synthetic self-test (does not read selector results):

```bash
python3 -B skill_benchmark/scripts/test_rq2b_v7_offline_analysis_contract.py
```

## Files

- `b1_runner_output_schema.json`: strict Top-100 first-stage row.
- `b2_runner_output_schema.json`: strict fixed-Top-20 reranker row.
- `analysis_contract.json`: frozen counts, aliases, endpoints, scopes and tests.
- `validate_rq2b_v7_runner_outputs.py`: mechanical label-free validator.
- `analyse_rq2b_v7_offline_outputs.py`: offline label join, scoring and P1-P5.
- `test_rq2b_v7_offline_analysis_contract.py`: synthetic contract regression tests.
