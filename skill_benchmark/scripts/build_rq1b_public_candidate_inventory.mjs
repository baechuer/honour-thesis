#!/usr/bin/env node
/**
 * Local-only discovery aid for RQ1b. It inventories preserved public original
 * artifacts and proposes lexical near-neighbour pairs for manual curation.
 * Suggestions are not clusters, gold labels, prompts, or retrieval results.
 */
import { createHash } from "node:crypto";
import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const sourceRoots = [
  path.resolve("skill_benchmark/skills/public_imported_background"),
  path.resolve(
    "skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/emmraan-agent-skills-1124ce40/skills",
  ),
  path.resolve(
    "skill_benchmark/rq1b_naturalistic_public_replication/staged_sources/skillme-skills-a28c4ce9/skills",
  ),
];
const outputRoot = path.resolve(
  "skill_benchmark/rq1b_naturalistic_public_replication/manifest",
);
const inventoryPath = path.join(outputRoot, "source_inventory.jsonl");
const suggestionsPath = path.join(outputRoot, "lexical_neighbour_suggestions.jsonl");
const reviewQueuePath = path.join(outputRoot, "manual_source_review_queue.jsonl");
const summaryPath = path.join(outputRoot, "candidate_discovery_summary.json");

const STOPWORDS = new Set([
  "about", "after", "also", "and", "are", "but", "can", "for", "from",
  "into", "not", "only", "or", "that", "the", "this", "to", "use", "when",
  "with", "you", "your", "skill", "skills", "agent", "agents", "using",
]);

async function walkForOriginals(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      results.push(...await walkForOriginals(fullPath));
    } else if (entry.name === "SKILL.original.md") {
      results.push(fullPath);
    }
  }
  return results;
}

