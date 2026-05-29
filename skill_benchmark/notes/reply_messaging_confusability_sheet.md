# Reply Messaging Confusability Sheet

Use this sheet to annotate the first metadata-only nanobot runs for the `reply_messaging` family.

## How to use

1. Run the scripted prompts and keep the raw outputs in `runtime/confusability_results/`.
2. For each row, inspect the corresponding raw output and write:
   - the skill nanobot appeared to select
   - whether it matches the intended gold skill
   - the nearest wrong alternative
   - whether the case feels too easy, nicely confusable, or unstable

## Annotation Table

| Prompt ID | Intended gold | Selected skill | Correct? | Closest wrong alternative | Notes |
|---|---|---|---|---|---|
| `reply_p1_professor_reply` | `professor-email-reply` |  |  |  |  |
| `reply_p2_polish_supervisor` | `reply-polisher` |  |  |  |  |
| `reply_p3_groupwork_coordination` | `groupwork-reply` |  |  |  |  |
| `reply_p4_followup_commitment` | `followup-reply-writer` |  |  |  |  |
| `reply_p5_generic_fresh_draft` | `reply-drafter` |  |  |  |  |

## Repeat Runs

If a prompt feels borderline or unstable, rerun it 3 times and note whether the selected skill changes across runs.
