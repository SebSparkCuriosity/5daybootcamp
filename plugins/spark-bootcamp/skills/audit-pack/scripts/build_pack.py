#!/usr/bin/env python3
"""Compile the week's audit trail into one regulator/investor-ready pack.

Reads (relative to the founder's project root, passed as --root or cwd):
  .spark/state.json      journey state, including artefacts[]
  CHANGELOG.md           append-only log of every artefact and its number
  DECISIONS.md           decision log with rationale

Writes:
  .spark/deliverables/audit-pack.md

Degrades gracefully: any missing input is noted in the pack rather than
crashing. Uses only the Python standard library.
"""

import argparse
import json
import os
import re
import sys
from datetime import date


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return None
    except OSError as exc:
        print(f"warning: could not read {path}: {exc}", file=sys.stderr)
        return None


def load_state(path):
    raw = read_text(path)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"warning: {path} is not valid JSON: {exc}", file=sys.stderr)
        return None


NUMBER_RE = re.compile(r"[-+]?\d[\d,]*\.?\d*\s*%?")


def first_number(text):
    """Pull the first number-looking token out of a string, or a dash."""
    if not text:
        return "-"
    match = NUMBER_RE.search(str(text))
    return match.group(0).strip() if match else "-"


def build_headline(state):
    """Return (target, achieved) strings for the pack's opening line."""
    if not state:
        return ("(state.json missing, target unknown)",
                "(state.json missing, outcome unknown)")
    target = state.get("headline_target") or "(no headline_target set)"
    # Prefer the day-5 outcome as "what was achieved"; fall back to a
    # summary of completed days.
    days = state.get("days") or {}
    day5 = days.get("5") or {}
    achieved = day5.get("outcome")
    if not achieved:
        done = [d for d in days.values() if d.get("complete")]
        achieved = f"{len(done)} of {len(days)} days completed"
    return (str(target), str(achieved))


def build_artefact_rows(state):
    """Every logged artefact with its date and its number.

    Returns a list of (date, skill, path, result_number, result_text).
    """
    rows = []
    if not state:
        return rows
    for a in state.get("artefacts") or []:
        at = a.get("at") or "-"
        skill = a.get("skill") or "-"
        path = a.get("path") or "-"
        result = a.get("result")
        rows.append((at, skill, path, first_number(result), result or "-"))
    return rows


def render(state, changelog, decisions, today):
    target, achieved = build_headline(state)
    founder = (state or {}).get("founder", "the founder")
    business_type = (state or {}).get("business_type", "unspecified")
    idea = (state or {}).get("idea", "")

    out = []
    out.append("# Audit Pack")
    out.append("")
    out.append(f"Compiled {today} for {founder}.")
    out.append("")
    out.append("## Headline outcome")
    out.append("")
    out.append(f"**Target:** {target}")
    out.append("")
    out.append(f"**Achieved:** {achieved}")
    out.append("")
    if idea:
        out.append(f"**Business:** {idea} (type: {business_type})")
        out.append("")

    out.append("## Artefacts")
    out.append("")
    rows = build_artefact_rows(state)
    if rows:
        out.append("| Date | Skill | Artefact | Number |")
        out.append("| --- | --- | --- | --- |")
        for at, skill, path, number, _ in rows:
            out.append(f"| {at} | {skill} | {path} | {number} |")
        out.append("")
        out.append(f"Total artefacts logged: {len(rows)}.")
    else:
        out.append("No artefacts recorded in .spark/state.json yet. "
                   "Run the day skills first, then rebuild this pack.")
    out.append("")

    out.append("## Change log")
    out.append("")
    if changelog:
        out.append("```")
        out.append(changelog.rstrip())
        out.append("```")
    else:
        out.append("CHANGELOG.md not found. Nothing has been logged yet.")
    out.append("")

    out.append("## Decision log")
    out.append("")
    if decisions:
        out.append(decisions.rstrip())
    else:
        out.append("DECISIONS.md not found. No decisions have been recorded.")
    out.append("")

    out.append("---")
    out.append("This pack is a draft compiled from the founder's own logs. "
               "It reflects what was recorded, not independent verification. "
               "Have a qualified adviser review it before you rely on it. "
               "Spark does not warrant it.")
    out.append("")
    return "\n".join(out), len(rows)


def main():
    parser = argparse.ArgumentParser(description="Build the Spark audit pack.")
    parser.add_argument("--root", default=os.getcwd(),
                        help="Founder project root (default: cwd)")
    parser.add_argument("--out",
                        help="Output path (default: <root>/.spark/deliverables/audit-pack.md)")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    state = load_state(os.path.join(root, ".spark", "state.json"))
    changelog = read_text(os.path.join(root, "CHANGELOG.md"))
    decisions = read_text(os.path.join(root, "DECISIONS.md"))

    today = date.today().isoformat()
    text, count = render(state, changelog, decisions, today)

    out_path = args.out or os.path.join(root, ".spark", "deliverables",
                                        "audit-pack.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    print(f"Wrote {out_path}")
    print(f"Artefacts in pack: {count}")
    if not state:
        print("Note: state.json was missing or unreadable. "
              "Headline and artefact table are incomplete.")


if __name__ == "__main__":
    main()
