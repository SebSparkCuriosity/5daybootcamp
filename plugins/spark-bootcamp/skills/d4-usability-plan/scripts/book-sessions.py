#!/usr/bin/env python3
"""Turn the usability test plan's booking table into ready-to-send booking
messages, one per tester. It never sends and never spends.

The founder recruited these testers on Day 1. This just drafts the "here is a
slot, does it work?" message for each of them so booking 5 sessions is three
minutes of copy-paste, not an afternoon of writing.

Usage:
  book-sessions.py 04-gtm/tests/usability-test-plan.md
  book-sessions.py 04-gtm/tests/usability-test-plan.md --founder Seb --url https://my-mvp.vercel.app --minutes 30

It reads the Markdown booking table (the pipe table under "## Booking table"),
pulls tester name, channel and proposed slot from each row, and prints a
booking message for every tester who is not already confirmed. It also writes
the same messages to booking-messages.md next to the plan so nothing is lost.

Graceful by design: if the plan file or its booking table is missing, it prints
a clear message and a blank template you can fill by hand. It needs no third-
party libraries and never crashes on a malformed table: rows it cannot parse are
reported and skipped, not fatal.
"""

import argparse
import os
import re
import sys


MESSAGE = (
    "Hi {name},\n\n"
    "Thanks again for offering to look at what I built this week. It is live now. "
    "Could I borrow {minutes} minutes to watch you try it? No prep needed, I just "
    "want to see it through fresh eyes.\n\n"
    "Proposed slot: {slot}\n"
    "Where: I will send the link ({url}) and hop on a quick call.\n\n"
    "Does that time work? Happy to move it around your day.\n\n"
    "{founder}"
)


def find_booking_rows(text):
    """Return the list of pipe-table rows under '## Booking table'. Returns an
    empty list if the heading or table is absent, never raises."""
    lines = text.splitlines()
    rows = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## booking table"):
            in_section = True
            continue
        if in_section:
            if stripped.startswith("##"):
                break  # next section, table is over
            if stripped.startswith("|"):
                rows.append(stripped)
    return rows


def parse_rows(rows):
    """Parse pipe rows into dicts. Skips the header and the |---| separator.
    Tolerates short rows and placeholder cells."""
    testers = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0].lower()
        if first in ("tester", "") or set(cells[0]) <= set("- :"):
            continue  # header or separator
        if cells[0].startswith("[") and cells[0].endswith("]"):
            continue  # unfilled template placeholder
        name = cells[0]
        channel = cells[1] if len(cells) > 1 else ""
        slot = cells[2] if len(cells) > 2 else ""
        status = cells[3].lower() if len(cells) > 3 else ""
        testers.append({"name": name, "channel": channel, "slot": slot, "status": status})
    return testers


def blank_template():
    return (
        "No booking table found, or it is still all placeholders.\n"
        "Add rows to the '## Booking table' section of your plan like this,\n"
        "then run this helper again:\n\n"
        "| Tester | Channel | Proposed slot | Status |\n"
        "|--------|---------|---------------|--------|\n"
        "| Jane Roberts | WhatsApp | Thu 3pm | drafted |\n"
    )


def main():
    ap = argparse.ArgumentParser(description="Draft usability-session booking messages")
    ap.add_argument("plan", help="Path to 04-gtm/tests/usability-test-plan.md")
    ap.add_argument("--founder", default="", help="Your name for the sign-off")
    ap.add_argument("--url", default="[your live MVP URL]", help="The live MVP URL")
    ap.add_argument("--minutes", default="30", help="Session length in minutes")
    args = ap.parse_args()

    if not os.path.exists(args.plan):
        print("Plan not found at %s." % args.plan)
        print("Write the usability test plan first, then run this helper.\n")
        print(blank_template())
        return

    with open(args.plan, "r", encoding="utf-8") as fh:
        text = fh.read()

    testers = parse_rows(find_booking_rows(text))
    pending = [t for t in testers if t["status"] != "confirmed"]

    if not testers:
        print(blank_template())
        return

    confirmed = sum(1 for t in testers if t["status"] == "confirmed")
    print("Testers in the plan: %d. Confirmed: %d. Target: 5.\n" % (len(testers), confirmed))

    if not pending:
        print("Every tester is already confirmed. Nothing to draft. Good work.")
        return

    blocks = []
    for t in pending:
        msg = MESSAGE.format(
            name=t["name"],
            minutes=args.minutes,
            slot=t["slot"] or "[propose a specific time in the next 48 hours]",
            url=args.url,
            founder=args.founder or "[your name]",
        )
        header = "--- %s (%s) ---" % (t["name"], t["channel"] or "channel?")
        blocks.append(header + "\n" + msg)

    out = "\n\n".join(blocks)
    print(out)
    print("\n" + "=" * 60)
    print("These are DRAFTS. Nothing has been sent. You press send.")
    print("A booking counts as confirmed only when the tester says yes to a time.")

    # Save alongside the plan so the drafts are not lost.
    try:
        out_path = os.path.join(os.path.dirname(os.path.abspath(args.plan)),
                                "booking-messages.md")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("# Booking messages (drafts, not sent)\n\n" + out + "\n")
        print("\nSaved a copy to %s" % out_path)
    except Exception as exc:
        print("\nCould not save a copy (%s). The messages above are still good to copy." % exc)


if __name__ == "__main__":
    main()
