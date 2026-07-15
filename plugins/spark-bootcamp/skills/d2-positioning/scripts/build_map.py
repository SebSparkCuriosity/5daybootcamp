#!/usr/bin/env python3
"""Render 02-market/positioning.json into a one-page 2x2 positioning map, and
check it against the done-condition.

The written positioning.md is the artefact of record. This script is the
convenience layer: it turns the same structured data into a 2x2 board you can
eyeball and, later, put in front of a prospect. Statement, USP and picture read
from one file so they never drift.

It uses the standard library only, so it never needs an install and never
crashes on a missing dependency. It reads your brand colours from
.spark/brand/brand.json if that file exists, and falls back to Spark's dark
green and gold if it does not. A missing or malformed file is reported plainly,
never a stack trace.

Three modes:
  build_map.py --init
      Write a skeleton positioning.json to fill in, then stop.
  build_map.py --data 02-market/positioning.json --out 02-market/positioning-map.html
      Render the JSON to a one-page HTML map.
  build_map.py --check 02-market/positioning.json
      Count players, verify a Moore statement exists and the USP is under 20
      words. Print PASS or a clear list of what is missing.

Expected shape of positioning.json:
  {
    "business": "Acme Trust Tools",
    "moore": "For trust administrators at small Jersey trust companies who need
              to close files without three days of manual checks, Acme is a
              compliance workspace that produces an audit-ready file in one
              click. Unlike the incumbent spreadsheet, Acme logs every change.",
    "usp": "The only audit trail trust admins never have to build by hand.",
    "axes": {
      "x": {"label": "Price", "low": "Cheap", "high": "Premium"},
      "y": {"label": "Auditability", "low": "Manual", "high": "Automatic"}
    },
    "players": [
      {"name": "Acme (you)", "x": 0.35, "y": 0.9, "you": true},
      {"name": "Rival A",    "x": 0.8,  "y": 0.4},
      ...
    ]
  }
x and y are 0.0 (left / bottom) to 1.0 (right / top).
"""

import argparse
import html
import json
import os
import sys

SPARK_PRIMARY = "#0B3D2E"   # dark green
SPARK_ACCENT = "#C9A227"    # gold

MIN_PLAYERS = 6
MAX_USP_WORDS = 20

SKELETON = {
    "business": "Your business name",
    "moore": (
        "For [target buyer] who [has this need], [your business] is a "
        "[category] that [delivers this benefit]. Unlike [the main rival or "
        "the status quo], we [the one thing they cannot claim]."
    ),
    "usp": "The one sentence, under 20 words, no rival can honestly say.",
    "axes": {
        "x": {"label": "Axis the buyer weighs", "low": "Low", "high": "High"},
        "y": {"label": "Second axis the buyer weighs", "low": "Low", "high": "High"},
    },
    "players": [
        {"name": "You", "x": 0.3, "y": 0.85, "you": True},
        {"name": "Rival A", "x": 0.8, "y": 0.4},
        {"name": "Rival B", "x": 0.65, "y": 0.55},
        {"name": "Rival C", "x": 0.2, "y": 0.3},
        {"name": "Status quo (spreadsheet / do nothing)", "x": 0.15, "y": 0.15},
        {"name": "Rival D", "x": 0.55, "y": 0.7},
    ],
}


def load_brand(root):
    """Return (primary, accent), falling back to Spark colours."""
    path = os.path.join(root, ".spark", "brand", "brand.json")
    primary, accent = SPARK_PRIMARY, SPARK_ACCENT
    if not os.path.exists(path):
        return primary, accent
    try:
        with open(path, encoding="utf-8") as f:
            brand = json.load(f)
        colours = brand.get("colours", brand.get("colors", {}))
        primary = colours.get("primary", primary)
        accent = colours.get("accent", accent)
    except (ValueError, OSError) as exc:
        print("Note: could not read brand.json (" + str(exc) + "). Using Spark colours.")
    return primary, accent


def load_data(path):
    if not os.path.exists(path):
        print("No data file at " + path + ". Run with --init to write a skeleton first.")
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as exc:
        print("FAIL: " + path + " is not valid JSON (" + str(exc) + ").")
        return None


