#!/usr/bin/env python3
"""Record the week's win.

Writes 05-sale/WON-DEAL.md with the tier, date and amount, plus the paperwork
checklist. Pure standard library, so it never fails on a missing package. If a
required value is not given it prints a clear message and writes what it can,
never crashing.

Usage:
  python3 record-win.py \
    --tier "cash | deposit | pilot | loi" \
    --amount "2000" \
    --currency "GBP" \
    --date "2026-07-17" \
    --client "Client Name Ltd" \
    --package "Reconciliation Autopilot" \
    [--balance "2000 due on go-live"] \
    [--kickoff "2026-07-21 10:00"] \
    [--letter-sent yes] \
    [--invoice-sent yes] \
    [--project-root /path/to/founder/project] \
    [--notes "anything worth remembering"]

All flags are optional so the script degrades gracefully. Anything missing is
written as TODO so the founder can see exactly what is still open.
"""

import argparse
import datetime
import os
import sys

TIER_LABELS = {
    "cash": "Tier 1: cash in full",
    "deposit": "Tier 2: a paid deposit",
    "pilot": "Tier 3: a signed paid pilot",
    "loi": "Tier 4: a signed letter of intent (date and amount)",
}


def val(x, fallback="TODO"):
    return x if x else fallback


def main():
    p = argparse.ArgumentParser(description="Record the week's win to WON-DEAL.md")
    p.add_argument("--tier", default="")
    p.add_argument("--amount", default="")
    p.add_argument("--currency", default="GBP")
    p.add_argument("--date", default="")
    p.add_argument("--client", default="")
    p.add_argument("--package", default="")
    p.add_argument("--balance", default="")
    p.add_argument("--kickoff", default="")
    p.add_argument("--letter-sent", dest="letter_sent", default="")
    p.add_argument("--invoice-sent", dest="invoice_sent", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--project-root", dest="project_root", default=".")
    args = p.parse_args()

    tier_key = (args.tier or "").strip().lower()
    tier_label = TIER_LABELS.get(tier_key, val(args.tier))
    if tier_key and tier_key not in TIER_LABELS:
        print(
            "Note: '%s' is not one of cash/deposit/pilot/loi. Writing it as given."
            % args.tier,
            file=sys.stderr,
        )

    date = args.date or datetime.date.today().isoformat()
    out_dir = os.path.join(args.project_root, "05-sale")
    out_path = os.path.join(out_dir, "WON-DEAL.md")

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        print("Could not create %s: %s" % (out_dir, e), file=sys.stderr)
        print("Falling back to current directory.", file=sys.stderr)
        out_path = "WON-DEAL.md"

    def tick(flag):
        return "yes" if (flag or "").strip().lower() in ("y", "yes", "true", "1") else "TODO"

    amount_line = (
        "%s %s" % (args.currency, args.amount) if args.amount else "TODO (put a number here)"
    )

    lines = [
        "# WON: the week's deal",
        "",
        "**Client:** %s" % val(args.client),
        "**Package:** %s" % val(args.package),
        "**Tier reached:** %s" % tier_label,
        "**Amount:** %s" % amount_line,
        "**Date won:** %s" % date,
        "",
        "## The commitment",
        "",
        "- Balance / schedule: %s" % val(args.balance, "n/a (paid in full)"),
        "- Engagement letter sent: %s" % tick(args.letter_sent),
        "- Invoice sent: %s" % tick(args.invoice_sent),
        "- Kickoff booked: %s" % val(args.kickoff),
        "",
        "## Notes",
        "",
        val(args.notes, "(none)"),
        "",
        "---",
        "",
        "The letter and invoice are drafts. Have a qualified lawyer review the",
        "letter before you rely on it. Spark does not warrant it.",
        "",
    ]

    content = "\n".join(lines)

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        print("Could not write %s: %s" % (out_path, e), file=sys.stderr)
        print("Here is the content so you can paste it in yourself:\n", file=sys.stderr)
        print(content)
        sys.exit(1)

    print("Wrote %s" % out_path)
    missing = [
        name
        for name, v in (
            ("tier", args.tier),
            ("amount", args.amount),
            ("client", args.client),
        )
        if not v
    ]
    if missing:
        print(
            "Still open (written as TODO): %s. Fill these before you log the win."
            % ", ".join(missing)
        )


if __name__ == "__main__":
    main()
