#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const singleFreezePath = join(root, "round3_clean_only_scoring_freeze", "clean_only_scoring_freeze_v1.json");
const outputRoot = join(root, "round3_clean_only_joint_group_freeze");
const groups = {
  task_specification: ["use_condition", "input_precondition", "output_artifact"],
  execution_verification: ["workflow_procedure", "success_verification"],
  applicability_capability: ["boundary_not_for", "dependency_resource"],
};

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const relativePath = (path) => relative(repo, path);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function groupCondition(group) {
  return `REMOVE_${group.toUpperCase()}_R3`;
}

function familyKey(entry) {
  return `${entry.composition_id}\u0000${entry.routing_family_id}\u0000${entry.gold_label}`;
}

function lineEnding(text) {
  return text.includes("\r\n") ? "\r\n" : "\n";
}

function deriveUnionMask(source, componentMasks, context) {
  const sourceLines = source.split(/\r?\n/);
  const componentLines = componentMasks.map(({ field, text }) => ({ field, lines: text.split(/\r?\n/) }));
  for (const component of componentLines) {
    assert(component.lines.length === sourceLines.length, `${context}/${component.field}: line count changed.`);
  }
  const removedByField = Object.fromEntries(componentLines.map((component) => [component.field, []]));
  const unionLines = [];
  const removedLines = [];
  for (let index = 0; index < sourceLines.length; index += 1) {
    const original = sourceLines[index];
    let removed = false;
    for (const component of componentLines) {
      const observed = component.lines[index];
      assert(observed === original || observed === "", `${context}/${component.field}: non-deletion mutation at line ${index + 1}.`);
      if (original !== "" && observed === "") {
        removed = true;
        removedByField[component.field].push(index + 1);
      }
    }
    if (removed) removedLines.push(index + 1);
    unionLines.push(removed ? "" : original);
  }
  return {
    text: unionLines.join(lineEnding(source)),
    removed_line_numbers: removedLines,
    removed_line_numbers_by_component: removedByField,
  };
}

