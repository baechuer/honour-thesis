# Microbatch 001 format-repair preservation

Seven coordinator returns had an extra blank line at EOF, causing
`git diff --check` to fail. Their original bytes are preserved as single-line
base64 files (with decoded SHA-256 verification in the ledger), and the
pre-replay final dispositions are preserved as JSON. The review judgments and
canonical output hashes are semantic JSON hashes and were not changed. A
separate V2 reconciliation replay is required because final dispositions bind
raw coordinator-return file hashes.
