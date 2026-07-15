#!/usr/bin/env python3
"""Check a brand palette against WCAG AA contrast.

Pure standard library. No installs, no network. Give it the tokens file and it
tells you, in plain English, whether your colours are legible on your background.

AA thresholds, the same ones every accessibility auditor uses:
  - normal text needs a contrast ratio of at least 4.5 to 1
  - large text and user-interface parts need at least 3.0 to 1

Usage:
  python3 check_contrast.py --tokens 02-market/brand/brand-tokens.json

Exit code 0 means the palette passes AA. Exit code 1 means at least one
colour that carries text failed, and the reason is printed. Nothing is written;
this script only reads and reports.
"""

import argparse
import json
import sys

WHITE = "#FFFFFF"
BLACK = "#000000"


def norm_hex(value):
    """Accept '#0B3D2E', '0b3d2e' or '#036' and return '#RRGGBB' upper-case."""
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError("not a 3 or 6 digit hex colour: %r" % value)
    int(v, 16)  # raises if not hex
    return "#" + v.upper()


def _channel(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_colour):
    h = norm_hex(hex_colour).lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(hex_a, hex_b):
    la = relative_luminance(hex_a)
    lb = relative_luminance(hex_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def load_tokens(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description="Check a brand palette against WCAG AA.")
    ap.add_argument("--tokens", required=True, help="Path to brand-tokens.json")
    args = ap.parse_args()

    try:
        tokens = load_tokens(args.tokens)
    except FileNotFoundError:
        print("No tokens file at %s. Write brand-tokens.json first." % args.tokens)
        return 1
    except (ValueError, json.JSONDecodeError) as exc:
        print("brand-tokens.json is not valid JSON: %s" % exc)
        return 1

    colours = tokens.get("colours", {})
    surface = colours.get("surface", WHITE)

    # role -> (colour key, minimum ratio it must clear)
    # ink and muted and primary carry text, so they need 4.5. accent is used
    # for large elements and UI, so 3.0 is the honest bar for it.
    checks = [
        ("ink (body text)", "ink", 4.5),
        ("primary (headings, links)", "primary", 4.5),
        ("muted (secondary text)", "muted", 4.5),
        ("accent (buttons, rules)", "accent", 3.0),
    ]

    print("Palette contrast against your surface colour %s" % surface)
    print("WCAG AA: 4.5:1 for normal text, 3.0:1 for large text and UI.\n")

    failed = []
    for label, key, minimum in checks:
        value = colours.get(key)
        if not value:
            continue
        try:
            ratio = contrast_ratio(value, surface)
        except ValueError as exc:
            print("  %-28s %s  INVALID (%s)" % (label, value, exc))
            failed.append(label)
            continue
        verdict = "PASS" if ratio >= minimum else "FAIL"
        if verdict == "FAIL":
            failed.append(label)
        print("  %-28s %s  %.2f:1  needs %.1f  %s" %
              (label, norm_hex(value), ratio, minimum, verdict))

    print()
    if failed:
        print("FAIL: %d colour(s) below the AA bar: %s." % (len(failed), ", ".join(failed)))
        print("Fix: darken the failing colour until it clears its bar, then run again.")
        print("A pale brand colour can move to 'accent'; text roles need a darker value.")
        return 1

    print("PASS: every text and UI colour clears WCAG AA on your surface.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
