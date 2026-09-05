#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const baselineRoot = join(root, "materialized_masks");
const baseline = JSON.parse(await readFile(join(baselineRoot, "MASK_MATERIALIZATION_MANIFEST.json"), "utf8"));
const remediationRoot = join(root, "remediation_submissions", "canonical");
const remediationStatus = JSON.parse(await readFile(join(remediationRoot, "INGESTION_STATUS.json"), "utf8"));
if (remediationStatus.status !== "COMPLETE_PENDING_REMATERIALISATION") throw new Error("Remediation maps are not complete.");
const lineage = JSON.parse(await readFile(join(root, "residual_packets", "private_lineage_manifest.json"), "utf8"));
const outputRoot = join(root, "materialized_masks_remediated");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const lineageByItem = new Map(lineage.items.map((entry) => [entry.item_id, entry]));
const baselineByComposition = new Map(baseline.compositions.map((entry) => [entry.composition_id, entry]));
const remediationByItem = new Map();
for (const name of Array.from({ length: 12 }, (_, index) => `batch_${String(index + 1).padStart(2, "0")}.json`)) {
  const submission = JSON.parse(await readFile(join(remediationRoot, name), "utf8"));
  for (const item of submission.items) remediationByItem.set(item.item_id, item);
}

function addEdit(byLine, edit, source, field) {
  const replacement = edit.kind === "DELETE_LINE" ? "" : edit.replacement;
  for (let line = edit.line_start; line <= edit.line_end; line += 1) {
    const existing = byLine.get(line);
    if (existing && existing.replacement !== replacement) return { line, existing, incoming: { replacement, source, field } };
    byLine.set(line, {
      replacement,
      sources: [...new Set([...(existing?.sources ?? []), source])],
      fields: [...new Set([...(existing?.fields ?? []), field])],
    });
  }
  return null;
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const remediated = [];
for (const summary of remediationStatus.item_summary) {
  const itemId = summary.item_id;
  const route = lineageByItem.get(itemId);
  const supplemental = remediationByItem.get(itemId);
  if (!route || !supplemental) throw new Error(`Missing route or remediation map for ${itemId}.`);
  const baselineComposition = baselineByComposition.get(route.composition_id);
  const baselineState = baselineComposition?.conditions[route.condition];
  const entry = { item_id: itemId, composition_id: route.composition_id, condition: route.condition, fields: route.fields };
  if (summary.remediation_status !== "SUPPLEMENTAL_MAPPED") {
    entry.status = "EXCLUDED_UNSAFE_MIXED_CARRIER";
    remediated.push(entry);
    continue;
  }
  if (baselineState?.status !== "MATERIALIZED_PENDING_AUDIT") {
    entry.status = "BASELINE_NOT_MATERIALIZED";
    remediated.push(entry);
    continue;
  }
  const baselineLedger = JSON.parse(await readFile(baselineState.ledger_path, "utf8"));
  const candidateEntries = [];
  let conflict = null;
  for (const baselineCandidate of baselineLedger.candidates) {
    const supplementalCandidate = supplemental.candidates.find((candidate) => candidate.label === baselineCandidate.label);
    const byLine = new Map();
    for (const edit of baselineCandidate.edits) {
      conflict ??= addEdit(byLine, { kind: edit.edit_kinds.includes("REWRITE_LINE") ? "REWRITE_LINE" : "DELETE_LINE", line_start: edit.line, line_end: edit.line, replacement: edit.replacement }, "baseline", edit.fields.join("+"));
    }
    for (const field of route.fields) {
      const map = supplementalCandidate.field_maps[field];
      if (map.status !== "SUPPLEMENTAL_SAFE_MAP") continue;
      for (const edit of map.edits) conflict ??= addEdit(byLine, edit, "supplemental", field);
    }
    if (conflict) break;
    const original = await readFile(baselineCandidate.original_path, "utf8");
    const lines = original.split("\n");
    const edits = [...byLine.entries()].sort(([left], [right]) => left - right).map(([line, edit]) => ({ line, ...edit }));
    for (const edit of edits) lines[edit.line - 1] = edit.replacement;
    const masked = lines.join("\n");
    const dir = join(outputRoot, route.condition, route.composition_id);
    await mkdir(dir, { recursive: true });
    const maskedPath = join(dir, `${baselineCandidate.label}.md`);
    await writeFile(maskedPath, masked);
    candidateEntries.push({
      label: baselineCandidate.label,
      skill_id: baselineCandidate.skill_id,
      original_path: baselineCandidate.original_path,
      masked_path: maskedPath,
      original_sha256: sha256(original),
      masked_sha256: sha256(masked),
      edits,
    });
  }
  if (conflict) {
    entry.status = "EDIT_CONFLICT";
    entry.conflict = conflict;
  } else {
    const ledgerPath = join(outputRoot, route.condition, route.composition_id, "mask_ledger.json");
    await writeFile(ledgerPath, `${JSON.stringify({ status: "MATERIALIZED_REMEDIATED_PENDING_AUDIT", item_id: itemId, composition_id: route.composition_id, condition: route.condition, fields: route.fields, candidates: candidateEntries }, null, 2)}\n`);
    entry.status = "MATERIALIZED_REMEDIATED_PENDING_AUDIT";
    entry.ledger_path = ledgerPath;
    entry.candidates = candidateEntries.map((candidate) => ({ label: candidate.label, original_sha256: candidate.original_sha256, masked_sha256: candidate.masked_sha256, edit_count: candidate.edits.length }));
  }
  remediated.push(entry);
}
const counts = {};
for (const entry of remediated) counts[entry.status] = (counts[entry.status] ?? 0) + 1;
await writeFile(join(outputRoot, "REMEDIATED_MASK_MANIFEST.json"), `${JSON.stringify({
  status: "REMEDIATED_MASKS_PENDING_AUDIT_NO_SELECTOR_EXECUTION",
  remediation_status_sha256: sha256(await readFile(join(remediationRoot, "INGESTION_STATUS.json"))),
  counts,
  items: remediated,
}, null, 2)}\n`);
console.log(JSON.stringify({ status: "REMEDIATED_MASKS_PENDING_AUDIT_NO_SELECTOR_EXECUTION", counts }));
