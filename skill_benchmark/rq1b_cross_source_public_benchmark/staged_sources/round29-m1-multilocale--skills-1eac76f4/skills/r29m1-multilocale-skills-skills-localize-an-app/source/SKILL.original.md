---
name: localize-an-app
description: End-to-end recipe for translating a whole application with Multilocale — choose the ecosystem's own i18n runtime, create a project with explicit locales, import an existing catalogue once, download the generated files, and wire them in. Covers both a greenfield app with no i18n and an app already running next-intl, react-i18next, Lingui, Android resources or iOS .strings. Use when asked to localize, internationalize, translate, or add languages to an app, website or repository, rather than to change a single phrase.
license: Apache-2.0
compatibility: Requires Node.js, a shell with filesystem access to the app's source, and a Multilocale account (https://app.multilocale.com)
metadata:
  author: Multilocale
  version: '1.0.0'
  repository: https://github.com/multilocale/skills
allowed-tools: Bash(multilocale:*) Bash(npx multilocale:*)
---

# Localize an app with Multilocale

## Before anything: who does what

**`multilocale` is a CLI that syncs translation _files_. It is not a runtime
library.** Multilocale stores one phrase row per key and locale and machine
translates between them; the app's own i18n runtime renders those strings.

- Do **not** add any `@multilocale/*` npm dependency.
  `@multilocale/multilocale-react` and `@multilocale/multilocale-js-client` are
  unmaintained 2023 packages and `@multilocale/react` is 404 on npm. The one
  maintained package is `multilocale`, the CLI.
- Rendering stays with the ecosystem's standard: next-intl, react-i18next,
  Lingui, Android string resources, iOS `.strings`, and so on.

**This skill needs a shell.** If you are running as a remote MCP connector or
in a host with no filesystem, you cannot do this work: say so, and hand the
commands below to the user instead of inventing phrases. The Multilocale
connector can create the project and review the copy, but it can never read the
app's source or write a file.

## Never guess a flag — and check the build first

The installed CLI describes itself, and that is the source of truth:

```bash
npx --yes multilocale schema            # whole command tree as JSON
npx --yes multilocale schema import     # one subcommand's arguments and flags
npx --yes multilocale --help
```

Every data command also accepts `--json`, which puts a parseable result on
stdout and moves progress logs to stderr.

Two capabilities differ by version and change the recipe. Check both before
starting; each check is read-only:

| Check                                            | If listed                                          | If not                                      |
| ------------------------------------------------ | -------------------------------------------------- | ------------------------------------------- |
| `multilocale schema projects` shows `update`     | `projects update … --paths` sets a project's paths | Set `paths` over REST (last section)        |
| `multilocale schema import` shows `--no-flatten` | `import` flattens nested dictionaries itself       | Flatten the files yourself before importing |

## Get a session

```bash
npx multilocale signup --email you@example.com --json   # no account yet
npx multilocale login                                   # existing account
export MULTILOCALE_API_KEY=<key secret>                 # headless / CI
```

Precedence is stored browser session → stored key → environment variable. With
no credentials and no terminal, commands fail fast with login instructions
rather than opening a browser. New API keys are read-only — widen their scopes
on the project's API keys page before running a write command.

---

## Recipe 1 — greenfield: the app has no i18n yet

**1. Pick the ecosystem's standard runtime and install it.**

| App                                  | Runtime                | Files it reads                       |
| ------------------------------------ | ---------------------- | ------------------------------------ |
| Next.js App Router                   | `next-intl`            | `messages/<locale>.json`             |
| Vite / React Router / Remix / Gatsby | `react-i18next`        | `locales/<locale>.json`              |
| Compile-time catalogs                | `@lingui/react`        | `src/locales/<locale>/messages.json` |
| Android                              | resource qualifiers    | `res/values-<locale>/strings.xml`    |
| iOS                                  | `NSLocalizedString`    | `<locale>.lproj/Localizable.strings` |
| Jekyll / static site                 | data files + templates | `_data/<locale>/strings.json`        |

