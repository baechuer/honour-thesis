# Thesis Progress Tracker

> **RQ1 SCIENTIFIC CLOSURE (2026-09-04).** RQ1 is scientifically complete and thesis-integrated. It is answered by (1) 350 controlled field-isolation clusters plus the separate examples/tests negative control, and (2) a public original-document removal experiment over 82 source compositions. The scored public freeze contains 1,078 composition-family cases, 2,156 prompt rows and 4,312 ranking rows per retriever. Use condition and success/verification are stable individual effects under both BM25 and Qwen; task specification and execution/verification are stable joint-group effects under both. Other individual fields are retriever-conditional and boundary/not-for has no stable positive strict Top-1 effect. The 2026-08-30 derivative field-card result is historical sensitivity only. The unblinded researcher-confirmation workspace at `skill_benchmark/rq1_human_review/2026-09-04/` is complete: all 350 controlled, 194 public-gold and 402 public-removal rows were approved (`946/946`). Frozen labels or intended transformations were visible, so this is not blinded or independent annotation. No further RQ1 experiment is required under the current scope. Freeze the canonical evidence; remaining RQ1 work is final submission editing, and the active research focus moves to RQ2. Canonical index: `thesis_notes/current/RQ1/README.md`. HD/Medal readiness: `thesis_notes/current/RQ1/reviews/RQ1 HD and Medal Readiness Assessment - 2026-09-04.md`. Dated entries below are preserved as history and do not override this block.

## Historical RQ1 Timeline (Non-Canonical)

The dated records below preserve how the method changed. They are not current instructions or thesis-facing evidence unless the canonical RQ1 index explicitly cites them.

> **2026-08-31 RQ1 public-corpus counting policy.** Use the 82-entry
> source-hash-deduplicated composition registry as the single intake frame for
> future public RQ1 work. Do not treat it as 82 scored clusters: the completed
> public-card result is exactly 46 scored compositions / 99 strict routing
> families / 198 prompts, while 87 / 174 denotes the historical native-V2
> subset only. New discovery must be merged into a future registry release
> before one complete-case scoring subset is frozen; it cannot be appended to
> an existing result. Policy:
> `thesis_notes/current/RQ1/supporting/RQ1 Public Corpus Consolidation Policy - 2026-08-31.md`.

> **2026-08-31 RQ1 complete-original redaction extension -- closed as a
> feasibility audit, not a selector result.** A prompt/label-blind,
> source-line field-removal protocol was tested on complete public original
> documents to see whether natural artifacts could support the same field-removal
> contrast as derivative public cards. It could not: the first residual gate
> found 35 residual items out of 42; after supplemental mapping and exact-diff
> reconstruction, the fresh residual gate found 28 residual items out of 31
> rebuilt masks, leaving only three clear items. No retrieval, Qwen embedding,
> external transfer, hosted compute, human review packet, or thesis result was
> produced. The extension therefore neither strengthens nor weakens the RQ1a/
> public-card RQ1b routing claims; it records a real limitation of selective
> field deletion in complete natural skill documents. Evidence:
> `thesis_notes/checkpoints/methods/RQ1 Public Original-Document Redaction
> Feasibility Closure - 2026-08-31.md`.

> **2026-08-30 RQ1 final result status -- thesis integration complete, author
> review recorded.** RQ1a is reported as seven researcher-authored,
> mechanically rubric-checked and author-reviewed controlled field-isolation
> suites. The cluster-level analysis averages prompt variants within each of 50
> clusters and gives positive hidden-to-exposed Top-1 bootstrap intervals for
> every field/retriever combination. The 350-row ledger retrospectively records
> iterative author review: 350 retained / 0 excluded. This is not independent
> or blinded annotation. Protocol and receipt:
> `thesis_notes/archive/RQ1/original-document-lineage/RQ1a Human Review Protocol - 2026-08-30.md` and
> `skill_benchmark/rq1a_field_discriminability/human_review_2026-08-30/author_review_confirmation_receipt.json`.

> **2026-08-30 RQ1b final public-artifact finding -- thesis integration
> complete.** Keep three evidence layers distinct: (1) the 1,099-artifact
> public-source discovery frame supplies source provenance and candidate
> material, not a corpus-wide manual field audit; (2) the 46-composition,
> 99-family, 198-prompt candidate-synchronous public-card removal experiment
> is the scored RQ1b result; and (3) the original-only naturalistic curation
> records remain feasibility/no-selector evidence. In the scored public-card
> result, no statistically reliable single-field Top-1 or MRR effect is
> detected for BM25 or Qwen because every corresponding composition-bootstrap
> interval includes zero. This qualifies RQ1a rather than overturning it:
> controlled fields can be sufficient when isolated, while source-grounded
> derivative cards retain redundant and joint evidence. The joint mask strata
> remain separately denominated supporting evidence. Final sources:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/` and
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/`.

> **2026-08-30 RQ1b result/failure analysis -- user-approved and complete.**
> The completed single-field primary matrix and joint-group supporting matrix
> now enter a frozen, local-only synthesis. It will report absolute performance, paired
> effects, `FULL -> MASK` routing regressions, mask recoveries, rank/margin
> weakening, cross-retriever agreement and case-level evidence without changing
> any scientific input. The primary and supporting strata remain separate. The
> closure reviewed every predeclared cross-retriever-concordant transition: 13
> regressions and 3 recoveries. Eleven regressions are explained by a directly
> intent-matching removed field/group, while two are explicit retrieval-
> sensitivity counterexamples in which unmasked task information already
> distinguishes the target; all three recoveries show residual-field redundancy.
> Thesis LaTeX/PDF remains unchanged pending the researcher's review. Evidence:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/`.
> SOP: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Result Synthesis and Failure
> Analysis SOP - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 joint-group supporting analysis.** The primary
> V2+V3 result remains the single-field availability analysis. A separate
> supporting extension now tests three information sets, with every candidate
> in a composition receiving the same marker in every field of that set. Local
> BM25 has completed after strict provenance, mask and denominator validation.
> The experiment has separate denominators rather than one pooled score: task
> specification `85 families / 170 prompts / 41 compositions`,
> execution/verification `89 / 178 / 44`, applicability/capability `82 / 164 /
> 41`. Only the task-specification Top-1 interval excludes zero; margin loss is
> stable for all three groups. Treat this as evidence about jointly available
> information, not proof that any one field is causal. The Qwen twin is now
> complete: it sent precisely those 36 new cards, reused all 24 V3 query and 12
> `FULL` cache entries, and completed four no-retry calls. Qwen shows a stable
> execution/verification loss across Top-1, MRR and margin; task specification
> is stable for MRR/margin but not Top-1; applicability/capability remains
> inconclusive. See
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Joint Group Extension Amendment -
> 2026-08-30.md`.

> **2026-08-30 RQ1b final public-corpus consolidation and V3 accounting
> correction.** `skill_benchmark/rq1b_final_public_corpus_v1/` is now the
> canonical stratified registry. It records 76 historical cross-source C6
> candidate compositions / 408 cases, the nested V2 scored field-card subset
> of 48 compositions / 87 strict-preserved routing families / 174 prompts, and
> six direct V3 C6 parent compositions / 32 cases (four complete, two partial).
> The source-hash provenance union is 82 compositions, but is **not** a pooled
> retrieval denominator. Earlier prose in this tracker that states V3 as
> `37 compositions / 231 cases` is superseded: the number inherited the former
> cross-source running count and cannot be reconstructed from V3 C6 files.
> V2 is the only scored public-card RQ1b stratum; V3 remains curation-only.
> Wave 039 discovery drafts are closed without C1 and excluded from the final
> registry. Evidence: `skill_benchmark/rq1b_final_public_corpus_v1/` and
> `thesis_notes/checkpoints/methods/RQ1b Final Public Corpus Registry And V3
> Accounting Reconciliation - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 complete-triad integration.** The four reproducible
> direct V3 C6 triads with all six target-by-variant cases are now harmonised
> into V2-compatible seven-field card/mask artifacts. Two V3 four-case parents
> remain quarantined. This creates a prospective 52-composition / 99-family /
> 198-prompt matrix, but does not overwrite V2 or create a new selector result.
> The next gate is a separately logged local BM25 extension, followed by a
> fresh exact-payload approval before any Qwen transfer. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Complete-Triad Integration Amendment - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 selector execution prepared.** The execution
> amendment reuses the immutable completed V2 rows only after hash, freeze and
> coverage verification, while scoring solely the imported four-V3-triad
> extension (192 rows per retriever). BM25 is local; Qwen first produces an
> exact local payload and must receive a fresh scope-specific text-transfer
> approval before any provider call. Native V2, imported V3 and a supplemental
> harmonised 99-family view remain separately labelled. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Selector Execution Amendment - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 BM25 complete; Qwen preflight sealed.** The local
> runner verified and reused 1,392 V2 BM25 rows, computed only 192 imported-V3
> rows, and produced a correctly stratified 1,584-row package. Imported V3
> `FULL` BM25 Top-1 is 0.750; input/precondition and workflow/procedure are
> the largest descriptive perturbations, but this 12-family stratum is
> supplemental rather than a replacement for V2's field-eligible primary
> result. Qwen preflight has zero calls and seals 120 V3-only texts (96 cards,
> 24 prompts), at most 13 no-retry requests. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V2 Plus V3 BM25 And Qwen Preflight - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 Qwen extension complete.** The separately authorised
> Qwen `text-embedding-v4` run sent exactly 120 preflighted V3 texts (96 cards,
> 24 prompts), completed 13/13 no-retry calls and persisted the new embeddings.
> It scores 192 imported-V3 rows and reuses 1,392 frozen V2 rows by verified
> reference. Imported V3 `FULL` gives Top-1 0.7917 and MRR 0.8889; the
> separately labelled 99-family harmonised supplemental view gives Top-1
> 0.8485 and MRR 0.9184. This does not change V2's primary field-eligibility
> estimate and has not been written into thesis LaTeX/PDF. Evidence:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30/qwen/`.

> **2026-08-30 RQ1b final unified public-artifact result.** V2 and V3 are now
> one final candidate-synchronous field-removal experiment. The source corpus
> contains 52 frozen composition artifacts, but only 46 contribute strict
> routing families; the scored experiment is therefore 46 compositions, 99
> strict families, 198 prompts, eight conditions and 1,584 rows per retriever.
> Direct/paraphrase and multiple families are first averaged within a
> composition, followed by a 5,000-replicate paired composition bootstrap.
> Qwen `FULL` is 84.85% Top-1 / 0.918 MRR; BM25 `FULL` is 69.19% / 0.832. All
> unified single-field Top-1 and MRR intervals include zero, so the final RQ1b
> result reports directional public-artifact field-availability effects, not a
> universal independent benefit from any one field. V2/V3 is retained only as
> source provenance, not as two experiment denominators. Evidence:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`.

> **2026-08-30 RQ1b complete metric ledger and bounded conclusion.** A final
> local-only ledger now records all retained selector outcomes: absolute Top-1,
> MRR, rank, native margin, raw paired changes, composition-level bootstrap
> intervals and Top-1 transitions. The unified 46-composition/99-family
> single-field experiment has no stable Top-1 or MRR field effect: every such
> CI includes zero. It nevertheless shows positive margin evidence for several
> BM25 fields (input, workflow, success and boundary) and Qwen success. The
> V2-only joint masks preserve their proper 70--77-family eligibility subsets:
> each raw Top-1 comparison falls after group removal, with stable margin loss
> for all BM25 groups and Qwen task specification. The defensible conclusion is
> distributed/redundant field evidence in natural public skill cards, not a
> universally decisive isolated field. Evidence:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_final_result_ledger_2026-08-30/`.

> **2026-08-30 RQ1b V2+V3 joint-group extension prepared.** To test the
> distributed-information interpretation directly, the three V2 joint masks
> will be materialised over the four complete V3 triads. This creates an
> extended supporting analysis of task specification (85 families),
> execution/verification (89) and applicability/capability (82). Local BM25
> may run after materialisation validation; Qwen is separately gated because it
> requires 36 newly rendered candidate-card texts. No thesis result has been
> written. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Joint Group Extension Amendment - 2026-08-30.md`.

| Workstream | Current status | Completed evidence | Boundary / next gate |
| --- | --- | --- | --- |
| RQ1b V3 Wave 039 broad public intake and source-only review | `M0--M3 + PROVENANCE PASS / 153 CAPTURED / 146 BYTE-DISTINCT ADDITIONS / T0 + T0S ACTIVE` | Five M0 lanes returned 118 metadata leads; 87 were fresh against the source frame and 84 remained after excluding 47 previously successful M1 roots. A balanced 20-root M1 pass yielded 19 valid pins and 191 paths; M2 froze 153, M3 captured 153/153 and full-frame dedup froze 146 byte-distinct originals (7 aliases). Header-title-only T0 supplied four low-recall triads. T0S separately partitions all 146 originals into five source-disjoint batches to discover source-grounded 3–4 peer-route drafts without prompts or labels. | T0/T0S are source-only feasibility gates, not clusters, prompts, gold labels, selectors, metrics or results. A T0S proposal must first pass literal/hash/origin audit and then independent T0 review. Strict V3 remains 37 compositions / 231 cases. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_039_2026-08-30/`. |
| RQ1b V3 Wave 038 diversified public intake and T0 closure | `M0--M3 + PROVENANCE + T0 CLOSED / 377 CAPTURED / 243 BYTE-DISTINCT ADDITIONS / 8 TRIADS / 0 C1 ADVANCES` | Six navigation scouts produced 66 leads, 32 fresh by origin-name comparison. Twenty pin-verified roots yielded 2,090 paths; deterministic M2 selected 377; exact-once M3 captured and locally rehashed all 377. Complete-frame deduplication against 30,989 prior hashes retained 132 historical and 2 within-wave aliases, then froze 243 newly byte-distinct originals. Header-title-only triage formed 58 lexical drafts and selected eight source-disjoint triads. Three independent source-only reviewers returned one nonparallel and seven no-common-envelope decisions; all literal/hash audits passed. | Strict source-only curation feasibility, not a cluster, prompt, label, selector, metric or result. Broad title overlap alone was insufficient. No C1 packet exists; strict V3 remains 37 compositions / 231 cases. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_038_2026-08-30/`. |
| RQ1b V3 Wave 037 local-source T0 and C1 closure | `T0 + C1 CLOSED / 18 TRIADS / 54 REHASHED SOURCES / 3 C1 PACKETS / 0 C2 ADVANCES` | After Wave 036's network stop, local-only preparation scanned 10,000 retained distinct-title lexical drafts, excluded 1,971 touching historical C0/C6 sources, and selected 18 source-disjoint triads. Literal-valid T0 review produced 13 nonparallel, two no-plausible-triad and three C1 packets. All six independent C1 returns and nine bound sources passed exact-span/rehash audit; pgvector and PMax were nonparallel/component sets, while caching had no unanimous C2 advance. | This is strict source-only curation feasibility, not a cluster, prompt, label, selector, retrieval, metric, information-field or thesis result. Strict V3 remains 37 compositions / 231 cases. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 037 Local T0 and C1 Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 036 public-source discovery | `M0 COMPLETE / 39 UNIQUE REPOSITORY LEADS / 32 NEW / M1 TERMINAL GITHUB RATE LIMIT / 0 SOURCE BODIES` | Two independent metadata scouts produced 40 leads; one was a within-wave duplicate and seven overlapped prior waves. Twenty predeclared M1 commit requests each received GitHub HTTP 403 `rate limit exceeded` on their sole permitted attempt. | This is a temporary network boundary, not a source-quality or scientific rejection. No tree path, source body, source-frame addition, triage, cluster, prompt, label, selector, metric or result exists. Fresh M1--M3 must occur under a separately logged later pass. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 036 Public Discovery Stop - 2026-08-30.md`. |
| RQ1b V3 Wave 035 public-source intake and C1 closure | `M0--M3 + PROVENANCE PASS / 238 CAPTURED / 116 BYTE-DISTINCT ADDITIONS / 2 T0 C1 PACKETS / 0 C2 ADVANCES` | Twelve commit-pinned roots yielded 238 one-shot raw captures and 116 rehashed novel originals. Five source-only T0 batches proposed two four-skill C1 packets; both packets received two literal-valid independent C1 reviews. Both were rejected as nonparallel/component sets: a common inference wrapper’s provider/model family, and broad client-app containers mixed with a host wrapper and unequal lifecycle work. | This is strict source-only curation feasibility, not a prompt, label, selector, retrieval, metric, information-field or thesis result. Strict V3 remains 37 compositions / 231 prompt cases. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 035 Intake and C1 Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 034 public-source intake and C1 closure | `M0--M3 + PROVENANCE PASS / 17 PINNED ROOTS / 456 CAPTURED / 114 BYTE-DISTINCT ADDITIONS / 2 T0 C1 PACKETS / 0 C2 ADVANCES` | Thirty-six navigation leads produced a commit-pinned 456-path roster. Every one-shot raw capture succeeded; SHA-256 deduplication retained 342 historical aliases and admitted 114 rehashed originals. Two independent C1 reviews for each of two source-only packets rejected one as a component/nonparallel set and the other for no common envelope. | No prompt, gold label, selector, metric or retrieval result exists. `READY_FOR_C1` was only a triage state, not a valid cluster. Strict V3 remains 37 compositions / 231 prompt cases. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 034 Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 033 C4A--C6 strict closure | `C4A--C6 PASS / 1 TRIAD / 6 LOW-RISK STRICT CASES / 0 EXCLUSIONS / V3 COHORT 37 COMPOSITIONS / 231 PROMPT CASES` | A pathway-input triad completed independent source-only C4A cards, two key-blind model-assisted C4B adequacy reviews, C5 target reconciliation and C6 source/ledger freeze. The source intake captured 322 artifacts and retained 199 byte-distinct additions; only one of the two C1 advances reached this closure. Both literal builder cards passed; the original canonical audit failure is retained and its r1 amendment uses an existing exact builder excerpt. C4B records 6/6 singleton agreements and C5 6/6 target matches. | This is strict public-skill curation feasibility, not human annotation, a field-effect finding, selector input, metric or retrieval result. Keep 37/231 distinct from the historical cross-source campaign. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 033 C4A-C6 Strict Freeze - 2026-08-30.md`. |
| RQ1b V3 Wave 032 C4A--C6 strict closure | `C4A--C6 PASS / 1 TRIAD / 6 LOW-RISK STRICT CASES / 0 EXCLUSIONS / V3 COHORT 36 COMPOSITIONS / 225 PROMPT CASES` | The security, user-research, and visual/documentation survey triad completed source-deidentified seven-slot cards, two independent key-blind model-assisted C4B adequacy reviews, C5 target reconciliation and C6 source/ledger freeze. Both original C4A nonliteral-quote drafts and the first trailing-space C4B evidence audit are retained; fresh exact-span cards plus a mechanical one-character amendment produce the passing r1 chain. It records 6/6 exact singleton agreements and sealed-target matches. | This is strict public-skill curation feasibility, not human annotation, a field-effect finding, selector input, metric or retrieval result. Keep 36/225 distinct from the historical cross-source campaign. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032 C4A-C6 Strict Freeze - 2026-08-30.md`. |
| RQ1b V3 Wave 032 multi-root public-source intake | `M0--M1 AND PROVENANCE PASS / 5 PINNED ROOTS / 171 CAPTURED / 85 BYTE-DISTINCT ADDITIONS / 5 T0 GROUPS IN INDEPENDENT REVIEW` | Five roots contributed 171 exact-once public-body captures. Clean-frame SHA-256 deduplication admitted 85 originals, retained 80 historical aliases and 6 within-wave aliases, then froze the source amendment. Five non-overlapping prompt-free structural groups cover 19 artifacts. | T0 is source-only: no prompts, gold labels, selectors, metrics or results. Only consensus `READY_FOR_C1` groups can receive C1 literal source-evidence construction. At intake closure V3 was 35/219; after the separate W32 C4--C6 closure the live total is 36/225. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032 Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 031 C1--C3 curation closure | `C1 PASS / C2 STRICT-NONPARALLEL OR MULTI-ADEQUACY STOP / 0 NEW CLUSTERS` | Two source-only framework groups passed T0/C1 literal source evidence. Orchestration rejected all 6/6 C2 task positions for unsafe multi-adequacy. RAG retained 2/6 cue-safe positions, but its 4/6 C2 rejections prevented the complete candidate symmetry required for C4. | This is a retained negative strict-public-cluster feasibility observation, not a field effect or retrieval result. Neither composition advances to C4 or counts toward V3. Strict total remains 35/219. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 C1-C3 Curation Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 031 pinned public-source intake | `M0--M1 AND PROVENANCE PASS / 4 PINNED ROOTS / 313 CAPTURED / 100 BYTE-DISTINCT ADDITIONS / 213 ALIASES / 10 T0 TRIADS IN REVIEW` | Four commit-pinned roots exposed 482 eligible paths. A deterministic 313-path roster completed one-shot public-body capture without failures, then full-frame SHA-256 deduplication and a zero-failure provenance amendment. The 100 novel bodies all came from one root; the other three roots are historical byte aliases. | T0 is source-only triage: no prompts, gold labels, selectors, metrics or results. Only `READY_FOR_C1` triads may receive C1 evidence construction. Strict V3 total remains 35 compositions / 219 cases. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 Public Source Intake Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 029 C4A--C6 strict closure | `C4A--C6 PASS / 1 TRIAD / 6 LOW-RISK STRICT CASES / 0 EXCLUSIONS / V3 COHORT 35 COMPOSITIONS / 219 PROMPT CASES` | The W27/W29 fintech, healthcare and game UI triad completed literal seven-slot card preservation, two independent key-blind model-assisted C4B reviews, C5 target reconciliation and C6 source/ledger SHA-256 validation. The original reviewer-2 response is retained; its one non-exact selected-card quote was corrected only by a fresh, single-packet key-blind review. The amended C4B audit records 6/6 exact singleton agreements, all target-consistent. | This is strict public-skill curation feasibility, not human annotation, a field-effect finding, selector input, metric or retrieval result. Keep its 35/219 V3 source-frame count distinct from the historical 76-composition cross-source campaign. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 C4A-C6 Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 030 broad multidomain public-source intake | `285 M0 LEADS / 21 M1 ROOTS / 108 CAPTURED / 53 BYTE-DISTINCT ADDITIONS / 55 FROZEN ALIASES / PRE-D1` | Sixteen search lanes produced 285 de-duplicated metadata leads (six 403 failures retained). Twenty-one roots completed one-shot pinned commit/tree-path census, then a deterministic 108-body source capture, clean-frame SHA-256 deduplication and additive provenance freeze. | The 53 additions and lexical-neighbour list are source discovery only. No D1/C1--C6 composition, prompt, label, selector, metric or result exists. Official strict total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 030 Broad Multidomain Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 029 supplemental public-source intake | `5 CAPTURED / 5 BYTE-DISTINCT ADDITIONS / 0 ALIASES / D1 READY_FOR_C1 / C1 PASS / C2 PASS / C3R1 LOW-RISK PASS / C4A PENDING` | Five predeclared public `SKILL.md` originals passed one-shot capture, byte rehash, clean-frame SHA-256 deduplication and provenance-only amendment freeze. Two independent source-only reviews of the W27/W29 UI-design triad reached audited `READY_FOR_C1`; C1 binding and literal-chain finalisation passed. C2 binding produced six drafts. Both blind C3 reviewers required a cue-only shortening of over-bundled source constraints; mechanical C3R1 scan and two fresh blind C3R1 reviews then allowed all six as low-risk operational requests. | C4A must build and literal-audit source-deidentified seven-slot cards before any adequacy review. Shared-template and mixed-domain risk remain exclusion criteria. Wave 028 is excluded. No strict label, selector, metric or result exists. Official strict total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 Targeted Supplemental Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 028 public-source capture | `QUARANTINED / 243 UNIQUE ROSTER URLS / 362 MANIFEST RECORDS / 119 DUPLICATE URLs / 0 ADMISSIONS` | M0 found 200 public metadata leads; M1 pinned 16 trees with 633 paths; a 243-URL roster was created. A detached capture process overlapped its resume, yielding 362 manifest records and a report inconsistent with the manifest. All records remain retained for audit. | Exact-once provenance failed, so no W28 source is admitted to the frozen frame or used for D1/C1 screening. No cluster, prompt, gold, representation, selector, metric or result exists. Official strict total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 028 Capture Quarantine - 2026-08-30.md`. |
| RQ1b V3 Wave 027 targeted public-source intake | `289 CAPTURED / 235 BYTE-DISTINCT ADDITIONS / 54 FROZEN ALIASES / PRE-C1` | Sixteen pinned public repository trees produced a 289-body one-shot capture. Full-frame SHA-256 deduplication admitted 235 new public originals as a provenance-only amendment. A 235-source canonical-path/literal-heading inventory and deterministic local lexical-neighbour list support reading order only. | No D1/C1 disposition, C2--C6 case, prompt, gold label, representation, selector, metric or retrieval result exists. Official total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 027 Targeted Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 026 broad public-source intake | `197 CAPTURED / 172 BYTE-DISTINCT ADDITIONS / 25 FROZEN ALIASES / PRE-C1` | Sixteen pinned public repository trees produced a 197-body one-shot capture. Full-frame SHA-256 deduplication admitted 172 new public originals as a provenance-only amendment. A 172-source canonical-path/literal-heading inventory and deterministic local lexical-neighbour list support reading order only. | No D1/C1 disposition, C2--C6 case, prompt, gold label, representation, selector, metric or retrieval result exists. Official total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 026 Broad Public Source Intake - 2026-08-30.md`. |
| RQ1b V3 Wave 025 broad public-source intake | `230 CAPTURED / 198 BYTE-DISTINCT ADDITIONS / 31 FROZEN ALIASES / 1 WITHIN-WAVE ALIAS / PRE-C1 CLOSED` | Twelve pinned public repository trees produced a 230-body one-shot capture. Full-frame SHA-256 deduplication admitted 198 new public originals as a provenance-only amendment. The health-digest candidate closed before D1 because targeted reviews were mechanically invalid and later readings disagreed on peer parallelism; short-form ads are `LIKELY_NONPARALLEL`; frame extraction/analysis/transcription is component/granularity-confounded. | No D1/C1 disposition, C2--C6 case, prompt, gold label, representation, selector, metric or retrieval result exists. Official total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 025 Broad Public Source Intake - 2026-08-30.md` and `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_025_2026-08-30/source_only_triage/HEALTH_DIGEST_TRIAD_CLOSURE_2026-08-30.md`. |
| RQ1b V3 Wave 024 source intake and C4A closure | `232 CLEAN CAPTURES / 87 BYTE-DISTINCT ADDITIONS / 1 C1--C3 TRIAD / 1 C4A REJECT / 0 C4B--C6` | A corrected, predeclared roster admits only a SHA-verified 232-body clean stream: 120 original exact-once captures plus 112 separately captured URLs that were never attempted initially. A 251-URL duplicate-attempt set is quarantined. The sole CaseMark derivative-analysis triad passed C1 and six C3 low-risk cue reviews, then two literal-valid builder cards jointly omitted a qualifying Candidate A workflow excerpt; two independent source-only conformance reviews rejected canonicalisation. | Capture/provenance and card-completeness feasibility only. No canonical card, blind adequacy review, gold label, selector, metric or retrieval result exists. Do not repair omitted source evidence. Official total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_024_2026-08-30/README.md`. |
| RQ1b V3 Wave 023 source-intake closure | `145 CAPTURED / 1 BYTE-DISTINCT ADDITION / 144 FROZEN ALIASES / 0 D1 SCREENS` | Four public repositories were pinned, cloned only for path enumeration and captured once without executing source code. Exact deduplication retained one healthcare library router; all other bodies were already frozen. | The router is an unpaired additive source asset, not a 3--4 candidate strict composition. This is no prompt, gold, selector, metric or retrieval result; the official total remains 34 C1--C6-frozen compositions / 213 packets. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_023_2026-08-30/README.md`. |
| RQ1b V3 Wave 021 D1--C1 closure | `87 CAPTURED / 71 BYTE-DISTINCT ADDITIONS / 8 D1 SCREENS / 1 C1 REJECT / 0 C2--C6` | Eight structural source-only screens covered 69 additions. A bookkeeping/controller, FP&A and tax triad was the only D1 advance. Its independent C1 reviews agreed on exact source evidence but materially disagreed over whether the Controller and FP&A are independent first routes; the main-thread C1 decision fails closed. | This is strict public-source feasibility work, not a valid cluster, prompt, gold label, field card, selector, metric or retrieval result. The official total remains 34 C1--C6-frozen compositions / 213 strict packets. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 021 D1-C1 Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 022 M0--M1 navigation stop | `644 M0 LEADS / 40 M1 ATTEMPTS / 0 TREE SUCCESSES / 0 SOURCE BODIES` | Eight targeted repository-search lanes produced 644 navigation-only leads. The predeclared first five roots per lane all persisted a single failed M1 tree-metadata outcome. | This is neither source admission nor a cluster result. Do not retry those 40 roots automatically; use a later non-duplicative public discovery route. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_022_2026-08-30/README.md`. |
| RQ1b V3 Wave 019 C1--C4A closure | `100 CAPTURED / 84 BYTE-DISTINCT ADDITIONS / 2 C1--C3 ADVANCES / 2 C4A REJECTS / 0 C4B--C6` | The accounting quartet and native-Office triad passed source-only C1, then all 14 direct/paraphrase packets passed C3 after six cue-only edits. For each composition, two literal-valid anonymous cards were independently reviewed; both C4A decisions reject canonicalisation because qualifying original-source workflow, verification or boundary evidence was omitted/misallocated. | This is field-card completeness evidence, not a semantic-proximity, gold-label, selector, metric or retrieval result. No principal repair/union is allowed. The live total remains 34 C1--C6-frozen compositions / 213 strict packets. Continue source discovery and triage. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 019 C1-C4A Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 020 initial public-source triage | `86 CAPTURED / 78 BYTE-DISTINCT ADDITIONS / 5 GROUPS SCREENED / 0 C1 ADVANCES SO FAR` | The new amendment holds public originals for later source-only screening. Completed initial groups were all lifecycle, component, methodology or different-deliverable combinations, so none enters C1. | These are discovery/provenance and pre-C1 source-triage counts, not valid clusters or retrieval evidence. Continue local source-only triage before materialising any D1/C1 composition. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_020_2026-08-30/source_only_triage/W20_INITIAL_TRIAGE_LOG.md`. |
| RQ1b V3 Wave 018 duplicate-only source intake | `30 CAPTURED / 0 BYTE-DISTINCT ADDITIONS / 0 D1 SCREENS` | The 30 public Kubernetes/platform-operation leads all captured successfully, then SHA-256 deduplication against the immutable frame plus Waves 009--017 classified every body as an already-frozen alias. | This is a duplicate-only provenance closure, not a valid cluster, D1 rejection, prompt, gold, representation, selector, metric or retrieval result. The live total remains 34 C1--C6-frozen compositions / 213 strict packets. Continue fresh, non-overlapping public discovery. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 018 Duplicate-Only Source Intake Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 017 source intake and triage | `19 CAPTURED / 7 BYTE-DISTINCT ADDITIONS / 5 D1 REJECTS / 0 C1 ADVANCES` | Single-attempt capture and multi-frame deduplication retained seven additive public originals and 12 aliases. Five source-only triages reject pair-only, container/downstream, multi-adequate, or nonparallel families before C1. | This is source discovery feasibility, not a valid cluster, prompt, gold, representation, selector, metric or retrieval result. The live total remains 34 C1--C6-frozen compositions / 213 strict packets. Continue broader cross-origin discovery. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 017 Source Intake and Triage Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 016 C1--C4A closure | `C1/C3 COMPLETE / C4A CONFORMANCE REJECT / 0 C4B--C6 ADVANCES` | One GitHub Actions triad passed source-only C1 and six C2 packets passed C3 with two cue-only revisions. Two literal-valid anonymous C4A cards were built, but both independent C4A conformance reviewers found qualifying source evidence omitted by both builders. | This is a field-card completeness rejection, not a semantic-proximity, gold-label, selector, metric or retrieval result. No principal card repair is permitted. The live total remains 34 C1--C6-frozen compositions / 213 strict packets. Continue discovery. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 016 C1-C4A Closure - 2026-08-30.md`. |
| RQ1b V3 Wave 013 cross-origin C1 screen | `SOURCE INTAKE COMPLETE / 56 READABLE / 19 BYTE-DISTINCT ADDITIONS / 3 C1 REJECTS / 0 C2 ADVANCES` | 56 no-retry captures yielded 37 pre-frozen byte aliases and 19 source-frame additions. Security review, GDPR/compliance, and presentation-authoring compositions passed source binding and literal evidence checks, but each was rejected as a component/container or multiple-adequate composition. | This is strict-feasibility evidence, not a valid cluster, prompt, gold, representation, selector, metric or retrieval result. The live total remains 34 C1--C6-frozen candidate compositions / 213 strict packets. Continue cross-origin public discovery under unchanged gates. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 013 Cross-Origin Source Discovery and C1 Checkpoint - 2026-08-30.md`. |
| RQ1b V3 Wave 012 cross-origin C1 screen | `SOURCE INTAKE COMPLETE / 29 READABLE / 11 BYTE-DISTINCT ADDITIONS / 2 C1 REJECTS / 0 C2 ADVANCES` | One non-retried 404 is retained. Two source-only D1 records (four generic code-review sources and three data-visualisation sources) passed literal/hash binding, then C1 rejected both as non-parallel or component/container compositions. | This is strict-feasibility evidence, not a valid cluster, prompt, gold, representation, selector, metric or retrieval result. Continue cross-origin source discovery; never compensate for the reject by relaxing peer parallelism. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_012_2026-08-30/` and `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_012_2026-08-30/`. |
| RQ1b V3 Waves 009--011 source-only C1 closures | `DISCOVERY CONTINUES / 100 BYTE-DISTINCT SOURCE ADDITIONS / 2 C1 REJECTS / 0 NEW C2--C6 PARENTS` | Wave 009 video editing and Wave 010 contract review each passed local source/hash binding but C1 rejected the candidates as non-parallel containers, specialised implementations, or preparation roles. Wave 011 fetched 127 catalog leads: only six byte-distinct additions survived deduplication and all share one origin. Combined additions are 88 + 6 + 6 = 100. | Source counts are not cluster counts. No new source has passed beyond C1, and no prompt, gold, representation, ablation, selector, metric or retrieval result exists. Next: cross-origin source discovery, then unchanged source-only D1/C1 and C2--C6 gates. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`, `d1_source_intake_wave_010_2026-08-30/`, `d1_source_intake_wave_011_2026-08-30/`. |
| RQ1b V3 Wave 009 public-source amendment | `PROVENANCE FREEZE COMPLETE / 199 RETRIEVED / 88 BYTE-DISTINCT ADDITIONS / 111 FROZEN DUPLICATES / NO CLUSTER OR RETRIEVAL RESULT` | All artifacts were fetched once, locally rehashed and exact-byte deduplicated against the immutable 29,292-record source frame. The 88 byte-distinct originals form a separate Wave 009 amendment; no old source record was modified. | Addition is source provenance only, not D1/C1 eligibility, a prompt, label, representation, selector input, metric or result. Run local source-only D1 triage and require unchanged C1--C6 gates before counting any valid parent cluster. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`. |

