#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import { basename, join, relative, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const sourceRoot = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const round3ManifestPath = join(root, "forced_round3_masks", "FORCED_ROUND3_MASK_MANIFEST.json");
const clearanceRoot = join(root, "forced_round3_clearance", "canonical_round3");
const lineagePath = join(sourceRoot, "source_packets", "private_lineage_manifest.json");
const rosterPath = resolve("skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json");
const outputRoot = join(root, "round3_clean_only_scoring_freeze");
const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const signature = (hashes) => [...hashes].sort().join("|");
const relativePath = (path) => relative(repo, path);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function bytesDigest(path) {
  return sha256(await readFile(path));
}

function hashObject(value) {
  return sha256(`${JSON.stringify(value)}\n`);
}

function increment(object, key) {
  object[key] = (object[key] ?? 0) + 1;
}

const [round3Manifest, lineage, roster] = await Promise.all([
  readJson(round3ManifestPath),
  readJson(lineagePath),
  readJson(rosterPath),
]);

assert(round3Manifest.units?.length === 574, `Expected 574 Round-3 units, found ${round3Manifest.units?.length}.`);
assert(lineage.compositions?.length === 82, `Expected 82 source compositions, found ${lineage.compositions?.length}.`);
assert(roster.rows?.length === 408, `Expected 408 frozen roster rows, found ${roster.rows?.length}.`);

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite existing freeze root: ${relativePath(outputRoot)}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const clearanceFiles = (await readdir(clearanceRoot)).filter((name) => /^OR82-\d{3}-.+\.json$/.test(name)).sort();
assert(clearanceFiles.length === 574, `Expected 574 Round-3 canonical records, found ${clearanceFiles.length}.`);
const clearanceByUnit = new Map();
for (const fileName of clearanceFiles) {
  const path = join(clearanceRoot, fileName);
  const record = await readJson(path);
  assert(record.unit_id === basename(fileName, ".json"), `${fileName}: unit_id mismatch.`);
  assert(!clearanceByUnit.has(record.unit_id), `Duplicate clearance record ${record.unit_id}.`);
  clearanceByUnit.set(record.unit_id, { record, path, sha256: await bytesDigest(path) });
}

const lineageByComposition = new Map(lineage.compositions.map((composition) => [composition.composition_id, composition]));
const compositionBySignature = new Map();
for (const composition of lineage.compositions) {
  const key = signature(composition.candidate_source_sha256);
  assert(!compositionBySignature.has(key), `Duplicate source signature for ${composition.composition_id}.`);
  compositionBySignature.set(key, composition);
}

const rosterFamilies = new Map();
const rosterRowsByComposition = new Map();
for (const row of roster.rows) {
  const composition = compositionBySignature.get(signature(row.candidates.map((candidate) => candidate.source_sha256)));
  assert(composition, `No OR82 source composition matches frozen roster row ${row.proposal_id}/${row.strict_gold_skill_id}.`);
  const candidateBySkill = new Map(composition.candidates.map((candidate) => [candidate.source_id, candidate]));
  const goldCandidate = candidateBySkill.get(row.strict_gold_skill_id);
  assert(goldCandidate, `${composition.composition_id}: frozen gold ${row.strict_gold_skill_id} is absent from source lineage.`);
  const familyKey = `${composition.composition_id}\u0000${row.proposal_id}\u0000${row.strict_gold_skill_id}`;
  const family = rosterFamilies.get(familyKey) ?? {
    composition_id: composition.composition_id,
    source_composition_id: composition.source_composition_id,
    proposal_id: row.proposal_id,
    strict_gold_skill_id: row.strict_gold_skill_id,
    gold_label: goldCandidate.label,
    variants: {},
  };
  assert(!family.variants[row.prompt_variant], `${familyKey}: duplicate ${row.prompt_variant} row in frozen roster.`);
  family.variants[row.prompt_variant] = {
    prompt: row.prompt,
    prompt_variant: row.prompt_variant,
    roster_row_sha256: hashObject(row),
  };
  rosterFamilies.set(familyKey, family);
  const rows = rosterRowsByComposition.get(composition.composition_id) ?? [];
  rows.push(row);
  rosterRowsByComposition.set(composition.composition_id, rows);
}

