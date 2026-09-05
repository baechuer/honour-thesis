# Results Writing Packet

Date: 2026-09-04  
Status: `RQ1 CURRENT / RESEARCHER REVIEW COMPLETE / COMMUNICATION REVISION VERIFIED`  
Purpose: one readable inventory of completed result packages before drafting the Results chapter. It keeps experimental populations, metrics, and claim limits separate. It does not replace frozen machine-readable outputs.

## 1. Version Boundary Before Writing

The current RQ1 evidence roles are:

| Record | What it tests | Result state | Writing treatment now |
| --- | --- | --- | --- |
| Controlled RQ1 field isolation | Same neutral context for three AI-assisted near-neighbours; expose exactly one candidate-specific field. | Complete; all 350 rows were reviewed and approved by the researcher with labels visible. | First RQ1 experiment: controlled evidence that each field can help within its own suite. |
| 2026-08-30 field-card ablation | Source-grounded, seven-slot derivative cards; synchronously hide one slot from every candidate. | Complete; every individual Top-1/MRR interval crosses zero. | Historical sensitivity analysis only. Do not pool with the main result. |
| Public-original Round 3, 2026-09-04 | Exact public `SKILL.md` compared with the exact same source after source-line removal of one named field. | Complete, source-grounded and mechanically validated; all 194 scored public-gold and 402 scored removal-fidelity rows were approved by the researcher. | Second RQ1 intervention and current thesis-facing public-artifact evidence. |
| Public field-presence review | Binary review of 29,292 complete primary public skill documents by a Codex `gpt-5.6-terra` agent at `xhigh` reasoning. | Complete in 31 recorded batches; retained summary and batch totals accepted by the researcher. The exact row-level decisions and verbatim batch prompt are not retained. | Descriptive support that the fields are common; not routing evidence or a released per-document annotation dataset. |

The two public treatments are not interchangeable: field cards preserve distributed slot evidence, whereas the latest experiment removes cited source lines and may leave a non-executable document. They must not be pooled. The author chose the later original-source result as the thesis-facing public intervention and retains the 2026-08-30 field-card null result as documented historical sensitivity.

Counting clarification: the source pipeline contains 199 upstream paired prompt/gold families, but 194 occur in at least one clean scored field condition. It generated 574 composition-field transformations, 439 of which were all-candidate `CLEAR`; 402 also had a paired prompt/gold binding and occur in the scoring freeze. The researcher-review denominators are therefore 194 public gold decisions and 402 transformation-fidelity decisions, not 199 and 574.

The complete researcher review contains 946 approved rows: 350 controlled, 194 public gold, and 402 public-removal transformations. Labels were visible for controlled and public-gold review, while intact and removed documents were visible for removal-fidelity review. This records researcher approval, not blinded or independent annotation.

RQ2a is confirmatory and user-reviewed. RQ2b's B3-v2 file retains its historical `PENDING USER REVIEW / NOT THESIS TEXT` status because it is an immutable local synthesis record. Later B5 integration is verified in `thesis_latex/chapters/05_methodology.tex`, `06_results.tex`, and `07_discussion.tex`; RQ2b is therefore eligible for results writing. The historical B3 status must not be copied as the current thesis status.

## 2. Metric Dictionary

| Metric | Meaning | Use and restriction |
| --- | --- | --- |
| Tie-adjusted Top-1 | Expected rank-one accuracy under a deliberate tie. | RQ1a hidden condition only: identical candidates should score 1/3. |
| Strict Hit@1 | The frozen singleton gold skill is rank one. | RQ1 public-original and RQ2b. It is agreement with this strict label, not proof that no alternative would work. |
| MRR / MRR@20 | Reciprocal rank of the strict gold, averaged over the stated unit. | Secondary rank-quality evidence. |
| Recall@20 | Gold occurs in the first-stage top twenty. | RQ2b only; it is B2's candidate-coverage ceiling. |
| Native margin | Gold score minus best wrong-candidate score. | Diagnostic within one selector only. Do not numerically compare BM25 and cosine margins. |
| Full-minus-removed delta | Paired performance on full original minus the exact masked variant. | RQ1 public-original. Positive means removal weakens routing. |
| 95% paired bootstrap interval | Repeated cluster/composition-resampling stability range. | An interval excluding zero supports a stable direction in that frozen population. It is not a claim of universal causation. |

## 3. RQ1 Experiment 1: Controlled Field-Isolation Evidence

All seven suites use three candidates. `hidden` has deliberately identical candidate content, so Top-1 is 1/3 by construction. `exposed` adds only the candidate-specific tested field. Values below are combined direct/paraphrase prompts; boundary also contains its approved implicit-authority prompts.

