#!/usr/bin/env python3
"""Scaffold and check a competitor matrix CSV for the d2-competitor-scan skill.

Two modes, chosen automatically:
  - If the target file does NOT exist, write a starter CSV with default
    columns and a couple of placeholder rows, then stop.
  - If the target file DOES exist, check it against the done-condition:
    6+ rival rows, 5+ dimension columns, every row sourced. Print PASS or
    a clear list of what is missing.

Usage:
    python scaffold_matrix.py 02-market/competitor-matrix.csv

No third-party libraries. Uses only the standard library, so it never needs
an install and never crashes on a missing dependency.
"""

import csv
import os
import sys

# Default columns: rival name, five buyer-facing dimensions, and a source column.
DEFAULT_HEADER = [
    "rival",
    "price",
    "built_for",
    "main_strength",
    "main_weakness",
    "regulated_jersey_fit",
    "source",
]

PLACEHOLDER_ROWS = [
    [
        "Status quo (spreadsheet / do nothing)",
        "0",
        "everyone coping manually",
        "free, familiar",
        "slow, error-prone, no audit trail",
        "assumption: no controls",
        "assumption, confirm in interviews",
    ],
    [
        "Rival 2 (replace me)",
        "price on request",
        "who they serve",
        "their one real strength",
        "the gap buyers complain about",
        "data residency / audit posture",
        "https://... (cite the page)",
    ],
]

MIN_RIVALS = 6
MIN_DIMENSIONS = 5  # dimension columns = all columns except rival and source


def scaffold(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(DEFAULT_HEADER)
        writer.writerows(PLACEHOLDER_ROWS)
    print("Starter CSV written to " + path)
    print("Columns: " + ", ".join(DEFAULT_HEADER))
    print("")
    print("Next: replace the placeholder rows. Aim for 6+ rivals, 5+ dimensions,")
    print("and a source in every row. Run this script again to check it.")


def check(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        print("FAIL: the file is empty.")
        return 1

    header = [c.strip().lower() for c in rows[0]]
    data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)]

    problems = []

    # Count dimension columns: everything that is not the rival or source column.
    has_source_col = "source" in header
    non_dimension = {"rival", "source"}
    dimension_cols = [c for c in header if c not in non_dimension]
    n_dimensions = len(dimension_cols)

    n_rivals = len(data_rows)

    if n_rivals < MIN_RIVALS:
        problems.append(
            "only {} rival rows, need {}+".format(n_rivals, MIN_RIVALS)
        )
    if n_dimensions < MIN_DIMENSIONS:
        problems.append(
            "only {} dimension columns, need {}+".format(n_dimensions, MIN_DIMENSIONS)
        )

    # Every row must have a non-empty source.
    if not has_source_col:
        problems.append("no 'source' column found; add one and cite each row")
    else:
        src_idx = header.index("source")
        unsourced = []
        for r in data_rows:
            name = r[0].strip() if r else "(blank)"
            src = r[src_idx].strip() if len(r) > src_idx else ""
            if not src:
                unsourced.append(name)
        if unsourced:
            problems.append(
                "rows with no source: " + ", ".join(unsourced)
            )

    print("Rivals: {}   Dimensions: {}".format(n_rivals, n_dimensions))
    if problems:
        print("FAIL:")
        for p in problems:
            print("  - " + p)
        print("")
        print("Fix these, then run the check again.")
        return 1

    print("PASS: 6+ rivals, 5+ dimensions, every row sourced.")
    print("Now write the gap sentence at the foot of 02-market/competitors.md.")
    return 0


def main(argv):
    if len(argv) != 2:
        print("Usage: python scaffold_matrix.py <path-to-competitor-matrix.csv>")
        return 2
    path = argv[1]
    if os.path.exists(path):
        return check(path)
    scaffold(path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
