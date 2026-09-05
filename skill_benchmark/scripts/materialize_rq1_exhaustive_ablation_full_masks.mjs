#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const ledgerPath = join(root, "canonical_field_map_ledger", "CANONICAL_FIELD_MAP_LEDGER.json");
const outputRoot = join(root, "full_target_masks");
const ledger = JSON.parse(await readFile(ledgerPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const proxyTokens = (text) => text.match(/\S+/gu)?.length ?? 0;
const groups = {
  task_specification: ["use_condition", "input_precondition", "output_artifact"],
  execution_verification: ["workflow_procedure", "success_verification"],
  applicability_capability: ["boundary_not_for", "dependency_resource"],
};

const mapCache = new Map();
const sourceCache = new Map();
const readMap = async (path) => {
  if (!mapCache.has(path)) mapCache.set(path, JSON.parse(await readFile(path, "utf8")));
  return mapCache.get(path);
};
const readSource = async (path) => {
  if (!sourceCache.has(path)) sourceCache.set(path, await readFile(path, "utf8"));
  return sourceCache.get(path);
};
const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";
const verifySpan = (lines, span, context) => {
  const actual = lines.slice(span.line_start - 1, span.line_end).join("\n");
  if (actual !== span.quote) throw new Error(`${context}: quote mismatch at ${span.line_start}-${span.line_end}`);
};
const maskSource = (source, componentMaps, context) => {
  const ending = endingOf(source);
  const lines = source.split(/\r?\n/);
  const removedLines = new Set();
  const ranges = [];
  for (const { field, candidate } of componentMaps) {
    for (const span of candidate.target_spans) {
      verifySpan(lines, span, `${context}/${field}`);
      for (let line = span.line_start; line <= span.line_end; line += 1) removedLines.add(line);
      ranges.push({
        field,
        line_start: span.line_start,
        line_end: span.line_end,
        quote: span.quote,
        rationale: span.rationale,
        collateral_fields: span.collateral_fields,
      });
    }
  }
  const masked = lines.map((line, index) => removedLines.has(index + 1) ? "" : line).join(ending);
  return { masked, removedLines: [...removedLines].sort((a, b) => a - b), ranges };
};
const stats = (source, masked) => {
  const originalTokens = proxyTokens(source);
  const remainingTokens = proxyTokens(masked);
  const removedTokens = originalTokens - remainingTokens;
  const removedFraction = originalTokens ? removedTokens / originalTokens : 0;
  return {
    original_proxy_tokens: originalTokens,
    removed_proxy_tokens: removedTokens,
    remaining_proxy_tokens: remainingTokens,
    removed_fraction: removedFraction,
    near_empty: removedFraction >= 0.7 || remainingTokens < 100,
  };
};

const singleRows = [];
for (const unit of ledger.units) {
  const map = await readMap(unit.canonical_map_path);
  const mappedByLabel = new Map(map.candidates.map((candidate) => [candidate.label, candidate]));
  const candidateRows = [];
  for (const sourceCandidate of unit.candidates) {
    const mapped = mappedByLabel.get(sourceCandidate.label);
    const source = await readSource(sourceCandidate.canonical_source_path);
    if (sha256(source) !== sourceCandidate.source_sha256) throw new Error(`${unit.unit_id}/${sourceCandidate.label}: source hash mismatch`);
    const result = maskSource(source, [{ field: unit.target_field, candidate: mapped }], `${unit.unit_id}/${sourceCandidate.label}`);
    const destination = join(outputRoot, "single", unit.target_field, unit.composition_id, `${sourceCandidate.label}.md`);
    await mkdir(resolve(destination, ".."), { recursive: true });
    await writeFile(destination, result.masked);
    candidateRows.push({
      label: sourceCandidate.label,
      source_path: sourceCandidate.canonical_source_path,
      masked_path: destination,
      source_sha256: sourceCandidate.source_sha256,
      masked_sha256: sha256(result.masked),
      map_status: mapped.status,
      removed_line_numbers: result.removedLines,
      removed_line_ranges: result.ranges,
      ...stats(source, result.masked),
    });
  }
  singleRows.push({
    unit_id: unit.unit_id,
    composition_id: unit.composition_id,
    target_field: unit.target_field,
    candidates: candidateRows,
  });
}

const unitsByCompositionField = new Map(ledger.units.map((unit) => [`${unit.composition_id}::${unit.target_field}`, unit]));
const compositionIds = [...new Set(ledger.units.map((unit) => unit.composition_id))].sort();
const jointRows = [];
for (const compositionId of compositionIds) {
  for (const [group, fields] of Object.entries(groups)) {
    const units = fields.map((field) => unitsByCompositionField.get(`${compositionId}::${field}`));
    if (units.some((unit) => !unit)) throw new Error(`${compositionId}/${group}: missing component unit`);
    const maps = await Promise.all(units.map((unit) => readMap(unit.canonical_map_path)));
    const candidateRows = [];
    for (const sourceCandidate of units[0].candidates) {
      const source = await readSource(sourceCandidate.canonical_source_path);
      const componentMaps = maps.map((map, index) => ({
        field: fields[index],
        candidate: map.candidates.find((candidate) => candidate.label === sourceCandidate.label),
      }));
      if (componentMaps.some((component) => !component.candidate)) throw new Error(`${compositionId}/${group}/${sourceCandidate.label}: missing component map`);
      const result = maskSource(source, componentMaps, `${compositionId}/${group}/${sourceCandidate.label}`);
      const destination = join(outputRoot, "joint", group, compositionId, `${sourceCandidate.label}.md`);
      await mkdir(resolve(destination, ".."), { recursive: true });
      await writeFile(destination, result.masked);
      candidateRows.push({
        label: sourceCandidate.label,
        source_path: sourceCandidate.canonical_source_path,
        masked_path: destination,
        source_sha256: sourceCandidate.source_sha256,
        masked_sha256: sha256(result.masked),
        removed_line_numbers: result.removedLines,
        component_ranges: result.ranges,
        ...stats(source, result.masked),
      });
    }
    jointRows.push({ composition_id: compositionId, group, fields, candidates: candidateRows });
  }
}

const candidateMaskCount = singleRows.reduce((sum, unit) => sum + unit.candidates.length, 0)
  + jointRows.reduce((sum, unit) => sum + unit.candidates.length, 0);
const manifest = {
  status: "RQ1_EXHAUSTIVE_FULL_TARGET_MASKS_MATERIALIZED_NO_SELECTOR",
  boundary: "Deterministic source transformations only; no prompts, labels, selector outputs, or routing results.",
  source_ledger_path: ledgerPath,
  composition_count: compositionIds.length,
  single_unit_count: singleRows.length,
  joint_unit_count: jointRows.length,
  candidate_mask_count: candidateMaskCount,
  joint_groups: groups,
  single_units: singleRows,
  joint_units: jointRows,
};
if (manifest.composition_count !== 82) throw new Error(`Expected 82 compositions, found ${manifest.composition_count}`);
if (manifest.single_unit_count !== 574) throw new Error(`Expected 574 single units, found ${manifest.single_unit_count}`);
if (manifest.joint_unit_count !== 246) throw new Error(`Expected 246 joint units, found ${manifest.joint_unit_count}`);
if (manifest.candidate_mask_count !== 2650) throw new Error(`Expected 2650 candidate masks, found ${manifest.candidate_mask_count}`);
await mkdir(outputRoot, { recursive: true });
const manifestPath = join(outputRoot, "TARGET_MASK_MANIFEST.json");
await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({
  status: manifest.status,
  compositions: manifest.composition_count,
  single_units: manifest.single_unit_count,
  joint_units: manifest.joint_unit_count,
  candidate_masks: manifest.candidate_mask_count,
  manifest_sha256: sha256(await readFile(manifestPath, "utf8")),
}));
