#!/usr/bin/env python3
"""Check a Day 3 build brief (PRD.md) is buildable.

Three checks, matching the skill's done-condition:
  1. At least one numbered requirement (R1, R2, ...) exists.
  2. A non-goals / not-in-scope section exists and is non-empty.
  3. The success metric contains a number.

Optionally cross-checks against a moscow file: every Must line should be
covered by a requirement. Pass --moscow to enable. Degrades gracefully:
no external libraries, and a missing moscow file is a warning, not a crash.

Usage:
  python3 check-brief.py 03-product/docs/PRD.md
  python3 check-brief.py 03-product/docs/PRD.md --moscow 03-product/requirements-moscow.md
"""

import argparse
import re
import sys
from pathlib import Path

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def colour(text, code):
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def read(path):
    p = Path(path)
    if not p.exists():
        print(colour(f"FAIL: {path} does not exist. Write the PRD first.", RED))
        sys.exit(2)
    return p.read_text(encoding="utf-8")


def check_requirements(text):
    reqs = re.findall(r"(?mi)^#{0,4}\s*R\d+\s*[:.]", text)
    return len(reqs)


def check_non_goals(text):
    # Find a heading that names non-goals / out of scope / not in scope.
    pattern = re.compile(r"(?mi)^#{1,6}.*(non-goal|not in scope|out of scope).*$")
    m = pattern.search(text)
    if not m:
        return False
    # Grab text from that heading to the next heading and confirm it has content.
    tail = text[m.end():]
    next_heading = re.search(r"(?m)^#{1,6}\s", tail)
    body = tail[: next_heading.start()] if next_heading else tail
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    real = [ln for ln in lines if not re.fullmatch(r"[-*>\s]*", ln)
            and "<" not in ln]  # ignore template placeholders like <thing>
    return len(real) > 0


def check_metric(text):
    pattern = re.compile(r"(?mi)^#{1,6}.*success metric.*$")
    m = pattern.search(text)
    if not m:
        # Fall back: look for an "outcome as a number" section.
        return bool(re.search(r"\d", text)), "no 'Success metric' heading found"
    tail = text[m.end():]
    next_heading = re.search(r"(?m)^#{1,6}\s", tail)
    body = tail[: next_heading.start()] if next_heading else tail
    has_number = bool(re.search(r"\d", body))
    return has_number, None


def check_moscow(text, moscow_path):
    p = Path(moscow_path)
    if not p.exists():
        print(colour(f"  warn: {moscow_path} not found, skipping Must cross-check.", YELLOW))
        return None
    mtext = p.read_text(encoding="utf-8")
    # Musts: lines under a "Must" heading, or lines starting with Must markers.
    musts = re.findall(r"(?mi)^\s*[-*]\s+(.*)$", mtext)
    # Rough: count bullet lines that fall after a heading containing 'must'.
    must_count = 0
    in_must = False
    for line in mtext.splitlines():
        if re.match(r"(?i)^#{1,6}.*must", line):
            in_must = True
            continue
        if re.match(r"^#{1,6}\s", line):
            in_must = False
            continue
        if in_must and re.match(r"^\s*[-*]\s+\S", line):
            must_count += 1
    req_count = check_requirements(text)
    return must_count, req_count


def main():
    ap = argparse.ArgumentParser(description="Check a Day 3 build brief is buildable.")
    ap.add_argument("prd", help="path to PRD.md")
    ap.add_argument("--moscow", help="optional path to moscow.md for a Must cross-check")
    args = ap.parse_args()

    text = read(args.prd)
    problems = []

    req_count = check_requirements(text)
    if req_count == 0:
        problems.append("No numbered requirements found. Each Must needs an R1, R2, ...")
    elif req_count > 7:
        print(colour(f"  warn: {req_count} requirements. More than 7 is too many for one week.", YELLOW))

    if not check_non_goals(text):
        problems.append("No non-empty non-goals section. List what you are NOT building.")

    metric_ok, metric_note = check_metric(text)
    if metric_note:
        print(colour(f"  warn: {metric_note}", YELLOW))
    if not metric_ok:
        problems.append("Success metric has no number. State it as a number with a deadline.")

    if args.moscow:
        result = check_moscow(text, args.moscow)
        if result:
            must_count, rc = result
            if must_count and rc < must_count:
                print(colour(
                    f"  warn: {must_count} Musts in moscow but only {rc} requirements. "
                    "Some Musts may be uncovered.", YELLOW))

    print()
    if problems:
        print(colour("BRIEF NOT READY:", RED))
        for p in problems:
            print(colour(f"  - {p}", RED))
        sys.exit(1)

    print(colour(f"BRIEF READY: {req_count} numbered requirements, "
                 "non-goals present, metric is a number.", GREEN))
    sys.exit(0)


if __name__ == "__main__":
    main()
