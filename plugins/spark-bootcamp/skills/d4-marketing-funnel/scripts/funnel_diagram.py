#!/usr/bin/env python3
"""Build a Mermaid funnel diagram from the stage table in funnel.md.

Reads the four-stage table, checks every stage has a channel, an asset and a
metric, writes 04-gtm/funnel.mmd next to the source, and prints a Markdown
block to paste back into funnel.md.

No third-party libraries. If the file or table is missing, it says exactly
what is wrong and exits non-zero. It never invents a missing value: a
fabricated metric is worse than a blank one.

Expected table shape in funnel.md (a standard Markdown table):

    | Stage | Channel | Asset | Metric |
    | --- | --- | --- | --- |
    | Awareness | LinkedIn, Jersey finance community | Explainer post | 200 reached |
    | Interest | ... | ... | ... |
    | Consideration | ... | ... | ... |
    | Purchase | ... | ... | ... |
"""

import os
import re
import sys

STAGES = ["Awareness", "Interest", "Consideration", "Purchase"]
BLANK = {"", "-", "tbd", "todo", "to build", "n/a", "?"}


def die(msg):
    print("Funnel diagram: " + msg, file=sys.stderr)
    sys.exit(1)


def parse_table(text):
    """Return {stage: {channel, asset, metric}} from the first matching table."""
    rows = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        stage = cells[0]
        # Skip the header and the --- separator row.
        if stage.lower() == "stage" or set(cells[0]) <= set("-: "):
            continue
        for canonical in STAGES:
            if stage.lower() == canonical.lower():
                rows[canonical] = {
                    "channel": cells[1],
                    "asset": cells[2],
                    "metric": cells[3],
                }
    return rows


def check(rows):
    missing = []
    for stage in STAGES:
        if stage not in rows:
            missing.append("stage '%s' is not in the table" % stage)
            continue
        for field in ("channel", "asset", "metric"):
            value = rows[stage][field]
            if value.strip().lower() in BLANK:
                missing.append("stage '%s' is missing its %s" % (stage, field))
    return missing


def has_number(metric):
    return bool(re.search(r"\d", metric))


def build_mermaid(rows):
    lines = ["flowchart TD"]
    prev = None
    for i, stage in enumerate(STAGES):
        node = "S%d" % (i + 1)
        r = rows[stage]
        label = "%s<br/>%s<br/>%s" % (stage, r["channel"], r["metric"])
        label = label.replace('"', "'")
        lines.append('    %s["%s"]' % (node, label))
        if prev:
            lines.append("    %s --> %s" % (prev, node))
        prev = node
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        die("usage: funnel_diagram.py <path-to-funnel.md>")
    src = sys.argv[1]
    if not os.path.exists(src):
        die("cannot find %s. Write the four-stage table first, then rerun." % src)

    with open(src, "r", encoding="utf-8") as fh:
        text = fh.read()

    rows = parse_table(text)
    if not rows:
        die("no stage table found. Add a Markdown table with columns "
            "Stage | Channel | Asset | Metric and one row per stage.")

    problems = check(rows)
    if problems:
        print("Funnel diagram: the funnel is not complete yet.", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        print("Fill those in and run this again. Nothing was written.",
              file=sys.stderr)
        sys.exit(1)

    # Soft warning: a metric with no digit is probably not measurable.
    for stage in STAGES:
        if not has_number(rows[stage]["metric"]):
            print("Note: stage '%s' metric has no number in it. Every stage "
                  "needs one. Value was: %s"
                  % (stage, rows[stage]["metric"]), file=sys.stderr)

    mermaid = build_mermaid(rows)
    out = os.path.join(os.path.dirname(os.path.abspath(src)), "funnel.mmd")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(mermaid)

    print("Wrote " + out)
    print("\nPaste this block into funnel.md:\n")
    print("```mermaid")
    print(mermaid.rstrip())
    print("```")


if __name__ == "__main__":
    main()
