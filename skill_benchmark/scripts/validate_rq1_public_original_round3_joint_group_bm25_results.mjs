#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezeRoot = join(root, "round3_clean_only_joint_group_freeze");
const resultRoot = join(root, "round3_clean_only_joint_group_bm25_results");
const freezePath = join(freezeRoot, "joint_group_scoring_freeze_v1.json");
const resultPath = join(resultRoot, "bm25_results.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const [freeze, results] = await Promise.all([readJson(freezePath), readJson(resultPath)]);
assert(results.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_BM25_COMPLETE", "Unexpected result status.");
assert(results.boundary.freeze_sha256 === await digestFile(freezePath), "Result freeze hash does not match current freeze.");
assert(results.boundary.retriever === "local_bm25", "Unexpected retriever.");
assert(results.boundary.no_external_transmission && results.boundary.no_query_rewrite && results.boundary.no_reranker, "Result boundary drift.");

const caseById = new Map(freeze.cases.map((entry) => [entry.case_id, entry]));
const expectedRows = freeze.cases.length * 4;
assert(results.rows.length === expectedRows, `Expected ${expectedRows} rows, found ${results.rows.length}.`);
const seenRows = new Set();
const seenConditionKeys = new Set();
const groupRows = Object.fromEntries(Object.keys(freeze.groups).map((group) => [group, 0]));
for (const row of results.rows) {
  assert(!seenRows.has(row.row_id), `Duplicate result row ID ${row.row_id}.`);
  seenRows.add(row.row_id);
  const frozen = caseById.get(row.case_id);
  assert(frozen, `${row.row_id}: case is absent from freeze.`);
  assert(row.group === frozen.group, `${row.row_id}: group mismatch.`);
  assert(row.composition_id === frozen.composition_id, `${row.row_id}: composition mismatch.`);
  assert(row.routing_family_id === frozen.routing_family_id, `${row.row_id}: routing family mismatch.`);
  assert(row.gold_label === frozen.gold_label, `${row.row_id}: gold label mismatch.`);
  assert(["direct", "paraphrase"].includes(row.prompt_variant), `${row.row_id}: invalid prompt variant.`);
  const expectedCondition = frozen.group_condition;
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
  groupRows[row.group] += 1;
}

for (const frozen of freeze.cases) {
  for (const variant of ["direct", "paraphrase"]) {
    for (const condition of ["FULL_ORIGINAL", frozen.group_condition]) {
      assert(seenConditionKeys.has(`${frozen.case_id}\u0000${variant}\u0000${condition}`), `${frozen.case_id}: missing ${variant}/${condition} result.`);
    }
  }
}

console.log(JSON.stringify({
  status: "PASS",
  result_sha256: await digestFile(resultPath),
  freeze_cases: freeze.cases.length,
  expected_rows: expectedRows,
  validated_rows: results.rows.length,
  group_rows: groupRows,
  all_pairs_complete: true,
  no_external_transmission: true,
}, null, 2));
