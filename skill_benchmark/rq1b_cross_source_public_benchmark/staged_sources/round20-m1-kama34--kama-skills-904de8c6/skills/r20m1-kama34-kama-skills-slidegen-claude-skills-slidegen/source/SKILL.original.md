---
name: slidegen
description: Generate AI image presentations from slide outlines. Each slide rendered as an image via configurable APIs with preset styles, reference-based consistency, and quality scoring.
argument-hint: "[--help | --edit [dir] <comment> | --polish=N [dir] | --compare <dir1> <dir2> | --notes [dir] | --learn=N | --create-preset <name> | --export pdf [dir] | --preset <name> | --provider <name> | --model <id> | --no-ref | --resolution <1K|2K|4K> | --quality <low|medium|high> | --format <png|jpeg> | --size <WxH> | style: <desc>] <outline or file path>"
---

# Slidegen — AI Image Presentation Generator

You generate complete presentations as AI-generated images from slide outlines. Every generation produces a set of PNG slides and an assembled PDF, with consistent visual style across all slides.

## References

Before generating, internalize these references:
- `references/providers.md` — **CRITICAL**: Provider API configs (endpoints, request formats, auth, async handling)
- `references/image-prompt-guide.md` — **CRITICAL**: How to compose effective prompts for image generation models
- `references/scoring-subroutine.md` — Slide scoring (1-10 on 6 axes), used by --polish, --learn, --compare
- `references/content-review-subroutine.md` — Content quality checks (3-second test, narrative flow, redundancy, CTA clarity, hierarchy)
- `references/polish-procedure.md` — `--polish=N` iterative improvement cycle
- `references/ab-testing.md` — A/B variant generation for weak slides (used by --polish)
- `references/design-memory.md` — Design pattern memory (read/write protocol)
- `references/compare-procedure.md` — `--compare` side-by-side scoring
- `references/notes-procedure.md` — `--notes` speaker notes generation
- `references/preset-format.md` — Prompt-template preset specification

## Input Parsing

Parse the user's input to determine the subcommand or mode.

### Global Flags (can combine with any mode)

- `--provider <name>` — API provider: `polza` (default), `openai`, `custom`
- `--model <id>` — Model ID (default: `google/gemini-3.1-flash-image-preview` for Polza)
- `--no-ref` — Disable reference-based style consistency (generate each slide independently)
- `--base-url <url>` — Custom provider endpoint URL
- `--api-key-env <VAR>` — Environment variable name for the API key
- `--resolution <1K|2K|4K>` — Image resolution (Polza only, default: `1K`). Higher = better quality but slower and more expensive (1K≈4.8₽, 2K≈7.2₽, 4K≈10.8₽ per slide)
- `--quality <low|medium|high>` — Image quality (OpenAI only, default: `high`)
- `--format <png|jpeg>` — Output image format (Polza only, default: `jpeg`)
- `--size <WxH>` — Output image dimensions (OpenAI only, default: `1792x1024`). Supported: `1024x1024`, `1536x1024`, `1024x1536`, `1792x1024`, `1024x1792`

### Subcommands (handle before anything else)

**`--help`**: Display usage help and stop. Show:

```
Slidegen — AI Image Presentation Generator

Usage:
  /slidegen <outline or file>                     Generate with unique design
  /slidegen --preset <name> <outline>              Generate with preset style
  /slidegen style: <desc> <outline>                Generate with custom style
  /slidegen --edit [dir] <comment>                 Edit existing presentation
  /slidegen --polish=N [dir]                       Iterative quality improvement (N cycles)
  /slidegen --compare <dir1> <dir2>                Compare two presentations
  /slidegen --notes [dir]                          Generate speaker notes
  /slidegen --learn=N                              Self-improving loop (N cycles)
  /slidegen --create-preset <name>                 Create a new preset
  /slidegen --export pdf [dir]                     Reassemble PDF from PNGs
  /slidegen --help                                 Show this help

Provider flags (combinable with any mode):
  --provider <name>                                polza (default), openai, custom
  --model <id>                                     Model ID for the provider
  --no-ref                                         Generate without style references
  --base-url <url>                                 Custom provider endpoint
  --api-key-env <VAR>                              API key env variable name

Image quality flags:
  --resolution <1K|2K|4K>                          Image resolution (Polza, default: 1K)
  --quality <low|medium|high>                      Image quality (OpenAI, default: high)
  --format <png|jpeg>                              Output format (Polza, default: jpeg)
  --size <WxH>                                     Image dimensions (OpenAI, default: 1792x1024)
```

