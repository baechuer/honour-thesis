# External SkillRouter Corpus Richness Audit - 2026-06-23

This checkpoint records a static corpus and prompt audit for SkillRouter-Eval-Core. The purpose is to interpret the external benchmark as portability evidence without overclaiming that it has the same difficulty profile as the local frozen-v0.4 controlled benchmark.

## Artifacts

- Audit script: `skill_benchmark/scripts/audit_skill_corpus_richness.py`
- JSON output: `skill_benchmark/outputs/skill_corpus_richness_audit.json`
- Markdown output: `skill_benchmark/outputs/skill_corpus_richness_audit.md`

The audit is local and lexical/structural only. It detects markdown headings, section labels, procedural cues, prompt length, file/path cues, and explicit input/output cues. It cannot prove whether a skill was AI-generated unless source metadata says so.

## Skill-Body Structure

| Corpus | Rows | Median tokens | P90 tokens | H1 | Rich schema | Procedural | Use | Input | Workflow | Output | Constraints | Dependencies |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SkillRouter all | 79141 | 726 | 2020 | 95.0% | 27.6% | 78.8% | 49.0% | 29.5% | 57.3% | 29.9% | 20.7% | 46.4% |
| SkillRouter scored gold names | 533 | 885 | 2310 | 98.5% | 27.4% | 79.2% | 66.6% | 23.5% | 62.9% | 35.5% | 26.3% | 54.8% |
| Local controlled gold+alts | 240 | 260.5 | 335 | 100.0% | 72.9% | 73.3% | 95.8% | 67.1% | 73.3% | 42.9% | 60.8% | 47.1% |
| Local public import wrappers | 460 | 321 | 356 | 100.0% | 0.0% | 2.2% | 100.0% | 1.3% | 2.2% | 0.0% | 0.7% | 100.0% |

Rich schema is defined as at least four of use/input/workflow/output/constraints appearing as explicit headings, or at least three plus at least three numbered steps.

## Frequent SkillRouter Headings

Common H2 headings in the full SkillRouter corpus:

| Heading | Count |
|---|---:|
| `overview` | 13568 |
| `best practices` | 10567 |
| `when to use` | 10041 |
| `when to use this skill` | 9642 |
| `related skills` | 6926 |
| `examples` | 6862 |
| `quick reference` | 6723 |
| `workflow` | 6442 |
| `quick start` | 6382 |
| `references` | 6358 |
| `resources` | 6241 |
| `purpose` | 5994 |

Common H2 headings in the scored gold-name subset:

| Heading | Count |
|---|---:|
| `overview` | 240 |
| `best practices` | 139 |
| `quick start` | 114 |
| `dependencies` | 99 |
| `code style guidelines` | 84 |
| `when to use this skill` | 69 |
| `quick reference` | 63 |
| `reading and analyzing content` | 58 |
| `troubleshooting` | 44 |
| `resources` | 43 |

## Prompt-Side Explicitness

| Prompt set | Rows | Mean tokens | Median tokens | P90 tokens | <50 tokens | >=200 tokens | File/path refs | Numbered steps | Explicit input | Explicit output | Mean closest alternatives |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SkillRouter scored tasks | 75 | 198.4 | 169 | 314 | 1.3% | 41.3% | 97.3% | 40.0% | 92.0% | 85.3% | 0 |
| Local controlled prompts | 245 | 36.8 | 25 | 64 | 85.3% | 0.4% | 28.2% | 0.0% | 18.4% | 26.9% | 3.4 |
| Local public-gold prompts | 144 | 30.1 | 29 | 37 | 99.3% | 0.0% | 18.1% | 0.0% | 21.5% | 47.2% | 4.0 |

The SkillRouter prompt median is 169 rough whitespace tokens, and the mean is 198.4. This is paragraph-sized task text rather than a short user request. Many scored tasks include file names, input explanations, explicit steps, and expected outputs.

## Interpretation

- SkillRouter-Eval-Core is not uniformly "rich I3" data: only about 27% of all or scored gold-name skill bodies satisfy the strict rich-schema definition.
- However, the corpus is highly markdown-normalized. H1 headings are present for 95.0% of all rows and 98.5% of scored gold-name rows; procedural signals appear in about 79% of scored gold-name rows.
- Frequent headings such as `overview`, `when to use`, `workflow`, `quick start`, `dependencies`, and `best practices` mean full-body retrieval often searches clean documentation sections, not arbitrary chaotic text.
- SkillRouter scored prompts are much longer and more explicit than local controlled prompts. They include far more file/path cues, input/output cues, and numbered steps.
- The local controlled benchmark is harder in a different way: prompts are shorter, usually single-gold, and intentionally include near-neighbour alternatives.

## Thesis Use

Use this checkpoint as a validity caveat for external SkillRouter-Eval-Core results:

> SkillRouter-Eval-Core is useful as an external portability benchmark, but its skills and prompts differ from the local controlled benchmark. Its skill bodies are often clean markdown documentation with repeated section labels, and its prompts are paragraph-sized task specifications with explicit file/input/output cues. Therefore, external results should be reported as portability evidence rather than merged with the local controlled semantic-confusability results.

This does not invalidate SkillRouter-Eval-Core. It explains why results on this benchmark may favour full-body retrieval or differ from the local thesis benchmark.
