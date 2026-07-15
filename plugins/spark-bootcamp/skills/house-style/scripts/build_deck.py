#!/usr/bin/env python3
"""Spark deck builder. One content file plus brand tokens, one branded deck out.

Reads a YAML content file and .spark/brand/brand.json, then emits a slide deck
that looks like the founder's company. If python-pptx is installed you get a
.pptx. If it is not, you get a self-contained reveal.js HTML deck instead, and
the install line printed once, so the founder is never blocked.

Usage:
    build_deck.py --content deck.yaml --brand .spark/brand/brand.json --out 04-gtm/sales-deck

    # --out has no extension: the builder adds .pptx or .html depending on what
    # is available. Force a format with --format pptx|html if you want to.

Content YAML shape (also in references/deck-content.example.yaml):

    title: Acme, idea into system
    subtitle: A fixed-price pilot in five weeks
    slides:
      - heading: The problem
        bullets:
          - Trust admins rekey the same data four times
          - Every rekey is an audit risk
        notes: Speaker note, optional
      - heading: What we built
        body: A single paragraph instead of bullets, optional

brand.json shape this reads (every key optional, safe defaults if absent):

    {
      "name": "Acme Ltd",
      "colours": { "primary": "#0B5FEF", "accent": "#00C2A8", "ink": "#12141A" },
      "fonts":   { "heading": "Arial", "body": "Calibri" },
      "contact": { "email": "hi@acme.je", "url": "acme.je" }
    }

American spelling "colors" is accepted as an alias for "colours". Fonts default
to system-safe Arial and Calibri so a deck opens the same everywhere.

The script never crashes on missing input: a missing brand file falls back to
Spark defaults and says so; a missing content file exits 2 with a clear message.
"""

import argparse
import json
import os
import sys
import html


# ----- Spark safe defaults -------------------------------------------------

DEFAULTS = {
    "name": "Your Company",
    "primary": "#0B5FEF",
    "accent": "#00C2A8",
    "ink": "#12141A",
    "paper": "#FFFFFF",
    "font_heading": "Arial",
    "font_body": "Calibri",
    "contact_email": "",
    "contact_url": "",
}


def log(msg):
    print("[build_deck] " + msg, file=sys.stderr)


def load_brand(path):
    """Read brand.json into a flat token dict. Missing or broken file is fine."""
    tokens = dict(DEFAULTS)
    if not path or not os.path.exists(path):
        log("no brand.json found, using Spark defaults (primary %s)." % DEFAULTS["primary"])
        return tokens
    try:
        with open(path, "r", encoding="utf-8") as fh:
            b = json.load(fh)
    except Exception as e:
        log("brand.json could not be read (%s), using Spark defaults." % e)
        return tokens

    tokens["name"] = b.get("name") or tokens["name"]
    colours = b.get("colours") or b.get("colors") or {}
    tokens["primary"] = colours.get("primary") or tokens["primary"]
    tokens["accent"] = colours.get("accent") or tokens["accent"]
    tokens["ink"] = colours.get("ink") or tokens["ink"]
    tokens["paper"] = colours.get("paper") or tokens["paper"]
    fonts = b.get("fonts") or {}
    tokens["font_heading"] = fonts.get("heading") or tokens["font_heading"]
    tokens["font_body"] = fonts.get("body") or tokens["font_body"]
    contact = b.get("contact") or {}
    tokens["contact_email"] = contact.get("email") or ""
    tokens["contact_url"] = contact.get("url") or ""
    return tokens


def load_content(path):
    """Read the deck content. YAML if PyYAML is present, else a tiny fallback."""
    if not path or not os.path.exists(path):
        log("content file not found: %s" % path)
        sys.exit(2)
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(raw)
    except ImportError:
        log("PyYAML not installed, using the built-in minimal parser. "
            "For full YAML support: pip install pyyaml")
        data = _mini_yaml(raw)
    except Exception as e:
        log("content YAML could not be parsed: %s" % e)
        sys.exit(2)
    if not isinstance(data, dict) or "slides" not in data:
        log("content needs a top-level 'slides:' list. Nothing to build.")
        sys.exit(2)
    return data


