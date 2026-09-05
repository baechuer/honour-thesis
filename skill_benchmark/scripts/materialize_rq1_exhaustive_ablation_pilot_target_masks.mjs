#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const packetRoot = join(root, "pilot_packets");
const canonicalRoot = join(root, "pilot_maps", "canonical");
const outputRoot = join(root, "pilot_target_masks");
const publicManifest = JSON.parse(await readFile(join(packetRoot, "agent_packet_manifest.json"), "utf8"));
const privateManifest = JSON.parse(await readFile(join(packetRoot, "private_lineage_manifest.json"), "utf8"));
const privateByUnit = new Map(privateManifest.items.map((item) => [item.unit_id, item]));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const proxyTokens = (text) => text.match(/\S+/gu)?.length ?? 0;
const lineEnding = (text) => text.includes("\r\n") ? "\r\n" : "\n";

const unitRows = [];
const mapsByCompositionField = new Map();
for (const item of publicManifest.items) {
  const privateItem = privateByUnit.get(item.unit_id);
  if (!privateItem) throw new Error(`Missing private lineage for ${item.unit_id}`);
  const submission = JSON.parse(await readFile(join(canonicalRoot, `${item.unit_id}.json`), "utf8"));
  mapsByCompositionField.set(`${privateItem.composition_id}::${item.target_field}`, submission);
  const unitRoot = join(outputRoot, "single", item.target_field, privateItem.composition_id);
  await mkdir(unitRoot, { recursive: true });
  const candidateRows = [];
  for (const expectedCandidate of item.candidates) {
    const mapped = submission.candidates.find((candidate) => candidate.label === expectedCandidate.label);
    if (!mapped) throw new Error(`${item.unit_id}: missing map for ${expectedCandidate.label}`);
    const sourcePath = join(packetRoot, item.unit_id, expectedCandidate.path);
    const original = await readFile(sourcePath, "utf8");
    if (sha256(original) !== expectedCandidate.sha256) throw new Error(`${item.unit_id}/${expectedCandidate.label}: source hash mismatch`);
    const ending = lineEnding(original);
    const lines = original.split(/\r?\n/);
    const removedLines = new Set();
    for (const span of mapped.target_spans) {
      for (let line = span.line_start; line <= span.line_end; line += 1) removedLines.add(line);
    }
    const maskedLines = lines.map((line, index) => removedLines.has(index + 1) ? "" : line);
    const masked = maskedLines.join(ending);
    const originalTokens = proxyTokens(original);
    const remainingTokens = proxyTokens(masked);
    const removedTokens = originalTokens - remainingTokens;
    const destination = join(unitRoot, `${expectedCandidate.label}.md`);
    await writeFile(destination, masked);
    candidateRows.push({
      label: expectedCandidate.label,
      map_status: mapped.status,
      source_path: sourcePath,
      masked_path: destination,
      source_sha256: sha256(original),
      masked_sha256: sha256(masked),
      original_proxy_tokens: originalTokens,
      removed_proxy_tokens: removedTokens,
      remaining_proxy_tokens: remainingTokens,
      removed_fraction: originalTokens ? removedTokens / originalTokens : 0,
      near_empty: (originalTokens ? removedTokens / originalTokens >= 0.7 : false) || remainingTokens < 100,
      removed_line_ranges: mapped.target_spans.map((span) => ({
        line_start: span.line_start,
        line_end: span.line_end,
        quote: span.quote,
        rationale: span.rationale,
        collateral_fields: span.collateral_fields,
      })),
    });
  }
  unitRows.push({ unit_id: item.unit_id, composition_id: privateItem.composition_id, target_field: item.target_field, candidates: candidateRows });
}

const groups = {
  task_specification: ["use_condition", "input_precondition", "output_artifact"],
  execution_verification: ["workflow_procedure", "success_verification"],
  applicability_capability: ["boundary_not_for", "dependency_resource"],
};
const compositionIds = [...new Set(privateManifest.items.map((item) => item.composition_id))].sort();
const jointRows = [];
for (const compositionId of compositionIds) {
  for (const [group, fields] of Object.entries(groups)) {
    const maps = fields.map((field) => mapsByCompositionField.get(`${compositionId}::${field}`));
    if (maps.some((map) => !map)) throw new Error(`${compositionId}/${group}: missing component map`);
    const unitRoot = join(outputRoot, "joint", group, compositionId);
    await mkdir(unitRoot, { recursive: true });
    const candidateLabels = maps[0].candidates.map((candidate) => candidate.label);
    const candidateRows = [];
    for (const label of candidateLabels) {
      const packetItem = publicManifest.items.find((item) => privateByUnit.get(item.unit_id)?.composition_id === compositionId && item.target_field === fields[0]);
      const expectedCandidate = packetItem.candidates.find((candidate) => candidate.label === label);
      const sourcePath = join(packetRoot, packetItem.unit_id, expectedCandidate.path);
      const original = await readFile(sourcePath, "utf8");
      const ending = lineEnding(original);
      const lines = original.split(/\r?\n/);
      const removedLines = new Set();
      const componentRanges = [];
      for (const [index, map] of maps.entries()) {
        const candidate = map.candidates.find((entry) => entry.label === label);
        for (const span of candidate.target_spans) {
          for (let line = span.line_start; line <= span.line_end; line += 1) removedLines.add(line);
          componentRanges.push({ field: fields[index], line_start: span.line_start, line_end: span.line_end });
        }
      }
      const masked = lines.map((line, index) => removedLines.has(index + 1) ? "" : line).join(ending);
      const originalTokens = proxyTokens(original);
      const remainingTokens = proxyTokens(masked);
      const removedTokens = originalTokens - remainingTokens;
      const destination = join(unitRoot, `${label}.md`);
      await writeFile(destination, masked);
      candidateRows.push({
        label,
        source_path: sourcePath,
        masked_path: destination,
        source_sha256: sha256(original),
        masked_sha256: sha256(masked),
        original_proxy_tokens: originalTokens,
        removed_proxy_tokens: removedTokens,
        remaining_proxy_tokens: remainingTokens,
        removed_fraction: originalTokens ? removedTokens / originalTokens : 0,
        near_empty: (originalTokens ? removedTokens / originalTokens >= 0.7 : false) || remainingTokens < 100,
        component_ranges: componentRanges,
      });
    }
    jointRows.push({ composition_id: compositionId, group, fields, candidates: candidateRows });
  }
}

const manifest = {
  status: "RQ1_EXHAUSTIVE_PILOT_TARGET_MASKS_MATERIALIZED_NO_SELECTOR",
  boundary: "Target and joint source transformations only; no residual clearance, matched control, prompt, label, or routing result.",
  single_units: unitRows,
  joint_units: jointRows,
};
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "TARGET_MASK_MANIFEST.json"), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ status: manifest.status, single_units: unitRows.length, joint_units: jointRows.length, candidate_masks: unitRows.reduce((sum, unit) => sum + unit.candidates.length, 0) + jointRows.reduce((sum, unit) => sum + unit.candidates.length, 0) }));
