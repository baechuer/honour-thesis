# V7 Phase-7 I3 merged artifacts

This package combines 2,430 source-SHA-identical unambiguous V3 extractions with 1,368 fresh source-only V7 extractions. All 3,798 rows pass schema, identity, exact-source-substring and I3C/I3-flat evidence-multiset checks.

The artifacts are not yet authorised for formal selectors: the historical V3 semantic-QA attempt is not inherited, and a fresh current blinded, stratified semantic QA remains mandatory.

Replay: `python3 -B skill_benchmark/scripts/merge_rq2b_v7_i3.py --verify`
