#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile, stat, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const preflightRoot = join(root, "round3_clean_only_qwen_preflight");
const payloadPath = join(preflightRoot, "payload.json");
const manifestPath = join(preflightRoot, "manifest.json");
const authorisationPath = join(preflightRoot, "authorisation.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

try {
  await stat(authorisationPath);
  throw new Error(`Refusing to overwrite authorisation receipt: ${authorisationPath}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const [payload, manifest] = await Promise.all([readJson(payloadPath), readJson(manifestPath)]);
const payloadSha256 = await digestFile(payloadPath);
if (manifest.payload_sha256 !== payloadSha256) throw new Error("Preflight payload hash mismatch.");
const receipt = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_QWEN_ONE_RUN_AUTHORISED",
  recorded_on: "2026-09-04",
  approval_source: "User message: ok allow, following the exact preflight scope presented in the immediately preceding assistant message.",
  payload_sha256: payloadSha256,
  endpoint: payload.boundary.endpoint,
  model: payload.boundary.model,
  dimensions: payload.boundary.dimensions,
  cache_root: payload.inputs.cache_root,
  maximum_new_texts: payload.counts.new_texts_total.texts,
  maximum_utf8_bytes: payload.counts.new_texts_total.utf8_bytes,
  maximum_local_lexical_token_proxy: payload.counts.new_texts_total.local_lexical_token_proxy,
  maximum_request_attempts: payload.counts.maximum_request_attempts_no_retry,
  maximum_successful_calls: payload.counts.maximum_successful_calls_no_retry,
  automatic_retries: 0,
  scope: "Qwen text-embedding-v4 dense twin only; no query rewrite, reranker, hosted job, or thesis/PDF write.",
};
await writeFile(authorisationPath, `${JSON.stringify(receipt, null, 2)}\n`);
console.log(JSON.stringify({ status: receipt.status, payload_sha256, maximum_new_texts: receipt.maximum_new_texts, maximum_request_attempts: receipt.maximum_request_attempts }, null, 2));
