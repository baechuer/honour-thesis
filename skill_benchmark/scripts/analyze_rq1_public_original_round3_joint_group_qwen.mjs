#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezePath = join(root, "round3_clean_only_joint_group_freeze", "joint_group_scoring_freeze_v1.json");
const preflightPath = join(root, "round3_clean_only_joint_group_qwen_preflight", "payload.json");
const resultsRoot = join(root, "round3_clean_only_joint_group_qwen_results");
const resultsPath = join(resultsRoot, "qwen_results.json");
const outputRoot = join(resultsRoot, "analysis");
const bootstrapResamples = 10_000;
const seed = 20260904;

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function quantile(sortedValues, probability) {
  const position = (sortedValues.length - 1) * probability;
  const lower = Math.floor(position);
  const upper = Math.ceil(position);
  if (lower === upper) return sortedValues[lower];
  return sortedValues[lower] + (sortedValues[upper] - sortedValues[lower]) * (position - lower);
}

function mulberry32(value) {
  let state = value >>> 0;
  return () => {
    state += 0x6D2B79F5;
    let output = state;
    output = Math.imul(output ^ (output >>> 15), output | 1);
    output ^= output + Math.imul(output ^ (output >>> 7), output | 61);
    return ((output ^ (output >>> 14)) >>> 0) / 4294967296;
  };
}

function bootstrapMean(values, localSeed) {
  const rng = mulberry32(localSeed);
  const estimates = [];
  for (let iteration = 0; iteration < bootstrapResamples; iteration += 1) {
    let sum = 0;
    for (let index = 0; index < values.length; index += 1) sum += values[Math.floor(rng() * values.length)];
    estimates.push(sum / values.length);
  }
  estimates.sort((left, right) => left - right);
  return { estimate: mean(values), ci95: [quantile(estimates, 0.025), quantile(estimates, 0.975)] };
}

function pairedObservation(full, removed) {
  return {
    full_hit_at_1: full.hit_at_1,
    removed_hit_at_1: removed.hit_at_1,
    hit_at_1_delta: full.hit_at_1 - removed.hit_at_1,
    full_mrr: full.reciprocal_rank,
    removed_mrr: removed.reciprocal_rank,
    mrr_delta: full.reciprocal_rank - removed.reciprocal_rank,
    full_gold_rank: full.gold_rank,
    removed_gold_rank: removed.gold_rank,
    gold_rank_worsening: removed.gold_rank - full.gold_rank,
    full_margin: full.native_margin,
    removed_margin: removed.native_margin,
    margin_delta: full.native_margin - removed.native_margin,
    full_correct_removed_wrong: full.hit_at_1 === 1 && removed.hit_at_1 === 0 ? 1 : 0,
    full_wrong_removed_correct: full.hit_at_1 === 0 && removed.hit_at_1 === 1 ? 1 : 0,
    winner_changed: full.winner_label !== removed.winner_label ? 1 : 0,
  };
}

function averageObservations(observations) {
  const metricNames = Object.keys(observations[0]);
  return Object.fromEntries(metricNames.map((metric) => [metric, mean(observations.map((observation) => observation[metric]))]));
}

function summarizeCompositionObservations(compositionObservations, localSeed) {
  const metrics = [
    "full_hit_at_1",
    "removed_hit_at_1",
    "hit_at_1_delta",
    "full_mrr",
    "removed_mrr",
    "mrr_delta",
    "full_gold_rank",
    "removed_gold_rank",
    "gold_rank_worsening",
    "full_margin",
    "removed_margin",
    "margin_delta",
    "full_correct_removed_wrong",
    "full_wrong_removed_correct",
    "winner_changed",
  ];
  return Object.fromEntries(metrics.map((metric, index) => [metric, bootstrapMean(compositionObservations.map((entry) => entry[metric]), localSeed + index * 10_003)]));
}

const [freeze, results] = await Promise.all([readJson(freezePath), readJson(resultsPath)]);
assert(results.boundary.payload_sha256 === await digestFile(preflightPath), "Result does not bind to the frozen Qwen payload.");
assert(results.rows.length === freeze.cases.length * 4, "Unexpected Qwen row count.");

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite existing analysis root: ${outputRoot}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const rowByKey = new Map();
for (const row of results.rows) {
  const key = `${row.case_id}\u0000${row.prompt_variant}\u0000${row.condition}`;
  assert(!rowByKey.has(key), `Duplicate result key ${key}.`);
  rowByKey.set(key, row);
}

