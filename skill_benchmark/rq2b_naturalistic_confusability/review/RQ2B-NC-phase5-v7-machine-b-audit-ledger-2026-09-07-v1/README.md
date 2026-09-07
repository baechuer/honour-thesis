# RQ2b-NC V7 Machine B existing-return audit ledger

This versioned ledger is the Machine B-only replay of the frozen V7 protocol.
It does not open the opaque token join, reveal target identities, decide an
acceptable set, or make a retrieval or library-level claim.

`validated_existing_return_pairs.jsonl` preserves one row for each pre-existing
two-return pair. A failed lane is recorded as invalid and reissue-required; its
original return remains in place and is not overwritten. The ledger was built
only after the V7 execution freeze and sealed audit inputs passed hash replay.

The authoritative inputs are bound in `summary.json`: the V7 Machine B handoff
manifest and the frozen strict unified blind protocol. Current reconciliation
evidence is in the versioned Machine B reconciliation root named in the
summary. Three older partial reconciliation directories are preserved as
historical artifacts only; they are not adopted as current reconciliation
evidence.

Replay validation uses the frozen protocol's `validate` subcommand for each
recorded batch and lane. Before any reissue or finalisation, recheck the
manifest hash, the raw-return hash recorded in the ledger, the return schema,
target blindness, and the complete K=6 plus two-tail packet binding.
