#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezeRoot = join(root, "round3_clean_only_joint_group_freeze");
const freezePath = join(freezeRoot, "joint_group_scoring_freeze_v1.json");
const outputRoot = join(root, "round3_clean_only_joint_group_qwen_preflight");
const cacheRoot = resolve("skill_benchmark/cache/rq1_public_original_round3_qwen_text_embedding_v4_1024");
const endpoint = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1";
const model = "text-embedding-v4";
const dimensions = 1024;
const maximumBatchTexts = 10;
const cacheSchema = "RQ1_PUBLIC_ORIGINAL_R3_QWEN_EMBEDDING_CACHE_V1";

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const digestFile = async (path) => sha256(await readFile(path));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function tokenProxy(text) {
  return text.normalize("NFKC").toLowerCase().match(/[a-z0-9]+/g)?.length ?? 0;
}

function countTotals(rows) {
  return {
    texts: rows.length,
    utf8_bytes: rows.reduce((sum, row) => sum + row.utf8_bytes, 0),
    local_lexical_token_proxy: rows.reduce((sum, row) => sum + row.local_lexical_token_proxy, 0),
  };
}

async function validCache(textId) {
  const path = join(cacheRoot, `${textId}.json`);
  try {
    const entry = await readJson(path);
    assert(entry.schema_version === cacheSchema, `${path}: unexpected cache schema.`);
    assert(entry.endpoint === endpoint && entry.model === model && entry.dimensions === dimensions, `${path}: cache model binding mismatch.`);
    assert(entry.text_id === textId && entry.text_sha256 === textId, `${path}: text hash mismatch.`);
    assert(Array.isArray(entry.embedding) && entry.embedding.length === dimensions, `${path}: invalid embedding length.`);
    assert(entry.embedding.every((value) => Number.isFinite(value)), `${path}: non-finite embedding.`);
    return { valid: true, path: relativePath(path) };
  } catch (error) {
    if (error.code === "ENOENT") return { valid: false };
    throw error;
  }
}

function relativePath(path) {
  return path.startsWith(`${repo}/`) ? path.slice(repo.length + 1) : path;
}

