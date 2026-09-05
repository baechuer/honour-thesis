#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const bm25Path = join(root, "round3_clean_only_bm25_results", "analysis", "bm25_paired_analysis.json");
const qwenPath = join(root, "round3_clean_only_qwen_results", "analysis", "qwen_paired_analysis.json");
const outputRoot = join(root, "round3_clean_only_twin_synthesis");

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

function snapshot(field) {
  const primary = field.combined_primary;
  return {
    eligible_compositions: field.eligible_compositions,
    eligible_routing_families: field.eligible_routing_families,
    full_hit_at_1: primary.full_hit_at_1,
    removed_hit_at_1: primary.removed_hit_at_1,
    hit_at_1_delta: primary.hit_at_1_delta,
    hit_at_1_delta_direction: direction(primary.hit_at_1_delta),
    mrr_delta: primary.mrr_delta,
    mrr_delta_direction: direction(primary.mrr_delta),
    native_margin_delta: primary.margin_delta,
    gold_rank_worsening: primary.gold_rank_worsening,
    winner_changed: primary.winner_changed,
    full_correct_to_removed_wrong: primary.full_correct_removed_wrong,
    full_wrong_to_removed_correct: primary.full_wrong_removed_correct,
    prompt_row_transitions: field.prompt_row_transition_counts,
  };
}

const [bm25, qwen] = await Promise.all([readJson(bm25Path), readJson(qwenPath)]);
assert(bm25.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_BM25_PAIRED_ANALYSIS_COMPLETE", "Unexpected BM25 analysis status.");
assert(qwen.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_PAIRED_ANALYSIS_COMPLETE", "Unexpected Qwen analysis status.");
assert(JSON.stringify(Object.keys(bm25.fields)) === JSON.stringify(Object.keys(qwen.fields)), "Twin analyses have different fields.");

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite existing synthesis root: ${outputRoot}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const fieldResults = {};
const support = {
  stable_positive_in_both: [],
  stable_positive_bm25_only: [],
  stable_positive_qwen_only: [],
  neither_stably_positive: [],
};

for (const field of Object.keys(bm25.fields)) {
  const bm25Snapshot = snapshot(bm25.fields[field]);
  const qwenSnapshot = snapshot(qwen.fields[field]);
  fieldResults[field] = { bm25: bm25Snapshot, qwen_text_embedding_v4_1024: qwenSnapshot };
  const bm25Positive = bm25Snapshot.hit_at_1_delta_direction === "STABLE_POSITIVE";
  const qwenPositive = qwenSnapshot.hit_at_1_delta_direction === "STABLE_POSITIVE";
  if (bm25Positive && qwenPositive) support.stable_positive_in_both.push(field);
  else if (bm25Positive) support.stable_positive_bm25_only.push(field);
  else if (qwenPositive) support.stable_positive_qwen_only.push(field);
  else support.neither_stably_positive.push(field);
}

const synthesis = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_TWIN_SYNTHESIS_COMPLETE",
  boundary: {
    bm25_analysis_sha256: await digestFile(bm25Path),
    qwen_analysis_sha256: await digestFile(qwenPath),
    common_freeze_sha256: bm25.boundary.freeze_sha256,
    primary_comparison: "Within retriever and within target field: full original public skill document versus the matched original document with only the target information field removed.",
    retrievers: ["local_bm25", "qwen_text_embedding_v4_1024"],
    excluded_methods: ["query rewrite", "reranker", "cross-retriever raw-score comparison", "cross-field pooled effect"],
  },
  statistical_plan: {
    primary_unit: "composition",
    within_family_aggregation: "mean of direct and paraphrase paired observations",
    within_composition_aggregation: "equal-weight mean over eligible routing families",
    uncertainty: "10,000 seeded composition-clustered paired bootstrap resamples, inherited from the frozen per-retriever analyses",
    effect_rule: "A field is labelled stable positive for a retriever only where the 95% bootstrap CI for Full minus Removed Hit@1 is entirely above zero.",
  },
  support_by_hit_at_1: support,
  field_results: fieldResults,
  failure_analysis_guide: {
    full_correct_to_removed_wrong: "The prompt was correctly routed with the original document and incorrectly routed after removing the target field. This is the clearest observed selection failure consistent with loss of that field, but does not prove the field was the only information used.",
    full_wrong_to_removed_correct: "The original document was misrouted but the removal condition selected the gold skill. These countervailing cases prevent interpreting every removal as harmful and are retained rather than discarded.",
    native_margin_delta: "Original gold-versus-leading-negative score margin minus removed-document margin. It is a within-retriever diagnostic only: BM25 and cosine-margin magnitudes are not comparable to one another.",
    scope: "The experiment tests the routing value lost when a named field is removed from genuine public skill documents. It does not establish that public skills isolate fields cleanly, that every field is causal in every document, or generalise beyond this curated strict-gold public composition set.",
  },
};

await mkdir(outputRoot, { recursive: true });
const synthesisPath = join(outputRoot, "twin_synthesis.json");
await writeFile(synthesisPath, `${JSON.stringify(synthesis, null, 2)}\n`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${await digestFile(synthesisPath)}  twin_synthesis.json\n`);

console.log(JSON.stringify({
  status: synthesis.status,
  support_by_hit_at_1: synthesis.support_by_hit_at_1,
  output: outputRoot,
}, null, 2));
