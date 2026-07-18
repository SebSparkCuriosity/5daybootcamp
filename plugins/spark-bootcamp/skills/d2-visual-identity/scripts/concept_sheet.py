#!/usr/bin/env python3
"""Compose logo concept SVGs into one side-by-side choice sheet.

Pure standard library. Reads every .svg in --dir (sorted by name), inlines each
into a self-contained HTML page showing it three ways: large on white, tiny at
32 pixels (the squint test), and on a dark panel (the reversed test). The
founder opens one file and points at the winner.

Usage:
  python3 concept_sheet.py --dir 02-market/brand/concepts \
      --out 02-market/brand/logo-concepts.html
"""

import argparse
import os
import re
import sys


def strip_svg(markup):
    """Drop XML prologue and doctype so the SVG inlines cleanly into HTML."""
    markup = re.sub(r"<\?xml[^>]*\?>", "", markup)
    markup = re.sub(r"<!DOCTYPE[^>]*>", "", markup, flags=re.IGNORECASE)
    return markup.strip()


def card(name, svg):
    label = os.path.splitext(name)[0].replace("-", " ").replace("_", " ")
    return f"""
  <section class="card">
    <h2>{label}</h2>
    <div class="large">{svg}</div>
    <div class="row">
      <div class="tiny" title="32px squint test">{svg}</div>
      <div class="dark" title="on dark">{svg}</div>
    </div>
  </section>"""


def main():
    ap = argparse.ArgumentParser(description="Build a logo concept choice sheet.")
    ap.add_argument("--dir", required=True, help="Folder holding concept .svg files")
    ap.add_argument("--out", required=True, help="Output HTML path")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        print(f"No folder at {args.dir}. Save the concept SVGs there first.")
        return 1

    files = sorted(f for f in os.listdir(args.dir) if f.lower().endswith(".svg"))
    if not files:
        print(f"No .svg files in {args.dir}. Save the concepts there first.")
        return 1

    cards = []
    for name in files:
        with open(os.path.join(args.dir, name), "r", encoding="utf-8") as fh:
            cards.append(card(name, strip_svg(fh.read())))

    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Logo concepts</title>
<style>
  body {{ margin:0; background:#F4F6F5; color:#12211B;
         font-family:system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:32px 20px 56px; }}
  h1 {{ font-size:1.6rem; margin:0 0 4px; }}
  .hint {{ color:#5B6B63; margin:0 0 24px; }}
  .card {{ background:#fff; border:1px solid #E4E7E5; border-radius:14px;
           padding:20px 24px; margin-bottom:20px; }}
  .card h2 {{ font-size:1rem; margin:0 0 14px; text-transform:capitalize; color:#5B6B63; }}
  .large svg {{ max-width:100%; height:auto; max-height:140px; display:block; }}
  .row {{ display:flex; gap:20px; align-items:center; margin-top:16px; }}
  .tiny svg {{ width:32px; height:32px; display:block; }}
  .tiny {{ border:1px dashed #E4E7E5; border-radius:8px; padding:10px; }}
  .dark {{ background:#12211B; border-radius:8px; padding:14px 18px; }}
  .dark svg {{ max-height:48px; width:auto; display:block; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Pick the one you would put on an invoice</h1>
  <p class="hint">Each concept shown large, at 32 pixels (the squint test), and on dark.</p>
{''.join(cards)}
</div>
</body>
</html>
"""
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {args.out} with {len(files)} concepts. Open it with the founder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
