#!/usr/bin/env node

// Build prompt/gold/source-blind S3 packets from technically audited S2 masks.

import { createHash } from "node:crypto";
import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const masksRoot = join(root, "materialized_masks");
const auditPath = join(root, "technical_audit", "technical_mask_audit.json");
const outputRoot = join(root, "blind_residual_packets");
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const manifest = JSON.parse(await readFile(join(masksRoot, "MASK_MATERIALIZATION_MANIFEST.json"), "utf8"));
const audit = JSON.parse(await readFile(auditPath, "utf8"));
if (audit.status !== "TECHNICAL_AUDIT_PASS_PENDING_BLIND_RESIDUAL_REVIEW") {
  throw new Error(`S2 audit is not eligible: ${audit.status}`);
}

const auditByKey = new Map(audit.rows.map((row) => [`${row.composition_id}/${row.condition}/${row.candidate_label}`, row]));
const items = [];
for (const composition of manifest.compositions) {
  for (const [condition, state] of Object.entries(composition.conditions)) {
    if (state.status !== "MATERIALIZED_PENDING_TECHNICAL_AUDIT" || state.fields.length !== 1) continue;
    const field = state.fields[0];
    const sourceLedger = JSON.parse(await readFile(state.ledger_path, "utf8"));
    for (const candidate of sourceLedger.candidates) {
      const auditRow = auditByKey.get(`${composition.composition_id}/${condition}/${candidate.label}`);
      if (!auditRow || auditRow.status !== "PASS") throw new Error(`Missing technical pass for ${composition.composition_id}/${condition}/${candidate.label}.`);
    }
    items.push({
      composition_id: composition.composition_id,
      condition,
      field,
      source_ledger_path: state.ledger_path,
      candidates: sourceLedger.candidates,
    });
  }
}
items.sort((left, right) => left.field.localeCompare(right.field) || left.composition_id.localeCompare(right.composition_id));

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const publicItems = [];
const privateItems = [];
for (let index = 0; index < items.length; index += 1) {
  const item = items[index];
  const itemId = `S3-${String(index + 1).padStart(3, "0")}`;
  const batchId = `batch_${String(Math.floor(index / 3) + 1).padStart(2, "0")}`;
  const itemDir = join(outputRoot, batchId, itemId);
  await mkdir(itemDir, { recursive: true });
  const publicCandidates = [];
  const privateCandidates = [];
  for (const candidate of item.candidates) {
    const text = await readFile(candidate.masked_path, "utf8");
    const destination = join(itemDir, `${candidate.label}.md`);
    await cp(candidate.masked_path, destination);
    publicCandidates.push({ label: candidate.label, path: `${candidate.label}.md` });
    privateCandidates.push({
      label: candidate.label,
      masked_sha256: sha256(text),
      source_mask_path: candidate.masked_path,
      packet_path: destination,
    });
  }
  await writeFile(join(itemDir, "packet.json"), `${JSON.stringify({
    item_id: itemId,
    target_field: item.field,
    candidates: publicCandidates,
  }, null, 2)}\n`);
  publicItems.push({ batch_id: batchId, item_id: itemId, target_field: item.field, candidates: publicCandidates });
  privateItems.push({
    batch_id: batchId,
    item_id: itemId,
    composition_id: item.composition_id,
    condition: item.condition,
    target_field: item.field,
    source_ledger_path: item.source_ledger_path,
    candidates: privateCandidates,
  });
}

const schema = {
  status: "BLIND_RESIDUAL_REVIEW_COMPLETE",
  batch_id: "batch_XX",
  items: [{
    item_id: "S3-XXX",
    target_field: "one of the seven field names",
    candidates: [{
      label: "candidate_a",
      review: {
        status: "CLEAR | RESIDUAL_FOUND | UNCERTAIN",
        evidence: [{ line_start: 1, line_end: 1, quote: "Exact masked-document substring." }],
        rationale: "Brief masked-text-only rationale.",
      },
    }],
  }],
};
const instructions = `# RQ1 S3 Blind Residual Review\n\nYou receive anonymous masked candidate documents and a target field category. Do not infer or seek originals, prompts, gold labels, sources, candidate provenance, maps, selectors, prior results or external information. Read only the assigned packet.\n\nFor every candidate, decide whether the masked document still explicitly states a candidate-specific value for the target field.\n\n- CLEAR: no explicit candidate-specific target-field value remains. Evidence must be empty.\n- RESIDUAL_FOUND: an explicit remaining target-field value remains. Cite its masked-document line range and an exact quote.\n- UNCERTAIN: the masked text does not support a clear decision. Evidence must be empty.\n\nDo not count generic method prose, task names, or unrelated field content merely because it is correlated with the target field. Do not decide which skill a prompt should select. Write exactly one JSON object using RESIDUAL_REVIEW_SCHEMA.json to the assigned output path.\n`;
await writeFile(join(outputRoot, "README.md"), instructions);
await writeFile(join(outputRoot, "RESIDUAL_REVIEW_SCHEMA.json"), `${JSON.stringify(schema, null, 2)}\n`);
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({
  status: "RQ1_S3_BLIND_RESIDUAL_REVIEW_READY",
  batch_size: 3,
  items: publicItems,
}, null, 2)}\n`);
await writeFile(join(outputRoot, "private_lineage_manifest.json"), `${JSON.stringify({
  status: "PRIVATE_COORDINATOR_LINEAGE_DO_NOT_SHARE_WITH_REVIEWERS",
  inputs: {
    materialisation_manifest_sha256: sha256(await readFile(join(masksRoot, "MASK_MATERIALIZATION_MANIFEST.json"), "utf8")),
    technical_audit_sha256: sha256(await readFile(auditPath, "utf8")),
  },
  items: privateItems,
}, null, 2)}\n`);
console.log(JSON.stringify({ status: "RQ1_S3_BLIND_RESIDUAL_REVIEW_READY", items: publicItems.length, batches: new Set(publicItems.map((item) => item.batch_id)).size }));
