#!/usr/bin/env python3
"""Build a logo and a brand board from brand-tokens.json.

Pure standard library. No installs, no network, no design software. Give it your
tokens file and it writes two things next to it:

  logo.svg          a clean wordmark a non-designer can ship today
  brand-board.html  a one-page reference: swatches with hex and contrast, fonts,
                    the logo, and your tone line

It refuses to build if the palette fails WCAG AA, because a brand board that
looks fine on your screen and fails a regulator's eye on a projector is worse
than none. Fix the colour, run again.

Usage:
  python3 build_identity.py --tokens 02-market/brand/brand-tokens.json

Writes into the same folder as the tokens file unless you pass --out-dir.
"""

import argparse
import json
import os
import sys

# Reuse the exact AA maths from the checker so there is one source of truth.
# If for any reason it cannot be imported, fall back to a local copy so this
# script still runs rather than crashing.
try:
    from check_contrast import contrast_ratio, norm_hex
except Exception:  # pragma: no cover - defensive fallback
    def norm_hex(value):
        v = value.strip().lstrip("#")
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        if len(v) != 6:
            raise ValueError("bad hex: %r" % value)
        int(v, 16)
        return "#" + v.upper()

    def _channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def contrast_ratio(a, b):
        def lum(h):
            h = norm_hex(h).lstrip("#")
            r, g, bb = (int(h[i:i + 2], 16) for i in (0, 2, 4))
            return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(bb)
        la, lb = lum(a), lum(b)
        hi, lo = max(la, lb), min(la, lb)
        return (hi + 0.05) / (lo + 0.05)


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def build_logo_svg(name, colours, heading_font):
    """A wordmark: a rounded initial tile plus the name, with an accent full stop.

    Renders anywhere because it uses a generic font family, not a downloaded one.
    """
    ink = norm_hex(colours.get("ink", "#12211B"))
    primary = norm_hex(colours.get("primary", "#0B3D2E"))
    accent = norm_hex(colours.get("accent", primary))
    surface = norm_hex(colours.get("surface", "#FFFFFF"))

    initial = (name.strip()[:1] or "S").upper()
    # Generic family so the SVG is portable. If the heading font names a serif,
    # keep the wordmark serif; otherwise sans. Cheap heuristic, honest result.
    family = "serif" if "serif" in heading_font.lower() and "sans" not in heading_font.lower() else "sans-serif"

    tile = 64
    pad = 20
    text_x = tile + 24
    # Rough width so the viewBox fits the name without a font metrics library.
    char_w = 30
    text_w = len(name) * char_w
    width = text_x + text_w + pad
    height = tile + pad * 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{esc(name)} logo">
  <rect width="{width}" height="{height}" fill="{surface}"/>
  <rect x="{pad}" y="{pad}" width="{tile}" height="{tile}" rx="14" fill="{primary}"/>
  <text x="{pad + tile / 2}" y="{pad + tile / 2 + 1}" font-family="{family}" font-size="38" font-weight="700" fill="{surface}" text-anchor="middle" dominant-baseline="central">{esc(initial)}</text>
  <text x="{text_x}" y="{height / 2 + 1}" font-family="{family}" font-size="44" font-weight="700" fill="{ink}" dominant-baseline="central">{esc(name)}<tspan fill="{accent}">.</tspan></text>
