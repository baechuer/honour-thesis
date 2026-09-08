---
name: pixijs-2d
description: "Use this skill first for ANY PixiJS v8 task; it routes to the right specialized skill for the job. Covers the core PixiJS surface: Application setup, the scene graph (Container, Sprite, Graphics, Text), rendering (WebGL/WebGPU/Canvas, render loop), assets, events, filters, and the ticker. Triggers on: pixi, pixi.js, pixijs, PixiJS, v8, Application, app.init, Sprite, Container, Graphics, Text, Assets, Ticker, renderer, WebGL, WebGPU, scene graph, filter, texture, BitmapText, how do I draw, how do I render, how do I animate in pixi."
license: MIT
metadata:
  author: PixiJS (docs) / Emmraan
  version: 1.0.0
  domain: 2d-graphics
  triggers:
    - pixi
    - pixi.js
    - pixijs
    - application
    - sprite
    - graphics
    - ticker
---

Entry point for the PixiJS v8 skill collection. PixiJS is the fastest library available for the web, working across all devices and allowing you to create rich, interactive graphics and cross-platform applications using WebGL, WebGPU, and Canvas as a fallback.

## How to use this skill

1. Find the specialized skill in the router below that best matches the task.
2. Load that skill's `SKILL.md` and follow its guidance.
3. If no sub-skill fits (the task references a specific class, function, option, or API surface not listed below), **WebFetch `https://pixijs.download/release/docs/llms.txt`**. That file is the auto-generated, always-current index of the full PixiJS API and guides. Each entry links to a `.html.md` page you can WebFetch for the detailed content.

## Skill router

### Foundations

| Skill | Load when... |
|---|---|
| [pixijs-application](./pixijs-application/SKILL.md) | Creating or configuring a PixiJS `Application`, calling `app.init()`, accessing `app.stage`/`renderer`/`canvas`/`screen`, resize/ticker plugins, `app.destroy()`. |
| [pixijs-core-concepts](./pixijs-core-concepts/SKILL.md) | Understanding the renderer pipeline, choosing WebGL/WebGPU/Canvas, render loop internals, systems and pipes. |

### Scene Objects

| Skill | Load when... |
|---|---|
| [pixijs-scene-container](./pixijs-scene-container/SKILL.md) | Working with `Container`: `addChild`/`removeChild`, transforms, `zIndex`, bounds, `toGlobal`/`toLocal`, `destroy`. |
| [pixijs-scene-sprite](./pixijs-scene-sprite/SKILL.md) | Drawing images: `Sprite`, `AnimatedSprite`, `NineSliceSprite`, `TilingSprite`. |
| [pixijs-scene-graphics](./pixijs-scene-graphics/SKILL.md) | Drawing vector shapes or paths: `Graphics`, `GraphicsContext`, `fill`/`stroke`, `FillGradient`, SVG. |
| [pixijs-scene-text](./pixijs-scene-text/SKILL.md) | Rendering text: `Text`, `BitmapText`, `HTMLText`, `SplitText`, `TextStyle`. |

### Utilities

| Skill | Load when... |
|---|---|
| [pixijs-assets](./pixijs-assets/SKILL.md) | Loading resources: `Assets.init`, `Assets.load`, bundles, manifests, spritesheets, caching. |
| [pixijs-events](./pixijs-events/SKILL.md) | Handling pointer/mouse/touch/wheel input: `eventMode`, `FederatedEvent`, `hitArea`, `cursor`, drag. |
| [pixijs-ticker](./pixijs-ticker/SKILL.md) | Per-frame logic or controlling the render loop: `Ticker`, `deltaTime`, `UPDATE_PRIORITY`, `maxFPS`. |

### Effects

| Skill | Load when... |
|---|---|
| [pixijs-filters](./pixijs-filters/SKILL.md) | Applying visual effects: `BlurFilter`, `ColorMatrixFilter`, `DisplacementFilter`, `Filter.from`, `pixi-filters`. |

## Fallback: canonical PixiJS docs

If the task references a class, function, option, or API surface not covered by any sub-skill above, **WebFetch `https://pixijs.download/release/docs/llms.txt`**. It's the auto-generated index of the full PixiJS API and guides, regenerated on every release. Each entry links to a `.html.md` page you can WebFetch for the detailed content. Use this fallback whenever the router table doesn't point at an obvious match.
