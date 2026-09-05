# Thesis LaTeX Draft

This folder is the living LaTeX thesis scaffold.

Target length: 30-40 pages.

## Current Structure

- `main.tex`: thesis entry point, now using the supplied 2024 `usydthesis`
  class, template title page, preliminary-matter order, page numbering, and
  chapter/contents formatting.
- `chapters/00_abstract.tex`: abstract.
- `chapters/00_declaration.tex`: academic-integrity declaration placeholder.
- `chapters/00_acknowledgements.tex`: optional acknowledgements placeholder.
- `chapters/01_introduction.tex`: introduction and research questions.
- `chapters/02_literature_review.tex`: literature review adapted from Assignment 3.
- `chapters/03_conceptual_framework.tex`: artifact vs representation vs retrieval policy.
- `chapters/04_benchmark_design.tex`: benchmark design and validation.
- `chapters/05_methodology.tex`: methods, representations, retrievers, metrics.
- `chapters/06_results.tex`: current and placeholder results.
- `chapters/07_discussion.tex`: interpretation and failure modes.
- `chapters/08_conclusion.tex`: conclusion placeholder.
- `chapters/appendix_a_benchmark_rubric.tex`: benchmark rubric placeholder.
- `chapters/appendix_b_prompt_examples.tex`: prompt examples placeholder.
- Bibliography: currently uses `../references.bib` from the project root.

## Page Budget

Suggested final page allocation for a 30-40 page thesis:

- Abstract: 1 page.
- Introduction: 4-5 pages.
- Literature Review: 8-10 pages.
- Conceptual Framework: 3-4 pages.
- Benchmark Design: 4-5 pages.
- Methodology: 5-6 pages.
- Results: 5-7 pages.
- Discussion: 4-5 pages.
- Conclusion: 1-2 pages.
- Appendices: outside the main 30-40 pages if allowed.

The public USYD pages I checked do not state a strict public page count for this exact thesis. Treat the 30-40 page target as the working target from your unit/supervisor materials unless Canvas says otherwise.

## USYD Alignment Notes

## Template Alignment

The supplied `thesis_2024_latex.zip` has been used as a formatting reference.
Its `usydthesis` class and supporting style assets are vendored locally in
`usydthesis.cls` and `style/`. The thesis keeps its existing research chapters,
bibliography database, and current content; template sample prose and the
historical declaration wording were not imported as thesis claims.

Official public pages checked:

- INFO4990 unit page: https://www.sydney.edu.au/units/INFO4990
- Computer Science Honours table: https://www.sydney.edu.au/handbooks/science/table-a/subject-areas/computer-science/honours-unit-of-study-table.html
- Related CS project unit page: https://www.sydney.edu.au/units/INFO4914

Implications for this scaffold:

- Include a literature review, research plan, methodology, evaluation, ethics/copyright awareness, and clear communication of research contribution.
- Keep the thesis written in an academic CS style, with explicit research questions, method, results, failure analysis, and limitations.
- Preserve placeholders for ethics/declaration and downstream validation until exact Canvas/supervisor requirements are known.

## Current Framing

RQ1: Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

RQ2: How do skill representation and retrieval-pipeline choices affect the preservation and use of the routing-relevant operational information identified in RQ1 under semantic confusability, and what accuracy, candidate-recall, and retrieval-cost trade-offs result?

Current framing note, 2026-08-02: RQ1a's seven field-isolation suites are reviewed and complete. RQ2a development, immutable freeze, 280-cluster confirmatory matrix, paired statistics, cost ledger, failure analysis, user review, and thesis integration are complete. The final result rejects a universal field-heading advantage under Qwen single-vector selection while supporting a narrower representation-retrieval compatibility claim. RQ2b is an unreviewed draft. Historical I1/I2/I3, M6, and external SkillRouter results are retained separately as exploratory or portability evidence; graph/tree/DAG and downstream execution remain outside the active implementation.

## Compile

From this folder:

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If `latexmk` is available:

```sh
latexmk -pdf main.tex
```
