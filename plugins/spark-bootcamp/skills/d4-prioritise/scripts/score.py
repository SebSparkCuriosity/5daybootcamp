#!/usr/bin/env python3
"""Score product-test feedback with RICE + MoSCoW and rank testers by buying intent.

Reads a small input block the founder fills in (changes + testers), computes RICE
scores and tester totals, then writes:
  <project>/04-gtm/feedback-synthesis.md
  <project>/04-gtm/buying-signal-scorecard.csv

Degrades gracefully:
  - PyYAML present  -> reads scoring-input.yaml.
  - PyYAML missing  -> reads scoring-input.txt (plain key: value blocks).
  - Neither input present -> writes a template and exits with instructions.
Never crashes on a missing optional library. If Python is unavailable entirely,
the reference guide carries the formulas for a hand calculation.
"""

import argparse
import csv
import os
import sys
from datetime import date

TEMPLATE = """# d4-prioritise scoring input
# One 'change' block per requested change, one 'tester' block per person.
# RICE score = (reach * impact * confidence) / effort. MoSCoW: Must|Should|Could|Won't.
# Tester signals are each 0..3: pain, budget, timing, pull. from_page: yes|no.

changes:
  - name: One-screen onboarding
    reach: 4
    impact: 3          # 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal
    confidence: 1.0    # 1.0 saw it, 0.8 one account, 0.5 hunch, 0.2 guess
    effort: 0.5        # person-days
    moscow: Must
  - name: Dark mode
    reach: 1
    impact: 0.5
    confidence: 0.5
    effort: 1.0
    moscow: "Won't"

testers:
  - name: Alex (Trust Co)
    pain: 3
    budget: 2
    timing: 3
    pull: 3
    from_page: yes
  - name: Sam (Fund admin)
    pain: 2
    budget: 1
    timing: 1
    pull: 1
    from_page: no
"""


def find_input(project):
    yaml_path = os.path.join(project, "04-gtm", "scoring-input.yaml")
    txt_path = os.path.join(project, "04-gtm", "scoring-input.txt")
    return yaml_path, txt_path


def parse_txt(path):
    """Fallback parser: blocks separated by '---', 'key: value' lines.
    First block header 'changes' or 'testers' switches section via a line 'section: changes'."""
    changes, testers = [], []
    section = None
    current = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower() in ("section: changes", "[changes]"):
                section = "changes"
                continue
            if line.lower() in ("section: testers", "[testers]"):
                section = "testers"
                continue
            if line == "---":
                if current and section == "changes":
                    changes.append(current)
                elif current and section == "testers":
                    testers.append(current)
                current = {}
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                current[k.strip()] = v.strip().strip('"').strip("'")
        if current and section == "changes":
            changes.append(current)
        elif current and section == "testers":
            testers.append(current)
    return {"changes": changes, "testers": testers}


def load_data(yaml_path, txt_path):
    try:
        import yaml  # type: ignore
        if os.path.exists(yaml_path):
            with open(yaml_path, encoding="utf-8") as fh:
                return yaml.safe_load(fh) or {}, "yaml"
    except ImportError:
        print("PyYAML not installed. Falling back to plain-text input.", file=sys.stderr)
    if os.path.exists(txt_path):
        return parse_txt(txt_path), "txt"
    if os.path.exists(yaml_path):
        # YAML file exists but no PyYAML: try the txt parser on it, it is close enough.
        return parse_txt(yaml_path), "txt-on-yaml"
    return None, None


def num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def rice(c):
    reach = num(c.get("reach"))
    impact = num(c.get("impact"))
    conf = num(c.get("confidence"))
    effort = num(c.get("effort"), 1.0) or 1.0
    return round((reach * impact * conf) / effort, 2)


def band(total):
    if total >= 9:
        return "Hot"
    if total >= 5:
        return "Warm"
    return "Cool"


def truthy(v):
    return str(v).strip().lower() in ("yes", "true", "1", "y")