def _mini_yaml(raw):
    """A deliberately small YAML reader for the deck shape only.

    Handles: top-level title/subtitle scalars, a slides list of mappings with
    heading/body/notes scalars and a bullets list. Enough to run when PyYAML is
    absent. Not a general YAML parser.
    """
    doc = {"slides": []}
    cur = None
    in_bullets = False
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0 and s.endswith(":") is False and ":" in s and not s.startswith("- "):
            key, _, val = s.partition(":")
            doc[key.strip()] = val.strip().strip('"').strip("'")
            in_bullets = False
        elif s.startswith("- heading:") or (s.startswith("-") and cur is None):
            cur = {"bullets": []}
            doc["slides"].append(cur)
            in_bullets = False
            if ":" in s:
                _, _, val = s.partition("heading:")
                cur["heading"] = val.strip().strip('"').strip("'")
        elif s.startswith("- ") and in_bullets and cur is not None:
            cur["bullets"].append(s[2:].strip().strip('"').strip("'"))
        elif cur is not None and s.startswith("bullets:"):
            in_bullets = True
        elif cur is not None and ":" in s:
            key, _, val = s.partition(":")
            cur[key.strip()] = val.strip().strip('"').strip("'")
            in_bullets = False
    return doc


# ----- PPTX path -----------------------------------------------------------

def build_pptx(content, brand, out_path):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    def rgb(hexstr):
        h = hexstr.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    primary = rgb(brand["primary"])
    ink = rgb(brand["ink"])
    accent = rgb(brand["accent"])

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    def title_slide():
        s = prs.slides.add_slide(blank)
        box = s.shapes.add_textbox(Inches(0.9), Inches(2.6), Inches(11.5), Inches(2.5))
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = content.get("title", brand["name"])
        r.font.size = Pt(44); r.font.bold = True
        r.font.name = brand["font_heading"]; r.font.color.rgb = ink
        if content.get("subtitle"):
            p2 = tf.add_paragraph()
            r2 = p2.add_run(); r2.text = content["subtitle"]
            r2.font.size = Pt(22); r2.font.name = brand["font_body"]
            r2.font.color.rgb = primary
        # accent bar
        bar = s.shapes.add_shape(1, Inches(0.9), Inches(2.35), Inches(2.2), Inches(0.12))
        bar.fill.solid(); bar.fill.fore_color.rgb = accent; bar.line.fill.background()

    def content_slide(sl):
        s = prs.slides.add_slide(blank)
        head = s.shapes.add_textbox(Inches(0.9), Inches(0.6), Inches(11.5), Inches(1.1))
        hp = head.text_frame.paragraphs[0]
        hr = hp.add_run(); hr.text = sl.get("heading", "")
        hr.font.size = Pt(32); hr.font.bold = True
        hr.font.name = brand["font_heading"]; hr.font.color.rgb = primary
        body = s.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(11.5), Inches(4.8))
        tf = body.text_frame; tf.word_wrap = True
        bullets = sl.get("bullets") or []
        if bullets:
            for i, b in enumerate(bullets):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                r = p.add_run(); r.text = "•  " + str(b)
                r.font.size = Pt(20); r.font.name = brand["font_body"]
                r.font.color.rgb = ink
                p.space_after = Pt(10)
        elif sl.get("body"):
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = str(sl["body"])
            r.font.size = Pt(20); r.font.name = brand["font_body"]; r.font.color.rgb = ink
        if sl.get("notes"):
            s.notes_slide.notes_text_frame.text = str(sl["notes"])

    title_slide()
    for sl in content["slides"]:
        content_slide(sl)

    prs.save(out_path)
    return len(content["slides"]) + 1  # + title slide


# ----- reveal.js HTML fallback ---------------------------------------------

