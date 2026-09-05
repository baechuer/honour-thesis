# RQ1b V3 C4A v1.1 Slot-Assignment Amendment

Date: 2026-08-29  
Status: `PROSPECTIVE SOURCE-ONLY REPAIR / NO C4A REBUILD YET / NO CARD OR REVIEW RESULT`

## Problem Addressed

The original C4A schema treated the seven slots as a list but did not say what
to do when one natural-source sentence jointly names the supplied material, the
operation and the resulting artifact. Two independent builders then placed such
sentences in different slots. The issue is under-specified representation
transcription, not an observed field or routing effect.

## Amendment

C4A v1.1 makes slots non-exclusive. The same **exact contiguous** source span
must be repeated in every slot whose explicit inclusion rule it satisfies. It
also gives each slot a fixed inclusion definition: task context; required
material/state; deliverable/state change; action; acceptance test; route-out;
or named resource. `NOT_STATED` means no literal source span satisfies that
specific definition.

## Safeguards

The rule does not permit paraphrase, inference, source identity lines,
prompt/gold consultation, or target-aware tie-breaking. It creates a new C4A
method version only; it does not rewrite or relabel the original Wave 001
packets or their independent draft returns. A fresh pair of source-only
builders and a literal audit are required before C4B.
