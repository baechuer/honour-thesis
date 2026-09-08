# V7 pre-outcome analysis freeze

This package seals the 1,077 label-free runtime queries and keeps labels in offline-only ledgers before any V7 selector outcome is observed. Retrieval/reranking code may read only `label_free_query_runtime.jsonl`; it must not read the label adapter or reviewed-neighbour ledger.

Dependency groups are connected components of same-lane reporting-group edges and shared designated-source lineage. No reviewed distractor or model result creates an edge. The exposure ledger conservatively records prior human/result exposure, and the D_q ledger is only a predefined reviewed diagnostic subset.

Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_analysis_freeze.py --verify`
