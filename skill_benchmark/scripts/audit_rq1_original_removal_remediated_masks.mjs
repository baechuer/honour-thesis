#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const masksRoot = join(root, "materialized_masks_remediated");
const manifest = JSON.parse(await readFile(join(masksRoot, "REMEDIATED_MASK_MANIFEST.json"), "utf8"));
const freshReviewPath = join(root, "residual_recheck_submissions", "canonical", "INGESTION_STATUS.json");
const freshReview = JSON.parse(await readFile(freshReviewPath, "utf8"));
const outputRoot = join(root, "audit");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const rows = [];
let failures = 0;
for (const item of manifest.items.filter((entry) => entry.status === "MATERIALIZED_REMEDIATED_PENDING_AUDIT")) {
  const ledger = JSON.parse(await readFile(item.ledger_path, "utf8"));
  for (const candidate of ledger.candidates) {
    const original = await readFile(candidate.original_path, "utf8");
    const masked = await readFile(candidate.masked_path, "utf8");
    const expectedLines = original.split("\n");
    const allowed = new Map(candidate.edits.map((edit) => [edit.line, edit.replacement]));
    for (const [line, replacement] of allowed) expectedLines[line - 1] = replacement;
    const actualLines = masked.split("\n");
    const changed = actualLines.flatMap((value, index) => value === original.split("\n")[index] ? [] : [index + 1]);
    const unexpected = changed.filter((line) => !allowed.has(line));
    const pass = unexpected.length === 0 && masked === expectedLines.join("\n") && sha256(original) === candidate.original_sha256 && sha256(masked) === candidate.masked_sha256;
    if (!pass) failures += 1;
    rows.push({ item_id: item.item_id, composition_id: item.composition_id, condition: item.condition, candidate_label: candidate.label, status: pass ? "PASS" : "FAIL", changed_lines: changed, unexpected_changed_lines: unexpected });
  }
}
const result = {
  status: failures > 0 ? "TECHNICAL_AUDIT_FAIL"
    : freshReview.status === "COMPLETE" ? "TECHNICAL_AUDIT_PASS_FRESH_RESIDUAL_RECHECK_COMPLETE"
      : "TECHNICAL_AUDIT_PASS_PENDING_FRESH_RESIDUAL_AND_HUMAN_REVIEW",
  candidate_masks: rows.length,
  failures,
  fresh_residual_review: {
    status: freshReview.status,
    residual_item_counts: freshReview.residual_item_counts,
  },
  rows,
  boundary: "This is an exact diff/hash audit, not a residual-cue review or selector result.",
};
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "remediated_mask_technical_audit.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({ status: result.status, candidate_masks: result.candidate_masks, failures }));
