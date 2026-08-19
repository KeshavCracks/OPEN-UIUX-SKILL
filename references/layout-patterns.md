# Layout Patterns — Structure That Reads as Designed

225 of 328 corpus prompts are hero sections; 60 are full landing pages. The first screen
is where the corpus spends most of its effort, and so should you.

---

## 1. Hero archetypes

Pick one deliberately. Each has a different center of gravity.

### A. Full-bleed media + overlaid type
*The most common corpus hero (203 prompts include video backgrounds).*

```
┌──────────────────────────────────┐
│  nav                             │
│                                  │
│        MASSIVE HEADLINE          │   full-bleed image/video
│        sub-copy line             │   + dark scrim
│        [ CTA ]                   │
│                                  │
│  caption ↓            meta/right │
└──────────────────────────────────┘
```
- `h-screen` with `style={{ height: '100dvh' }}` — `dvh` fixes mobile browser chrome.
- Media: `absolute inset-0 object-cover`, `z-10`.
- Scrim: `absolute inset-0 bg-black/40` or
  `bg-gradient-to-t from-black/80 via-black/20 to-transparent`. **Never skip the scrim** —
  text over unmodified media is the #1 legibility failure.
- Content: `relative z-50`.
- Anchor small elements in the bottom corners (`absolute bottom-10 left-10`) — the corpus
  does this constantly and it instantly reads as art-directed rather than centered-default.

### B. Editorial split
```
┌────────────────┬─────────────────┐
│  HEADLINE      │                 │
│  body copy     │     image       │
│  [CTA]         │                 │
└────────────────┴─────────────────┘
```
- Asymmetric ratio: `grid-cols-[1.2fr_1fr]` or `[7fr_5fr]`. Never `50/50` — even splits
  look like a template.
- Let the image bleed off the right edge of the viewport.

### C. Oversized type as the hero
```
┌──────────────────────────────────┐
│ small eyebrow                    │
│ HUGE                             │
│ TYPE THAT                        │
│ FILLS THE SCREEN                 │
│              ↘ small meta block  │
└──────────────────────────────────┘
```
- `text-[14vw]` … `text-[17.5vw]`, `leading-none`, `tracking-tight`, sometimes
  `whitespace-nowrap` with `overflow-hidden` so it crops at the edges.
- Requires near-zero decoration. The type *is* the design.
- Gradient text is a corpus favourite here:
  `bg-gradient-to-b from-[#646973] to-[#BBCCD7] bg-clip-text text-transparent`.

### D. Centered minimal
```
┌──────────────────────────────────┐
│              eyebrow             │
│         Focused Headline         │
│        one line of sub-copy      │
│        [ CTA ]  [ ghost ]        │
│         ┌──────────────┐         │
│         │  product UI  │         │
└─────────┴──────────────┴─────────┘
```
- The SaaS default. Safe but generic — earn it with an exceptional type scale, a
  distinctive background treatment (grid, glow, noise), and a real product screenshot.
- If you use this, the *background* must carry the personality.

### E. Interactive signature
Cursor spotlight, hover-reveal grid, draggable object, WebGL plane. One striking
interaction with minimal supporting content. See `effects-cookbook.md`.

---

## 2. Landing page skeleton

Corpus component frequency (CTA 505, pricing 250, stats 236, hero 183, marquee 170):

```
1  Nav               sticky, transparent → solid on scroll
2  Hero              full viewport, one focal point, primary CTA
3  Social proof      logo marquee or a one-line stat strip   ← immediately after hero
4  Problem/Value     2–3 blocks, alternating alignment
5  Features          bento or 3-col grid, staggered reveal
6  Showcase          product visual, screenshot, or case study
7  Metrics           3–4 big numbers, tabular-nums, count-up
8  Testimonials      1 large quote > 6 small cards
9  Pricing           3 tiers, middle emphasized
10 FAQ               accordion, 5–7 items
11 CTA               full-bleed, high contrast, single action
12 Footer            multi-column, oversized wordmark
```

Not every page needs all twelve. A strong page uses 6–8 and gives each real space.

### Rhythm rules
- **Alternate density.** Dense section → airy section → dense. Uniform density reads flat.
- **Alternate ground.** Dark → slightly lighter → dark. Sections that share a background
  need clearly distinct spacing to avoid merging.
- **One focal point per section.** If a section has two competing focal elements, split it.
- **Vary alignment.** Do not left-align every section header. Move one to center, one to
  a `grid-cols-[1fr_2fr]` split.

