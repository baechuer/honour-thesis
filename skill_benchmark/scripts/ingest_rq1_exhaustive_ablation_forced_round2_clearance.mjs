#!/usr/bin/env node

import { copyFile, mkdir } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const source = process.argv[2];
if (!source) throw new Error("Usage: ingest_rq1_exhaustive_ablation_forced_round2_clearance.mjs <submission.json>");
const resolvedSource = resolve(source);
const validation = spawnSync(process.execPath, ["skill_benchmark/scripts/validate_rq1_exhaustive_ablation_forced_round2_clearance.mjs", resolvedSource], { encoding: "utf8" });
if (validation.status !== 0) throw new Error(validation.stderr || validation.stdout || "validation failed");
const submission = JSON.parse(await (await import("node:fs/promises")).readFile(resolvedSource, "utf8"));
const destination = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_clearance/canonical_round2", `${submission.unit_id}.json`);
await mkdir(dirname(destination), { recursive: true });
await copyFile(resolvedSource, destination, 0);
console.log(JSON.stringify({ status: "RQ1_FORCED_ROUND2_FRESH_CLEARANCE_INGESTED", unit_id: submission.unit_id, destination, validation: validation.stdout.trim() }));
