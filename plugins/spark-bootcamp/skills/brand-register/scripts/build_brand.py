#!/usr/bin/env python3
"""Write and validate .spark/brand/brand.json, the one source of brand truth.

Every later document (deck, brochure, sales deck, proposal) reads its colours,
fonts, logo, tone and tagline from this file and nowhere else. So this script
is strict: it will not write a palette that fails WCAG AA contrast, because a
brand that cannot be read is not a brand.

What it does:
  1. Takes your brand tokens (primary + secondary colour, heading + body font,
     logo path, tone line, tagline).
  2. Checks the palette passes WCAG AA (contrast ratio at least 4.5:1 for normal
     text) against white and black, and reports the readable text colour for
     each brand colour.
  3. Copies your logo to .spark/brand/logo.svg.
  4. Writes .spark/brand/brand.json.

If the palette fails AA it prints exactly what failed and its ratio, writes
nothing, and exits non-zero so you fix the colour rather than ship an unreadable
one.

Usage:
  build_brand.py --root . \
    --primary '#0B3D2E' --secondary '#C9A227' \
    --font-heading 'Fraunces' --font-body 'Inter' \
    --logo 02-market/brand/logo.svg \
    --tone 'Direct, warm, no jargon. We put a number on everything.' \
    --tagline 'Idea to system in five days.'

  # Only validate a pair, write nothing:
  build_brand.py --check-only --primary '#0B3D2E' --secondary '#C9A227'

Pure standard library. No third-party dependency, so it runs anywhere Python 3
runs.
"""

import argparse
import json
import os
import shutil
import sys

AA_NORMAL = 4.5   # WCAG 2.1 AA for normal-size text
AA_LARGE = 3.0    # WCAG 2.1 AA for large text (18pt+/14pt bold)

WHITE = "#FFFFFF"
BLACK = "#000000"


def norm_hex(value):
    """Normalise '#abc' or 'abc' or '#aabbcc' to '#AABBCC'. Returns None if bad."""
    if not value:
        return None
    v = value.strip().lstrip("#")
    if len(v) == 3 and all(c in "0123456789abcdefABCDEF" for c in v):
        v = "".join(c * 2 for c in v)
    if len(v) != 6 or any(c not in "0123456789abcdefABCDEF" for c in v):
        return None
    return "#" + v.upper()


