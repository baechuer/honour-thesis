#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { basename, dirname, resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: validate_rq1_exhaustive_ablation_forced_round3_clearance.mjs <submission.json>");
const submission = JSON.parse(await readFile(resolve(submissionPath), "utf8"));
const packetRoot = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round3_clearance_packets");
const packet = JSON.parse(await readFile(resolve(packetRoot, submission.unit_id, "packet.json"), "utf8"));
const statuses = new Set(["CLEAR", "RESIDUAL", "UNCERTAIN"]);
const fail = (message) => { throw new Error(message); };

if (submission.unit_id !== packet.unit_id || submission.target_field !== packet.target_field) fail("unit identity mismatch");
if (!Array.isArray(submission.candidates) || submission.candidates.length !== packet.candidates.length) fail("candidate coverage mismatch");
const expected = new Map(packet.candidates.map((candidate) => [candidate.label, candidate]));
for (const candidate of submission.candidates) {
  const expectedCandidate = expected.get(candidate.label);
  if (!expectedCandidate) fail(`unexpected candidate ${candidate.label}`);
  if (!statuses.has(candidate.status)) fail(`${candidate.label}: invalid status`);
  if (!Array.isArray(candidate.residual_spans)) fail(`${candidate.label}: residual_spans required`);
  if (candidate.status === "RESIDUAL" && candidate.residual_spans.length === 0) fail(`${candidate.label}: residual requires exact evidence`);
  if (candidate.status !== "RESIDUAL" && candidate.residual_spans.length !== 0) fail(`${candidate.label}: only residual may carry evidence`);
  const text = await readFile(resolve(packetRoot, packet.unit_id, expectedCandidate.path), "utf8");
  const lines = text.split(/\r?\n/);
  for (const span of candidate.residual_spans) {
    if (!Number.isInteger(span.line_start) || !Number.isInteger(span.line_end) || span.line_start < 1 || span.line_end < span.line_start) fail(`${candidate.label}: invalid line range`);
    if (lines.slice(span.line_start - 1, span.line_end).join("\n") !== span.quote) fail(`${candidate.label}: exact quote mismatch at ${span.line_start}-${span.line_end}`);
    if (typeof span.rationale !== "string" || !span.rationale.trim()) fail(`${candidate.label}: residual rationale required`);
  }
  if (typeof candidate.rationale !== "string" || !candidate.rationale.trim()) fail(`${candidate.label}: rationale required`);
  expected.delete(candidate.label);
}
if (expected.size) fail(`missing candidate ${[...expected.keys()].join(", ")}`);
console.log(JSON.stringify({ status: "RQ1_FORCED_ROUND3_FRESH_BLIND_CLEARANCE_SUBMISSION_VALID", unit_id: submission.unit_id, source_file: basename(submissionPath), parent_dir: dirname(resolve(submissionPath)) }));
