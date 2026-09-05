# Context Scale Audit

Date: 2026-05-28

This note records whether the current benchmark actually stresses context-window scale.

## Current Skill Counts

- Active benchmark skill library: 2089 `SKILL.md` files.
- Historical 1006-skill Nanobot workspace still exists as the previous full M0 export.
- Core M0 workspace/result is historical: 67 evaluated prompts against the old controlled core.

## Active 2089 Representation Scale

The active 2089-skill condition strengthens the scalability argument.

Approximate selector-visible token counts from the local evaluator:

| Representation | Approx selector-visible tokens |
|---|---:|
| R1 flat metadata | 105,272 |
| Full `SKILL.md` documents | 1,065,572 |
| M3 schema cards | 590,432 |
| M6 flat shortlist + schema rerank | 111,268 |

Interpretation:

- Compact metadata exposure is now meaningfully large, though still potentially feasible for some 200k-context models.
- Full artifacts and rich structured cards are far beyond practical single-context exposure.
- The 2089-skill condition is therefore a stronger near-context-limit setting for progressive disclosure and a clear context-overflow setting for full skill artifacts.

The older 1006-skill measurements below are kept as historical context.

## Nanobot Progressive-Disclosure Context Size

Nanobot progressive disclosure does not load all full `SKILL.md` files into the initial system prompt. It injects an XML skill summary containing:

- skill name;
- description;
- location;
- availability flag;
- missing requirements, if any.

Measured using Nanobot's `SkillsLoader.build_skills_summary()` logic:

| Workspace | Skill entries in summary | Summary chars | Summary words | Rough token estimate |
|---|---:|---:|---:|---:|
| Core M0 workspace | 75 | 27,751 | 2,049 | about 7k tokens by chars/4 |
| Full 1006-skill workspace | 1013 | 368,606 | 21,773 | about 92k tokens by chars/4 |

## Other Representation Sizes

| Representation | Words | Interpretation |
|---|---:|---|
| R1 name + description only | 17,343 | Definitely fits a 200k context window. |
| R1 flat metadata JSONL text field | 21,367 | Fits a 200k context window. |
| All full `SKILL.md` files | 292,427 words / 1,987,067 chars | Does not fit comfortably in 200k tokens. |
| R2 structured procedural JSONL | 323,499 words | Does not fit comfortably in 200k tokens. |

## Interpretation

The current 1006-skill benchmark is a valid **semantic/procedural scale** benchmark: it creates many plausible candidates and shows that retrieval methods differ under semantic confusion.

It is not yet a strong **context-overflow** benchmark for modern 200k-context models if the system only exposes compact name/description metadata. The full Nanobot summary is roughly 92k tokens by a chars/4 estimate, so it likely fits in a 200k window.

However, the full skill artifacts and structured procedural representations exceed a 200k context budget. This supports the need for retrieval or candidate subsetting before full artifact loading, but not necessarily before compact metadata exposure at the current 1006-skill scale.

## Consequence for Thesis Claims

Avoid claiming:

> The 1006-skill benchmark proves that all skill metadata cannot fit in context.

Safer claim:

> At 1006 skills, compact metadata may still fit in a large context window, but semantic competition already degrades selection. Full skill artifacts and richer structured representations exceed practical context budgets, so retrieval remains necessary when the system must preserve procedural information rather than only expose short descriptions.

## What This Means for Next Experiments

There are two possible scale regimes:

1. **Semantic scale regime**: keep 1006 skills and analyze retrieval accuracy under semantically confusable candidates.
2. **Context stress regime**: increase to roughly 3000-5000+ compact skill cards, or inflate realistic metadata, to test whether progressive disclosure itself becomes context-expensive under 200k windows.

Recommendation:

- Use the active 2089-skill benchmark for scale-sensitive semantic/procedural retrieval comparisons.
- Keep the 1006-skill benchmark as historical comparison for older provider results.
- Do not mix the context-overflow claim with the semantic-confusion claim: compact metadata may still fit, but full artifacts and richer procedural representations do not.

Historical 1006-skill update:

A 2000-skill condition may already be close to the practical limit for Nanobot-style XML progressive disclosure. The current 1006-skill Nanobot summary is roughly 92k tokens by chars/4 estimate. If summary size scales approximately linearly, a 2000-skill summary would be roughly 180k tokens before the user request, tool schemas, memory, and other system context. Therefore, 2000 skills is a sensible near-context-limit condition for progressive disclosure, even if plain name+description text still fits more comfortably.

## M0 Status

Nanobot progressive-disclosure M0 has been run on the controlled core workspace only.

Current M0 core result:

- 67 evaluated prompts.
- 61.2% strict top-1.
- 64.2% strict any-hit.
- 31.3% no explicit skill loaded.
- Mean full skill docs loaded: 0.78.

Full 1006-skill Nanobot M0 has **not** been run. The full workspace exists at:

`skill_benchmark/runtime/m0_workspaces/current_full`

The result directory exists but is empty:

`skill_benchmark/runtime/m0_results_current_full`

Running full M0 would be useful as a context/cost stress test, but it is not necessary for the main retrieval-only comparison unless we explicitly want to evaluate normal Nanobot behavior at 1006 visible skill cards.
