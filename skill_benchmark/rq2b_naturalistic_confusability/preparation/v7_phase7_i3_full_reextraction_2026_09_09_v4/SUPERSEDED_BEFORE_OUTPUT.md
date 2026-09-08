# Superseded before worker output

State: `SUPERSEDED_BEFORE_ANY_I3V4_OUTPUT`.

The V4 preparation remains immutable and auditable, but no worker output was
written. Before the first batch completed, a prospective false-positive review
found that two lexical gates were too broad:

- a body example containing a legitimate `description:` or benchmark-related
  field name could be rejected even when it described the skill's actual task;
- a positive input condition such as a user who "does not have" something could
  be confused with a negative not-for/route-out boundary.

V4.1 narrows these checks to structurally parsed frontmatter metadata and clear
not-for/use-prohibition language. It preserves the same 3,798 sources, seven
fields, identities, batches, V7 prompts, K=6 packets, labels and QA thresholds.

