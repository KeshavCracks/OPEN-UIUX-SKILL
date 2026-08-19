#!/usr/bin/env python3
"""
find_prompts.py — search the MotionSites prompt index shipped with this skill.

The index holds metadata + one-line summaries for all 328 prompts. Full prompt
bodies are NOT committed; see `--where` for how to fetch them locally.

Examples
--------
    # what's available, at a glance
    python3 scripts/find_prompts.py --stats

    # prompts using a specific technique (repeatable, AND-ed)
    python3 scripts/find_prompts.py --effect cursor-spotlight
    python3 scripts/find_prompts.py --effect scroll-pin --effect horizontal-scroll

    # free-text over title / category / summary
    python3 scripts/find_prompts.py --query "luxury ecommerce"

    # filter by stack, type, platform, access
    python3 scripts/find_prompts.py --stack gsap --type hero --free

    # dump full JSON records for programmatic use
    python3 scripts/find_prompts.py --effect marquee --json

    # list every tag you can filter on
    python3 scripts/find_prompts.py --list-effects
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "prompt-index.json"
STATS = ROOT / "assets" / "corpus-stats.json"
LOCAL_MD = ROOT / "local" / "motionsites-all-prompts.md"

FETCH_HINT = """\
Full prompt bodies are not committed to this repo (they belong upstream).
To materialise them locally into ./local/ (gitignored):

  git clone --depth 1 https://github.com/xianxian-sensen/motionsites-prompts /tmp/msp
  python3 scripts/build_corpus.py --src /tmp/msp --out .

18 curated full-text exemplars are always available in ./examples/.
"""


def load() -> list[dict]:
    if not INDEX.exists():
        sys.exit(f"index missing: {INDEX}\n\n{FETCH_HINT}")
    return json.loads(INDEX.read_text(encoding="utf-8"))["prompts"]


def show_stats() -> None:
    s = json.loads(STATS.read_text(encoding="utf-8"))
    print(f"MotionSites corpus — {s['prompt_count']} prompts")
    print(f"  source   {s['source']}")
    print(f"  platform {s['platform']}")
    print(f"  access   {s['access']}")
    L = s["length_chars"]
    print(f"  length   min {L['min']} · median {L['p50']} · mean {L['mean']} · max {L['max']} chars")

    def block(title: str, data: dict, n: int = 12) -> None:
        print(f"\n{title}")
        width = max((len(k) for k in list(data)[:n]), default=0)
        for k, v in list(data.items())[:n]:
            print(f"  {k:<{width}}  {v}")

    block("stack coverage (prompts)", s["stack_prompt_coverage"])
    block("effect coverage (prompts)", s["effect_prompt_coverage"], 18)
    block("easing curves (occurrences)", s["easing_curves_top"], 6)
    block("colors (occurrences)", s["colors_top"], 8)
    block("fonts (occurrences)", s["fonts_top"], 8)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Search the MotionSites prompt index.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=FETCH_HINT,
    )
    ap.add_argument("--query", "-q", help="substring match on title/category/summary")
    ap.add_argument("--effect", "-e", action="append", default=[], help="require this effect tag (repeatable)")
    ap.add_argument("--stack", "-s", action="append", default=[], help="require this stack tag (repeatable)")
    ap.add_argument("--section", action="append", default=[], help="require this section tag (repeatable)")
    ap.add_argument("--type", "-t", help="prompt type, e.g. hero, features, pricing")
    ap.add_argument("--platform", choices=["website", "app"])
    ap.add_argument("--free", action="store_true", help="only free prompts")
    ap.add_argument("--premium", action="store_true", help="only premium prompts")
    ap.add_argument("--min-chars", type=int, default=0)
    ap.add_argument("--limit", "-n", type=int, default=20)
    ap.add_argument("--json", action="store_true", help="emit full JSON records")
    ap.add_argument("--stats", action="store_true", help="print corpus statistics and exit")
    ap.add_argument("--list-effects", action="store_true", help="list all filterable tags and exit")
    ap.add_argument("--where", action="store_true", help="explain where full prompt text lives")
    args = ap.parse_args()

    if args.where:
        print(FETCH_HINT)
        print(f"local full corpus present: {LOCAL_MD.exists()}  ({LOCAL_MD})")
        return
    if args.stats:
        show_stats()
        return

    rows = load()

    if args.list_effects:
        for label, key in (("effects", "effects"), ("stack", "stack"), ("sections", "sections")):
            c = Counter(tag for r in rows for tag in r[key])
            print(f"\n{label}:")
            for tag, n in c.most_common():
                print(f"  {tag:<20} {n}")
        return

    out = rows
    if args.query:
        q = args.query.lower()
        out = [r for r in out if q in f"{r['title']} {r['category']} {r['summary']}".lower()]
    for e in args.effect:
        out = [r for r in out if e in r["effects"]]
    for s in args.stack:
        out = [r for r in out if s in r["stack"]]
    for s in args.section:
        out = [r for r in out if s in r["sections"]]
    if args.type:
        out = [r for r in out if (r["type"] or "").lower() == args.type.lower()]
    if args.platform:
        out = [r for r in out if r["platform"] == args.platform]
    if args.free:
        out = [r for r in out if r["is_free"]]
    if args.premium:
        out = [r for r in out if not r["is_free"]]
    if args.min_chars:
        out = [r for r in out if r["chars"] >= args.min_chars]

    # richest prompts first
    out.sort(key=lambda r: (-len(r["effects"]), -r["chars"]))
    total = len(out)
    out = out[: args.limit]

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    if not out:
        print("no matches. try --list-effects to see available tags.")
        return

    print(f"{total} match(es); showing {len(out)}\n")
    for r in out:
        tier = "free" if r["is_free"] else "premium"
        print(f"● {r['title']}  ({r['category']} · {r['type']} · {tier} · {r['chars']:,} chars)")
        print(f"    {r['summary']}")
        if r["effects"]:
            print(f"    fx    {', '.join(r['effects'])}")
        if r["stack"]:
            print(f"    stack {', '.join(r['stack'])}")
        if r["palette"]:
            print(f"    hues  {' '.join(r['palette'][:5])}")
        if r["fonts"]:
            print(f"    type  {', '.join(r['fonts'][:4])}")
        print()

    if total > len(out):
        print(f"… {total - len(out)} more (raise --limit)")


if __name__ == "__main__":
    main()