| Field | Prompts | BM25 hidden -> exposed (lift) | Qwen hidden -> exposed (lift) | Exposed MRR, BM25 / Qwen |
| --- | ---: | ---: | ---: | ---: |
| Use condition | 100 | .333 -> .845 (+.512) | .333 -> .910 (+.577) | .903 / .955 |
| Input / precondition | 100 | .333 -> .955 (+.622) | .333 -> .970 (+.637) | .977 / .985 |
| Output / artifact | 100 | .333 -> .767 (+.433) | .333 -> .960 (+.627) | .861 / .978 |
| Workflow / procedure | 100 | .333 -> .780 (+.447) | .333 -> .620 (+.287) | .875 / .795 |
| Success / verification | 100 | .333 -> .740 (+.407) | .333 -> .590 (+.257) | .852 / .770 |
| Boundary / not-for | 150 | .333 -> .833 (+.500) | .333 -> .747 (+.413) | .911 / .867 |
| Dependency / resource | 100 | .333 -> 1.000 (+.667) | .333 -> .990 (+.657) | 1.000 / .995 |

**Controlled answer.** Every tested operational field can distinguish the constructed near-neighbours when it is the only candidate-specific information available. The seven fields use separate 50-cluster suites, so these rows do not rank fields against one another. The field values were used as written and were not forced to equal length; the result therefore measures the practical value of exposing the information, including its amount and specificity, rather than a length-normalised effect of field meaning alone. It does not establish independent public-document effects.

Source: `thesis_notes/current/Current Results Summary.md` and the seven `skill_benchmark/outputs/rq1a_*_bm25_qwen_embedding.*` outputs.

### Examples/tests negative control

Examples/tests were evaluated only in the controlled experiment. They were **not** included in the public-original removal experiment, and no public-document examples/tests deletion was run. In 50 three-sibling clusters where all operational information was shared and only examples/tests differed, generic prompts had no true operational gold: BM25 changed from .333 hidden to .227 with examples, TF-IDF remained about .330, and Qwen changed from .333 to .280. DeepSeek and Codex reasoning selectors marked these generic rows ambiguous. All methods selected the matching candidate on the deliberately rare exact-example prompts. Thus examples/tests remain a negative control and workflow-support information: they can attract a selector when a request copies an example, but they do not provide a stable independent capability distinction.

## 4. RQ1: Latest Public-Original Single-Field Removal

Population: exact source documents, strict singleton labels, direct/paraphrase pairs averaged within a routing family, then equal-weighted within a source composition. Each field has its own clean-only denominator; no field values are pooled. The edited document may be non-executable by design.

| Field | Source compositions | BM25 Hit@1 delta [95% CI] | Qwen Hit@1 delta [95% CI] | Conservative reading |
| --- | ---: | ---: | ---: | --- |
| Use condition | 57 | +.114 [.067, .167] | +.058 [.031, .092] | Stable under both. |
| Input / precondition | 53 | +.098 [.051, .149] | +.016 [-.017, .052] | BM25 only. |
| Output / artifact | 49 | +.122 [.065, .187] | +.003 [-.036, .036] | BM25 only. |
| Workflow / procedure | 63 | +.151 [.086, .215] | +.040 [-.024, .100] | BM25 only. |
| Success / verification | 59 | +.117 [.059, .182] | +.027 [.005, .054] | Stable under both. |
| Boundary / not-for | 69 | +.024 [-.014, .064] | -.022 [-.054, .008] | No stable positive Top-1 effect. |
| Dependency / resource | 52 | +.091 [.046, .139] | +.013 [-.048, .067] | BM25 only. |

The frozen twin contains 1,078 composition-family cases, 2,156 prompt rows, and 4,312 ranking rows per retriever. Qwen ran 190 successful no-retry calls, embedding 1,898 cache-miss texts; no query rewrite or reranking was used.

**Public-original answer.** Use condition and success/verification have cross-retriever stable evidence. Other fields are retriever-conditional, and boundary/not-for has no stable positive strict Top-1 result in this population.

