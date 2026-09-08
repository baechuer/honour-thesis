# V7 I1 identity overlay source-only review

State: `PENDING_TWO_INDEPENDENT_SOURCE_ONLY_IDENTITY_REVIEWS`. The failed Phase-7 QA exposed 39 malformed native descriptions: 17 orphan block-marker declarations and 22 literal `>` values. No source or historical representation is overwritten.

Each reviewer reads only one identical local input and the frozen instruction, returns all 39 rows independently, and does not inspect the other lane. Exact agreement can be reconciled mechanically; disagreements go to a source-only coordinator.

Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i1_identity_overlay_review.py --verify`.