**`--create-preset <name>`**: Interactive preset creation wizard.

1. Extract preset name from arguments. If missing, ask for one (kebab-case).
2. Ask 7 questions **ONE AT A TIME**, waiting for each answer:
   - **Mood**: "What mood? (professional, playful, dramatic, calm, futuristic, elegant, bold)"
   - **Color scheme**: "Light or dark? (dark, light, deep navy, warm cream...)"
   - **Accent color**: "Accent color? (#ff6b35, electric blue, warm coral...)"
   - **Typography**: "Font personality? (geometric & modern, classic & refined, rounded & friendly, sharp & technical)"
   - **Density**: "Content density? (minimal with whitespace, balanced, information-dense)"
   - **Textures**: "Background textures? (gradient mesh, geometric patterns, clean flat, frosted glass, subtle noise)"
   - **Save location**: "Save preset globally or locally? (global: ~/.claude/slidegen-presets/, local: ./.slidegen-presets/)"
3. Synthesize answers into a prompt template with concrete visual parameters: specific colors (hex values), typography mood, background treatment, decoration style. The template MUST include `{{SLIDE_CONTENT}}` and `{{SLIDE_ROLE}}` placeholders.
4. Based on save location answer:
   - **Global**: Create `~/.claude/slidegen-presets/` if needed, write `<name>.preset.md` there
   - **Local**: Create `./.slidegen-presets/` in the current working directory if needed, write `<name>.preset.md` there
   Write per `references/preset-format.md`.
5. Generate demo presentation using `assets/demo-outline.md` with that preset.
6. **QA** — Run the QA procedure. Print score report. If overall average score < 7, print warning: "Preset scored below 7 — consider refining style parameters."
7. Print summary: preset path (noting global vs local), demo path, QA results, how to use (`/slidegen --preset <name> <outline>`).

Stop here — do not proceed to generation.

**`--learn=N`**: Self-improving learning loop. Parse N from the argument (e.g., `--learn=5`). Default N=3, max N=10.

1. Generate a presentation from `assets/demo-outline.md` using current design approach.
2. Run Scoring Subroutine → score-report.md.
3. Analyze: which axes scored lowest? What prompt patterns produced weak results?
4. Adjust approach: modify prompt construction strategy based on analysis.
5. Regenerate with adjusted approach.
6. Write Design Memory entry using the write protocol in `references/design-memory.md`.
7. Print iteration summary: score delta, what changed, what improved.
8. Repeat from step 2 until N iterations complete or overall avg >= 9.

Stop here — do not proceed to generation.

**`--polish=N [dir]`**: Iterative design improvement cycle. Follow the Polish Procedure in `references/polish-procedure.md`. Stop here — do not proceed to generation.

**`--compare <dir1> <dir2>`**: Compare two presentations side-by-side with scoring. Follow the Compare Procedure in `references/compare-procedure.md`. Stop here — do not proceed to generation.

**`--notes [dir]`**: Generate speaker notes for the presentation. Follow the Notes Procedure in `references/notes-procedure.md`. Stop here — do not proceed to generation.

**`--edit [dir] <comment>`**: Edit an existing presentation based on a free-text comment.

1. **Resolve project directory** (see Directory Auto-Detection below).
2. **Load state**: read `prompts.json` and `meta.json` from the project directory.
3. **List slides**: print a numbered list of all slides with their roles and prompt summaries (first 50 chars of each prompt).
4. **Identify affected slides**: Claude analyzes the comment to determine which slides need changes. If ambiguous (e.g., "make it more modern"), ask user to confirm slide numbers.
5. **Modify prompts**: update the affected prompts in `prompts.json` based on the comment. Preserve the style suffix and unaffected parts of the prompt.
6. **Regenerate**: regenerate only the affected slides using the API. Use the style anchor from `meta.json` as reference (unless `--no-ref` or the anchor itself is being regenerated).
7. **QA**: run scoring on regenerated slides only. If any score < 6 on any axis, regenerate with improved prompt (max 2 retries).
8. **Reassemble PDF**: rebuild `slides.pdf` from all PNGs (unchanged + regenerated).
9. **Update state**: save updated `prompts.json`.
10. **Report**: print which slides were regenerated, old vs new scores, output paths.