const pairedFamiliesByComposition = new Map();
const familyExclusions = [];
for (const family of rosterFamilies.values()) {
  const variants = Object.keys(family.variants).sort();
  if (variants.length !== 2 || !family.variants.direct || !family.variants.paraphrase) {
    familyExclusions.push({
      composition_id: family.composition_id,
      proposal_id: family.proposal_id,
      strict_gold_skill_id: family.strict_gold_skill_id,
      reason: "MISSING_FROZEN_DIRECT_PARAPHRASE_PAIR",
      present_variants: variants,
    });
    continue;
  }
  const paired = pairedFamiliesByComposition.get(family.composition_id) ?? [];
  paired.push({
    ...family,
    routing_family_id: sha256(`${family.composition_id}\u0000${family.proposal_id}\u0000${family.strict_gold_skill_id}`),
  });
  pairedFamiliesByComposition.set(family.composition_id, paired);
}

const compositionUnitByField = new Map();
for (const unit of round3Manifest.units) {
  assert(fields.includes(unit.target_field), `${unit.unit_id}: unknown target field ${unit.target_field}.`);
  assert(lineageByComposition.has(unit.composition_id), `${unit.unit_id}: missing source lineage.`);
  const key = `${unit.composition_id}\u0000${unit.target_field}`;
  assert(!compositionUnitByField.has(key), `Duplicate Round-3 unit ${key}.`);
  const clearance = clearanceByUnit.get(unit.unit_id);
  assert(clearance, `${unit.unit_id}: missing canonical clearance record.`);
  const clearanceByLabel = new Map(clearance.record.candidates.map((candidate) => [candidate.label, candidate]));
  const manifestLabels = unit.candidates.map((candidate) => candidate.label).sort();
  const clearanceLabels = [...clearanceByLabel.keys()].sort();
  assert(JSON.stringify(manifestLabels) === JSON.stringify(clearanceLabels), `${unit.unit_id}: clearance candidate labels differ from manifest.`);
  const allClear = unit.candidates.every((candidate) => clearanceByLabel.get(candidate.label).status === "CLEAR");
  compositionUnitByField.set(key, { unit, clearance, allClear });
}

const cases = [];
const exclusions = [];
const fieldSummary = Object.fromEntries(fields.map((field) => [field, {
  total_composition_units: 0,
  fully_clear_units: 0,
  clean_units_with_paired_prompt_gold_binding: 0,
  eligible_composition_family_cases: 0,
  eligible_prompt_rows: 0,
  excluded_by_reason: {},
}]));

