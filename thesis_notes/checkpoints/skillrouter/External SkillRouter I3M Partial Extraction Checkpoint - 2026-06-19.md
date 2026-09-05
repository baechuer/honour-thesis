# External SkillRouter I3M Partial Extraction Checkpoint - 2026-06-19

Purpose: start a model-parsed `I3M` external validation track for the public `pipizhao/SkillRouter-Eval-Core` benchmark, using the same seven-field I3M schema as the local full-library parse.

Status: first 3,000-row external I3M extraction complete for parse coverage. A small QA residue remains for selector-valid strictness, recorded below.

## Context

The local benchmark already has a completed model-parsed I3M representation for all 2,433 local skills. SkillRouter-Eval-Core previously had only:

- `I1`: flat metadata.
- `I2`: full skill artifact.
- `I3H`: heuristic structured extraction.

This checkpoint records the first attempt to create external `I3M` rows from the SkillRouter `I2` artifact file:

- Input: `skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl`
- Target subset: first 3,000 rows.
- Target chunking:
  - rows `0-999`
  - rows `1000-1999`
  - rows `2000-2999`

## Code Changes

Parser updated:

- `skill_benchmark/scripts/model_parse_i3m_skills.py`

New capabilities:

- `--input-jsonl`: parse external JSONL rows containing `text`, `body`, or `artifact`.
- `--family-label`: assign a stable family to external rows.
- `--offset`: select a disjoint row range.
- `--retry-failed`: treat prior `parse_failed` rows as pending and summarize the latest row per skill.
- Evidence-validation change: if an extracted item has evidence that cannot be found in the artifact, the item is dropped and recorded as a QA warning instead of remaining selector-visible.

Rationale for the evidence change:

- The model sometimes merged multiple bullets into one evidence quote.
- Keeping those unsupported items would leak ungrounded model inferences into I3M.
- Dropping unsupported items makes I3M stricter: only artifact-grounded information is selector-visible.

## Subagent Runs

Initial concurrent run:

- Spawned three worker subagents.
- Each worker owned one 1,000-row chunk.
- API concurrency: `10` per worker, about `30` total.
- Outcome: stopped after a quality check because many rows failed under provider/network pressure.

Patched rerun:

- Evidence handling was patched and a 10-row cache-backed check passed:
  - selected rows: `10`
  - valid row rate: `90.0%`
  - evidence exact rate: `99.5%`
  - evidence case-insensitive rate: `100.0%`
- Spawned three new worker subagents with `--force`, still at concurrency `10` per worker.
- Outcome: one chunk completed but had very high parse-failure rate due operational API failures.

Repair run:

- Added `--retry-failed`.
- Spawned three repair subagents with:
  - explicit `--base-url https://api.deepseek.com`
  - `--concurrency 3`
  - `--timeout 120`
  - `--max-retries 1`
  - `--fallback-model deepseek-chat`
- Outcome: stopped manually because the run was slow and old failed rows still dominated the live deduplicated summary.

All spawned subagents were closed after interruption.

## Current Partial Files

Model parse JSONL chunks:

- `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks/external_i3m_chunk_00000_00999_model_parse.jsonl`
- `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks/external_i3m_chunk_01000_01999_model_parse.jsonl`
- `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks/external_i3m_chunk_02000_02999_model_parse.jsonl`

Representation chunks:

- `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks/external_i3m_chunk_00000_00999_representation.jsonl`
- `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks/external_i3m_chunk_01000_01999_representation.jsonl`
- `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks/external_i3m_chunk_02000_02999_representation.jsonl`

## Current Partial Counts

Deduplicated latest-row summary after stopping all workers:

| Chunk | Raw rows | Dedup rows | Latest successful rows | Latest valid rows | Latest parse-failed rows | Rows with warnings | Evidence exact | Evidence case-insensitive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `00000-00999` | 413 | 387 | 160 | 160 | 227 | 95 | 99.6% | 100.0% |
| `01000-01999` | 173 | 172 | 172 | 172 | 0 | 123 | 99.5% | 100.0% |
| `02000-02999` | 1028 | 1000 | 151 | 151 | 849 | 93 | 99.7% | 100.0% |

Interpretation:

- Successful rows are strongly evidence-grounded after the patch.
- The extraction schema itself appears viable.
- The main blocker is operational API reliability under concurrent calls, not the I3M schema.

## Failure Pattern

Dominant failure:

```text
Model parse failed after retries: <urlopen error [Errno 8] nodename nor servname provided, or not known>
```

