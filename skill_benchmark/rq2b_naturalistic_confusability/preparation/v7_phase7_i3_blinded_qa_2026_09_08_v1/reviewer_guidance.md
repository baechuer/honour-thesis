# V7 blinded I1/I3 extraction-fidelity QA

Judge only whether native name/description plus the visible evidence faithfully preserve source information that could change skill selection. Do not judge any benchmark prompt, target, acceptable set, ranking, or result. Do not use network access.

The packet contains only evidence that the actual I3C/I3-flat serializers retain. A heading or duplicate already omitted by the serializer is not visible and must not be scored.

Critical codes (critical=true, major=false):
- EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING
- BENCHMARK_OR_ROUTING_LEAKAGE

Major codes (critical=false, major=true), only when selection meaning materially changes:
- WRONG_OPERATIONAL_FIELD
- MISSING_SELECTION_CRITICAL_CONTENT
- NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN
- BOUNDARY_POLARITY_MISCLASSIFIED

`dependencies_resources` is for packages, tools, APIs, files, credentials and external resources. `input_preconditions` is for the task input/state a caller must supply. A prohibition/not-for statement belongs in `constraints_boundaries`, not workflow. Workflow evidence must itself express an operation; a bare Step heading or noun fragment is not self-contained.

Do not report a major for harmless overlap, formatting, an empty source-absent field, or information already fully carried by native name/description. Critical and major are mutually exclusive for a row. A clean row has both false and no codes. Notes must quote exact evidence for every error.
