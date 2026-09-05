#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { access, mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const requestedBatch = args[0] === "--batch" ? args[1] : null;
if (args.length !== 0 && (!requestedBatch || args.length !== 2)) throw new Error("Usage: node ingest_rq1_original_removal_residual_reviews.mjs [--batch batch_01]");
const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const packetRoot = join(root, "residual_packets");
const workRoot = join(root, "residual_submissions", "agent_work");
const canonicalRoot = join(root, "residual_submissions", "canonical");
const validator = resolve("skill_benchmark/scripts/validate_rq1_original_removal_residual_review.mjs");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const packetManifest = JSON.parse(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8"));

const runValidator = (submissionPath) => new Promise((resolveRun, rejectRun) => {
  const child = spawn(process.execPath, [validator, submissionPath], { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = ""; let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.on("error", rejectRun);
  child.on("close", (code) => code === 0 ? resolveRun(JSON.parse(stdout)) : rejectRun(new Error(`Validation failed for ${submissionPath}: ${stderr || stdout}`)));
});

const expectedBatches = packetManifest.batches.map((entry) => entry.batch_id).sort();
const workFiles = (await readdir(workRoot).catch(() => [])).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
const selected = requestedBatch ? [`${requestedBatch}.json`] : workFiles;
if (selected.length === 0) throw new Error("No residual-review submission found.");
await mkdir(canonicalRoot, { recursive: true });
const latest = [];
for (const fileName of selected) {
  const workSource = join(workRoot, fileName);
  const canonicalCandidate = join(canonicalRoot, fileName);
  const workRaw = await readFile(workSource);
  let source = workSource;
  let raw = workRaw;
  let normalised = false;
  try {
    await runValidator(workSource);
  } catch (rawError) {
    await access(canonicalCandidate);
    const candidateRaw = await readFile(canonicalCandidate);
    const candidate = JSON.parse(candidateRaw);
    if (candidate.provenance?.canonicalized_from !== resolve(workSource)
      || candidate.provenance?.method !== "lossless_flat_to_nested_schema_normalisation") {
      throw rawError;
    }
    source = canonicalCandidate;
    raw = candidateRaw;
    normalised = true;
  }
  const validation = await runValidator(source);
  const parsed = JSON.parse(raw);
  const output = join(canonicalRoot, fileName);
  if (source !== output) await writeFile(output, raw);
  latest.push({ batch_id: parsed.batch_id, validation, sha256: sha256(raw), raw_submission_sha256: sha256(workRaw), normalised, output });
}
const canonicalFiles = (await readdir(canonicalRoot)).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
const itemSummary = [];
for (const fileName of canonicalFiles) {
  const review = JSON.parse(await readFile(join(canonicalRoot, fileName), "utf8"));
  const packet = packetManifest.batches.find((entry) => entry.batch_id === review.batch_id);
  for (const item of review.items) {
    const fields = packet.items.find((entry) => entry.item_id === item.item_id).fields;
    const reviews = item.candidates.flatMap((candidate) => fields.map((field) => ({ candidate_label: candidate.label, field, ...candidate.field_reviews[field] })));
    const residuals = reviews.filter((entry) => entry.status === "RESIDUAL_FOUND");
    const uncertain = reviews.filter((entry) => entry.status === "UNCERTAIN");
    itemSummary.push({ item_id: item.item_id, residual_status: residuals.length > 0 ? "RESIDUAL_FOUND" : uncertain.length > 0 ? "UNCERTAIN" : "CLEAR", residual_count: residuals.length, uncertain_count: uncertain.length, reviews });
  }
}
const counts = {};
for (const item of itemSummary) counts[item.residual_status] = (counts[item.residual_status] ?? 0) + 1;
const remaining = expectedBatches.filter((batch) => !canonicalFiles.includes(`${batch}.json`));
const result = { status: remaining.length === 0 ? "COMPLETE" : "PARTIAL", canonical_batches: canonicalFiles.map((name) => name.slice(0, -5)), completed_batches: canonicalFiles.length, expected_batches: expectedBatches.length, remaining_batches: remaining, residual_item_counts: counts, item_summary: itemSummary, latest_ingested: latest };
await writeFile(join(canonicalRoot, "INGESTION_STATUS.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({ status: result.status, completed_batches: result.completed_batches, expected_batches: result.expected_batches, remaining_batches: result.remaining_batches, residual_item_counts: counts, ingested: latest }));
