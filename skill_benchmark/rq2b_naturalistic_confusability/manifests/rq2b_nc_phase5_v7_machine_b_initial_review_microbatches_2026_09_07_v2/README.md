# RQ2b-NC V7 Machine B initial-review microbatches

This is a deterministic, target-blind dispatch for the first 24 of the 341
Machine B groups that have no prior returns. Groups are ordered by SHA-256 of
`batch_id`; a whole six-main plus two-tail V7 packet is the indivisible unit.
Each group occurs once in the reviewer-A assignment and once in the reviewer-B
assignment. Machine ownership never substitutes for the two independent lanes.

Each reviewer may read only the target-blind render named in that reviewer's
assignment and the frozen V7 schema/rubric. They must not inspect a peer
return, the allocation or opaque-token join, target identity, main/tail role,
source provenance, retrieval/reranking output, or metrics. Returns are written
to the frozen lane-specific canonical path and validated before any
reconciliation.

The v1 directory remains as an empty preflight artifact: it made no assignment
file because the selected reusable renders had not yet been materialised. V2
reconstructed those renders from the frozen V7 packet and hash-verified them.
The regenerated target-blind renders are review inputs only and are not part of
this Git dispatch package.
