---
name: multilocale
description: Manage translations on multilocale.com with the `multilocale` CLI — add a phrase and machine-translate it into every project locale, correct a single translation, share one phrase across projects, roll a project out to new locales, download translation dictionaries (JSON, JavaScript, Swift .strings, Android strings.xml), import existing translation files, and audit duplicate or unused keys. Use when asked to add or fix a translation, localize an app into more languages, sync translation files with a codebase, audit localization coverage, or anything involving the `multilocale` command or app.multilocale.com data.
license: Apache-2.0
compatibility: Requires Node.js, network access, and a Multilocale account (https://app.multilocale.com)
metadata:
  author: Multilocale
  version: '1.0.0'
  repository: https://github.com/multilocale/skills
allowed-tools: Bash(multilocale:*) Bash(npx multilocale:*)
---

# Multilocale CLI

`multilocale` manages translation data on
[app.multilocale.com](https://app.multilocale.com): projects, one phrase row
per key and locale, machine translation into every configured locale,
translation-file download and import for app codebases, and cross-project
phrase sharing.

Run it as `multilocale` when installed globally (`npm install -g multilocale`)
or as `npx multilocale` otherwise. `multilocale --help` and
`multilocale <command> --help` are accurate and self-sufficient; prefer them
over memory when unsure of a flag, and `multilocale schema` prints the whole
command tree as JSON. `multilocale skills list` names the guides bundled with
the installed version, and `multilocale skills get multilocale` prints the
copy of this guide matching it.

## Setup

No account yet? Create one without leaving the terminal — the generated
password prints exactly once, and the session is stored so every other
command works immediately:

```bash
multilocale signup --email founder@example.com --json
```

Two ways to authenticate an existing account:

```bash
multilocale login              # interactive: choose browser or API key
multilocale login --browser    # browser flow; tokens land in ~/.multilocale/
multilocale login --with-key   # masked prompt for an API key secret
multilocale logout             # clears the stored session and any stored key
```

Or export `MULTILOCALE_API_KEY=<key secret>` — no login step needed, the key
is read from the environment on every command. Keys are created per project in
app.multilocale.com under the project's API keys page; new keys default to
read-only scopes, so widen them there before running write commands. The
secret is never accepted as a command-line argument.

Precedence: a stored browser session wins over a stored key, which wins over
the environment variable. Commands reuse the saved session and refresh it
automatically. In an interactive terminal, a command that finds no credentials
still starts the browser login on its own; without a terminal (agents, CI,
pipes) it fails fast with exit code 1 and login instructions on stderr instead
of opening a browser.

## Machine-readable output

Every data command accepts `--json`: raw, parseable JSON on stdout, no color.
Mutations print a small result object (`{ "ok": true, … }`). Errors always go
to stderr with exit code 1 — as a single-line JSON object when `--json` is
set — and progress logs move to stderr in json mode, so stdout is exactly the
JSON result.

```bash
multilocale projects list --json
multilocale phrases get SOME_KEY --json
multilocale schema                  # the whole command tree as JSON
multilocale schema phrases list     # one subcommand's arguments and flags
```

## Where to start

| You want                                            | Run                                             |
| --------------------------------------------------- | ----------------------------------------------- |
| The projects in this account                        | `multilocale projects list`                     |
| One project's locales and metadata                  | `multilocale projects read <idOrName>`          |
| A project's locales, name, context or paths changed | `multilocale projects update <idOrName> …`      |
| The phrases of a project                            | `multilocale phrases list`                      |
| A new phrase, translated to all locales             | `multilocale add …`                             |
| Fix one translation in one language                 | `multilocale update …`                          |
| Reuse an existing phrase in another project         | `multilocale share …`                           |
| Whole new languages for a project                   | `multilocale localize …`                        |
| Dictionary files written into a codebase            | `multilocale download`                          |
| An existing codebase's files uploaded once          | `multilocale import`                            |
| Consolidation and cleanup candidates                | `multilocale duplicates` · `multilocale unused` |

## Projects and configuration

A `multilocale.json` anywhere under the working directory supplies the default
project:

```json
{ "organizationId": "…", "projectId": "…" }
```

When it is missing, commands list the account's projects, ask which one to
use, and write the file for next time. `--project <idOrName>` overrides it per
invocation. The same file can also hold `download` defaults: `format`,
`extension`, `header`, `postScript`, and `paths`.

```bash
multilocale projects list                     # names and ids
multilocale projects get [projectIdOrName]    # raw JSON; all projects when omitted
multilocale projects read <projectIdOrName>   # formatted single-project view
multilocale projects create <name> --locales en,es,fr --default-locale en
multilocale projects update <projectIdOrName> --paths "messages/%lang%.json"
```

Project names are unique per organization, so commands accept a project by id
or by name interchangeably.

`projects update` is the only way to set a project's `paths`, which `import`
and `unused` read off the **project** — and a project's `paths` win over the
`paths` in `multilocale.json`, so a project carrying the wrong ones silently
overrides local configuration. It also repairs the nameless projects older
signups created (`--name`, `--locales`, `--default-locale`, `--paths` in one
call). Locale handling is deliberately additive: `--locales` adds,
`--remove-locales` removes, and only `--set-locales` replaces the list
outright. Confirm a `--set-locales` or `--remove-locales` with the user first —
on the wire the locale list is a complete replacement.

Older published builds have no `projects update`. Check with
`multilocale schema projects` before relying on it; without it, the same field
is settable over the REST API (`PUT /api/projects/:projectId`).

## Reading phrases

```bash
multilocale phrases list --project <p>        # grouped by language
multilocale phrases list -l fr                # one language
multilocale phrases list -k SOME_KEY          # one key across languages
multilocale phrases list --languages          # just the language list
multilocale phrases get [key] -l fr -n 20     # raw JSON rows, limited
```

`phrases get` prints the underlying rows, including the `projects` sharing
list and machine-translation provenance — read it before any destructive
change. `multilocale duplicates` lists keys whose default-language values are
identical (candidates for consolidation via `multilocale share`).
`multilocale unused` greps the local JavaScript sources (`.js`, `.jsx`, `.ts`,
`.tsx`, `.cjs`, `.mjs`) for each key and lists the ones never referenced —
treat the output as candidates, not proof: keys assembled dynamically at
runtime look unused. Android projects are not supported by `unused` yet.

## Adding a phrase — check for an existing one first

```bash
multilocale add "Save"                        # value defaults to the key
multilocale add "SAVE_BUTTON" "Save"
multilocale add "Max guests" --context "Hotel management app; the maximum number of hotel guests a room sleeps, not software users"
```

`add` creates the phrase in the project's default locale and machine-translates
it into every other configured locale in one shot. It refuses a key that
already exists in the project. Translation models: `gpt-5-nano` (default),
`gpt-5-mini`, `gemini-3.5-flash`, `claude-haiku-4-5` — select with
`-m/--model`. For short or ambiguous UI strings always pass `-c/--context`
with the product domain, what the word means there, and the UI role; an
isolated two-word string routinely machine-translates to the wrong sense.

`add` always creates a fresh, independent phrase for the target project. If
the key already exists in another project of the organization and the copy
should stay identical, attach the existing phrase with `multilocale share`
instead — adding it again creates a second, independently drifting set of
translations. Each `add` also spends machine translation on every target
locale, so do not loop it over a whole translation file: that is what
`multilocale import` is for.

## Sharing a phrase across projects

```bash
multilocale share "Save" other-project another-project --project source-project
```

`share` attaches each target project to every locale row of the source
phrase. From then on there is one row per locale for all attached projects —
an edit or deletion reaches every one of them. The targets receive only the
locales the source phrase has; locales a target project supports beyond that
stay missing until translated.

## Updating one translation

```bash
multilocale update "Save" "Enregistrer" -l fr
```

Sets the exact value for one key in one language (default: the project's
default locale) and clears the machine-translated flags, since the value is
now human-edited. If the phrase is shared, the CLI prints the affected
projects — the change reaches all of them. There is no model or context
option here: context matters only at machine-translation time (`add`,
`localize`, `import`).

## Deleting a key

```bash
multilocale delete "OLD_KEY"
```

Removes every locale row of the key from the current project. Shared rows are
deleted outright, not detached — projects sharing the key lose it too. Run
`multilocale phrases get "OLD_KEY"` first, check the `projects` field, and
confirm that blast radius with the user before deleting.

## Rolling out new locales

```bash
multilocale localize fr,de,ja
multilocale localize all
```

Adds the locales to the project and machine-translates every existing phrase
into them (`-m/--model` as for `add`). Cost scales with keys × new locales —
report the phrase count and get agreement before running `all`. Interruptions
are safe: a re-run reconciles the project and translates only what is still
missing.

## Translation files: download and import

```bash
multilocale download
multilocale download --format esm --extension js
multilocale download --post-script "prettier --write translations/"
```

`download` writes the project's dictionaries into the current directory tree:

- Android projects (detected by an `AndroidManifest.xml`): one
  `res/values-<locale>/strings.xml` per language, with Android's escaping
  rules applied.
- Everything else: one file per locale at the project's configured `paths`
  (`%lang%` placeholder), defaulting to `translations/<locale>.json`.
  Formats: `json`, `esm` (`export default {…}`), `js`/`cjs`
  (`module.exports = {…}`), and `swift` (`<locale>.lproj/Localizable.strings`).
- `--header` prepends a line to every generated file; `--post-script` runs a
  shell command after writing (formatters, codegen).

`import` is the reverse, for onboarding an existing codebase: it reads the
Android `strings.xml` files or the JSON dictionaries matching the project's
paths, uploads them as phrases, and machine-translates keys that are missing
from some configured locales. Import once per codebase — re-importing creates
duplicate rows rather than merging.

A phrase is a flat key/value pair, and `import` reads JSON only — no YAML,
gettext, XLIFF, `.properties` or `.arb`. Nested or namespaced dictionaries
(next-intl, react-i18next namespaces, Lingui catalogs) need flattening into dot
paths: newer builds do it during `import` and say so, and `--no-flatten` makes
them refuse instead; older published builds store the nested object as the
phrase value and then spend translation credits turning it into garbage. Run
`multilocale schema import` — if `--no-flatten` is listed the build flattens,
otherwise flatten the files before importing. For the whole app-localization
workflow, see the `localize-an-app` skill.

## Errors → remediation

| Symptom                                            | Fix                                                                                       |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Browser login never completes                      | Rerun `multilocale login --browser`; the login URL is printed for manual use, and it times out after 5 minutes |
| 401 / authorization error mid-command              | Session expired — `multilocale login`, or export `MULTILOCALE_API_KEY`, then retry        |
| `Not logged in, and no terminal to log in from.`   | Headless run without credentials — export `MULTILOCALE_API_KEY=<key secret>`, or run `multilocale login` once in an interactive terminal |
| 401 / 403 with an API key on a write command       | New keys are read-only — widen the key's scopes on the project's API keys page in app.multilocale.com |
| `a phrase with key "…" already exists`             | Use `multilocale update` to change it, or `multilocale share` to attach another project   |
| `no phrase found with key … and language …`        | Check the key with `multilocale phrases list -k <key>`; if the locale is missing, `multilocale localize <locale>` adds it |
| `There are no projects`                            | Create one: `multilocale projects create <name> --locales …`                              |
| `Could not detect project type`                    | Run from the app's root: Android needs an `AndroidManifest.xml`, JavaScript a `package.json` |
| Wrong project touched                              | The nearest `multilocale.json` wins — check its `projectId`, or pass `--project` explicitly |
