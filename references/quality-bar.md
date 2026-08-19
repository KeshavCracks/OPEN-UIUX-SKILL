# Quality Bar — The Anti-Generic Review

Run this **before** declaring any UI work finished. It is written as a diagnostic: each
item names a failure mode, why it reads as cheap, and the fix.

---

## Part 1 — The instant-tell audit

These are the specific things that make a page identifiable as AI-generated within one
second. If your output has any of them, fix it before anything else.

| # | Tell | Why it reads cheap | Fix |
|---|---|---|---|
| 1 | Purple→blue or purple→pink diagonal gradient | The single most overused AI default | Neutral ground + one restrained accent. Vertical gradients between near-hues. |
| 2 | Everything centered | No art direction; the layout of last resort | Anchor elements to corners, use asymmetric grids, let content bleed off-edge |
| 3 | Three identical cards in a row | Zero hierarchy — nothing is more important | Bento with one dominant cell, or vary card size/content type |
| 4 | Headline at `text-4xl`/`text-5xl` | Timid; display type should be *loud* | `clamp(40px, 6.5vw, 105px)` with `leading-[0.95] tracking-[-0.03em]` |
| 5 | Default tracking on display type | Big type at default tracking looks unset | `-0.02em` to `-0.05em` |
| 6 | Default line-height on headlines | Lines float apart, no block presence | `leading-[0.95]` … `leading-[1.05]` |
| 7 | "Lorem ipsum" / "Feature One" / "Your Company" | Instantly unreal | Write plausible, specific product copy with real names and numbers |
| 8 | Emoji as icons | Inconsistent, unprofessional at any size | `lucide-react`, uniform `strokeWidth` |
| 9 | `transition: all 0.3s` | Animates unintended properties, drops frames | Name the properties; use `--ease-out` |
| 10 | No hover states | Feels dead and unfinished | Every interactive element gets hover + focus-visible |
| 11 | Text directly on an image with no scrim | Illegible at some viewport, always | Gradient or flat scrim under all overlaid text |
| 12 | Uniform section padding everywhere | Flat rhythm, nothing breathes | Alternate dense and airy sections |
| 13 | 5+ colors in the palette | Reads as a bug tracker, not a brand | Neutrals + exactly one accent |
| 14 | Pure `#000` background and `#fff` text | Flat and glaring; shadows impossible | `#0a0a0a` ground, `#f5f5f5` ink |
| 15 | Hard grey `box-shadow` on cards | Bootstrap-era default | Alpha layering, hairline borders, or a glow |
| 16 | Icon in a colored circle above centered text ×3 | The definitive template feature grid | Left-aligned icon, real hierarchy, varied cell weight |
| 17 | Buttons with cramped padding | Cheap, hard to hit | `px-6 py-3` minimum, `rounded-full` |
| 18 | Every element animating on scroll | Exhausting; nothing stands out | Animate section-level groups, `once: true` |

---

## Part 2 — Structured self-review

Work through each block. Be honest — the point is to find problems, not to pass.

### Direction
- [ ] Can I state the visual direction in 3–6 concrete words? (Not "modern and clean.")
- [ ] Is there exactly **one** signature move, and is it actually memorable?
- [ ] Would this design be plausible for *this specific brand* and no other? If the copy
      could be swapped for any other company, the design is generic.

### Typography
- [ ] Display type uses `clamp()` and fills its container at 1440px
- [ ] Tracking tightened on display, widened on small uppercase labels
- [ ] Leading `0.9–1.05` on display, `1.5–1.6` on body
- [ ] At most 2 families (+1 mono), each with a distinct job
- [ ] Body text max-width ≈ `65ch`
- [ ] Type scale has real jumps — no two levels within 15% of each other
- [ ] `-webkit-font-smoothing: antialiased` set on dark themes

