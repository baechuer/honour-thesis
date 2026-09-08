# V7 Phase-7 blinded I1/I3 QA v2

V2 retains the exact 120-row v1 source-only sample and cross-assignment, but replaces the ambiguous synthetic calibration instrument with isolated cases, explicit error-code precedence and a defined `affected_fields` convention. The scientific threshold is unchanged. V1 returns remain preserved but are not accepted.

Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa_v2.py --verify`.