def count_words(text):
    return len([w for w in str(text).split() if w.strip()])


def check(path):
    data = load_data(path)
    if data is None:
        return 1

    problems = []

    moore = str(data.get("moore", "")).strip()
    # A real Moore statement has substance and no bracketed placeholders left in.
    if count_words(moore) < 15 or "[" in moore:
        problems.append(
            "no complete Moore statement (need 15+ words, no [placeholders] left)"
        )

    usp = str(data.get("usp", "")).strip()
    usp_words = count_words(usp)
    if usp_words == 0:
        problems.append("USP is empty")
    elif usp_words >= MAX_USP_WORDS:
        problems.append(
            "USP is {} words, must be under {}".format(usp_words, MAX_USP_WORDS)
        )

    players = data.get("players", [])
    placed = [
        p for p in players
        if isinstance(p, dict) and p.get("name") and _has_coords(p)
    ]
    if len(placed) < MIN_PLAYERS:
        problems.append(
            "only {} players placed with coordinates, need {}+".format(
                len(placed), MIN_PLAYERS
            )
        )

    if not any(isinstance(p, dict) and p.get("you") for p in players):
        problems.append("no player marked \"you\": true, so the map does not show where you sit")

    print("Players placed: {}   USP words: {}".format(len(placed), usp_words))
    if problems:
        print("FAIL:")
        for p in problems:
            print("  - " + p)
        print("")
        print("Fix these, then run the check again.")
        return 1

    print("PASS: Moore statement written, {}+ players placed, USP under {} words.".format(
        MIN_PLAYERS, MAX_USP_WORDS))
    return 0


def _has_coords(p):
    try:
        float(p.get("x"))
        float(p.get("y"))
        return True
    except (TypeError, ValueError):
        return False


def _clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 0.5
    return max(0.0, min(1.0, v))


def render(data, root, out):
    primary, accent = load_brand(root)
    business = html.escape(str(data.get("business", "Your business")))
    moore = html.escape(str(data.get("moore", "")))
    usp = html.escape(str(data.get("usp", "")))

    axes = data.get("axes", {})
    ax = axes.get("x", {})
    ay = axes.get("y", {})
    x_label = html.escape(str(ax.get("label", "X axis")))
    x_low = html.escape(str(ax.get("low", "Low")))
    x_high = html.escape(str(ax.get("high", "High")))
    y_label = html.escape(str(ay.get("label", "Y axis")))
    y_low = html.escape(str(ay.get("low", "Low")))
    y_high = html.escape(str(ay.get("high", "High")))

    dots = []
    labels = []
    for p in data.get("players", []):
        if not (isinstance(p, dict) and p.get("name") and _has_coords(p)):
            continue
        cx = _clamp(p.get("x")) * 100.0
        cy = (1.0 - _clamp(p.get("y"))) * 100.0  # SVG y grows downward
        you = bool(p.get("you"))
        fill = accent if you else "#ffffff"
        stroke = primary
        r = 1.6 if you else 1.1
        dots.append(
            '<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            'stroke="{stroke}" stroke-width="0.4"/>'.format(
                cx=cx, cy=cy, r=r, fill=fill, stroke=stroke
            )
        )
        name = html.escape(str(p.get("name")))
        weight = "700" if you else "400"
        # nudge label to the right of the dot; anchor start
        labels.append(
            '<text x="{tx:.1f}" y="{ty:.1f}" font-size="2.4" '
            'font-weight="{weight}" fill="{primary}">{name}</text>'.format(
                tx=cx + 2.4, ty=cy + 0.9, weight=weight, primary=primary, name=name
            )
        )

    svg_dots = "\n      ".join(dots)
    svg_labels = "\n      ".join(labels)

    doc = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{business} - positioning map</title>
