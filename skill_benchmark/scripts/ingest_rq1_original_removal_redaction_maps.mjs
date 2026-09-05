#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const requestedBatch = args[0] === "--batch" ? args[1] : null;
if (args.length !== 0 && (!requestedBatch || args.length !== 2)) {
  throw new Error("Usage: node ingest_rq1_original_removal_redaction_maps.mjs [--batch batch_01]");
}

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const workRoot = join(root, "redaction_submissions", "agent_work");
const canonicalRoot = join(root, "redaction_submissions", "canonical");
const validator = resolve("skill_benchmark/scripts/validate_rq1_original_removal_redaction_map.mjs");
const packetsRoot = join(root, "redaction_packets");
const manifest = JSON.parse(await readFile(join(packetsRoot, "agent_packet_manifest.json"), "utf8"));

const runValidator = (submissionPath) => new Promise((resolveRun, rejectRun) => {
  const child = spawn(process.execPath, [validator, submissionPath], { stdio: ["ignore", "pipe", "pipe"] });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.on("error", rejectRun);
  child.on("close", (code) => {
    if (code !== 0) rejectRun(new Error(`Validation failed for ${submissionPath}: ${stderr || stdout}`));
    else resolveRun(JSON.parse(stdout));
  });
});

const expectedBatchIds = manifest.batches.map((entry) => entry.batch_id).sort();
const workFiles = (await readdir(workRoot).catch(() => []))
  .filter((name) => /^batch_\d{2}\.json$/.test(name))
  .sort();
const selected = requestedBatch ? [`${requestedBatch}.json`] : workFiles;
if (selected.length === 0) throw new Error("No redaction-map submission found.");

await mkdir(canonicalRoot, { recursive: true });
const latest = [];
for (const fileName of selected) {
  const submissionPath = join(workRoot, fileName);
  const validation = await runValidator(submissionPath);
  const raw = await readFile(submissionPath);
  const parsed = JSON.parse(raw);
  const sha256 = createHash("sha256").update(raw).digest("hex");
  const outputPath = join(canonicalRoot, fileName);
  await writeFile(outputPath, raw);
  latest.push({ batch_id: parsed.batch_id, sha256, validation, output: outputPath });
}

const canonicalFiles = (await readdir(canonicalRoot))
  .filter((name) => /^batch_\d{2}\.json$/.test(name))
  .sort();
const dispositionCounts = {};
for (const fileName of canonicalFiles) {
  const parsed = JSON.parse(await readFile(join(canonicalRoot, fileName), "utf8"));
  for (const composition of parsed.compositions) {
    for (const candidate of composition.candidates) {
      for (const [field, map] of Object.entries(candidate.field_maps)) {
        dispositionCounts[field] ??= {};
        dispositionCounts[field][map.status] = (dispositionCounts[field][map.status] ?? 0) + 1;
      }
    }
  }
}
const remaining = expectedBatchIds.filter((batchId) => !canonicalFiles.includes(`${batchId}.json`));
await writeFile(
  join(canonicalRoot, "INGESTION_STATUS.json"),
  `${JSON.stringify({
    status: remaining.length === 0 ? "COMPLETE" : "PARTIAL",
    canonical_batches: canonicalFiles.map((name) => name.slice(0, -5)),
    completed_batches: canonicalFiles.length,
    expected_batches: expectedBatchIds.length,
    remaining_batches: remaining,
    candidate_field_dispositions: dispositionCounts,
    latest_ingested: latest,
  }, null, 2)}\n`,
);
console.log(JSON.stringify({ status: remaining.length === 0 ? "COMPLETE" : "PARTIAL", ingested: latest, completed_batches: canonicalFiles.length, expected_batches: expectedBatchIds.length, remaining_batches: remaining, candidate_field_dispositions: dispositionCounts }));
