#!/usr/bin/env python3
"""A lightweight accessibility check for the landing page.

Four checks, the ones that actually keep a regulated buyer or a screen-reader
user out: colour contrast, form labels, keyboard reachability, and image alt
text. It parses the HTML with the Python standard library (html.parser), so it
needs no third-party package and never crashes on a missing library.

It writes a pass/flag report to 03-product/site/accessibility-report.md and
prints PASS or a numbered list of flags. Exit code is 0 on PASS and 1 when
there are flags, so a script can gate on it, but the report is the artefact of
record either way.

Usage:
  a11y_check.py 03-product/site/index.html --root .
"""

import argparse
import json
import os
import sys
from html.parser import HTMLParser

INTERACTIVE_NATIVE = {"a", "button", "input", "select", "textarea"}


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = []        # (attrs dict)
        self.labels = []        # 'for' values
        self.aria_label_ids = set()
        self.images = []        # (attrs dict)
        self.clickable_divs = []  # tags with onclick that are not native-interactive
        self.styles = []        # inline <style> text

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("input", "textarea", "select"):
            if a.get("type") not in ("hidden", "submit", "button"):
                self.inputs.append((tag, a))
        elif tag == "label":
            if a.get("for"):
                self.labels.append(a["for"])
        elif tag == "img":
            self.images.append(a)
        if "onclick" in a and tag not in INTERACTIVE_NATIVE:
            role = a.get("role", "")
            tabindex = a.get("tabindex")
            if role not in ("button", "link") or tabindex is None:
                self.clickable_divs.append(tag)

    def handle_data(self, data):
        pass


class StyleGrabber(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_style = False
        self.css = []

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self._in_style = True

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.css.append(data)


def rel_lum(hexcol):
    h = hexcol.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = lin(r), lin(g), lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(hex1, hex2):
    l1, l2 = rel_lum(hex1), rel_lum(hex2)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", help="Path to the landing page HTML")
    ap.add_argument("--root", default=".", help="Founder project root holding .spark")
    ap.add_argument("--out", default="03-product/site/accessibility-report.md")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    page = args.page if os.path.isabs(args.page) else os.path.join(root, args.page)

    try:
        with open(page, encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print("ERROR: cannot read %s (%s)" % (page, e), file=sys.stderr)
        sys.exit(1)

    col = Collector()
    col.feed(html)
    sg = StyleGrabber()
    sg.feed(html)

    flags = []
    passes = []

    # 1. Contrast. Prefer the measured ratio in brand.json; else compute primary on white.
    brand_path = os.path.join(root, ".spark", "brand", "brand.json")
    ratio = None
    primary = None
    try:
        with open(brand_path, encoding="utf-8") as f:
            brand = json.load(f)
        primary = brand.get("primary")
        ratio = (brand.get("contrast", {}).get("primary", {}) or {}).get("on_white")
    except Exception:
        pass
    if ratio is None and primary:
        ratio = contrast(primary, "#FFFFFF")
    if ratio is None:
        flags.append("Contrast: no brand.json and no primary colour to test. Check text-on-white by hand (need 4.5:1).")
    elif ratio >= 4.5:
        passes.append("Contrast: body text %s on white is %.2f:1 (AA pass, needs 4.5)." % (primary or "primary", ratio))
    else:
        flags.append("Contrast: text %s on white is only %.2f:1 (needs 4.5). Darken the primary and rebuild." % (primary, ratio))

    # 2. Form labels. Every visible input needs a <label for> or an aria-label.
    unlabelled = []
    for tag, a in col.inputs:
        fid = a.get("id")
        has_label = fid and fid in col.labels
        has_aria = a.get("aria-label") or a.get("aria-labelledby")
        if not has_label and not has_aria:
            unlabelled.append(a.get("name") or a.get("id") or "(unnamed %s)" % tag)
    if not col.inputs:
        flags.append("Labels: no form fields found. A landing page with no capture is not launchable.")
    elif unlabelled:
        flags.append("Labels: %d field(s) have no label: %s. Add a <label for> or aria-label." % (len(unlabelled), ", ".join(unlabelled)))
    else:
        passes.append("Labels: all %d form field(s) have an associated label." % len(col.inputs))

    # 3. Keyboard reachability. Flag onclick on non-interactive elements, and outline:none.
    kb_issues = []
    if col.clickable_divs:
        kb_issues.append("%d non-button element(s) with onclick and no keyboard role/tabindex" % len(col.clickable_divs))
    css = "".join(sg.css).lower()
    if ("outline:none" in css.replace(" ", "") or "outline:0" in css.replace(" ", "")) and "focus" not in css:
        kb_issues.append("focus outline removed with no visible replacement")
    if kb_issues:
        flags.append("Keyboard: " + "; ".join(kb_issues) + ". Use native buttons/links and keep a visible focus ring.")
    else:
        passes.append("Keyboard: controls are native and a visible focus style is present.")

    # 4. Alt text. Every <img> needs an alt attribute (empty alt allowed for decorative, but flagged for review).
    missing_alt = [a.get("src", "(no src)") for a in col.images if "alt" not in a]
    empty_alt = [a.get("src", "(no src)") for a in col.images if a.get("alt", None) == ""]
    if not col.images:
        passes.append("Alt text: no images on the page, nothing to caption.")
    elif missing_alt:
        flags.append("Alt text: %d image(s) have no alt attribute: %s. Add descriptive alt, or alt=\"\" if purely decorative." % (len(missing_alt), ", ".join(missing_alt)))
    elif empty_alt:
        flags.append("Alt text: %d image(s) have empty alt (decorative). Confirm they carry no meaning: %s." % (len(empty_alt), ", ".join(empty_alt)))
    else:
        passes.append("Alt text: all %d image(s) have descriptive alt text." % len(col.images))

    status = "PASS" if not flags else "FLAGGED"

    # Write the report.
    lines = ["# Accessibility report", "", "Page: `%s`" % os.path.relpath(page, root), "", "Result: **%s**" % status, ""]
    if passes:
        lines.append("## Passed")
        lines.append("")
        for p in passes:
            lines.append("- " + p)
        lines.append("")
    if flags:
        lines.append("## Flags to fix")
        lines.append("")
        for i, fl in enumerate(flags, 1):
            lines.append("%d. %s" % (i, fl))
        lines.append("")
        lines.append("## Consciously accepted")
        lines.append("")
        lines.append("If you decide not to fix a flag above, move it here with a one-line reason. An empty list means every flag was fixed.")
        lines.append("")
    lines.append("Checked: contrast, form labels, keyboard reachability, image alt text.")
    out_path = os.path.join(root, args.out) if not os.path.isabs(args.out) else args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("Accessibility check: %s" % status)
    for p in passes:
        print("  pass: " + p)
    for i, fl in enumerate(flags, 1):
        print("  flag %d: %s" % (i, fl))
    print("\nReport written to %s" % out_path)
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
