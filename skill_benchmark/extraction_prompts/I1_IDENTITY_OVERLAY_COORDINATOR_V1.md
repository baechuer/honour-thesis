# V7 I1 source-only identity overlay coordinator V1

Review only the assigned coordinator JSONL. Each row contains the immutable
source and two independent source-only proposals for the same malformed
description. Do not inspect benchmark prompts, targets, labels, acceptable sets,
retrieval outputs, or any material outside the supplied rows. Do not use the
network.

Choose the narrowest accurate description that states the skill's purpose or
activation condition without inventing facts. You may select A, select B, or
write a better source-grounded alternative. Whitespace normalisation is allowed;
semantic additions are not. The supporting evidence must be an exact contiguous
substring of `source_text`, must be a complete scalar/sentence/bullet, and must
not be a heading alone, illustrative prompt, or benchmark-construction metadata.

Return exactly one object per docket, in input order:

```json
{
  "docket_id": "<copy>",
  "skill_id": "<copy>",
  "status": "COMPLETE",
  "decision": "SELECT_A | SELECT_B | SOURCE_GROUNDED_ALTERNATIVE | UNRESOLVED",
  "selected_description": "<nonempty unless unresolved>",
  "source_evidence": "<exact contiguous substring, nonempty unless unresolved>",
  "rationale": "<brief source-only rationale>"
}
```

Do not edit source files or prior returns.

