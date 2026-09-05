#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_residual_recheck.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_removal_v2/residual_recheck_packets");
const statuses = new Set(["CLEAR", "RESIDUAL_FOUND", "UNCERTAIN"]);
const fail = (message) => { throw new Error(message); };
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
if (submission.status !== "RESIDUAL_REVIEW_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.items)) fail("Invalid fresh residual-review submission.");
const manifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const batch = manifest.batches.find((entry) => entry.batch_id === submission.batch_id);
if (!batch || submission.items.length !== batch.items.length) fail("Batch item count mismatch.");
const expectedItems = new Map(batch.items.map((entry) => [entry.item_id, entry]));
const seenItems = new Set();
let decisions = 0;
for (const item of submission.items) {
  const expected = expectedItems.get(item.item_id);
  if (!expected || seenItems.has(item.item_id)) fail(`Invalid item ${item.item_id}.`);
  seenItems.add(item.item_id);
  if (!Array.isArray(item.candidates) || item.candidates.length !== expected.candidates.length) fail(`Candidate count mismatch for ${item.item_id}.`);
  const seenCandidates = new Set();
  for (const candidate of item.candidates) {
    if (!expected.candidates.includes(candidate.label) || seenCandidates.has(candidate.label)) fail(`Invalid candidate ${item.item_id}/${candidate.label}.`);
    seenCandidates.add(candidate.label);
    if (JSON.stringify(Object.keys(candidate.field_reviews ?? {}).sort()) !== JSON.stringify([...expected.fields].sort())) fail(`Field review mismatch for ${item.item_id}/${candidate.label}.`);
    const lineCount = (await readFile(join(root, submission.batch_id, item.item_id, `${candidate.label}.md`), "utf8")).split("\n").length;
    for (const field of expected.fields) {
      const review = candidate.field_reviews[field];
      if (!review || !statuses.has(review.status) || !Array.isArray(review.evidence)) fail(`Invalid review ${item.item_id}/${candidate.label}/${field}.`);
      if (review.status === "RESIDUAL_FOUND" && review.evidence.length === 0) fail(`Residual lacks evidence ${item.item_id}/${candidate.label}/${field}.`);
      if (review.status !== "RESIDUAL_FOUND" && review.evidence.length !== 0) fail(`Only residual may cite evidence ${item.item_id}/${candidate.label}/${field}.`);
      for (const evidence of review.evidence) {
        if (!Number.isInteger(evidence.line_start) || !Number.isInteger(evidence.line_end) || evidence.line_start < 1 || evidence.line_end < evidence.line_start || evidence.line_end > lineCount || typeof evidence.note !== "string") fail(`Invalid evidence ${item.item_id}/${candidate.label}/${field}.`);
      }
      decisions += 1;
    }
  }
}
console.log(JSON.stringify({ status: "VALID", batch_id: submission.batch_id, items: seenItems.size, field_candidate_reviews: decisions }));
