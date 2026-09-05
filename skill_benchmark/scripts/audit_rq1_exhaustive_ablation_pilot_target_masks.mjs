#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const manifestPath = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1/pilot_target_masks/TARGET_MASK_MANIFEST.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const lineEnding = (text) => text.includes("\r\n") ? "\r\n" : "\n";
const failures = [];

for (const unit of manifest.single_units) {
  for (const candidate of unit.candidates) {
    const original = await readFile(candidate.source_path, "utf8");
    const actualMasked = await readFile(candidate.masked_path, "utf8");
    if (sha256(original) !== candidate.source_sha256) failures.push(`${unit.unit_id}/${candidate.label}: source hash mismatch`);
    if (sha256(actualMasked) !== candidate.masked_sha256) failures.push(`${unit.unit_id}/${candidate.label}: masked hash mismatch`);
    const removed = new Set();
    for (const span of candidate.removed_line_ranges) for (let line = span.line_start; line <= span.line_end; line += 1) removed.add(line);
    const expected = original.split(/\r?\n/).map((line, index) => removed.has(index + 1) ? "" : line).join(lineEnding(original));
    if (expected !== actualMasked) failures.push(`${unit.unit_id}/${candidate.label}: reconstruction mismatch`);
  }
}
for (const unit of manifest.joint_units) {
  for (const candidate of unit.candidates) {
    const original = await readFile(candidate.source_path, "utf8");
    const actualMasked = await readFile(candidate.masked_path, "utf8");
    if (sha256(original) !== candidate.source_sha256) failures.push(`${unit.composition_id}/${unit.group}/${candidate.label}: source hash mismatch`);
    if (sha256(actualMasked) !== candidate.masked_sha256) failures.push(`${unit.composition_id}/${unit.group}/${candidate.label}: masked hash mismatch`);
    const removed = new Set();
    for (const span of candidate.component_ranges) for (let line = span.line_start; line <= span.line_end; line += 1) removed.add(line);
    const expected = original.split(/\r?\n/).map((line, index) => removed.has(index + 1) ? "" : line).join(lineEnding(original));
    if (expected !== actualMasked) failures.push(`${unit.composition_id}/${unit.group}/${candidate.label}: reconstruction mismatch`);
  }
}
console.log(JSON.stringify({ status: failures.length ? "FAIL" : "PASS", single_units: manifest.single_units.length, joint_units: manifest.joint_units.length, failures }, null, 2));
if (failures.length) process.exit(1);
