#!/usr/bin/env python3
"""Export a markdown onboarding pack to PDF.

Usage:
    python3 md_to_pdf.py <input.md> <output.pdf>

Degrades gracefully. If no PDF library is installed it writes an HTML file
next to the requested output and tells you how to get a real PDF. It never
crashes on a missing optional dependency.
"""

import sys
import os
import re
import html


def read_brand(start_dir):
    """Pull brand tokens from .spark/brand/brand.json if present. Optional."""
    import json
    tokens = {"primary": "#111111", "name": ""}
    # Walk up a few levels looking for a .spark/brand/brand.json.
    d = os.path.abspath(start_dir)
    for _ in range(6):
        candidate = os.path.join(d, ".spark", "brand", "brand.json")
        if os.path.isfile(candidate):
            try:
                with open(candidate, encoding="utf-8") as f:
                    data = json.load(f)
                tokens["primary"] = (
                    data.get("colours", {}).get("primary")
                    or data.get("colors", {}).get("primary")
                    or data.get("primary")
                    or tokens["primary"]
                )
                tokens["name"] = data.get("name", tokens["name"])
            except Exception:
                pass
            break
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return tokens


def md_to_html_body(md_text):
    """A small, dependency-free markdown to HTML converter.

    Handles headings, tables, ordered and unordered lists, horizontal rules,
    bold, and paragraphs. Good enough for the onboarding pack template.
    """
    lines = md_text.splitlines()
    out = []
    i = 0
    n = len(lines)

    def inline(text):
        text = html.escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
        return text

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            level = min(level, 6)
            content = stripped[level:].strip()
            out.append(f"<h{level}>{inline(content)}</h{level}>")
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # Table: a line with pipes followed by a separator row.
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            out.append("<table><thead><tr>")
            for c in header:
                out.append(f"<th>{inline(c)}</th>")
            out.append("</tr></thead><tbody>")
            i += 2
            while i < n and "|" in lines[i].strip():
                row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>")
                for c in row:
                    out.append(f"<td>{inline(c)}</td>")
                out.append("</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        # Ordered list.
        if re.match(r"^\d+\.\s", stripped):
            out.append("<ol>")
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                item = re.sub(r"^\d+\.\s", "", lines[i].strip())
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # Unordered list.
        if re.match(r"^[-*]\s", stripped):
            out.append("<ul>")
            while i < n and re.match(r"^[-*]\s", lines[i].strip()):
                item = re.sub(r"^[-*]\s", "", lines[i].strip())
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # Paragraph.
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    return "\n".join(out)


def build_html(md_text, primary):
    body = md_to_html_body(md_text)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; color: #111;
          line-height: 1.5; max-width: 720px; margin: 40px auto; padding: 0 24px; }}
  h1 {{ color: {primary}; font-size: 26px; }}
  h2 {{ color: {primary}; font-size: 19px; margin-top: 32px; border-bottom: 2px solid {primary};
        padding-bottom: 4px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px 10px; text-align: left; font-size: 14px; }}
  th {{ background: {primary}; color: #fff; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
  a {{ color: {primary}; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 md_to_pdf.py <input.md> <output.pdf>")
        return 1

    in_path, out_path = sys.argv[1], sys.argv[2]
    if not os.path.isfile(in_path):
        print(f"Input not found: {in_path}")
        return 1

    with open(in_path, encoding="utf-8") as f:
        md_text = f.read()

    brand = read_brand(os.path.dirname(os.path.abspath(in_path)))
    html_doc = build_html(md_text, brand["primary"])

    # Try weasyprint first (best output), then fpdf2, then fall back to HTML.
    try:
        from weasyprint import HTML  # type: ignore
        HTML(string=html_doc).write_pdf(out_path)
        print(f"PDF written: {out_path}")
        return 0
    except Exception:
        pass

    try:
        from fpdf import FPDF  # type: ignore
        # fpdf cannot render HTML richly, so lay out the plain text simply.
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=11)
        for raw in md_text.splitlines():
            line = raw.rstrip()
            if line.startswith("# "):
                pdf.set_font("Helvetica", "B", 16)
                pdf.multi_cell(0, 8, line[2:])
                pdf.set_font("Helvetica", size=11)
            elif line.startswith("## "):
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 13)
                pdf.multi_cell(0, 7, line[3:])
                pdf.set_font("Helvetica", size=11)
            elif line.strip() in ("---", ""):
                pdf.ln(3)
            else:
                # Strip markdown emphasis and table pipes for the plain layout.
                clean = line.replace("**", "").replace("|", "  ")
                pdf.multi_cell(0, 6, clean)
        pdf.output(out_path)
        print(f"PDF written: {out_path}")
        return 0
    except Exception:
        pass

    # Fallback: write HTML next to the requested output.
    html_out = os.path.splitext(out_path)[0] + ".html"
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print("No PDF library found, so I wrote HTML instead:")
    print(f"  {html_out}")
    print("The HTML is fine to send. For a real PDF, install one of these and re-run:")
    print("  pip install weasyprint   (best output)")
    print("  pip install fpdf2        (lighter, plain layout)")
    print("Or open the HTML in a browser and use Print to PDF.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
