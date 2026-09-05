#!/usr/bin/env node

import { copyFile, mkdir, readFile } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: canonicalize_rq1_exhaustive_ablation_map.mjs <submission.json>");
const source = resolve(submissionPath);
const validation = spawnSync(process.execPath, ["skill_benchmark/scripts/validate_rq1_exhaustive_ablation_map.mjs", source], { encoding: "utf8" });
process.stdout.write(validation.stdout);
process.stderr.write(validation.stderr);
if (validation.status !== 0) process.exit(validation.status ?? 1);
const submission = JSON.parse(await readFile(source, "utf8"));
const outputRoot = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1", "pilot_maps", "canonical");
await mkdir(outputRoot, { recursive: true });
const destination = resolve(outputRoot, `${submission.unit_id}.json`);
await copyFile(source, destination);
console.log(JSON.stringify({ status: "CANONICALIZED", source: basename(source), destination }));