def write_synthesis(path, changes):
    scored = []
    for c in changes:
        c = dict(c)
        c["rice"] = rice(c)
        scored.append(c)
    # Sort by RICE desc; Must beats Should on ties.
    order = {"Must": 0, "Should": 1, "Could": 2, "Won't": 3}
    scored.sort(key=lambda x: (-x["rice"], order.get(str(x.get("moscow")), 9)))
    # Top 3 buildable (effort <= 1.0) flagged.
    flagged = 0
    for c in scored:
        c["build_friday"] = False
        if flagged < 3 and num(c.get("effort"), 1.0) <= 1.0:
            c["build_friday"] = True
            flagged += 1

    lines = []
    lines.append("# Feedback synthesis (Day 4)\n")
    lines.append(f"_Generated {date.today().isoformat()} by d4-prioritise._\n")
    if scored:
        top = scored[0]
        lines.append(
            f"The clearest signal: **{top.get('name','(unnamed)')}** scores {top['rice']} on RICE "
            f"and is the change to build first.\n"
        )
    lines.append("## Changes, ranked by RICE\n")
    lines.append("| Change | Reach | Impact | Confidence | Effort | RICE | MoSCoW | |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in scored:
        flag = "**BUILD FRIDAY**" if c["build_friday"] else ""
        lines.append(
            f"| {c.get('name','(unnamed)')} | {num(c.get('reach')):g} | {num(c.get('impact')):g} | "
            f"{int(num(c.get('confidence'))*100)}% | {num(c.get('effort'),1.0):g} | {c['rice']} | "
            f"{c.get('moscow','?')} | {flag} |"
        )
    lines.append("")
    lines.append(f"**{flagged} changes flagged for Friday.** Everything else waits.\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return len(scored), flagged


def write_scorecard(path, testers):
    rows = []
    for t in testers:
        pain = int(num(t.get("pain")))
        budget = int(num(t.get("budget")))
        timing = int(num(t.get("timing")))
        pull = int(num(t.get("pull")))
        from_page = truthy(t.get("from_page"))
        if from_page:
            pull = max(pull, 3)
        total = pain + budget + timing + pull
        rows.append({
            "tester": t.get("name", "(unnamed)"),
            "pain": pain, "budget": budget, "timing": timing, "pull": pull,
            "total_out_of_12": total, "warmth": band(total),
            "from_live_page": "yes" if from_page else "no",
        })
    # Hottest first; live-page hand-raisers win ties.
    rows.sort(key=lambda r: (-r["total_out_of_12"], r["from_live_page"] != "yes"))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    fields = ["rank", "tester", "pain", "budget", "timing", "pull",
              "total_out_of_12", "warmth", "from_live_page"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".", help="Path to the founder's project root.")
    args = ap.parse_args()

    gtm = os.path.join(args.project, "04-gtm")
    os.makedirs(gtm, exist_ok=True)
    yaml_path, txt_path = find_input(args.project)

    data, mode = load_data(yaml_path, txt_path)
    if data is None:
        with open(yaml_path, "w", encoding="utf-8") as fh:
            fh.write(TEMPLATE)
        print("No scoring input found. I have written a template for you to fill in:")
        print(f"  {yaml_path}")
        print("Fill in your changes and testers, then run this script again.")
        print("(No PyYAML? Save it as scoring-input.txt using 'section: changes' / "
              "'section: testers' headers and '---' between blocks.)")
        return 0

    changes = data.get("changes") or []
    testers = data.get("testers") or []
    if not changes and not testers:
        print("Input file has no changes and no testers. Nothing to score.", file=sys.stderr)
        return 1

    syn_path = os.path.join(gtm, "feedback-synthesis.md")
    card_path = os.path.join(gtm, "buying-signal-scorecard.csv")
    n_changes, flagged = write_synthesis(syn_path, changes)
    n_testers = write_scorecard(card_path, testers)

    print(f"Wrote {syn_path}: {n_changes} changes scored, {flagged} flagged BUILD FRIDAY.")
    print(f"Wrote {card_path}: {n_testers} testers ranked by buying intent.")
    print(f"(Input read as: {mode}.)")
    if flagged < 3 and n_changes >= 3:
        print("Note: fewer than 3 changes were buildable in <=1 person-day. "
              "Review efforts or accept a shorter Friday list.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
