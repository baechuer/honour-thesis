#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const expansionRoot = join(root, "expansion_packets");
const expansionMaps = join(root, "expansion_maps", "canonical_units");
const pilotRoot = join(root, "pilot_packets");
const pilotMaps = join(root, "pilot_maps", "canonical");
const outputRoot = join(root, "canonical_field_map_ledger");
const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];
const sha256 = (text) => createHash("sha256").update(text).digest("hex");

const expansionPrivate = JSON.parse(await readFile(join(expansionRoot, "private_lineage_manifest.json"), "utf8"));
const pilotPrivate = JSON.parse(await readFile(join(pilotRoot, "private_lineage_manifest.json"), "utf8"));
const pilotByCompositionField = new Map(
  pilotPrivate.items.map((item) => [`${item.composition_id}::${item.target_field}`, item]),
);

if (expansionPrivate.items.length !== 82) throw new Error(`Expected 82 compositions, found ${expansionPrivate.items.length}`);
const rows = [];
for (const composition of expansionPrivate.items) {
  for (const field of fields) {
    const pilot = composition.disposition === "PILOT_CANONICAL_REUSE";
    const pilotItem = pilotByCompositionField.get(`${composition.composition_id}::${field}`);
    if (pilot && !pilotItem) throw new Error(`${composition.composition_id}/${field}: missing pilot lineage`);
    const unitId = pilot ? pilotItem.unit_id : `${composition.composition_unit_id}-${field}`;
    const mapPath = pilot ? join(pilotMaps, `${unitId}.json`) : join(expansionMaps, `${unitId}.json`);
    const map = JSON.parse(await readFile(mapPath, "utf8"));
    if (map.target_field !== field) throw new Error(`${unitId}: target field mismatch`);
    if (map.candidates.length !== composition.candidates.length) throw new Error(`${unitId}: candidate count mismatch`);
    const mappedByLabel = new Map(map.candidates.map((candidate) => [candidate.label, candidate]));
    const candidates = [];
    for (const candidate of composition.candidates) {
      const mapped = mappedByLabel.get(candidate.label);
      if (!mapped) throw new Error(`${unitId}: missing ${candidate.label}`);
      const sourcePath = resolve(candidate.packet_source_path ?? candidate.packet_path);
      const source = await readFile(sourcePath, "utf8");
      const expectedHash = candidate.sha256 ?? candidate.source_sha256;
      if (sha256(source) !== expectedHash) throw new Error(`${unitId}/${candidate.label}: source hash mismatch`);
      candidates.push({
        label: candidate.label,
        source_id: candidate.source_id,
        source_path: candidate.source_path,
        canonical_source_path: sourcePath,
        source_sha256: expectedHash,
        map_status: mapped.status,
        target_span_count: mapped.target_spans.length,
      });
    }
    rows.push({
      unit_id: `${composition.composition_id}-${field}`,
      map_unit_id: unitId,
      map_origin: pilot ? "PILOT_CANONICAL_REUSE" : "EXPANSION_CANONICAL",
      composition_unit_id: composition.composition_unit_id,
      composition_id: composition.composition_id,
      registry_id: composition.registry_id,
      source_composition_id: composition.source_composition_id,
      target_field: field,
      canonical_map_path: mapPath,
      candidates,
    });
  }
}

const manifest = {
  status: "RQ1_EXHAUSTIVE_CANONICAL_FIELD_MAP_LEDGER_COMPLETE_NO_SELECTOR",
  boundary: "Source-only canonical field maps and source lineage; no prompts, labels, selector outputs, or routing results.",
  composition_count: 82,
  source_document_count: new Set(rows.flatMap((row) => row.candidates.map((candidate) => candidate.canonical_source_path))).size,
  unique_source_content_hash_count: new Set(rows.flatMap((row) => row.candidates.map((candidate) => candidate.source_sha256))).size,
  field_order: fields,
  field_unit_count: rows.length,
  units: rows,
};
if (manifest.field_unit_count !== 574) throw new Error(`Expected 574 field units, found ${manifest.field_unit_count}`);
if (manifest.source_document_count !== 265) throw new Error(`Expected 265 source documents, found ${manifest.source_document_count}`);
await mkdir(outputRoot, { recursive: true });
const outputPath = join(outputRoot, "CANONICAL_FIELD_MAP_LEDGER.json");
await writeFile(outputPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({
  status: manifest.status,
  compositions: manifest.composition_count,
  source_documents: manifest.source_document_count,
  unique_source_content_hashes: manifest.unique_source_content_hash_count,
  field_units: manifest.field_unit_count,
  sha256: sha256(await readFile(outputPath, "utf8")),
}));
