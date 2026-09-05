# External SkillRouter I3C V2 Remaining I1/I3C Neural Matrix Upload Failure - 2026-06-21

## Failed Job

| Field | Value |
|---|---|
| Job ID | `6a37bdd33093dba73ce2b559` |
| Job URL | `https://huggingface.co/jobs/baechuer1/6a37bdd33093dba73ce2b559` |
| Final status | `ERROR` |
| Failure point | Hub upload after `easy_I3C_embedding` |

The job completed the first grouped target condition but failed when trying to commit the condition JSON to the dataset repo. The Hugging Face API returned:

`403 Forbidden: pass create_pr=1 as a query parameter to create a Pull Request`

## Recovered Log Row

| Condition | Hit@1 | MRR@10 | Recall@20 | FullCov@20 | Query total ms |
|---|---:|---:|---:|---:|---:|
| `easy_I3C_embedding` | 45.3% | 0.525 | 55.1% | 37.3% | 3246.4 |

The local JSON/MD artifact from this failed job is not recoverable because the HF job container is ephemeral and the upload failed.

## Replacement Run

Replacement job `6a37c2b63093dba73ce2b58d` was launched with these changes:

- groups embedding and rerank in one subprocess per tier/layer, so rerank can reuse the embedding cache;
- uses `create_pr=True` for Hub upload attempts;
- treats upload failures as non-fatal so the job can continue and emit all metrics to logs;
- keeps quiet progress disabled.
