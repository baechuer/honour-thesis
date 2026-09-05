#!/usr/bin/env node

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join, relative } from "node:path";

const repoRoot = process.cwd();
const inputPath = join(
  repoRoot,
  "skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json",
);
const outputRoot = join(repoRoot, "skill_benchmark/rq1_public_original_removal_v2/source_packets");
const batchSize = 3;

const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const roster = JSON.parse(await readFile(inputPath, "utf8"));
if (!Array.isArray(roster.rows) || roster.counts?.compositions !== 76) {
  throw new Error("Unexpected frozen roster shape or composition count.");
}

const compositions = new Map();
for (const row of roster.rows) {
  const key = JSON.stringify([...row.candidate_composition_key].sort());
  const signature = JSON.stringify(
    [...row.candidates]
      .map((candidate) => ({
        skill_id: candidate.skill_id,
        source_sha256: candidate.source_sha256,
        source_path: candidate.canonical_source.packet_original_path,
      }))
      .sort((a, b) => a.skill_id.localeCompare(b.skill_id)),
  );
  const existing = compositions.get(key);
  if (existing && existing.signature !== signature) {
    throw new Error(`Inconsistent candidate membership for composition ${key}`);
  }
  if (!existing) compositions.set(key, { key, signature, candidates: row.candidates });
}

if (compositions.size !== 76) {
  throw new Error(`Expected 76 unique compositions, found ${compositions.size}.`);
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });

const privateManifest = [];
const agentManifest = [];
const ordered = [...compositions.values()].sort((a, b) => a.key.localeCompare(b.key));

for (let index = 0; index < ordered.length; index += 1) {
  const composition = ordered[index];
  const opaqueId = `ODR-${String(index + 1).padStart(3, "0")}`;
  const batchId = `batch_${String(Math.floor(index / batchSize) + 1).padStart(2, "0")}`;
  const packetDir = join(outputRoot, batchId, opaqueId);
  await mkdir(packetDir, { recursive: true });

  const candidates = [...composition.candidates].sort((a, b) => a.skill_id.localeCompare(b.skill_id));
  const packetCandidates = [];
  const privateCandidates = [];
  for (let candidateIndex = 0; candidateIndex < candidates.length; candidateIndex += 1) {
    const candidate = candidates[candidateIndex];
    const label = `candidate_${String.fromCharCode(97 + candidateIndex)}`;
    const sourcePath = candidate.canonical_source.packet_original_path;
    const sourceBytes = await readFile(sourcePath);
    const actualSha = sha256(sourceBytes);
    if (actualSha !== candidate.source_sha256) {
      throw new Error(`Source hash mismatch for ${candidate.skill_id}.`);
    }
    const packetPath = join(packetDir, `${label}.md`);
    await copyFile(sourcePath, packetPath);
    packetCandidates.push({ label, sha256: actualSha, path: `${label}.md` });
    privateCandidates.push({
      label,
      skill_id: candidate.skill_id,
      source_sha256: actualSha,
      source_path: relative(repoRoot, sourcePath),
      packet_path: relative(repoRoot, packetPath),
    });
  }
  const publicPacket = { composition_id: opaqueId, candidates: packetCandidates };
  await writeFile(join(packetDir, "packet.json"), `${JSON.stringify(publicPacket, null, 2)}\n`);
  agentManifest.push({ batch_id: batchId, composition_id: opaqueId, candidates: packetCandidates });
  privateManifest.push({
    batch_id: batchId,
    composition_id: opaqueId,
    candidate_composition_key: JSON.parse(composition.key),
    candidates: privateCandidates,
  });
}

await writeFile(
  join(outputRoot, "agent_packet_manifest.json"),
  `${JSON.stringify({ status: "SOURCE_ONLY_PARSE_READY", batch_size: batchSize, compositions: agentManifest }, null, 2)}\n`,
);
await writeFile(
  join(outputRoot, "private_lineage_manifest.json"),
  `${JSON.stringify({ source_roster: relative(repoRoot, inputPath), compositions: privateManifest }, null, 2)}\n`,
);

console.log(JSON.stringify({ compositions: ordered.length, batches: Math.ceil(ordered.length / batchSize), output: relative(repoRoot, outputRoot) }));
