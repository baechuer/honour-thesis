---
name: slidev
description: Generate Slidev presentations from slide outlines with preset styles, unique designs, custom style descriptions, and image placement.
argument-hint: "[--help | --dev [dir] | --export <format> [dir] | --edit [dir] <comment> | --picture [auto|paths...] [dir] | --create-preset <name> | --learn=N | --deep_learn=N | --figma=<URL> | --no-preset | --preset <name> | style: <desc>] <outline or file path>"
---

# Slidev Presentation Generator

You generate complete Slidev presentation projects from slide outlines. Every generation produces a polished, distinctive presentation ready to run.

## References

Before generating, internalize these references:
- `references/slidev-syntax.md` — Slidev markdown syntax
- `references/slidev-layouts.md` — Layout selection guide
- `references/slidev-animations.md` — Animations & transitions
- `references/preset-format.md` — Preset file specification
- `references/layout-css-patterns.md` — **CRITICAL**: Battle-tested CSS patterns for each layout type (alignment, backgrounds, overlays)
- `references/design-principles.md` — **CRITICAL**: Gamma-level design quality principles (visual rhythm, layout diversity, typography drama, icon system, card variation, decorative layer, visual arc, data viz, mockups, SVG diagrams, spacing, accent hierarchy). Apply in ALL modes: generation, editing, presets, Visual QA.
- `references/scoring-subroutine.md` — Slide scoring (1-10 on 9 axes), used by --polish, --learn, --compare
- `references/content-review-subroutine.md` — Content quality checks (3-second test, narrative flow, redundancy, CTA clarity, hierarchy)
- `references/polish-procedure.md` — `--polish=N` iterative improvement cycle
- `references/ab-testing.md` — A/B variant generation for weak slides (used by --polish)
- `references/design-memory.md` — Design pattern memory (read/write protocol)
- `references/compare-procedure.md` — `--compare` side-by-side scoring
- `references/notes-procedure.md` — `--notes` speaker notes generation
- `references/responsive-check.md` — `--responsive` aspect ratio check

## Input Parsing

Parse the user's input to determine the subcommand or mode:

### Subcommands (handle before anything else)

**`--help`**: Display usage help and stop. Show:

```
Slidev Presentation Generator

Usage:
  /slidev <outline or file>                     Generate with unique design
  /slidev --preset <name> <outline>              Generate with preset style
  /slidev style: <desc> <outline>                Generate with custom style
  /slidev --theme <name> <outline>               Generate with specific theme
  /slidev --polish=N [dir]                       Iterative quality improvement (N cycles)
  /slidev --edit [dir] <comment>                 Edit existing presentation
  /slidev --picture [auto|paths...] [dir]        Add images to slides
  /slidev --compare <dir1> <dir2>                Compare two presentations
  /slidev --notes [dir]                          Generate speaker notes
  /slidev --responsive [dir]                     Check 4:3 rendering
  /slidev --export <format> [dir]                Export (html|pdf|png2pdf|pngs|png_N)
  /slidev --dev [dir]                            Launch dev server
  /slidev --create-preset <name>                 Create a new preset
  /slidev --learn=N                              Self-improving loop (N cycles)
  /slidev --learn=N --preset <name>            Preset learning (create + refine with visual critic)
  /slidev --deep_learn=N                       Preset deep learning (auto-refine N cycles)
  /slidev --deep_learn=N --preset <name>       Deep learn a specific preset
  /slidev --add_archetype [name]              Add a new composition archetype
  /slidev --stitch=design <outline>             Stitch придумывает стиль → наш pipeline генерирует
  /slidev --stitch=full <outline>              Stitch генерирует ВСЮ презу → адаптируем в Slidev
  /slidev --stitch=improve <dir>               Stitch делает variants каждого слайда готовой презы
  /slidev --stitch=design --learn=N            Learn с Stitch-стилями
  /slidev --stitch=learn=N              Learn from Stitch as design teacher (N cycles)
  /slidev --figma=<URL>                         Create preset from Figma template
  /slidev --figma=<URL> --learn=N               Figma learning (create preset + refine with Figma reference)
  /slidev --figma=<URL> --deep_learn=N           Same as --figma --learn (both trigger FDL)
  /slidev --figma=<URL> <outline>               Create preset from Figma + generate presentation
  /slidev --no-preset <outline>                Generate without auto-preset (Unique mode)
  /slidev --help                                 Show this help
```

**`--create-preset <name>`**: Interactive preset creation wizard.

1. Extract preset name from arguments. If missing, ask for one (kebab-case).
2. Ask 8 questions **ONE AT A TIME**, waiting for each answer:
   - **Mood**: "What mood? (professional, playful, dramatic, calm, futuristic, elegant, bold)"
   - **Color scheme**: "Light or dark? (dark, light, deep navy, warm cream...)"
   - **Accent color**: "Accent color? (#ff6b35, electric blue, warm coral...)"
   - **Typography**: "Font personality? (geometric & modern, rounded & friendly, sharp & technical, humanist & classic, condensed & bold)"
   - **Density**: "Content density? (minimal with whitespace, balanced, information-dense)"
   - **Textures**: "Background textures? (subtle noise, gradient mesh, geometric patterns, clean flat, frosted glass)"
   - **Slide types**: "Какие типы слайдов чаще всего будут? (метрики/числа, таймлайны, команда, портфолио, сравнения, данные...)"
   - **Transitions**: "Slide transitions? (fade, slide-left, none...)"
   - **Save location**: "Save preset globally or locally? (global: ~/.claude/slidev-presets/, local: ./.slidev-presets/ in current project)"
