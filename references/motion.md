# Motion — Choreography, Not Decoration

86.5% of website prompts in the corpus contain animation instructions. But the motion is
strikingly conservative: fades, scales, slides, staggers. Almost no particles, almost no
3D. **The premium signal is timing and restraint, not novelty.**

Guiding principle from the corpus analysis: motion exists to *guide* attention, never to
*compete* for it. If a user notices the animation before the content, it is wrong.

---

## 1. Easing — use these exact curves

The corpus is dominated by two curves. Memorize them.

| Curve | Hits | Name | Use for |
|---|---|---|---|
| `cubic-bezier(0.16, 1, 0.3, 1)` | **85** | expo-out | The house default. Entrances, reveals, scroll-ins. Fast start, long graceful settle. |
| `cubic-bezier(0.22, 1, 0.36, 1)` | **60** | quint-out | Slightly softer expo-out. Interchangeable. |
| `cubic-bezier(0.4, 0, 0.2, 1)` | 22 | standard | Material-style. Small UI state changes, hovers. |
| `cubic-bezier(0.23, 1, 0.32, 1)` | 22 | quart-out | Long, luxurious slides. |
| `cubic-bezier(0.34, 1.56, 0.64, 1)` | 8 | back-out | Overshoot. Playful pops — badges, toggles. Use rarely. |
| `cubic-bezier(0.76, 0, 0.24, 1)` | 5 | in-out-quart | Symmetric moves: modals, page transitions, accordions. |

```css
:root {
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-alt: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-std:     cubic-bezier(0.4, 0, 0.2, 1);
  --ease-inout:   cubic-bezier(0.76, 0, 0.24, 1);
}
```

**Never use `ease`, `linear` (except marquees/rotation), or `ease-in` for entrances.**
`ease-in` on an entrance makes the element feel like it is falling in reverse.
`ease-out` (115 hits) is the correct default for anything appearing.

### Framer Motion spring alternative

`spring` appears 57 times, with `stiffness` (32) and `damping` (37):

```js
transition={{ type: "spring", stiffness: 100, damping: 20, mass: 1 }}   // settled, premium
transition={{ type: "spring", stiffness: 400, damping: 30 }}            // snappy UI feedback
```

Springs for anything the user directly manipulates (drag, hover-follow, cursor).
Bezier curves for anything triggered by scroll or time.

---

## 2. Duration

Corpus frequencies: `300ms` (86) · `200ms` (65) · `500ms` (60) · `0.6s` (56) · `0.8s` (56) · `700ms` (23).

| Interaction | Duration |
|---|---|
| Hover / focus / small state | **150–250ms** |
| Button press, toggle | 200ms |
| Card lift, image zoom | 300–400ms |
| Scroll-reveal entrance | **600–800ms** |
| Large hero / mask reveal | 800–1200ms |
| Page transition | 600–900ms |
| Marquee full loop | 20–40s, `linear`, infinite |

Two failure modes, both common in AI output:
- **Too fast** (<150ms) — the change is perceived as a glitch, not a transition.
- **Too slow** (>1200ms for a small element) — feels laggy and blocks interaction.

**Never `transition: all`.** Transition specific properties. `transition: all` animates
layout properties you did not intend and destroys frame rate:

```css
transition: transform 300ms var(--ease-out), opacity 300ms var(--ease-out);
```

---

## 3. The scroll-reveal pattern (75 prompts)

The workhorse. Content fades and rises as it enters the viewport, once.

**Framer Motion — the exact corpus idiom:**

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
>
```

Those exact literals — `initial={{ opacity: 0, y: 20 }}`, `whileInView={{ opacity: 1, y: 0 }}`,
`viewport={{ once: true, margin: "-100px" }}` — are repeated verbatim across the corpus.

Key details:
- **`once: true`** always. Re-animating on every scroll-past is nauseating.
- **`margin: "-100px"`** fires slightly *before* the element is fully visible, so it has
  finished by the time the user reads it. Without this the animation feels late.
- **`y: 20`, not `y: 100`.** Subtle. Large travel distances look cheap.
- Never animate `opacity` from 0 on above-the-fold content that matters for LCP.

**Vanilla `IntersectionObserver`** (39 prompts) when React is not in play:

```js
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { rootMargin: '-100px 0px', threshold: 0.1 });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
```
```css
[data-reveal]      { opacity:0; transform:translateY(20px);
                     transition: opacity .8s var(--ease-out), transform .8s var(--ease-out); }
[data-reveal].in   { opacity:1; transform:none; }
```

---

## 4. Stagger (426 hits)

Stagger is what turns a group of elements into a *sequence*. It is the highest
value-per-line motion technique in the corpus.

```jsx
// Parent orchestrates, children inherit
const container = { hidden:{}, visible:{ transition:{ staggerChildren: 0.08, delayChildren: 0.1 } } };
const item = {
  hidden:  { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition:{ duration: 0.8, ease:[0.16,1,0.3,1] } },
};

<motion.ul variants={container} initial="hidden" whileInView="visible" viewport={{ once:true, margin:"-100px" }}>
  {items.map(i => <motion.li key={i.id} variants={item}>…</motion.li>)}
