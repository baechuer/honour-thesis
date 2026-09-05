#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const [submissionPath, outputPath] = process.argv.slice(2);
if (!submissionPath || !outputPath) throw new Error("Usage: node canonicalize_rq1_original_removal_v3_82_parse.mjs <submission.json> <output.json>");

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const pending = JSON.parse(await readFile(join(root, "parse_ledger/pending_v3_source_only_parse_packets.json"), "utf8"));
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
const composition = submission.compositions?.[0];
const packet = pending.packets.find((entry) => entry.composition_id === composition?.composition_id);
if (!packet || packet.batch_id !== submission.batch_id) throw new Error("Unknown pending composition or batch mismatch.");
const pathByLabel = new Map(packet.candidates.map((candidate) => [candidate.label, candidate.path]));
for (const candidate of composition.candidates) {
  const source = await readFile(resolve(repo, pathByLabel.get(candidate.label)), "utf8");
  const lines = source.split("\n");
  for (const field of Object.values(candidate.fields)) {
    for (const evidence of field.evidence) evidence.quote = lines.slice(evidence.line_start - 1, evidence.line_end).join("\n");
  }
}
await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(submission, null, 2)}\n`);
console.log(JSON.stringify({ status: "CANONICALIZED", composition_id: composition.composition_id, output: outputPath }));
