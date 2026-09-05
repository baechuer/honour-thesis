#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const sourceRoot = join(root, "source_packets");
const lineagePath = join(sourceRoot, "private_lineage_manifest.json");
const mapsRoot = join(root, "redaction_submissions", "canonical");
const eligibilityPath = join(root, "family_field_eligibility.json");
const outputRoot = join(root, "materialized_masks");
const singleConditions = {
  REMOVE_USE_ORIGINAL: ["use_condition"],
  REMOVE_INPUT_ORIGINAL: ["input_precondition"],
  REMOVE_OUTPUT_ORIGINAL: ["output_artifact"],
  REMOVE_WORKFLOW_ORIGINAL: ["workflow_procedure"],
  REMOVE_SUCCESS_ORIGINAL: ["success_verification"],
  REMOVE_BOUNDARY_ORIGINAL: ["boundary_not_for"],
  REMOVE_DEPENDENCY_ORIGINAL: ["dependency_resource"],
};
const groupConditions = {
  REMOVE_TASK_SPECIFICATION_ORIGINAL: ["use_condition", "input_precondition", "output_artifact"],
  REMOVE_EXECUTION_VERIFICATION_ORIGINAL: ["workflow_procedure", "success_verification"],
  REMOVE_APPLICABILITY_CAPABILITY_ORIGINAL: ["boundary_not_for", "dependency_resource"],
};
const conditions = { ...singleConditions, ...groupConditions };
const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const lineage = JSON.parse(await readFile(lineagePath, "utf8"));
const eligibility = JSON.parse(await readFile(eligibilityPath, "utf8"));
const mapsByComposition = new Map();
for (const batch of Array.from({ length: 26 }, (_, index) => `batch_${String(index + 1).padStart(2, "0")}`)) {
  const submission = JSON.parse(await readFile(join(mapsRoot, `${batch}.json`), "utf8"));
  for (const composition of submission.compositions) mapsByComposition.set(composition.composition_id, composition);
}
const availabilityByComposition = new Map(eligibility.composition_conditions.map((entry) => [entry.composition_id, entry.condition_availability]));

function mergeEdits(fieldMaps, fields) {
  const byLine = new Map();
  for (const field of fields) {
    const map = fieldMaps[field];
    if (map.status === "NO_DIRECT_VALUE") continue;
    if (map.status !== "SAFE_MAP") throw new Error(`Unsafe field map ${field}.`);
    for (const edit of map.edits) {
      for (let line = edit.line_start; line <= edit.line_end; line += 1) {
        const replacement = edit.kind === "DELETE_LINE" ? "" : edit.replacement;
        const existing = byLine.get(line);
        if (existing && existing.replacement !== replacement) {
          return { conflict: { line, existing, incoming: edit } };
        }
        byLine.set(line, { replacement, fields: [...new Set([...(existing?.fields ?? []), field])], edit_kinds: [...new Set([...(existing?.edit_kinds ?? []), edit.kind])], evidence_ids: [...new Set([...(existing?.evidence_ids ?? []), ...edit.evidence_ids])] });
      }
    }
  }
  return { edits: [...byLine.entries()].sort(([left], [right]) => left - right).map(([line, edit]) => ({ line, ...edit })) };
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const manifest = [];
for (const sourceComposition of lineage.compositions) {
  const compositionId = sourceComposition.composition_id;
  const reviewMap = mapsByComposition.get(compositionId);
  const availability = availabilityByComposition.get(compositionId);
  const compositionEntry = { composition_id: compositionId, conditions: {} };
  for (const [conditionName, fields] of Object.entries(conditions)) {
    const simpleKey = Object.entries(singleConditions).find(([, value]) => value.length === 1 && value[0] === fields[0])?.[1]?.[0];
    const isGroup = fields.length > 1;
    const materialisable = isGroup
      ? fields.every((field) => availability[field]?.materialisable)
      : availability[simpleKey]?.materialisable;
    if (!materialisable) {
      compositionEntry.conditions[conditionName] = { status: "NOT_MATERIALISABLE", fields };
      continue;
    }
    const candidateEntries = [];
    let conflict = null;
    for (const candidate of sourceComposition.candidates) {
      const mapCandidate = reviewMap.candidates.find((entry) => entry.label === candidate.label);
      const merged = mergeEdits(mapCandidate.field_maps, fields);
      if (merged.conflict) {
        conflict = { candidate_label: candidate.label, ...merged.conflict };
        break;
      }
      const sourcePath = join(sourceRoot, sourceComposition.batch_id, compositionId, `${candidate.label}.md`);
      const original = await readFile(sourcePath, "utf8");
      const lines = original.split("\n");
      for (const edit of merged.edits) lines[edit.line - 1] = edit.replacement;
      const masked = lines.join("\n");
      const conditionDir = join(outputRoot, conditionName, compositionId);
      await mkdir(conditionDir, { recursive: true });
      const maskedPath = join(conditionDir, `${candidate.label}.md`);
      await writeFile(maskedPath, masked);
      candidateEntries.push({
        label: candidate.label,
        skill_id: candidate.skill_id,
        original_sha256: sha256(original),
        masked_sha256: sha256(masked),
        original_path: sourcePath,
        masked_path: maskedPath,
        edits: merged.edits,
      });
    }
    if (conflict) {
      await rm(join(outputRoot, conditionName, compositionId), { recursive: true, force: true });
      compositionEntry.conditions[conditionName] = { status: "EDIT_CONFLICT", fields, conflict };
    } else {
      const ledgerPath = join(outputRoot, conditionName, compositionId, "mask_ledger.json");
      const ledger = { status: "MATERIALIZED_PENDING_AUDIT", composition_id: compositionId, condition: conditionName, fields, candidates: candidateEntries };
      await writeFile(ledgerPath, `${JSON.stringify(ledger, null, 2)}\n`);
      compositionEntry.conditions[conditionName] = { status: "MATERIALIZED_PENDING_AUDIT", fields, ledger_path: ledgerPath, candidates: candidateEntries.map((candidate) => ({ label: candidate.label, original_sha256: candidate.original_sha256, masked_sha256: candidate.masked_sha256, edit_count: candidate.edits.length })) };
    }
  }
  manifest.push(compositionEntry);
}

const summary = {};
for (const conditionName of Object.keys(conditions)) {
  summary[conditionName] = {};
  for (const entry of manifest) {
    const status = entry.conditions[conditionName].status;
    summary[conditionName][status] = (summary[conditionName][status] ?? 0) + 1;
  }
}
await writeFile(join(outputRoot, "MASK_MATERIALIZATION_MANIFEST.json"), `${JSON.stringify({
  status: "MATERIALIZED_PENDING_AUDIT_NO_SELECTOR_EXECUTION",
  inputs: { eligibility_path: eligibilityPath, eligibility_sha256: sha256(await readFile(eligibilityPath)), redaction_map_root: mapsRoot },
  condition_definitions: conditions,
  summary,
  compositions: manifest,
}, null, 2)}\n`);
console.log(JSON.stringify({ status: "MATERIALIZED_PENDING_AUDIT_NO_SELECTOR_EXECUTION", summary }));
