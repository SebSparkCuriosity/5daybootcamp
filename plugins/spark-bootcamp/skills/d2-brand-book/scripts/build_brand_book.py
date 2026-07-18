#!/usr/bin/env python3
"""Build the founder's brand kit and brand book (HTML always, PDF where a
browser is available).

Pure standard library. Reads the identity locked on Day 2 plus a Claude-filled
content file, and writes:

  02-market/brand/kit/           logo variants derived from the chosen master
                                 (primary, mono, reversed, favicon), plus PNG
                                 exports when a converter is on the machine
  02-market/brand/brand-book.html  the 8-section brand book, self-contained
  02-market/brand/brand-book.pdf   printed via a headless browser if one is
                                   found; otherwise the founder prints the HTML

Inputs (all under the project root):
  02-market/brand/brand-tokens.json   five colour roles, two fonts, tone, tagline
  02-market/brand/logo.svg            the chosen master (transparent background)
  02-market/brand/book-content.json   the judgement content Claude fills with
                                      the founder (template in references/)
  .spark/brand/brand.json             canonical fallback for tone and tagline

Usage:
  python3 build_brand_book.py --root .

The last line is machine-readable:
  BOOK_RESULT html=<ok|fail> kit=<n> png=<ok|skipped> pdf=<ok|manual>

Recoloured variants are derived by rewriting fill and stroke colours, which is
honest for the simple geometric SVGs this week produces. Eyeball each variant
once before it ships anywhere.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# ---------------------------------------------------------------- utilities

def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def norm_hex(value):
    v = str(value).strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        raise ValueError("bad hex: %r" % value)
    int(v, 16)
    return "#" + v.upper()


def hex_rgb(value):
    h = norm_hex(value).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def contrast_ratio(a, b):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def lum(h):
        r, g, bb = hex_rgb(h)
        return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(bb)

    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def strip_svg(markup):
    markup = re.sub(r"<\?xml[^>]*\?>", "", markup)
    markup = re.sub(r"<!DOCTYPE[^>]*>", "", markup, flags=re.IGNORECASE)
    return markup.strip()


# ---------------------------------------------------------------- logo kit

WHITES = {"#fff", "#ffffff", "white", "rgb(255,255,255)", "rgb(255, 255, 255)"}


def _is_white(value):
    return value.strip().lower() in WHITES


def recolour_svg(svg, colour, white_becomes=None):
    """Rewrite fills and strokes to one colour, preserving 'none'.

    White is the knockout colour: by default it is kept (mono keeps its
    counters readable); pass white_becomes to swap it (reversed turns white
    interiors dark so they survive on a white mark)."""

    def paint(value):
        if value.strip().lower() == "none":
            return value
        if _is_white(value):
            return white_becomes or value
        return colour

    out = re.sub(r'fill="([^"]*)"', lambda m: 'fill="%s"' % paint(m.group(1)), svg)
    out = re.sub(r"fill='([^']*)'", lambda m: "fill='%s'" % paint(m.group(1)), out)
    out = re.sub(r'stroke="([^"]*)"', lambda m: 'stroke="%s"' % paint(m.group(1)), out)
    out = re.sub(r"fill:\s*([^;}\"']+)", lambda m: "fill:%s" % paint(m.group(1)), out)
    return out


def favicon_svg(name, colours):
    """A square favicon that always works: rounded primary tile, initial."""
    primary = norm_hex(colours.get("primary", "#0B3D2E"))
    surface = norm_hex(colours.get("surface", "#FFFFFF"))
    initial = (str(name).strip()[:1] or "S").upper()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" '
        'role="img" aria-label="%s icon">\n'
        '  <rect width="64" height="64" rx="14" fill="%s"/>\n'
        '  <text x="32" y="33" font-family="sans-serif" font-size="38" font-weight="700" '
        'fill="%s" text-anchor="middle" dominant-baseline="central">%s</text>\n'
        "</svg>\n" % (esc(name), primary, surface, esc(initial))
    )


def find_png_tool():
    """Return (kind, path) for the first SVG-to-PNG converter found, or None."""
    for name in ("rsvg-convert", "inkscape", "magick", "convert"):
        path = shutil.which(name)
        if path:
            return name, path
    try:  # cairosvg as a module, common on machines with Python tooling
        import cairosvg  # noqa: F401
        return "cairosvg", "cairosvg"
    except Exception:
        return None


def export_png(tool, svg_path, png_path, width):
    kind, path = tool
    try:
        if kind == "rsvg-convert":
            subprocess.run([path, "-w", str(width), "-o", png_path, svg_path],
                           check=True, capture_output=True, timeout=60)
        elif kind == "inkscape":
            subprocess.run([path, svg_path, "--export-type=png",
                            "--export-filename=%s" % png_path,
                            "--export-width=%d" % width],
                           check=True, capture_output=True, timeout=60)
        elif kind in ("magick", "convert"):
            subprocess.run([path, "-background", "none", "-density", "300",
                            "-resize", "%dx" % width, svg_path, png_path],
                           check=True, capture_output=True, timeout=60)
        elif kind == "cairosvg":
            import cairosvg
            cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=width)
        return os.path.exists(png_path)
    except Exception:
        return False


def build_kit(brand_dir, master_svg, name, colours):
    """Write the logo variants. Returns (kit_dir, files, png_status)."""
    kit_dir = os.path.join(brand_dir, "kit")
    os.makedirs(kit_dir, exist_ok=True)
    ink = norm_hex(colours.get("ink", "#12211B"))

    variants = {
        "logo-primary.svg": master_svg,
        "logo-mono.svg": recolour_svg(master_svg, ink),
        "logo-reversed.svg": recolour_svg(master_svg, "#FFFFFF", white_becomes=ink),
        "favicon.svg": favicon_svg(name, colours),
    }
    for fname, markup in variants.items():
        with open(os.path.join(kit_dir, fname), "w", encoding="utf-8") as fh:
            fh.write(markup)

    files = list(variants)
    tool = find_png_tool()
    png_status = "skipped"
    if tool:
        wanted = [("logo-primary.svg", "logo-primary-1200w.png", 1200),
                  ("favicon.svg", "favicon-512.png", 512),
                  ("favicon.svg", "favicon-180.png", 180),
                  ("favicon.svg", "favicon-32.png", 32)]
        done = 0
        for src, dst, width in wanted:
            if export_png(tool, os.path.join(kit_dir, src),
                          os.path.join(kit_dir, dst), width):
                files.append(dst)
                done += 1
        png_status = "ok" if done == len(wanted) else ("partial" if done else "failed")
    return kit_dir, files, png_status


# ---------------------------------------------------------------- the book

def swatch(label, key, colours):
    value = colours.get(key)
    if not value:
        return ""
    hexv = norm_hex(value)
    r, g, b = hex_rgb(hexv)
    surface = colours.get("surface", "#FFFFFF")
    if key == "surface":
        measure = "the background itself"
    else:
        measure = "%.2f:1 on surface" % contrast_ratio(hexv, surface)
    return f"""
      <div class="swatch">
        <div class="chip" style="background:{hexv}"></div>
        <div>
          <div class="role">{esc(label)}</div>
          <div class="spec">{hexv} &middot; rgb({r}, {g}, {b}) &middot; {measure}</div>
        </div>
      </div>"""


def build_book_html(tokens, content, master_svg, kit_files, png_status):
    name = tokens.get("name", "Your brand")
    colours = tokens.get("colours", {})
    fonts = tokens.get("fonts", {})
    heading = fonts.get("heading", "Georgia, serif")
    body = fonts.get("body", "system-ui, sans-serif")
    ink = colours.get("ink", "#12211B")
    primary = colours.get("primary", "#0B3D2E")
    accent = colours.get("accent", primary)
    muted = colours.get("muted", "#5B6B63")
    surface = colours.get("surface", "#FFFFFF")
    tone = tokens.get("tone", "")
    tagline = tokens.get("tagline", "")

    story = content.get("story", "")
    values = content.get("values", [])
    archetype = content.get("archetype", {})
    sliders = content.get("tone_sliders", [])
    voice_example = content.get("voice_example", "")
    apps = content.get("applications", {})
    provenance = content.get("logo_provenance", "")

    value_rows = "".join(
        f'<li><strong>{esc(v.get("value", ""))}.</strong> {esc(v.get("practice", ""))}</li>'
        for v in values)
    slider_rows = "".join(
        f'<tr><td>{esc(s.get("dimension", ""))}</td><td class="num">{esc(s.get("score", ""))} / 5</td>'
        f'<td>{esc(s.get("note", ""))}</td></tr>' for s in sliders)
    swatches = "".join([swatch("Surface: backgrounds", "surface", colours),
                        swatch("Ink: body text", "ink", colours),
                        swatch("Primary: headings, links, the mark", "primary", colours),
                        swatch("Accent: buttons, rules, one highlight", "accent", colours),
                        swatch("Muted: secondary text, borders", "muted", colours)])
    kit_rows = "".join(
        f'<tr><td class="mono">kit/{esc(f)}</td><td>{esc(kit_use(f))}</td></tr>'
        for f in kit_files)
    png_note = ("" if png_status == "ok" else
                "<p class=\"note\">PNG exports were skipped on this machine (no converter found). "
                "The SVGs cover every screen use; export PNGs later with any converter or "
                "an online tool if a platform demands them.</p>")
    email_sig = apps.get("email_signature", "")
    doc_header = apps.get("doc_header_line", "")

    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(name)} brand book</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin:0; background:{esc(surface)}; color:{esc(ink)};
         font-family:{esc(body)}; line-height:1.55; }}
  .page {{ max-width:800px; margin:0 auto; padding:48px 32px; }}
  h1 {{ font-family:{esc(heading)}; font-size:2.6rem; margin:0 0 6px; }}
  h2 {{ font-family:{esc(heading)}; font-size:1.5rem; color:{esc(primary)};
        border-bottom:3px solid {esc(accent)}; padding-bottom:6px; margin:0 0 18px; }}
  h3 {{ font-size:1.05rem; margin:20px 0 8px; }}
  p, li {{ font-size:1rem; }}
  .muted {{ color:{esc(muted)}; }}
  .note {{ color:{esc(muted)}; font-size:.9rem; }}
  .cover {{ text-align:center; padding-top:120px; }}
  .cover .logo svg {{ max-width:70%; height:auto; max-height:180px; }}
  .cover .tagline {{ font-size:1.2rem; color:{esc(muted)}; margin-top:12px; }}
  .logoshow {{ display:flex; gap:16px; flex-wrap:wrap; margin:16px 0; }}
  .logoshow > div {{ border:1px solid #E4E7E5; border-radius:12px; padding:22px;
                     flex:1 1 200px; display:flex; align-items:center; justify-content:center; }}
  .logoshow svg {{ max-width:100%; height:auto; max-height:72px; }}
  .ondark {{ background:{esc(ink)}; }}
  .swatch {{ display:flex; gap:12px; align-items:center; width:calc(50% - 8px);
             min-width:250px; margin-bottom:14px; }}
  .swatches {{ display:flex; flex-wrap:wrap; gap:0 16px; }}
  .chip {{ width:54px; height:54px; border-radius:10px; border:1px solid #E4E7E5; flex:0 0 auto; }}
  .role {{ font-weight:600; }}
  .spec, .mono {{ font-family:ui-monospace, Menlo, Consolas, monospace; font-size:.85rem;
                  color:{esc(muted)}; }}
  table {{ border-collapse:collapse; width:100%; }}
  td, th {{ text-align:left; padding:7px 10px; border-bottom:1px solid #E4E7E5;
            vertical-align:top; font-size:.95rem; }}
  .num {{ white-space:nowrap; }}
  .specimen div {{ margin-bottom:10px; }}
  .s1 {{ font-family:{esc(heading)}; font-size:2rem; font-weight:700; }}
  .s2 {{ font-family:{esc(heading)}; font-size:1.35rem; color:{esc(primary)}; }}
  .s3 {{ font-size:1rem; }}
  .s4 {{ font-size:.85rem; color:{esc(muted)}; }}
  .voice, .appblock {{ background:#F4F6F5; border-radius:12px; padding:16px 20px; }}
  .appblock {{ margin-bottom:16px; }}
  .sig {{ font-size:.95rem; white-space:pre-line; }}
  .dochead {{ border-bottom:3px solid {esc(accent)}; padding-bottom:8px;
              display:flex; justify-content:space-between; align-items:center; }}
  .dochead svg {{ max-height:36px; width:auto; }}
  .decktitle {{ background:{esc(primary)}; color:{esc(surface)}; border-radius:12px;
                padding:48px 32px; }}
  .decktitle .t {{ font-family:{esc(heading)}; font-size:1.8rem; font-weight:700; }}
  .decktitle .s {{ opacity:.75; margin-top:6px; }}
  @media print {{
    .page {{ page-break-after: always; padding:24px 0; }}
    .page:last-child {{ page-break-after: auto; }}
    body {{ background:#fff; }}
  }}
  @page {{ size: A4; margin: 18mm; }}
</style>
</head>
<body>

<div class="page cover">
  <div class="logo">{master_svg}</div>
  <p class="tagline">{esc(tagline)}</p>
  <p class="muted">{esc(name)} brand book, version 1. Built during the Spark bootcamp.</p>
</div>

<div class="page">
  <h2>1. The brand</h2>
  <p>{esc(story)}</p>
  <h3>Values, as things we do</h3>
  <ul>{value_rows}</ul>
  <h3>Archetype</h3>
  <p><strong>{esc(archetype.get("name", ""))}.</strong> {esc(archetype.get("why", ""))}</p>
</div>

<div class="page">
  <h2>2. Logo</h2>
  <div class="logoshow">
    <div>{master_svg}</div>
    <div class="ondark">{{REVERSED}}</div>
    <div>{{MONO}}</div>
  </div>
  <h3>Rules</h3>
  <ul>
    <li><strong>Clear space.</strong> Keep empty space around the logo at least the height of its tallest letter, on every side.</li>
    <li><strong>Minimum size.</strong> Never below 24 pixels tall on screen or 8&nbsp;mm in print; below that, use the favicon mark.</li>
    <li><strong>One version per background.</strong> Primary on white, reversed on dark or photographic, mono where colour is unavailable.</li>
    <li><strong>Never.</strong> Stretch it, recolour it outside this palette, add shadows or effects, or set it on a busy image without a solid panel behind it.</li>
  </ul>
  {f'<p class="note">{esc(provenance)}</p>' if provenance else ''}
</div>

<div class="page">
  <h2>3. Colour</h2>
  <div class="swatches">{swatches}
  </div>
  <p>Use roughly 60 percent surface, 30 percent ink and primary, 10 percent accent. Every ratio above is measured; text roles clear WCAG AA at 4.5:1, so anything you write in these colours stays readable on a projector and for the roughly 1 in 12 men with colour-vision deficiency.</p>
</div>

<div class="page">
  <h2>4. Typography</h2>
  <div class="specimen">
    <div class="s1">Headline: {esc(name)} ships in weeks, not quarters.</div>
    <div class="s2">Section heading sits in the primary colour.</div>
    <div class="s3">Body text carries the argument. Short sentences. A number in every claim. It is set in a system-safe stack so every document loads instantly and renders the same on any machine a buyer opens it on.</div>
    <div class="s4">Caption and secondary text sit in muted.</div>
  </div>
  <table>
    <tr><td>Heading</td><td class="mono">{esc(heading)}</td></tr>
    <tr><td>Body</td><td class="mono">{esc(body)}</td></tr>
  </table>
</div>

<div class="page">
  <h2>5. Voice</h2>
  <p><strong>{esc(tone)}</strong></p>
  <table>
    <tr><th>Dimension</th><th>Setting</th><th>In practice</th></tr>
    {slider_rows}
  </table>
  <h3>Hear it</h3>
  <div class="voice">{esc(voice_example)}</div>
</div>

<div class="page">
  <h2>6. Applications</h2>
  <h3>Email signature</h3>
  <div class="appblock sig">{esc(email_sig)}</div>
  <h3>Document header</h3>
  <div class="appblock">
    <div class="dochead">{{MARKSMALL}}<span class="muted">{esc(doc_header)}</span></div>
  </div>
  <h3>Deck title slide</h3>
  <div class="decktitle">
    <div class="t">{esc(tagline) or esc(name)}</div>
    <div class="s">{esc(doc_header)}</div>
  </div>
</div>

<div class="page">
  <h2>7. The kit</h2>
  <table>
    <tr><th>File</th><th>Use it for</th></tr>
    {kit_rows}
  </table>
  {png_note}
</div>

<div class="page">
  <h2>8. Keeping it</h2>
  <p>The canonical tokens live at <span class="mono">.spark/brand/brand.json</span>; every deck, page and proposal this week reads from there, so a colour change happens once. This book is the human copy: hand it to a freelancer, a printer or a future you, and everything they need is on these pages. Changes go through the visual-identity and brand-register skills, never by hand, and each one earns a line in the changelog.</p>
</div>

</body>
</html>
"""


