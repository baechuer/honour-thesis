#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const waveId = process.argv[2];
const start = Number.parseInt(process.argv[3] ?? "0", 10);
const count = Number.parseInt(process.argv[4] ?? "6", 10);
if (!waveId || !Number.isInteger(start) || !Number.isInteger(count) || start < 0 || count < 1 || count > 6) {
  throw new Error("Usage: build_rq1_exhaustive_ablation_forced_round2_clearance_wave.mjs <wave-id> <start> [count 1-6]");
}

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(await readFile(join(root, "forced_round2_masks", "FORCED_ROUND2_MASK_MANIFEST.json"), "utf8"));
const packetRoot = join(root, "forced_round2_clearance_packets");
const assignmentRoot = join(root, "forced_round2_clearance", "assignments", waveId);
const workRoot = join(root, "forced_round2_clearance", "agent_work_round2");
const compositionIds = [...new Set(manifest.units.map((unit) => unit.composition_id))].sort();
const selected = compositionIds.slice(start, start + count);
if (!selected.length) throw new Error(`No compositions at offset ${start}`);

const assignments = [];
for (const compositionId of selected) {
  const units = manifest.units.filter((unit) => unit.composition_id === compositionId).sort((left, right) => left.target_field.localeCompare(right.target_field));
  if (units.length !== 7) throw new Error(`${compositionId}: expected seven single-field units, found ${units.length}`);
  const assignment = {
    status: "RQ1_FORCED_ROUND2_FRESH_BLIND_CLEARANCE_ASSIGNMENT",
    boundary: "Read only this assignment, the Round-2 SOP, and its listed anonymous packet documents. Do not read originals, source identities, prompts, gold labels, source maps, Round-1 reviews, selector outputs, or results. No network.",
    wave_id: waveId,
    composition_id: compositionId,
    units: units.map((unit) => ({
      unit_id: unit.unit_id,
      target_field: unit.target_field,
      packet_path: join(packetRoot, unit.unit_id, "packet.json"),
      output_path: join(workRoot, `${unit.unit_id}.json`),
    })),
  };
  await mkdir(assignmentRoot, { recursive: true });
  await mkdir(workRoot, { recursive: true });
  const assignmentPath = join(assignmentRoot, `${compositionId}.json`);
  await writeFile(assignmentPath, `${JSON.stringify(assignment, null, 2)}\n`);
  assignments.push({ composition_id: compositionId, assignment_path: assignmentPath, unit_count: units.length });
}

const wave = {
  status: "RQ1_FORCED_ROUND2_FRESH_BLIND_CLEARANCE_WAVE_READY",
  wave_id: waveId,
  start,
  composition_count: assignments.length,
  unit_count: assignments.reduce((sum, row) => sum + row.unit_count, 0),
  assignments,
};
await writeFile(join(assignmentRoot, "WAVE_MANIFEST.json"), `${JSON.stringify(wave, null, 2)}\n`);
console.log(JSON.stringify(wave));