3. Synthesize answers into concrete design params using `/frontend-design` principles (distinctive Google Fonts — never Inter/Roboto/Arial/generic choices, cohesive palette with dominant+accent hierarchy, atmospheric backgrounds, CSS). The CSS block MUST include layout-specific styles per `references/preset-format.md` — explicit `text-align: center` on `h1`, `p`, `div` for all centered layouts (cover, section, fact, end, statement, center), plus background image overlay support for cover/section. See `references/layout-css-patterns.md` for the required patterns.
   Based on the "Slide types" answer, generate the `archetypes` section with `preferred`/`avoid` lists and the `shapes` section with appropriate defaults. For example, if the user said "метрики и команда", set `preferred: [stat-hero, profile-grid, bento-grid]` and `icon_container: circle`.
   After determining the accent color, check it against the AI color blacklist (hue 240-290 at saturation >50%). If the accent falls in this range, regenerate with a different hue. Common safe alternatives: teal (#0D9488), amber (#D97706), emerald (#059669), rose (#E11D48).
4. Based on save location answer:
   - **Global**: Create `~/.claude/slidev-presets/` if needed, write `<name>.preset.md` there
   - **Local**: Create `.slidev-presets/` in the current working directory if needed, write `<name>.preset.md` there
   Write per `references/preset-format.md`.
4b. **Generate theme directory**: Based on the preset's CSS block and font/color choices, generate a `<name>-theme/` directory alongside the preset file with:
   - `package.json` (Slidev theme metadata with font defaults — use Slidev's native `fonts.serif` key for body font slot even though value is sans-serif)
   - `styles/index.css` (CSS variables, base layout, shape vocabulary from preset CSS block)
   - `styles/layouts.css` (layout-specific text alignment, background overlay support)
   - `layouts/none.vue`, `layouts/default.vue` (passthrough: `<template><div class="slidev-layout" style="padding:0;overflow:hidden;"><slot /></div></template>`)
   - `layouts/cover.vue` (bg-accent background), `layouts/section.vue` (bg-alt), `layouts/end.vue` (bg-accent)
5. Generate demo presentation using `assets/demo-outline.md` with that preset, output to `demo-<name>/`.
6. **Visual QA** — Run the Visual QA Loop for `demo-<name>/`.
7. Print summary: preset path (noting global vs local), demo path, Visual QA results, how to preview, how to use.

**`--add_archetype [name]`**: Add a new composition archetype to the library.

1. If `name` not provided — ask "Как назвать архетип? (kebab-case)"
2. Ask: **"Для какого типа контента этот архетип? Опишите ситуацию, когда существующие архетипы не подходят."**
3. Based on the answer, determine:
   - How many archetypes are actually needed (may be 1, may be 2-3 for different aspects)
   - Density level for each (low / medium / medium-high / high)
   - Group classification (hero / grid / split / timeline / table / cta)
   - Which content types it serves
   - Which shape elements it uses (circles, pills, hexagons, etc.)
4. Generate HTML skeleton following the format in `references/composition-archetypes.md` (using `{{SLOT}}` markers, `layout: none`, max 3 div nesting levels, inline styles)
5. Append the archetype record(s) to `references/composition-archetypes.md` — both the archetype definition AND its content-type association in the mapping table at the top
6. Generate a test slide using the new archetype with sample content and export as PNG for visual verification
7. Report: archetype name(s), density, content types served, and the test slide PNG path

Stop here — do not proceed to generation.

**`--stitch=<mode> <outline>`**: Use Google Stitch AI as a design partner. Three modes:

```
/slidev --stitch=design <outline>    Stitch придумывает визуальный стиль → мы делаем презу
/slidev --stitch=full <outline>      Stitch генерирует ВСЮ презу → мы адаптируем в Slidev
/slidev --stitch=improve <dir>       Stitch делает variants каждого слайда готовой презы
```

Can be combined with `--learn=N`: `/slidev --stitch=design --learn=7`

**CRITICAL:** Always use `modelId: "GEMINI_3_1_PRO"` for all Stitch calls — самая умная модель.

### Stitch Mode: design

Stitch придумывает визуальный стиль (мы НЕ задаём ему цвета/шрифты — он сам). Мы получаем от него стиль и конвертируем в пресет.

**ST-D1: Parse outline** — Прочитать outline. Сформировать описание презентации на английском: тема, аудитория, настроение, количество слайдов.

**ST-D2: Создать 3 проекта с разными промптами** — Каждый проект получает ОДИНАКОВЫЙ контент но РАЗНЫЙ промпт для стиля. Мы НЕ задаём шрифты, цвета, roundness — Stitch решает сам.

Для каждого из 3 стилей:
```
1. create_project({ title: "slidev-style-<N>-<topic>" }) → получить projectId

2. generate_screen({
     projectId: "<id>",
     prompt: "<полный промпт — см. ниже>",
     deviceType: "DESKTOP",
     modelId: "GEMINI_3_1_PRO"
   })
   → Блокирующий вызов (1-5 мин). Возвращает { screenId, html, screenshotUrl }.
   HTML готов — шаг 3 не нужен.
```

**Промпты для 3 стилей** (отличаются ТОЛЬКО стилевым направлением):
- **Style 1**: "Design a complete presentation as a single-page website. Each slide is a `<section>` tag, 16:9 aspect ratio. Topic: [topic]. [slide count] slides. Content per slide: [brief per-slide content]. **Style direction: clean, professional, trustworthy.** Choose your own color palette, fonts, and layout — make it look like a premium human-designed presentation, NOT AI-generated."
- **Style 2**: "Design a complete presentation as a single-page website. Each slide is a `<section>` tag, 16:9 aspect ratio. Topic: [topic]. [slide count] slides. Content per slide: [brief per-slide content]. **Style direction: bold, energetic, modern.** Choose your own color palette, fonts, and layout — make it look like a premium human-designed presentation, NOT AI-generated."
- **Style 3**: "Design a complete presentation as a single-page website. Each slide is a `<section>` tag, 16:9 aspect ratio. Topic: [topic]. [slide count] slides. Content per slide: [brief per-slide content]. **Style direction: elegant, editorial, refined.** Choose your own color palette, fonts, and layout — make it look like a premium human-designed presentation, NOT AI-generated."

**ВАЖНО**: В промпте указываем ВЕСЬ контент всех слайдов (кратко). Stitch генерирует ЦЕЛЫЙ "сайт" — все слайды в одном экране. Каждый слайд в `<section>`.

**ST-D3: Получить и проанализировать 3 HTML** — Для каждого стиля:
1. `get_screen` → получить HTML
2. Извлечь из HTML (Stitch сам выбрал — мы только читаем):
   - Цветовая палитра (background, text, accent, surface)
   - Шрифты (headline, body)
   - Border-radius
   - Декоративные паттерны (градиенты, тени, формы)
   - Структура layout'ов

**ST-D4: Агент выбирает лучший стиль** — Оценка по:
- 50-point AI Detection Rubric (docs/research/ai-presentation-detection-guide-ru.md)
- Контрастность и читаемость
- Запоминаемость дизайна
- Соответствие теме и аудитории
Записать выбор и причины в `stitch-style-selection.md`.

**ST-D5: Конвертировать в пресет** — Из победившего HTML извлечь стиль → записать `.slidev-presets/stitch-<timestamp>.preset.md`:
- Шрифты из HTML → `fonts.sans`, `fonts.body` (**serif check**: если Stitch выбрал serif → заменить ближайшим sans-serif)
- Цвета из HTML → `--color-accent`, `--bg-base`, `--bg-alt`, `--bg-accent` и производные
- Roundness из HTML → `card_radius`, `icon_container`
- Декоративные приёмы → описание в aesthetic section пресета

**ST-D6: Стандартный pipeline** — PDL (3 цикла) → генерация презентации. Если `--learn=N` → learning loop.

**ST-D7: Cleanup** — Удалить 3 Stitch-проекта (временные).

### Stitch Mode: full

Stitch генерирует всю презентацию целиком как HTML-сайт. Мы извлекаем стиль И контент, адаптируем в Slidev.

**ST-F1: Parse outline** — Так же как ST-D1.

**ST-F2: Создать 3 проекта, каждый = полная презентация** — Промпт содержит ВСЕ слайды с контентом:

```
generate_screen({
  projectId: "<id>",
  prompt: "Design a complete presentation as a single-page website where each slide
    is a <section> tag with width:100% and aspect-ratio:16/9.

    CONTENT:
    Slide 1 (Cover): [title, subtitle]
    Slide 2 (Problem): [heading, 3 pain points]
    Slide 3 (Solution): [heading, key features]
    ...
    Slide N (CTA): [call to action, contacts]

    Style direction: [clean professional / bold energetic / elegant editorial].
    Design a COMPLETE, polished presentation. Each section should have distinct
    layout (not all identical). Use real visual hierarchy — hero numbers large,
    body text readable, decorative accents varied. Make it NOT look AI-generated.",
  deviceType: "DESKTOP",
  modelId: "GEMINI_3_1_PRO"
})
```

**ST-F3: Получить HTML** — `get_screen` для каждого стиля.

**ST-F4: Агент выбирает лучший** — Так же как ST-D4.

**ST-F5: Парсинг HTML → Slidev** — Из победившего HTML:
1. Разделить по `<section>` тегам → получить HTML каждого слайда
2. Извлечь общий стиль → создать `styles/index.css` + пресет
3. **FONT SIZE RECALCULATION** — Stitch генерирует для веб-viewport (~1440px), а Slidev рендерит на 960x540. Все font-size из Stitch HTML нужно пересчитать:
   - Stitch px → Slidev rem: разделить на 16, затем проверить против FONT SIZE FLOOR
   - **ПОСЛЕ пересчёта** — применить FONT SIZE FLOOR из Step 5:
     - Body text: если < 1.25rem → поднять до 1.25rem
     - Headings: если < 2.2rem → поднять до 2.2rem
     - Labels/pills: если < 0.65rem → поднять до 0.65rem
   - **Типичные пересчёты из Stitch:**
     - Stitch 14px (0.875rem) body → Slidev 1.25rem (поднять)
     - Stitch 12px (0.75rem) caption → Slidev 0.85rem (поднять, если body-текст)
     - Stitch 24px (1.5rem) heading → Slidev 2.2rem (поднять)
     - Stitch 48px (3rem) hero → Slidev 3rem+ (ок)
   - **НЕ копировать font-size из Stitch напрямую** — всегда пересчитать и валидировать
4. Для каждого слайда:
   - Извлечь inline styles → адаптировать под CSS variables
   - Сохранить layout-структуру (grid/flex)
   - Обернуть в `layout: none` + `position:absolute;inset:0` Slidev-обёртку
5. Собрать `slides.md` из всех слайдов
6. **Запустить ПОЛНЫЙ QA pipeline включая ВСЕ BLOCKING checks** (QA-0a/0b/0c → visual QA). BLOCKING checks (font size, CSS vars, decoration visibility) ОБЯЗАНЫ остановить pipeline если нарушены — даже в --stitch=full режиме. Stitch-режим НЕ является исключением из QA.

**ST-F6: Cleanup**.

### Stitch Mode: improve

Берёт ГОТОВУЮ презентацию и для каждого слайда запрашивает у Stitch варианты. Сохраняет целостность стиля.

**ST-I1: Прочитать готовую презентацию** — `<dir>/slides.md` и `styles/index.css`. Извлечь общий стиль (палитра, шрифты, формы).

**ST-I2: Создать Stitch-проект с дизайн-системой презентации**:
```
create_project({ title: "slidev-improve-<name>" })

create_design_system({
  projectId: "<id>",
  designSystem: {
    displayName: "Current presentation style",
    theme: {
      colorMode: "<LIGHT|DARK — из styles/index.css>",
      headlineFont: "<соответствие шрифту из презентации>",
      bodyFont: "<соответствие>",
      roundness: "<соответствие card_radius>",
      customColor: "<--color-accent hex>"
    }
  }
})
```

**ST-I3: Для каждого слайда** с оценкой < 7 из score-report (или для всех, если score-report нет):
1. Сгенерировать экран в Stitch с контентом этого слайда:
   ```
   generate_screen({
     projectId: "<id>",
     prompt: "Presentation slide: [slide content]. Style must match the design system. 16:9.",
     deviceType: "DESKTOP",
     modelId: "GEMINI_3_1_PRO"
   })
   ```
2. Запросить 3 варианта:
   ```
   generate_variants({
     projectId: "<id>",
     selectedScreenIds: ["<screen_id>"],
     prompt: "Generate alternative layouts for this presentation slide. Keep content and color scheme, vary the layout structure and visual hierarchy.",
     variantOptions: {
       variantCount: 3,
       creativeRange: "EXPLORE",
       aspects: ["LAYOUT"]
     }
   })
   ```
3. Применить дизайн-систему ко всем вариантам:
   ```
   apply_design_system({ projectId, selectedScreenInstances, assetId })
   ```
4. Получить HTML всех вариантов → выбрать лучший layout
5. Адаптировать layout-идею (grid-структуру, позиционирование) обратно в наш Slidev-слайд

**ST-I4: Собрать улучшенный slides.md** — Заменить слабые слайды на улучшенные варианты. Запустить QA.

**ST-I5: Cleanup**.

**Stitch MCP Server** — кастомный `stitch-slidev` MCP-сервер на базе `@google/stitch-sdk`. Все вызовы **блокирующие** (await) — никакого поллинга.

| Тул | Описание |
|-----|----------|
| `create_project` | Создание проекта. Возвращает `{ projectId, name }` |
| `generate_screen` | **Генерация экрана И скачивание HTML** — один вызов, блокирующий. Возвращает `{ screenId, html, screenshotUrl }` |
| `get_project` | Получение деталей проекта + список экранов |
| `get_screen_html` | Скачивание HTML существующего экрана. Возвращает `{ html }` |
| `get_screen_image` | URL скриншота экрана |
| `generate_variants` | Генерация вариантов дизайна. Возвращает массив `{ id, html }` |

**Стратегия получения HTML из Stitch:**

1. Создать проект: `create_project({ title: "..." })` → получить `projectId`
2. Сгенерировать экран с HTML: `generate_screen({ projectId, prompt, deviceType: "DESKTOP", modelId: "GEMINI_3_1_PRO" })`
   - Вызов **блокирующий** — ждёт завершения генерации на сервере (1-5 минут)
   - Возвращает **готовый HTML** в поле `html` — не нужен curl/WebFetch/поллинг
   - Также возвращает `screenshotUrl`
3. Для существующего экрана: `get_screen_html({ projectId, screenId })` → `{ html }`
4. Для вариантов: `generate_variants({ projectId, screenId, prompt, variantCount: 3, creativeRange: "EXPLORE" })` → массив `{ id, html }`

**КРИТИЧНО: `generate_screen` может выполняться 1-5 минут.** Это нормально — SDK ждёт завершения генерации на сервере. НЕ прерывать, НЕ повторять.

**NO FALLBACK**: `--stitch` требует Stitch. Без него — стоп.

Stop here after Stitch procedure completes. If combined with `--learn=N`, proceed to Learning Loop.

**`--stitch=learn=N`**: Learn from Stitch as external design teacher. Compares Stitch output with our output side-by-side, extracts CSS patterns.

### Stitch Learn Procedure

**STL-1: Generate N diverse outlines** — Same as L-2 in --learn: Russian language, varied industries/formats/sizes.

**STL-2: For each cycle i = 1 to N:**

**STL-2.1: Stitch generates** — `create_project({ title })` → `generate_screen({ projectId, prompt, deviceType: "DESKTOP", modelId: "GEMINI_3_1_PRO" })`. Промпт включает все слайды. Вызов блокирующий — возвращает готовый HTML в поле `html`. Сохранить в `<edu_dir>/stitch_<i>/stitch-output.html`.

**STL-2.2: Our generator makes the same presentation** — Standard pipeline with current skill rules, same outline. Save to `<edu_dir>/stitch_<i>/our-output/`. Export PNG.

**STL-2.3: Comparative analysis** — Compare both HTML outputs across 6 dimensions, extracting concrete CSS values:

```
BACKGROUNDS:
  Stitch: [layers count, gradient types, opacity values]
  Ours:   [layers count, gradient types, opacity values]
  Gap:    [what Stitch does better]
  → RULE: [specific CSS addition to skill]

LAYOUT:
  Stitch: [grid templates, proportions, asymmetry]
  Ours:   [grid templates]
  → RULE: [...]

TYPOGRAPHY:
  Stitch: [size hierarchy, weight distribution]
  Ours:   [...]
  → RULE: [...]

DECORATION:
  Stitch: [shapes, opacity, sizes, positions]
  Ours:   [...]
  → New decoration-library.md components if found

CARDS:
  Stitch: [card variety, bento ratios, styles]
  Ours:   [...]
  → RULE: [...]

HIERARCHY:
  Stitch: [focal point ratio, dominant element size]
  Ours:   [...]
  → RULE: [...]
```

**STL-2.4: Extract patterns** → append to `docs/research/stitch-learned-patterns.md`:
```markdown
## Pattern: [name]
- Source: Stitch cycle [i], slide [N]
- CSS: [concrete CSS code]
- When: [which slide types benefit]
- Added to: [which skill file was updated]
```

If a new decoration shape/behavior is found → add to `references/decoration-library.md` as a new component with {{PLACEHOLDER}} template.

**STL-2.5: Apply improvements** via Python script (same as L-3e). Update SKILL.md, design-principles.md, decoration-library.md.

**STL-2.6: Промежуточный отчёт** пользователю:
```
━━━ Stitch Learn <i>/<N> — СРАВНЕНИЕ ━━━

Оценка Stitch: X/10
Наша оценка:   Y/10
Разница:       [+/-Z]

Что Stitch делает лучше:
  - [аспект] — извлечено правило: "[описание]"
  - [аспект] — новый компонент в decoration-library
  ...

Что мы делаем лучше:
  + [аспект] (сохраняем)

Применено правил: [кол-во]
Новых компонентов в библиотеке: [кол-во]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**STL-2.7: Git commit + tag** — same as L-3f/L-3g in --learn.

**STL-3: Final report** with progress.md table (same format as --learn).

**Stitch API handling**: `generate_screen` блокирующий (1-5 мин). Если ошибка — STOP (no fallback). НЕ повторять вызов.

**`--learn=N`**: Learning loop. Parse N from the argument (e.g., `--learn=5`).
- **Without `--preset`**: Self-improving skill loop. Follow the Learning Loop Procedure (L-1 through L-5) — improves SKILL.md and design-principles.md based on visual critique.
- **With `--preset <name>`**: Preset learning loop. Creates (or uses named) preset, generates N demo presentations, visual critic evaluates and proposes CSS/font/color improvements. Follow the Preset Learning Procedure (PL-1 through PL-6).

Stop here — do not proceed to generation.

**`--deep_learn=N`**: Preset deep learning loop. Creates (or uses named) preset, then iteratively auto-refines it through N cycles of 3 visual test runs with convergence detection. N must be >= 2.
- **With `--preset <name>`**: deep learn a specific preset
- **Without `--preset`**: interactive wizard creates the initial preset (same as `--create-preset`)

Follow the Preset Deep Learning Procedure (PDL-1 through PDL-7). Stop here — do not proceed to generation.

**`--figma=<URL>`**: Create a preset from a Figma presentation template. Optionally run a learning loop with live Figma comparison.

**URL Parsing**: Extract `fileKey` and optional `nodeId` from the Figma URL:
- `https://figma.com/design/:fileKey/:fileName?node-id=:nodeId` → convert `-` to `:` in nodeId
- `https://figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey
- If no `node-id` in URL → use `0:1` (first page)
- If URL is not `figma.com/design/...` → error: `--figma only supports Figma Design files (figma.com/design/...)`

**Compatibility checks**:
- `--figma` is **incompatible** with `--stitch`, `--preset`, `--no-preset`, `style:`. If any present → error: `--figma cannot be combined with --stitch/--preset/--no-preset/style:. It creates its own preset.`
- `--figma` is **compatible** with `--learn=N`, `--deep_learn=N`, `<outline>`.

**Dispatch logic**:
1. Always run the **Figma Extraction Procedure (FIG-1 through FIG-5)** first → creates preset + archetypes + reference data.
2. If `--learn=N` or `--deep_learn=N` present → run **Figma Learning Loop (FDL-1 through FDL-5)**. Both flags trigger the same FDL procedure (since fixes never go to SKILL.md, the distinction is irrelevant). Maximum N: 10. Stop after FDL.
3. If `<outline>` present (no --learn) → generate presentation using the created Figma preset. Continue to Generation Modes with the Figma preset loaded.
4. If neither `--learn` nor `<outline>` → generate demo presentation using `assets/demo-outline.md` with the Figma preset, run Visual QA, print summary. Stop.

### Figma Extraction Procedure

**FIG-1: File Structure Reconnaissance** — Use `mcp__figma__use_figma` (Plugin API) to run JavaScript that traverses the node tree on the target page:

```javascript
// Pseudocode for the JS to run via use_figma:
// 1. Get the target page (by nodeId or first page)
// 2. Iterate page.children — find all FRAME nodes
// 3. Filter: abs(width/height - 16/9) < 0.05*16/9 (aspect ratio ~16:9 ±5%)
// 4. Sort by y position (top to bottom) then x (left to right)
// 5. Return: [{id, name, width, height, index}]
```

Result: ordered list of slide frames. If 0 frames found → error: `No slides found (frames with ~16:9 aspect ratio). Check file structure.` If > 20 frames → take first 20, warn: `Found <N> slides, using first 20 (maximum for extraction).`

**FIG-2: Global Style Extraction** — For ALL slide frames, collect design statistics via `mcp__figma__use_figma` (Plugin API). Run a single JS call that traverses all children recursively and collects:

**Colors** — group all `fills` by frequency:
- Frame background fills (direct children fills with full area) → most frequent = `--bg-base`, second = `--bg-alt`
- Small bright-colored elements (used in <20% of nodes) → `--color-accent`
- Text node colors by frequency → most frequent = `--color-text`, second = `--color-muted`
- Derive `--color-accent-rgb` (R,G,B triple), `--bg-accent` (accent at 12% opacity over bg-base)
- **AI Color Blacklist check**: if accent hue 240-290 at saturation >50% → shift to nearest safe hue (teal #0D9488, amber #D97706, emerald #059669, rose #E11D48). Log replacement.

**Fonts** — collect all `fontFamily`, `fontSize`, `fontWeight` from text nodes:
- Heading font: most frequent fontFamily in nodes with fontSize ≥ 24px → `fonts.sans`
- Body font: most frequent fontFamily in nodes with fontSize < 24px → `fonts.body`
- **Serif check**: if either font is serif → find nearest sans-serif (per skill rule: serif banned). Log: `Font "<name>" (serif) → "<replacement>" (sans-serif)`

**Spacing** — collect from auto-layout frames:
- Median `itemSpacing` across all auto-layout frames → standard gap
- Median `paddingLeft`/`paddingTop` → base padding

**Shapes** — collect `cornerRadius`:
- Median cornerRadius of frames with width 100-400px (card-sized) → `card_radius`
- Nodes with cornerRadius ≥ 50% of min(width,height) → `icon_container: circle`
- Nodes with cornerRadius 8-16px → `icon_container: rounded-square`

**Effects** — collect `effects` array:
- Drop shadows → extract offset, blur, color for aesthetic description
- Background blurs → note in aesthetic section

Convert all collected data into `.preset.md` format per `references/preset-format.md` (YAML frontmatter + aesthetic description + CSS block with `:root` variables).

**FIG-3: Per-Slide Extraction** — For each slide frame from FIG-1, extract four levels of data:

**Level 1 — Screenshot (visual reference):**
- Call `mcp__figma__get_design_context(nodeId, fileKey)` → returns screenshot inline + React+Tailwind code
- Call `mcp__figma__get_screenshot(nodeId, fileKey)` → returns screenshot URL. Download via WebFetch and save to `figma-<name>-figma/slide-<N>-<name>/reference.png` — this is the persistent visual reference used as fallback when Figma API is unavailable during FDL.
- Save React+Tailwind code as code hint for layout understanding

**Level 2 — Structure (positions and sizes):**
- Call `mcp__figma__get_metadata(nodeId, fileKey)` → XML with node IDs, layer types, names, positions, sizes
- Parse the XML into a structured list: `[{name, type, x, y, width, height, children: [...]}]`

**Level 3 — Detailed properties (exact CSS values):**
- Call `mcp__figma__use_figma` with JS that for each child element (recursive, max depth 3) extracts:
  - `fills` (array of paint objects), `strokes`, `effects` (shadow, blur)
  - `fontSize`, `fontFamily`, `fontWeight`, `lineHeight`, `letterSpacing`
  - `layoutMode` (HORIZONTAL/VERTICAL/NONE), `itemSpacing`, `paddingLeft/Right/Top/Bottom`
  - `constraints`, `layoutAlign`, `layoutGrow`, `layoutSizingHorizontal/Vertical`
  - `cornerRadius`, `opacity`
  - `characters` (text content — for determining which elements become slots)
  - `type` (TEXT, FRAME, RECTANGLE, ELLIPSE, etc.)
- Save as `blueprint.json` in the archetype's directory (`figma-<name>-figma/slide-<N>-<name>/blueprint.json`):

```json
{
  "slideIndex": 1,
  "slideName": "Cover",
  "frameWidth": 1440,
  "frameHeight": 810,
  "elements": [
    {
      "name": "Title",
      "type": "TEXT",
      "x": 120, "y": 280, "width": 1200, "height": 80,
      "fontSize": 48, "fontFamily": "Inter", "fontWeight": 700,
      "lineHeight": 1.1, "letterSpacing": -0.02,
      "fills": [{"type": "SOLID", "color": "#1A1A2E"}],
      "characters": "Presentation Title Here",
      "slot": "TITLE"
    },
    {
      "name": "Card Container",
      "type": "FRAME",
      "x": 120, "y": 400, "width": 1200, "height": 300,
      "layoutMode": "HORIZONTAL", "itemSpacing": 24,
      "paddingLeft": 0, "paddingTop": 0,
      "cornerRadius": 0,
      "children": [
        {
          "name": "Card 1",
          "type": "FRAME",
          "x": 0, "y": 0, "width": 384, "height": 300,
          "cornerRadius": 12,
          "fills": [{"type": "SOLID", "color": "#F5F5F0"}],
          "layoutMode": "VERTICAL", "itemSpacing": 12,
          "paddingLeft": 24, "paddingTop": 24,
          "children": ["..."]
        }
      ]
    }
  ]
}
```

**Level 4 — Code hint:**
- Already obtained in Level 1 via `get_design_context` — the React+Tailwind code
- Used as supplementary hint for understanding grid structure (flex vs grid, column ratios)

**FIG-4: Archetype Conversion** — From FIG-3 data, for each slide, build a composition archetype.

**Step 4-pre: Deduplication** — Before converting, group slides by layout similarity. Two slides are **duplicates** (merged into one archetype) ONLY if ALL of the following match exactly:
- Same number of direct children at the top level
- Same `layoutMode` (HORIZONTAL/VERTICAL/NONE) on the root frame
- Same grid structure (column/row count, same fr ratios ±5%)
- Same element type sequence (TEXT, FRAME, FRAME, TEXT vs TEXT, FRAME, TEXT, FRAME = different)
- Same nesting depth

If ANY detail differs — different spacing, different element sizes, different decorative elements, different number of sub-elements inside cards, different background treatment — they are **separate archetypes**. Err on the side of keeping more archetypes. Name duplicates: first occurrence becomes the archetype, others reference it via `duplicateOf` in source.json.

**Image-only and decoration-only slides** (no text children, only images/shapes/fills): these are **NOT skipped**. Create archetypes with `{{IMAGE}}` or `{{BACKGROUND}}` slots. These are valuable as gallery, showcase, full-bleed, and visual break archetypes. Content type: `visual-break`. Slot: `{{IMAGE_URL}}` for the primary image area, optionally `{{CAPTION}}` if there's any small text.

**Step 4a: Determine content type** — Analyze elements in the blueprint:
- First slide with one large heading (fontSize ≥ 36px) + subtitle + minimal other content → `intro` (cover)
- Last slide with button-like element or CTA text → `cta`
- Slide with 1-2 very large numbers (fontSize ≥ 48px) + small label → `metric`
- Slide with 3+ similarly-sized child frames in a row/grid → `credentials` or `scope` (cards/grid)
- Slide with circular image containers + text blocks → `team`
- Slide with ordered steps or numbered items → `process`
- Slide with one large heading + one paragraph, minimal decoration → `vision` (section divider)
- Slide with no text, only images/shapes/fills → `visual-break` (gallery, full-bleed, mosaic)
- Default for unrecognized patterns → `context` (two-col-text)

**Step 4b: Build HTML skeleton** — Convert Figma layout to HTML with `{{SLOT}}` markers:

- **Auto-layout HORIZONTAL** → `display:flex; flex-direction:row; gap:<itemSpacing>px`
- **Auto-layout VERTICAL** → `display:flex; flex-direction:column; gap:<itemSpacing>px`
- **No auto-layout (absolute positioning)** → `position:relative` container with `position:absolute` children
- **Nested frames** → nested `<div>` elements. **Max 3 levels** — if deeper, flatten (merge intermediate frames' styles into parent or child). Log: `Slide <N>: nesting flattened from <X> to 3 levels`
- **Text elements** → `{{SLOT_NAME}}` markers. Naming convention:
  - Single heading → `{{TITLE}}`
  - Single subtitle/paragraph → `{{SUBTITLE}}` or `{{DESCRIPTION}}`
  - Items in repeated grid → `{{CARD_1_TITLE}}`, `{{CARD_1_DESC}}`, `{{CARD_2_TITLE}}`, etc.
  - Large number → `{{METRIC_VALUE}}`
  - Small label above metric → `{{METRIC_LABEL}}`
- **Viewport conversion** — Figma uses arbitrary coords (e.g., 1440x810), Slidev renders at 960x540:
  - Position: `figma_x / figma_frame_width * 100` → percentage
  - Font size: `figma_fontSize / 16` → rem, then apply Font Size Floor: body ≥ 1.25rem, heading ≥ 2.2rem, label ≥ 0.65rem
  - Spacing (gap, padding): `figma_px / 16` → rem
  - Proportions (width ratios between siblings) → preserved as fr units or percentages

Wrap entire skeleton in:
```html
<div style="position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;...padding:...">
  <!-- archetype content here -->
</div>
```

All slides use `layout: none` + `.slidev-layout { padding: 0 !important; overflow: hidden; }` (per Rule 25).

**Step 4c: Create flexibility rules** — For each archetype, generate a flexibility rules file (`flexibility.yaml`) stored alongside the archetype:

```yaml
archetype: figma-<name>
content_type: <detected type from step 4a>
figma_source:
  nodeId: "<nodeId>"
  name: "<frame name from Figma>"

slots:
  title:
    max_length: <estimated from text box width: width_px / avg_char_width>
    overflow: shrink-font     # shrink-font | truncate | wrap
  cards:                       # only if repeated elements detected
    count_in_figma: <N>
    min: <max(2, N-1)>
    max: <N+2>
    scaling: grid-auto         # grid-auto (change columns) | wrap (overflow row) | stack (vertical)

layout:
  grid_columns: flexible       # flexible (can change col count) | fixed (exact match required)
  preserve:                    # IMMUTABLE — these must match Figma
    - spacing-ratio
    - font-size-hierarchy
    - color-usage
    - border-radius
  flexible:                    # ADAPTABLE — can change to fit content
    - column-count
    - card-count
    - text-length
```

**FIG-5: Preset Assembly** — Assemble all outputs into a complete preset:

**Directory structure:**
```
.slidev-presets/
  figma-<name>.preset.md               # global style + CSS (from FIG-2)
  figma-<name>-theme/                   # Slidev theme directory (generated from CSS block)
    package.json
    styles/index.css
    layouts/none.vue, default.vue
    layouts/cover.vue, section.vue, end.vue
  figma-<name>-figma/                   # Figma reference data
    source.json                         # {fileKey, sourceUrl, nodeIds, extractedAt}
    slide-1-<name>/
      blueprint.json                    # element properties (from FIG-3 Level 3)
      archetype.html                    # HTML skeleton with {{SLOT}} (from FIG-4b)
      flexibility.yaml                  # scaling rules (from FIG-4c)
    slide-2-<name>/
      ...
```

**Preset frontmatter** — add `figma` section to the standard preset YAML:
```yaml
---
name: figma-<name>
figma:
  fileKey: "<fileKey>"
  sourceUrl: "<full Figma URL>"
  extractedAt: "<ISO 8601 timestamp>"
  slideCount: <N>
  archetypes:
    - id: figma-<slide-1-name>
      nodeId: "<nodeId>"
      contentType: <detected type>
    - id: figma-<slide-2-name>
      nodeId: "<nodeId>"
      contentType: <detected type>
# ... rest of standard preset fields (fonts, theme, colorSchema, accentColor, etc.)
---
```

**Archetypes block:**
```archetypes
preferred: [figma-<slide-1-name>, figma-<slide-2-name>, ...]
avoid: []
cta_style: figma-<cta-slide-name>
cover_style: figma-<cover-slide-name>
```

**Theme directory** — generate from the CSS block (same as `--create-preset` step 4b): `package.json`, `styles/index.css`, layout Vue files.

**source.json:**
```json
{
  "fileKey": "<key>",
  "sourceUrl": "<URL>",
  "extractedAt": "<ISO 8601>",
  "figmaFrameWidth": 1440,
  "figmaFrameHeight": 810,
  "slideNodes": [
    {"index": 1, "nodeId": "1:2", "name": "Cover", "contentType": "intro"}
  ]
}
```

Print extraction summary:
```
━━━ Figma Extraction Complete ━━━
Source: <URL>
Slides extracted: <N>
Preset: .slidev-presets/figma-<name>.preset.md

Archetypes:
  1. figma-<name> (intro) — 3 slots, flexible grid
  2. figma-<name> (scope) — 5 slots, 3-col grid
  ...

Fonts: <heading> + <body>
Palette: <bg-base> / <accent> / <text>
```

### Figma Learning Loop (FDL)

Triggered when `--figma=<URL>` is combined with `--learn=N` or `--deep_learn=N`. Both flags trigger the same FDL loop (since fixes are always scoped to the preset, not SKILL.md).

**Maximum N**: 10. If N > 10, cap at 10 and notify.

**FDL-1: Initialization** — Preset is already created by FIG-Extract. Create the next sequential `edu_XX/` directory (same as standard `--learn` L-1). Store `fileKey` and the slide `nodeId` list from `source.json` for live queries during comparison.

**FDL-2: Generate N diverse outlines** — Same as L-2: create all outlines upfront. Save each as `<edu_dir>/learn_<i>/outline.md`. **All outlines MUST be in Russian.** Vary across industries, formats, sizes, tone (same diversity rules as standard --learn).

**FDL-3: Learning cycle** — For i = 1 to N:

**FDL-3a: Generate presentation** — Launch a subagent (Agent tool) to run the full `/slidev` pipeline:
- Uses the Figma preset from FIG-5 (re-reads `.preset.md` from disk — it may have been modified by prior cycle's fixes)
- Uses the outline from `<edu_dir>/learn_<i>/outline.md`
- Outputs to `<edu_dir>/learn_<i>/`
- During Composition Planning: match content types to Figma archetypes (see "Figma Archetype Priority" section below)
- During slot filling: apply `flexibility.yaml` rules

**FDL-3b: Export** — After creation:
```bash
cd <edu_dir>/learn_<i> && npm install && npx playwright install chromium
npx slidev export --format png --output slides
```
If export fails, log error in critique.md and skip to FDL-3g. Do NOT abort the entire learning loop.

**FDL-3c: Figma Live Comparison** — For **EVERY** generated slide (not just those with Figma archetypes), run three comparison levels. For each slide:
- If the slide used a Figma archetype → compare against that archetype's Figma `nodeId`
- If the slide used a standard fallback archetype → compare against the **closest matching** Figma slide by content type. This ensures that even fallback archetypes maintain visual consistency with the Figma template's design language.

Read the `nodeId` from `source.json`.

**Level 1 — Visual comparison (screenshot vs screenshot):**
- Get fresh Figma screenshot: `mcp__figma__get_screenshot(nodeId, fileKey)` → returns image
- Critic agent sees BOTH: our exported PNG from `slides/<N>.png` + Figma screenshot
- Evaluates: overall visual impression, color correspondence, typography proportions, layout balance
- For fallback archetype slides: evaluate whether the slide **looks like it belongs** in the same presentation as the Figma slides. Same color palette? Same font treatment? Same whitespace density? Same footer style?

**Level 2 — Structural comparison (positions and sizes):**
- Get fresh metadata: `mcp__figma__get_metadata(nodeId, fileKey)` → XML with positions/sizes
- Parse our `slides.md` — extract CSS values (position, width, height, grid-template, gap, padding)
- Compare with tolerances:
  - Element positions (heading, cards, icons): ±5% of viewport
  - Element proportions (width/height ratio): ±10%
  - Nesting hierarchy (level count, element order): exact match

**Level 3 — Style comparison (exact CSS values):**
- Get fresh properties: `mcp__figma__use_figma` with JS → extract fonts, colors, spacing, radius, effects for the slide's elements
- Compare against our CSS values:

| Property | Figma Source | Our CSS | Tolerance |
|----------|-------------|---------|-----------|
| font-size | `fontSize` (px → rem) | `font-size` | ±0.15rem |
| font-weight | `fontWeight` | `font-weight` | exact |
| color | `fills[0].color` (hex) | `color` / `var(--*)` | ΔE < 5 (CIEDE2000) |
| spacing (gap) | `itemSpacing` (px → rem) | `gap` | ±0.25rem |
| padding | `padding*` (px → rem) | `padding` | ±0.5rem |
| border-radius | `cornerRadius` (px) | `border-radius` | ±2px |
| position | `x, y` (normalized %) | position/margin/grid | ±5% viewport |

**FDL-3d: Critic Report** — Launch a subagent (Agent tool) as a Figma fidelity critic. Provide all three comparison levels. The critic writes to `<edu_dir>/learn_<i>/critique.md`:

```markdown
# Figma Fidelity Report: Iteration <i>

## Overall Fidelity Score: X/10

## Per-Slide Comparison

### Slide N: <name> (archetype: figma-<name>, nodeId: <id>)
- **Visual fidelity**: X/10 — <brief note>
- **Structural fidelity**: X/10 — <brief note>
- **Style fidelity**: X/10 — <brief note>

Issues:
1. [CRITICAL|MAJOR|MINOR] <description> — Figma: <value>, Ours: <value>, tolerance: <threshold>
   → Fix: <target file> — <exact change description>

## Adaptation Quality
- Slides where flexibility rules worked well: [list]
- Slides where flexibility rules failed: [list + reason]
  → Fix: update flexibility.yaml — <specific change>

## What Matched Well
- [list of archetype parts that matched — do NOT modify these]
```

Critic scoring guide:
- **Visual fidelity**: Does our slide LOOK like the Figma original? Color mood, typography weight, whitespace distribution.
- **Structural fidelity**: Are elements in the right positions? Grid structure, hierarchy depth, element ordering.
- **Style fidelity**: Do exact CSS values match within tolerance? Font sizes, colors, spacing, border-radius.

Overall score = weighted average: Visual 40% + Structural 30% + Style 30%.

**FDL-3e: Apply fixes** — Automatic (same policy as PDL-2.4):
- `critical` severity: always apply
- `major` severity: always apply
- `minor` severity: auto-apply only if fix touches a single CSS property; otherwise defer

Fixes go to:
- **Archetype HTML** (`figma-<name>-figma/slide-<N>/archetype.html`) — layout, positioning, grid structure
- **Preset CSS** (`.preset.md` CSS block) — colors, fonts, spacing variables
- **Flexibility rules** (`figma-<name>-figma/slide-<N>/flexibility.yaml`) — if content adaptation failed

**NEVER** modify SKILL.md, design-principles.md, or any other skill file.

After applying changes to the preset CSS, regenerate the `<name>-theme/` directory from the updated CSS block (same as PDL-2.4).

Log all changes to `<edu_dir>/learn_<i>/changes-applied.md`:
```
# Figma Learning Cycle <i> Changes

## Applied
1. [archetype: figma-cover] gap: 2rem → 1.5rem — severity: major
   Figma value: 24px (1.5rem), was: 2rem

## Skipped
1. [archetype: figma-cards] shadow blur: 8px → 6px — severity: minor, reason: multi-property shadow change
```

**FDL-3f: Intermediate report** — Print to user:
```
━━━ Figma Learning: Итерация <i>/<N> ━━━

Figma Fidelity: X/10
  Визуальное совпадение:   X/10
  Структурное совпадение:  X/10
  Стилевое совпадение:     X/10

Правки: <X> applied (critical: <C>, major: <M>), <Y> skipped (minor)
Идеальные слайды: <count>/<total>
Проблемные: <slide names with scores below 7>
```

**FDL-3g: Git commit** — Stage and commit all artifacts for this iteration:
```bash
git add <edu_dir>/learn_<i>/
git add .slidev-presets/figma-<name>.preset.md
git add .slidev-presets/figma-<name>-figma/
git commit -m "learn(slidev-figma): iteration <i>/<N> — fidelity <score>/10"
git tag figma-learn-<edu_dir>-iter-<i>
```

**FDL-4: Convergence detection** — After each cycle's report, check:
- If Fidelity Score ≥ 9/10 for **two consecutive cycles** → stop early:
  ```
  Раннее завершение: fidelity стабилизировался на <score>/10 в циклах <c-1> и <c>.
  ```
  Skip remaining cycles, proceed to FDL-5.
- If score decreased vs previous cycle (regression) → warn but do NOT stop. Next cycle will attempt to fix it.

**FDL-5: Final report** — Write to `<edu_dir>/figma-learning-report.md` and print:
```markdown
# Figma Learning Report

## Source: <Figma URL>
## Cycles: <actual> / <N planned>
## Early stop: yes/no (reason)
## Final Fidelity: X/10

## Fidelity Progression
Cycle 1: ██████░░░░ 6.2
Cycle 2: ████████░░ 7.8
Cycle 3: █████████░ 9.1

## Archetype Changes Summary
- figma-<cover>: <N> fixes (<list>)
- figma-<cards>: <N> fixes (<list>)
...

## Flexibility Rules Updated
- figma-<cards>: max changed 5 → 6, scaling changed grid-auto → wrap
...

## Final Preset State
- Path: .slidev-presets/figma-<name>.preset.md
- Archetypes: <N>
- Theme: .slidev-presets/figma-<name>-theme/
```

Stop here — do not proceed to generation.

### Figma Procedure: Edge Cases

| Situation | Behavior |
|-----------|----------|
| URL is not `figma.com/design/...` | Error: `--figma only supports Figma Design files (figma.com/design/...)` Stop. |
| No access to Figma file (API error) | Error: `No access to Figma file. Ensure the file is shared or you are authorized.` Stop. |
| No 16:9 frames found on the page | Error: `No slides found (frames with ~16:9 aspect ratio). Check file structure.` Stop. |
| Frame nesting > 3 levels | Flatten to 3 levels during archetype creation. Log warning. |
| Figma API unavailable during FDL learning cycle | Retry 2× with 10s pause. If still unavailable → use cached `blueprint.json` and saved `reference.png` from `figma-<name>-figma/slide-<N>-<name>/` directory (saved during FIG-3). Visual comparison uses cached PNG; structural/style comparison uses cached blueprint. Log: `⚠ Figma API unavailable, using cached reference for slide <N>` |
| Slide frame contains only image fill (no child elements) | Create archetype with `{{IMAGE}}` / `{{BACKGROUND}}` slots, content type `visual-break`. Useful for gallery, showcase, full-bleed slides. Log: `Slide <N> "<name>": image-only, created as visual-break archetype` |
| Serif font detected in Figma | Replace with nearest sans-serif. Log replacement. |
| Accent color in AI blacklist (hue 240-290, sat >50%) | Shift hue to nearest safe color. Log replacement. |
| > 20 slide frames in file | Take first 20. Warn: `Found <N> slides, using first 20 (maximum for extraction).` |

### Figma Procedure: Limitations (v1)

- **Images not extracted** — background photos, illustrations become placeholders in archetypes. Use `--picture` separately after generation.
- **Figma components not resolved** — we see expanded instances, not component masters.
- **Animations not extracted** — Figma does not store slide transitions. Defaults from preset are used.
- **One file = one preset** — cannot merge slides from multiple Figma files into one preset.

**`--polish=N [dir]`**: Iterative design improvement cycle. Runs N rounds (default 3, max 5) of score → redesign weak slides → re-score. Includes A/B testing for weak slides and content review. Follow the Polish Procedure in `references/polish-procedure.md`. Stop here — do not proceed to generation.

**`--compare <dir1> <dir2>`**: Compare two presentations side-by-side with scoring. Follow the Compare Procedure in `references/compare-procedure.md`. Stop here — do not proceed to generation.

**`--notes [dir]`**: Generate speaker notes for slides that don't have them. Follow the Notes Procedure in `references/notes-procedure.md`. Stop here — do not proceed to generation.

**`--responsive [dir]`**: Check presentation rendering at 4:3 aspect ratio. Follow the Responsive Check in `references/responsive-check.md`. Stop here — do not proceed to generation.

**`--dev [dir]`**: Launch the Slidev dev server for an existing presentation.

1. **Resolve project directory**:
   - If `dir` is provided, use it directly
   - Otherwise, auto-detect: look for `slides.md` in the current working directory. If not found, look for subdirectories containing `slides.md` (one level deep). If multiple found, list them and ask the user to pick.
   - If no Slidev project found, emit error: `No Slidev project found. Run /slidev <outline> to create one.`
2. **Install dependencies** if `node_modules/` doesn't exist: run `npm install` in the project directory
3. **Start dev server**: run in the background using this exact pattern to keep the process alive (slidev reads stdin for keyboard shortcuts and exits on EOF):
   ```bash
   cd <project-dir> && (sleep infinity | npx slidev) 2>&1
   ```
   Run this via Bash with `run_in_background: true`.
4. **Wait for ready**: use the Read tool to read the background task's output file and check for the URL
5. **Report**: print the local URL (e.g. `http://localhost:3030/`) once the server is ready. Note: the server continues running in the background.

Stop here — do not proceed to generation.

**`--export <format> [dir]`**: Export the presentation to various formats.

Formats:
- `html` — Build as a static SPA (hostable HTML)
- `pdf` — Export as PDF (Chromium print mode — may lose `filter:blur`, `backdrop-filter`, overlay gradients)
- `png2pdf` — Export as PDF via PNG screenshots (pixel-perfect, recommended for presentations with CSS effects)
- `pngs` — Export all slides as individual PNG images
- `png_N` — Export a single slide N as PNG (e.g. `png_3` for slide 3)

Procedure:

1. **Resolve project directory** (same rules as `--dev`): use `dir` if provided, otherwise auto-detect.
2. **Install dependencies** if `node_modules/` doesn't exist: run `npm install` in the project directory.
3. **Ensure playwright-chromium** is installed (required for pdf/png exports):
   - For `pdf`, `png2pdf`, `pngs`, or `png_N` formats: run `npx playwright install chromium` if not already available.
4. **Run export command** based on format:
   - `html`: `cd <dir> && npx slidev build --base /` — output goes to `<dir>/dist/`
   - `pdf`: `cd <dir> && npx slidev export --output slides.pdf` — output is `<dir>/slides.pdf`
   - `png2pdf`: Pixel-perfect PDF via PNG screenshots. Procedure:
     1. Export PNGs: `cd <dir> && npx slidev export --format png --output slides-tmp`
     2. Ensure Python `Pillow` is available: `pip install Pillow` (skip if already installed)
     3. Combine PNGs into PDF using this Python script:
        ```python
        from PIL import Image
        import os, re

        png_dir = 'slides-tmp'
        files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
        files.sort(key=lambda x: int(re.match(r'(\d+)', x).group()))

        images = []
        for f in files:
            images.append(Image.open(os.path.join(png_dir, f)).convert('RGB'))

        images[0].save(
            'slides.pdf',
            save_all=True,
            append_images=images[1:],
            resolution=150.0,
            quality=95
        )

        for img in images:
            img.close()
        ```
     4. Clean up: `rm -rf <dir>/slides-tmp`
     5. Output is `<dir>/slides.pdf`
   - `pngs`: `cd <dir> && npx slidev export --format png --output slides` — output is `<dir>/slides/` directory with numbered PNGs
   - `png_N`: `cd <dir> && npx slidev export --format png --range N --output slide-N` — output is single PNG for slide N
5. **Report**: print the output file/directory path and format.

**`--edit [dir] <comment>`**: Edit an existing Slidev presentation based on a free-text comment.

The comment describes what to change — content, styling, structure, animations, composition, or any combination. Examples:
- `"сделай тёмную тему"` — switch color scheme to dark
- `"добавь слайд после 3-го про статистику"` — insert a new slide
- `"убери все анимации"` — remove v-clicks and transitions
- `"увеличь шрифт заголовков"` — adjust typography
- `"замени палитру на синюю"` — change color scheme
- `"перепиши слайд 5 более кратко"` — rewrite specific slide content
- `"добавь заметки для спикера"` — add presenter notes
- `"смени слайд 5 на bento-grid"` — change slide composition archetype
- `"сделай круглые иконки вместо прямоугольных"` — change shape vocabulary
- `"замени карточки на icon-trio"` — swap rectangular cards for circle icon containers

Procedure:

1. **Resolve project directory** (same rules as `--dev`): use `dir` if provided, otherwise auto-detect by looking for `slides.md`.
2. **Read all project files** to understand the current state:
   - `slides.md` (required — the main presentation)
   - `styles/index.css` (if exists)
   - `uno.config.ts` (if exists)
   - All files in `components/` (if directory exists)
   - `package.json` (if exists)
   - `.slidev-presets/*.preset.md` or `~/.claude/slidev-presets/*.preset.md` (if the presentation was generated with a preset — check headmatter or project directory for clues)
   - `references/composition-archetypes.md` (always — needed for archetype-aware editing)
3. **Analyze the comment** to determine what needs to change:
   - **Content edits**: adding/removing/rewriting slides or bullet points
   - **Style edits**: colors, fonts, backgrounds, spacing, layout changes
   - **Structure edits**: reordering slides, changing layouts, splitting/merging
   - **Animation edits**: transitions, v-clicks, reveals
   - **Component edits**: adding/modifying Vue components
   - **Composition edits**: changing a slide's archetype (e.g., "switch slide 5 to bento-grid"), swapping rectangular cards for circle containers, changing shape vocabulary
   - **Font edits**: changing fonts — must respect the 2-font rule (max 2 visual identities) and font number blacklist
4. **Invoke `/frontend-design` thinking AND `references/design-principles.md`** for any visual or style-related edits. Before changing colors, fonts, layouts, backgrounds, components, or adding new slides:
   - Understand the existing aesthetic direction from the current `styles/index.css`, headmatter, and per-slide styles
   - Apply `/frontend-design` principles to ensure edits are cohesive, bold, and intentional — not generic
   - New slides must match the existing visual language (same palette, typography, spatial rhythm)
   - Style changes must be holistic: don't just swap a color — reconsider contrast, accent hierarchy, background treatment, and typography pairing as a system
   - Even for content-only edits, consider whether layout choice and spacing deserve `/frontend-design`-level attention (e.g., a new slide with a single stat deserves `fact` layout with dramatic styling, not a plain `default`)
   - Apply ALL Design Principles: new slides must maintain visual rhythm (Principle 1), not repeat the layout of adjacent slides (Principle 2), use the Icon component instead of emoji (Principle 4), and match the presentation's accent hierarchy (Principle 12)
   - **Archetype awareness**: When adding new slides, classify their content type and select an appropriate archetype from `references/composition-archetypes.md`. Check the archetypes of neighboring slides — the new slide's archetype must differ from its immediate neighbors (entropy rule). Use the archetype's HTML skeleton and fill `{{SLOT}}` markers with content.
   - **Shape vocabulary**: If the presentation uses a preset with a `shapes` section (check `.slidev-presets/`), new elements must match the existing shape vocabulary. If the presentation uses circle icon containers, new slides must too. If it uses pill badges, keep that consistent.
   - **Font discipline**: When changing fonts, enforce the 2-font rule — max 2 visual font identities (heading + body). Check the font number blacklist for number-heavy slides. Never introduce a 3rd font.
   - **Word count**: After editing, recount words on modified slides. If >40 (>60 for tables) — warn and suggest splitting or moving content to speaker notes.
   - **Action titles**: If editing a slide title, ensure it's a statement/insight, not a label. Check against generic phrase blacklist.
   - **Source citations**: If adding a statistic, include source citation.
   - **Emphasis check**: Don't over-bold edited content — max 10-15% of text bold.
5. **Apply changes surgically** using the Edit tool:
   - Only modify files and sections that the comment requires
   - Preserve everything the comment doesn't mention
   - Maintain consistency: if changing accent color in `styles/index.css`, also update it in per-slide `<style>` blocks and headmatter if referenced there
   - When adding slides: maintain the `---` separator convention, classify the new slide's content type, select an archetype from `references/composition-archetypes.md` that differs from neighboring slides, and use the archetype's HTML skeleton with `layout: none`
   - When changing composition (user asks to change an archetype): look up the requested archetype in `references/composition-archetypes.md`, replace the slide's HTML with the new archetype's skeleton, preserve content but reflow it into the new structure
   - When changing design (colors, fonts, backgrounds), update all relevant locations: CSS variables, headmatter fonts, per-slide styles. Respect shape vocabulary from preset.
   - When editing content: verify word count ≤40, font size ≥1.25rem for body, ≥2.2rem for headings
   - When changing images: verify visual style consistency with existing images (same color temperature, contrast)
   - When editing layout: verify whitespace ≥30%, padding ≥44px, gap ≥16px
5. **Verify consistency** after edits:
   - Slide count matches intent (unchanged unless comment asks to add/remove)
   - No broken references (e.g., deleted component still used in slides)
   - CSS variables are consistent between `styles/index.css` and inline usage
   - Headmatter and CSS don't contradict each other
6. **Visual QA** — Run the Visual QA Loop for the project directory.
7. **Report** what was changed:
   - List each file modified and a brief summary of changes
   - If slides were added/removed, show the new slide count
   - Include Visual QA results
   - Remind how to preview: `cd <dir> && npm run dev` or `/slidev --dev <dir>`

Key principles:
- **Minimal diff**: Change only what's needed. Don't rewrite `slides.md` from scratch when only one slide needs editing.
- **Preserve design intent**: If the presentation uses a preset style, respect its aesthetic when making changes. Don't introduce clashing visual elements.
- **Cascade awareness**: A color change in CSS variables should be the only edit needed if the slides reference variables correctly. But if per-slide `<style>` blocks use hardcoded colors, update those too.
- **Content fidelity**: When rewriting content, maintain the same level of detail and tone unless the comment explicitly asks for a different approach.

Stop here — do not proceed to generation.

**`--picture [source] [dir]`**: Add images to an existing Slidev presentation.

Syntax:
```
/slidev --picture auto [dir]                    Standalone: auto-search images
/slidev --picture <path1> [path2...] [dir]      Standalone: user-provided images
/slidev --preset X --picture auto <outline>     Modifier on generation
/slidev --edit --picture auto <dir> "<comment>" Modifier on edit
```

#### Picture Placement Procedure

**P-1: Read slides.md** — parse all slides: number, layout, title, content.

**P-2: Select candidate slides** — which slides should get images:
- Always: `cover`, `section`, `image-left`, `image-right`, `image` layouts
- Consider: content slides describing concrete visual subjects
- Skip: `fact`, `statement`, `end` layouts; code-heavy slides; slides already with images

**P-3: Acquire images**

*Auto mode:*
- For each candidate slide: derive search query from title + key content words
- Search via `mcp__brave-search__brave_web_search` (query + "high quality photo")
- Download to `<dir>/public/images/slide-N-keyword.jpg` via `curl -L -o`
- Verify file is non-empty; skip slide on failure

*User-provided mode:*
- Copy files to `<dir>/public/images/` (or reference if already in `public/`)
- Distribute across candidate slides in order
- Fewer images than candidates → remaining slides unchanged
- Fewer candidates than images → extras unused, noted in report

After acquiring all images, verify visual style consistency across the set. All images should share similar color temperature, contrast level, and compositional style. If images vary significantly, apply a CSS harmonization filter on all image elements: `filter: saturate(0.85) contrast(1.05)` to unify the look. Do not mix photographic images with illustrations or AI-generated imagery.

**P-4: Update slides.md** — for each slide that got an image:
- `cover`/`section` → set background via **per-slide `<style>` CSS** (NOT frontmatter `background:` prop, which gets blocked by theme's opaque `background-color`). Use: `background: url('/images/slide-N-keyword.jpg') center/cover no-repeat !important;` on `.slidev-layout`.
- `default` (text-heavy) → change layout to `image-right`, add `image:` prop
- `image-left`/`image-right`/`image` → update `image:` prop
- For any slide with background image: add dark overlay via `::before`, set ALL text elements to `text-align: center` explicitly, set text colors to white/near-white. See `references/layout-css-patterns.md` for exact CSS patterns.

**P-5: Add CSS overlay** (if background images on cover/section):
In `styles/index.css`, add overlay support. But **each per-slide `<style>` must also**:
1. Set `background: url(...) center/cover no-repeat !important` on `.slidev-layout` (overrides theme's background-color)
2. Set `text-align: center` explicitly on `h1`, `p`, and other text elements (overrides theme's text-align)
3. Set text colors to white/near-white for readability against dark overlay
4. **CRITICAL — Use gradient overlay, not uniform opacity**, especially on cover/statement slides with multiple text elements at different vertical positions. Uniform overlays fail on high-contrast photos (bright spots bleed through). Use: `background: linear-gradient(to bottom, rgba(bg, 0.92) 0%, rgba(bg, 0.80) 60%, rgba(bg, 0.70) 100%)` — stronger where text is densest (usually top/center), lighter at edges where the image can show through.
5. **Minimum overlay opacity**: 0.85 in any zone where text appears. After adding images, verify that the SMALLEST text on the slide (subtitles, dates, attributions) is fully legible.

```css
/* styles/index.css — background image overlay support */
.slidev-layout.cover, .slidev-layout.section { position: relative; }
.slidev-layout.cover::before, .slidev-layout.section::before {
  content: ''; position: absolute; inset: 0;
  /* Gradient overlay — stronger where text lives (top/center), lighter at bottom */
  background: linear-gradient(to bottom, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.75) 70%, rgba(0,0,0,0.65) 100%);
  z-index: 0; pointer-events: none;
}
.slidev-layout.cover > *, .slidev-layout.section > * { position: relative; z-index: 1; }
```

**P-6: Run Visual QA Loop** — always triggered after picture placement.

**P-7: Report** — which slides got images, sources, skipped slides and why.

Stop here — do not proceed to generation.

**`--learn=N`**: Enhanced learning loop. First runs deep_learn to create/refine a preset, then runs N cycles of generate → export → research-grade critique → improve.

**Maximum N**: 10. If N > 10, cap at 10 and notify the user.

### Learning Loop Procedure

**L-1: Create education folder** — Scan for existing `edu_*` directories in the working directory. Create the next sequential one (e.g., `edu_01`, `edu_02`). All iterations for this learning run go inside this folder.

**L-2: Generate N diverse outlines** — Create all outlines upfront to ensure diversity. Save each as `<edu_dir>/learn_<i>/outline.md`. **All outlines MUST be written in Russian** (titles, slide names, bullet points — everything in Russian). Outlines must vary across:
- **Industries**: tech startup, education, healthcare, finance, creative agency, nonprofit, SaaS, retail, AI/ML, sustainability
- **Formats**: pitch deck, educational lecture, product launch, quarterly report, team onboarding, keynote talk, investor update, workshop
- **Sizes**: mix of 8-10 slides (short), 12-14 (medium), 15-16 (long)
- **Tone**: formal, casual, inspirational, data-heavy, storytelling, technical

Each outline follows the standard outline format:
```markdown
# Presentation Title
## Slide 1: Title
- Point 1
- Point 2
## Slide 2: Another Title
- Content here
```

**L-3: Learning iteration loop** — For i = 1 to N:

**L-3-pdl: Run PDL (Deep Learn) for this iteration** — Each cycle starts with a fresh PDL run using the CURRENT (possibly improved) skill rules:
- If i == 1 and no `--preset`: **auto-create preset WITHOUT asking questions.** Analyze the outlines from L-2. Based on outline content, autonomously decide: mood (infer from topic), color scheme (light/dark), accent color (safe palette — never purple), typography (sans+sans pair from Good pairs table), density, textures, archetypes, transitions. Save as `learn-auto-<timestamp>.preset.md`. Do NOT ask any questions.
- If i == 1 and `--preset <name>` was provided: use that preset as starting point.
- If i > 1: re-run PDL on the preset from the previous iteration, using the UPDATED SKILL.md rules (improvements from prior cycles feed back into PDL).
- PDL runs with N=3 internal cycles (auto-critique of the preset itself).
- Save the refined preset for this iteration as `<edu_dir>/learn_<i>/preset-cycle-<i>.preset.md`.

**L-3a: Create presentation** — Launch a subagent (Agent tool) to run the full `/slidev` generation pipeline for `<edu_dir>/learn_<i>/outline.md`. The subagent:
- Reads the current SKILL.md (to pick up any improvements from prior iterations)
- Uses the outline from `<edu_dir>/learn_<i>/outline.md`
- Outputs the project to `<edu_dir>/learn_<i>/`
- Runs the full generation procedure (Steps 1-7) including Visual QA
- **Uses the preset from L-3-pdl** (this iteration's PDL output) — each cycle gets a progressively better preset

**L-3b: Export** — After creation, export the presentation:
```bash
cd <edu_dir>/learn_<i> && npm install && npx playwright install chromium
npx slidev export --format png --output slides
npx slidev export --output slides.pdf
```
If export fails (missing deps, rendering errors), log the error in `<edu_dir>/learn_<i>/critique.md` and skip to L-3f with a note about the export failure. Do NOT abort the entire learning loop.

**L-3c: Critic agent** — Launch a subagent (Agent tool) as a **demanding design critic**. Provide it with:

Critic agent prompt:
```
You are a demanding presentation design critic. Your job is to analyze a Slidev presentation and find every design flaw, comparing against professional Gamma-quality standards.

INPUTS:
- Presentation slides: <edu_dir>/learn_<i>/slides.md
- Exported slide images: <edu_dir>/learn_<i>/slides/*.png (read ALL of them visually)
- Current skill rules: .claude/skills/slidev/SKILL.md
- Design principles: .claude/skills/slidev/references/design-principles.md
- Scoring Subroutine: .claude/skills/slidev/references/scoring-subroutine.md
- Content Review Subroutine: .claude/skills/slidev/references/content-review-subroutine.md
- **RESEARCH CORPUS (read BEFORE scoring):**
  - docs/research/ai-presentation-detection-guide-ru.md — 50-point AI detection rubric, 6 signatures of AI slides, fix playbook
  - docs/research/ugly-presentations-anti-patterns-ru.md — 170+ anti-patterns with severity ratings (CRITICAL/MAJOR/MINOR)
  - docs/research/beautiful-presentations-guide-ru.md — industry standards from Reynolds, Duarte, Tufte, McKinsey, TED, Apple, YC

ANALYSIS PROCESS:
1. Read ALL research documents FIRST — internalize the full detection rubric, anti-pattern checklist, and industry standards
2. Read slides.md — check compliance with ALL Slide Authoring Rules and Design Quality Rules
3. Read EVERY exported PNG — apply the full QA-4 visual checklist + QA-8 critic checklist
4. **Apply the 50-point AI Detection Rubric** from the research — score the presentation on all 8 categories (color, typography, layout, visual effects, imagery, content structure, content quality, metadata). If total > 16 → flag as "still looks AI-generated"
5. **Apply the Anti-Pattern Bible** — check every CRITICAL and MAJOR anti-pattern from the research. Each violation = a systemic issue
6. Cross-reference: do the rules in SKILL.md and design-principles.md actually produce good results? Are there gaps?
7. Look for SYSTEMIC issues — patterns that appear across multiple slides, not just one-off problems
8. Run the Scoring Subroutine — score each slide on 9 axes
9. Run the Content Review Subroutine — check 3-second test, narrative flow, redundancy, CTA clarity, information hierarchy
10. Check for anti-patterns from industry research:
   - Generic label titles instead of action titles (Ghost Deck test: do titles tell a story?)
   - Purple/indigo as primary palette (AI color blacklist)
   - Three-column icon grid repeated >1 time
   - All-caps eyebrow labels on every slide (max 30%)
   - "Thank You" ending instead of CTA
   - Recommendation buried after slide 5
   - Body text centered on multi-line content
   - Font sizes below 1.25rem for body, below 2.2rem for headings
   - >40 words on a content slide
   - Bold on >15% of text
   - Bar charts not starting at zero
   - Statistics without source citations
   - Sub-bullets deeper than 2 levels

OUTPUT FORMAT — write to <edu_dir>/learn_<i>/critique.md:

# Critique: [Presentation Title] (Learn Iteration <i>)

## Overall Score: X/10

## Systemic Issues (affect the skill itself)

### Issue 1: [Title]
- **Severity**: critical | major | minor
- **Category**: rhythm | layout | typography | icons | cards | decoration | arc | data-viz | mockups | diagrams | spacing | accent | rendering | content | structure
- **Frequency**: How many slides affected
- **Description**: What's wrong
- **Evidence**: What was observed in specific PNGs and/or MD structure
- **Root cause**: Why the current skill rules allowed this to happen
- **Proposed skill fix**: Specific change to SKILL.md or design-principles.md — be precise about WHAT to add/change and WHERE

## Slide-Specific Issues (one-off problems in this presentation)

### Slide N: [issue]
- **Description**: ...
- **Severity**: ...

## What Worked Well
- List things the skill got right — these rules should be preserved

## Design Summary
- **Palette type**: dark | light | mixed
- **Palette mood**: [short description, e.g., "warm gold on deep navy"]
- **Font character**: serif-heavy | geometric-sans | humanist | monospace-accent
- **Decoration style**: geometric | organic | linear | pattern | minimal
- **Strongest axis**: [which scoring axis scored highest on average]
- **Weakest axis**: [which scoring axis scored lowest on average]
```

**L-3c1.5: Персональный research по каждому слайду** — Для КАЖДОГО слайда в презентации:

1. **Сформулировать 5-10 вопросов к слайду**. Примеры:
   - "Правильно ли подобран шрифт для заголовка на этом слайде?"
   - "Соответствует ли цветовой контраст между текстом и фоном стандартам WCAG?"
   - "Является ли этот layout оптимальным для данного типа контента?"
   - "Не выглядит ли этот слайд как AI-сгенерированный? По каким признакам?"
   - "Достаточно ли визуальной иерархии — что первым бросается в глаза?"
   - "Уместна ли плотность контента для презентационного формата?"
   - "Работает ли декоративный элемент или он отвлекает?"
   - "Соблюдено ли правило третей в композиции?"
   Вопросы должны быть КОНКРЕТНЫМИ для данного слайда, а не общими.

2. **Research по качественным источникам** — для каждого вопроса искать ответ:
   - **Приоритет 1**: Наши docs/research/ (ai-presentation-detection-guide, beautiful-presentations-guide, ugly-presentations-anti-patterns) — СНАЧАЛА ищем тут
   - **Приоритет 2**: Авторитетные источники в интернете (WebSearch):
     - Дизайн: `site:smashingmagazine.com`, `site:nngroup.com`, `site:uxdesign.cc`, `site:medium.com/tag/design`
     - Типографика: `site:practicaltypography.com`, `site:typewolf.com`
     - Презентации: `site:duarte.com`, `site:garr.com` (Garr Reynolds), `site:ted.com`
     - Data viz: `site:storytellingwithdata.com`, `site:tableau.com/blog`
   - **НЕ использовать**: случайные блоги, SEO-контент, сайты-генераторы
   - На каждый вопрос — 1-2 авторитетных источника

3. **Оценить слайд на основе research** — для каждого слайда написать вердикт:
   ```
   Слайд N: [тема]
   Вопросы и находки:
     Q1: [вопрос]
     A1: [ответ из research] — источник: [ссылка/документ]
     Вердикт: ✓ соответствует / ✗ нарушает [что именно]

     Q2: [вопрос]
     A2: [ответ] — источник: [ссылка]
     Вердикт: ...

   Итог слайда: X/10, ключевые недочёты: [список]
   ```

4. **Сохранить ценные находки** — если research выявил полезное правило или insight, которого НЕТ в наших docs/research/:
   - Создать/дополнить `docs/research/learn-discoveries.md`:
   ```markdown
   ## Находка: [тема]
   - **Источник**: [URL или документ]
   - **Суть**: [1-2 предложения]
   - **Применимость**: [к каким слайдам/ситуациям]
   - **Дата**: YYYY-MM-DD
   - **Обнаружено в**: edu_XX/learn_<i>, слайд N
   ```
   - Только ДЕЙСТВИТЕЛЬНО полезные находки (не общие истины)
   - Максимум 3-5 находок за итерацию

5. **Записать полный research-отчёт** в `<edu_dir>/learn_<i>/slide-research.md`

Этот research ИНФОРМИРУЕТ дальнейшую критику — critique.md (L-3c) должен учитывать все найденные несоответствия.

**L-3c2: ПРОМЕЖУТОЧНЫЙ ОТЧЁТ — Результаты критики** — Напечатать пользователю СРАЗУ после завершения критики:
```
━━━ Итерация обучения <i>/<N> — ОТЧЁТ КРИТИКА ━━━

Оценка: X/10
AI-детекция: XX/50 (>16 = всё ещё выглядит как AI)

Найдено КРИТИЧЕСКИХ проблем: [кол-во]
  - [название проблемы 1] — затронуто [кол-во] слайдов
  - [название проблемы 2] — ...

Найдено СЕРЬЁЗНЫХ проблем: [кол-во]
  - [название проблемы 1] — затронуто [кол-во] слайдов
  - ...

Что сработало хорошо:
  + [пункт 1]
  + [пункт 2]

Полный отчёт: <edu_dir>/learn_<i>/critique.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Дождаться, пока пользователь прочитает, прежде чем переходить к исправлениям.

**L-3c3: A/B on weakest slides** — After critique, if any slide scores < 6, run the A/B Testing Subroutine (`references/ab-testing.md`) on the 2 weakest slides. Include the variant comparison in `critique.md` under a "## A/B Alternatives" section showing what could have been done differently. This provides concrete before/after examples for the improvement spec.

**L-3c4: Фаза исследования и продумывания** — Для каждой КРИТИЧЕСКОЙ и СЕРЬЁЗНОЙ проблемы из critique.md запустить многоступенчатый анализ:

1. **Декомпозиция проблемы** — разбить на корневую причину и последствия. Спросить "почему?" 3 раза (метод 5 Why). Пример: "текст не помещается" → "потому что font-size слишком большой" → "потому что правило не учитывает плотность контента" → корень: "нет связи между количеством контента и допустимым font-size"

2. **Поиск решений в research** — перечитать соответствующие секции из docs/research/:
   - Если проблема с типографикой → beautiful-presentations-guide секции 2-3
   - Если проблема с layout → ugly-presentations-anti-patterns секции 6-7
   - Если проблема с AI-похожестью → ai-presentation-detection-guide часть 5 (Fix Playbook)
   - Если не нашёл → запустить веб-поиск (WebSearch) по запросу "presentation design [проблема] best practice"

3. **Веб-поиск** (опционально, для сложных проблем) — если research-документы не содержат решения:
   - Искать: "[проблема] presentation design solution site:medium.com OR site:uxdesign.cc OR site:smashingmagazine.com"
   - Искать: "slidev [проблема] fix" для Slidev-специфичных багов
   - Сохранить найденное в `<edu_dir>/learn_<i>/research-notes.md`

4. **Генерация 2-3 вариантов решения** — для каждой проблемы предложить минимум 2 подхода с trade-offs. Выбрать лучший на основе:
   - Минимальность изменений (YAGNI)
   - Совместимость с другими правилами
   - Подтверждение из research

5. **Записать план исправлений** в `<edu_dir>/learn_<i>/fix-plan.md`:
```markdown
# План исправлений — Итерация <i>

## Проблема 1: [название]
### Корневая причина (5 Why)
1. [почему 1]
2. [почему 2]
3. [корень]

### Источник решения
- [research документ] секция [X] / [URL из веб-поиска]

### Варианты
A) [описание] — плюсы: ... минусы: ...
B) [описание] — плюсы: ... минусы: ...

### Выбранный вариант: [A/B] — причина: [...]

### Конкретные правки
- Файл: [путь]
- Секция: [название]
- Было: "[фрагмент]"
- Стало: "[новый текст]"
```

**L-3d: Generate improvement spec** — На основе fix-plan.md (а не напрямую из critique.md), создать `<edu_dir>/learn_<i>/improvements.md`:

```markdown
# Improvements from Learn Iteration <i>

## Applied Changes (critical + major systemic issues only)

### Change 1: [Title]
- **File**: SKILL.md | references/design-principles.md
- **Section**: [exact section name]
- **Type**: add_rule | modify_rule | add_example | expand_checklist
- **Description**: What to change and why
- **Before**: [relevant excerpt or "N/A" for new additions]
- **After**: [exact text to write]

## Deferred (minor issues — logged for review)
- [minor issue 1]
- [minor issue 2]
```

**L-3e: Apply improvements via script** — Read the improvements.md and generate a Python script to apply changes:

1. Create `<edu_dir>/learn_<i>/apply-fixes.py` with all changes as string replacements:
```python
#!/usr/bin/env python3
"""Auto-generated fix script for learn iteration <i>"""
import pathlib, sys

def apply(path, old, new, description):
    p = pathlib.Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        print(f"  SKIP: '{description}' — old text not found in {path}")
        return False
    text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')
    print(f"  OK: {description}")
    return True

changes = 0
total = 0

# --- Change 1: [description] ---
total += 1
if apply(
    ".claude/skills/slidev/SKILL.md",
    """old text fragment here""",
    """new text fragment here""",
    "Change 1: [description]"
): changes += 1

# --- Change 2: [description] ---
# ... repeat for each change ...

print(f"\nApplied {changes}/{total} changes")
if changes < total:
    print("Some changes were skipped — check output above")
    sys.exit(1)
```

2. Only include changes marked as critical or major severity
3. Before generating each replacement, verify the old text doesn't contradict an existing rule
4. Run the script:
```bash
cd <project_root> && python3 <edu_dir>/learn_<i>/apply-fixes.py
```
5. If script exits with error (some changes skipped) — log in improvements.md and continue
6. Delete the script after successful execution: `rm <edu_dir>/learn_<i>/apply-fixes.py`

**L-3e2: ПРОМЕЖУТОЧНЫЙ ОТЧЁТ — Применённые исправления** — Напечатать пользователю СРАЗУ после применения исправлений:
```
━━━ Итерация обучения <i>/<N> — ИСПРАВЛЕНИЯ ━━━

Применено изменений: [кол-во]
  1. [название] → [файл]:[секция]
     Было: "[фрагмент]"
     Стало: "[новый текст]"
  2. ...

Отложено незначительных: [кол-во]
  - [проблема] — причина: [почему отложено]

Подробности: <edu_dir>/learn_<i>/improvements.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After applying improvements, write the iteration's design pattern to Design Memory using the overall score from `critique.md`. Follow the Write Protocol in `references/design-memory.md`. Only write if score >= 8 (type "high") or score < 6 (type "low"). Skip write for scores 6-8 (not distinctive enough to learn from).

**L-3f: Git commit с тегом** — Commit после КАЖДОГО цикла. Тег позволяет откатиться к любому циклу:

```bash
# Stage presentation artifacts
git add -f <edu_dir>/learn_<i>/outline.md
git add -f <edu_dir>/learn_<i>/slides.md
git add -f <edu_dir>/learn_<i>/slides/*.png
git add -f <edu_dir>/learn_<i>/slides.pdf
git add -f <edu_dir>/learn_<i>/critique.md
git add -f <edu_dir>/learn_<i>/improvements.md
git add -f <edu_dir>/learn_<i>/fix-plan.md
git add -f <edu_dir>/learn_<i>/preset-cycle-<i>.preset.md
git add -f <edu_dir>/progress.md

# Stage skill changes
git add -f .claude/skills/slidev/SKILL.md
git add -f .claude/skills/slidev/references/design-principles.md
git add -f .claude/skills/slidev/references/scoring-subroutine.md

# Commit with score in message
git commit -m "learn(<i>/<N>): [topic] — score X/10 — [summary]"

# Tag for rollback
git tag "learn-cycle-<i>-score-X"
```

**Do NOT stage**: `node_modules/`, `package.json`, `uno.config.ts`, `styles/`, `components/`, `dist/`, `slides-qa/`.

**L-3g: Обновить сводную таблицу** — После каждого цикла обновлять `<edu_dir>/progress.md` (создать при первом цикле, дополнять при последующих):

```markdown
# Прогресс обучения

| Цикл | Тема | Оценка | AI-детекция | Лучший? | Git тег | PDF |
|------|------|--------|-------------|---------|---------|-----|
| 1 | [тема] | 5.0/10 | 28/50 | — | learn-cycle-1-score-5 | edu_XX/learn_1/slides.pdf |
| 2 | [тема] | 6.4/10 | 18/50 | ✓ лучший | learn-cycle-2-score-6 | edu_XX/learn_2/slides.pdf |
| 3 | [тема] | 5.8/10 | 22/50 | ✗ регрессия | learn-cycle-3-score-5 | edu_XX/learn_3/slides.pdf |

## Лучший цикл: 2 (6.4/10)
Откат к лучшему: `git checkout learn-cycle-2-score-6 -- .claude/skills/slidev/`

## Ключевые изменения по циклам
- Цикл 1 → 2: +1.4 (декор inline HTML, structural break rule)
- Цикл 2 → 3: -0.6 (регрессия — [причина])

## Как откатиться
1. Посмотри PDF лучшего цикла: откройте файл из колонки PDF
2. Если устраивает: `git checkout learn-cycle-<N>-score-<X> -- .claude/skills/slidev/`
3. Это вернёт SKILL.md и references к состоянию того цикла
```

Колонка "Лучший?" — сравнение текущей оценки с максимальной из предыдущих. progress.md коммитится ВМЕСТЕ с основным коммитом цикла (в L-3f).

**L-4: Summary** — After all N iterations, create `<edu_dir>/summary.md`:

```markdown
# Learning Run Summary: edu_XX

## Overview
- **Iterations**: N
- **Date**: YYYY-MM-DD
- **Starting skill version**: [git hash before learning]
- **Final skill version**: [git hash after learning]

## Iterations

### Learn 1: [Topic]
- Score: X/10
- Key findings: ...
- Changes applied: ...

### Learn 2: [Topic]
...

## Cumulative Skill Changes
[Diff summary of all changes made to SKILL.md and design-principles.md across all iterations]

## Deferred Issues (minor — need human review)
- [all minor issues from all iterations]

## Recommendations
- [patterns observed across iterations]
- [suggested areas for manual improvement]

## Score Progression
```
Learn 1: ██████░░░░ 5.8  (topic, palette mood from Design Summary)
Learn 2: ████████░░ 7.5  (topic, palette mood)
...
```

## Patterns Observed
Synthesize across all critique.md Design Summary blocks:
- [pattern 1 with delta, e.g., "Dark themes score +1.2 avg on decoration visibility"]
- [pattern 2 with delta]
```

Commit the summary:
```bash
git add <edu_dir>/summary.md
git commit -m "learn(summary): edu_XX — N iterations completed, [total changes] improvements applied"
```

**L-5: Report** — Print to the user:
```
━━━ Обучение завершено: edu_XX ━━━

  Итераций: N
  Темы: [список тем]
  Улучшений скилла: [кол-во] изменений применено
  Отложено: [кол-во] незначительных для ревью

  Прогресс оценок:
  | Цикл | Оценка | AI-детекция | Статус |
  |------|--------|-------------|--------|
  | 1    | X/10   | XX/50       | —      |
  | 2    | X/10   | XX/50       | ✓/✗    |
  | 3    | X/10   | XX/50       | ✓/✗    |

  Лучший цикл: [N] (X/10)
  PDF лучшего: <edu_dir>/learn_<N>/slides.pdf

  Если текущее состояние хуже лучшего цикла:
    git checkout learn-cycle-<N>-score-<X> -- .claude/skills/slidev/

  Сводная таблица: <edu_dir>/progress.md
  Все итерации: <edu_dir>/learn_<i>/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Stop here — do not proceed to generation.

### Preset Learning Procedure

Triggered by `--learn=N --preset <name>` or `--learn=N` (with preset specified). Creates/refines a preset through N visual test runs with user-confirmed improvements.

**PL-1: Initialization**
- If `--preset <name>` specified: generate an initial `.preset.md` from the name — infer mood, colors, fonts, CSS from the name/description. Save to `.slidev-presets/<name>.preset.md`.
- If `--preset` not specified: run the interactive wizard (8 questions, same as `--create-preset`) to create the initial preset.
- Create working directory: `preset-learn-<name>/`
- Scaffold the Slidev project once inside the working directory:
  - Write `package.json` with standard Slidev deps (`@slidev/cli: latest`, `@slidev/theme-default: latest`)
  - Run `npm install`
  - Run `npx playwright install chromium`
  - This scaffolding is reused for ALL N runs — only `slides.md` and `styles/index.css` change between runs.

**PL-2: Generate demo presentations**
- Generate N diverse outlines (ALL in Russian). Vary across industries, formats, sizes (8-16 slides), and tones. Use `assets/demo-outline.md` as structural reference.
- For each outline i = 1 to N:
  1. Write `slides.md` by running the full generation procedure (Steps 1-8) using the current preset in Preset mode. Output to `preset-learn-<name>/run-<i>/`.
  2. Apply the current preset's CSS to `styles/index.css`.
  3. Export PNGs: `cd preset-learn-<name> && npx slidev export --format png --output run-<i>/slides`
  4. **Optimization**: Reuse the scaffolded `node_modules/` — do NOT run `npm install` for every run. Run all generations in the same scaffolded directory, moving `slides.md` and `styles/index.css` between runs, and copying exported PNGs to `run-<i>/slides/`.

**PL-3: Visual critic**
- Launch a subagent (Agent tool) as a **demanding visual design critic** for presets. Provide:
  - All exported PNGs from all N runs (read ALL visually)
  - The current `.preset.md` file content
  - `references/scoring-subroutine.md` — apply the 9-axis scoring (1-10 scale): composition variety, shape diversity, font discipline, visual impact, layout uniqueness, typography drama, color conviction, content clarity, decorative quality
  - `references/design-principles.md` — check compliance

- Critic output — write to `preset-learn-<name>/critic-report.md`:

```
# Preset Critic Report: <name>

## Overall Score: X/10

## Scoring Per Run
- Run 1 ([topic]): X/10 — [strongest axis], [weakest axis]
- Run 2 ([topic]): X/10 — ...
...

## Systemic CSS/Style Issues

### Issue 1: [Title]
- **Severity**: critical | major | minor
- **Frequency**: N/N runs affected
- **Description**: What's wrong visually
- **Evidence**: Which PNGs show the problem
- **Root cause**: Which part of .preset.md causes this
- **Proposed fix**:
  - **Before**: [relevant excerpt from .preset.md]
  - **After**: [proposed replacement text]

## What Works Well
- [list CSS patterns, font choices, color decisions that scored well]
```

**PL-4: Propose changes**
- Read the critic report. Present a numbered list of proposed changes to the user:
```
Предлагаемые изменения для пресета '<name>':
1. [description] — Severity: critical
   Было: "<excerpt>"
   Стало: "<proposed text>"
2. [description] — Severity: major
   ...

Применить изменения? (да / нет / выбрать)
```
- `да` — apply all
- `нет` — discard all
- `выбрать` — user picks by number

**PL-5: Apply**
- For each approved change: read `.preset.md`, apply via Edit tool, verify.
- Only modify `.preset.md` (YAML frontmatter + CSS block). Do NOT change preset name.
- After saving preset changes, regenerate the `<name>-theme/` directory from the updated CSS block. Subsequent test presentations use `theme: ./theme`.

**PL-6: Report**
```
Preset learning complete: <name>

  Runs: N
  Score: X/10
  Changes applied: N
  Changes skipped: N
  Preset: .slidev-presets/<name>.preset.md
```

Stop here — do not proceed to generation.

### Preset Deep Learning Procedure

Triggered by `--deep_learn=N` (with or without `--preset <name>`). Creates/refines a preset through N cycles of automated visual critique and improvement. Also used internally by Step 0.4 (auto-preset) as an inline variant with N=3.

**PDL-1: Initialization**
- Parse N. If N < 2, error: `--deep_learn requires N >= 2 (minimum two cycles to observe improvement).` Stop.
- If `--preset <name>` specified: generate initial `.preset.md` from the name. Save to `.slidev-presets/<name>.preset.md`.
- If `--preset` not specified: run the interactive wizard (8 questions) to create the initial preset.
- If called as inline variant from Step 0.4: the initial preset is already created — skip wizard.
- Create working directory: `preset-deep-learn-<name>/`
- Snapshot the original preset: copy `.preset.md` to `preset-deep-learn-<name>/preset-snapshot-original.preset.md`
- Scaffold the Slidev project once inside the working directory:
  - Write `package.json` with standard Slidev deps
  - Run `npm install`
  - Run `npx playwright install chromium`
  - This scaffolding is reused for ALL cycles and runs.

**PDL-2: Training cycle** — **MUST execute ALL N cycles.** Do NOT skip, abbreviate, or reduce the number of cycles for any reason. Repeat for c = 1 to N:

**PDL-2.1: Generate outlines** — Generate 3 diverse outlines (ALL in Russian). Topics MUST NOT repeat across cycles. Vary: industry, scope, complexity, geography.

**PDL-2.2: Run presentations** — For each of the 3 outlines:
1. Re-read `.preset.md` from disk (it may have been modified by the previous cycle)
2. Write `slides.md` using the full generation procedure (Steps 1-8) with the current preset in Preset mode
3. Update `styles/index.css` from the current preset's CSS block
4. Export PNGs: `npx slidev export --format png --output slides`
5. Copy PNGs to `preset-deep-learn-<name>/cycle-<c>/run-<i>/slides/`
6. **Optimization**: Reuse the scaffolded `node_modules/` — only swap `slides.md` and `styles/index.css` between runs.

**PDL-2.3: Visual critic** — Launch a subagent as a demanding visual critic. Provide:
- All PNGs from the 3 runs in this cycle
- Current `.preset.md` content
- `references/scoring-subroutine.md` and `references/design-principles.md`
- **For cycle > 1**: also provide the previous cycle's critic report (`cycle-<c-1>/critic-report.md`). Instruct the critic to:
  - Check whether issues from the previous cycle were fixed
  - If an issue persists despite a fix attempt: **escalate its severity** (minor → major, major → critical)
  - If new issues appeared after fixes: flag as **REGRESSION**
- Evaluate composition archetype adequacy: was the right archetype selected for each content type? Are there slides where a different archetype would create better visual variety?
- Check archetype preferences: does the preset's `preferred` list match what actually works well? Should any archetypes be added to or removed from `preferred`/`avoid`?
- Evaluate shape vocabulary: are circle containers, pill badges, and other non-rectangular shapes being used effectively? Or does the presentation still look like "all rectangles"?
- Check for anti-patterns from industry research:
   - Generic label titles instead of action titles (Ghost Deck test: do titles tell a story?)
   - Purple/indigo as primary palette (AI color blacklist)
   - Three-column icon grid repeated >1 time
   - All-caps eyebrow labels on every slide (max 30%)
   - "Thank You" ending instead of CTA
   - Recommendation buried after slide 5
   - Body text centered on multi-line content
   - Font sizes below 1.25rem for body, below 2.2rem for headings
   - >40 words on a content slide
   - Bold on >15% of text
   - Bar charts not starting at zero
   - Statistics without source citations
   - Sub-bullets deeper than 2 levels

Critic output — write to `preset-deep-learn-<name>/cycle-<c>/critic-report.md` (same format as PL-3 critic, plus escalation/regression annotations).

**PDL-2.4: Auto-apply changes** — **CRITICAL: Changes are applied automatically without user confirmation.**
- `critical` severity: always apply
- `major` severity: always apply
- `minor` severity: auto-apply only if the fix touches a single CSS property or font value; otherwise skip and log as deferred

For each change: read `.preset.md`, apply via Edit tool, verify the edit took effect. After applying changes to the preset, regenerate the `<name>-theme/` directory from the updated CSS block. Test presentations in PDL-2.2 must use `theme: ./theme` (not `theme: default`).

Log all changes (applied and skipped) to `preset-deep-learn-<name>/cycle-<c>/changes-applied.md`:
```
# Cycle <c> Changes

## Applied
1. [description] — severity: critical
   Before: "<excerpt>"
   After: "<new text>"

## Skipped
1. [description] — severity: minor, reason: multi-property change
```

**Safety guardrails (NEVER violated):**
- Changes ONLY to `.preset.md` (CSS + YAML frontmatter + `archetypes` section + `shapes` section)
- NEVER delete the preset file
- NEVER change the preset's `name` field
- If an Edit fails (old_string not found in file): log as skipped, continue to next change

**PDL-2.5: Cycle status** — Print:
```
Цикл <c>/<N> завершён.
  Качество:    <score>/10
  Прогоны:     3/3 успешных
  Правки:      <X applied, Y skipped>
  Регрессии:   <count or "нет">
```

**PDL-3: Convergence detection (early stopping)** — After each cycle's status, check:
- If the critic's overall quality score is **9 or 10 for two consecutive cycles**: stop early.
  ```
  Раннее завершение: качество стабилизировалось на <score>/10 в циклах <c-1> и <c>.
  ```
  Skip remaining cycles, proceed to PDL-5.
- If score decreased vs. previous cycle (regression): warn but do NOT stop — the next cycle will attempt to fix it.

**PDL-4: (reserved for future use)**

**PDL-5: Final report** — Write to `preset-deep-learn-<name>/final-report.md` and print:
```
# Preset Deep Learning Report: <name>

## Summary
- Cycles executed: <actual> / <N planned>
- Early stop: yes/no (reason)
- Final score: X/10

## Score Progression
Cycle 1: ██████░░░░ 6.2
Cycle 2: ████████░░ 7.8
Cycle 3: █████████░ 9.1

## Total Changes
- Applied: N
- Skipped: N
- Regressions: N

## Preset Diff (original → final)
[Show before/after of key sections of .preset.md that changed]
```

**PDL-6: Save** — Ask the user where to save the final preset:
```
Пресет '<name>' готов. Сохранить:
1. Локально: .slidev-presets/<name>.preset.md (уже сохранён)
2. Глобально: ~/.claude/slidev-presets/<name>.preset.md

Выбор (1/2):
```
If global: copy the preset to `~/.claude/slidev-presets/` and add to registry if `~/.claude/slidev-presets.json` exists.

**Note**: When called as inline variant from Step 0.4, PDL-6 is skipped — preset stays in `.slidev-presets/` automatically.

**PDL-7: Cleanup** — Ask user: `Удалить рабочую директорию preset-deep-learn-<name>/? (да/нет)`

**Note**: When called as inline variant from Step 0.4, PDL-7 is skipped — working directory is cleaned up automatically.

Stop here — do not proceed to generation (unless called as inline variant from Step 0.4, in which case return to Step 0.4 flow).

## Visual QA Loop

A reusable subroutine for visual quality assurance. Input: `<dir>` (project directory). Called after generation, editing, preset demo creation, and picture placement.

### Phase 1: CSS Code Review (before rendering)

**QA-0: Pre-render code review** — Before exporting PNGs, read `slides.md` and check the CSS code directly. This catches structural issues that are hard to spot visually.

**QA-0a: CSS correctness checks** — For EACH slide in the file, verify:
- **Centered layouts** (`cover`, `section`, `fact`, `end`, `statement`, `center`): confirm `text-align: center` is set on `h1`, `h2` and single-line elements (subtitle, date, attribution). Confirm multi-line `p` and `li` (>60 chars or >1 line) use `text-align: left` with `max-width: 600px; margin: 0 auto` — left-aligned in centered container. If multi-line body text is centered, fix immediately.
- **Background image slides**: confirm the background is set via per-slide CSS (`background: url(...) center/cover no-repeat !important` on `.slidev-layout`), NOT via frontmatter `background:` prop. If using frontmatter prop, switch to CSS approach. Confirm `::before` overlay is present for readability. Confirm text colors are white/near-white.
- **Text-on-image contrast**: if a slide has a background image or dark background, confirm text colors are explicitly set to white/light values.
- **No reliance on CSS inheritance** for text alignment, colors, or font properties on centered layouts — all must be explicit due to Slidev theme specificity overrides.
- **layout:none enforcement (Rule 25 + Rule 46)**: Global frontmatter MAY contain `layout: none` (it sets slide 1's layout), but slide 1's HTML content MUST come immediately after the global frontmatter — no extra `---` separator creating a blank slide. Every slide with raw HTML using `position:absolute;inset:0` must have `layout: none` in its frontmatter. Every slide with `layout: none` must have a `<style>` block containing `.slidev-layout { padding: 0 !important; overflow: hidden; }`. Auto-fix: add if missing.
- **Pure #FFFFFF/#000000 scan**: Scan all inline `style="..."` for `#FFFFFF`, `#fff`, `#FFF`, `color:white`, `#000000`, `#000`, `color:black`. Exclude `rgba(255,255,255,...)` and `rgba(0,0,0,...)` (transparency OK). Auto-fix: `#FFFFFF`/`#fff` → preset's warm off-white (e.g., `var(--bg-base)` or `#FAFAF8`); `#000000`/`#000` → `var(--color-text)` or warm off-black. QA-0c retains its CRITICAL flag as defense-in-depth fallback.
- **Pill line-height:1**: Find all elements where the SAME `style` contains ALL THREE: (1) `border-radius` 16-24px, (2) `padding` with values, (3) `display:inline-flex`. Check for `line-height:1`. Auto-fix: insert if missing. **Theme-class adaptation**: if pills use `class="label-pill"`, verify theme CSS `.label-pill` includes `line-height:1`.

**QA-0b: Design Principles compliance** — Review the ENTIRE slides.md against `references/design-principles.md`:
- **Principle 1 (Rhythm)**: Count consecutive dense content slides. If 3+ `default` layouts in a row without a breathing slide (`section`/`statement`/`fact`), insert one.
- **Principle 2 (Layout diversity)**: Check that consecutive slides have different visual structures. If 2+ slides share the same pattern (e.g., "label + line + 2-column grid"), restructure one.
- **Principle 3 (Typography)**: Verify at least 3 type scales exist. Key metrics should be hero-sized (4-8rem). If all headings are the same size, fix it. **CRITICAL**: Measure statement/fact/section slide main text against 3rem minimum — if below, flag as critical and fix immediately.
- **Principle 4 (Icons)**: Search for emoji characters (📱💳⭐🧠📊🚗 etc.). If found, replace with `<Icon>` component. Ensure `components/Icon.vue` exists.
- **Principle 5 (Cards)**: Check if all cards use identical styling. If yes, differentiate with at least 2 card styles.
- **Principle 7 (Visual arc)**: Confirm the climax slide (Ask/CTA) has distinct visual treatment — different background, larger type, or unique color.
- **Principle 8 (Data viz)**: Check bar charts for value labels, tables for hero-column highlights.
- **Colorblind safety (Principle 8 expansion)**: Check that no data visualization uses red+green, green+brown, blue+purple, or green+black as the only differentiator. Recommend blue+orange for binary pairs.
- **Principle 9 (Mockups)**: Check device mockups for wireframe content. If empty, add wireframe UI.
- **Principle 10 (Diagrams)**: Check for text arrows (→ ↓ ← ↑) used as diagram connectors. Replace with SVG.
- **Principle 11 (Spacing)**: Check content vertical distribution — should not be crammed to top.
- **Principle 12 (Accent hierarchy)**: Verify accent color is used at varying intensities, not full saturation everywhere.
- **HTML nesting depth (Rule 17)**: Scan for HTML nesting deeper than 3 levels (3+ opening `<div>` tags before content). Slidev will render these as raw HTML code. Flatten immediately.
- **Font size minimum (Rule 20) — BLOCKING (applies to ALL modes including --stitch)**: Check all font sizes. Body text below `1.25rem` = CRITICAL — raise to minimum. Headings below `2.2rem` = CRITICAL. Labels/eyebrows below `0.65rem` = CRITICAL. If ANY violation → STOP pipeline. Auto-fix: raise to minimum. If content overflows → shorten text first, then move to speaker notes, then split slide (per Font Size Exemption). NEVER reduce font below minimum. **NOTE: --stitch=full generates web-viewport sizes (0.85rem body is typical) — these MUST be raised to presentation minimums during ST-F5 or caught here.**
- **Content density (Rule 22)**: Count visual blocks per slide. If any slide has 6+ distinct elements (cards, tables, charts, lists), split or remove secondary content.
- **Breathing slides (Visual Rhythm Override)**: Count consecutive dense `default` layout slides. If 4+ in a row, convert 1-2 to statement/fact layout.
- **Background image overlays (Rule P-5)**: If cover/section slides have background images, verify overlay uses gradient (not uniform opacity) with minimum 0.85 in text zones.

#### Feedback-Driven QA-0b Checks (code grep)

- [ ] **Pill centering:** Grep `border-radius.*20px` (or pill/badge/chip patterns). Verify each has `line-height: 1`, `display:.*flex`, `align-items: center`. Missing = WARNING
- [ ] **Pill-on-gradient mud:** Grep `rgba(` in pill/badge background context + `radial-gradient` on same slide. Both present = WARNING "potential mud overlap — use opaque pill background"
- [ ] **Icon container uniformity:** Find all `border-radius:50%` with icon containers on same slide. If 3+ with identical width+height+border = WARNING "uniform icon containers"
- [ ] **Grid element similarity:** Within each grid container, grep `border-radius` values. If different values among same-level children = WARNING "Gestalt similarity violation"
- [ ] **Rule of Thirds heuristic:** On non-breathing, non-cover, non-CTA slides: if heading has `text-align:center` AND no `grid-template-columns` with unequal fractions AND no asymmetric width splits = WARNING "dead center layout — consider Rule of Thirds"
- [ ] **Pie chart segment count:** If slides.md contains pie/donut chart markup with >5 segments/items = FAIL "pie chart exceeds 5 segments — use bar chart instead"
- [ ] **Caption proximity heuristic:** Within grid/flex containers, check that caption/label elements are in the same or immediately adjacent cell as their referent element. If separated by >1 cell = WARNING "Gestalt proximity violation"
- [ ] **CSS Variables enforcement (BLOCKING):** Scan all inline `style=""` attributes AND `<style scoped>` / `<style>` blocks for hardcoded hex (#XXXXXX, #XXX). Exclude: inside url(), CSS comments, styles/index.css variable definitions. If ANY hardcoded hex in color/background/border-color → STOP. Auto-fix: replace with matching var(--name). If no matching variable → create one in styles/index.css, then use it. Zero tolerance.
- [ ] **Body font size minimum (BLOCKING):** Find all `font-size:` declarations in BOTH inline `style=""` attributes AND `<style scoped>` / `<style>` blocks within slides.md. Scan CSS class definitions (e.g., `.s2-card-desc { font-size: 0.85rem }`) — not just inline styles. Labels/eyebrows (text-transform:uppercase or letter-spacing:0.1em+ or inside pill) → min 0.65rem. Pill badge → min 0.7rem. Body text → min 1.25rem. Headings → min 2.2rem. If ANY violation in either inline or scoped CSS → STOP. Auto-fix: raise to minimum. If overflow → shorten text first → speaker notes → split (per Font Size Exemption). NEVER shrink font.
- [ ] **bg-level distribution** (non-blocking): Count slides per bg-level. Warn if bg-base < 55%, bg-alt > 35%, or strict alternating across 4+ slides. No auto-fix — logged to QA-10 report.
- [ ] **Action titles check** (WARNING): For each h1/h2 slide title: if 1-2 words → WARNING "topic label". If noun phrase without verb/number/comparison → WARNING "weak title". Not auto-fixable. Logged to QA-10 report. Cover and CTA slides exempt (Rule 30).
- [ ] **Icon diversity:** Collect all icon containers across deck. If 100% identical shape → warn "All icon containers identical. Use at least 2 shapes (icon-circle, icon-rounded, icon-ghost)."
- [ ] **Decoration visibility (BLOCKING):** Scan all decorative div elements (z-index:0, pointer-events:none). If slide has light background AND decorative opacity < 0.12 → STOP. Auto-fix: raise to 0.15. If ANY decorative element < 200px width or height → STOP. Auto-fix: raise to 250px.
- [ ] **Focal point check (WARNING):** For each content slide, compare the largest and second-largest elements by font-size. If they differ by < 1.5x → WARNING "no clear focal point — one element should dominate at 2x+ size."

Fix any issues found before proceeding to visual review.

**QA-0c: Anti-Pattern Scan** — Before rendering, scan slides.md for these specific anti-patterns. This phase catches problems that QA-0a (CSS) and QA-0b (design principles) miss — pattern-specific bad practices identified by industry research.

**Scope note:** Some items overlap with QA-0a/QA-0b — this is intentional redundancy for defense-in-depth.

**Content density:**
- [ ] Words per content slide ≤40 (WARNING >40, CRITICAL >75; exception: table/comparison slides ≤60)
- [ ] Bullets per slide ≤4 (reinforces Rule 21)
- [ ] Words per bullet ≤12
- [ ] Text lines per slide ≤6

**Typography:**
- [ ] Body text ≥1.25rem (CRITICAL if smaller) (redundant with QA-0b BLOCKING check)
- [ ] Headings ≥2.2rem (CRITICAL if smaller)
- [ ] Line-height 1.3–1.45 for body text
- [ ] Bold usage ≤15% of total text
- [ ] No centered multi-line body text (CRITICAL) (redundant with QA-0a)
- [ ] Type treatments per slide ≤3 distinct combinations of font-family+weight+style (CRITICAL)
- [ ] No `font-style: italic` outside `<blockquote>`, attribution, or caption context (CRITICAL)
- [ ] Heading font not in Font Number Blacklist for number-heavy decks (CRITICAL)

**Color:**
- [ ] Primary accent not in AI blacklist (hue 240-290, sat >50%) = WARNING
- [ ] Body text contrast ≥4.5:1 against background (CRITICAL)
- [ ] No colorblind-unsafe data pairs (red+green, green+brown, blue+purple). Hue ranges: red (0-30) + green (90-165) = FAIL; brown (20-40) + green (90-165) = WARNING
- [ ] No pure `#000000` or `#FFFFFF` in any background or text color (CRITICAL)
- [ ] All backgrounds use only `var(--bg-base)`, `var(--bg-alt)`, or `var(--bg-accent)` — no hardcoded background colors (CRITICAL)
- [ ] Background temperature consistency: all 3 bg-levels share same warm/cool temperature (CRITICAL)
- [ ] Muted text contrast: `--color-muted` vs each bg-level and `--color-accent-bg` in styles/index.css — all pairs ≥ 4.5:1 (CRITICAL)

**AI tells:**
- [ ] No generic slide titles from blacklist: "Обзор", "Ключевые выводы", "О нас", "Наше решение", "Введение", "Итоги", "Резюме" (CRITICAL)
- [ ] `icon-trio` archetype used ≤1 time per deck
- [ ] All-caps eyebrow labels on ≤30% of slides
- [ ] Last slide is NOT "Спасибо" / "Thank You" / "Вопросы?" (CRITICAL)
- [ ] Action title by slide 2-3 surfaces main conclusion (business decks)
- [ ] No text arrow characters (→←↑↓⟶➜▶) in visible content outside `<code>` and `<!-- -->` (CRITICAL)
- [ ] No 3+ identical icon containers (same width+height+border-radius+border) on one slide — exception: numbered steps (CRITICAL)
- [ ] Only 1 decorative gradient type used — classify each gradient as decorative vs functional/structural. Both radial and linear as decorative = WARNING

**Data viz:**
- [ ] Bar chart Y-axis starts at zero (CRITICAL if not)
- [ ] Charts have ≤5-6 series/slices
- [ ] Statistics have source citations (WARNING if missing)

**Structure:**
- [ ] Sub-bullet nesting ≤2 levels (CRITICAL if deeper)
- [ ] Ghost Deck test: read slide titles in sequence — must tell coherent story (manual check)

Fix all CRITICAL items before proceeding to visual review. Log WARNINGs for reviewer attention.

### Phase 2: Visual Export & Review

**QA-1: Prepare** — `npm install` if no `node_modules/` in `<dir>`, then `npx playwright install chromium`.

**QA-2: Export PNGs** — `cd <dir> && npx slidev export --format png --output slides-qa` → produces `slides-qa/1.png, 2.png, ...`

**QA-2b: Render verification (BLOCKING)** — After export, verify:
1. **Slide count matches**: number of PNGs must equal the number of slides in `slides.md` (count `---` separators). If extra PNGs → blank slide from global headmatter (Rule 46). Fix: remove `layout` from global frontmatter.
2. **No blank slides**: Read slide 1 PNG visually. If blank/white → global headmatter has `layout: none`. Fix immediately.
3. **No raw HTML**: Read 2-3 content slide PNGs. If any shows `<div style="..."` text → HTML rendering failure (Rule 45 violation). Fix: move visual properties from inline styles to per-slide `<style>` CSS classes, then re-export.
If ANY of these checks fail → fix and re-export before proceeding to QA-3.

**QA-3: Count slides** — glob `<dir>/slides-qa/*.png` to get the list.

**QA-4: Per-slide visual review** — Read **EVERY** slide PNG with the Read tool (no skipping). Apply `/frontend-design` thinking — evaluate each slide as a designer who cares deeply about visual quality. For each slide, run this full checklist:

#### Text & Readability
- [ ] All text is fully legible — no text blends into the background
- [ ] Sufficient contrast ratio between text and background (white text on dark overlay ≥ 0.4 opacity, dark text on light bg)
- [ ] No text is clipped, cut off, or overflowing outside the visible slide area
- [ ] Text hierarchy is clear — heading visually dominant over body text
- [ ] Font rendering looks correct (not missing, not fallback system font)

#### Alignment & Positioning
- [ ] On centered layouts (cover, section, fact, end, statement, center): ALL text elements are actually centered — not left-shifted or right-shifted
- [ ] On default/content layouts: text and bullets are properly left-aligned with consistent indentation
- [ ] On two-cols: both columns are visible, roughly equal width, content doesn't overlap
- [ ] On image-left/image-right: image is on the correct side, text content is on the other side
- [ ] No unexpected empty space that suggests a positioning error
- [ ] Elements are vertically balanced — content isn't crammed at top or floating at bottom

#### Images (if applicable)
- [ ] Background images are visible (not blocked by opaque theme background-color)
- [ ] Background images have sufficient overlay for text readability
- [ ] Images in image-left/image-right layouts are visible and properly sized
- [ ] Image content is appropriate for the slide topic (not random, not broken)
- [ ] Images don't distract from text content — proper visual hierarchy maintained

#### Color & Palette
- [ ] Colors match the defined CSS variables / preset palette
- [ ] Accent color is used consistently across slides (headings, bullets, borders)
- [ ] No jarring color inconsistencies between slides
- [ ] Background treatment is consistent across similar slide types
- [ ] **CRITICAL — WCAG contrast**: Body text contrast ≥4.5:1 against background. Large text ≥3:1. Verify — do not estimate.
- [ ] **CRITICAL — Background variation (dark themes)**: Compare this slide's background to previous slide. Are they visually distinguishable? Section dividers MUST be noticeably different.
- [ ] **Colorblind safety**: No data visualization uses red+green as only differentiator
- [ ] **Whitespace**: Slide has ≥30% empty space, padding ≥44px from edges, gaps ≥16px between elements

#### Layout & Composition
- [ ] Layout matches the intended type (cover looks like cover, fact shows big number, etc.)
- [ ] Content density is balanced — not overcrowded, not too empty
- [ ] Whitespace is intentional and consistent
- [ ] Slide doesn't feel "broken" or "unfinished"

#### Design Principles Compliance
- [ ] **No emoji** visible — all icons are SVG-based (Principle 4)
- [ ] **Device mockups** (if any) contain wireframe UI, not empty boxes (Principle 9)
- [ ] **Diagrams** (if any) use SVG arrows, not text characters (Principle 10)
- [ ] **Charts** (if any) have value labels on key data points (Principle 8)
- [ ] **Card variety** — if multiple cards on slide, at least some visual differentiation (Principle 5)
- [ ] **Accent hierarchy** — accent color appears at varying intensities, not uniform (Principle 12)
- [ ] **Vertical balance** — content is well-distributed, not pushed to top (Principle 11)
- [ ] **Typographic drama** — key numbers/statements are oversized relative to body text (Principle 3)

#### v-click note
- Elements in initial hidden state due to `v-click`/`v-clicks` are **expected** to be invisible in static export — this is NOT a bug unless the slide is completely empty with no visible content at all.

#### Feedback-Driven Visual Checks (per slide)

- [ ] **Pill centering:** Text inside pill/badge elements is vertically centered (not shifted up)
- [ ] **Pill clarity:** Pill boundaries are crisp — no "mud" effect from gradient bleed-through
- [ ] **Muted text readability:** Palest text on this slide is readable against its background (especially on accent-colored surfaces)
- [ ] **Gestalt proximity:** Labels/captions are adjacent to their referent elements (not >1/4 slide height away)

#### Feedback-Driven Visual Checks (deck-level, after all slides reviewed)

- [ ] **Rule of Thirds:** At least 30% of content slides use off-center focal points (not all dead-center)
- [ ] **Background consistency:** No unexpected color temperature shifts between adjacent slides
- [ ] **Gradient consistency:** Decorative gradients all use the same type (all radial OR all linear)
- [ ] **Icon container variation:** No slide has 3+ identical icon circles in a row (unless numbered steps)
- [ ] **Muted text contrast (deck-level):** `--color-muted` is readable on ALL surface types across the entire deck

**QA-5: Compile issues** — build a list of `slide N — [category] issue description`. If none → proceed to Phase 3.

**QA-6: Fix** — Edit tool, apply `/frontend-design` thinking, targeted fixes only. Reference `references/layout-css-patterns.md` for proven CSS patterns.

**QA-7: Iterate** — if issues were found and fixed → go to QA-2 for another cycle. Repeat until NO issues remain. The agent decides when quality is sufficient — there is no iteration limit. Only proceed to Phase 3 when the visual review passes clean.

### Phase 3: Design Critic Review

After all visual issues are resolved (or max iterations reached), perform a final holistic review as a **demanding design critic** who loves beautiful presentations and nitpicks every detail.

**QA-8: Critic pass** — Re-read all slide PNGs one final time. Step into the role of an exacting presentation designer reviewing a colleague's work. Evaluate with `/frontend-design` principles:

- **Overall cohesion**: Do all slides feel like they belong to the same presentation? Is there a consistent visual language (color, spacing, typography, decoration) across every slide?
- **First impression**: Does the cover slide make a strong opening statement? Would you remember this presentation after seeing 20 others?
- **Visual rhythm**: Is there a good alternation between high-impact slides (cover, fact, section) and content slides? Does the pacing feel intentional?
- **Typography quality**: Are fonts distinctive and well-paired? Or do they feel generic? Is the hierarchy (heading > subheading > body) clear and consistent?
- **Color conviction**: Does the palette feel bold and intentional, or timid and forgettable? Is the accent color doing work or just decorating?
- **Spatial quality**: Is whitespace generous and purposeful? Or are slides either cramped or wastefully empty?
- **Image integration** (if images present): Do images enhance the message or just fill space? Are overlays creating good text-image relationships?
- **Professional polish**: Would you be confident presenting this to a demanding audience? Any slide that feels "off" or "cheap"?
- **No AI slop**: Does anything feel like generic AI output — overused fonts, cliched gradients, predictable layouts, emoji icons, empty device mockups, text-arrow diagrams?
- **Visual rhythm**: Is there good pacing — breathing slides between dense content? Or is it an unbroken wall of information?
- **Layout diversity**: Does each slide feel like its own composition? Or do they blur into one repeating template?
- **Typographic drama**: Are key numbers/statements dramatically large? Or is everything the same cautious size?
- **Decorative personality**: Do the slides have visual character beyond content? Or are they just text on a background?
- **Visual arc**: Does the presentation build to a climax? Is the Ask/CTA slide the most visually impactful?
- **Accent system**: Is the accent color used purposefully at varying intensities? Or is it the same brightness everywhere?

**QA-9: Critic fixes** — If the critic identifies issues, fix them. These are quality-of-life improvements, not bugs — adjust colors, spacing, typography, or composition to elevate the overall feel. Apply `/frontend-design` thinking. After fixes, re-export and re-run the critic pass (QA-8). Repeat until the critic is satisfied — there is no iteration limit. The agent decides when the presentation meets the quality bar.

### Phase 4: Cleanup & Report

**QA-10: Cleanup** — `rm -rf <dir>/slides-qa`

**QA-10b: Design Memory Write (conditional)** — If Scoring Subroutine was run during this session (e.g., as part of `--polish`), write the result to Design Memory. Follow the Write Protocol in `references/design-memory.md`.

**QA-11: Report** — Include all phases:
```
Visual QA Results:
  Code review: N issues found and fixed pre-render
  Visual review: N iteration(s), [all resolved | N issues remain]
  Design critic: [pass — presentation is polished | N refinements applied]
```

<HARD-GATE>
**MANDATORY QUALITY GATES — NEVER SKIP:**
1. **Step 0.4 PDL**: When creating a new preset (NO_MATCH), you MUST run Preset Deep Learn (PDL-1 through PDL-5) with N=3. No exceptions. No "for practicality". No "the user just wants export". The preset MUST be visually validated before use.
2. **Step 7 Visual QA Loop**: After generating slides.md, you MUST run the full Visual QA Loop (Phase 1-4). No exceptions. This includes CSS code review, PNG export, per-slide visual inspection, and design critic review.
Skipping either of these gates produces untested output. If you skip them, the presentation is defective by definition regardless of how it looks.
</HARD-GATE>

### Generation Modes

**`--no-preset` flag**: If present, skip Step 0 entirely and proceed directly to mode selection below.

#### Step 0: Auto-Preset (runs before mode selection if no `--preset`, no `--no-preset`, no `--figma`, and no `style:` prefix)

When the user calls `/slidev <topic>` without explicit style flags:

**Step 0.1: Scan existing presets** — Collect all `.preset.md` files from:
- `.slidev-presets/` (local project directory)
- `~/.claude/slidev-presets/` (global)
- `~/.claude/slidev-presets.json` (registry — read JSON, resolve all mapped paths)

If no presets found anywhere, skip to Step 0.4 (create new).

**Step 0.2: LLM matching** — Evaluate the presentation topic against each preset's name and aesthetic description. For each preset, consider: does this preset's mood, color scheme, and visual style fit the topic? Output one of:
- `MATCH: <preset-name>` — a suitable preset was found
- `NO_MATCH` — no existing preset fits this topic

**Step 0.3: If MATCH** — Load the matched preset using the standard Preset Resolution (4-tier lookup). Continue to mode "Preset mode" below.

**Step 0.4: If NO_MATCH (or no presets exist)** — Create and refine a new preset:
1. Generate an initial `.preset.md` based on the topic — infer mood, colors, fonts, CSS from the presentation subject. **CRITICAL — Light/Dark balance**: Do NOT default to dark themes. Alternate between light and dark across generations. Light themes are appropriate for: commercial proposals, investor reports, educational content, healthcare, corporate presentations. Dark themes are appropriate for: tech product demos, developer talks, creative portfolios, gaming. When in doubt, prefer light — light themes have better readability and fewer CSS specificity issues. Examples: a tech startup pitch → light cream with bold accent; a healthcare lecture → clean white with calming palette; a developer talk → dark with neon accent; a corporate proposal → light editorial.
   Include `archetypes` and `shapes` sections based on the presentation type:
   - Commercial proposal (КП) → `preferred: [bento-grid, stat-hero, profile-grid, card-mosaic]`, `icon_container: circle`, `stat_display: typographic`
   - Pitch deck → `preferred: [stat-hero, icon-trio, timeline-horizontal, asymmetric-split]`, `icon_container: circle`
   - Technical talk → `preferred: [two-col-text, data-spotlight, comparison-table, timeline-horizontal]`, `icon_container: rounded-square`
   - Educational lecture → `preferred: [icon-trio, timeline-zigzag, bento-grid, quote-pull]`, `icon_container: circle`
   Verify the generated accent color is not in the AI color blacklist (hue 240-290, sat >50%). If it is, shift hue to nearest safe alternative.
2. Save it to `.slidev-presets/<inferred-name>.preset.md` (local)
3. **CRITICAL — MUST NOT SKIP**: Run the **Preset Deep Learn Procedure (PDL-1 through PDL-5)** with N=3 as an inline variant. This step is **mandatory** — do NOT skip it for any reason (speed, practicality, token savings, or any other justification). The entire point of auto-preset is visual validation through iterative critique. A preset without PDL is an untested guess.
   - PDL-6 (save prompt) is skipped — preset is already saved locally
   - PDL-7 (cleanup prompt) is skipped — working directory is cleaned up automatically
   - All other steps (scaffolding, 3 cycles of visual critique, auto-apply, convergence) MUST run fully
4. Continue to mode "Preset mode" with the refined preset

#### Mode Selection

1. **Preset mode**: Input contains `--preset <name|path>` (or auto-preset matched/created one) → extract preset identifier, remainder is outline
2. **Figma preset mode**: `--figma` flag present → preset already created by FIG-Extract, use it directly. Enter Preset mode with the Figma preset loaded. See "Figma Archetype Priority" section for archetype selection and slot filling.
3. **Custom style mode**: Input starts with `style:` → extract style description, remainder is outline
4. **Unique mode**: `--no-preset` flag present → generate a completely unique design (current default behavior, no preset involvement)

### Outline Source

The outline can be:
- **Inline text** provided directly after the command/flags
- **File path** (e.g. `./my-outline.md`) → read the file to get the outline

Extract the outline: a structured list of slides with titles and content points.

## Hard Constraint

**The generated presentation MUST have exactly the same number of slides, in exactly the same order, with exactly the same content as the outline.** Never add, remove, merge, or reorder slides. The outline is the contract.

### Font Size Exemption

When text at the required minimum font size overflows the slide:
1. **Shorten text** to the core message (rephrasing is allowed)
2. **Move secondary details** to speaker notes
3. **Split slide** into two if core message cannot be shortened
Priority: shorten first → speaker notes second → split last. **NEVER reduce font below the minimum.**

### Visual Rhythm Override

**When the outline has 4+ consecutive dense content slides without any natural section break**, you MUST convert 1-2 of them to a breathing layout (`statement`, `fact`, or `center`) — choosing the slide with the single most impactful number, quote, or insight. **This is NOT adding or removing slides** — it's changing the LAYOUT of an existing outline slide to create visual breathing room. The slide content is preserved but presented as a dramatic centerpiece instead of a dense grid.

**Example**: An outline slide with "Traction: +20% MoM growth, 5000 users, NPS 70" → promote "+20% MoM" to a full-screen `fact` layout with hero-sized typography, and integrate the other two metrics as small supporting text below it.

**Target**: In a 10+ slide deck, at least 2-3 slides should use breathing layouts (statement/fact/center) distributed throughout the deck. In a 15+ slide deck, at least 3-4.

## Mode: Preset

### Preset Resolution

Resolve the preset name using this 4-tier lookup (local takes priority over global):

1. **Direct path**: If the name contains `/`, `\`, or ends in `.md` → read as file path
2. **Local**: Read `./.slidev-presets/<name>.preset.md` (current project directory)
3. **Registry**: Read `~/.claude/slidev-presets.json` → look up name in the JSON object → read the mapped path
4. **Global convention**: Read `~/.claude/slidev-presets/<name>.preset.md`

If none found, emit a clear error:
```
Preset "<name>" not found. Tried:
  1. As file path: <name>
  2. Local: ./.slidev-presets/<name>.preset.md
  3. In registry: ~/.claude/slidev-presets.json
  4. Global: ~/.claude/slidev-presets/<name>.preset.md
```

### Applying Preset

Parse the preset's YAML frontmatter and body:
- Map frontmatter fields to Slidev headmatter (theme, colorSchema, fonts, aspectRatio, transition)
- When resolving fonts from a preset: `fonts.body` (or legacy `fonts.serif`) maps to Slidev headmatter `fonts.serif` key — Slidev uses this key name internally for the second font slot regardless of whether the font is actually serif.
- Validation: if the `fonts.body` value matches any font in the Serif Blacklist → replace with nearest sans-serif equivalent. Log: "Preset font [name] is serif — replaced with [replacement]."
- Use `accentColor` for CSS variable `--slidev-theme-primary`
- Use the aesthetic description to guide layout choices, background treatments, and styling decisions
- If the preset contains a fenced `css` block, write it verbatim to `styles/index.css`

## Design Thinking (applies to Unique and Custom Style modes)

Before making any design decisions, invoke `/frontend-design` thinking AND read `references/design-principles.md`. Understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What is this presentation about? Who is the audience? A developer talk, a sales pitch, an academic lecture, and a creative portfolio all demand radically different aesthetics.
- **Tone**: Pick a clear direction — don't be generic. Options include: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these as inspiration but design one that is true to the content.
- **Differentiation**: What makes this presentation UNFORGETTABLE? What's the one thing someone will remember about its visual identity?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity. Match implementation complexity to the aesthetic vision: maximalist designs need elaborate CSS with extensive effects; minimalist designs need restraint, precision, and careful attention to spacing and typography.

### Design Decisions Checklist (from Design Principles)

During Design Thinking, you MUST also decide:
1. **Visual rhythm plan**: Which slides will be "breathing" slides (section/statement/fact)? Map the pacing before writing any content.
2. **Layout rotation plan**: What 4-5 different layout structures will you use? Assign them across slides to avoid repetition.
3. **Decorative motif**: What 1-2 decorative elements define this presentation's personality? (geometric circles, gradient blobs, dot grids, diagonal lines, etc.)
4. **Accent hierarchy**: Define 3 levels of accent color (primary/secondary/ambient) as CSS variables.
5. **Visual arc**: Which slide is the climax? How will visual intensity build toward it?
6. **Typography scales**: Define hero (6-12em for centered stat-hero, 4-8em for inline hero), heading (1.8-2.5em), and body (0.85-1.1em) scales. Centered breathing slides should use the maximum of the hero range.
7. **Card styles**: Which 2-3 card variations will you use and where?
8. **Icon approach**: outlined or filled SVG style? What stroke width?

### Design Memory Consultation

Before finalizing design decisions in Unique and Custom Style modes, read `~/.claude/slidev-design-memory.json` (if it exists). Follow the Read Protocol in `references/design-memory.md`. Use high-scoring patterns as inspiration (not templates) and avoid low-scoring patterns.

## Mode: Unique

Generate a completely unique design. Apply `/frontend-design` aesthetic principles:

### Font Selection
- Choose fonts that are beautiful, unique, and interesting — unexpected, characterful choices that elevate the presentation
- NEVER use generic fonts: Inter, Roboto, Arial, Open Sans, Space Grotesk, or system fonts
- NEVER converge on common AI-favorite choices across generations
- **CRITICAL: Never use a serif font.** All fonts must be sans-serif. Blacklisted serif families include (non-exhaustive): Source Serif 4, Newsreader, Merriweather, Playfair Display, DM Serif Display, Garamond, Georgia, Lora, Noto Serif, Crimson Text, EB Garamond, Libre Baskerville, Cormorant, Spectral, Bitter, Zilla Slab, Roboto Slab, Rockwell. If a preset specifies a serif font, replace it with the nearest sans-serif equivalent before generation.
- CYRILLIC FONT RULES — For Russian-language presentations (detected by Cyrillic characters in the outline):

  CYRILLIC WHITELIST (confirmed full Cyrillic coverage at all weights):
    Heading: Manrope, Plus Jakarta Sans, Montserrat, Rubik, Noto Sans, Geist, Hanken Grotesk, IBM Plex Sans
    Body: DM Sans, Nunito, Source Sans Pro, IBM Plex Sans, Noto Sans, Rubik, Manrope, Arimo

  CYRILLIC BLACKLIST (Latin-only — NO Cyrillic glyphs):
    Outfit, Sora, Barlow, Urbanist, Epilogue, Lexend, Spline Sans, Work Sans, Be Vietnam Pro, Public Sans

  If outline contains Cyrillic and a font from the Cyrillic Blacklist is selected → replace with the nearest Cyrillic-safe alternative. Log: "Font [X] has no Cyrillic, replaced with [Y]."
- Pair a distinctive sans-display font (geometric/condensed, for headings) with a sans-text font (humanist/rounded, for body) from Google Fonts. Contrast through character (geometric vs humanist, condensed vs proportional, angular vs rounded), not through serif/sans category split.
- Good sans+sans pairs:
  | Heading (display) | Body (text) | Contrast type |
  |-------------------|-------------|---------------|
  | Manrope | DM Sans | Semi-rounded vs Humanist |
  | Plus Jakarta Sans | Nunito | Geometric vs Rounded friendly |
  | Montserrat | Source Sans Pro | Geometric bold vs Neutral clean |
  | Rubik | IBM Plex Sans | Rounded warm vs Corporate humanist |
  | Geist | Noto Sans | Modern tech vs Universal neutral |
- Monospace: JetBrains Mono, Fira Code, IBM Plex Mono, Source Code Pro

### Font Number Blacklist
- **CRITICAL — Number-heavy presentations** (financial, metrics, data): NEVER select these fonts for headings — their digits render unevenly or bold is indistinguishable from regular in Chromium headless export: `Syne, Playfair Display, Bodoni Moda, Bricolage Grotesque`
- Bricolage Grotesque: bold digits visually indistinguishable from regular weight at display sizes — confirmed via human feedback.
- Before selecting a heading font, check if the outline contains 3+ slides with prominent numbers (budgets, metrics, percentages). If yes, verify the chosen font is NOT on the blacklist. For fonts not on the blacklist: if font's bold-regular weight delta < 300 = WARNING.

### Strict 2-Font Rule
- **Maximum 2 visual font identities in the entire presentation.** Heading font (sans-display) for: headings, numbers, labels, hero text. Body font (sans-text) for: descriptions, bullets, supporting text.
- Labels differ from headings only via `text-transform`, `letter-spacing`, `font-size` — same font-family.
- Hero numbers use heading font, just larger. Not a separate visual style.
- Monospace fonts used exclusively in code blocks (`<code>`, `<pre>`) do not count as a visual font identity — they serve a functional role.

### Color & Theme
- Commit to a cohesive aesthetic. Dominant colors with sharp accents outperform timid, evenly-distributed palettes
- Build a dominant palette (2-3 base colors) + one sharp accent
- Define as CSS variables: `--color-bg`, `--color-text`, `--color-accent`, `--color-surface`
- Map to Slidev variables: `--slidev-theme-primary`, `--slidev-theme-background`
- **CRITICAL — Vary between dark and light schemes across generations.** Do NOT always default to dark. Check the last 3 generated presentations (via design memory) — if all were dark, this one MUST be light. Light themes: cream (#F8F7F4), warm white (#FAFAF8), soft gray (#F0F0ED). Dark themes: navy (#0C1524), charcoal (#1A1A2E), deep slate (#0F172A). When unsure, prefer light.
- Never use plain white (#fff) or plain black (#000) as backgrounds — always tinted
- Avoid cliched color schemes (particularly purple gradients on white backgrounds)

### Backgrounds & Visual Details
- Create atmosphere and depth rather than defaulting to solid colors
- Use gradient meshes, noise textures, geometric SVG patterns, layered transparencies, dramatic shadows, or grain overlays
- Apply via CSS `background` on `:root` or specific slide classes
- Can use inline SVG data URIs for patterns
- Vary between organic (blurs, gradients) and geometric (grids, dots) across generations
- Backgrounds should add contextual effects that match the overall aesthetic

### Spatial Composition
- Use unexpected layouts where appropriate: asymmetry, overlap, diagonal flow, grid-breaking elements
- Generous negative space OR controlled density — both work when intentional
- Don't default to predictable, cookie-cutter slide layouts

### Motion & Transitions
- Match transition to the aesthetic mood
- Calm/elegant → `fade`
- Dynamic/energetic → `slide-left` or `slide-up`
- Technical → `none` or very short `fade`
- Focus on high-impact moments: one well-orchestrated reveal creates more delight than scattered micro-interactions

## Mode: Custom Style

Parse the style description after `style:`. Apply `/frontend-design` thinking to translate descriptive terms into a bold, cohesive aesthetic direction:
- Mood words → color temperature, contrast level, spatial density
- Style references (brutalist, minimal, corporate, playful) → font choices, spacing, decoration, background treatment
- Color mentions → full palette construction with dominant/accent hierarchy
- Interpret creatively — don't just map keywords literally, build a complete visual identity
- Then follow the same generation procedure as Unique mode

## Theme Support

**`--theme <name>`**: Use a non-default Slidev theme. This is a modifier — combine with generation modes (unique, preset, custom style). Example: `/slidev --theme seriph <outline>`.

### Supported Themes
- **Primary**: `default` (current behavior), `seriph`, `apple-basic`
- **Experimental**: `bricks`, `shibainu`, `penguin`, `dracula`
- **Unknown**: print warning, attempt best-effort generation

### Generation Changes

**Step 2 (package.json)**: If `--theme` is not `default`, replace `"@slidev/theme-default": "latest"` with `"@slidev/theme-<name>": "latest"`.

**Step 5 (slides.md headmatter)**: Set `theme: <name>`.

**Step 4 (styles/index.css)**: For non-default themes, skip theme-default-specific CSS overrides (blockquote reset, explicit text-align for centered layouts). Instead add:
```css
/* Theme: <name> — theme-specific overrides may be needed.
   Check exported PNGs for CSS specificity issues. */
```

### Visual QA Theme Conditioning

Rules about `@slidev/theme-default` CSS specificity (Rules 9, 10, 24, 29, 32) become conditional:
- If `theme == "default"`: apply these rules as written
- If `theme != "default"`: skip these rules. Instead, during QA-4 visual review, pay extra attention to text alignment, background rendering, and blockquote styling — flag any visual issues that suggest theme CSS conflicts.

### Theme Detection in Post-Generation Operations

`--polish`, `--edit`, `--compare` and other post-generation subcommands detect the current theme by reading `theme:` from `slides.md` headmatter. This theme context is passed to Visual QA and A/B testing steps.

## Generation Procedure

### Step 1: Resolve Design Parameters

Apply the Design Thinking section above (for Unique/Custom Style modes) or parse the preset (for Preset mode). Based on mode, determine:
- `theme`: Slidev theme (usually `default`)
- `colorSchema`: `light` or `dark`
- `fonts`: `{ sans, body, mono }` from Google Fonts (all must be sans-serif)
- `palette`: CSS variables for colors
- `transition`: default slide transition
- `aspectRatio`: usually `16/9`
- `backgroundCSS`: CSS for backgrounds/textures
- `aesthetic`: free-text description for guiding per-slide decisions

### Step 1.5: Theme Resolution

1. Check if the resolved preset has a co-located theme directory (`<preset-name>-theme/` sibling to the .preset.md file)
2. If theme directory exists:
   a. Copy it to the output presentation directory as `theme/`
   b. Set slides.md frontmatter: `theme: ./theme`
   c. Skip `styles/index.css` generation (styles live in theme/)
   d. Skip `components/Icon.vue` generation IF theme provides it
3. If theme directory does not exist:
   a. Set slides.md frontmatter: `theme: default`
   b. Generate `styles/index.css` as before (current behavior)
   c. Generate `components/Icon.vue` as before

### Step 2: Scaffold package.json

```json
{
  "name": "<project-name>",
  "private": true,
  "scripts": {
    "dev": "slidev",
    "build": "slidev build",
    "export": "slidev export"
  },
  "dependencies": {
    "@slidev/cli": "latest",
    "@slidev/theme-default": "latest"
  }
}
```

If using a non-default theme, add the theme package to dependencies.

### Step 3: Write uno.config.ts

```ts
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'slide-heading': 'text-4xl font-bold tracking-tight',
    'slide-subheading': 'text-2xl font-light opacity-80',
    'slide-accent': 'text-[var(--color-accent)]',
  },
})
```

Customize shortcuts based on the design aesthetic.

### Step 4: Write styles/index.css

Include:
- FONT LOADING RULE — styles/index.css MUST begin with an explicit @import url() that loads ALL needed weights:

  ```css
  @import url('https://fonts.googleapis.com/css2?family=<HEADING_FONT>:wght@400;500;600;700;800&family=<BODY_FONT>:wght@400;500;600;700&display=swap');
  ```

  Do NOT rely on Slidev's automatic font loading from frontmatter — it loads only weights 400+600 by default. The @import ensures ALL weights used in inline styles are available, preventing synthetic bold rendering artifacts where Cyrillic and Latin characters render at different thicknesses.
- CSS variable definitions (palette) — **MUST include 3-level accent hierarchy** (Principle 12): `--color-accent` (full), `--color-accent-dim` (40-60% opacity), `--color-accent-bg` (8-15% opacity). **MUST also include decomposed RGB variables** for rgba() composability: `--accent-rgb: R, G, B;` (from --color-accent), `--bg-base-rgb: R, G, B;` (from --bg-base), `--text-rgb: R, G, B;` (from --color-text). **MUST also define `--color-accent-warm`**: a warm-toned secondary accent (amber, coral, terracotta) for CTA buttons, key metrics on 1-2 slides, and temperature contrast. Example: if primary accent is teal (#0D9488), warm accent = amber (#D97706). Use sparingly (1-2 slides) but it MUST exist to break chromatic monotony
- Background textures/gradients
- Font overrides if needed
- Custom utility classes
- **Card style variants** (Principle 5): `.card-solid`, `.card-ghost`, `.card-accent`, `.card-glass`, `.card-stripe` — at least 2-3 distinct styles. `.card-stripe` adds a colored top border: `border-top: 3px solid var(--color-accent); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);` — use for case studies, portfolio items, metric comparisons.
- **Decorative motif classes** (Principle 6): CSS pseudo-element patterns for the chosen decorative motifs (geometric circles, gradient blobs, dot grids, diagonal lines, etc.)
- **Shape vocabulary CSS** (if preset has `shapes` section): Generate CSS classes corresponding to the shape settings. For `icon_container: circle` → `.icon-container { width:56px; height:56px; border-radius:50%; background:var(--color-accent-bg); border:1.5px solid var(--color-accent-dim); display:flex; align-items:center; justify-content:center; }`. For `stat_display: typographic` → `.stat-hero { font-size:5rem; font-weight:800; color:var(--color-accent); line-height:1; }` (no card wrapper). For `label_style: pill` → `.label-pill { display:inline-flex; background:rgba(255,255,255,0.06); border:1.5px solid var(--color-accent-dim); border-radius:20px; padding:6px 18px; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.15em; color:var(--color-accent); font-weight:600; }`. For `photo_mask: circle` → `.photo-circle { border-radius:50%; overflow:hidden; }`. These classes are used by archetype HTML skeletons.
- If preset mode with CSS block, write the preset's CSS verbatim (can extend but not contradict)

#### Background Level System (REQUIRED)

Generate these 3 CSS variables in `styles/index.css`:
```css
--bg-base: <hex>;    /* 60% of slides — primary content background */
--bg-alt: <hex>;     /* 30% of slides — section dividers, alternating content */
--bg-accent: <hex>;  /* 10% of slides — cover, CTA */
```

Rules:
- All 3 must share the same color temperature (all warm or all cool)
- Luminance delta between --bg-base and --bg-accent: max 40%
- Never pure #000 or #FFF
- Add a CSS comment with contrast ratios: `--color-muted` vs each bg-level, `--color-text` vs each bg-level

#### Decorative Gradient Type Choice

Choose exactly ONE decorative gradient type for the presentation and note it in a CSS comment:
```css
/* Decorative gradient type: radial-gradient */
```
This is a behavioral constraint — enforce during Step 5 when writing slides. Decorative = blobs, glows, washes. Functional (card tints, bg-accent) are exempt.

#### Muted Text — Weakest Segment Check

After defining `--color-muted`, verify its contrast ratio against ALL bg-levels and `--color-accent-bg`. The **lowest ratio** must be ≥ 4.5:1. If not, darken `--color-muted` until it passes. Document ratios in a CSS comment.

### Figma Preset: Design Language Override

**CRITICAL:** When using a Figma-sourced preset (detected by `figma:` section in preset frontmatter), the **Figma template's visual language overrides standard design-principles.md rules** wherever they conflict. The Figma template was created by a human designer — their design choices take priority over generic skill rules.

**Concrete overrides:**
- **Icons**: If the Figma template does not use icons → do NOT add `<Icon>` components. Skip design-principles Principle 4 entirely. The template chose pure typography — respect that.
- **Backgrounds**: If the Figma template uses only `--bg-base` (white) for content slides → do NOT use `--bg-alt` on any content slide. Only use bg-alt/bg-accent where the Figma template itself uses them (section dividers, cover, CTA).
- **Decorative elements**: If the Figma template does not use decorative blobs/gradients on content slides → do NOT add them. Only use decorations where the template uses them.
- **Card structure**: If the Figma template shows text ABOVE gray cards (cards as image placeholders) → do NOT put text INSIDE cards.
- **Shape vocabulary**: If the Figma template does not use circular icon containers, pill badges, or other shapes → do NOT add them.
- **Typography scale**: Use the exact font sizes from the Figma template's archetypes, not the generic skill minimums (the Figma values already satisfy minimums because FIG-4 applied Font Size Floor during extraction).

**How to determine what the Figma template does:** Read the archetype.html files and the preset's aesthetic description. If an element type (icons, decorations, shapes) is absent from ALL archetypes → the template deliberately excludes it.

**What standard rules STILL apply with Figma presets:**
- Font Size Floor (body ≥ 1.25rem, heading ≥ 2.2rem) — safety net
- Content density limits (≤40 words per slide)
- Hard Constraint (exact slide count and order from outline)
- Visual QA pipeline (QA-0a/0b/0c)
- Footer structure (from the archetype templates)

### Figma Archetype Priority

**CRITICAL — VERBATIM COPY RULE:** When using a Figma-sourced preset, Figma archetypes are used as **literal HTML templates**, NOT as "inspiration" or "reference". You MUST copy the archetype.html file verbatim and ONLY replace `{{SLOT}}` markers with content.

**What you MUST NOT do with Figma archetypes:**
- Do NOT rewrite the HTML structure
- Do NOT replace inline `style=""` attributes with CSS classes
- Do NOT add HTML elements that don't have corresponding `{{SLOT}}` markers
- Do NOT remove HTML elements from the archetype
- Do NOT change CSS values (font-size, padding, gap, colors, flex ratios)
- Do NOT substitute `var(--color-*)` variables with other variables or hardcoded values

**Archetype selection:**
1. For each slide, determine content type from outline (as usual)
2. Look for a Figma archetype with matching `contentType` in `figma.archetypes[]`
3. If found → **copy** its HTML skeleton from `figma-<name>-figma/slide-<N>-<name>/archetype.html` verbatim. Replace ONLY `{{SLOT}}` markers.
4. If no matching `contentType` → find the **closest** Figma archetype by visual structure (e.g., a slide with 4 items → use figma-three-cards with flexibility rules). **Prefer adapting a Figma archetype over falling back to standard archetypes** — this preserves visual consistency with the Figma template.
5. Only if NO Figma archetype can reasonably fit → fallback to standard archetype from `references/composition-archetypes.md`. But even then, the standard archetype MUST use the same CSS values from the Figma preset (same fonts, colors, spacing, border-radius, background). Match the Figma template's visual language — not the standard archetype's defaults.
6. If outline has more slides than Figma archetypes of that type → reuse the same Figma archetype for multiple slides (different content, same layout)

**Slot Filling with Flexibility Rules** — When filling `{{SLOT}}` markers in a Figma archetype:
1. Read `flexibility.yaml` from the archetype's directory (`figma-<name>-figma/slide-<N>-<name>/flexibility.yaml`)
2. For **repeating elements** (cards, list items):
   - Content count < `slots.<name>.min` → merge slots or add subtle placeholder
   - Content count within `min..max` → apply `scaling` strategy:
     - `grid-auto`: adjust `grid-template-columns` (e.g., `repeat(3,1fr)` → `repeat(4,1fr)`)
     - `wrap`: keep grid definition, elements flow naturally with `flex-wrap:wrap`
     - `stack`: switch from horizontal to vertical layout
   - Content count > `slots.<name>.max` → truncate, move overflow to speaker notes
3. For **text slots**:
   - Text length > `slots.<name>.max_length` → apply `overflow` strategy:
     - `shrink-font`: reduce font-size by 0.1rem steps (but never below Font Size Floor)
     - `truncate`: cut text with ellipsis
     - `wrap`: allow text wrapping (may increase element height)
4. **Preserved properties** (from `layout.preserve`) are NEVER changed:
   - `spacing-ratio`: gap proportions between elements stay as extracted from Figma
   - `font-size-hierarchy`: ratio of heading-to-body font sizes stays fixed
   - `color-usage`: accent/muted/text color assignment per element stays fixed
   - `border-radius`: corner radius values stay as extracted

### Step 4.5: Composition Planning

Before writing slides, create a Composition Plan that maps each outline slide to a named archetype from `references/composition-archetypes.md`. This replaces ad-hoc layout selection with structured, content-aware composition.

**Procedure:**

1. **Read preset archetypes** (if present): load `preferred` and `avoid` lists from the preset's `archetypes` section. If no archetypes section, use empty defaults.

2. **Classify each slide's content type**: For each slide in the outline, determine its content type from this taxonomy:
   - `intro` — first slide, company/product name
   - `credentials` — experience, stats, certifications
   - `context` — task description, parameters
   - `vision` — visualization, concept, design
   - `scope` — list of works, features
   - `process` — stages, timeline, steps
   - `team` — people, roles
   - `metric` — key number, budget, KPI
   - `portfolio` — cases, projects, examples
   - `trust` — guarantees, quality control
   - `terms` — conditions, legal, payment
   - `cta` — call to action, contacts

3. **Select archetype for each slide** using the mapping table in `references/composition-archetypes.md`:
   a. Get candidate archetypes from content type mapping
   b. Remove any archetypes in the preset's `avoid` list
   c. Remove archetypes used in the last 3 slides (entropy window = 4)
   d. If previous slide was high-density, prefer low/medium-density candidates
   e. If a candidate is in the preset's `preferred` list AND matches the content type, select it (tie-breaker)
   f. Select the most suitable remaining candidate
   g. **Fallback**: if empty after filtering → relax entropy window to 2 and retry. If still empty → ignore density filter AND entropy window, select the candidate with the lowest recent-use count.

4. **Cost-of-Inaction Check** — After classifying content types, check if COI applies:
   - **Explicit types:** pitch, investor, sales, proposal, fundraising, business case, report, quarterly, annual, workshop, training, educational
   - **Keyword detection:** if the full outline text (titles + bullet content) contains 3+ of: "рост", "выручка", "инвестор", "revenue", "ROI", "клиенты", "рынок", "прибыль", "метрики", "KPI", "конкуренты", "growth", "market", "profit", "traction", "отчёт", "результаты" → treat as business
   - Check if any slide addresses cost of inaction (keywords: "risk of inaction", "what happens if", "without this", "status quo cost", "стоимость бездействия", "если ничего не делать", "текущие потери")
   - If no such slide → insert a cost-of-inaction slide after the problem/pain slide (or after slide 2 if no pain slide)
   - **COI framing by type** (language matches slide content):
     - pitch/investor/fundraising: "Что потеряет инвестор, не присоединившись сейчас" / "What investors lose by waiting"
     - report/quarterly/annual: "Что произойдёт, если не масштабировать текущие результаты" / "The cost of not scaling these results"
     - sales/proposal: "Сколько стоит каждый месяц без этого решения" / "Every month without this costs [X]"
     - workshop/training/educational: "Что произойдёт, если участники не применят знания" / "What happens if you don't apply this"
   - Use numbers from outline if available; otherwise directional language. Never hallucinate company-specific statistics.
   - Log: "Added cost-of-inaction slide not present in original outline."
   - **Hard Constraint exemption:** cost-of-inaction auto-insert is an explicit exception to the "same number of slides as outline" constraint.

5. **Layout Budget Rule** — After assigning archetypes, validate composition variety:
   - Mandatory archetypes (EXEMPT from budget): cover-hero (slide 1), cta-warm (last slide).
   - For non-exempt content slides:
     a. No single layout-group may exceed 40% of content slides
     b. Split-group (two-col-text, asymmetric-split) specifically: max 30%
     c. No more than 2 consecutive slides from the same layout-group
   - Layout groups: hero (section-divider, stat-hero, quote-pull), grid (icon-trio, bento-grid, card-mosaic, profile-grid), split (two-col-text, asymmetric-split), timeline (timeline-horizontal, timeline-zigzag), table (data-spotlight, comparison-table).
   - If violated: replace excess slides with archetypes from under-represented groups. Prefer breathing slides (stat-hero, quote-pull) to break monotony.

6. **Validate deck-level constraints**:
   - Every 10-slide deck contains minimum: 1 low-density, 1 medium, 1 high-density archetype
   - No more than 2 consecutive high-density archetypes
   - At least 3 different archetype groups (hero/grid/split/timeline/table/cta) in any 10-slide deck
   - `profile-grid` appears at most once per deck
   - `icon-trio` appears at most once per deck (same as `profile-grid`)
   - **Visual structure dedup**: After assigning archetypes, check the RENDERED visual structure (not archetype names). Two-col-text, card-mosaic (2×2), and timeline-horizontal (2×2 grid) all render as "4-cell grid" visually. Count slides that will render as a 2×2 or similar grid — if >30% of content slides share this visual pattern, replace excess with non-grid archetypes (asymmetric-split, stat-hero, quote-pull, bento-grid with asymmetric sizing). **Deck-level grid fingerprint cap**: Count ALL slides in the deck (consecutive or not) whose visual renders as "heading + grid of 3+ cards". If count > 35% of content slides (e.g., >3 in a 10-slide deck, >4 in a 12-slide deck), replace excess slides with non-grid archetypes. Additionally, when two bento-grid slides share the same column ratio (e.g., both use 1.25fr/1fr), alternate the ratio globally: if slide A uses 1.25fr/1fr (featured-left), slide B must use 1fr/1.25fr (featured-right). Apply this globally across all bento-grid instances in the deck — not just adjacent ones — to create intentional mirror variation. **CRITICAL — consecutive grid-group slides**: When two consecutive content slides both belong to the grid group (icon-trio, bento-grid, card-mosaic, profile-grid), they share the visual fingerprint "heading-top-left + card-grid-below" regardless of their internal card configuration. At least ONE of the two must break this fingerprint by: (A) using a centered heading instead of top-left, (B) placing the heading text INSIDE the featured card as an oversized element, or (C) ensuring the grid uses a clearly asymmetric column ratio of 1.4fr+ vs 1fr. Back-to-back equal-column card grids with top-left headings = layout monotony regardless of which archetypes are named.
   - **Adjacent slide structural fingerprint**: After completing the Composition Plan, check every pair of adjacent slides. Assign each a visual fingerprint: "centered-hero", "left-heading+grid-right", "left-heading+2col", "asymmetric-40/60", "left-heading+card-rows", "centered-stat+pills". If two adjacent slides share the same fingerprint, replace one with a structurally different archetype. This catches cases where different archetype names (e.g., stat-hero-asymmetric and asymmetric-split) produce visually identical layouts.
   - **Adjacent focal gravity audit**: Beyond structural fingerprint, check the visual gravity (where the eye is drawn first) of adjacent slides. Classify each as left-dominant, right-dominant, or center-dominant. Never have 2+ adjacent slides with the same gravity direction — alternate left/center/right to create visual rhythm across the deck.
   - For business presentations (KP, pitch, report): main conclusion must be surfaced as action title by slide 2-3. If outline buries it after slide 5, formulate action titles that bring the conclusion forward.
   - **Ghost Deck test — ENHANCED**: After creating the Composition Plan, read all planned action titles in sequence.
     **FAIL conditions** (any one = rewrite the title immediately):
     - Title is 1-2 words ("Продукт", "Команда", "Рынок") → FAIL
     - Title is a noun phrase without verb or claim ("Финансовый прогноз", "Конкурентный анализ") → FAIL
     - Title could apply to any company in the sector without change → FAIL
     - Title does not contain a number, comparison, or outcome → WEAK (rewrite recommended)
     - Title contains a counting number but no claim/outcome ("Три барьера", "Пять этапов", "4 принципа") → FAIL — counting items is a label, not an insight. Rewrite with the key finding: "Три барьера тормозят 85% компаний" or "5 этапов сокращают внедрение вдвое".
     **GOOD title patterns:** specific number ("Выручка 72 млн ₽ к 2027 году"), claim ("Enterprise растёт в 2,5 раза быстрее рынка"), outcome ("Каждый рубль инвестиций с конкретным возвратом"), question ("Готовы к партнёрству?"), verb ("Подключите первый объект бесплатно").
     Cover slide (slide 1) and CTA slide (last slide) are exempt (aligns with Rule 30).
     **Section divider slides**: Heading may be a topic label ONLY IF the description below it contains a claim, number, comparison, or outcome. If the description is also generic (no number, verb, or outcome), FAIL — upgrade the heading to an insight. Pattern: 'Почему клиенты остаются' (heading) + 'Долгосрочные партнёрства — показатель 78% возврата' (description with number) → PASS. 'Наши достижения' (heading) + 'Результаты нашей работы' (description, no claim) → FAIL. Rewrite heading as the insight: '78% клиентов возвращаются — не случайность'.
   - Cover archetype always first, CTA archetype always last
   - **Section divider differentiation**: When a deck has 2+ section-divider slides, they MUST differ visually. Alternate between: (A) centered heading with radial glow (current template), (B) left-aligned heading at 3.5rem+ with a large decorative number or geometric shape on the right side, PLUS a tertiary lower anchor: either (i) a row of section-count pills at bottom-left ('Раздел 1 из 3 · 3 слайда'), or (ii) a progress indicator row with 3 dots (filled=current, empty=future). This grounds the lower third of the slide and transforms empty space into intentional navigation cues. (C) full-width heading with a horizontal accent line below. No two section slides may use the same composition variant. **CRITICAL — 3+ section dividers background variety**: When a deck has 3 or more section-divider slides, they MUST NOT all use the same background color (e.g., all solid bg-accent). At least ONE section divider must use a visually distinct background treatment: (A) bg-alt background with heading ≥4rem (compensates for lighter bg with oversized type — the larger heading creates the structural break that the accent color provides on other section slides), (B) bg-accent with a `rgba(0,0,0,0.18)` overlay applied to the background div (creates a perceptibly darker teal vs clean bg-accent — visible at PNG export resolution), or (C) the asymmetric panel variant where a dark diagonal or solid panel fills 40%+ of the slide area. Goal: if someone flips through ONLY the section-divider slides in sequence, each should feel visually distinct in color/value — not just in layout.
   - **Section divider visual weight on bg-accent**: When a section divider uses bg-accent (teal) background, white text alone is insufficient — the slide looks like a "pause screen." MUST include at least ONE prominent decorative element: a large translucent circle (300px+, rgba(255,255,255,0.12)), a bold horizontal rule (4px, white, 60% width), a large ghost number ("02", 8rem, rgba(255,255,255,0.12) minimum — values below 0.10 are invisible on teal at PNG export resolution), or an arc element (6px border, white, 400px). The decorative element must occupy at least 20% of the slide area.

5. **Assign background levels** using distribution algorithm (replaces per-archetype table):

   ```
   1. Slide 1 (cover) → bg-accent
   2. Last slide (CTA/end) → bg-accent
   3. Breathing/statement slides (quote-pull, stat-hero with "breathing" annotation) → bg-alt
   4. Section dividers → bg-accent (LIGHT themes) or bg-alt (DARK themes). On light themes, section dividers MUST use the accent color background with white/light text to create a clear structural break. On dark themes, bg-alt provides sufficient contrast.
   5. Count remaining unassigned slides as R
   6. Assign bg-alt to floor(R * 0.25) additional slides, spaced every 3rd-4th content slide. bg-alt MUST appear on at least 25% of non-cover/CTA slides (minimum 2 in a 10-slide deck, minimum 3 in a 12+ slide deck)
   7. All remaining slides → bg-base

   Validation: bg-base must be ≥55% of total. If not, convert bg-alt to bg-base starting from the last assigned bg-alt slide.

   Anti-checkerboard validation: After assignment, check for strict alternating patterns (bg-base, bg-alt, bg-base, bg-alt...). bg-alt MUST serve a semantic purpose: (A) section entry/divider, (B) breathing slide on a different topic, or (C) pre-CTA bridge. If the assignment produces an alternating checkerboard, override by keeping bg-base for 2-3 consecutive content slides and only switching to bg-alt for genuine structural transitions. Good pattern: base, base, alt (section break), base, base, base, alt (pre-CTA). Bad pattern: base, alt, base, alt, base, alt.
   ```

   No inline background colors — only `var(--bg-*)` tokens.

6. **Output Composition Plan** as a table in the generation context:
   ```
   | Slide | Content Type | Archetype | Group | Density | Bg-Level |
   |-------|-------------|-----------|-------|---------|----------|
   | 1     | intro       | cover-hero | hero | low     | --bg-accent |
   | 2     | credentials | bento-grid | grid | medium-high | --bg-base |
   ...
   ```

This plan is consumed by Step 5: for each slide, use the archetype's HTML skeleton from `references/composition-archetypes.md` and fill `{{SLOT}}` markers with content from the outline. Apply the preset's shape vocabulary when rendering elements.

### Step 5: Write slides.md

**FONT SIZE FLOOR** — NEVER set any inline font-size below these minimums:
- Hero/stat numbers: ≥6rem (centered stat-hero slides: ≥8rem for maximum drama)
- Split-layout heading cap: two-col-text and asymmetric-split archetypes — if heading exceeds 50 characters, reduce font-size to 2.0–2.1rem AND shorten text to ≤2 visual lines. Move secondary detail to card content, not heading.
- Headings (h1, h2): ≥2.2rem
- Body text (descriptions, paragraphs, card content): ≥1.25rem
- Labels/eyebrows (uppercase, pill text): ≥0.65rem
- Pill badge text: ≥0.7rem
If content doesn't fit at these sizes — SHORTEN THE TEXT, never shrink the font. Maximum words per card: 15. Maximum words per bullet: 10.

**CSS VARIABLE ENFORCEMENT** — When writing inline styles in slides.md:
- NEVER hardcode hex color values (#XXXXXX or #XXX). Always use var(--name).
- Required COLOR variables: var(--color-accent), var(--color-text), var(--color-muted), var(--bg-base), var(--bg-alt), var(--bg-accent), var(--color-surface), var(--color-surface-border), var(--color-accent-dim), var(--color-accent-bg).
- Required FONT variables: var(--font-heading), var(--font-body).
- For rgba: use var(--accent-rgb) → rgba(var(--accent-rgb), 0.15). Also use --bg-base-rgb, --text-rgb.
- rgba() with numeric literals like rgba(255,255,255,0.1) is ALSO a violation if it corresponds to a defined color. Exception: generic transparency overlays rgba(255,255,255,...) and rgba(0,0,0,...) NOT tied to the palette are acceptable.
- The ONLY acceptable hardcoded values: pixel sizes, rem values, percentages.
- Hardcoded hex in color/background/border-color/font-family = VIOLATION.

**BACKGROUND LAYER SYSTEM** — Every slide MUST have minimum 2 background layers implemented as real HTML div elements (z-index:0, pointer-events:none):

Layer 1 (base): solid color — var(--bg-base), var(--bg-alt), or var(--bg-accent)

Layer 2 (atmosphere): ONE of these, as a positioned div inside the background:
  - Radial glow: radial-gradient(ellipse at 80% 20%, rgba(var(--accent-rgb),OPACITY), transparent 60%)
  - Ambient gradient: linear-gradient(135deg, rgba(var(--accent-rgb),OPACITY), transparent)
  - Vignette: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.06) 100%)

Layer 3 (texture, on 30-40% of slides): dot-grid, noise, or stripes from references/decoration-library.md

CRITICAL: use real HTML <div> elements, NOT CSS pseudo-elements. ::after/::before do NOT render in Slidev headless PNG export.

OPACITY CALIBRATION:
  Light bg-base (luminance > 75%, e.g. #FAF9F6 cream): atmosphere 0.25-0.35 (HARD MINIMUM 0.25), texture 0.15-0.22 (HARD MINIMUM 0.15). Dot-grid dots: 0.22 minimum. Arc/ring borders: 2px width and 0.30 minimum.
  Light bg-alt (luminance 65-75%, e.g. #E8E6DF warm beige): atmosphere 0.35-0.45 (HARD MINIMUM 0.35). bg-alt absorbs teal/cool glows more aggressively than pure cream — use 0.35+ or add a secondary warm highlight layer. Texture: 0.18-0.25.
  Dark backgrounds (luminance < 30%): atmosphere 0.08-0.15, texture 0.03-0.08
  These minimums are non-negotiable — decoration below these values is INVISIBLE in PNG export.
  IMPORTANT: When placing decorations on bg-alt slides, EXPLICITLY set opacity to 0.35+ — decoration library defaults (0.20-0.25) pass bg-base but FAIL bg-alt. Override the library default for every bg-alt slide.
  Card-mosaic and comparison-table archetypes: despite being card-heavy, MUST include at minimum 1 decorative element (corner circle, arc, or dot-grid) to prevent flat-document appearance.

**GHOST TYPOGRAPHY** — On stat-hero and breathing slides, add a decorative ghost element: the hero number or key symbol rendered at 12-20rem, opacity 0.04-0.08, positioned absolute behind content. Example: `<div style="position:absolute;top:50%;right:5%;transform:translateY(-50%);font-family:var(--font-heading);font-size:18rem;font-weight:800;color:rgba(var(--accent-rgb),0.06);line-height:1;pointer-events:none;z-index:0;">₽</div>`. Use on 2-3 slides per deck maximum. Good candidates: currency symbols (₽, $), percentages, key metric numbers.

**DATA VIZ RULE** — If a slide contains 3+ numeric metrics, at least ONE must be visualized as inline SVG, not text-in-card. Proportions → donut chart (stroke-dasharray). Comparison → horizontal bar chart (rect elements). Growth → line with dots. Parts of whole → stacked bar. SVG must use var(--color-accent) for fill/stroke, max 5 data points, labels inline, viewBox-based, include <title> for accessibility.

**METRIC HIERARCHY** — When a slide has 2+ numbers, they MUST differ in size using a 3-level system: Level 1 (hero): 7-10rem single primary metric, Level 2 (supporting): 3-4rem for 2-3 secondary metrics, Level 3 (context): 1.25-1.5rem body text. BANNED: all metrics at the same font-size — this creates competition for attention instead of clear hierarchy. Learned from Stitch: ratio primary:secondary:body should be approximately 7:3:1.

**CARD DIVERSITY** — BANNED: 3+ cards with identical styling on one slide. When showing 3 items, MUST use one of: a) Bento grid: 1 large (grid-row:span 2 or 1.4fr) + 2 smaller, b) Mixed styles: card-solid + card-ghost + card-accent, c) Size hierarchy: first card accent-bordered + larger, rest surface, d) One card = metric hero (big number), rest = supporting text.

**FOCAL POINT** — Every content slide MUST have ONE dominant element visually 4x+ larger than the next largest. Stat slides: hero number 6-10rem, supporting 1.5-2rem. Centered breathing slides: hero number up to 12rem. Card slides: featured card 40-60% of content area. Data slides: chart is dominant, text supports. Quote slides: quote 2-3rem, attribution 0.85rem. **Data-spotlight with 3+ metrics**: NEVER show all metrics at equal size — pick the MOST impactful number (highest ROI, biggest delta, most surprising stat) and render it as hero (4-6rem), with the remaining metrics as supporting pills or small cards (1.5-2rem) below. Equal-sized metric cards are a strong AI-tell and violate Principle 3. **Bento-grid featured cell**: The featured (larger) cell heading MUST use font-size ≥3.5rem to establish clear visual dominance over side cards. Side card headings at 2.2-2.4rem. If the featured cell heading is below 3.5rem, the bento asymmetry is wasted — it looks like a regular equal grid.

Structure:
1. **Headmatter** — theme, title, fonts, colorSchema, transition, aspectRatio, etc.
2. **Slides** — each separated by `---`, with per-slide frontmatter

For each slide in the outline:

1. **Use the Composition Plan from Step 4.5**: For each slide, look up its assigned archetype. Use `layout: none` and the archetype's HTML skeleton from `references/composition-archetypes.md`. Fill `{{SLOT}}` markers with content from the outline. Apply the preset's shape vocabulary (icon containers, stat display style, label style, photo masks) when rendering elements within the skeleton.

   If no Composition Plan exists (Step 4.5 was not executed for any reason), fall back to the legacy layout selection:
   - Title/intro → `cover`
   - Section break → `section`
   - Bullet points → `default`
   - Single statement → `statement` or `center`
   - Statistic → `fact`
   - Quote → `quote`
   - Comparison → `two-cols`
   - Closing → `end`

   **Content quality checks during writing**: For each slide, verify: (a) word count ≤40 (≤60 for tables), (b) title is an action title (statement, not label), (c) body text uses `font-size ≥1.25rem`, (d) no more than 4 bullets with ≤12 words each, (e) multi-line body text is left-aligned even on centered layouts, (f) line-height 1.3-1.45 for body, (g) if slide contains a chart, apply chart-specific rules from Rule 41 — bar chart Y-axis starts at zero, chart title = insight, ≤5-6 series.

   **Icon-trio title length gate**: Before generating an icon-trio slide, count characters in each ITEM_TITLE. If ANY title exceeds 15 characters, generate the entire icon-trio with `align-items:flex-start;text-align:left` on ALL columns (not just the long one). Long centered titles create the "hourglass" anti-pattern where text wraps unevenly under centered icons. Russian titles frequently exceed 15 chars — always check.

   **Icon-trio density gate**: If each icon-trio item has fewer than 10 words of description, either: (a) expand descriptions to include a supporting stat or outcome (e.g., "94% forecast accuracy"), OR (b) switch to bento-grid archetype which creates more visual weight through an asymmetric featured card. Icon-trio with 5-word descriptions creates 75%+ empty space — structural emptiness, not whitespace.

   **Timeline-horizontal connector requirement**: Every timeline-horizontal slide MUST include a visual connector between phase cards — a horizontal line, numbered dots connected by a line, or SVG arrows. Without a connector, a timeline renders as a disconnected card grid (indistinguishable from icon-trio). Minimum implementation: a 2px accent-colored line running behind/through the cards at their vertical center, with numbered circle markers at each phase.

   **Statistics source citation**: Any specific statistic (percentage, currency amount, count, ratio) MUST include a source attribution. Format: small text below the stat in `font-size:0.7rem; color:var(--color-muted)` — either "(Источник: McKinsey, 2024)" inline or as a footnote. Internal case study data uses "(Внутренние данные)". AI-generated placeholder statistics must be labeled as estimates. Unsourced specific numbers destroy pitch deck credibility.

   **Enforcement rules during writing**:
   - **Gradient type**: Use ONLY the decorative gradient type chosen in Step 4. If "radial-gradient" was chosen: decorative blobs use radial-gradient, card backgrounds use solid colors (no linear-gradient decoration). If "linear-gradient" was chosen: decorative overlays use linear-gradient, no radial-gradient blobs. bg-accent slide may use linear-gradient regardless (structural, exempt).
   - **Text arrows**: NEVER write `→`, `←`, `↑`, `↓`, `⟶`, `➜`, `▶` in visible slide content. Use textual rephrasing, SVG arrows, or timeline archetypes instead.
   - **Italic**: NEVER use `font-style: italic` except in `<blockquote>` elements, attribution lines, and image captions.
   - **Eyebrow label limit (30%)**: Eyebrow labels (0.7rem uppercase letter-spaced text above headings) are permitted on AT MOST 30% of slides in the deck. For a 10-slide deck: max 3 slides with eyebrows. Track usage during writing — when the limit is reached, omit the eyebrow on remaining slides and let the heading speak for itself. Section dividers count toward the limit. Cover and CTA slides are exempt (they have their own label patterns).
   **MANDATORY COUNTER**: Before writing each slide, compute: allowed = floor(total_content_slides × 0.30). Track with a comment before each slide: <!-- eyebrow: N/allowed -->. When eyebrow_count reaches 'allowed', ALL subsequent slides get NO eyebrow label — the heading speaks for itself. Example: 8-slide deck (6 content slides, cover+CTA exempt) → allowed = floor(6 × 0.30) = 1 eyebrow total on content slides. After that 1 eyebrow is used, the remaining 5 content slides have NO eyebrow label.
   - **Background colors**: Use only `var(--bg-base)`, `var(--bg-alt)`, `var(--bg-accent)` as assigned in the Composition Plan. No hardcoded hex background colors.
   - **CRITICAL — bg-accent export fallback**: For slides using `--bg-accent` as full-slide background (cover, CTA), ALWAYS include the hex fallback value in the var() function: `background:var(--bg-accent, #0D9488)` (replace #0D9488 with the actual accent hex from the preset). Slidev's headless PNG export may fail to resolve CSS custom properties on absolutely-positioned inner divs. The fallback ensures the background renders even if variable resolution fails. Apply the same pattern to ALL color variables on bg-accent slides: `color:var(--color-text, #FAF9F6)` for white text on accent backgrounds.

   **Bento side card dedup rule**: When the bento-grid featured cell contains a sub-grid of 3+ numbers (e.g., team breakdown showing 4 departments), the small side cards MUST show DIFFERENT data — growth percentages, period comparisons, or qualitatively distinct metrics (not in the sub-grid). NEVER repeat a number from the featured sub-grid in a side card. This is a direct content duplication anti-pattern visible in exported PNGs.

   **Stat-hero variation rule**: When a deck has 2+ stat-hero slides, they MUST differ structurally. Use at least 2 of: (A) centered hero number + supporting pills below (standard), (B) asymmetric — hero number on left 40%, supporting context stacked on right 60%, (C) comparison — two numbers side by side with a divider, (D) text hero — a statement/phrase as the hero element instead of a number. Track stat-hero usage and enforce alternation.

   **CRITICAL — Visual Rhythm (Principle 1)**: Insert `section`, `statement`, or `fact` breathing slides every 2-3 content slides. If the outline doesn't explicitly include them, use section dividers between major topic shifts, or promote a key insight from a content slide into a standalone statement/fact slide.

   **CRITICAL — Layout Diversity (Principle 2)**: Do NOT repeat the same visual structure (heading position + content arrangement) on more than 2 consecutive slides. Rotate between: hero-left/content-right, cards grid, timeline/stepper, centered hero, asymmetric split, full-bleed visual, comparison table, quote/callout. Track your layout choices — if you used "title top-left + 2-column grid" on slide 3, use something different on slide 4.

   **STRUCTURAL BREAK RULE**: Track the heading position pattern across consecutive content slides. After 2 content slides with "label-top-left + heading-below + grid/cards-below" structure, the 3rd MUST break the pattern using one of: (a) centered layout — heading centered at 3rem+, no label, content centered below (stat-hero, section-divider), (b) visual-dominant — a large metric or visual element occupies the left 40%, text is secondary on the right, (c) heading-only — no eyebrow label above the heading, heading speaks for itself. This rule applies regardless of archetype names — what matters is the VISUAL structure as rendered, not the archetype label. **Total frequency cap**: The label-top-left + heading + grid/cards pattern may NOT appear on more than 40% of content slides total. For a 10-slide deck (8 content), max 3 slides. For a 12-slide deck (10 content), max 4. Count and verify before finalizing slides.md.

   **PATTERN BREAK total frequency**: After generating Composition Plan, count slides using "label-top + heading + grid/cards" structure. If > 40% of content slides use this pattern → MUST replace excess with: a) Full-bleed centered: stat-hero, quote-pull, b) Visual-dominant: one large element left/right, text secondary, c) Minimal: heading + single sentence, generous whitespace, d) Inverted: content top, heading bottom, e) Asymmetric split: 30/70 or 70/30.

