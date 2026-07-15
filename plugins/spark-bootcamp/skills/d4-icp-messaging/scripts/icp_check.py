#!/usr/bin/env python3
"""Check 04-gtm/messaging.md against the Day 4 done-conditions.

Rules, all three must pass:
  1. The ICP is one sentence with exactly 3 criteria.
  2. The one-liner is under 20 words.
  3. Five objections are answered.

Degrades gracefully: no third-party libraries, pure standard library. If the file
is missing it says so and exits non-zero. It never crashes on odd formatting; it
reports what it could not find so a human can fix it by hand.

Usage:
    python3 icp_check.py 04-gtm/messaging.md
"""

import re
import sys


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"FAIL: {path} does not exist. Write the messaging file first.")
        sys.exit(2)
    except OSError as exc:
        print(f"FAIL: could not read {path}: {exc}")
        sys.exit(2)


def section(text, heading):
    """Return the body under '## heading' up to the next '## ' or end."""
    pattern = re.compile(
        r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def count_criteria(body):
    """Count bullet lines that look like criteria."""
    if not body:
        return 0
    return len([ln for ln in body.splitlines() if re.match(r"^\s*[-*]\s+\S", ln)])


def one_liner_words(body):
    """First non-empty, non-bracketed prose line under One-liner."""
    if not body:
        return None, 0
    for line in body.splitlines():
        stripped = line.strip().lstrip("-*").strip()
        if not stripped:
            continue
        if stripped.startswith("[") or stripped.startswith(">"):
            continue
        return stripped, len(stripped.split())
    return None, 0


def count_objections(body):
    """Count numbered objection lines (1. ... through 5. ...)."""
    if not body:
        return 0
    return len(re.findall(r"^\s*\d+\.\s+\S", body, re.MULTILINE))


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 icp_check.py <path-to-messaging.md>")
        sys.exit(2)

    path = sys.argv[1]
    text = read(path)
    problems = []

    icp = section(text, "ICP")
    criteria = count_criteria(icp)
    if icp is None:
        problems.append("No '## ICP' section found.")
    elif criteria != 3:
        problems.append(
            f"ICP must have exactly 3 criteria, found {criteria}. "
            "List them as three bullet lines."
        )

    liner = section(text, "One-liner")
    text_line, words = one_liner_words(liner)
    if liner is None:
        problems.append("No '## One-liner' section found.")
    elif text_line is None:
        problems.append("One-liner section is empty. Write the sentence.")
    elif words >= 20:
        problems.append(f"One-liner is {words} words, must be under 20. Cut it down.")

    objections = section(text, "Objections")
    obj_count = count_objections(objections)
    if objections is None:
        problems.append("No '## Objections' section found.")
    elif obj_count < 5:
        problems.append(
            f"Found {obj_count} numbered objections, need 5. "
            "Number them 1. to 5., each with an answer."
        )

    if problems:
        print("FAIL")
        for item in problems:
            print(f"  - {item}")
        sys.exit(1)

    print("PASS")
    print(f"  - ICP: 3 criteria")
    print(f"  - One-liner: {words} words (under 20)")
    print(f"  - Objections answered: {obj_count}")
    sys.exit(0)


if __name__ == "__main__":
    main()
