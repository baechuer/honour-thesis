# Prospective V7 SkillRouter embedding window amendment

State: `AWAITING_EXPLICIT_USER_APPROVAL_NOT_EXECUTION_AUTHORITY`. This source-only audit found 30 of 15,192 document-representation rows above the tested 7,500-token host ceiling: I2=28, I3C=1, I3-flat=1, I1=0. The proposal uses exact lossless 7,500-token windows, 256-token overlap and max-window cosine only for those rows. It never truncates or excludes a candidate.

This package does not authorise model execution. Replay: `.venv-rq2b-v7/bin/python -B skill_benchmark/scripts/build_rq2b_v7_skillrouter_window_amendment.py --verify`.
