#!/usr/bin/env python3
"""Check a Day 3 blueprint (blueprint.md) is complete for the chosen path.

The blueprint models the build once so building is mechanical. What "complete"
means depends on business_type:

  software: an ERD (erDiagram) AND a system diagram (flowchart/graph).
  hardware: a system diagram (flowchart/graph) AND a bill of materials table
            (a Markdown table under a BOM / bill of materials heading).
  services: a service blueprint, i.e. a flowchart with at least 2 lanes
            (subgraphs) OR a sequenceDiagram.

It also runs a light Mermaid sanity check on every fenced ```mermaid block:
fences are balanced, each block names a known diagram type on its first line,
and brackets/parentheses/braces are balanced within the block.

No external libraries. Nothing here renders Mermaid; it only checks structure,
so it runs anywhere Python 3 does. A missing file exits 2 with a clear message.

Usage:
  python3 check-blueprint.py 03-product/docs/blueprint.md --type software
  python3 check-blueprint.py 03-product/docs/blueprint.md            # type read from .spark/state.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

KNOWN_TYPES = (
    "erDiagram", "flowchart", "graph", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "journey", "gantt", "pie", "mindmap",
)


def colour(text, code):
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def read(path):
    p = Path(path)
    if not p.exists():
        print(colour(f"FAIL: {path} does not exist. Write the blueprint first.", RED))
        sys.exit(2)
    return p.read_text(encoding="utf-8")


def mermaid_blocks(text):
    """Return the inner body of every ```mermaid ...``` fence."""
    return re.findall(r"(?ms)^```mermaid[^\n]*\n(.*?)^```", text)


def first_keyword(block):
    for line in block.splitlines():
        s = line.strip()
        if s and not s.startswith("%%"):  # skip mermaid comments
            return s
    return ""


def block_type(block):
    kw = first_keyword(block)
    for t in KNOWN_TYPES:
        if kw == t or kw.startswith(t + " ") or kw.startswith(t):
            return t
    return None


def brackets_balanced(block):
    pairs = {")": "(", "]": "[", "}": "{"}
    opens = set(pairs.values())
    stack = []
    in_quote = False
    for ch in block:
        if ch == '"':
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if ch in opens:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


def count_lanes(block):
    return len(re.findall(r"(?mi)^\s*subgraph\b", block))


def has_bom_table(text):
    """A Markdown table under a heading naming a bill of materials / BOM."""
    m = re.search(r"(?mi)^#{1,6}.*(bill of materials|\bbom\b).*$", text)
    if not m:
        return False
    tail = text[m.end():]
    nxt = re.search(r"(?m)^#{1,6}\s", tail)
    body = tail[: nxt.start()] if nxt else tail
    # A table needs a separator row of dashes and at least one data row.
    has_sep = re.search(r"(?m)^\s*\|?[\s:|-]*-[\s:|-]*\|", body)
    data_rows = [ln for ln in body.splitlines()
                 if ln.strip().startswith("|") and not re.fullmatch(r"[\s:|-]*", ln.strip())]
    return bool(has_sep) and len(data_rows) >= 2


def read_type_from_state():
    for base in (Path.cwd(), *Path.cwd().parents):
        sp = base / ".spark" / "state.json"
        if sp.exists():
            try:
                return json.loads(sp.read_text(encoding="utf-8")).get("business_type")
            except Exception:
                return None
    return None


def main():
    ap = argparse.ArgumentParser(description="Check a Day 3 blueprint is complete.")
    ap.add_argument("blueprint", help="path to blueprint.md")
    ap.add_argument("--type", choices=["software", "hardware", "services"],
                    help="business path (default: read from .spark/state.json)")
    args = ap.parse_args()

    text = read(args.blueprint)
    btype = args.type or read_type_from_state()
    if not btype:
        print(colour("FAIL: no --type given and business_type not found in "
                     ".spark/state.json. Pass --type software|hardware|services.", RED))
        sys.exit(2)

    problems = []
    blocks = mermaid_blocks(text)
    types_present = []

    # Light Mermaid sanity check on every block.
    for i, block in enumerate(blocks, 1):
        t = block_type(block)
        if t is None:
            problems.append(f"Mermaid block {i} does not start with a known diagram type "
                            f"({', '.join(KNOWN_TYPES[:5])}, ...).")
        else:
            types_present.append(t)
        # Bracket balance only means anything for flowchart node shapes. ER and
        # sequence diagrams use tokens like o{ and }| as cardinality, which are
        # not bracket pairs, so checking them would raise false alarms.
        if t in ("flowchart", "graph") and not brackets_balanced(block):
            problems.append(f"Mermaid block {i} has unbalanced brackets. It will not render.")

    def has(*wanted):
        return any(t in types_present for t in wanted)

    if btype == "software":
        if not has("erDiagram"):
            problems.append("Software needs a data model: one ```mermaid erDiagram``` block.")
        if not has("flowchart", "graph"):
            problems.append("Software needs a system diagram: a ```mermaid flowchart``` block.")
    elif btype == "hardware":
        if not has("flowchart", "graph"):
            problems.append("Hardware needs a system diagram: a ```mermaid flowchart``` block.")
        if not has_bom_table(text):
            problems.append("Hardware needs a bill of materials: a Markdown table under a "
                            "'Bill of materials' heading, with a total cost.")
    elif btype == "services":
        lanes_ok = any(count_lanes(b) >= 2 for b in blocks if block_type(b) in ("flowchart", "graph"))
        if not (lanes_ok or has("sequenceDiagram")):
            problems.append("Services needs a service blueprint: a ```mermaid flowchart``` with "
                            "at least 2 lanes (subgraphs), or a ```mermaid sequenceDiagram```.")

    print()
    if problems:
        print(colour(f"BLUEPRINT NOT READY ({btype}):", RED))
        for p in problems:
            print(colour(f"  - {p}", RED))
        sys.exit(1)

    print(colour(f"BLUEPRINT READY ({btype}): {len(blocks)} Mermaid diagram(s), "
                 "structure complete for the path.", GREEN))
    sys.exit(0)


if __name__ == "__main__":
    main()