2. **Apply animations**:
   - Bullet lists → wrap in `<v-clicks>`
   - Code blocks → use step highlighting `{1|2-3|5}`
   - Key reveals → use `<v-click>`

3. **Style with UnoCSS** classes for spacing, alignment, typography

4. **Add per-slide `<style>`** block — REQUIRED for centered layouts. Reference `references/layout-css-patterns.md` for proven CSS patterns. For `cover`, `section`, `fact`, `end`, `statement`, `center` layouts: ALWAYS include explicit `text-align: center` on `h1`, `p`, and other text elements. For slides with background images: use CSS `background:` on `.slidev-layout` (not frontmatter prop), add `::before` overlay, and set white text colors.

5. **Apply Typographic Drama (Principle 3)**: Key numbers and metrics must use hero scale (4-8em). Statement/fact slides should have 3-5em text minimum. Ensure at least 3 distinct type scales across the presentation. **Typography tier assignment**: Before writing slides, assign each slide to a tier: TIER 1 (hero, 1-2 slides): 4-8rem for the single most important number/statement. TIER 2 (emphasis, 2-3 slides): 3-3.5rem for section headings and key insights. TIER 3 (standard, remaining): 2.2-2.8rem for content headings. Every deck MUST have at least 1 TIER 1 and 2 TIER 2 slides. If all headings are the same size, the deck has failed typographic drama.

