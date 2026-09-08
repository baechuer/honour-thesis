# RQ2b-NC V7 sealed coordinator dispatch

Each coordinator receives only its `*_sealed_packets.jsonl`, its reviewer manifest, and `coordinator_return_schema.json`. It must not inspect the admin ledger, any target join, main/tail role, rank, provenance, historical label, retrieval outcome, or another coordinator's packet file.

For every packet, write one strict-schema return to a coordinator-specific return directory, naming the file by `coordinator_dispatch_id`. The return itself contains only the frozen coordinator schema fields; the dispatch ID is transport metadata and must not be inserted into the return JSON.

These inputs are target-blind. They are not decisions, finalised groups, acceptable sets, or experimental results.
