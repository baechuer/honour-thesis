# RQ2b-NC V7 prompt-bound coordinator re-review

Each coordinator reads only its own `*_sealed_packets.jsonl`, own reviewer manifest, and `coordinator_return_schema.json`. It must not inspect the admin ledger, historical V2 packets/returns, target join, rank, main/tail role, provenance, retrieval outcome, acceptable-set artifact, or another coordinator's files.

For every manifest row, create exactly one strict-schema return named by `coordinator_dispatch_id` in the coordinator-specific return directory. Copy all supplied hash bindings verbatim. Use one literal source anchor from the supplied skill. `REOPEN_PACKET` or `CONFIRMED_UNCLEAR` is required when the sealed packet does not support a defensible resolution.

This is prospective target-blind review input only. It does not finalise any group or update the library.
