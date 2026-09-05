#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const freezePath = join(root, "round3_clean_only_joint_group_freeze", "joint_group_scoring_freeze_v1.json");
const preflightRoot = join(root, "round3_clean_only_joint_group_qwen_preflight");
const payloadPath = join(preflightRoot, "payload.json");
const manifestPath = join(preflightRoot, "manifest.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const [freeze, payload, manifest] = await Promise.all([readJson(freezePath), readJson(payloadPath), readJson(manifestPath)]);
assert(payload.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_QWEN_PREFLIGHT_LOCAL_ONLY_NOT_EXECUTED", "Unexpected preflight status.");
assert(manifest.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_QWEN_PREFLIGHT_MANIFEST_LOCAL_ONLY_NOT_EXECUTED", "Unexpected manifest status.");
assert(manifest.payload_sha256 === await digestFile(payloadPath), "Payload hash mismatch.");
assert(payload.boundary.network_calls === 0 && payload.boundary.texts_transmitted === 0, "Preflight must have no network activity.");
assert(payload.boundary.external_text_transfer_authorized === false && payload.boundary.paid_api_authorized === false, "Preflight must not imply external authorisation.");
assert(payload.inputs.freeze.sha256 === await digestFile(freezePath), "Preflight freeze hash mismatch.");
assert(payload.counts.frozen_cases === freeze.cases.length, "Frozen case count mismatch.");
assert(payload.counts.expected_dense_ranking_rows === freeze.cases.length * 4, "Expected dense row count mismatch.");
assert(JSON.stringify(payload.counts.group_case_counts) === JSON.stringify(Object.fromEntries(Object.keys(freeze.groups).map((group) => [group, freeze.cases.filter((entry) => entry.group === group).length]))), "Group case counts mismatch.");
assert(payload.documents.length === freeze.cases.reduce((sum, row) => sum + row.candidate_count * 2, 0), "Document-instance count mismatch.");
assert(payload.queries.length === freeze.cases.length * 2, "Query-instance count mismatch.");
const inventoryIds = new Set(payload.text_inventory.map((entry) => entry.text_id));
assert(inventoryIds.size === payload.text_inventory.length, "Duplicate text inventory ID.");
for (const entry of payload.text_inventory) {
  assert(sha256(Buffer.from(entry.text, "utf8")) === entry.text_id, `Inventory text hash mismatch: ${entry.text_id}`);
  assert(entry.roles.length > 0, `Inventory text has no roles: ${entry.text_id}`);
}
for (const item of [...payload.documents, ...payload.queries]) assert(inventoryIds.has(item.text_id), `Unresolved text ID ${item.text_id}`);
const caseByIdAndGroup = new Map(freeze.cases.map((entry) => [`${entry.case_id}\u0000${entry.group}`, entry]));
for (const item of payload.documents) {
  const caseRow = caseByIdAndGroup.get(`${item.case_id}\u0000${item.group}`);
  assert(caseRow && item.group === caseRow.group, `Document group mismatch for ${item.case_id}.`);
  assert(["FULL_ORIGINAL", caseRow.group_condition].includes(item.condition), `Document condition mismatch for ${item.case_id}.`);
}
for (const item of payload.queries) {
  const caseRow = caseByIdAndGroup.get(`${item.case_id}\u0000${item.group}`);
  assert(caseRow && item.group === caseRow.group, `Query group mismatch for ${item.case_id}.`);
}
const documentIds = new Set(payload.documents.map((item) => item.text_id));
const queryIds = new Set(payload.queries.map((item) => item.text_id));
assert(documentIds.size === payload.counts.unique_document_texts, "Unique document count mismatch.");
assert(queryIds.size === payload.counts.unique_query_texts, "Unique query count mismatch.");
assert(inventoryIds.size === payload.counts.unique_texts, "Unique inventory count mismatch.");
assert(payload.counts.new_texts_total.texts === payload.counts.new_document_texts.texts + payload.counts.new_query_texts.texts, "New text partition mismatch.");
assert(payload.counts.maximum_request_attempts_no_retry === payload.counts.maximum_successful_calls_no_retry, "Request/success ceilings must agree without retry.");

console.log(JSON.stringify({
  status: "PASS_LOCAL_ONLY",
  payload_sha256: manifest.payload_sha256,
  unique_documents: documentIds.size,
  unique_queries: queryIds.size,
  new_texts: payload.counts.new_texts_total,
  maximum_request_attempts_no_retry: payload.counts.maximum_request_attempts_no_retry,
  network_calls: 0,
  texts_transmitted: 0,
}, null, 2));
