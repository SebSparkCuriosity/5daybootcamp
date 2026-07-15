#!/usr/bin/env python3
"""Check a Spark rate card before it goes near a buyer.

Rules, all of them the Spark house rules for Day 5 pricing:
  1. At least three prices are present.
  2. Every price is at or above the GBP 2,000 floor.
  3. Exactly one package is marked recommended.
  4. Every package carries a "Worth it because..." value line.

Usage:
    python3 price-check.py 05-sale/RATE-CARD.md

Exit code 0 means the card passes. Exit code 1 means it fails, and the
reasons are printed. No third-party libraries. If the file is missing it
says so plainly rather than crashing.
"""

import re
import sys

FLOOR = 2000


def read(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        print(f"Cannot find {path}. Write the rate card first, then run this again.")
        sys.exit(1)
    except OSError as exc:
        print(f"Could not read {path}: {exc}")
        sys.exit(1)


def find_prices(text):
    """Pull GBP figures like 'GBP 3,500' or '£2,000' into plain integers."""
    prices = []
    for match in re.finditer(r"(?:GBP|£)\s*([0-9][0-9,]*)", text):
        digits = match.group(1).replace(",", "")
        try:
            prices.append(int(digits))
        except ValueError:
            continue
    return prices


def main():
    if len(sys.argv) < 2:
        print("Give me the rate card path, for example:")
        print("  python3 price-check.py 05-sale/RATE-CARD.md")
        sys.exit(1)

    path = sys.argv[1]
    text = read(path)
    lower = text.lower()

    problems = []

    prices = find_prices(text)
    if len(prices) < 3:
        problems.append(
            f"Found {len(prices)} price(s). A rate card needs three packages with three numbers."
        )

    below = [p for p in prices if p < FLOOR]
    if below:
        joined = ", ".join(f"GBP {p:,}" for p in below)
        problems.append(
            f"These prices sit below the GBP 2,000 floor: {joined}. Lift the scope, do not drop the price."
        )

    recommended = lower.count("recommended")
    if recommended == 0:
        problems.append("No package is marked recommended. Mark exactly one as the default win.")
    elif recommended > 1:
        problems.append(
            f"'recommended' appears {recommended} times. Mark exactly one package, not several."
        )

    worth = lower.count("worth it because")
    if worth < 3:
        problems.append(
            f"Found {worth} 'Worth it because...' line(s). Each of the three packages needs one."
        )

    if problems:
        print("Rate card not ready:")
        for item in problems:
            print(f"  - {item}")
        sys.exit(1)

    ordered = sorted(prices)
    print("Rate card passes.")
    print(f"  Prices found: {', '.join(f'GBP {p:,}' for p in ordered)}")
    print(f"  Floor respected: lowest is GBP {ordered[0]:,}, at or above GBP {FLOOR:,}.")
    print("  Exactly one recommended package, three value assumptions present.")
    sys.exit(0)


if __name__ == "__main__":
    main()