Stop here — do not proceed to generation.

**`--export pdf [dir]`**: Reassemble PDF from existing PNGs.

1. **Resolve project directory** (see Directory Auto-Detection below).
2. **Validate PNGs**: check that all `slides/slide-*.png` files exist and have consistent dimensions. If any are missing or mismatched, report which files are problematic and stop.
3. **Assemble PDF**: run the PDF Assembly procedure (see Phase 3 below).
4. **Report**: print output path.

Stop here — do not proceed to generation.

## Directory Auto-Detection

Several commands accept an optional `[dir]` argument. When omitted:

1. Look for `prompts.json` in the current working directory
2. If not found, scan one level deep for the most recently modified subdirectory containing `prompts.json`
3. If multiple found, list them and ask the user to pick
4. If none found, print error: "No slidegen project found. Run `/slidegen <outline>` to create one."

## Generation Modes

After subcommands are handled, determine the generation mode:

1. **Preset mode** — `--preset <name>`: Load preset from `references/preset-format.md` lookup order. Use the preset's prompt template for all slides.
2. **Custom Style mode** — `style: <desc>`: User provides a free-text style description. Convert to a style suffix appended to every prompt.
3. **Unique mode** (default) — No style specified: Claude designs a unique visual direction for this presentation. Consult Design Memory (`references/design-memory.md`) for inspiration and avoidance patterns.

## Generation Procedure

### Step 1: Resolve Provider, API Key, and Image Settings

Follow `references/providers.md` to resolve the provider, model, endpoint, and API key based on flags or defaults.

**Resolve image quality settings** based on provider:
- **Polza**: `image_resolution` from `--resolution` (default `1K`), `output_format` from `--format` (default `jpeg`)
- **OpenAI**: `quality` from `--quality` (default `high`), `size` from `--size` (default `1792x1024`)
- **Custom**: same as Polza (Polza-compatible format)

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

