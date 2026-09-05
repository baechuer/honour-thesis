#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const expectedFields = [
  "boundary_not_for",
  "dependency_resource",
  "input_precondition",
  "output_artifact",
  "success_verification",
  "use_condition",
  "workflow_procedure",
];
const validStatuses = new Set(["PRESENT", "NOT_PRESENT", "UNCERTAIN"]);
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const lineage = JSON.parse(await readFile(join(root, "source_packets/private_lineage_manifest.json"), "utf8"));
const ledger = JSON.parse(await readFile(join(root, "parse_ledger/parse_ledger.json"), "utf8"));
const lineageById = new Map(lineage.compositions.map((row) => [row.composition_id, row]));
const failures = [];
const fieldStatuses = {};
let evidenceSpans = 0;

for (const row of ledger.rows) {
  const sourceRow = lineageById.get(row.composition_id);
  if (!sourceRow) {
    failures.push({ composition_id: row.composition_id, issue: "MISSING_LINEAGE" });
    continue;
  }
  if (!["REUSED_VERIFIED_SOURCE_ONLY_PARSE", "PARSED_NEW_SOURCE_ONLY"].includes(row.parse_status)) {
    failures.push({ composition_id: row.composition_id, issue: "NONFINAL_PARSE_STATUS", status: row.parse_status });
    continue;
  }
  if (!Array.isArray(row.candidates) || row.candidates.length !== sourceRow.candidates.length) {
    failures.push({ composition_id: row.composition_id, issue: "CANDIDATE_COUNT_MISMATCH" });
    continue;
  }
  const sourceByLabel = new Map(sourceRow.candidates.map((candidate) => [candidate.label, candidate]));
  for (const candidate of row.candidates) {
    const source = sourceByLabel.get(candidate.label);
    if (!source) {
      failures.push({ composition_id: row.composition_id, candidate: candidate.label, issue: "UNKNOWN_CANDIDATE" });
      continue;
    }
    const bytes = await readFile(resolve(process.cwd(), source.packet_path));
    if (hash(bytes) !== source.source_sha256) {
      failures.push({ composition_id: row.composition_id, candidate: candidate.label, issue: "SOURCE_HASH_MISMATCH" });
      continue;
    }
    const lines = bytes.toString("utf8").split("\n");
    if (JSON.stringify(Object.keys(candidate.fields ?? {}).sort()) !== JSON.stringify(expectedFields)) {
      failures.push({ composition_id: row.composition_id, candidate: candidate.label, issue: "FIELD_SCHEMA_MISMATCH" });
      continue;
    }
    for (const field of expectedFields) {
      const record = candidate.fields[field];
      fieldStatuses[field] ??= {};
      fieldStatuses[field][record?.status] = (fieldStatuses[field][record?.status] ?? 0) + 1;
      if (!record || !validStatuses.has(record.status) || !Array.isArray(record.evidence)) {
        failures.push({ composition_id: row.composition_id, candidate: candidate.label, field, issue: "INVALID_FIELD_RECORD" });
        continue;
      }
      if ((record.status === "NOT_PRESENT" && record.evidence.length !== 0) || (record.status === "PRESENT" && record.evidence.length === 0)) {
        failures.push({ composition_id: row.composition_id, candidate: candidate.label, field, issue: "STATUS_EVIDENCE_MISMATCH" });
      }
      for (const evidence of record.evidence) {
        const quote = lines.slice(evidence.line_start - 1, evidence.line_end).join("\n");
        if (!Number.isInteger(evidence.line_start) || !Number.isInteger(evidence.line_end) || evidence.line_start < 1 || evidence.line_end < evidence.line_start || evidence.line_end > lines.length || evidence.quote !== quote) {
          failures.push({ composition_id: row.composition_id, candidate: candidate.label, field, issue: "NONEXACT_EVIDENCE", line_start: evidence.line_start, line_end: evidence.line_end });
        }
        evidenceSpans += 1;
      }
    }
  }
}

const result = {
  status: failures.length === 0 ? "RQ1_ORIGINAL_REMOVAL_V3_82_PARSE_AUDIT_PASS" : "RQ1_ORIGINAL_REMOVAL_V3_82_PARSE_AUDIT_FAIL",
  counts: {
    ledger_compositions: ledger.rows.length,
    lineage_compositions: lineage.compositions.length,
    reused_verified: ledger.rows.filter((row) => row.parse_status === "REUSED_VERIFIED_SOURCE_ONLY_PARSE").length,
    newly_parsed: ledger.rows.filter((row) => row.parse_status === "PARSED_NEW_SOURCE_ONLY").length,
    evidence_spans: evidenceSpans,
  },
  field_statuses: fieldStatuses,
  failures,
};
await mkdir(join(root, "audit"), { recursive: true });
await writeFile(join(root, "audit/parse_audit.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
if (failures.length) process.exitCode = 1;
