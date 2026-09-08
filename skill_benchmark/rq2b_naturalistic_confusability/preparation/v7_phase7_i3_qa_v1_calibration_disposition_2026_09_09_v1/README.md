# V7 I3 QA v1 calibration disposition

State: `INVALID_CALIBRATION_INSTRUMENT_AND_REVIEWER_RETURNS_NOT_ACCEPTED`. All raw v1 calibration and sample returns are preserved here byte-for-byte, but none is selected as semantic-QA evidence. The v1 scientific threshold is not relaxed. A v2 instrument isolates each synthetic defect, defines code precedence and `affected_fields`, and requires fresh reviewer contexts.

Replay: `python3 -B skill_benchmark/scripts/freeze_rq2b_v7_i3_qa_v1_calibration_disposition.py --verify`.
