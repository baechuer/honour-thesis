#!/usr/bin/env node

import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: ingest_rq1_exhaustive_ablation_full_clearance.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const source = resolve(submissionPath);
const submission = JSON.parse(await readFile(source, "utf8"));
const { spawnSync } = await import("node:child_process");
const validation = spawnSync(process.execPath, [
  resolve("skill_benchmark/scripts/validate_rq1_exhaustive_ablation_full_clearance.mjs"),
  source,
], { encoding: "utf8" });
if (validation.status !== 0) throw new Error(validation.stdout || validation.stderr || "clearance validation failed");
const canonicalRoot = join(root, "full_clearance", "canonical_round1");
await mkdir(canonicalRoot, { recursive: true });
const destination = join(canonicalRoot, `${submission.unit_id}.json`);
await copyFile(source, destination);
const clearCandidates = submission.candidates.filter((candidate) => candidate.status === "CLEAR").length;
console.log(JSON.stringify({
  status: "INGESTED",
  unit_id: submission.unit_id,
  target_field: submission.target_field,
  candidates: submission.candidates.length,
  clear_candidates: clearCandidates,
  all_clear: clearCandidates === submission.candidates.length,
}));
