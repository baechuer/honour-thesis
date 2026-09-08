# RQ2b-NC V7 sealed coordinator dispatch (V2)

Each coordinator receives only its `*_sealed_packets.jsonl`, its reviewer manifest, and `coordinator_return_schema.json`. It must not inspect the admin ledger, any target join, main/tail role, rank, provenance, historical label, retrieval outcome, or another coordinator's packet file.

For every packet, write one strict-schema return to a coordinator-specific return directory, naming the file by `coordinator_dispatch_id`. The return itself contains only the frozen coordinator schema fields; the dispatch ID is transport metadata and must not be inserted into the return JSON. Copy `reviewer_a_return_sha256`, `reviewer_b_return_sha256`, and `fresh_source_render_sha256` verbatim from the supplied packet.

V2 is the only active coordinator dispatch. The preserved V1 package omitted the two required input-return SHA bindings and therefore must not be used to create coordinator returns.

These inputs are target-blind. They are not decisions, finalised groups, acceptable sets, or experimental results.
