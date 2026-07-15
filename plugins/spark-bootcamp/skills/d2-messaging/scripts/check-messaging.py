#!/usr/bin/env python3
"""Check a messaging.md against the Spark done-conditions.

Rules:
  - one-liner under 12 words
  - exactly three key messages, each with a proof line
  - 60-word pitch between 55 and 65 words

Degrades gracefully: if the file's headings do not match the template, it
tells you what it could not find rather than crashing. Exit code 0 on all PASS,
1 otherwise, so it can gate a workflow.
"""
import re
import sys


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"Could not find {path}. Write 02-market/messaging.md first.")
        sys.exit(1)


def section(text, title):
    """Return the body under a '## title' heading, or None if absent."""
    pat = re.compile(rf"^#{{1,6}}\s*{re.escape(title)}.*?$(.*?)(?=^#{{1,6}}\s|\Z)",
                     re.IGNORECASE | re.MULTILINE | re.DOTALL)
    m = pat.search(text)
    return m.group(1).strip() if m else None


def words(s):
    return len(re.findall(r"[A-Za-z0-9'&/-]+", s))


def first_real_line(body):
    for line in body.splitlines():
        line = line.strip().lstrip(">-*").strip()
        line = re.sub(r"\(\s*\d+\s*words?\s*\)", "", line, flags=re.IGNORECASE).strip()
        if line:
            return line
    return ""


def check(path):
    text = read(path)
    passes = []

    # One-liner
    body = section(text, "one-liner") or section(text, "one liner")
    if body is None:
        print("MISS  one-liner: no '## One-liner' section found.")
        passes.append(False)
    else:
        n = words(first_real_line(body))
        ok = 0 < n < 12
        print(f"{'PASS' if ok else 'FAIL'}  one-liner: {n} words (need under 12).")
        passes.append(ok)

    # Three messages, each with proof
    body = section(text, "key messages") or section(text, "three key messages") \
        or section(text, "messages")
    if body is None:
        print("MISS  key messages: no '## Key messages' section found.")
        passes.append(False)
    else:
        proofs = len(re.findall(r"proof", body, re.IGNORECASE))
        arrows = len(re.findall(r"->|→", body))
        signals = max(proofs, arrows)
        ok = signals >= 3
        print(f"{'PASS' if ok else 'FAIL'}  key messages: {signals} proof lines detected (need 3, each 'Claim -> Proof').")
        passes.append(ok)

    # Pitch 55-65 words
    body = section(text, "pitch") or section(text, "60-word pitch") \
        or section(text, "30-second pitch")
    if body is None:
        print("MISS  pitch: no '## Pitch' section found.")
        passes.append(False)
    else:
        clean = re.sub(r"\(\s*\d+\s*words?\s*\)", "", body, flags=re.IGNORECASE)
        n = words(clean)
        ok = 55 <= n <= 65
        print(f"{'PASS' if ok else 'FAIL'}  pitch: {n} words (need 55 to 65).")
        passes.append(ok)

    if all(passes):
        print("\nAll checks PASS. Messaging is ready to log.")
        return 0
    print("\nSome checks did not pass. Fix them, then run this again.")
    return 1


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "02-market/messaging.md"
    sys.exit(check(target))
