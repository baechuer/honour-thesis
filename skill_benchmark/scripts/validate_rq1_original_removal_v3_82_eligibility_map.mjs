#!/usr/bin/env node

// Validate one prompt/label-free S1 eligibility-map submission against its
// source packet. This is structural validation, not a residual or routing test.

import { readFile } from "node:fs/promises";
import { basename, resolve } from "node:path";

const submissionPath = process.argv[2];
if (!submissionPath) throw new Error("Usage: node validate_rq1_original_removal_v3_82_eligibility_map.mjs <submission.json>");
const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const packetsRoot = resolve(root, "eligibility_packets");
const fields = [
  "use_condition", "input_precondition", "output_artifact", "workflow_procedure",
  "success_verification", "boundary_not_for", "dependency_resource",
];
const allowedStatuses = new Set(["SAFE_MAP", "NO_DIRECT_VALUE", "UNSAFE_MIXED_CARRIER", "UNCERTAIN"]);
const submission = JSON.parse(await readFile(resolve(repo, submissionPath), "utf8"));
const failures = [];
const addFailure = (message) => failures.push(message);

if (submission.status !== "ELIGIBILITY_MAP_COMPLETE") addFailure("status must be ELIGIBILITY_MAP_COMPLETE");
if (!/^batch_\d{2}$/.test(submission.batch_id ?? "")) addFailure("invalid batch_id");
const batchDir = resolve(packetsRoot, submission.batch_id ?? "missing");
const manifest = JSON.parse(await readFile(resolve(packetsRoot, "agent_packet_manifest.json"), "utf8"));
const expectedCompositions = manifest.compositions.filter((row) => row.batch_id === submission.batch_id);
const actualCompositions = new Map((submission.compositions ?? []).map((row) => [row.composition_id, row]));
if (actualCompositions.size !== expectedCompositions.length) addFailure("composition coverage mismatch");

for (const expectedComposition of expectedCompositions) {
  const actualComposition = actualCompositions.get(expectedComposition.composition_id);
  if (!actualComposition) { addFailure(`missing composition ${expectedComposition.composition_id}`); continue; }
  const evidencePath = resolve(batchDir, expectedComposition.composition_id, "field_evidence.json");
  const packetEvidence = JSON.parse(await readFile(evidencePath, "utf8"));
  const evidenceByCandidate = new Map(packetEvidence.candidates.map((candidate) => [candidate.label, candidate.direct_evidence]));
  const actualCandidates = new Map((actualComposition.candidates ?? []).map((candidate) => [candidate.label, candidate]));
  if (actualCandidates.size !== expectedComposition.candidates.length) addFailure(`${expectedComposition.composition_id}: candidate coverage mismatch`);

  for (const expectedCandidate of expectedComposition.candidates) {
    const actualCandidate = actualCandidates.get(expectedCandidate.label);
    if (!actualCandidate) { addFailure(`${expectedComposition.composition_id}: missing ${expectedCandidate.label}`); continue; }
    const sourcePath = resolve(batchDir, expectedComposition.composition_id, expectedCandidate.path);
    const sourceLines = (await readFile(sourcePath, "utf8")).split("\n");
    const maps = actualCandidate.field_maps ?? {};
    if (JSON.stringify(Object.keys(maps).sort()) !== JSON.stringify([...fields].sort())) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}: seven-field coverage mismatch`);

    for (const field of fields) {
      const map = maps[field];
      if (!map || !allowedStatuses.has(map.status)) { addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: invalid or missing status`); continue; }
      const supplied = evidenceByCandidate.get(expectedCandidate.label)?.[field] ?? [];
      const suppliedIds = new Set(supplied.map((item) => item.evidence_id));
      const additional = map.additional_direct_evidence ?? [];
      const additionalIds = new Set();
      for (const item of additional) {
        if (!/^.+_extra_\d+$/.test(item.evidence_id ?? "")) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: invalid additional evidence id`);
        if (additionalIds.has(item.evidence_id)) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: duplicate additional evidence id`);
        additionalIds.add(item.evidence_id);
        if (!Number.isInteger(item.line_start) || !Number.isInteger(item.line_end) || item.line_start < 1 || item.line_end < item.line_start || item.line_end > sourceLines.length) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: additional evidence range outside source`);
      }
      const knownIds = new Set([...suppliedIds, ...additionalIds]);
      const rangeByEvidenceId = new Map([
        ...supplied.map((item) => [item.evidence_id, item]),
        ...additional.map((item) => [item.evidence_id, item]),
      ]);
      const covered = map.covered_evidence_ids ?? [];
      const edits = map.edits ?? [];
      if (typeof map.rationale !== "string" || map.rationale.trim().length < 12) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: missing specific rationale`);
      if (map.status === "SAFE_MAP") {
        for (const evidenceId of knownIds) if (!covered.includes(evidenceId)) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: SAFE_MAP misses ${evidenceId}`);
        if (knownIds.size === 0) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: SAFE_MAP has no direct evidence`);
        if (edits.length === 0) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: SAFE_MAP has no edits`);
      } else {
        if (edits.length || additional.length) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: non-safe map contains edits or additional evidence`);
        for (const evidenceId of covered) if (!suppliedIds.has(evidenceId)) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: non-safe map cites unknown supplied evidence ${evidenceId}`);
        if (map.status === "NO_DIRECT_VALUE" && suppliedIds.size > 0) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: NO_DIRECT_VALUE contradicts source evidence`);
      }
      const blocking = map.blocking_evidence ?? [];
      if (map.status === "UNSAFE_MIXED_CARRIER") {
        if (!Array.isArray(blocking) || blocking.length === 0) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: unsafe map lacks blocking evidence`);
        for (const item of blocking) {
          if (!Number.isInteger(item.line_start) || !Number.isInteger(item.line_end) || item.line_start < 1 || item.line_end < item.line_start || item.line_end > sourceLines.length) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: blocking evidence outside source`);
          if (typeof item.non_target_content !== "string" || item.non_target_content.trim().length < 8) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: blocking evidence lacks named non-target content`);
        }
      } else if (blocking.length) {
        addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: only unsafe maps may contain blocking evidence`);
      }
      for (const edit of edits) {
        if (!new Set(["DELETE_LINE", "REWRITE_LINE"]).has(edit.kind)) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: invalid edit kind`);
        if (!Number.isInteger(edit.line_start) || !Number.isInteger(edit.line_end) || edit.line_start < 1 || edit.line_end < edit.line_start || edit.line_end > sourceLines.length) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: edit range outside source`);
        if (!Array.isArray(edit.evidence_ids) || edit.evidence_ids.length === 0) addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: edit lacks evidence ids`);
        for (const evidenceId of edit.evidence_ids ?? []) {
          if (!knownIds.has(evidenceId)) {
            addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: edit cites unknown ${evidenceId}`);
            continue;
          }
          const evidence = rangeByEvidenceId.get(evidenceId);
          if (edit.line_start < evidence.line_start || edit.line_end > evidence.line_end) {
            addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: edit extends beyond ${evidenceId}`);
          }
        }
        if (edit.kind === "REWRITE_LINE" && typeof edit.replacement !== "string") addFailure(`${expectedComposition.composition_id}/${expectedCandidate.label}/${field}: rewrite lacks replacement`);
      }
    }
  }
}

const result = { status: failures.length ? "FAIL" : "PASS", submission: basename(submissionPath), failures };
console.log(JSON.stringify(result, null, 2));
process.exitCode = failures.length ? 1 : 0;