Source: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md`.

## 5. RQ1: Latest Public-Original Joint Group Removal

This is a supporting test of three exact-union line-deletion groups. It cannot attribute an effect to a single component or claim additivity.

| Group | Families / compositions | BM25: full -> removed Hit@1; delta [95% CI] | Qwen: full -> removed Hit@1; delta [95% CI] |
| --- | ---: | --- | --- |
| Task specification: use + input + output | 99 / 37 | .784 -> .518; +.266 [.196, .336] | .872 -> .784; +.088 [.005, .162] |
| Execution/verification: workflow + success | 138 / 51 | .790 -> .614; +.176 [.094, .262] | .864 -> .790; +.074 [.007, .141] |
| Applicability/capability: boundary + dependency | 132 / 50 | .780 -> .644; +.136 [.087, .186] | .848 -> .834; +.014 [-.043, .062] |

Task specification and execution/verification are stable in both first-stage retrievers. Applicability/capability is only stable under BM25. The dense execution used 342 new masked documents, no queries, and 35 successful no-retry calls.

Sources: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group BM25 Result - 2026-09-04.md` and `RQ1 Public Original Round 3 Joint Group Qwen Result - 2026-09-04.md`.

## 6. RQ2a: Matched-Content Representation Study

Population: 280 confirmatory controlled clusters, 600 prompts, 22 conditions, 13,200 aligned rows. Every non-shared representation expresses the same seven operational propositions; only organisation, order or neutral dilution changes.

| Selector | Representation | Top-1 | MRR | Strict confusion |
| --- | --- | ---: | ---: | ---: |
| BM25 | fielded | .864 | .921 | .127 |
| BM25 | flat | .843 | .911 | .147 |
| BM25 | prose | .840 | .908 | .152 |
| Qwen single-vector | fielded | .757 | .863 | .252 |
| Qwen single-vector | flat | .824 | .902 | .185 |
| Qwen single-vector | prose | .782 | .873 | .233 |
| Qwen field-aware uniform top-two | fielded | .823 | .901 | .145 |
| SkillRouter cross-encoder | fielded | .951 | .973 | .053 |
| SkillRouter cross-encoder | flat | .955 | .975 | .048 |
| SkillRouter cross-encoder | prose | .946 | .969 | .058 |
| Any selector | shared-only (designed 3-way tie) | .333 | .611 | .000 |

Preregistered headline contrasts:

| Contrast | Top-1 delta [95% CI] | Reading |
| --- | --- | --- |
| Qwen fielded - flat | -.067 [-.099, -.036] | Field headings harm this pooled single-vector condition. |
| BM25 fielded - flat | +.021 [.010, .033] | Detectable but below the frozen 3pp practical threshold. |
| SkillRouter fielded - flat | -.004 [-.014, .006] | No stable organisation effect. |
| Qwen field-aware - Qwen fielded | +.066 [.021, .111] | Field-wise aggregation recovers the fielded pooling deficit. |

**RQ2a answer.** Candidate-specific operational facts matter, but headings are not a universal accuracy mechanism. The frozen field-aware rule restores the fielded Qwen deficit but does not beat flat Qwen overall (.823 vs .824).

Source: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.

## 7. RQ2b V3: Full-Library Representation and Retrieval Matrix

Population: 2,433 skills, 381 strict-gold prompts, 86 semantic clusters. Controlled and public-gold strata remain separate. B1 ranks the whole library; B2 reranks the exact persisted B1 Top-20, so B1 Recall@20 limits B2 recovery. The table reports cluster-macro strict Hit@1. `I1` is discovery metadata; `I2` is original full skill; `I3-flat` is extracted evidence without labels; `I3C` is the same evidence field-labelled.

### 7.1 Cluster-macro strict Hit@1

| Stratum | B1 retriever | I1 B1 / Qwen B2 / SR B2 | I2 B1 / Qwen B2 / SR B2 | I3-flat B1 / Qwen B2 / SR B2 | I3C B1 / Qwen B2 / SR B2 |
| --- | --- | --- | --- | --- | --- |
| Controlled | BM25 | .559 / .741 / .689 | .535 / .685 / .682 | .452 / .712 / .673 | .453 / .713 / .689 |
| Controlled | Qwen embedding | .351 / .588 / .561 | .367 / .553 / .570 | .358 / .577 / .538 | .361 / .592 / .560 |
| Controlled | SkillRouter embedding | .700 / .785 / .717 | .656 / .723 / .714 | .679 / .765 / .725 | .682 / .777 / .737 |
| Public-gold | BM25 | .597 / .771 / .734 | .644 / .812 / .779 | .512 / .718 / .715 | .504 / .718 / .712 |
| Public-gold | Qwen embedding | .612 / .812 / .772 | .686 / .842 / .796 | .560 / .734 / .747 | .538 / .758 / .752 |
| Public-gold | SkillRouter embedding | .761 / .845 / .772 | .806 / .834 / .771 | .752 / .785 / .790 | .746 / .785 / .785 |

