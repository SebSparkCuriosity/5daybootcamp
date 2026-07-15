#!/usr/bin/env python3
"""Build the founder's landing page from brand.json and proposition.md.

Reads the founder's brand tokens, their proposition headline and metric, and
their business_type, then writes a finished, on-brand, single-page site to
03-product/site/index.html using the house template in references/landing.html.

It never crashes. Missing brand file, thin proposition, no state: it fills a
neutral default, writes the page anyway, and prints exactly what it guessed so
the founder can fix it before launch.

Usage:
  build_landing.py --root .            # founder project root holding .spark
  build_landing.py --root /path/to/project --out 03-product/site/index.html
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "references", "landing.html")

# One row per path: the variant that decides the CTA, hero and fields.
VARIANTS = {
    "software": {
        "kind": "signup",
        "cta": "Create your account",
        "hero": "",
        "fields": [("name", "Your name", "text"), ("email", "Work email", "email")],
    },
    "hardware": {
        "kind": "waitlist",
        "cta": "Join the waitlist",
        "hero": '<div class="hero-media"><img src="hero.png" alt="{alt}"></div>',
        "fields": [("name", "Your name", "text"), ("email", "Email", "email")],
    },
    "services": {
        "kind": "booking",
        "cta": "Book a call",
        "hero": "",
        "fields": [
            ("name", "Your name", "text"),
            ("email", "Email", "email"),
            ("note", "What do you need help with?", "textarea"),
        ],
    },
}

DEFAULT_BRAND = {
    "primary": "#0B3D2E",
    "secondary": "#C9A227",
    "fonts": {"heading": "Georgia", "body": "system-ui"},
    "logo": "",
    "tagline": "",
}


def note(msg):
    print("  note: " + msg)


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def load_state(root):
    st = read_json(os.path.join(root, ".spark", "state.json")) or {}
    return {
        "business_type": (st.get("business_type") or "").strip().lower(),
        "founder": st.get("founder") or "",
        "idea": st.get("idea") or "",
    }


def parse_proposition(text):
    """Pull a headline, a subhead and a metric out of proposition.md.

    We do not assume a rigid format. The first H1 or first bold line is the
    headline; the first line with a number and a unit-ish token is the metric;
    the first ordinary sentence after the headline is the subhead. Anything we
    cannot find comes back empty and the caller fills a default.
    """
    headline = subhead = metric = ""
    if not text:
        return headline, subhead, metric
    lines = [ln.strip() for ln in text.splitlines()]
    for ln in lines:
        if ln.startswith("# "):
            headline = ln[2:].strip()
            break
    if not headline:
        for ln in lines:
            m = re.match(r"^\*\*(.+?)\*\*", ln)
            if m:
                headline = m.group(1).strip()
                break
    # Metric: a line containing a digit and a percent, currency, or "from ... to".
    for ln in lines:
        if re.search(r"\d", ln) and re.search(r"%|£|\$|from .+ to |x |per |days?|hours?|weeks?", ln, re.I):
            metric = re.sub(r"^[#>*\-\s]+", "", ln).strip().rstrip(".")
            break
    # Subhead: first substantial prose line that is not the headline or metric.
    for ln in lines:
        clean = re.sub(r"^[#>*\-\s]+", "", ln).strip()
        if len(clean) > 30 and clean != headline and clean != metric and not clean.startswith("|"):
            subhead = clean
            break
    return headline, subhead, metric


def build_fields(fields):
    out = []
    for name, label, kind in fields:
        fid = "f_" + name
        out.append('    <div>')
        out.append('      <label for="%s">%s</label>' % (fid, label))
        if kind == "textarea":
            out.append('      <textarea id="%s" name="%s" rows="3"></textarea>' % (fid, name))
        else:
            req = ' required' if name == "email" else ''
            out.append('      <input type="%s" id="%s" name="%s"%s>' % (kind, fid, name, req))
        out.append('    </div>')
    return "\n".join(out)


def readable_on(hexcol):
    """Return #000000 or #FFFFFF, whichever is more legible on the colour."""
    try:
        h = hexcol.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        # perceived luminance
        lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#000000" if lum > 0.55 else "#FFFFFF"
    except Exception:
        return "#000000"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Founder project root holding .spark")
    ap.add_argument("--out", default="03-product/site/index.html", help="Output path, relative to root")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print("Building landing page for project: " + root)

    template = read_text(TEMPLATE)
    if template is None:
        print("ERROR: cannot read the house template at %s" % TEMPLATE, file=sys.stderr)
        sys.exit(1)

    state = load_state(root)
    btype = state["business_type"]
    if btype not in VARIANTS:
        note("business_type not set or unknown ('%s'); defaulting to 'software'. Set it in state.json." % btype)
        btype = "software"
    variant = VARIANTS[btype]
    print("  path: %s" % btype)

    brand = read_json(os.path.join(root, ".spark", "brand", "brand.json"))
    if not brand:
        note("no .spark/brand/brand.json; using neutral defaults. Run brand-register to fix the look.")
        brand = DEFAULT_BRAND
    primary = brand.get("primary") or DEFAULT_BRAND["primary"]
    secondary = brand.get("secondary") or DEFAULT_BRAND["secondary"]
    fonts = brand.get("fonts") or {}
    font_heading = fonts.get("heading") or DEFAULT_BRAND["fonts"]["heading"]
    font_body = fonts.get("body") or DEFAULT_BRAND["fonts"]["body"]
    tagline = brand.get("tagline") or ""
    logo = brand.get("logo") or ""

    prop_text = read_text(os.path.join(root, "02-market", "proposition.md"))
    headline, subhead, metric = parse_proposition(prop_text)
    if not headline:
        headline = state["idea"] or "A better way, live this week."
        note("no headline found in proposition.md; using the idea line. Edit the H1 in index.html.")
    if not subhead:
        subhead = "Built for people who need this to actually work, not just look good in a deck."
        note("no subhead found; using a placeholder. Edit the .subhead paragraph.")
    if not metric:
        metric = "[ADD YOUR NUMBER]"
        note("no metric found in proposition.md; left a visible [ADD YOUR NUMBER] marker.")

    # Privacy notice link. It ships beside the site; the founder copies it into the deploy.
    privacy_href = "privacy-notice.html"
    if not os.path.exists(os.path.join(root, ".spark", "deliverables", "data-protection", "privacy-notice.md")):
        note("privacy-notice.md not found; link left as privacy-notice.html. Do NOT launch capture without it live.")

    brand_name = state["founder"] or "Your brand"
    if logo:
        logo_block = '<img src="logo.svg" alt="%s logo">' % brand_name
    else:
        logo_block = ""
        note("no logo in brand.json; showing the name as text. Copy logo.svg into the deploy folder to add it.")

    hero = variant["hero"].format(alt=headline) if variant["hero"] else ""

    subs = {
        "{{HEADLINE}}": headline,
        "{{SUBHEAD}}": subhead,
        "{{METRIC}}": metric,
        "{{BRAND_PRIMARY}}": primary,
        "{{BRAND_SECONDARY}}": secondary,
        "{{ON_ACCENT}}": readable_on(secondary),
        "{{FONT_HEADING}}": font_heading,
        "{{FONT_BODY}}": font_body,
        "{{TAGLINE}}": tagline or "Idea to system in five days.",
        "{{BRAND_NAME}}": brand_name,
        "{{LOGO_BLOCK}}": logo_block,
        "{{HERO_MEDIA}}": hero,
        "{{FORM_FIELDS}}": build_fields(variant["fields"]),
        "{{CTA_LABEL}}": variant["cta"],
        "{{CAPTURE_KIND}}": variant["kind"],
        "{{PRIVACY_HREF}}": privacy_href,
        "{{SUPABASE_URL}}": "",
        "{{SUPABASE_ANON}}": "",
        "{{FORMSPREE_ID}}": "",
    }
    html = template
    for k, v in subs.items():
        html = html.replace(k, str(v))

    out_path = os.path.join(root, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("\nWrote %s" % out_path)
    print("CTA: %s   capture kind: %s" % (variant["cta"], variant["kind"]))
    print("Next: wire the capture store (see capture-store.md), then run a11y_check.py.")
    if metric == "[ADD YOUR NUMBER]":
        print("REMINDER: put your real number on the page before you launch.")


if __name__ == "__main__":
    main()
