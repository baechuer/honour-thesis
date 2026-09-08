# V7 gate-reissue sealed coordinator dispatch

The coordinator may read only `coordinator_reviewer_manifest.jsonl`, `coordinator_sealed_packets.jsonl`, and `coordinator_return_schema.json`. The administrative assignment ledger is sealed. Write one strict-schema return per coordinator dispatch ID to the configured coordinator return directory.
