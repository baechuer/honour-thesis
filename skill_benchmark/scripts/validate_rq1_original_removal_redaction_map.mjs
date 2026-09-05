#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const [submissionPath] = process.argv.slice(2);
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_redaction_map.mjs <submission.json>");

const root = resolve("skill_benchmark/rq1_public_original_removal_v2/redaction_packets");
const fields = ["use_condition", "input_precondition", "output_artifact", "workflow_procedure", "success_verification", "boundary_not_for", "dependency_resource"];
const statuses = new Set(["SAFE_MAP", "NO_DIRECT_VALUE", "UNSAFE_MIXED_CARRIER", "UNCERTAIN"]);
const editKinds = new Set(["DELETE_LINE", "REWRITE_LINE"]);
const fail = (message) => { throw new Error(message); };

const submission = JSON.parse(await readFile(submissionPath, "utf8"));
if (submission.status !== "REDACTION_MAP_COMPLETE" || typeof submission.batch_id !== "string" || !Array.isArray(submission.compositions)) {
  fail("Expected REDACTION_MAP_COMPLETE batch submission.");
}
const manifest = JSON.parse(await readFile(join(root, "agent_packet_manifest.json"), "utf8"));
const batch = manifest.batches.find((entry) => entry.batch_id === submission.batch_id);
if (!batch || submission.compositions.length !== batch.compositions.length) fail("Batch composition count mismatch.");
const expectedByComposition = new Map(batch.compositions.map((entry) => [entry.composition_id, entry]));
const seenCompositions = new Set();
let maps = 0;
let safeMaps = 0;

for (const composition of submission.compositions) {
  const expected = expectedByComposition.get(composition.composition_id);
  if (!expected || seenCompositions.has(composition.composition_id)) fail(`Unknown or duplicate composition ${composition.composition_id}.`);
  seenCompositions.add(composition.composition_id);
  if (!Array.isArray(composition.candidates) || composition.candidates.length !== expected.candidates.length) fail(`Candidate count mismatch for ${composition.composition_id}.`);
  const expectedLabels = new Set(expected.candidates);
  const seenCandidates = new Set();
  for (const candidate of composition.candidates) {
    if (!expectedLabels.has(candidate.label) || seenCandidates.has(candidate.label)) fail(`Unexpected candidate ${composition.composition_id}/${candidate.label}.`);
    seenCandidates.add(candidate.label);
    const directEvidence = JSON.parse(await readFile(join(root, submission.batch_id, composition.composition_id, "field_evidence.json"), "utf8"))
      .candidates.find((entry) => entry.label === candidate.label).direct_evidence;
    if (JSON.stringify(Object.keys(candidate.field_maps ?? {}).sort()) !== JSON.stringify([...fields].sort())) {
      fail(`Field key mismatch for ${composition.composition_id}/${candidate.label}.`);
    }
    for (const field of fields) {
      const map = candidate.field_maps[field];
      if (!map || !statuses.has(map.status) || !Array.isArray(map.edits) || !Array.isArray(map.covered_evidence_ids)) {
        fail(`Invalid field map for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      const expectedEvidenceIds = directEvidence[field].map((entry) => entry.evidence_id).sort();
      const covered = [...map.covered_evidence_ids].sort();
      if (map.status === "SAFE_MAP") {
        if (expectedEvidenceIds.length === 0) {
          fail(`SAFE_MAP cannot be used without direct evidence for ${composition.composition_id}/${candidate.label}/${field}.`);
        }
        if (JSON.stringify(covered) !== JSON.stringify(expectedEvidenceIds) || (expectedEvidenceIds.length > 0 && map.edits.length === 0)) {
          fail(`SAFE_MAP must cover direct evidence exactly for ${composition.composition_id}/${candidate.label}/${field}.`);
        }
        const directById = new Map(directEvidence[field].map((entry) => [entry.evidence_id, entry]));
        const editsCovered = new Set();
        for (const edit of map.edits) {
          if (!editKinds.has(edit.kind) || !Number.isInteger(edit.line_start) || !Number.isInteger(edit.line_end) || edit.line_start < 1 || edit.line_end < edit.line_start || !Array.isArray(edit.evidence_ids) || edit.evidence_ids.length === 0 || typeof edit.rationale !== "string") {
            fail(`Invalid edit for ${composition.composition_id}/${candidate.label}/${field}.`);
          }
          if (edit.kind === "REWRITE_LINE" && typeof edit.replacement !== "string") {
            fail(`REWRITE_LINE needs replacement for ${composition.composition_id}/${candidate.label}/${field}.`);
          }
          if (edit.kind === "REWRITE_LINE" && edit.line_start !== edit.line_end) {
            fail(`REWRITE_LINE must edit exactly one source line for ${composition.composition_id}/${candidate.label}/${field}.`);
          }
          if (edit.kind === "DELETE_LINE" && "replacement" in edit && edit.replacement !== "") {
            fail(`DELETE_LINE must have no replacement for ${composition.composition_id}/${candidate.label}/${field}.`);
          }
          for (const evidenceId of edit.evidence_ids) {
            const evidence = directById.get(evidenceId);
            if (!evidence || edit.line_start < evidence.line_start || edit.line_end > evidence.line_end) {
              fail(`Edit must stay within cited direct evidence for ${composition.composition_id}/${candidate.label}/${field}.`);
            }
            editsCovered.add(evidenceId);
          }
        }
        if (JSON.stringify([...editsCovered].sort()) !== JSON.stringify(expectedEvidenceIds)) {
          fail(`Edits must cover each direct evidence id for ${composition.composition_id}/${candidate.label}/${field}.`);
        }
        safeMaps += 1;
      } else if (map.edits.length !== 0 || map.covered_evidence_ids.length !== 0) {
        fail(`Non-safe map cannot contain edits or covered ids for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      if (map.status === "NO_DIRECT_VALUE" && expectedEvidenceIds.length !== 0) {
        fail(`NO_DIRECT_VALUE conflicts with direct evidence for ${composition.composition_id}/${candidate.label}/${field}.`);
      }
      maps += 1;
    }
  }
}
console.log(JSON.stringify({ status: "VALID", batch_id: submission.batch_id, compositions: seenCompositions.size, candidate_field_maps: maps, safe_maps: safeMaps }));
