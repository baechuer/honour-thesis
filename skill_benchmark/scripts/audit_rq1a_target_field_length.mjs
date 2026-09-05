#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const repoRoot = path.resolve(import.meta.dirname, "../..");
const suiteRoot = path.join(repoRoot, "skill_benchmark/rq1a_field_discriminability");
const outputDir = path.join(
  repoRoot,
  "skill_benchmark/outputs/rq1a_target_field_length_audit_2026-09-04",
);

const fields = [
  "use_condition",
  "input_precondition",
  "output_artifact",
  "dependency_resource",
  "boundary_not_for",
  "success_verification",
  "workflow_procedure",
];

function visibleWordCount(value) {
  const text = Array.isArray(value) ? value.join(" ") : String(value ?? "");
  return text.match(/\S+/g)?.length ?? 0;
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

const fieldRows = [];
const clusterRows = [];

for (const field of fields) {
  const clustersDir = path.join(suiteRoot, field, "clusters");
  const unitPaths = fs
    .readdirSync(clustersDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => path.join(clustersDir, entry.name, "unit.json"))
    .filter((unitPath) => fs.existsSync(unitPath))
    .sort();

  const goldCounts = [];
  const alternativeCounts = [];
  let uniqueLongestGold = 0;
  let tieAwareLongestCredit = 0;

  for (const unitPath of unitPaths) {
    const unit = JSON.parse(fs.readFileSync(unitPath, "utf8"));
    const candidates = unit.skills.map((skill) => ({
      skill_id: skill.skill_id,
      role: skill.role,
      word_count: visibleWordCount(skill[field]),
    }));
    const gold = candidates.find((candidate) => candidate.skill_id === unit.gold_skill_id);
    if (!gold) {
      throw new Error(`Missing gold candidate in ${unitPath}`);
    }

    const alternatives = candidates.filter((candidate) => candidate.skill_id !== unit.gold_skill_id);
    const longest = Math.max(...candidates.map((candidate) => candidate.word_count));
    const longestCandidates = candidates.filter((candidate) => candidate.word_count === longest);
    const goldIsLongest = gold.word_count === longest;

    goldCounts.push(gold.word_count);
    alternativeCounts.push(...alternatives.map((candidate) => candidate.word_count));
    uniqueLongestGold += Number(goldIsLongest && longestCandidates.length === 1);
    tieAwareLongestCredit += goldIsLongest ? 1 / longestCandidates.length : 0;

    clusterRows.push({
      field,
      cluster_id: unit.cluster_id,
      gold_skill_id: unit.gold_skill_id,
      gold_word_count: gold.word_count,
      alternative_word_counts: alternatives.map((candidate) => candidate.word_count),
      longest_skill_ids: longestCandidates.map((candidate) => candidate.skill_id),
      gold_is_unique_longest: goldIsLongest && longestCandidates.length === 1,
      tie_aware_longest_credit: goldIsLongest ? 1 / longestCandidates.length : 0,
    });
  }

  fieldRows.push({
    field,
    clusters: unitPaths.length,
    gold_mean_words: mean(goldCounts),
    alternative_mean_words: mean(alternativeCounts),
    unique_longest_gold: uniqueLongestGold,
    tie_aware_longest_top1: tieAwareLongestCredit / unitPaths.length,
  });
}

fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(
  path.join(outputDir, "length_audit.json"),
  `${JSON.stringify({ field_rows: fieldRows, cluster_rows: clusterRows }, null, 2)}\n`,
);

const tableRows = fieldRows.map((row) =>
  `| ${row.field} | ${row.clusters} | ${row.gold_mean_words.toFixed(1)} | ${row.alternative_mean_words.toFixed(1)} | ${row.unique_longest_gold}/${row.clusters} | ${row.tie_aware_longest_top1.toFixed(3)} |`,
);
const report = `# RQ1 Controlled Target-Field Length Diagnostic

Date: 2026-09-04

This is a descriptive length/detail check, not a retrieval result. For each controlled cluster it counts whitespace-delimited words in the candidate-specific target field. The final column selects the candidate with the longest target-field value and divides credit across exact length ties. It does not show that BM25 or Qwen used length directly; it only tests whether gold identity is associated with field length or detail.

| Field | Clusters | Gold mean words | Alternative mean words | Gold uniquely longest | Tie-aware longest Top-1 |
| --- | ---: | ---: | ---: | ---: | ---: |
${tableRows.join("\n")}

## Interpretation boundary

- High values show that length or detail is associated with the gold field in that controlled suite. The association is strongest for boundary/not-for and dependency/resource.
- This does not show that BM25 or Qwen used length, and it does not invalidate the paired hidden-versus-exposed comparison.
- The controlled result should be stated as the practical value of exposing the field content as written, including its amount and specificity, rather than as a length-normalised effect of field meaning alone.
- A length/detail-matched sensitivity set could strengthen future work, but it is not required for that bounded claim.
`;
fs.writeFileSync(path.join(outputDir, "README.md"), report);

process.stdout.write(`${report}\n`);
