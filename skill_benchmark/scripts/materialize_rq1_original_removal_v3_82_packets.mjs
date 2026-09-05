#!/usr/bin/env node

// Build one source-only packet set for the canonical 82-composition registry.
// It deliberately does not inspect prompts, labels, selectors, or prior scores.

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { basename, isAbsolute, join, relative, resolve } from "node:path";

const repo = process.cwd();
const oldRoot = join(repo, "skill_benchmark/rq1_public_original_removal_v2");
const outputRoot = join(repo, "skill_benchmark/rq1_public_original_removal_v3_82_registry");
const publicRegistry = join(repo, "skill_benchmark/rq1b_final_public_corpus_v1/composition_registry.jsonl");
const sourceFrame = join(repo, "skill_benchmark/rq1b_v3_public_source_frame");
const batchSize = 3;
const c6Files = [
  "c4b_blind_review_wave_001_v2_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
  "c4b_blind_review_wave_029_2026-08-30/c6_freeze/c6_frozen_strict_cases.jsonl",
  "d1_directed_discovery_wave_032_2026-08-30/c6_strict_freeze_wave_032_2026-08-30/c6_frozen_strict_cases.jsonl",
  "d1_directed_discovery_wave_033_2026-08-30/c6_strict_freeze_wave_033_2026-08-30/c6_frozen_strict_cases.jsonl",
];

const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const sourceSignature = (hashes) => [...hashes].sort().join("|");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const readJsonl = async (path) => (await readFile(path, "utf8"))
  .split("\n")
  .filter(Boolean)
  .map(JSON.parse);

async function walk(root, matching, found = []) {
  const entries = await (await import("node:fs/promises")).readdir(root, { withFileTypes: true });
  for (const entry of entries) {
    const path = join(root, entry.name);
    if (entry.isDirectory()) await walk(path, matching, found);
    else if (matching(entry.name)) found.push(path);
  }
  return found;
}

async function buildV3SourceIndex() {
  const manifests = await walk(
    sourceFrame,
    (name) => name === "canonical_sources.jsonl" || name === "canonical_sources_amendment.jsonl" || name === "source_manifest.jsonl",
  );
  const index = new Map();
  for (const manifest of manifests) {
    for (const row of await readJsonl(manifest)) {
      if (!row.sha256 || !row.canonical?.absolute_path) continue;
      const sourcePath = isAbsolute(row.canonical.absolute_path)
        ? row.canonical.absolute_path
        : resolve(repo, row.canonical.absolute_path);
      if (!index.has(row.sha256)) index.set(row.sha256, { sourcePath, sourceId: row.source_id ?? null });
    }
  }
  return index;
}

const oldLineage = await readJson(join(oldRoot, "source_packets/private_lineage_manifest.json"));
if (oldLineage.compositions.length !== 76) throw new Error("Expected exactly 76 historical source compositions.");

const oldBySignature = new Map();
for (const composition of oldLineage.compositions) {
  const key = sourceSignature(composition.candidates.map((candidate) => candidate.source_sha256));
  if (oldBySignature.has(key)) throw new Error(`Historical duplicate composition signature: ${key}`);
  oldBySignature.set(key, composition);
}

const v3BySignature = new Map();
for (const relativeC6Path of c6Files) {
  for (const row of await readJsonl(join(sourceFrame, relativeC6Path))) {
    const hashes = row.candidate_source_hashes.map((candidate) => candidate.source_sha256 ?? candidate);
    const key = sourceSignature(hashes);
    const existing = v3BySignature.get(key);
    if (existing && existing.compositionId !== row.composition_id) throw new Error(`V3 source signature has conflicting composition IDs: ${key}`);
    if (!existing) {
      v3BySignature.set(key, {
        compositionId: row.composition_id,
        candidates: row.candidate_source_hashes.map((candidate) => ({
          sourceSha256: candidate.source_sha256 ?? candidate,
          sourceId: candidate.source_id ?? null,
        })),
      });
    }
  }
}
if (v3BySignature.size !== 6) throw new Error(`Expected 6 direct-V3 compositions, found ${v3BySignature.size}.`);

const registryRows = await readJsonl(publicRegistry);
if (registryRows.length !== 82) throw new Error(`Expected 82 registry compositions, found ${registryRows.length}.`);

