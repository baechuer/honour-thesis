---
name: localization-workspace
description: Review and manage a Multilocale localization workspace — projects, locale coverage, exact phrase translations, duplicate source copy, machine-translation status, locale dictionaries, project setup, locale rollout, and carefully confirmed phrase changes. This is a remote connector over translation data only; it cannot read or edit files in a codebase, so localizing an actual app also needs the `multilocale` CLI. Use when asked to audit translation completeness, inspect or revise localized copy, add a phrase or locale, export a language dictionary, or understand which Multilocale projects share a phrase.
license: Apache-2.0
compatibility: Requires the Multilocale MCP connector (https://mcp.multilocale.com/mcp) and a Multilocale account with access to at least one project
metadata:
  author: Multilocale
  version: '1.0.0'
  repository: https://github.com/multilocale/skills
---

# Localization workspace with Multilocale

## What this connector can and cannot do

Read this before planning any work. The Multilocale connector is remote and
OAuth-scoped: it can read and write translation data, but it cannot see or edit
the user's codebase.

| It can                                                                    | It cannot                                                  |
| ------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Read and write translation data — projects, locales, phrases, team roster | Read, search, write or diff any file on the user's machine |
| Machine-translate one phrase, or every phrase of a new locale             | Extract the strings an app currently hard-codes            |
| Export a locale dictionary as bounded, paginated JSON                     | Write a translation file into a repository                 |
| Audit coverage and duplicate source copy inside a project                 | Run a command, install a package, or open a pull request   |

So **"localize my app" is not a request this connector can complete on its
own.** Reading the strings a codebase already contains, and writing translation
files back into it, is the job of the `multilocale` CLI (`npx multilocale`) —
run by the user, or by an agent that does have shell and filesystem access,
such as Claude Code, Codex or Cursor. `multilocale import` uploads a codebase's
existing flat JSON or Android `strings.xml`; `multilocale download` writes every
locale back out.

When a user asks for a whole app to be localized:

1. Say plainly that this connector holds the translation data while the CLI
   moves the files, so part of the work happens in their terminal.
2. Do the part that does belong here — create or inspect the project, set its
   locales, review coverage, fix wording.
3. Hand over the file-side commands, and point at the companion
   `localize-an-app` skill (`npx skills add multilocale/skills`) and
   https://www.multilocale.com/integrations/cli/ for the full recipe.

Never invent phrase keys or values from a guess about the user's UI, and never
report an app as localized on the strength of connector calls alone: no tool
here has read a line of their code.

## Connecting

This skill drives the Multilocale MCP connector. The user must have connected
Multilocale and signed in to an account with access to a project. If a call
fails with an authorization error, ask the user to connect Multilocale instead
of retrying or asking for an API key.

## Start by resolving the project

Project names are organization-scoped slugs. Most phrase tools take the
project name, while project detail and write tools may accept an id or name.

- Call `list_projects` when the user has not identified a project precisely.
- Use `get_project` for exact metadata or `show_project_overview` when an
  inline overview would help.
- Do not guess a project from a common name such as `app` or `website`.
- Use the returned project name for phrase calls. Never infer an organization
  id; OAuth supplies the tenant boundary.

## Available tools

Project and team reads:

| Tool                    | Use it for                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| `list_projects`         | Discover accessible project ids, names, default locales and locale lists                       |
| `get_project`           | Read one project's bounded metadata                                                            |
| `show_project_overview` | Render one project's safe inline overview                                                      |
| `list_team_members`     | See a roster with display name and role only; email and internal member/role IDs stay excluded |

Phrase reads and audits:

| Tool                           | Use it for                                                            |
| ------------------------------ | --------------------------------------------------------------------- |
| `list_phrases`                 | Bounded phrase preview, optionally filtered by locale or exact key    |
| `get_phrase`                   | Exact key across locales, including generated-copy status and sharing |
| `search_phrases`               | Search keys and values when the exact key is unknown                  |
| `find_missing_translations`    | Coverage percentages and missing keys by locale                       |
| `find_duplicate_phrase_values` | Duplicate default-locale values that may be consolidation candidates  |
| `export_locale_dictionary`     | Paginated flat key/value export for one locale                        |

Writes:

| Tool             | Use it for                                                             |
| ---------------- | ---------------------------------------------------------------------- |
| `add_project`    | Create a project with a default locale and initial locale set          |
| `update_project` | Replace locales, change the default locale, or set translation context |
| `add_phrase`     | Create a new key and machine-translate it to configured locales        |
| `add_locale`     | Add one locale and machine-translate every missing source key          |
| `share_phrase`   | Attach every locale row of one key to additional projects              |
| `update_phrase`  | Overwrite one translation and mark it as human-edited                  |
| `delete_phrase`  | Permanently delete a key's complete locale group                       |

## Choose the narrowest read

Use `get_phrase` when the key is known. Use `search_phrases` only to discover a
key, then switch to the exact read before editing. `list_phrases` and search
results are bounded previews; they are not evidence that a large project has no
more rows.

Use `export_locale_dictionary` for a broad locale review. It returns
`hasMore`; continue with the returned next `skip` until false. Values can be
truncated at 500 characters and each page contains at most 50 entries. If
`valuesTruncated`, `offsetCapReached`, or a `partial` status is returned, say
that the export is a preview and do not silently treat it as a byte-exact file.
Use the Multilocale CLI when the user needs the complete file bytes.

`find_missing_translations` checks at most 10 locales and scans at most 2,000
phrases per locale. `find_duplicate_phrase_values` scans at most 2,000 source
phrases. Treat `partial`, `scanTruncated`, `sourceScanTruncated`,
`targetScanTruncated`, or `localesTruncated` as an explicit completeness caveat,
not evidence that unscanned copy is complete or unique.

## A standard localization audit

When asked to audit a project:

1. `get_project` to establish its default locale and configured locales.
2. `find_missing_translations` across all configured target locales.
3. `find_duplicate_phrase_values` to identify repeated default-locale copy.
4. `list_phrases` per target locale when the user wants a bounded review of
   machine-generated values.
5. `get_phrase` for each key whose wording or sharing needs close review.
6. `export_locale_dictionary` only when the user requests a full language
   dictionary or a broad copy review; paginate until `hasMore` is false, and
   preserve any `partial` caveat.

Report coverage gaps separately from copy quality. A present machine-generated
value counts as translated, but it may still need human review.

## Writes require exact intent

Do not turn an audit, suggestion, or translation request into a saved workspace
change. Before any write, identify the exact project, key or locale, summarize
what will happen, and obtain the user's approval when the host has not already
shown an approval prompt.

All seven writes declare `destructiveHint: true`. This is a conservative
cross-host approval boundary because each one persists a workspace mutation;
it does not mean every write deletes data. The individual tool description and
the rules below identify whether the operation creates data, replaces a list,
widens sharing, overwrites copy, spends translation capacity, or deletes rows.

`add_project` refuses a duplicate name. Include the default locale in the
planned locale set and show all initial locales before creating it.

`add_phrase` refuses an existing key. First call `get_phrase`; if it exists,
use `update_phrase` only after the user chooses one locale and approves the
replacement. Show the source value, configured target locales, requested model
when specified, and context. The tool can spend translation credits and saves
machine-generated values.

`add_locale` can translate every source key and therefore has variable cost and
a potentially large write surface. First call `find_missing_translations` for
the proposed locale, report the missing-key count, translation model and
context, then confirm. Do not call it once per missing key.

`update_project` treats `locales` as a **complete replacement list**, not a
patch. Read the project first, preserve every locale the user did not ask to
remove, and explicitly confirm any removal. A new default locale must be in
the replacement list.

`share_phrase` makes future edits affect every attached project. Read the exact
key first, resolve each target with `get_project`, remove the source project
and duplicates from the target list, then show the resulting sharing set.

## Overwrites and deletion

`update_phrase` overwrites an existing value. It is idempotent but destructive:
read the exact key and locale immediately before the call, show the previous
and proposed values, list every shared project from the read result, and
confirm the replacement. Do not overwrite a different locale as a shortcut for
adding a missing translation.

`delete_phrase` permanently removes every locale row for the key. If the rows
are shared, deletion also affects those other projects; it is not a detach
operation. Immediately before deletion, call `get_phrase` without a language
filter, show the number of translations and all shared projects, and ask for
explicit confirmation naming the key and source project. Never perform broad
or inferred deletion.

## Interactive views

`show_project_overview` renders a bounded project card, and `get_phrase` can
render a phrase-detail card, in hosts that support MCP Apps. When a card is
visible, add analysis the card does not show instead of restating every field.
