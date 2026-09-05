# RQ1 Public Original-Document Redaction Feasibility Closure

Date: 2026-08-31

## Scope

This is a local, source-only feasibility audit of selective information removal
from complete public original skill documents. It is not the completed
derivative public-card RQ1b selector experiment.

## Protocol Path

1. Hash-verified originals from the frozen 76-composition corpus were parsed
   by source-only agents, with no prompt, gold-label, selector, or result text.
2. Conservative first-pass maps were materialised and passed exact-diff/hash
   audit.
3. A stratified prompt/label-blind residual review covered 42
   composition-condition items spanning seven fields and three field groups:
   `35 RESIDUAL_FOUND / 7 CLEAR`.
4. The 35 residual items received a source-only supplemental mapping pass:
   `32 SUPPLEMENTAL_MAPPED / 3 UNSAFE_MIXED_CARRIER`; one otherwise mapped item
   then encountered an edit conflict during rematerialisation.
5. The 31 rebuilt masks passed an independent exact-diff/hash audit (104
   candidate documents; zero technical failures).
6. A fresh prompt/label-blind reviewer saw only these rebuilt masked documents:
   `28 RESIDUAL_FOUND / 3 CLEAR` across 31 items.

## Decision

The public-original field-removal intervention is **not suitable for retrieval
scoring** under its current no-capability-expansion and explicit-residual rules.
Three clean items are not a credible single-field or group denominator. No
BM25, Qwen, hosted SkillRouter, API call, selector result, human review packet,
or thesis LaTeX/PDF result was produced.

This is not evidence that a field has no routing value. It is evidence that a
natural full skill document repeats operational facts in multiple sections, so
reliably removing only one field while retaining a fair competing document is
often infeasible. The existing RQ1a controlled suites and derivative public-card
RQ1b results retain their own stated claim boundaries.

## Evidence

- `skill_benchmark/rq1_public_original_removal_v2/residual_submissions/canonical/INGESTION_STATUS.json`
- `skill_benchmark/rq1_public_original_removal_v2/remediation_submissions/canonical/INGESTION_STATUS.json`
- `skill_benchmark/rq1_public_original_removal_v2/audit/remediated_mask_technical_audit.json`
- `skill_benchmark/rq1_public_original_removal_v2/residual_recheck_submissions/canonical/INGESTION_STATUS.json`
