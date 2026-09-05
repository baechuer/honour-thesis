#!/usr/bin/env node

import { readFile, readdir, writeFile } from "node:fs/promises";
import { join, relative, resolve } from "node:path";

const root = resolve("skill_benchmark/rq1_public_original_removal_v3_82_registry");
const ledgerPath = join(root, "parse_ledger/parse_ledger.json");
const canonicalRoot = join(root, "parse_submissions/canonical");
const ledger = JSON.parse(await readFile(ledgerPath, "utf8"));
const pendingRows = ledger.rows.filter((row) => row.parse_status === "PENDING_NEW_SOURCE_ONLY_PARSE");
if (pendingRows.length !== 6) throw new Error(`Expected six pending V3 parse rows, found ${pendingRows.length}.`);

const submissions = [];
for (const filename of (await readdir(canonicalRoot)).filter((name) => /^OR82-\d{3}\.json$/.test(name)).sort()) {
  const submission = JSON.parse(await readFile(join(canonicalRoot, filename), "utf8"));
  if (submission.status !== "PARSE_COMPLETE" || submission.compositions?.length !== 1) throw new Error(`Invalid canonical submission ${filename}.`);
  submissions.push({ filename, submission, composition: submission.compositions[0] });
}
if (submissions.length !== 6) throw new Error(`Expected six canonical V3 submissions, found ${submissions.length}.`);
const parsedById = new Map(submissions.map((entry) => [entry.composition.composition_id, entry]));
if (parsedById.size !== 6) throw new Error("Duplicate canonical V3 composition IDs.");

for (const row of pendingRows) {
  const parsed = parsedById.get(row.composition_id);
  if (!parsed) throw new Error(`Missing canonical parse for ${row.composition_id}.`);
  row.parse_status = "PARSED_NEW_SOURCE_ONLY";
  row.canonical_submission = `parse_submissions/canonical/${parsed.filename}`;
  row.candidates = parsed.composition.candidates;
}
const counts = ledger.rows.reduce((acc, row) => {
  acc[row.parse_status] = (acc[row.parse_status] ?? 0) + 1;
  return acc;
}, {});
if (counts.REUSED_VERIFIED_SOURCE_ONLY_PARSE !== 76 || counts.PARSED_NEW_SOURCE_ONLY !== 6) throw new Error(`Unexpected final parse status: ${JSON.stringify(counts)}`);
ledger.status = "RQ1_ORIGINAL_REMOVAL_V3_82_PARSE_LEDGER_COMPLETE";
ledger.counts = { compositions: 82, reused_verified: 76, newly_parsed: 6, pending_new_parse: 0 };
await writeFile(ledgerPath, `${JSON.stringify(ledger, null, 2)}\n`);
await writeFile(
  join(root, "parse_ledger/INGESTION_STATUS.json"),
  `${JSON.stringify({ status: "PASS", counts, canonical_submissions: submissions.map((entry) => `parse_submissions/canonical/${entry.filename}`) }, null, 2)}\n`,
);
console.log(JSON.stringify({ status: "PASS", compositions: ledger.rows.length, counts }));
