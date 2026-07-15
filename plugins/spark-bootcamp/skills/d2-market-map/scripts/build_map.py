#!/usr/bin/env python3
"""Render 02-market/market-map.json into a one-page HTML market-map diagram.

The written market-map.md is the artefact of record. This script is the
convenience layer: it turns the same structured data into a board you can
eyeball and, later, put in front of a prospect. State and picture read from one
file so they never drift.

It uses the standard library only. It reads your brand colours from
.spark/brand/brand.json if that file exists, and falls back to Spark's dark
green and gold if it does not. It never crashes on a missing or malformed file:
it prints exactly what was wrong, and where it could, writes a usable page
anyway.

Usage:
  build_map.py --root . --data 02-market/market-map.json --out 02-market/market-map.html
  build_map.py --root . --init          # write a skeleton market-map.json to fill in

Expected shape of market-map.json:
  {
    "business": "Acme Trust Tools",
    "problem": "Trust administrators struggle to ... which costs them ...",
    "target_segment": "Trust administrators at small Jersey trust companies",
    "segments":    [{"name": "...", "note": "..."}, ...],           # 3 or more
    "value_chain": ["...", "...", "...", "..."],                    # 4 or more
    "incumbents":  [{"name":"...","bucket":"direct","note":"...","source":"..."}, ...],  # 6 or more
    "substitutes": ["...", "...", "..."],                           # 3 or more
    "gap": "One paragraph naming where the map is thin."
  }
Bucket is one of: direct, adjacent, diy.
"""

import argparse
import html
import json
import os
import sys

SPARK_PRIMARY = "#0B3D2E"   # dark green
SPARK_ACCENT = "#C9A227"    # gold
SPARK_INK = "#12211B"
SPARK_PAPER = "#FBFAF6"

BUCKET_LABELS = {
    "direct": "Direct",
    "adjacent": "Adjacent",
    "diy": "DIY / generic",
    "generic": "DIY / generic",
}

SKELETON = {
    "business": "",
    "problem": "Paste the one-sentence problem from validated-problem.md",
    "target_segment": "",
    "segments": [
        {"name": "", "note": ""},
        {"name": "", "note": ""},
        {"name": "", "note": ""},
    ],
    "value_chain": ["", "", "", ""],
    "incumbents": [
        {"name": "", "bucket": "direct", "note": "", "source": ""},
        {"name": "", "bucket": "direct", "note": "", "source": ""},
        {"name": "", "bucket": "adjacent", "note": "", "source": ""},
        {"name": "", "bucket": "adjacent", "note": "", "source": ""},
        {"name": "", "bucket": "diy", "note": "", "source": ""},
        {"name": "", "bucket": "diy", "note": "", "source": ""},
    ],
    "substitutes": ["", "", ""],
    "gap": "",
}


def load_brand(root):
    """Return (primary, accent) from brand.json, or Spark defaults."""
    path = os.path.join(root, ".spark", "brand", "brand.json")
    primary, accent = SPARK_PRIMARY, SPARK_ACCENT
    try:
        with open(path, "r", encoding="utf-8") as fh:
            brand = json.load(fh)
        colours = brand.get("colours") or brand.get("colors") or brand
        primary = colours.get("primary", primary) or primary
        accent = (
            colours.get("secondary")
            or colours.get("accent")
            or accent
        ) or accent
        print("Brand colours loaded from .spark/brand/brand.json.")
    except FileNotFoundError:
        print("No brand.json yet: using Spark's dark green and gold.")
    except (json.JSONDecodeError, AttributeError, TypeError):
        print("brand.json could not be read: using Spark defaults instead.")
    return primary, accent


def esc(value):
    return html.escape(str(value if value is not None else ""))


