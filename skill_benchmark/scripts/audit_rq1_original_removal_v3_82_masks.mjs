#!/usr/bin/env node

// Independently verify S2 source hashes and exact line-level reconstruction.
// It deliberately does not inspect semantic residuals or retrieval outcomes.

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const masksRoot = join(root, "materialized_masks");
const manifestPath = join(masksRoot, "MASK_MATERIALIZATION_MANIFEST.json");
const outputRoot = join(root, "technical_audit");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const rows = [];
let failures = 0;

for (const composition of manifest.compositions) {
  for (const [condition, state] of Object.entries(composition.conditions)) {
    if (state.status !== "MATERIALIZED_PENDING_TECHNICAL_AUDIT") continue;
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
      const unexpectedChangedLines = changedLines.filter((line) => !allowed.has(line));
      const noOpAllowedLines = [...allowed.keys()].filter((line) => !changedLines.includes(line));
      const originalHash = sha256(original);
      const maskedHash = sha256(masked);
      const status = originalHash === candidate.source_packet_sha256
        && originalHash === candidate.original_sha256
        && maskedHash === candidate.masked_sha256
        && masked === expectedLines.join("\n")
        && unexpectedChangedLines.length === 0 ? "PASS" : "FAIL";
      if (status === "FAIL") failures += 1;
      rows.push({
        composition_id: composition.composition_id,
        condition,
        candidate_label: candidate.label,
        status,
        original_sha256: originalHash,
        masked_sha256: maskedHash,
        expected_edit_lines: [...allowed.keys()].sort((left, right) => left - right),
        actual_changed_lines: changedLines,
        unexpected_changed_lines: unexpectedChangedLines,
        no_op_allowed_lines: noOpAllowedLines,
      });
    }
  }
}
const byCondition = {};
for (const row of rows) {
  byCondition[row.condition] ??= { compositions: new Set(), candidate_masks: 0, pass: 0, fail: 0 };
  const summary = byCondition[row.condition];
  summary.compositions.add(row.composition_id);
  summary.candidate_masks += 1;
  summary[row.status.toLowerCase()] += 1;
}
for (const summary of Object.values(byCondition)) summary.compositions = summary.compositions.size;
const result = {
  status: failures === 0 ? "TECHNICAL_AUDIT_PASS_PENDING_BLIND_RESIDUAL_REVIEW" : "TECHNICAL_AUDIT_FAIL",
  candidate_mask_rows: rows.length,
  failures,
  ledgered_noop_lines: rows.reduce((sum, row) => sum + row.no_op_allowed_lines.length, 0),
  by_condition: byCondition,
  rows,
  boundary: "This audit checks only source hashes and ledgered diffs. It is not a residual, routing, retrieval, or field-effect result.",
};
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "technical_mask_audit.json"), `${JSON.stringify(result, null, 2)}\n`);
const lines = [
  "# RQ1 82-Registry Original-Document Technical Mask Audit",
  "",
  `Status: \`${result.status}\``,
  "",
  `- Candidate masks: ${result.candidate_mask_rows}`,
  `- Hash/diff failures: ${result.failures}`,
  `- Ledgered no-op lines: ${result.ledgered_noop_lines}`,
  "",
  "| Condition | Compositions | Candidate masks | Pass | Fail |",
  "| --- | ---: | ---: | ---: | ---: |",
  ...Object.entries(byCondition).sort(([left], [right]) => left.localeCompare(right)).map(([condition, summary]) => `| ${condition} | ${summary.compositions} | ${summary.candidate_masks} | ${summary.pass} | ${summary.fail} |`),
  "",
  "Passing this audit does not clear residual values or authorise selector scoring.",
];
await writeFile(join(outputRoot, "technical_mask_audit.md"), `${lines.join("\n")}\n`);
console.log(JSON.stringify({ status: result.status, candidate_mask_rows: result.candidate_mask_rows, failures, by_condition: byCondition }));
