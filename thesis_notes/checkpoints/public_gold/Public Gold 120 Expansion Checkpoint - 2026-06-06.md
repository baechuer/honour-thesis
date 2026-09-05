# Public Gold 120 Expansion Checkpoint - 2026-06-06

Purpose:

- Expand the externally authored public-gold validation stratum from 82 to 120 prompts.
- Keep public-gold separate from the controlled benchmark so it tests external validity and public-skill messiness rather than clean causal field effects.
- Preserve provider/tool names when they are genuine dependencies, while still rejecting exact skill-name, repository-slug, or copied-card leakage.

## What Changed

- Added 38 public-gold cases in `skill_benchmark/scripts/generate_public_gold_validation.py`.
- Regenerated `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`.
- Regenerated `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Updated public-gold cleanup metadata through `skill_benchmark/scripts/refine_public_gold_label_metadata.py`.
- Rewrote one low-information prompt so the broad combined leakage audit no longer has a high-risk `skill-finder` title cue.

New public-gold coverage includes:

- web quality and SEO;
- API design, API documentation, Claude API, and Admin API implementation;
- security review, best practices, ownership mapping, and monitoring;
- Jira, Linear, Trello, Slack, Teams, Twilio, and webhook automation;
- Mailchimp, social publishing, YouTube, Google Ads;
- proposal/report/job/offer/DocuSign workflows;
- expense tracking, QuickBooks, Stripe, subscription management;
- transcription, podcast, news monitoring, data analysis, and XLSX manipulation.

## Current Public-Gold Composition

- Public-gold prompts: 120.
- Stable strict public-gold cases: 80.
- Stable cases with acceptable alternatives: 37.
- Hard public-label cases: 3.
- Provider/tool-explicit prompts: 64.
- Provider-implicit or generic prompts: 56.

## Validation Results

Public-gold-only audit over 120 prompts:

| Gate | Result |
|---|---:|
| Step 1 integrity | PASS, 120/120 prompts, 0 missing references |
| Step 2 procedural distinctness | PASS, 120/120 prompts |
| Step 2 requirement alignment | PASS, 111/120 prompts |
| Step 3 semantic confusability | PASS, 110/120 prompts |
| Step 4 leakage | PASS, 0 critical and 0 high-risk leaks |

Broad combined audit over controlled, public-gold, and low-information prompts:

| Gate | Result |
|---|---:|
| Step 1 integrity | PASS, 333/333 prompts |
| Step 2 procedural distinctness | PASS, 333/333 prompts |
| Step 2 requirement alignment | WARN, 298/333 prompts |
| Step 3 semantic confusability | PASS, 302/333 prompts |
| Step 4 leakage | PASS, 0 critical and 0 high-risk leaks |

## Interpretation

The public-gold expansion is valid enough for the next selector-evaluation pass. It should still be treated as an external-validity stratum, not merged uncritically into the controlled benchmark.

The current selector results for public-gold are historical because they were run on the older 82-prompt stratum. Before final public-gold claims, rerun:

- local selectors;
- Qwen embedding/reranking conditions;
- SkillRouter embedding/reranking conditions;
- M6-v1-local field-aware reranking where candidate caches are available.

## Caveats

- The 120-case stratum has passed automated construction gates, but only the original 32-case subset has a detailed line-by-line manual adjudication note.
- Some public-gold tasks are naturally high-specificity provider cases. These are useful for external validity but should be reported separately from provider-implicit cases.
- The weak requirement-alignment and weak semantic-confusability prompts should become failure-analysis targets, not automatic removals.
