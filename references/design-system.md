# Design System — Tokens That Read as Expensive

Every value below is grounded in frequency analysis of the 328-prompt corpus. Where a
number appears, it is the number the corpus actually uses, not a guess.

Fill this out **before** writing components. A design system defined after the fact is
just a description of accidents.

---

## 1. Typography

Type is where premium is won or lost. It gets the most attention in the corpus by a
wide margin.

### Fluid display type — always `clamp()`

`clamp(` appears **647 times** across the corpus. Display type is never a fixed size and
never a bare Tailwind step like `text-5xl`. It scales with the viewport.

The shape is always `clamp(min, preferred-vw, max)`:

```css
/* Real values pulled from the corpus */
--fs-display : clamp(40px, 6.5vw, 105px);   /* hero headline — most common shape */
--fs-h1      : clamp(3rem, 10vw, 140px);    /* oversized editorial hero */
--fs-h2      : clamp(32px, 4vw, 56px);      /* section headline */
--fs-h3      : clamp(24px, 3vw, 48px);
--fs-lead    : clamp(18px, 2vw, 34px);      /* hero subcopy */
--fs-body    : clamp(16px, 1.25vw, 20px);
--fs-caption : clamp(12px, 0.86vw, 14px);   /* labels, eyebrows */
```

Tailwind equivalent — put the arbitrary value inline:

```jsx
<h1 className="text-[clamp(40px,6.5vw,105px)] leading-[0.95] tracking-[-0.04em]">
```

Rule of thumb: the `vw` term should be large enough that the headline nearly fills its
container at every width. If the headline looks small on a 1440px screen, the `vw` is
too low.

### Tracking (letter-spacing)

Tight at display sizes, loose at label sizes. This inversion is the single most reliable
typographic tell of professional work.

| Role | Value | Corpus hits |
|---|---|---|
| Huge display (>72px) | `-0.04em` … `-0.05em` | 34 / 22 |
| Headline (40–72px) | `-0.02em` … `-0.03em` | 86 / 41 |
| Body | `-0.01em` … `0` | 38 |
| Eyebrow / label / nav (uppercase, small) | `0.15em` … `0.3em` | 23 / 30 |

`tracking-tight` alone appears 332 times. Never leave display type at default tracking.

### Leading (line-height)

| Role | Value | Corpus hits |
|---|---|---|
| Display headline | `0.9` – `1.05` | 45 / 56 / 61 |
| Sub-headline | `1.1` – `1.2` | 52 / 30 |
| Body paragraph | `1.5` – `1.6` | 21 / 38 |

Display type at `leading-normal` is the most common amateur mistake. Set it to `0.95`.

### Font pairing

The corpus converges hard on a small set. Top families by frequency:

| Font | Hits | Role |
|---|---|---|
| Inter | 53 | Default UI/body sans — the safe, correct choice |
| Instrument Serif | 38 | Display serif for editorial contrast |
| Manrope | 16 | Geometric sans, warmer than Inter |
| Barlow | 13 | Condensed-friendly, technical |
| JetBrains Mono | 9 | Labels, data, code, timestamps |
| Anton | 8 | Ultra-bold poster display |
| Geist | 8 | Modern neutral (Vercel) |
| Space Grotesk | 6 | Quirky-technical display |

**The three-role system** — assign each font a job, never let one font do everything:

1. **Sans body** — Inter / Geist / Manrope. Readability. 400–500 weight.
2. **Display** — either the same sans at 600–900 and huge, *or* a contrasting serif
   (Instrument Serif, Playfair Display, italic) for editorial tension.
3. **Mono accent** — JetBrains Mono / IBM Plex Mono for eyebrows, metadata, stats,
   `tabular-nums` figures. Used small and uppercase with wide tracking.

Load pattern used throughout the corpus:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');
```

Always include `&display=swap`. Always set `-webkit-font-smoothing: antialiased` and
`-moz-osx-font-smoothing: grayscale` on the root (25 / 16 hits) — it visibly thins type
on dark backgrounds, which is the look.

---

## 2. Color

### The corpus palette is overwhelmingly neutral

Top colors across 2,693 hex occurrences:

```
#ffffff  137    #1a1a1a   59    #0a0a0a   35    #f5f5f5   26
#000000   74    #111111   49    #f0f0f0   30    #0c0c0c   25
```

Seven of the top eight are pure greyscale. **Premium is neutrals plus restraint**, not a
colorful palette. When color does appear it is a single saturated accent:
`#ffda00` (22), `#85d743` (14), `#3b82f6` (12).

### Build a palette with this structure

```css
:root {
  /* Ground — pick a dark OR light stance and commit */
  --bg:            #0a0a0a;   /* never pure #000 for large fields; #0a0a0a reads richer */
  --bg-elevated:   #141414;   /* cards, panels — one step up, not a border */
  --bg-inset:      #050505;

  /* Ink — never pure white on dark; it vibrates */
  --fg:            #f5f5f5;
  --fg-muted:      rgba(245,245,245,0.62);
  --fg-subtle:     rgba(245,245,245,0.38);

  /* Hairlines — the corpus does borders as alpha, not solid greys */
  --line:          rgba(255,255,255,0.10);
  --line-strong:   rgba(255,255,255,0.20);

  /* Exactly ONE accent */
  --accent:        #ffda00;
  --accent-ink:    #0a0a0a;   /* text color that sits on the accent */
}
```

### Rules

