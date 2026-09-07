# Gate memo — no semantic resolution performed

This memo is target-blind. It records why specified groups are withheld from reconciliation; it does not decide adequacy, open a target join, or modify K=6.

## Required user decisions

- `RQ2B-P4-V7-U0323`: historical V7 material records `REOPEN_PACKET`. Decide whether this is a purely local packet/anchor defect that permits a fresh independent A+B reissue on the same frozen packet, or a substantive coverage/construct concern requiring explicit defer/exclude or a prospective amendment. No automatic K=8 change is permitted.
- `RQ2B-P4-V7-U0527`: both raw lanes fail the frozen source-anchor/rationale validator. Preserve both originals. Preferred path: after the U0323 method decision, issue a fresh independent A+B review on the unchanged frozen packet; alternative: explicit defer/exclude. Do not invent anchors, rationales, or adequacy.

## Additional mechanical docket entries discovered in Machine A evidence

- `RQ2B-P4-V7-U0979` and `RQ2B-P4-V7-U1078`: reviewer-B identity/cryptographic binding drift. A valid lane alone is insufficient; retain the raw record and choose a traceable fresh B-lane (or fresh A+B) reissue, or defer/exclude.
- `RQ2B-P4-V7-U1068`: reviewer-B raw return is absent at the frozen Machine-A source commit.
- `RQ2B-P4-V7-U1157`: neither raw return is present at the frozen Machine-A source commit.

The last four are not semantic repairs and are listed because the mechanical replay cannot make them disappear.
