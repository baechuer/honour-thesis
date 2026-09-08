# V1 disposition

Status: `EXPLORATORY_SUPERSEDED_BEFORE_PROVIDER_REQUEST`.

This zero-network preflight is retained as audit evidence. It reused the legacy
chunker exactly and exposed a short-boundary progress bug: when an entire chunk
was already shorter than the 256-token overlap budget, the next chunk advanced
by only one character. One I3-flat document therefore produced 767 redundant
lossless windows. No provider request or selector run occurred.

The V2 prospective implementation correction preserves the intended method:
7,500-token maximum exact-substring Markdown windows, at most 256 overlap tokens,
lossless no-gap character coverage, maximum-window cosine, and stable source-SHA
ties. V1 must never be used for provider execution.
