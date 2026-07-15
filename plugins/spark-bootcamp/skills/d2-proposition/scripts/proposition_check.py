#!/usr/bin/env python3
"""Check a proposition write-up against the Day 2 done conditions.

This does not judge whether the proposition is good. It checks the three
things Spark insists on, so nothing fuzzy sneaks through to Day 3:

  1. At least three jobs, three pains and three gains, each tagged to a
     numbered quote from discovery, like "(quote: Q3)".
  2. A proposition statement of fewer than 25 words.
  3. A success metric with both a baseline and a target.

It parses the Markdown by heading, so keep the headings from
references/proposition-template.md exactly as they are.

Usage:
  proposition_check.py 02-market/proposition.md

It never crashes. A missing file or a missing section is reported plainly and
counted as a fail, not an exception. Exit code 0 when every check passes,
1 when a check fails, 2 when the file cannot be read at all. Pure standard
library: nothing to install.
"""

import argparse
import os
import re
import sys

# Headings the parser looks for. Matched case-insensitively, ignoring the
# leading "##" and any trailing whitespace.
JOBS_H = "customer jobs"
PAINS_H = "customer pains"
GAINS_H = "customer gains"
STATEMENT_H = "proposition statement"
METRIC_H = "success metric"

QUOTE_TAG = re.compile(r"\(quote:\s*Q\d+\s*\)", re.IGNORECASE)
BULLET = re.compile(r"^\s*[-*]\s+(.*\S.*)$")
# Italic prompt lines in the template start and end with an asterisk pair.
# We skip anything that is purely a prompt so an unfilled template does not
# read as passing.
PROMPT_ONLY = re.compile(r"^\s*\*.*\*\s*$")


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("FAIL: file not found: {}".format(path))
        print("      Run the skill to write it first, or check the path.")
        return None
    except OSError as e:
        print("FAIL: cannot read {}: {}".format(path, e))
        return None


def split_sections(text):
    """Return {normalised heading: [lines]} for every '##' section."""
    sections = {}
    current = None
    for raw in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*\S)\s*$", raw)
        if m:
            current = m.group(1).strip().lower()
            sections[current] = []
        elif current is not None:
            sections[current].append(raw)
    return sections


def bullets(lines):
    """Real filled-in bullets from a section, skipping template prompts."""
    out = []
    for line in lines or []:
        m = BULLET.match(line)
        if not m:
            continue
        content = m.group(1).strip()
        # A template example bullet is italic prompt text plus a sample tag.
        # Strip the tag, and if what remains is a pure italic prompt, skip it:
        # real founder content is not wrapped in asterisks.
        stripped = QUOTE_TAG.sub("", content).strip()
        if PROMPT_ONLY.match(stripped) or PROMPT_ONLY.match(content):
            continue
        out.append(content)
    return out


def check_canvas_list(sections, heading, label):
    """Three or more bullets, each carrying a quote tag."""
    lines = sections.get(heading)
    if lines is None:
        return False, "no '{}' section found".format(heading)
    items = bullets(lines)
    if len(items) < 3:
        return False, "{} has {} filled bullet(s), need at least 3".format(
            label, len(items))
    untagged = [b for b in items if not QUOTE_TAG.search(b)]
    if untagged:
        return False, "{} of {} {} bullet(s) have no (quote: Qn) tag".format(
            len(untagged), len(items), label)
    return True, "{} {} tagged to quotes".format(len(items), label)


def check_statement(sections):
    lines = sections.get(STATEMENT_H)
    if lines is None:
        return False, "no '{}' section found".format(STATEMENT_H)
    text_lines = []
    for line in lines:
        s = line.strip()
        if not s or PROMPT_ONLY.match(s):
            continue
        text_lines.append(s)
    if not text_lines:
        return False, "statement is empty"
    statement = " ".join(text_lines)
    words = re.findall(r"[A-Za-z0-9'./%-]+", statement)
    n = len(words)
    if n == 0:
        return False, "statement is empty"
    if n >= 25:
        return False, "statement is {} words, must be under 25".format(n)
    return True, "statement is {} words".format(n)


def check_metric(sections):
    lines = sections.get(METRIC_H)
    if lines is None:
        return False, "no '{}' section found".format(METRIC_H)
    body = "\n".join(lines).lower()
    has_baseline = "baseline" in body
    has_target = "target" in body
    has_measure = "measured by" in body or "measure" in body
    # A number somewhere in the metric block, so it is not all words.
    has_number = re.search(r"\d", body) is not None
    missing = []
    if not has_baseline:
        missing.append("baseline")
    if not has_target:
        missing.append("target")
    if not has_measure:
        missing.append("measurement method")
    if not has_number:
        missing.append("a number")
    if missing:
        return False, "metric missing: " + ", ".join(missing)
    return True, "metric has baseline, target and measure"


def main():
    ap = argparse.ArgumentParser(description="Check a proposition write-up.")
    ap.add_argument("path", nargs="?", default="02-market/proposition.md",
                    help="path to proposition.md (default 02-market/proposition.md)")
    args = ap.parse_args()

    text = read_file(args.path)
    if text is None:
        return 2

    sections = split_sections(text)

    checks = [
        check_canvas_list(sections, JOBS_H, "jobs"),
        check_canvas_list(sections, PAINS_H, "pains"),
        check_canvas_list(sections, GAINS_H, "gains"),
        check_statement(sections),
        check_metric(sections),
    ]

    print("Proposition check: {}".format(args.path))
    print("-" * 48)
    all_ok = True
    for ok, msg in checks:
        mark = "PASS" if ok else "FAIL"
        print("  [{}] {}".format(mark, msg))
        all_ok = all_ok and ok
    print("-" * 48)

    if all_ok:
        print("PASS: proposition meets the Day 2 done conditions.")
        return 0
    print("FAIL: fix the items above and re-run.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
