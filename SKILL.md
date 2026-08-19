---
name: open-uiux
description: >
  Design and build genuinely high-end web UI — cinematic hero sections, scroll-driven
  landing pages, and polished marketing sites. Use this skill whenever the task involves
  creating, redesigning, or critiquing a website, landing page, hero section, or any
  front-end UI where visual quality matters. Encodes the design system distilled from
  328 production-grade prompts from motionsites.ai.
license: MIT (skill) / Unlicense (upstream corpus)
---

# Open UI/UX — Building Websites That Look Expensive

## What this skill gives you

Most AI-generated websites fail the same way: centered text, a purple-blue gradient,
three equal cards with rounded corners, generic stock copy, `transition: all 0.3s`.
Technically correct, visually forgettable.

This skill encodes what separates that from work that looks *designed*. It is derived
from statistical and structural analysis of **328 production prompts** from
[motionsites.ai](https://motionsites.ai) (~2.87M characters, avg 8,755 chars/prompt) —
prompts written specifically to make AI produce high-end results.

The headline finding: **"premium" is not a style, it is a level of specificity.**
The corpus average prompt is 8,755 characters for what is often a *single hero section*.
Nothing is left to the model's default taste — every hex value, every easing curve,
every letter-spacing value is stated. That is the whole trick.

## The workflow

Follow these phases in order. Do not skip to code.

### Phase 1 — Commit to a direction (before any code)

Never start with a layout. Start with a **stance**. Write down, explicitly:

1. **One reference feeling** in 3–6 words — "brutalist swiss editorial", "wet obsidian
   fintech", "sun-bleached film-grain travel". Vague ("modern, clean, professional")
   guarantees generic output.
2. **The one signature move** — the single thing a visitor remembers. Cursor-following
   spotlight, horizontal-scroll pinned gallery, oversized type that crops off-canvas,
   a mask reveal on scroll. Exactly one. Two competing signatures read as noise.
3. **A concrete design system** — see `references/design-system.md`. Fill in real values,
   not placeholders.

If the user gave you a vague brief, pick a strong direction and state your choice in one
line. A committed opinion beats asking three clarifying questions.

### Phase 2 — Write the build spec

Write out the spec *before* the implementation, at the specificity level of
`examples/`. Every element gets: exact size (with a `clamp()` for fluid type), exact
color hex, exact weight and tracking, exact spacing, exact motion (duration + easing +
trigger + stagger). See `references/spec-template.md` for the structure to fill in.

This is the single highest-leverage step. A vague spec produces vague UI regardless of
how good the implementation is.

### Phase 3 — Build

Default stack, matching corpus dominance (React 84% · Tailwind 81% · TypeScript 61% ·
Framer Motion 34%):

```
React 18 + TypeScript + Vite + Tailwind CSS + framer-motion (motion/react) + lucide-react
```

Deviate when the task demands it (static HTML for a single artifact, Next.js for an
existing app) — but keep the *design* rules regardless of stack.

Consult, as needed:
- `references/design-system.md` — tokens: type scale, color, spacing, radius, shadow
- `references/motion.md` — easing curves, durations, scroll choreography, reduced-motion
- `references/layout-patterns.md` — hero archetypes, section rhythm, page skeletons
- `references/effects-cookbook.md` — copy-paste recipes for the signature effects
- `references/quality-bar.md` — the anti-generic checklist and self-review pass

### Phase 4 — Self-review against the quality bar

Before declaring done, run `references/quality-bar.md` against your own output. It
contains the failure modes that make AI UI recognizable as AI UI. Fix what it catches.

## Non-negotiables

These come straight from what the corpus does relentlessly, and what it never does.

1. **Type carries the design.** A hero headline is `clamp(2.5rem, 8vw, 7rem)`, not
   `text-5xl`. Tight tracking (`-0.02em` to `-0.05em`) and tight leading (`0.9`–`1.0`)
   at display sizes. `tracking-tight` appears 332× in the corpus; `clamp(` appears 647×.
2. **Contrast over decoration.** Premium reads as: near-black or off-white ground, one
   accent used *once or twice per screen*, and large fields of empty space. The top
   corpus colors are `#ffffff`, `#000000`, `#1a1a1a`, `#111111`, `#0a0a0a` — pure
   neutrals. Color is punctuation, not paint.
3. **One accent, deployed sparingly.** If everything is highlighted, nothing is.
4. **Motion is choreography, not decoration.** 300–800ms, ease-out or spring, staggered
   60–120ms, triggered on scroll-into-view, `once: true`. Never animate everything.
5. **Never center everything.** Asymmetry, off-grid placement, and deliberate overflow
   are what read as "designed". The corpus crops type off-canvas constantly.
6. **Real content, always.** Write plausible product copy, real names, real numbers.
   Never ship "Lorem ipsum", "Feature One", or "Your Company Here".
7. **Full-bleed first screen.** `h-screen` / `100dvh`, one dominant focal element,
   brand identity legible in under 3 seconds.
8. **Respect the user.** `prefers-reduced-motion`, real focus states, `alt` text,
   keyboard reachability, and AA contrast on actual text.

## Using the prompt corpus

Three committed artifacts let you mine the source material:

| File | What it is | When to use it |
|---|---|---|
| `assets/prompt-catalog.md` | All 328 prompts, one line each, grouped by category | Browsing for direction |
| `assets/prompt-index.json` | Same, structured: effects, stack, fonts, palette per prompt | Programmatic filtering |
| `assets/corpus-stats.json` | Aggregate frequencies: colors, fonts, easings, effects | Settling "what's typical" |
| `examples/*.md` | 18 full gold-standard prompts, verbatim | Calibrating spec depth |

Find prompts matching an effect:

```bash
python3 scripts/find_prompts.py --effect cursor-spotlight --effect scroll-pin
python3 scripts/find_prompts.py --query "luxury ecommerce" --limit 5
python3 scripts/find_prompts.py --stats
```

Read at least one file in `examples/` before writing a spec for an unfamiliar effect —
it recalibrates how much detail "enough detail" actually is.

> The full 2.9 MB verbatim prompt corpus is **not** committed here (it belongs to the
> upstream project). Regenerate it locally into `local/` with:
> `git clone --depth 1 https://github.com/xianxian-sensen/motionsites-prompts /tmp/msp && python3 scripts/build_corpus.py --src /tmp/msp --out .`

## Attribution

Prompt corpus: [xianxian-sensen/motionsites-prompts](https://github.com/xianxian-sensen/motionsites-prompts),
released under the Unlicense, scraped from [motionsites.ai](https://motionsites.ai).
This skill contributes the analysis, taxonomy, distilled design rules, and tooling.
