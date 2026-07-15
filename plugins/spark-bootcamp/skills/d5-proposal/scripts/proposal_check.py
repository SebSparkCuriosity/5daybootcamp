#!/usr/bin/env python3
"""Check a Spark proposal against the six one-page rules.

Usage:
    python3 proposal_check.py 05-sale/PROPOSAL.md

Checks, in order:
  1. One page. Body is under 500 words (a real one-pager runs 250 to 450).
  2. A numeric target. At least one number tied to an outcome word.
  3. A 1 to 6 week timeline. A "N week" phrase with N between 1 and 6.
  4. One price. Exactly one currency figure (GBP or the pound sign).
  5. One next step. A "Next step" heading or line is present.
  6. Names the buyer. A "To:" line names a person.

Prints PASS or a numbered list of exactly what is missing. Never crashes.
Exit code 0 on PASS, 1 on any failure, 2 on a usage or file error.
"""

import sys
import os
import re


def load(path):
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def word_count(text):
    # Count words in prose, ignoring markdown table pipes and rule lines.
    cleaned = re.sub(r"[|>#*_`-]", " ", text)
    return len(cleaned.split())


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 proposal_check.py <proposal.md>")
        return 2

    text = load(sys.argv[1])
    if text is None:
        return 2

    low = text.lower()
    problems = []

    # 1. One page.
    words = word_count(text)
    if words > 500:
        problems.append(
            f"Too long: {words} words. A one-pager is under 500. Cut it back."
        )

    # 2. A numeric target near an outcome word.
    outcome_words = r"(hour|day|week|minute|%|percent|per cent|from|to|cut|save|reduc|faster|fund|matter|report|seat|client|case)"
    if not re.search(r"\d", text) or not re.search(
        r"\d[\d,\.]*\s*\w*.{0,40}" + outcome_words, low
    ):
        problems.append(
            "No numeric target found. State the outcome as a number (for example 'from 3 days to 0.5 days')."
        )

    # 3. A 1 to 6 week timeline. Accept "N week", "week N" and spelled-out numbers.
    word_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
    weeks = []
    weeks += re.findall(r"(\d+)\s*(?:to\s*\d+\s*)?weeks?", low)
    weeks += re.findall(r"weeks?\s*(\d+)", low)
    weeks = [int(w) for w in weeks]
    for name, val in word_num.items():
        if re.search(name + r"\s*(?:to\s*\w+\s*)?weeks?", low):
            weeks.append(val)
    week_ok = any(1 <= w <= 6 for w in weeks)
    if not week_ok:
        problems.append(
            "No 1 to 6 week timeline found. Give a delivery window inside six weeks."
        )

    # 4. Exactly one price (currency figure).
    prices = re.findall(r"(?:£|gbp\s*)\s*\d[\d,]*", low)
    if len(prices) == 0:
        problems.append("No price found. State one price (for example GBP 2,000).")
    elif len(prices) > 1:
        problems.append(
            f"Found {len(prices)} prices. A proposal states ONE price. Remove the others or move options to a note."
        )

    # 5. One next step.
    if "next step" not in low:
        problems.append(
            "No next step found. Add a 'Next step' line with one clear action."
        )

    # 6. Names the buyer.
    to_line = re.search(r"(?m)^\s*(?:\*\*)?\s*to\s*:?\s*(?:\*\*)?\s*(.+)$", text, re.I)
    named = bool(to_line and len(to_line.group(1).strip()) >= 3)
    if not named:
        problems.append(
            "No named buyer found. Start with a 'To:' line naming the person, their role and firm."
        )

    if problems:
        print("NOT READY. Fix these, then re-run:")
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}")
        return 1

    print(f"PASS. {words} words, one price, a 1 to 6 week timeline, a numeric target, a next step, a named buyer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
