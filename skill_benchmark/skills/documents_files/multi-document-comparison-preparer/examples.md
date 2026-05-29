# Multi-Document Comparison Preparer Examples

## Example 1

User ask:

`Prepare these two contract excerpts so I can compare the payment and termination clauses.`

Example output:

- Comparison dimensions: payment terms, notice period, termination trigger
- Document A
  - Payment terms: Net 14 days
  - Notice period: 30 days
  - Termination trigger: material breach
- Document B
  - Payment terms: Net 30 days
  - Notice period: 14 days
  - Termination trigger: material breach or insolvency
- Differences or gaps
  - Document B has a broader termination condition
  - Document A requires faster payment

## Example 2

User ask:

`Line these two policy drafts up so I can compare what changed.`

Example output:

- Comparison dimensions: submission deadline, approval path, reimbursement cap
- Draft A
  - Submission deadline: five working days
  - Approval path: manager then finance
  - Reimbursement cap: AUD 1,500
- Draft B
  - Submission deadline: three working days
  - Approval path: manager only for low-cost items
  - Reimbursement cap: AUD 2,000
- Differences or gaps
  - Draft B shortens lead time and loosens low-cost approval
  - Draft B raises the reimbursement cap
