#!/usr/bin/env node

import { copyFile, mkdir } from "node:fs/promises";
import { basename, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: ingest_rq1_exhaustive_ablation_forced_round3_clearance.mjs <submission.json>");
const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const validator = resolve("skill_benchmark/scripts/validate_rq1_exhaustive_ablation_forced_round3_clearance.mjs");
const validation = spawnSync(process.execPath, [validator, resolve(submissionPath)], { encoding: "utf8" });
if (validation.status !== 0) throw new Error(validation.stderr || validation.stdout || "validation failed");
const destinationRoot = join(root, "forced_round3_clearance", "canonical_round3");
await mkdir(destinationRoot, { recursive: true });
const destination = join(destinationRoot, basename(submissionPath));
await copyFile(resolve(submissionPath), destination);
console.log(JSON.stringify({ status: "RQ1_FORCED_ROUND3_FRESH_CLEARANCE_INGESTED", destination, validation: validation.stdout.trim() }));
