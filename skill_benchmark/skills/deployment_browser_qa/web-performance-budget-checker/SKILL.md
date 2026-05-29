---
name: web-performance-budget-checker
description: "Evaluates a web page against performance budgets using load metrics, bundle clues, trace evidence, network weight, and user-impact prioritization."
---

# Web Performance Budget Checker

Checks whether a page meets speed and budget expectations.

## Use when

- The user asks about load time, performance budget, bundle size, Core Web Vitals, or trace evidence.
- The task requires performance diagnosis rather than functional interaction debugging.
- The output should prioritize performance fixes by user impact.

## Not for

- Visual screenshot regression comparison.
- Deployment smoke verification.
- Accessibility interaction auditing.

## Preconditions

- A target page, performance report, trace, or network evidence is available.
- Budget thresholds or performance goals are stated or can be proposed.
- The user wants diagnosis or prioritization, not a broad UI review.

## Workflow

1. Identify target pages, devices, and performance budgets.
2. Review load metrics, bundle size, blocking resources, images, and network waterfalls.
3. Separate lab data, field data, and configuration assumptions.
4. Prioritize bottlenecks by user impact and implementation effort.
5. Return concrete performance checks and fixes.

## Writing rules

- Do not claim field performance from lab-only evidence.
- Attach findings to a metric or trace clue.
- Avoid generic optimization advice without evidence.

## Default shape

- Metric or budget
- Observed issue
- Evidence
- Priority fix
