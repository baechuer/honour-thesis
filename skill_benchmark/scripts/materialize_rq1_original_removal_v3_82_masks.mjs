#!/usr/bin/env node

// Deterministically apply only the frozen S1 source maps. This is a technical
// materialisation step, not a residual or routing evaluation.

import { createHash } from "node:crypto";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const packetRoot = join(root, "eligibility_packets");
const canonicalRoot = join(root, "eligibility_submissions", "canonical");
const ledgerPath = join(root, "eligibility_ledger", "eligibility_ledger.json");
const outputRoot = join(root, "materialized_masks");
const fields = [
  "use_condition", "input_precondition", "output_artifact", "workflow_procedure",
  "success_verification", "boundary_not_for", "dependency_resource",
];
const conditions = {
  REMOVE_USE_CONDITION: ["use_condition"],
  REMOVE_INPUT_PRECONDITION: ["input_precondition"],
  REMOVE_OUTPUT_ARTIFACT: ["output_artifact"],
  REMOVE_WORKFLOW_PROCEDURE: ["workflow_procedure"],
  REMOVE_SUCCESS_VERIFICATION: ["success_verification"],
  REMOVE_BOUNDARY_NOT_FOR: ["boundary_not_for"],
  REMOVE_DEPENDENCY_RESOURCE: ["dependency_resource"],
  REMOVE_TASK_SPECIFICATION: ["use_condition", "input_precondition", "output_artifact"],
  REMOVE_EXECUTION_VERIFICATION: ["workflow_procedure", "success_verification"],
  REMOVE_APPLICABILITY_CAPABILITY: ["boundary_not_for", "dependency_resource"],
};
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function mergeEdits(fieldMaps, conditionFields) {
  const byLine = new Map();
  for (const field of conditionFields) {
    const map = fieldMaps[field];
    if (!map) throw new Error(`Missing field map ${field}.`);
    if (map.status === "NO_DIRECT_VALUE") continue;
    if (map.status !== "SAFE_MAP") throw new Error(`Non-safe field map ${field}.`);
    for (const edit of map.edits) {
      const replacement = edit.kind === "DELETE_LINE" ? "" : edit.replacement;
      for (let line = edit.line_start; line <= edit.line_end; line += 1) {
        const existing = byLine.get(line);
        if (existing && existing.replacement !== replacement) {
          return { conflict: { line, existing, incoming: { field, edit } } };
        }
        byLine.set(line, {
          replacement,
          fields: [...new Set([...(existing?.fields ?? []), field])],
          edit_kinds: [...new Set([...(existing?.edit_kinds ?? []), edit.kind])],
          evidence_ids: [...new Set([...(existing?.evidence_ids ?? []), ...edit.evidence_ids])],
        });
      }
    }
  }
  return {
    edits: [...byLine.entries()]
      .sort(([left], [right]) => left - right)
      .map(([line, edit]) => ({ line, ...edit })),
  };
}

const packetManifest = await readJson(join(packetRoot, "agent_packet_manifest.json"));
const sourceByComposition = new Map(packetManifest.compositions.map((row) => [row.composition_id, row]));
const eligibility = await readJson(ledgerPath);
const mapsByComposition = new Map();
for (let index = 1; index <= 28; index += 1) {
  const batchId = `batch_${String(index).padStart(2, "0")}`;
  const submission = await readJson(join(canonicalRoot, `${batchId}.json`));
  for (const composition of submission.compositions) mapsByComposition.set(composition.composition_id, composition);
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const compositionRows = [];
for (const eligibilityRow of eligibility.rows) {
  const source = sourceByComposition.get(eligibilityRow.composition_id);
  const maps = mapsByComposition.get(eligibilityRow.composition_id);
  if (!source || !maps) throw new Error(`Missing frozen source or map for ${eligibilityRow.composition_id}.`);
  const row = { composition_id: eligibilityRow.composition_id, conditions: {} };
  for (const [condition, conditionFields] of Object.entries(conditions)) {
    const eligible = conditionFields.every((field) => eligibilityRow.conditions[field]?.status === "MAP_READY");
    if (!eligible) {
      row.conditions[condition] = { status: "NOT_MAP_READY", fields: conditionFields };
      continue;
    }
    const candidates = [];
    let conflict = null;
    for (const sourceCandidate of source.candidates) {
      const mapCandidate = maps.candidates.find((candidate) => candidate.label === sourceCandidate.label);
      const merged = mergeEdits(mapCandidate.field_maps, conditionFields);
      if (merged.conflict) {
        conflict = { candidate_label: sourceCandidate.label, ...merged.conflict };
        break;
      }
      const sourcePath = join(packetRoot, source.batch_id, source.composition_id, sourceCandidate.path);
      const original = await readFile(sourcePath, "utf8");
      const originalSha256 = sha256(original);
      if (originalSha256 !== sourceCandidate.sha256) throw new Error(`Source hash mismatch ${source.composition_id}/${sourceCandidate.label}.`);
      const lines = original.split("\n");
      for (const edit of merged.edits) lines[edit.line - 1] = edit.replacement;
      const masked = lines.join("\n");
      const conditionDir = join(outputRoot, condition, source.composition_id);
      await mkdir(conditionDir, { recursive: true });
      const maskedPath = join(conditionDir, `${sourceCandidate.label}.md`);
      await writeFile(maskedPath, masked);
      candidates.push({
        label: sourceCandidate.label,
        source_packet_sha256: sourceCandidate.sha256,
        original_sha256: originalSha256,
        masked_sha256: sha256(masked),
        original_path: sourcePath,
        masked_path: maskedPath,
        edits: merged.edits,
      });
    }
    const conditionDir = join(outputRoot, condition, source.composition_id);
    if (conflict) {
      await rm(conditionDir, { recursive: true, force: true });
      row.conditions[condition] = { status: "EDIT_CONFLICT", fields: conditionFields, conflict };
      continue;
    }
    const ledger = {
      status: "MATERIALIZED_PENDING_TECHNICAL_AUDIT",
      composition_id: source.composition_id,
      condition,
      fields: conditionFields,
      candidates,
    };
    const conditionLedgerPath = join(conditionDir, "mask_ledger.json");
    await writeFile(conditionLedgerPath, `${JSON.stringify(ledger, null, 2)}\n`);
    row.conditions[condition] = {
      status: "MATERIALIZED_PENDING_TECHNICAL_AUDIT",
      fields: conditionFields,
      ledger_path: conditionLedgerPath,
      candidate_count: candidates.length,
    };
  }
  compositionRows.push(row);
}

const summary = {};
for (const condition of Object.keys(conditions)) {
  summary[condition] = {};
  for (const row of compositionRows) {
    const status = row.conditions[condition].status;
    summary[condition][status] = (summary[condition][status] ?? 0) + 1;
  }
}
const manifest = {
  status: "MATERIALIZED_PENDING_TECHNICAL_AUDIT_NO_RESIDUAL_OR_SELECTOR_EXECUTION",
  inputs: {
    eligibility_ledger_path: ledgerPath,
    eligibility_ledger_sha256: sha256(await readFile(ledgerPath, "utf8")),
    canonical_map_root: canonicalRoot,
    source_packet_manifest_sha256: sha256(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8")),
  },
  condition_definitions: conditions,
  summary,
  compositions: compositionRows,
  boundary: "Deterministic source-map application only. This does not test residual information, routing, or retrieval.",
};
await writeFile(join(outputRoot, "MASK_MATERIALIZATION_MANIFEST.json"), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ status: manifest.status, summary }));