---

## 3. Section header pattern

The corpus's standard section opener:

```jsx
<div className="flex flex-col gap-4 max-w-3xl">
  <span className="text-xs uppercase tracking-[0.2em] text-white/50 font-mono">
    01 — Capabilities
  </span>
  <h2 className="text-[clamp(32px,4vw,56px)] leading-[1.05] tracking-[-0.03em]">
    Everything you need, nothing you don't
  </h2>
  <p className="text-white/60 text-lg max-w-[55ch] leading-relaxed">
    Supporting sentence that adds information rather than restating the headline.
  </p>
</div>
```

The mono, uppercase, wide-tracked eyebrow with a number is a signature move — it costs
one line and immediately reads editorial.

---

## 4. Cards

Default card:

```jsx
<div className="group relative rounded-2xl border border-white/10 bg-white/[0.03] p-8
                transition-[transform,border-color] duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]
                hover:-translate-y-1 hover:border-white/20">
  <Icon className="size-5 text-white/70" strokeWidth={1.5} />
  <h3 className="mt-6 text-xl tracking-[-0.01em]">Title</h3>
  <p className="mt-2 text-white/55 leading-relaxed">Body copy that says something specific.</p>
</div>
```

**Break the uniform grid.** Three identical cards is the most generic possible layout.
Use a bento instead — vary the spans:

```jsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:auto-rows-[220px]">
  <div className="md:col-span-2 md:row-span-2">…</div>  {/* hero cell */}
  <div>…</div>
  <div>…</div>
  <div className="md:col-span-3">…</div>                 {/* wide cell */}
</div>
```

One cell should be visually dominant. Equal-weight grids have no hierarchy.

---

## 5. Navigation

```jsx
<header className="fixed top-0 inset-x-0 z-50 transition-colors duration-300
                   bg-transparent data-[scrolled=true]:bg-black/70
                   data-[scrolled=true]:backdrop-blur-md
                   data-[scrolled=true]:border-b data-[scrolled=true]:border-white/10">
```

- Transparent over the hero, then solid + `backdrop-blur` after ~80px of scroll.
- Height 64–80px. Wordmark left, links center or right, one CTA button far right.
- Nav links: `text-sm`, `text-white/70`, `hover:text-white`, 200ms.
- Mobile: full-screen overlay panel, not a cramped dropdown. Animate with a clip or
  slide, stagger the links in at 0.05s.

---

## 6. Buttons

```jsx
/* Primary — the one accent moment */
<button className="rounded-full bg-white px-7 py-3.5 text-sm font-medium text-black
                   transition-transform duration-200 hover:scale-[1.02] active:scale-[0.98]">
  Get started
</button>

/* Secondary — ghost */
<button className="rounded-full border border-white/20 px-7 py-3.5 text-sm
                   text-white/90 transition-colors duration-200
                   hover:border-white/40 hover:bg-white/5">
  Read the docs
</button>
```

- `rounded-full` is the corpus default (694 hits).
- Comfortable padding: `px-6 py-3` minimum; cramped buttons read cheap.
- **Exactly one primary CTA per viewport.** Two primaries = no primary.
- Always ship `:hover`, `:active`, `:focus-visible`, and `:disabled`.
- Minimum 44×44px touch target.

---

## 7. Footer

Underrated as a premium signal. The corpus treats it as a real section:

- Multi-column link grid, generous `py-20`.
- An **oversized wordmark** — often `text-[12vw]`, low contrast (`text-white/5`), placed
  behind or below the links. Very high impact, near-zero effort.
- Newsletter input with an inline pill submit.
- Bottom bar: copyright, legal links, socials, `text-xs text-white/40`.

---

## 8. Responsive discipline

Where AI-generated pages usually break:

| Problem | Fix |
|---|---|
| Display type overflows on mobile | `clamp()` with a sane min; test at 320px |
| Fixed `h-screen` clipped by mobile chrome | use `100dvh` |
| Horizontal-scroll section unusable on touch | vertical stack below `md` |
| Hover-only reveals invisible on touch | always-visible under `lg` |
| Sidebars squeezing content | hide below `lg`, replace with a sheet |
| Absolute-positioned decor overlapping text | `hidden sm:block` on decorative layers |
| Page scrolls sideways | `overflow-x: clip` on the wrapper + find the offender |

Test at **320 / 768 / 1024 / 1440 / 1920**. The corpus writes explicit
`@media (max-width: 768px)` blocks (47 hits) rather than hoping utilities cover it.
