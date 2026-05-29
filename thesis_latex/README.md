# Thesis LaTeX Draft

This folder is the living LaTeX thesis scaffold.

Target length: 30-40 pages.

## Current Structure

- `main.tex`: thesis entry point.
- `chapters/00_abstract.tex`: abstract.
- `chapters/00_declaration.tex`: declaration and acknowledgements placeholders.
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

Official public pages checked:

- INFO4990 unit page: https://www.sydney.edu.au/units/INFO4990
- Computer Science Honours table: https://www.sydney.edu.au/handbooks/science/table-a/subject-areas/computer-science/honours-unit-of-study-table.html
- Related CS project unit page: https://www.sydney.edu.au/units/INFO4914

Implications for this scaffold:

- Include a literature review, research plan, methodology, evaluation, ethics/copyright awareness, and clear communication of research contribution.
- Keep the thesis written in an academic CS style, with explicit research questions, method, results, failure analysis, and limitations.
- Preserve placeholders for ethics/declaration and downstream validation until exact Canvas/supervisor requirements are known.

## Current Framing

RQ1: What information must agent skill representations preserve to distinguish semantically similar but procedurally distinct skills at scale?

RQ2: How do retrieval strategies that use flat text, dense embeddings, structured procedural fields, or hybrid reranking differ in accuracy, efficiency, and failure modes when applied to scalable skill libraries?

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
