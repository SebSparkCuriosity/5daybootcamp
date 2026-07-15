#!/usr/bin/env python3
"""coach-route.py

The coach's engine. Reads .spark/state.json, works out exactly where the
founder is in the five-day sprint, and prints three things and no more:

  1. WHERE YOU ARE   the current day and its target
  2. WHAT YOU'VE DONE the days signed off and the artefacts logged so far
  3. YOUR NEXT MOVE   the ONE command to run next

It never does the work. It points. It never crashes: a missing or broken
state file is reported in plain English with the one command that fixes it,
not a stack trace.

Usage: coach-route.py [PROJECT_ROOT]
  PROJECT_ROOT  where the founder's project lives (default: current directory).
                If .spark/state.json is not found there, the script walks up
                the directory tree looking for it.

Exit code is always 0. Read the printed blocks, not the exit status.

The journey map below is the coach's single source of truth for routing. If a
day's skills ship under different ids, update the map here in one place. The
human-readable copy lives in references/journey-map.md.
"""

import json
import os
import sys

PLUGIN = "spark-bootcamp"


def cmd(skill_id):
    return "/{plugin}:{skill}".format(plugin=PLUGIN, skill=skill_id)


# The five-day chain. Each day has a short target reminder and an ordered list
# of steps. Each step names the skill to run, and the artefact that proves the
# step is done. The coach walks the chain and stops at the first step whose
# artefact does not yet exist.
JOURNEY = {
    1: {
        "name": "Discovery",
        "target": "prove real people feel the pain, from 8 to 12 interviews",
        "steps": [
            ("d1-refine-idea", "01-discovery/idea-brief.md"),
            ("d1-define-interviewees", "01-discovery/interview-target-spec.md"),
            ("d1-contact-list", "01-discovery/contact-list.md"),
            ("d1-run-interviews", "01-discovery/interview-notes.md"),
            ("d1-synthesise", "01-discovery/discovery-synthesis.md"),
        ],
    },
    2: {
        "name": "Market",
        "target": "size the market and stake out one position you can win",
        "steps": [
            ("d2-market-map", "02-market/market-map.md"),
            ("d2-competitors", "02-market/competitor-scan.md"),
            ("d2-positioning", "02-market/positioning.md"),
            ("d2-pricing", "02-market/pricing.md"),
        ],
    },
    3: {
        "name": "Product",
        "target": "ship the smallest slice a real prospect can act on",
        "steps": [
            ("d3-scope", "03-product/scope.md"),
            ("d3-brand", ".spark/brand/brand.json"),
            ("d3-build", "03-product/build-notes.md"),
        ],
    },
    4: {
        "name": "Go to market",
        "target": "one live page and an outreach list ready to send",
        "steps": [
            ("d4-offer", "04-gtm/offer.md"),
            ("d4-landing", "04-gtm/landing-page.md"),
            ("d4-outreach", "04-gtm/outreach-list.md"),
        ],
    },
    5: {
        "name": "The sale",
        "target": "hit your headline number: a real customer acts",
        "steps": [
            ("d5-send", "05-sale/outreach-log.md"),
            ("d5-close", "05-sale/sale.md"),
        ],
    },
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
    print(body.rstrip("\n"))
    print("")


def not_started():
    block(
        "Where you are",
        "You have not started yet. There is no .spark/state.json in this project.",
    )
    block(
        "What you have finished",
        "Nothing logged yet, and that is fine. Everyone starts here.",
    )
    block(
        "Your next move",
        "Run  {c}\n\nThat captures your name, your path, your one-sentence idea and "
        "your numeric target for the week, and opens the journey.".format(c=cmd("start")),
    )


def broken_state(path, err):
    block(
        "Where you are",
        "I found {p} but could not read it:\n  {e}".format(p=path, e=err),
    )
    block(
        "What you have finished",
        "I cannot tell until the state file reads cleanly.",
    )
    block(
        "Your next move",
        "The state file is the spine of the whole week, so do not hand-patch it.\n"
        "Run  {c}  to re-open the sprint and rebuild it cleanly.".format(c=cmd("start")),
    )


def artefact_present(project_root, state, path):
    """A step is done if its artefact exists on disk OR is logged in state."""
    if os.path.exists(os.path.join(project_root, path)):
        return True
    for a in state.get("artefacts", []) or []:
        if a.get("path") == path:
            return True
    return False


def main():
    start_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    state_path = find_state(start_dir)
    if not state_path:
        not_started()
        return

    project_root = os.path.dirname(os.path.dirname(state_path))

    try:
        with open(state_path, "r", encoding="utf-8") as fh:
            state = json.load(fh)
    except Exception as err:  # noqa: BLE001 - report anything, never crash
        broken_state(state_path, err)
        return

    founder = (state.get("founder") or "").strip()
    hello = "{name}, ".format(name=founder) if founder else ""
    days = state.get("days", {}) or {}

    def day_complete(n):
        d = days.get(str(n)) or {}
        return bool(d.get("complete"))

    # Current day: the first day 1..5 that is not signed off.
    current = None
    for n in range(1, 6):
        if not day_complete(n):
            current = n
            break

    # ---- WHERE YOU ARE ----------------------------------------------------
    if current is None:
        block(
            "Where you are",
            "{h}all five days are signed off. Day 5, the sale, is done.\n"
            "Your headline target was: {t}".format(
                h=hello, t=state.get("headline_target", "(not recorded)")
            ),
        )
    else:
        meta = JOURNEY[current]
        block(
            "Where you are",
            "{h}you are on Day {n}: {name}.\n"
            "The point of today: {target}.\n"
            "Your week's headline target: {ht}".format(
                h=hello,
                n=current,
                name=meta["name"],
                target=meta["target"],
                ht=state.get("headline_target", "(not recorded)"),
            ),
        )

    # ---- WHAT YOU'VE FINISHED --------------------------------------------
    done_lines = []
    completed_days = [n for n in range(1, 6) if day_complete(n)]
    if completed_days:
        done_lines.append(
            "Days signed off: "
            + ", ".join("Day {n} ({name})".format(n=n, name=JOURNEY[n]["name"]) for n in completed_days)
        )
    else:
        done_lines.append("No day is fully signed off yet.")

    artefacts = state.get("artefacts", []) or []
    done_lines.append("Artefacts logged so far: {n}".format(n=len(artefacts)))
    if artefacts:
        for a in artefacts[-3:]:
            done_lines.append("  - {p} ({r})".format(p=a.get("path", "?"), r=a.get("result", "")))
        if len(artefacts) > 3:
            done_lines.append("  (showing the last 3)")

    block("What you have finished", "\n".join(done_lines))

    # ---- YOUR NEXT MOVE ---------------------------------------------------
    if current is None:
        block(
            "Your next move",
            "Nothing. You are done. Log the win, tell Seb at Spark, and go celebrate.\n"
            "If you want to line up the next customer, start a fresh sprint with  {c}.".format(
                c=cmd("start")
            ),
        )
        return

    meta = JOURNEY[current]
    next_step = None
    for skill_id, artefact in meta["steps"]:
        if not artefact_present(project_root, state, artefact):
            next_step = (skill_id, artefact)
            break

    if next_step is None:
        # Every step's artefact exists, but the day is not signed off.
        block(
            "Your next move",
            "Every step of Day {n} has produced its artefact, but the day is not signed "
            "off yet. Run the last skill in the chain again to confirm and mark Day {n} "
            "complete, then come back to me:\n\n  {c}".format(
                n=current, c=cmd(meta["steps"][-1][0])
            ),
        )
        return

    skill_id, artefact = next_step
    block(
        "Your next move",
        "Run  {c}\n\nThat is the next step of Day {n}. It writes  {art}.\n"
        "Do that one thing, then run me again and I will point you at the next.".format(
            c=cmd(skill_id), n=current, art=artefact
        ),
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as err:  # noqa: BLE001 - last-resort net, never crash on the founder
        print("Where you are")
        print("-------------")
        print("The coach hit an unexpected snag: {e}".format(e=err))
        print("")
        print("Your next move")
        print("--------------")
        print("Run  {c}  to check your setup, then run the coach again.".format(c=cmd("doctor")))
    sys.exit(0)
