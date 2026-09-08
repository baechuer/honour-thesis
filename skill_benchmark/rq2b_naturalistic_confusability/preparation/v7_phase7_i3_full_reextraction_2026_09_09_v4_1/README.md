# V7 Phase-7 I3 full re-extraction V4.1

State: `PENDING_3798_SOURCE_ONLY_V4_1_EXTRACTIONS`. V4 was superseded before any worker output. V4.1 changes only false-positive safeguards for source-internal task language; all 3,798 source bytes, identities, seven fields, 95 batch memberships, V7 prompts, K=6 packets, labels and QA thresholds are unchanged.

Workers read only their assigned `i3v41_input_NNN.jsonl` and `I3C_SUBAGENT_EXTRACTION_V4_1.md`. Replay: `python3 -B skill_benchmark/scripts/prepare_rq2b_v7_i3_full_reextraction_v4_1.py --verify`.
