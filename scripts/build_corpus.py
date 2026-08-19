#!/usr/bin/env python3
"""
build_corpus.py — Regenerate the OPEN-UIUX-SKILL data artifacts from the
upstream MotionSites prompt dump.

Upstream source (Unlicense / public domain):
    https://github.com/xianxian-sensen/motionsites-prompts

Usage
-----
    # 1. clone the upstream dump somewhere
    git clone --depth 1 https://github.com/xianxian-sensen/motionsites-prompts /tmp/msp

    # 2. regenerate everything
    python3 scripts/build_corpus.py --src /tmp/msp --out .

Outputs
-------
  assets/prompt-index.json     committed  — searchable metadata for all 328 prompts
  assets/prompt-catalog.md     committed  — human/agent scannable one-line catalog
  assets/corpus-stats.json     committed  — aggregate statistics used by the references
  examples/*.md                committed  — a small curated set of gold-standard prompts
  local/motionsites-all-prompts.md    LOCAL ONLY (gitignored) — every prompt, full text
  local/motionsites-all-prompts.json  LOCAL ONLY (gitignored) — every prompt, full text

`local/` is intentionally excluded from git: it is a 2.9 MB verbatim mirror of the
upstream corpus and belongs to the upstream project, not to this skill.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------
# Effect / capability taxonomy.
# Each tag maps to the substrings that signal it inside a prompt body.
# --------------------------------------------------------------------------
EFFECT_TAGS: dict[str, tuple[str, ...]] = {
    "cursor-spotlight": ("spotlight", "cursor-following", "follows the cursor", "radial reveal"),
    "custom-cursor": ("custom cursor", "cursor dot", "cursor blob", "cursor trail"),
    "magnetic": ("magnetic",),
    "marquee": ("marquee", "infinite ticker", "scrolling ticker"),
    "parallax": ("parallax",),
    "scroll-pin": ("position: sticky", "sticky top-0", "pin the", "scrolltrigger", "pinned"),
    "horizontal-scroll": ("horizontal scroll", "scrolls horizontally", "x-scroll"),
    "scroll-reveal": ("whileinview", "intersectionobserver", "useinview", "scroll-triggered", "reveal on scroll"),
    "text-split": ("splittext", "per-character", "character stagger", "split the heading", "letter by letter"),
    "text-scramble": ("scramble", "glitch text", "decode text"),
    "typewriter": ("typewriter", "typing effect", "types out"),
    "counter": ("count up", "counter animates", "odometer", "tabular-nums"),
    "clip-reveal": ("clip-path", "clippath", "mask-image", "-webkit-mask"),
    "image-mask": ("mask-composite", "circular mask", "soft circular"),
    "canvas": ("<canvas", "getcontext(", "requestanimationframe"),
    "webgl-shader": ("shader", "webgl", "fragment shader", "three.js"),
    "particles": ("particle", "starfield", "dot field"),
    "noise-grain": ("noise", "grain", "feturbulence"),
    "glassmorphism": ("backdrop-filter", "backdrop-blur", "glassmorphism", "liquid glass"),
    "blend-mode": ("mix-blend", "blend-mode"),
    "gradient-text": ("background-clip: text", "bg-clip-text"),
    "3d-transform": ("perspective(", "rotatex", "rotatey", "transform-style: preserve-3d", "tilt"),
    # NOTE: keep "morph" out of the plain substring table — it collides with
    # "glassmorphism"/"neumorphism". It is handled by EFFECT_REGEX below.
    "orbit": ("orbit",),
    "drag": ("draggable", "drag to", "pointerdown", "dragconstraints"),
    "carousel": ("carousel", "slider", "swiper", "embla"),
    "accordion": ("accordion", "collapsible"),
    "bento": ("bento",),
    "video-bg": ("<video", "background video", "autoplay loop muted"),
    "smooth-scroll": ("lenis", "smooth scroll", "locomotive"),
    "hover-reveal": ("hover reveal", "on hover the image", "hover state reveals"),
    "glow": ("glow", "box-shadow: 0 0", "drop-shadow"),
    "marquee-logos": ("logo cloud", "logo marquee", "trusted by"),
    "theme-dark": ("bg-black", "#000000", "#0a0a0a", "#111111", "dark-themed", "dark theme"),
}

LIB_TAGS: dict[str, tuple[str, ...]] = {
    "react": ("react",),
    "typescript": ("typescript", ".tsx", "typescript"),
    "vite": ("vite",),
    "next": ("next.js", "nextjs"),
    "tailwind": ("tailwind",),
    "framer-motion": ("framer-motion", "motion/react", "framer motion"),
    "gsap": ("gsap", "scrolltrigger"),
    "three": ("three.js", "@react-three", "webgl"),
    "lenis": ("lenis",),
    "lucide": ("lucide",),
    "swiper": ("swiper",),
    "d3": ("d3.", "d3 ", "recharts"),
    "vanilla-html": ("<!doctype html", "<!DOCTYPE html"),
}

SECTION_TAGS: dict[str, tuple[str, ...]] = {
    "hero": ("hero",),
    "navbar": ("navbar", "nav bar", "navigation"),
    "features": ("feature",),
    "pricing": ("pricing", "plan"),
    "testimonials": ("testimonial", "review"),
    "faq": ("faq", "frequently asked"),
    "cta": ("cta", "call to action", "call-to-action"),
    "footer": ("footer",),
    "stats": ("stats", "metrics", "kpi"),
    "gallery": ("gallery", "grid of images"),
    "form": ("form", "input field", "waitlist", "sign up", "signup"),
    "dashboard": ("dashboard",),
}

# Tags that need word-boundary precision (plain substrings would over-match,
# e.g. "morph" inside "glassmorphism").
EFFECT_REGEX: dict[str, str] = {
    "morph": r"\bmorph(s|ing|ed)?\b",
    "orbit": r"\borbit(s|ing|al)?\b",
    "tilt": r"\btilt(s|ing|ed)?\b",
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def detect(text_low: str, table: dict[str, tuple[str, ...]]) -> list[str]:
    found = {tag for tag, needles in table.items() if any(n in text_low for n in needles)}
    if table is EFFECT_TAGS:
        found |= {tag for tag, pat in EFFECT_REGEX.items() if re.search(pat, text_low)}
    return sorted(found)


# Lines that are code/markup rather than prose. Summaries must never quote these.
_CODEY = re.compile(
    r"""(^\s*[.#@&*/<}{|\[-])          # css selector, at-rule, html, list, table
      | ^\s*\w[\w-]*\s*[:{]\s          # `property: value` / `selector {`
      | [{};]\s*$                      # ends like code
      | ^\s*(const|let|var|import|export|function|return|class|div|span)\b
      | \b(px|rem|vw|vh|deg)\s*[;,)]   # unit soup
      | ^\s*\w+\s*=\s*["']             # attribute assignment
      | createElement | className | =>  # inline JS/JSX
    """,
    re.X | re.I,
)
_PROSE_START = re.compile(
    r"^(build|create|design|recreate|make|implement|generate|develop|produce|"
    r"a |an |the |this |dark|light|premium|luxury|modern|minimal|cinematic|full|"
    r"single|landing|hero)\b",
    re.I,
)


def first_sentence(text: str, limit: int = 200) -> str:
    """Pull an English one-line summary out of a prompt body.

    Strategy: scan the first ~80 lines, keep only prose-looking lines, and
    prefer one that opens like a build instruction ("Build a ...", "Create a ...").
    """
    body = text.strip()
    body = re.sub(r"^-{3,}\s*", "", body)
    body = re.sub(r"^\*{0,2}prompt(\s*to\s*recreate[^\n]*)?:?\*{0,2}\s*", "", body, flags=re.I)
    # drop fenced code blocks entirely
    body = re.sub(r"```.*?```", " ", body, flags=re.S)

    candidates: list[str] = []
    for raw in body.split("\n")[:80]:
        line = norm(raw)
        if not line or _CODEY.search(line):
            continue
        line = re.sub(r"[*`_#]+", "", line).strip()
        if len(line) < 30 or line.count(" ") < 4:
            continue
        # reject lines that are mostly punctuation/identifiers
        letters = sum(c.isalpha() or c.isspace() for c in line)
        if letters / len(line) < 0.75:
            continue
        candidates.append(line)
        if len(candidates) >= 12:
            break

    if not candidates:
        return norm(re.sub(r"[*`_#]+", "", body))[:limit]

    best = next((c for c in candidates if _PROSE_START.match(c)), candidates[0])
    m = re.search(r"^(.{40,}?[.!])(\s|$)", best + " ")
    out = m.group(1) if m else best
    return out[:limit].rstrip(" ,;:-") + ("…" if len(out) > limit else "")


def extract_fonts(text: str) -> list[str]:
    fonts: list[str] = []
    for fam in re.findall(r"family=([A-Za-z0-9+]+)", text):
        fonts.append(fam.replace("+", " "))
    for fam in re.findall(r"font-family:\s*['\"]([A-Za-z0-9 ]+)['\"]", text):
        fonts.append(fam.strip())
    seen, out = set(), []
    for f in fonts:
        key = f.lower()
        if key not in seen and len(f) > 2 and "symbols" not in key:
            seen.add(key)
            out.append(f)
    return out[:6]


def extract_palette(text: str, top: int = 6) -> list[str]:
    hexes = [h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", text)]
    return [h for h, _ in Counter(hexes).most_common(top)]


def build_records(raw: list[dict]) -> list[dict]:
    records = []
    for item in raw:
        body = item.get("prompt_text", "") or ""
        low = body.lower()
        records.append(
            {
                "id": item.get("id"),
                "title": norm(item.get("title", "")),
                "category": item.get("category"),
                "type": item.get("type"),
                "page_type": item.get("page_type"),
                "platform": item.get("platform"),
                "is_free": bool(item.get("is_free")),
                "chars": len(body),
                "summary": first_sentence(body),
                "stack": detect(low, LIB_TAGS),
                "effects": detect(low, EFFECT_TAGS),
                "sections": detect(low, SECTION_TAGS),
                "fonts": extract_fonts(body),
                "palette": extract_palette(body),
            }
        )
    return records


def build_stats(raw: list[dict], records: list[dict]) -> dict:
    corpus = "\n".join(x.get("prompt_text", "") for x in raw).lower()

    def hits(*needles: str) -> int:
        return sum(corpus.count(n.lower()) for n in needles)

    easings = Counter(
        re.sub(r"\s+", "", e)
        for e in re.findall(r"cubic-bezier\([^)]*\)", corpus)
    )
    hexes = Counter(h.lower() for h in re.findall(r"#[0-9a-f]{6}\b", corpus))
    fonts = Counter(f.replace("+", " ") for f in re.findall(r"family=([a-z0-9+]+)", corpus))

    effect_freq = Counter()
    stack_freq = Counter()
    for r in records:
        effect_freq.update(r["effects"])
        stack_freq.update(r["stack"])

    lengths = sorted(r["chars"] for r in records)
    return {
        "source": "https://github.com/xianxian-sensen/motionsites-prompts",
        "prompt_count": len(records),
        "platform": dict(Counter(r["platform"] for r in records)),
        "access": {"free": sum(1 for r in records if r["is_free"]),
                   "premium": sum(1 for r in records if not r["is_free"])},
        "type": dict(Counter(r["type"] for r in records).most_common()),
        "category_top": dict(Counter(r["category"] for r in records).most_common(20)),
        "length_chars": {
            "min": lengths[0],
            "p50": lengths[len(lengths) // 2],
            "p90": lengths[int(len(lengths) * 0.9)],
            "max": lengths[-1],
            "mean": round(sum(lengths) / len(lengths)),
        },
        "stack_prompt_coverage": dict(stack_freq.most_common()),
        "effect_prompt_coverage": dict(effect_freq.most_common()),
        "easing_curves_top": dict(easings.most_common(12)),
        "colors_top": dict(hexes.most_common(24)),
        "fonts_top": dict(fonts.most_common(24)),
        "raw_token_hits": {
            k: hits(*v)
            for k, v in {
                "hover": ("hover",),
                "blur": ("blur",),
                "stagger": ("stagger",),
                "mask": ("mask",),
                "reveal": ("reveal",),
                "clamp()": ("clamp(",),
                "rounded-full": ("rounded-full",),
                "tracking-tight": ("tracking-tight",),
                "backdrop-blur": ("backdrop-blur", "backdrop-filter"),
                "prefers-reduced-motion": ("prefers-reduced-motion",),
                "aria-*": ("aria-",),
                "pointer-events-none": ("pointer-events-none",),
                "overflow-hidden": ("overflow-hidden",),
                "requestAnimationFrame": ("requestanimationframe",),
                "IntersectionObserver": ("intersectionobserver",),
            }.items()
        },
    }


# Curated exemplars: diverse, self-contained, well-structured prompts that show
# the house style at its best. Selected by hand after reading the corpus.
EXEMPLAR_IDS = [
    "interactive-discovery",
]
EXEMPLAR_TARGETS = [
    # (slug, match-on-title substring, why it is worth shipping)
    ("cursor-spotlight-hero", "Interactive Discovery",
     "Layered cursor-following spotlight that masks a second image — the canonical MotionSites hero."),
]


def pick_exemplars(raw: list[dict], limit: int = 18) -> list[dict]:
    """Choose a diverse, high-signal subset: spread across type + effect coverage."""
    scored = []
    for item in raw:
        body = item.get("prompt_text", "") or ""
        low = body.lower()
        effects = detect(low, EFFECT_TAGS)
        structure = body.count("\n#") + body.count("\n**")
        # favour well-structured, medium-length, effect-rich prompts
        score = len(effects) * 3 + min(structure, 60) * 0.5
        if not (3000 <= len(body) <= 16000):
            score -= 25
        scored.append((score, item, effects))
    scored.sort(key=lambda t: -t[0])

    chosen: list[dict] = []
    seen_type: Counter = Counter()
    seen_effects: set[str] = set()
    for score, item, effects in scored:
        t = item.get("type") or "other"
        if seen_type[t] >= 4:
            continue
        fresh = set(effects) - seen_effects
        if chosen and not fresh and len(chosen) > 8:
            continue
        chosen.append(item)
        seen_type[t] += 1
        seen_effects |= set(effects)
        if len(chosen) >= limit:
            break
    return chosen


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:60]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="path to a clone of motionsites-prompts")
    ap.add_argument("--out", default=".", help="path to the skill repo root")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    raw = json.loads((src / "motionsites_all_prompts.json").read_text(encoding="utf-8"))

    records = build_records(raw)
    stats = build_stats(raw, records)

    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / "examples").mkdir(parents=True, exist_ok=True)
    (out / "local").mkdir(parents=True, exist_ok=True)

    # ---- committed: searchable index -------------------------------------
    (out / "assets" / "prompt-index.json").write_text(
        json.dumps(
            {
                "schema": "motionsites-prompt-index/1",
                "source": stats["source"],
                "license": "Unlicense (upstream); index derived by OPEN-UIUX-SKILL",
                "note": "Metadata + one-line summaries only. Full prompt bodies stay upstream.",
                "count": len(records),
                "prompts": records,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    # ---- committed: markdown catalog -------------------------------------
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_cat[r["category"] or "Uncategorised"].append(r)
    lines = [
        "# MotionSites Prompt Catalog",
        "",
        f"{len(records)} prompts, indexed by category. Metadata + summaries only — full bodies live",
        "upstream at <https://github.com/xianxian-sensen/motionsites-prompts>.",
        "",
        "Columns: **Title** — effects · stack",
        "",
    ]
    for cat in sorted(by_cat, key=lambda c: (-len(by_cat[c]), c)):
        lines.append(f"## {cat} ({len(by_cat[cat])})")
        lines.append("")
        for r in sorted(by_cat[cat], key=lambda x: x["title"]):
            fx = ", ".join(r["effects"][:6]) or "—"
            st = ", ".join(r["stack"][:5]) or "—"
            lines.append(f"- **{r['title']}** — {r['summary']}")
            lines.append(f"  - fx: `{fx}` · stack: `{st}`")
        lines.append("")
    (out / "assets" / "prompt-catalog.md").write_text("\n".join(lines), encoding="utf-8")

    # ---- committed: stats -------------------------------------------------
    (out / "assets" / "corpus-stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # ---- committed: curated exemplars ------------------------------------
    for f in (out / "examples").glob("*.md"):
        f.unlink()
    exemplars = pick_exemplars(raw)
    manifest = []
    for item in exemplars:
        slug = slugify(item.get("title") or item.get("id"))
        body = item["prompt_text"]
        low = body.lower()
        fx = detect(low, EFFECT_TAGS)
        st = detect(low, LIB_TAGS)
        header = (
            f"# {item['title']}\n\n"
            f"> Gold-standard reference prompt from the MotionSites corpus (Unlicense).\n"
            f"> Category `{item['category']}` · type `{item['type']}` · platform `{item['platform']}`\n"
            f"> Effects: `{', '.join(fx) or '—'}`\n"
            f"> Stack: `{', '.join(st) or '—'}`\n\n"
            f"Read this for **the level of specificity a build spec needs** — exact hex values,\n"
            f"exact Tailwind classes, exact easing and duration, exact copy.\n\n---\n\n"
        )
        (out / "examples" / f"{slug}.md").write_text(header + body.strip() + "\n", encoding="utf-8")
        manifest.append({"file": f"examples/{slug}.md", "title": item["title"],
                         "category": item["category"], "effects": fx})
    (out / "examples" / "INDEX.json").write_text(
        json.dumps({"count": len(manifest), "exemplars": manifest}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    # ---- LOCAL ONLY: full corpus -----------------------------------------
    (out / "local" / "motionsites-all-prompts.json").write_text(
        json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    md = [
        "# MotionSites — All Prompts (full text)",
        "",
        "**LOCAL WORKSPACE COPY — not committed to git.**",
        "",
        f"Source: {stats['source']} (Unlicense / public domain).",
        f"{len(raw)} prompts, {sum(len(x.get('prompt_text','')) for x in raw):,} characters.",
        "",
        "---",
        "",
        "## Table of contents",
        "",
    ]
    for i, item in enumerate(raw, 1):
        md.append(f"{i}. [{item['title']}](#{i}-{slugify(item['title'])}) — `{item['category']}`")
    md.append("")
    for i, item in enumerate(raw, 1):
        md += [
            "---",
            "",
            f"## {i}. {item['title']}",
            "",
            f"- **id:** `{item['id']}`",
            f"- **category:** {item['category']} · **type:** {item['type']} · "
            f"**platform:** {item['platform']} · **{'free' if item['is_free'] else 'premium'}**",
            f"- **zh description:** {item.get('description','')}",
            "",
            item["prompt_text"].strip(),
            "",
        ]
    (out / "local" / "motionsites-all-prompts.md").write_text("\n".join(md), encoding="utf-8")

    print(f"indexed   {len(records)} prompts")
    print(f"exemplars {len(manifest)} -> examples/")
    print(f"local     local/motionsites-all-prompts.{{json,md}} (gitignored)")


if __name__ == "__main__":
    main()
