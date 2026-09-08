# V7 I3 V4.1.1 validator amendment

V4.1 incorrectly treated the word `unsupported` as a route-out even when a skill legitimately returns `unsupported` as one possible assessment label. Before output selection, merge, QA or selector execution, V4.1.1 narrows only that automatic guard. It preserves the original output and replays every attempt under the corrected validator.

Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_v4_1_1_validator_amendment.py --verify`. Focused tests: `python3 -B skill_benchmark/scripts/test_validate_rq2b_v7_i3_v4_1_1_batch.py`.
