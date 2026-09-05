#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_v3_82_parse.mjs <submission.json>");

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const pending = JSON.parse(await readFile(join(root, "parse_ledger/pending_v3_source_only_parse_packets.json"), "utf8"));
const fields = [...pending.fields].sort();
const statuses = new Set(["PRESENT", "NOT_PRESENT", "UNCERTAIN"]);
const classifications = new Set(["DIRECT_VALUE", "GENERIC_CONTEXT", "CORRELATED_CONTEXT"]);
const carriers = new Set(["title", "heading", "prose", "step", "example", "code", "resource", "other"]);
const fail = (message) => { throw new Error(message); };
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
if (submission.status !== "PARSE_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.compositions) || submission.compositions.length !== 1) {
  fail("Submission must contain one PARSE_COMPLETE composition.");
}
const composition = submission.compositions[0];
const expected = pending.packets.find((packet) => packet.composition_id === composition.composition_id);
if (!expected || expected.batch_id !== submission.batch_id) fail("Unknown pending composition or batch mismatch.");
const expectedByLabel = new Map(expected.candidates.map((candidate) => [candidate.label, candidate]));
if (!Array.isArray(composition.candidates) || composition.candidates.length !== expectedByLabel.size) fail("Candidate count mismatch.");
const seen = new Set();
let evidenceSpans = 0;
for (const candidate of composition.candidates) {
  const expectedCandidate = expectedByLabel.get(candidate.label);
  if (!expectedCandidate || seen.has(candidate.label)) fail(`Unexpected or duplicate candidate ${candidate.label}.`);
  seen.add(candidate.label);
  if (JSON.stringify(Object.keys(candidate.fields ?? {}).sort()) !== JSON.stringify(fields)) fail(`Field schema mismatch for ${candidate.label}.`);
  const source = await readFile(resolve(repo, expectedCandidate.path), "utf8");
  const lines = source.split("\n");
  for (const field of fields) {
    const record = candidate.fields[field];
    if (!record || !statuses.has(record.status) || !Array.isArray(record.evidence)) fail(`Invalid field record ${candidate.label}/${field}.`);
    if (record.status === "NOT_PRESENT" && record.evidence.length !== 0) fail(`NOT_PRESENT must be empty: ${candidate.label}/${field}.`);
    if (record.status === "PRESENT" && record.evidence.length === 0) fail(`PRESENT needs evidence: ${candidate.label}/${field}.`);
    for (const evidence of record.evidence) {
      if (
        !Number.isInteger(evidence.line_start)
        || !Number.isInteger(evidence.line_end)
        || evidence.line_start < 1
        || evidence.line_end < evidence.line_start
        || evidence.line_end > lines.length
        || !classifications.has(evidence.classification)
        || !carriers.has(evidence.carrier)
        || typeof evidence.note !== "string"
        || Object.hasOwn(evidence, "quote")
      ) fail(`Invalid source evidence in ${candidate.label}/${field}.`);
      evidenceSpans += 1;
    }
  }
}
console.log(JSON.stringify({ status: "VALID", composition_id: composition.composition_id, batch_id: submission.batch_id, evidence_spans: evidenceSpans }));
