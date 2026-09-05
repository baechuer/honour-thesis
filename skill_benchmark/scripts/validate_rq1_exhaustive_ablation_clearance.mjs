#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) {
  throw new Error("Usage: validate_rq1_exhaustive_ablation_clearance.mjs <submission.json>");
}

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(
  await readFile(resolve(root, "pilot_target_masks/TARGET_MASK_MANIFEST.json"), "utf8"),
);
const submission = JSON.parse(await readFile(resolve(submissionPath), "utf8"));
const expected = manifest.single_units.find((item) => item.unit_id === submission.unit_id);
if (!expected) throw new Error(`Unknown unit_id ${submission.unit_id}`);

const failures = [];
if (submission.target_field !== expected.target_field) {
  failures.push(`target_field mismatch: ${submission.target_field} != ${expected.target_field}`);
}
if (!Array.isArray(submission.candidates)) failures.push("candidates must be an array");

const actualByLabel = new Map(
  (submission.candidates ?? []).map((candidate) => [candidate.label, candidate]),
);
for (const expectedCandidate of expected.candidates) {
  const actual = actualByLabel.get(expectedCandidate.label);
  if (!actual) {
    failures.push(`missing candidate ${expectedCandidate.label}`);
    continue;
  }
  if (!new Set(["CLEAR", "RESIDUAL", "UNCERTAIN"]).has(actual.status)) {
    failures.push(`${actual.label}: invalid status ${actual.status}`);
  }
  if (!Array.isArray(actual.residual_spans)) {
    failures.push(`${actual.label}: residual_spans must be an array`);
  }
  const spans = Array.isArray(actual.residual_spans) ? actual.residual_spans : [];
  if (actual.status === "CLEAR" && spans.length) {
    failures.push(`${actual.label}: CLEAR cannot have residual spans`);
  }
  if (actual.status === "RESIDUAL" && !spans.length) {
    failures.push(`${actual.label}: RESIDUAL requires at least one exact span`);
  }
  if (typeof actual.rationale !== "string" || !actual.rationale.trim()) {
    failures.push(`${actual.label}: rationale required`);
  }

  const lines = (await readFile(expectedCandidate.masked_path, "utf8")).split(/\r?\n/);
  const intervals = [];
  for (const [index, span] of spans.entries()) {
    const prefix = `${actual.label}.residual_spans[${index}]`;
    if (
      !Number.isInteger(span.line_start) ||
      !Number.isInteger(span.line_end) ||
      span.line_start < 1 ||
      span.line_end < span.line_start ||
      span.line_end > lines.length
    ) {
      failures.push(`${prefix}: invalid line range`);
      continue;
    }
    const exact = lines.slice(span.line_start - 1, span.line_end).join("\n");
    if (span.quote !== exact) failures.push(`${prefix}: quote is not exact masked text`);
    if (typeof span.rationale !== "string" || !span.rationale.trim()) {
      failures.push(`${prefix}: rationale required`);
    }
    intervals.push([span.line_start, span.line_end]);
  }
  intervals.sort((left, right) => left[0] - right[0] || left[1] - right[1]);
  for (let index = 1; index < intervals.length; index += 1) {
    if (intervals[index][0] <= intervals[index - 1][1]) {
      failures.push(`${actual.label}: residual spans overlap`);
    }
  }
}

const expectedLabels = new Set(expected.candidates.map((candidate) => candidate.label));
const extras = [...actualByLabel.keys()].filter((label) => !expectedLabels.has(label));
if (extras.length) failures.push(`unexpected candidates: ${extras.join(", ")}`);

const result = {
  status: failures.length ? "FAIL" : "PASS",
  submission: submissionPath,
  failures,
};
console.log(JSON.stringify(result, null, 2));
if (failures.length) process.exit(1);
