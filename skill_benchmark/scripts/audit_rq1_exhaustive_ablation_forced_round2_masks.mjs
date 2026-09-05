#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifestPath = join(root, "forced_round2_masks", "FORCED_ROUND2_MASK_MANIFEST.json");
const outputPath = join(root, "forced_round2_masks", "audit", "exact_diff_audit.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";

function expectedForced(round1, removedLineNumbers) {
  const lines = round1.split(/\r?\n/);
  const removed = new Set(removedLineNumbers);
  return lines.map((line, index) => removed.has(index + 1) ? "" : line).join(endingOf(round1));
}

const failures = [];
let checked = 0;
let residualCandidates = 0;
let clearCandidates = 0;
let removedLines = 0;
for (const unit of manifest.units) {
  for (const candidate of unit.candidates) {
    checked += 1;
    const round1 = await readFile(candidate.round1_masked_path, "utf8");
    const forced = await readFile(candidate.forced_masked_path, "utf8");
    if (sha256(round1) !== candidate.round1_masked_sha256) failures.push(`${unit.unit_id}/${candidate.label}: round-one hash mismatch`);
    if (sha256(forced) !== candidate.forced_masked_sha256) failures.push(`${unit.unit_id}/${candidate.label}: forced hash mismatch`);
    const expected = expectedForced(round1, candidate.forced_removed_line_numbers);
    if (forced !== expected) failures.push(`${unit.unit_id}/${candidate.label}: output differs beyond ledgered line deletions`);
    const lines = round1.split(/\r?\n/);
    for (const span of candidate.residual_spans_removed) {
      const actual = lines.slice(span.line_start - 1, span.line_end).join("\n");
      if (actual !== span.quote) failures.push(`${unit.unit_id}/${candidate.label}: residual quote mismatch ${span.line_start}-${span.line_end}`);
      for (let line = span.line_start; line <= span.line_end; line += 1) {
        if (!candidate.forced_removed_line_numbers.includes(line)) failures.push(`${unit.unit_id}/${candidate.label}: residual line ${line} not deleted`);
      }
    }
    if (candidate.round1_clearance_status === "RESIDUAL") residualCandidates += 1;
    if (candidate.round1_clearance_status === "CLEAR") {
      clearCandidates += 1;
      if (candidate.forced_removed_line_numbers.length !== 0 || forced !== round1) failures.push(`${unit.unit_id}/${candidate.label}: round-one clear card changed`);
    }
    removedLines += candidate.forced_removed_line_numbers.length;
  }
}
const audit = {
  status: failures.length === 0 ? "RQ1_FORCED_ROUND2_EXACT_DIFF_AUDIT_PASS_PENDING_FRESH_BLIND_CLEARANCE" : "RQ1_FORCED_ROUND2_EXACT_DIFF_AUDIT_FAIL",
  boundary: "Local transformation validation only. This does not establish that target information is absent after forced removal and is not a routing result.",
  checked_units: manifest.units.length,
  checked_candidates: checked,
  round1_residual_candidates: residualCandidates,
  round1_clear_candidates: clearCandidates,
  forced_removed_lines: removedLines,
  failures,
};
await mkdir(resolve(outputPath, ".."), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(audit, null, 2)}\n`);
console.log(JSON.stringify(audit));
