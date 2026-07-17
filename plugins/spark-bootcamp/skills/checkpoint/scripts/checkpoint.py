#!/usr/bin/env python3
"""checkpoint.py

Bookends a day of the five-day sprint with a number. It never does the work
and it never writes state: it reads .spark/state.json (read only, walking up
the tree the same way the coach does) and prints a tight briefing so the
founder can commit to one target in the morning and record one outcome at
night. The actual writes go through the journey-state helper, invoked by the
SKILL after the founder has confirmed. Keeping the write in one place keeps
concurrent skills from clobbering the state file.

Usage: checkpoint.py <open|close> [PROJECT_ROOT]
  open   print yesterday's result, today's day target reminder, and ask the
         founder to name the ONE number they commit to today.
  close  print today's committed target next to a prompt for the actual
         outcome, then print tomorrow's first command. On Day 4 close it also
         prints the Thursday gating number: is the Friday sales meeting booked?
  PROJECT_ROOT  where the founder's project lives (default: current directory).

Exit code is always 0 unless the mode argument is missing. Read the printed
blocks, not the exit status. Stdlib only, so nothing to install.
"""

import json
import os
import sys

PLUGIN = "spark-bootcamp"


def cmd(skill_id):
    return "/{plugin}:{skill}".format(plugin=PLUGIN, skill=skill_id)


# The one-line target reminder per day, and the first command of each day so
# "close" can point at tomorrow's opening move. This mirrors the coach's
# journey map; if day skills are renamed, update both in step.
DAY_TARGET = {
    1: "develop the idea deep enough to test, then hold the interviews booked in pre-work",
    2: "size the market and stake out one position you can win",
    3: "ship the smallest slice a real prospect can act on",
    4: "one live page and an outreach list ready to send",
    5: "hit your headline number: a real customer acts",
}

FIRST_COMMAND = {
    1: cmd("d1-refine-idea"),
    2: cmd("d2-market-map"),
    3: cmd("d3-product-context"),
    4: cmd("d4-usability-plan"),
    5: cmd("d5-triage"),
}


def find_state(start):
    """Walk up from start looking for .spark/state.json. Returns its path or None."""
    here = os.path.abspath(start)
    while True:
        candidate = os.path.join(here, ".spark", "state.json")
        if os.path.isfile(candidate):
            return candidate
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent


def block(title, body):
    print(title)
    print("-" * len(title))
    print(str(body).rstrip("\n"))
    print("")


def load_state(start_dir):
    state_path = find_state(start_dir)
    if not state_path:
        block(
            "No sprint found",
            "There is no .spark/state.json in this project.\n"
            "Run  {c}  to open the sprint first.".format(c=cmd("start")),
        )
        return None, None
    try:
        with open(state_path, "r", encoding="utf-8") as fh:
            return json.load(fh), state_path
    except Exception as err:  # noqa: BLE001 - report anything, never crash
        block(
            "Cannot read the state file",
            "I found {p} but could not read it:\n  {e}\n\n"
            "Do not hand-patch it. Run  {c}  to rebuild it cleanly.".format(
                p=state_path, e=err, c=cmd("start")
            ),
        )
        return None, None


def current_day(state):
    """The first day 1..5 not signed off. None means the whole week is done."""
    days = state.get("days", {}) or {}
    for n in range(1, 6):
        d = days.get(str(n)) or {}
        if not d.get("complete"):
            return n
    return None


def day_field(state, n, field):
    d = (state.get("days", {}) or {}).get(str(n)) or {}
    return d.get(field)


def artefacts_for(state, n):
    """Artefacts whose path sits under the day n folder, newest last."""
    prefix = "0{n}-".format(n=n)
    out = []
    for a in state.get("artefacts", []) or []:
        path = a.get("path", "") or ""
        if path.startswith(prefix) or ("/0{n}-".format(n=n) in path):
            out.append(a)
    return out


