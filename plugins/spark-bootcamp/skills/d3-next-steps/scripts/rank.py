#!/usr/bin/env python3
"""Rank open launch items by impact, then lowest effort.

Reads a simple pipe-delimited file: one item per line, "item | impact | effort".
Impact and effort are 1 to 3. Prints a ranked table and flags the top 3 as
candidate blockers (only the ones with impact 3). Degrades gracefully: no third
-party libraries, and it tells you plainly if the input looks wrong rather than
crashing.

Usage:
  python3 rank.py items.txt
  # or pipe it:  cat items.txt | python3 rank.py

Input line example:
  Payment link takes a real charge | 3 | 1
Lines that are blank or start with # are ignored.
"""

import sys


def read_lines(path):
    if path and path != "-":
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.readlines()
        except OSError as e:
            print(f"Could not open {path}: {e}", file=sys.stderr)
            print("Falling back to reading from standard input.", file=sys.stderr)
    return sys.stdin.readlines()


def parse(lines):
    items, skipped = [], 0
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            print(f"Line {n} ignored (need 'item | impact | effort'): {line}",
                  file=sys.stderr)
            skipped += 1
            continue
        name, imp, eff = parts
        try:
            imp_i, eff_i = int(imp), int(eff)
        except ValueError:
            print(f"Line {n} ignored (impact and effort must be 1 to 3): {line}",
                  file=sys.stderr)
            skipped += 1
            continue
        if not (1 <= imp_i <= 3 and 1 <= eff_i <= 3):
            print(f"Line {n} ignored (impact and effort must be 1 to 3): {line}",
                  file=sys.stderr)
            skipped += 1
            continue
        items.append({"item": name, "impact": imp_i, "effort": eff_i})
    return items, skipped


def rank(items):
    # Impact descending, then effort ascending (quick wins beat slow ones).
    return sorted(items, key=lambda x: (-x["impact"], x["effort"]))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "-"
    items, skipped = parse(read_lines(path))

    if not items:
        print("No valid items found. Give me lines like: item | impact | effort")
        return 1

    ranked = rank(items)

    # Top 3 with impact 3 are the candidate blockers. Never more than 3.
    blockers = [it for it in ranked if it["impact"] == 3][:3]
    blocker_names = {id(it) for it in blockers}

    print(f"{'Rank':>4}  {'Imp':>3}  {'Eff':>3}  {'Blocker':>7}  Item")
    print("-" * 60)
    for i, it in enumerate(ranked, 1):
        flag = "yes" if id(it) in blocker_names else "no"
        print(f"{i:>4}  {it['impact']:>3}  {it['effort']:>3}  {flag:>7}  {it['item']}")

    print()
    print(f"Open items ranked: {len(ranked)}")
    print(f"Candidate blockers (impact 3, top 3): {len(blockers)}")
    if len(blockers) < 3:
        print("Fewer than 3 true blockers. You may be ahead. Confirm by hand.")
    if skipped:
        print(f"Lines skipped as malformed: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
