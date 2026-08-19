# Build Spec Template

Fill this in **before** writing code. The corpus average is 8,755 characters of spec for
what is often one section — that specificity *is* the quality difference. Every `‹›`
below must become a concrete value. If you leave one vague, the implementation will be
vague in exactly that place.

Delete sections that don't apply. Keep the specificity.

---

```markdown
# ‹Project name› — ‹Section or page›

## 0. Direction
- **Feeling (3–6 words):** ‹e.g. wet obsidian precision fintech›
- **Signature move:** ‹exactly one — e.g. cursor-spotlight reveal on hero›
- **Reference tension:** ‹what contrasts with what — e.g. 120px display type vs 11px mono labels›
- **Ground:** ‹dark | light›

## 1. Stack
- React 18 + TypeScript + Vite
- Tailwind CSS ‹v3 | v4›
- framer-motion (`import { motion } from "motion/react"`)
- lucide-react for icons
- ‹any extra: gsap/ScrollTrigger, lenis, swiper›

## 2. Fonts
```css
@import url('https://fonts.googleapis.com/css2?family=‹Family›:wght@‹weights›&display=swap');
```
- Body/UI: **‹Inter›** — weights ‹400, 500›
- Display: **‹Instrument Serif, italic›**
- Mono/labels: **‹JetBrains Mono›** — weight ‹400›, uppercase, `tracking-[0.2em]`
- Root: `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`

## 3. Color tokens
```css
:root {
  --bg:          ‹#0a0a0a›;
  --bg-elevated: ‹#141414›;
  --fg:          ‹#f5f5f5›;
  --fg-muted:    ‹rgba(245,245,245,0.62)›;
  --fg-subtle:   ‹rgba(245,245,245,0.38)›;
  --line:        ‹rgba(255,255,255,0.10)›;
  --line-strong: ‹rgba(255,255,255,0.20)›;
  --accent:      ‹#ffda00›;
  --accent-ink:  ‹#0a0a0a›;
}
```
Accent appears exactly at: ‹primary CTA› and ‹one highlighted stat›.

## 4. Type scale
| Role | Size | Weight | Tracking | Leading |
|---|---|---|---|---|
| Display | `clamp(‹40px›, ‹6.5vw›, ‹105px›)` | ‹500› | ‹-0.04em› | ‹0.95› |
| H2 | `clamp(‹32px›, ‹4vw›, ‹56px›)` | ‹500› | ‹-0.03em› | ‹1.05› |
| H3 | `clamp(‹24px›, ‹3vw›, ‹32px›)` | ‹500› | ‹-0.02em› | ‹1.15› |
| Lead | `clamp(‹18px›, ‹2vw›, ‹24px›)` | ‹400› | ‹-0.01em› | ‹1.5› |
| Body | `clamp(‹16px›, ‹1.25vw›, ‹18px›)` | ‹400› | ‹0› | ‹1.6› |
| Label | ‹12px› | ‹500› | ‹0.2em› uppercase | ‹1› |

## 5. Spacing & radius
- Scale: `4 8 12 16 24 32 48 64 96 128 160`
- Section padding: `clamp(‹64px›, ‹10vh›, ‹160px›)` block, `px-‹5› sm:px-‹10› lg:px-‹14›`
- Max width: ‹1280px›; text column ‹65ch›
- Radius: cards ‹16px›, buttons ‹9999px›, inputs ‹12px›

## 6. Motion tokens
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-std: cubic-bezier(0.4, 0, 0.2, 1);
```
- Hover: ‹200ms› `--ease-std`
- Reveal: ‹800ms› `--ease-out`, `initial={{opacity:0,y:20}}`, `viewport={{once:true,margin:"-100px"}}`
- Stagger: ‹0.08s›
- Reduced motion: all of the above collapse to instant

## 7. Layout structure
Root: `‹min-h-screen bg-[--bg] text-[--fg] antialiased›`

### Section ‹N›: ‹Name›
- **Container:** ‹exact classes›
- **Grid:** ‹grid-cols-[1.2fr_1fr] gap-16, collapsing to 1 col under md›
- **Elements**, in z-order:
  1. ‹Layer name› — `‹exact classes›` — ‹exact copy or asset›
  2. …
- **Copy:**
  - Eyebrow: "‹real text›"
  - Headline: "‹real text›"
  - Sub: "‹real text›"
  - CTA: "‹real verb phrase›"
- **Motion:** ‹what animates, trigger, duration, easing, stagger›
- **Hover states:** ‹element → change, duration›
- **Responsive:** at ‹768px› ‹exact change›; at ‹520px› ‹exact change›

## 8. Assets
- ‹name›: `‹exact URL or path›` — ‹aspect ratio, object-fit, alt text›
- Video: `‹url›` — `autoPlay loop muted playsInline`, poster `‹url›`, scrim ‹bg-black/40›

## 9. Content
Real copy for every string. Real names, real numbers, plausible claims.
- ‹list every piece of user-visible text›

## 10. Acceptance checklist
- [ ] No horizontal overflow at 320px
- [ ] Display type fills its container at 1440px
- [ ] Contrast ≥ 4.5:1 on body text
- [ ] Every interactive element has hover + focus-visible
- [ ] `prefers-reduced-motion` honored
- [ ] No console errors; all RAF/listeners cleaned up
- [ ] ‹signature move› works and degrades gracefully on touch
```

---

## Worked example (abbreviated)

> **Direction:** wet obsidian precision fintech. Signature: cursor-tracked gradient
> border on the pricing cards. Tension: 96px display against 11px mono labels.
>
> **Fonts:** Inter 400/500 body; Instrument Serif italic display; JetBrains Mono labels.
>
> **Color:** `--bg #0a0a0a`, `--fg #f5f5f5`, `--fg-muted rgba(245,245,245,.62)`,
> `--line rgba(255,255,255,.10)`, `--accent #85d743` (used only on the "Start free"
> button and the "+312%" stat).
>
> **Hero:** `h-[100dvh]`, grid `[1.2fr_1fr]`, `px-14`.
> H1 `clamp(48px,7vw,112px)/0.95/-0.04em`, two lines, mask-revealed from `y:110%`,
> 0.9s `cubic-bezier(0.16,1,0.3,1)`, 0.08s stagger.
> Eyebrow `01 — TREASURY`, 11px mono, `tracking-[0.24em]`, `text-white/50`.
> Copy: "Move money like it's 2030." / "Settlement in 400ms across 47 currencies.
> No correspondent banks, no cut-off times."
> CTA: "Start free" (accent pill) + "Talk to sales" (ghost).
> Below 768px: grid → 1 col, visual drops to `aspect-[4/3]`, H1 min falls to 40px.

Note how every number is decided. That is the whole method.
