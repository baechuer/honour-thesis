# V7 Phase-8 sealed quality coordinator dispatch

The 109 disagreement/unclear packets from the immutable two-review reconciliation are split deterministically across three fresh coordinators (37/36/36). A coordinator may read only its assigned packet file, this README, and the return schema. It must choose one listed allowed decision, cite visible packet anchors, and give a specific rationale. Do not inspect benchmark labels, acceptable sets, retrieval/reranking outputs, metrics, or another coordinator's return.

Write exactly one return row per assignment row, in order, to `returns/coordinator_group_N_return.jsonl`. No return creates a quality PASS; adverse findings still need a separate traceable disposition.

Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_coordinator_dispatch.py --verify`.
