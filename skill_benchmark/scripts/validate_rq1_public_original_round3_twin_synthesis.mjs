#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const bm25Path = join(root, "round3_clean_only_bm25_results", "analysis", "bm25_paired_analysis.json");
const qwenPath = join(root, "round3_clean_only_qwen_results", "analysis", "qwen_paired_analysis.json");
const synthesisPath = join(root, "round3_clean_only_twin_synthesis", "twin_synthesis.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function direction(metric) {
  if (metric.ci95[0] > 0) return "STABLE_POSITIVE";
  if (metric.ci95[1] < 0) return "STABLE_NEGATIVE";
  return "INDETERMINATE";
}

const [bm25, qwen, synthesis] = await Promise.all([readJson(bm25Path), readJson(qwenPath), readJson(synthesisPath)]);
assert(synthesis.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_TWIN_SYNTHESIS_COMPLETE", "Unexpected synthesis status.");
assert(synthesis.boundary.bm25_analysis_sha256 === await digestFile(bm25Path), "BM25 analysis hash mismatch.");
assert(synthesis.boundary.qwen_analysis_sha256 === await digestFile(qwenPath), "Qwen analysis hash mismatch.");
assert(synthesis.boundary.common_freeze_sha256 === bm25.boundary.freeze_sha256 && bm25.boundary.freeze_sha256 === qwen.boundary.freeze_sha256, "Twin freeze mismatch.");

const expectedSupport = { stable_positive_in_both: [], stable_positive_bm25_only: [], stable_positive_qwen_only: [], neither_stably_positive: [] };
for (const field of Object.keys(bm25.fields)) {
  const fieldResult = synthesis.field_results[field];
  assert(fieldResult, `Missing synthesis field ${field}.`);
  const bm25Delta = bm25.fields[field].combined_primary.hit_at_1_delta;
  const qwenDelta = qwen.fields[field].combined_primary.hit_at_1_delta;
  assert(fieldResult.bm25.hit_at_1_delta.estimate === bm25Delta.estimate, `${field}: BM25 delta mismatch.`);
  assert(fieldResult.qwen_text_embedding_v4_1024.hit_at_1_delta.estimate === qwenDelta.estimate, `${field}: Qwen delta mismatch.`);
  const bm25Positive = direction(bm25Delta) === "STABLE_POSITIVE";
  const qwenPositive = direction(qwenDelta) === "STABLE_POSITIVE";
  if (bm25Positive && qwenPositive) expectedSupport.stable_positive_in_both.push(field);
  else if (bm25Positive) expectedSupport.stable_positive_bm25_only.push(field);
  else if (qwenPositive) expectedSupport.stable_positive_qwen_only.push(field);
  else expectedSupport.neither_stably_positive.push(field);
}
assert(JSON.stringify(synthesis.support_by_hit_at_1) === JSON.stringify(expectedSupport), "Support classification mismatch.");
console.log(JSON.stringify({ status: "PASS", fields: Object.keys(synthesis.field_results).length, support_by_hit_at_1: expectedSupport }, null, 2));
