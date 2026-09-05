#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezePath = join(root, "round3_clean_only_scoring_freeze", "clean_only_scoring_freeze_v1.json");
const resultsPath = join(root, "round3_clean_only_qwen_results", "qwen_results.json");
const analysisPath = join(root, "round3_clean_only_qwen_results", "analysis", "qwen_paired_analysis.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

const [freeze, results, analysis] = await Promise.all([readJson(freezePath), readJson(resultsPath), readJson(analysisPath)]);
assert(analysis.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_PAIRED_ANALYSIS_COMPLETE", "Unexpected analysis status.");
assert(analysis.boundary.freeze_sha256 === await digestFile(freezePath), "Analysis freeze hash mismatch.");
assert(analysis.boundary.qwen_result_sha256 === await digestFile(resultsPath), "Analysis result hash mismatch.");
assert(analysis.statistical_plan.primary_unit === "composition", "Analysis must use composition as primary unit.");
assert(analysis.statistical_plan.bootstrap_seed === 20260904, "Unexpected bootstrap seed.");

const rowByKey = new Map(results.rows.map((row) => [`${row.case_id}\u0000${row.prompt_variant}\u0000${row.condition}`, row]));
const checked = {};
for (const field of freeze.fields) {
  const cases = freeze.cases.filter((entry) => entry.target_field === field);
  const observationsByComposition = new Map();
  for (const caseRow of cases) {
    const familyValues = [];
    for (const variant of ["direct", "paraphrase"]) {
      const full = rowByKey.get(`${caseRow.case_id}\u0000${variant}\u0000FULL_ORIGINAL`);
      const removed = rowByKey.get(`${caseRow.case_id}\u0000${variant}\u0000REMOVE_${field.toUpperCase()}_R3`);
      assert(full && removed, `${caseRow.case_id}/${variant}: missing paired row.`);
      familyValues.push({
        full_hit: full.hit_at_1,
        removed_hit: removed.hit_at_1,
        hit_delta: full.hit_at_1 - removed.hit_at_1,
        mrr_delta: full.reciprocal_rank - removed.reciprocal_rank,
      });
    }
    const family = {
      full_hit: mean(familyValues.map((value) => value.full_hit)),
      removed_hit: mean(familyValues.map((value) => value.removed_hit)),
      hit_delta: mean(familyValues.map((value) => value.hit_delta)),
      mrr_delta: mean(familyValues.map((value) => value.mrr_delta)),
    };
    const families = observationsByComposition.get(caseRow.composition_id) ?? [];
    families.push(family);
    observationsByComposition.set(caseRow.composition_id, families);
  }
  const compositionValues = [...observationsByComposition.values()].map((families) => ({
    full_hit: mean(families.map((value) => value.full_hit)),
    removed_hit: mean(families.map((value) => value.removed_hit)),
    hit_delta: mean(families.map((value) => value.hit_delta)),
    mrr_delta: mean(families.map((value) => value.mrr_delta)),
  }));
  const reported = analysis.fields[field];
  assert(reported.eligible_compositions === compositionValues.length, `${field}: composition count mismatch.`);
  assert(reported.eligible_routing_families === cases.length, `${field}: family count mismatch.`);
  const values = {
    full_hit: mean(compositionValues.map((value) => value.full_hit)),
    removed_hit: mean(compositionValues.map((value) => value.removed_hit)),
    hit_delta: mean(compositionValues.map((value) => value.hit_delta)),
    mrr_delta: mean(compositionValues.map((value) => value.mrr_delta)),
  };
  const tolerance = 1e-12;
  assert(Math.abs(values.full_hit - reported.combined_primary.full_hit_at_1.estimate) < tolerance, `${field}: full Hit@1 estimate mismatch.`);
  assert(Math.abs(values.removed_hit - reported.combined_primary.removed_hit_at_1.estimate) < tolerance, `${field}: removed Hit@1 estimate mismatch.`);
  assert(Math.abs(values.hit_delta - reported.combined_primary.hit_at_1_delta.estimate) < tolerance, `${field}: Hit@1 delta mismatch.`);
  assert(Math.abs(values.mrr_delta - reported.combined_primary.mrr_delta.estimate) < tolerance, `${field}: MRR delta mismatch.`);
  for (const metric of Object.values(reported.combined_primary)) {
    assert(metric.ci95[0] <= metric.ci95[1], `${field}: invalid confidence interval ordering.`);
  }
  checked[field] = { eligible_compositions: compositionValues.length, hit_at_1_delta: values.hit_delta, mrr_delta: values.mrr_delta };
}

console.log(JSON.stringify({ status: "PASS", checked, no_cross_field_pooling: true }, null, 2));