1. **Never pure black on a large field.** `#0a0a0a`/`#111111` have depth; `#000000` goes
   flat and makes shadows impossible. Use `#000` only for true-black video letterboxing.
2. **Never pure white text on dark.** `#f5f5f5` or `rgba(255,255,255,0.92)`. Pure white
   at large sizes glares and halos.
3. **Borders are alpha, not grey.** `border-white/10` (242 hits for `/10`) survives on
   any background; `#333` only works on one.
4. **One accent, two appearances max per viewport.** Primary CTA + one highlighted word
   or stat. That is the whole budget.
5. **Layer with alpha, not new hexes.** `bg-white/5`, `bg-white/10` (305 hits for
   `bg-white/`) give consistent elevation without palette sprawl.

### Light-mode variant

Light "premium" is harder and rarer. If you go light: off-white ground (`#fefffc`,
`#f7f8f8`, `#f0f1f3` — all in the corpus), near-black ink (`#1a1a1a`, `#2c2c2c`), and
**2px** borders in a warm grey (`#dde3dd`) rather than 1px cool grey. Light designs need
heavier hairlines to avoid looking washed out.

---

## 3. Spacing & rhythm

Use a strict scale. Arbitrary spacing is the fastest way to look unconsidered.

```
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 160 · 200
```

| Context | Value |
|---|---|
| Section vertical padding (desktop) | `py-24` … `py-40` (96–160px) |
| Section vertical padding (mobile) | `py-16` … `py-20` |
| Page horizontal gutter | `px-5` mobile → `px-10` tablet → `px-14`/`px-20` desktop |
| Max content width | `max-w-7xl` (1280px); text columns `max-w-[65ch]` |
| Grid gap | `gap-4` … `gap-8` |

**Generous whitespace is the cheapest premium signal available.** When a layout looks
cheap, the fix is almost always more space around the focal element, not more elements.

Fluid section padding, corpus style:

```css
padding-block: clamp(64px, 10vh, 160px);
```

---

## 4. Radius

Pick one radius language and hold it. Mixing radii is a strong amateur tell.

| Language | Values | Feel |
|---|---|---|
| Sharp / editorial | `0` … `4px` | Swiss, brutalist, fashion, luxury |
| Soft / product | `12px` (`rounded-xl`) … `16px` (`rounded-2xl`, 171 hits) | SaaS default |
| Pill | `9999px` (`rounded-full`, **694 hits**) | Buttons, tags, avatars |

Note how dominant `rounded-full` is: the corpus almost universally makes **buttons and
pills fully round** while keeping **cards at `rounded-2xl` or sharp**. That contrast —
round buttons, squarer cards — is itself part of the look.

Nested radius rule: inner radius = outer radius − padding. A 16px card with 8px padding
holds a 8px inner element.

---

## 5. Elevation & surface

The corpus almost never uses classic drop shadows on dark themes. Depth comes from:

1. **Alpha layering** — `bg-white/5` over the ground.
2. **Hairline top-highlight** — the inset trick that makes a surface look lit:
   ```css
   box-shadow: 0 8px 32px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.5);
   ```
3. **Backdrop blur** — `backdrop-blur` / `backdrop-filter` appear **416 times**:
   ```css
   background: linear-gradient(rgba(255,255,255,0.35), rgba(255,255,255,0.12));
   backdrop-filter: blur(16px);
   -webkit-backdrop-filter: blur(16px);   /* always ship the prefix — 36 hits */
   border: 1px solid rgba(255,255,255,0.2);
   ```
4. **Glow** instead of shadow on dark: `box-shadow: 0 0 80px -20px var(--accent)`.

For light themes, use real but soft shadows: `0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06)`.
Never `box-shadow: 0 4px 6px rgba(0,0,0,0.3)` — the hard grey shadow of default UI kits.

---

## 6. Grid & breakpoints

Corpus breakpoint frequency: `768` (47), `1024` (8), `640` (8), `900` (7), `520` (8).
Tailwind defaults align well — use them.

```
sm 640 · md 768 · lg 1024 · xl 1280
```

Usage skews `md:` (1,894) and `sm:` (1,722) over `lg:` (840): **most responsive work
happens at the phone→tablet boundary.** Design desktop-first for the visual, then fix
the sub-768px collapse carefully — that is where AI output usually breaks.

Standard collapse behaviour:
- Multi-column grids → single column
- Display type → drop the `vw` term's effect via a lower `clamp()` min
- Fixed sidebars → hidden or a sheet
- Horizontal-scroll sections → vertical stack or native snap-scroll
- Hover-only affordances → always-visible on touch

---

## 7. Iconography & imagery

- **Icons:** `lucide-react` (185 prompts). Consistent stroke width — `1.5` for elegant,
  `2` for sturdy. Never mix icon libraries. Size icons in even steps: 16/20/24.
- **Images:** always `object-cover` with an explicit `aspect-[16/9]`/`aspect-[4/5]`.
  Never let images set their own height. Add `loading="lazy"` below the fold.
- **Video backgrounds** appear in 203 prompts — the most common single effect. Always
  `autoPlay loop muted playsInline` plus a scrim overlay
  (`bg-black/40` or a gradient) so text stays legible.
- **Grain/noise overlay** (26 prompts) is a cheap, high-impact premium texture:
  ```css
  .grain::after {
    content:''; position:absolute; inset:0; pointer-events:none; opacity:.035;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  ```
