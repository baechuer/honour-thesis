---
name: slidecraft
description: Use when generating a two-layer presentation from a slide outline. Generates AI background images (text-free) via configurable APIs (Polza.ai default), then assembles a Slidev project with HTML/CSS text overlay. Supports preset styles, custom style descriptions, reference-based consistency, dual-layer QA scoring, and all management subcommands.
argument-hint: "[--help | --edit [dir] <comment> | --polish=N [dir] | --compare <dir1> <dir2> | --notes [dir] | --learn=N | --create-preset <name> | --export <format> [dir] | --dev [dir] | --responsive [dir] | --picture [auto|paths...] [dir] | --preset <name> | --provider <name> | --model <id> | --no-ref | style: <desc>] <outline or file path>"
---

# SlideCraft — Two-Layer Presentation Generator

You generate complete two-layer presentations from slide outlines. Every generation produces:
1. **AI-generated PNG backgrounds** — visual layer with no text, empty zones reserved for text
2. **Slidev HTML/CSS text overlay** — crisp, browser-rendered text positioned precisely over those zones

The separation of layers eliminates AI text garbling: AI handles only the visual canvas, Slidev handles all typography with pixel-perfect quality.

## References

Before generating, internalize these references:

- `references/providers.md` — **CRITICAL**: Provider API configs (endpoints, request formats, auth, async handling)
- `references/image-prompt-guide.md` — **CRITICAL**: How to compose text-free prompts for background generation (no text in prompts, empty zone specification, zone background requirements)
- `references/layout-plan-format.md` — **CRITICAL**: JSON schema for zone planning, zone types, position format, prompt_hint generation, coordinate-to-CSS mapping, zone_strategy presets, per-role default zone layouts
- `references/text-overlay-rules.md` — **CRITICAL**: CSS absolute positioning over background-image, z-index layering, Slidev layout:none requirements, v-clicks compatibility in zone divs, text contrast guarantees, font rendering, background mismatch remediation
- `references/design-principles.md` — **CRITICAL**: 12 design quality principles (visual rhythm, layout diversity, typography drama, icon system, card variation, decorative layer, visual arc, data viz, mockups, SVG diagrams, spacing, accent hierarchy). Apply in ALL modes
- `references/layout-css-patterns.md` — **CRITICAL**: CSS patterns for text overlay, zone div patterns, z-index layers, background image CSS
- `references/scoring-subroutine.md` — Dual-layer slide scoring (1-10 on 6 axes: Visual Impact, Layout Precision, Typography Quality, Color Conviction, Content Clarity, Layer Harmony)
- `references/content-review-subroutine.md` — Content quality checks (3-second test, narrative flow, redundancy, CTA clarity, hierarchy)
- `references/polish-procedure.md` — `--polish=N` iterative improvement cycle for two-layer slides
- `references/ab-testing.md` — A/B variant generation for weak slides (image layer or text layer targeted)
- `references/design-memory.md` — Design pattern memory (read/write protocol, `~/.claude/slidecraft-design-memory.json`)
- `references/compare-procedure.md` — `--compare` side-by-side scoring on composite exports
- `references/notes-procedure.md` — `--notes` speaker notes generation
- `references/preset-format.md` — Two-layer preset specification (visual + typography fields)
- `references/responsive-check.md` — `--responsive` aspect ratio check procedure
- `references/slidev-syntax.md` — Slidev markdown syntax reference
- `references/slidev-layouts.md` — Layout selection guide (only `layout: none` is used in SlideCraft)
- `references/slidev-animations.md` — Animations & transitions (v-clicks compatible inside zone divs)

## Input Parsing

Parse the user's input to determine the subcommand or generation mode.

### Global Flags (combine with any mode)

- `--provider <name>` — API provider: `polza` (default), `openai`, `custom`
- `--model <id>` — Model ID (default: `google/gemini-3.1-flash-image-preview` for Polza)
- `--no-ref` — Disable reference-based style consistency (generate each slide independently)
- `--base-url <url>` — Custom provider endpoint URL
- `--api-key-env <VAR>` — Environment variable name for the API key

### Subcommands (handle before anything else)

---

**`--help`**: Display usage help and stop.

```
SlideCraft — Two-Layer Presentation Generator

Usage:
  /slidecraft <outline or file>                        Generate with unique design
  /slidecraft --preset <name> <outline>                Generate with preset style
  /slidecraft style: <desc> <outline>                  Generate with custom style
  /slidecraft --edit [dir] <comment>                   Edit existing presentation
  /slidecraft --polish=N [dir]                         Iterative quality improvement (N cycles)
  /slidecraft --compare <dir1> <dir2>                  Compare two presentations
  /slidecraft --notes [dir]                            Generate speaker notes
  /slidecraft --learn=N                                Self-improving loop (N cycles)
  /slidecraft --create-preset <name>                   Create a new preset
  /slidecraft --export <format> [dir]                  Export (html|pdf|png2pdf|pngs|png_N)
  /slidecraft --dev [dir]                              Launch dev server
  /slidecraft --responsive [dir]                       Check 4:3 rendering
  /slidecraft --picture [auto|paths...] [dir]          Add photos to non-text zones
  /slidecraft --help                                   Show this help

Provider flags (combinable with any mode):
  --provider <name>         polza (default), openai, custom
  --model <id>              Model ID for the provider
  --no-ref                  Generate without style references
  --base-url <url>          Custom provider endpoint
  --api-key-env <VAR>       API key env variable name
```

Stop here — do not proceed to generation.

---

**`--create-preset <name>`**: Interactive two-layer preset creation wizard.

1. Extract preset name from arguments. If missing, ask for one (kebab-case).
2. Ask 9 questions **ONE AT A TIME**, waiting for each answer:
   - **Mood**: "What mood? (professional, playful, dramatic, calm, futuristic, elegant, bold, minimal)"
   - **Color palette**: "Primary palette? (dark navy, warm cream, vivid gradient, monochrome...include hex values if known)"
   - **Accent color**: "Accent color? (#ff6b35, electric blue, warm coral...)"
   - **Typography**: "Font personality? (geometric & modern, humanist & warm, classic & refined, editorial, technical)"
   - **Content density**: "Content density? (minimal with whitespace, balanced, information-dense)"
   - **Background textures**: "Background textures? (gradient mesh, geometric patterns, clean flat, frosted glass, subtle noise)"
   - **Slide transition**: "Slide transitions? (fade, slide-left, slide-up, none)"
   - **Zone strategy** (NEW): "Default text zone layout? (text-left-60: text on left 60% with visual right 35%, text-center: centered text in middle, text-bottom-40: visual top 55% with text bottom 40%, text-split-50-50: left column text / right column visual)"
   - **Text contrast mode** (NEW): "Text on zones: light text on dark zones or dark text on light zones? (light-on-dark / dark-on-light)"
