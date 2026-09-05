#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(
  await readFile(join(root, "pilot_target_masks", "TARGET_MASK_MANIFEST.json"), "utf8"),
);
const roundRoots = [
  { round: 3, path: join(root, "pilot_clearance", "round3_canonical") },
  { round: 2, path: join(root, "pilot_clearance", "round2_canonical") },
  { round: 1, path: join(root, "pilot_clearance", "canonical") },
];
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const units = [];

for (const expected of manifest.single_units) {
  let selected = null;
  for (const rootEntry of roundRoots) {
    try {
      const path = join(rootEntry.path, `${expected.unit_id}.json`);
      const text = await readFile(path, "utf8");
      const review = JSON.parse(text);
      if (review.candidates.every((candidate) => candidate.status === "CLEAR")) {
        selected = { round: rootEntry.round, path, sha256: sha256(text), review };
        break;
      }
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  if (!selected) throw new Error(`${expected.unit_id}: no all-CLEAR canonical review`);
  units.push({
    unit_id: expected.unit_id,
    composition_id: expected.composition_id,
    target_field: expected.target_field,
    clearance_round: selected.round,
    review_path: selected.path,
    review_sha256: selected.sha256,
    candidate_count: selected.review.candidates.length,
    all_clear: true,
  });
}

const output = {
  status: "RQ1_EXHAUSTIVE_PILOT_SINGLE_FIELD_CLEARANCE_FROZEN_NO_SELECTOR",
  boundary: "Target-clearance mechanics only; no damage control, prompt, label, selector, routing metric, or thesis result.",
  single_units: units.length,
  candidate_masks: units.reduce((sum, unit) => sum + unit.candidate_count, 0),
  round_distribution: Object.fromEntries(
    [1, 2, 3].map((round) => [String(round), units.filter((unit) => unit.clearance_round === round).length]),
  ),
  units,
};
const outputRoot = join(root, "pilot_clearance", "final");
await mkdir(outputRoot, { recursive: true });
await writeFile(join(outputRoot, "FINAL_CLEARANCE_LEDGER.json"), `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify({
  status: output.status,
  single_units: output.single_units,
  candidate_masks: output.candidate_masks,
  round_distribution: output.round_distribution,
}));
