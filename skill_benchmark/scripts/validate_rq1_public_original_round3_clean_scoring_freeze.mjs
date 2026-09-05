#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezeRoot = join(root, "round3_clean_only_scoring_freeze");
const freezePath = join(freezeRoot, "clean_only_scoring_freeze_v1.json");
const summaryPath = join(freezeRoot, "freeze_summary.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const freeze = await readJson(freezePath);
const summary = await readJson(summaryPath);
assert(freeze.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_CLEAN_ONLY_SCORING_FREEZE_V1", "Unexpected freeze status.");
assert(summary.status === "PASS_NO_SCORING", "Unexpected summary status.");
assert(freeze.boundary.no_selector_results && freeze.boundary.no_external_transmission, "Freeze boundary must state no scoring and no transmission.");

for (const input of Object.values(freeze.inputs)) {
  if (!input.path || !input.sha256) continue;
  const actual = await digestFile(resolve(repo, input.path));
  assert(actual === input.sha256, `Frozen input hash mismatch: ${input.path}`);
}

const clearance = freeze.inputs.canonical_round3_clearance;
const clearanceRoot = resolve(repo, clearance.path);
const clearanceFiles = (await readdir(clearanceRoot)).filter((name) => /^OR82-\d{3}-.+\.json$/.test(name)).sort();
const aggregate = sha256((await Promise.all(clearanceFiles.map(async (name) => `${name}:${await digestFile(join(clearanceRoot, name))}`))).join("\n"));
assert(clearanceFiles.length === clearance.record_count, "Canonical clearance record count changed.");
assert(aggregate === clearance.aggregate_sha256, "Canonical clearance aggregate hash changed.");

const caseIds = new Set();
const fieldCounts = Object.fromEntries(freeze.fields.map((field) => [field, { cases: 0, prompts: 0 }]));
for (const entry of freeze.cases) {
  assert(!caseIds.has(entry.case_id), `Duplicate case ID ${entry.case_id}.`);
  caseIds.add(entry.case_id);
  assert(freeze.fields.includes(entry.target_field), `${entry.case_id}: invalid target field.`);
  assert([3, 4].includes(entry.candidate_count), `${entry.case_id}: candidate count is not 3 or 4.`);
  assert(entry.candidates.length === entry.candidate_count, `${entry.case_id}: candidate cardinality mismatch.`);
  assert(entry.candidates.some((candidate) => candidate.label === entry.gold_label), `${entry.case_id}: gold label absent.`);
  assert(entry.prompt_variants.length === 2, `${entry.case_id}: expected two prompt variants.`);
  assert(entry.prompt_variants.map((variant) => variant.prompt_variant).join(",") === "direct,paraphrase", `${entry.case_id}: prompt order is not direct,paraphrase.`);
  for (const candidate of entry.candidates) {
    assert(candidate.round3_clearance_status === "CLEAR", `${entry.case_id}/${candidate.label}: non-clear candidate in freeze.`);
    assert(await digestFile(resolve(repo, candidate.full_original.path)) === candidate.full_original.sha256, `${entry.case_id}/${candidate.label}: original hash mismatch.`);
    assert(await digestFile(resolve(repo, candidate.remove_field_r3.path)) === candidate.remove_field_r3.sha256, `${entry.case_id}/${candidate.label}: Round-3 mask hash mismatch.`);
  }
  fieldCounts[entry.target_field].cases += 1;
  fieldCounts[entry.target_field].prompts += 2;
}

assert(freeze.counts.complete_case_composition_family_cases === freeze.cases.length, "Frozen case count differs from declared count.");
assert(freeze.counts.complete_case_prompt_rows === freeze.cases.length * 2, "Frozen prompt count differs from declared count.");
for (const field of freeze.fields) {
  assert(fieldCounts[field].cases === freeze.field_summary[field].eligible_composition_family_cases, `${field}: case count differs from field summary.`);
  assert(fieldCounts[field].prompts === freeze.field_summary[field].eligible_prompt_rows, `${field}: prompt count differs from field summary.`);
}

console.log(JSON.stringify({
  status: "PASS_NO_SCORING",
  frozen_cases: freeze.cases.length,
  frozen_prompt_rows: freeze.cases.length * 2,
  field_counts: fieldCounts,
  all_seven_fields_complete_with_paired_binding: freeze.counts.all_seven_fields_complete_with_paired_binding,
}, null, 2));
