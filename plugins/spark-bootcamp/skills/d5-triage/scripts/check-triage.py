#!/usr/bin/env python3
"""Validate a Day 5 TRIAGE.md against the two hard rules.

Rules checked:
  1. Fix Now holds at most 3 items.
  2. Every Fix Now item has an effort estimate under 90 minutes.

Usage:
  python3 check-triage.py 05-sale/TRIAGE.md

Degrades gracefully: no third-party libraries, standard library only.
Never crashes on a malformed file; prints a clear message instead.
"""
import re
import sys


def find_section(lines, heading_word):
    """Return the lines belonging to the section whose H2 contains heading_word."""
    out = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            inside = heading_word.lower() in line.lower()
            continue
        if inside:
            out.append(line)
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check-triage.py <path-to-TRIAGE.md>")
        return 2

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("FAIL: cannot find %s. Write the triage first." % path)
        return 1
    except OSError as exc:
        print("FAIL: could not read %s (%s)." % (path, exc))
        return 1

    fix_now = find_section(lines, "Fix Now")
    if not fix_now:
        print("FAIL: no 'Fix Now' section found. Use the reference template.")
        return 1

    # Count table rows that look like real items: a leading number in the first cell.
    problems = []
    item_count = 0
    efforts = []
    for line in fix_now:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        # Skip header ("#") and separator ("---") rows.
        first = cells[0]
        if first in ("#", "") or set(first) <= set("-: "):
            continue
        if not first.isdigit():
            continue
        item_count += 1
        # Effort is the numeric cell; grab the last integer on the row.
        nums = re.findall(r"\d+", " ".join(cells[1:]))
        if not nums:
            problems.append("Row %s has no effort estimate." % first)
            continue
        effort = int(nums[-1])
        efforts.append(effort)
        if effort >= 90:
            problems.append("Row %s effort is %d min, not under 90." % (first, effort))

    if item_count == 0:
        print("PASS (empty Fix Now). Nothing queued. Confirm the page is good enough to sell as is.")
        return 0

    if item_count > 3:
        problems.append("Fix Now has %d items, maximum is 3." % item_count)

    if problems:
        print("FAIL:")
        for p in problems:
            print("  - " + p)
        return 1

    total = sum(efforts)
    print("PASS: %d Fix Now item(s), %d min total, each under 90 min." % (item_count, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
