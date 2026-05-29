# Low-Information Prompt Stress Set

This prompt set is intentionally separate from the main confusability benchmark.

Purpose:

- test whether methods depend too heavily on explicit procedural cue words;
- simulate more realistic user requests where users say "help me with this" instead of naming outputs and constraints;
- inspect whether selectors fall back to broad or domain-neighbor skills when the request is underspecified.

These prompts still have a defensible gold skill, but the wording is deliberately less explicit than the main benchmark. Results should be reported as a stress test, not as a replacement for the main benchmark.

Do not mix these prompts into the main `skill_benchmark/prompts/*.json` set unless gold-label stability is revalidated.
