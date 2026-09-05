#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezeRoot = join(root, "round3_clean_only_joint_group_freeze");
const freezePath = join(freezeRoot, "joint_group_scoring_freeze_v1.json");
const defaultOutputRoot = join(root, "round3_clean_only_joint_group_bm25_results");
const argumentsSet = new Set(process.argv.slice(2));
const dryRun = argumentsSet.has("--dry-run");
const selfTest = argumentsSet.has("--self-test");
const requestedOutput = process.argv.find((argument) => argument.startsWith("--output="));
const outputRoot = requestedOutput ? resolve(requestedOutput.slice("--output=".length)) : defaultOutputRoot;

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function tokenise(text) {
  return text
    .normalize("NFKC")
    .toLowerCase()
    .match(/[a-z0-9]+/g) ?? [];
}

function buildBm25(documents) {
  const documentCount = documents.length;
  const termFrequencies = documents.map((document) => {
    const frequencies = new Map();
    for (const token of tokenise(document.text)) frequencies.set(token, (frequencies.get(token) ?? 0) + 1);
    return frequencies;
  });
  const lengths = termFrequencies.map((frequencies) => [...frequencies.values()].reduce((sum, count) => sum + count, 0));
  const averageLength = lengths.reduce((sum, length) => sum + length, 0) / documentCount;
  const documentFrequency = new Map();
  for (const frequencies of termFrequencies) {
    for (const token of frequencies.keys()) documentFrequency.set(token, (documentFrequency.get(token) ?? 0) + 1);
  }
  return { documentCount, termFrequencies, lengths, averageLength, documentFrequency };
}

function scoreBm25(index, documentIndex, queryTokens, k1 = 1.5, b = 0.75) {
  const frequencies = index.termFrequencies[documentIndex];
  let score = 0;
  for (const token of queryTokens) {
    const frequency = frequencies.get(token) ?? 0;
    if (frequency === 0) continue;
    const frequencyAcrossDocuments = index.documentFrequency.get(token) ?? 0;
    const idf = Math.log(1 + (index.documentCount - frequencyAcrossDocuments + 0.5) / (frequencyAcrossDocuments + 0.5));
    const denominator = frequency + k1 * (1 - b + b * (index.lengths[documentIndex] / index.averageLength));
    score += idf * ((frequency * (k1 + 1)) / denominator);
  }
  return score;
}

function rankDocuments(candidates, prompt) {
  const index = buildBm25(candidates);
  const queryTokens = tokenise(prompt);
  const scored = candidates.map((candidate, documentIndex) => ({
    label: candidate.label,
    score: scoreBm25(index, documentIndex, queryTokens),
    document_tokens: index.lengths[documentIndex],
  }));
  scored.sort((left, right) => right.score - left.score || left.label.localeCompare(right.label));
  return scored.map((candidate, indexPosition) => ({ ...candidate, rank: indexPosition + 1 }));
}

function toResultRow(caseRow, promptVariant, condition, candidateTexts) {
  const ranking = rankDocuments(candidateTexts, promptVariant.prompt);
  const gold = ranking.find((candidate) => candidate.label === caseRow.gold_label);
  assert(gold, `${caseRow.case_id}: gold label absent from ranking.`);
  const leadingNegative = ranking.find((candidate) => candidate.label !== caseRow.gold_label);
  return {
    row_id: sha256(`${caseRow.case_id}\u0000${promptVariant.prompt_variant}\u0000${condition}`),
    case_id: caseRow.case_id,
    composition_id: caseRow.composition_id,
    source_composition_id: caseRow.source_composition_id,
    group: caseRow.group,
    component_fields: caseRow.component_fields,
    routing_family_id: caseRow.routing_family_id,
    proposal_id: caseRow.proposal_id,
    strict_gold_skill_id: caseRow.strict_gold_skill_id,
    gold_label: caseRow.gold_label,
    prompt_variant: promptVariant.prompt_variant,
    prompt_sha256: sha256(promptVariant.prompt),
    condition,
    candidate_count: caseRow.candidate_count,
    tokenisation: "NFKC_lowercase_ascii_alnum",
    bm25: { k1: 1.5, b: 0.75 },
    ranking,
    winner_label: ranking[0].label,
    gold_rank: gold.rank,
    hit_at_1: gold.rank === 1 ? 1 : 0,
    reciprocal_rank: 1 / gold.rank,
    gold_native_score: gold.score,
    leading_negative_native_score: leadingNegative.score,
    native_margin: gold.score - leadingNegative.score,
  };
}