Date: 2026-08-05

> **2026-08-30 RQ1b V3 current priority.** C4A--C6 Wave 001 is now terminal:
> four of nine C4A packets were
> admitted, five strictly rejected, and C6 froze 14 prompt cases across three
> parent compositions. Only one parent composition is complete for every
> candidate target and both direct/paraphrase variants; all frozen cases retain
> high/medium cue-risk annotations. This is not 14 valid clusters or a
> selector/metric/routing result; public-source discovery has resumed under
> unchanged gates.
> Execution record:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Priority Execution - 2026-08-30.md`.

> **2026-08-28 active RQ1b field-type ablation.** RQ1b now has an active
> source-grounded public field-card availability test. It retains the strict
> public source/prompt/gold roster, verifies that a `FULL` card preserves gold,
> then synchronously withholds one field type from all candidates and measures
> conditional routing degradation or redundancy. It does not claim a field is
> uniquely decisive. Its six-family pre-scoring pilot passed with 5/6 applicable
> families on 2026-08-28; the checkpoint is
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_pilot_2026-08-28/RQ1B_FIELD_TYPE_ABLATION_PILOT_CHECKPOINT_2026-08-28.md`.
> No selector, embedding, API, retrieval, metric, or thesis result exists.

> **2026-08-29 RQ1b-A v2 results completed.** The frozen source-grounded
> field-card availability experiment now has both predeclared selector twins:
> local BM25 and separately authorised Qwen `text-embedding-v4`. Each covers
> the same 87 strict-preserved routing families, 174 original prompts and
> eight `FULL`/candidate-synchronous-mask conditions (1,392 rows per
> selector). Qwen's external stage completed 126/126 serial no-retry calls and
> persisted 1,246 embeddings; its post-run integrity audit passed. Across
> all-eligible composition-aware estimates, no field's Qwen `FULL-MASK`
> Top-1 or MRR interval excludes zero. RQ1b v2 therefore contributes a
> bounded public-card redundancy result rather than a universal field ranking;
> RQ1a remains the controlled field-sufficiency result. No thesis LaTeX/PDF
> change has been made. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 joint-mask next stage.** The user authorised a
> prospective joint-field extension after reviewing the single-field design.
> It has three fixed semantic groups and will measure whether combined task
> specification, execution/verification, or applicability/capability facts
> jointly retain non-redundant routing value. Freeze and local BM25 are in
> progress; a fresh exact Qwen payload approval remains required. This is a
> separate amendment, not a reinterpretation of the v2 results. Detailed SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Joint Field-Set Availability Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 local progress.** The three group masks have been
> frozen and mechanically verified against immutable v2 `FULL` cards. Local
> BM25 is complete and audited (696 rows, zero network); all three joint-set
> bootstrap intervals cross zero, so no BM25-only joint contribution claim is
> available. Qwen is prepared but unrun: only 402 new mask-derived card texts
> require transfer because prior v2 query/FULL embeddings are cache hits. A
> separate exact Qwen approval is the next gate.

> **2026-08-29 RQ1b v2.1 joint-mask results completed.** Both frozen selector
> twins now pass audit on the same 87 strict routing families, 174 prompts and
> four conditions (696 rows each). Qwen used the exact authorised 402 new
> candidate-card texts only; all queries remained cache hits, 41/41 no-retry
> calls succeeded, and the cache-only score recovery was independently
> validated. Qwen and BM25 both show directional degradation for all three
> coherent masks but all primary composition-bootstrap Top-1/MRR intervals
> cross zero. RQ1b v2.1 is therefore complete as a bounded public
> combined-information availability/redundancy result; it neither establishes
> a decisive field set nor changes RQ1a's controlled sufficiency finding. No
> thesis LaTeX/PDF update has been made. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v3 started: large public source frame before expansion.**
> A local inventory found many `SKILL.original.md` paths, but raw paths include
> staged mirrors, historical copies, packet material, quarantine and generated
> overlays. V3 therefore starts with provenance-aware hash deduplication and
> a canonical source manifest before forming a new 100+ composition cluster
> cohort. The future corpus audit is bounded to field recoverability and
> co-occurrence in its declared source frame, while strict cluster formation
> remains a separate routing-validity task. No V3 score, embedding, external
> transfer or thesis result exists. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 discovery-path refinement.** C0 lexical screening is
> retained as a strict feasibility audit rather than silently tuned after poor
> container/component yield. A separate prospective D1 path will discover
> source-grounded public candidates through explicit target, provider/interface
> and applicability contrasts; all later strict validity gates remain fixed.
> This is not a cluster, gold-label, selector or field-effect result. Record:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 D1 Directed Public-Source Discovery Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C0 Wave 001 complete.** Thirty source-only lexical
> triads were reviewed over 90 unique canonical sources after a passing
> provenance/disjointness audit. Three advance to C1 source evidence; the
> remaining 27 are rejected for container/component (18), copy/derivative (2),
> insufficient operational contrast (6), or no common envelope (1). This is a
> lexical-discovery feasibility calibration only; it produces no strict label,
> prompt, retrieval, embedding, metric or thesis result. The next local step
> is a title-signal-containment-prioritised C0 wave, while the three advances
> remain pending C1. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_001_2026-08-29/C0_SOURCE_REVIEW_WAVE_001_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 002r1 complete.** Thirty additional
> source-only lexical triads, using 90 sources disjoint from Wave 001, passed
> provenance and source-binding audit. Seven advance only to C1 source
> evidence; the remainder fail as component/container (14), insufficient
> contrast (7), or no shared envelope (2). Together the two waves have ten C1
> candidates from 60 screened triads. This remains a discovery feasibility
> record: no strict label, prompt, retrieval, embedding, metric, transfer or
> thesis result exists. The title-signal filter prioritised queue order only.
> Record:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_002r1_2026-08-29/C0_SOURCE_REVIEW_WAVE_002R1_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 local discovery checkpoint.** V3-S0/S1 are complete:
> the declared local frame holds 29,292 SHA-unique canonical public-original
> artifacts from 1,613 origins and 2,476 duplicate-path aliases. V3-S2's
> deterministic structural census and V3-C0a lexical triage are also complete;
> each of the broad and distinct-title queues retains 10,000 cross-origin
> triad drafts. This is not a count of valid clusters or a semantic prevalence
> result. V3-C0b source-only envelope/operational-contrast screening is next;
> no V3 gold label, prompt, selector, external text transfer, metric or thesis
> result exists. See
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`.

> **2026-08-29 RQ1b-A construction checkpoint.** The active non-pilot
> field-card input is frozen after a pre-review source-surface-cue amendment:
> 48 compositions, 128 strict routing families, and 256 prompt variants.
> Thirty-eight cards are unchanged and ten are literal-safe same-slot repairs;
> ten cue-affected compositions are strictly excluded. FULL-card preservation
> is pending two blinded selection-only reviews. This is construction evidence,
> not a retrieval or field-effect result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_SURFACE_CUE_AMENDMENT_COMPLETION_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 001.** Of the first 18
> packet-ordered families, six passed dual-blind FULL-card preservation for
> direct and paraphrase prompts. Twelve were excluded from later ablation
> scoring because no candidate was fully adequate (nine), reviewers disagreed
> (two), or more than one candidate was fully adequate (one). This is progress
> on validity control only, with no selector, retrieval, embedding, metric,
> field-effect, or thesis result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 002.** The next 18 packets
> yielded 13 strict-preserved families and five exclusions. Cumulative gate
> state: 36 adjudicated, 19 passed, 17 excluded, 92 pending. This is an
> ongoing benchmark-validity control, not a selector, retrieval, embedding,
> metric, field-effect, or thesis result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 003.** Eighteen more reviewed
> families produced 12 pass and six exclusion. Cumulative status is 54
> adjudicated, 31 strict-preserved, 23 excluded and 74 pending. The four
> mechanically invalid response files were not used; independent valid
> replacements were audited before adjudication. This remains validity control
> with no selector, retrieval, embedding, metric, field-effect or thesis
> result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_003_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 004.** 17 validly reviewed
> packets yielded 14 strict-preserved and three exclusion. Cumulative state is
> 71 adjudicated, 45 strict-preserved, 26 excluded, 56 undispatched, plus one
> `UNADJUDICATED_FORMAT_HOLD` after repeated mechanical evidence failures. This
> is still benchmark-validity control, not a selector, retrieval, embedding,
> metric, field-effect or thesis result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 005.** 15 of 18 further
> families passed and three were excluded, for 60 strict-preserved and 29
> excluded across 89 adjudicated families. There are 38 undispatched families
> and one separate format hold. This is not selector, retrieval, embedding,
> metric, field-effect or thesis evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 006.** Wave 006 adds 13 passed
> and five excluded, for 73 strict-preserved and 34 excluded across 107
> adjudicated families. Twenty are undispatched and one is held for format
> audit. This is pre-scoring benchmark validity, not thesis results. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate, Wave 007.** Of 18 further packets,
> 12 passed and six were excluded. The gate now holds 85 strict-preserved and
> 40 excluded families across 125 adjudications, with two undispatched and one
> separate format hold. Exact-evidence mechanics invalidated ten A-side and
> four B-side initial payloads; independent replacements were validated before
> adjudication. This is still benchmark-validity control, not retrieval,
> embedding, metric, field-effect or thesis evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A strict-gold gate completed.** All 128 active packets
> have a final state: 87 strict-preserved, 40 excluded and one format hold.
> The full local chain validates after final adjudication; 77--86 preserved
> families remain eligible per field. The next stage is a residual-redundancy
> audit, not retrieval scoring. No selector, embedding, metric, external API
> or thesis result has been produced. Completion checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_COMPLETION_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 001.** Six source-card-only
> residual packets cover 124 candidate-field targets: 96 exact review
> agreements, with 58 `none`, 35 `partial`, three `substantial`, and 28
> retained disagreements. This records redundancy strata only and does not
> test retrieval. Forty-two packets remain. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 002.** The next six packets
> add 142 targets, yielding 43 `none`, 54 `partial`, 14 `substantial`, and 31
> disagreements. Cumulative coverage is 12/48 packets and 266/994 targets;
> this remains redundancy bookkeeping only. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 003.** Six packets add 117
> targets; cumulative local coverage is 18/48 packets and 383/994 targets.
> This remains redundancy bookkeeping, not selector evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_003_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 004.** Six source-card-only
> packets add 123 targets: 26 `none`, 48 `partial`, 13 `substantial`, and 36
> disagreements. The cumulative local ledger is 24/48 packets and 506/994
> targets. Response-schema and literal-quote failures were retained as
> mechanical history and independently replaced before consensus; they do not
> indicate a strict-gold, source-card, or routing failure. No selector,
> embedding, retrieval, metric, external API, or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 005.** Six packets add 113
> targets: 47 `none`, 26 `partial`, nine `substantial`, and 31 disagreements.
> Cumulative local coverage is 30/48 packets and 619/994 targets. Mechanical
> response failures were retained and independently replaced; they are not
> route, source-card, or gold-label findings. No selector, embedding,
> retrieval, metric, external API, or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 006.** Six source-card-only
> packets add 120 targets: 54 `none`, 25 `partial`, 12 `substantial`, and 29
> retained disagreements. Cumulative coverage is 36/48 packets and 739/994
> targets. This is redundancy bookkeeping only; the 91 exact agreements and
> any independent replacement reviews do not constitute selector, retrieval,
> embedding, metric, external API, or thesis evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 007.** Six source-card-only
> packets add 128 targets: 83 `none`, 24 `partial`, eight `substantial`, and
> 13 retained disagreements. Cumulative coverage is 42/48 packets and 867/994
> targets. The 115 exact agreements and replacement payloads remain audit
> mechanics only; there is no selector, retrieval, embedding, metric, external
> API, or thesis result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A ready for local BM25, pending approval.** All 48
> residual-redundancy packets and 994 targets are consensus-bound (391 `none`,
> 287 `partial`, 97 `substantial`, 219 disagreements; 775 exact agreements).
> Input integrity, opaque packet bindings, the original review core, the
> condition-materialisation freeze amendment, and 48 candidate-synchronous
> condition audits pass. The usable strict primary pool is 87 routing families
> with 77--86 eligible families per field; 40 strict failures and one
> unadjudicated format hold remain excluded. This is pre-scoring readiness only:
> no BM25, selector, retrieval, embedding, metric, API, or thesis result has
> been created. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_LOCAL_PRE_BM25_READINESS_CHECKPOINT_2026-08-29.md`.

> **2026-08-28 RQ1b method amendment.** The raw-full-document mask campaign
> is now a bounded feasibility audit only. The active RQ1b plan is
> RQ1b-N unchanged-public-artifact validation plus RQ1b-S
> source-grounded field-card winner-side target neutralisation and sham
> control. A six-family pilot is pending; it produces no selector, embedding,
> API, retrieval, metric, or thesis result and must pass all card-fidelity and
> isolation gates before scaling. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Natural-Artifact And Source-Grounded Field-Card Protocol - 2026-08-28.md`.

> **2026-08-28 RQ1b-S validation-pilot outcome.** Stopped before any
> neutralisation or model run. The first three field cards all preserved the
> existing strict gold under two blind prompt-plus-card reviews, but their
> independently named primary fields drifted from the pre-locked raw-artifact
> field. Since the required input/precondition and output/artifact examples
> fail this reaffirmation gate, the six-family pilot cannot meet its
> predeclared acceptance criterion. This is a source-grounded derivative-card
> attribution finding only, not an RQ1 retrieval, embedding, API, or thesis
> metric. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_card_pilot_2026-08-28/RQ1B_S_FIELD_CARD_PILOT_CHECKPOINT_2026-08-28.md`.

> **2026-08-15 RQ2 status.** RQ1a remains `REVIEWED / COMPLETE`. RQ2a remains `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`. RQ2b's base-v1 B0G full-pool semantic review completed mechanically, but its acceptable-set freeze remains `BLOCKED BEFORE RETRIEVAL`: 14 strict-gold rows are not fully acceptable and eight scored prompts have no fully acceptable reviewed candidate after 7,710 resolved review units. A user-directed review of only those 14 gold labels retained six and excluded eight material workflow mismatches. Its 381-prompt strict-gold-only v1.1 manifest is materialised and locally validated, not a selector result or acceptable-set repair. The first v1.1 review found two P1 and two P2 local contract defects; remediation passed a fresh rereview with no P0/P1 and is sealed locally for strict-contract components only. B1X remains an untransmitted 2,433-row/57-chunk I3C packet; the next step is a separate B1R text-transfer authorisation packet. No source-text transfer, Qwen reranker call, scientific RQ2b selector run, or thesis-result writing is authorised.

This is the high-level tracker for the thesis so the project does not drift. Detailed benchmark criteria live in `skill_benchmark/notes/benchmark_methodology_rubric.md`. The experimental roadmap lives in `thesis_notes/current/Thesis Experiment Roadmap.md`. The canonical information-layer framing lives in `thesis_notes/current/Information Layer Framework.md`. The source of truth for experiment method choices, information-layer/retriever/reranker combinations, run commands, and execution venues is `thesis_notes/current/Experiment Methodology Tracker.md`. The detailed RQ1 test-unit design, leakage controls, and few-shot field templates live in `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`.

Canonical I3 model-extraction protocol: `thesis_notes/current/I3 Model Extraction Protocol.md`.

> **2026-08-26 RQ1b cross-source current-status override.** The detailed table below is historical through Round 08. The live main RQ1b curation state is `C0A/C0B ROUND 09 COMPLETE / 1,761 HASH-VERIFIED ORIGINALS / 115 COMPLETED C0B SCREENS / 94 STRUCTURAL REJECTIONS / 21 C1-PASSED SOURCE-BACKED DRAFTS / 3 C6-FROZEN CANDIDATE COMPOSITIONS / 17 FROZEN STRICT PROMPT PACKETS / 3 UNRESOLVED PROMPTS / NO RETRIEVAL RESULTS`. Round 09 screened 23 fresh, no-reuse cross-source compositions from 73 SHA-verified originals and produced zero new C0B drafts: each was explicitly rejected for a source-supported container/component, generic-specialist, lifecycle/prerequisite, adapter/interface, or abstraction mismatch. This is a useful feasibility signal, not a retrieval result and not evidence that the strict benchmark has failed. The source-agnostic pool may continue to grow; no prompt, label, acceptable set, model/API call, retrieval input, metric, or thesis result has been created for unadvanced drafts.

> **2026-08-26 RQ1b Round 10 navigation exhaustion.** Six independent source-navigation passes covered all major topical slices of the present 1,761-original pool after excluding 354 candidates already screened in C0B. They produced no fresh strict 3--4 candidate composition: remaining near-matches were containers, specialists, components, lifecycle stages, adapters, or different task objects. This is an auditable source-pool feasibility finding, not a performance result. The next authorised curation action is new public-source discovery and exact-original staging under the existing cross-source protocol; do not dilute the strict peer-route or strict-singleton gates merely to reach a numerical target.