3. Synthesize answers into a two-layer preset with:
   - **Visual layer**: style suffix for AI prompts (concrete colors, background treatment, decoration style), zone_strategy value, text_contrast_mode
   - **Text layer**: font pair (Google Fonts), CSS variables (accent, bg, text, surface), transition, colorSchema
   - Write per `references/preset-format.md`.
4. Based on save location (ask if not provided):
   - **Global**: Create `~/.claude/slidecraft-presets/` if needed, write `<name>.preset.md` there
   - **Local**: Create `./.slidecraft-presets/` if needed, write `<name>.preset.md` there
5. Generate demo presentation using `assets/demo-outline.md` with that preset (run the full pipeline, Steps 1–7).
6. **Dual QA** — run Phase 1 image QA and Phase 2 composite QA. Print dual score report with 6-axis scoring. If overall average < 7, print: "Preset scored below 7 — consider refining style parameters or zone strategy."
7. Print summary: preset path (global vs local), demo output path, QA results, how to use (`/slidecraft --preset <name> <outline>`).

Stop here — do not proceed to generation.

---

**`--learn=N`**: Self-improving learning loop. Parse N from argument (e.g., `--learn=5`). Default N=3, max N=10.

1. **Generate N diverse outlines** upfront. Vary: topic domain (tech, healthcare, finance, education, creative), presentation format (pitch, lecture, report, onboarding, keynote), slide count (8–16 slides), tone (formal, casual, data-heavy, storytelling). Save each to a working `edu_NN/learn_N/outline.md`.
2. **For each outline, run the full pipeline** (Steps 1–7):
   - Generate layout-plan.json, prompts.json
   - Generate AI background PNGs (Phase 1)
   - Assemble Slidev project
   - Install dependencies, run dual QA (Phase 2)
3. **Score each composite output** via `references/scoring-subroutine.md` — 6 axes. Write `score-report.md`.
4. **Analyze patterns**: Which zone strategies produced cleanest empty zones? Which prompt structures preserved zone boundaries? Which font pairings scored highest on Typography Quality? Which zone_strategies had the best Layout Precision scores?
5. **Write `improvements.md`** with findings for both image-layer prompt strategies and text-layer positioning strategies. Format: category (image|text|both), severity (critical|major|minor), proposed change, before/after.
6. **Apply improvements**: modify prompt construction strategy and zone placement heuristics for the next iteration.
7. **Write design memory entry** (`references/design-memory.md` write protocol) with both `visual` and `text` sub-objects. Entry type: `success` if avg ≥ 7, `failure` if avg < 5.
8. Print iteration summary: score delta, what changed, what improved.
9. After all N iterations, write `edu_NN/summary.md` with score progression, cumulative changes, and observed patterns. Commit learning artifacts.

Stop here — do not proceed to generation.

---

**`--polish=N [dir]`**: Iterative dual-layer improvement cycle. Follow `references/polish-procedure.md`. Remediation table:

| Axis | Source layer | Action |
|------|-------------|--------|
| Visual impact | Image | Regenerate PNG with A/B variant prompts |
| Layout precision | Both | Adjust zone coordinates in layout-plan.json → update prompt_hint → regenerate PNG → update CSS |
| Typography quality | Text | Adjust font sizes, weights, colors, line-height in slides.md CSS |
| Color conviction | Image | Regenerate PNG with A/B variant palettes |
| Content clarity | Text | Restructure text, simplify bullets, adjust hierarchy |
| Layer harmony | Both | Analyze which layer causes dissonance → targeted fix |

Max 5 polish cycles. Early exit if overall score ≥ 9. Auto-capture preset if final score ≥ 9. Stop here — do not proceed to generation.

---

**`--compare <dir1> <dir2>`**: Compare two presentations side-by-side. Follow `references/compare-procedure.md`. Comparison is performed on composite exports (Phase 2 output — final composite PNG with both layers merged). Score on all 6 axes. Output:

```
| Slide | Axis              | Dir1 | Dir2 | Delta |
|-------|-------------------|------|------|-------|
| 1     | Visual impact     | 8    | 7    | +1    |
| 1     | Layer harmony     | 9    | 6    | +3    |
...
| Overall               | 7.8  | 6.5  | +1.3  |
```

Stop here — do not proceed to generation.

---

**`--notes [dir]`**: Generate speaker notes. Follow `references/notes-procedure.md`. Add 4-point speaker notes per slide (Opening / Key message / Details / Transition). Stop here — do not proceed to generation.

---

**`--responsive [dir]`**: Check presentation at 4:3 aspect ratio. Follow `references/responsive-check.md`. Switch `aspectRatio` to `4/3`. Verify: zone divs don't overflow, background PNGs scale correctly (check letterboxing), text remains readable. Fix CSS if needed. Stop here — do not proceed to generation.

---

**`--dev [dir]`**: Launch Slidev dev server for an existing SlideCraft presentation.

1. **Resolve project directory** (see Directory Auto-Detection below).
2. **Install dependencies** if `node_modules/` doesn't exist: run `npm install` in the project directory.
3. **Start dev server** using this exact pattern (slidev reads stdin for keyboard shortcuts and exits on EOF):
   ```bash
   cd <project-dir> && (sleep infinity | npx slidev) 2>&1
   ```
   Run via Bash with `run_in_background: true`.
4. **Wait for ready**: use the Read tool to read the background task's output file and check for the URL.
5. **Report**: print the local URL (e.g. `http://localhost:3030/`) once the server is ready. The server continues running in the background.

Stop here — do not proceed to generation.

---

**`--export <format> [dir]`**: Export the composite presentation.

Formats:
- `html` — Static SPA via `npx slidev build --base /` → output in `<dir>/dist/`
- `pdf` — PDF via Slidev's built-in export (may lose CSS backdrop-filter effects)
- `png2pdf` — Pixel-perfect PDF: export PNGs first, then Python Pillow assemble
- `pngs` — Individual composite PNG files per slide
- `png_N` — Single slide N as PNG

Procedure:

1. **Resolve project directory** (see Directory Auto-Detection below).
2. **Install dependencies** if `node_modules/` doesn't exist: run `npm install`.
3. **Ensure playwright-chromium** for `pdf`, `png2pdf`, `pngs`, `png_N`: run `npx playwright install chromium`.
4. **Run export command**:
   - `html`: `cd <dir> && npx slidev build --base /`
   - `pdf`: `cd <dir> && npx slidev export --output slides.pdf`
   - `png2pdf`: Two-stage export:
     1. `cd <dir> && npx slidev export --format png --output slides-tmp`
     2. Ensure Pillow: `pip install Pillow 2>/dev/null || pip3 install Pillow 2>/dev/null`
     3. Python script:
        ```python
        from PIL import Image
        import os, re
        png_dir = 'slides-tmp'
        files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
        files.sort(key=lambda x: int(re.match(r'(\d+)', x).group()))
        images = [Image.open(os.path.join(png_dir, f)).convert('RGB') for f in files]
        images[0].save('slides.pdf', save_all=True, append_images=images[1:],
                       resolution=150.0, quality=95)
        for img in images: img.close()
        ```
     4. `rm -rf <dir>/slides-tmp`
   - `pngs`: `cd <dir> && npx slidev export --format png --output slides`
   - `png_N`: `cd <dir> && npx slidev export --format png --range N --output slide-N`
