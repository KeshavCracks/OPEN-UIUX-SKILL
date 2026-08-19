# Effects Cookbook

Working recipes for the signature effects that appear most in the corpus. Each is
distilled from real prompts. Pick **one** as the page's signature move — these are
expensive in attention, and stacking them produces noise.

Coverage counts are the number of the 328 prompts using each technique.

---

## 1. Cursor-following spotlight reveal · 11 prompts

The canonical MotionSites hero: a second image is revealed only inside a soft circle
that trails the cursor. Full reference: `examples/interactive-discovery.md`.

**How it works:** two stacked full-bleed images. The top one is masked by a radial
gradient rendered to an offscreen canvas, converted to a data URL, and applied as
`mask-image`. The cursor position is lerped for smooth trailing.

```jsx
function RevealLayer({ image, x, y, radius = 260 }) {
  const [mask, setMask] = useState("");
  useEffect(() => {
    const c = document.createElement("canvas");
    c.width = window.innerWidth; c.height = window.innerHeight;
    const ctx = c.getContext("2d");
    const g = ctx.createRadialGradient(x, y, 0, x, y, radius);
    // soft falloff — the hard-edge version looks cheap
    [[0,1],[0.4,1],[0.6,0.75],[0.75,0.4],[0.88,0.12],[1,0]]
      .forEach(([stop, a]) => g.addColorStop(stop, `rgba(255,255,255,${a})`));
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(x, y, radius, 0, Math.PI * 2); ctx.fill();
    setMask(c.toDataURL());
  }, [x, y, radius]);

  return (
    <div
      className="absolute inset-0 z-30 bg-cover bg-center pointer-events-none"
      style={{
        backgroundImage: `url(${image})`,
        maskImage: `url(${mask})`, WebkitMaskImage: `url(${mask})`,
        maskSize: "100% 100%", WebkitMaskSize: "100% 100%",
      }}
    />
  );
}
```

Smoothed cursor tracking (the lerp is what makes it feel expensive):

```jsx
const [pos, setPos] = useState({ x: 0, y: 0 });
useEffect(() => {
  const target = { x: innerWidth / 2, y: innerHeight / 2 };
  const smooth = { ...target };
  const onMove = (e) => { target.x = e.clientX; target.y = e.clientY; };
  let raf;
  const loop = () => {
    smooth.x += (target.x - smooth.x) * 0.1;   // 0.1 = trailing weight
    smooth.y += (target.y - smooth.y) * 0.1;
    setPos({ ...smooth });
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);
  window.addEventListener("mousemove", onMove, { passive: true });
  return () => { cancelAnimationFrame(raf); window.removeEventListener("mousemove", onMove); };
}, []);
```

Cheaper CSS-only variant for a glow (no second image):

```jsx
<div style={{ background:`radial-gradient(400px circle at ${x}px ${y}px, rgba(255,255,255,.08), transparent 70%)` }}
     className="absolute inset-0 pointer-events-none" />
```

Mobile: disable entirely and show the base image. There is no cursor.

---

## 2. Glassmorphism panel · 173 prompts

The most common surface treatment in the corpus.

```css
.glass {
  background-image: linear-gradient(rgba(255,255,255,0.35), rgba(255,255,255,0.12));
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);      /* always ship the prefix */
  border: 1px solid rgba(255,255,255,0.2);
  box-shadow: 0 8px 32px rgba(0,0,0,0.12),
              inset 0 1px 0 rgba(255,255,255,0.5);   /* the inset top-light is essential */
}
```

The `inset 0 1px 0` highlight is what sells the material — it simulates light catching
the top edge. Without it the panel just looks blurry.

Glass **only works over something busy** — an image, video, or gradient. Over a flat
background it is invisible. Blur radius 8–24px; beyond 40px it becomes fog.

---

## 3. Gradient-border card (mask-composite) · 63 prompts

The `-webkit-mask` + `mask-composite: xor` trick — 42 verbatim occurrences.

