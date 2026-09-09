# RQ2b-NC V7 Phase-8 quality closure v1

Status: `PASS_PHASE8_QUALITY_CLOSURE_PRE_OUTCOME`.

This versioned package closes the five strict quality-report interfaces used by
the Phase-8 execution root. It replays 3,798 exact source files, 1,077 prompt
identities, and complete 1,077-row dependency and exposure ledgers.

The final semantic evidence comprises six split decisions, 129 cue decisions
(including two traceable blocked-packet reissues), 55 final source-relation
decisions, and 51 prompt near-copy decisions. The 41 avoidable-cue prompts stay
byte-frozen, are excluded from primary inferential summaries, and remain in a
separate sensitivity-only stratum. The 25 source-equivalence edges and three
prompt-dependency edges are prospective offline-analysis overlays only.

No query, source, label, acceptable set, retrieval output, result, or metric is
created or modified. The package is a quality gate, not experiment authority.

Exact replay:

```sh
python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_closure.py --root "$PWD" --output-dir skill_benchmark/rq2b_naturalistic_confusability/preparation/v7_phase8_quality_closure_2026_09_09_v1 --verify
```
