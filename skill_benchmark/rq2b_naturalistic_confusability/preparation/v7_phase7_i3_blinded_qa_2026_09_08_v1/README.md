# V7 Phase-7 blinded I1/I3 QA

Six 20-row slots form a 120-row sample: 60 reused and 60 fresh. The sampler targets 15 rows per global length quartile within each provenance, then includes all rows from any smaller provenance/quartile cell and deterministically redistributes the shortfall. Fresh rows are cross-assigned away from their extractor group. Reviewers receive only source text, native I1 metadata and actual selector-visible retained evidence.

Replay: `python3 -B skill_benchmark/scripts/build_rq2b_v7_i3_blinded_qa.py --verify`
