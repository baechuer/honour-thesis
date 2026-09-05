#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

INPUT="skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl"
OUT_DIR="skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks"
REP_DIR="skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks"
LOG_DIR="skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/logs"

mkdir -p "$OUT_DIR" "$REP_DIR" "$LOG_DIR"

PER_CHUNK_CONCURRENCY="${I3M_PER_CHUNK_CONCURRENCY:-6}"
TIMEOUT="${I3M_TIMEOUT:-45}"
MAX_RETRIES="${I3M_MAX_RETRIES:-1}"
MAX_CHARS="${I3M_MAX_CHARS:-22000}"
MAX_OUTPUT_TOKENS="${I3M_MAX_OUTPUT_TOKENS:-5000}"

run_chunk() {
  local start="$1"
  local end="$2"
  local label
  label="$(printf "%05d_%05d" "$start" "$end")"

  python3 skill_benchmark/scripts/model_parse_i3m_skills.py \
    --mode full \
    --input-jsonl "$INPUT" \
    --family-label skillrouter_eval_core_all_i2 \
    --offset "$start" \
    --limit 1000 \
    --output-jsonl "$OUT_DIR/external_i3m_chunk_${label}_model_parse.jsonl" \
    --representation-jsonl "$REP_DIR/external_i3m_chunk_${label}_representation.jsonl" \
    --report-md "$OUT_DIR/external_i3m_chunk_${label}_report.md" \
    --base-url https://api.deepseek.com \
    --model deepseek-v4-flash \
    --thinking disabled \
    --concurrency "$PER_CHUNK_CONCURRENCY" \
    --timeout "$TIMEOUT" \
    --max-retries "$MAX_RETRIES" \
    --fallback-model deepseek-v4-flash \
    --max-chars "$MAX_CHARS" \
    --max-output-tokens "$MAX_OUTPUT_TOKENS" \
    --retry-failed \
    > "$LOG_DIR/fast_parallel_chunk_${label}_2026-06-19.log" 2>&1
}

run_chunk 0 999 &
pid0=$!
run_chunk 1000 1999 &
pid1=$!
run_chunk 2000 2999 &
pid2=$!

echo "$pid0 $pid1 $pid2" > "$LOG_DIR/fast_parallel_first3000_child_pids_2026-06-19.pid"

wait "$pid0"
wait "$pid1"
wait "$pid2"