<style>
  :root {{ --primary: {primary}; --accent: {accent}; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 2rem 1rem; font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #14231d; background: #f6f5f1; }}
  .wrap {{ max-width: 820px; margin: 0 auto; }}
  h1 {{ color: var(--primary); font-size: 1.5rem; margin: 0 0 .25rem; }}
  .sub {{ color: #55665f; margin: 0 0 1.5rem; font-size: .95rem; }}
  .card {{ background: #fff; border: 1px solid #e3e0d8; border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; }}
  .card h2 {{ font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); margin: 0 0 .5rem; }}
  .moore {{ font-size: 1.05rem; line-height: 1.5; }}
  .usp {{ font-size: 1.25rem; font-weight: 700; color: var(--primary); line-height: 1.4; }}
  .mapwrap {{ position: relative; }}
  .axis-y {{ position: absolute; left: -0.5rem; top: 50%; transform: rotate(-90deg) translateX(50%); transform-origin: left top; font-weight: 700; color: var(--primary); font-size: .85rem; white-space: nowrap; }}
  .axis-x {{ text-align: center; font-weight: 700; color: var(--primary); font-size: .85rem; margin-top: .4rem; }}
  svg {{ width: 100%; height: auto; display: block; }}
  .foot {{ color: #77857e; font-size: .8rem; }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>{business}</h1>
    <p class="sub">Positioning map. Where we win, and the one thing no rival can claim.</p>

    <div class="card">
      <h2>Positioning statement</h2>
      <p class="moore">{moore}</p>
    </div>

    <div class="card">
      <h2>The one USP</h2>
      <p class="usp">{usp}</p>
    </div>

    <div class="card">
      <h2>The 2x2</h2>
      <div class="mapwrap">
        <div class="axis-y">{y_label} &rarr;</div>
        <svg viewBox="-2 -2 118 108" role="img" aria-label="Positioning map">
          <!-- quadrant frame -->
          <rect x="0" y="0" width="100" height="100" fill="#fbfaf7" stroke="#d8d4ca" stroke-width="0.5"/>
          <line x1="50" y1="0" x2="50" y2="100" stroke="#d8d4ca" stroke-width="0.5" stroke-dasharray="1.5 1.5"/>
          <line x1="0" y1="50" x2="100" y2="50" stroke="#d8d4ca" stroke-width="0.5" stroke-dasharray="1.5 1.5"/>
          <!-- axis end labels -->
          <text x="1" y="103.5" font-size="2.4" fill="#77857e">{x_low}</text>
          <text x="99" y="103.5" font-size="2.4" fill="#77857e" text-anchor="end">{x_high}</text>
          <text x="-1.5" y="99" font-size="2.4" fill="#77857e" text-anchor="end" transform="rotate(-90 -1.5 99)">{y_low}</text>
          <text x="-1.5" y="1.5" font-size="2.4" fill="#77857e" text-anchor="start" transform="rotate(-90 -1.5 1.5)">{y_high}</text>
          {svg_dots}
          {svg_labels}
        </svg>
        <div class="axis-x">{x_label} &rarr;</div>
      </div>
    </div>

    <p class="foot">Gold dot is you. Generated by spark-bootcamp d2-positioning. The written positioning.md is the record; this page is the picture.</p>
  </div>
</body>
</html>
""".format(
        business=business, primary=primary, accent=accent, moore=moore, usp=usp,
        x_label=x_label, x_low=x_low, x_high=x_high,
        y_label=y_label, y_low=y_low, y_high=y_high,
        svg_dots=svg_dots, svg_labels=svg_labels,
    )

    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("Positioning map written to " + out)


def init(path):
    if os.path.exists(path):
        print(path + " already exists. Not overwriting it.")
        return 0
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(SKELETON, f, indent=2)
        f.write("\n")
    print("Skeleton written to " + path)
    print("Fill it in, then render with --data and --out.")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description="Build or check a 2x2 positioning map.")
    ap.add_argument("--root", default=".", help="Founder project root (for brand.json).")
    ap.add_argument("--data", help="Path to positioning.json to render.")
    ap.add_argument("--out", help="Path to write the HTML map.")
    ap.add_argument("--init", metavar="PATH", nargs="?", const="02-market/positioning.json",
                    help="Write a skeleton positioning.json and stop.")
    ap.add_argument("--check", metavar="PATH", help="Check a positioning.json against the done-condition.")
    args = ap.parse_args(argv[1:])

    if args.init is not None:
        return init(args.init)

    if args.check:
        return check(args.check)

    if args.data and args.out:
        data = load_data(args.data)
        if data is None:
            return 1
        render(data, args.root, args.out)
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
