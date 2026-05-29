# Clarification-First Cases

These are intentionally too underspecified for a forced gold-label retrieval test.

Examples:

- "Can you help me with this PDF?"
- "Can you make this document better?"
- "Can you check this data?"
- "Can you review this code?"

For a main-agent downstream test, the correct behavior may be to ask a clarifying question before choosing a skill. These cases should not be scored with strict top-1 retrieval accuracy unless the benchmark also supports an `ask_clarifying_question` outcome.
