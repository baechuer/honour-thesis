#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: validate_rq1_exhaustive_ablation_map.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "pilot_packets");
const manifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const submission = JSON.parse(await readFile(resolve(submissionPath), "utf8"));
const expected = manifest.items.find((item) => item.unit_id === submission.unit_id);
if (!expected) throw new Error(`Unknown unit_id ${submission.unit_id}`);
const failures = [];
if (submission.target_field !== expected.target_field) failures.push(`target_field mismatch: ${submission.target_field} != ${expected.target_field}`);
if (!Array.isArray(submission.candidates)) failures.push("candidates must be an array");
const allowedFields = new Set(["use_condition", "input_precondition", "output_artifact", "workflow_procedure", "success_verification", "boundary_not_for", "dependency_resource"]);
const actualByLabel = new Map((submission.candidates ?? []).map((candidate) => [candidate.label, candidate]));
for (const candidate of expected.candidates) {
  const actual = actualByLabel.get(candidate.label);
  if (!actual) {
    failures.push(`missing candidate ${candidate.label}`);
    continue;
  }
  const validStatuses = new Set(["MAPPED", "NO_TARGET_CUE"]);
  if (!validStatuses.has(actual.status)) failures.push(`${candidate.label}: invalid status ${actual.status}`);
  if (!Array.isArray(actual.target_spans)) failures.push(`${candidate.label}: target_spans must be an array`);
  const spans = Array.isArray(actual.target_spans) ? actual.target_spans : [];
  if (actual.status === "MAPPED" && spans.length === 0) failures.push(`${candidate.label}: MAPPED requires target spans`);
  if (actual.status === "NO_TARGET_CUE" && spans.length !== 0) failures.push(`${candidate.label}: NO_TARGET_CUE cannot have spans`);
  const documentPath = join(root, dirname(expected.packet_path), candidate.path);
  const lines = (await readFile(documentPath, "utf8")).split(/\r?\n/);
  const intervals = [];
  for (const [index, span] of spans.entries()) {
    const prefix = `${candidate.label}.target_spans[${index}]`;
    if (!Number.isInteger(span.line_start) || !Number.isInteger(span.line_end) || span.line_start < 1 || span.line_end < span.line_start || span.line_end > lines.length) {
      failures.push(`${prefix}: invalid line range`);
      continue;
    }
    const exact = lines.slice(span.line_start - 1, span.line_end).join("\n");
    if (span.quote !== exact) failures.push(`${prefix}: quote does not exactly equal complete source lines`);
    if (typeof span.rationale !== "string" || !span.rationale.trim()) failures.push(`${prefix}: rationale required`);
    if (!Array.isArray(span.collateral_fields)) failures.push(`${prefix}: collateral_fields must be an array`);
    for (const field of span.collateral_fields ?? []) {
      if (!allowedFields.has(field) || field === expected.target_field) failures.push(`${prefix}: invalid collateral field ${field}`);
    }
    intervals.push([span.line_start, span.line_end]);
  }
  intervals.sort((left, right) => left[0] - right[0] || left[1] - right[1]);
  for (let index = 1; index < intervals.length; index += 1) {
    if (intervals[index][0] <= intervals[index - 1][1]) failures.push(`${candidate.label}: target spans overlap`);
  }
}
const extra = [...actualByLabel.keys()].filter((label) => !expected.candidates.some((candidate) => candidate.label === label));
if (extra.length) failures.push(`unexpected candidates: ${extra.join(", ")}`);
const result = { status: failures.length ? "FAIL" : "PASS", submission: submissionPath, failures };
console.log(JSON.stringify(result, null, 2));
if (failures.length) process.exit(1);
