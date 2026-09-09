# V7 Phase-8 quality review dispatch v1

Every one of the 241 target-blind quality packets is assigned to exactly two distinct reviewer groups. The deterministic pair cycle yields 482 assignments: groups 1 and 2 receive 161 each, group 3 receives 160. Reviewers may read only their packet slots, this README, and the return schema; they must not inspect other reviewer returns, benchmark labels, acceptable sets, retrieval outputs, or metrics.

For each row, choose exactly one decision from `allowed_decisions`, cite only visible source/prompt anchors, and give a specific rationale. Any `BLOCKED_OR_UNCLEAR` or reviewer disagreement goes to a sealed coordinator. A return does not itself create a quality PASS or authorise an experiment.

Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_phase8_quality_review_dispatch.py --verify`.
