#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const requestedBatch = args[0] === "--batch" ? args[1] : null;
if (args.length !== 0 && (!requestedBatch || args.length !== 2)) {
  throw new Error("Usage: node ingest_rq1_original_removal_remediation_maps.mjs [--batch batch_01]");
}
const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const packetRoot = join(root, "remediation_packets");
const workRoot = join(root, "remediation_submissions", "agent_work");
const canonicalRoot = join(root, "remediation_submissions", "canonical");
const validator = resolve("skill_benchmark/scripts/validate_rq1_original_removal_remediation_map.mjs");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const manifest = JSON.parse(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8"));
const expectedBatches = manifest.batches.map((entry) => entry.batch_id).sort();
const runValidator = (submissionPath) => new Promise((resolveRun, rejectRun) => {
  const child = spawn(process.execPath, [validator, submissionPath], { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = ""; let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.on("error", rejectRun);
  child.on("close", (code) => code === 0 ? resolveRun(JSON.parse(stdout)) : rejectRun(new Error(stderr || stdout)));
});

await mkdir(canonicalRoot, { recursive: true });
const selected = requestedBatch ? [`${requestedBatch}.json`] : (await readdir(workRoot).catch(() => [])).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
if (selected.length === 0) throw new Error("No remediation-map submission found.");
const latest = [];
for (const fileName of selected) {
  const source = join(workRoot, fileName);
  const validation = await runValidator(source);
  const raw = await readFile(source);
  const parsed = JSON.parse(raw);
  const output = join(canonicalRoot, fileName);
  await writeFile(output, raw);
  latest.push({ batch_id: parsed.batch_id, validation, sha256: sha256(raw), output });
}

const canonicalFiles = (await readdir(canonicalRoot)).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
const byItem = [];
for (const fileName of canonicalFiles) {
  const review = JSON.parse(await readFile(join(canonicalRoot, fileName), "utf8"));
  for (const item of review.items) {
    const maps = item.candidates.flatMap((candidate) => Object.entries(candidate.field_maps).map(([field, map]) => ({ candidate_label: candidate.label, field, status: map.status, edit_count: map.edits.length })));
    const status = maps.some((entry) => entry.status === "UNSAFE_MIXED_CARRIER") ? "UNSAFE_MIXED_CARRIER"
      : maps.some((entry) => entry.status === "UNCERTAIN") ? "UNCERTAIN"
      : "SUPPLEMENTAL_MAPPED";
    byItem.push({ item_id: item.item_id, remediation_status: status, maps });
  }
}
const counts = {};
for (const entry of byItem) counts[entry.remediation_status] = (counts[entry.remediation_status] ?? 0) + 1;
const remaining = expectedBatches.filter((batch) => !canonicalFiles.includes(`${batch}.json`));
const result = {
  status: remaining.length === 0 ? "COMPLETE_PENDING_REMATERIALISATION" : "PARTIAL",
  completed_batches: canonicalFiles.length,
  expected_batches: expectedBatches.length,
  remaining_batches: remaining,
  remediation_item_counts: counts,
  item_summary: byItem,
  latest_ingested: latest,
};
await writeFile(join(canonicalRoot, "INGESTION_STATUS.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({ status: result.status, completed_batches: result.completed_batches, expected_batches: result.expected_batches, remediation_item_counts: counts, ingested: latest }));
