# External SkillRouter I3C V2 Remaining I1/I3C Grouped Neural Matrix HF Job Launch - 2026-06-21

## Purpose

Rerun the remaining corrected `I1/I3C` neural matrix in a safer grouped layout after job `6a37bdd33093dba73ce2b559` failed on Hub upload.

## Execution Venue

| Field | Value |
|---|---|
| Venue | Hugging Face Jobs |
| Account | `baechuer1` |
| Job ID | `6a37c2b63093dba73ce2b58d` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a37c2b63093dba73ce2b58d` |
| Hardware | `l4x1` |
| Timeout | `8h` |
| Required secret | `HF_TOKEN` |
| Quiet progress | disabled |

## Group Order

1. `easy_I3C` with modes `embedding,rerank`
2. `hard_I1` with modes `embedding,rerank`
3. `hard_I3C` with modes `embedding,rerank`

The two Easy/I1 rows remain recovered from cancelled job `6a3773a1953ed90bfb9469b7`.

`FULL` remains excluded and should be run separately as the expensive full-document baseline.

## Persistence Policy

The job attempts Hub uploads with `create_pr=True`, because direct commits to the dataset repo failed. Upload failures are non-fatal; the job should continue and print all condition metrics to logs.
