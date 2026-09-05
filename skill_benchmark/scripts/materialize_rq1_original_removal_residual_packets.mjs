#!/usr/bin/env node

import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const eligibility = JSON.parse(await readFile(join(root, "family_field_eligibility.json"), "utf8"));
const masksRoot = join(root, "materialized_masks");
const outputRoot = join(root, "residual_packets");
const batchSize = 3;
const conditionLookup = {
  use_condition: { name: "REMOVE_USE_ORIGINAL", fields: ["use_condition"] },
  input_precondition: { name: "REMOVE_INPUT_ORIGINAL", fields: ["input_precondition"] },
  output_artifact: { name: "REMOVE_OUTPUT_ORIGINAL", fields: ["output_artifact"] },
  workflow_procedure: { name: "REMOVE_WORKFLOW_ORIGINAL", fields: ["workflow_procedure"] },
  success_verification: { name: "REMOVE_SUCCESS_ORIGINAL", fields: ["success_verification"] },
  boundary_not_for: { name: "REMOVE_BOUNDARY_ORIGINAL", fields: ["boundary_not_for"] },
  dependency_resource: { name: "REMOVE_DEPENDENCY_ORIGINAL", fields: ["dependency_resource"] },
  task_specification: { name: "REMOVE_TASK_SPECIFICATION_ORIGINAL", fields: ["use_condition", "input_precondition", "output_artifact"] },
  execution_verification: { name: "REMOVE_EXECUTION_VERIFICATION_ORIGINAL", fields: ["workflow_procedure", "success_verification"] },
  applicability_capability: { name: "REMOVE_APPLICABILITY_CAPABILITY_ORIGINAL", fields: ["boundary_not_for", "dependency_resource"] },
};

const eligiblePairs = new Map();
for (const row of eligibility.family_rows) {
  for (const [field, specification] of Object.entries(conditionLookup)) {
    if (!row.conditions[field].eligible) continue;
    const key = `${row.composition_id}\u0000${specification.name}`;
    eligiblePairs.set(key, { composition_id: row.composition_id, condition: specification.name, fields: specification.fields });
  }
}
const pairs = [...eligiblePairs.values()].sort((left, right) => `${left.condition}/${left.composition_id}`.localeCompare(`${right.condition}/${right.composition_id}`));
if (pairs.length === 0) throw new Error("No score-eligible materialized conditions found.");

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const instructions = [
  "# RQ1 Original-Document Residual Review",
  "",
  "You receive only masked anonymous candidate documents and the name of the field or field group that was removed. You must not seek or infer the original documents, prompts, gold labels, source provenance, historical curation, selector outcomes, or external information.",
  "",
  "For each candidate and each target field, decide whether the masked document still contains a candidate-specific, explicit value of that field. Task/method names, generic parameters, and correlated non-target facts do not by themselves count as a residual. Only mark RESIDUAL_FOUND when the text still explicitly states the target field's specific input/trigger/output/workflow/verification/boundary/dependency value.",
  "",
  "Use CLEAR when no such explicit target value remains; RESIDUAL_FOUND with inclusive source lines and a brief note when it does; UNCERTAIN when you cannot decide. Do not make routing judgments.",
].join("\n");
await writeFile(join(outputRoot, "RESIDUAL_REVIEW_INSTRUCTIONS.md"), `${instructions}\n`);

const publicBatches = [];
const privateItems = [];
for (let index = 0; index < pairs.length; index += 1) {
  const pair = pairs[index];
  const itemId = `RMR-${String(index + 1).padStart(3, "0")}`;
  const batchId = `batch_${String(Math.floor(index / batchSize) + 1).padStart(2, "0")}`;
  const ledger = JSON.parse(await readFile(join(masksRoot, pair.condition, pair.composition_id, "mask_ledger.json"), "utf8"));
  const itemDir = join(outputRoot, batchId, itemId);
  await mkdir(itemDir, { recursive: true });
  const candidates = [];
  for (const candidate of ledger.candidates) {
    await cp(candidate.masked_path, join(itemDir, `${candidate.label}.md`));
    candidates.push(candidate.label);
  }
  await writeFile(join(itemDir, "packet.json"), `${JSON.stringify({ item_id: itemId, condition: pair.condition, fields: pair.fields, candidates }, null, 2)}\n`);
  const publicBatch = publicBatches.find((entry) => entry.batch_id === batchId) ?? (() => { const entry = { batch_id: batchId, items: [] }; publicBatches.push(entry); return entry; })();
  publicBatch.items.push({ item_id: itemId, condition: pair.condition, fields: pair.fields, candidates });
  privateItems.push({ item_id: itemId, batch_id: batchId, composition_id: pair.composition_id, condition: pair.condition, fields: pair.fields });
}
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({ status: "PROMPT_BLIND_RESIDUAL_REVIEW_READY", batches: publicBatches }, null, 2)}\n`);
await writeFile(join(outputRoot, "private_lineage_manifest.json"), `${JSON.stringify({ status: "PRIVATE_COORDINATOR_LINEAGE", items: privateItems }, null, 2)}\n`);
console.log(JSON.stringify({ status: "READY", eligible_composition_conditions: pairs.length, batches: publicBatches.length, output: outputRoot }));
