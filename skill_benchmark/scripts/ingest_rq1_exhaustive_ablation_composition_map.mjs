#!/usr/bin/env node

import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { spawnSync } from "node:child_process";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: ingest_rq1_exhaustive_ablation_composition_map.mjs <submission.json>");
const source = resolve(submissionPath);
const validation = spawnSync(process.execPath, ["skill_benchmark/scripts/validate_rq1_exhaustive_ablation_composition_map.mjs", source], { encoding: "utf8" });
process.stdout.write(validation.stdout);
process.stderr.write(validation.stderr);
if (validation.status !== 0) process.exit(validation.status ?? 1);

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const canonicalCompositionRoot = resolve(root, "expansion_maps", "canonical_compositions");
const canonicalUnitRoot = resolve(root, "expansion_maps", "canonical_units");
const submission = JSON.parse(await readFile(source, "utf8"));
const privateManifest = JSON.parse(await readFile(resolve(root, "expansion_packets", "private_lineage_manifest.json"), "utf8"));
const lineage = privateManifest.items.find((item) => item.composition_unit_id === submission.composition_unit_id);
if (!lineage || lineage.disposition !== "EXPANSION_SOURCE_ONLY_MAPPING") throw new Error(`${submission.composition_unit_id}: invalid private lineage`);

await mkdir(canonicalCompositionRoot, { recursive: true });
await mkdir(canonicalUnitRoot, { recursive: true });
await copyFile(source, resolve(canonicalCompositionRoot, `${submission.composition_unit_id}.json`));

const fields = Object.keys(submission.candidates[0].field_maps);
for (const field of fields) {
  const unit = {
    unit_id: `${submission.composition_unit_id}-${field}`,
    composition_unit_id: submission.composition_unit_id,
    composition_id: lineage.composition_id,
    target_field: field,
    candidates: submission.candidates.map((candidate) => ({
      label: candidate.label,
      status: candidate.field_maps[field].status,
      target_spans: candidate.field_maps[field].target_spans,
    })),
  };
  await writeFile(resolve(canonicalUnitRoot, `${submission.composition_unit_id}-${field}.json`), `${JSON.stringify(unit, null, 2)}\n`);
}
console.log(JSON.stringify({
  status: "INGESTED",
  composition_unit_id: submission.composition_unit_id,
  composition_id: lineage.composition_id,
  canonical_units: fields.length,
}));
