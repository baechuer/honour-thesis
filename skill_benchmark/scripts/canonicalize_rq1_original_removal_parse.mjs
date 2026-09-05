#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

const [submissionPath, outputPath] = process.argv.slice(2);
if (!submissionPath || !outputPath) {
  throw new Error("Usage: node canonicalize_rq1_original_removal_parse.mjs <submission.json> <output.json>");
}

const root = resolve("skill_benchmark/rq1_public_original_removal_v2/source_packets");
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
for (const composition of submission.compositions) {
  for (const candidate of composition.candidates) {
    const source = await readFile(join(root, submission.batch_id, composition.composition_id, `${candidate.label}.md`), "utf8");
    const lines = source.split("\n");
    for (const field of Object.values(candidate.fields)) {
      for (const evidence of field.evidence) {
        evidence.quote = lines.slice(evidence.line_start - 1, evidence.line_end).join("\n");
      }
    }
  }
}

await mkdir(dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(submission, null, 2)}\n`);
console.log(JSON.stringify({ status: "CANONICALIZED", batch_id: submission.batch_id, output: outputPath }));