</svg>
"""


def swatch_row(label, key, colours, minimum):
    value = colours.get(key)
    if not value:
        return ""
    surface = colours.get("surface", "#FFFFFF")
    try:
        hexv = norm_hex(value)
        ratio = contrast_ratio(value, surface)
        verdict = "PASS" if ratio >= minimum else "FAIL"
    except ValueError:
        hexv, ratio, verdict = value, 0.0, "INVALID"
    badge = "#0B3D2E" if verdict == "PASS" else "#B00020"
    return f"""
      <div class="swatch">
        <div class="chip" style="background:{esc(hexv)}"></div>
        <div class="meta">
          <div class="role">{esc(label)}</div>
          <div class="hex">{esc(hexv)}</div>
          <div class="ratio">{ratio:.2f}:1 on surface, needs {minimum} <span class="badge" style="background:{badge}">{verdict}</span></div>
        </div>
      </div>"""


def build_board_html(tokens):
    name = tokens.get("name", "Your brand")
    colours = tokens.get("colours", {})
    fonts = tokens.get("fonts", {})
    tone = tokens.get("tone", "")
    tagline = tokens.get("tagline", "")
    surface = colours.get("surface", "#FFFFFF")
    ink = colours.get("ink", "#12211B")
    muted = colours.get("muted", "#5B6B63")
    primary = colours.get("primary", "#0B3D2E")
    heading = fonts.get("heading", "Georgia, 'Times New Roman', serif")
    body = fonts.get("body", "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif")

    rows = "".join([
        swatch_row("Ink (body text)", "ink", colours, 4.5),
        swatch_row("Primary (headings, links)", "primary", colours, 4.5),
        swatch_row("Muted (secondary text)", "muted", colours, 4.5),
        swatch_row("Accent (buttons, rules)", "accent", colours, 3.0),
        swatch_row("Surface (background)", "surface", colours, 0),
    ])

    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(name)} brand board</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin:0; background:{esc(surface)}; color:{esc(ink)};
         font-family:{esc(body)}; line-height:1.5; }}
  .wrap {{ max-width:840px; margin:0 auto; padding:40px 24px 64px; }}
  h1 {{ font-family:{esc(heading)}; font-size:2.4rem; margin:0 0 4px; color:{esc(ink)}; }}
  h2 {{ font-family:{esc(heading)}; font-size:1.3rem; margin:40px 0 12px;
        color:{esc(primary)}; border-bottom:2px solid {esc(colours.get('accent', primary))};
        padding-bottom:6px; }}
  .tagline {{ color:{esc(muted)}; font-size:1.05rem; margin:0 0 24px; }}
  .logo {{ border:1px solid #E4E7E5; border-radius:12px; padding:24px; overflow-x:auto; }}
  .logo img {{ max-width:100%; height:auto; display:block; }}
  .swatches {{ display:flex; flex-wrap:wrap; gap:16px; }}
  .swatch {{ display:flex; gap:12px; align-items:center; width:calc(50% - 8px);
             min-width:240px; }}
  .chip {{ width:56px; height:56px; border-radius:10px; border:1px solid #E4E7E5;
           flex:0 0 auto; }}
  .role {{ font-weight:600; }}
  .hex {{ font-family:ui-monospace, Menlo, Consolas, monospace; color:{esc(muted)}; }}
  .ratio {{ font-size:.85rem; color:{esc(muted)}; }}
  .badge {{ color:#fff; border-radius:6px; padding:1px 7px; font-size:.75rem; margin-left:4px; }}
  .specimen {{ border:1px solid #E4E7E5; border-radius:12px; padding:20px; }}
  .specimen .h {{ font-family:{esc(heading)}; font-size:1.8rem; }}
  .specimen .b {{ font-family:{esc(body)}; font-size:1rem; }}
  .fontname {{ font-family:ui-monospace, Menlo, Consolas, monospace; color:{esc(muted)};
               font-size:.85rem; }}
  .tone {{ background:#F4F6F5; border-radius:12px; padding:16px 20px; }}
  @media (max-width:560px) {{ .swatch {{ width:100%; }} }}
</style>
</head>
<body>
<div class="wrap">
  <h1>{esc(name)}</h1>
  <p class="tagline">{esc(tagline) or "Brand board, generated Day 2."}</p>

  <h2>Logo</h2>
  <div class="logo"><img src="logo.svg" alt="{esc(name)} logo"></div>

  <h2>Palette</h2>
  <div class="swatches">{rows}
  </div>

  <h2>Type</h2>
  <div class="specimen">
    <div class="h">{esc(name)} ships in weeks, not quarters.</div>
    <div class="fontname">Heading: {esc(heading)}</div>
    <p class="b">This is body text. It is set in a system-safe font so every
    document loads instantly, works offline, and reads the same on every device
    a regulated buyer might open it on. No downloads, no licences, no surprises.</p>
    <div class="fontname">Body: {esc(body)}</div>
  </div>

  <h2>Tone</h2>
  <div class="tone">{esc(tone) or "Set your tone line in brand-tokens.json."}</div>
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Build logo.svg and brand-board.html from tokens.")
    ap.add_argument("--tokens", required=True, help="Path to brand-tokens.json")
    ap.add_argument("--out-dir", help="Where to write outputs (default: tokens folder)")
    args = ap.parse_args()

    try:
        with open(args.tokens, "r", encoding="utf-8") as fh:
            tokens = json.load(fh)
    except FileNotFoundError:
        print("No tokens file at %s. Write brand-tokens.json first." % args.tokens)
        return 1
    except (ValueError, json.JSONDecodeError) as exc:
        print("brand-tokens.json is not valid JSON: %s" % exc)
        return 1

    colours = tokens.get("colours", {})
    surface = colours.get("surface", "#FFFFFF")
    name = tokens.get("name") or "Your brand"
    fonts = tokens.get("fonts", {})
    heading = fonts.get("heading", "Georgia, 'Times New Roman', serif")
    body = fonts.get("body", "")

    # Refuse to build on an AA failure. Text roles must clear their bar.
    problems = []
    for key, minimum in (("ink", 4.5), ("primary", 4.5), ("muted", 4.5), ("accent", 3.0)):
        v = colours.get(key)
        if not v:
            continue
        try:
            r = contrast_ratio(v, surface)
        except ValueError:
            problems.append("%s (%s) is not a valid hex colour" % (key, v))
            continue
        if r < minimum:
            problems.append("%s (%s) is %.2f:1 on surface, needs %.1f" % (key, norm_hex(v), r, minimum))

    if problems:
        print("Not building. The palette fails WCAG AA:")
        for p in problems:
            print("  - " + p)
        print("Darken the failing colour, or move a pale colour to 'accent', then run again.")
        return 1

    if not fonts.get("heading") or not body:
        print("Need two fonts. Set fonts.heading and fonts.body in brand-tokens.json.")
        return 1

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.tokens))
    os.makedirs(out_dir, exist_ok=True)

    logo_path = os.path.join(out_dir, "logo.svg")
    board_path = os.path.join(out_dir, "brand-board.html")

    with open(logo_path, "w", encoding="utf-8") as fh:
        fh.write(build_logo_svg(name, colours, heading))
    with open(board_path, "w", encoding="utf-8") as fh:
        fh.write(build_board_html(tokens))

    print("Built:")
    print("  " + logo_path)
    print("  " + board_path)
    print("Palette passes WCAG AA. Two fonts set. One SVG wordmark written.")
    print("Next: open brand-board.html to eyeball it, then run brand-register.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
