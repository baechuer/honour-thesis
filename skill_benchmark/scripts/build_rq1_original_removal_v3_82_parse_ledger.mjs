#!/usr/bin/env node

// Reuse only exact-hash, source-only parse records from the historical 76
// compositions. The six V3 additions remain explicitly pending new parsing.

import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join, relative } from "node:path";

const repo = process.cwd();
const oldRoot = join(repo, "skill_benchmark/rq1_public_original_removal_v2");
const root = join(repo, "skill_benchmark/rq1_public_original_removal_v3_82_registry");
const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "workflow_procedure",
  "success_verification",
  "boundary_not_for",
  "dependency_resource",
].sort();

const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));

const oldLineage = await readJson(join(oldRoot, "source_packets/private_lineage_manifest.json"));
const newLineage = await readJson(join(root, "source_packets/private_lineage_manifest.json"));
const oldByCompositionId = new Map(oldLineage.compositions.map((row) => [row.composition_id, row]));
const historicalParse = new Map();
const canonicalRoot = join(oldRoot, "parse_submissions/canonical");
for (const filename of (await readdir(canonicalRoot)).filter((name) => /^batch_\d+\.json$/.test(name)).sort()) {
  const submission = await readJson(join(canonicalRoot, filename));
  if (submission.status !== "PARSE_COMPLETE" || !Array.isArray(submission.compositions)) {
    throw new Error(`Invalid historical parse submission: ${filename}`);
  }
  for (const composition of submission.compositions) {
    if (historicalParse.has(composition.composition_id)) throw new Error(`Duplicate historical parse composition ${composition.composition_id}.`);
    historicalParse.set(composition.composition_id, composition);
  }
}
if (historicalParse.size !== 76) throw new Error(`Expected 76 historical parses, found ${historicalParse.size}.`);

const ledgerRows = [];
const pendingPackets = [];
for (const composition of newLineage.compositions) {
  const packetCandidates = composition.candidates;
  for (const candidate of packetCandidates) {
    const bytes = await readFile(join(repo, candidate.packet_path));
    if (sha256(bytes) !== candidate.source_sha256) throw new Error(`New packet hash mismatch: ${candidate.packet_path}`);
  }

  if (composition.lineage === "HISTORICAL_76_REUSED_SOURCE_ONLY_PARSE") {
    const oldSource = oldByCompositionId.get(composition.source_composition_id);
    const oldParsed = historicalParse.get(composition.source_composition_id);
    if (!oldSource || !oldParsed) throw new Error(`Historical source/parse unavailable for ${composition.composition_id}.`);
    const oldByLabel = new Map(oldSource.candidates.map((candidate) => [candidate.label, candidate]));
    const parsedByLabel = new Map(oldParsed.candidates.map((candidate) => [candidate.label, candidate]));
    const candidates = packetCandidates.map((candidate) => {
      const oldCandidate = oldByLabel.get(candidate.label);
      const parsedCandidate = parsedByLabel.get(candidate.label);
      if (!oldCandidate || !parsedCandidate || oldCandidate.source_sha256 !== candidate.source_sha256) {
        throw new Error(`Historical candidate identity mismatch for ${composition.composition_id}/${candidate.label}.`);
      }
      if (JSON.stringify(Object.keys(parsedCandidate.fields).sort()) !== JSON.stringify(fields)) {
        throw new Error(`Historical parse field schema mismatch for ${composition.composition_id}/${candidate.label}.`);
      }
      return { label: candidate.label, fields: parsedCandidate.fields };
    });
    ledgerRows.push({
      composition_id: composition.composition_id,
      registry_id: composition.registry_id,
      source_composition_id: composition.source_composition_id,
      lineage: composition.lineage,
      parse_status: "REUSED_VERIFIED_SOURCE_ONLY_PARSE",
      previous_canonical_submission: relative(repo, join(canonicalRoot, `${oldSource.batch_id}.json`)),
      candidates,
    });
  } else if (composition.lineage === "DIRECT_V3_NEW_SOURCE_ONLY_PARSE") {
    ledgerRows.push({
      composition_id: composition.composition_id,
      registry_id: composition.registry_id,
      source_composition_id: composition.source_composition_id,
      lineage: composition.lineage,
      parse_status: "PENDING_NEW_SOURCE_ONLY_PARSE",
    });
    pendingPackets.push({
      batch_id: composition.batch_id,
      composition_id: composition.composition_id,
      candidates: packetCandidates.map((candidate) => ({
        label: candidate.label,
        sha256: candidate.source_sha256,
        path: candidate.packet_path,
      })),
    });
  } else {
    throw new Error(`Unexpected parse lineage ${composition.lineage}.`);
  }
}

const reused = ledgerRows.filter((row) => row.parse_status === "REUSED_VERIFIED_SOURCE_ONLY_PARSE").length;
const pending = ledgerRows.filter((row) => row.parse_status === "PENDING_NEW_SOURCE_ONLY_PARSE").length;
if (ledgerRows.length !== 82 || reused !== 76 || pending !== 6 || pendingPackets.length !== 6) {
  throw new Error(`Unexpected unified parse ledger coverage: ${JSON.stringify({ rows: ledgerRows.length, reused, pending, packets: pendingPackets.length })}`);
}

await mkdir(join(root, "parse_ledger"), { recursive: true });
await writeFile(
  join(root, "parse_ledger", "parse_ledger.json"),
  `${JSON.stringify({
    status: "RQ1_ORIGINAL_REMOVAL_V3_82_PARSE_LEDGER_PARTIAL",
    schema_fields: fields,
    counts: { compositions: 82, reused_verified: reused, pending_new_parse: pending },
    rows: ledgerRows,
  }, null, 2)}\n`,
);
await writeFile(
  join(root, "parse_ledger", "pending_v3_source_only_parse_packets.json"),
  `${JSON.stringify({
    status: "SIX_DIRECT_V3_COMPOSITIONS_PENDING_SOURCE_ONLY_PARSE",
    fields,
    packets: pendingPackets,
  }, null, 2)}\n`,
);
console.log(JSON.stringify({ status: "PASS", compositions: ledgerRows.length, reused_verified: reused, pending_new_parse: pending }, null, 2));
