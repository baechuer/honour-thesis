#!/usr/bin/env node

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(await readFile(join(root, "forced_round3_masks", "FORCED_ROUND3_MASK_MANIFEST.json"), "utf8"));
const outputRoot = join(root, "forced_round3_clearance_packets");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const items = [];

for (const unit of manifest.units) {
  const unitRoot = join(outputRoot, unit.unit_id);
  await mkdir(unitRoot, { recursive: true });
  const candidates = [];
  for (const candidate of unit.candidates) {
    const destination = join(unitRoot, `${candidate.label}.md`);
    await copyFile(candidate.round3_masked_path, destination);
    const text = await readFile(destination, "utf8");
    if (sha256(text) !== candidate.round3_masked_sha256) throw new Error(`${unit.unit_id}/${candidate.label}: copy hash mismatch`);
    candidates.push({ label: candidate.label, path: `${candidate.label}.md`, sha256: candidate.round3_masked_sha256 });
  }
  await writeFile(join(unitRoot, "packet.json"), `${JSON.stringify({
    status: "RQ1_FORCED_ROUND3_FRESH_BLIND_CLEARANCE_PACKET",
    boundary: "Anonymous Round-3 masked documents and target field only. No original, prompt, gold label, source identity, field map, prior clearance, selector output, or routing result.",
    unit_id: unit.unit_id,
    target_field: unit.target_field,
    candidates,
  }, null, 2)}\n`);
  items.push({ unit_id: unit.unit_id, composition_id: unit.composition_id, target_field: unit.target_field, packet_path: `${unit.unit_id}/packet.json`, candidates });
}

const packetManifest = {
  status: "RQ1_FORCED_ROUND3_FRESH_BLIND_CLEARANCE_PACKETS_READY",
  boundary: "Reviewers receive only anonymous Round-3 masked documents and the target-field category.",
  unit_count: items.length,
  candidate_count: items.reduce((sum, item) => sum + item.candidates.length, 0),
  items,
};
if (packetManifest.unit_count !== 574 || packetManifest.candidate_count !== 1855) throw new Error(`Unexpected coverage ${JSON.stringify(packetManifest)}`);
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify(packetManifest, null, 2)}\n`);
console.log(JSON.stringify({ status: packetManifest.status, units: packetManifest.unit_count, candidates: packetManifest.candidate_count }));
