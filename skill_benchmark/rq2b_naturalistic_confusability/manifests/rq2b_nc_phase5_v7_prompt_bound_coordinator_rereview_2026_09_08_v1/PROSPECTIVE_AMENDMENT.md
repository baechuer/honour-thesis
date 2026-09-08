# Prospective amendment: prompt-bound coordinator re-review

## Why this amendment exists

Historical V2 coordinator packets provided two sealed A/B assessments and one source-visible candidate. V2 evidence remains preserved, but `REOPEN_PACKET` outcomes demonstrated that this input did not always support a unique adequacy resolution. This amendment does not overwrite or reinterpret V2.

## What changes

Every re-review packet adds the original V7 target-blind prompt and the frozen adequacy rubric. The return schema binds the prompt render, fresh source render, both selected independent-return hashes, and a hash of the complete coordinator input packet.

## Scope and safeguards

All 832 prior disagreement groups and all 2,291 candidate-level disagreement packets are re-reviewed, so the amendment does not cherry-pick historical reopens. Each group stays whole and is assigned to exactly one coordinator. Coordinators receive no target identity, gold label, source path/provenance, rank, main/tail role, retrieval outcome, metric, acceptable-set status, admin ledger, or peer coordinator material. The six historical gate-docket groups remain outside this scope.

## What this does not authorise

This package does not authorise a target join, group finalisation, acceptable-set creation, library change, K change, retrieval run, metric, or thesis result update. Those require later gates under the master SOP.