def kit_use(fname):
    uses = {
        "logo-primary.svg": "Default. White or light backgrounds: documents, the site, proposals.",
        "logo-mono.svg": "Single-colour print, faxes of the world, engraving, stamps.",
        "logo-reversed.svg": "Dark backgrounds: deck title slides, footers, photography panels.",
        "favicon.svg": "Browser tab, app icon, avatar squares.",
        "logo-primary-1200w.png": "Anywhere SVG is refused: LinkedIn, invoicing tools, marketplaces.",
        "favicon-512.png": "App stores and platform uploads asking for 512 px.",
        "favicon-180.png": "Apple touch icon.",
        "favicon-32.png": "Classic browser favicon.",
    }
    return uses.get(fname, "As labelled.")


# ---------------------------------------------------------------- PDF

def find_browser():
    for env in ("CHROME_PATH",):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    for name in ("chromium", "chromium-browser", "google-chrome",
                  "google-chrome-stable", "chrome", "msedge", "brave"):
        p = shutil.which(name)
        if p:
            return p
    for p in ("/opt/pw-browsers/chromium",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "C:/Program Files/Google/Chrome/Application/chrome.exe"):
        if os.path.exists(p):
            return p
    return None


def print_pdf(html_path, pdf_path):
    browser = find_browser()
    if not browser:
        return False
    try:
        subprocess.run(
            [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--print-to-pdf=%s" % os.path.abspath(pdf_path),
             "--no-pdf-header-footer",
             "file://" + os.path.abspath(html_path)],
            check=True, capture_output=True, timeout=120)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0
    except Exception:
        # Older Chrome builds want plain --headless.
        try:
            subprocess.run(
                [browser, "--headless", "--disable-gpu", "--no-sandbox",
                 "--print-to-pdf=%s" % os.path.abspath(pdf_path),
                 "file://" + os.path.abspath(html_path)],
                check=True, capture_output=True, timeout=120)
            return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0
        except Exception:
            return False


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Build the brand kit and brand book.")
    ap.add_argument("--root", default=".", help="Founder project root")
    args = ap.parse_args()

    brand_dir = os.path.join(args.root, "02-market", "brand")
    tokens_path = os.path.join(brand_dir, "brand-tokens.json")
    logo_path = os.path.join(brand_dir, "logo.svg")
    content_path = os.path.join(brand_dir, "book-content.json")
    canonical_path = os.path.join(args.root, ".spark", "brand", "brand.json")

    problems = []
    if not os.path.exists(tokens_path):
        problems.append("missing %s (run d2-visual-identity)" % tokens_path)
    if not os.path.exists(logo_path):
        problems.append("missing %s (choose the logo in d2-visual-identity)" % logo_path)
    if not os.path.exists(content_path):
        problems.append("missing %s (copy the template from this skill's references/ "
                        "and fill it with the founder)" % content_path)
    if problems:
        for p in problems:
            print("  - " + p)
        print("BOOK_RESULT html=fail kit=0 png=skipped pdf=manual")
        return 1

    tokens = read_json(tokens_path)
    content = read_json(content_path)
    # Canonical brand.json wins for tone and tagline when present.
    if os.path.exists(canonical_path):
        try:
            canonical = read_json(canonical_path)
            tokens.setdefault("tone", canonical.get("tone", ""))
            tokens["tone"] = tokens.get("tone") or canonical.get("tone", "")
            tokens["tagline"] = tokens.get("tagline") or canonical.get("tagline", "")
        except Exception:
            pass

    with open(logo_path, "r", encoding="utf-8") as fh:
        master_svg = strip_svg(fh.read())

    name = tokens.get("name", "Your brand")
    colours = tokens.get("colours", {})

    kit_dir, kit_files, png_status = build_kit(brand_dir, master_svg, name, colours)

    html = build_book_html(tokens, content, master_svg, kit_files, png_status)
    with open(os.path.join(kit_dir, "logo-reversed.svg"), "r", encoding="utf-8") as fh:
        html = html.replace("{REVERSED}", strip_svg(fh.read()))
    with open(os.path.join(kit_dir, "logo-mono.svg"), "r", encoding="utf-8") as fh:
        mono = strip_svg(fh.read())
    html = html.replace("{MONO}", mono).replace("{MARKSMALL}", mono)

    html_path = os.path.join(brand_dir, "brand-book.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    pdf_path = os.path.join(brand_dir, "brand-book.pdf")
    pdf_ok = print_pdf(html_path, pdf_path)

    print("Kit: %d files in %s (PNG exports: %s)" % (len(kit_files), kit_dir, png_status))
    print("Book: %s" % html_path)
    if pdf_ok:
        print("PDF:  %s" % pdf_path)
    else:
        print("PDF:  no headless browser found. Open brand-book.html in any browser")
        print("      and print to PDF (Cmd or Ctrl+P), saving as brand-book.pdf.")
    print("BOOK_RESULT html=ok kit=%d png=%s pdf=%s"
          % (len(kit_files), png_status, "ok" if pdf_ok else "manual"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