**2. Create the project with explicit locales.** Do not rely on whatever
project signup created for you:

```bash
npx multilocale projects create my-app --default-locale en --locales en,es,fr,de --json
```

The default locale is added to the locale list automatically if you leave it
out. `projects create` sets no `paths`, which is what you want — see the trap
about server-side paths below.

**3. Pin the project and choose where files land** in a `multilocale.json` at
the app root:

```json
{
  "projectId": "<the id printed above>",
  "format": "json",
  "extension": "json",
  "paths": ["messages/%lang%.json"]
}
```

`%lang%` is replaced with each of the project's locales. Without a pinned
`projectId` every command has to resolve a project, which is how agent runs
stall.

**4. Add the source strings.** Each `add` writes the default locale and machine
translates into every other configured locale in one shot:

```bash
npx multilocale add "Save"
npx multilocale add "SAVE_BUTTON" "Save"
npx multilocale add "Max guests" -c "Hotel app; how many people a room sleeps, not software users"
```

Always pass `-c/--context` for short or ambiguous UI strings; an isolated
two-word string routinely translates to the wrong sense. Models available via
`-m/--model`: `gpt-5-nano` (default), `gpt-5-mini`, `gemini-3.5-flash`,
`claude-haiku-4-5`.

Do **not** loop `add` over a whole file — every call spends machine translation
on every locale. That is what `import` is for (Recipe 2).

**5. Download the dictionaries.**

```bash
npx multilocale download
npx multilocale download --format esm --extension js
npx multilocale download --post-script "prettier --write messages/"
```

**6. Wire the runtime at the files you just downloaded**, and add a
`postScript` in `multilocale.json` if the runtime needs a different shape —
at minimum to drop the injected `"locale"` key (see traps).

**7. Commit the generated files.** A fresh clone must build with no account and
no network.

**8. Add languages later** with one command; existing keys are translated into
the new locales and the run is resumable:

```bash
npx multilocale localize it,ja,pt
npx multilocale localize all
```

---

## Recipe 2 — the app already has i18n

The incumbent library keeps rendering. Multilocale becomes where the strings
are edited and translated. Nothing is ripped out until the round trip is
proven.

**1. Detect the incumbent — do not replace it.**

```bash
grep -E '"(next-intl|i18next|react-i18next|vue-i18n|@lingui/core|svelte-i18n|@formatjs/[a-z-]+)"' package.json
git ls-files | grep -Ei '(locales?|messages|translations|lang|i18n)/.*\.(json|ya?ml|po|xlf|xliff|properties|arb)$' | head -50
find . -name AndroidManifest.xml -o -name '*.lproj' | head
```

Record: the library, the catalogue paths, the locale ids used in the
filenames, and which locale is the source.

**2. Flatten the catalogue — only if it is nested.** A Multilocale phrase is a
flat key/value pair. A nested or namespaced catalogue — which is what
next-intl, react-i18next namespaces and Lingui produce — becomes
`checkout.failed` style dot paths.

If the catalogue is already flat, **skip this step**: importing it untouched
keeps every key byte-identical to the `t()` calls in the source, which is what
you want.

If it is nested and `multilocale schema import` lists `--no-flatten`, the CLI
flattens during import and prints which files it flattened; go to step 3 and
read that output. If the flag is absent, **your build stores the nested object
as the phrase value and then spends translation credits turning it into
garbage** — flatten first, into a scratch directory, leaving the app's own
catalogue untouched:

```bash
mkdir -p .multilocale-import
for f in messages/*.json; do
  node -e '
    const fs = require("fs")
    const [src, dst] = process.argv.slice(1)
    const flat = {}
    const escape = segment => segment.replaceAll("\\", "\\\\").replaceAll(".", "\\.")
    const walk = (node, path) => {
      for (const [k, v] of Object.entries(node)) {
        const next = [...path, escape(k)]
        if (v && typeof v === "object" && !Array.isArray(v)) walk(v, next)
        else if (v !== null && v !== undefined) flat[next.join(".")] = String(v)
      }
    }
    walk(JSON.parse(fs.readFileSync(src, "utf8")), [])
    fs.writeFileSync(dst, JSON.stringify(flat, null, 2))
  ' "$f" ".multilocale-import/$(basename "$f")"
done
```