for (const composition of lineage.compositions) {
  const pairedFamilies = pairedFamiliesByComposition.get(composition.composition_id) ?? [];
  const rosterRows = rosterRowsByComposition.get(composition.composition_id) ?? [];
  for (const field of fields) {
    const summary = fieldSummary[field];
    summary.total_composition_units += 1;
    const unitState = compositionUnitByField.get(`${composition.composition_id}\u0000${field}`);
    assert(unitState, `${composition.composition_id}/${field}: missing Round-3 unit.`);
    const clearanceStatuses = Object.fromEntries(unitState.unit.candidates.map((candidate) => [candidate.label, unitState.clearance.record.candidates.find((entry) => entry.label === candidate.label).status]));
    if (!unitState.allClear) {
      const reason = "NOT_ALL_CANDIDATES_CLEAR";
      increment(summary.excluded_by_reason, reason);
      exclusions.push({
        composition_id: composition.composition_id,
        source_composition_id: composition.source_composition_id,
        unit_id: unitState.unit.unit_id,
        target_field: field,
        level: "composition_field_unit",
        reason,
        candidate_clearance_statuses: clearanceStatuses,
      });
      continue;
    }
    summary.fully_clear_units += 1;
    if (pairedFamilies.length === 0) {
      const reason = rosterRows.length === 0 ? "NO_FROZEN_STRICT_PROMPT_GOLD_BINDING" : "NO_COMPLETE_FROZEN_DIRECT_PARAPHRASE_PAIR";
      increment(summary.excluded_by_reason, reason);
      exclusions.push({
        composition_id: composition.composition_id,
        source_composition_id: composition.source_composition_id,
        unit_id: unitState.unit.unit_id,
        target_field: field,
        level: "composition_field_unit",
        reason,
        candidate_clearance_statuses: clearanceStatuses,
      });
      continue;
    }
    summary.clean_units_with_paired_prompt_gold_binding += 1;
    for (const family of pairedFamilies) {
      const candidateDocs = [];
      for (const candidate of unitState.unit.candidates) {
        const sourceCandidate = composition.candidates.find((entry) => entry.label === candidate.label);
        assert(sourceCandidate, `${unitState.unit.unit_id}/${candidate.label}: no source candidate.`);
        const sourcePath = resolve(repo, sourceCandidate.packet_path);
        const sourceSha256 = await bytesDigest(sourcePath);
        assert(sourceSha256 === sourceCandidate.source_sha256, `${unitState.unit.unit_id}/${candidate.label}: source hash mismatch.`);
        const round3Sha256 = await bytesDigest(candidate.round3_masked_path);
        assert(round3Sha256 === candidate.round3_masked_sha256, `${unitState.unit.unit_id}/${candidate.label}: Round-3 mask hash mismatch.`);
        candidateDocs.push({
          label: candidate.label,
          skill_id: sourceCandidate.source_id,
          full_original: { path: relativePath(sourcePath), sha256: sourceSha256 },
          remove_field_r3: { path: relativePath(candidate.round3_masked_path), sha256: round3Sha256 },
          round3_clearance_status: "CLEAR",
        });
      }
      const caseId = sha256(`${unitState.unit.unit_id}\u0000${family.routing_family_id}`);
      cases.push({
        case_id: caseId,
        composition_id: composition.composition_id,
        source_composition_id: composition.source_composition_id,
        registry_id: composition.registry_id,
        unit_id: unitState.unit.unit_id,
        target_field: field,
        proposal_id: family.proposal_id,
        routing_family_id: family.routing_family_id,
        strict_gold_skill_id: family.strict_gold_skill_id,
        gold_label: family.gold_label,
        candidate_count: candidateDocs.length,
        candidates: candidateDocs,
        prompt_variants: [family.variants.direct, family.variants.paraphrase],
        clearance_record: { path: relativePath(unitState.clearance.path), sha256: unitState.clearance.sha256 },
      });
      summary.eligible_composition_family_cases += 1;
      summary.eligible_prompt_rows += 2;
    }
  }
}

const duplicateCaseIds = cases.length - new Set(cases.map((entry) => entry.case_id)).size;
assert(duplicateCaseIds === 0, `Duplicate case IDs: ${duplicateCaseIds}.`);
for (const caseRow of cases) {
  assert(caseRow.prompt_variants.map((entry) => entry.prompt_variant).join(",") === "direct,paraphrase", `${caseRow.case_id}: prompt variants are not in frozen direct/paraphrase order.`);
  assert(caseRow.candidates.some((candidate) => candidate.label === caseRow.gold_label), `${caseRow.case_id}: gold label is absent.`);
}

