#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) {
  throw new Error("Usage: node validate_rq1_original_removal_parse.mjs <submission.json>");
}

const root = resolve("skill_benchmark/rq1_public_original_removal_v2/source_packets");
const instructions = [
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

const fail = (message) => { throw new Error(message); };
const submission = JSON.parse(await readFile(submissionPath, "utf8"));
if (submission.status !== "PARSE_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.compositions)) {
  fail("Submission must contain PARSE_COMPLETE, batch_id, and compositions.");
}

const batchManifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const expected = batchManifest.compositions.filter((entry) => entry.batch_id === submission.batch_id);
if (expected.length === 0 || submission.compositions.length !== expected.length) {
  fail("Submission does not cover exactly one known batch.");
}

const expectedById = new Map(expected.map((entry) => [entry.composition_id, entry]));
const seenCompositions = new Set();
let evidenceCount = 0;
for (const composition of submission.compositions) {
  if (!expectedById.has(composition.composition_id) || seenCompositions.has(composition.composition_id)) {
    fail(`Unexpected or duplicate composition ${composition.composition_id}.`);
  }
  seenCompositions.add(composition.composition_id);
  const expectedCandidates = expectedById.get(composition.composition_id).candidates;
  if (!Array.isArray(composition.candidates) || composition.candidates.length !== expectedCandidates.length) {
    fail(`Candidate count mismatch for ${composition.composition_id}.`);
  }
  const expectedByLabel = new Map(expectedCandidates.map((candidate) => [candidate.label, candidate]));
  const seenCandidates = new Set();
  for (const candidate of composition.candidates) {
    if (!expectedByLabel.has(candidate.label) || seenCandidates.has(candidate.label)) {
      fail(`Unexpected or duplicate candidate in ${composition.composition_id}.`);
    }
    seenCandidates.add(candidate.label);
    const keys = Object.keys(candidate.fields ?? {}).sort();
    if (JSON.stringify(keys) !== JSON.stringify([...instructions].sort())) {
      fail(`Field key mismatch for ${composition.composition_id}/${candidate.label}.`);
    }
    const sourceText = await readFile(join(root, submission.batch_id, composition.composition_id, `${candidate.label}.md`), "utf8");
    for (const field of instructions) {
      const record = candidate.fields[field];
      if (!record || !statuses.has(record.status) || !Array.isArray(record.evidence)) {
        fail(`Invalid field record for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      if (record.status === "NOT_PRESENT" && record.evidence.length !== 0) {
        fail(`NOT_PRESENT must have no evidence for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      if (record.status === "PRESENT" && record.evidence.length === 0) {
        fail(`PRESENT must include source evidence for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      for (const evidence of record.evidence) {
        const lines = sourceText.split("\n");
        if (!Number.isInteger(evidence.line_start) || !Number.isInteger(evidence.line_end) || evidence.line_start < 1 || evidence.line_end < evidence.line_start || evidence.line_end > lines.length) {
          fail(`Invalid line range for ${composition.composition_id}/${candidate.label}/${field}.`);
        }
        if (!classifications.has(evidence.classification) || !carriers.has(evidence.carrier) || typeof evidence.note !== "string") {
          fail(`Invalid evidence metadata for ${composition.composition_id}/${candidate.label}/${field}.`);
        }
        evidenceCount += 1;
      }
    }
  }
}

console.log(JSON.stringify({ status: "VALID", batch_id: submission.batch_id, compositions: seenCompositions.size, evidence_spans: evidenceCount }));
