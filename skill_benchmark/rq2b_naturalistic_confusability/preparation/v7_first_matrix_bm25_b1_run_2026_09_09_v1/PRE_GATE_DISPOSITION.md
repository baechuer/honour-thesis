# Pre-gate disposition

State: `SUPERSEDED_BEFORE_FORMAL_EXECUTION_NOT_SELECTED_AS_SCIENTIFIC_OUTPUT`.

This label-free local BM25 run started before the Phase-7 semantic-QA gate was
closed. The subsequent frozen QA v2 failed with 1 critical and 44 major rows.
It also led to a prospective 39-row I1 identity overlay and a full-corpus I3 V4
re-extraction. Therefore the four output cells in this package do not use the
final representation hashes and cannot enter the formal 36-cell matrix.

The raw 53 MiB `b1.jsonl` is retained locally and hash-bound by
`run_receipt.json`, but excluded from Git because it is superseded,
deterministically regenerable, and not scientific evidence. The README and
receipt are preserved as an audit trail. After the repaired representations pass
fresh blinded QA, all four BM25 B1 cells must be rerun from the final hashes.

No metric, target join, acceptable-set join, or thesis result was produced from
this pre-gate run.
