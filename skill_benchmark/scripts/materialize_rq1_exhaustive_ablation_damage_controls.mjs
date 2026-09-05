#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const targetManifest = JSON.parse(
  await readFile(join(root, "pilot_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"),
);
const canonicalRoot = join(root, "pilot_maps", "canonical");
const outputRoot = join(root, "pilot_damage_controls");
const regions = ["frontmatter", "early_body", "middle_body", "late_body"];
const seeds = [1103, 2207, 3301];
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const tokenCount = (text) => text.match(/\S+/gu)?.length ?? 0;

function lineRegions(lines) {
  const result = Array(lines.length).fill("early_body");
  let bodyStart = 0;
  if (lines[0]?.trim() === "---") {
    const close = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
    if (close >= 0) {
      for (let index = 0; index <= close; index += 1) result[index] = "frontmatter";
      bodyStart = close + 1;
    }
  }
  const bodyLength = Math.max(0, lines.length - bodyStart);
  for (let index = bodyStart; index < lines.length; index += 1) {
    const fraction = bodyLength ? (index - bodyStart) / bodyLength : 0;
    result[index] = fraction < 1 / 3 ? "early_body" : fraction < 2 / 3 ? "middle_body" : "late_body";
  }
  return result;
}

function lineTokens(line, lineIndex, region) {
  const output = [];
  for (const match of line.matchAll(/\S+/gu)) {
    output.push({ lineIndex, start: match.index, end: match.index + match[0].length, text: match[0], region });
  }
  return output;
}

function ranked(tokens, seed, unitId, label, region) {
  return [...tokens].sort((left, right) => {
    const leftHash = sha256(`${seed}|${unitId}|${label}|${region}|${left.lineIndex}|${left.start}|${left.text}`);
    const rightHash = sha256(`${seed}|${unitId}|${label}|${region}|${right.lineIndex}|${right.start}|${right.text}`);
    return leftHash.localeCompare(rightHash);
  });
}