def do_open(state):
    founder = (state.get("founder") or "").strip()
    hello = "{name}, ".format(name=founder) if founder else ""
    n = current_day(state)

    if n is None:
        block(
            "Nothing to open",
            "All five days are signed off. The sprint is complete.\n"
            "Your headline target was: {t}".format(
                t=state.get("headline_target", "(not recorded)")
            ),
        )
        return

    # Yesterday's result, so today builds on something real.
    if n > 1:
        prev_target = day_field(state, n - 1, "target") or "(no target was set)"
        prev_outcome = day_field(state, n - 1, "outcome") or "(no outcome recorded)"
        block(
            "Yesterday, Day {p}".format(p=n - 1),
            "Target: {t}\nOutcome: {o}".format(t=prev_target, o=prev_outcome),
        )
    else:
        block(
            "Yesterday",
            "This is Day 1. Nothing to look back on yet.\n"
            "Your week's headline target is: {t}".format(
                t=state.get("headline_target", "(not recorded)")
            ),
        )

    already = day_field(state, n, "target")
    if already:
        block(
            "Today, Day {n}, already has a target".format(n=n),
            "It is: {t}\n"
            "If that still holds, you are open. If you want to change it, name "
            "the new number and I will write it.".format(t=already),
        )
    else:
        block(
            "{h}open Day {n}".format(h=hello, n=n),
            "The shape of today is: {r}\n\n"
            "Now put ONE number on it that you commit to by tonight. One target, "
            "not three. It must be observable and countable. If you cannot name a "
            "number, we do not start the day.".format(r=DAY_TARGET.get(n, "")),
        )
    block(
        "What I need from you",
        "Say today's target as a single sentence with a digit in it. I will read "
        "it back, and only write it once you say yes.",
    )


def do_close(state):
    founder = (state.get("founder") or "").strip()
    hello = "{name}, ".format(name=founder) if founder else ""
    n = current_day(state)

    if n is None:
        block(
            "Nothing to close",
            "All five days are already signed off. The sprint is complete.",
        )
        return

    target = day_field(state, n, "target")
    if not target:
        block(
            "No target to close against",
            "Day {n} has no target on record, so there is nothing to measure. "
            "Run checkpoint open first, set today's number, then close.".format(n=n),
        )
        return

    block(
        "{h}close Day {n}".format(h=hello, n=n),
        "You committed to: {t}\n\n"
        "Now tell me the actual outcome, with the number. What really happened? "
        "Hit it, beat it or miss it, we log the truth. No rounding up.".format(t=target),
    )

    arts = artefacts_for(state, n)
    if arts:
        lines = "\n".join(
            "  - {p}  ({r})".format(p=a.get("path", "?"), r=a.get("result", "no result"))
            for a in arts
        )
        block("Artefacts logged today", lines)
    else:
        block(
            "Artefacts logged today",
            "None logged under Day {n} yet. If you produced something, make sure "
            "the day's skills logged it before you close.".format(n=n),
        )

    # Thursday gate. Day 4 close is the point of no return for the week.
    if n == 4:
        block(
            "THE THURSDAY GATE (do not skip)",
            "One question decides whether Friday is a sale or a scramble:\n\n"
            "  Is the Friday sales meeting BOOKED, with a named prospect and a "
            "time in the diary?\n\n"
            "YES: you are on track. Close Day 4 and go into Day 5 to make the ask.\n"
            "NO:  stop. Friday has no sale to close without a booked meeting. Your "
            "real Day 4 job is not done until that slot is confirmed. Fix that "
            "before you close.",
        )

    nxt = FIRST_COMMAND.get(n + 1)
    if nxt:
        block(
            "Tomorrow's first move",
            "Once I mark today complete, Day {d} opens with:\n\n  {c}\n\n"
            "Start tomorrow in a FRESH session (or run /clear first). It keeps "
            "Claude fast and cheap, and your usage lasts the week. Your progress "
            "lives on disk, so nothing is lost: open a new session, run "
            "/spark-bootcamp:coach, and I will pick up right here.".format(d=n + 1, c=nxt),
        )
    else:
        block(
            "That is the week",
            "Day 5 is the last day. Close it and the sprint is done. Then run "
            "{c} to see where you landed against your headline target.".format(
                c=cmd("coach")
            ),
        )


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("open", "close"):
        print("Usage: checkpoint.py <open|close> [PROJECT_ROOT]")
        sys.exit(2)

    mode = sys.argv[1]
    start_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

    state, _ = load_state(start_dir)
    if state is None:
        return  # a plain-English message was already printed

    if mode == "open":
        do_open(state)
    else:
        do_close(state)


if __name__ == "__main__":
    main()