A dot inside a key is escaped to `\.` so it cannot be mistaken for the
separator the flattening just introduced — which means a key that already
contained a literal dot changes shape. Check with
`multilocale phrases list -k <key>` after importing and reconcile with the
`t()` calls in the source. Re-nesting is this function run backwards, splitting
on _unescaped_ dots only.

Keep a copy of what you are about to upload — step 7 diffs the round trip
against it:

```bash
cp -R .multilocale-import /tmp/flattened-before
```

If the catalogue is YAML, gettext, XLIFF, `.properties`, `.arb` or a JS/TS
module, convert it to flat JSON here — `import` reads nothing else (see the
format table).

**3. Create a project whose locales match the filenames exactly.** The CLI
substitutes each locale into `%lang%` and matches files by suffix, so a project
locale `fr` never finds `fr-FR.json`:

```bash
npx multilocale projects create my-app --default-locale en --locales en,fr,de,ja --json
```

**4. Point `paths` at the flattened files:**

```json
{
  "projectId": "…",
  "format": "json",
  "extension": "json",
  "paths": [".multilocale-import/%lang%.json"]
}
```

`import` and `unused` read `paths` off the **project** and fall back to
`multilocale.json` only when the project has none — so if the project already
carries paths (every project created by `multilocale signup` does), set them on
the project instead:

```bash
npx multilocale projects update my-app --paths ".multilocale-import/%lang%.json"
```

and if that subcommand does not exist in your build, use the REST call in the
last section.

**5. Import once.**

```bash
npx multilocale import --json
```

`import` uploads every matched file and machine translates the keys missing
from some configured locales. **It is not idempotent** — a second run creates
duplicate rows instead of merging. If it went wrong, delete the bad keys before
re-importing.

**6. Verify before trusting it.**

```bash
npx multilocale phrases list --languages          # every locale that arrived
npx multilocale phrases list -l fr                # spot-check one language
npx multilocale phrases list -k some.dotted.key   # one key across locales
npx multilocale duplicates                        # identical source values
```

Compare the key count against the flattened source. A value that reads
`[object Object]` means step 2 was skipped for that file.

**7. Run in parallel, then switch.** Download into the same scratch directory
and diff against what you flattened — this proves the round trip before
anything in the app changes:

```bash
npx multilocale download
diff <(jq -S . .multilocale-import/fr.json) <(jq -S . /tmp/flattened-before/fr.json)
```

Expect exactly one difference: the injected `"locale"` key. When the diff is
otherwise clean, repoint the incumbent loader at the downloaded files — either
by setting `paths` to the app's real catalogue location, or by keeping the
scratch directory and adding a `postScript` that re-nests the keys and drops
`"locale"`. Delete the old catalogue only after a build passes.

**8. From here on**, strings are edited in Multilocale and pulled down:

```bash
npx multilocale add "New string" -c "<where it appears>"
npx multilocale update "Save" "Enregistrer" -l fr    # fix one translation
npx multilocale localize it,pt                       # add languages
npx multilocale download                             # refresh the files
npx multilocale unused                               # keys no source file mentions
```

---

## What `import` and `download` actually support

| Format                                                              | `import`                                               | `download`                          |
| ------------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------- |
| Flat JSON at `paths`, in a project with a `package.json`            | yes                                                    | yes (`--format json`)               |
| Android `res/values*/strings.xml` (an `AndroidManifest.xml` exists) | yes                                                    | yes (automatic, escaped)            |
| JS/TS module catalogue (`export default {…}`)                       | **no**                                                 | yes (`--format esm`, `js`, `cjs`)   |
| iOS `<locale>.lproj/Localizable.strings`                            | **no**                                                 | yes (`--format swift`)              |
| Nested or namespaced JSON                                           | as dot paths when the build flattens, otherwise **no** | flat only — re-nest in a postScript |
| YAML, gettext `.po`, XLIFF, `.properties`, `.arb`, `.resx`          | **no**                                                 | **no**                              |