If generating in Unique or Custom Style mode, read Design Memory (`references/design-memory.md` read protocol):
- Draw inspiration from "success" entries (don't copy — extract principles)
- Avoid patterns from "failure" entries
- Skip silently if memory file doesn't exist

### Step 3: Design Thinking

Determine the visual direction for the presentation. This is where Claude makes creative decisions.

**In Preset mode:** Use the preset's frontmatter parameters (mood, palette, typography, decoration) as the style direction. Skip creative decisions.

**In Custom Style mode:** Parse the user's style description into concrete visual parameters.

**In Unique mode:** Design a bold, distinctive visual direction:
- **Palette**: Choose 3-5 colors with a dominant + accent hierarchy. Use specific hex values.
- **Typography mood**: Describe the feeling (geometric modern, classic refined, etc.)
- **Background treatment**: Gradients, textures, patterns, solid — be specific.
- **Decorative elements**: Lines, shapes, icons, overlays, borders.
- **Composition approach**: How content is arranged (centered, asymmetric, grid, etc.)

Document the visual direction as a **style suffix** — a paragraph of English text that will be appended to every slide prompt for baseline consistency. Example:

> "Style: Dark navy background (#1a1a2e) with subtle gradient to deep purple. Clean geometric sans-serif typography, white headings (48pt equivalent), light gray body text (24pt equivalent). Electric blue (#0066ff) accent for highlights. Thin horizontal line separators. Rounded rectangle cards with subtle shadow. 16:9 aspect ratio."

### Step 4: Plan Slides (Phase 1 — Planning)

For each slide in the outline, generate:

1. **Role** — one of: `cover`, `section`, `content`, `stat`, `quote`, `comparison`, `end`
2. **Text content** — the actual text that will appear on the slide:
   - Heading (required)
   - Subheading (optional)
   - Body text / bullets / key points (optional)
   - Figures / metrics (optional)
3. **Visual description** — slide-specific visual notes beyond the style suffix:
   - Layout composition (centered, left-aligned, split, etc.)
   - Special elements (charts, diagrams, icons)
   - Emphasis / focal point
4. **Final prompt** — combine all of the above into a single English prompt for the image API. Follow `references/image-prompt-guide.md` for prompt composition best practices.

**CRITICAL**: The prompt MUST include:
- Explicit text content (every word that should appear on the slide)
- Typography instructions (font sizes, weights, alignment)
- The style suffix (appended at the end)
- Aspect ratio instruction: "16:9 aspect ratio presentation slide"
- Slide role description (see rule 11 in Slide Prompt Authoring Rules below)

**Before proceeding to Step 5:** run prompt review (Step 6a) — verify each prompt is detailed enough, contains the style suffix, has the role description, and has no contradictions. Fix any issues before generating images.

Save all prompts to `prompts.json`:
```json
{
  "slides": [
    {
      "index": 1,
      "role": "cover",
      "heading": "Title Text",
      "subheading": "Subtitle",
      "body": null,
      "prompt": "Full prompt text...",
      "style_suffix": "Style: Dark navy..."
    }
  ],
  "style_suffix": "Style: Dark navy...",
  "generation_mode": "unique"
}
```

### Step 5: Generate Images (Phase 2 — Generation)

**Output directory naming:** derive from the outline topic. Slugify the topic to kebab-case, e.g., "AI in Healthcare" → `ai-in-healthcare/`. If the directory already exists, append a timestamp: `ai-in-healthcare-1710400000/`.

Create the output directory: `mkdir -p <output-dir>/slides`

Determine the generation mode:
- If slide count < 3 OR `--no-ref` flag: use **no-reference mode**
- Otherwise: use **reference mode** (default)

**Reference mode:**

1. **Generate slide 1** (cover) — call the provider API with the slide 1 prompt, no reference images. Save result to `<output-dir>/slides/slide-01.png`. Print: "Generated slide 1/<total>"
2. **Generate slide 2** — call the provider API with the slide 2 prompt, no reference images. Save to `<output-dir>/slides/slide-02.png`. Print: "Generated slide 2/<total>"
3. **Select style anchor** — read both PNGs. Score each on the anchor selection rubric:

   | Criterion (1-5) | Description |
   |---|---|
   | Layout density | Multiple content elements vs single centered title |
   | Background complexity | Represents intended visual style |
   | Decorative elements | Contains representative decorative details |
   | Typography variety | Shows heading + body text styles |

   Higher total score wins. Tie → slide 2 wins. Record anchor index in `meta.json`.

4. **Regenerate the non-anchor slide** — the slide that lost anchor selection was generated without a style reference and is likely stylistically inconsistent. **CRITICAL**: regenerate the losing slide using the winning anchor as reference image. Replace the old PNG. This ensures ALL slides in the deck share the same visual foundation.

5. **Generate slides 3..N** — for each remaining slide:
   - Read the style anchor PNG as base64
   - Call the provider API with the slide prompt + anchor image as reference
   - Save to `<output-dir>/slides/slide-NN.png`
   - Print: "Generated slide N/<total>"
   - Handle async responses per `references/providers.md`

**No-reference mode:**

Generate all slides sequentially without reference images. Print progress after each.

**Error handling during generation:**
- Per-slide timeout (120 seconds): print warning, skip slide, continue
- Rate limit (429): exponential backoff — 5s, 10s, 20s (max 3 retries)
- At the end: report any skipped slides, suggest `--edit` to regenerate them

Save `meta.json`:
```json
{
  "provider": "polza",
  "model": "google/gemini-3.1-flash-image-preview",
  "mode": "reference",
  "style_anchor": 2,
  "aspect_ratio": "16:9",
  "resolution": "1K",
  "format": "jpeg",
  "created": "2026-03-14T12:00:00Z",
  "slide_count": 10
}
```

### Step 6: Quality Assurance (Phase 3 — QA)

**6a. Prompt Review** (**IMPORTANT: this check runs during Step 4, before generation begins**):
- Is each prompt detailed enough? (minimum: text content + layout + style suffix)
- Does every prompt contain the style suffix?
- Are there contradictions between the prompt and style suffix?
- Fix any issues before sending to the API.

**6b. Visual Review** (after generation):
Read EVERY generated PNG. For each slide, run these **concrete checks**:

1. **Language & Script Verification** — **CRITICAL gate, check FIRST**:
   - Detect the expected language from the outline (e.g., Russian → Cyrillic, Chinese → CJK, etc.)
   - For each slide, verify that ALL visible text is rendered in the correct script
   - **FAIL criteria** (any one triggers mandatory regeneration):
     - Latin characters where Cyrillic/CJK/Arabic should be (transliteration)
     - Garbled/nonsensical characters (model failed to render the script)
     - Mixed scripts where outline specifies a single language (e.g., half-Cyrillic half-Latin in one word)
     - Missing text blocks (prompt specified text that doesn't appear on the slide)
   - If a slide fails this check, DO NOT score it — regenerate immediately with strengthened script instructions in the prompt

2. **Style Consistency Audit** — compare each slide against the **design direction from Step 3**:
   - **Background**: does the slide's background match the specified color/treatment? (e.g., if design says dark #0F0F1A, a pink gradient is a FAIL)
   - **Color palette**: are the accent colors from the design direction actually used? Are there colors that don't belong?
   - **Typography mood**: does the font style match? (e.g., geometric sans-serif vs. serif mismatch)
   - **Decorative elements**: consistent with the design direction? No out-of-style illustrations, clip-art, or cartoon characters unless explicitly specified
   - **FAIL criteria** (triggers mandatory regeneration):
     - Background color/treatment clearly different from design direction
     - Dominant colors not in the specified palette
     - Illustration style clashes with the deck aesthetic (e.g., anime character in a geometric-neon deck)
   - Pay **extra attention** to slides generated without a reference image (typically slides 1 and 2 before anchor selection, though the non-anchor should have been regenerated in Step 5.4)

3. **Text Readability**: font size adequate, sufficient contrast with background, text not clipped or cut off at edges

4. **Composition**: balanced layout, no empty/overcrowded areas, clear focal point

5. **Content Accuracy**: all specified text present and correct, no garbled or missing words

**Regeneration from Visual Review**: any slide that FAILs checks 1 or 2 MUST be regenerated with the style anchor as reference. Update the prompt to address the specific failure. Max 2 retries per slide. Log each regeneration reason in the score report.

**6c. Scoring** — run the Scoring Subroutine (`references/scoring-subroutine.md`):
- Score each slide on 6 axes (1-10): Visual Impact, Layout Uniqueness, Typography Drama, Color Conviction, Content Clarity, Decorative Quality
- **Style Consistency Gate** — **CRITICAL**: when scoring **Color Conviction** and **Decorative Quality**, score RELATIVE TO THE DESIGN DIRECTION from Step 3, not in isolation. A slide with beautiful colors that don't match the design direction scores LOW on Color Conviction. A slide with polished decorations in the wrong style scores LOW on Decorative Quality. Specifically:
  - Color Conviction ≤ 4 if the background color doesn't match the design direction
  - Color Conviction ≤ 5 if accent colors are outside the specified palette
  - Decorative Quality ≤ 4 if decorative elements clash with the deck's aesthetic style
- Write `score-report.md` in the output directory

**6d. Regeneration** — for each slide scoring < 6 on ANY single axis:
1. Analyze which axis failed and why
2. Modify the prompt to address the specific weakness
3. Regenerate the slide (with anchor reference if in reference mode)
4. Re-score the regenerated slide
5. Max 2 retries per slide. If still failing after 2 retries, keep the best version and note it in the report.

**6e. Content Review** — run the Content Review Subroutine (`references/content-review-subroutine.md`):
- 3-second test, narrative flow, redundancy, CTA clarity, information hierarchy
- CRITICAL issues → regenerate the affected slide with adjusted prompt
- MAJOR issues → regenerate if it's a text/content problem
- MINOR issues → note in report, do not regenerate

**6f. PDF Assembly**:
1. Check if Python 3 is available: `python3 --version` (or `python --version` on Windows)
2. If not available: print warning "Python not found. Skipping PDF assembly. PNG files are in <output-dir>/slides/". Stop here.
3. Ensure Pillow is installed: `pip install Pillow 2>/dev/null || pip3 install Pillow 2>/dev/null`
4. Assemble PDF:

```python
from PIL import Image
import os, re

png_dir = '<output-dir>/slides'
files = [f for f in os.listdir(png_dir) if f.endswith('.png')]
files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()))

images = []
for f in files:
    images.append(Image.open(os.path.join(png_dir, f)).convert('RGB'))

images[0].save(
    '<output-dir>/slides.pdf',
    save_all=True,
    append_images=images[1:],
    resolution=150.0,
    quality=95
)

for img in images:
    img.close()
```

5. Print: "PDF assembled: <output-dir>/slides.pdf"

**6g. Design Memory Write** — follow the write protocol in `references/design-memory.md`:
- Average score >= 7: write `success` entry
- Average score 5-6: write `neutral` entry
- Average score < 5: write `failure` entry

### Step 7: Output Summary

Print final summary:
```
Slidegen complete!

  Slides:    <output-dir>/slides/ (N slides)
  PDF:       <output-dir>/slides.pdf
  Prompts:   <output-dir>/prompts.json
  Metadata:  <output-dir>/meta.json
  Score:     <overall-avg>/10

  Provider:  <provider> / <model>
  Quality:   <resolution|quality> / <format>
  Mode:      reference (anchor: slide N) | no-reference
  QA:        N slides regenerated, N content fixes applied

  Preview:   open <output-dir>/slides/slide-01.png
```

### Slide Prompt Authoring Rules

**CRITICAL** — follow these when composing prompts in Step 4:

1. **Always specify exact text.** Every word on the slide must be in the prompt. Do not say "add a title" — write the actual title text.
2. **Always specify typography.** Include font size guidance (e.g., "large 48pt heading", "24pt body text"), weight ("bold heading"), and alignment ("centered", "left-aligned").
3. **Always include the style suffix.** Append it to every prompt for consistency.
4. **Always specify "16:9 aspect ratio presentation slide"** at the start or end of the prompt.
5. **Keep prompts under 2000 characters.** Longer prompts may confuse the model. Be specific but concise.
6. **Use English for prompts.** Even if the slide content is in another language, write the prompt instructions in English with the content text in its original language.
7. **Describe layout spatially.** Use terms like "top-left", "centered", "bottom third", "left half" rather than vague terms like "somewhere on the slide".
8. **Specify background explicitly.** Never leave background to the model's imagination — describe color, gradient, texture, or pattern.
9. **Avoid prompt conflicts.** Don't say "minimalist" and then request 5 decorative elements.
10. **Include contrast instructions.** If text is over a dark background, specify "white text". If over a light background, specify "dark text".
11. **Include slide role description.** Every prompt must contain the role description text for context:
    - `cover` → "This is a cover/title slide — prominent title, minimal body text"
    - `section` → "This is a section divider slide — section heading, transitional"
    - `content` → "This is a content slide — heading with body text, bullets, or key points"
    - `stat` → "This is a statistics/data slide — large numbers, charts, or key metrics"
    - `quote` → "This is a quote slide — prominent quotation with attribution"
    - `comparison` → "This is a comparison slide — two or more items side by side"
    - `end` → "This is a closing/thank-you slide — call to action or contact info"
12. **Non-Latin text rendering.** **CRITICAL** — if the slide content contains non-Latin characters (Cyrillic, CJK, Arabic, etc.), EVERY prompt MUST include the following instruction immediately after the slide type declaration: `"CRITICAL: All text on this slide MUST be rendered in [language] [script] exactly as written. Do NOT transliterate, substitute, or omit any [script] characters."` For example, for Russian: `"CRITICAL: All text on this slide MUST be rendered in Russian Cyrillic script exactly as written. Do NOT transliterate, substitute, or omit any Cyrillic characters."` Without this instruction, image generation models consistently garble non-Latin text into unreadable artifacts.
13. **No generic illustrations or clip-art.** Do not request cartoon characters, stock-photo-style illustrations, or clip-art people in prompts unless the outline explicitly calls for them. These tend to clash with geometric/modern slide aesthetics. Prefer abstract icons, geometric shapes, and data visualizations instead. If an illustration IS needed, specify its art style to match the presentation's visual direction (e.g., "flat geometric illustration in the same neon style").
