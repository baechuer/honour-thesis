#!/usr/bin/env node

import { readdir, readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(await readFile(join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"));
const canonicalRoot = join(root, "full_clearance", "canonical_round1");
let names = [];
try { names = (await readdir(canonicalRoot)).filter((name) => name.endsWith(".json")); } catch (error) { if (error.code !== "ENOENT") throw error; }
const canonical = [];
for (const name of names) canonical.push(JSON.parse(await readFile(join(canonicalRoot, name), "utf8")));
const expectedFields = new Map();
for (const unit of manifest.single_units) expectedFields.set(unit.unit_id, unit.target_field);
const byField = Object.fromEntries([...new Set(manifest.single_units.map((unit) => unit.target_field))].sort().map((field) => [field, { reviewed_units: 0, clear_units: 0, residual_candidates: 0, uncertain_candidates: 0 }]));
let reviewedCandidates = 0;
let clearCandidates = 0;
let residualCandidates = 0;
let uncertainCandidates = 0;
for (const review of canonical) {
  const row = byField[review.target_field];
  if (!row) throw new Error(`${review.unit_id}: unknown field`);
  row.reviewed_units += 1;
  let unitClear = true;
  for (const candidate of review.candidates) {
    reviewedCandidates += 1;
    if (candidate.status === "CLEAR") { clearCandidates += 1; continue; }
    unitClear = false;
    if (candidate.status === "RESIDUAL") { residualCandidates += 1; row.residual_candidates += 1; }
    if (candidate.status === "UNCERTAIN") { uncertainCandidates += 1; row.uncertain_candidates += 1; }
  }
  if (unitClear) { row.clear_units += 1; }
}
const completed = new Set(canonical.map((review) => review.unit_id));
const output = {
  status: completed.size === manifest.single_unit_count ? "FULL_CLEARANCE_ROUND1_COMPLETE" : "FULL_CLEARANCE_ROUND1_IN_PROGRESS",
  expected_units: manifest.single_unit_count,
  reviewed_units: completed.size,
  missing_unit_count: manifest.single_units.filter((unit) => !completed.has(unit.unit_id)).length,
  next_missing_units: manifest.single_units.filter((unit) => !completed.has(unit.unit_id)).slice(0, 12).map((unit) => unit.unit_id),
  reviewed_candidates: reviewedCandidates,
  clear_candidates: clearCandidates,
  residual_candidates: residualCandidates,
  uncertain_candidates: uncertainCandidates,
  by_field: byField,
};
console.log(JSON.stringify(output));
