#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const singleFreezePath = join(root, "round3_clean_only_scoring_freeze", "clean_only_scoring_freeze_v1.json");
const groupRoot = join(root, "round3_clean_only_joint_group_freeze");
const groupFreezePath = join(groupRoot, "joint_group_scoring_freeze_v1.json");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const digestFile = async (path) => sha256(await readFile(path));
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function familyKey(entry) {
  return `${entry.composition_id}\u0000${entry.routing_family_id}\u0000${entry.gold_label}`;
}

function lineEnding(text) {
  return text.includes("\r\n") ? "\r\n" : "\n";
}

function deriveUnion(source, componentMasks, context) {
  const sourceLines = source.split(/\r?\n/);
  const masks = componentMasks.map(({ field, text }) => ({ field, lines: text.split(/\r?\n/) }));
  for (const mask of masks) assert(mask.lines.length === sourceLines.length, `${context}/${mask.field}: line-count drift.`);
  const result = [];
  for (let index = 0; index < sourceLines.length; index += 1) {
    const original = sourceLines[index];
    let removed = false;
    for (const mask of masks) {
      const observed = mask.lines[index];
      assert(observed === original || observed === "", `${context}/${mask.field}: non-deletion mutation at line ${index + 1}.`);
      if (original !== "" && observed === "") removed = true;
    }
    result.push(removed ? "" : original);
  }
  return result.join(lineEnding(source));
}

const [single, group] = await Promise.all([readJson(singleFreezePath), readJson(groupFreezePath)]);
assert(single.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_CLEAN_ONLY_SCORING_FREEZE_V1", "Unexpected single-field freeze.");
assert(group.status === "RQ1_PUBLIC_ORIGINAL_ROUND3_JOINT_GROUP_SCORING_FREEZE_V1", "Unexpected group freeze.");
assert(group.inputs.single_field_freeze.sha256 === await digestFile(singleFreezePath), "Single-field freeze hash mismatch.");
assert(group.cases.length === 369 && group.counts.group_ranking_rows === 1476, "Unexpected group case/row count.");

const singleByFieldAndFamily = new Map(single.cases.map((entry) => [`${entry.target_field}\u0000${familyKey(entry)}`, entry]));
const seenCaseIds = new Set();
const perGroup = Object.fromEntries(Object.keys(group.groups).map((name) => [name, { cases: 0, compositions: new Set() }]));
const seenDocumentKeys = new Set();
for (const entry of group.cases) {
  assert(!seenCaseIds.has(entry.case_id), `Duplicate group case ${entry.case_id}.`);
  seenCaseIds.add(entry.case_id);
  assert(group.groups[entry.group], `${entry.case_id}: unknown group.`);
  assert(JSON.stringify(entry.component_fields) === JSON.stringify(group.groups[entry.group]), `${entry.case_id}: component-field drift.`);
  assert(entry.group_condition === `REMOVE_${entry.group.toUpperCase()}_R3`, `${entry.case_id}: condition drift.`);
  assert(entry.prompt_variants.map((variant) => variant.prompt_variant).join(",") === "direct,paraphrase", `${entry.case_id}: prompt-pair drift.`);
  assert([3, 4].includes(entry.candidate_count) && entry.candidates.length === entry.candidate_count, `${entry.case_id}: candidate cardinality drift.`);
  perGroup[entry.group].cases += 1;
  perGroup[entry.group].compositions.add(entry.composition_id);
  const key = familyKey(entry);
  for (const field of entry.component_fields) {
    const component = singleByFieldAndFamily.get(`${field}\u0000${key}`);
    assert(component, `${entry.case_id}/${field}: missing component single-field case.`);
    assert(entry.component_case_ids[field] === component.case_id, `${entry.case_id}/${field}: component case ID mismatch.`);
  }
  for (const candidate of entry.candidates) {
    const documentKey = `${entry.group}\u0000${entry.composition_id}\u0000${candidate.label}`;
    seenDocumentKeys.add(documentKey);
    const source = await readFile(resolve(repo, candidate.full_original.path), "utf8");
    assert(sha256(source) === candidate.full_original.sha256, `${entry.case_id}/${candidate.label}: original hash mismatch.`);
    const componentMasks = [];
    for (const field of entry.component_fields) {
      const component = singleByFieldAndFamily.get(`${field}\u0000${key}`);
      const singleCandidate = component.candidates.find((item) => item.label === candidate.label);
      assert(singleCandidate?.round3_clearance_status === "CLEAR", `${entry.case_id}/${candidate.label}/${field}: component not clear.`);
      assert(candidate.component_masks[field].sha256 === singleCandidate.remove_field_r3.sha256, `${entry.case_id}/${candidate.label}/${field}: component mask identity mismatch.`);
      const text = await readFile(resolve(repo, candidate.component_masks[field].path), "utf8");
      assert(sha256(text) === candidate.component_masks[field].sha256, `${entry.case_id}/${candidate.label}/${field}: component mask hash mismatch.`);
      componentMasks.push({ field, text });
    }
    const expected = deriveUnion(source, componentMasks, `${entry.case_id}/${candidate.label}`);
    const groupText = await readFile(resolve(repo, candidate.remove_group_r3.path), "utf8");
    assert(sha256(groupText) === candidate.remove_group_r3.sha256, `${entry.case_id}/${candidate.label}: group mask hash mismatch.`);
    assert(groupText === expected, `${entry.case_id}/${candidate.label}: group mask is not the component union.`);
    assert(candidate.group_clearance === "DERIVED_CLEAR_EXACT_UNION", `${entry.case_id}/${candidate.label}: derived-clear label drift.`);
  }
}

for (const [groupName, expected] of Object.entries({ task_specification: [99, 37], execution_verification: [138, 51], applicability_capability: [132, 50] })) {
  assert(perGroup[groupName].cases === expected[0], `${groupName}: case-count mismatch.`);
  assert(perGroup[groupName].compositions.size === expected[1], `${groupName}: composition-count mismatch.`);
}
assert(group.derived_group_clearance.length === seenDocumentKeys.size, "Derived-clearance document count mismatch.");

console.log(JSON.stringify({
  status: "PASS",
  group_cases: group.cases.length,
  materialised_group_documents: seenDocumentKeys.size,
  group_summary: Object.fromEntries(Object.entries(perGroup).map(([name, value]) => [name, { cases: value.cases, compositions: value.compositions.size }])),
  no_selector_results: group.boundary.no_selector_results,
  no_external_transmission: group.boundary.no_external_transmission,
}, null, 2));
