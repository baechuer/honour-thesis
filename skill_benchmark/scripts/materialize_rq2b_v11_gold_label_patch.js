#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const base = path.join(root, "rq2b_full_library", "rq2b-full-library-v1-2026-08-02");
const target = path.join(root, "rq2b_full_library", "rq2b-full-library-v1.1-2026-08-15");
const remediation = path.join(target, "gold_label_remediation_v1_2026-08-15");

function readJsonl(filePath) {
  return fs
    .readFileSync(filePath, "utf8")
    .trim()
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function fail(message) {
  throw new Error(message);
}

const decisionsPath = path.join(remediation, "gold_label_decisions.jsonl");
const basePromptsPath = path.join(base, "prompt_manifest.jsonl");
const strictStatusPath = path.join(
  base,
  "b0g_semantic_review_v2_2026-08-09",
  "final_freeze_v2_2026-08-09",
  "strict_gold_status.jsonl",
);

const decisions = readJsonl(decisionsPath);
const strictFailures = readJsonl(strictStatusPath).filter(
  (row) => !row.strict_gold_accepted_after_duplicate_closure,
);
const prompts = readJsonl(basePromptsPath);
const decisionByPrompt = new Map(decisions.map((row) => [row.prompt_id, row]));

if (decisions.length !== 14 || decisionByPrompt.size !== 14) {
  fail("Expected exactly 14 unique remediation decisions.");
}
if (strictFailures.length !== 14) {
  fail("Expected exactly 14 base-v1 strict-gold failures.");
}

for (const failure of strictFailures) {
  const decision = decisionByPrompt.get(failure.prompt_id);
  if (!decision) fail(`Missing decision for ${failure.prompt_id}.`);
  if (decision.gold_skill !== failure.strict_gold_skill_id) {
    fail(`Gold mismatch for ${failure.prompt_id}.`);
  }
}
for (const decision of decisions) {
  if (!strictFailures.some((row) => row.prompt_id === decision.prompt_id)) {
    fail(`Unexpected decision prompt ${decision.prompt_id}.`);
  }
}

const exclusions = new Set(
  decisions
    .filter((row) => row.decision === "exclude_from_future_scored_corpus")
    .map((row) => row.prompt_id),
);
const retained = decisions.filter((row) => row.decision === "retain_gold_label_skill");
if (exclusions.size !== 8 || retained.length !== 6) {
  fail("Expected six retained labels and eight exclusions.");
}

const materializedPrompts = prompts.filter((row) => !exclusions.has(row.prompt_id));
const scoredPrompts = materializedPrompts.filter((row) => row.stratum !== "stress");
const countByStratum = (rows) =>
  rows.reduce((counts, row) => {
    counts[row.stratum] = (counts[row.stratum] || 0) + 1;
    return counts;
  }, {});
const counts = countByStratum(materializedPrompts);
const scoredCounts = countByStratum(scoredPrompts);

if (
  materializedPrompts.length !== 393 ||
  scoredPrompts.length !== 381 ||
  counts.controlled !== 243 ||
  counts.public_gold !== 138 ||
  counts.stress !== 12 ||
  scoredCounts.controlled !== 243 ||
  scoredCounts.public_gold !== 138
) {
  fail("Materialized prompt counts do not match the approved remediation scope.");
}

fs.mkdirSync(target, { recursive: true });
const promptManifestPath = path.join(target, "prompt_manifest.jsonl");
const scoredPromptIdsPath = path.join(target, "scored_prompt_ids.json");
const reportPath = path.join(target, "materialization_report.json");

fs.writeFileSync(
  promptManifestPath,
  `${materializedPrompts.map((row) => JSON.stringify(row)).join("\n")}\n`,
);
fs.writeFileSync(
  scoredPromptIdsPath,
  `${JSON.stringify(scoredPrompts.map((row) => row.prompt_id), null, 2)}\n`,
);
fs.writeFileSync(
  reportPath,
  `${JSON.stringify(
    {
      version: "rq2b-full-library-v1.1-2026-08-15",
      parent_version: "rq2b-full-library-v1-2026-08-02",
      evaluation_scope: "strict_gold_only",
      accepted_metrics: ["strict_Hit@1", "strict_MRR@10", "strict_Recall@K"],
      unavailable_metrics: ["acceptable_Hit@K", "acceptable_Recall@K"],
      base_prompt_manifest_sha256: sha256(basePromptsPath),
      remediation_decisions_sha256: sha256(decisionsPath),
      base_strict_failures: strictFailures.length,
      retained_gold_labels: retained.length,
      excluded_prompts: [...exclusions].sort(),
      resulting_prompt_counts: counts,
      resulting_scored_prompt_counts: scoredCounts,
      output_files: {
        prompt_manifest: path.basename(promptManifestPath),
        scored_prompt_ids: path.basename(scoredPromptIdsPath),
      },
    },
    null,
    2,
  )}\n`,
);

console.log(
  JSON.stringify(
    {
      status: "pass",
      prompt_count: materializedPrompts.length,
      scored_prompt_count: scoredPrompts.length,
      counts,
      retained_gold_labels: retained.length,
      excluded_prompts: exclusions.size,
    },
    null,
    2,
  ),
);
