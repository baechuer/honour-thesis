# V7 Machine B full raw-collection validation

This is a mechanical collection checkpoint, not a coordinator reconciliation or
an acceptable-set result. It replays the frozen V7 packet/return validator over
the deterministic 341-group Machine-B continuation scope, using only the
documented traceable single-lane reissues. The review coordinator-context gate
remains open, so no target join, final disposition, main/tail designation,
retrieval claim, or library modification is materialised here.

The replay found 340 groups with two validated independent raw returns. One
group remains `STARTED_INCOMPLETE`: both original returns fail the frozen
source-anchor/rationale check and no unused independent reviewer lane remains
for a valid reissue. Its original returns are retained; this checkpoint does
not invent a replacement or treat it as finalised.

