# V7 Phase-7 I3 full re-extraction V4

State: `PENDING_3798_SOURCE_ONLY_V4_EXTRACTIONS`. This prospective repair was triggered by the frozen blinded-QA v2 failure. It re-extracts all 3,798 source-hash-unique artifacts under the same seven-field representation schema; no historical semantic payload is selected.

There are 95 indivisible batches (94 x 40 rows, one x 38), deterministically assigned to three extraction groups. Workers may read only their input and `I3C_SUBAGENT_EXTRACTION_V4.md`. No benchmark prompt, target, label, acceptable set or result is permitted.

Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i3_full_reextraction_v4.py --verify`.