const units = [];
for (const unit of targetManifest.single_units) {
  const map = JSON.parse(await readFile(join(canonicalRoot, `${unit.unit_id}.json`), "utf8"));
  const candidateRows = [];
  for (const candidate of unit.candidates) {
    const source = await readFile(candidate.source_path, "utf8");
    const ending = source.includes("\r\n") ? "\r\n" : "\n";
    const lines = source.split(/\r?\n/);
    const regionByLine = lineRegions(lines);
    const mapped = map.candidates.find((entry) => entry.label === candidate.label);
    const protectedLines = new Set();
    for (const span of mapped.target_spans) {
      for (let line = span.line_start; line <= span.line_end; line += 1) protectedLines.add(line - 1);
    }
    const targetByRegion = Object.fromEntries(regions.map((region) => [region, 0]));
    for (const lineIndex of protectedLines) {
      targetByRegion[regionByLine[lineIndex]] += tokenCount(lines[lineIndex] ?? "");
    }
    const eligibleByRegion = Object.fromEntries(regions.map((region) => [region, []]));
    for (let lineIndex = 0; lineIndex < lines.length; lineIndex += 1) {
      if (protectedLines.has(lineIndex)) continue;
      const region = regionByLine[lineIndex];
      eligibleByRegion[region].push(...lineTokens(lines[lineIndex], lineIndex, region));
    }
    const targetTotal = Object.values(targetByRegion).reduce((sum, value) => sum + value, 0);
    const replicateRows = [];
    for (const [replicateIndex, seed] of seeds.entries()) {
      const quotas = Object.fromEntries(
        regions.map((region) => [region, Math.min(targetByRegion[region], eligibleByRegion[region].length)]),
      );
      let deficit = targetTotal - Object.values(quotas).reduce((sum, value) => sum + value, 0);
      const regionOrder = [...regions].sort((left, right) =>
        sha256(`${seed}|${unit.unit_id}|${candidate.label}|${left}`).localeCompare(
          sha256(`${seed}|${unit.unit_id}|${candidate.label}|${right}`),
        ),
      );
      while (deficit > 0) {
        let progressed = false;
        for (const region of regionOrder) {
          if (quotas[region] < eligibleByRegion[region].length) {
            quotas[region] += 1;
            deficit -= 1;
            progressed = true;
            if (deficit === 0) break;
          }
        }
        if (!progressed) break;
      }
      const selected = regions.flatMap((region) =>
        ranked(eligibleByRegion[region], seed, unit.unit_id, candidate.label, region).slice(0, quotas[region]),
      );
      const selectedByLine = new Map();
      for (const token of selected) {
        if (!selectedByLine.has(token.lineIndex)) selectedByLine.set(token.lineIndex, []);
        selectedByLine.get(token.lineIndex).push(token);
      }
      const controlLines = [...lines];
      for (const [lineIndex, tokens] of selectedByLine) {
        let line = controlLines[lineIndex];
        for (const token of tokens.sort((left, right) => right.start - left.start)) {
          line = `${line.slice(0, token.start)}${line.slice(token.end)}`;
        }
        controlLines[lineIndex] = line;
      }
      const control = controlLines.join(ending);
      const actualByRegion = Object.fromEntries(regions.map((region) => [region, quotas[region]]));
      const targetProtected = [...protectedLines].every((lineIndex) => controlLines[lineIndex] === lines[lineIndex]);
      const tolerance = Math.max(5, Math.ceil(targetTotal * 0.1));
      const totalPass = Math.abs(selected.length - targetTotal) <= tolerance;
      const regionPass = regions.every((region) => {
        const required = Math.ceil(targetByRegion[region] * 0.9);
        return actualByRegion[region] >= required || eligibleByRegion[region].length < required;
      });
      const destination = join(
        outputRoot,
        "single",
        unit.target_field,
        unit.composition_id,
        `control_${replicateIndex + 1}`,
        `${candidate.label}.md`,
      );
      await mkdir(resolve(destination, ".."), { recursive: true });
      await writeFile(destination, control);
      replicateRows.push({
        replicate: replicateIndex + 1,
        seed,
        path: destination,
        sha256: sha256(control),
        target_proxy_tokens: targetTotal,
        removed_proxy_tokens: selected.length,
        tolerance,
        target_by_region: targetByRegion,
        removed_by_region: actualByRegion,
        eligible_by_region: Object.fromEntries(regions.map((region) => [region, eligibleByRegion[region].length])),
        total_pass: totalPass,
        region_pass: regionPass,
        target_lines_protected: targetProtected,
        mechanical_pass: totalPass && regionPass && targetProtected,
      });
    }
    const passingReplicates = replicateRows.filter((replicate) => replicate.mechanical_pass).length;
    candidateRows.push({
      label: candidate.label,
      source_path: candidate.source_path,
      source_sha256: candidate.source_sha256,
      target_map_path: join(canonicalRoot, `${unit.unit_id}.json`),
      target_proxy_tokens: targetTotal,
      passing_replicates: passingReplicates,
      candidate_control_eligible: passingReplicates >= 2,
      replicates: replicateRows,
    });
  }
  units.push({
    unit_id: unit.unit_id,
    composition_id: unit.composition_id,
    target_field: unit.target_field,
    candidates: candidateRows,
    unit_control_eligible: candidateRows.every((candidate) => candidate.candidate_control_eligible),
  });
}

const manifest = {
  status: "RQ1_EXHAUSTIVE_PILOT_DAMAGE_CONTROLS_MATERIALIZED_NO_SELECTOR",
  boundary: "Local deterministic damage controls only; target-retention semantic review and scoring remain pending.",
  seeds,
  units,
};
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "DAMAGE_CONTROL_MANIFEST.json"), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({
  status: manifest.status,
  units: units.length,
  candidates: units.reduce((sum, unit) => sum + unit.candidates.length, 0),
  controls: units.reduce((sum, unit) => sum + unit.candidates.reduce((inner, candidate) => inner + candidate.replicates.length, 0), 0),
  eligible_units: units.filter((unit) => unit.unit_control_eligible).length,
}));
