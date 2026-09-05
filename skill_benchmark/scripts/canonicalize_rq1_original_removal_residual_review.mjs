#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) {
  throw new Error("Usage: node canonicalize_rq1_original_removal_residual_review.mjs <submission.json>");
}

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const allowedStatuses = new Set(["CLEAR", "RESIDUAL_FOUND", "UNCERTAIN"]);
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
const batchId = submission.batch_id;
if (typeof batchId !== "string" || !Array.isArray(submission.reviews)) {
  throw new Error("Only legacy flat residual-review submissions with batch_id and reviews[] may be canonicalized.");
}

const manifest = JSON.parse(await readFile(join(root, "residual_packets", "agent_packet_manifest.json"), "utf8"));
const batch = manifest.batches.find((entry) => entry.batch_id === batchId);
if (!batch) throw new Error(`Unknown batch ${batchId}.`);

const records = new Map();
for (const review of submission.reviews) {
  const candidate = review.candidate ?? review.candidate_id;
  const status = review.status ?? review.decision ?? review.verdict;
  if (typeof review.item_id !== "string" || typeof candidate !== "string" || typeof review.field !== "string") {
    throw new Error("Legacy review is missing item_id, candidate, or field.");
  }
  if (!allowedStatuses.has(status) || !Array.isArray(review.evidence)) {
    throw new Error(`Invalid legacy decision for ${review.item_id}/${candidate}/${review.field}.`);
  }
  const key = `${review.item_id}\u0000${candidate}\u0000${review.field}`;
  if (records.has(key)) throw new Error(`Duplicate legacy decision ${key}.`);
  const evidence = review.evidence.map((entry) => ({
    line_start: entry.line_start ?? entry.start_line ?? entry.start,
    line_end: entry.line_end ?? entry.end_line ?? entry.end,
    note: entry.note,
  }));
  records.set(key, { status, evidence });
}

const items = batch.items.map((item) => ({
  item_id: item.item_id,
  candidates: item.candidates.map((label) => ({
    label,
    field_reviews: Object.fromEntries(item.fields.map((field) => {
      const key = `${item.item_id}\u0000${label}\u0000${field}`;
      const decision = records.get(key);
      if (!decision) throw new Error(`Missing legacy decision ${key}.`);
      records.delete(key);
      return [field, decision];
    })),
  })),
}));

if (records.size !== 0) {
  throw new Error(`Legacy submission contains ${records.size} unexpected decision(s).`);
}

const canonical = {
  status: "RESIDUAL_REVIEW_COMPLETE",
  batch_id: batchId,
  items,
  provenance: {
    canonicalized_from: resolve(submissionPath),
    method: "lossless_flat_to_nested_schema_normalisation",
  },
};
const outputPath = join(root, "residual_submissions", "canonical", `${batchId}.json`);
await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(canonical, null, 2)}\n`);
console.log(JSON.stringify({ status: "CANONICALIZED", batch_id: batchId, output: outputPath, field_candidate_reviews: submission.reviews.length }));
