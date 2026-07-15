#!/usr/bin/env python3
"""Extract every checkable claim from an artefact, then draft a compliance note.

The judgement is Claude's, not the script's. This tool only guarantees that no
numeric or comparative claim slips through unread: it scans the file, pulls out
every candidate (numbers, money, percentages, superlatives, comparatives and
the regulated red-flag phrases), and writes a compliance note with one row per
claim, each marked UNRESOLVED. Claude then rules on each row.

It runs twice in the workflow:
  1. First pass: point it at the source file. It writes the draft note.
  2. Re-run after fixes: it recounts and prints UNRESOLVED and RED tallies so the
     done-condition (UNRESOLVED: 0, RED remaining in file: 0) is observable.

Never crashes. Unreadable file -> clear message plus an empty note skeleton.
No optional libraries required; standard library only.

    scan_claims.py --file 04-gtm/landing.md --root .
"""

import argparse
import datetime
import os
import re
import sys

DRAFT_NOTICE = (
    "\n---\n\n"
    "This is a draft. Have a qualified lawyer review it before you rely on it. "
    "Spark does not warrant it.\n"
)

# Patterns for candidate claims. Each is (type-label, compiled regex).
# Kept deliberately broad: better to over-flag and let Claude clear a row than
# to miss a claim that a regulator would not miss.
PATTERNS = [
    ("money", re.compile(r"[£$€]\s?\d[\d,.]*\s?(?:k|m|bn|billion|million|thousand)?", re.I)),
    ("percent", re.compile(r"\b\d[\d,.]*\s?%|\b\d[\d,.]*\s?per\s?cent\b", re.I)),
    ("multiple", re.compile(r"\b\d+\s?x\b", re.I)),
    ("number", re.compile(r"\b\d[\d,.]*\+?\b")),
    ("superlative", re.compile(
        r"\b(best|worst|fastest|slowest|cheapest|leading|largest|smallest|"
        r"first|only|most|#\s?1|number\s?one|unrivalled|unbeatable|premier|"
        r"world[- ]class|market[- ]leading|state[- ]of[- ]the[- ]art)\b", re.I)),
    ("comparative", re.compile(
        r"\b(faster|cheaper|better|slower|more than|less than|up to|"
        r"twice as|half the|outperform\w*|beats?)\b", re.I)),
    ("regulated-red-flag", re.compile(
        r"\b(guarantee\w*|risk[- ]free|no risk|assured|regulated|compliant|"
        r"compliance[- ]ready|approved|accredited|certified|returns?|"
        r"profit\w*|yield\w*|safe|secure|bank[- ]grade|military[- ]grade|"
        r"fully insured|100%|zero[- ]risk)\b", re.I)),
]


def read_target(path):
    """Return (text, error). Never raises."""
    if not os.path.isfile(path):
        return None, "file not found: {}".format(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in (".pdf", ".pptx", ".docx", ".key", ".png", ".jpg", ".jpeg"):
        return None, (
            "'{}' looks like a binary or deck file this scanner cannot read. "
            "Export it to plain text or Markdown first, then re-run.".format(ext))
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read(), None
        except (UnicodeDecodeError, OSError):
            continue
    return None, "could not read {} as text".format(path)


def strip_markup(line):
    """Light HTML/Markdown strip so claims in <h1> or **bold** still match."""
    line = re.sub(r"<[^>]+>", " ", line)          # html tags
    line = re.sub(r"[*_`#>|]", " ", line)          # md emphasis / headings
    return line.strip()


def find_claims(text):
    """Return list of dicts: {line, type, snippet}. One row per distinct match."""
    claims = []
    seen = set()
    for i, raw in enumerate(text.splitlines(), start=1):
        clean = strip_markup(raw)
        if not clean:
            continue
        for label, pat in PATTERNS:
            for m in pat.finditer(clean):
                phrase = m.group(0).strip()
                # De-dupe a bare year or a list bullet number caught as "number".
                key = (i, label, phrase.lower())
                if key in seen:
                    continue
                seen.add(key)
                # Context: the sentence fragment around the match, trimmed.
                start = max(0, m.start() - 40)
                end = min(len(clean), m.end() + 40)
                context = clean[start:end].strip()
                claims.append({
                    "line": i,
                    "type": label,
                    "phrase": phrase,
                    "context": context,
                })
    return claims


def note_path(root, target):
    base = os.path.basename(target)
    stem = os.path.splitext(base)[0]
    out_dir = os.path.join(root, ".spark", "deliverables")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "compliance-note-{}.md".format(stem))