> **2026-08-26 RQ1b cross-source source-expansion Round 11--13.** The main pool now contains `1,928` SHA-verified public original artefacts from `53` origins after provenance-pinned, local byte staging of `JayRHa/AgentSkills` (75 MIT files), `coo-labs/skills` (13 CC-BY-4.0 files), `escoffier-labs/skillet` (39 MIT files), `Kilo-Org/skills` (3 MIT files), `tartinerlabs/skills` (13 MIT files), `mauromedda/agent-toolkit` (14 MIT files), and `soderlind/skills` (10 files). The last source contains no declared repository licence file and is explicitly tagged `NO_DECLARED_REPOSITORY_LICENSE_LOCAL_ANALYSIS_ONLY`: it is retained for internal provenance-pinned analysis only, with no licence inferred, copied, or redistribution implied. This corrects the prior Round 11--12 origin count to `52`; the live Round 13 count is `53`. Round 11 C0B structurally rejected 13 source-agnostic leads. Round 13 screened four more cross-source 3--4-candidate leads: three are source-backed drafts (evidence-form analysis, repository-documentation artefacts, and named CI/CD platforms) and one is a generic--specialist structural reject (pre-commitment decision support). Its 28 evidence substrings were exact-validated against the packet originals; C1 then passed all three drafts for candidate count, origin diversity, source hashes, and no candidate reuse.
>
> **2026-08-26 RQ1b Round 13 C2--C6 completion and Round 14 C0B update.** All 22 direct/paraphrase packets from the three Round 13 C1-passed compositions passed the literal C3 audit. A separate local semantic-risk audit retained 12 packets with no recorded residual cue risk, marked two API-documentation packets as `low_explicit_interface_affordance`, and marked the eight CI/CD-platform packets as `high_platform_affordance_without_product_name`. The latter are valid strict operational-context packets but must never be described as evidence of implicit semantic routing. Two independent model-assisted blinded C4 reviews covered every card in all 22 packets, agreed on the same unique fully adequate card for every packet, and passed exact-substring validation for every cited card evidence. C5 then matched all 22 singleton choices to their sealed C2 construction targets; C6 rechecked C1 hashes, composition, manual C3 coverage, and candidate reuse, freezing three additional candidate compositions and 22 additional primary strict packets. Round 14 then admitted 135 net-new originals from three sources (two large candidate repositories were exact duplicates and contribute no new bodies), refreshing the source pool to `2,063` SHA-verified originals from `56` origins. Its one C0B worklist proposal was structurally rejected after all six quoted source substrings were exact-validated: the group mixed general SEO blogging, general technical blogging, and a publisher-specific technical blog route. The live cumulative C0B state is `133 COMPLETED SCREENS / 109 STRUCTURAL REJECTIONS / 24 SOURCE-BACKED DRAFTS / 6 C6-FROZEN CANDIDATE COMPOSITIONS / 39 FROZEN STRICT PROMPT PACKETS / 3 UNRESOLVED PROMPTS / NO RETRIEVAL RESULTS`. These are curation and feasibility figures only, not representation, selector, model/API, metric, retrieval, or downstream-task results. Continue source expansion and C0A/C0B screening; do not weaken strict peer-route or strict-singleton gates to force a 100-cluster count.

Note: some lower sections retain historical 1006/2089/2349 results for comparison. The active result summary is `thesis_notes/current/Current Results Summary.md`.

> **2026-08-26 RQ1b Round 15 public-source expansion and C0B/C1 closure.** Twelve new public repositories added 1,132 net-new SHA-verified originals after exact-duplicate and missing-frontmatter exclusion, refreshing the source-agnostic pool to 3,195 originals from 68 origins. A repository with no declared licence is a reference-only provenance status, not an eligibility exclusion: its reproducibility record will supply source URL, commit, path, hash, and reconstruction instructions rather than bundle raw text. Four independent C0B source-only reviews screened eleven 3--4 candidate proposals; the unified ledger exact-validated all 36 stored source substrings, retaining seven source-backed drafts and rejecting four for non-peer/container, lifecycle, or over-broad-envelope structure. C1 passed all seven retained drafts: source hashes, 3--4 candidate size, at least two origins, zero within-round reuse, and zero overlap with the 21 candidates in prior frozen C6 packets. The prior wrong-navigation-file C1 run is preserved as a non-scientific input-contract failure and is excluded from curation counts. Live C0B totals are now 144 completed screens, 113 structural rejections, 31 source-backed drafts, seven new C1-passed drafts, six C6-frozen candidate compositions, 39 frozen strict prompt packets, and no retrieval results. Next gate: cue-safe C2 prompt drafting for the seven C1-passed Round 15 drafts; no prompt, gold label, acceptable set, model/API call, retrieval input, metric, or thesis result yet exists for them.

> **2026-08-27 RQ1b Round 15 C2--C6 closure.** The seven Round 15 C1-passed compositions produced 46 cue-audited C2 prompts. C3's final manual ledger allowed all 46 after preserving any residual cue-risk annotation. C4 used two independent model-assisted blinded reviews per packet across two disjoint reviewer pairs; a provenance-leaking first materialisation was invalidated before acceptance, and the replacement C4R03 reviews were citation-exact audited. Of 46 packets, 43 received the same strict singleton from both reviewers and three (`C4R03-037`, `C4R03-040`, `C4R03-044`) remain reviewer disagreements, not forced labels. C5/C6 passed with no integrity failure, freezing seven new candidate compositions and 43 strict prompt packets. The running primary curation total is therefore 13 frozen cross-source candidate compositions and 82 strict prompt packets; the three new unresolved prompts remain outside the strict stratum. These are curation figures only, not retrieval, embedding, reranking, API, metric, or downstream-task results. See `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 15 C2-C6 Closure - 2026-08-27.md`.

> **2026-08-28 RQ1b cross-source Round 32 closure override.** Round 32 completed C6 under the unchanged strict public-artifact protocol: 211 M0 leads became 121 exact-new roots, 112 pinned sources, 588 byte-verified originals from 28 origins, two C1-passed source-backed drafts, and finally two new C6-frozen candidate compositions with seven strict prompt packets. Five C4 reviewer-disagreement prompts remain explicitly non-primary; no prompt was relabelled. The live running state is **51 frozen candidate compositions / 304 strict prompt packets / 31 unresolved-or-exploratory-or-target-mismatch prompts / no retrieval results**. This crosses the minimum 50-composition feasibility target, but it is curation evidence only, not selector accuracy, embeddings, reranking, an API result, or a metric. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 32 M0-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 33 M0-C0B closure.** The required fresh discovery-first pass recorded 201 navigation-only leads, retained 119 exact-new repository roots, commit-pinned 99, and produced 279 byte-verified original artefacts from 19 origins after the bounded source-only staging gate. C0A generated two mechanically valid 3-candidate navigation proposals; C0B exact-source screening rejected both for non-parallel first-route structure, with all six evidence substrings locally verified. Therefore Round 33 adds **zero** C1 drafts, frozen compositions, strict prompts, or non-primary prompts. The live state remains **51 frozen candidate compositions / 304 strict prompt packets / 31 unresolved-or-exploratory-or-target-mismatch prompts / no retrieval results**. The zero yield is a strict feasibility curation outcome, not a selector or representation result; the next action is another discovery-first source wave toward 100 without gate relaxation. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 33 M0-C0B Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 34 C0B--C6 closure.** The same discovery-first source cohort produced eight C0A navigation proposals. Source-only C0B exact-evidence screening retained three peer-route drafts and rejected five; C1 then passed all three for hashes, origin diversity, candidate size, and no reuse. C2/C3 created 20 cue-controlled packets; source-specific workflow wording was removed before the final literal/manual C3 check. Eleven remaining bounded operational-context packets retain `medium` residual cue-risk annotations, and nine retain `low`; those annotations are preserved rather than silently treated as implicit-semantic evidence. Two independent **model-assisted, not human** blinded C4 reviews yielded eight exact singletons, six multiple-adequate outcomes, and six disagreements. C5/C6 froze the three compositions and eight strict packets only. The live strict state is therefore **54 frozen candidate compositions / 312 strict prompt packets / 43 non-primary unresolved-or-exploratory-or-target-mismatch packets / no retrieval results**. These are curation and feasibility counts, not selector accuracy, embedding, reranking, API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 34 C0B-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 35 M0--M2 closure.** Discovery recorded 697 public navigation leads, retained 691 exact-new roots, and commit-pinned all 691. Blobless census completed for 435 roots, recorded 256 fetch failures as non-admissions without automatic retry, and found 17,601 `SKILL.md` paths. The bounded source cohort completed all 47 stage batches: 140 origins and 2,411 paths were rehashed, yielding **2,158 canonical original artefacts from 134 origins** after 128 missing-frontmatter exclusions and 125 exact-byte duplicate exclusions, with zero integrity or staging failure. M2 then extracted source-provided name/description/heading navigation metadata for all 2,158 records. C0A has been partitioned by exact M0 discovery-query provenance, not by a new semantic classifier. This is source-pool preparation only, not a candidate composition, prompt, label, model/API call, retrieval input, metric, or result. Round 35 C0A navigation proposals must still pass source-isolated C0B, C1, C2/C3, two model-assisted blinded C4 reviews, C5, and C6 before they can increase the current **54 frozen candidate compositions / 312 strict prompt packets**. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 35 M0-M2 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 35 C0A--C6 closure.** C0A retained 30 navigation-only triads from the fresh source cohort; exact-source C0B retained six parallel-peer drafts and rejected 24, with 115/115 stored evidence excerpts verified against pinned originals. C1 passed all six. C2/C3 produced 36 final cue-controlled prompt packets. The final literal audit passed all 36; a protocol-completeness source-informed C3 review was subsequently added without C4 access and conservatively marked 23 construction-sensitivity risks `high`, three `medium`, and ten `low`. Parent adjudication retained those warnings but applied the frozen rule that genuine bounded user operational context is allowed without source identity or copied wording, yielding ten `low` and 26 `medium` residual-risk annotations. C4's two independent **model-assisted, not human** blinded reviewers produced 22 exact singleton agreements, seven multiple-adequate packets, and seven disagreements; citation repairs altered excerpts only, never judgments. C5/C6 froze **five** new compositions and **22** strict packets after source-hash/reuse and sealed-target checks. The live strict state is now **59 frozen candidate compositions / 334 strict prompt packets / 57 non-primary unresolved-or-exploratory-or-target-mismatch packets / no retrieval results**. This remains curation/feasibility evidence, not selector accuracy, embeddings, reranking, API, metrics, or downstream-task evidence. Sixteen more strict compositions are needed for the 75 target; next work is a fresh discovery-first public-source cohort under unchanged gates. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 35 C0A-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 36 M0 closure.** A fresh six-domain discovery pass plus coordinator seed recorded 185 repository-level public leads, canonicalised them to 169 roots, and removed 118 roots already present in earlier M0 manifests. The remaining **51 exact-new roots** are navigation-only: no commit pin, repository tree, source body, candidate composition, prompt, gold label, acceptable set, retrieval input, model/API call, metric, or result exists yet. Round 36 M1 will make exactly one `HEAD` pin attempt per root; failed pins remain durable non-admissions. This does not change the current **59 frozen candidate compositions / 334 strict prompt packets / 57 non-primary packets / no retrieval results**. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 36 M0 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 36 M1--M2 closure.** The first in-sandbox pin attempt failed uniformly before DNS resolution and is recorded as a transport failure, not as repository evidence. The real M1 pin then fixed 50/51 fresh roots, retained one failed root as a no-retry non-admission, and bloblessly counted 2,809 `SKILL.md` paths. The predeclared 3--64-path source-only bound staged 602 paths from 34 origins; hash rechecking retained **477 canonical originals from 32 origins** with zero stage or integrity failure. M2 then extracted only source-provided frontmatter/headings for all 477. This expands a provenance-preserved navigation pool only: it adds no composition, prompt, gold label, blinded judgement, selector input, retrieval result, embedding, API call, metric, or result. The strict state remains **59 frozen candidate compositions / 334 strict prompt packets / 57 non-primary packets / no retrieval results**. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 36 M1-M2 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 36 C0A--C6 closure.** C0A retained six navigation proposals from the new source pool; C0B exact-source screening retained three peer-route drafts and structurally rejected three, with 23/23 stored source-evidence excerpts verified against the byte-preserved originals. C1 passed all three on candidate size, origin diversity, hashes, and prior-freeze non-reuse. C2 created 18 direct/paraphrase packets and final literal C3 found no candidate-name, title/short-line, or copied multi-token cue. The separate source-informed C3 audit retained six `high`, eight `medium`, and four `low` construction-sensitivity records; after the frozen protocol adjudication, the allowed bounded user context retains four `low` and 14 `medium` residual-risk annotations. Two independent **model-assisted, not human** blinded C4 reviews reached 18 exact singleton agreements. Three schema aliases, seven C3 evidence strings, and five C4 citation strings were normalised or shortened only to exact existing source/card substrings; no judgement, rationale, prompt, candidate, or label changed. C5/C6 then sealed-target-checked and froze **three** new compositions and **18** strict packets. Post-freeze shape/identity QA confirms all 18 packets belong to three unique three-candidate sets with the strict gold present. The live strict state is **62 frozen candidate compositions / 352 strict prompt packets / 57 non-primary unresolved-or-exploratory-or-target-mismatch packets / no retrieval results**. Thirteen more compositions are needed for the 75 target. This is curation/feasibility evidence only, not human annotation, selector accuracy, embeddings, reranking, API, metric, or downstream-task evidence. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 36 C0A-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 37 M0--M2 closure.** Eight broad public discovery lanes produced 264 navigation leads, canonicalised to 82 roots and excluded 52 historic roots, leaving 30 exact-new roots. A sandbox-only all-DNS failure is preserved separately as a transport event; one real external HEAD probe per fresh root then pinned 29 and recorded one repository-not-found non-admission without retry. Blob-filtered tree census completed for all 29 pinned roots (852 `SKILL.md` paths); the predeclared 3--64-path bound selected 11 origins / 273 paths. Local source-only staging preserved and hash-checked 216 canonical originals from those 11 origins after 57 exact-byte duplicates and frontmatter exclusions, with zero integrity/staging failure. M2 extracted source-provided frontmatter/heading previews for all 216 and assigned six mutually exclusive C0A navigation lanes by frozen M0 discovery domain. This creates no composition, prompt, label, adequacy judgement, retrieval input, model/API call, metric, or result; the strict state remains **62 frozen candidate compositions / 352 strict prompt packets / 57 non-primary packets / no retrieval results**. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 37 M0-M2 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source Round 37 C0A--C0B closure.** Six source-pool navigation lanes produced two tentative triads. One was mechanically rejected because two candidates shared an origin. The one three-origin commerce/analytics triad advanced to SHA-verified exact-original C0B review, which rejected it as generic-plus-specialised/interface-container structure: the GA4 connector covers broad reporting, navigation, configuration, and event transmission, whereas the HubSpot sales-reporting and Google Ads budget artifacts are bounded domain workflows. All five cited C0B evidence substrings were exact-validated. Round 37 therefore adds **zero** C1 drafts, prompts, blinded reviews, frozen compositions, strict packets, or non-primary packets; the live strict state remains **62 frozen candidate compositions / 352 strict prompt packets / 57 non-primary packets / no retrieval results**. This is a curation feasibility outcome, not a selector, representation, model/API, metric, or downstream-task result. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 37 C0A-C0B Closure - 2026-08-28.md`.

## 2026-07-26 Current RQ State

### 2026-08-26 RQ1b discovery-first curation cadence

For every new RQ1b cross-source C0A source-screening cohort, first run and
record a fresh public-source discovery pass, even if it yields only duplicates,
structurally unsuitable leads, or no usable additions. Begin that discovery at
the cohort boundary rather than after the prior cohort is exhausted, and allow
the next discovery pass to run in parallel with C2--C6 review of the prior
cohort. This is an efficiency and coverage rule, not a relaxation of validity:
new discoveries cannot be added to a C1-passed candidate composition or a
blinded C4 packet. Public artefacts with no declared repository licence remain
`REFERENCE_ONLY` provenance sources and are eligible for cluster construction;
releases preserve URL, commit, path, hash, and reconstruction instructions
rather than redistributing their raw text. See
`skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md` Section 7.

> **2026-08-27 RQ1b Round 16 M0--M2 intake.** Three independent,
> domain-separated M0 passes recorded 37 public-repository leads: 12
> business/writing, 13 science/data, and 12 engineering/operations. A
> discovery-first M1 batch then commit-pinned 15 domain-diverse sources and
> sparse-cloned only `SKILL.md` and licence metadata; no source code was run.
> Of 2,249 pinned files, 1,901 are net-new SHA-verified originals from ten
> origins, while 340 are exact-byte duplicates and eight lack required
> frontmatter. All 1,901 staged originals passed M2A source-only navigation
> extraction (name/description for every item; headings for 1,892). This is
> not a cluster, prompt, label, acceptable set, review, embedding, retrieval,
> metric, or result; the strict curation total remains 13 frozen compositions
> and 82 strict prompt packets. Round 16 may now enter C0A source-agnostic
> proposal sorting. Missing declared licence remains a reference-only
> provenance status, not an eligibility exclusion. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 16 M0-M2 Intake - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 16 C0A--C6 closure and Round 17 discovery-first intake.** From the 1,901 staged Round 16 originals, source-agnostic C0A retained seven 3-candidate proposals; source-only C0B then passed four (`codebase assessment`, `data orchestration`, `event automation`, and `PDF preparation`) and structurally rejected three non-parallel/container/asymmetric proposals. C1 verified all four retained compositions: 3 candidates each, at least two origins, source hashes intact, and no reuse against prior frozen packets. C2 produced 24 direct/paraphrase prompts; C3's literal v2 audit passed all 24 after five cue-only rewordings, and its manual record marks all as explicit operational-context prompts with residual risk rather than cue-free language. Two independent source-deidentified C4 reviews per packet reached an exact singleton agreement on all 24 packets. A local C4 transcript-normalisation card-order error for four event-automation packets was caught by C5's sealed-intent check, retained as a failed audit artefact, corrected under v2 paths, and revalidated before any freeze. Corrected C5/C6 then froze four additional 3-candidate compositions and 24 primary strict packets. The running primary curation total is **17 frozen compositions / 106 strict prompt packets**. Every Round 16 packet had at least one C4 reviewer mark high operational-context directness, so these packets must be reported as explicit-constraint natural-artifact cases, never as proof of implicit semantic routing. No retrieval, representation, embedding, reranking, API, metric, or downstream result has been run.
>
> The required discovery-first work for the next cohort is already complete: Round 17 M0 recorded 30 deduplicated public-source leads across product/UX, legal, financial research, data engineering, databases, security, diagrams, cloud, and SRE. A local provenance screen found eight already present in older source-pool/C0B records, leaving 22 net-new M1 discovery candidates. They remain leads only; no new Round 17 repository is pinned, staged, clustered, labeled, or included in any retrieval input. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 16 C0A-C6 Closure and Round 17 M0 Discovery - 2026-08-27.md`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/discovery_round17_cross_domain_2026-08-27.md`.

> **2026-08-27 RQ1b Round 17 corrected M1--C1 status.** A broader discovery-first M1 batch commit-pinned 32 public repositories, sparse-staged `SKILL.md` artefacts without executing source code, and found 1,704 frontmatter-valid bodies. Canonicalisation removed 382 repeated paths across 362 exact SHA-256 duplicate groups from the M1 *navigation* manifest while preserving duplicate provenance; the resulting source-only inventory contains 1,322 canonical, byte-verified originals from 31 origins. M2A derived only names, descriptions, and headings; it then refreshed the C0 source pool to 3,223 exact originals. C0A formed 29 source-navigation proposals. C0B copied 101 originals into hash-verified review packets and completed independent model-assisted full-source screens: 19 proposals were structurally rejected and 10 were retained only as `C0_SOURCE_BACKED_DRAFT_NOT_A_CLUSTER_OR_RESULT`. The unified C0B ledger verifies 101/101 literal evidence substrings. C1 then passed all ten drafts on source hash, 3--4 candidate count, two-or-more origins, candidate source-hash uniqueness, and no reuse against every frozen C6 candidate manifest. C2 drafting is in progress; **the primary frozen total remains 17 compositions / 106 strict prompt packets**. This is curation and feasibility work only: no prompt packet has yet passed C3/C4/C5/C6, and no retrieval, representation, embedding, reranking, API, metric, or downstream result was run. Evidence: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round17_staged_source_summary_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m2a_round17_navigation_summary_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_structural_ledger_round17_validation_2026-08-27.json`, and `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c1_round17_integrity_summary_2026-08-27.json`.

> **2026-08-27 RQ1b Round 17 C2--C6 closure.** The ten C1-passed cross-source 3--4-candidate compositions yielded 70 final direct/paraphrase C2 prompts. C3 v2 passed literal cue audit for all 70 prompts; its manual ledger records 34 initially allowed explicit operational-context prompts and 36 prompts reworded to remove literal cues, with residual risk retained rather than erased. Two independent source-deidentified, model-assisted (not human) C4 reviewers assessed all 250 anonymous candidate cards across 70 packets. The first C4 audit failed closed because 26 Reviewer-A evidence spans were not exact substrings; only those citations were repaired against the same anonymous cards, without changing any adequacy judgement or rationale, before the successful re-audit. The final C4 audit has 70/70 exact singleton agreements and zero reviewer disagreements; C5 then unsealed the key and verified that every singleton matches its sealed C2 construction target. C6 rechecked C1 hashes/composition/reuse and C3 coverage, freezing all ten Round 17 compositions and 70 prompt packets. The live strict curation total is therefore **27 frozen cross-source candidate compositions / 176 strict prompt packets**. These counts are curation and feasibility evidence only, not retrieval, representation, embedding, reranking, API, metric, or downstream-task results. Every final packet retains its residual cue-risk annotation and must not be described as implicit-semantic evidence. Evidence: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round17_literal_cue_audit_v2_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round17_model_assisted_consensus_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round17_strata_summary_2026-08-27.json`, and `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round17_primary_freeze_summary_2026-08-27.json`.

> **2026-08-27 RQ1b Round 18 M0--M1 small-source intake.** Broad M0 discovery recorded 112 raw public-source leads and canonicalised them to 83 reachable GitHub repository roots. A commit-tree-only census found 16,208 `SKILL.md` paths across those roots; this is a scheduling observation, not a source-quality judgement. The small-source schedule selected 56 roots with at most 100 paths each. M1 sparse byte staging fetched only their pinned `SKILL.md` artefacts and repository-licence blobs, without executing source code: 1,689 paths were discovered, 1,157 bodies were stage-eligible, and canonicalisation retained 1,120 byte-verified originals across 44 origins after 37 exact duplicate paths and 14 missing-frontmatter paths were excluded from the navigation set. A separately materialised 1,000-skill large source is explicitly outside this Round 18 small-source aggregate pending its own integrity/scheduling plan; an interrupted large-source acquisition has no M1 manifest and is excluded. Next is M2 source-only navigation metadata, followed by C0A source-navigation proposals and independent C0B full-source structural screens. No candidate composition, prompt, label, reviewer adequacy decision, retrieval input, model call, metric, or result has been created for Round 18. Evidence: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m0_round18_discovery_summary_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_tree_census_summary_2026-08-27.json`, and `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/m1_round18_small_staged_source_summary_2026-08-27.json`.

> **2026-08-27 RQ1b Round 18 M2--C6 closure.** M2 derived source-only navigation metadata for all 1,120 Round 18 canonical originals. Five disjoint navigation curators proposed nine 3-candidate C0A compositions; the C0A merge verified all candidate IDs and two-origin minimums but did not assert peerhood. Independent model-assisted C0B reviewers then read the 27 exact original artefacts and recorded 46 literal source substrings: seven proposals were rejected because their originals showed containment, generic--specialist asymmetry, lifecycle mismatch, or no bounded shared route. Two source-backed drafts remained: product/account/business health diagnosis and publication-figure production. C1 rechecked their hashes, candidate counts, source diversity, and no reuse against all earlier C6 packets. C2 drafted 12 direct/paraphrase prompts; two literal source phrase overlaps were reworded, after which C3 passed 12/12. C3 records all final prompts as high residual operational-context risk, so they are not evidence of purely implicit user intent. Two source-deidentified model-assisted C4 reviewers independently returned the same singleton fully-adequate card for every packet; their returned card-level adequacy decisions were preserved in a compact local transcription and exact evidence citations were re-extracted from the same anonymous cards before the C4 validator ran. C5 unsealed all 12 singleton mappings and confirmed their sealed C2 targets; C6 froze two new candidate compositions and 12 primary strict packets. The running strict curation total is **29 frozen cross-source candidate compositions / 188 strict prompt packets**. This remains curation and feasibility evidence only: no retrieval, embedding, reranking, API, metric, or downstream-task result has been run. Evidence: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round18_structural_ledger_validation_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round18_literal_cue_audit_2026-08-27.json`, `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round18_model_assisted_consensus_2026-08-27.json`, and `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round18_primary_freeze_summary_2026-08-27.json`.