Project type is detected by file presence anywhere below the working
directory: an `AndroidManifest.xml` makes it an Android project, otherwise a
`package.json` makes it a JavaScript one, otherwise every file command fails
with `Could not detect project type`. Run from the app root.

## Traps, all verified against multilocale@1.2.2

| Trap                                                                                                                                               | What to do                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| A project's `paths` **override** the `paths` in `multilocale.json`. Every project created by `multilocale signup` ships `translations/%lang%.json` | Use a project from `projects create` (it sets none), or set them with `projects update` / REST        |
| `download` injects `"locale": "<lang>"` into every generated dictionary; only the `swift` writer filters it out                                    | Strip it in a `postScript`; it is not a message                                                       |
| Older builds store nested values as objects, then machine translate them                                                                           | Check `schema import` for `--no-flatten`; flatten first when it is absent                             |
| `import` is not a merge                                                                                                                            | Run it once per codebase                                                                              |
| `localize` throws `Not implemented yet` on Android projects                                                                                        | Manage Android locales from app.multilocale.com, then `download`                                      |
| `localize` reads `paths` from the project only, never `multilocale.json`                                                                           | With no project paths it falls back to the phrases already on multilocale.com, which is usually right |
| `unused` greps only `.js .jsx .ts .tsx .cjs .mjs`                                                                                                  | Swift, Kotlin, Vue, Svelte and Ruby keys all report as unused — treat output as candidates            |
| The nearest `multilocale.json` in the tree wins                                                                                                    | Keep exactly one, at the app root                                                                     |
| `delete` and `update` reach every project sharing the key                                                                                          | Run `multilocale phrases get <key>` and read `projects` first                                         |
| There is no YAML output format                                                                                                                     | The whitelist is `cjs`, `esm`, `json`, `js`, `swift`                                                  |

### Setting `paths` on the project itself

Prefer the CLI when the build has it:

```bash
npx multilocale projects update my-app --paths "messages/%lang%.json"
```

Otherwise use the REST API. **Send the project back whole, with only the fields
you mean to change replaced** — read, merge, PUT:

```bash
AUTH="Authorization: Basic $(printf %s "$MULTILOCALE_API_KEY" | base64)"
curl -s "https://api.multilocale.com/api/projects/$PROJECT_ID" -H "$AUTH" \
  | jq '.paths = ["messages/%lang%.json"]' \
  | curl -s -X PUT "https://api.multilocale.com/api/projects/$PROJECT_ID" \
      -H "$AUTH" -H 'Content-Type: application/json' --data-binary @-
```

A body carrying only `{"paths": …}` looks like it works — the stored document
is merged field by field — but the handler compares the body's `logo` against
the stored one and deletes the project's logo image when they differ, so a
partial body silently destroys the logo. Read-then-merge avoids it.

Authentication is the key **secret alone**, base64-encoded — no key/secret pair
and no colon. The key needs the `projects:write` scope; new keys are read-only
until widened.

## Working examples

Each is a real app, built in CI, that this recipe is drawn from:

- Next.js + next-intl — https://github.com/multilocale/nextjs-multi-language-website-example
- Remix + react-i18next — https://github.com/multilocale/remix-multi-language-website-example
- Gatsby + react-i18next — https://github.com/multilocale/gatsby-multi-language-website-example
- Lingui — https://github.com/multilocale/linguijs-multi-language-website-example
- Jekyll — https://github.com/multilocale/jekyll-multi-language-website-example
- iOS — https://github.com/multilocale/ios-multi-language-app-example
- Android — https://github.com/multilocale/android-multi-language-app-example

Guides: https://www.multilocale.com/developers/ ·
CLI reference: `npx multilocale skills get multilocale`
