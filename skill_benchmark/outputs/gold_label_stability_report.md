# Gold Label Stability Report

This report records the Step 4 manual review of the remaining unstable or weak Step 2 cases.

## Overall Status

- Step 4 gold-label stability status: **PASS**
- Reviewed cases: 7
- Cases kept after clarification: 7
- Cases removed as ambiguous: 0
- Step 2 after gold-label refinement: 67/67 prompts pass, 186/186 gold/alternative pairs pass
- Step 2 after later prompt-leakage reduction: 65/67 prompts pass, 183/186 gold/alternative pairs pass
- Step 3 after refinement: 61/67 prompts pass, 162/186 gold/alternative pairs remain semantically plausible

Interpretation: the reviewed cases are gold-label stable after prompt and skill-boundary refinements. The alternatives remain useful near-neighbor distractors, but the gold skill can now be defended procedurally.

## Reviewed Cases

| Prompt | Gold Skill | Stability Decision | Change Made |
|---|---|---|---|
| `web_p5_frontend_debugging` | `frontend-debugger` | Stable | Clarified that the deliverable is source-level cause plus smallest code patch, not pass/fail UI behavior. |
| `doc_p2_document_rewriter` | `document-rewriter` | Stable | Removed negated alternative terms and stated the positive requirement: continuous revised prose in the same document form. |
| `obs_p5_root_cause` | `metrics-root-cause-diagnoser` | Stable | Clarified causal driver attribution and added boundaries against anomaly-only and capacity-forecast interpretations. |
| `reply_p2_polish_supervisor` | `reply-polisher` | Stable after boundary clarification | Marked the quoted draft as source text, and sharpened the distinction between polishing an already-written reply and drafting a new academic reply. |
| `sec_p2_security_code_review` | `security-code-reviewer` | Stable | Clarified that the artifact is a single handler implementation and that the target is code-level security flaws, not an end-to-end auth flow review. |
| `sec_p1_threat_model` | `security-threat-modeler` | Stable after leakage reduction | The prompt is a general pre-implementation security design exercise; auth and privacy alternatives are plausible but narrower. |
| `skill_p2_install_existing` | `skill-installer` | Stable after leakage reduction | The prompt asks to add a public catalog capability to the active local library; packaging is a plausible but wrong distribution-oriented alternative. |

## Method Notes

- Cases were not rewritten to make alternatives unrelated. The goal was to preserve semantic confusability while making the procedural reason for the gold label explicit.
- Negated alternative wording was reduced where it was causing embedding noise.
- Source payloads such as quoted reply text were separated from routing intent so the validation script scores the instruction rather than incidental content.
- Some alternatives remain reasonable near-neighbor confusions; this is desirable for the benchmark.

## Follow-up Status

Prompt-leakage analysis has now been completed. The benchmark has 0 critical exact-name leaks and 0 high-risk title/phrase leaks after prompt rewriting. The offline selector/evaluator harness is now implemented, and the current 466-skill scale condition shows useful retrieval pressure. The next step is stronger embedding/reranking baselines and a fresh M0 progressive-disclosure run on the current prompt/skill version.