6. **Apply Visual Arc (Principle 7)**: Make the climax slide (usually Ask/CTA) the most visually distinct — different background, larger type, unique color treatment. Build visual intensity gradually from calm beginning to dramatic climax.

7. **Apply Vertical Spacing (Principle 11)**: Content should feel vertically balanced. Use flexbox centering or generous padding. Content should not cram to the top leaving empty bottom space.

8. **Apply Decorative Layer (Principle 6) — DECORATION FROM LIBRARY**: When adding decorative elements:
   1. Open references/decoration-library.md
   2. Pick a shape (circle, arc, blob, dot-grid, ring, diamond, line-horizontal)
   3. Pick a behavior (gradient-fill, solid-fill, glow, border-only)
   4. Pick a position (corner-TR, corner-BL, center-behind, edge-right, etc.)
   5. Pick a scale (subtle/medium/bold/hero) based on slide importance
   6. Pick opacity from the preset table (light-theme-* or dark-theme-*)
   7. Assemble HTML by substituting {{PLACEHOLDERS}}
   8. Insert into the slide's background div
   DIVERSITY RULES: No two adjacent slides use the same shape+position combination. Per deck: minimum 3 different shapes, minimum 2 different positions. Rotate: if slide N used corner-TR, slide N+1 uses corner-BL or edge-right. NEVER invent decoration CSS outside the library.