> **2026-08-27 RQ1b Round 19 M0--C6 closure.** A fresh broad M0 pass recorded 110 raw leads and reduced them to 95 new public GitHub roots after prior-root exclusion. M1 commit-pinned and byte-staged 1,626 canonical `SKILL.md` originals from 51 origins without executing source code; sources without a declared repository licence remain provenance-tagged rather than excluded. M2/C0A produced twelve source-navigation proposals. C0B exact-validated 36 source-evidence substrings, structurally rejected eleven proposals for nonparallel or asymmetric routes, and retained one source-backed 3-candidate marketing-copy composition. C1 passed hashes, origin diversity, and prior-C6 non-reuse. Six direct/paraphrase C2 prompts passed final literal C3 after one cue-only rewording, but every packet retains `high` residual operational-context risk. Two source-deidentified, model-assisted (not human) C4 reviewers agreed on a unique fully-adequate card for four prompts and disagreed on two because an additional candidate could be fully adequate. A citation-only repair restored literal Markdown/line-break evidence spans without altering either reviewer's adequacy choices or rationales; the C4 audit then passed. C5/C6 froze the one composition's four agreed strict packets and excluded the two disagreements from strict top-1. The live strict curation total is **30 frozen cross-source candidate compositions / 192 strict prompt packets / 5 unresolved prompts**. These remain curation and feasibility counts only, not retrieval, representation, embedding, reranking, API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 19 M0-C6 Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 20 M0--C6 closure.** Discovery-first M0 recorded 146 raw GitHub leads, canonicalised them to 141 roots, and excluded 29 roots already represented in prior intake, leaving 112 new roots. M1 commit-pinned 98 small-source roots and byte-staged 2,291 `SKILL.md` paths without executing source code. Exact-byte canonicalisation retained 2,282 originals from 88 origins; nine duplicate aliases remain provenance-only and sources without a declared repository licence remain eligible with their status recorded. M2/C0A produced twelve source-navigation proposals. Four independent C0B source-packet reviewers exact-validated 105 literal source substrings, structurally rejected eleven nonparallel, container/component, lifecycle, adapter/interface, or generic-specialist proposals, and retained one source-backed 3-candidate model-routing composition. C1 passed source hashes, three distinct origins, and non-reuse against every prior C6 composition. C2 produced six direct/paraphrase packets; a C3 cue-only wording repair led to a 6/6 literal pass, while every final prompt retains `medium` residual operational-context risk. Before C4, ID-only queue materialisation and then a residual comment-marker check both failed closed; a backwards-compatible local resolver/scrubber repair changed no candidate, prompt, label, or source text and the final 6 anonymous packets passed deidentification. Two independent source-deidentified, model-assisted (not human) C4 reviewers agreed on five exact singleton packets and one multi-adequate packet. C5/C6 froze the five singleton packets from one composition; the multi-adequate packet remains outside strict top-1. The live strict curation total is **31 frozen cross-source candidate compositions / 197 strict prompt packets / 6 unresolved prompts**. These remain curation and feasibility counts only, not retrieval, representation, embedding, reranking, API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 20 M0-C6 Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 21 M0--C6 closure.** Discovery-first M0 recorded 173 public GitHub leads; M1/M2 locally staged 1,419 canonical navigation records from 60 origins without executing source code. C0A proposed 21 source-navigation triads; one source-backed data-protection-compliance triad passed C0B exact evidence and C1 integrity. Its six C2 packets passed C3 literal cue audit; manual records retain `medium` or `high` residual operational-context risk. Two independent source-deidentified, model-assisted (not human) C4 reviewers reached exact singleton agreement for all six packets, and C5/C6 froze the six packets from that one composition. The other 20 C0B structural-reject dispositions remain pending batch-transcript integration and are not counted as fully integrated records. The live strict curation total is **32 frozen cross-source candidate compositions / 203 strict prompt packets / 6 unresolved prompts / no retrieval results**. These are curation and feasibility counts only, not representation, selector, model/API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 21 M0-C6 Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 22 M0--C6 closure.** Discovery-first M0 canonicalised 127 public-source leads to 100 exact-new roots; M1/M2 byte-staged and source-navigated 585 canonical `SKILL.md` originals from 38 origins without executing source code. Four C0A domain lanes proposed seven source-navigation triads. C0B exact-validated 54 literal source-evidence substrings, retained one source-backed three-origin document-authoring triad, and structurally rejected six proposals; C1 passed the retained composition's source hashes, origin diversity, candidate size, and no-reuse check. Six direct/paraphrase C2 packets passed C3 literal audit, with manual records retaining medium or high operational-context risk. Two independent source-deidentified, model-assisted (not human) C4 reviewers reached exact singleton agreement for four packets and disagreed on two document-authoring/verification packets; only the four agreements passed C5/C6. The live strict curation total is **33 frozen cross-source candidate compositions / 207 strict prompt packets / 8 unresolved prompts / no retrieval results**. These are curation and feasibility counts only, not representation, selector, model/API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 22 M0-C6 Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 23 M0--C0A no-proposal closure.** Discovery-first M0 recorded 90 public-source leads, canonicalised them to 25 exact-new roots after prior-root exclusion, and M1/M2 retained 249 byte-verified navigation records from 11 origins without executing source code. Three independent source-navigation C0A lanes then formed no legal 3--4-candidate proposal: one lane had only two origins, while the other lanes' apparent groups had generic-specialist, lifecycle, container/component, interface-only, or multi-adequacy risk. No C0B/C1/C2--C6 work was attempted. The strict state remains **33 frozen cross-source candidate compositions / 207 strict prompt packets / 8 unresolved prompts / no retrieval results**. This is a strict-public-triad feasibility record, not a negative retrieval or representation result. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 23 M0-C0A No-Proposal Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 24 M0--C0A no-proposal closure.** Four discovery lanes recorded 103 public GitHub leads; M0 retained 42 exact-new roots after 53 prior-root exclusions. M1/M2 byte-staged and source-navigated 201 canonical originals from 15 origins without executing source code; stage and census failures remain explicit non-admissions. Two C0A lanes had fewer than three origins. Two independent C0A curators reviewed the remaining business/policy and software/infrastructure lanes and found no bounded cross-origin 3--4-candidate formation without generic-specialist, lifecycle, container/component, interface, or multi-adequacy risk. No C0B/C1/C2--C6 work was attempted. The strict state remains **33 frozen cross-source candidate compositions / 207 strict prompt packets / 8 unresolved prompts / no retrieval results**. This is a strict-public-triad feasibility record, not a negative retrieval or representation result. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 24 M0-C0A No-Proposal Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 25 M0--C6 closure.** Four targeted discovery lanes recorded 89 public GitHub leads; after canonicalisation and 37 prior-root exclusions, M0 retained 47 exact-new roots. M1/M2 byte-staged and source-navigated 198 hash-verified public originals from 14 origins without executing source code; unreachable, census, and staging failures remain explicit non-admissions. C0A produced two source-navigation triads: C0B exact-validated 18 literal source-evidence substrings, structurally rejected the research-analysis triad because it included an interface router and nonparallel routes, and retained one document-transform triad. C1 passed its three source hashes, distinct origins, candidate uniqueness, and no-reuse check. Its six C2 packets passed final C3 literal audit after one cue-only wording repair; manual C3 records retain four `high` and two `medium` residual operational-context risks. Two independent source-deidentified, model-assisted (not human) C4 reviewers reached exact singleton agreement for all six packets. C5/C6 froze the one composition and its six packets with no integrity failure. The live strict state is **34 frozen cross-source candidate compositions / 213 strict prompt packets / 8 unresolved prompts / no retrieval results**. These are curation and feasibility figures only, not representation, selector, model/API, metric, or downstream-task results. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 25 M0-C6 Closure - 2026-08-27.md`.

> **2026-08-27 RQ1b Round 26 M0--C3 in progress.** A fresh discovery-first pass recorded 110 public GitHub leads, canonicalised them to 103 roots, and retained 53 exact-new roots after 50 historic-root exclusions. M1 pinned all 53 and used blob-filtered tree census (2,476 `SKILL.md` paths); the predeclared 3--64-path cohort selected 25 origins. A corrected `round26-m1v2` staging pass fixed an inherited `r24m1` ID-prefix provenance defect without changing any source bytes: it retained 707 unique, hash-verified originals from 25 origins, with 18 missing-frontmatter and 13 exact-duplicate paths excluded from navigation. C0A created nine source-navigation proposals; C0B exact-validated 71 source substrings, structurally rejected seven nonparallel/container/lifecycle/asymmetric proposals, and retained two source-backed drafts. C1 passed both drafts with no frozen-candidate reuse. C2 created 12 direct/paraphrase prompts and C3 v2 passed literal audit 12/12 after two cue-only rewordings. The separate model-assisted manual C3 review records six `high` and six `low`/`medium` residual cue risks. **No blinded C4, C5, or C6 action has occurred; the live strict total remains 34 frozen compositions / 213 strict packets / 8 unresolved prompts / no retrieval results.** The two Round 26 drafts are not valid clusters and must either retain explicit high-cue annotations or be revised before C4. Evidence: `m1_round26_source_navigation_summary_v2_2026-08-27.json`, `c0b_round26_literal_validation_summary_2026-08-27.json`, `c1_round26_integrity_summary_2026-08-27.json`, `c3_round26_mechanical_cue_audit_v2_2026-08-27.json`, and `working/c3_round26_manual_dispositions_2026-08-27.jsonl`.

> **2026-08-28 RQ1b Round 26 C4--C6 closure and Round 27 M0 intake.** Round 26's two source-backed, three-candidate compositions advanced only after a schema-normalisation card preserved all 12 C3 rationales and their six `high` residual-cue annotations. Two independent source-deidentified, model-assisted (not human) C4 reviewers covered all 12 blinded packets. A four-citation exact-substring repair changed only card-evidence spans, never adequacy or rationale; the final key-blind audit has 12/12 exact singleton agreements, zero multi-adequate packets, zero disagreements, and no audit failure. C5 confirmed every unsealed singleton matched its sealed C2 construction target, and C6 rechecked C1 hashes, candidate composition, reuse, and C3 coverage before freezing two compositions and 12 packets. The live strict state is now **36 frozen cross-source candidate compositions / 225 strict prompt packets / 8 unresolved prompts / no retrieval results**. In parallel, Round 27 discovery recorded 131 navigation-only public leads, canonicalised them to 119 roots, excluded 80 exact historic roots, and retained 39 new roots for M1; no source body, candidate composition, prompt, label, retrieval input, or metric has yet been created from Round 27. These are curation and feasibility figures only, never a selector result or implicit-semantic evidence. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 26 C4-C6 Closure and Round 27 M0 Intake - 2026-08-28.md`.

> **2026-08-28 RQ1b Round 27 M1--C6 closure.** Of the 39 exact-new M0 roots, 37 were commit-pinned and two unreachable roots remain explicit non-admissions. Blobless census found 4,808 `SKILL.md` paths; the predeclared 3--64-path cohort staged 630 paths from 28 origins. M1 rehashed every preserved original, retaining 612 canonical navigation records after 17 missing-frontmatter paths and one exact-byte duplicate were excluded. Four isolated C0A workers proposed 11 navigation-only triads; C0B exact-validated 66 source-evidence substrings, structurally rejected 10 directions, and retained one three-origin social-copy triad. C1 passed source hashes and prior-C6 non-reuse. Its first six C2 prompts passed literal C3 but were held as high source-identifying operational bundles; the separate v2 C2 set was retained instead after a fresh literal C3 pass and an independent manual C3 review recorded six `medium` residual-cue explicit-context cases. Two source-deidentified, model-assisted (not human) C4 reviewers returned 2 exact singleton agreements, 1 multi-adequate agreement, and 3 disagreements. A C5 implementation defect that initially collapsed the multi-adequate packet into unresolved was corrected in a new `v3_corrected` ledger; the prior `v2` output remains preserved and superseded. C6 froze only the two strict packets from the one composition; the multi-adequate packet remains exploratory and the three disagreements remain outside strict top-1. The live strict state is **37 frozen cross-source candidate compositions / 227 strict prompt packets / 12 unresolved-or-exploratory prompts / no retrieval results**. These are curation and feasibility figures only, never selector performance or implicit-semantic evidence. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 27 M1-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b Round 28 M0--C6 closure.** Four discovery lanes recorded 163 public leads, retaining 57 exact-new roots after historic-root exclusion. M1 byte-staged 296 canonical, hash-verified public originals from 20 origins without executing source code; M2/C0A formed six navigation-only triads. C0B exact-validated 36 source-evidence substrings, rejected five structural nonparallel/asymmetric directions, and retained one three-origin project-status triad. C1 passed its hashes, origin diversity, and non-reuse check. Six direct/paraphrase C2 packets passed literal and manual C3 with low residual operational-context cue risk. Two source-deidentified, model-assisted (not human) C4 reviewers agreed on one singleton fully adequate card for every packet. A four-span citation-only repair corrected Markdown/newline evidence spans without changing any adequacy judgment or rationale; final C4 audit passed. C5/C6 froze one new composition and six strict packets. The live strict state is **38 frozen cross-source candidate compositions / 233 strict prompt packets / 12 unresolved-or-exploratory prompts / no retrieval results**. These are curation/feasibility figures only, never selector performance or implicit-semantic evidence. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 28 M0-C6 Closure - 2026-08-28.md`.

| Workstream | Current state | What exists now | Next permission |
|---|---|---|---|
| RQ1a seven operational-field suites | `REVIEWED / COMPLETE` | 350 reviewed clusters and 750 prompts across seven fields. | Keep frozen except for proven errors; reuse reviewed propositions in RQ2a. |
| RQ1a examples/tests | `COMPLETE / SUPPORTING` | Negative-control evidence that generic examples are support text rather than stable routing evidence. | No broad redesign. |
| RQ1b public-realism audit | `COMPLETE / SUPPORTING CONTEXT` | Recoverability audit over 460 public originals. | Corrective QA only; it is distinct from the naturalistic replication. |
| RQ1b naturalistic public-skill replication | `WAVE 001 FROZEN / NATURAL_ORIGINAL_ONLY / NOT EXECUTED` | 62 valid clusters over 129 source-disjoint original candidates; two prompts each, model-assisted two-reviewer singleton acceptable-set agreement, exact residual maps, and frozen hashes. | Meets the 50-cluster natural-original threshold. All are original-only, not mask-eligible; do not claim causal masking, human annotation, or selector performance. No retrieval or external transmission has run. |
| RQ1b Wave 002 naturalistic extension | `P0-P4 FROZEN / 432 ORIGINALS / 17 VALID ORIGINAL_ONLY` | Five new pinned public sources across legal, science/clinical, finance, marketing, and education; all 25 logged families were read locally, yielding 17 frozen clusters and 8 explicit rejections. The final 34 prompts passed P1 with zero candidate-name, heading/short-line, or exact 3/4-token source-phrase hits; P2 has 34/34 current two-reviewer model-assisted singleton decisions (R1 replaces three revised prompts); P3 marks all 17 original-only. Zero candidate reuse within Wave 002 and zero Wave 001 overlap. | Preserve the separate freeze and evidence boundary. Do not append to Wave 001 or run representation, selector, API, or scoring work unless separately designed and authorised. |
| RQ1b Wave 003 mass candidate pool | `D4C INITIAL + SECOND + THIRD + FOURTH + FIFTH COMPLETE / 31 DRAFTS / 30 REJECTIONS / 516 NET-NEW` | Nine pinned, direct, licensed sources produced 573 byte-preserved files. Local integrity audit verified all staged SHA-256 values, found zero pre-Wave overlap, retained/excluded 57 same-wave byte duplicates, and established 516 net-new artifacts. D4a reverified every canonical original and emitted source-provided metadata only. The complete 14-family initial D4c queue created nine drafts and five rejections; the complete separate 11-family queue added five drafts and six rejections, including a candidate-reuse exclusion that preserves Draft 003. The complete third twelve-family queue added five drafts and seven rejections after full-source reading, including explicit containment, subsystem/prerequisite, resource-management, and pointer-only exclusions. The completed fourth twelve-family queue added seven drafts and rejected five pairs for contained/subcomponent, prerequisite, non-neighbour training-family, or sequential-composition relations. The completed fifth twelve-family queue added five drafts and rejected seven pairs for platform specialisation, broad-review subsumption, bidirectional overlap, orthogonal/composable properties, explicit specialised routing, model-selection followed by feasibility checking, and prelaunch-versus-active-failure work. | The 500-artifact source-volume target is met, but it is not a 516-cluster benchmark. Next: nominate another unused D4b family or begin P0--P4 only under a separate authorised curation plan; every current draft remains ineligible for selector/API/scoring work. |
| RQ1b Wave 003 latest 2026-08-25 update | `SIXTH D4C PARTIAL / 32 DRAFTS / 33 REJECTIONS / 8 PAIRS UNREAD` | Sixth queue identity audit found zero prior appearances for all 24 candidate IDs. Its first four full-source decisions yielded one source-backed draft and three explicit rejections for design-then-implementation or containment relations. | This is still source screening only; no Wave 003 item is a valid cluster or eligible for selector/API/scoring work. |
| RQ1b same-repository multi-candidate feasibility audit | `CLOSED AS FEASIBILITY AUDIT / M0 262 / M1 ROUNDS 2-13 / 2,713 BYTE-AUDITED ORIGINALS / 1,486 POST-HOLD NAVIGATION ARTEFACTS / M2 A-M 11 DRAFTS, 74 REJECTS / NO NEW FROZEN QUARTET BENCHMARK` | This line asked a narrow ecosystem question: whether one real public library naturally contains a strict 3--4 candidate routing problem, excluding containers, components, lifecycle stages, specialised implementations, and provider/interface variants. The source-first process preserved 2,713 originals. Rounds 3-13 supply 1,486 post-hold navigation artefacts, but M2 A-M yields 11 source-backed drafts with broad-envelope/multi-adequacy risk and 74 explicit structural rejections; no Wave 003 M6 quartet was frozen. Together with the separate E1 audit (six strict frozen triads from 74 parent pairs), this supports only the cautious feasibility reading that strict same-repository multi-neighbour units can exist but are scarce under the protocol. It is not an RQ1b main benchmark, retrieval result, or a claim about cross-source aggregate libraries. | Preserve all sources and rejection evidence. Do not continue same-repository triad/quartet mining or use its drafts as performance data. Main RQ1b curation moves to `skill_benchmark/rq1b_cross_source_public_benchmark/` under its separate frozen protocol. |
| RQ1b cross-source public-skill benchmark (main) | `ROUND 40 C6 FROZEN / 69 FROZEN CANDIDATE COMPOSITIONS / 383 FROZEN STRICT PROMPT PACKETS / 72 UNRESOLVED-OR-EXPLORATORY-OR-TARGET-MISMATCH PROMPTS / NO RETRIEVAL RESULTS` | Main naturalistic RQ1b unit: a curated 3--4 candidate aggregate-library cluster whose individual candidates are exact-byte-preserved public original skills from at least two sources. Declared licences are retained as provenance metadata; absence of one is not an eligibility exclusion or a redistribution claim. Amendment 01 permits symmetric operational variants when every candidate supplies a peer first-route under a bounded shared envelope; it retains exclusions for containers, components, prerequisites, lifecycle stages, adapters, duplicates, and generic--specialist asymmetry. The primary stratum requires two blinded, model-assisted reviews to agree on the same single fully adequate candidate for each cue-controlled prompt. A multiple-adequate or reviewer-disagreement prompt is separate and never forced into strict top-1. The source pool is origin-agnostic: sources are combined to simulate an aggregate library, not mined one repository at a time. Round 40 corrected an M1 historic-prefix defect without source-byte change; from 108 net-new roots it byte-staged 816 SHA-verified originals from 46 origins, then advanced three C1 triads. After source-informed C2 rewrites, final C3 allowed all 18 cue-controlled packets with residual risk retained. C4 produced 16 strict singleton agreements and two disagreements; 27 citation repairs changed only evidence spans. C6 froze three compositions and 16 strict packets. All final packets retain residual cue-risk annotations and must not be described as evidence of implicit semantic routing. | Continue discovery-first, origin-agnostic public-source expansion toward the current 75-composition goal while retaining the same strict gates. The 383 frozen prompt packets are curation artefacts, not 383 independent clusters, retrieval inputs, model results, or metrics; C6 froze 69 candidate compositions only. No model/API/retrieval work is authorised. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 39 M0-C6 Closure - 2026-08-28.md` and `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 40 M0-C6 Closure - 2026-08-28.md`. Authority: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md`. |
| RQ1b cross-source main live override | `ROUND 41 C6 FROZEN / 72 COMPOSITIONS / 401 STRICT PACKETS / 78 NON-PRIMARY / NO RETRIEVAL RESULTS` | Round 41's four C1-passed cross-source triads passed final C3 cue control after a lineage-preserved 16-prompt rewrite/recheck and three-prompt post-review. Two anonymous model-assisted C4 reviews produced 18 strict singleton, three multi-adequate, and three disagreement packets. C5/C6 froze only three triads and 18 strict packets; multiple-adequate and disagreement packets remain outside strict top-1. | This row supersedes the earlier Round 40 live count. Continue fresh-discovery-first C0--C6 toward 75 compositions. Counts are curation artefacts, not 401 independent tasks, human labels, selector inputs, model results, or metrics. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 41 M0-C6 Closure - 2026-08-28.md`. |
| RQ1b cross-source main live override | `ROUND 42 C6 FROZEN / 76 COMPOSITIONS / 408 STRICT PACKETS / 119 NON-PRIMARY / NO RETRIEVAL RESULTS` | Round 42 performed fresh M0--M1 discovery/staging, admitted six C0B source-backed drafts through C1, then applied literal and source-informed C3 cue control. Final C3 retained 36 low- and 12 medium-risk packets, with zero high-risk packet advanced. Two anonymous model-assisted C4 reviewer pairs judged 48 packets: seven agreed singletons, 34 multiple-adequate, and seven disagreements. C5/C6 froze the seven sealed-target-matched packets over four candidate compositions; source hashes and candidate reuse passed. | This row supersedes the Round 41 live count and meets the user-directed 75-composition curation target. The 408 strict packets and 119 non-primary packets are curation artefacts, not independent tasks, human labels, selector inputs, model results, or metrics. No retrieval/API/embedding/reranking work ran. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 42 M0-C6 Closure - 2026-08-28.md`. |
| RQ1b V3 large-frame C0 source triage | `W1--W10 COMPLETE / 29,292 CANONICAL PUBLIC ORIGINALS / 300 TRIADS SCREENED / 28 HISTORICAL C1 SOURCE-EVIDENCE PERMISSIONS / NO V3 VALID CLUSTER OR RETRIEVAL RESULT` | V3 keeps a separately frozen, hash-deduplicated local public-original source frame for discovery and structural heading census. Ten deliberately diversified, zero-overlap C0 waves have screened 300 lexical cross-origin triads source-only. Wave 010 rejects all 30 before C1 (21 container/component/nonparallel, two insufficient contrast, seven no common envelope). The C0 lexical path demonstrates why same-topic title/FTS neighbours cannot be treated as peer route candidates. | This is not an all-public-skill census, taxonomy-induction claim, semantic field-prevalence estimate, valid cluster count, human annotation, prompt/gold result, selector input, metric, or retrieval result. The structural census reports only explicit heading markers. Preserve C0 as a lexical-discovery calibration; the two W7 and one W8 C1 permissions all failed source-evidence review before prompt construction. Evidence: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`, `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 010 Closure - 2026-08-29.md`, `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_010_2026-08-29/C0_SOURCE_REVIEW_WAVE_010_FINALISER_AUDIT.json`, and `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_003_2026-08-29/C1_SOURCE_EVIDENCE_WAVE_003_FINALISER_AUDIT.json`. |
| RQ1b V3 D1 Wave 006 source-semantic recruitment | `COMPLETE / FIVE LOCAL-ONLY LANES / THREE W6R2 SOURCE-BOUND TRIADS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | Five source-only lanes proposed three cross-source triads. The original W6 and W6r1 quotation failures are preserved; W6r2 changes only literal evidence, rehashes all nine originals, passes zero-reuse source binding, and enters prompt-free C1. C1 rejects web deployment and CI/CD for insufficient operational contrast beyond provider/runtime implementation, and Semgrep/CodeQL/Horusec because Horusec is a broad multi-tool container. | This is not an all-public-skill census, semantic-field prevalence estimate, strict cluster, prompt, gold label, field annotation, selector input, metric or retrieval result. It records a source-only feasibility limit: provider and implementation names cannot stand in for bounded, request-relevant peer-route differences. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 006r2 And C1 Closure - 2026-08-29.md`, `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_006r2_2026-08-29/D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json`, and `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_006r2_2026-08-29/C1_SOURCE_EVIDENCE_WAVE_006R2_FINALISER_AUDIT.json`. |
| RQ1b V3 D1 Wave 007r1 source-semantic recruitment | `C1-C3 COMPLETE / FIVE SOURCE-BOUND TRIADS / TWO C2 PERMISSIONS / 12 DRAFTS / 8 C3-ALLOWED / 4 UNSAFE-CUE REJECTS / NO VALID CLUSTER OR RETRIEVAL RESULT` | The initial materialisation failure is retained; r1 changes only six nonliteral excerpts and passes literal evidence, source binding, rehash and source-reuse checks for 15 originals. C1 advances database-distribution migration and workflow-orchestration migration; proposal and compliance reject for no common envelope, while video derivatives reject as adjacent workflow components. The two C1 advances yield 12 cue-controlled drafts; C3 allows eight after local mechanical scan, and rejects four workflow-migration prompts even after a preserved cue-only r1 rewrite because their necessary rule bundles remain high residual cues. | C3 allowance is not cue-safety proof, gold-label validation, field annotation, representation, selector input, metric or routing result. The eight allowed packets remain stopped behind the separate C4A field-card schema hold. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 And C1 Closure - 2026-08-30.md`, `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 C2-C3 Closure - 2026-08-30.md`, and `skill_benchmark/rq1b_v3_public_source_frame/c3_cue_control_wave_007r1r1_2026-08-30/C3_FINALISER_AUDIT.json`. |
| RQ1b V3 D1 Wave 008 source-first expansion | `COMPLETE / FIVE LOCAL-ONLY LANES / ONE NO-CANDIDATE / TWO PRE-MATERIALISATION REJECTS / TWO C1 REJECTS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | Wave 008 uses previously unused canonical sources from the frozen 29,292-artifact public-original frame. Two recruits (database schema migration and WCAG accessibility audit) pass r2 source hash, literal-span and zero-reuse materialisation across six origins, after an earlier retained binding/span failure. Independent source-only C1 and coordinator review reject both as generic-specialist/nonparallel scope: a broad migration container sits alongside tool/ORM routes, and static-code/page-component/comprehensive-site audits are not peer first routes. | This is a discovery feasibility negative, not semantic field-prevalence, strict singleton-label, field-effect, selector, metric or retrieval evidence. The structural-marker census remains descriptive; no C2--C6 work is authorised or required for this wave. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 008 And C1 Closure - 2026-08-30.md` and `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_008_2026-08-30/C1_SOURCE_EVIDENCE_WAVE_008_FINALISER_AUDIT.json`. |
| RQ1b V3 structural marker summary | `COMPLETE / 29,292 CANONICAL ORIGINALS / LOCAL-ONLY HEADING-MARKER DESCRIPTION / NOT SEMANTIC PREVALENCE` | The deterministic seven-marker matcher spans 1,564 canonical-content origin identities (and 1,613 raw source-path origin identities when duplicate aliases retain additional provenance): workflow/procedure marker 45.514%, output/artifact 31.684%, use-condition 30.418%; 24.952% have no matching marker and only seven have all seven. Pairwise marker co-occurrence and source-origin coverage are retained for later public recoverability sampling. | Do not say the fields were discovered from this corpus, that heading absence proves semantic absence, or that these marker counts establish routing value. The analysis has no prompt, gold, selector, metric or retrieval result. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/structural_marker_summary_v3_2026-08-29/STRUCTURAL_MARKER_SUMMARY.md`. |
| RQ1b V3 C1 source-evidence Wave 002 | `COMPLETE / TWO W7 C0 PERMISSIONS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | The two lexical C0 advances were source-hash-bound and independently reviewed without prompts/labels. The performance-decay trio rejects for no bounded common envelope; the threat-intelligence trio rejects as producer-consumer lifecycle roles. | This screening negative does not test any information field, representation or retriever. It records why two tempting same-topic triads cannot become strict clusters. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_002_2026-08-29/C1_SOURCE_EVIDENCE_WAVE_002_FINALISER_AUDIT.json`. |
| RQ1b legacy cross-source to V3 provenance map | `PASS / 26 C6 MANIFESTS / 408 PRIMARY ROWS / 391 PACKET IDS / 76 COMPOSITIONS / ALL SHA-MAPPED / NOT MERGED` | The local audit maps every legacy C6 frozen-primary candidate SHA to one canonical record in the V3 source frame: 57 triads and 19 quartets, with zero unmapped compositions. | Hash inclusion proves only shared immutable source provenance. It does not pool protocols, convert model-assisted legacy C3/C4 into V3/human annotation, validate V3 cards, create a V3 strict label, or authorise selector/retrieval work. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/legacy_c6_mapping_2026-08-29/legacy_c6_to_v3_source_frame_mapping.json`. |
| RQ1b V3 D1 directed discovery | `W1 C1 COMPLETE / 4 SOURCE-ONLY TRIADS / 1 C2 PERMISSION / 3 C1 REJECTS / NO CLUSTER OR RETRIEVAL RESULT` | D1 searches for explicit natural source-to-target, artifact-format, runtime or interface constraints while keeping every later gate unchanged. W1 rehashed 12 originals and literal-validated every card span. C1 retained only the typed PDF/DOCX/XLSX-to-Markdown peer-route triad for later prompt construction. It rejected a serial version-upgrade lifecycle and two runtime/framework-only families whose core operational route remained the same. | A C1 advance is not semantic validation, a prompt, gold label, valid cluster, selector input, metric or routing result. D1 stays separately counted from lexical C0; future waves must continue source-first discovery and the unchanged C1--C6 gates. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/c1_source_evidence_wave_001/C1_SOURCE_EVIDENCE_WAVE_001_CHECKPOINT.md`. |
| RQ1b V3 D1 directed discovery | `W2 MATERIALISED / 2 CROSS-ORIGIN TRIADS / 6 REHASHED ORIGINALS / C1 ACTIVE / NO CLUSTER OR RETRIEVAL RESULT` | W2 adds a provider-specific web-hosting triad (Vercel/Render/Netlify) and a hosted-LLM integration triad (OpenAI/Claude/Gemini). Both have exact trigger/operation/output/constraint spans and no source reuse, but neither has a prompt, intended winner or strict label. C1 must reject any broad fallback, container, multiple-adequate or interface-only composition before C2. | Mechanical binding is not peer-route validation, cue control, singleton adequacy, field evidence or routing evidence. W2 is reported separately from lexical C0 and D1 W1. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json`. |
| RQ1b V3 D1 directed discovery | `W2 C1 COMPLETE / 2 CROSS-ORIGIN TRIADS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | C1 rejects both W2 compositions after rehash and literal evidence checks. Vercel/Netlify are direct deploy-to-URL routes but Render is a resource/deployment container; OpenAI/Claude/Gemini share the same text-generation operation and vary provider/client interface only. | These are source-only peer-route findings, not prompts, strict gold labels, field effects or routing results; they should guide new discovery rather than weaken C1 standards. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/c1_source_evidence_wave_002/C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md`. |
| RQ1b V3 D1 directed discovery | `W3 INITIAL MECHANICAL FAIL RETAINED / W3R1 C1 COMPLETE / 3 TRIADS / 9 ORIGINALS / ZERO C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | W3's first materialisation failed closed because one LGPD constraint excerpt was not literal. W3r1 changes only that source span, then rehashes and literal-validates all nine source originals. C1 rejects Scala/Java/PySpark as one migration chain with insufficient contrast, the PDF triad for a generic parser container, and the privacy triad for broad-programme versus specialist-workflow asymmetry. | These source-only peer-route findings do not show that language, output, jurisdiction or boundary information lacks routing value in general. They establish neither cue safety, a prompt, strict singleton label, field effect, representation, selector input nor routing result. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_003_2026-08-29/` and `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_003r1_2026-08-29/c1_source_evidence_wave_003r1/C1_SOURCE_EVIDENCE_WAVE_003R1_CHECKPOINT.md`. |
| RQ1b V3 D1 directed discovery | `W4 INITIAL MECHANICAL FAIL RETAINED / W4R1 C1 COMPLETE / 3 CROSS-ORIGIN TRIADS / 9 ORIGINALS / THREE C2 PERMISSIONS / NO CLUSTER OR RETRIEVAL RESULT` | W4r1 corrects only nonliteral Markdown-formatting spans from the retained W4 materialisation failure, then rehashes and literal-validates nine cross-origin originals. Source-only C1 permits later prompt construction for agreement review, structured-data visualisation and presentation-authoring compositions. The NDA source retains `NOT STATED` for its absent explicit boundary; no constraint was invented. | C1 advances are neither valid clusters nor gold labels. C2 must construct de-cued direct/paraphrase prompts, C3 must audit source/name/template/tool cues, two key-blind C4 reviews must agree on one fully adequate candidate, and C5/C6 must freeze the full lineage before any selector experiment. Evidence: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_004r1_2026-08-29/c1_source_evidence_wave_004r1/C1_SOURCE_EVIDENCE_WAVE_004R1_CHECKPOINT.md` and `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 C2 Prompt Construction and Cue-Control Handoff SOP - 2026-08-29.md`. |
| RQ1b V3 C2-C3 cue-controlled prompt packet wave | `COMPLETE / 4 C1-APPROVED COMPOSITIONS / 24 PACKETS ALLOW C4 / 20 HIGH RISK / 4 MEDIUM RISK / NO CLUSTER OR RETRIEVAL RESULT` | C2 formed direct and intent-preserving paraphrase packets for each candidate. C3 preserved the original C2 ledger, performed one cue-only r1 wording change, and confirmed zero unresolved copied source phrases. It annotated genuine retained operational constraints rather than calling them implicit semantic evidence. | This does not validate a gold skill, source-card fidelity, singleton adequacy, selector input or metric. Build seven-slot anonymous cards, literal-audit them, then conduct two C4 key-blind selection-only reviews. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 C3 Wave 001 Cue Gate Checkpoint - 2026-08-29.md`. |
| RQ1b V3 C4A field-card builder packets | `MATERIALISED / 4 COMPOSITIONS / 12 HASH-VERIFIED ORIGINALS / NO CARD OR REVIEW RESULT` | Anonymous local builder packets use source copies and a fixed seven-slot evidence schema. The private source-to-label map is separate; public packets contain no prompt, title map, source ID or sealed C2 target. | This materialisation does not establish field-card fidelity or a strict label. Require two independent builder transcriptions plus literal/identity-line audits before C4B key-blind review. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 C4A Builder Packet Materialisation - 2026-08-29.md`. |
| RQ1b V3 C4A dual-builder calibration | `HOLD / 2 INDEPENDENT SOURCE-ONLY DRAFT BUILDS / NO CANONICAL CARD OR C4B REVIEW` | Independent builders materially differ on whether natural trigger-action-artifact statements belong to input, workflow or output. The drafts were not selected opportunistically; no literal-valid canonical card was created. | This is a field-card schema calibration issue, not a routing or field-effect result. Add a source-only slot-placement rule and rebuild independently before any C4B selection review. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 C4A Dual-Builder Calibration Hold - 2026-08-29.md`. |
| RQ1b V3 C4A v1.2 packet rebuild | `MATERIALISED / 4 COMPOSITIONS / 12 HASH-VERIFIED ORIGINALS / AWAITING INDEPENDENT BUILDERS / NO CARD OR REVIEW RESULT` | The v1.2 packet rules preserve non-exclusive literal excerpts but distinguish user input from dependency/resource and ordinary workflow from explicit success/verification. New anonymous packet copies are source-hash-bound and omit prompts, source maps and targets. | This does not cure the calibration hold by itself. Persist two independent source-only returns, literal-audit them, audit slot conformance without prompt/target access, then decide whether C4B can begin. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Wave 001 Packet Materialisation - 2026-08-29.md`. |
| RQ1b V3 D1 directed discovery | `W5 C1 COMPLETE / 20 SOURCE-ONLY DRAFTS / 7 C1 REVIEWED / 5 C2 PERMISSIONS / 2 C1 REJECTS / NO CLUSTER OR RETRIEVAL RESULT` | W5 retains five bounded peer-route compositions for later cue-controlled construction: accessibility remediation, content-corpus audit, transaction control, agreement-form review and data-model representation. Pre-release security is rejected as complementary controls; resource forecasting is rejected because its envelope is only an overly broad taxonomy. | A C2 permission is not a valid cluster, prompt validity, gold label, selector input or routing result. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 W5 C1 Source-Evidence Closure - 2026-08-29.md`. |
| RQ1b V3 C2-C3 cue-controlled prompt packet wave | `WAVE 002 COMPLETE / 5 C1-APPROVED COMPOSITIONS / 30 PACKETS ALLOW C4 WITH RISK ANNOTATION / 25 LOW, 1 MEDIUM, 4 HIGH / NO CLUSTER OR RETRIEVAL RESULT` | C2 constructed one direct and one intent-preserving paraphrase per candidate, then a mechanical cue inventory and independent source-deidentified review requested nine cue-only r1 changes. Fresh packet-level C3r1 recheck preserves all 30 under explicit residual-risk records. | This is neither cue-safety proof nor a strict label, source-card fidelity, singleton adequacy, selector input or metric. The four high-risk packets contain necessary but strongly route-specific operational detail and cannot be presented as implicit semantic routing evidence. C4A v1.1 fresh construction/literal audit remains required before C4B. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 C2-C3 Wave 002 Cue Gate Checkpoint - 2026-08-29.md`. |
| RQ1b V3 D1 W5 C1 source-evidence closure | `COMPLETE / 7 REVIEWED / 5 C2 PERMISSIONS / 2 REJECTS / NO CLUSTER OR RETRIEVAL RESULT` | Three independent source-only reviewers and a principal literal recheck retain five bounded peer-route compositions. Security is rejected because code/dependency/secret checking is complementary; forecasting is rejected because cash/workforce/capacity share only an overly abstract label. | A C2 permission is not a strict cluster or gold label. C2/C3/C4-C6 must still establish cue-controlled singleton adequacy; no selector or metric exists. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 W5 C1 Source-Evidence Closure - 2026-08-29.md`. |
| RQ1b cross-source masked field-evidence execution | `P0 MASTER-ROSTER PRECHECK PASS / P0.5 IN PROGRESS / P1-P7 NOT STARTED FOR THE REMAINING CORPUS / NO MASKS OR RESULTS` | The prospective paired design contains 76 candidate compositions, 209 strict routing-test families, and 408 prompt variants. A family is one candidate composition plus one strict-gold target; a single composition may therefore have several distinct masked conditions. It fixes prompt and candidate membership while comparing `natural_original` with `target_evidence_masked`. P0 has reconstructed all 408 strict C6-to-C2 prompt links across 26 locked C2 files, source-hashed every canonical artifact, and retained physical source lineage. The first four-family P0.5 pilot applies two anonymous prompt-and-candidate field coders, exact-substring response validation, sealed-gold compatibility, then P1/P2 mapping for the one initially lockable output-artifact family. Its source-wide field carrier structure is inseparable, so it too fails closed to `ORIGINAL_ONLY`; all four pilot families are original-only and no mask is permitted. | This is pre-retrieval local curation, not a frozen execution result. It supersedes neither historical Wave 001/Wave 002 original-only records nor RQ1a/RQ2. No mask, selector, embedding, API, or metric has run. Protocol: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Cross-Source Masked Field-Evidence Execution Protocol - 2026-08-28.md`; P0 roster: `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json`; pilot audits: `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p05_field_coding_round01_2026-08-28/P05_ROUND01_AUDIT.md` and `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p1_evidence_mapping_round01_2026-08-28/P1_P2_UNION_DECISION.md`. |
| RQ1b masked-execution checkpoint | `B01--B10 AND PILOT CURATION COMPLETE / B11 IN PROGRESS / 0 MASKED COPIES / 0 SELECTOR RESULTS` | Twelve post-pilot locked families are already `ORIGINAL_ONLY` after literal-valid P1/P2 mapping or P3 preflight. One union contained no inseparable cue, but P3 failed because mapped differential spans were non-unique/overlapping. | This is no-retrieval feasibility evidence only. Resume from the checkpoint, not from historical Wave 001/Wave 002 or RQ2: `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/RQ1B_MASKED_EXECUTION_CHECKPOINT_2026-08-28.md`. |
| RQ1b Wave 003 M2 queue hygiene | `RECORDED / FORWARD EXCLUSION RULE` | Audit of retained A--G source-screen ledgers finds 73 decisions, nine drafts, 64 rejects, and no prompt/label leakage. Eight IDs were reused only across rejected Wave F screens, so no valid packet is affected. | New M2 queues must exclude candidates from any protocol-complete source screen unless re-reading a named incomplete or quarantined record. Evidence: `wave_003_multicandidate_m2_candidate_reuse_audit_2026-08-26.md`. |
| RQ1b multi-neighbour expansion (E1) | `COMPLETE / STRICT PUBLIC-TRIAD FEASIBILITY AUDIT / 6 T0-T5 FROZEN TRIADS / NO RETRIEVAL` | The immutable audit covers 79 frozen natural-original clusters, 74 pairs, five pre-existing triplets, and 163 frozen candidate IDs. A local batch triage completed coverage for the final eight Wave 002 parents, then parent-curator T2 completed 74/74 parent-pair coverage: 78 source-screen decisions contain 69 rejections and nine source-backed drafts. T3 retained six strict singleton packets and rejected three multi-adequacy drafts; all six T3 survivors have two model-assisted blinded T4 singleton consensuses with cue-risk retained. T5 rechecked every original source hash and found zero cross-packet or third-candidate reuse, freezing six `VALID_TRIADIC_EXTENSION_ORIGINAL_ONLY` packets. Because 6/74 is below the predeclared 30-triad standalone robustness threshold, this is feasibility evidence only, not a multi-neighbour routing benchmark, causal field result, human annotation, or selector/embedding/API/retrieval result. Detailed evidence is in `rq1b_mn_e1_wave12_strict_feasibility_checkpoint_2026-08-26.md`. | Do not add third candidates by relaxing strict singleton or inserting workflow components. Treat E1 as closed. Any future Wave 3 expansion must be separately designed and frozen with a larger parent-pair pool; no retrieval/scoring is authorised by this E1 closure. |
| RQ2a matched-content mechanism study | `CONFIRMATORY COMPLETE / THESIS-INTEGRATED` | Eight validated representations, four primary selector runs, 13,200 confirmatory rows, frozen statistics, costs, failure analysis, and immutable evidence hashes. | No further RQ2a scoring required. Preserve the bounded claim and artifacts. |
| RQ2a field-aware selector | `CONFIRMATORY COMPLETE / UNIFORM-TOP-TWO` | Leakage-free seven-field Qwen adapter; frozen rule gains `+6.6pp` over Qwen fielded single-vector but is descriptively tied with flat Qwen. | Treat as Qwen-specific mechanism evidence, not a universal field-aware win. |
| RQ2a confirmatory result | `COMPLETE / USER-REVIEWED` | Primary Qwen fielded-minus-flat is `-6.7pp`; operational-content positive controls pass for BM25, Qwen, and SkillRouter. | Thesis integration complete; use `RQ2a Confirmatory Results and Analysis - 2026-08-02.md`. |
| RQ2b end-to-end full-library study | `BASE-V1 B0G BLOCKED / V1.1 STRICT-GOLD MANIFEST READY` | Frozen 2,433-skill/401-prompt base corpus, provenance-correct I1/I2, exact untransmitted I3C packet, v17 zero-network smoke, and a completed 7,710-unit B0G audit. Base-v1 cannot freeze an acceptable set. The focused remediation retains six gold labels and excludes eight prompts; its 381-scored-prompt strict-gold-only v1.1 manifest is locally validated. | B1R, Qwen calls, native SkillRouter encoder model download/compute or hosted transfer, reranking, and thesis writing remain later, separately authorised gates. |
| Graph/tree/downstream extensions | `OUT OF CORE / NOT ACTIVE` | Historical plans and partial artifacts only. | Do not run as current RQ2 work. |

Canonical state and completion gates: `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