const freeze = await readJson(singleFreezePath);
assert(freeze.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_CLEAN_ONLY_SCORING_FREEZE_V1", "Unexpected single-field freeze status.");
assert(freeze.cases.length === 1078, "Unexpected single-field case count.");
assert(freeze.boundary.no_selector_results && freeze.boundary.no_external_transmission, "Single-field freeze boundary drift.");

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite joint-group freeze root: ${relativePath(outputRoot)}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const casesByFieldAndFamily = new Map();
for (const entry of freeze.cases) {
  const key = `${entry.target_field}\u0000${familyKey(entry)}`;
  assert(!casesByFieldAndFamily.has(key), `Duplicate single-field case ${key}.`);
  casesByFieldAndFamily.set(key, entry);
}

const groupCases = [];
const exclusions = [];
const derivedClearance = [];
const materialisedDocs = new Map();
const allFamilyKeys = new Set(freeze.cases.map(familyKey));
const groupSummary = {};

for (const [group, fields] of Object.entries(groups)) {
  const included = [];
  const groupExclusions = [];
  for (const key of [...allFamilyKeys].sort()) {
    const components = fields.map((field) => casesByFieldAndFamily.get(`${field}\u0000${key}`));
    if (components.some((component) => !component)) {
      const [composition_id, routing_family_id, gold_label] = key.split("\u0000");
      const exclusion = {
        group,
        composition_id,
        routing_family_id,
        gold_label,
        reason: "COMPONENT_FIELD_NOT_ELIGIBLE_IN_SINGLE_FIELD_FREEZE",
        missing_fields: fields.filter((field, index) => !components[index]),
      };
      exclusions.push(exclusion);
      groupExclusions.push(exclusion);
      continue;
    }
    const [base] = components;
    assert(components.every((component) => component.composition_id === base.composition_id && component.routing_family_id === base.routing_family_id && component.gold_label === base.gold_label), `${group}/${key}: component family mismatch.`);
    assert(JSON.stringify(components.map((component) => component.prompt_variants)) === JSON.stringify(components.map(() => base.prompt_variants)), `${group}/${key}: component prompt binding mismatch.`);
    const candidateLabels = base.candidates.map((candidate) => candidate.label);
    assert(components.every((component) => JSON.stringify(component.candidates.map((candidate) => candidate.label)) === JSON.stringify(candidateLabels)), `${group}/${key}: candidate labels mismatch.`);
    const candidates = [];
    for (const label of candidateLabels) {
      const componentCandidates = components.map((component) => component.candidates.find((candidate) => candidate.label === label));
      assert(componentCandidates.every(Boolean), `${group}/${key}/${label}: missing component candidate.`);
      const fullOriginal = componentCandidates[0].full_original;
      assert(componentCandidates.every((candidate) => candidate.full_original.sha256 === fullOriginal.sha256 && candidate.full_original.path === fullOriginal.path), `${group}/${key}/${label}: full-source identity mismatch.`);
      assert(componentCandidates.every((candidate) => candidate.round3_clearance_status === "CLEAR"), `${group}/${key}/${label}: non-clear component entered group.`);
      const documentKey = `${group}\u0000${base.composition_id}\u0000${label}`;
      let document = materialisedDocs.get(documentKey);
      if (!document) {
        const sourcePath = resolve(repo, fullOriginal.path);
        const source = await readFile(sourcePath, "utf8");
        assert(sha256(source) === fullOriginal.sha256, `${group}/${base.composition_id}/${label}: source hash mismatch.`);
        const componentMasks = [];
        for (let index = 0; index < fields.length; index += 1) {
          const descriptor = componentCandidates[index].remove_field_r3;
          const path = resolve(repo, descriptor.path);
          const text = await readFile(path, "utf8");
          assert(sha256(text) === descriptor.sha256, `${group}/${base.composition_id}/${label}/${fields[index]}: component mask hash mismatch.`);
          componentMasks.push({ field: fields[index], text, descriptor });
        }
        const union = deriveUnionMask(source, componentMasks, `${group}/${base.composition_id}/${label}`);
        const path = join(outputRoot, "group_masks", group, base.composition_id, `${label}.md`);
        await mkdir(dirname(path), { recursive: true });
        await writeFile(path, union.text);
        document = {
          label,
          skill_id: componentCandidates[0].skill_id,
          full_original: fullOriginal,
          remove_group_r3: { path: relativePath(path), sha256: sha256(union.text) },
          component_masks: Object.fromEntries(componentMasks.map(({ field, descriptor }) => [field, descriptor])),
          component_clearance_statuses: Object.fromEntries(fields.map((field) => [field, "CLEAR"])),
          group_clearance: "DERIVED_CLEAR_EXACT_UNION",
          removed_line_numbers: union.removed_line_numbers,
          removed_line_numbers_by_component: union.removed_line_numbers_by_component,
        };
        materialisedDocs.set(documentKey, document);
        derivedClearance.push({ group, composition_id: base.composition_id, ...document });
      }
      candidates.push(document);
    }
    groupCases.push({
      case_id: sha256(`${group}\u0000${key}`),
      group,
      group_condition: groupCondition(group),
      component_fields: fields,
      composition_id: base.composition_id,
      source_composition_id: base.source_composition_id,
      registry_id: base.registry_id,
      proposal_id: base.proposal_id,
      routing_family_id: base.routing_family_id,
      strict_gold_skill_id: base.strict_gold_skill_id,
      gold_label: base.gold_label,
      candidate_count: candidates.length,
      candidates,
      prompt_variants: base.prompt_variants,
      component_case_ids: Object.fromEntries(fields.map((field, index) => [field, components[index].case_id])),
    });
    included.push(groupCases.at(-1));
  }
  groupSummary[group] = {
    component_fields: fields,
    eligible_composition_family_cases: included.length,
    eligible_compositions: new Set(included.map((entry) => entry.composition_id)).size,
    eligible_prompt_rows: included.length * 2,
    planned_ranking_rows: included.length * 4,
    excluded_family_keys: groupExclusions.length,
  };
}

assert(groupCases.length === 369, `Expected 369 group cases, found ${groupCases.length}.`);
assert(groupSummary.task_specification.eligible_composition_family_cases === 99, "Unexpected task-specification denominator.");
assert(groupSummary.execution_verification.eligible_composition_family_cases === 138, "Unexpected execution/verification denominator.");
assert(groupSummary.applicability_capability.eligible_composition_family_cases === 132, "Unexpected applicability/capability denominator.");
assert(new Set(groupCases.map((entry) => entry.case_id)).size === groupCases.length, "Duplicate group case IDs.");

const groupFreeze = {
  status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_SCORING_FREEZE_V1",
  frozen_on: "2026-09-04",
  boundary: {
    purpose: "Supporting within-composition routing comparison of exact public originals versus exact group unions of validated Round-3 single-field deletions.",
    no_selector_results: true,
    no_external_transmission: true,
    no_prompt_or_gold_mutation: true,
    groups_are_separate_estimands: true,
    excluded_methods: ["QUERY_REWRITE", "RERANKER", "CROSS_GROUP_POOLED_EFFECT"],
  },
  inputs: {
    single_field_freeze: { path: relativePath(singleFreezePath), sha256: await digestFile(singleFreezePath) },
  },
  groups,
  counts: {
    group_cases: groupCases.length,
    group_prompt_rows: groupCases.length * 2,
    group_ranking_rows: groupCases.length * 4,
    materialised_group_documents: materialisedDocs.size,
  },
  group_summary: groupSummary,
  cases: groupCases,
  derived_group_clearance: derivedClearance,
  exclusions,
  notes: [
    "Every admitted group document is a deterministic line-deletion union of individually Round-3 CLEAR component masks.",
    "The group-clearance label is derived from exact component clearance plus exact-union audit; it does not imply masked skill executability.",
  ],
};

await mkdir(outputRoot, { recursive: true });
const outputs = [
  ["joint_group_scoring_freeze_v1.json", groupFreeze],
  ["derived_group_clearance.json", { status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_DERIVED_CLEARANCE_V1", records: derivedClearance }],
  ["group_exclusions.json", { status: "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_EXCLUSIONS_V1", records: exclusions }],
];
for (const [name, content] of outputs) await writeFile(join(outputRoot, name), `${JSON.stringify(content, null, 2)}\n`);
const sums = [];
for (const [name] of outputs) sums.push(`${await digestFile(join(outputRoot, name))}  ${name}`);
await writeFile(join(outputRoot, "SHA256SUMS"), `${sums.join("\n")}\n`);

console.log(JSON.stringify({
  status: groupFreeze.status,
  group_summary: groupSummary,
  materialised_group_documents: materialisedDocs.size,
  output: outputRoot,
}, null, 2));
