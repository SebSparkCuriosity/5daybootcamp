#!/usr/bin/env python3
"""Seed 05-sale/OBJECTIONS.md from the Day 4 objections plus the standard eight.

Degrades gracefully: if the Day 4 file is missing or unreadable, it falls back to
the standard eight alone and tells you so. It never crashes.

Usage:
  python3 build-objections.py --day4 04-gtm/messaging.md --out 05-sale/OBJECTIONS.md
"""
import argparse
import os
import re
import sys
from datetime import date

STANDARD_EIGHT = [
    "It's too expensive.",
    "I need to think about it.",
    "We already do this another way.",
    "Is it compliant / what about the regulator?",
    "What about our data / GDPR?",
    "Can you send me a proposal?",
    "Now isn't a good time.",
    "How do I know it'll work?",
]

TEMPLATE = """- **Objection:** {obj}
  - Acknowledge:
  - Reframe (the number or the proof):
  - Redirect (a question that moves forward):
"""


def extract_objections(path):
    """Best effort pull of objection-like lines from a markdown file."""
    if not path or not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except Exception as exc:  # never crash on a bad read
        print(f"Note: could not read {path} ({exc}). Using the standard eight only.")
        return []

    found = []
    capture = False
    for line in text.splitlines():
        low = line.lower()
        if "objection" in low and line.strip().startswith("#"):
            capture = True
            continue
        if capture and line.strip().startswith("#"):
            capture = False
        if capture:
            m = re.match(r"\s*(?:[-*]|\d+\.)\s+(.*)", line)
            if m and m.group(1).strip():
                found.append(m.group(1).strip().strip('"'))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day4", default="04-gtm/messaging.md",
                    help="Path to the Day 4 icp-messaging file.")
    ap.add_argument("--out", default="05-sale/OBJECTIONS.md",
                    help="Where to write the seeded objections file.")
    args = ap.parse_args()

    from_day4 = extract_objections(args.day4)
    if from_day4:
        print(f"Pulled {len(from_day4)} objection(s) from {args.day4}.")
    else:
        print("No Day 4 objections found. Seeding with the standard eight.")

    # De-duplicate, keep Day 4 first (they came from real prospects).
    seen = set()
    ordered = []
    for obj in from_day4 + STANDARD_EIGHT:
        key = obj.lower().strip(". ")
        if key not in seen:
            seen.add(key)
            ordered.append(obj)

    header = (
        "# Objections\n\n"
        f"Seeded {date.today().isoformat()} by d5-rehearse. "
        f"{len(ordered)} objections. Answer every one in your own words: "
        "acknowledge, reframe with a number, redirect with a question.\n\n"
        "A price objection is usually a value question in disguise. "
        "Model answers live in the skill's references/objection-library.md.\n\n"
    )
    body = "\n".join(TEMPLATE.format(obj=o) for o in ordered)

    out_dir = os.path.dirname(args.out)
    if out_dir and not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as exc:
            print(f"Could not create {out_dir} ({exc}). Writing to current directory.")
            args.out = os.path.basename(args.out)

    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(header + body + "\n")
    except Exception as exc:
        print(f"Could not write {args.out} ({exc}). Here is the content instead:\n")
        print(header + body)
        return 1

    print(f"Wrote {args.out} with {len(ordered)} objections. "
          "Now finish each answer aloud, not just on the page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