function runSelfTest() {
  const sample = rankDocuments([
    { label: "candidate_b", text: "alpha beta" },
    { label: "candidate_a", text: "alpha beta" },
    { label: "candidate_c", text: "gamma delta" },
  ], "alpha");
  assert(sample.map((entry) => entry.label).join(",") === "candidate_a,candidate_b,candidate_c", "Tie-break self-test failed.");
  const unique = rankDocuments([
    { label: "candidate_a", text: "convert PDF input to JSON" },
    { label: "candidate_b", text: "edit spreadsheet formulas" },
  ], "convert a PDF to JSON");
  assert(unique[0].label === "candidate_a", "Lexical ranking self-test failed.");
  return { status: "SELF_TEST_PASS", tie_break: "label_ascending", tokeniser: "NFKC_lowercase_ascii_alnum" };
}

if (selfTest) {
  console.log(JSON.stringify(runSelfTest(), null, 2));
  process.exit(0);
}

const freeze = await readJson(freezePath);
assert(freeze.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_SCORING_FREEZE_V1", "Unexpected frozen input status.");
assert(freeze.boundary.no_selector_results && freeze.boundary.no_external_transmission, "Frozen input does not declare a no-scoring boundary.");
assert(freeze.cases.length === 369, `Expected 369 frozen group cases, found ${freeze.cases.length}.`);
const plannedRows = freeze.cases.length * 2 * 2;

if (dryRun) {
  console.log(JSON.stringify({
    status: "DRY_RUN_PASS_NO_SCORING",
    freeze_path: "skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_joint_group_freeze/joint_group_scoring_freeze_v1.json",
    frozen_cases: freeze.cases.length,
    conditions_per_case: 2,
    prompt_variants_per_case: 2,
    planned_ranking_rows: plannedRows,
    group_case_counts: Object.fromEntries(Object.keys(freeze.groups).map((group) => [group, freeze.cases.filter((entry) => entry.group === group).length])),
    no_result_output_written: true,
  }, null, 2));
  process.exit(0);
}

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite BM25 result root: ${outputRoot}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const rows = [];
async function loadCandidate(candidate, condition) {
  const descriptor = condition === "FULL_ORIGINAL" ? candidate.full_original : candidate.remove_group_r3;
  const bytes = await readFile(resolve(repo, descriptor.path));
  assert(sha256(bytes) === descriptor.sha256, `${candidate.label}: ${condition} hash mismatch.`);
  return { label: candidate.label, text: bytes.toString("utf8") };
}

for (const caseRow of freeze.cases) {
  for (const promptVariant of caseRow.prompt_variants) {
    const fullCandidates = await Promise.all(caseRow.candidates.map((candidate) => loadCandidate(candidate, "FULL_ORIGINAL")));
    const removedCandidates = await Promise.all(caseRow.candidates.map((candidate) => loadCandidate(candidate, "REMOVE_GROUP_R3")));
    rows.push(toResultRow(caseRow, promptVariant, "FULL_ORIGINAL", fullCandidates));
    rows.push(toResultRow(caseRow, promptVariant, caseRow.group_condition, removedCandidates));
  }
}
assert(rows.length === plannedRows, `Expected ${plannedRows} ranking rows, wrote ${rows.length}.`);
assert(new Set(rows.map((row) => row.row_id)).size === rows.length, "Duplicate result row IDs.");

const perGroup = Object.fromEntries(Object.keys(freeze.groups).map((group) => [group, {}]));
for (const group of Object.keys(freeze.groups)) {
  for (const condition of ["FULL_ORIGINAL", `REMOVE_${group.toUpperCase()}_R3`]) {
    const subset = rows.filter((row) => row.group === group && row.condition === condition);
    perGroup[group][condition] = {
      rows: subset.length,
      hit_at_1: subset.reduce((sum, row) => sum + row.hit_at_1, 0) / subset.length,
      mrr: subset.reduce((sum, row) => sum + row.reciprocal_rank, 0) / subset.length,
    };
  }
}

const results = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_BM25_COMPLETE",
  boundary: {
    freeze_sha256: await digestFile(freezePath),
    retriever: "local_bm25",
    no_external_transmission: true,
    no_query_rewrite: true,
    no_reranker: true,
  },
  configuration: { tokenisation: "NFKC_lowercase_ascii_alnum", k1: 1.5, b: 0.75 },
  counts: { frozen_cases: freeze.cases.length, ranking_rows: rows.length },
  raw_prompt_row_descriptive_summary_not_primary: perGroup,
  rows,
};

await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "bm25_results.json"), `${JSON.stringify(results, null, 2)}\n`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${await digestFile(join(outputRoot, "bm25_results.json"))}  bm25_results.json\n`);
console.log(JSON.stringify({ status: results.status, counts: results.counts, output: outputRoot }, null, 2));
