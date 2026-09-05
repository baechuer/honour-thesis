# RQ1 Public Original Round 3 Joint Group Qwen Result

Date: 2026-09-04  
Status: `COMPLETE / MECHANICALLY AND SOURCE VALIDATED / RESEARCHER REVIEWED WITH EDITS VISIBLE / INTEGRATED INTO THESIS`

## Scope and Integrity

This is the dense twin of the original-source joint group-removal test. It uses
the same 369 frozen composition-family cases, strict singleton golds,
direct/paraphrase prompts, group masks and composition-level bootstrap plan as
the local BM25 run.

- Freeze SHA-256: `7a73a3d4026ffa32b855ae3844cf3d63046aff9535435294a2cf742f84cc9062`
- Authorised payload SHA-256: `8d9d87e791a0f34807f4a2ae8f85ec43798a7df356bffd8a38a4db22520bb2ea`
- Result SHA-256: `9e22601201ab32605d021b83418efa56a051db43147b1e2da8b4488b394440d4`
- Analysis SHA-256: `9edf55d448b6612e8a141ba57490417c4a96969da81cde037ee7ee20693420fc`
- DashScope international `text-embedding-v4`, 1024 dimensions.
- 342 new group-masked candidate documents sent; zero query texts sent.
- 35 request attempts, 35 successful calls, zero retries, 283,526
  provider-reported input tokens.
- 1,476/1,476 rank rows passed independent identity, pair, rank, checksum and
  composition-level analysis validation.

## Result

Primary estimates first average the two prompt forms within each routing family,
then equally average families within composition. The 95% intervals use 10,000
seeded composition-clustered paired bootstrap resamples. A positive delta means
the original document routed better than the group-removed document.

| Group | Full Hit@1 | Removed Hit@1 | Hit@1 delta [95% CI] | MRR delta [95% CI] | Cosine-margin delta [95% CI] |
| --- | ---: | ---: | ---: | ---: | ---: |
| Task specification | 0.872 | 0.784 | +0.088 [+0.005, +0.162] | +0.047 [-0.006, +0.092] | +0.0237 [+0.0112, +0.0366] |
| Execution/verification | 0.864 | 0.790 | +0.074 [+0.007, +0.141] | +0.039 [+0.001, +0.076] | +0.0198 [+0.0096, +0.0312] |
| Applicability/capability | 0.848 | 0.834 | +0.014 [-0.043, +0.062] | +0.010 [-0.022, +0.038] | +0.0062 [+0.0005, +0.0122] |

## Reading the Result

Task specification and execution/verification show positive Top-1 intervals in
both the BM25 and Qwen twins. Applicability/capability is positive in BM25 but
its Qwen Top-1 interval crosses zero. Qwen cosine margins decline for every
group, including applicability; this is a within-Qwen diagnostic and does not
override the non-stable Top-1 result or combine numerically with BM25 margins.

This supports a narrow combined-information statement only. It cannot identify
the decisive field within a group, establish additivity, or establish that the
removed documents remain executable. It does not update thesis LaTeX/PDF.

## Canonical Artifacts

- SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md`
- Result: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_qwen_results/qwen_results.json`
- Analysis: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_qwen_results/analysis/qwen_paired_analysis.json`
