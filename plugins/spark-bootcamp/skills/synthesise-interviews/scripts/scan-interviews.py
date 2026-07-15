#!/usr/bin/env python3
"""Count and index a folder of interview records before you synthesise them.

This does the one thing you must not eyeball: it counts the records, so the
synthesis is honest about how much evidence it actually rests on. It reads
every .md file in a folder, reports how many there are, classifies the
confidence that count buys you, and prints a short index (filename, first
heading, size) so you can cite records by name.

It reads nothing but the filesystem and uses only the standard library, so it
runs anywhere Python 3 runs. If the folder is missing or empty it says so
plainly and exits 0 (an empty run is a finding, not a crash).

Usage:
  scan-interviews.py 01-discovery/interviews
  scan-interviews.py 01-discovery/interviews --json

Confidence bands (records found):
  8 or more : strong. Synthesise and cite 8+ records.
  5 to 7    : usable. Synthesise, but flag the thinner base.
  1 to 4    : weak. Report patterns as tentative. Say the base is small.
  0         : none. Do not synthesise. Go and run more interviews.
"""

import argparse
import glob
import json
import os
import sys


def first_heading(path):
    """Return the first Markdown heading in a file, or the bare filename."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("#"):
                    return line.lstrip("#").strip()
    except OSError:
        pass
    return os.path.basename(path)


def band(n):
    """Map a record count to a confidence band and a one-line instruction."""
    if n >= 8:
        return "strong", "Synthesise and cite 8+ records."
    if n >= 5:
        return "usable", "Synthesise, but flag the thinner base in the findings."
    if n >= 1:
        return "weak", "Report patterns as tentative. Say the base is small."
    return "none", "Do not synthesise. Run more interviews first."


def main():
    ap = argparse.ArgumentParser(description="Count and index interview records.")
    ap.add_argument("folder", help="Folder of .md interview records")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args()

    folder = args.folder
    if not os.path.isdir(folder):
        msg = f"No folder at {folder}. There are no interview records to read yet."
        if args.json:
            print(json.dumps({"folder": folder, "count": 0, "band": "none",
                              "records": [], "note": msg}))
        else:
            print(msg)
            print("Confidence: none. Run interviews and save them here first.")
        return 0

    paths = sorted(glob.glob(os.path.join(folder, "*.md")))
    records = [{"file": os.path.relpath(p, "."),
                "title": first_heading(p),
                "bytes": os.path.getsize(p)} for p in paths]
    n = len(records)
    label, instruction = band(n)

    if args.json:
        print(json.dumps({"folder": folder, "count": n, "band": label,
                          "instruction": instruction, "records": records}, indent=2))
        return 0

    print(f"Records found: {n}")
    print(f"Confidence: {label}. {instruction}")
    if n == 0:
        return 0
    print("")
    print("Index (cite records by file):")
    for r in records:
        thin = "  [thin: under 400 bytes]" if r["bytes"] < 400 else ""
        print(f"  - {r['file']}  ({r['title']}){thin}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