9. **Icon Container Selection (Principle 4)**: For each slide with icons:
   a. Check the deck's icon container history so far
   b. If all previous icons used the same shape → pick a different one
   c. Match shape to archetype: stat-hero/cover-hero → icon-circle; card-mosaic/comparison-table/bento-grid → icon-rounded; icon-trio/timeline → icon-ghost OR icon-circle (alternate)
   d. A deck MUST use at least 2 different icon container shapes (icon-circle, icon-rounded, icon-ghost).
   e. NEVER use 3+ identical icon containers on a single slide — this is the strongest AI-generation tell. On slides with 3+ icons, vary shapes but NOT in a mechanical rotation (circle→rounded→ghost→circle→...). Instead, assign shapes by semantic purpose: icon-circle for primary/featured items, icon-rounded for secondary/supporting, icon-ghost for tertiary/supplementary. This creates visual hierarchy, not just visual variety. Across the deck, vary the assignment — what's "primary" on one slide might use icon-rounded on another. The goal is unpredictability, not pattern.
   f. **Icon container bg-level adaptation**: icon-ghost (transparent bg + thin border) is INVISIBLE on bg-alt backgrounds where the border blends into warm grey. Rule: on bg-alt slides, replace icon-ghost with icon-circle or icon-rounded (both have opaque backgrounds). On bg-accent slides, use icon-container-cover (white-forward). Only use icon-ghost on bg-base slides where the border has sufficient contrast.

