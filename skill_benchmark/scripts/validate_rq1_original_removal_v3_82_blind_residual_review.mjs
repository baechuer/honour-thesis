#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { basename, join, resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_v3_82_blind_residual_review.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry", "blind_residual_packets");
const manifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const submission = JSON.parse(await readFile(resolve(process.cwd(), submissionPath), "utf8"));
const failures = [];
const expectedItems = manifest.items.filter((item) => item.batch_id === submission.batch_id);
const actualItems = new Map((submission.items ?? []).map((item) => [item.item_id, item]));
if (submission.status !== "BLIND_RESIDUAL_REVIEW_COMPLETE") failures.push("status must be BLIND_RESIDUAL_REVIEW_COMPLETE");
if (!/^batch_\d{2}$/.test(submission.batch_id ?? "")) failures.push("invalid batch_id");
if (actualItems.size !== expectedItems.length) failures.push("item coverage mismatch");
for (const expected of expectedItems) {
  const actual = actualItems.get(expected.item_id);
  if (!actual) { failures.push(`missing ${expected.item_id}`); continue; }
  if (actual.target_field !== expected.target_field) failures.push(`${expected.item_id}: target field mismatch`);
  const candidates = new Map((actual.candidates ?? []).map((candidate) => [candidate.label, candidate]));
  if (candidates.size !== expected.candidates.length) failures.push(`${expected.item_id}: candidate coverage mismatch`);
  for (const expectedCandidate of expected.candidates) {
    const candidate = candidates.get(expectedCandidate.label);
    if (!candidate) { failures.push(`${expected.item_id}: missing ${expectedCandidate.label}`); continue; }
    const review = candidate.review ?? {};
    if (!new Set(["CLEAR", "RESIDUAL_FOUND", "UNCERTAIN"]).has(review.status)) failures.push(`${expected.item_id}/${expectedCandidate.label}: invalid review status`);
    if (typeof review.rationale !== "string" || review.rationale.trim().length < 12) failures.push(`${expected.item_id}/${expectedCandidate.label}: rationale missing`);
    const evidence = review.evidence ?? [];
    if (!Array.isArray(evidence)) { failures.push(`${expected.item_id}/${expectedCandidate.label}: evidence must be an array`); continue; }
    if (review.status === "RESIDUAL_FOUND" && evidence.length === 0) failures.push(`${expected.item_id}/${expectedCandidate.label}: residual requires evidence`);
    if (review.status !== "RESIDUAL_FOUND" && evidence.length !== 0) failures.push(`${expected.item_id}/${expectedCandidate.label}: only residual may cite evidence`);
    const lines = (await readFile(join(root, submission.batch_id, expected.item_id, expectedCandidate.path), "utf8")).split("\n");
    for (const item of evidence) {
      if (!Number.isInteger(item.line_start) || !Number.isInteger(item.line_end) || item.line_start < 1 || item.line_end < item.line_start || item.line_end > lines.length) failures.push(`${expected.item_id}/${expectedCandidate.label}: evidence range outside masked document`);
      if (typeof item.quote !== "string" || item.quote.trim().length === 0) failures.push(`${expected.item_id}/${expectedCandidate.label}: evidence quote missing`);
      const carrier = lines.slice(item.line_start - 1, item.line_end).join("\n");
      if (typeof item.quote === "string" && !carrier.includes(item.quote)) failures.push(`${expected.item_id}/${expectedCandidate.label}: evidence quote not found in cited lines`);
    }
  }
}
const result = { status: failures.length ? "FAIL" : "PASS", submission: basename(submissionPath), failures };
console.log(JSON.stringify(result, null, 2));
process.exitCode = failures.length ? 1 : 0;
