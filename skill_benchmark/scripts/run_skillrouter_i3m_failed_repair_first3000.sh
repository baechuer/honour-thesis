#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

INPUT="skill_benchmark/external/skillrouter_eval_core/derived/representations/all_I2.jsonl"
OUT_DIR="skill_benchmark/external/skillrouter_eval_core/outputs/i3m_model_parse/chunks"
REP_DIR="skill_benchmark/external/skillrouter_eval_core/derived/representations/i3m_chunks"

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
    --concurrency 2 \
    --timeout 120 \
    --max-retries 2 \
    --fallback-model deepseek-chat \
    --max-chars 22000 \
    --retry-failed
}

run_chunk 0 999
run_chunk 1000 1999
run_chunk 2000 2999
