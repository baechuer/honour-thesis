#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const root = 'skill_benchmark/rq1b_naturalistic_public_replication';
const clustersDir = path.join(root, 'clusters');
const outputPath = path.join(root, 'manifest', 'draft_pool_audit.json');
const inventoryPath = path.join(root, 'manifest', 'source_inventory.jsonl');

const sourceInventory = new Map(
  fs
    .readFileSync(inventoryPath, 'utf8')
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line))
    .map((entry) => [entry.skill_id, entry.source_path]),
);

const cards = fs
  .readdirSync(clustersDir, { recursive: true })
  .filter((entry) => entry.endsWith('cluster_card.md'))
  .sort()
  .map((relativePath) => {
    const cardPath = path.join(clustersDir, relativePath);
    const text = fs.readFileSync(cardPath, 'utf8');
    const idMatch = text.match(/^# RQ1(?:B|b) Draft ([0-9]+):/m);
    const id = idMatch ? `RQ1B Draft ${idMatch[1]}` : null;
    const status = text.match(/^Status: `([^`]+)`/m)?.[1] ?? null;
    const primaryField = text.match(/Tentative primary distinguishing field: `([^`]+)`/m)?.[1] ?? null;
    const candidates = [...text.matchAll(/^\s+- `(public-[^`]+)`$/gm)].map((match) => match[1]);
    const gates = [...text.matchAll(/^\| ([^|]+) \| `([^`]+)` \|/gm)].map((match) => ({
      gate: match[1].trim(),
      status: match[2],
    }));

    return {
      id,
      status,
      primary_field: primaryField,
      candidates,
      gate_statuses: gates,
      card_path: cardPath,
    };
  });

const fieldCounts = Object.fromEntries(
  [...new Set(cards.map((card) => card.primary_field).filter(Boolean))]
    .sort()
    .map((field) => [field, cards.filter((card) => card.primary_field === field).length]),
);

const sourceUsage = new Map();
for (const card of cards) {
  for (const candidate of card.candidates) {
    sourceUsage.set(candidate, [...(sourceUsage.get(candidate) ?? []), card.id]);
  }
}

const reusedCandidates = [...sourceUsage.entries()]
  .filter(([, cardIds]) => cardIds.length > 1)
  .map(([candidate, cardIds]) => ({ candidate, cards: cardIds }));

const missingSources = [...sourceUsage.keys()]
  .filter((candidate) => {
    const sourcePath = sourceInventory.get(candidate);
    return !sourcePath || !fs.existsSync(sourcePath);
  })
  .sort();

const audit = {
  audit_type: 'RQ1B_DRAFT_POOL_LOCAL_ONLY',
  generated_at_utc: new Date().toISOString(),
  boundaries: {
    original_sources_only: true,
    prompts_created: false,
    labels_created: false,
    reviewer_packets_created: false,
    model_or_retrieval_runs: false,
    external_calls: false,
  },
  draft_cluster_count: cards.length,
  candidate_skill_count: sourceUsage.size,
  primary_field_counts: fieldCounts,
  source_disjointness: {
    required_at_freeze: true,
    reused_candidate_count: reusedCandidates.length,
    reused_candidates: reusedCandidates,
  },
  source_integrity: {
    missing_source_count: missingSources.length,
    missing_sources: missingSources,
  },
  cards,
};

fs.writeFileSync(outputPath, `${JSON.stringify(audit, null, 2)}\n`);
console.log(JSON.stringify({
  draft_cluster_count: audit.draft_cluster_count,
  candidate_skill_count: audit.candidate_skill_count,
  primary_field_counts: audit.primary_field_counts,
  reused_candidate_count: audit.source_disjointness.reused_candidate_count,
  missing_source_count: audit.source_integrity.missing_source_count,
}, null, 2));
