#!/usr/bin/env node

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const masks = JSON.parse(await readFile(join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"));
const outputRoot = join(root, "full_clearance_packets");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const publicItems = [];
const privateItems = [];

for (const unit of masks.single_units) {
  const unitRoot = join(outputRoot, unit.unit_id);
  await mkdir(unitRoot, { recursive: true });
  const publicCandidates = [];
  for (const candidate of unit.candidates) {
    const destination = join(unitRoot, `${candidate.label}.md`);
    await copyFile(candidate.masked_path, destination);
    const text = await readFile(destination, "utf8");
    if (sha256(text) !== candidate.masked_sha256) throw new Error(`${unit.unit_id}/${candidate.label}: copy hash mismatch`);
    publicCandidates.push({ label: candidate.label, path: `${candidate.label}.md`, sha256: candidate.masked_sha256 });
  }
  const packet = {
    status: "RQ1_EXHAUSTIVE_FULL_CLEARANCE_PACKET",
    boundary: "Masked documents and target field only. No prompt, gold label, source identity, source map, candidate role, selector output or routing result.",
    unit_id: unit.unit_id,
    target_field: unit.target_field,
    candidates: publicCandidates,
  };
  await writeFile(join(unitRoot, "packet.json"), `${JSON.stringify(packet, null, 2)}\n`);
  publicItems.push({ unit_id: unit.unit_id, target_field: unit.target_field, packet_path: `${unit.unit_id}/packet.json`, candidates: publicCandidates });
  privateItems.push({
    unit_id: unit.unit_id,
    composition_id: unit.composition_id,
    target_field: unit.target_field,
    candidates: unit.candidates.map((candidate) => ({ label: candidate.label, masked_path: candidate.masked_path, masked_sha256: candidate.masked_sha256 })),
  });
}

const publicManifest = {
  status: "RQ1_EXHAUSTIVE_FULL_CLEARANCE_PACKETS_READY",
  boundary: "Anonymous target-ablated documents only; no prompt, gold, source-map, selector or routing information.",
  unit_count: publicItems.length,
  items: publicItems,
};
const privateManifest = {
  status: "PRIVATE_MAIN_THREAD_LINEAGE_NOT_FOR_REVIEWERS",
  unit_count: privateItems.length,
  items: privateItems,
};
if (publicManifest.unit_count !== 574) throw new Error(`Expected 574 units, found ${publicManifest.unit_count}`);
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify(publicManifest, null, 2)}\n`);
await writeFile(join(outputRoot, "private_lineage_manifest.json"), `${JSON.stringify(privateManifest, null, 2)}\n`);
console.log(JSON.stringify({ status: publicManifest.status, units: publicManifest.unit_count, candidate_documents: publicItems.reduce((sum, item) => sum + item.candidates.length, 0) }));
