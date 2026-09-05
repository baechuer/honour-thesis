#!/usr/bin/env node

import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const sourceRoot = join(root, "source_packets");
const sourceLineage = JSON.parse(await readFile(join(sourceRoot, "private_lineage_manifest.json"), "utf8"));
const residualRoot = join(root, "residual_submissions", "canonical");
const residual = JSON.parse(await readFile(join(residualRoot, "INGESTION_STATUS.json"), "utf8"));
const residualLineage = JSON.parse(await readFile(join(root, "residual_packets", "private_lineage_manifest.json"), "utf8"));
const mapsRoot = join(root, "redaction_submissions", "canonical");
const outputRoot = join(root, "remediation_packets");
const fieldsByCondition = {
  REMOVE_USE_ORIGINAL: ["use_condition"],
  REMOVE_INPUT_ORIGINAL: ["input_precondition"],
  REMOVE_OUTPUT_ORIGINAL: ["output_artifact"],
  REMOVE_WORKFLOW_ORIGINAL: ["workflow_procedure"],
  REMOVE_SUCCESS_ORIGINAL: ["success_verification"],
  REMOVE_BOUNDARY_ORIGINAL: ["boundary_not_for"],
  REMOVE_DEPENDENCY_ORIGINAL: ["dependency_resource"],
  REMOVE_TASK_SPECIFICATION_ORIGINAL: ["use_condition", "input_precondition", "output_artifact"],
  REMOVE_EXECUTION_VERIFICATION_ORIGINAL: ["workflow_procedure", "success_verification"],
  REMOVE_APPLICABILITY_CAPABILITY_ORIGINAL: ["boundary_not_for", "dependency_resource"],
};

const mapsByComposition = new Map();
for (const name of Array.from({ length: 26 }, (_, index) => `batch_${String(index + 1).padStart(2, "0")}`)) {
  const payload = JSON.parse(await readFile(join(mapsRoot, `${name}.json`), "utf8"));
  for (const composition of payload.compositions) mapsByComposition.set(composition.composition_id, composition);
}
const sourceByComposition = new Map(sourceLineage.compositions.map((entry) => [entry.composition_id, entry]));
const lineageByItem = new Map(residualLineage.items.map((entry) => [entry.item_id, entry]));
const residualItems = residual.item_summary
  .filter((entry) => entry.residual_status === "RESIDUAL_FOUND")
  .map((entry) => {
    const lineage = lineageByItem.get(entry.item_id);
    if (!lineage) throw new Error(`Missing residual lineage for ${entry.item_id}.`);
    const fields = fieldsByCondition[lineage.condition];
    if (!fields) throw new Error(`Unknown condition ${lineage.condition}.`);
    return { ...entry, ...lineage, fields };
  })
  .sort((left, right) => left.condition.localeCompare(right.condition) || left.composition_id.localeCompare(right.composition_id));

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const instructions = `# RQ1 Original-Document Residual-Cue Remediation Instructions

You receive only anonymous original candidate documents, their current source-line edit ledger, and a source-blind residual-cue challenge. You must not infer or seek prompts, gold labels, source provenance, selectors, scores, or results.

## Aim

The first map removed documented field values but a separate blind reviewer found one or more explicit candidate-specific values still visible in the masked version. For every candidate and target field in an assigned item, find any additional direct source lines needed to remove that field value from the original skill document.

This is a routing-only document intervention. The revised document may be incomplete or non-executable. Do not broaden capability. Deleting a specific format, package, threshold, or prerequisite must not turn it into a broader claim such as \"any file\" or \"any dependency\".

## Decisions

- SUPPLEMENTAL_SAFE_MAP: every additional direct value you found can be removed by exact source-line edits outside the existing-edit ledger.
- NO_SUPPLEMENTAL_EDIT_NEEDED: no further direct value exists for this candidate/field. This is prohibited when the residual challenge names that candidate/field.
- UNSAFE_MIXED_CARRIER: a remaining direct value is inseparable from non-target content in the source carrier. Do not speculate.
- UNCERTAIN: source text makes the decision indeterminate. Do not speculate.

## Edit rules

1. Cite source evidence lines for every edit; edit ranges must sit inside cited evidence ranges.
2. Delete a whole line only when it is wholly target-field content. A rewrite affects exactly one line and may use only the literal marker \`[information removed]\` where grammar needs a complement.
3. Do not overlap an existing edit in \`existing_edits.json\`.
4. Inspect the whole original document for repeated direct values, not only the cited challenge. Do not treat generic task/method names or merely correlated prose as target values.
5. Do not add any capability, title, source, or candidate marker.

## Output

Write the exact JSON schema in \`REMEDIATION_SCHEMA.json\` to the assigned output. Include every item, candidate, and requested field. A challenge-marked candidate/field must be SUPPLEMENTAL_SAFE_MAP, UNSAFE_MIXED_CARRIER, or UNCERTAIN; it cannot be NO_SUPPLEMENTAL_EDIT_NEEDED.\n`;
await writeFile(join(outputRoot, "REMEDIATION_INSTRUCTIONS.md"), instructions);

