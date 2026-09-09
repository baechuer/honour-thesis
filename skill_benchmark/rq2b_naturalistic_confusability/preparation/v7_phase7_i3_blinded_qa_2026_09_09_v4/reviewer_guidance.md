# V7 blinded I1/I3 full-corpus V4.1.3 extraction-fidelity QA v4

Judge only whether native name/description plus the visible evidence faithfully preserve source information that could materially change skill selection. Do not judge any benchmark prompt, target, acceptable set, ranking, or result. Do not use network access.

All rows come from the warning-audited full-corpus V4.1.3 extraction. The packet contains only evidence that the actual I3C/I3-flat serializers retain. A heading or duplicate already omitted by the serializer is not visible and must not be scored. Do not demand exhaustive summarisation: report missing content only when the omitted source fact could distinguish the skill from a plausible neighbour and is not already fully carried by native name/description or another retained span.

Critical codes (critical=true, major=false):
- EVIDENCE_NOT_EXACT_SOURCE_SUBSTRING
- BENCHMARK_OR_ROUTING_LEAKAGE

Major codes (critical=false, major=true), only when selection meaning materially changes:
- WRONG_OPERATIONAL_FIELD
- MISSING_SELECTION_CRITICAL_CONTENT
- NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN
- BOUNDARY_POLARITY_MISCLASSIFIED

Field rules: `dependencies_resources` is for packages, tools, APIs, files, credentials and external resources. `input_preconditions` is for task input/state a caller must supply. A prohibition/not-for statement belongs in `constraints_boundaries`, not workflow. Workflow evidence must itself express an operation; a bare heading or noun fragment is not self-contained.

Error-code precedence prevents double-counting one defect. Critical codes take precedence over majors. For the same visible span, use BOUNDARY_POLARITY_MISCLASSIFIED instead of WRONG_OPERATIONAL_FIELD; use NON_SELF_CONTAINED_OR_GENERIC_SELECTOR_SPAN instead of also calling the same truncated span missing; use WRONG_OPERATIONAL_FIELD instead of also calling that same span missing from its destination field. MISSING_SELECTION_CRITICAL_CONTENT is for a distinct material fact that has no adequate visible carrier.

`affected_fields` names the current defective container for a retained bad/misplaced span. For genuinely missing content, name the destination field where the omitted fact belongs. Do not add both origin and destination merely because a span is misplaced.

Do not report a major for harmless overlap, formatting, an empty source-absent field, or information already fully carried by native name/description. Critical and major are mutually exclusive for a row. A clean row has both false and no codes. Notes must quote exact source evidence for every error and follow the precedence above.
