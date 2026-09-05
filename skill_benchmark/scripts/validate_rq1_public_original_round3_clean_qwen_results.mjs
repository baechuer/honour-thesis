#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezeRoot = join(root, "round3_clean_only_scoring_freeze");
const resultRoot = join(root, "round3_clean_only_qwen_results");
const freezePath = join(freezeRoot, "clean_only_scoring_freeze_v1.json");
const preflightPath = join(root, "round3_clean_only_qwen_preflight", "payload.json");
const resultPath = join(resultRoot, "qwen_results.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const [freeze, preflight, results] = await Promise.all([readJson(freezePath), readJson(preflightPath), readJson(resultPath)]);
assert(results.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_COMPLETE", "Unexpected result status.");
assert(results.boundary.payload_sha256 === await digestFile(preflightPath), "Result payload hash does not match the frozen preflight.");
assert(results.boundary.model === "text-embedding-v4" && results.boundary.dimensions === 1024, "Unexpected Qwen embedding configuration.");
assert(results.boundary.endpoint === "https://dashscope-intl.aliyuncs.com/compatible-mode/v1", "Unexpected Qwen endpoint.");
assert(results.boundary.no_query_rewrite && results.boundary.no_reranker && results.boundary.automatic_retries === 0, "Result boundary drift.");
assert(results.counts.frozen_cases === freeze.cases.length, "Frozen case count mismatch.");
assert(results.counts.ranking_rows === freeze.cases.length * 4, "Frozen ranking row count mismatch.");
assert(results.execution.cache_misses === preflight.counts.new_texts_total.texts, "Unexpected cache-miss count.");
assert(results.execution.request_attempts <= preflight.counts.maximum_request_attempts_no_retry, "Request-attempt ceiling exceeded.");
assert(results.execution.successful_calls <= preflight.counts.maximum_successful_calls_no_retry, "Successful-call ceiling exceeded.");

const caseById = new Map(freeze.cases.map((entry) => [entry.case_id, entry]));
const expectedRows = freeze.cases.length * 4;
assert(results.rows.length === expectedRows, `Expected ${expectedRows} rows, found ${results.rows.length}.`);
const seenRows = new Set();
const seenConditionKeys = new Set();
const fieldRows = Object.fromEntries(freeze.fields.map((field) => [field, 0]));
for (const row of results.rows) {
  assert(!seenRows.has(row.row_id), `Duplicate result row ID ${row.row_id}.`);
  seenRows.add(row.row_id);
  const frozen = caseById.get(row.case_id);
  assert(frozen, `${row.row_id}: case is absent from freeze.`);
  assert(row.target_field === frozen.target_field, `${row.row_id}: field mismatch.`);
  assert(row.composition_id === frozen.composition_id, `${row.row_id}: composition mismatch.`);
  assert(row.routing_family_id === frozen.routing_family_id, `${row.row_id}: routing family mismatch.`);
  assert(row.gold_label === frozen.gold_label, `${row.row_id}: gold label mismatch.`);
  assert(["direct", "paraphrase"].includes(row.prompt_variant), `${row.row_id}: invalid prompt variant.`);
  const expectedCondition = `REMOVE_${row.target_field.toUpperCase()}_R3`;
  assert(["FULL_ORIGINAL", expectedCondition].includes(row.condition), `${row.row_id}: invalid condition.`);
  const conditionKey = `${row.case_id}\u0000${row.prompt_variant}\u0000${row.condition}`;
  assert(!seenConditionKeys.has(conditionKey), `Duplicate condition row ${conditionKey}.`);
  seenConditionKeys.add(conditionKey);
  assert(row.candidate_count === frozen.candidate_count && row.ranking.length === frozen.candidate_count, `${row.row_id}: candidate cardinality mismatch.`);
  const frozenLabels = frozen.candidates.map((candidate) => candidate.label).sort();
  const rankedLabels = row.ranking.map((candidate) => candidate.label).sort();
  assert(JSON.stringify(frozenLabels) === JSON.stringify(rankedLabels), `${row.row_id}: candidate labels mismatch.`);
  assert(row.ranking.map((candidate) => candidate.rank).join(",") === Array.from({ length: frozen.candidate_count }, (_, index) => index + 1).join(","), `${row.row_id}: non-consecutive ranks.`);
  assert(row.winner_label === row.ranking[0].label, `${row.row_id}: winner mismatch.`);
  const gold = row.ranking.find((candidate) => candidate.label === row.gold_label);
  assert(gold?.rank === row.gold_rank, `${row.row_id}: gold rank mismatch.`);
  assert(row.hit_at_1 === (row.gold_rank === 1 ? 1 : 0), `${row.row_id}: Hit@1 mismatch.`);
  assert(row.reciprocal_rank === 1 / row.gold_rank, `${row.row_id}: reciprocal rank mismatch.`);
  fieldRows[row.target_field] += 1;
}

for (const frozen of freeze.cases) {
  for (const variant of ["direct", "paraphrase"]) {
    for (const condition of ["FULL_ORIGINAL", `REMOVE_${frozen.target_field.toUpperCase()}_R3`]) {
      assert(seenConditionKeys.has(`${frozen.case_id}\u0000${variant}\u0000${condition}`), `${frozen.case_id}: missing ${variant}/${condition} result.`);
    }
  }
}

console.log(JSON.stringify({
  status: "PASS",
  result_sha256: await digestFile(resultPath),
  preflight_payload_sha256: await digestFile(preflightPath),
  freeze_cases: freeze.cases.length,
  expected_rows: expectedRows,
  validated_rows: results.rows.length,
  field_rows: fieldRows,
  all_pairs_complete: true,
  qwen_embedding_configuration: "DashScope international text-embedding-v4, 1024 dimensions, no retry",
}, null, 2));