### Step 6: Write Custom Components (REQUIRED)

**ALWAYS create these components** for every presentation:

**6a. Icon component (REQUIRED — Principle 4)**: Create `components/Icon.vue` using the template from `references/design-principles.md`. This replaces ALL emoji usage. Include icons relevant to the presentation topic. Use `<Icon name="..." :size="32" color="var(--color-accent)" />` in slides. **CRITICAL: Every icon name used in slides.md MUST have a matching v-if branch in Icon.vue with a complete SVG path.** Before finalizing slides.md, cross-reference all `<Icon name="...">` calls with Icon.vue's v-if branches. If a needed icon is not defined, ADD it with a real SVG path. Never use an icon name that doesn't exist in Icon.vue.

**6b. Custom cards/metrics** (if needed): Create component variants with different visual styles per Principle 5 (Card Variation). Not all cards should look identical.

**6c. Device mockups** (if showing product UI — Principle 9): If the presentation shows phone/laptop screens, create a `components/PhoneMock.vue` with proper wireframe UI — status bar, navigation, colored placeholder blocks, buttons. NEVER create empty gray rectangles with text labels.

**6d. Other custom elements** (animated counters, gradient text, etc.): Create Vue SFCs in `components/`:

```vue
<!-- components/GradientText.vue -->
<template>
  <span class="gradient-text"><slot /></span>
</template>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, var(--color-accent), var(--color-primary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
```

