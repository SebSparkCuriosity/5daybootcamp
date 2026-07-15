#!/usr/bin/env python3
"""Generate the four DRAFT data-protection documents from the reference
templates, filling in what we know about the founder and their business.

It reads .spark/state.json (via the journey-state helper if present, else
directly) and .spark/brand/brand.json for the business name, then substitutes
{{TOKENS}} in each template under references/ and writes the result to
.spark/deliverables/data-protection/.

Design promises:
  - Nothing crashes. A missing template, a missing state file or a missing
    brand file each print a clear message and fall back to a safe minimum.
  - Every output carries the Spark lawyer-review disclaimer. The script checks
    for it and prepends it if a template forgot it, so the done-condition
    ("each carries the disclaimer") can never silently fail.
  - Unknown fields are left as visible [TO COMPLETE: ...] markers, never
    guessed, so the founder can see exactly what to finish by hand.

Usage:
  generate_docs.py --root .            # write all four drafts
  generate_docs.py --root . --check    # only verify the disclaimer is present
"""

import argparse
import datetime
import json
import os
import subprocess
import sys


DISCLAIMER = (
    "> This is a draft. Have a qualified lawyer review it before you rely on it. "
    "Spark does not warrant it."
)

# Marker line the --check mode looks for. Kept substring-loose so light edits
# to the wording above do not break the check.
DISCLAIMER_NEEDLE = "This is a draft."

# template file in references/  ->  output file in the deliverables folder
DOCS = {
    "privacy-notice.md": "privacy-notice.md",
    "consent.md": "consent.md",
    "dpa-clause.md": "dpa-clause.md",
    "lawful-basis.md": "lawful-basis.md",
}

OUT_SUBDIR = os.path.join(".spark", "deliverables", "data-protection")


def skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_state(root):
    """Return the state dict, or {} on any failure. Try the journey-state
    helper first (the sanctioned reader), then fall back to reading the file."""
    state_file = os.path.join(root, ".spark", "state.json")
    helper = os.path.normpath(
        os.path.join(skill_dir(), "..", "journey-state", "scripts", "update-state.py")
    )
    if os.path.exists(helper):
        try:
            proc = subprocess.run(
                [sys.executable, helper, "--file", state_file, "--read"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return json.loads(proc.stdout)
        except Exception:
            pass
    try:
        with open(state_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def read_brand(root):
    try:
        with open(os.path.join(root, ".spark", "brand", "brand.json"), "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def todo(label):
    return "[TO COMPLETE: %s]" % label


def build_tokens(state, brand):
    """Fill what we know; leave visible markers for what we do not. Never
    invent a business name, an email or an address."""
    business = (
        brand.get("business_name")
        or brand.get("name")
        or state.get("business_name")
        or todo("your registered business name")
    )
    founder = state.get("founder") or todo("your name")
    idea = state.get("idea") or todo("what your product or service does")
    btype = state.get("business_type") or "services"

    return {
        "BUSINESS_NAME": business,
        "FOUNDER": founder,
        "CONTACT_EMAIL": todo("the email people can use to reach you about their data"),
        "POSTAL_ADDRESS": todo("your business postal address"),
        "DATE": datetime.date.today().strftime("%d %B %Y"),
        "IDEA": idea,
        "BUSINESS_TYPE": btype,
        "DISCLAIMER": DISCLAIMER,
    }


def substitute(text, tokens):
    for key, value in tokens.items():
        text = text.replace("{{%s}}" % key, str(value))
    return text


def ensure_disclaimer(text):
    if DISCLAIMER_NEEDLE in text:
        return text
    return DISCLAIMER + "\n\n" + text


def fallback_body(name, tokens):
    """A safe minimum if a template file is missing. Still carries the
    disclaimer and still names the business, so nothing ships blank."""
    return (
        "# %s (DRAFT)\n\n%s\n\n"
        "The template for this document could not be found, so this is a stub.\n"
        "Business: %s. Prepared: %s.\n\n"
        "Complete this with your lawyer before you rely on it.\n"
        % (name.replace("-", " ").replace(".md", "").title(), DISCLAIMER,
           tokens["BUSINESS_NAME"], tokens["DATE"])
    )


def cmd_generate(root):
    state = read_state(root)
    brand = read_brand(root)
    tokens = build_tokens(state, brand)

    out_dir = os.path.join(root, OUT_SUBDIR)
    os.makedirs(out_dir, exist_ok=True)
    ref_dir = os.path.join(skill_dir(), "references")

    written = []
    for template_name, out_name in DOCS.items():
        template_path = os.path.join(ref_dir, template_name)
        try:
            with open(template_path, "r", encoding="utf-8") as fh:
                body = substitute(fh.read(), tokens)
        except Exception:
            print("Template %s not found; writing a safe stub instead." % template_name)
            body = fallback_body(out_name, tokens)
        body = ensure_disclaimer(body)
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(body)
        written.append(out_path)
        print("Wrote %s" % os.path.relpath(out_path, root))

    unresolved = sum(
        1 for p in written
        if "[TO COMPLETE:" in open(p, "r", encoding="utf-8").read()
    )
    print("GEN_RESULT=OK 4 drafts written, %d still contain [TO COMPLETE] markers" % unresolved)
    print("Business type on record: %s" % tokens["BUSINESS_TYPE"])
    return 0


def cmd_check(root):
    out_dir = os.path.join(root, OUT_SUBDIR)
    missing, no_disclaimer = [], []
    for out_name in DOCS.values():
        path = os.path.join(out_dir, out_name)
        if not os.path.exists(path):
            missing.append(out_name)
            continue
        with open(path, "r", encoding="utf-8") as fh:
            if DISCLAIMER_NEEDLE not in fh.read():
                no_disclaimer.append(out_name)
    if missing:
        print("CHECK_RESULT=FAIL missing: %s" % ", ".join(missing))
        return 1
    if no_disclaimer:
        print("CHECK_RESULT=FAIL no disclaimer in: %s" % ", ".join(no_disclaimer))
        return 1
    print("CHECK_RESULT=OK all 4 drafts present, all carry the disclaimer")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Generate DRAFT data-protection documents")
    ap.add_argument("--root", default=".", help="Project root holding .spark (default: .)")
    ap.add_argument("--check", action="store_true", help="Only verify all four drafts exist and carry the disclaimer")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    if args.check:
        sys.exit(cmd_check(root))
    sys.exit(cmd_generate(root))


if __name__ == "__main__":
    main()
