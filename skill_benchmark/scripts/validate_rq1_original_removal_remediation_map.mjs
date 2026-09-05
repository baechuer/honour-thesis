#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_remediation_map.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_removal_v2/remediation_packets");
const allowedStatuses = new Set(["SUPPLEMENTAL_SAFE_MAP", "NO_SUPPLEMENTAL_EDIT_NEEDED", "UNSAFE_MIXED_CARRIER", "UNCERTAIN"]);
const allowedKinds = new Set(["DELETE_LINE", "REWRITE_LINE"]);
const fail = (message) => { throw new Error(message); };
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
if (submission.status !== "REMEDIATION_MAP_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.items)) fail("Invalid remediation-map submission.");
const manifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const batch = manifest.batches.find((entry) => entry.batch_id === submission.batch_id);
if (!batch || submission.items.length !== batch.items.length) fail("Batch item count mismatch.");
const expectedItems = new Map(batch.items.map((entry) => [entry.item_id, entry]));
const seenItems = new Set();
let decisions = 0;
for (const item of submission.items) {
  const expected = expectedItems.get(item.item_id);
  if (!expected || seenItems.has(item.item_id)) fail(`Unknown or duplicate item ${item.item_id}.`);
  seenItems.add(item.item_id);
  if (!Array.isArray(item.candidates) || item.candidates.length !== expected.candidates.length) fail(`Candidate count mismatch for ${item.item_id}.`);
  const seenCandidates = new Set();
  for (const candidate of item.candidates) {
    if (!expected.candidates.includes(candidate.label) || seenCandidates.has(candidate.label)) fail(`Invalid candidate ${item.item_id}/${candidate.label}.`);
    seenCandidates.add(candidate.label);
    if (JSON.stringify(Object.keys(candidate.field_maps ?? {}).sort()) !== JSON.stringify([...expected.fields].sort())) fail(`Field map mismatch for ${item.item_id}/${candidate.label}.`);
    const source = await readFile(join(root, submission.batch_id, item.item_id, `${candidate.label}.md`), "utf8");
    const lineCount = source.split("\n").length;
    const existing = JSON.parse(await readFile(join(root, submission.batch_id, item.item_id, `${candidate.label}.existing_edits.json`), "utf8"));
    for (const field of expected.fields) {
      const map = candidate.field_maps[field];
      if (!map || !allowedStatuses.has(map.status) || !Array.isArray(map.source_evidence) || !Array.isArray(map.edits)) fail(`Invalid field map ${item.item_id}/${candidate.label}/${field}.`);
      const challenge = existing.residual_challenges[field];
      if (challenge && map.status === "NO_SUPPLEMENTAL_EDIT_NEEDED") fail(`Challenge cannot be dismissed for ${item.item_id}/${candidate.label}/${field}.`);
      if (map.status === "SUPPLEMENTAL_SAFE_MAP") {
        if (map.source_evidence.length === 0 || map.edits.length === 0) fail(`Safe map needs evidence and edits for ${item.item_id}/${candidate.label}/${field}.`);
      } else if (map.source_evidence.length !== 0 || map.edits.length !== 0) {
        fail(`Non-safe map cannot contain evidence or edits for ${item.item_id}/${candidate.label}/${field}.`);
      }
      const existingLines = new Set((existing.existing_edits[field] ?? []).flatMap((edit) => Array.from({ length: edit.line_end - edit.line_start + 1 }, (_, index) => edit.line_start + index)));
      const evidenceLines = new Set();
      for (const evidence of map.source_evidence) {
        if (!Number.isInteger(evidence.line_start) || !Number.isInteger(evidence.line_end) || evidence.line_start < 1 || evidence.line_end < evidence.line_start || evidence.line_end > lineCount || typeof evidence.note !== "string") fail(`Invalid source evidence ${item.item_id}/${candidate.label}/${field}.`);
        for (let line = evidence.line_start; line <= evidence.line_end; line += 1) evidenceLines.add(line);
      }
      for (const edit of map.edits) {
        if (!allowedKinds.has(edit.kind) || !Number.isInteger(edit.line_start) || !Number.isInteger(edit.line_end) || edit.line_start < 1 || edit.line_end < edit.line_start || edit.line_end > lineCount || typeof edit.rationale !== "string") fail(`Invalid edit ${item.item_id}/${candidate.label}/${field}.`);
        if (edit.kind === "REWRITE_LINE" && (edit.line_start !== edit.line_end || edit.replacement !== "[information removed]")) fail(`Rewrite must use the approved marker on one line for ${item.item_id}/${candidate.label}/${field}.`);
        if (edit.kind === "DELETE_LINE" && "replacement" in edit && edit.replacement !== "") fail(`Delete cannot carry replacement for ${item.item_id}/${candidate.label}/${field}.`);
        for (let line = edit.line_start; line <= edit.line_end; line += 1) {
          if (!evidenceLines.has(line)) fail(`Edit outside cited source evidence for ${item.item_id}/${candidate.label}/${field}.`);
          if (existingLines.has(line)) fail(`Supplement overlaps existing edit for ${item.item_id}/${candidate.label}/${field}.`);
        }
      }
      decisions += 1;
    }
  }
}
console.log(JSON.stringify({ status: "VALID", batch_id: submission.batch_id, items: seenItems.size, field_candidate_maps: decisions }));
