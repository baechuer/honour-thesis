#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const materialization = JSON.parse(await readFile(join(root, "materialized_masks", "MASK_MATERIALIZATION_MANIFEST.json"), "utf8"));
const residualLedger = JSON.parse(await readFile(join(root, "blind_residual_ledger", "blind_residual_ledger.json"), "utf8"));
const privateLineage = JSON.parse(await readFile(join(root, "blind_residual_packets", "private_lineage_manifest.json"), "utf8"));

const statusByItem = new Map(residualLedger.rows.map((row) => [row.item_id, row.status]));
const statusByCompositionField = new Map();
for (const item of privateLineage.items) {
  const status = statusByItem.get(item.item_id);
  if (!status) throw new Error(`Missing blind residual status for ${item.item_id}`);
  const key = `${item.composition_id}::${item.target_field}`;
  if (statusByCompositionField.has(key)) throw new Error(`Duplicate residual item for ${key}`);
  statusByCompositionField.set(key, status);
}

const fieldStatus = (compositionId, field) => statusByCompositionField.get(`${compositionId}::${field}`) ?? null;
const deriveStatus = (sourceStatus, compositionId, fields) => {
  if (sourceStatus !== "MATERIALIZED_PENDING_TECHNICAL_AUDIT") return { status: "NOT_ELIGIBLE", reason: sourceStatus };
  const statuses = fields.map((field) => ({ field, status: fieldStatus(compositionId, field) }));
  if (statuses.some(({ status }) => status === null)) return { status: "NOT_ELIGIBLE", reason: "MISSING_S3_SINGLE_FIELD_REVIEW", fields: statuses };
  if (statuses.some(({ status }) => status === "UNCERTAIN")) return { status: "NOT_ELIGIBLE", reason: "S3_UNCERTAIN", fields: statuses };
  if (statuses.some(({ status }) => status === "RESIDUAL_FOUND")) return { status: "NOT_ELIGIBLE", reason: "S3_RESIDUAL_FOUND", fields: statuses };
  return { status: "ELIGIBLE_FOR_STRICT_FAMILY_LINKAGE", reason: "ALL_COMPONENT_FIELDS_CLEAR", fields: statuses };
};

const rows = materialization.compositions.map((composition) => ({
  composition_id: composition.composition_id,
  conditions: Object.fromEntries(Object.entries(composition.conditions).map(([condition, source]) => [
    condition,
    {
      fields: source.fields,
      ...deriveStatus(source.status, composition.composition_id, source.fields),
    },
  ])),
}));

const summary = {};
for (const row of rows) {
  for (const [condition, result] of Object.entries(row.conditions)) {
    summary[condition] ??= {};
    summary[condition][result.status] = (summary[condition][result.status] ?? 0) + 1;
  }
}

const output = {
  status: "RQ1_S3_GROUP_ELIGIBILITY_DERIVED_NO_SELECTOR_EXECUTION",
  inputs: {
    materialization_status: materialization.status,
    residual_status: residualLedger.status,
  },
  boundary: "Derived leakage eligibility only. No prompt, gold-label, retrieval, or field-effect result is included.",
  summary,
  rows,
};
const outputRoot = join(root, "blind_residual_ledger");
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "group_eligibility_ledger.json"), `${JSON.stringify(output, null, 2)}\n`);
const lines = [
  "# RQ1 82-Registry S3 Derived Group Eligibility",
  "",
  `Status: \`${output.status}\``,
  "",
  "| Condition | Eligible for strict-family linkage | Not eligible |",
  "| --- | ---: | ---: |",
  ...Object.entries(summary).sort(([left], [right]) => left.localeCompare(right)).map(([condition, counts]) => `| ${condition} | ${counts.ELIGIBLE_FOR_STRICT_FAMILY_LINKAGE ?? 0} | ${(counts.NOT_ELIGIBLE ?? 0)} |`),
  "",
  "A joint group is eligible only when every component single-field mask is CLEAR in S3. This is a leakage gate, not a routing result.",
];
await writeFile(join(outputRoot, "GROUP_ELIGIBILITY_SUMMARY.md"), `${lines.join("\n")}\n`);
console.log(JSON.stringify({ status: output.status, summary }));
