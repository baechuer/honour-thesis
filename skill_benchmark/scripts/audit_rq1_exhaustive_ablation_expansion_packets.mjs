#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "expansion_packets");
const publicPath = join(root, "agent_packet_manifest.json");
const privatePath = join(root, "private_lineage_manifest.json");
const publicManifest = JSON.parse(await readFile(publicPath, "utf8"));
const privateManifest = JSON.parse(await readFile(privatePath, "utf8"));
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const errors = [];
let candidateDocuments = 0;

if (privateManifest.source_registry_compositions !== 82) errors.push("private source registry count is not 82");
if (publicManifest.items.length !== 80) errors.push(`expected 80 expansion items, found ${publicManifest.items.length}`);
if (privateManifest.items.length !== 82) errors.push(`expected 82 private lineage items, found ${privateManifest.items.length}`);
if (privateManifest.items.filter((item) => item.disposition === "PILOT_CANONICAL_REUSE").length !== 2) errors.push("pilot reuse count is not 2");

for (const item of publicManifest.items) {
  const lineage = privateManifest.items.find((entry) => entry.composition_unit_id === item.composition_unit_id);
  if (!lineage || lineage.disposition !== "EXPANSION_SOURCE_ONLY_MAPPING") {
    errors.push(`${item.composition_unit_id}: missing expansion lineage`);
    continue;
  }
  const packetPath = join(root, item.packet_path);
  const packet = JSON.parse(await readFile(packetPath, "utf8"));
  if (packet.composition_unit_id !== item.composition_unit_id) errors.push(`${item.composition_unit_id}: packet id mismatch`);
  if (Object.keys(packet.field_definitions).length !== 7) errors.push(`${item.composition_unit_id}: field count is not 7`);
  if (JSON.stringify(packet.candidates) !== JSON.stringify(item.candidates)) errors.push(`${item.composition_unit_id}: packet candidates differ from manifest`);
  if (JSON.stringify(item.candidates.map((candidate) => candidate.label)) !== JSON.stringify(lineage.candidates.map((candidate) => candidate.label))) {
    errors.push(`${item.composition_unit_id}: private/public candidate order mismatch`);
  }
  for (const candidate of item.candidates) {
    const bytes = await readFile(join(root, item.composition_unit_id, candidate.path));
    if (sha256(bytes) !== candidate.sha256) errors.push(`${item.composition_unit_id}/${candidate.label}: packet source hash mismatch`);
    const privateCandidate = lineage.candidates.find((entry) => entry.label === candidate.label);
    if (!privateCandidate || privateCandidate.sha256 !== candidate.sha256) errors.push(`${item.composition_unit_id}/${candidate.label}: private hash mismatch`);
    candidateDocuments += 1;
  }
}

const publicBytes = await readFile(publicPath);
const privateBytes = await readFile(privatePath);
const audit = {
  status: errors.length ? "FAIL" : "PASS",
  source_registry_compositions: privateManifest.source_registry_compositions,
  expansion_compositions: publicManifest.items.length,
  pilot_reuse_compositions: privateManifest.items.filter((item) => item.disposition === "PILOT_CANONICAL_REUSE").length,
  composition_field_units: privateManifest.source_registry_compositions * publicManifest.field_order.length,
  expansion_candidate_documents: candidateDocuments,
  field_order: publicManifest.field_order,
  agent_packet_manifest_sha256: sha256(publicBytes),
  private_lineage_manifest_sha256: sha256(privateBytes),
  errors,
};
await mkdir(join(root, "audit"), { recursive: true });
await writeFile(join(root, "audit", "packet_audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
console.log(JSON.stringify(audit));
if (errors.length) process.exit(1);