const batches = [];
for (let start = 0, batchIndex = 1; start < residualItems.length; start += 3, batchIndex += 1) {
  const batchId = `batch_${String(batchIndex).padStart(2, "0")}`;
  const items = residualItems.slice(start, start + 3);
  const batchDir = join(outputRoot, batchId);
  await mkdir(batchDir, { recursive: true });
  const batchEntries = [];
  for (const item of items) {
    const sourceComposition = sourceByComposition.get(item.composition_id);
    const mapComposition = mapsByComposition.get(item.composition_id);
    if (!sourceComposition || !mapComposition) throw new Error(`Missing source or map for ${item.composition_id}.`);
    const itemDir = join(batchDir, item.item_id);
    await mkdir(itemDir, { recursive: true });
    const challengeByKey = new Map(item.reviews.filter((review) => review.status === "RESIDUAL_FOUND")
      .map((review) => [`${review.candidate_label}\u0000${review.field}`, { evidence: review.evidence }]));
    const candidates = [];
    for (const candidate of sourceComposition.candidates) {
      await cp(join(sourceRoot, sourceComposition.batch_id, item.composition_id, `${candidate.label}.md`), join(itemDir, `${candidate.label}.md`));
      const mappedCandidate = mapComposition.candidates.find((entry) => entry.label === candidate.label);
      const existingEdits = Object.fromEntries(item.fields.map((field) => [field, mappedCandidate.field_maps[field].edits]));
      const challenges = Object.fromEntries(item.fields.map((field) => [field, challengeByKey.get(`${candidate.label}\u0000${field}`) ?? null]));
      await writeFile(join(itemDir, `${candidate.label}.existing_edits.json`), `${JSON.stringify({ label: candidate.label, existing_edits: existingEdits, residual_challenges: challenges }, null, 2)}\n`);
      candidates.push(candidate.label);
    }
    const itemManifest = { item_id: item.item_id, condition: item.condition, fields: item.fields, candidates };
    await writeFile(join(itemDir, "ITEM_MANIFEST.json"), `${JSON.stringify(itemManifest, null, 2)}\n`);
    batchEntries.push(itemManifest);
  }
  batches.push({ batch_id: batchId, items: batchEntries });
}
const schema = {
  status: "REMEDIATION_MAP_COMPLETE",
  batch_id: "batch_01",
  items: [{ item_id: "RMR-001", candidates: [{ label: "candidate_a", field_maps: { input_precondition: { status: "SUPPLEMENTAL_SAFE_MAP", source_evidence: [{ line_start: 1, line_end: 1, note: "Direct input requirement." }], edits: [{ kind: "DELETE_LINE", line_start: 1, line_end: 1, rationale: "Whole line is an input requirement." }] } } }] }],
};
await writeFile(join(outputRoot, "REMEDIATION_SCHEMA.json"), `${JSON.stringify(schema, null, 2)}\n`);
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({ status: "SOURCE_ONLY_RESIDUAL_REMEDIATION_READY", batches }, null, 2)}\n`);
console.log(JSON.stringify({ status: "READY", residual_items: residualItems.length, batches: batches.length, output: outputRoot }));
