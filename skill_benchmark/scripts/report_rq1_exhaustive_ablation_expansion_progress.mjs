#!/usr/bin/env node

import { readdir, readFile } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_exhaustive_ablation_v1");
const manifest = JSON.parse(await readFile(join(root, "expansion_packets", "agent_packet_manifest.json"), "utf8"));
const canonicalRoot = join(root, "expansion_maps", "canonical_compositions");
let canonicalFiles = [];
try {
  canonicalFiles = (await readdir(canonicalRoot)).filter((name) => name.endsWith(".json"));
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const completed = new Set(canonicalFiles.map((name) => name.replace(/\.json$/u, "")));
const missing = manifest.items.map((item) => item.composition_unit_id).filter((id) => !completed.has(id));
console.log(JSON.stringify({
  status: missing.length ? "IN_PROGRESS" : "EXPANSION_MAPPING_COMPLETE",
  expected_expansion_compositions: manifest.items.length,
  completed_expansion_compositions: completed.size,
  completed_composition_field_units: completed.size * manifest.field_order.length,
  pilot_reuse_composition_field_units: 14,
  total_completed_composition_field_units: completed.size * manifest.field_order.length + 14,
  target_composition_field_units: 574,
  next_missing: missing.slice(0, 12),
  missing_count: missing.length,
}));
