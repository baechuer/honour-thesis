#!/usr/bin/env node

import { copyFile, mkdir, readFile } from "node:fs/promises";
import { basename, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: node canonicalize_rq1_original_removal_v3_82_blind_residual_review.mjs <submission.json>");
const resolved = resolve(process.cwd(), submissionPath);
const validation = spawnSync(process.execPath, ["skill_benchmark/scripts/validate_rq1_original_removal_v3_82_blind_residual_review.mjs", resolved], { encoding: "utf8" });
process.stdout.write(validation.stdout);
process.stderr.write(validation.stderr);
if (validation.status !== 0) process.exit(validation.status ?? 1);
const submission = JSON.parse(await readFile(resolved, "utf8"));
const destination = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_submissions/canonical", `${submission.batch_id}.json`);
await mkdir(resolve(destination, ".."), { recursive: true });
await copyFile(resolved, destination);
console.log(JSON.stringify({ status: "CANONICALIZED", source: basename(resolved), destination }, null, 2));
