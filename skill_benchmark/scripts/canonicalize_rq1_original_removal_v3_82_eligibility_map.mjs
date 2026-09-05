#!/usr/bin/env node

// Promote one validated agent eligibility map without modifying its content.

import { execFileSync } from "node:child_process";
import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { basename, join, relative, resolve } from "node:path";

const sourceArgument = process.argv[2];
if (!sourceArgument) throw new Error("Usage: node canonicalize_rq1_original_removal_v3_82_eligibility_map.mjs <agent_submission.json>");
const supersedeInvalid = process.argv.includes("--supersede-invalid");
const repo = process.cwd();
const sourcePath = resolve(repo, sourceArgument);
const source = JSON.parse(await readFile(sourcePath, "utf8"));
const batchId = source.batch_id;
if (!/^batch_\d{2}$/.test(batchId ?? "")) throw new Error("Submission has invalid batch_id.");

execFileSync(process.execPath, [
  "skill_benchmark/scripts/validate_rq1_original_removal_v3_82_eligibility_map.mjs",
  relative(repo, sourcePath),
], { cwd: repo, stdio: "inherit" });

const destinationDir = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_submissions/canonical");
const destinationPath = join(destinationDir, `${batchId}.json`);
try {
  await stat(destinationPath);
  if (!supersedeInvalid) throw new Error(`Refusing to overwrite canonical submission: ${relative(repo, destinationPath)}`);
  let existingIsValid = true;
  try {
    execFileSync(process.execPath, [
      "skill_benchmark/scripts/validate_rq1_original_removal_v3_82_eligibility_map.mjs",
      relative(repo, destinationPath),
    ], { cwd: repo, stdio: "ignore" });
  } catch (error) {
    existingIsValid = false;
  }
  if (existingIsValid) throw new Error(`Refusing to supersede a valid canonical submission: ${relative(repo, destinationPath)}`);
  const archiveDir = join(destinationDir, "superseded");
  await mkdir(archiveDir, { recursive: true });
  await copyFile(destinationPath, join(archiveDir, `${batchId}.pre_quality_amendment.json`));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
await mkdir(destinationDir, { recursive: true });
await copyFile(sourcePath, destinationPath);
console.log(JSON.stringify({ status: "CANONICALIZED", source: basename(sourcePath), destination: relative(repo, destinationPath) }, null, 2));
