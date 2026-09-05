#!/usr/bin/env node

// Create prompt/label-free S1 removal-mapping packets from the 82-registry
// source-only parse ledger. This does not materialise any masked documents.

import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { join, relative, resolve } from "node:path";

const repo = process.cwd();
const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const sourceRoot = join(root, "source_packets");
const outputRoot = join(root, "eligibility_packets");
const ledgerPath = join(root, "parse_ledger", "parse_ledger.json");
const lineagePath = join(sourceRoot, "private_lineage_manifest.json");
const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];
const batchSize = 3;
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

try {
  await stat(outputRoot);
  throw new Error(`Refusing to overwrite existing output root: ${relative(repo, outputRoot)}`);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}

const ledger = await readJson(ledgerPath);
const lineage = await readJson(lineagePath);
if (ledger.rows?.length !== 82 || lineage.compositions?.length !== 82) {
  throw new Error("Expected a complete 82-composition source-only ledger.");
}
const lineageById = new Map(lineage.compositions.map((row) => [row.composition_id, row]));
const packetRows = [];

await mkdir(outputRoot, { recursive: true });
for (const [index, row] of ledger.rows.entries()) {
  const source = lineageById.get(row.composition_id);
  if (!source || source.candidates.length !== row.candidates.length) {
    throw new Error(`Lineage mismatch for ${row.composition_id}.`);
  }
  const batchId = `batch_${String(Math.floor(index / batchSize) + 1).padStart(2, "0")}`;
  const packetDir = join(outputRoot, batchId, row.composition_id);
  await mkdir(packetDir, { recursive: true });
  const candidates = [];

  for (const parsedCandidate of row.candidates) {
    const sourceCandidate = source.candidates.find((candidate) => candidate.label === parsedCandidate.label);
    if (!sourceCandidate) throw new Error(`Missing source candidate ${row.composition_id}/${parsedCandidate.label}.`);
    const sourcePath = resolve(repo, sourceCandidate.packet_path);
    const bytes = await readFile(sourcePath);
    if (sha256(bytes) !== sourceCandidate.source_sha256) {
      throw new Error(`Packet source hash mismatch for ${row.composition_id}/${parsedCandidate.label}.`);
    }
    const targetPath = join(packetDir, `${parsedCandidate.label}.md`);
    await copyFile(sourcePath, targetPath);
    const directEvidence = {};
    for (const field of fields) {
      directEvidence[field] = (parsedCandidate.fields[field]?.evidence ?? [])
        .filter((evidence) => evidence.classification === "DIRECT_VALUE")
        .map((evidence, evidenceIndex) => ({
          evidence_id: `${field}_${String(evidenceIndex + 1).padStart(2, "0")}`,
          line_start: evidence.line_start,
          line_end: evidence.line_end,
          carrier: evidence.carrier,
          note: evidence.note,
          quote: evidence.quote,
        }));
    }
    candidates.push({
      label: parsedCandidate.label,
      sha256: sourceCandidate.source_sha256,
      path: `${parsedCandidate.label}.md`,
      direct_evidence: directEvidence,
    });
  }

  await writeFile(join(packetDir, "packet.json"), `${JSON.stringify({
    composition_id: row.composition_id,
    candidates: candidates.map(({ label, sha256, path }) => ({ label, sha256, path })),
  }, null, 2)}\n`);
  await writeFile(join(packetDir, "field_evidence.json"), `${JSON.stringify({
    composition_id: row.composition_id,
    candidates: candidates.map(({ label, direct_evidence }) => ({ label, direct_evidence })),
  }, null, 2)}\n`);
  packetRows.push({ batch_id: batchId, composition_id: row.composition_id, candidates: candidates.map(({ label, sha256, path }) => ({ label, sha256, path })) });
}

const instructions = `# RQ1 82-Registry Source-Only Field-Removal Mapping\n\nYou receive only an anonymous composition packet: original candidate documents, their SHA-256 hashes, and a seven-field direct-evidence map. Do not infer or seek prompts, labels, source provenance, prior cards, selector outputs, results, or external information. Do not access files outside your assigned batch.\n\n## Task\n\nFor every candidate and field, determine whether all explicit values of that field can be removed from the original document without broadening the documented skill capability. This is a routing-only intervention, so the edited text may be incomplete or non-executable. Do not make it more usable by adding general language.\n\n## Dispositions\n\n- \`SAFE_MAP\`: every supplied direct-value span, and every additional direct occurrence you find on full-document inspection, can be removed with exact line edits.\n- \`NO_DIRECT_VALUE\`: there is no supplied direct value and no additional direct occurrence. No edits.\n- \`UNSAFE_MIXED_CARRIER\`: at least one direct value is inseparable from non-target content in the same textual carrier. No edits.\n- \`UNCERTAIN\`: source text does not support a safe decision. No edits.\n\n## Edit Rules\n\n1. Inspect the whole document for repeated explicit values, not only supplied evidence. Record any extra direct occurrence under \`additional_direct_evidence\`, then cover it.\n2. \`DELETE_LINE\` is allowed only for a line block wholly devoted to the target field. \`REWRITE_LINE\` must provide an exact replacement, preserve non-target content, and use only \`[information removed]\` where grammar demands it.\n3. Never generalise a value: removing \`PDF\`, a package, version, threshold, path, credential, task type, or authority limit cannot become a broader category.\n4. Do not remove merely correlated task/method prose. Do not change title, source, candidate identity, or non-target field content unless the literal text itself is a target direct value.\n5. Be conservative: if a safe exact map is doubtful, return \`UNSAFE_MIXED_CARRIER\` or \`UNCERTAIN\`.\n\nWrite exactly one JSON object following \`REDACTION_SCHEMA.json\` to the assigned output path.\n`;
const schema = {
  status: "ELIGIBILITY_MAP_COMPLETE",
  batch_id: "batch_XX",
  quality_amendment: "UNSAFE_MIXED_CARRIER must include blocking_evidence; see ELIGIBILITY_QUALITY_AMENDMENT.md.",
  compositions: [{
    composition_id: "OR82-XXX",
    candidates: [{
      label: "candidate_a",
      field_maps: Object.fromEntries(fields.map((field) => [field, {
        status: "SAFE_MAP | NO_DIRECT_VALUE | UNSAFE_MIXED_CARRIER | UNCERTAIN",
        covered_evidence_ids: ["field_01"],
        additional_direct_evidence: [{ evidence_id: "field_extra_01", line_start: 1, line_end: 1, rationale: "Direct repeated value." }],
        edits: [{ kind: "DELETE_LINE | REWRITE_LINE", line_start: 1, line_end: 1, evidence_ids: ["field_01"], replacement: "[information removed]" }],
        rationale: "Brief source-only rationale.",
      }]))
    }]
  }]
};
await writeFile(join(outputRoot, "REDACTION_INSTRUCTIONS.md"), instructions);
await writeFile(join(outputRoot, "REDACTION_SCHEMA.json"), `${JSON.stringify(schema, null, 2)}\n`);
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({
  status: "RQ1_ORIGINAL_REMOVAL_V3_82_SOURCE_ONLY_ELIGIBILITY_READY",
  batch_size: batchSize,
  fields,
  compositions: packetRows,
}, null, 2)}\n`);
console.log(JSON.stringify({ status: "PASS", compositions: packetRows.length, batches: Math.ceil(packetRows.length / batchSize), output: relative(repo, outputRoot) }, null, 2));