const outputGroups = {};
for (const group of Object.keys(freeze.groups)) {
  const groupCases = freeze.cases.filter((caseRow) => caseRow.group === group);
  const familiesByComposition = new Map();
  const transitions = [];
  for (const caseRow of groupCases) {
    const variantObservations = {};
    for (const variant of ["direct", "paraphrase"]) {
      const full = rowByKey.get(`${caseRow.case_id}\u0000${variant}\u0000FULL_ORIGINAL`);
      const removed = rowByKey.get(`${caseRow.case_id}\u0000${variant}\u0000${caseRow.group_condition}`);
      assert(full && removed, `${caseRow.case_id}/${variant}: incomplete paired result.`);
      variantObservations[variant] = pairedObservation(full, removed);
      if (variantObservations[variant].full_correct_removed_wrong || variantObservations[variant].full_wrong_removed_correct) {
        transitions.push({
          case_id: caseRow.case_id,
          composition_id: caseRow.composition_id,
          routing_family_id: caseRow.routing_family_id,
          prompt_variant: variant,
          gold_label: caseRow.gold_label,
          transition: variantObservations[variant].full_correct_removed_wrong ? "FULL_CORRECT_TO_REMOVED_WRONG" : "FULL_WRONG_TO_REMOVED_CORRECT",
          full_winner: full.winner_label,
          removed_winner: removed.winner_label,
          full_gold_rank: full.gold_rank,
          removed_gold_rank: removed.gold_rank,
          full_margin: full.native_margin,
          removed_margin: removed.native_margin,
        });
      }
    }
    const familyObservation = averageObservations(Object.values(variantObservations));
    const families = familiesByComposition.get(caseRow.composition_id) ?? [];
    families.push({
      routing_family_id: caseRow.routing_family_id,
      combined: familyObservation,
      direct: variantObservations.direct,
      paraphrase: variantObservations.paraphrase,
    });
    familiesByComposition.set(caseRow.composition_id, families);
  }
  const compositionObservations = [...familiesByComposition.entries()].map(([compositionId, families]) => ({
    composition_id: compositionId,
    family_count: families.length,
    combined: averageObservations(families.map((family) => family.combined)),
    direct: averageObservations(families.map((family) => family.direct)),
    paraphrase: averageObservations(families.map((family) => family.paraphrase)),
  }));
  const groupIndex = Object.keys(freeze.groups).indexOf(group);
  const combined = summarizeCompositionObservations(compositionObservations.map((entry) => entry.combined), seed + groupIndex * 100_000);
  const direct = summarizeCompositionObservations(compositionObservations.map((entry) => entry.direct), seed + groupIndex * 100_000 + 1);
  const paraphrase = summarizeCompositionObservations(compositionObservations.map((entry) => entry.paraphrase), seed + groupIndex * 100_000 + 2);
  const sortedTransitions = transitions.sort((left, right) => left.composition_id.localeCompare(right.composition_id) || left.routing_family_id.localeCompare(right.routing_family_id) || left.prompt_variant.localeCompare(right.prompt_variant));
  outputGroups[group] = {
    primary_unit: "equal_weight_composition_after_within_family_prompt_average_and_within_composition_family_average",
    eligible_compositions: compositionObservations.length,
    component_fields: freeze.groups[group],
    eligible_routing_families: groupCases.length,
    repeated_prompt_rows: groupCases.length * 2,
    combined_primary: combined,
    direct_slice: direct,
    paraphrase_slice: paraphrase,
    prompt_row_transition_counts: {
      full_correct_to_removed_wrong: transitions.filter((entry) => entry.transition === "FULL_CORRECT_TO_REMOVED_WRONG").length,
      full_wrong_to_removed_correct: transitions.filter((entry) => entry.transition === "FULL_WRONG_TO_REMOVED_CORRECT").length,
      examples: sortedTransitions.slice(0, 12),
    },
    composition_family_counts: compositionObservations.map((entry) => ({ composition_id: entry.composition_id, family_count: entry.family_count })),
  };
}

const analysis = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_QWEN_PAIRED_ANALYSIS_COMPLETE",
  boundary: {
    freeze_sha256: await digestFile(freezePath),
    preflight_payload_sha256: await digestFile(preflightPath),
    qwen_result_sha256: await digestFile(resultsPath),
    retriever: "qwen_text_embedding_v4_1024",
    endpoint: results.boundary.endpoint,
    model: results.boundary.model,
    dimensions: results.boundary.dimensions,
    external_embedding_execution: true,
    no_query_rewrite: true,
    no_reranker: true,
    scope: "Group-specific, derived-clear complete-case, full-original versus Round-3 group-removal paired analysis.",
  },
  statistical_plan: {
    primary_unit: "composition",
    within_family_aggregation: "mean of direct and paraphrase paired observations",
    within_composition_aggregation: "equal-weight mean over eligible routing families",
    uncertainty: "10,000 seeded composition-clustered paired bootstrap resamples",
    bootstrap_seed: seed,
    warning: "Prompt-row numbers are repeated measures and are descriptive only; no cross-group pooled effect is calculated.",
  },
  groups: outputGroups,
};

await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "qwen_paired_analysis.json"), `${JSON.stringify(analysis, null, 2)}\n`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${await digestFile(join(outputRoot, "qwen_paired_analysis.json"))}  qwen_paired_analysis.json\n`);

const concise = Object.fromEntries(Object.entries(outputGroups).map(([group, result]) => [group, {
  eligible_compositions: result.eligible_compositions,
  hit_at_1_full: result.combined_primary.full_hit_at_1,
  hit_at_1_removed: result.combined_primary.removed_hit_at_1,
  hit_at_1_delta: result.combined_primary.hit_at_1_delta,
  mrr_delta: result.combined_primary.mrr_delta,
  full_correct_to_removed_wrong_prompt_rows: result.prompt_row_transition_counts.full_correct_to_removed_wrong,
  full_wrong_to_removed_correct_prompt_rows: result.prompt_row_transition_counts.full_wrong_to_removed_correct,
}]));
console.log(JSON.stringify({ status: analysis.status, concise }, null, 2));
