#!/usr/bin/env node

import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { basename, join, resolve } from "node:path";

const workspace = resolve(".");
const sourceRoot = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const outputRoot = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "pilot_packets");
const sourceManifest = JSON.parse(await readFile(join(sourceRoot, "source_packets", "private_lineage_manifest.json"), "utf8"));
const pilotIds = ["OR82-006", "OR82-017"];
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

const selected = sourceManifest.compositions.filter((composition) => pilotIds.includes(composition.composition_id));
if (selected.length !== pilotIds.length) throw new Error(`Expected ${pilotIds.length} pilot compositions, found ${selected.length}`);

await mkdir(outputRoot, { recursive: true });
const publicItems = [];
const privateItems = [];
let sequence = 1;
for (const composition of selected.sort((left, right) => left.composition_id.localeCompare(right.composition_id))) {
  for (const [targetField, definition] of Object.entries(fieldDefinitions)) {
    const unitId = `EXA-P${String(sequence).padStart(3, "0")}`;
    const unitRoot = join(outputRoot, unitId);
    await mkdir(unitRoot, { recursive: true });
    const candidates = [];
    const privateCandidates = [];
    for (const candidate of composition.candidates) {
      const sourcePath = resolve(workspace, candidate.packet_path);
      const bytes = await readFile(sourcePath);
      const actualSha = sha256(bytes);
      if (actualSha !== candidate.source_sha256) throw new Error(`${composition.composition_id}/${candidate.label} source hash mismatch`);
      const destination = join(unitRoot, `${candidate.label}.md`);
      await copyFile(sourcePath, destination);
      candidates.push({ label: candidate.label, path: basename(destination), sha256: actualSha });
      privateCandidates.push({ label: candidate.label, source_path: candidate.source_path, packet_source_path: candidate.packet_path, sha256: actualSha });
    }
    const packet = {
      unit_id: unitId,
      target_field: targetField,
      field_definition: definition,
      instructions: [
        "Map every complete source line carrying explicit or semantically equivalent candidate-specific target-field information.",
        "Mixed carriers may be deleted and must list collateral operational fields.",
        "Use non-overlapping complete line ranges. Quote each complete line range exactly, joined by newline.",
        "Do not preserve executability. Do not invent, paraphrase, broaden, or replace capability text.",
        "Use NO_TARGET_CUE only when the full candidate document contains no candidate-specific target-field value."
      ],
      candidates: candidates.map(({ label, path, sha256: hash }) => ({ label, path, sha256: hash })),
    };
    await writeFile(join(unitRoot, "packet.json"), `${JSON.stringify(packet, null, 2)}\n`);
    publicItems.push({ unit_id: unitId, target_field: targetField, packet_path: `${unitId}/packet.json`, candidates: packet.candidates });
    privateItems.push({ unit_id: unitId, composition_id: composition.composition_id, registry_id: composition.registry_id, source_composition_id: composition.source_composition_id, target_field: targetField, candidates: privateCandidates });
    sequence += 1;
  }
}

await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({ status: "RQ1_EXHAUSTIVE_PILOT_SOURCE_ONLY_PACKETS", items: publicItems }, null, 2)}\n`);
await writeFile(join(outputRoot, "private_lineage_manifest.json"), `${JSON.stringify({ status: "PRIVATE_NOT_FOR_MAPPERS", items: privateItems }, null, 2)}\n`);
console.log(JSON.stringify({ status: "PILOT_PACKETS_READY", compositions: selected.length, units: publicItems.length, candidates: publicItems.reduce((sum, item) => sum + item.candidates.length, 0) }));