Secondary failure:

```text
Model parse failed after retries: Expecting ',' delimiter ...
```

Interpretation:

- Most failures are network/provider resolution errors under heavy parallel API pressure.
- A few failures are malformed JSON responses, which should be recoverable with retries or a stricter fallback model.
- This should not be interpreted as evidence against model-parsed I3M.

## Recommended Next Step

Resume repair with much lower total concurrency:

- Use `--retry-failed`.
- Use `--concurrency 1` per chunk, or run one chunk at a time.
- Keep `--base-url https://api.deepseek.com`.
- Keep `--timeout 120`.
- Use `--max-retries 2` or `3`.
- Consider processing smaller subchunks of 100-250 rows if provider instability continues.

Do not report external I3M results until each chunk has:

- `1000` deduplicated rows.
- `0` latest parse-failed rows, or a manually justified residual list.
- evidence case-insensitive rate above `99%`.
- no selector-visible ungrounded evidence items.

## 2026-06-19 Failed-Row Repair Relaunch

The failed/missing rows were relaunched with total script concurrency `2`, one chunk at a time.

Runner:

- `skill_benchmark/scripts/run_skillrouter_i3m_failed_repair_first3000.sh`

Launch method:

- Python `subprocess.Popen(..., start_new_session=True)` from `/Users/jackyzhang/Work/Honour Thesis`.

Live process at launch:

- Parent PID: `64364`
- First parser PID observed: `64368`

Log:

- `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/logs/repair_first3000_concurrency2_2026-06-19.log`

PID file:

- `skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/logs/repair_first3000_concurrency2_2026-06-19.pid`

Command pattern per chunk:

```bash
python3 skill_benchmark/scripts/model_parse_i3m_skills.py \
  --mode full \
  --input-jsonl skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl \
  --family-label skillrouter_eval_core_all_i2 \
  --offset <0|1000|2000> \
  --limit 1000 \
  --base-url https://api.deepseek.com \
  --concurrency 2 \
  --timeout 120 \
  --max-retries 2 \
  --fallback-model deepseek-chat \
  --max-chars 22000 \
  --retry-failed
```

Pre-relaunch status for chunk `00000-00999` after the foreground test:

- raw rows: `440`
- deduplicated rows: `387`
- successful/latest valid rows: `184`
- latest parse-failed rows: `203`

The repair job should be treated as running asynchronously until the log/report files show completion.

## 2026-06-19 Fast Parallel Completion Update

The slow sequential repair job was stopped and replaced with a fast parallel repair pass:

- Runner: `skill_benchmark/scripts/run_skillrouter_i3m_failed_repair_first3000_fast_parallel.sh`
- Per-chunk concurrency: `6`
- Total active chunk workers: `3`
- Primary model: `deepseek-v4-flash`
- Thinking mode: disabled
- Timeout: `45` seconds
- Final strict repair model for residual malformed-JSON rows: `deepseek-chat`
- Strict repair max output tokens: `12000`

Final deduplicated latest-row status:

| Chunk | Raw rows | Dedup rows | Latest valid rows | Latest parse-failed rows |
|---|---:|---:|---:|---:|
| `00000-00999` | 1267 | 1000 | 1000 | 0 |
| `01000-01999` | 1011 | 1000 | 1000 | 0 |
| `02000-02999` | 1883 | 1000 | 997 | 0 |
| **Total** | **4161** | **3000** | **2997** | **0** |

Completion interpretation:

- The first 3,000 SkillRouter-Eval-Core skills now all have a latest model-parse row.
- There are `0` latest parse-failed rows.
- `2997/3000` rows pass the stricter selector-valid check used by the current local summariser.
- The remaining `3` QA residues are not parse failures:
  - `data/help-bitwize-music-studio-claude-ai-music-skil`: unsupported `metadata` item dropped.
  - `data/json-api-mock-generator`: one dependency/resource item lacked exact evidence.
  - `data/klippenstein-journalist`: one dependency/resource item lacked exact evidence.

Do not yet report external benchmark retrieval results from these I3M rows. A coverage check found that the 75 scored SkillRouter tasks use 186 unique gold skills at rows `27018-27213`, while this completed I3M subset covers rows `0-2999`. The next method step is therefore not a direct retrieval ablation from this slice; it is to parse either the task-relevant gold/candidate pool under a fixed candidate universe, or a full tier/library, then compare `I1`, `I2`, `I3H`, `I3M`, and optionally `I3C` under SkillRouter-Eval-Core metrics.