## 2026-07-17 Historical RQ Focus And Claim-Discipline Checkpoint

This earlier checkpoint is retained for provenance. Its RQ2 classifications are superseded by the 2026-07-26 table above.

| Workstream | Primary RQ | Current status | Thesis use | Claim discipline |
|---|---|---|---|---|
| RQ1a field-isolation suites | RQ1 | Complete for use condition, input/precondition, output/artifact, dependency/resource, boundary/not-for, success/verification, and workflow/procedure. | Central evidence for which skill-side information helps distinguish semantically similar skills. | Report as controlled causal evidence under `shared_context_only` versus `shared_context_plus_field`, not as natural public-skill prevalence. |
| RQ1a examples/tests suite | RQ1 negative control | Complete as an adjacent diagnostic. | Shows that not every skill-document section is a routing signal. | Do not count examples/tests as an eighth operational routing field; frame as support/execution context unless the prompt nearly matches a stored example. |
| RQ1b public-realism audit | RQ1 external validity | Complete for 460 upstream public originals. | Shows whether the seven fields are present or recoverable in public skills. | Report as recoverability/audit evidence, not selector accuracy. Note noisy dependency and success/verification evidence. |
| Frozen-v0.4 I1/I2/I3 representation matrix | Historical RQ2-adjacent | Complete for local/Qwen/SkillRouter families, with caveats for historical rows. | Exploratory motivation and feasibility evidence only. | It is not matched-content confirmatory RQ2a evidence. |
| SkillRouter-Eval-Core I3C/I2 external track | Historical portability/cost | I3C is complete; neural I2 full-context comparator is incomplete except recovered partial rows. | Portability and scale-cost motivation only. | Do not claim a complete external neural comparison or a new RQ2 answer. |
| Graph/tree/grouping retrieval | Out of current core | Not evaluated. | Future work only. | Do not imply I4/I5 results exist because R4 edge files exist. |
| Downstream task validation | Secondary / not active | Planned only. | Possible later validation. | Until run, claims stop at routing/candidate selection. |

Presentation and synthesis work now applied in the thesis draft:

- Chapter 6 now puts the RQ1 field-isolation logic before the broader RQ2 strategy matrix.
- Chapter 6 now includes a compact RQ1 synthesis table with field tiers: strong, strong-but-contextual, conditional/reasoning-heavy, and support/negative-control.
- Chapter 6 now includes a representative qualitative pattern table for input/precondition, output/artifact, dependency/resource, and boundary/not-for.
- The field result paragraphs now state weaker prompt variants and the relevant claim boundary, especially for boundary/not-for, success/verification, workflow/procedure, and examples/tests.
- The draft uses consistent labels: `shared_context_only`, `shared_context_plus_field`, `direct`, `paraphrase`, `contextual`, `implicit_authority`, and `rare_exact_match`.
- Historical/global field-ablation tables are now labelled as diagnostic or RQ2-adjacent evidence rather than the main RQ1 causal claim.

## 2026-06-23 Methodology Correction Checkpoint

This checkpoint records the source correction made after the wrapper/original-doc concern.

- Local I3C has **not** been produced yet. No local Codex/ChatGPT subagent extraction has been run for the 2433 frozen-v0.4 skills. Current local structured-field rows remain I3H/R2/R3 unless explicitly relabelled after a future local I3C extraction and QA pass.
- Public imported full-body source is now corrected in the shared full-text loader: `run_offline_selectors.load_full_skill_texts()` calls `full_skill_source_path()`, so public imports prefer `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md` when present and fall back to the wrapper only if the original is missing.
- Public imported R1/R2/R3 export is now corrected: `export_skill_representations.py` keeps the stable local wrapper skill id but derives public-imported descriptions and structured extraction from `source/SKILL.original.md` when present, rather than mixing benchmark wrapper sections into the extracted fields.
- Public-style controlled skills were too regular and benchmark-like in the previous generator. `generate_public_style_controlled_expansion.py` now regenerates these 32 skills as messier public-style docs: average 741.5 rough words, varied headings, embedded tables/YAML handoff snippets, sibling-skill confusion notes, examples, and boundary prose. They still contain the intended use/input/output/procedure/dependency information, but not as one repeated clean schema. They are controlled synthetic skills, not upstream public originals.
- Public-style controlled regeneration checkpoint: `thesis_notes/checkpoints/benchmark/Public Style Controlled Messy Regeneration - 2026-06-23.md`.
- Rebuilt local representations after the patch: `skill_benchmark/representations/manifest.json` now reports 2433 skills, 2433 R1 rows, 2433 R2 rows, 2433 R3 rows, and 62032 R4 edges.
- Integrity check after rebuild passed: `skill_benchmark/outputs/benchmark_integrity_report.md/json` reports 245 prompts and 2433 skills.
- Refreshed local crossed lexical matrix after the messy public-style controlled regeneration: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md/json`. Controlled BM25 full top-1 is 66.5%, controlled TF-IDF full top-1 is 69.4%, public-gold BM25 full top-1 is 59.0%, and public-gold TF-IDF full top-1 is 48.6%.
- Refreshed Qwen provider matrix after the same correction: `skill_benchmark/outputs/frozen_v0_4_{controlled,public_gold}_qwen_{r1,r2,full}_{embedding,qwen_rerank_top20,local_schema_top20}.json`. Controlled Qwen + Qwen-rerank top-1 is I1 51.0%, I3H/R2 58.4%, I2/full 62.9%. Public-gold Qwen + Qwen-rerank top-1 is I1 73.6%, I3H/R2 70.8%, I2/full 72.9%.
- Refreshed Qwen-only fixed M6-v2 task-heavy reports: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md/json` and `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md/json`. These now intentionally include Qwen sources only; older SkillRouter M6-v2 fixed rows remain historical until a corrected-source SkillRouter rerun is performed.
- Compact rerun summary: `skill_benchmark/outputs/frozen_v0_4_refreshed_matrix_summary_2026_06_23.md`.
- Rerun checkpoint: `thesis_notes/checkpoints/benchmark/Local Matrix Rerun After Public Source Correction - 2026-06-23.md`.

## Current Source-Of-Truth Audit

This section is the anti-drift map. If a future result, thesis paragraph, or rerun disagrees with this section, pause before reporting it.

### Canonical Source Choices

| Source / stratum | What it is | What we use it for | Canonical source files | Why this source is used | Current caveat |
|---|---|---|---|---|---|
| Controlled frozen-v0.4 benchmark | Thesis-authored semantic-confusability benchmark with designed gold skills and near-neighbour alternatives. | Main causal evidence for whether information layers help under procedurally confusable skill selection. | `skill_benchmark/prompts/*.json`, `skill_benchmark/skills/**/SKILL.md`, freeze manifest `skill_benchmark/versions/benchmark-v0.4-2026-06-16.*` | It is controlled enough to isolate procedural distinctions, gold rationale, alternatives, and field axes. | Skills often explicitly expose proposed fields because this stratum is designed to test whether those fields matter. This is acceptable for causal testing, but not enough for external validity by itself. |
| Public-gold frozen-v0.4 benchmark | Publicly authored/imported skills promoted into gold-label retrieval cases. | External-validity stratum for messy public skills and provider/tool cues. Report separately from controlled. | Prompts: `skill_benchmark/prompts_public_gold/*.json`; labels: `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`; public skill originals: `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md` | It tests whether the information-layer story survives skills not authored only for the benchmark. | Final public-gold full-artifact rows must use `source/SKILL.original.md`. The shared full-text loader, representation exporter, local deterministic rows, and Qwen rows now use this policy; pre-correction SkillRouter rows remain historical until rerun. |
| Public imported wrappers | Normalized top-level public skill wrappers in the local benchmark tree. | Provenance, import bookkeeping, stable skill IDs, source URL/license metadata, background-scale inclusion. | `skill_benchmark/skills/public_imported_background/<skill>/SKILL.md` | They keep the imported corpus addressable by local skill IDs and retain source metadata. | They should not be treated as the final public full-body source for I2/RFULL comparison. Keep them for IDs/provenance; selection text should prefer `source/SKILL.original.md` when present. |
| Low-information stress prompts | Small prompt set with deliberately vague or weak procedural evidence. | Stress test for methods that depend on explicit request-side field cues. | `skill_benchmark/prompts_low_information/*.json` | It checks whether field-aware methods are merely exploiting richly worded prompts. | Not part of headline controlled/public-gold accuracy. Use as robustness or limitation evidence. |
| SkillRouter-Eval-Core external benchmark | Public external benchmark from `pipizhao/SkillRouter-Eval-Core`, with Easy/Hard pools and multi-skill tasks. | Portability and scale check outside the local benchmark. | Raw: `skill_benchmark/external/skillrouter_eval_core/raw`; derived: `skill_benchmark/external/skillrouter_eval_core/derived`; outputs: `skill_benchmark/external/skillrouter_eval_core/outputs` | It tests whether information-layer claims transfer to 78K-79K public-skill pools and multi-skill routing metrics. | It is not the same difficulty regime as local controlled. SkillRouter tasks are longer and more explicit, and skill bodies are often clean markdown documentation. Do not use it as a replacement for controlled evidence. |
| Local paid-model I3M | DeepSeek/API model-parsed local I3 representation for all 2433 frozen-v0.4 skills. | Feasibility/pass attempt showing I3 fields are recoverable with a paid provider parser. | `skill_benchmark/representations/I3M_model_parsed.jsonl`, `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.md` | It provides extraction-quality evidence and helped debug the schema. | Not thesis-facing I3C. Do not relabel as ChatGPT/Codex extraction, and do not use as a headline result unless the paid-provider route is explicitly accepted. |
| External I3C V2 | ChatGPT/Codex-subagent parsed I3 fields for SkillRouter-Eval-Core using evidence validation and no external provider extraction API. | Primary external extracted-field artifact. | Full-all: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`; top-20 pool: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl` | It is the practical non-paid-provider extraction route and has strict evidence-substring QA. | This exists for the external benchmark, not yet for the local frozen-v0.4 benchmark. Local I3C reruns cannot be claimed until local I3C is produced. |
| External I2 full body | Full SkillRouter-Eval-Core skill body, usually serialized as `name`, `description`, and `body`. | Full-document comparator for external I1/I3C results. | `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl` and tier-specific derived files | Needed to compare compressed/extracted information against full-document retrieval. | Neural full-context I2 is only partially recovered locally: Easy/I2 embedding completed; Easy/I2 rerank and Hard/I2 are not complete in local artifacts. |

### Information-Layer Provenance

| Layer | Meaning | Current local status | Current external SkillRouter status | Use in thesis |
|---|---|---|---|---|
| I0 | Progressive disclosure: main agent sees compact cards and may load full skill docs. | Historical 67-prompt/67-skill core only. | Not run. | Baseline/context discussion only unless rerun. |
| I1 / R1 | Flat card: name, short description, family/tags. | Current frozen-v0.4 I1 rows exist for local, Qwen, SkillRouter, M6 diagnostics. | Current I1 FTS/BM25 and neural rows exist, except some failed/cancelled neural variants are partial. | Baseline information layer. |
| I2 / RFULL | Full source skill artifact. | Current local loader now uses controlled top-level skills and public-imported originals. Local crossed lexical rows, local offline rows, and Qwen provider rows have been refreshed after this correction; SkillRouter local full rows generated before the correction are historical until rerun. | FTS/BM25 I2 exists. Neural I2 full-context is incomplete except Easy embedding recovered. | Full-information comparator and cost upper bound, not automatically the best representation. |
| I3H / R2-R3 | Heuristic/section-exported structured fields. | Current frozen-v0.4 local I3 condition. | Older external heuristic I3 condition exists but is superseded by I3C for thesis-facing extracted-field claims. | Valid local structured-field condition if labelled heuristic. |
| I3M | Paid-provider model-parsed I3. | Complete local feasibility artifact with high evidence match. | External rows 0-2999 extraction-quality pilot only; scored gold rows are outside this slice. | Supporting feasibility/pass attempt only. |
| I3C | ChatGPT/Codex-subagent parsed I3. | Not yet produced for local frozen-v0.4. | Complete and cleaned for SkillRouter full-all and top-20 pool; FTS/BM25 and I3C neural rows exist. | Thesis-facing practical extraction route, but local I3C remains pending. |
| I4 | Relation-aware information: alternatives, dependency, composition, hierarchy edges. | `R4_graph_edges.jsonl` exists as an exported edge artifact, but no evaluated graph/relation retrieval experiment is complete. | Planned only. | Future work unless implemented as explicit relation/graph experiment. |
| I5 | Hierarchy/grouping information: category tree, broad-to-atomic routing. | Planned only. | Planned only. | Future work unless implemented as tree/DAG routing experiment. |

