#!/usr/bin/env node

// Assemble the source-only S1 ledger once every independently validated batch
// is canonical. It deliberately has no access to prompts, labels, or scores.

import { execFileSync } from "node:child_process";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join, relative, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const packets = JSON.parse(await readFile(join(root, "eligibility_packets", "agent_packet_manifest.json"), "utf8"));
const canonicalRoot = join(root, "eligibility_submissions", "canonical");
const outputRoot = join(root, "eligibility_ledger");
const fields = packets.fields;
const expectedBatches = [...new Set(packets.compositions.map((item) => item.batch_id))].sort();
const files = new Set((await readdir(canonicalRoot)).filter((name) => /^batch_\d{2}\.json$/.test(name)));
const missing = expectedBatches.filter((batchId) => !files.has(`${batchId}.json`));
if (missing.length) throw new Error(`Cannot build incomplete ledger; missing canonical batches: ${missing.join(", ")}`);

const expectedByComposition = new Map(packets.compositions.map((item) => [item.composition_id, item]));
const rows = [];
for (const batchId of expectedBatches) {
  execFileSync(process.execPath, [
    "skill_benchmark/scripts/validate_rq1_original_removal_v3_82_eligibility_map.mjs",
    relative(repo, join(canonicalRoot, `${batchId}.json`)),
  ], { cwd: repo, stdio: "inherit" });
  const submission = JSON.parse(await readFile(join(canonicalRoot, `${batchId}.json`), "utf8"));
  if (submission.status !== "ELIGIBILITY_MAP_COMPLETE" || submission.batch_id !== batchId) throw new Error(`Invalid canonical status for ${batchId}.`);
  for (const composition of submission.compositions) {
    const expected = expectedByComposition.get(composition.composition_id);
    if (!expected || expected.batch_id !== batchId) throw new Error(`Unexpected composition ${composition.composition_id} in ${batchId}.`);
    const candidateByLabel = new Map(composition.candidates.map((candidate) => [candidate.label, candidate]));
    const conditionStates = {};
    for (const field of fields) {
      const candidateStatuses = expected.candidates.map((expectedCandidate) => {
        const map = candidateByLabel.get(expectedCandidate.label)?.field_maps?.[field];
        if (!map) throw new Error(`Missing ${composition.composition_id}/${expectedCandidate.label}/${field}.`);
        return { label: expectedCandidate.label, status: map.status };
      });
      const statuses = candidateStatuses.map((item) => item.status);
      const safe = statuses.every((status) => status === "SAFE_MAP" || status === "NO_DIRECT_VALUE");
      const editable = statuses.includes("SAFE_MAP");
      conditionStates[field] = {
        status: safe && editable ? "MAP_READY" : safe ? "NO_EDITABLE_VALUE" : "ORIGINAL_ONLY",
        candidate_statuses: candidateStatuses,
      };
    }
    rows.push({ composition_id: composition.composition_id, conditions: conditionStates });
  }
}
if (rows.length !== 82) throw new Error(`Expected 82 composition rows, got ${rows.length}.`);
const counts = Object.fromEntries(fields.map((field) => [field, {
  MAP_READY: rows.filter((row) => row.conditions[field].status === "MAP_READY").length,
  NO_EDITABLE_VALUE: rows.filter((row) => row.conditions[field].status === "NO_EDITABLE_VALUE").length,
  ORIGINAL_ONLY: rows.filter((row) => row.conditions[field].status === "ORIGINAL_ONLY").length,
}]));
await mkdir(outputRoot, { recursive: true });
const result = {
  status: "RQ1_ORIGINAL_REMOVAL_V3_82_S1_SOURCE_ONLY_ELIGIBILITY_COMPLETE",
  boundary: "Source-only removal mapping. MAP_READY still requires deterministic materialisation and an independent prompt/gold-blind residual review before any strict-family or selector use.",
  counts: { compositions: rows.length, by_field: counts },
  rows,
};
await writeFile(join(outputRoot, "eligibility_ledger.json"), `${JSON.stringify(result, null, 2)}\n`);
await writeFile(join(outputRoot, "ELIGIBILITY_SUMMARY.md"), [
  "# RQ1 82-Registry Source-Only Eligibility Summary",
  "",
  `Status: \`${result.status}\``,
  "",
  "| Field | Map-ready | No editable value | Original only |",
  "| --- | ---: | ---: | ---: |",
  ...fields.map((field) => `| ${field} | ${counts[field].MAP_READY} | ${counts[field].NO_EDITABLE_VALUE} | ${counts[field].ORIGINAL_ONLY} |`),
  "",
  "This is not a mask-residual, retrieval, or field-effect result.",
].join("\n") + "\n");
console.log(JSON.stringify({ status: result.status, compositions: rows.length, by_field: counts, output: relative(repo, outputRoot) }, null, 2));