def render(data, primary, accent):
    business = esc(data.get("business") or "Market map")
    problem = esc(data.get("problem") or "(problem sentence not set)")
    target = esc(data.get("target_segment") or "")

    segments = data.get("segments") or []
    value_chain = data.get("value_chain") or []
    incumbents = data.get("incumbents") or []
    substitutes = data.get("substitutes") or []
    gap = esc(data.get("gap") or "(gap paragraph not written yet)")

    seg_cards = "\n".join(
        '<div class="card"><h3>{name}</h3><p>{note}</p></div>'.format(
            name=esc(s.get("name") if isinstance(s, dict) else s),
            note=esc(s.get("note") if isinstance(s, dict) else ""),
        )
        for s in segments
    ) or '<p class="empty">No segments yet. Aim for 3 or more.</p>'

    chain_steps = []
    for i, stage in enumerate(value_chain):
        arrow = '<span class="arrow">&rarr;</span>' if i > 0 else ""
        chain_steps.append(
            '{arrow}<div class="stage"><span class="num">{n}</span>{label}</div>'.format(
                arrow=arrow, n=i + 1, label=esc(stage)
            )
        )
    chain = "".join(chain_steps) or '<p class="empty">No value chain yet. Aim for 4 or more stages.</p>'

    rows = "\n".join(
        "<tr><td>{name}</td><td><span class=\"pill {cls}\">{bucket}</span></td>"
        "<td>{note}</td><td class=\"src\">{source}</td></tr>".format(
            name=esc(inc.get("name")),
            cls=esc((inc.get("bucket") or "").lower()),
            bucket=esc(BUCKET_LABELS.get((inc.get("bucket") or "").lower(), inc.get("bucket") or "?")),
            note=esc(inc.get("note")),
            source=esc(inc.get("source")) or '<em class="warn">no source</em>',
        )
        for inc in incumbents
    ) or '<tr><td colspan="4" class="empty">No incumbents yet. Aim for 6 or more, each sourced.</td></tr>'

    subs = "\n".join(
        '<li>{s}</li>'.format(s=esc(sub)) for sub in substitutes
    ) or '<li class="empty">No substitutes yet. Aim for 3 or more.</li>'

    counts = "{seg} segments &middot; {stage} stages &middot; {inc} incumbents &middot; {sub} substitutes".format(
        seg=len(segments), stage=len(value_chain), inc=len(incumbents), sub=len(substitutes)
    )

    return TEMPLATE.format(
        business=business,
        problem=problem,
        target=("Target segment: " + target) if target else "",
        counts=counts,
        seg_cards=seg_cards,
        chain=chain,
        rows=rows,
        subs=subs,
        gap=gap,
        primary=primary,
        accent=accent,
        ink=SPARK_INK,
        paper=SPARK_PAPER,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{business}</title>
<style>
  :root {{ --primary: {primary}; --accent: {accent}; --ink: {ink}; --paper: {paper}; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color: var(--ink); background: var(--paper); margin: 0; padding: 2rem; line-height: 1.5; }}
  header {{ border-bottom: 4px solid var(--accent); padding-bottom: 1rem; margin-bottom: 1.5rem; }}
  h1 {{ color: var(--primary); margin: 0 0 .4rem; font-size: 1.6rem; }}
  .problem {{ font-size: 1.1rem; font-style: italic; color: var(--primary); margin: .3rem 0; }}
  .meta {{ color: #555; font-size: .85rem; }}
  section {{ margin: 1.8rem 0; }}
  h2 {{ color: var(--primary); font-size: 1.15rem; border-left: 5px solid var(--accent);
        padding-left: .6rem; margin-bottom: .8rem; }}
  .cards {{ display: flex; flex-wrap: wrap; gap: .8rem; }}
  .card {{ flex: 1 1 220px; border: 1px solid #ddd; border-top: 3px solid var(--primary);
           border-radius: 6px; padding: .8rem; background: #fff; }}
  .card h3 {{ margin: 0 0 .3rem; font-size: 1rem; color: var(--primary); }}
  .card p {{ margin: 0; font-size: .9rem; color: #444; }}
  .chain {{ display: flex; flex-wrap: wrap; align-items: center; gap: .3rem; }}
  .stage {{ background: var(--primary); color: #fff; padding: .6rem .8rem; border-radius: 6px;
            font-size: .9rem; display: flex; align-items: center; gap: .4rem; }}
  .stage .num {{ background: var(--accent); color: var(--ink); border-radius: 50%;
                 width: 1.4rem; height: 1.4rem; display: inline-flex; align-items: center;
                 justify-content: center; font-weight: 700; font-size: .8rem; }}
  .arrow {{ color: var(--accent); font-size: 1.4rem; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; }}
  th, td {{ text-align: left; padding: .55rem .6rem; border-bottom: 1px solid #e5e5e5; font-size: .9rem; }}
  th {{ background: var(--primary); color: #fff; }}
  .pill {{ font-size: .75rem; padding: .15rem .5rem; border-radius: 999px; color: #fff; white-space: nowrap; }}
  .pill.direct {{ background: #b23a2e; }}
  .pill.adjacent {{ background: #b8860b; }}
  .pill.diy, .pill.generic {{ background: #4a6b5b; }}
  .src {{ font-size: .8rem; color: #555; }}
  .warn {{ color: #b23a2e; }}
  ul {{ margin: 0; padding-left: 1.2rem; }}
  li {{ margin: .2rem 0; }}
  .gap {{ background: #fff; border: 1px solid var(--accent); border-left: 5px solid var(--accent);
          padding: 1rem; border-radius: 6px; }}
  .empty {{ color: #999; font-style: italic; }}
  footer {{ margin-top: 2rem; font-size: .75rem; color: #888; border-top: 1px solid #ddd; padding-top: .8rem; }}
</style>
</head>
<body>
<header>
  <h1>{business}</h1>
  <p class="problem">&ldquo;{problem}&rdquo;</p>
  <p class="meta">{target}</p>
  <p class="meta">{counts}</p>
</header>

<section>
  <h2>Segments</h2>
  <div class="cards">{seg_cards}</div>
</section>

<section>
  <h2>Value chain</h2>
  <div class="chain">{chain}</div>
</section>

<section>
  <h2>Incumbents</h2>
  <table>
    <thead><tr><th>Name</th><th>Bucket</th><th>What they do</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</section>

<section>
  <h2>Substitutes</h2>
  <ul>{subs}</ul>
</section>

<section>
  <h2>The gap</h2>
  <div class="gap">{gap}</div>
</section>

<footer>Spark AI Agency &middot; Day 2 market map. Every incumbent carries a source.
Market figures are sourced or flagged as assumptions.</footer>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build the Day 2 market-map HTML diagram.")
    parser.add_argument("--root", default=".", help="Project root (holds .spark/).")
    parser.add_argument("--data", default="02-market/market-map.json", help="Input JSON data file.")
    parser.add_argument("--out", default="02-market/market-map.html", help="Output HTML file.")
    parser.add_argument("--init", action="store_true", help="Write a skeleton market-map.json and exit.")
    args = parser.parse_args()

    data_path = os.path.join(args.root, args.data)

    if args.init:
        os.makedirs(os.path.dirname(data_path) or ".", exist_ok=True)
        if os.path.exists(data_path):
            print("Refusing to overwrite existing {p}. Delete it first if you want a fresh skeleton.".format(p=data_path))
            return 0
        with open(data_path, "w", encoding="utf-8") as fh:
            json.dump(SKELETON, fh, indent=2)
            fh.write("\n")
        print("Wrote skeleton {p}. Fill it in, then run this script again without --init.".format(p=data_path))
        return 0

    try:
        with open(data_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        print("No data file at {p}.".format(p=data_path))
        print("Run: build_map.py --root {r} --init  to create a skeleton to fill in.".format(r=args.root))
        return 1
    except json.JSONDecodeError as exc:
        print("Could not parse {p}: {e}".format(p=data_path, e=exc))
        print("The written market-map.md is still your artefact of record. Fix the JSON and re-run.")
        return 1

    primary, accent = load_brand(args.root)
    page = render(data, primary, accent)

    out_path = os.path.join(args.root, args.out)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)

    seg = len(data.get("segments") or [])
    stage = len(data.get("value_chain") or [])
    inc = len(data.get("incumbents") or [])
    sub = len(data.get("substitutes") or [])
    print("Wrote {p}.".format(p=out_path))
    print("Counts: {s} segments, {v} value-chain stages, {i} incumbents, {u} substitutes.".format(
        s=seg, v=stage, i=inc, u=sub))

    short = []
    if seg < 3:
        short.append("segments (need 3+)")
    if stage < 4:
        short.append("value-chain stages (need 4+)")
    if inc < 6:
        short.append("incumbents (need 6+)")
    if sub < 3:
        short.append("substitutes (need 3+)")
    unsourced = [i.get("name") or "?" for i in (data.get("incumbents") or []) if not (i.get("source"))]
    if short:
        print("Still short on: " + ", ".join(short) + ". The map is not done until these are met.")
    if unsourced:
        print("Unsourced incumbents (fix before you call this done): " + ", ".join(esc(n) for n in unsourced))
    if not short and not unsourced:
        print("All counts met and every incumbent is sourced. Map is done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