### Color & surface
- [ ] Neutral ground; one accent appearing ≤2× per viewport
- [ ] Not pure black / pure white
- [ ] Borders as alpha (`white/10`), not solid greys
- [ ] Depth from layering/blur/glow rather than hard drop shadows
- [ ] Body text ≥ 4.5:1 contrast; large text ≥ 3:1 — **check the muted greys**, this is
      where it usually fails (`text-white/40` on `#0a0a0a` fails)

### Layout
- [ ] Hero is full viewport (`100dvh`) with one dominant focal element
- [ ] Something is asymmetric or deliberately off-grid
- [ ] Section density and background alternate
- [ ] One focal point per section
- [ ] Whitespace is generous — if unsure, add more
- [ ] Consistent spacing scale, no arbitrary one-off values

### Motion
- [ ] Easing is `cubic-bezier(0.16,1,0.3,1)` or a listed alternative — never `ease`/`linear`
- [ ] Hover 150–250ms; reveals 600–800ms
- [ ] Scroll reveals use `once: true` and `margin: "-100px"`
- [ ] Staggers total under ~1.2s
- [ ] Only `transform` and `opacity` animate
- [ ] Every RAF loop and event listener is cleaned up
- [ ] `prefers-reduced-motion` is honored and the page is fully usable without motion

### Content
- [ ] All copy is real, specific, and plausible — no placeholders
- [ ] Headlines say something; no "Welcome to our website"
- [ ] Numbers are believable and consistent across the page
- [ ] Every image has meaningful `alt` (or `alt=""` if purely decorative)
- [ ] Exactly one primary CTA per viewport, with a specific verb

### Responsive
- [ ] Checked at 320 / 768 / 1024 / 1440
- [ ] No horizontal overflow at any width
- [ ] `100dvh` not `100vh` for full-screen sections
- [ ] Hover-dependent content reachable on touch
- [ ] Horizontal-scroll and pinned sections have mobile fallbacks
- [ ] Touch targets ≥ 44×44px

### Accessibility
- [ ] Visible `:focus-visible` ring on every interactive element
- [ ] Logical heading order, one `<h1>`
- [ ] Semantic landmarks: `header`/`nav`/`main`/`footer`
- [ ] Keyboard-operable: menus, accordions, carousels, modals
- [ ] Decorative layers are `aria-hidden` + `pointer-events-none`
- [ ] Split-text animations expose the full string to screen readers

### Engineering
- [ ] No console errors or React key warnings
- [ ] Images sized with explicit aspect ratios; below-fold images lazy
- [ ] Fonts preconnected with `display=swap`
- [ ] No layout shift on load (reserve space for media)
- [ ] Video has `poster`, `muted`, `playsInline`

---

## Part 3 — The three questions

If the checklist passes but the work still feels flat, ask these:

1. **What is the one thing someone will remember?** If you cannot answer in a short
   phrase, the design has no center. Add or amplify a signature move.

2. **What would I remove?** Premium design is subtractive. Find the weakest element and
   delete it, then check whether the page got better. It usually does.

3. **Where is the tension?** Good design has contrast: huge type against tiny labels,
   dense blocks against empty fields, sharp cards against pill buttons. A page where
   everything is medium-sized and evenly spaced has no tension and will read as bland
   no matter how correct it is.

---

## Part 4 — When the brief is vague

Do not respond to "make me a landing page" with clarifying questions. Make three
decisions, state them in one line, and build:

1. **Industry stance** — fintech reads dark/precise/mono-labelled; wellness reads
   warm/serif/airy; agency reads bold/oversized/monochrome; DTC reads
   photographic/editorial.
2. **Ground** — dark or light. Dark is more forgiving and reads premium faster.
3. **Signature move** — one from `effects-cookbook.md`.

Then say: *"I went with a dark, precise fintech direction — Instrument Serif display
against Inter, one amber accent, and a cursor-spotlight hero. Happy to change any of it."*

A committed, opinionated result the user can react to is far more useful than a
questionnaire.
