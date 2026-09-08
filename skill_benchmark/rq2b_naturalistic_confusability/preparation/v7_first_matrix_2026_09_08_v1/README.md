# V7 first-matrix preparation v1

Status: `PASS_V7_SOURCE_PORTABILITY_AND_MATRIX_PREPARATION_NOT_EXECUTION_SEALED`.

The V7 benchmark/acceptable-set freeze is complete. This package makes its 3,798 primary source documents portable and records the core-first experiment plan. It does not materialise the four representations, authorise inference, create results or reopen labels. The 528-group successor remains deferred.

## Contents

- `first_matrix_conditions.jsonl`: 36 configurations from four representations, three first stages and three ranking endpoints; 12 distinct first-stage runs.
- `fixed_candidate_bridge_conditions.jsonl`: six additional reranker-view comparisons using the exact persisted B05 candidate lists. Their `representation` is the reranker-visible view; candidate generation always uses B05/I2, not that varying view.
- `source_manifest.jsonl`: exact frozen primary Markdown path, SHA-256 and size for each of 3,798 sources.
- `source_paths.txt`: explicit literal Git pathspec intake, not a blanket add instruction.
- `readiness_report.json`: counts, hashes, remaining execution gates and narrow credential-pattern screen.

Every planned configuration has `execution_authorised=false`. Names and proposed Top-20 runtime settings do not substitute for endpoint/model/tokenizer/window/representation verification. The immutable audit remains K=6 plus two tails; full-library retrieval will not be restricted to those eight reviewed candidates.

Final prompt scope is 1,077 (881 strict, 196 multi-acceptable; 714 NC, 363 parent-delta), with 149 exclusions preserved. Prompts are not independent clusters. The statistical dependency/exposure ledger remains a separate required input.

## Exact read-only replay

From a clean checkout of the eventual main preparation commit, with Python 3.10+:

```sh
python3 -B skill_benchmark/scripts/verify_rq2b_nc_phase5_v7_sealed_token_join_acceptable_set_audit.py
python3 -B skill_benchmark/scripts/verify_rq2b_nc_v7_acceptable_set_final_library_freeze.py
python3 -B skill_benchmark/scripts/prepare_rq2b_v7_first_matrix.py --verify
git diff --check
```

All three verifiers were replayed successfully during preparation. The older upstream audit's historical open-gate status is not an instruction to reopen U0323: the downstream final-freeze package explicitly records the later exclusions. Read the final-freeze decision and lineage together.

The preparation verifier recomputes the generated files and their source hashes using only this checkout. It does not contact providers or silently recover missing files. On mismatch, stop and investigate; do not normalise frozen source content.

## Intake, preservation and exclusions

Baseline freeze commit: `fad26f1673afb5d5c15b29a0bfc1d9bd4d9d5c6e`.

At that commit, 631 selected source paths were present; 3,167 were missing. The original research workspace contained all 3,798 exact matches. The preparation script validated the entire bounded intake before restoring only missing files with exclusive creation (`xb`); no existing source or raw return was overwritten. Total source bytes: 19,662,831. This restores portability, not new library membership or new evidence semantics.

Source authority is the Phase-3 source union and Phase-4 path-resolution ledger referenced in `readiness_report.json`. The manifest retains upstream provenance metadata; this package does not independently assert that every auxiliary file or licence text has been byte-replayed. No fetched model or arbitrary download is included.

The narrow credential-pattern scan found no unresolved flags. One already-versioned Kubernetes example contains a literal ellipsis-only private-key placeholder; it is recorded as an example, not a real key. Pattern screening is not a guarantee against all forms of sensitive content.

Excluded from this commit intake (left untouched): `.env`/`.env.*` and local credentials; `.venv*`, `__pycache__`, `skill_benchmark/cache/`, `skill_benchmark/runtime/provider_cache/`; `tmp/`, `thesis_latex/tmp/`, local scratch outputs; `skill_benchmark_snapshot*.tar.gz` and other archive snapshots; downloaded model weights; the two example theses under Downloads; and all unrelated untracked files. Existing `.gitignore` already covers the principal runtime/cache/archive paths. Only frozen-ledger primary-source paths, this package/script, the design spec/roadmap and two current tracker banners are staged in the new preparation commit. Prior V7 reconciliation commits retain their original scope.

## Next step, not an inference command

Finish V7-wide I1/I2/I3C/I3-flat materialisation and semantic QA, seal the dependency/exposure and model/length/cost inputs, then run B36 and C6. Evaluate wiki/graph/tree feasibility afterwards; design the optional small system last. See `thesis_notes/current/RQ2 First Matrix and Architecture Extension Roadmap - 2026-09-08.md`.
