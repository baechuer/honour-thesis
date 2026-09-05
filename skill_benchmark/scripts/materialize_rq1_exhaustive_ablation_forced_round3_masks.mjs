#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const masks = JSON.parse(await readFile(join(root, "forced_round2_masks", "FORCED_ROUND2_MASK_MANIFEST.json"), "utf8"));
const canonicalRoot = join(root, "forced_round2_clearance", "canonical_round2");
const outputRoot = join(root, "forced_round3_masks");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const proxyTokens = (text) => text.match(/\S+/gu)?.length ?? 0;
const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";

function verifySpan(lines, span, context) {
  const actual = lines.slice(span.line_start - 1, span.line_end).join("\n");
  if (actual !== span.quote) throw new Error(`${context}: residual quote mismatch at ${span.line_start}-${span.line_end}`);
}

function redactResidualLines(masked, residualSpans, context) {
  const lines = masked.split(/\r?\n/);
  const removed = new Set();
  for (const span of residualSpans) {
    verifySpan(lines, span, context);
    for (let line = span.line_start; line <= span.line_end; line += 1) removed.add(line);
  }
  return {
    text: lines.map((line, index) => removed.has(index + 1) ? "" : line).join(endingOf(masked)),
    lineNumbers: [...removed].sort((a, b) => a - b),
  };
}

function deletionStats(before, after) {
  const beforeTokens = proxyTokens(before);
  const afterTokens = proxyTokens(after);
  return {
    before_round3_proxy_tokens: beforeTokens,
    round3_removed_proxy_tokens: beforeTokens - afterTokens,
    after_round3_proxy_tokens: afterTokens,
    round3_removed_fraction_of_round2_mask: beforeTokens ? (beforeTokens - afterTokens) / beforeTokens : 0,
  };
}

const units = [];
let candidateCount = 0;
let residualCandidateCount = 0;
let clearCandidateCount = 0;
let uncertainCandidateCount = 0;
let removedLineCount = 0;

for (const unit of masks.units) {
  const review = JSON.parse(await readFile(join(canonicalRoot, `${unit.unit_id}.json`), "utf8"));
  if (review.unit_id !== unit.unit_id || review.target_field !== unit.target_field) {
    throw new Error(`${unit.unit_id}: canonical Round-2 review identity mismatch`);
  }
  const decisions = new Map(review.candidates.map((candidate) => [candidate.label, candidate]));
  const candidates = [];
  for (const candidate of unit.candidates) {
    const decision = decisions.get(candidate.label);
    if (!decision) throw new Error(`${unit.unit_id}/${candidate.label}: absent from canonical Round-2 review`);
    const round2 = await readFile(candidate.forced_masked_path, "utf8");
    if (sha256(round2) !== candidate.forced_masked_sha256) throw new Error(`${unit.unit_id}/${candidate.label}: Round-2 hash mismatch`);
    const residualSpans = decision.status === "RESIDUAL" ? decision.residual_spans : [];
    const { text: round3, lineNumbers } = redactResidualLines(round2, residualSpans, `${unit.unit_id}/${candidate.label}`);
    const destination = join(outputRoot, "single", unit.target_field, unit.composition_id, `${candidate.label}.md`);
    await mkdir(dirname(destination), { recursive: true });
    await writeFile(destination, round3);
    candidateCount += 1;
    removedLineCount += lineNumbers.length;
    if (decision.status === "RESIDUAL") residualCandidateCount += 1;
    if (decision.status === "CLEAR") clearCandidateCount += 1;
    if (decision.status === "UNCERTAIN") uncertainCandidateCount += 1;
    candidates.push({
      label: candidate.label,
      source_path: candidate.source_path,
      round2_masked_path: candidate.forced_masked_path,
      round2_masked_sha256: candidate.forced_masked_sha256,
      round2_clearance_status: decision.status,
      residual_spans_removed: residualSpans,
      round3_removed_line_numbers: lineNumbers,
      round3_masked_path: destination,
      round3_masked_sha256: sha256(round3),
      ...deletionStats(round2, round3),
    });
  }
  units.push({ unit_id: unit.unit_id, composition_id: unit.composition_id, target_field: unit.target_field, candidates });
}

const manifest = {
  status: "RQ1_EXHAUSTIVE_ABLATION_FORCED_ROUND3_MASKS_MATERIALIZED_NO_SELECTOR",
  boundary: "Deterministic deletion of exact spans cited by the canonical Round-2 fresh-clearance ledger. Round-2 clear and uncertain cards are copied unchanged. This routing-only transformation does not establish complete target-field removal; fresh blind clearance remains required.",
  parent_round2_mask_manifest: join(root, "forced_round2_masks", "FORCED_ROUND2_MASK_MANIFEST.json"),
  parent_round2_clearance_ledger: canonicalRoot,
  single_unit_count: units.length,
  candidate_count: candidateCount,
  round2_residual_candidate_count: residualCandidateCount,
  round2_clear_candidate_count: clearCandidateCount,
  round2_uncertain_candidate_count: uncertainCandidateCount,
  forced_removed_line_count: removedLineCount,
  units,
};
if (manifest.single_unit_count !== 574 || manifest.candidate_count !== 1855 || manifest.round2_residual_candidate_count !== 383 || manifest.round2_clear_candidate_count !== 1464 || manifest.round2_uncertain_candidate_count !== 8) {
  throw new Error(`Unexpected coverage: ${JSON.stringify({ units: manifest.single_unit_count, candidates: manifest.candidate_count, residuals: manifest.round2_residual_candidate_count, clear: manifest.round2_clear_candidate_count, uncertain: manifest.round2_uncertain_candidate_count })}`);
}
await mkdir(outputRoot, { recursive: true });
const manifestPath = join(outputRoot, "FORCED_ROUND3_MASK_MANIFEST.json");
await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ status: manifest.status, units: manifest.single_unit_count, candidates: manifest.candidate_count, round2_residual_candidates: manifest.round2_residual_candidate_count, forced_removed_lines: manifest.forced_removed_line_count, manifest_sha256: sha256(await readFile(manifestPath, "utf8")) }));
