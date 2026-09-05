# RQ1b V3 C4A v1.1 Wave 001 Builder Consistency Hold

Status: `LOCAL ONLY / CALIBRATION HOLD / NO C4B / NO STRICT LABEL / NO SELECTOR OR METRIC`

## Scope

This checkpoint records the first two independent source-only builder returns
for the v1.1 packet family. It is a card-construction calibration record, not
a candidate-cluster result. The builders received only anonymous original
source packets and the v1.1 non-exclusive slot rule. They received no C2
prompt, sealed target, source map, provenance, selector output, embedding,
metric, or online material.

## Observed Problem

The amendment correctly allowed an exact excerpt to appear in multiple slots,
but it did not make the slot *inclusion rules* sufficiently deterministic for
builders. In the document-conversion composition, the same line about reading
the converted Markdown was assigned as `workflow_procedure` by one builder and
as `success_verification` by the other. The latter is not an explicit test,
acceptance condition, threshold, or verification action under the fixed
success/verification definition.

There were similar boundary ambiguities in the legal-agreement composition:
a provided agreement was sometimes recorded as a `dependency_resource`, even
where it was more naturally a required input. These are source-card
preservation issues, not evidence that a routing field is ineffective.

## Disposition

No Wave 001 v1.1 candidate card is canonicalised from these returns. The
attempt does not pass C4A, does not enter C4B, and cannot contribute a strict
gold label, public-cluster count, field frequency, prompt result, selector
input, or metric. The four packet source copies remain valid immutable inputs.

The two original response deliveries for the remaining two packets were not
persisted as response files before their completed workers were closed. They
are therefore treated as unavailable for audit rather than reconstructed or
silently relied upon. This is a transport-record deficiency, not a scientific
rejection of either composition.

## Required Repair Before C4A Resumes

1. Strengthen the builder contract with counterexamples that distinguish a
   required input from a resource and a core operation from explicit
   verification, while preserving exact-source-only and non-exclusive rules.
2. Require every return to be persisted as an immutable JSON response before a
   worker is closed.
3. Run literal-substring and identity-line validation on every persisted
   response.
4. Run a separate source-only slot-rule audit. If two literal-valid cards
   materially disagree in the operational chain, hold that composition for
   repair or exclusion; do not select a convenient version.

## Claim Boundary

This hold says only that the current C4A v1.1 builder instructions do not yet
produce sufficiently consistent slot assignment for card canonicalisation. It
does not estimate public-skill field prevalence, strict-triad yield, semantic
fidelity, human agreement, retrieval accuracy, or any RQ1 effect.
