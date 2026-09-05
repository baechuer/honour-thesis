# Benchmark Residual Validation Reasons - 2026-06-06

This note records the post-refinement status for the controlled and public/non-controlled benchmark strata. The goal was to make validation pass where the issue was prompt wording, metadata handling, or an audit-script artifact, and to document the remaining cases where forcing a pass would weaken benchmark validity.

## What Was Improved

- Updated the requirement-alignment and semantic-confusability audits to distinguish strict gold labels from recorded acceptable equivalents.
- Tightened controlled prompts that had accidental provider cues, weak procedural boundaries, or colon-triggered truncation in the audit preprocessor.
- Tightened public-gold prompts through `skill_benchmark/scripts/generate_public_gold_validation.py`, then regenerated `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`.
- Reduced controlled prompt leakage to zero critical and zero high-risk leaks.
- Kept public skills as imported artifacts; the public wrappers were not rewritten to overfit the benchmark.

## Final Controlled Status

| Gate | Result | Status |
|---|---:|---|
| Step 1 integrity | 201/201 prompts resolve; 2433 skills resolve | PASS |
| Step 2 procedural distinctness | 201/201 prompts; 646/646 pairs have 2+ primary differentiating axes | PASS |
| Step 2 requirement alignment | 199/201 prompts; 657/659 pairs; strict top-1 194/201; gold-or-acceptable top-1 199/201 | PASS with 2 residual cases |
| Step 3 semantic confusability | 182/201 prompts; 516/646 plausible pairs | PASS by rubric threshold, not all-green |
| Step 4 prompt leakage | 0 critical exact-name leaks; 0 high-risk leaks | PASS |

### Controlled Requirement-Alignment Residuals

| Prompt | Gold | Strongest competing skill | Reason not forced to pass |
|---|---|---|---|
| `api_mcp_tooling_p3_webhook_integration_planner` | `webhook-integration-planner` | `webhook-contract-planner` | The two skills are near-duplicates around event selection, signature verification, idempotency, retries, ordering, and dead-letter behavior. The contract skill is arguably a valid answer for much of the prompt. This should be treated as a merge/exclusion/adjudication issue, not a prompt wording issue. |
| `skill_p2_install_existing` | `skill-installer` | `skill-packager` | The gold cue is "install", but using that exact word creates leakage risk. When rephrased as "fetch, enable, and prepare for active local use", the packager skill still scores higher because it also handles existing packages and file verification. This is a scoring-boundary limitation and should be manually adjudicated rather than overfit. |

### Controlled Semantic-Confusability Residuals

There are 19 controlled prompts with fewer than two listed alternatives marked plausible by the embedding diagnostic. The controlled set still passes the rubric threshold because 182/201 prompts pass. These should not all be forced green because:

- several have real all-skill neighbours in top-k but only one of the listed alternatives crosses the current plausibility threshold;
- some are high-precision tasks where the gold skill is naturally clearer than two listed alternatives;
- adding weak alternatives only to satisfy the count would reduce manual cluster quality;
- this diagnostic is construction evidence, not the final selector result.

Recommended treatment: keep them as "semantic residual / audit target" cases and inspect only if they dominate final selector failures.

## Final Public / Non-Controlled Status

| Gate | Result | Status |
|---|---:|---|
| Step 1 integrity | 120/120 prompts resolve; 2433 skills resolve | PASS |
| Step 2 procedural distinctness | 120/120 prompts; 459/459 pairs have at least one differentiator; 417/459 have 2+ primary differentiating axes | PASS |
| Step 2 requirement alignment | 115/120 prompts; 510/517 pairs; strict top-1 98/120; gold-or-acceptable top-1 118/120 | PASS with 5 residual cases |
| Step 3 semantic confusability | 116/120 prompts; 382/517 plausible pairs | PASS with 4 residual cases |
| Step 4 prompt leakage | 0 critical exact-name leaks; 0 high-risk leaks | PASS |

### Public Requirement-Alignment Residuals

| Prompt | Gold | Strongest competing skill | Reason not forced to pass |
|---|---|---|---|
| `public_gold_p81_shopify_automation` | `public-office-shopify-automation` | `public-office-woocommerce-automation`, `public-office-amazon-seller` | Public commerce automation wrappers are highly parallel: platform name plus product/order/inventory/customer workflows. The prompt is human-stable because it explicitly asks for Shopify Admin API, but the wrapper-level embedding cannot strongly separate platform-specific ecommerce skills. |
| `public_gold_p92_security_review` | `public-swebench-security-review` | `security-code-reviewer`, `api-security-threat-reviewer` | The local controlled `security-code-reviewer` is a strong acceptable equivalent and ranks first. The strict public wrapper is broad/checklist-like, so this is a public-label/wrapper granularity issue rather than a bad test prompt. |
| `public_gold_p102_webhook_automation` | `public-office-webhook-automation` | `webhook-contract-planner`, `webhook-integration-planner` | Webhook automation, webhook integration, and webhook contract planning overlap heavily on receivers, signatures, retries, idempotency, and downstream actions. This is a genuine near-duplicate region. |
| `public_gold_p109_job_description` | `public-office-job-description` | `public-office-offer-letter` | HR writing skills share role, compensation, candidate, and hiring vocabulary. The prompt is human-stable as an employer-side job posting, but embedding margin remains too small. |
| `public_gold_p112_expense_tracker` | `public-office-expense-tracker` | `public-office-expense-report` | Expense tracker and expense report are naturally adjacent; the distinction is ongoing register/workflow versus one-off report. The public wrappers are not rich enough for the automated alignment margin to separate them reliably. |

### Public Semantic-Confusability Residuals

| Prompt | Gold | Reason not forced to pass |
|---|---|---|
| `public_gold_p90_claude_api` | `public-anthropic-claude-api` | Provider-specific Claude API integration has one strong public/API neighbour, but not two listed alternatives crossing the embedding plausibility threshold. |
| `public_gold_p91_admin_api_endpoint` | `public-swebench-add-admin-api-endpoint` | This is a highly specific Ghost/SWE-bench endpoint task. It is useful as external-validity noise, but it does not naturally have two close public neighbours in the current library. |
| `public_gold_p94_security_ownership_map` | `public-openai-security-ownership-map` | Security ownership topology is highly specialized. Threat-model and repo-review neighbours are related but not close enough under the diagnostic threshold. |
| `public_gold_p111_docusign_automation` | `public-office-docusign-automation` | DocuSign envelope automation has one related office automation neighbour, but no second strong equivalent without introducing artificial distractors. |

## Interpretation

The benchmark is valid for current controlled and public-gold evaluation, but it is not "perfectly green." That is preferable to overfitting. The remaining controlled residuals identify duplicate/near-duplicate skill definitions and a leakage/alignment tradeoff. The remaining public residuals identify realistic public-skill messiness: broad wrappers, provider-specific duplicates, and high-specificity public skills with too few natural neighbours.

For thesis reporting, controlled clusters should remain the main causal evidence for field/representation comparisons. Public-gold should be reported as external-validity stress testing with strict and gold-or-acceptable scoring separated.
