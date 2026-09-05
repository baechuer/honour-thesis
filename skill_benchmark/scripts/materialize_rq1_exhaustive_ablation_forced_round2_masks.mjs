#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const masks = JSON.parse(await readFile(join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"));
const canonicalRoot = join(root, "full_clearance", "canonical_round1");
const outputRoot = join(root, "forced_round2_masks");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const proxyTokens = (text) => text.match(/\S+/gu)?.length ?? 0;

const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";
const canonicalPathFor = (unit) => join(canonicalRoot, `${unit.unit_id}.json`);

function verifySpan(lines, span, context) {
  const actual = lines.slice(span.line_start - 1, span.line_end).join("\n");
  if (actual !== span.quote) {
    throw new Error(`${context}: residual quote mismatch at ${span.line_start}-${span.line_end}`);
  }
}

function redactResidualLines(masked, residualSpans, context) {
  const ending = endingOf(masked);
  const lines = masked.split(/\r?\n/);
  const removed = new Set();
  for (const span of residualSpans) {
    verifySpan(lines, span, context);
    for (let line = span.line_start; line <= span.line_end; line += 1) removed.add(line);
  }
  const forced = lines.map((line, index) => removed.has(index + 1) ? "" : line).join(ending);
  return { forced, lineNumbers: [...removed].sort((a, b) => a - b) };
}

function deletionStats(before, after) {
  const beforeTokens = proxyTokens(before);
  const afterTokens = proxyTokens(after);
  return {
    before_force_proxy_tokens: beforeTokens,
    force_removed_proxy_tokens: beforeTokens - afterTokens,
    after_force_proxy_tokens: afterTokens,
    force_removed_fraction_of_round1_mask: beforeTokens ? (beforeTokens - afterTokens) / beforeTokens : 0,
  };
}

const units = [];
let candidateCount = 0;
let residualCandidateCount = 0;
let forcedLineCount = 0;

for (const unit of masks.single_units) {
  const review = JSON.parse(await readFile(canonicalPathFor(unit), "utf8"));
  if (review.unit_id !== unit.unit_id || review.target_field !== unit.target_field) {
    throw new Error(`${unit.unit_id}: canonical review identity mismatch`);
  }
  const reviewByLabel = new Map(review.candidates.map((candidate) => [candidate.label, candidate]));
  const candidates = [];
  for (const candidate of unit.candidates) {
    const decision = reviewByLabel.get(candidate.label);
    if (!decision) throw new Error(`${unit.unit_id}/${candidate.label}: absent from canonical review`);
    const round1 = await readFile(candidate.masked_path, "utf8");
    if (sha256(round1) !== candidate.masked_sha256) {
      throw new Error(`${unit.unit_id}/${candidate.label}: round-one hash mismatch`);
    }
    const residualSpans = decision.status === "RESIDUAL" ? decision.residual_spans : [];
    const { forced, lineNumbers } = redactResidualLines(round1, residualSpans, `${unit.unit_id}/${candidate.label}`);
    const destination = join(outputRoot, "single", unit.target_field, unit.composition_id, `${candidate.label}.md`);
    await mkdir(dirname(destination), { recursive: true });
    await writeFile(destination, forced);
    if (decision.status === "RESIDUAL") residualCandidateCount += 1;
    forcedLineCount += lineNumbers.length;
    candidateCount += 1;
    candidates.push({
      label: candidate.label,
      source_path: candidate.source_path,
      round1_masked_path: candidate.masked_path,
      round1_masked_sha256: candidate.masked_sha256,
      round1_clearance_status: decision.status,
      residual_spans_removed: residualSpans,
      forced_removed_line_numbers: lineNumbers,
      forced_masked_path: destination,
      forced_masked_sha256: sha256(forced),
      ...deletionStats(round1, forced),
    });
  }
  units.push({
    unit_id: unit.unit_id,
    composition_id: unit.composition_id,
    target_field: unit.target_field,
    candidates,
  });
}

const manifest = {
  status: "RQ1_EXHAUSTIVE_ABLATION_FORCED_ROUND2_MASKS_MATERIALIZED_NO_SELECTOR",
  boundary: "Deterministic second-pass deletion of every exact residual span cited in the canonical round-one blind-clearance ledger. This is a routing-only representation transformation. It can damage or make skills non-executable, and it does not itself establish complete target-field removal; fresh blind clearance is required.",
  parent_round1_mask_manifest: join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json"),
  parent_round1_clearance_ledger: canonicalRoot,
  single_unit_count: units.length,
  candidate_count: candidateCount,
  round1_residual_candidate_count: residualCandidateCount,
  forced_removed_line_count: forcedLineCount,
  units,
};
if (manifest.single_unit_count !== 574 || manifest.candidate_count !== 1855 || manifest.round1_residual_candidate_count !== 1145) {
  throw new Error(`Unexpected coverage: ${JSON.stringify({ units: manifest.single_unit_count, candidates: manifest.candidate_count, residuals: manifest.round1_residual_candidate_count })}`);
}
await mkdir(outputRoot, { recursive: true });
const manifestPath = join(outputRoot, "FORCED_ROUND2_MASK_MANIFEST.json");
await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({
  status: manifest.status,
  units: manifest.single_unit_count,
  candidates: manifest.candidate_count,
  round1_residual_candidates: manifest.round1_residual_candidate_count,
  forced_removed_lines: manifest.forced_removed_line_count,
  manifest_sha256: sha256(await readFile(manifestPath, "utf8")),
}));