Components in `components/` are auto-registered and available in slides.

**6e. SVG diagrams (Principle 10)**: For flywheel, flow charts, cycles — use inline SVG in slides with proper `<path>` arrows and `<marker>` arrowheads. See `references/design-principles.md` for SVG patterns. NEVER use text arrows (→ ↓ ← ↑) or CSS absolute positioning to simulate diagrams.

### Step 6.5: Picture Placement (conditional)

If `--picture` modifier is present on the generation command, run the Picture Placement Procedure (P-1 through P-7) on the generated project directory. This adds images to the slides before the Visual QA step verifies them.

### Step 7: Visual QA

**CRITICAL — MUST NOT SKIP.** Run the full Visual QA Loop (all 4 phases) for `<project-dir>`. This is mandatory after EVERY generation, regardless of whether `--export` is also specified. Export happens AFTER Visual QA, not instead of it.

### Step 8: Output Summary

After writing all files, print (include Visual QA results):

```
Created Slidev presentation:

  <project-dir>/
    package.json
    slides.md
    uno.config.ts
    styles/
      index.css
    components/       (if created)
      ...
    public/           (if created)
      ...

To run:
  cd <project-dir>
  npm install
  npm run dev
```

## Slide Authoring Rules

1. **v-clicks for bullets**: Always wrap bullet lists in `<v-clicks>` for progressive reveal. **CRITICAL — v-clicks compatibility**: `v-clicks` and `v-click` ONLY work reliably on standard Markdown content (bullet lists, paragraphs) at the top level of a slide, NOT inside custom HTML `<div>` wrappers. If a slide uses a custom HTML layout (flex grids, card containers, custom steppers), DO NOT use `v-clicks` — either present the slide as static, or restructure it to use only Markdown content at the top level with layout applied via global CSS classes on a single root wrapper div.
2. **Step highlighting for code**: Use `{1|2-3|5}` syntax for code walkthroughs
3. **Layout matching**: Choose layout per slide based on content type — don't default everything to `default`
4. **Scoped styles**: Use per-slide `<style>` blocks for slide-specific styling
5. **UnoCSS utilities**: Use utility classes for spacing, flex, grid — avoid inline styles
6. **Presenter notes**: Add `<!-- notes -->` with speaking points when the outline suggests them
7. **No placeholder images**: Don't reference images that don't exist. Use CSS gradients, SVG patterns, or Icon components as visual elements instead
8. **Semantic HTML**: Use proper heading hierarchy within each slide
9. **CRITICAL — Text alignment on centered layouts**: For `cover`, `section`, `fact`, `end`, `statement`, `center` layouts — set `text-align: center` on `h1`, `h2` and single-line elements (date, subtitle, attribution) in the per-slide `<style>` block. **Multi-line body text** (`p`, `li`, `span` with >60 characters or >1 line of content) MUST be `text-align: left` with `max-width: 600px; margin: 0 auto` — left-aligned text in a centered container. NEVER center bullet lists or multi-line paragraphs — this is a major readability anti-pattern. See `references/layout-css-patterns.md`.
10. **CRITICAL — Background images via CSS, not frontmatter**: When adding background images to `cover` or `section` slides, set the background via per-slide `<style>` CSS (`background: url(...) center/cover no-repeat !important` on `.slidev-layout`), NOT via the `background:` frontmatter prop. The frontmatter prop renders on a parent element, but the theme's opaque `background-color` on `.slidev-layout` blocks it. Per-slide CSS overrides the theme directly.
11. **CRITICAL — No emoji icons (Principle 4)**: NEVER use emoji (📱💳⭐🧠📊 etc.) as visual elements. Always use the `<Icon>` component with SVG icons that match the presentation's style. Emoji are inconsistent across platforms and look unprofessional.
12. **CRITICAL — No empty mockups (Principle 9)**: Device mockups (phones, laptops) must contain wireframe-level UI — status bar, navigation, colored placeholder blocks, buttons. NEVER show empty gray rectangles with text labels.
13. **SVG diagrams (Principle 10)**: For flywheels, flow charts, cycles — use inline SVG with `<path>`, `<marker>`, and proper arrowheads. NEVER simulate diagrams with CSS absolute positioning and text arrow characters. **CRITICAL — SVG `<text>` element incompatibility**: NEVER use `<text>` elements inside inline SVG diagrams in Slidev. Chromium's headless export renderer treats SVG `font-size` attributes as document-scale CSS pixels, causing text to render 5–15× larger than expected and overflow the containing shapes. Instead: (A) use a CSS flexbox HTML flow diagram for any diagram requiring text labels (flex column of styled divs with CSS arrows between them), or (B) if SVG shape-only diagrams are needed, keep them label-free. SVG `<path>`, `<rect>`, `<circle>`, `<line>`, `<marker>`, and `<polygon>` elements without `<text>` are safe.
14. **Data viz labels (Principle 8)**: Bar charts must show value labels on key bars. Tables must highlight the hero column. Donut/pie charts must have text labels.
15. **Card diversity (Principle 5)**: Use 2-3 visually distinct card styles (solid, ghost, gradient, glass) — not the same surface style everywhere.
16. **Accent hierarchy (Principle 12)**: Use accent color at 3 intensities: primary (full), secondary (40-60% opacity), ambient (8-15% opacity). Don't use full-intensity accent everywhere.
17. **CRITICAL — Image path discipline**: Never generate `background: url('/images/...')` unless (a) the `--picture` subcommand was invoked and the file exists, OR (b) a CSS-only atmospheric fallback is provided that looks good WITHOUT the image. For cover/section slides without real images, use multi-layer CSS gradients + decorative pseudo-elements to create atmosphere. Example: `background: radial-gradient(ellipse 80% 60% at 30% 40%, rgba(accent, 0.12), transparent 60%), radial-gradient(ellipse 60% 80% at 80% 70%, rgba(secondary, 0.15), transparent 60%), var(--color-bg);`
18. **CRITICAL — Icon name verification**: Before using `<Icon name="X">`, verify that `X` is defined in Icon.vue's `v-if` branches. If a new icon is needed, ADD it to Icon.vue first. Never reference an undefined icon name. Icon.vue should include a `v-else` fallback that renders a visible placeholder (a question-mark circle) so missing icons are immediately obvious during QA.

    **Icon centering**: When an `<Icon>` must appear centered (e.g., in a card header or feature cell), always wrap it in an explicit flex div: `<div style="display:flex;justify-content:center;align-items:center;margin-bottom:8px;"><Icon name="..." /></div>`. Do NOT rely on the card's parent flex/grid container to center an inline SVG element — `<Icon>` renders as `display:inline` by default and will left-align within block containers without an explicit centering wrapper.
