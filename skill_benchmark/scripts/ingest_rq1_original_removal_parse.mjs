#!/usr/bin/env node

import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const args = process.argv.slice(2);
const requestedBatch = args[0] === "--batch" ? args[1] : null;
if (args.length !== 0 && (!requestedBatch || args.length !== 2)) {
  throw new Error("Usage: node ingest_rq1_original_removal_parse.mjs [--batch batch_01]");
}

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const packetsRoot = join(root, "source_packets");
const workRoot = join(root, "parse_submissions", "agent_work");
const canonicalRoot = join(root, "parse_submissions", "canonical");
const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];
const statuses = new Set(["PRESENT", "NOT_PRESENT", "UNCERTAIN"]);
const classifications = new Set(["DIRECT_VALUE", "GENERIC_CONTEXT", "CORRELATED_CONTEXT"]);
const carriers = new Set(["title", "heading", "prose", "step", "example", "code", "resource", "other"]);
const manifest = JSON.parse(await readFile(join(packetsRoot, "agent_packet_manifest.json"), "utf8"));
const expectedByBatch = new Map();
for (const composition of manifest.compositions) {
  const rows = expectedByBatch.get(composition.batch_id) ?? [];
  rows.push(composition);
  expectedByBatch.set(composition.batch_id, rows);
}

const fail = (message) => { throw new Error(message); };

async function canonicalise(inputPath) {
  const submission = JSON.parse(await readFile(inputPath, "utf8"));
  if (submission.status !== "PARSE_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.compositions)) {
    fail(`${inputPath}: expected PARSE_COMPLETE batch submission.`);
  }
  if (requestedBatch && submission.batch_id !== requestedBatch) {
    fail(`${inputPath}: does not match requested ${requestedBatch}.`);
  }
  const expected = expectedByBatch.get(submission.batch_id);
  if (!expected || submission.compositions.length !== expected.length) {
    fail(`${inputPath}: batch composition count mismatch.`);
  }

  const expectedCompositions = new Map(expected.map((row) => [row.composition_id, row]));
  const seenCompositions = new Set();
  let evidenceSpans = 0;
  for (const composition of submission.compositions) {
    const expectedComposition = expectedCompositions.get(composition.composition_id);
    if (!expectedComposition || seenCompositions.has(composition.composition_id)) {
      fail(`${inputPath}: unknown or duplicate composition ${composition.composition_id}.`);
    }
    seenCompositions.add(composition.composition_id);
    if (!Array.isArray(composition.candidates) || composition.candidates.length !== expectedComposition.candidates.length) {
      fail(`${inputPath}: candidate count mismatch for ${composition.composition_id}.`);
    }
    const expectedCandidates = new Map(expectedComposition.candidates.map((row) => [row.label, row]));
    const seenCandidates = new Set();
    for (const candidate of composition.candidates) {
      if (!expectedCandidates.has(candidate.label) || seenCandidates.has(candidate.label)) {
        fail(`${inputPath}: unknown or duplicate candidate ${composition.composition_id}/${candidate.label}.`);
      }
      seenCandidates.add(candidate.label);
      if (JSON.stringify(Object.keys(candidate.fields ?? {}).sort()) !== JSON.stringify([...fields].sort())) {
        fail(`${inputPath}: field key mismatch for ${composition.composition_id}/${candidate.label}.`);
      }
      const source = await readFile(join(packetsRoot, submission.batch_id, composition.composition_id, `${candidate.label}.md`), "utf8");
      const lines = source.split("\n");
      for (const fieldName of fields) {
        const record = candidate.fields[fieldName];
        if (!record || !statuses.has(record.status) || !Array.isArray(record.evidence)) {
          fail(`${inputPath}: invalid field record ${composition.composition_id}/${candidate.label}/${fieldName}.`);
        }
        if (record.status === "NOT_PRESENT" && record.evidence.length !== 0) {
          fail(`${inputPath}: NOT_PRESENT has evidence for ${composition.composition_id}/${candidate.label}/${fieldName}.`);
        }
        if (record.status === "PRESENT" && record.evidence.length === 0) {
          fail(`${inputPath}: PRESENT has no evidence for ${composition.composition_id}/${candidate.label}/${fieldName}.`);
        }
        for (const evidence of record.evidence) {
          if (!Number.isInteger(evidence.line_start) || !Number.isInteger(evidence.line_end) || evidence.line_start < 1 || evidence.line_end < evidence.line_start || evidence.line_end > lines.length) {
            fail(`${inputPath}: invalid evidence lines for ${composition.composition_id}/${candidate.label}/${fieldName}.`);
          }
          if (!classifications.has(evidence.classification) || !carriers.has(evidence.carrier) || typeof evidence.note !== "string") {
            fail(`${inputPath}: invalid evidence metadata for ${composition.composition_id}/${candidate.label}/${fieldName}.`);
          }
          evidence.quote = lines.slice(evidence.line_start - 1, evidence.line_end).join("\n");
          evidenceSpans += 1;
        }
      }
    }
  }
  return { submission, evidenceSpans };
}

const workFiles = (await readdir(workRoot))
  .filter((name) => /^batch_\d{2}\.json$/.test(name))
  .sort();
const selected = requestedBatch ? [`${requestedBatch}.json`] : workFiles;
if (selected.length === 0) fail("No agent-work parse files found.");

await mkdir(canonicalRoot, { recursive: true });
const summaries = [];
for (const fileName of selected) {
  const inputPath = join(workRoot, fileName);
  const { submission, evidenceSpans } = await canonicalise(inputPath);
  const outputPath = join(canonicalRoot, fileName);
  await writeFile(outputPath, `${JSON.stringify(submission, null, 2)}\n`);
  summaries.push({ batch_id: submission.batch_id, compositions: submission.compositions.length, evidence_spans: evidenceSpans, output: outputPath });
}

const currentCanonical = (await readdir(canonicalRoot))
  .filter((name) => /^batch_\d{2}\.json$/.test(name))
  .sort();
const remaining = [...expectedByBatch.keys()].sort().filter((batch) => !currentCanonical.includes(`${batch}.json`));
const completed = currentCanonical.length;
await writeFile(
  join(canonicalRoot, "INGESTION_STATUS.json"),
  `${JSON.stringify({
    status: remaining.length === 0 ? "COMPLETE" : "PARTIAL",
    canonical_batches: currentCanonical.map((name) => name.slice(0, -5)),
    completed_batches: completed,
    expected_batches: expectedByBatch.size,
    remaining_batches: remaining,
    latest_ingested: summaries,
  }, null, 2)}\n`,
);
console.log(JSON.stringify({ status: remaining.length === 0 ? "COMPLETE" : "PARTIAL", ingested: summaries, completed_batches: completed, expected_batches: expectedByBatch.size, remaining_batches: remaining }));