def build_reveal(content, brand, out_path):
    def esc(x):
        return html.escape(str(x))

    slides_html = []
    title = esc(content.get("title", brand["name"]))
    subtitle = esc(content.get("subtitle", ""))
    slides_html.append(
        '<section><h1>%s</h1>%s</section>' % (
            title,
            ('<p class="sub">%s</p>' % subtitle) if subtitle else "",
        )
    )
    for sl in content["slides"]:
        heading = esc(sl.get("heading", ""))
        inner = ""
        bullets = sl.get("bullets") or []
        if bullets:
            inner = "<ul>" + "".join("<li>%s</li>" % esc(b) for b in bullets) + "</ul>"
        elif sl.get("body"):
            inner = "<p>%s</p>" % esc(sl["body"])
        notes = ('<aside class="notes">%s</aside>' % esc(sl["notes"])) if sl.get("notes") else ""
        slides_html.append("<section><h2>%s</h2>%s%s</section>" % (heading, inner, notes))

    # reveal.js is inlined as a minimal self-contained slideshow so the file
    # opens offline with no network. It is not the full library: it does arrow
    # and space navigation, which is all a founder needs to present.
    page = """<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --primary:{primary}; --accent:{accent}; --ink:{ink}; --paper:{paper};
           --fh:{fh}; --fb:{fb}; }}
  html,body {{ margin:0; height:100%; background:#0b0d11; color:var(--ink);
               font-family:var(--fb),Arial,sans-serif; }}
  .deck {{ position:fixed; inset:0; }}
  section {{ display:none; position:absolute; inset:0;
             padding:6vh 8vw; box-sizing:border-box; background:var(--paper);
             flex-direction:column; justify-content:center; }}
  section.active {{ display:flex; }}
  h1 {{ font-family:var(--fh),Arial,sans-serif; color:var(--ink);
        font-size:clamp(2rem,6vw,4rem); margin:0 0 .4em; }}
  h2 {{ font-family:var(--fh),Arial,sans-serif; color:var(--primary);
        font-size:clamp(1.6rem,4.5vw,2.8rem); margin:0 0 .6em; }}
  h1::after {{ content:""; display:block; width:3rem; height:.35rem;
        background:var(--accent); margin-top:.5rem; border-radius:3px; }}
  .sub {{ color:var(--primary); font-size:clamp(1.1rem,2.5vw,1.6rem); }}
  ul {{ font-size:clamp(1.1rem,2.6vw,1.7rem); line-height:1.6; max-width:48rem; }}
  li {{ margin:.35em 0; }}
  p {{ font-size:clamp(1.1rem,2.6vw,1.7rem); max-width:48rem; line-height:1.5; }}
  .notes {{ display:none; }}
  .hud {{ position:fixed; bottom:1rem; right:1.25rem; color:var(--primary);
          font-family:var(--fb),Arial; font-size:.9rem; opacity:.7; }}
  @media (prefers-color-scheme: dark) {{
    section {{ background:#0e1014; }} :root {{ --ink:#EDF0F4; --paper:#0e1014; }}
  }}
</style></head>
<body>
<div class="deck">
{slides}
</div>
<div class="hud"><span id="n">1</span> / {count}</div>
<script>
  var s = document.querySelectorAll('.deck > section');
  var i = 0;
  function show(k) {{
    i = Math.max(0, Math.min(s.length - 1, k));
    s.forEach(function(el, idx) {{ el.classList.toggle('active', idx === i); }});
    document.getElementById('n').textContent = (i + 1);
  }}
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') show(i + 1);
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') show(i - 1);
    if (e.key === 'Home') show(0);
    if (e.key === 'End') show(s.length - 1);
  }});
  document.addEventListener('click', function() {{ show(i + 1); }});
  show(0);
</script>
</body></html>
""".format(
        title=title,
        primary=brand["primary"], accent=brand["accent"],
        ink=brand["ink"], paper=brand["paper"],
        fh=brand["font_heading"], fb=brand["font_body"],
        slides="\n".join(slides_html),
        count=len(content["slides"]) + 1,
    )
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return len(content["slides"]) + 1


# ----- main ----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Build a branded Spark deck.")
    ap.add_argument("--content", required=True, help="Path to the deck YAML content file.")
    ap.add_argument("--brand", default=".spark/brand/brand.json", help="Path to brand.json.")
    ap.add_argument("--out", required=True, help="Output path, with or without extension.")
    ap.add_argument("--format", choices=["pptx", "html", "auto"], default="auto",
                    help="Force a format. Default auto: pptx if python-pptx is present, else html.")
    args = ap.parse_args()

    brand = load_brand(args.brand)
    content = load_content(args.content)

    base, ext = os.path.splitext(args.out)
    want = args.format
    if want == "auto":
        ext_l = ext.lower()
        if ext_l == ".pptx":
            want = "pptx"
        elif ext_l in (".html", ".htm"):
            want = "html"
        else:
            want = "pptx"  # aspire to pptx, fall back below if missing

    # Try pptx, fall back to reveal.js html if the library is missing.
    if want == "pptx":
        try:
            import pptx  # noqa: F401
        except ImportError:
            log("python-pptx is not installed. Building a reveal.js HTML deck instead.")
            log("For a .pptx next time: pip install python-pptx")
            want = "html"

    if want == "pptx":
        out_path = base + ".pptx"
        try:
            n = build_pptx(content, brand, out_path)
        except Exception as e:
            log("pptx build failed (%s). Falling back to HTML deck." % e)
            out_path = base + ".html"
            n = build_reveal(content, brand, out_path)
    else:
        out_path = base + ".html"
        n = build_reveal(content, brand, out_path)

    print(out_path)
    log("wrote %s (%d slides) for %s." % (out_path, n, brand["name"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