</motion.ul>
```

Stagger intervals:

| Count | Interval |
|---|---|
| 2–4 large blocks | `0.12–0.15s` |
| 5–8 cards | `0.08s` |
| Word-level in a headline | `0.04–0.06s` |
| Character-level | `0.02–0.03s` |

Total sequence should finish inside **~1.2s**. Twelve cards at 0.15s = 1.8s of waiting;
drop to 0.05s or reveal the grid as one unit.

---

## 5. Text reveal techniques

**Line/word mask reveal** — the most premium text entrance. Wrap each line in an
`overflow-hidden` container and slide the inner element up from below:

```jsx
<span className="block overflow-hidden">
  <motion.span
    className="block"
    initial={{ y: "110%" }}
    whileInView={{ y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1], delay: i * 0.08 }}
  >{line}</motion.span>
</span>
```

`110%` rather than `100%` guarantees descenders clear the mask.

**Per-character stagger** (`SplitText`, 14 hits) — for short headlines only. Always mark
the container with the real text for screen readers and `aria-hidden` the split spans.

**Typewriter** (12 prompts) — 50ms/char is the corpus value. Only for terminal/AI-chat
motifs; it delays comprehension, so never on a primary headline.

---

## 6. Hover (1,290 hits — the most frequent token in the entire corpus)

Every interactive element needs a hover state. Missing hover states are the clearest
"unfinished" signal.

```css
.card {
  transition: transform 300ms var(--ease-out), border-color 300ms var(--ease-out);
}
.card:hover { transform: translateY(-4px); border-color: var(--line-strong); }
```

Corpus-favoured hover moves:
- **Lift** — `translateY(-4px)` on cards. Subtle. Never `-20px`.
- **Image zoom in a fixed frame** — parent `overflow-hidden`, child `scale(1.05)` over
  500–700ms. The frame stays put; only the image grows.
- **Border brighten** — `border-white/10` → `border-white/20`.
- **Underline wipe** — a pseudo-element scaling `scaleX(0)` → `1` with
  `transform-origin: left`.
- **Arrow nudge** — icon `translateX(4px)` on link hover.
- **Text swap** — two stacked copies, one slides out as the other slides in.

Rules:
- Hover on the **container**, not the child — use `group`/`group-hover:` in Tailwind.
- Always pair with `focus-visible` — the corpus under-does this (2 hits) and it is a
  genuine gap you should close.
- Never rely on hover alone to reveal essential information; touch devices have none.

---

## 7. Scroll choreography

**Pinned sections** (37 prompts) — `position: sticky; top: 0` on a child of a tall
parent. The pure-CSS version handles most cases without GSAP:

```html
<section class="h-[300vh] relative">
  <div class="sticky top-0 h-screen flex items-center overflow-hidden"><!-- content --></div>
</section>
```

**Horizontal scroll** (14 prompts) — translate a track by scroll progress:

```jsx
const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end end"] });
const x = useTransform(scrollYProgress, [0, 1], ["0%", "-66%"]);
// <motion.div style={{ x }} className="flex gap-8">
```
Always provide a vertical fallback under `md`.

**Parallax** (33 prompts) — different layers move at different rates. Keep it subtle;
`10–25%` of scroll distance. Anything more induces motion sickness.

```jsx
const y = useTransform(scrollYProgress, [0, 1], ["0%", "20%"]);
```

**Smooth scroll / Lenis** — nice, but it hijacks native scrolling. Only add it when the
design depends on scroll-linked animation feeling continuous, and always disable under
`prefers-reduced-motion`.

**Marquee** (30 prompts) — duplicate the content twice and translate `-50%`:

```css
.marquee-track { display:flex; width:max-content; animation: scroll 30s linear infinite; }
@keyframes scroll { to { transform: translateX(-50%); } }
.marquee:hover .marquee-track { animation-play-state: paused; }
```
Fade the edges with a mask so items don't pop at the boundary:
```css
mask-image: linear-gradient(90deg, transparent, #000 10%, #000 90%, transparent);
```

---

## 8. Performance

- **Only animate `transform` and `opacity`.** Animating `width`, `height`, `top`, `left`,
  `margin`, or `box-shadow` triggers layout/paint per frame and drops frames.
- `will-change: transform` (49 hits) on elements that *will* animate — then remove it.
  Leaving it on everything wastes GPU memory.
- Always clean up: `removeEventListener` (28), `cancelAnimationFrame` (16). Every
  `requestAnimationFrame` loop (97 hits) needs a teardown in the effect's return.
- Throttle scroll/mouse work through `requestAnimationFrame`, never run it raw.
- Use `{ passive: true }` (25 hits) on scroll/touch listeners.
- Lerp for cursor-following smoothness (71 hits): `current += (target - current) * 0.1`.

```jsx
useEffect(() => {
  let raf;
  const loop = () => { /* ... */ raf = requestAnimationFrame(loop); };
  raf = requestAnimationFrame(loop);
  window.addEventListener('mousemove', onMove, { passive: true });
  return () => { cancelAnimationFrame(raf); window.removeEventListener('mousemove', onMove); };
}, []);
```

---

## 9. Reduced motion — non-negotiable

Only 19 corpus prompts mention `prefers-reduced-motion`. **This is the corpus's biggest
weakness — do not inherit it.** Always ship this:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```

In React, gate scroll-linked and looping effects:

```jsx
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
<motion.div
  initial={reduced ? false : { opacity: 0, y: 20 }}
  whileInView={reduced ? {} : { opacity: 1, y: 0 }}
/>
```

Content must remain fully readable and reachable with all motion disabled — never put
essential content behind an animation that never runs.
