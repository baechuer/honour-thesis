#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repoRoot = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const rosterPath = join(repoRoot, "skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json");
const lineagePath = join(root, "source_packets/private_lineage_manifest.json");
const redactionRoot = join(root, "redaction_submissions/canonical");
const outputPath = join(root, "family_field_eligibility.json");
const fields = ["use_condition", "input_precondition", "output_artifact", "workflow_procedure", "success_verification", "boundary_not_for", "dependency_resource"];
const groups = {
  task_specification: ["use_condition", "input_precondition", "output_artifact"],
  execution_verification: ["workflow_procedure", "success_verification"],
  applicability_capability: ["boundary_not_for", "dependency_resource"],
};
const sha256 = (value) => createHash("sha256").update(value).digest("hex");

const roster = JSON.parse(await readFile(rosterPath, "utf8"));
const lineage = JSON.parse(await readFile(lineagePath, "utf8"));
const redactionFiles = (await readdir(redactionRoot)).filter((name) => /^batch_\d{2}\.json$/.test(name)).sort();
if (redactionFiles.length !== 26) throw new Error(`Expected 26 canonical redaction maps, found ${redactionFiles.length}.`);

const compositionsByKey = new Map(lineage.compositions.map((composition) => [JSON.stringify([...composition.candidate_composition_key].sort()), composition]));
const mapsByComposition = new Map();
for (const fileName of redactionFiles) {
  const submission = JSON.parse(await readFile(join(redactionRoot, fileName), "utf8"));
  for (const composition of submission.compositions) mapsByComposition.set(composition.composition_id, composition);
}
if (mapsByComposition.size !== 76) throw new Error(`Expected 76 redaction-map compositions, found ${mapsByComposition.size}.`);

const candidateMap = (composition, label) => {
  const candidate = composition.candidates.find((entry) => entry.label === label);
  if (!candidate) throw new Error(`Missing map candidate ${composition.composition_id}/${label}.`);
  return candidate;
};

function singleDisposition(lineageComposition, mapComposition, targetSkillId, field) {
  const labelsBySkill = new Map(lineageComposition.candidates.map((candidate) => [candidate.skill_id, candidate.label]));
  const targetLabel = labelsBySkill.get(targetSkillId);
  if (!targetLabel) throw new Error(`Target ${targetSkillId} is not in ${lineageComposition.composition_id}.`);
  const candidateStates = lineageComposition.candidates.map((candidate) => {
    const map = candidateMap(mapComposition, candidate.label).field_maps[field];
    return { label: candidate.label, skill_id: candidate.skill_id, status: map.status, edits: map.edits.length };
  });
  const target = candidateStates.find((candidate) => candidate.label === targetLabel);
  const unsafe = candidateStates.filter((candidate) => !["SAFE_MAP", "NO_DIRECT_VALUE"].includes(candidate.status));
  const eligible = target.status === "SAFE_MAP" && unsafe.length === 0;
  const reason = eligible
    ? "ELIGIBLE"
    : target.status !== "SAFE_MAP"
      ? `TARGET_${target.status}`
      : `CANDIDATE_${unsafe.map((candidate) => `${candidate.label}_${candidate.status}`).join("__")}`;
  return { eligible, reason, target_label: targetLabel, candidate_states: candidateStates };
}

const compositionConditions = [];
for (const lineageComposition of lineage.compositions) {
  const mapComposition = mapsByComposition.get(lineageComposition.composition_id);
  const fieldsByCandidate = {};
  for (const candidate of lineageComposition.candidates) {
    fieldsByCandidate[candidate.label] = candidateMap(mapComposition, candidate.label).field_maps;
  }
  const conditionAvailability = {};
  for (const field of fields) {
    const statuses = Object.values(fieldsByCandidate).map((fieldMaps) => fieldMaps[field].status);
    conditionAvailability[field] = {
      materialisable: statuses.every((status) => ["SAFE_MAP", "NO_DIRECT_VALUE"].includes(status)) && statuses.includes("SAFE_MAP"),
      candidate_statuses: statuses,
    };
  }
  for (const [group, components] of Object.entries(groups)) {
    conditionAvailability[group] = {
      materialisable: components.every((field) => conditionAvailability[field].materialisable),
      components,
    };
  }
  compositionConditions.push({
    composition_id: lineageComposition.composition_id,
    candidate_composition_key: lineageComposition.candidate_composition_key,
    candidates: lineageComposition.candidates.map((candidate) => ({ label: candidate.label, skill_id: candidate.skill_id })),
    condition_availability: conditionAvailability,
  });
}

