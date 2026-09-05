#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const masksRoot = join(root, "materialized_masks");
const manifestPath = join(masksRoot, "MASK_MATERIALIZATION_MANIFEST.json");
const outputRoot = join(root, "audit");
const hash = (value) => createHash("sha256").update(value).digest("hex");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const rows = [];
const replacementCounts = new Map();
let failures = 0;

for (const composition of manifest.compositions) {
  for (const [condition, state] of Object.entries(composition.conditions)) {
    if (state.status !== "MATERIALIZED_PENDING_AUDIT") continue;
    const ledger = JSON.parse(await readFile(state.ledger_path, "utf8"));
    for (const candidate of ledger.candidates) {
      const original = await readFile(candidate.original_path, "utf8");
      const masked = await readFile(candidate.masked_path, "utf8");
      const originalLines = original.split("\n");
      const maskedLines = masked.split("\n");
      const expectedLines = [...originalLines];
      const allowed = new Map(candidate.edits.map((edit) => [edit.line, edit.replacement]));
      for (const [line, replacement] of allowed) expectedLines[line - 1] = replacement;
      const changedLines = [];
      for (let index = 0; index < Math.max(originalLines.length, maskedLines.length); index += 1) {
        if (originalLines[index] !== maskedLines[index]) changedLines.push(index + 1);
      }
      const allowedLines = [...allowed.keys()].sort((left, right) => left - right);
      const unexpectedChangedLines = changedLines.filter((line) => !allowed.has(line));
      const noOpAllowedLines = allowedLines.filter((line) => !changedLines.includes(line));
      const diffWithinLedger = unexpectedChangedLines.length === 0;
      const exactReconstruction = masked === expectedLines.join("\n");
      const originalHash = hash(original);
      const maskedHash = hash(masked);
      const hashMatch = originalHash === candidate.original_sha256 && maskedHash === candidate.masked_sha256;
      for (const edit of candidate.edits) replacementCounts.set(edit.replacement, (replacementCounts.get(edit.replacement) ?? 0) + 1);
      const status = diffWithinLedger && exactReconstruction && hashMatch ? "PASS" : "FAIL";
      if (status === "FAIL") failures += 1;
      rows.push({
        composition_id: composition.composition_id,
        condition,
        candidate_label: candidate.label,
        status,
        original_sha256: originalHash,
        masked_sha256: maskedHash,
        expected_edit_lines: allowedLines,
        actual_changed_lines: changedLines,
        unexpected_changed_lines: unexpectedChangedLines,
        no_op_allowed_lines: noOpAllowedLines,
        diff_within_ledger: diffWithinLedger,
        exact_reconstruction: exactReconstruction,
        hash_match: hashMatch,
      });
    }
  }
}
const byCondition = {};
for (const row of rows) {
  byCondition[row.condition] ??= { candidate_masks: 0, pass: 0, fail: 0, compositions: new Set() };
  byCondition[row.condition].candidate_masks += 1;
  byCondition[row.condition][row.status.toLowerCase()] += 1;
  byCondition[row.condition].compositions.add(row.composition_id);
}
for (const summary of Object.values(byCondition)) summary.compositions = summary.compositions.size;

await mkdir(outputRoot, { recursive: true });
const result = {
  status: failures === 0 ? "TECHNICAL_AUDIT_PASS_PENDING_RESIDUAL_AND_HUMAN_REVIEW" : "TECHNICAL_AUDIT_FAIL",
  candidate_mask_rows: rows.length,
  failures,
  by_condition: byCondition,
  replacement_counts: Object.fromEntries([...replacementCounts.entries()].sort(([left], [right]) => left.localeCompare(right))),
  rows,
  boundary: "This audit verifies source hashes and exact diff coverage only. It is not a residual-cue audit, a human review, or a retrieval result.",
};
await writeFile(join(outputRoot, "technical_mask_audit.json"), `${JSON.stringify(result, null, 2)}\n`);
const lines = [
  "# RQ1 Original-Document Mask Technical Audit",
  "",
  `Status: \`${result.status}\``,
  "",
  `- Candidate-mask rows: ${result.candidate_mask_rows}`,
  `- Diff/hash failures: ${result.failures}`,
  "",
  "| Condition | Compositions | Candidate masks | Pass | Fail |",
  "|---|---:|---:|---:|---:|",
  ...Object.entries(byCondition).sort(([left], [right]) => left.localeCompare(right)).map(([condition, summary]) => `| ${condition} | ${summary.compositions} | ${summary.candidate_masks} | ${summary.pass} | ${summary.fail} |`),
  "",
  "This audit does not approve masks for selector scoring. Residual-value review and the protocol's human-review record remain required.",
];
await writeFile(join(outputRoot, "technical_mask_audit.md"), `${lines.join("\n")}\n`);
console.log(JSON.stringify({ status: result.status, candidate_mask_rows: result.candidate_mask_rows, failures, by_condition: byCondition }));
