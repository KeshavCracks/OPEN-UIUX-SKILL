# OPEN-UIUX-SKILL

An agent skill for building websites that look **designed** rather than generated.

Distilled from statistical and structural analysis of **328 production-grade website
prompts** from [motionsites.ai](https://motionsites.ai)

> **The core finding:** "premium" is not a visual style — it is a *level of specificity*.
> The average corpus prompt spends 8,755 characters on what is often a single hero
> section, specifying every hex value, easing curve, and letter-spacing. Nothing is left
> to the model's default taste. This skill encodes those defaults so an agent has good
> taste before it starts.

---

## Install

Drop the repo into your agent's skills directory:

```bash
git clone https://github.com/KeshavCracks/OPEN-UIUX-SKILL ~/.claude/skills/open-uiux
```

Any agent runtime that reads `SKILL.md` front-matter (Claude Skills, Cursor rules, or a
plain system-prompt include) can use it. The entry point is [`SKILL.md`](SKILL.md);
everything else is loaded on demand.

---

## Layout

```
SKILL.md                        entry point — workflow + non-negotiables
references/
  design-system.md              type scale, color, spacing, radius, elevation tokens
  motion.md                     easing curves, durations, scroll choreography, a11y
  layout-patterns.md            hero archetypes, page skeleton, nav/cards/footer
  effects-cookbook.md           15 copy-paste recipes for the signature effects
  quality-bar.md                anti-generic audit + structured self-review
  spec-template.md              the pre-code build spec to fill in
assets/
  prompt-catalog.md             all 328 prompts, one line each, by category
  prompt-index.json             structured index: effects, stack, fonts, palette
  corpus-stats.json             aggregate frequencies behind every claim in the docs
examples/                       18 verbatim gold-standard prompts
scripts/
  find_prompts.py               search the index
  build_corpus.py               regenerate all artifacts from upstream
demo/
  index.html                    the skill applied to itself — a reference build
```

### Demo

[`demo/index.html`](demo/index.html) is a single-file page built by following this skill
end to end — neutral ground with one accent, `clamp()` display type at `-0.045em`,
expo-out motion, a bento with one dominant cell, mask-composite gradient borders, a
lerped cursor spotlight, and full reduced-motion handling. Open it directly, or:

```bash
python3 -m http.server 3000 --directory demo
```

It doubles as a worked example of the tokens in `references/design-system.md`.

---

## Searching the corpus

```bash
python3 scripts/find_prompts.py --stats                  # what's in there
python3 scripts/find_prompts.py --list-effects           # every filterable tag
python3 scripts/find_prompts.py --effect cursor-spotlight
python3 scripts/find_prompts.py --effect scroll-pin --stack gsap
python3 scripts/find_prompts.py -q "luxury ecommerce" -n 5
python3 scripts/find_prompts.py --effect marquee --json
```

---

## What the analysis found

Every rule in `references/` is backed by frequency data, not opinion. A sample:

| Signal | Finding |
|---|---|
| Stack | React 84% · Tailwind 81% · TypeScript 61% · Framer Motion 34% |
| Easing | `cubic-bezier(0.16, 1, 0.3, 1)` dominates (85 uses), then `(0.22, 1, 0.36, 1)` (60) |
| Color | 7 of the top 8 colors are pure greyscale — premium is neutrals + one accent |
| Type | `clamp()` 647× · `tracking-tight` 332× — fluid, tightly tracked display type |
| Motion | Reveals 600–800ms, hovers 150–250ms, staggers 60–120ms |
| Top effect | Video backgrounds (203 prompts), then dark themes (174), glassmorphism (173) |
| Gap | `prefers-reduced-motion` appears in only 19 of 328 prompts — the skill fixes this |

Full numbers in [`assets/corpus-stats.json`](assets/corpus-stats.json).

---

## Regenerating the data

The full 2.9 MB verbatim prompt corpus is **deliberately not committed** — it belongs to
the upstream project. Only derived metadata, statistics, and a curated exemplar set ship
here. To materialise the full text locally (into the gitignored `local/`):

```bash
git clone --depth 1 https://github.com/xianxian-sensen/motionsites-prompts /tmp/msp
python3 scripts/build_corpus.py --src /tmp/msp --out .
```

This regenerates `assets/`, `examples/`, and `local/motionsites-all-prompts.{md,json}`.

---

## Attribution & license

- **Prompt corpus:** scraped from
  [motionsites.ai](https://motionsites.ai).
- **This skill** — the taxonomy, analysis, distilled design guidance, and tooling — is
  MIT licensed. See [LICENSE](LICENSE).