5. **Report**: print output file/directory path and format.

Stop here — do not proceed to generation.

---

**`--edit [dir] <comment>`**: Edit an existing SlideCraft presentation based on a free-text comment.

**Step 1: Resolve project directory** (see Directory Auto-Detection below).

**Step 2: Read all project files**: `layout-plan.json`, `slides.md`, `prompts.json`, `meta.json`, `styles/index.css`, `components/Icon.vue`.

**Step 3: Detect edit type** using this decision tree:

1. Does the edit move, resize, or reposition text zones? → **BOTH** (full cycle)
2. Does the edit change visual style (colors, mood, decorative elements, background) without moving zones? → **VISUAL** (PNG only)
3. Does the edit change text content, font sizes, or text styling without moving zones? → **TEXT** (Slidev layer only)

**Edit type examples:**
```
"Change heading on slide 3"            → TEXT  — update HTML in slides.md, Phase 2 QA only
"Make font size bigger"                → TEXT  — update CSS, Phase 2 QA only
"Make background brighter on slide 5"  → VISUAL — modify prompt, regenerate PNG, Phase 1+2 QA
"Move bullets to the right"            → BOTH  — update layout-plan + prompt_hint + PNG + CSS, dual QA
"Add a new bullet point"               → TEXT  — update HTML (if text fits zone)
"Change accent color"                  → TEXT  — CSS-only change
"Add decorative elements on left"      → VISUAL — modify prompt, regenerate PNG
```

**TEXT edits**:
1. Update HTML/CSS in `slides.md` for affected slides. Preserve all zone div coordinates.
2. Run Phase 2 QA (composite export, visual review).
3. If any zone overflows with new text: reduce font size or truncate. If zone is still insufficient: flag to user that zone resize is needed (requires BOTH edit type).

**VISUAL edits**:
1. Modify `prompts.json` for affected slides — update visual description, preserve zone instructions (prompt_hint must remain intact).
2. Regenerate affected PNGs via provider API (with anchor reference from `meta.json` unless `--no-ref` or anchor is being regenerated).
3. Phase 1 QA: verify zones are still clean in new PNG. Max 2 regen attempts if zones violated.
4. Phase 2 QA: export composite, verify text overlay still reads correctly against new background.

**BOTH edits**:
1. Update zone coordinates in `layout-plan.json` for affected slides.
2. Re-generate `prompt_hint` from updated zone positions (per `references/layout-plan-format.md`).
3. Update `prompts.json` with new prompt_hint and any visual changes.
4. Regenerate affected PNGs.
5. Phase 1 QA: verify new zones are empty.
6. Update CSS zone positions in `slides.md` to match new coordinates from `layout-plan.json`.
7. Phase 2 QA: full composite export + visual review.

**Overflow escalation**: If during TEXT or VISUAL edit the Phase 2 QA reveals text overflowing zone boundaries, escalate to BOTH edit type and adjust zone height/width in `layout-plan.json` before re-generating.

**Final step**: Update `prompts.json` with all changes. Print which slides were edited, edit type, QA results.

Stop here — do not proceed to generation.

---

**`--picture [auto|paths...] [dir]`**: Add real photos to non-text zones of AI-generated backgrounds.

**Step 1: Resolve project directory** (see Directory Auto-Detection below).

**Step 2: Read `layout-plan.json`** and identify free zones — areas NOT occupied by text zones. Free zones are coordinate regions on each slide where no `zones[]` entry exists. Calculate approximate free zone coordinates per slide.

**Step 3: Select candidate slides** — slides that have meaningful free zones (area ≥ 25% of slide). Skip: cover slides with centered full-frame composition, slides where all zones tile the full canvas.

**Step 4: Acquire images**:

*Auto mode:*
- For each candidate slide: derive search query from slide heading + key content words
- Search via `mcp__brave-search__brave_web_search` (query + "high quality photo")
- Download to `<dir>/public/images/slide-N-keyword.jpg` via `curl -L -o`
- Verify file is non-empty; skip slide on failure

*User-provided paths:*
- Copy files to `<dir>/public/images/`
- Distribute across candidate slides in order
- Fewer images than candidates → remaining slides unchanged; extras → noted in report

**Step 5: Update `slides.md`** — for each slide getting a photo, add a new `<div>` layer between the AI background (z-index: 0) and text zones (z-index: 2):
```html
<div class="zone-photo" style="left:<x>%;top:<y>%;width:<w>%;height:<h>%;z-index:1;
  background:url('/images/slide-N-keyword.jpg') center/cover no-repeat;
  border-radius:8px;">
</div>
```
Adjust text zone `z-index` to `2` on all affected slides. Add gradient overlay at photo edges in `styles/index.css` to blend with AI background:
```css
.zone-photo::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(var(--bg-rgb), 0.6) 0%, transparent 30%,
              transparent 70%, rgba(var(--bg-rgb), 0.6) 100%);
}
```

**Step 6: Phase 2 QA** on affected slides — export composite PNGs, verify photos don't interfere with text readability. If contrast drops below threshold, add stronger gradient overlay on the photo.

**Step 7: Report** — which slides got photos, sources, skipped slides and reasons.

Stop here — do not proceed to generation.

---

## Directory Auto-Detection

Several commands accept an optional `[dir]` argument. When omitted:

1. Look for `layout-plan.json` in the current working directory
2. If not found, scan one level deep for the most recently modified subdirectory containing `layout-plan.json`
3. If multiple found, list them and ask the user to pick
4. If none found, print error: "No SlideCraft project found. Run `/slidecraft <outline>` to create one."

---

## Generation Modes

After subcommands are handled, determine the generation mode:

1. **Preset mode** — `--preset <name>`: Load preset using the lookup order in `references/preset-format.md` (direct path → `./.slidecraft-presets/<name>.preset.md` → `~/.claude/slidecraft-presets/<name>.preset.md`). Apply the preset's visual style suffix for AI prompts and its text layer settings (fonts, CSS variables, zone_strategy) for Slidev assembly.

2. **Custom Style mode** — `style: <desc>`: User provides a free-text style description. Convert to a concrete style suffix for AI prompts + derive font and palette choices for the text layer.

3. **Unique mode** (default): Claude designs a bold, distinctive visual direction. Consult Design Memory (`references/design-memory.md`) for inspiration (from `visual` sub-object) and avoidance patterns.

---

## Generation Procedure

### Step 1: Resolve Provider and API Key

Follow `references/providers.md` to resolve the provider, model, endpoint, and API key based on flags or defaults.

If the API key environment variable is not set, print error and stop:

```
Error: API key not found.

For Polza (default provider):
  1. Register at https://polza.ai?referral=dA0vnQPKuQ
  2. Generate an API key in your dashboard
  3. Set the environment variable:
     export POLZA_API_KEY=your-key

For other providers:
  OpenAI: export OPENAI_API_KEY=your-key
  Custom: export CUSTOM_API_KEY=your-key (or use --api-key-env=YOUR_VAR)
```

### Step 2: Read Design Memory

Read `~/.claude/slidecraft-design-memory.json` (if it exists). Follow the Read Protocol in `references/design-memory.md`. Draw from both sub-objects:
- **`visual` sub-object**: palette patterns, decoration styles, zone clarity rates — use for AI prompt design
- **`text` sub-object**: font pairings, positioning accuracy, contrast results — use for Slidev assembly
- Draw inspiration from `success` entries (extract principles, don't copy exactly)
- Avoid patterns from `failure` entries
- Skip silently if file doesn't exist

### Step 3: Design Thinking

Determine the visual direction and text design for this presentation. This is where Claude makes creative decisions that govern both layers.

**In Preset mode**: Use the preset's parameters directly. Parse frontmatter for `mood`, `palette`, `decoration`, `zone_strategy`, `fonts`, `text_color`, `accent_color`, `transition`, `colorSchema`. Use the style suffix body for AI prompts. Skip creative decisions below.

**In Custom Style mode**: Parse the user's style description into:
- Concrete visual parameters (colors, background treatment, decoration style)
- Font pair (Google Fonts — NEVER Inter/Roboto/Arial/generic)
- Text color strategy (light-on-dark vs dark-on-light)
- Zone strategy preference (if implied by style)

**In Unique mode**: Design a bold, distinctive visual direction:

*Visual layer (AI prompts):*
- **Palette**: Choose 3-5 colors with a dominant + accent hierarchy. Commit to specific hex values.
- **Background treatment**: Gradients, geometric patterns, subtle textures — be specific.
- **Decorative elements**: What elements will populate non-zone areas (geometric shapes, organic blobs, architectural details, abstract motifs).
- **Composition approach**: How the visual interacts with the empty zones (decorative elements framing zones, gradient fade toward zones). **CRITICAL: AI must NEVER draw panels, cards, boxes, or any rectangular containers in text zones.** If the design calls for card-like containers around text, those are created in the CSS layer (Step 6), not by the AI. The AI draws only the atmospheric background + decorative elements outside zones.

*Text layer (Slidev):*
- **Font pair**: Distinctive Google Fonts — display font + body font. Good pairs: Outfit + Source Serif 4, Syne + Literata, Cabinet Grotesk + Newsreader, Plus Jakarta Sans + Fraunces, Bricolage Grotesque + Lora. NEVER Inter/Roboto/Arial.
- **CSS variables**: Define `--color-accent`, `--color-accent-dim`, `--color-accent-bg`, `--color-bg`, `--color-text`, `--color-surface` with specific hex values.
- **Typography scales**: Hero (3-5em), heading (2-2.5em), body (0.95-1.1em). Define accent hierarchy: primary (full), secondary (40-60% opacity), ambient (8-15% opacity).
- **Accent hierarchy**: 3 intensity levels for the accent color across zone types.

*Zone strategy*: Choose a default zone placement approach based on content type:
- `text-left-60` — text in left 60% of slide, visual elements fill right 35%. Good for content/stat slides.
- `text-center` — centered text block (20-80% horizontal, 30-70% vertical). Good for quotes, cover, section.
- `text-bottom-40` — text in bottom 40%, visual or decorative fills top. Good for dramatic backgrounds.
- `text-split-50-50` — left column text, right column visual. Good for comparisons.

Document all decisions as a **style suffix** (for AI prompts) + **text design plan** (for Slidev assembly). The style suffix is a paragraph of English describing the visual to the AI model.

Example style suffix:
> "Style: Deep navy background (#1a1a2e) with subtle geometric grid overlay at 4% opacity. Electric blue (#00d4ff) accent lines forming abstract architectural motifs on the right side and bottom corners. Smooth gradient fade from deep navy to near-black at right edge. No panels, cards, boxes, or rectangular containers in the image — text containers are handled by CSS overlay. 16:9 aspect ratio presentation background."

### Step 4: Plan Slides

For each slide in the outline, create a complete zone plan. This produces `layout-plan.json` and `prompts.json`.

**4a: Parse outline, assign roles.**

Assign roles:
- First slide → `cover`
- Major topic shifts → `section`
- Bullet/body content → `content`
- Key metrics/numbers → `stat`
- Quotations → `quote`
- Two-item comparisons → `comparison`
- Final slide → `end`

**4b: Determine text content per slide.**

For each slide, identify:
- **Heading** (required): the main title or statement
- **Subheading** (optional): subtitle or descriptor
- **Body** (optional): bullets, paragraphs, key points — up to 4 items per content slide
- **Figures** (optional): metrics, statistics, key numbers
- **CTA** (optional): call to action text

**4c: Apply zone strategy and generate zone objects.**

For each slide, apply the default zone_strategy OR override per-role:

Default zone layouts per role (follow `references/layout-plan-format.md` for exact coordinates):
- `cover`: centered title + subtitle — heading in 10-80% horizontal, 35-50% vertical; subheading 15-80%, 55-63%
- `section`: centered heading — 15-70%, 40-58% vertical
- `content` (text-left-60): heading 5-58%, 8-20%; body 5-58%, 25-78%
- `stat`: large number centered 20-60%, 30-55%; label below 20-60%, 58-68%
- `quote`: quotation 10-80%, 30-60%; attribution 25-65%, 62-70%
- `comparison`: left column 3-47%, 15-85%; right column 52-47%, 15-85%
- `end`: centered heading 10-80%, 40-52%; CTA 20-60%, 55-65%

For each zone object, define:
```json
{
  "id": "title",
  "type": "heading",
  "text": "Actual heading text goes here",
  "position": { "x": "10%", "y": "35%", "w": "80%", "h": "15%" },
  "style": {
    "fontSize": "3em",
    "fontWeight": "bold",
    "color": "white",
    "textAlign": "center"
  }
}
```

Zone types: `heading`, `subheading`, `list`, `body`, `stat`, `quote`, `cta`, `caption`

**4d: Generate `prompt_hint` for each slide.**

Convert zone positions to an explicit English instruction. For each zone:
```
"Leave the area from [x] to [x+w] horizontally, [y] to [y+h] vertically completely empty —
no text, no decorative elements. Background must be uniform [dark|light] in this region."
```
The `[dark|light]` value is derived from text color: white/light text → zone must be dark, dark text → zone must be light. Combine all zone instructions into a single `prompt_hint`.

**4e: Write `layout-plan.json`.**

```json
{
  "slides": [
    {
      "slide": 1,
      "role": "cover",
      "zones": [
        {
          "id": "title",
          "type": "heading",
          "text": "Presentation Title",
          "position": { "x": "10%", "y": "35%", "w": "80%", "h": "15%" },
          "style": {
            "fontSize": "3em",
            "fontWeight": "bold",
            "color": "white",
            "textAlign": "center"
          }
        },
        {
          "id": "subtitle",
          "type": "subheading",
          "text": "Subtitle text",
          "position": { "x": "15%", "y": "55%", "w": "70%", "h": "8%" },
          "style": {
            "fontSize": "1.4em",
            "color": "rgba(255,255,255,0.7)",
            "textAlign": "center"
          }
        }
      ],
      "visual_description": "Dark gradient background with geometric decorative elements on edges",
      "prompt_hint": "Leave the area from 10% to 90% horizontally, 35% to 50% vertically completely empty — no text, no decorative elements. Background must be uniform dark in this region. Leave the area from 15% to 85% horizontally, 55% to 63% vertically completely empty — uniform dark."
    }
  ],
  "zone_strategy": "text-center",
  "text_contrast_mode": "light-on-dark"
}
```

**4f: Write `prompts.json`.**

For each slide, generate the full image generation prompt following the **Slide Prompt Authoring Rules** below (no text in prompts, only zone instructions). Save to `prompts.json`:

```json
{
  "slides": [
    {
      "index": 1,
      "role": "cover",
      "prompt": "Full text-free prompt for the AI background image...",
      "style_suffix": "Style: Dark navy...",
      "prompt_hint": "Leave the area..."
    }
  ],
  "style_suffix": "Style: Dark navy...",
  "generation_mode": "unique"
}
```

**4g: Prompt review before proceeding.**

Before advancing to Step 5, verify each prompt:
- Does each prompt contain the prompt_hint (empty zone instructions)?
- Is the style suffix appended to every prompt?
- Are there any text words, names, or numbers in the prompt that should NOT appear in the image? → Remove them.
- Are there contradictions (e.g., "dark background" in style_suffix but "light zone required" in prompt_hint)?
- Is each prompt under 2000 characters?
Fix any issues before generating images.

**Output directory naming**: slugify the outline topic to kebab-case, e.g., "AI in Healthcare" → `ai-in-healthcare/`. If directory already exists, append a timestamp: `ai-in-healthcare-1710400000/`. Create: `mkdir -p <output-dir>/slides`.

### Step 5: Generate Images (Phase 1 — Image Generation)

Determine generation mode:
- If slide count < 3 OR `--no-ref` flag: use **no-reference mode**
- Otherwise: use **reference mode** (default)

**Reference mode:**

1. **Generate slide 1** (cover) — call provider API with slide 1 prompt, no reference images. Save to `<output-dir>/slides/slide-01.png`. Print: "Generated slide 1/<total>"
2. **Generate slide 2** — call provider API with slide 2 prompt, no reference images. Save to `<output-dir>/slides/slide-02.png`. Print: "Generated slide 2/<total>"
3. **Select style anchor** — read both PNGs. Score on anchor selection rubric:

   | Criterion (1-5) | Description |
   |---|---|
   | Layout density | Multiple compositional elements vs single centered image |
   | Background complexity | Represents intended visual style and atmosphere |
   | Decorative elements | Contains representative decorative details from style |
   | Zone clarity | Zones appear clean and uncluttered |

   Higher total score wins. Tie → slide 2 wins. Record anchor index in `meta.json`.

4. **Describe anchor palette in text** — after selecting the anchor, analyze its visual characteristics and write an **anchor palette description** (3-4 sentences): dominant colors with hex values, background treatment, decoration style, overall mood. This description is prepended to every subsequent slide prompt to reinforce consistency even when the reference image alone is insufficient.

   Example: `"STYLE CONSISTENCY: This presentation uses a dark navy (#0d1b2a) to deep teal (#1b3a4b) gradient background with cyan (#00f0ff) accent elements. Decorative motifs are geometric hexagons and circuit-board traces, positioned in the right 30-40% of slides. The mood is tech-forward and professional. ALL slides MUST maintain this exact palette and decoration style — do not introduce new colors, warm tones, or different decoration styles."`

5. **Generate slides 3..N** — for each remaining slide:
   - Read the style anchor PNG as base64
   - **Prepend the anchor palette description** to the slide prompt (before zone instructions)
   - Call provider API with slide prompt + anchor image as reference
   - Save to `<output-dir>/slides/slide-NN.png`
   - Print: "Generated slide N/<total>"
   - Handle async responses per `references/providers.md`

**No-reference mode:**

Generate all slides sequentially without reference images. Print progress after each.

**Error handling:**
- Per-slide timeout (120 seconds): print warning, skip slide, continue
- Rate limit (429): exponential backoff — 5s, 10s, 20s (max 3 retries)
- At the end: report any skipped slides, suggest `--edit` to regenerate them

**Phase 1 QA — inline image review (run immediately after generating each PNG):**

Read each generated PNG and verify:
1. **Zone emptiness**: Are the specified zone areas actually empty? No text, no decorative elements crossing into zones?
2. **Zone background uniformity**: Is the background in each zone uniform enough for text overlay? (No visible pattern variation, gradient discontinuity, or decorative element edges within the zone area — should read as a single flat or smoothly graduated color region at presentation scale.)
3. **Zone contrast**: Is the zone background the right tone (dark for white text, light for dark text)?
4. **Stylistic consistency**: Does this slide visually match the style anchor? Check:
   - Same color palette (dominant + accent colors match within the same hue family)?
   - Same decoration style (geometric shapes, organic blobs, etc. — same motif type)?
   - Same background treatment (gradient direction, texture type)?
   - **If ANY of these differ significantly** (e.g., teal palette vs orange palette, or geometric vs organic decorations), the slide MUST be regenerated with the anchor palette description reinforced: prepend `"CRITICAL STYLE CONSISTENCY: You MUST use EXACTLY the same color palette as the reference image. Dominant color: [hex], accent: [hex]. Do NOT introduce any new colors, warm tones, or different decoration styles. Match the reference image's visual style precisely."`
   - **Exception for "peak intensity" slides** (typically the Ask/CTA/investment slide): a subtle hue shift toward warm/gold is acceptable to create emphasis, but the overall decoration style and composition approach must remain consistent. The shift should be an accent intensification, not a complete palette change.

**If zone not empty → regenerate** with reinforced prompt: prepend `"CRITICAL: the area at X% to X+W% horizontally, Y% to Y+H% vertically MUST BE COMPLETELY EMPTY — no text, no decorations, no elements of any kind. The zone must blend seamlessly into the background — do NOT draw visible rectangles or borders around it."`

**If zone background mismatches planned contrast** (e.g., planned dark but AI generated light): update the text color in `layout-plan.json` for that zone before proceeding to Step 6 assembly. Switch white text to dark text (or vice versa) to match actual background.

**Regeneration cap**: Up to 2 attempts per slide. If zone is still violated after 2 attempts, proceed to assembly and note in `score-report.md`. Phase 2 QA can compensate with a semi-transparent overlay behind text zones.

**Save `meta.json`:**

```json
{
  "provider": "polza",
  "model": "google/gemini-3.1-flash-image-preview",
  "mode": "reference",
  "style_anchor": 2,
  "aspect_ratio": "16:9",
  "created": "2026-03-14T12:00:00Z",
  "slide_count": 10,
  "zone_strategy": "text-left-60",
  "text_contrast_mode": "light-on-dark"
}
```

### Step 6: Assemble Slidev Project

Create the Slidev project structure with AI PNGs as backgrounds and text overlay via CSS absolute positioning. ALL slides use `layout: none`.

**Project structure:**
```
<output-dir>/
  package.json
  uno.config.ts
  slides.md
  styles/
    index.css
  components/
    Icon.vue
  slides/
    slide-01.png
    slide-02.png
    ...
  layout-plan.json
  prompts.json
  meta.json
```

**6a: Write `package.json`:**

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

**6b: Write `uno.config.ts`** — UnoCSS shortcuts for consistent zone text styling:

```ts
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'slide-heading': 'text-4xl font-bold tracking-tight leading-tight',
    'slide-subheading': 'text-2xl font-light opacity-80 leading-snug',
    'slide-accent': 'text-[var(--color-accent)]',
    'slide-body': 'text-lg leading-relaxed',
    'slide-stat': 'text-6xl font-bold tracking-tighter',
  },
})
```

**6c: Write `styles/index.css`** — CSS variables, zone base styles, slide background declarations, and all slide-specific background references:

```css
/* CSS Variables */
:root {
  --color-bg: #1a1a2e;
  --color-text: #ffffff;
  --color-accent: #00d4ff;
  --color-accent-dim: rgba(0, 212, 255, 0.5);
  --color-accent-bg: rgba(0, 212, 255, 0.1);
  --color-surface: rgba(255, 255, 255, 0.05);
  --font-sans: 'Outfit', sans-serif;
  --font-serif: 'Source Serif 4', serif;
}

/* Slide container — fills the entire slide */
.slide-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

/* AI background layer — always z-index 0 */
.slide-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  z-index: 0;
}

/* Text zone base — always z-index 1 (or 2 when photos are present) */
.zone {
  position: absolute;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

/* Zone card styles — CSS-rendered containers for text.
   Use these instead of asking AI to draw panels/boxes.
   The card and text are the SAME DOM element = perfect alignment always. */
.zone-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px 28px;
  backdrop-filter: blur(8px);
}
.zone-card-solid {
  background: rgba(0, 0, 30, 0.55);
  border-radius: 12px;
  padding: 24px 28px;
}
.zone-card-accent {
  background: linear-gradient(135deg, var(--color-accent-bg), rgba(0,0,0,0.3));
  border: 1px solid var(--color-accent-dim);
  border-radius: 12px;
  padding: 24px 28px;
}

/* Background references — one class per slide */
.slide-01 { background-image: url('./slides/slide-01.png'); }
.slide-02 { background-image: url('./slides/slide-02.png'); }
/* ... (continue for all slides) */

/* Blockquote reset — override theme-default styling */
.slidev-layout blockquote {
  background: transparent !important;
  border-left: none !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  color: inherit !important;
}

/* Optional: semi-transparent overlay fallback for zones where Phase 1 QA
   found non-uniform backgrounds (apply class conditionally per slide) */
.zone-overlay {
  background: rgba(0, 0, 0, 0.45);
  border-radius: 4px;
  padding: 8px 12px;
}
```

**6d: Write `slides.md`** — all slides with `layout: none`, slide container div, background class, zone divs with coordinates directly from `layout-plan.json`.

Global headmatter:
```yaml
---
theme: default
title: Presentation Title
fonts:
  sans: Outfit
  serif: Source Serif 4
colorSchema: dark
transition: slide-left
aspectRatio: '16/9'
---
```

For each slide:
```markdown
---
layout: none
---

<div class="slide-container">
  <div class="slide-bg slide-01"></div>

  <div class="zone" style="left:10%;top:35%;width:80%;height:15%;">
    <h1 style="font-size:3em;font-weight:bold;color:white;text-align:center;margin:0;line-height:1.1;">
      Presentation Title
    </h1>
  </div>

  <div class="zone" style="left:15%;top:55%;width:70%;height:8%;">
    <p style="font-size:1.4em;color:rgba(255,255,255,0.7);text-align:center;margin:0;">
      Subtitle text
    </p>
  </div>
</div>
```

**Zone content rules:**
- Copy coordinates directly from `layout-plan.json` (x → left, y → top, w → width, h → height)
- Use inline styles on text elements (not just on the zone div) — do NOT rely on CSS class inheritance due to Slidev theme CSS specificity
- Text colors must match what Phase 1 QA confirmed (may differ from original plan if background mismatch was found)
- **Card containers are CSS-only, never AI-drawn.** If the design calls for a panel/card around text, add `zone-card`, `zone-card-solid`, or `zone-card-accent` class to the zone div:
  ```html
  <div class="zone zone-card" style="left:5%;top:8%;width:55%;height:80%;">
    <h1>Heading</h1>
    <p>Content inside a glass card — perfectly aligned because card = zone div</p>
  </div>
  ```
  This guarantees the card border and text are always perfectly aligned (same DOM element).
- `v-clicks` work inside zone divs for bullet lists — test pattern:
  ```html
  <div class="zone" style="left:5%;top:25%;width:58%;height:55%;">
    <v-clicks>

    - First bullet point
    - Second bullet point
    - Third bullet point

    </v-clicks>
  </div>
  ```
- Lists use native Markdown syntax inside zone divs (Slidev renders them correctly)
- Zone divs MUST NOT nest more than 2 levels deep (Slidev rendering limit)

**6e: Write `components/Icon.vue`** — SVG icon component (no emoji):

```vue
<template>
  <span :style="{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }">
    <svg v-if="name === 'check'" :width="size" :height="size" viewBox="0 0 24 24"
         fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 12 4 9"></polyline>
    </svg>
    <svg v-else-if="name === 'arrow-right'" :width="size" :height="size" viewBox="0 0 24 24"
         fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <line x1="5" y1="12" x2="19" y2="12"></line>
      <polyline points="12 5 19 12 12 19"></polyline>
    </svg>
    <!-- Add icons relevant to the presentation topic -->
    <!-- ALWAYS add a fallback: -->
    <svg v-else :width="size" :height="size" viewBox="0 0 24 24"
         fill="none" :stroke="color" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="12"></line>
      <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
  </span>
</template>
<script setup>
defineProps({
  name: { type: String, required: true },
  size: { type: Number, default: 24 },
  color: { type: String, default: 'currentColor' }
})
</script>
```

**CRITICAL zone-to-CSS coordinate mapping:**
```
layout-plan.json position.x  →  CSS left
layout-plan.json position.y  →  CSS top
layout-plan.json position.w  →  CSS width
layout-plan.json position.h  →  CSS height
```
These are direct mappings. Copy the percentage values verbatim.

**z-index layer system:**
- AI background PNG: z-index 0 (`.slide-bg`)
- Text overlay zones: z-index 1 (`.zone`)
- Optional photo divs: z-index 1 (photos), z-index 2 (text zones when photos present)

### Step 6.5: Install Dependencies

After scaffolding the project (Step 6), install npm dependencies and Playwright:

```bash
cd <output-dir> && npm install && npx playwright install chromium
```

This step is required before Phase 2 QA (Step 7) or `--dev`. Run synchronously and wait for completion. If `npm install` fails, print the error and stop — the QA and dev steps will not work without dependencies.

### Step 7: Dual QA (Phase 2 — Composite Review)

**Phase 2 QA — composite export and visual review:**

**7a: Export composite PNGs via Slidev:**
```bash
cd <output-dir> && npx slidev export --format png --output slides-qa
```
This renders the full composite (AI background + text overlay) as PNG files.

**7b: Read EVERY composite PNG.** For each slide, apply this two-layer visual checklist:

*Image layer:*
- [ ] AI background is visible (not blocked by opaque Slidev theme elements)
- [ ] Background visually matches intended style and mood
- [ ] No AI-generated text artifacts visible in zone areas
- [ ] Background renders correctly at 16:9 (no letterboxing, no stretching)

*Text layer:*
- [ ] All text is fully legible — no text blends into background
- [ ] Sufficient contrast (white text on dark bg, dark text on light bg)
- [ ] Text is NOT clipped, cut off, or overflowing outside its zone boundary
- [ ] Text hierarchy is clear — heading visually dominant over body/bullets
- [ ] Font rendering looks correct (not fallback system font)
- [ ] Zone positioning matches intent (heading at top, bullets below, stats centered)

*Layer harmony:*
- [ ] Text zones are positioned over the clean background areas (not over busy visual areas)
- [ ] Text colors work against the actual AI background (not just the planned background)
- [ ] Overall composition feels intentional — text and visual elements complement each other
- [ ] No visual clutter where text overlaps decorative AI elements

**7c: Scoring** — run `references/scoring-subroutine.md` on composite PNGs:

| Axis | What is evaluated |
|------|-------------------|
| Visual impact | AI background quality + overall first impression |
| Layout precision | Text positioning accuracy — do zones land where planned? |
| Typography quality | Readability, contrast, font hierarchy, sizing |
| Color conviction | AI palette + harmony between image and text color layers |
| Content clarity | Information hierarchy, clarity, brevity |
| Layer harmony | How well the AI background and text overlay work together |

Score each slide on all 6 axes (1-10). Write `<output-dir>/score-report.md`.

**7d: Remediation** — for each slide scoring < 6 on ANY axis:
1. Identify the source layer (image problem, text problem, or both)
2. Apply targeted fix:
   - **Image problem** (Visual impact, Color conviction): modify prompt → regenerate PNG (up to 2 attempts) → re-export composite
   - **Text problem** (Typography quality, Content clarity): adjust CSS in `slides.md` → re-export composite → re-score. CSS adjustments capped at 3 attempts — if still failing, flag to user
   - **Positioning problem** (Layout precision): adjust zone CSS coordinates in `slides.md` → re-export. If misalignment is structural (zones need to be in different positions), update `layout-plan.json` and regenerate PNG (BOTH fix)
   - **Harmony problem** (Layer harmony): determine whether the text placement lands on busy AI area → adjust zone coordinates OR reinforce zone instruction in prompt → regenerate PNG

**7e: Content review** — run `references/content-review-subroutine.md`:
- 3-second test: is the key message obvious at a glance?
- Narrative flow: do slides tell a coherent story?
- Redundancy: is any information repeated without purpose?
- CTA clarity: is the call-to-action on the final slide clear?
- CRITICAL issues → fix text content in `slides.md`
- MINOR issues → note in report, do not regenerate

**7f: Cleanup:**
```bash
rm -rf <output-dir>/slides-qa
```

### Step 8: Export & Summary

**8a: PDF assembly** — assemble a standalone PDF from composite PNGs (the most portable format):

1. Check Python 3: `python3 --version` (or `python --version` on Windows)
2. If not available: print warning "Python not found. Skipping PDF assembly. Preview with `--dev`."
3. Ensure Pillow: `pip install Pillow 2>/dev/null || pip3 install Pillow 2>/dev/null`
4. Export composite PNGs first: `cd <output-dir> && npx slidev export --format png --output slides-export`
5. Assemble PDF:
   ```python
   from PIL import Image
   import os, re
   png_dir = '<output-dir>/slides-export'
   files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
   files.sort(key=lambda x: int(re.match(r'(\d+)', x).group()))
   images = [Image.open(os.path.join(png_dir, f)).convert('RGB') for f in files]
   images[0].save('<output-dir>/slides.pdf', save_all=True,
                  append_images=images[1:], resolution=150.0, quality=95)
   for img in images: img.close()
   ```
6. `rm -rf <output-dir>/slides-export`
7. Print: "PDF assembled: <output-dir>/slides.pdf"

**8b: Design memory write** — follow write protocol in `references/design-memory.md`. Write to `~/.claude/slidecraft-design-memory.json` (separate from slidegen/slidev memory). Entry format includes both `visual` and `text` sub-objects:
```json
{
  "date": "2026-03-14",
  "topic": "Presentation topic",
  "type": "success",
  "score": 8.5,
  "visual": {
    "style_suffix": "Style suffix used for AI prompts...",
    "palette": "palette description",
    "effective_patterns": ["pattern that worked well"],
    "zone_clarity": "95% — zones clean on first attempt"
  },
  "text": {
    "fonts": "Outfit + Source Serif 4",
    "positioning_accuracy": "high — no QA repositioning needed",
    "contrast_issues": false
  }
}
```
- Average score ≥ 7: type `"success"`
- Average score 5-6: type `"neutral"`
- Average score < 5: type `"failure"`
Max 50 entries, FIFO eviction.

**8c: Print final summary:**

```
SlideCraft complete!

  Output:    <output-dir>/
  Slides:    <output-dir>/slides/ (N AI background PNGs)
  Project:   <output-dir>/slides.md
  PDF:       <output-dir>/slides.pdf
  Layout:    <output-dir>/layout-plan.json
  Prompts:   <output-dir>/prompts.json
  Score:     <overall-avg>/10 (Visual: X | LayerHarmony: X | Typography: X)

  Provider:  <provider> / <model>
  Mode:      reference (anchor: slide N) | no-reference
  Zones:     N slides with clean zones on first attempt, N required reinforcement
  QA:        Phase 1 — N regenerations; Phase 2 — N text fixes, N image fixes

  Preview:   /slidecraft --dev <output-dir>
  Export:    /slidecraft --export png2pdf <output-dir>
```

---

## Slide Prompt Authoring Rules

**CRITICAL** — follow when composing prompts in Step 4. These rules differ significantly from slidegen because SlideCraft prompts must NOT contain text.

1. **NEVER include text content in prompts.** This is the most fundamental difference from slidegen. Do NOT write "heading reads 'Market Overview'" — write "Leave area at X,Y empty." The AI generates the visual background only; all text comes from Slidev.

2. **Always specify empty zones explicitly.** Every prompt MUST include the full `prompt_hint` from `layout-plan.json`. Zone instructions come first in the prompt, before visual descriptions.

3. **Zones must blend seamlessly into the background.** Do NOT draw visible rectangles, borders, boxes, or panels to mark empty zones. The zone area should be an organic, natural part of the overall background — the same base color/gradient continuing smoothly through the zone. Explicitly require: "The empty zone area must blend seamlessly into the surrounding background — do NOT draw visible borders, rectangles, panels, or any visual markers around the empty area. The zone should simply be a calm region of the same background color/gradient, free of decorative elements."

4. **Keep visual elements outside zones.** State explicitly where decorative elements should go: "Place all geometric shapes, icons, and decorative elements ONLY in the areas outside the text zones. Decorative elements should frame the empty zones naturally, not border them."

5. **Specify "16:9 aspect ratio presentation background slide"** at the start of every prompt.

6. **Keep prompts under 2000 characters.** Zone instructions + visual description + style suffix. Be specific but concise.

7. **Use English for prompts.** Even if slide content is in another language, prompts are always in English.

8. **Describe the visual spatially.** Use "top-right corner", "bottom third", "left 35% of the slide" for decorative element placement.

9. **Specify background treatment explicitly.** Never leave the background to the model's imagination — describe color, gradient direction, texture. The background must be predictable in the zone areas.

10. **Always include the style suffix.** Append it to every prompt. The style suffix ensures visual consistency across all slides in the presentation.

11. **Include slide role description for visual context:**
    - `cover` → "This is a cover/title slide background — minimal, impactful, empty center zone for text overlay"
    - `section` → "This is a section divider slide background — transitional, clean, large empty zone for section heading"
    - `content` → "This is a content slide background — supporting visual context, left zone empty for text, right side can have decorative elements"
    - `stat` → "This is a statistics slide background — clean, emphasis-supporting, central zone empty for large numbers"
    - `quote` → "This is a quote slide background — atmospheric, centered zone empty for quotation text"
    - `comparison` → "This is a comparison slide background — two-area composition, both zones empty for text columns"
    - `end` → "This is a closing slide background — memorable, impactful, central zone empty for CTA text"

12. **Prompt structure template:**
    ```
    16:9 aspect ratio presentation background slide. [Role description.]

    [STYLE CONSISTENCY anchor palette description — for slides 3+ in reference mode]

    CRITICAL empty zones (these areas must blend seamlessly into the background —
    NO visible rectangles, borders, or panels marking them):
    [prompt_hint from layout-plan.json — list all zones]
    Zones must have background suitable for [white/dark] text overlay.

    Visual elements (placed ONLY outside the empty zones, framing them naturally):
    [decoration description, color palette, background treatment,
    atmospheric elements, compositional approach]

    [Style suffix]
    ```

13. **Zone background contrast instruction.** Always conclude zone instructions with the contrast requirement: "Zones must have background suitable for [white/dark] text overlay." This is separate from the visual description.

14. **Anti-visible-rectangle rule.** NEVER instruct the AI to "create a panel", "draw a box", "add a card", or "add a rectangle" for zones. The AI must NOT draw any containers, frames, or bordered areas where text will go. If the design needs card/panel containers around text, those are created by CSS classes (`zone-card`, `zone-card-solid`, `zone-card-accent`) in the Slidev layer — this guarantees perfect alignment between container border and text. The AI draws ONLY the atmospheric background + decorative elements outside zones. Use language like "leave this area as calm, uncluttered continuation of the background" rather than "create an empty panel/box/card here."

---

## Design Quality Principles

Apply these principles in ALL modes (generation, editing, presets, Visual QA). They govern the text layer and overall composition quality.

1. **Visual rhythm**: Alternate content slides with breathing slides (section/quote/stat roles). Never 3+ content slides in a row without visual relief. In a 10+ slide deck, at least 2-3 non-content slides distributed throughout.

2. **Layer intentionality**: Every zone placement must be intentional. Zones should align with the visual composition of the AI background — text should land on calm background areas, not fight with busy visual elements.

3. **Typography quality**: Use 3+ distinct type scales across the presentation. Headings at 2-3em, key stats at 3-6em, body at 0.95-1.1em. Zone height must accommodate the font size with appropriate line-height.

4. **No emoji**: NEVER use emoji in zone text content. Use `<Icon>` SVG component exclusively. Emoji render inconsistently across platforms and look unprofessional.

5. **Contrast guarantee**: Text color in every zone must be confirmed against the actual AI-generated background (not just the planned color). Phase 1 QA may update text colors if background differs from plan.

6. **Zone overflow prevention**: Zone height must be sufficient for the planned text content. A heading zone at 8% height will clip `3em` text with line wrapping. Size zones appropriately: single-line heading = ~12-15% height, 3-bullet list = ~35-45% height.

7. **Visual arc**: Build toward a climax. The most impactful content (key stat, big claim, CTA) should have the most dramatic visual treatment — both in the AI background and in the text styling.

8. **Font pair discipline**: Use the chosen font pair consistently across ALL slides. Never mix fonts mid-presentation. Apply `font-family: var(--font-sans)` or `var(--font-serif)` inline on zone text elements.

9. **CSS specificity discipline**: Always use inline styles on text elements inside zone divs (not just on the zone div container). Slidev theme CSS specificity overrides inherited properties from parent divs. Inline styles on the actual text element are the most reliable.

10. **Zone boundary discipline**: Zone divs MUST NOT overlap each other. Verify coordinate math: if heading zone is at y=8%, h=15%, the next zone must start at y=23% or later (accounting for margin). Overlapping zones create visual confusion.

---

## Output File Summary

```
<output-dir>/
  package.json          — Slidev project config
  uno.config.ts         — UnoCSS shortcuts for zone text styling
  slides.md             — Slidev presentation (all layout:none + zone divs)
  styles/
    index.css           — CSS variables, zone styles, background image refs
  components/
    Icon.vue            — SVG icon component
  slides/
    slide-01.png        — AI-generated background (text-free)
    slide-02.png
    ...
  layout-plan.json      — Zone coordinates, text content, zone strategy
  prompts.json          — AI prompts used for generation
  meta.json             — Generation metadata (provider, mode, anchor, created)
  score-report.md       — Dual QA scoring results (6 axes per slide)
  slides.pdf            — Assembled PDF from composite exports
```
