#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const requestedBatch = args[0] === "--batch" ? args[1] : null;
if (args.length !== 0 && (!requestedBatch || args.length !== 2)) throw new Error("Usage: node ingest_rq1_original_removal_residual_recheck.mjs [--batch batch_01]");
const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const packetRoot = join(root, "residual_recheck_packets");
const workRoot = join(root, "residual_recheck_submissions", "agent_work");
const canonicalRoot = join(root, "residual_recheck_submissions", "canonical");
const validator = resolve("skill_benchmark/scripts/validate_rq1_original_removal_residual_recheck.mjs");
const hash = (value) => createHash("sha256").update(value).digest("hex");
const manifest = JSON.parse(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8"));
const expected = manifest.batches.map((entry) => entry.batch_id).sort();
const runValidator = (path) => new Promise((resolveRun, rejectRun) => {
  const child = spawn(process.execPath, [validator, path], { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = ""; let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; }); child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.on("error", rejectRun); child.on("close", (code) => code === 0 ? resolveRun(JSON.parse(stdout)) : rejectRun(new Error(stderr || stdout)));
});
await mkdir(canonicalRoot, { recursive: true });
const selected = requestedBatch ? [`${requestedBatch}.json`] : (await readdir(workRoot).catch(() => [])).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
if (!selected.length) throw new Error("No fresh residual review found.");
const latest = [];
for (const name of selected) {
  const source = join(workRoot, name); const validation = await runValidator(source); const raw = await readFile(source); const parsed = JSON.parse(raw); const output = join(canonicalRoot, name);
  await writeFile(output, raw); latest.push({ batch_id: parsed.batch_id, validation, sha256: hash(raw), output });
}
const files = (await readdir(canonicalRoot)).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
const itemSummary = [];
for (const name of files) {
  const review = JSON.parse(await readFile(join(canonicalRoot, name), "utf8"));
  const batch = manifest.batches.find((entry) => entry.batch_id === review.batch_id);
  for (const item of review.items) {
    const fields = batch.items.find((entry) => entry.item_id === item.item_id).fields;
    const decisions = item.candidates.flatMap((candidate) => fields.map((field) => ({ candidate_label: candidate.label, field, ...candidate.field_reviews[field] })));
    const residuals = decisions.filter((entry) => entry.status === "RESIDUAL_FOUND"); const uncertain = decisions.filter((entry) => entry.status === "UNCERTAIN");
    itemSummary.push({ item_id: item.item_id, residual_status: residuals.length ? "RESIDUAL_FOUND" : uncertain.length ? "UNCERTAIN" : "CLEAR", residual_count: residuals.length, uncertain_count: uncertain.length, reviews: decisions });
  }
}
const counts = {}; for (const item of itemSummary) counts[item.residual_status] = (counts[item.residual_status] ?? 0) + 1;
const remaining = expected.filter((batch) => !files.includes(`${batch}.json`));
const result = { status: remaining.length ? "PARTIAL" : "COMPLETE", completed_batches: files.length, expected_batches: expected.length, remaining_batches: remaining, residual_item_counts: counts, item_summary: itemSummary, latest_ingested: latest };
await writeFile(join(canonicalRoot, "INGESTION_STATUS.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({ status: result.status, completed_batches: result.completed_batches, expected_batches: result.expected_batches, residual_item_counts: counts, ingested: latest }));