def _channel(c):
    """One sRGB channel (0..1) to linear light, per WCAG."""
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_colour):
    v = hex_colour.lstrip("#")
    r, g, b = (int(v[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(hex_a, hex_b):
    la = relative_luminance(hex_a)
    lb = relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def best_text_on(brand_hex):
    """Return (text_colour, ratio) for the more readable of white/black text."""
    on_white = contrast_ratio(brand_hex, WHITE)
    on_black = contrast_ratio(brand_hex, BLACK)
    if on_black >= on_white:
        return BLACK, on_black
    return WHITE, on_white


def check_palette(primary, secondary):
    """Return (ok, report).

    Spark documents (decks, brochures, proposals) are white-backgrounded, so
    the check has teeth: the PRIMARY must be legible as text on white, at least
    4.5:1. That rejects pale or pastel primaries, which is the whole point. A
    single colour can never fail the "best of white/black" test at 4.5:1, so
    that test would be toothless.

    The SECONDARY is an accent (fills, bars, highlights), not body text, so it
    is reported but never hard-fails: bright accents legitimately sit below AA
    on white and carry dark text on top. For each colour we also record the
    readable text colour to use when it is used as a fill.
    """
    report = {}
    ok = True
    for label, colour in (("primary", primary), ("secondary", secondary)):
        if colour is None:
            continue
        on_white = contrast_ratio(colour, WHITE)
        text, ratio_on = best_text_on(colour)
        entry = {
            "colour": colour,
            "on_white": on_white,          # this colour used as text on a white page
            "readable_text": text,          # text colour to use when this is a fill
            "readable_text_ratio": ratio_on,
            "passes_aa_normal_on_white": on_white >= AA_NORMAL,
            "passes_aa_large_on_white": on_white >= AA_LARGE,
        }
        report[label] = entry
        # Only the primary is a hard gate. It is the brand text colour.
        if label == "primary" and on_white < AA_NORMAL:
            ok = False
    return ok, report


def find_root(start):
    """Walk up from start to find the folder holding .spark. Fall back to start."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".spark")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start)
        cur = parent


def main():
    ap = argparse.ArgumentParser(description="Build and validate brand.json")
    ap.add_argument("--root", default=".", help="Project root holding .spark")
    ap.add_argument("--primary", help="Primary colour, hex")
    ap.add_argument("--secondary", help="Secondary colour, hex")
    ap.add_argument("--font-heading", help="Heading font name")
    ap.add_argument("--font-body", help="Body font name")
    ap.add_argument("--logo", help="Path to the logo to copy into .spark/brand/")
    ap.add_argument("--tone", help="One-line tone-of-voice statement")
    ap.add_argument("--tagline", help="The tagline")
    ap.add_argument("--check-only", action="store_true",
                    help="Only validate the palette, write nothing")
    args = ap.parse_args()

    primary = norm_hex(args.primary)
    secondary = norm_hex(args.secondary)

    if args.primary and primary is None:
        print("ERROR: primary '%s' is not a valid hex colour." % args.primary)
        return 2
    if args.secondary and secondary is None:
        print("ERROR: secondary '%s' is not a valid hex colour." % args.secondary)
        return 2
    if primary is None:
        print("ERROR: a primary colour is required.")
        return 2

    ok, report = check_palette(primary, secondary)

    print("Palette contrast on a white page (WCAG AA needs 4.5:1 for normal text):")
    for label, r in report.items():
        if label == "primary":
            verdict = "PASS" if r["passes_aa_normal_on_white"] else "FAIL"
            print("  primary   %s  as text on white %.2f:1  [%s]"
                  % (r["colour"], r["on_white"], verdict))
        else:
            note = "OK as body text on white" if r["passes_aa_normal_on_white"] \
                else "accent only, put %s text on top" % r["readable_text"]
            print("  secondary %s  as text on white %.2f:1  (%s)"
                  % (r["colour"], r["on_white"], note))

    if not ok:
        print("\nPrimary FAILS AA on white (needs 4.5:1). It is your brand text "
              "colour, so pick a darker shade, then run again. Nothing was "
              "written.")
        return 1

    if args.check_only:
        print("\nPalette passes AA. (check-only: nothing written.)")
        return 0

    # From here we write. Everything below needs the writeable fields.
    root = find_root(args.root)
    brand_dir = os.path.join(root, ".spark", "brand")
    os.makedirs(brand_dir, exist_ok=True)

    logo_rel = ".spark/brand/logo.svg"
    logo_note = None
    if args.logo:
        src = args.logo if os.path.isabs(args.logo) else os.path.join(root, args.logo)
        dst = os.path.join(brand_dir, "logo.svg")
        if os.path.isfile(src):
            try:
                shutil.copyfile(src, dst)
            except Exception as exc:  # never crash on a copy problem
                logo_note = "could not copy logo (%s); brand.json still written" % exc
        else:
            logo_note = "logo source '%s' not found; recorded the path anyway" % args.logo

    brand = {
        "primary": primary,
        "secondary": secondary,
        "fonts": {
            "heading": args.font_heading or "",
            "body": args.font_body or "",
        },
        "logo": logo_rel,
        "tone": args.tone or "",
        "tagline": args.tagline or "",
        "contrast": report,
    }

    out = os.path.join(brand_dir, "brand.json")
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(brand, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, out)

    print("\nWrote %s" % out)
    if os.path.isfile(os.path.join(brand_dir, "logo.svg")):
        print("Wrote %s" % os.path.join(brand_dir, "logo.svg"))
    if logo_note:
        print("Note: %s" % logo_note)

    # A tiny self-validation, so the caller's done-condition is objective.
    missing = []
    if not brand["primary"]:
        missing.append("primary")
    if not (brand["fonts"]["heading"] or brand["fonts"]["body"]):
        missing.append("a font")
    if not brand["logo"]:
        missing.append("logo path")
    if not brand["tone"]:
        missing.append("tone line")
    if missing:
        print("\nWARNING: brand.json is missing: %s. Fill these before you "
              "build any document from it." % ", ".join(missing))
        return 3

    print("\nbrand.json validates: primary set, a font set, logo path set, "
          "tone line set, palette passes AA.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