### Experiment Families And Current Use

| Experiment family | What it tests | Current state | Which result should be trusted | Why we use it | What not to claim |
|---|---|---|---|---|---|
| Frozen-v0.4 crossed I1/I2/I3 matrix | Whether complete information-layer/strategy conditions change retrieval under fixed method families. | Current on 245 controlled, 144 public-gold, 2433 skills. | `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md` and `.json` | Central RQ2 evidence because method, stratum, budget, and layer are cross-tabulated. Partial RQ1 evidence only where fields are ablated. | Do not compare rows with different candidate budgets as direct wins. Do not treat this matrix alone as the final answer to which individual field matters. |
| Local lexical controls | BM25/TF-IDF over I1, I2, I3. | Current frozen-v0.4. | Crossed lexical rows in the matrix. | Cleanest test of information-layer content because retriever is fixed. | Do not present BM25/TF-IDF as the proposed final architecture. |
| Qwen provider rows | Generic strong embedding and learned reranker over I1/I2/I3. | Current frozen-v0.4. | Frozen-v0.4 Qwen rows in matrix. | Tests whether information-layer effects survive a modern provider embedding/reranker. | Provider choice is not the contribution. Provider API cost must be labelled. |
| SkillRouter frozen-v0.4 rows | Skill-specific embedding and reranker over local benchmark I1/I2/I3. | Current frozen-v0.4, recovered from hosted GPU jobs. | Frozen-v0.4 SkillRouter rows in matrix and recovered summaries. | Tests against a domain-specific skill retrieval model. | Do not mix local smoke tests with hosted full-matrix results. |
| M6-v1 local field-aware diagnostic | Deterministic field-aware reranking over first-stage candidates. | Current frozen-v0.4, but diagnostic. | Frozen-v0.4 M6-v1 rows, labelled diagnostic. | Shows whether explicit fields contain usable reranking signal. | Do not claim it is robust semantic understanding; it is lexical/prototype-like. |
| M6-v2 semantic field diagnostic | No-rewrite semantic field matching with fixed/tuned policies. | Current frozen-v0.4, calibration-sensitive. | Fixed task-heavy policy rows for thesis-facing diagnostic; tuned rows only as diagnostics. | Tests selective field use without generating hidden requirements. | Do not claim all fields help. Many rows prefer task-only or first-stage-heavy scoring. |
| SkillRouter-Eval-Core FTS/BM25 | External I1/I2/I3/I3C lexical portability test. | Complete for I3C V2 full-all. | `skillrouter_eval_core_fts_information_layers_i3c_v2.md/json` | External portability and cost evidence that structured operational fields can preserve useful retrieval signal at much lower token volume. | Do not merge with local benchmark. It has different prompts, multi-gold tasks, and cleaner public documentation. Do not use it alone to rank which individual field matters for RQ1. |
| SkillRouter-Eval-Core neural I3C | External SkillRouter embedding and reranker over I3C full context. | Complete for I3C full-context shared embedding; results recovered from logs. | `skillrouter_eval_core_skillrouter_neural_i3c_fullcontext_shared_2026_06_21_recovered_summary.md/json` | Tests I3C under SkillRouter's own embedding/reranker, using model-limit context and chunking instead of 4096 caps. | Do not compare against incomplete I2 neural as if the matrix is finished. |
| SkillRouter-Eval-Core neural I2 | External SkillRouter full-body comparator under neural model. | Incomplete in local artifacts. Easy/I2 embedding recovered; rerank and Hard not complete. | `skillrouter_eval_core_skillrouter_neural_i2_fullcontext_retry_2026_06_22_recovered_summary.md/json` only for Easy embedding. | Needed eventually for a full neural I2 vs I3C cost/accuracy comparison. | Do not claim full neural I2 matrix results. The recovered Easy row is useful but partial. |
| M0 progressive disclosure | Main-agent card selection and full-doc loading behavior. | Historical/core only. | `skill_benchmark/outputs/m0_progressive_disclosure_core_report.md` | Useful baseline for context/cost discussion. | Not current on 2433-skill scale. |
| Downstream task validation | Whether better candidate selection improves final task outputs. | Planned only. | `skill_benchmark/outputs/step8_downstream_validation_plan.md` | Needed for final agent-reliability claims. | Do not claim downstream task-success evidence yet. |

### Known Deviations And Guardrails

| Deviation / risk | Current status | Why it matters | Required handling |
|---|---|---|---|
| Public-gold full artifact used normalized wrapper text in existing rows. | Fixed in shared local full-text loader and representation exporter on 2026-06-23; crossed lexical, local offline, and Qwen provider matrices refreshed. | It can make public full-body rows test wrapper/import text rather than upstream public skill text. | Treat pre-correction SkillRouter `full` / `RFULL` rows as historical until rerun from `source/SKILL.original.md`. |
| Local I3C does not exist yet. | Not produced. | The local headline should not pretend DeepSeek I3M or heuristic R2 is ChatGPT/Codex I3C. | Say local structured-field results are I3H/R2 unless and until local I3C is extracted and rerun. |
| I3M is paid-provider extraction. | Complete but not chosen as practical route. | It may be good, but it has different cost/provenance from I3C. | Label it as DeepSeek/API feasibility/pass attempt. |
| External I3H was broad and heuristic. | Superseded for primary external field claims. | Early I3H underperformed I2 and used broad heuristic fields. | Use cleaned I3C V2 for thesis-facing external extracted-field claims; keep I3H as archival/debug. |
| External SkillRouter neural jobs had several failed/cancelled attempts. | Multiple recovered/cancelled jobs are recorded. | Failed uploads, token expiry, and quiet progress can create duplicate or invalid rows. | Only report rows from recovered summary files or checkpoints. Never infer missing rows. |
| 4096-token external full-context runs are invalid for full-context claims. | Cancelled/diagnostic. | User wanted full body at model limit, not artificially capped 4096. | Use 32768 embedder and 40960 reranker limits with chunking/aggregation for overlength docs. |
| External neural I2 full-context matrix incomplete. | Easy/I2 embedding only recovered locally. | I3C neural can look worse/better without a complete I2 comparator. | Mark I2 neural as pending/incomplete; do not use it as final I2-vs-I3C neural comparison. |
| Embedding caches were not always persisted. | I2 retry lost document embeddings after OAuth expiry. | Long full-body runs can waste money if not resumable. | Future hosted jobs must upload shards/checkpoints as they run and use stable HF credentials. |
| SkillRouter-Eval-Core is cue-rich. | Corpus audit complete. | External prompts average about 198 rough tokens and often contain input/output/file cues. | Use it as portability/scale evidence, not as proof the local hard cases are solved. |
| Controlled benchmark explicitly exposes information fields. | Intentional but limited. | It could look like "cheating" if claimed as natural public-skill evidence. | Explain controlled = causal test; public-gold/external = external validity. |
| Public skills already contain many headings. | Verified by corpus/public audit. | Full-body baselines can be strong because full bodies are clean documentation, not chaotic raw text. | Explain full-body strength as a corpus property and cost trade-off. |
| Top-20 and top-100 budgets are mixed in historical notes. | Historical rows retained. | Larger candidate budgets can inflate reranker performance. | Compare top-20 to top-20; report top-50/top-100 as cost/recall trade-offs. |
| Strict and acceptable labels differ on public-gold. | Acceptable alternatives exist. | Strict-only can punish genuinely equivalent public skills. | Always report strict and acceptable for public-gold when available. |
| M6-v2 tuning can overfit. | Full-set tuned rows exist. | Full-set best weights are not final evidence. | Use fixed global policy or dev/test-selected weights for thesis claims. |
| Graph/tree retrieval methods are not done. | R4 edge export exists, but evaluated I4 graph/relation retrieval and I5 tree routing are not complete. | The thesis should not imply relation/hierarchy experiments exist. | Discuss as future work unless implemented and evaluated. |
| Downstream validation not run. | Planned only. | Offline retrieval does not prove final agent output quality. | Keep final claims to candidate selection unless Step 9 is executed. |

### Current Claim Boundaries

Safe current claims:

- The local controlled benchmark provides the clearest evidence that exposing structured procedural information can improve retrieval under fixed retrievers and rerankers.
- Public-gold results are mixed but useful: structured fields often improve candidate recall, while public names/descriptions and provider cues sometimes dominate top-1 ordering.
- Full skill text is an important comparator but not a free win. It increases selector-visible text, can add noise, and has different fixed indexing versus per-query retrieval costs.
- External SkillRouter-Eval-Core I3C V2 gives portability evidence: under FTS/BM25, I3C improves over I1 and is competitive with or better than I2 on several Easy/Hard metrics while using about one tenth of the I2 token volume.
- M6-v1 and M6-v2 are field-use diagnostics. They show that fields can help, but also that selective activation and reranker calibration are necessary.

Unsafe current claims:

- Do not say local I3C results exist.
- Do not say graph/tree experiments have been run.
- Do not say downstream task success is demonstrated.
- Do not say pre-correction public-gold full-body provider/SkillRouter rows are final until they are rerun with public originals.
- Do not say the external neural I2 vs I3C matrix is complete.
- Do not say "I3 always beats full documents"; the actual result depends on corpus, retriever, reranker, and metric.

### Atomic Script And Pipeline Audit

This subsection records the actual operational pipeline at script level. It exists to prevent a future rerun from silently changing source files, information layers, retrievers, candidate budgets, or execution venue.

#### Atomic Source Flow

| Step | Artifact or script | Actual behavior | Expected for thesis? | Current caveat |
|---|---|---|---|---|
| Public import | `skill_benchmark/scripts/import_public_background_skills.py` | Discovers/uses public skill URLs, downloads each upstream `SKILL.md` into `source/SKILL.original.md`, writes `source/IMPORT.json`, and writes a normalized local top-level wrapper at `SKILL.md`. It deletes and recreates `skill_benchmark/skills/public_imported_background` when run. | Yes for corpus import and provenance, but not for final public full-body evaluation. | Because it rewrites the whole public import tree, rerun only when intentionally creating a new benchmark/corpus version. |
| Public wrapper | `skill_benchmark/skills/public_imported_background/<skill>/SKILL.md` | Contains normalized benchmark metadata, dependency profile, use/not-for text, and source links. | Yes for stable local IDs and provenance. | Not the canonical full public document for I2/RFULL. |
| Public original | `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md` | Stores the upstream public skill text when download succeeds. | Yes. This is the intended source for final public full-body/I2 comparisons. | The shared local full-text loader and representation exporter now prefer this path; pre-correction result files remain historical. |
| Controlled skills | `skill_benchmark/skills/<family>/<skill>/SKILL.md` | Hand-authored or generated controlled skill artifacts with explicit routing, input, output, workflow, dependency, boundary, and success signals. | Yes. This is the controlled causal test stratum. | It intentionally exposes proposed fields; claims must say this is a controlled causal setting, not natural public validity by itself. |
| Prompt labels | `skill_benchmark/prompts/*.json`, `skill_benchmark/prompts_public_gold/*.json`, low-info prompt files, acceptable-alternative JSON | Store prompt text, gold skill, closest alternatives, and acceptable alternatives. | Yes. These define the local evaluation strata. | Controlled/public/low-info must be reported separately. |
| External SkillRouter raw | `skill_benchmark/external/skillrouter_eval_core/raw` | Contains SkillRouter-Eval-Core raw Easy/Hard skill rows and tasks/relevance files. | Yes for external validation. | It is a different dataset with multi-skill tasks and cue-rich prompts. |
| External I2 | `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl` and tier subsets | Serializes external full skill body as metadata plus raw body text from SkillRouter rows. | Yes for external full-body comparator. | Neural I2 full-context matrix is still incomplete locally. |
| External I3C | `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl` | Cleaned Codex-subagent I3C V2 extraction over all external Hard-tier skills, with exact evidence validation. | Yes for thesis-facing external extracted-field condition. | Exists externally only; local frozen-v0.4 I3C is pending. |

#### Local Representation Export Scripts

| Script | Reads | Writes | What it actually does | Expected? | Caveat / required handling |
|---|---|---|---|---|---|
| `export_skill_representations.py` | Local `skill_benchmark/skills/**/SKILL.md`; for public imports, also reads `source/SKILL.original.md` when present. | `R1_flat_metadata.jsonl`, `R2_structured_procedural.jsonl`, `R3_dependency_resource_aware.jsonl`, `R4_graph_edges.jsonl`, representation manifest. | Builds R1 from stable skill id plus description. For public imports, the description and R2/R3 structured text now come from `source/SKILL.original.md` when present, while the wrapper id is preserved for label compatibility. Exports R4 edge rows from extracted fields/resources/public-source signals. | Yes for local I1/I3H/R3 export. | R4 is only an exported edge artifact, not evidence that I4 graph retrieval ran. |
| `validate_benchmark_integrity.py` | Prompt JSON files, local skills, public import manifest. | Integrity markdown/json report. | Checks duplicate prompt IDs, malformed skills, missing frontmatter, name/directory mismatch, unresolved gold skills, unresolved alternatives, and public import status counts. | Yes. | It validates references and corpus shape, not semantic gold-label quality. |
| `build_frozen_v0_4_information_matrix.py` | Existing result JSON files under `skill_benchmark/outputs`. | `frozen_v0_4_information_layer_matrix.md/json`. | Aggregates local BM25/TF-IDF, Qwen, SkillRouter, M6-v1, and M6-v2 result artifacts; adds candidate recall, bootstrap intervals, and paired McNemar tests where per-prompt rows exist. | Yes for current matrix reporting. | It does not rerun experiments; if an upstream row predates the public-original correction, the matrix faithfully reports that historical artifact and must be caveated. |
| `run_crossed_lexical_representations.py` | R1/R2/R3 plus full texts via shared full-text loader. | Crossed lexical matrix JSON/MD. | Runs BM25/TF-IDF over I1/R1, I3H/R2/R3, and full text for controlled/public-gold strata. | Yes for lexical controls after source policy is correct. | Refreshed on 2026-06-23 after the public-original loader/exporter correction and public-style controlled regeneration. |

#### Local Selector Scripts

| Script | Reads | Writes | What it actually does | Expected? | Caveat / required handling |
|---|---|---|---|---|---|
| `run_offline_selectors.py` | Prompt files, R1/R2/R3, local skills through `load_full_skill_texts`. | `offline_selector_evaluation.md/json` or configured outputs. | Runs deterministic BM25, TF-IDF, MiniLM, and local schema rerank baselines; evaluates strict/acceptable top-1, top-5, MRR, non-main/public false positives, and token totals. | Yes for local lexical/offline baselines. | `load_full_skill_texts()` now uses `full_skill_source_path()` so public imports prefer `source/SKILL.original.md`; pre-correction outputs remain historical. |
| `run_provider_selectors.py` | Prompt files, R1/R2/R3, full texts from `run_offline_selectors.load_full_skill_texts`, provider credentials from `.env`. | Provider result JSON/MD. | Runs OpenAI-compatible/Qwen embeddings, optional Qwen reranker over top-20 candidates, and optional local-schema reranker. Caches embeddings/rerank scores under `skill_benchmark/runtime/provider_cache`. | Yes for Qwen/provider comparison. | New full rows inherit the corrected public-original full-text loader. Provider cost and API provenance must be labelled; pre-correction provider outputs remain historical. |
| `run_skillrouter_selectors.py` | Prompt files, R1/R2, full texts from `load_full_skill_texts`, SkillRouter HF models. | SkillRouter selector JSON/MD. | Runs `pipizhao/SkillRouter-Embedding-0.6B`; optional `pipizhao/SkillRouter-Reranker-0.6B` reranks top-20 by default. Supports prompt-subset smoke tests. | Yes for smoke tests and hosted/local result generation when command/venue is recorded. | New full rows inherit the corrected public-original full-text loader. Script defaults are 2048 token limits; full hosted matrix rows must explicitly record actual max-length overrides. Pre-correction SkillRouter outputs remain historical. |
| `run_m6v1_field_aware_reranker.py` | First-stage result rows plus R1/R2/R3. | M6-v1 diagnostic rerank JSON/MD. | Reranks first-stage candidates with deterministic field-aware lexical matching. | Diagnostic yes. | Do not claim this is a learned or robust semantic reranker. Candidate budget must be reported. |
| `run_m6v2_semantic_field_reranker.py` and `sweep_m6v2_*` | First-stage rows, R1/R2/R3, provider embeddings/cache. | M6-v2 semantic diagnostic outputs. | Extracts request-side field text, embeds active fields and candidate field chunks, aggregates field similarities, and evaluates fixed/tuned policies. | Diagnostic yes. | Tuned rows can overfit. Thesis-facing use should be fixed global policy or clearly marked diagnostic. |

#### Local Extraction Scripts

| Script | Reads | Writes | What it actually does | Expected? | Caveat / required handling |
|---|---|---|---|---|---|
| `model_parse_i3m_skills.py` | Local skills or an external JSONL via `--input-jsonl`; `.env` provider key; R1 metadata. | Raw model parse JSONL, representation JSONL, report MD. | Calls an OpenAI-compatible chat provider, defaulting to DeepSeek env/model settings, to extract seven I3 fields with exact evidence quotes. Supports `--offset`, `--limit`, `--retry-failed`, caching, concurrency, and external row parsing. | Yes as a paid-provider feasibility/pass attempt. | This is I3M, not I3C. Do not use it as the practical Codex/ChatGPT extraction result unless the thesis explicitly accepts paid-provider extraction. |
| `I3 Model Extraction Protocol.md` | Methodology document, not executable. | Protocol text. | Defines the schema and evidence-grounding standard for model extraction. | Yes. | It is a protocol; actual compliance must be checked in output QA reports. |
| `prepare_skillrouter_i3c_full_extraction.py` | External `all_I2.jsonl` plus cleaned top-20 seed I3C rows. | I3C full-all manifest, input chunks, seed-cache JSONL. | Creates missing-row chunks with `source_row_index`, writes exact output paths, seeds already-QA-passed top-20 rows, and records prompt path `I3C_SUBAGENT_EXTRACTION_V2.md`. | Yes for external I3C V2 full-all extraction preparation. | It prepares work only; it does not itself parse chunks. |
| `I3C_SUBAGENT_EXTRACTION_V2.md` | Prompt read by subagents. | No direct output. | Requires one JSON object per input row, exact evidence substrings, sparse/missing-field QA metadata, and no external APIs. | Yes. | Every worker must be given only its assigned input artifact text. |
| `merge_i3c_subagent_chunks.py` | Subagent chunk outputs and matching input chunks. | Merged normalized I3C JSONL and summary JSON. | Normalizes rows, preserves skill identity, records absent fields/warnings, counts parse failures and field coverage. | Partly yes. | The base merge script normalizes and counts but does not by itself enforce every stricter V2 QA rule; final cleaning/check scripts and manual evidence-substring checks complete the QA chain. |

#### Public Field-Richness Audit Scripts

| Script | Reads | Writes | What it actually does | Expected? | Caveat / required handling |
|---|---|---|---|---|---|
| `audit_public_skill_fields.py` | `public_imported_background` skill dirs; prefers `source/SKILL.original.md` over wrapper when present. | `public_skill_field_audit.jsonl`, summary JSON, MD report. | Heuristically detects routing/input/output/workflow/boundary/dependency/resource/example/safety/environment/hierarchy evidence using frontmatter, headings, and keywords. | Yes for corpus characterization. | This is a heuristic field-presence audit, not retrieval evidence. |
| `audit_rq1_public_field_realism.py` | The 460 imported upstream public files at `public_imported_background/<skill>/source/SKILL.original.md`. | `rq1_public_field_realism_audit.md/json` and `rq1_public_field_realism_audit_rows.jsonl`. | Focused RQ1b audit for the same seven fields used in RQ1a: use condition, input/precondition, output/artifact, workflow/procedure, boundary/not-for, dependency/resource, and success/verification. Classifies each as explicit, implicit, missing, and flags noisy/mixed dependency, boundary, and success evidence. | Yes for the current RQ1b public-realism checkpoint. | It is a heuristic recoverability audit, not a selector run. It should be paired with RQ1a field-isolation results rather than reported as routing accuracy. |
| `model_verify_public_skill_fields.py` | Heuristic audit rows and each row's `audit_file`. | `public_skill_field_model_audit.jsonl`. | Samples/verifies field evidence with a provider model, requiring evidence quotes to be found in the audited text. | Yes as spot-check support. | Defaults to DeepSeek/provider API and usually a sample limit; label as model-assisted audit, not exhaustive unless run exhaustively. |
| `compare_public_skill_field_audits.py` | Heuristic audit JSONL and model audit JSONL. | Agreement JSON/MD. | Compares heuristic-present versus model-present statuses, evidence found, confidence, and disagreements. | Yes for audit reliability discussion. | It compares audits; it does not change benchmark labels or selector results. |

#### External SkillRouter-Eval-Core Scripts

| Script | Reads | Writes | What it actually does | Expected? | Caveat / required handling |
|---|---|---|---|---|---|
| `prepare_skillrouter_eval_core.py` | Raw external Easy/Hard `.jsonl.gz`, `tasks.jsonl`, `relevance.json`. | Derived tasks, `hard_only_skill_ids.txt`, I1/I2/I3H all/tier JSONL, manifest, README. | Converts the external benchmark into local derived layers. I1 is metadata. I2 is full external row body. I3H is heuristic structured fields using local export logic. | Yes for external baseline preparation. | I3H is heuristic and superseded by I3C for thesis-facing external extracted-field claims. |
| `build_i3c_v2_fts_representations.py` | Cleaned full-all I3C plus external tier I2 files. | `easy_I3C.jsonl`, `hard_I3C.jsonl`, summary JSON. | Serializes cleaned I3C fields as `name`, `description`, and labelled field bullets; records absent fields, parse flags, warning counts, field counts, and token totals. | Yes for external I3C FTS/BM25. | If an I3C row is missing, it emits a fallback name/description row and marks parse failure; current full-all cleaned artifact has complete coverage. |
| `run_skillrouter_eval_core_fts_ablation.py` | External derived representations and relevance/task files. | External FTS/BM25 result JSON/MD plus SQLite FTS indexes. | Builds disk-backed SQLite FTS5 BM25 indexes per tier/layer; queries scored tasks; reports Hit@1, MRR@10, nDCG@10, Recall@k, FullCov@k, hard-only top1, tokens, and query/index time. | Yes for external lexical portability. | Different metric regime from local single-gold benchmark. Recall/FullCov matter more here because tasks may have multiple gold skills. |
| `run_skillrouter_eval_core_skillrouter_matrix.py` | External raw rows for I1/FULL/I2 when available; derived I3C for I3C; tasks/relevance. | External neural result JSON/MD, per-condition progress JSON, optional HF uploaded artifacts, optional doc-embedding shard cache. | Runs SkillRouter embedding-only retrieval and SkillRouter embedding plus reranker. FULL/I2 text is `name | description | body` from raw rows. I3C text is `name | description | cleaned I3C fields`. Reranker uses top-20 candidates by default. | Yes for external neural matrix when run on HF/hosted GPU with model-limit context. | Script default max lengths are 4096 unless overridden. Valid full-context runs must record 32768 embedder and 40960 reranker limits, checkpoint shards, and recovered rows. |
| `hf_skillrouter_eval_core_i2_checkpointed_job.py` | External raw/derived files and HF credentials. | HF checkpoint dataset artifacts, doc-embedding shards, result/progress files. | Job wrapper for checkpointed I2 full-context run. Downloads prior matching artifacts, validates shard metadata, uploads document embedding shards/manifests during the run, and resumes from cache if hashes/skill IDs/model/max length match. | Yes for future I2 full-context completion. | The local tracker should not report results from this until final compact summary or recovered artifacts exist locally. |

#### Result And Cost Accounting Rules

| Rule | What to record every time | Why |
|---|---|---|
| Representation source | Whether the run used controlled top-level `SKILL.md`, public `source/SKILL.original.md`, public wrapper `SKILL.md`, external raw row `body`, or cleaned I3C fields. | Prevents wrapper/original/full-body drift. |
| Information layer | I1, I2/RFULL, I3H/R2/R3, I3M, I3C, I4, or I5. | Prevents relabelling heuristic/paid-provider/Codex fields. |
| Retriever and reranker | BM25, TF-IDF, MiniLM, Qwen embedding, Qwen rerank, SkillRouter embedding, SkillRouter rerank, M6-v1, M6-v2. | Prevents comparing information-layer and method changes as one effect. |
| Candidate budget | Top-20, top-50, top-100, or all. | Reranker results are conditional on candidate availability. |
| Execution venue | Local laptop, local smoke test, Hugging Face Job, recovered logs, uploaded artifacts. | Prevents treating tiny smoke tests or failed HF jobs as full results. |
| Context limits | Embedding max length, reranker max length, chunking/aggregation policy. | 4096-token runs are not full-context external full-body claims. |
| Token/cost split | Selector-visible document tokens, one-time/fixed document embedding cost, per-query embedding/retrieval/rerank time, agent-visible loaded skill tokens if measured. | The thesis trade-off is fixed preprocessing/indexing cost versus repeated query-time selection and context cost. |
| Result provenance | Exact output JSON/MD path, recovered log checkpoint, job ID, and whether row is complete/partial/failed. | Prevents duplicate failed/cancelled jobs from contaminating the result matrix. |

#### Current Script-Level Deviations To Fix Before New Claims

| Deviation | Affected scripts/artifacts | Fix before claiming |
|---|---|---|
| Pre-correction public full-body provider/SkillRouter rows may use wrappers. | Historical provider/SkillRouter public `full`/`RFULL` outputs. | The shared loader/exporter and crossed lexical rows are fixed. Rerun paid/provider and SkillRouter rows only after the corpus/source policy is intentionally frozen. |
| Local I3C absent. | Local frozen-v0.4 extraction/results. | Produce Codex/ChatGPT-style local I3C with exact-evidence QA, then rerun I3C conditions if thesis needs local I3C rather than I3H/I3M. |
| External I2 neural full-context incomplete. | I2 HF jobs and recovered summaries. | Resume/run checkpointed I2 full-context with persisted doc embeddings and recover final compact summary before comparing neural I2 vs I3C. |
| R4 graph artifact exists without graph retrieval. | `R4_graph_edges.jsonl`, any I4 language. | Either implement/evaluate graph/relation retrieval or keep I4/I5 as future work. |
| Model-assisted public audit is provider/API based. | `model_verify_public_skill_fields.py`. | Label it as sampled provider verification; do not confuse it with no-external-API I3C extraction. |

