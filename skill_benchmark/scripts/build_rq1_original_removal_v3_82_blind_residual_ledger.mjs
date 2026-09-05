#!/usr/bin/env node

import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const packetRoot = join(root, "blind_residual_packets");
const canonicalRoot = join(root, "blind_residual_submissions", "canonical");
const outputRoot = join(root, "blind_residual_ledger");
const manifest = JSON.parse(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8"));
const expectedBatches = [...new Set(manifest.items.map((item) => item.batch_id))].sort();
const existing = new Set((await readdir(canonicalRoot, { withFileTypes: true })).filter((entry) => entry.isFile() && /^batch_\d{2}\.json$/.test(entry.name)).map((entry) => entry.name.slice(0, -5)));
const missing = expectedBatches.filter((batch) => !existing.has(batch));
if (missing.length) throw new Error(`Missing canonical residual batches: ${missing.join(", ")}`);
const reviewByItem = new Map();
for (const batchId of expectedBatches) {
  const path = join(canonicalRoot, `${batchId}.json`);
  const validation = spawnSync(process.execPath, ["skill_benchmark/scripts/validate_rq1_original_removal_v3_82_blind_residual_review.mjs", path], { encoding: "utf8" });
  process.stdout.write(validation.stdout);
  process.stderr.write(validation.stderr);
  if (validation.status !== 0) process.exit(validation.status ?? 1);
  const submission = JSON.parse(await readFile(path, "utf8"));
  for (const item of submission.items) reviewByItem.set(item.item_id, item);
}
const rows = manifest.items.map((item) => {
  const review = reviewByItem.get(item.item_id);
  const candidate_reviews = review.candidates.map((candidate) => ({ label: candidate.label, status: candidate.review.status }));
  const statuses = candidate_reviews.map((candidate) => candidate.status);
  return {
    item_id: item.item_id,
    target_field: item.target_field,
    status: statuses.every((status) => status === "CLEAR") ? "CLEAR" : statuses.includes("UNCERTAIN") ? "UNCERTAIN" : "RESIDUAL_FOUND",
    candidate_reviews,
  };
});
const byField = {};
for (const row of rows) {
  byField[row.target_field] ??= { CLEAR: 0, RESIDUAL_FOUND: 0, UNCERTAIN: 0 };
  byField[row.target_field][row.status] += 1;
}
const result = {
  status: "RQ1_S3_BLIND_RESIDUAL_REVIEW_COMPLETE_NO_SELECTOR_EXECUTION",
  items: rows.length,
  by_field: byField,
  rows,
  boundary: "Blind residual clearance only. This is not strict-family linkage, retrieval, or a field-effect result.",
};
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "blind_residual_ledger.json"), `${JSON.stringify(result, null, 2)}\n`);
const lines = [
  "# RQ1 82-Registry S3 Blind Residual Review Summary",
  "",
  `Status: \`${result.status}\``,
  "",
  "| Field | Clear | Residual found | Uncertain |",
  "| --- | ---: | ---: | ---: |",
  ...Object.entries(byField).sort(([left], [right]) => left.localeCompare(right)).map(([field, counts]) => `| ${field} | ${counts.CLEAR} | ${counts.RESIDUAL_FOUND} | ${counts.UNCERTAIN} |`),
  "",
  "This is a leakage gate, not a retrieval result.",
];
await writeFile(join(outputRoot, "BLIND_RESIDUAL_SUMMARY.md"), `${lines.join("\n")}\n`);
console.log(JSON.stringify({ status: result.status, items: rows.length, by_field: byField }));