const freeze = await readJson(freezePath);
assert(freeze.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_SCORING_FREEZE_V1", "Unexpected frozen input status.");
assert(freeze.boundary.no_selector_results && freeze.boundary.no_external_transmission, "Freeze boundary does not permit a Qwen preflight.");
try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite preflight root: ${relativePath(outputRoot)}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const inventory = new Map();
const documents = [];
const queries = [];
function registerText(text, role) {
  const textId = sha256(Buffer.from(text, "utf8"));
  const existing = inventory.get(textId);
  if (existing) {
    assert(existing.text === text, `SHA-256 collision for ${textId}.`);
    existing.roles.push(role);
  } else {
    inventory.set(textId, {
      text_id: textId,
      text_sha256: textId,
      text,
      utf8_bytes: Buffer.byteLength(text, "utf8"),
      local_lexical_token_proxy: tokenProxy(text),
      roles: [role],
    });
  }
  return textId;
}

for (const caseRow of freeze.cases) {
  for (const candidate of caseRow.candidates) {
    for (const [condition, descriptor] of Object.entries({
      FULL_ORIGINAL: candidate.full_original,
      [caseRow.group_condition]: candidate.remove_group_r3,
    })) {
      const absolutePath = resolve(repo, descriptor.path);
      const bytes = await readFile(absolutePath);
      assert(sha256(bytes) === descriptor.sha256, `${caseRow.case_id}/${candidate.label}/${condition}: frozen file hash mismatch.`);
      const textId = registerText(bytes.toString("utf8"), {
        kind: "document",
        case_id: caseRow.case_id,
        composition_id: caseRow.composition_id,
        group: caseRow.group,
        condition,
        candidate_label: candidate.label,
      });
      documents.push({
        case_id: caseRow.case_id,
        composition_id: caseRow.composition_id,
        group: caseRow.group,
        component_fields: caseRow.component_fields,
        condition,
        candidate_label: candidate.label,
        text_id: textId,
      });
    }
  }
  for (const promptVariant of caseRow.prompt_variants) {
    const textId = registerText(promptVariant.prompt, {
      kind: "query",
      case_id: caseRow.case_id,
      composition_id: caseRow.composition_id,
      group: caseRow.group,
      routing_family_id: caseRow.routing_family_id,
      prompt_variant: promptVariant.prompt_variant,
    });
    queries.push({
      case_id: caseRow.case_id,
      composition_id: caseRow.composition_id,
      group: caseRow.group,
      routing_family_id: caseRow.routing_family_id,
      prompt_variant: promptVariant.prompt_variant,
      text_id: textId,
    });
  }
}

const textInventory = [...inventory.values()].sort((left, right) => left.text_id.localeCompare(right.text_id));
const documentIds = new Set(documents.map((row) => row.text_id));
const queryIds = new Set(queries.map((row) => row.text_id));
const cacheStates = new Map(await Promise.all(textInventory.map(async (entry) => [entry.text_id, await validCache(entry.text_id)])));
const cached = textInventory.filter((entry) => cacheStates.get(entry.text_id).valid);
const missing = textInventory.filter((entry) => !cacheStates.get(entry.text_id).valid);
const missingDocuments = missing.filter((entry) => documentIds.has(entry.text_id));
const missingQueries = missing.filter((entry) => queryIds.has(entry.text_id));
const cachedDocuments = cached.filter((entry) => documentIds.has(entry.text_id));
const cachedQueries = cached.filter((entry) => queryIds.has(entry.text_id));
const callCeiling = Math.ceil(missingDocuments.length / maximumBatchTexts) + Math.ceil(missingQueries.length / maximumBatchTexts);

const payload = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_QWEN_PREFLIGHT_LOCAL_ONLY_NOT_EXECUTED",
  frozen_on: "2026-09-04",
  boundary: {
    endpoint,
    model,
    dimensions,
    maximum_batch_texts: maximumBatchTexts,
    external_text_transfer_authorized: false,
    paid_api_authorized: false,
    automatic_retries: 0,
    network_calls: 0,
    texts_transmitted: 0,
    notes: "The local lexical token proxy is an audit estimate, not provider billing usage. No API key is read by this preflight.",
  },
  inputs: {
    freeze: { path: relativePath(freezePath), sha256: await digestFile(freezePath) },
    cache_root: relativePath(cacheRoot),
    cache_schema: cacheSchema,
  },
  text_inventory: textInventory,
  documents,
  queries,
  counts: {
    frozen_cases: freeze.cases.length,
    expected_dense_ranking_rows: freeze.cases.length * 4,
    group_case_counts: Object.fromEntries(Object.keys(freeze.groups).map((group) => [group, freeze.cases.filter((entry) => entry.group === group).length])),
    document_instances: documents.length,
    query_instances: queries.length,
    unique_document_texts: documentIds.size,
    unique_query_texts: queryIds.size,
    unique_texts: textInventory.length,
    cached_document_texts: countTotals(cachedDocuments),
    cached_query_texts: countTotals(cachedQueries),
    new_document_texts: countTotals(missingDocuments),
    new_query_texts: countTotals(missingQueries),
    new_texts_total: countTotals(missing),
    maximum_request_attempts_no_retry: callCeiling,
    maximum_successful_calls_no_retry: callCeiling,
  },
};

await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "payload.json"), `${JSON.stringify(payload, null, 2)}\n`);
const manifest = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_QWEN_PREFLIGHT_MANIFEST_LOCAL_ONLY_NOT_EXECUTED",
  payload_sha256: await digestFile(join(outputRoot, "payload.json")),
  payload_counts: payload.counts,
  network_calls: 0,
  texts_transmitted: 0,
};
await writeFile(join(outputRoot, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${await digestFile(join(outputRoot, "payload.json"))}  payload.json\n${await digestFile(join(outputRoot, "manifest.json"))}  manifest.json\n`);
console.log(JSON.stringify(manifest, null, 2));