## Core Thesis Framing

The thesis is about skill retrieval as a candidate-subsetting component before the main agent loads full skill artifacts.

Current research position:

> This thesis investigates which operational information helps distinguish semantically similar but procedurally different skills, and how different representation and retrieval strategies preserve, organize, or exploit routing-relevant information at scale.

Current research questions:

**RQ1:** Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

**RQ2:** How do skill representation and retrieval-pipeline choices affect the preservation and use of the routing-relevant operational information identified in RQ1 under semantic confusability, and what accuracy, candidate-recall, and retrieval-cost trade-offs result?

Current RQ1 evidence programme:

- **Controlled field isolation:** 350 three-sibling clusters and 750 prompt variants across seven fields. Shared candidate context is held fixed; only one candidate-specific field is exposed. Every field has a positive cluster-bootstrap Top-1 lift under BM25 and Qwen. This establishes controlled sufficiency, not public prevalence or universal necessity.
- **Examples/tests negative control:** 50 separate clusters show that generic examples do not establish a distinct routing capability, while rare near-exact request/example matches can attract a selector. This is support information, not an eighth operational field.
- **Public original-document removal:** 82 source compositions and 265 originals yield 1,078 clean composition-family cases. Removing cited use-condition and success/verification lines lowers strict Hit@1 under both retrievers; other single fields are retriever-conditional and boundary/not-for is not stably positive. Joint task-specification and execution/verification removal is stable under both retrievers.
- **Supporting history only:** the 460-file recoverability audit, 62-cluster unexecuted natural-original wave, and 46-composition derivative field-card ablation remain preserved but are not the current second experiment.
- **Human review:** the old 350-row record is retrospective author confirmation. A prospective unblinded confirmation workflow covers 350 controlled clusters, 194 scored public gold families, and 402 scored public transformations. Frozen gold is visible in the first two streams. Live counts are maintained in the workspace `STATUS.md`, with exact decisions in packet receipts. No blinded, independent-human, or inter-rater claim is supported.
- No RQ1c is currently defined. RQ2a and RQ2b remain separate representation/retrieval studies and do not redefine the RQ1 result.

Earlier assignment wording, now developed:

**Previous RQ1:** How can agent skills be represented and retrieved so that agents can accurately select among semantically similar but procedurally distinct skills as skill libraries scale?

**Previous RQ2:** To what extent do structure-aware skill representations improve retrieval accuracy, context efficiency, and downstream task performance compared with flat description-based skill retrieval?

The previous questions are not wrong, but the current version is sharper. The old RQ2 framed the thesis as testing whether structure-aware representation improves performance. The current framing first uses RQ2a to isolate representation and explicit-use mechanisms under matched facts, then leaves practical full-library retrieval as the separately reviewed RQ2b stage.

Current evidence priority:

- Treat field-isolation and prompt-type/cluster-specific analysis as the main RQ1 evidence.
- Use the RQ1 test unit as the atomic design object: fixed explicit prompt, near-neighbour skill pair/cluster, shared neutral skill context, target skill-side field value, exact evidence, and fixed retriever/metric.
- Report I1, I2, and I3 as rough information conditions: I1 carries minimal metadata, I2 carries the full source artifact, and I3 carries the proposed operational information fields.
- Mark graph/tree/DAG information assumptions as TBD until their edge schemas, branch schemas, leakage controls, and intended retrieval role are specified.
- Do not claim graph/tree methods use the same information as I3 unless the experiment explicitly serializes or maps the same fields into relation or hierarchy form.
- Use the completed seven-field RQ1a suites as the direct evidence for which operational fields discriminate near-neighbour skills.

Historical correction, 2026-06-23:

- The existing I1/I3/I2 representation matrix is now historical exploratory RQ2-adjacent evidence because it changes content, structure, and sometimes retrieval conditions together.
- The existing global field ablation is useful RQ1 evidence, but it is not yet the cleanest RQ1 test because prompts are not all labelled by the single field that should resolve the confusion.
- This requirement is now satisfied by the seven RQ1a field-isolation suites. Use those suites, not the older global field-ablation table, for strong field-specific claims such as "input/precondition is stronger than success/verification as a first-pass routing signal."

RQ1 field-targeted test condition:

1. Use semantically similar skills from the same cluster or domain.
2. Hold the skill library, prompt, retriever, candidate budget, and scoring metric fixed.
3. Keep the prompt explicit enough for a stable gold label; do not make prompts vague to avoid leakage.
4. Vary only the skill-side operational information visible to the selector, such as controlled baseline description versus baseline plus output field.
5. The controlled baseline description should preserve shared cluster/task context while masking the `primary_distinguishing_field`.
6. The shared context may name broad task families such as PDF extraction, dataset quality, API work, browser evaluation, experiment execution, or compliance review; it must not name target values such as scanned/native, JSON/prose, validate/repair, legal-advice/no-legal-advice, HF Jobs/local, or visual-evidence/data-scrape.
7. Mark original descriptions that already expose the tested field as realistic but leaky for causal RQ1.
8. Label each prompt with a `primary_distinguishing_field` and optional `secondary_distinguishing_fields`.
9. Count a field as helpful only when adding that field improves top-1/MRR or reduces hard-negative sibling errors on prompts where that field is the labelled distinction.

Canonical RQ1a comparison, added 2026-06-24:

- Hidden field = `shared_context_only`: shared non-target skill context with the tested field omitted.
- Exposed field = `shared_context_plus_field`: the same shared context plus exactly one target field line.
- This hidden-versus-exposed contrast is the thesis-facing field-isolation result for every field suite.
- `field_only` and `full_skill_doc` are diagnostics only. `full_skill_doc` should not be treated as the main exposed-field condition because it adds whole-document noise, names, headings, and extra selector-visible cost.

Status update, 2026-07-17: the seven current RQ1a field suites have been authored, rubric-checked, run, and written into the result notes/thesis draft. Use condition is strong but wording-sensitive. Input/precondition is the cleanest strong signal. Output/artifact is strong under semantic retrieval but more lexical-sensitive under paraphrase. Dependency/resource is strong when defined as external capability compatibility and when the request or routing context carries the relevant platform/tool/API/runtime/version/resource cue. Boundary/not-for is useful but conditional, especially under implicit authority. Success/verification is positive but weaker because acceptance gates are often semantically close and paraphrase-sensitive. Workflow/procedure is positive but heterogeneous because order, missing step, changed operation, and completely different procedure contrasts vary in difficulty. Examples/tests are complete as a negative-control/support suite, not as a core operational field.

Candidate RQ1 fields to test:

| Field | Clean test case pattern | Expected evidence |
|---|---|---|
| use condition / task trigger | Two skills share domain and output, but one is for review and the other is for planning. | Adding use-condition text should reduce wrong sibling choices. |
| input / precondition | Skills share task words, but require different input state such as native PDF versus scanned PDF, OpenAPI spec versus webhook event, or repo logs versus source code. | Adding input/precondition text should improve field-labelled prompts. |
| output / artifact | Skills share input and domain, but produce different artifacts such as JSON table, prose summary, risk register, patch, or deployment report. | Adding output text should improve output-labelled prompts. |
| workflow / procedure | Skills share input and output type, but the correct one depends on procedure order or operation type such as extract-then-validate versus validate-then-repair. | Adding workflow/procedure text should improve procedure-labelled prompts. |
| boundary / not-for | Skills are plausible but one should be excluded by a negative condition such as not for OCR, not for legal advice, or not for production deploy. | Boundary-aware scoring should reduce unsafe or broad false positives. |
| dependency / resource | Skills share task words, but one requires a platform/tool/API/runtime/provenance resource such as Hugging Face Jobs, Chrome DevTools, GitHub Actions, AWS Cost Explorer, a database engine, or GPU. | Dependency/resource fields should help when the prompt or routing context carries the required external capability. |
| success / verification | Skills perform similar work, but success is judged by a different criterion such as page-grounded evidence, compile-pass, schema validity, or visual rendering. | Success/verification fields should help when output alone is insufficient. |

Current axis definition:

- Axis 1: information layer, meaning what is selector-visible about each skill.
- Axis 2: retrieval or encoding strategy, meaning how that information is searched, embedded, ranked, traversed, or reranked.
- Graph/tree/embedding/reranker methods should not be treated as the information itself.
- Explicit fields are not claimed as the only possible solution; they are one controllable way to test whether task, input, output, workflow, dependency, boundary, and success information matters. Relation and hierarchy information remain planned strategy/layer directions rather than settled RQ1 fields.

The thesis is not mainly about which commercial provider wins. Provider models are used to test whether the representation findings survive stronger retrievers and rerankers.

## Current Validity Critique

The latest detailed methodology critique is recorded in `thesis_notes/methodology/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`. The earlier critique response remains useful background in `thesis_notes/methodology/Critique Response and Validity Improvement Plan.md`.

The current benchmark risk register is `thesis_notes/current/Benchmark Risk Register and Mitigation Plan - 2026-06-06.md`. Use it when deciding whether to add prompts, import more public skills, create public-style controlled skills, or introduce new method variants.

Main validity risks to actively address:

- the controlled benchmark and schema reranker may be co-adapted;
- information-layer effects and retriever/reranker effects can be conflated if Qwen, SkillRouter, and local rerankers are compared while using different skill artifacts or exposed fields;
- gold labels may be unstable when public/background alternatives are plausible;
- 245 evaluated controlled prompts is enough for a controlled honours study but not for broad universal claims;
- generated background skills provide scale pressure but not full real-world messiness;
- MiniLM semantic-confusability checks are construction evidence, not final semantic authority;
- the public-skill field audit grounds the taxonomy but is not a full gold annotation study;
- downstream task success has not yet been demonstrated;
- the current M6-v1-local matcher is lexical field-aware routing, not robust semantic field understanding;
- the strongest SkillRouter + M6-v1 result uses a top-100 candidate budget, so it must not be compared as a direct reranker-only win over SkillRouter top-20 reranking;
- the crossed I1/I2/I3 information-layer-by-architecture matrix is complete for the audited frozen-v0.4 local, Qwen, SkillRouter, and diagnostic field-aware method families;
- M4/M5 graph/tree, M0 progressive disclosure, cost/latency instrumentation, and downstream validation remain separate unfinished experiment families rather than missing cells in the I1/I2/I3 matrix;
- first-pass bootstrap top-1 confidence intervals and paired McNemar tests exist for fixed-method I1/I3/I2 comparisons, but final thesis-selected MRR/top-k uncertainty and table integration remain to be done.
- prompt information level, provider/tool dependency cues, and boundary negations need to be stratified rather than treated as simple leakage/no-leakage. Provider names are valid evidence when the skill is provider-tailored; the risk is relying on the name without input/output/workflow support.

Current response:

- frame the thesis as controlled evidence about representation information, not a universal benchmark claim;
- treat information layer and retriever/reranker architecture as two experimental factors, and report missing matrix cells rather than hiding them;
- prioritize fair horizontal comparisons: I1/R1, I3/R2, and I2/full skill artifacts tested under the same retrievers/rerankers, prompt strata, scale, and candidate budgets;
- freeze the field taxonomy and method set before further tuning;
- run targeted independent/second-pass adjudication on non-core winners and strongest-method failures;
- perform a manual cluster design audit before adding more controlled or public-gold prompts;
- verify the field taxonomy against additional public skills as a background stress test, without turning them into evaluated gold tasks unless they are manually atomized and annotated;
- add public-style controlled skills to test whether the information-layer extraction pipeline can recover useful fields from messier skill artifacts, not only from neat schema-authored skills;
- run Step 9 downstream validation before final claims about agent reliability.

Historical crossed-design priority (superseded on 2026-07-26):

| Priority | Missing / hardening item | Why it matters |
|---|---|---|
| 1 | Integrate the frozen-v0.4 information-layer matrix into the thesis results chapter. | Superseded: this matrix is now exploratory context, not the new central RQ2 evidence. |
| 2 | Add a candidate-recall companion explanation for the results chapter. | Separates first-stage exclusion from reranker ordering failure. |
| 3 | Report public-gold by source-family and cluster type. | Prevents the public-gold stratum from acting like one undifferentiated bucket. |
| 4 | Add representative failure examples from controlled and public-gold reports. | Turns the numerical result into a clear argument about semantic confusion. |
| 5 | Decide whether extra paired bootstrap tests for MRR/top-k are needed. | First-pass top-1 CIs and McNemar tests exist; final tables may need more. |
| 6 | Add cost/latency/token reporting for top-20, top-50, and top-100 budgets. | Supports the thesis trade-off claim, not only accuracy. |
| 7 | Decide whether M4 tree and M5 graph are final experiments or discussion/future work. | Avoids adding graph/tree as decoration without a distinct information claim. |
| 8 | Audit M6-v2 field activation and M6-v1 request parsing if either is used in the final body. | Field-aware diagnostics should not be overclaimed as robust semantic understanding. |
| 9 | Run M0 and downstream validation only after the final method set and budget are chosen. | Avoids expensive agent runs before offline candidate selection is interpreted. |
| 10 | Harden SkillRouter-Eval-Core external validation after first FTS pass. | Tests whether information-layer claims transfer beyond the local benchmark without replacing the controlled benchmark. |
| 11 | Produce a true local I3C artifact before any local I3C reruns. | I3M is a DeepSeek/API feasibility attempt; thesis-facing local I3C claims need a Codex/ChatGPT-style extraction artifact rather than relabelling I3M. |

## Supervisor Feedback Incorporated

Assignment 3 feedback asked for more concrete empirical details from reviewed papers, clearer benchmark construction, and a more specific experimental setup including gold labels, model settings, prompts, and statistical comparison.

Current response plan:

- `thesis_notes/assignments/Supervisor Feedback Response Plan - A3 to Current Thesis.md`

Methodology impact:

- the literature review needs a concrete empirical-detail table for key papers;
- the benchmark chapter needs a reproducible construction pipeline;
- the methodology chapter needs a final method-configuration table;
- benchmark examples need prompt-level gold rationales, alternative rejection rationales, and field-axis justifications; the evidence map is `thesis_notes/current/Gold Label Evidence Map.md`;
- final result tables need strict versus acceptable labels, candidate budgets, model settings, and statistical uncertainty.

## Information Layers To Compare

- I0 progressive disclosure: main agent sees compact metadata and decides whether to load full skill docs.
- I1 flat skill card: skill name, description, family/tags.
- I2 full skill artifact: whole `SKILL.md` or fuller skill text.
- I3 structured selection fields: task/use condition, inputs, outputs, preconditions, workflow, constraints, dependencies/resources, boundaries, success criteria.
- I4 relation-aware information: similarity, alternatives, dependency, composition, belong-to, workflow/prerequisite edges.
- I5 hierarchy/grouping information: category, subcategory, task family, atomic skill grouping.

I3 extraction provenance:

- `I3H`: heuristic/section-based extraction. This is the current frozen-v0.4 R2/R3 condition and the first SkillRouter-Eval-Core external condition.
- `I3V`: model-assisted field verification/audit. This exists for the 460 imported public skills through DeepSeek-assisted verification.
- `I3M`: paid provider model-parsed I3 retrieval representation. Local full-library extraction completed on 2026-06-18 for all 2433 skills using DeepSeek and `I3_MODEL_EXTRACTION_V1`; external SkillRouter-Eval-Core I3M rows `0-2999` completed on 2026-06-19 as an extraction-quality pilot. Treat this as a pass/feasibility attempt, not the headline thesis route.
- `I3C`: ChatGPT/Codex-subagent parsed I3 retrieval representation. External SkillRouter-Eval-Core rows `3000-5999`, the 3284-row top-20 task-relevant pool, and the full 79,141-row Hard-tier library are complete and cleaned under the V2 prompt. Full-tier external I3C FTS/BM25 retrieval has now been run; local frozen-v0.4 I3C extraction is not yet present.

## Method Families

- M0: progressive disclosure baseline, where the main agent sees visible skill cards and decides which full skill documents to load.
- M1: lexical flat retrieval, such as BM25 or TF-IDF over metadata.
- M2: embedding retrieval over description or full skill text.
- M3: structured/schema-based retrieval.
- M4: tree routing, not implemented yet.
- M5: graph retrieval, not implemented yet.
- M6-v0: local two-stage retrieval plus deterministic schema reranking; keep as a diagnostic method, not the final structure-aware claim.
- M6-v1: proposed field-aware procedural reranker that parses request requirements and compares them against extracted skill fields.
- M7: API embedding retrieval, implemented and executed with Qwen.
- M8: API embedding retrieval plus neural reranking, implemented and executed with Qwen.
- M8b: API embedding retrieval plus local schema reranking, implemented and executed; strong historical/diagnostic hybrid.

## Active 2026-06-23 Snapshot