const cleanByField = Object.fromEntries(fields.map((field) => [field, fieldSummary[field].fully_clear_units]));
const commonCompleteCompositions = lineage.compositions.filter((composition) => fields.every((field) => compositionUnitByField.get(`${composition.composition_id}\u0000${field}`).allClear));
const commonCompleteWithPairedBinding = commonCompleteCompositions.filter((composition) => (pairedFamiliesByComposition.get(composition.composition_id) ?? []).length > 0);
const freeze = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_CLEAN_ONLY_SCORING_FREEZE_V1",
  frozen_on: "2026-09-04",
  boundary: {
    purpose: "Field-specific, clean-only, within-composition routing comparison of full public originals versus their Round-3 field-removal masks.",
    no_selector_results: true,
    no_external_transmission: true,
    no_prompt_or_gold_mutation: true,
    primary_conditions: ["FULL_ORIGINAL", "REMOVE_FIELD_R3"],
    primary_retrievers_planned: ["BM25_LOCAL", "QWEN_TEXT_EMBEDDING_V4_AFTER_SEPARATE_PAYLOAD_AUTHORISATION"],
    excluded_methods: ["QUERY_REWRITE", "RERANKER", "JOINT_FIELD_MASK"],
  },
  inputs: {
    source_lineage: { path: relativePath(lineagePath), sha256: await bytesDigest(lineagePath) },
    round3_mask_manifest: { path: relativePath(round3ManifestPath), sha256: await bytesDigest(round3ManifestPath) },
    canonical_round3_clearance: {
      path: relativePath(clearanceRoot),
      record_count: clearanceFiles.length,
      aggregate_sha256: sha256((await Promise.all(clearanceFiles.map(async (name) => `${name}:${await bytesDigest(join(clearanceRoot, name))}`))).join("\n")),
    },
    strict_prompt_gold_roster: { path: relativePath(rosterPath), sha256: await bytesDigest(rosterPath) },
  },
  fields,
  counts: {
    source_compositions: lineage.compositions.length,
    source_candidates: lineage.source_counts.candidates,
    round3_units: round3Manifest.units.length,
    fully_clear_units_by_field: cleanByField,
    paired_frozen_routing_families: [...pairedFamiliesByComposition.values()].flat().length,
    complete_case_composition_family_cases: cases.length,
    complete_case_prompt_rows: cases.length * 2,
    all_seven_fields_complete_compositions: commonCompleteCompositions.length,
    all_seven_fields_complete_with_paired_binding: commonCompleteWithPairedBinding.length,
    family_pair_exclusions: familyExclusions.length,
    exclusion_records: exclusions.length,
  },
  field_summary: fieldSummary,
  cases,
  notes: [
    "A case is eligible only when every candidate has a canonical Round-3 CLEAR decision for its target field and a frozen direct/paraphrase strict-gold prompt pair exists.",
    "Each field retains its own clean-only complete-case denominator; no score pooling across field denominators is permitted.",
    "This freeze has no selector score, external API call, or metric result.",
  ],
};

const exclusionLedger = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_CLEAN_ONLY_EXCLUSIONS_V1",
  frozen_on: "2026-09-04",
  family_pair_exclusions: familyExclusions,
  composition_field_exclusions: exclusions,
  notes: [
    "Exclusions preserve non-clear or unpaired units as overlap/feasibility evidence; they do not diagnose field usefulness.",
    "No excluded item may be added to the primary clean-only scoring denominator without a new, explicitly versioned freeze.",
  ],
};

const summary = {
  status: "PASS_NO_SCORING",
  frozen_on: "2026-09-04",
  source_compositions: lineage.compositions.length,
  source_candidates: lineage.source_counts.candidates,
  round3_units: round3Manifest.units.length,
  fully_clear_units_by_field: cleanByField,
  complete_case_composition_family_cases_by_field: Object.fromEntries(fields.map((field) => [field, fieldSummary[field].eligible_composition_family_cases])),
  complete_case_prompt_rows_by_field: Object.fromEntries(fields.map((field) => [field, fieldSummary[field].eligible_prompt_rows])),
  all_seven_fields_complete_compositions: commonCompleteCompositions.length,
  all_seven_fields_complete_with_paired_binding: commonCompleteWithPairedBinding.length,
  no_selector_results: true,
  no_external_transmission: true,
};

await mkdir(outputRoot, { recursive: true });
const outputs = [
  ["clean_only_scoring_freeze_v1.json", freeze],
  ["eligibility_exclusions.json", exclusionLedger],
  ["freeze_summary.json", summary],
];
for (const [name, value] of outputs) await writeFile(join(outputRoot, name), `${JSON.stringify(value, null, 2)}\n`);
const sumLines = [];
for (const [name] of outputs) sumLines.push(`${await bytesDigest(join(outputRoot, name))}  ${name}`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${sumLines.join("\n")}\n`);

console.log(JSON.stringify(summary, null, 2));
