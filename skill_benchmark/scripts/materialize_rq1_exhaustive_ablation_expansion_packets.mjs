#!/usr/bin/env node

import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { basename, join, resolve } from "node:path";

const workspace = resolve(".");
const sourceRoot = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const outputRoot = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "expansion_packets");
const sourceManifest = JSON.parse(await readFile(join(sourceRoot, "source_packets", "private_lineage_manifest.json"), "utf8"));
const pilotIds = new Set(["OR82-006", "OR82-017"]);
const fieldDefinitions = {
  use_condition: "Situations, goals, triggers, user intents, or operating circumstances under which this candidate should be selected.",
  input_precondition: "Required input objects, formats, states, schemas, prior artifacts, permissions, credentials, or other prerequisites.",
  output_artifact: "The concrete artifact, representation, report, file, transformed object, or other result the candidate produces.",
  workflow_procedure: "Ordered actions, methods, algorithms, decision paths, commands, or worked procedures used to perform the task.",
  success_verification: "Checks, thresholds, tests, evidence, or observable states that define or verify successful completion.",
  boundary_not_for: "Exclusions, unsupported cases, handoff conditions, prohibited uses, limitations, or circumstances where the candidate should not be selected.",
  dependency_resource: "Required tools, packages, services, APIs, companion skills, references, assets, models, runtimes, or external resources.",
};
const sha256 = (buffer) => createHash("sha256").update(buffer).digest("hex");

if (sourceManifest.compositions.length !== 82) {
  throw new Error(`Expected 82 source compositions, found ${sourceManifest.compositions.length}`);
}

await mkdir(outputRoot, { recursive: true });
const publicItems = [];
const privateItems = [];
let sequence = 1;
for (const composition of [...sourceManifest.compositions].sort((left, right) => left.composition_id.localeCompare(right.composition_id))) {
  const compositionUnitId = `EXA-C${String(sequence).padStart(3, "0")}`;
  sequence += 1;
  if (pilotIds.has(composition.composition_id)) {
    privateItems.push({
      composition_unit_id: compositionUnitId,
      disposition: "PILOT_CANONICAL_REUSE",
      composition_id: composition.composition_id,
      registry_id: composition.registry_id,
      source_composition_id: composition.source_composition_id,
      candidates: composition.candidates,
    });
    continue;
  }

  const unitRoot = join(outputRoot, compositionUnitId);
  await mkdir(unitRoot, { recursive: true });
  const candidates = [];
  const privateCandidates = [];
  for (const candidate of composition.candidates) {
    const sourcePath = resolve(workspace, candidate.packet_path);
    const bytes = await readFile(sourcePath);
    const actualSha = sha256(bytes);
    if (actualSha !== candidate.source_sha256) {
      throw new Error(`${composition.composition_id}/${candidate.label}: source hash mismatch`);
    }
    const destination = join(unitRoot, `${candidate.label}.md`);
    await copyFile(sourcePath, destination);
    candidates.push({ label: candidate.label, path: basename(destination), sha256: actualSha });
    privateCandidates.push({
      label: candidate.label,
      source_id: candidate.source_id,
      source_path: candidate.source_path,
      packet_source_path: candidate.packet_path,
      sha256: actualSha,
    });
  }

  const packet = {
    composition_unit_id: compositionUnitId,
    field_definitions: fieldDefinitions,
    instructions: [
      "Read every candidate document in full once and independently map all seven target fields.",
      "For each field, map every complete source line carrying explicit or semantically equivalent candidate-specific information.",
      "A line may be mapped to multiple fields. Mixed carriers may be deleted and must list every collateral operational field.",
      "Within one candidate-field map, use non-overlapping complete line ranges and quote each range exactly, joined by newline.",
      "Do not preserve executability. Do not invent, paraphrase, broaden, replace, or summarise capability text.",
      "Use NO_TARGET_CUE only when the full candidate document contains no candidate-specific value for that field.",
      "Do not infer prompts, gold labels, candidate roles, source identities, or routing outcomes."
    ],
    candidates,
  };
  await writeFile(join(unitRoot, "packet.json"), `${JSON.stringify(packet, null, 2)}\n`);
  publicItems.push({
    composition_unit_id: compositionUnitId,
    packet_path: `${compositionUnitId}/packet.json`,
    candidates,
  });
  privateItems.push({
    composition_unit_id: compositionUnitId,
    disposition: "EXPANSION_SOURCE_ONLY_MAPPING",
    composition_id: composition.composition_id,
    registry_id: composition.registry_id,
    source_composition_id: composition.source_composition_id,
    candidates: privateCandidates,
  });
}

const publicManifest = {
  status: "RQ1_EXHAUSTIVE_EXPANSION_SOURCE_ONLY_PACKETS",
  boundary: "No prompt, gold label, candidate role, selector output, historical routing result, or external service input.",
  field_order: Object.keys(fieldDefinitions),
  items: publicItems,
};
const privateManifest = {
  status: "PRIVATE_NOT_FOR_MAPPERS",
  source_registry_compositions: sourceManifest.compositions.length,
  pilot_canonical_reuse: [...pilotIds].sort(),
  items: privateItems,
};
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify(publicManifest, null, 2)}\n`);
await writeFile(join(outputRoot, "private_lineage_manifest.json"), `${JSON.stringify(privateManifest, null, 2)}\n`);
console.log(JSON.stringify({
  status: "EXPANSION_PACKETS_READY",
  source_compositions: sourceManifest.compositions.length,
  expansion_compositions: publicItems.length,
  pilot_reuse_compositions: pilotIds.size,
  composition_field_units: sourceManifest.compositions.length * Object.keys(fieldDefinitions).length,
  expansion_candidate_documents: publicItems.reduce((sum, item) => sum + item.candidates.length, 0),
}));
