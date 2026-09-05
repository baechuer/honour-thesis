#!/usr/bin/env node

import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v2");
const source = JSON.parse(await readFile(join(root, "materialized_masks_remediated", "REMEDIATED_MASK_MANIFEST.json"), "utf8"));
const outputRoot = join(root, "residual_recheck_packets");
const ready = source.items.filter((entry) => entry.status === "MATERIALIZED_REMEDIATED_PENDING_AUDIT").sort((left, right) => left.condition.localeCompare(right.condition) || left.composition_id.localeCompare(right.composition_id));
await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "README.md"), `# Fresh Residual Review\n\nYou receive anonymous masked documents only. Do not infer or seek prompts, gold labels, sources, selectors, previous maps, or results. For every candidate and listed field, use CLEAR only when no explicit candidate-specific value remains. Use RESIDUAL_FOUND only for explicit remaining values and cite masked-document line_start/line_end. Use UNCERTAIN only when necessary. Generic method wording and correlated non-target prose are not residual values.\n`);
const batches = [];
for (let start = 0, index = 1; start < ready.length; start += 3, index += 1) {
  const batchId = `batch_${String(index).padStart(2, "0")}`;
  const items = ready.slice(start, start + 3);
  const batchDir = join(outputRoot, batchId);
  await mkdir(batchDir, { recursive: true });
  const batchItems = [];
  for (const item of items) {
    const ledger = JSON.parse(await readFile(item.ledger_path, "utf8"));
    const itemDir = join(batchDir, item.item_id);
    await mkdir(itemDir, { recursive: true });
    for (const candidate of ledger.candidates) await cp(candidate.masked_path, join(itemDir, `${candidate.label}.md`));
    const manifest = { item_id: item.item_id, condition: item.condition, fields: item.fields, candidates: ledger.candidates.map((candidate) => candidate.label) };
    await writeFile(join(itemDir, "ITEM_MANIFEST.json"), `${JSON.stringify(manifest, null, 2)}\n`);
    batchItems.push(manifest);
  }
  batches.push({ batch_id: batchId, items: batchItems });
}
await writeFile(join(outputRoot, "agent_packet_manifest.json"), `${JSON.stringify({ status: "FRESH_SOURCE_BLIND_RESIDUAL_REVIEW_READY", batches }, null, 2)}\n`);
console.log(JSON.stringify({ status: "READY", items: ready.length, batches: batches.length }));