const compositionByKey = new Map(compositionConditions.map((entry) => [JSON.stringify([...entry.candidate_composition_key].sort()), entry]));
const compositionMapsById = new Map(lineage.compositions.map((entry) => [entry.composition_id, mapsByComposition.get(entry.composition_id)]));
const lineageById = new Map(lineage.compositions.map((entry) => [entry.composition_id, entry]));
const familyRows = [];
for (const row of roster.rows) {
  const composition = compositionByKey.get(JSON.stringify([...row.candidate_composition_key].sort()));
  if (!composition) throw new Error(`No source map for roster proposal ${row.proposal_id}.`);
  const lineageComposition = lineageById.get(composition.composition_id);
  const mapComposition = compositionMapsById.get(composition.composition_id);
  const conditions = {};
  for (const field of fields) conditions[field] = singleDisposition(lineageComposition, mapComposition, row.strict_gold_skill_id, field);
  for (const [group, components] of Object.entries(groups)) {
    const componentStates = components.map((field) => conditions[field]);
    conditions[group] = {
      eligible: componentStates.every((state) => state.eligible),
      reason: componentStates.every((state) => state.eligible)
        ? "ELIGIBLE"
        : components.filter((field) => !conditions[field].eligible).map((field) => `${field}_${conditions[field].reason}`).join("__"),
      components,
    };
  }
  familyRows.push({
    family_id: sha256(`${row.proposal_id}\u0000${row.strict_gold_skill_id}\u0000${row.prompt_variant}\u0000${row.prompt}`),
    proposal_id: row.proposal_id,
    composition_id: composition.composition_id,
    strict_gold_skill_id: row.strict_gold_skill_id,
    prompt: row.prompt,
    prompt_variant: row.prompt_variant,
    conditions,
  });
}

const summary = {};
for (const condition of [...fields, ...Object.keys(groups)]) {
  const eligibleRows = familyRows.filter((row) => row.conditions[condition].eligible);
  const eligibleCompositions = new Set(eligibleRows.map((row) => row.composition_id));
  const reasons = {};
  for (const row of familyRows) {
    if (!row.conditions[condition].eligible) reasons[row.conditions[condition].reason] = (reasons[row.conditions[condition].reason] ?? 0) + 1;
  }
  summary[condition] = { eligible_rows: eligibleRows.length, eligible_compositions: eligibleCompositions.size, rejected_rows: familyRows.length - eligibleRows.length, rejection_reasons: reasons };
}

const output = {
  status: "ELIGIBILITY_PREPARED_NO_MASKS",
  inputs: {
    roster: "skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json",
    roster_sha256: sha256(await readFile(rosterPath)),
    source_parse_status: "COMPLETE_76_COMPOSITIONS",
    redaction_map_status: "COMPLETE_76_COMPOSITIONS",
  },
  counts: { roster_rows: roster.rows.length, source_compositions: lineage.compositions.length, family_rows: familyRows.length },
  field_names: fields,
  group_definitions: groups,
  summary,
  composition_conditions: compositionConditions,
  family_rows: familyRows,
  notes: [
    "Eligibility is a technical preflight only. It creates no edited document and no retrieval result.",
    "A score-eligible family requires the strict-gold candidate to have a SAFE_MAP and all candidates to have SAFE_MAP or NO_DIRECT_VALUE for the tested field.",
    "Group eligibility is the conjunction of its frozen single-field eligibility states.",
  ],
};
await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify({ status: output.status, counts: output.counts, summary }));