- Active library: 2433 skills.
- Active main prompts: 245 controlled/evaluated prompts, including implicit-field, public-style controlled, and clear-confusability expansion prompts.
- Public imported skills: 460, all with original `SKILL.md` files downloaded.
- Public field audit: 460/460 public skills audited heuristically and with DeepSeek model-assisted verification.
- Public-gold stratum: 144 cleaned public-gold prompts; this creates 389 total controlled + public-gold evaluation prompts, or 401 broad prompts when the separate 12 low-information stress prompts are included.
- Current method cleanup: local schema rerank is `M6-v0`; `M6-v1-local` field-aware procedural reranking is implemented as a lexical prototype.
- Current main concern: show that extracted selection information helps when it is actually used as structured evidence, while separating field usefulness from extraction quality, candidate budget, length bias, and lexical overlap.
- Step 4b manual cluster audit: first pass complete in `skill_benchmark/outputs/cluster_design_audit.md`; future expansion should follow its expand/revise/freeze decisions.
- Public-style controlled expansion: 32 prose-style skills and 64 prompts added to test whether representation fields can be extracted from less neatly schema-authored artifacts.
- Active frozen-v0.4 selector reruns on 245 controlled / 144 public-gold / 2433 skills are complete for local, Qwen, and SkillRouter I1/R1, I3/R2, and I2/full information-layer conditions.
- Consolidated matrix: `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md`.
- Failure-mode companion: `skill_benchmark/outputs/frozen_v0_4_failure_mode_comparison.md`.
- External SkillRouter-Eval-Core validation track added separately under `skill_benchmark/external/skillrouter_eval_core`. The raw public benchmark has 87 tasks, 75 default scored tasks, 78,361 Easy skills, 79,141 Hard skills, and 780 Hard-only distractors. First external FTS/BM25 I1/I2/I3H report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers.md`.
- Local I3M paid-model feasibility layer completed for all 2433 skills. Artifact: `skill_benchmark/representations/I3M_model_parsed.jsonl`. Report: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.md`. Summary: 2333/2433 valid rows (95.9%), 0 parse-failed rows, 54,989 extracted items, 98.7% exact evidence, and 99.7% case-insensitive/whitespace-insensitive evidence. Do not treat this as local I3C.
- External SkillRouter-Eval-Core I3M extraction is complete for rows `0-2999`: 3000 deduplicated latest rows, 0 latest parse-failed rows, and 2997/3000 strict selector-valid rows after documented QA residues. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3M Partial Extraction Checkpoint - 2026-06-19.md`.
- External SkillRouter-Eval-Core I3C extraction is complete for rows `3000-5999` using ChatGPT/Codex subagents and no external provider extraction API: 3000 rows, 0 parse failures, 0 missing skill ids, and 98.66% exact evidence-match after merge repair. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C Subagent Parse Checkpoint - 2026-06-19.md`.
- I3C prompt V2 added at `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`; future subagent extraction should record sparse/generic/missing-field cases in QA metadata rather than forcing them into selector-visible fields.
- I3C V2 pilot on the first 200 rows of the SkillRouter top-20 task-relevant pool is complete: 2 subagents, 100 skills each, 200/200 rows, 0 parse failures, 0 missing skill ids, 100% exact evidence match, and populated QA warnings. Status: pass with minor QA caveats. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Pilot First 200 - 2026-06-19.md`.
- I3C V2 top-20 task-relevant pool extraction is complete and cleaned: 3284/3284 rows, 33 subagent chunks, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, and 25544/25544 exact evidence matches after removing 27 heading-only evidence items. Canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Top20 Pool Extraction Checkpoint - 2026-06-19.md`.
- External SkillRouter full-all I3C V2 extraction is complete and cleaned. Source `all_I2.jsonl` has 79141 skills; 3284 cleaned top-20 rows were seeded; 75857 missing rows were extracted across 759 chunks. Canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`. Clean QA: 79141/79141 rows, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 498836/498836 exact evidence matches, and 0 heading-only evidence after removing 438 generic heading-only items. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Full-All Extraction Completion - 2026-06-20.md`.
- External SkillRouter I3C V2 full-tier retrieval is now complete under SQLite FTS5 BM25. Result report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.md`. Easy I3C reaches 53.3% Hit@1, 0.586 MRR@10, 60.5% Recall@20, and 44.0% FullCoverage@20; Hard I3C reaches 45.3% Hit@1, 0.527 MRR@10, 59.2% Recall@20, and 40.0% FullCoverage@20.
- Corrected external SkillRouter-Eval-Core neural I1/FULL/I3C matrix job `6a3773a1953ed90bfb9469b7` was cancelled to stop Hugging Face GPU spend after it emitted only the Easy/I1 embedding and Easy/I1 rerank rows. No result files were uploaded to the Hub; the two rows are recovered locally from logs. The earlier neural job `6a373487953ed90bfb94663e` is diagnostic only because it used older derived I2 serialization and 2048-token caps. Next neural run should split `I1,I3C` from `FULL`, add progress logs, avoid `--quiet-progress`, and upload after every row. Cancellation checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Corrected Neural Matrix Cancelled Partial - 2026-06-21.md`.
- Remaining corrected neural `I1/I3C` job `6a37bdd33093dba73ce2b559` failed after completing `easy_I3C_embedding` because the Hub token could not commit directly to the dataset repo. Recovered log row: Easy/I3C embedding Hit@1 45.3%, MRR@10 0.525, Recall@20 55.1%, FullCov@20 37.3%. Failure checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Remaining I1 I3C Neural Matrix Upload Failure - 2026-06-21.md`.
- Grouped replacement job `6a37c2b63093dba73ce2b58d` completed on Hugging Face Jobs with quiet progress disabled. Hub uploads still failed with `403`, but all rows were recovered from logs: Easy/I3C embedding 45.3% Hit@1 / 0.525 MRR@10 / 55.1% Recall@20 / 37.3% FullCov@20; Easy/I3C rerank 57.3% / 0.630 / 55.1% / 37.3%; Hard/I1 embedding 44.0% / 0.535 / 57.9% / 40.0%; Hard/I1 rerank 52.0% / 0.581 / 57.9% / 40.0%; Hard/I3C embedding 37.3% / 0.477 / 53.7% / 37.3%; Hard/I3C rerank 48.0% / 0.563 / 53.7% / 37.3%. Launch checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Remaining I1 I3C Grouped Neural Matrix HF Job Launch - 2026-06-21.md`.
- External SkillRouter-Eval-Core I2/full-document neural baseline job `6a37cf7f953ed90bfb946ea4` was cancelled because it used the earlier 4096-token cap. It is invalid as a full-context comparator. The SkillRouter paper defines full inputs as name, description, and body, truncated at each model's input limit; local checks show the external I2 full documents fit under the SkillRouter embedder's 32768-token input limit, so I2 should be rerun later with model-limit context rather than 4096.
- External SkillRouter-Eval-Core I3C full-context neural rerun `6a37d2413093dba73ce2b60b` was cancelled before any condition completed because its condition loop obscured progress and risked avoidable repeated first-stage work. Do not report rows from this job.
- Replacement I3C full-context neural rerun `6a37d3a23093dba73ce2b60e` completed on Hugging Face Jobs with quiet progress disabled. It used the SkillRouter embedder's 32768-token limit and reranker's 40960-token limit, chunked/aggregated overlength serialized I3C documents, and shared the first-stage embedding retrieval per tier between embedding-only and embedding+reranker rows. Recovered rows: Easy/I3C embedding 46.7% Hit@1 / 0.531 MRR@10 / 55.1% Recall@20 / 37.3% FullCov@20; Easy/I3C rerank 57.3% / 0.631 / 55.1% / 37.3%; Hard/I3C embedding 37.3% / 0.477 / 53.7% / 37.3%; Hard/I3C rerank 48.0% / 0.563 / 53.7% / 37.3%. Completion checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C Full Context Shared Neural Matrix Completion - 2026-06-21.md`.
- External SkillRouter task-relevant pools prepared from existing full-library BM25 rankings plus all gold skills: top-20 union + gold has 3284 skills and is parsed as I3C V2; top-50 union + gold has 7113 skills and can now be materialized by filtering the full-all I3C V2 artifact, although no separate cleaned top-50 file exists yet. These pools are suitable for fixed-candidate I3C reranking tests, not full-library first-stage retrieval claims.
- Treat older 201/137/120/82 prompt results as historical unless explicitly used for development comparison.

Operational venue rule:

- Run local CPU/lexical/export/aggregation jobs locally.
- Run Qwen/DeepSeek conditions as local orchestration over provider APIs and label them as provider-cost conditions.
- Run I3C extraction through Codex subagents with evidence validation and no external APIs.
- Run full SkillRouter embedding/reranker matrices on Hugging Face Jobs or an equivalent hosted GPU environment.
- Use local SkillRouter execution only for tiny smoke tests, never as a full matrix result.

## Status Corrections Since Earlier Notes

Some older notes still mention 85 prompts, 137 prompts, 201 prompts, 82 public-gold prompts, 120 public-gold prompts, 2089 skills, 2349 skills, or 2401 skills. Treat those as historical unless explicitly labelled. The active frozen-v0.4 benchmark is 245 controlled prompts, 144 public-gold prompts, 12 low-information stress prompts, and 2433 skills.

Items previously marked done but now requiring redo or hardening:

- Step 7 field ablations: done as useful evidence, but final claims need length-control or field-dropout checks.
- M6-v1: implemented, but only as `M6-v1-local`; it still needs request-parser audit and possibly an M6-v2 semantic field matcher.
- SkillRouter comparison: done for R1/R2/full embedding and rerank on frozen v0.4, but top-20 rerank and any future top-100 hybrid budgets must be reported separately.
- Public-gold validation: expanded into a separate 144-prompt external-validity stratum; residual gold-label hard cases remain tracked; local/provider/SkillRouter selector runs are complete for frozen v0.4.
- Step 6 public field audit: done as heuristic/model-assisted evidence, but final paper-level claims need manual/sample calibration and evidence-span examples.
- Literature review: scaffold exists, but needs concrete empirical details from key papers.
- M0 progressive disclosure: historical only; not current on 245/2433.
- Downstream validation: planned only.

## Completed Work

- Thesis framing clarified: retriever/reranker is separate from the main agent.
- Benchmark library expanded to 2433 skills:
  - 169 controlled/evaluated skills, including 10 implicit-field stress skills and 32 public-style controlled skills.
  - 1800 generated background-scale skills.
  - 460 public imported background skills.
  - 4 support/email skills.
- Prompt set expanded to 245 controlled/evaluated prompts, plus 144 public-gold prompts and 12 low-information stress prompts.
- Controlled-core v2 clusters added:
  - office artifact workflows.
  - deployment/browser QA.
  - API/backend design.
- R1-R4 representations exported. Caveat: `R4_graph_edges.jsonl` exists as a relation artifact, but I4 graph/relation retrieval has not been evaluated.
- Step 1 integrity validation passed.
- Step 2 procedural distinctness and stricter prompt-specific alignment passed after prompt refinements and negation-aware scoring.
- Step 3 semantic confusability passed.
- Step 4 prompt leakage passed.
- Step 5 scale regime passed.
- Step 6 public/real-world skill field audit executed on all 460 imported public skills with heuristic extraction and DeepSeek model-assisted verification; disagreement packet regenerated for taxonomy review.
- Public imported background layer expanded to 460 skills and revalidated as a heuristic/model taxonomy and background stress-test layer.
- Public-style controlled expansion added 8 clusters, 32 skills, and 64 prompts; validation passes integrity, procedural distinctness, semantic confusability, and prompt leakage gates.
- Step 7 local selector/reranker evaluation passed as useful benchmark pressure.
- Step 7 local, Qwen, and SkillRouter selector families rerun on the frozen-v0.4 245-controlled / 144-public-gold / 2433-skill benchmark across I1/R1, I3/R2, and I2/full artifacts.
- External SkillRouter-Eval-Core downloaded and converted into separate I1/I2/I3 artifacts; Hard-only distractors identified as `hard_skill_ids - easy_skill_ids = 780`.
- First external SkillRouter-Eval-Core disk-backed lexical information-layer ablation completed with SQLite FTS5 BM25 over Easy/Hard I1/I2/I3H.
- I3M model-extraction prompt/schema drafted, pilot-gated, and run on the full local 2433-skill library as a paid-model feasibility attempt.
- External SkillRouter-Eval-Core I3M support added to the parser through `--input-jsonl`, `--offset`, `--family-label`, and `--retry-failed`; the first 3000-row external extraction is complete as an extraction-quality pilot but not a retrieval result.
- Step 7 field ablation executed on the active benchmark; use conditions, output artifacts, and workflow/procedure are the strongest helpful fields, while naive not-for/dependency concatenation can add noise.
- Step 8 M0 progressive-disclosure core baseline completed historically.
- Step 9 downstream validation plan prepared, but not executed.
- Optional Qwen/OpenAI provider runner added.
- Qwen core smoke test executed successfully with `text-embedding-v4` plus `qwen3-rerank` on 5 prompts.
- Qwen full-library provider runs completed for R1 flat cards, full `SKILL.md`, and R2 structured cards, with and without `qwen3-rerank`.
- Qwen + local schema reranker ablation completed on historical conditions and the pre-public-style 2401-skill full-skill provider condition.
- Low-information prompt stress test added and run separately to check whether schema reranking depends too strongly on explicit procedural cues.
- First-pass failure-mode comparison completed for the main R2/I3 Qwen, SkillRouter, and SkillRouter+M6-v1 rows on controlled and public-gold strata.
- Historical pre-v0.4 SkillRouter hosted embedding/reranking and SkillRouter-first-stage plus M6-v1-local rows exist for the 2401-skill benchmark. The active frozen-v0.4 local SkillRouter rows are recorded above; these are separate from the external SkillRouter-Eval-Core validation track.
- Thesis LaTeX methodology/results/discussion updated to use budget-fair interpretation and strict/acceptable metric separation.

## Current Key Results

### RQ1a Input/Precondition Field-Isolation

First completed field-targeted RQ1a suite:

- Suite: `skill_benchmark/rq1a_field_discriminability/input_precondition/`
- Result: `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.md`
- Design: 50 near-neighbour clusters, 100 prompts, one direct and one paraphrase-safe prompt per cluster, 3 sibling candidates per prompt.
- Control: shared neutral context hides the target field, making all siblings intentionally tied. Adding `input_precondition` is the experimental change.

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + input/precondition top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 91.0% | +57.7pp | 0.953 |
| BM25 | Combined | 33.3% | 95.5% | +62.2pp | 0.977 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 94.0% | +60.7pp | 0.970 |
| Qwen embedding | Combined | 33.3% | 97.0% | +63.7pp | 0.985 |

Conclusion for tracker purposes: input/precondition is supported as a strong discriminating field for controlled near-neighbour routing.

### RQ1a Output/Artifact Field-Isolation

Second completed field-targeted RQ1a suite:

- Suite: `skill_benchmark/rq1a_field_discriminability/output_artifact/`
- Result: `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.md`
- Design: 50 near-neighbour clusters, 100 prompts, one direct and one paraphrase-safe prompt per cluster, 3 sibling candidates per prompt.
- Control: shared neutral context hides the target field, making all siblings intentionally tied. Adding `output_artifact` is the experimental change.
- Main exposed condition: `shared_context_plus_field`, meaning shared non-target context plus `Output Artifact: ...`.

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + output/artifact top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 53.3% | +20.0pp | 0.723 |
| BM25 | Combined | 33.3% | 76.7% | +43.3pp | 0.861 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 92.0% | +58.7pp | 0.957 |
| Qwen embedding | Combined | 33.3% | 96.0% | +62.7pp | 0.978 |

Conclusion for tracker purposes: output/artifact is supported as a strong discriminating field, with a clear semantic-matching advantage for Qwen embedding on paraphrased deliverable requests.

### RQ1a Dependency/Resource Field-Isolation

Completed field-targeted RQ1a suite:

- Suite: `skill_benchmark/rq1a_field_discriminability/dependency_resource/`
- Result: `skill_benchmark/outputs/rq1a_dependency_resource_isolation_bm25_qwen_embedding.md`
- Subtype breakdown: `skill_benchmark/outputs/rq1a_dependency_resource_subtype_breakdown.md`
- Review artifact: `skill_benchmark/rq1a_field_discriminability/dependency_resource/cluster_review.md`
- Design: 50 near-neighbour clusters, 100 prompts, one direct and one contextual prompt per cluster, 3 sibling candidates per prompt.
- Control: shared neutral context hides the target field, making all siblings intentionally tied. Adding `dependency_resource` is the experimental change.
- Main exposed condition: `shared_context_plus_field`, meaning shared non-target context plus `Dependency / Resource: ...`.
- Contextual prompt rule: the task prompt remains positive and task-like, while routing context carries the required capability. The prompt must not select by saying "not X" or "rather than sibling Y".
- Version subtype: 9 clusters now test same-family version compatibility such as React 18 versus React 17/16, Node.js 20 versus 18/16, SQLAlchemy 2.0 versus 1.4/1.3, and Next.js 13 versus 12/14.
- Public-skill grounding audit: `skill_benchmark/outputs/public_dependency_signal_analysis.md` separates hard capability dependencies from generic setup/download text. Treat MCP/tool/server requirements, provider/API identity, auth boundaries, runtime/platform constraints, pinned versions, and required resources as routing-useful dependency/resource evidence. Treat generic install/build/test/lint commands and dependency-hygiene advice as execution or quality workflow unless they name a required external capability.
- Concrete boundary examples: `npm install` and `npm ci` are weak setup evidence by themselves; Chrome DevTools MCP, `GH_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`, Firebase CLI, React 18, and Node.js 20+ are capability-compatibility evidence when visible to the selector through the request or routing context.

Prompt subset `Combined` pools the direct and contextual prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + dependency/resource top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Contextual | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Combined | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| Qwen embedding | Contextual | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Combined | 33.3% | 99.0% | +65.7pp | 0.995 |

Conclusion for tracker purposes: dependency/resource is supported as a strong discriminating field when defined as external capability compatibility. The added version cases make the suite harder: Qwen direct version rows have one React-version miss, while contextual version rows are solved. This result should be read as individual field isolation, not as proof that dependency resolves every realistic mixed-field case. It also should not be generalized to raw setup text: generic `npm install`, `pip install`, `npm ci`, build/test/lint commands, and dependency-hygiene advice have weak or no routing value unless they encode a named capability, version, provider, tool, auth, runtime, or resource conflict. A future interaction suite may test whether dependency/resource adds extra value after input/output have already narrowed the candidate set.

### RQ1a Success/Verification Field-Isolation

Completed field-targeted RQ1a suite:

- Suite: `skill_benchmark/rq1a_field_discriminability/success_verification/`
- Result: `skill_benchmark/outputs/rq1a_success_verification_bm25_qwen_embedding.md`
- Review artifact: `skill_benchmark/rq1a_field_discriminability/success_verification/cluster_review.md`
- Design: 50 near-neighbour clusters, 100 prompts, one direct and one paraphrase-safe prompt per cluster, 3 sibling candidates per prompt.
- Control: shared neutral context hides the target field, making all siblings intentionally tied. Adding `success_verification` is the experimental change.
- Main exposed condition: `shared_context_plus_field`, meaning shared non-target context plus `Success / Verification: ...`.
- Scope: concrete acceptance gates only, such as schema validation, threshold checks, evidence/source anchoring, unresolved finding state, rollback proof, reproducible failure, or runtime smoke checks. Polished writing, broad style, persuasive wording, and generic output quality are excluded.

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + success/verification top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.703 |
| BM25 | Combined | 33.3% | 74.0% | +40.7pp | 0.852 |
| Qwen embedding | Direct | 33.3% | 70.0% | +36.7pp | 0.833 |
| Qwen embedding | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.707 |
| Qwen embedding | Combined | 33.3% | 59.0% | +25.7pp | 0.770 |

Conclusion for tracker purposes: success/verification is positive but comparatively weak as a routing discriminator. It is useful when the request names the acceptance gate directly, but it drops sharply under paraphrase and is less robust than input/precondition, output/artifact, use condition, or dependency/resource. Frame it as a conditional completion-gate signal, not as a strong first-pass semantic discriminator.

### RQ1a Boundary/Not-For Field-Isolation

Completed field-targeted RQ1a suite:

- Suite: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/`
- Result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md`
- Machine summary: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.json`
- Implicit-authority analysis: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/implicit_authority_analysis.md`
- Rubric summary: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/rubric_summary.md`
- Design: 50 near-neighbour clusters, 150 prompts, one direct, one paraphrase-safe, and one implicit-authority prompt per cluster, 3 sibling candidates per prompt.
- Control: shared neutral context hides the target boundary, making all siblings intentionally tied. Adding `boundary_not_for` is the experimental change.
- Main exposed condition: `shared_context_plus_field`, meaning shared non-target context plus `Boundary / Not For: ...`.

Prompt subset `Combined` pools direct, paraphrase-safe, and implicit-authority prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + boundary/not-for top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| BM25 | Paraphrase | 33.3% | 90.0% | +56.7pp | 0.943 |
| BM25 | Implicit authority | 33.3% | 62.0% | +28.7pp | 0.800 |
| BM25 | Combined | 33.3% | 83.3% | +50.0pp | 0.911 |
| Qwen embedding | Direct | 33.3% | 84.0% | +50.7pp | 0.917 |
| Qwen embedding | Paraphrase | 33.3% | 82.0% | +48.7pp | 0.907 |
| Qwen embedding | Implicit authority | 33.3% | 58.0% | +24.7pp | 0.777 |
| Qwen embedding | Combined | 33.3% | 74.7% | +41.3pp | 0.867 |

Conclusion for tracker purposes: boundary/not-for is useful, but conditional. It is strong when the request explicitly states the exclusion or guardrail and weaker when the prompt only implies authority, scope, or review context. Frame it as a scope/authority/guardrail signal, not as a simple positive matching field.

Frozen-v0.4 controlled results, top-1 by fixed method and information layer.

The BM25/TF-IDF and Qwen rows below were refreshed on 2026-06-23 after the public-original loader/exporter correction and messier public-style controlled regeneration. SkillRouter rows in this subsection are historical until rerun under the corrected corpus.

| Method family | I1 flat card | I3 structured fields | I2 full skill |
|---|---:|---:|---:|
| BM25 lexical, refreshed 2026-06-23 | 55.1% | 58.0% | 66.5% |
| TF-IDF lexical, refreshed 2026-06-23 | 52.6% | 59.6% | 69.4% |
| Qwen embedding, refreshed 2026-06-23 | 33.9% | 40.4% | 42.4% |
| Qwen embedding + Qwen rerank top-20, refreshed 2026-06-23 | 51.0% | 58.4% | 62.9% |
| Qwen + local schema top-20, refreshed 2026-06-23 | 42.9% | 49.4% | 49.8% |
| M6-v2 fixed task-heavy, Qwen only, refreshed 2026-06-23 | 35.5% | 38.4% | 40.8% |
| SkillRouter embedding, historical | 62.9% | 64.5% | 59.2% |
| SkillRouter embedding + SkillRouter rerank top-20, historical | 65.7% | 71.0% | 71.8% |
| SkillRouter embedding + M6-v1 diagnostic top-20, historical | 67.8% | 70.2% | 68.6% |

Frozen-v0.4 public-gold results, strict top-1 by fixed method and information layer.

The BM25/TF-IDF and Qwen rows below were refreshed on 2026-06-23 from upstream public `source/SKILL.original.md`. SkillRouter rows in this subsection are historical until rerun under the corrected source policy.

| Method family | I1 flat card | I3 structured fields | I2 full skill |
|---|---:|---:|---:|
| BM25 lexical, refreshed 2026-06-23 | 55.6% | 54.9% | 59.0% |
| TF-IDF lexical, refreshed 2026-06-23 | 56.9% | 50.7% | 48.6% |
| Qwen embedding, refreshed 2026-06-23 | 57.6% | 61.8% | 70.8% |
| Qwen embedding + Qwen rerank top-20, refreshed 2026-06-23 | 73.6% | 70.8% | 72.9% |
| Qwen + local schema top-20, refreshed 2026-06-23 | 58.3% | 55.6% | 61.1% |
| M6-v2 fixed task-heavy, Qwen only, refreshed 2026-06-23 | 54.9% | 56.9% | 59.7% |
| SkillRouter embedding, historical | 68.8% | 75.0% | 75.0% |
| SkillRouter embedding + SkillRouter rerank top-20, historical | 70.8% | 71.5% | 70.1% |
| SkillRouter embedding + M6-v1 diagnostic top-20, historical | 70.1% | 72.2% | 73.6% |

External SkillRouter-Eval-Core FTS/BM25 snapshot, 75 scored multi-skill tasks:

| Tier | Layer | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Approx tokens |
|---|---|---:|---:|---:|---:|---:|
| Easy | I1 flat metadata | 36.0% | 0.448 | 48.3% | 32.0% | 5.49M |
| Easy | I2 full body | 48.0% | 0.558 | 57.4% | 42.7% | 152.67M |
| Easy | I3C V2 cleaned fields | 53.3% | 0.586 | 60.5% | 44.0% | 15.68M |
| Hard | I1 flat metadata | 28.0% | 0.373 | 46.1% | 30.7% | 5.54M |
| Hard | I2 full body | 44.0% | 0.525 | 55.7% | 41.3% | 153.16M |
| Hard | I3C V2 cleaned fields | 45.3% | 0.527 | 59.2% | 40.0% | 15.83M |

External SkillRouter-Eval-Core neural full-context snapshot:

| Tier | Layer | Mode | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Status |
|---|---|---|---:|---:|---:|---:|---|
| Easy | I2 full body | SkillRouter embedding | 60.0% | 0.660 | 64.7% | 48.0% | Partial recovered row only; rerank and Hard missing. |
| Easy | I3C full context | SkillRouter embedding | 46.7% | 0.531 | 55.1% | 37.3% | Complete recovered row. |
| Easy | I3C full context | SkillRouter embedding + rerank top-20 | 57.3% | 0.631 | 55.1% | 37.3% | Complete recovered row. |
| Hard | I3C full context | SkillRouter embedding | 37.3% | 0.477 | 53.7% | 37.3% | Complete recovered row. |
| Hard | I3C full context | SkillRouter embedding + rerank top-20 | 48.0% | 0.563 | 53.7% | 37.3% | Complete recovered row. |

Read this neural table cautiously: the I3C rows are complete for I3C, but the I2 neural comparator is not complete, so this is not a final I2-vs-I3C neural matrix.

Current result interpretation:

- Controlled prompts show the clearest information-layer effect: I3 structured fields improve over I1 under lexical, Qwen, and SkillRouter settings, with statistically meaningful paired differences for TF-IDF, Qwen embedding, and Qwen rerank.
- Public-gold is more mixed. I3 often improves candidate recall and embedding-only retrieval, but public skill names/descriptions sometimes carry strong provider/task cues that help I1 after reranking.
- I2 full skill text is not automatically better. It can help SkillRouter on public-gold, but it hurts Qwen and lexical public-gold retrieval, showing that more text can add noise and cost.
- SkillRouter is the strongest candidate generator on many rows, especially in top-5/candidate recall, but it does not remove the need to compare information layers.
- M6-v1 and M6-v2 should be treated as transparent field-signal diagnostics for now, not as final superior architectures.
- External SkillRouter-Eval-Core now gives a stronger I3C portability signal. Under disk-backed BM25 on 75 multi-skill tasks and 78-79K skills, the thesis-facing primary comparison excludes the older heuristic extraction condition and compares I1, I2, and cleaned I3C V2. I3C V2 beats I2 on Easy Hit@1/MRR/Recall/FullCoverage and narrowly beats I2 on Hard Hit@1/MRR/Recall while using about 10% of the I2 token volume. I2 still slightly leads Hard FullCoverage@20. Local I3C remains pending because the current local model-parsed artifact is I3M/DeepSeek, not Codex-subagent I3C.

Failure-mode summary:

- Controlled Qwen R2 + Qwen rerank has an 18.0% first-stage exclusion problem, so the gold skill is often not in the top-20 candidate set.
- Controlled SkillRouter R2 reduces first-stage exclusion to about 2-3%, leaving most remaining errors as ordering failures among plausible near-neighbour skills.
- Public-gold methods have low first-stage exclusion but many ordering/acceptable-alternative issues, so strict and acceptable labels must be reported separately.

Historical results:

The 1006-, 2089-, and 2349-skill sections below are retained as historical development evidence and scale-comparison context. Do not use them as the active headline condition unless explicitly labelled.

Historical local full-library results on 1006 skills:

- M1 BM25 flat: 64.2% strict top-1.
- M1 TF-IDF flat: 58.2% strict top-1.
- M2a MiniLM description embedding: 47.8% strict top-1.
- M2b MiniLM full-skill embedding: 61.2% strict top-1.
- M3 TF-IDF schema: 71.6% strict top-1.
- M6 BM25 -> schema rerank: 71.6% strict top-1.
- M6 TF-IDF -> schema rerank: 70.2% strict top-1.
- M6 MiniLM full-skill -> schema rerank: 80.6% strict top-1.

M0 progressive disclosure on 67 controlled core skills:

- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full docs loaded: 0.78.

Qwen provider smoke test:

- Scale: core, 67 skills.
- Prompts: first 5 benchmark prompts.
- Method: `text-embedding-v4` over full `SKILL.md` plus `qwen3-rerank` over top-20 candidates.
- Result: 100.0% top-1, 100.0% top-5, MRR 1.000.
- Output report: `skill_benchmark/outputs/provider_selector_qwen_core_smoke.md`.

Historical Qwen provider full-library results on 1006 skills:

- R1 flat card embedding only: 35.8% top-1, 56.7% top-5.
- R1 flat card embedding + rerank: 64.2% top-1, 67.2% top-5.
- Full `SKILL.md` embedding only: 46.3% top-1, 71.6% top-5.
- Full `SKILL.md` embedding + rerank: 61.2% top-1, 65.7% top-5.
- R2 structured-card embedding only: 47.8% top-1, 65.7% top-5.
- R2 structured-card embedding + rerank: 65.7% top-1, 71.6% top-5.
- Output comparison: `skill_benchmark/outputs/provider_selector_qwen_comparison.md`.

Qwen + local schema reranker:

- Full `SKILL.md` embedding + local schema rerank, top-20: 68.7% top-1.
- Full `SKILL.md` embedding + local schema rerank, top-50: 80.6% top-1.
- Full `SKILL.md` embedding + local schema rerank, top-100: 85.1% top-1.
- Interpretation: Qwen embeddings are useful as a broad candidate generator, but procedural schema reranking is better aligned with the final selection task than Qwen's generic reranker.
- Output report: `thesis_notes/results/Qwen Local Schema Reranker Ablation.md`.

Interpretation:

- Qwen reranking improves top-1 over Qwen embedding-only for every tested representation.
- Generic Qwen reranking is weaker than procedural schema reranking on this benchmark.
- The current strongest result is Qwen full-skill retrieval plus local schema reranking over a top-100 candidate pool.
- This supports the thesis framing that strong semantic retrieval and procedural schema reranking are complementary.

Low-information stress test:

- 12 separate prompts with deliberately weaker procedural wording.
- Best strict top-1 is 41.7% for MiniLM full-skill embedding.
- Qwen full + local schema top-100 gets 25.0% top-1 and 66.7% top-5.
- Interpretation: the schema reranker is not cheating by inferring hidden intent; it needs procedural evidence in the request.
- Report: `thesis_notes/results/Low Information Stress Test.md`.

Failure mode analysis:

- Target: Qwen full-skill embedding plus local schema reranking over top-100 candidates.
- 10 strict top-1 failures.
- 4 failures are first-stage exclusions where Qwen does not place gold in top-100.
- 6 failures are reranker, boundary, negation, meta-skill, or annotation issues.
- Report: `thesis_notes/results/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.

Interpretation:

- The benchmark is currently good enough for method comparison.
- Structure-aware reranking is strongest among local methods so far.
- MiniLM is a construction/local baseline, not the final modern embedding baseline.

## What To Do Next

Follow the roadmap in `thesis_notes/current/Thesis Experiment Roadmap.md`.

Current phase: RQ2b B1S is sealed. Build and obtain separate B1R source-text transfer approval before any I3C extraction or scientific full-library retrieval.

Immediate next steps:

1. Move the frozen-v0.4 information-layer matrix into the thesis results chapter, grouped by information layer first and method second.
2. Add a candidate-recall companion table and explain first-stage exclusion versus reranker ordering failure.
3. Add representative controlled and public-gold failure cases to the failure-analysis chapter.
4. Report public-gold by source family, provider/tool cue status, and acceptable-alternative status.
5. Decide whether final selected comparisons need paired bootstrap/randomization tests for MRR/top-k beyond the existing top-1 CIs and McNemar tests.
6. Add thesis-ready experimental setup table: model settings, prompts, gold labels, candidate budgets, scoring rules, cache/cost, and metrics.
7. Add literature-review empirical-detail table responding to supervisor feedback.
8. Consolidate candidate-budget cost/latency for top-20, top-50, and top-100.
9. Decide whether M4 tree and M5 graph are final experiment families or discussion/future work.
10. Audit M6-v1/M6-v2 field activation if either diagnostic is included in the main thesis body.
11. Decide whether full 2433-skill M0 is useful as a context/cost stress test.
12. Run downstream validation on a small sample after the final method set and candidate budget are chosen.
13. Update thesis LaTeX chapters with final method, result, statistical, and failure-analysis tables.

## What Not To Do Yet

- Do not expand beyond the frozen 2433-skill benchmark unless final methods make the benchmark too easy or adjudication shows the scale layer is too artificial.
- It is acceptable to expand public skills as background/taxonomy validation if they are clearly separated from controlled gold skills.
- Do not treat provider choice as the thesis contribution.
- Do not add more providers or model variants unless they test a new representation claim.
- Do not tune prompts, gold labels, or schema weights after the final method set is frozen unless the change is logged as a validity correction.
- Do not run Step 9 downstream validation until the field taxonomy, final method set, and candidate budget are chosen.

## Canonical Reference Files

- Benchmark rubric: `skill_benchmark/notes/benchmark_methodology_rubric.md`
- Experiment roadmap: `thesis_notes/current/Thesis Experiment Roadmap.md`
- Draft final field taxonomy: `thesis_notes/methodology/Final Representation Field Taxonomy - Draft.md`
- Public model verification checkpoint: `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 460 Skills.md`
- Critique response plan: `thesis_notes/methodology/Critique Response and Validity Improvement Plan.md`
- Public expansion checkpoint: `thesis_notes/checkpoints/benchmark_validation/Public Expansion 2349 Validation Checkpoint.md`
- Provider API setup: `skill_benchmark/notes/provider_api_baselines.md`
- Literature refresh: `thesis_notes/literature/Reranking and Skill Retrieval Literature Refresh 2026-05-25.md`
- Offline selector results: `skill_benchmark/outputs/offline_selector_evaluation.md`
- M0 baseline report: `skill_benchmark/outputs/m0_progressive_disclosure_core_report.md`
- Step 9 downstream plan: `skill_benchmark/outputs/step8_downstream_validation_plan.md` (file name still says step8 from the earlier numbering)

## Drift Check

Before adding a new experiment, ask:

- Does this test a representation class or only a provider?
- Does it preserve the same prompts, gold labels, and scale condition?
- Does it report accuracy, top-k recall, MRR, context/cost, and failure modes?
- Does it help answer which information a skill representation needs to preserve?

If the answer is no, postpone it.
# 2026-08-29 RQ1b v2 Execution Hold And Follow-on Decisions

The frozen RQ1b field-type availability v2 corpus has passed local pre-BM25
validation. The authorised next action is local BM25 only over its 87 strict
preserved routing families and the seven field-specific subsets (77--86
families). Qwen dense scoring remains gated behind a local payload/cost
preflight and a separate exact external-text authorisation. Any expansion to a
100+ composition `RQ1b v3` cohort and any public-field prevalence census are
deferred until v2 results and failure analysis are reviewed. Neither may alter
v2 cards, labels, exclusions, or primary denominators. Decision note:
`thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Extension and Field Prevalence Decision Note - 2026-08-29.md`.

The authorised local BM25 run is now complete: 1,392 audited local rows over
87 strict families and two prompt variants per family. Use condition has the
largest directional `FULL-MASK` contrast, but its composition-bootstrap 95%
interval crosses zero and all other field contrasts are smaller or mixed.
Treat this as a conditional public-card result only. Qwen remains pending an
exact external-text payload/cost preflight and separate approval. Evidence:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_bm25_2026-08-29/BM25_RESULT_CHECKPOINT_2026-08-29.md`.