19. **CRITICAL — HTML nesting depth limit**: Keep HTML nesting to maximum 3 levels deep inside slides. Slidev's markdown parser fails to render deeply nested HTML — it outputs raw source code instead of rendered content. Flatten structures: instead of `<div><div><div><table>...</table></div></div></div>`, use `<table>` directly at the top level of the slide. Use UnoCSS utility classes on elements themselves instead of wrapping in container divs. When a complex layout is needed, prefer CSS Grid/Flexbox on a single wrapper div rather than nesting multiple wrappers. **Test pattern**: if you count more than 3 opening `<div>` tags before reaching the actual content element, you need to flatten.
20. **CRITICAL — Font size minimums**: Body text minimum `1.25rem` (20px). Headings minimum `2.2rem` (35px). Labels/eyebrows minimum `0.65rem`. Pill badge minimum `0.7rem`. Hero numbers minimum `4rem` (64px). If content doesn't fit — shorten text first, move to speaker notes second, split slide last. NEVER reduce font below minimum.
21. **Maximum items per action/list slide**: A single content slide MUST NOT exceed 4 distinct items or bullet points with descriptions. If an outline section has 5+ items, split across 2 slides with a clear part indicator, or reduce to the 3 most critical items and place others in speaker notes. Action plan slides with 5+ steps are particularly prone to density failure.
22. **Maximum visual blocks per slide**: A content slide should contain at most 4-5 distinct visual elements (cards, chart sections, tables, list groups). If the outline demands more content on one slide, SPLIT it into 2 slides or PRIORITIZE the 3-4 most impactful elements and move details to presenter notes. Exception: a single data table counts as one visual block even if it has many rows.
23. **CRITICAL — Per-slide CSS reliability hierarchy**: When styling slides with custom HTML layouts, follow this reliability order from most to least reliable: (1) Per-slide `<style>` with a SINGLE root wrapper div containing all content — works reliably when all slide content is inside one top-level element. (2) 100% inline styles on every element — most reliable for complex multi-column or deeply nested layouts. (3) Never rely on per-slide CSS classes applying to elements more than 2 nesting levels deep. If a slide requires 3+ levels of nesting, use 100% inline styles instead of CSS class names. Note: this reliability constraint is separate from the nesting depth rendering limit (Rule 19) — both apply simultaneously.
24. **CRITICAL — `end` layout background override**: The `@slidev/theme-default` `end` layout applies an opaque dark background that cannot be overridden without `!important`. To set a custom background on an `end` slide, use BOTH: `background: <color> !important; background-color: <color> !important;` in the per-slide `<style>` block. Setting only `background` is insufficient. Also explicitly set `color` on all child text elements, as the theme defaults to white text for the dark end layout.
25. **CRITICAL — Full-bleed slide layout height guarantee**: When building custom full-bleed slides using a background div + content div pattern, NEVER use `height:100%` on the content wrapper. Slidev injects padding into `.slidev-layout` that makes `height:100%` smaller than the full viewport, pushing `justify-content:center` content downward. Instead, use `position:absolute;inset:0` on BOTH the background and content wrappers:
    ```html
    <!-- Background layer -->
    <div style="position:absolute;inset:0;z-index:0;overflow:hidden;">
      <!-- decorative elements -->
    </div>
    <!-- Content layer -->
    <div style="position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;justify-content:center;padding:48px 80px;">
      <!-- slide content -->
    </div>
    ```
    Also set `padding:0 !important; overflow:hidden` on `.slidev-layout` in the per-slide `<style>` block as a supplementary safeguard.
26. **CRITICAL — Tag pill / accent chip on dark backgrounds**: `rgba(accent, 0.10–0.18)` background ONLY works on light/white backgrounds. On dark backgrounds (luminance < 30%), this formula produces a muddy dark tint — use one of these alternatives instead: (A) `background: rgba(255,255,255,0.08)` + `border: 1.5px solid rgba(accent, 0.60)` — "ghost chip with bright border"; (B) raise opacity to `rgba(accent, 0.25–0.30)` on dark slides; (C) fully saturated `background: rgba(accent, 1.0)` for small micro-chips. NEVER use `rgba(accent, 0.10–0.18)` as a chip background when the slide background is navy, charcoal, or any color with luminance below 25%.
27. **MANDATORY — Background variation in 3+ consecutive same-chapter content slides**: When 3+ content slides of the same type appear in sequence (e.g., three value slides), each slide MUST differ from its neighbors on at least one background dimension. Apply at minimum ONE of: (A) Progressive background lightening — shift 2–4% luminance per slide; (B) Decorative motif rotation — each slide gets a different motif (diagonal lines, dot grid, arc ring — never the same motif on two adjacent slides); (C) Accent blob corner rotation — place decorative blobs in different corners across the sequence. Identical backgrounds on 3+ consecutive content slides = visual rhythm failure.
28. **CRITICAL — Ghost decorative number opacity enforcement**: When using large background numerals ("01", "02") as decorative elements on content slides, apply the hue proximity rule (Principle 6): on warm peach/cream backgrounds, pink ghost numbers require minimum opacity **0.20** (same temperature family). On warm backgrounds, use navy ghost numbers at minimum **0.10** opacity instead — navy provides stronger contrast than same-hue pink. Any ghost number at opacity below 0.15 on a warm background will be invisible in exported PNGs. **Additional luminance rule**: On teal or medium-luminance bg-accent (luminance 20–40%), white ghost numbers require minimum opacity **0.16**. On dark (navy, charcoal) bg-accent (luminance <15%), minimum is 0.10. On light bg-accent (rare), minimum is 0.25. If you cannot meet the minimum opacity without it looking too heavy, remove the ghost number entirely rather than keeping an invisible element.
29. **CRITICAL — Override blockquote default styling**: `@slidev/theme-default` applies an opaque dark background (`background: <dark color>`) and a left accent border (`border-left: 4px solid var(--slidev-theme-primary)`) to ALL `<blockquote>` elements. Any slide using `<blockquote>` for a quote or statement will render as a "callout box" — not clean typographic text. ALWAYS add the following reset to `styles/index.css` for every presentation:
    ```css
    .slidev-layout blockquote {
      background: transparent !important;
      border-left: none !important;
      border: none !important;
      padding: 0 !important;
      margin: 0 !important;
      color: inherit !important;
    }
    ```
    Additionally, for centered layouts (statement/center/fact/end), set `text-align: center` explicitly on the `<blockquote>` element itself AND on every `<p>` inside it — flex container centering alone is insufficient because `<blockquote>` renders as a block element that can inherit left-alignment from theme selectors.
30. **CRITICAL — Content grid vertical centering (two-layer pattern)**: When a content slide uses `position:absolute;inset:0` layout with a label + heading + content grid/list, DO NOT put `justify-content:center` on the outer wrapper div. This centers the entire column (heading + content) as a block, which pulls the visual center upward by the heading height (~100-120px) and leaves an empty gap at the bottom. Instead, use the **two-layer pattern**:
    - Outer wrapper: `position:absolute;inset:0;z-index:1;display:flex;flex-direction:column;padding:44px 64px 44px` — NO `justify-content`
    - Label + heading block: static top-anchored, no special flex behavior
    - Content grid/list container: `flex:1;display:flex;flex-direction:column;justify-content:center` — centers the CONTENT within the space BELOW the heading
    ```html
    <div style="position:absolute;inset:0;z-index:1;padding:44px 64px 44px;display:flex;flex-direction:column;">
      <div style="...label styles...">LABEL</div>
      <h1 style="...heading styles;margin:0 0 20px;">Heading</h1>
      <!-- Content is centered in the remaining space -->
      <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:12px;">
        <!-- cards/rows/items here -->
      </div>
    </div>
    ```
    This ensures the heading anchors near the top while the content block centers in the remaining space, producing vertically balanced slides with content visible throughout the middle 60% of the slide height.

    **Grid rows for 4+ item lists (PREFERRED over space-evenly)**: When a content slide has a heading consuming >20% of slide height AND the content area contains 4+ items (cards, rows, list items), use `display:grid;grid-template-rows:repeat(N,1fr)` on the content container (where N = number of items), with `align-items:stretch`. Then give each item `height:100%;display:flex;align-items:center` so it fills its grid cell. This guarantees equal distribution regardless of item content size.

    `justify-content:space-evenly` is **NOT reliable** for vertical item lists: it only distributes whitespace BETWEEN auto-height items without stretching them — items cluster in the upper portion with a gap at the bottom. Reserve `space-evenly` only for horizontal flex containers where items have equal natural widths.

    ```html
    <!-- ✅ CORRECT: Grid 1fr rows — items stretch to fill available height -->
    <div style="flex:1;display:grid;grid-template-rows:1fr 1fr 1fr 1fr;gap:12px;align-items:stretch;">
      <div style="display:flex;align-items:center;gap:16px;background:...;border-radius:14px;padding:0 24px;">
        <!-- icon + text — no fixed padding-top/bottom; height comes from grid row -->
      </div>
      <!-- repeat for each item -->
    </div>

    <!-- ❌ WRONG: flex+space-evenly leaves gap at bottom when items have auto heights -->
    <div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly;gap:12px;">
      <div style="...;padding:20px 24px;">...</div>
    </div>
    ```

31. **CRITICAL — Blank slide prevention (separator + frontmatter discipline)**: When a slide requires per-slide frontmatter (`layout`, `transition`, `class`, etc.), the frontmatter block MUST immediately follow the `---` separator with NO blank lines, HTML comments, or other content between the `---` and the opening `---` of the frontmatter. Placing a comment or blank line between them creates TWO slides — one blank and one with content. **Correct pattern:**
    ```markdown
    ---
    layout: section
    ---

    <!-- comment about this slide goes HERE, after the frontmatter -->
    Slide content here
    ```
    **Wrong pattern (creates blank slide):**
    ```markdown
    ---

    <!-- comment about next slide -->
    ---
    layout: section
    ---
    ```
    For full-HTML custom slides using `layout: none`, consolidate the separator and frontmatter into a single block with the HTML content immediately following.

32. **CRITICAL — statement/fact layout CSS override limitation**: The `@slidev/theme-default` `statement` and `fact` layouts apply font sizes, text alignment, and colors with high-specificity CSS selectors that per-slide `<style>` blocks cannot reliably override. Symptoms: setting `h1 { font-size: 2.5em }` in a per-slide style for a `statement` slide renders at the theme default (~1em) instead. **Fix**: For any `statement` or `fact` slide requiring custom typography or visual treatment beyond what the theme provides, use `layout: none` with a full custom HTML div using inline styles. Reserve `layout: statement` and `layout: fact` ONLY when the theme's default rendering is acceptable.

33. **Non-default theme exploratory render**: For non-default themes, perform an exploratory render before full generation. Write a minimal 2-slide test (`cover` + `default` layout), export PNGs, check for unexpected styling. If the theme applies unusual defaults (different font rendering, unexpected background colors, unusual spacing), note them and adapt the generation accordingly. This prevents wasting a full generation on a theme that behaves unexpectedly.
34. **Theme + preset interaction**: When using `--theme` with `--preset`, the preset's CSS block takes precedence over theme defaults. Theme provides base styling; preset provides customization layer on top. If the preset was designed for `theme: default`, it may not work correctly with other themes — warn the user if the preset's `theme` field doesn't match the `--theme` flag.

## Design Quality Rules (powered by /frontend-design + Design Principles)

These rules combine `/frontend-design` aesthetic principles with the Gamma-level design principles from `references/design-principles.md`. Apply in ALL modes.

### Aesthetic Foundation
1. **Never repeat aesthetics**: Each unique-mode generation should feel different — vary dark/light, geometric/organic, warm/cool. No design should look the same across generations
2. **Typography drives design**: Font choice sets the tone. Choose fonts that are beautiful, unique, and characterful. Pair a distinctive display font with a refined body font. NEVER default to generic AI-favorite fonts
3. **Color with conviction**: Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Ensure accent color has sufficient contrast against backgrounds and text. Avoid cliched color schemes
4. **Whitespace is design**: Don't overcrowd slides. Generous negative space OR controlled density — both work when intentional
5. **Consistent visual language**: Once you choose a visual direction (e.g., rounded vs sharp, dense vs airy), maintain it across all slides with precision
6. **Background depth**: Create atmosphere and depth — gradient meshes, noise textures, geometric patterns, layered transparencies, grain overlays. Never default to flat solid colors
7. **Transition coherence**: Match transition style to overall aesthetic — don't mix competing motion styles
8. **No AI slop**: Never use generic AI-generated aesthetics — overused fonts (Inter, Roboto), cliched purple-on-white gradients, predictable layouts, cookie-cutter patterns, emoji as icons, empty device mockups, text-arrow diagrams. Every presentation must feel genuinely designed for its specific content and context
9. **Spatial intentionality**: Use unexpected layouts where appropriate — asymmetry, overlap, grid-breaking elements. Avoid predictable, evenly-spaced component patterns

### Presentation-Specific Quality (from Design Principles)
10. **Visual rhythm**: Alternate dense content slides with breathing slides (section/statement/fact). Never 3+ dense slides in a row. See Principle 1.
11. **Layout diversity**: Every slide must be visually distinguishable from its neighbors. Rotate 4-5 different layout structures per deck. See Principle 2.
12. **Typographic drama**: Use 3+ distinct type scales (hero 4-8em, heading 1.8-2.5em, body 0.85-1.1em). Key numbers must be oversized. See Principle 3.
13. **Professional iconography**: SVG icons via `<Icon>` component only. Zero emoji. See Principle 4.
14. **Card differentiation**: 2-3 visually distinct card styles per presentation. See Principle 5.
15. **Decorative personality**: 1-2 decorative motifs on 30-50% of slides. See Principle 6.
16. **Visual narrative arc**: Build visual intensity toward the climax (Ask/CTA). See Principle 7.
17. **Data viz polish**: Charts with value labels, highlighted hero columns, SVG with labels. See Principle 8.
18. **Realistic mockups**: Device frames with wireframe UI, not empty boxes. See Principle 9.
19. **Vector diagrams**: SVG diagrams with proper arrows, not CSS+text. See Principle 10.
20. **Vertical balance**: Content centered or well-distributed, not crammed to top. See Principle 11.
21. **Accent weight system**: 3 levels of accent intensity (primary/secondary/ambient). See Principle 12.
22. **Content density limit**: Max 4-5 visual blocks per slide. If a slide needs 6+ elements, split into 2 slides or move secondary details to presenter notes. Dense information walls overwhelm the audience and shrink text to unreadable sizes.
23. **Hero metric prominence**: When a slide shows 3-4 key metrics, DON'T make them all equal-sized cards. **Card-mosaic hierarchy**: In any 4-card equal grid (card-mosaic archetype), one card MUST be visually promoted — use card-accent style with 3rem heading vs 2.2rem on others, or span 2 columns. Equal-weight 2×2 grids with identical styling are a strong AI-tell. Pick the MOST impactful metric, make it hero-sized (centered, 3-6em), place the rest as smaller supporting elements below. If all metrics are equally important, use 2.5-3em minimum — never smaller than the heading text.
24. **Visible decoration**: Decorative elements (grain, scanlines, dot grids, blobs) must be visible in exported PNGs. Minimum opacity: 0.08-0.15 for patterns. If a decorative element isn't noticeable in a static screenshot, increase its opacity or size. Better 2-3 clearly visible decorative touches than 10 invisible ones.
25. **Font discipline**: Maximum 2 visual font identities per presentation (heading + body). Numbers, labels, and hero text use the heading font — never a third font. Check font number blacklist for number-heavy decks. See Font Number Blacklist in Mode: Unique.
26. **Composition-aware layouts**: Use the Composition Plan (Step 4.5) to select archetype for each slide. Never default to the same card-grid layout. Each slide uses a named archetype from `references/composition-archetypes.md`. Entropy rule: no archetype repeats within a 4-slide window.
27. **Shape variety**: At least 20-30% of visual elements should be non-rectangular: circle icon containers, pill badges, typographic heroes without card wrappers. Check the preset's shape vocabulary and apply it. All-rectangles = design failure.
28. **CTA color smoothness**: CTA slide background shares at least one color channel with the preceding slide. Penultimate slide begins the color transition. See Principle 7 CTA transition rule.
29. **Word count limits**: Maximum 40 words per content slide. 75+ words = CRITICAL "wall of text" — rewrite immediately. 150+ words = FORBIDDEN (document, not slide). Maximum 12 words per bullet point. Maximum 6 text lines per slide. Exception: table/comparison slides allow up to 60 words. If content exceeds limits, split across slides or move to speaker notes.
30. **Action titles**: Every slide title MUST be a statement/insight, not a label. "Выручка выросла на 23%" not "Финансовые показатели". "18 лет опыта в строительстве МО" not "О компании". Ghost Deck test: reading only slide titles in sequence must tell a coherent story. Exception: cover and CTA slides may use short titles.
31. **Generic phrase prohibition**: These phrases are BANNED as slide titles: "Ключевые выводы", "Обзор", "В заключение", "Наше решение", "Наш подход", "О нас", "Введение", "Итоги", "Резюме", "Key Takeaways", "Overview", "In Conclusion", "Our Approach", "Summary". Test: could any competitor send this presentation changing only the logo? If yes — titles are too generic.
32. **All-caps eyebrow labels limit**: All-caps uppercase labels (`text-transform: uppercase; letter-spacing`) allowed on max 30% of slides. Others use normal-case with accent color, or no label. Labels must be specific: "Q1 2025" not "ОБЗОР", "МОСКВА · 120 ТОЧЕК" not "КОНТЕКСТ".
33. **"Thank You" ending prohibition**: Last slide NEVER ends with "Спасибо", "Thank You", or "Вопросы?". Last slide = specific CTA with action and contact info. Use `cta-warm` archetype.
34. **Bold/emphasis limits**: Maximum 10-15% of text may be bold. Maximum 1 emphasis technique per element (bold OR accent color OR larger size — not all three simultaneously). Over-emphasis defeats emphasis.
35. **Line-height**: Body text `line-height: 1.3–1.45`. Headings `line-height: 1.05–1.15`. Values below 1.2 (too tight) or above 1.5 (too loose) for body text = WARNING.
36. **Sub-bullet depth limit**: Maximum 2 levels of bullet nesting. Sub-sub-bullets are forbidden. If hierarchy deeper than 2 is needed, restructure as cards, separate blocks, or split across slides.
37. **AI color blacklist**: These colors are BANNED as primary/dominant accent: any hue in range 240-290 (purple-indigo-violet spectrum) at saturation >50%. Specific examples: `#6366F1` (indigo-500), `#8B5CF6` (violet-500), `#A855F7` (purple-500), `#06B6D4` (cyan-500). Acceptable as secondary/ambient (≤10% coverage) but never as primary palette color. These are statistically the most common AI-default colors (Tailwind `bg-indigo-500` training bias).
38. **60-30-10 color distribution**: 60% dominant color (background), 30% secondary (text, surfaces, cards), 10% accent (CTA, key metrics, highlights). Maximum 4 distinct colors in entire presentation palette. See Principle 12 expansion in design-principles.md.
39. **WCAG contrast ratios**: Body text (<18pt) requires minimum 4.5:1 contrast ratio against background (WCAG AA). Large text (≥18pt or 14pt bold) requires minimum 3:1. UI elements (borders, icons) require 3:1. Do not round — 4.47:1 FAILS. Verify in QA-4 visual review.
40. **Colorblind-safe data encoding**: Prohibited pairs for data visualization: red+green, green+brown, blue+purple, green+black. Recommended alternative for binary pairs: blue+orange. Never use color as the ONLY differentiator — always add shape, pattern, or label.
41. **Chart-specific rules**: Bar charts: Y-axis MUST start at zero. Line charts: may truncate Y-axis. Pie/donut: max 5-6 segments (rest → "Other"), largest at 12 o'clock clockwise descending, donut preferred over pie. All charts: max 5-6 series/lines, no legends (label directly on data), chart title = insight not description ("Revenue grew 23%" not "Revenue chart"). 3D effects and dual Y-axes FORBIDDEN. See Principle 8 expansion.
42. **Statistics source citations**: Every statistic from external sources needs footnote or inline citation: `(source: McKinsey, 2024)`. Unsourced large numbers are a hallucination tell.
43. **Whitespace minimum**: Minimum 30% of slide area must be whitespace (empty space without text, icons, or cards). Padding from edges minimum 44px. Gap between elements minimum 16px. Maximum 2 large/dominant elements per slide.
44. **Image style consistency**: All photos in a presentation must share unified visual style — same color temperature, contrast level, and compositional approach. Do not mix photos and illustrations. If images vary, apply CSS filter to harmonize (e.g., `filter: saturate(0.8) contrast(1.1)` on all images).
45. **CRITICAL — Inline style property whitelist**: Slidev's markdown-to-Vue parser FAILS to render HTML blocks containing deeply nested inline `style="..."` attributes with CSS variable references like `var(--color-accent)`. The parser emits these as raw text instead of DOM elements. **Rule**: Inline `style="..."` attributes may ONLY contain structural layout properties: `position`, `inset`, `top/right/bottom/left`, `z-index`, `display`, `flex-direction`, `flex`, `align-items`, `justify-content`, `gap`, `padding`, `margin`, `width`, `height`, `max-width`, `min-height`, `grid-template-columns`, `grid-template-rows`, `overflow`. ALL visual properties — `color`, `background`, `border`, `border-radius`, `font-size`, `font-weight`, `font-family`, `opacity`, `box-shadow`, `text-transform`, `letter-spacing`, `line-height` — MUST be set via CSS classes in per-slide `<style>` blocks. Each slide defines unique class names (e.g., `.s2-hero`, `.s2-card`, `.s2-pill`) and applies them to elements. This separation ensures Slidev's parser processes the HTML as layout, not as text.
47. **CRITICAL — layout:none root div MUST use `position:absolute;inset:0`**: When a slide uses `layout: none`, the root div MUST be positioned with `position:absolute;inset:0` — NEVER use `position:relative;width:100%;height:100%`. With Slidev's none layout, the parent container has no explicit height, so `height:100%` resolves to 0px and content is invisible. The proven working pattern: `<div class="sN-root">` with `.sN-root { position: absolute; inset: 0; overflow: hidden; }` in the `<style>` block. Additionally, EVERY slide MUST have its own `<style>` block containing at minimum `.slidev-layout { padding: 0 !important; overflow: hidden; }` and all slide-specific visual classes.
46. **CRITICAL — Global frontmatter IS slide 1**: In Slidev, the global frontmatter (`---\ntheme:...\n---`) defines BOTH the global config AND slide 1's frontmatter. Content placed immediately after this block IS slide 1's content. **The first slide's content MUST come IMMEDIATELY after the global frontmatter's closing `---`** — no extra `---` separator, no blank lines with comments between them. `layout: none` in global frontmatter is correct (it sets slide 1's layout). The wrong pattern that creates a blank slide: `---\nglobal config\n---\n\n---\nlayout: none\n---\n<content>` — this puts a blank slide before the actual content. The correct pattern: `---\ntheme: default\nlayout: none\n---\n\n<slide 1 content>\n\n---\nlayout: none\n---\n\n<slide 2 content>`.

## Output Directory

- If user specifies a directory, use it
- Otherwise create a directory named after the presentation title (kebab-case)
- If generating a demo for a preset, use `demo-<preset-name>/`
