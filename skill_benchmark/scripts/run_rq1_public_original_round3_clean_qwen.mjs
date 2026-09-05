#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, rename, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const preflightRoot = join(root, "round3_clean_only_qwen_preflight");
const payloadPath = join(preflightRoot, "payload.json");
const authorisationPath = join(preflightRoot, "authorisation.json");
const outputRoot = join(root, "round3_clean_only_qwen_results");
const defaultDotenv = resolve(".env");
const dotenvArgument = process.argv.find((argument) => argument.startsWith("--dotenv="));
const dotenvPath = dotenvArgument ? resolve(dotenvArgument.slice("--dotenv=".length)) : defaultDotenv;
const cacheRoot = resolve("skill_benchmark/cache/rq1_public_original_round3_qwen_text_embedding_v4_1024");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function loadDotenv(contents) {
  for (const rawLine of contents.split("\n")) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const separator = line.indexOf("=");
    const key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim().replace(/^['"]|['"]$/g, "");
    if (!process.env[key]) process.env[key] = value;
  }
}

function chunks(rows, size) {
  return Array.from({ length: Math.ceil(rows.length / size) }, (_, index) => rows.slice(index * size, (index + 1) * size));
}

function l2Normalise(vector) {
  const norm = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0));
  assert(Number.isFinite(norm) && norm > 0, "Invalid embedding norm.");
  return vector.map((value) => value / norm);
}

function cosine(left, right) {
  const normalisedLeft = l2Normalise(left);
  const normalisedRight = l2Normalise(right);
  return normalisedLeft.reduce((sum, value, index) => sum + value * normalisedRight[index], 0);
}