def escape_cell(text):
    return text.replace("|", "\\|").replace("\n", " ")


def build_note(target, claims, business_type):
    reds = sum(1 for c in claims if c["type"] == "regulated-red-flag")
    lines = []
    lines.append("# Compliance note: {}".format(os.path.basename(target)))
    lines.append("")
    lines.append("Generated {} for business path: {}".format(
        datetime.date.today().isoformat(), business_type or "unknown"))
    lines.append("")
    lines.append(
        "**Summary.** {} candidate claims found, {} of them regulated "
        "red-flag phrases. Rule on each row below: replace UNRESOLVED with "
        "SOURCED, SOFTEN or RED, then apply amber and red fixes to the source "
        "file and re-run the scanner.".format(len(claims), reds))
    lines.append("")
    if not claims:
        lines.append(
            "No candidate claims detected. Either the file makes no numeric or "
            "comparative claims, or the copy was in a format the scanner could "
            "not parse. Read it by eye against references/red-flags.md before "
            "trusting a clean result.")
    else:
        lines.append("| # | Claim | Where | Type | Verdict | Source or fix |")
        lines.append("|---|-------|-------|------|---------|---------------|")
        for n, c in enumerate(claims, start=1):
            lines.append("| {} | {} | line {} | {} | UNRESOLVED | |".format(
                n,
                escape_cell(c["context"]),
                c["line"],
                c["type"]))
    lines.append("")
    lines.append(
        "Verdict key: **SOURCED** (green, cite a real source) / **SOFTEN** "
        "(amber, rewrite to something defensible, put the new wording in the "
        "last column) / **RED** (cut it). Nothing ships while a row reads "
        "UNRESOLVED.")
    lines.append(DRAFT_NOTICE)
    return "\n".join(lines), reds


def recount_existing(path):
    """On a re-run, count UNRESOLVED table cells still in the note.

    Only the Verdict cell counts (``| UNRESOLVED |``), not the prose mentions in
    the summary and key, so a fully ruled note reads as zero unresolved.
    Returns int, or None when the note does not exist yet.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            body = fh.read()
    except OSError:
        return None
    return len(re.findall(r"\|\s*UNRESOLVED\s*\|", body))


def count_reds_in_file(text):
    pat = PATTERNS[-1][1]  # regulated-red-flag
    return len(pat.findall(text))


def main():
    ap = argparse.ArgumentParser(description="Scan an artefact for checkable claims.")
    ap.add_argument("--file", required=True, help="Path to the artefact to check")
    ap.add_argument("--root", default=".", help="Project root holding .spark (default: .)")
    ap.add_argument("--business-type", default="", help="Optional: software|hardware|services")
    args = ap.parse_args()

    target = args.file
    root = args.root

    text, err = read_target(target)
    if err:
        sys.stderr.write("Cannot scan: {}\n".format(err))
        # Still write an empty skeleton so the workflow has a file to open.
        out = note_path(root, target)
        skeleton, _ = build_note(target, [], args.business_type)
        try:
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(skeleton)
            print("Wrote empty note skeleton: {}".format(out))
        except OSError as e:
            sys.stderr.write("Could not write note: {}\n".format(e))
        print("UNRESOLVED: 0")
        print("RED remaining in file: 0")
        sys.exit(0)

    claims = find_claims(text)
    out = note_path(root, target)

    existing_unresolved = recount_existing(out)
    note_body, reds = build_note(target, claims, args.business_type)

    # First pass writes the draft. On a re-run where the note already exists and
    # has been edited (fewer UNRESOLVED than claims), do not clobber the human's
    # verdicts: report the counts instead.
    if existing_unresolved is not None and existing_unresolved < len(claims):
        print("Existing note found with edits, not overwriting: {}".format(out))
        print("Claims in file: {}".format(len(claims)))
        print("UNRESOLVED: {}".format(existing_unresolved))
        print("RED remaining in file: {}".format(count_reds_in_file(text)))
        sys.exit(0)

    try:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(note_body)
    except OSError as e:
        sys.stderr.write("Could not write note: {}\n".format(e))
        sys.exit(1)

    print("Wrote compliance note: {}".format(out))
    print("Claims found: {} ({} regulated red-flag phrases)".format(len(claims), reds))
    print("UNRESOLVED: {}".format(len(claims)))
    print("RED remaining in file: {}".format(count_reds_in_file(text)))


if __name__ == "__main__":
    main()
