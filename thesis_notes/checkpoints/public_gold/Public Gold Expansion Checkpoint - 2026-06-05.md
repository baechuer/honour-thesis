# Public Gold Expansion Checkpoint - 2026-06-05

Purpose:

- Expand the public-gold validation stratum so the thesis has more than 200 evaluated prompts across controlled and public-authored skills.
- Clean public-gold labels by separating strict gold skills from documented acceptable alternatives.
- Rerun the benchmark validation gates after expansion.

## Current Scale

- Controlled/evaluated prompts: 137.
- Cleaned public-gold prompts: 82.
- Total evaluated prompt pool: 219.
- Total skill library: 2401 skills.
- Public imported skills: 460.

## What Changed

- Expanded `skill_benchmark/scripts/generate_public_gold_validation.py` from the earlier 32-case public-gold draft to 82 public-gold prompt cases.
- Regenerated:
  - `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`
  - `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`
  - `skill_benchmark/outputs/public_gold_validation_draft.md`
- Cleaned public-gold cases by moving true near-equivalent skills into `acceptable_alternatives`, so validation distinguishes between:
  - wrong but semantically plausible distractors;
  - acceptable near-equivalent public/generated skills;
  - residual hard cases where the label is defensible but difficult for local semantic diagnostics.

## Validation Results

| Gate | Result |
|---|---|
| Step 1 integrity | PASS: 82/82 prompt references resolve; 0 missing references. |
| Step 2 procedural distinctness | PASS: 82/82 prompts; 315/315 pairs have at least one primary procedural differentiator; 288/315 have two or more. |
| Step 2 prompt-specific requirement alignment | PASS with caveats: 79/82 prompts; gold top-1 among listed candidates for 79/82. |
| Step 3 semantic confusability | PASS: 78/82 prompts have at least two plausible alternatives under MiniLM; 220/315 listed gold/alternative pairs are plausible semantic neighbours. |
| Step 4 prompt leakage | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |

Residual Step 2 requirement-alignment hard cases:

- `public_gold_p47_figma_generate_library`
- `public_gold_p65_hf_local_models`
- `public_gold_p81_shopify_automation`

Interpretation:

- These are not automatically bad labels. They are realistic public-skill cases where platform-specific or artifact-specific distinctions are hard for a lightweight embedding diagnostic.
- Keep them for now as public-gold hard cases, but inspect them during final failure-mode analysis.

## Local Selector Results On Cleaned Public-Gold

Use only the `current_full` scale for public-gold. The `core` scale excludes public target skills, so its 0% strict top-1 is expected and not meaningful.

| Method | Strict Top-1 | Accept Top-1 | Strict Top-5 | Accept Top-5 | Strict MRR |
|---|---:|---:|---:|---:|---:|
| M1 BM25 flat | 51.2% | 67.1% | 86.6% | 92.7% | 0.659 |
| M1 TF-IDF flat | 50.0% | 63.4% | 86.6% | 91.5% | 0.649 |
| M2a MiniLM description | 48.8% | 59.8% | 81.7% | 87.8% | 0.626 |
| M2b MiniLM full skill | 35.4% | 47.6% | 64.6% | 72.0% | 0.494 |
| M3 TF-IDF schema | 40.2% | 51.2% | 79.3% | 89.0% | 0.567 |
| M6 BM25 -> schema rerank | 35.4% | 57.3% | 85.4% | 92.7% | 0.558 |
| M6 TF-IDF -> schema rerank | 36.6% | 52.4% | 81.7% | 89.0% | 0.556 |
| M6 MiniLM full -> schema rerank | 32.9% | 51.2% | 74.4% | 85.4% | 0.503 |

## Gold-Label Cleanup Pass

After the first 82-case expansion, three public-gold prompts were residual requirement-alignment hard cases:

- `public_gold_p47_figma_generate_library`
- `public_gold_p65_hf_local_models`
- `public_gold_p81_shopify_automation`

I tightened these prompts to make the procedural target clearer:

- Figma library now explicitly asks for variants, variables, tokens, and theming foundations inside Figma, not app-code implementation or rules-only output.
- Hugging Face local models now explicitly asks for GGUF/llama.cpp-style laptop inference and excludes browser-side Transformers.js.
- Shopify now explicitly asks for Shopify Admin product/order workflows and excludes WooCommerce, Amazon seller, and Stripe payment automation.

Result:

- Step 2 requirement alignment remains an overall PASS at 79/82 prompts and 311/315 passing pairs.
- The three cases remain useful hard cases for final failure-mode analysis rather than labels to silently remove.

## Semantic-Confusability Cleanup Pass

The first 82-case public-gold expansion had a Step 3 warning because several listed alternatives were either true acceptable equivalents or too distant to count as wrong-but-plausible distractors. I revised the public-gold alternative lists to add more realistic near-domain confusions, then removed alternatives that were so broad or close that they weakened gold-label stability.

Result:

- Step 1 integrity remains PASS: 82 prompts and 2401 skills resolve.
- Step 2 procedural distinctness remains PASS: 82/82 prompts and 315/315 pairs.
- Step 2 requirement alignment remains PASS: 79/82 prompts and 311/315 pairs.
- Step 3 semantic confusability is now PASS: 78/82 prompts and 220/315 plausible semantic-neighbour pairs.
- Step 4 prompt leakage remains PASS: 0 critical exact-name leaks and 0 high-risk leaks.

Remaining weak Step 3 prompts:

- `public_gold_p11_setup_pre_commit`
- `public_gold_p12_git_guardrails`
- `public_gold_p60_doc_coauthoring`
- `public_gold_p82_zendesk_automation`

Interpretation:

- These are acceptable residual hard cases. They are high-specificity public tasks where the gold label is naturally clearer than most wrong alternatives.
- Do not keep adding weaker distractors just to maximize Step 3; that would make the benchmark less faithful to realistic public skills.

## Interpretation

- The public-gold stratum is now large enough to serve as an external-validity check, but it should remain separate from the controlled benchmark.
- Flat public-wrapper retrieval is surprisingly competitive on public-gold prompts. This is useful diagnostic evidence: public skills often contain strong lexical routing cues.
- Naive schema/rerank methods underperform on public-gold, suggesting that extracted fields alone are not enough when public skills are broad, implicit, duplicated, or wrapper-like.
- The thesis claim should therefore stay precise: the question is which skill information helps retrieval, under which extraction and representation conditions, not "structure always wins."

## Next Work

- Rerun Qwen and SkillRouter provider conditions on the cleaned 82-prompt public-gold stratum.
- Run public-gold failure-mode analysis, especially where schema/rerank methods lose to flat lexical methods.
- Audit M6-v1 request-field extraction and public-skill field normalization.
- Add statistical uncertainty and paired tests after the final method set is frozen.
