#!/usr/bin/env node

import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const waveId = process.argv[2];
if (!waveId) throw new Error("Usage: build_rq1_exhaustive_ablation_full_clearance_wave.mjs <wave-id>");
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(await readFile(join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"));
const publicPackets = JSON.parse(await readFile(join(root, "full_clearance_packets", "agent_packet_manifest.json"), "utf8"));
const assignmentRoot = join(root, "full_clearance", "round1_assignments");
const canonicalRoot = join(root, "full_clearance", "canonical_round1");
const outputPath = join(assignmentRoot, `${waveId}.json`);
try { await readFile(outputPath, "utf8"); throw new Error(`${waveId} already exists; do not overwrite an assignment wave`); } catch (error) { if (error.code !== "ENOENT") throw error; }
let reviewedNames = [];
try { reviewedNames = (await readdir(canonicalRoot)).filter((name) => name.endsWith(".json")); } catch (error) { if (error.code !== "ENOENT") throw error; }
const reviewed = new Set(reviewedNames.map((name) => name.replace(/\.json$/u, "")));
const packetByUnit = new Map(publicPackets.items.map((item) => [item.unit_id, item]));
const fieldOrder = manifest.single_units.map((unit) => unit.target_field).filter((field, index, all) => all.indexOf(field) === index);
const remainingByComposition = new Map();
const reviewedByField = new Map(fieldOrder.map((field) => [field, 0]));
for (const unit of manifest.single_units) {
  if (reviewed.has(unit.unit_id)) {
    reviewedByField.set(unit.target_field, reviewedByField.get(unit.target_field) + 1);
    continue;
  }
  const rows = remainingByComposition.get(unit.composition_id) ?? [];
  rows.push(unit);
  remainingByComposition.set(unit.composition_id, rows);
}
const selected = [];
const selectedByField = new Map(fieldOrder.map((field) => [field, 0]));
for (const compositionId of [...remainingByComposition.keys()].sort()) {
  if (selected.length >= 18) break;
  const candidates = remainingByComposition.get(compositionId);
  candidates.sort((left, right) => {
    const leftScore = reviewedByField.get(left.target_field) + selectedByField.get(left.target_field);
    const rightScore = reviewedByField.get(right.target_field) + selectedByField.get(right.target_field);
    return leftScore - rightScore || fieldOrder.indexOf(left.target_field) - fieldOrder.indexOf(right.target_field);
  });
  const selectedUnit = candidates[0];
  selected.push(selectedUnit);
  selectedByField.set(selectedUnit.target_field, selectedByField.get(selectedUnit.target_field) + 1);
}
const batches = Array.from({ length: Math.ceil(selected.length / 3) }, (_, index) => selected.slice(index * 3, index * 3 + 3));
const assignment = {
  status: "RQ1_EXHAUSTIVE_FULL_CLEARANCE_ROUND1_ASSIGNMENT",
  wave_id: waveId,
  boundary: "Blind residual-clearance assignment only; no source originals, source maps, prompts, gold labels, candidate roles, selectors, metrics or routing results.",
  reviewer_batch_count: batches.length,
  batches: batches.map((units, index) => ({
    batch_id: `${waveId}-B${String(index + 1).padStart(2, "0")}`,
    units: units.map((unit) => {
      const packet = packetByUnit.get(unit.unit_id);
      if (!packet) throw new Error(`${unit.unit_id}: missing public packet`);
      return { unit_id: unit.unit_id, target_field: unit.target_field, packet_path: join(root, "full_clearance_packets", packet.packet_path), output_path: join(root, "full_clearance", "agent_work_round1", `${unit.unit_id}.json`) };
    }),
  })),
};
await mkdir(assignmentRoot, { recursive: true });
await mkdir(join(root, "full_clearance", "agent_work_round1"), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assignment, null, 2)}\n`);
console.log(JSON.stringify({ status: assignment.status, wave_id: waveId, reviewer_batches: assignment.reviewer_batch_count, unit_count: selected.length, units: selected.map((unit) => unit.unit_id) }));