```css
.grad-border { position: relative; border-radius: 16px; }
.grad-border::before {
  content: ""; position: absolute; inset: 0; border-radius: inherit;
  padding: 1px;                                   /* = border width */
  background: linear-gradient(135deg, rgba(255,255,255,.4), rgba(255,255,255,0));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  pointer-events: none;
}
```

Gives a true gradient border that respects `border-radius`. Combine with a
cursor-tracked gradient angle for a spotlight-border card.

---

## 4. Text mask reveal · 87 clip-reveal prompts

Text slides up from behind an invisible edge. The most premium text entrance available.

```jsx
{lines.map((line, i) => (
  <span key={i} className="block overflow-hidden">
    <motion.span
      className="block"
      initial={{ y: "110%" }}
      whileInView={{ y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1], delay: i * 0.08 }}
    >{line}</motion.span>
  </span>
))}
```

`110%` (not `100%`) so descenders fully clear. The outer `overflow-hidden` must be
`block` — inline elements do not clip.

CSS-only version with `clip-path`:

```css
.reveal      { clip-path: inset(0 0 100% 0); transition: clip-path .9s var(--ease-out); }
.reveal.in   { clip-path: inset(0 0 0 0); }
```

---

## 5. Marquee / infinite ticker · 30 prompts

```jsx
<div className="relative overflow-hidden
                [mask-image:linear-gradient(90deg,transparent,#000_10%,#000_90%,transparent)]">
  <div className="flex w-max animate-[scroll_30s_linear_infinite] hover:[animation-play-state:paused]">
    {[...items, ...items].map((it, i) => (          // duplicate exactly once
      <span key={i} className="px-8 text-white/50 whitespace-nowrap">{it}</span>
    ))}
  </div>
</div>
```
```css
@keyframes scroll { to { transform: translateX(-50%); } }
```

Non-negotiables: duplicate the list **exactly once** and translate **exactly -50%** —
any other combination produces a visible jump. Always `linear`. Always fade the edges
with a mask. Pause on hover if the items are readable content.

---

## 6. Scroll-pinned section · 37 prompts

Pure CSS handles most cases:

```html
<section class="relative h-[300vh]">
  <div class="sticky top-0 h-screen flex items-center justify-center overflow-hidden">
    <!-- stays put while the parent's 300vh scrolls past -->
  </div>
</section>
```

Parent height controls duration: `300vh` ≈ two extra screens of scroll. Drive internal
state from progress:

```jsx
const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end end"] });
const scale   = useTransform(scrollYProgress, [0, 1], [1, 1.3]);
const opacity = useTransform(scrollYProgress, [0, 0.8, 1], [1, 1, 0]);
```

`position: sticky` silently fails if any ancestor has `overflow: hidden`. Use
`overflow-x: clip` instead when you need horizontal containment.

---

## 7. Horizontal scroll gallery · 14 prompts

```jsx
const ref = useRef(null);
const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end end"] });
const x = useTransform(scrollYProgress, [0, 1], ["0%", "-66%"]);   // tune to track width

<section ref={ref} className="relative h-[300vh] hidden md:block">
  <div className="sticky top-0 h-screen flex items-center overflow-hidden">
    <motion.div style={{ x }} className="flex gap-8 pl-[10vw]">
      {items.map(i => <Card key={i.id} className="w-[70vw] md:w-[38vw] shrink-0" />)}
    </motion.div>
  </div>
</section>
```

Always ship a mobile fallback — a vertical stack, or native snap scrolling:
```css
.snap { display:flex; overflow-x:auto; scroll-snap-type:x mandatory; }
.snap > * { scroll-snap-align:center; flex:0 0 85%; }
```

---

## 8. Video background · 203 prompts (most common effect)

