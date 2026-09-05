#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { createHash } from "node:crypto";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: validate_rq1_exhaustive_ablation_composition_map.mjs <submission.json>");

const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];
const validStatuses = new Set(["MAPPED", "NO_TARGET_CUE"]);
const source = resolve(submissionPath);
const submission = JSON.parse(await readFile(source, "utf8"));
const packetRoot = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "expansion_packets");
const packetPath = join(packetRoot, submission.composition_unit_id ?? "", "packet.json");
const packet = JSON.parse(await readFile(packetPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const errors = [];

if (submission.composition_unit_id !== packet.composition_unit_id) errors.push("composition_unit_id mismatch");
if (!Array.isArray(submission.candidates)) errors.push("candidates must be an array");
const expectedLabels = packet.candidates.map((candidate) => candidate.label);
const actualLabels = Array.isArray(submission.candidates) ? submission.candidates.map((candidate) => candidate.label) : [];
if (JSON.stringify(expectedLabels) !== JSON.stringify(actualLabels)) errors.push("candidate labels/order mismatch");

for (const expected of packet.candidates) {
  const candidate = submission.candidates?.find((item) => item.label === expected.label);
  if (!candidate) continue;
  const documentPath = join(dirname(packetPath), expected.path);
  const document = await readFile(documentPath, "utf8");
  if (sha256(document) !== expected.sha256) errors.push(`${expected.label}: source hash mismatch`);
  const lines = document.split(/\r?\n/);
  const mapKeys = Object.keys(candidate.field_maps ?? {});
  if (JSON.stringify(mapKeys) !== JSON.stringify(fields)) {
    errors.push(`${expected.label}: field_maps keys/order mismatch`);
  }
  for (const field of fields) {
    const map = candidate.field_maps?.[field];
    if (!map || !validStatuses.has(map.status)) {
      errors.push(`${expected.label}/${field}: invalid or missing status`);
      continue;
    }
    if (!Array.isArray(map.target_spans)) {
      errors.push(`${expected.label}/${field}: target_spans must be an array`);
      continue;
    }
    if (map.status === "MAPPED" && map.target_spans.length === 0) errors.push(`${expected.label}/${field}: MAPPED requires spans`);
    if (map.status === "NO_TARGET_CUE" && map.target_spans.length !== 0) errors.push(`${expected.label}/${field}: NO_TARGET_CUE forbids spans`);
    let previousEnd = 0;
    for (const [index, span] of map.target_spans.entries()) {
      const tag = `${expected.label}/${field}/span_${index + 1}`;
      if (!Number.isInteger(span.line_start) || !Number.isInteger(span.line_end) || span.line_start < 1 || span.line_end < span.line_start || span.line_end > lines.length) {
        errors.push(`${tag}: invalid line range`);
        continue;
      }
      if (span.line_start <= previousEnd) errors.push(`${tag}: spans overlap or are unsorted`);
      previousEnd = span.line_end;
      const quote = lines.slice(span.line_start - 1, span.line_end).join("\n");
      if (span.quote !== quote) errors.push(`${tag}: quote mismatch`);
      if (typeof span.rationale !== "string" || !span.rationale.trim()) errors.push(`${tag}: missing rationale`);
      if (!Array.isArray(span.collateral_fields)) errors.push(`${tag}: collateral_fields must be an array`);
      for (const collateral of span.collateral_fields ?? []) {
        if (!fields.includes(collateral) || collateral === field) errors.push(`${tag}: invalid collateral field ${collateral}`);
      }
    }
  }
}

if (errors.length) {
  console.error(JSON.stringify({ status: "INVALID", submission: source, error_count: errors.length, errors }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({
  status: "VALID",
  composition_unit_id: submission.composition_unit_id,
  candidates: submission.candidates.length,
  field_maps: submission.candidates.length * fields.length,
  target_spans: submission.candidates.reduce((sum, candidate) => sum + fields.reduce((fieldSum, field) => fieldSum + candidate.field_maps[field].target_spans.length, 0), 0),
}));
