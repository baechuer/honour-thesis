#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifestPath = join(root, "full_target_masks", "TARGET_MASK_MANIFEST.json");
const auditRoot = join(root, "full_target_masks", "audit");
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const proxyTokens = (text) => text.match(/\S+/gu)?.length ?? 0;
const endingOf = (text) => text.includes("\r\n") ? "\r\n" : "\n";
const failures = [];
let checked = 0;
let nearEmpty = 0;
let zeroRemoval = 0;
const auditCandidate = async (candidate, context) => {
  const source = await readFile(candidate.source_path, "utf8");
  const masked = await readFile(candidate.masked_path, "utf8");
  const expected = source.split(/\r?\n/).map((line, index) => candidate.removed_line_numbers.includes(index + 1) ? "" : line).join(endingOf(source));
  if (sha256(source) !== candidate.source_sha256) failures.push(`${context}: source hash mismatch`);
  if (sha256(masked) !== candidate.masked_sha256) failures.push(`${context}: masked hash mismatch`);
  if (masked !== expected) failures.push(`${context}: non-target diff detected`);
  const originalTokens = proxyTokens(source);
  const remainingTokens = proxyTokens(masked);
  if (candidate.original_proxy_tokens !== originalTokens) failures.push(`${context}: original token count mismatch`);
  if (candidate.remaining_proxy_tokens !== remainingTokens) failures.push(`${context}: remaining token count mismatch`);
  if (candidate.removed_proxy_tokens !== originalTokens - remainingTokens) failures.push(`${context}: removed token count mismatch`);
  if (candidate.removed_proxy_tokens === 0) zeroRemoval += 1;
  if (candidate.near_empty) nearEmpty += 1;
  checked += 1;
};

for (const unit of manifest.single_units) {
  for (const candidate of unit.candidates) await auditCandidate(candidate, `single/${unit.unit_id}/${candidate.label}`);
}
for (const unit of manifest.joint_units) {
  for (const candidate of unit.candidates) await auditCandidate(candidate, `joint/${unit.composition_id}/${unit.group}/${candidate.label}`);
}

const audit = {
  status: failures.length ? "FAIL" : "PASS",
  boundary: "Exact-diff and manifest-integrity audit only; zero-removal and near-empty cases are reported, not excluded.",
  checked_candidate_masks: checked,
  expected_candidate_masks: manifest.candidate_mask_count,
  zero_removal_candidate_masks: zeroRemoval,
  near_empty_candidate_masks: nearEmpty,
  failure_count: failures.length,
  failures,
};
if (checked !== manifest.candidate_mask_count) failures.push(`checked ${checked}, expected ${manifest.candidate_mask_count}`);
audit.status = failures.length ? "FAIL" : "PASS";
audit.failure_count = failures.length;
await mkdir(auditRoot, { recursive: true });
await writeFile(join(auditRoot, "exact_diff_audit.json"), `${JSON.stringify(audit, null, 2)}\n`);
console.log(JSON.stringify(audit));
if (failures.length) process.exitCode = 1;