### 7.2 B1 MRR@20 / Recall@20

| Stratum | B1 retriever | I1 MRR / R@20 | I2 MRR / R@20 | I3-flat MRR / R@20 | I3C MRR / R@20 |
| --- | --- | --- | --- | --- | --- |
| Controlled | BM25 | .674 / .893 | .679 / .929 | .592 / .880 | .591 / .880 |
| Controlled | Qwen embedding | .466 / .728 | .489 / .773 | .466 / .710 | .467 / .715 |
| Controlled | SkillRouter embedding | .808 / .981 | .790 / .980 | .798 / .974 | .801 / .974 |
| Public-gold | BM25 | .688 / .893 | .768 / .984 | .618 / .873 | .613 / .865 |
| Public-gold | Qwen embedding | .727 / .962 | .782 / 1.000 | .699 / .919 | .681 / .921 |
| Public-gold | SkillRouter embedding | .848 / .992 | .867 / .992 | .836 / .992 | .835 / .975 |

### 7.3 Interpretation Boundary

I2 is the strongest representation on the public-gold stratum for all three first-stage retrievers. I3C is near-identical to I3-flat, so labels alone do not create a general full-library gain. Both B2 rerankers often improve ordering conditional on Top-20 inclusion, but cannot repair a B1 candidate miss. These are strict-label routing results, not downstream success or a graph/tree comparison.

Source: `skill_benchmark/rq2bv1/results/b3_v3_v2/B3_V2_LOCAL_ANALYSIS.md` and `B2_DUAL_RERANKER_V3_RESULTS.md`.

## 8. RQ2 Cost Tables

### RQ2a observed execution cost

| Condition | New calls | Provider tokens | Construction wall | New-query time / prompt |
| --- | ---: | ---: | ---: | ---: |
| BM25 | 0 | 0 | 0.000 s | .001100 s |
| Qwen single-vector | 590 | 1,175,784 | 1,085.293 s | .002869 s |
| Qwen field-aware | 77 | 13,583 | 203.259 s | .002398 s |
| SkillRouter cross-encoder | 0 | 0 | 0.000 s | 11.099921 s |

### RQ2b B1 corpus footprint and observed timing

| Retriever | Representation | One-time index/embed seconds | Mean query seconds | Selector-visible corpus tokens |
| --- | --- | ---: | ---: | ---: |
| BM25 | I1 / I2 / I3-flat / I3C | .021 / .233 / .067 / .083 | .001725 / .004461 / .002929 / .002895 | 63,013 / 825,269 / 212,457 / 228,222 |
| Qwen | I1 / I2 / I3-flat / I3C | 86.773 / 966.577 / 297.083 / 324.292 | .001236 / .002538 / .001825 / .001229 | 93,939 / 1,455,632 / 320,211 / 349,639 |
| SkillRouter | I1 / I2 / I3-flat / I3C | 11.392 / 80.286 / 15.848 / 16.967 | .003019 / .002708 / .003360 / .002662 | 96,372 / 1,458,065 / 322,644 / 352,072 |

I3 extraction is a shared one-time footprint, not double-charged to I3-flat and I3C. No durable comparable I3 extraction wall-time or provider invoice was recorded, so this is not a complete I2-versus-I3 total dollar-cost claim.

## 9. Recommended Results Chapter Sequence

1. Define strict labels and metric boundaries.
2. Present RQ1 Experiment 1 controlled field sufficiency, including examples/tests as a negative control.
3. Present the **chosen** RQ1 public-artifact treatment, without pooling it with the other treatment.
4. Present RQ2a matched-content organisation result.
5. Present RQ2b full-library trade-offs, labelled as strict-label evidence; separate controlled/public-gold strata and cost boundaries.
6. Discuss limits: field redundancy in natural documents, model dependence, absent graph/tree comparison, strict-gold endpoint, and incomplete I3 construction-cost ledger.

## 10. Pre-Drafting Decisions

- [x] Promote the 2026-09-04 original-source RQ1 removal results to the thesis-facing public RQ1 intervention and retain the 2026-08-30 field-card null result as historical sensitivity.
- [x] RQ2b status reconciled: B3-v2 is the frozen local result record; subsequent B5 integration is already present in the thesis chapters.
- [x] Approve the conservative language: cross-retriever stable RQ1 evidence for use condition, success/verification, task specification, and execution/verification; no claim that all seven fields are universally necessary or additive.
- [x] Complete and reconcile the prospective RQ1 researcher-review ledgers: 350 controlled, 194 scored public-gold, and 402 scored public-removal units (`946/946` approved).
