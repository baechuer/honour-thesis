# Semantic Confusability Repair - 2026-06-16

Purpose: improve Step 3 semantic-confusability coverage after the 401-prompt expansion without weakening gold-label stability.

## What Changed

I added semantically close but procedurally rejectable alternatives to weak prompts, using the Step 3 report's all-skill top-neighbour evidence as the source of candidates. Near-equivalent additions that harmed prompt-specific alignment were removed again.

Files touched include controlled prompt files in API, browser, deployment QA, GitHub/CI, Hugging Face, metrics/observability, office artifacts, office automation, and the two expansion prompt files, plus the public-gold validation/expansion prompt files.

## Before And After

| Gate | Before repair | After repair |
|---|---:|---:|
| Controlled Step 3 semantic confusability | 221/245 | 243/245 |
| Public-gold Step 3 semantic confusability | 137/144 | 144/144 |
| Controlled Step 2 procedural distinctness | 245/245 prompts; 779/779 pairs | 245/245 prompts; 830/830 pairs |
| Public-gold Step 2 procedural distinctness | 144/144 prompts; 555/555 pairs | 144/144 prompts; 575/575 pairs |
| Controlled prompt-specific alignment | 238/245 prompts; acceptable top-1 241/245 | 238/245 prompts; acceptable top-1 241/245 |
| Public-gold prompt-specific alignment | 131/144 prompts; acceptable top-1 138/144 | 131/144 prompts; acceptable top-1 138/144 |
| Controlled leakage | 0 critical / 0 high | 0 critical / 0 high |
| Public-gold leakage | 0 critical / 0 high | 0 critical / 0 high |

## Residual Step 3 Cases

Two controlled prompts remain weak under the MiniLM semantic-construction diagnostic:

- `obs_p2_latency_anomaly`
- `obs_p4_capacity_risk`

Reason retained: both are high-specificity metrics/observability intents. The available library has one strong close neighbour for each, but not two clean semantically close alternatives that are also procedurally rejectable. Forcing these to pass would likely require adding artificial near-duplicate skills, which would inflate Step 3 while weakening gold-label validity.

## Interpretation

The benchmark now has stronger semantic-neighbour coverage while preserving the stricter Step 2 and leakage gates. This is the right trade-off: Step 3 is high enough to support the semantic-confusion stress-test claim, and the remaining residuals are documented instead of overfit.