```jsx
<section className="relative h-screen overflow-hidden" style={{ height: "100dvh" }}>
  <video
    className="absolute inset-0 z-10 h-full w-full object-cover"
    autoPlay loop muted playsInline preload="auto" poster="/poster.jpg"
  >
    <source src="/hero.mp4" type="video/mp4" />
  </video>
  {/* scrim — mandatory for legibility */}
  <div className="absolute inset-0 z-20 bg-gradient-to-t from-black/85 via-black/35 to-black/50" />
  <div className="relative z-50 flex h-full flex-col justify-center px-6">…</div>
</section>
```

`muted` and `playsInline` are both required or iOS refuses to autoplay. Always supply a
`poster` so the first paint is not black. Consider swapping to a still image under `md`
to save mobile bandwidth.

---

## 9. Count-up statistics · 9 prompts

```jsx
function CountUp({ to, duration = 1600, suffix = "" }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [n, setN] = useState(0);
  useEffect(() => {
    if (!inView) return;
    const t0 = performance.now();
    let raf;
    const tick = (t) => {
      const p = Math.min((t - t0) / duration, 1);
      setN(Math.round(to * (1 - Math.pow(1 - p, 3))));   // ease-out cubic
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [inView, to, duration]);
  return <span ref={ref} className="tabular-nums">{n.toLocaleString()}{suffix}</span>;
}
```

`tabular-nums` is essential — without it the number visibly jitters as digits change width.

---

## 10. Magnetic button · 5 prompts

```jsx
const ref = useRef(null);
const [d, setD] = useState({ x: 0, y: 0 });
const onMove = (e) => {
  const r = ref.current.getBoundingClientRect();
  setD({ x: (e.clientX - (r.left + r.width / 2)) * 0.25,
         y: (e.clientY - (r.top + r.height / 2)) * 0.25 });
};

<motion.button
  ref={ref} onMouseMove={onMove} onMouseLeave={() => setD({ x: 0, y: 0 })}
  animate={d} transition={{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }}
>Get started</motion.button>
```

Strength `0.2–0.35`. Higher feels unhinged. Desktop only.

---

## 11. Hover image-reveal list · editorial favourite

Menu rows that summon an image following the cursor.

```jsx
<li className="group relative border-b border-white/10 py-8">
  <h3 className="text-[clamp(28px,5vw,72px)] transition-colors duration-300
                 text-white/40 group-hover:text-white">Project name</h3>
  <img src={src} alt=""
       className="pointer-events-none absolute right-[10%] top-1/2 z-20 w-[260px]
                  -translate-y-1/2 scale-90 rounded-lg opacity-0
                  transition-[opacity,transform] duration-500
                  ease-[cubic-bezier(0.16,1,0.3,1)]
                  group-hover:scale-100 group-hover:opacity-100" />
</li>
```

Dim non-hovered siblings for extra focus: `has-[:hover]` on the parent plus
`opacity-40` on the list, `opacity-100` on the hovered row.

---

## 12. Noise / grain overlay · 26 prompts

```css
.grain::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  opacity: .035; z-index: 60;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

Opacity `0.02–0.05` only. It should be felt, not seen. Kills the flat "digital" quality
of large solid fields — one of the highest impact-to-effort ratios available.

---

## 13. Gradient text · 29 prompts

```css
.grad-text {
  background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

Vertical (`180deg`) light-to-dark reads far more premium than the diagonal
purple→pink gradient that marks AI-generated design. Keep the two stops close in hue.

---

## 14. Blend-mode overlays · 75 prompts

```css
mix-blend-mode: difference;   /* white text auto-inverts over any background */
mix-blend-mode: exclusion;    /* similar, softer */
mix-blend-mode: screen;       /* lighten — glows, light leaks */
mix-blend-mode: overlay;      /* contrast boost — textures */
```

`difference` on a fixed wordmark or custom cursor is a strong art-direction move: the
element stays legible over any background with zero conditional logic.

---

## 15. Scroll progress bar

```jsx
const { scrollYProgress } = useScroll();
<motion.div style={{ scaleX: scrollYProgress }}
  className="fixed inset-x-0 top-0 z-[100] h-[2px] origin-left bg-white" />
```

Cheap, useful on long pages, and reads as considered detail.
