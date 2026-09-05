#!/usr/bin/env node

import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const sourceRoot = join(root, "source_packets");
const parseRoot = join(root, "parse_submissions", "canonical");
const outputRoot = join(root, "redaction_packets");
const fieldNames = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
];

const canonicalFiles = (await (await import("node:fs/promises")).readdir(parseRoot))
  .filter((name) => /^batch_\d{2}\.json$/.test(name))
  .sort();
if (canonicalFiles.length !== 26) {
  throw new Error(`Expected 26 canonical parse batches, found ${canonicalFiles.length}.`);
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });

const instructions = [
  "# RQ1 Original-Document Redaction Review Instructions",
  "",
  "You receive only anonymous original candidate documents and a source-only seven-field evidence map. You must not infer or seek prompts, labels, source provenance, historical curation, selector results, or any external information.",
  "",
  "## Aim",
  "",
  "For each candidate and field, assess whether the explicit documented value identified by the source parser can be removed from the original document without replacing it with a broader capability or deleting unrelated operational information.",
  "",
  "This is a routing-only intervention. The edited document may become incomplete or non-executable. That is allowed. Do not preserve execution merely to make a mask look nicer.",
  "",
  "## Required decision per candidate-field",
  "",
  "- SAFE_MAP: every DIRECT_VALUE evidence span can be removed through one or more exact line edits while retaining any non-target text in the line. List every edit.",
  "- NO_DIRECT_VALUE: the parser recorded no DIRECT_VALUE span. Provide no edit.",
  "- UNSAFE_MIXED_CARRIER: at least one direct value is inseparable from other field content in the same source carrier. Provide no speculative edit.",
  "- UNCERTAIN: source text is insufficient to distinguish a safe removal decision. Provide no edit.",
  "",
  "## Edit rules",
  "",
  "1. Edit only source lines tied to a supplied DIRECT_VALUE evidence id.",
  "2. Use DELETE_LINE only when the full cited line is target-field content. Use REWRITE_LINE only to retain non-target text while removing the target value. Each edit must list the DIRECT_VALUE evidence_ids it covers and its line range must be inside those evidence ranges.",
  "3. A rewrite must never generalise capability. For example, deleting PDF may yield a neutral phrase such as [input material] where grammar requires it; it must never become file, any file, or a wider capability.",
  "4. Do not edit GENERIC_CONTEXT or CORRELATED_CONTEXT; any remaining correlated wording is intentional and will be reported as natural residual information, not treated as a failed semantic erasure.",
  "5. Do not create title, source, or candidate-specific markers. A neutral marker, where necessary, must be exactly [information removed].",
  "6. When in doubt, reject the candidate-field as UNSAFE_MIXED_CARRIER or UNCERTAIN. Do not force a mask.",
  "",
  "## Output",
  "",
  "Write a JSON file following the provided schema. It must identify the decision for all seven fields of every candidate. A SAFE_MAP must cover every listed direct-evidence id exactly once. Do not make a routing judgment.",
  "",
].join("\n");
await writeFile(join(outputRoot, "REDACTION_INSTRUCTIONS.md"), instructions);

const batchManifest = [];
for (const fileName of canonicalFiles) {
  const parsed = JSON.parse(await readFile(join(parseRoot, fileName), "utf8"));
  const batchId = parsed.batch_id;
  const batchDir = join(outputRoot, batchId);
  await mkdir(batchDir, { recursive: true });
  const reviewCompositions = [];
  for (const composition of parsed.compositions) {
    const compositionDir = join(batchDir, composition.composition_id);
    await mkdir(compositionDir, { recursive: true });
    const reviewCandidates = [];
    for (const candidate of composition.candidates) {
      await cp(
        join(sourceRoot, batchId, composition.composition_id, `${candidate.label}.md`),
        join(compositionDir, `${candidate.label}.md`),
      );
      const evidence = {};
      for (const fieldName of fieldNames) {
        let index = 0;
        evidence[fieldName] = candidate.fields[fieldName].evidence
          .filter((span) => span.classification === "DIRECT_VALUE")
          .map((span) => ({
            evidence_id: `${fieldName}_${String(++index).padStart(2, "0")}`,
            line_start: span.line_start,
            line_end: span.line_end,
            carrier: span.carrier,
            note: span.note,
            quote: span.quote,
          }));
      }
      reviewCandidates.push({ label: candidate.label, direct_evidence: evidence });
    }
    const review = { composition_id: composition.composition_id, candidates: reviewCandidates };
    await writeFile(join(compositionDir, "field_evidence.json"), `${JSON.stringify(review, null, 2)}\n`);
    reviewCompositions.push({ composition_id: composition.composition_id, candidates: reviewCandidates.map((candidate) => candidate.label) });
  }
  batchManifest.push({ batch_id: batchId, compositions: reviewCompositions });
}
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({ status: "SOURCE_ONLY_REDACTION_REVIEW_READY", field_names: fieldNames, batches: batchManifest }, null, 2)}\n`);
console.log(JSON.stringify({ status: "READY", batches: batchManifest.length, compositions: batchManifest.reduce((count, batch) => count + batch.compositions.length, 0), output: outputRoot }));
