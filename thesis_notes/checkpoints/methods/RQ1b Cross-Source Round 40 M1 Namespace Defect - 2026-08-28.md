# RQ1b Cross-Source Round 40 M1 Namespace Defect

**Date:** 2026-08-28  
**Status:** `QUARANTINED_BEFORE_C0B_NOT_A_CLUSTER_OR_RESULT`

## Defect

The Round 40 staging runner correctly used `round40-m1-*` destination
directories, but inherited an unedited `--skill-prefix r39m1-*` literal from
the Round 39 runner. The bytes, pinned commits, path selection, source hashes,
and staging procedure were unaffected; the generated `skill_id` namespace was
not safe to use beside Round 39.

## Containment

- The defect was detected before any C0B source screen, prompt, label,
  blinded review, retrieval, model/provider call, metric, or result.
- Five C0A agents were stopped. Their metadata-only outputs were not merged or
  admitted; one returned proposal per completed lane is invalid solely because
  it names the quarantined identifiers.
- The 46 affected stage directories and their first inventory remain preserved
  under a Round 40 namespace quarantine rather than being deleted.

## Repair

The runner now emits `r40m1-*` identifiers. It reuses the exact same Round 40
M0 roots, pinned commits, 3--64 path-bound selection, and local byte source
trees, but writes a new corrected checkpoint/inventory. C0A resumes only from
that corrected inventory after its hashes and namespace are locally audited.

## Claim Boundary

This is a source-identity correction. It creates no empirical RQ1b evidence
and makes no claim about source suitability, cluster validity, or routing.