const v3SourceIndex = await buildV3SourceIndex();
const sourceCompositions = [];
for (const registryRow of registryRows) {
  const hashes = registryRow.candidate_source_sha256;
  const key = sourceSignature(hashes);
  const old = oldBySignature.get(key);
  const v3 = v3BySignature.get(key);
  if (old && v3) throw new Error(`Unexpected historical/V3 signature overlap: ${key}`);
  if (!old && !v3) throw new Error(`Registry composition cannot be sourced from the frozen 76+6 inputs: ${key}`);

  if (old) {
    sourceCompositions.push({
      registryId: registryRow.registry_id,
      lineage: "HISTORICAL_76_REUSED_SOURCE_ONLY_PARSE",
      sourceCompositionId: old.composition_id,
      sourceCandidates: old.candidates.map((candidate) => ({
        sourceSha256: candidate.source_sha256,
        sourcePath: resolve(repo, candidate.source_path),
        sourceId: candidate.skill_id,
      })),
    });
  } else {
    sourceCompositions.push({
      registryId: registryRow.registry_id,
      lineage: "DIRECT_V3_NEW_SOURCE_ONLY_PARSE",
      sourceCompositionId: v3.compositionId,
      sourceCandidates: v3.candidates.map((candidate) => {
        const indexed = v3SourceIndex.get(candidate.sourceSha256);
        if (!indexed) throw new Error(`No local source-frame path for V3 source ${candidate.sourceSha256}.`);
        return {
          sourceSha256: candidate.sourceSha256,
          sourcePath: indexed.sourcePath,
          sourceId: candidate.sourceId ?? indexed.sourceId,
        };
      }),
    });
  }
}

const counts = sourceCompositions.reduce(
  (acc, composition) => {
    acc[composition.lineage] = (acc[composition.lineage] ?? 0) + 1;
    acc.candidates += composition.sourceCandidates.length;
    return acc;
  },
  { candidates: 0 },
);
if (sourceCompositions.length !== 82 || counts.HISTORICAL_76_REUSED_SOURCE_ONLY_PARSE !== 76 || counts.DIRECT_V3_NEW_SOURCE_ONLY_PARSE !== 6 || counts.candidates !== 265) {
  throw new Error(`Unexpected merged source composition counts: ${JSON.stringify(counts)}`);
}

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite existing output root: ${relative(repo, outputRoot)}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

await mkdir(join(outputRoot, "source_packets"), { recursive: true });
const privateCompositions = [];
const publicCompositions = [];
for (const [index, composition] of sourceCompositions.sort((a, b) => a.registryId.localeCompare(b.registryId)).entries()) {
  const compositionId = `OR82-${String(index + 1).padStart(3, "0")}`;
  const batchId = `batch_${String(Math.floor(index / batchSize) + 1).padStart(2, "0")}`;
  const packetDir = join(outputRoot, "source_packets", batchId, compositionId);
  await mkdir(packetDir, { recursive: true });

  const privateCandidates = [];
  const publicCandidates = [];
  for (const [candidateIndex, candidate] of composition.sourceCandidates.entries()) {
    const label = `candidate_${String.fromCharCode(97 + candidateIndex)}`;
    const bytes = await readFile(candidate.sourcePath);
    const actualSha256 = digest(bytes);
    if (actualSha256 !== candidate.sourceSha256) {
      throw new Error(`Source hash mismatch for ${composition.registryId}/${candidate.sourceId ?? basename(candidate.sourcePath)}.`);
    }
    const packetPath = join(packetDir, `${label}.md`);
    await copyFile(candidate.sourcePath, packetPath);
    privateCandidates.push({
      label,
      source_sha256: actualSha256,
      source_id: candidate.sourceId,
      source_path: relative(repo, candidate.sourcePath),
      packet_path: relative(repo, packetPath),
    });
    publicCandidates.push({ label, sha256: actualSha256, path: `${label}.md` });
  }
  await writeFile(join(packetDir, "packet.json"), `${JSON.stringify({ composition_id: compositionId, candidates: publicCandidates }, null, 2)}\n`);
  privateCompositions.push({
    batch_id: batchId,
    composition_id: compositionId,
    registry_id: composition.registryId,
    source_composition_id: composition.sourceCompositionId,
    lineage: composition.lineage,
    candidate_source_sha256: privateCandidates.map((candidate) => candidate.source_sha256).sort(),
    candidates: privateCandidates,
  });
  publicCompositions.push({ batch_id: batchId, composition_id: compositionId, candidates: publicCandidates });
}

await writeFile(
  join(outputRoot, "source_packets", "private_lineage_manifest.json"),
  `${JSON.stringify({
    status: "RQ1_ORIGINAL_REMOVAL_V3_82_SOURCE_ONLY_PARSE_READY",
    canonical_registry: relative(repo, publicRegistry),
    source_counts: { compositions: 82, candidates: 265, historical_reused: 76, v3_new: 6 },
    compositions: privateCompositions,
  }, null, 2)}\n`,
);
await writeFile(
  join(outputRoot, "source_packets", "agent_packet_manifest.json"),
  `${JSON.stringify({
    status: "SOURCE_ONLY_PARSE_READY",
    batch_size: batchSize,
    compositions: publicCompositions,
  }, null, 2)}\n`,
);
await writeFile(
  join(outputRoot, "README.md"),
  "# RQ1 Public Original-Document Removal v3 (82 Registry)\n\n"
    + "Source-only parsing frame for the canonical 82-composition public registry. "
    + "It contains no prompts, gold labels, selector results, embeddings, or masks. "
    + "Historical 76 compositions may reuse verified source-only parse records; six direct-V3 compositions require new source-only parsing.\n",
);

console.log(JSON.stringify({ status: "PASS", output: relative(repo, outputRoot), batches: Math.ceil(sourceCompositions.length / batchSize), ...counts }, null, 2));