function cleanValue(value) {
  return value.trim().replace(/^['"]|['"]$/g, "").replace(/\s+/g, " ");
}

function parseArtifact(text) {
  const frontmatter = {};
  let body = text;
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (match) {
    body = text.slice(match[0].length);
    const lines = match[1].split(/\r?\n/);
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index];
      const field = line.match(/^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$/);
      if (!field) continue;
      const [, key, rawValue] = field;
      if (/^[>|][+-]?$/.test(rawValue.trim())) {
        const foldedLines = [];
        while (index + 1 < lines.length && (/^\s+/.test(lines[index + 1]) || lines[index + 1] === "")) {
          index += 1;
          if (lines[index].trim()) foldedLines.push(lines[index].trim());
        }
        frontmatter[key] = cleanValue(foldedLines.join(" "));
      } else {
        frontmatter[key] = cleanValue(rawValue);
      }
    }
  }
  const headings = [...body.matchAll(/^#{1,3}\s+(.+?)\s*#*\s*$/gm)]
    .map((heading) => heading[1].replace(/[`*_]/g, "").trim())
    .filter(Boolean)
    .slice(0, 60);
  return { frontmatter, body, headings };
}

function tokenize(value) {
  return (value.toLowerCase().match(/[\p{L}\p{N}][\p{L}\p{N}_+.#/-]*/gu) || [])
    .map((token) => token.replace(/^[-./]+|[-./]+$/g, ""))
    .filter((token) => token.length > 1 && !STOPWORDS.has(token));
}

function cosine(left, right) {
  let dot = 0;
  let leftMagnitude = 0;
  let rightMagnitude = 0;
  for (const value of left.values()) leftMagnitude += value * value;
  for (const value of right.values()) rightMagnitude += value * value;
  const [small, large] = left.size <= right.size ? [left, right] : [right, left];
  for (const [term, value] of small) dot += value * (large.get(term) || 0);
  return leftMagnitude && rightMagnitude ? dot / Math.sqrt(leftMagnitude * rightMagnitude) : 0;
}

function topSharedTerms(left, right, limit = 8) {
  return [...left.keys()]
    .filter((term) => right.has(term))
    .map((term) => ({ term, weight: left.get(term) * right.get(term) }))
    .sort((a, b) => b.weight - a.weight || a.term.localeCompare(b.term))
    .slice(0, limit)
    .map(({ term }) => term);
}

const originalPaths = (
  await Promise.all(sourceRoots.map(async (sourceRoot) => {
    try {
      return await walkForOriginals(sourceRoot);
    } catch (error) {
      if (error?.code === "ENOENT") return [];
      throw error;
    }
  }))
).flat().sort();
const inventory = [];

for (const sourcePath of originalPaths) {
  const text = await readFile(sourcePath, "utf8");
  const { frontmatter, body, headings } = parseArtifact(text);
  const skillId = path.basename(path.dirname(path.dirname(sourcePath)));
  const selectorText = [frontmatter.name || "", frontmatter.description || "", ...headings].join("\n");
  inventory.push({
    skill_id: skillId,
    source_path: path.relative(process.cwd(), sourcePath),
    source_sha256: createHash("sha256").update(text).digest("hex"),
    source_bytes: Buffer.byteLength(text, "utf8"),
    source_word_count: tokenize(body).length,
    frontmatter_name: frontmatter.name || null,
    frontmatter_description: frontmatter.description || null,
    headings,
    lexical_terms: tokenize(selectorText),
  });
}

const documentFrequency = new Map();
for (const row of inventory) {
  for (const term of new Set(row.lexical_terms)) {
    documentFrequency.set(term, (documentFrequency.get(term) || 0) + 1);
  }
}
const corpusSize = inventory.length;
for (const row of inventory) {
  const frequency = new Map();
  for (const term of row.lexical_terms) frequency.set(term, (frequency.get(term) || 0) + 1);
  row.vector = new Map(
    [...frequency].map(([term, count]) => [
      term,
      (1 + Math.log(count)) * Math.log((corpusSize + 1) / ((documentFrequency.get(term) || 0) + 1)),
    ]),
  );
}

const pairs = [];
for (let leftIndex = 0; leftIndex < inventory.length; leftIndex += 1) {
  const left = inventory[leftIndex];
  const ranked = [];
  for (let rightIndex = 0; rightIndex < inventory.length; rightIndex += 1) {
    if (leftIndex === rightIndex) continue;
    const right = inventory[rightIndex];
    const score = cosine(left.vector, right.vector);
    if (score > 0) ranked.push({ right, score });
  }
  ranked.sort((a, b) => b.score - a.score || a.right.skill_id.localeCompare(b.right.skill_id));
  for (const { right, score } of ranked.slice(0, 12)) {
    if (left.skill_id < right.skill_id) {
      pairs.push({
        left_skill_id: left.skill_id,
        right_skill_id: right.skill_id,
        lexical_cosine: Number(score.toFixed(6)),
        shared_terms: topSharedTerms(left.vector, right.vector),
        status: "SUGGESTION_ONLY_REQUIRES_MANUAL_SOURCE_REVIEW",
      });
    }
  }
}
pairs.sort((a, b) => b.lexical_cosine - a.lexical_cosine || a.left_skill_id.localeCompare(b.left_skill_id));

const bySkillId = new Map(inventory.map((row) => [row.skill_id, row]));
const normaliseForDuplicateCheck = (value) => (value || "")
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, " ")
  .trim();
const skillAppearances = new Map();
const reviewQueue = [];
for (const pair of pairs) {
  if (pair.lexical_cosine < 0.18) continue;
  const left = bySkillId.get(pair.left_skill_id);
  const right = bySkillId.get(pair.right_skill_id);
  const sameName = normaliseForDuplicateCheck(left.frontmatter_name)
    && normaliseForDuplicateCheck(left.frontmatter_name) === normaliseForDuplicateCheck(right.frontmatter_name);
  const sameDescription = normaliseForDuplicateCheck(left.frontmatter_description)
    && normaliseForDuplicateCheck(left.frontmatter_description) === normaliseForDuplicateCheck(right.frontmatter_description);
  if (sameName || sameDescription) continue;
  if ((skillAppearances.get(left.skill_id) || 0) >= 3) continue;
  if ((skillAppearances.get(right.skill_id) || 0) >= 3) continue;
  reviewQueue.push({
    queue_id: `RQ1B-CAND-${String(reviewQueue.length + 1).padStart(3, "0")}`,
    ...pair,
    left_source_path: left.source_path,
    left_source_sha256: left.source_sha256,
    left_name: left.frontmatter_name,
    left_description: left.frontmatter_description,
    right_source_path: right.source_path,
    right_source_sha256: right.source_sha256,
    right_name: right.frontmatter_name,
    right_description: right.frontmatter_description,
    curation_status: "UNSCREENED_NOT_A_CLUSTER",
    required_next_gate: "Manual original-source review for duplicate risk, semantic-neighbour relation, material operational distinction, and likely evidence spans.",
  });
  skillAppearances.set(left.skill_id, (skillAppearances.get(left.skill_id) || 0) + 1);
  skillAppearances.set(right.skill_id, (skillAppearances.get(right.skill_id) || 0) + 1);
  if (reviewQueue.length === 240) break;
}

await mkdir(outputRoot, { recursive: true });
await writeFile(
  inventoryPath,
  inventory.map(({ lexical_terms, vector, ...row }) => JSON.stringify({
    ...row,
    lexical_term_count: new Set(lexical_terms).size,
  })).join("\n") + "\n",
);
await writeFile(suggestionsPath, pairs.map((row) => JSON.stringify(row)).join("\n") + "\n");
await writeFile(reviewQueuePath, reviewQueue.map((row) => JSON.stringify(row)).join("\n") + "\n");
await writeFile(summaryPath, JSON.stringify({
  status: "LOCAL_DISCOVERY_ONLY_NOT_A_BENCHMARK_OR_RESULT",
  source_files: inventory.length,
  suggestion_pairs: pairs.length,
  manual_source_review_queue: reviewQueue.length,
  source_roots: sourceRoots.map((sourceRoot) => path.relative(process.cwd(), sourceRoot)),
  similarity_method: "TF-IDF cosine over frontmatter name, frontmatter description, and markdown headings",
  exclusions: [
    "No source body similarity model was used.",
    "No candidate cluster, prompt, gold label, acceptable-set judgement, field evidence, masking map, retrieval score, or external call was created.",
    "Every suggestion requires manual source review and independent acceptability review before it can enter RQ1b.",
  ],
}, null, 2) + "\n");

console.log(JSON.stringify({ source_files: inventory.length, suggestion_pairs: pairs.length, manual_source_review_queue: reviewQueue.length }));