async function cacheLoad(textId, payload) {
  const path = join(cacheRoot, `${textId}.json`);
  try {
    const entry = await readJson(path);
    assert(entry.schema_version === payload.inputs.cache_schema, `${path}: cache schema mismatch.`);
    assert(entry.endpoint === payload.boundary.endpoint && entry.model === payload.boundary.model && entry.dimensions === payload.boundary.dimensions, `${path}: cache model binding mismatch.`);
    assert(entry.text_id === textId && entry.text_sha256 === textId, `${path}: cache text binding mismatch.`);
    assert(Array.isArray(entry.embedding) && entry.embedding.length === payload.boundary.dimensions && entry.embedding.every(Number.isFinite), `${path}: invalid cached vector.`);
    return entry.embedding;
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

async function cacheStore(text, vector, payload, receipt) {
  await mkdir(cacheRoot, { recursive: true });
  const target = join(cacheRoot, `${text.text_id}.json`);
  try {
    await stat(target);
    throw new Error(`Cache entry already exists: ${target}`);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  const entry = {
    schema_version: payload.inputs.cache_schema,
    endpoint: payload.boundary.endpoint,
    model: payload.boundary.model,
    dimensions: payload.boundary.dimensions,
    text_id: text.text_id,
    text_sha256: text.text_id,
    local_lexical_token_proxy: text.local_lexical_token_proxy,
    provider_usage: receipt.provider_usage ?? {},
    embedding: vector,
  };
  const temporary = join(cacheRoot, `.${text.text_id}.tmp`);
  await writeFile(temporary, `${JSON.stringify(entry)}\n`);
  await rename(temporary, target);
}

function rankCase(caseRow, promptVariant, condition, documentMap, queryMap) {
  const query = queryMap.get(`${caseRow.case_id}\u0000${promptVariant.prompt_variant}`);
  assert(query, `${caseRow.case_id}/${promptVariant.prompt_variant}: missing query embedding.`);
  const ranking = caseRow.candidates.map((candidate) => {
    const vector = documentMap.get(`${caseRow.case_id}\u0000${condition}\u0000${candidate.label}`);
    assert(vector, `${caseRow.case_id}/${condition}/${candidate.label}: missing document embedding.`);
    return { label: candidate.label, score: cosine(query, vector) };
  }).sort((left, right) => right.score - left.score || left.label.localeCompare(right.label)).map((entry, index) => ({ ...entry, rank: index + 1 }));
  const gold = ranking.find((entry) => entry.label === caseRow.gold_label);
  const leadingNegative = ranking.find((entry) => entry.label !== caseRow.gold_label);
  return {
    row_id: sha256(`${caseRow.case_id}\u0000${promptVariant.prompt_variant}\u0000${condition}`),
    case_id: caseRow.case_id,
    composition_id: caseRow.composition_id,
    source_composition_id: caseRow.source_composition_id,
    target_field: caseRow.target_field,
    routing_family_id: caseRow.routing_family_id,
    proposal_id: caseRow.proposal_id,
    strict_gold_skill_id: caseRow.strict_gold_skill_id,
    gold_label: caseRow.gold_label,
    prompt_variant: promptVariant.prompt_variant,
    prompt_sha256: sha256(promptVariant.prompt),
    condition,
    candidate_count: caseRow.candidate_count,
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

const [payload, authorisation] = await Promise.all([readJson(payloadPath), readJson(authorisationPath)]);
const payloadSha256 = await digestFile(payloadPath);
assert(payload.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_PREFLIGHT_LOCAL_ONLY_NOT_EXECUTED", "Unexpected payload status.");
assert(authorisation.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_ONE_RUN_AUTHORISED", "External execution lacks local authorisation receipt.");
assert(authorisation.payload_sha256 === payloadSha256, "Authorisation payload hash mismatch.");
assert(authorisation.endpoint === payload.boundary.endpoint && authorisation.model === payload.boundary.model && authorisation.dimensions === payload.boundary.dimensions, "Authorisation model binding mismatch.");
assert(authorisation.maximum_new_texts >= payload.counts.new_texts_total.texts, "Authorisation new-text ceiling too low.");
assert(authorisation.maximum_request_attempts >= payload.counts.maximum_request_attempts_no_retry && authorisation.maximum_successful_calls >= payload.counts.maximum_successful_calls_no_retry, "Authorisation call ceiling too low.");
assert(authorisation.automatic_retries === 0, "Automatic retry is prohibited.");
try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite Qwen result root: ${outputRoot}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
loadDotenv(await readFile(dotenvPath, "utf8"));
const apiKey = process.env.DASHSCOPE_API_KEY;
assert(apiKey, "DASHSCOPE_API_KEY is unavailable in the configured dotenv or environment.");

const vectors = new Map();
const missingDocuments = [];
const missingQueries = [];
for (const text of payload.text_inventory) {
  const cached = await cacheLoad(text.text_id, payload);
  if (cached) vectors.set(text.text_id, cached);
  else if (text.roles.some((role) => role.kind === "document")) missingDocuments.push(text);
  else if (text.roles.some((role) => role.kind === "query")) missingQueries.push(text);
  else throw new Error(`${text.text_id}: text has no recognised role.`);
}
assert(missingDocuments.length + missingQueries.length <= authorisation.maximum_new_texts, "Cache miss count exceeds authorisation ceiling.");
const requests = [
  ...chunks(missingDocuments, payload.boundary.maximum_batch_texts).map((rows) => ({ role: "document", rows })),
  ...chunks(missingQueries, payload.boundary.maximum_batch_texts).map((rows) => ({ role: "query", rows })),
];
assert(requests.length <= authorisation.maximum_request_attempts && requests.length <= authorisation.maximum_successful_calls, "Request count exceeds authorisation ceiling.");
await mkdir(join(outputRoot, "requests"), { recursive: true });
let attempts = 0;
let successfulCalls = 0;
const providerUsage = {};
for (const requestPlan of requests) {
  attempts += 1;
  const attempt = { attempt: attempts, role: requestPlan.role, text_ids: requestPlan.rows.map((row) => row.text_id), text_count: requestPlan.rows.length, automatic_retry: false };
  await writeFile(join(outputRoot, "requests", `request_${String(attempts).padStart(4, "0")}_attempt.json`), `${JSON.stringify(attempt, null, 2)}\n`);
  const started = performance.now();
  let response;
  try {
    response = await fetch(`${payload.boundary.endpoint}/embeddings`, {
      method: "POST",
      headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: payload.boundary.model, input: requestPlan.rows.map((row) => row.text), dimensions: payload.boundary.dimensions, encoding_format: "float" }),
    });
  } catch (error) {
    await writeFile(join(outputRoot, "requests", `request_${String(attempts).padStart(4, "0")}_failure.json`), `${JSON.stringify({ ...attempt, state: "FAILED_STOP_NO_RETRY", error_type: error.name, error: error.message }, null, 2)}\n`);
    throw new Error(`Qwen request ${attempts} failed before a response; no retry was attempted.`);
  }
  if (!response.ok) {
    const body = await response.text();
    await writeFile(join(outputRoot, "requests", `request_${String(attempts).padStart(4, "0")}_failure.json`), `${JSON.stringify({ ...attempt, state: "FAILED_STOP_NO_RETRY", http_status: response.status, response_preview: body.slice(0, 500) }, null, 2)}\n`);
    throw new Error(`Qwen request ${attempts} returned HTTP ${response.status}; no retry was attempted.`);
  }
  const body = await response.json();
  const data = body.data;
  assert(Array.isArray(data) && data.length === requestPlan.rows.length, `Qwen request ${attempts}: response length mismatch.`);
  const ordered = [...data].sort((left, right) => Number(left.index) - Number(right.index));
  assert(ordered.every((item, index) => Number(item.index) === index), `Qwen request ${attempts}: response index mismatch.`);
  const receipt = { ...attempt, state: "SUCCESS", request_seconds: (performance.now() - started) / 1000, provider_usage: body.usage ?? {} };
  await writeFile(join(outputRoot, "requests", `request_${String(attempts).padStart(4, "0")}_receipt.json`), `${JSON.stringify(receipt, null, 2)}\n`);
  successfulCalls += 1;
  for (const [key, value] of Object.entries(receipt.provider_usage)) if (Number.isFinite(value)) providerUsage[key] = (providerUsage[key] ?? 0) + value;
  for (const [text, item] of requestPlan.rows.map((row, index) => [row, ordered[index]])) {
    const embedding = item.embedding;
    assert(Array.isArray(embedding) && embedding.length === payload.boundary.dimensions && embedding.every(Number.isFinite), `Qwen request ${attempts}: invalid embedding.`);
    await cacheStore(text, embedding, payload, receipt);
    vectors.set(text.text_id, embedding);
  }
  console.log(`QWEN_PROGRESS request=${attempts}/${requests.length} role=${requestPlan.role} texts=${requestPlan.rows.length} cache_written=${requestPlan.rows.length}`);
}

assert(vectors.size === payload.text_inventory.length, "Embedding inventory is incomplete after execution.");
const documentTextIdByKey = new Map(payload.documents.map((entry) => [`${entry.case_id}\u0000${entry.condition}\u0000${entry.candidate_label}`, entry.text_id]));
const queryTextIdByKey = new Map(payload.queries.map((entry) => [`${entry.case_id}\u0000${entry.prompt_variant}`, entry.text_id]));
const documentMap = new Map([...documentTextIdByKey.entries()].map(([key, textId]) => [key, vectors.get(textId)]));
const queryMap = new Map([...queryTextIdByKey.entries()].map(([key, textId]) => [key, vectors.get(textId)]));
const freeze = await readJson(resolve(repo, payload.inputs.freeze.path));
const rows = [];
for (const caseRow of freeze.cases) {
  for (const promptVariant of caseRow.prompt_variants) {
    rows.push(rankCase(caseRow, promptVariant, "FULL_ORIGINAL", documentMap, queryMap));
    rows.push(rankCase(caseRow, promptVariant, `REMOVE_${caseRow.target_field.toUpperCase()}_R3`, documentMap, queryMap));
  }
}
assert(rows.length === payload.counts.expected_dense_ranking_rows, "Dense ranking row count mismatch.");
assert(new Set(rows.map((row) => row.row_id)).size === rows.length, "Duplicate dense ranking row IDs.");
const result = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_COMPLETE",
  boundary: {
    payload_sha256: payloadSha256,
    endpoint: payload.boundary.endpoint,
    model: payload.boundary.model,
    dimensions: payload.boundary.dimensions,
    no_query_rewrite: true,
    no_reranker: true,
    automatic_retries: 0,
  },
  execution: { cache_hits: payload.text_inventory.length - requests.reduce((sum, request) => sum + request.rows.length, 0), cache_misses: requests.reduce((sum, request) => sum + request.rows.length, 0), request_attempts: attempts, successful_calls: successfulCalls, provider_usage: providerUsage },
  counts: { frozen_cases: freeze.cases.length, ranking_rows: rows.length },
  rows,
};
await writeFile(join(outputRoot, "qwen_results.json"), `${JSON.stringify(result, null, 2)}\n`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${await digestFile(join(outputRoot, "qwen_results.json"))}  qwen_results.json\n`);
console.log(JSON.stringify({ status: result.status, counts: result.counts, execution: result.execution, output: outputRoot }, null, 2));
