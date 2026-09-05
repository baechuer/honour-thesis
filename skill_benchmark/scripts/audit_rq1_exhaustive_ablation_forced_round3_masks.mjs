#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifestPath = join(root, "forced_round3_masks", "FORCED_ROUND3_MASK_MANIFEST.json");
const outputPath = join(root, "forced_round3_masks", "audit", "exact_diff_audit.json");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";
const failures = [];
let checked = 0;
let removedLines = 0;

for (const unit of manifest.units) {
  for (const candidate of unit.candidates) {
    checked += 1;
    const round2 = await readFile(candidate.round2_masked_path, "utf8");
    const round3 = await readFile(candidate.round3_masked_path, "utf8");
    if (sha256(round2) !== candidate.round2_masked_sha256) failures.push(`${unit.unit_id}/${candidate.label}: Round-2 hash mismatch`);
    if (sha256(round3) !== candidate.round3_masked_sha256) failures.push(`${unit.unit_id}/${candidate.label}: Round-3 hash mismatch`);
    const lines = round2.split(/\r?\n/);
    const removed = new Set(candidate.round3_removed_line_numbers);
    const expected = lines.map((line, index) => removed.has(index + 1) ? "" : line).join(endingOf(round2));
    if (round3 !== expected) failures.push(`${unit.unit_id}/${candidate.label}: output differs beyond ledgered line deletions`);
    for (const span of candidate.residual_spans_removed) {
      const actual = lines.slice(span.line_start - 1, span.line_end).join("\n");
      if (actual !== span.quote) failures.push(`${unit.unit_id}/${candidate.label}: residual quote mismatch ${span.line_start}-${span.line_end}`);
      for (let line = span.line_start; line <= span.line_end; line += 1) {
        if (!removed.has(line)) failures.push(`${unit.unit_id}/${candidate.label}: cited residual line ${line} was not removed`);
      }
    }
    if (candidate.round2_clearance_status !== "RESIDUAL" && (candidate.round3_removed_line_numbers.length !== 0 || round3 !== round2)) {
      failures.push(`${unit.unit_id}/${candidate.label}: non-residual Round-2 card changed`);
    }
    removedLines += candidate.round3_removed_line_numbers.length;
  }
}

const audit = {
  status: failures.length === 0 ? "RQ1_FORCED_ROUND3_EXACT_DIFF_AUDIT_PASS_PENDING_FRESH_BLIND_CLEARANCE" : "RQ1_FORCED_ROUND3_EXACT_DIFF_AUDIT_FAIL",
  boundary: "Local transformation validation only. This is not a target-absence proof or routing result.",
  checked_units: manifest.units.length,
  checked_candidates: checked,
  round2_residual_candidates: manifest.round2_residual_candidate_count,
  round2_clear_candidates: manifest.round2_clear_candidate_count,
  round2_uncertain_candidates: manifest.round2_uncertain_candidate_count,
  forced_removed_lines: removedLines,
  failures,
};
await mkdir(resolve(outputPath, ".."), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(audit, null, 2)}\n`);
console.log(JSON.stringify(audit));
