#!/usr/bin/env python3
"""The one logging helper every Spark bootcamp skill calls.

Two modes, one format each. Nothing else in the plugin writes CHANGELOG.md or
DECISIONS.md by hand: it all comes through here, so the log stays consistent
and auditable.

CHANGELOG mode (the common one). Appends a single line to CHANGELOG.md:

    YYYY-MM-DD HH:MM | <skill-id> | <artefact path> | <numeric result>

and registers the same artefact in .spark/state.json via the journey-state
helper, so state and log never drift apart.

    log.py --skill d1-define-interviewees \
           --artefact 01-discovery/interview-target-spec.md \
           --result "10 interviews targeted"

DECISIONS mode. Appends a decision and its one-line rationale to DECISIONS.md:

    YYYY-MM-DD HH:MM | <decision> | <rationale>

    log.py --decision "Chose the services path" \
           --rationale "Founder already sells advisory hours; fastest to a sale"

Both files are created with a header if they do not exist. Both appends are
newest at the bottom. The script never crashes: if the journey-state helper is
missing or the state file cannot be written, it still writes the log line and
tells you what it skipped.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys


CHANGELOG_HEADER = (
    "# Changelog\n"
    "\n"
    "Every artefact this bootcamp produces is logged here, newest at the bottom.\n"
    "Format: `YYYY-MM-DD HH:MM | skill-id | artefact path | numeric result`\n"
    "\n"
)

DECISIONS_HEADER = (
    "# Decisions\n"
    "\n"
    "Key decisions and why we made them, newest at the bottom.\n"
    "Format: `YYYY-MM-DD HH:MM | decision | rationale`\n"
    "\n"
)


def now_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def find_project_root(explicit):
    """Locate the folder that holds .spark (and therefore CHANGELOG.md and
    DECISIONS.md). Prefer an explicit --root. Otherwise walk up from the
    current directory looking for a .spark folder, and fall back to cwd."""
    if explicit:
        return os.path.abspath(explicit)
    cur = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(cur, ".spark")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.getcwd()


def append_line(path, header, line):
    """Append one line, creating the file with its header if absent. Ensures a
    trailing newline on whatever was there so lines never run together."""
    try:
        exists = os.path.exists(path)
        if not exists:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(header)
        else:
            # Guarantee the previous content ends in a newline before we add.
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            if content and not content.endswith("\n"):
                with open(path, "a", encoding="utf-8") as fh:
                    fh.write("\n")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        return True, ""
    except Exception as exc:
        return False, str(exc)


def sanitise(value):
    """Keep the pipe format intact: no field may contain a bare pipe or a
    newline. Swap them for safe substitutes rather than corrupt the log."""
    return value.replace("|", "/").replace("\n", " ").replace("\r", " ").strip()


def register_artefact(root, skill, artefact_path, result):
    """Append the artefact to state.json through the journey-state helper.
    Returns (ok, note). Degrades gracefully: a missing helper or a failed run
    never stops the log line from being written."""
    helper = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "journey-state", "scripts", "update-state.py")
    )
    if not os.path.exists(helper):
        return False, "journey-state helper not found; logged to CHANGELOG only"
    payload = json.dumps({"skill": skill, "path": artefact_path, "result": result})
    state_file = os.path.join(root, ".spark", "state.json")
    try:
        proc = subprocess.run(
            [sys.executable, helper, "--file", state_file, "--append-artefact", payload],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            return False, "journey-state helper reported: %s" % (proc.stderr.strip() or "non-zero exit")
        return True, ""
    except Exception as exc:
        return False, "could not run journey-state helper (%s); logged to CHANGELOG only" % exc


def main():
    ap = argparse.ArgumentParser(description="Spark bootcamp logging helper")
    ap.add_argument("--root", help="Project root holding .spark (default: nearest .spark ancestor)")
    # CHANGELOG mode
    ap.add_argument("--skill", help="Skill id producing the artefact")
    ap.add_argument("--artefact", help="Path to the artefact, relative to the project root")
    ap.add_argument("--result", help="The numeric or observable result, e.g. '10 interviews targeted'")
    # DECISIONS mode
    ap.add_argument("--decision", help="The decision taken (switches to DECISIONS mode)")
    ap.add_argument("--rationale", help="One-line reason for the decision")
    args = ap.parse_args()

    root = find_project_root(args.root)

    changelog_mode = bool(args.skill or args.artefact or args.result)
    decision_mode = bool(args.decision or args.rationale)

    if changelog_mode and decision_mode:
        sys.stderr.write("Pick one mode: either --skill/--artefact/--result OR --decision/--rationale.\n")
        sys.exit(2)
    if not changelog_mode and not decision_mode:
        sys.stderr.write("Nothing to log. Use --skill/--artefact/--result or --decision/--rationale.\n")
        sys.exit(2)

    stamp = now_stamp()

    if decision_mode:
        if not (args.decision and args.rationale):
            sys.stderr.write("DECISIONS mode needs both --decision and --rationale.\n")
            sys.exit(2)
        line = "%s | %s | %s" % (stamp, sanitise(args.decision), sanitise(args.rationale))
        path = os.path.join(root, "DECISIONS.md")
        ok, err = append_line(path, DECISIONS_HEADER, line)
        if not ok:
            sys.stderr.write("Could not write DECISIONS.md: %s\n" % err)
            sys.exit(1)
        print("LOG_RESULT=OK decision logged to %s" % path)
        return

    # CHANGELOG mode
    if not (args.skill and args.artefact and args.result):
        sys.stderr.write("CHANGELOG mode needs --skill, --artefact and --result.\n")
        sys.exit(2)
    line = "%s | %s | %s | %s" % (
        stamp, sanitise(args.skill), sanitise(args.artefact), sanitise(args.result),
    )
    path = os.path.join(root, "CHANGELOG.md")
    ok, err = append_line(path, CHANGELOG_HEADER, line)
    if not ok:
        sys.stderr.write("Could not write CHANGELOG.md: %s\n" % err)
        sys.exit(1)

    reg_ok, note = register_artefact(root, args.skill, args.artefact, args.result)
    if reg_ok:
        print("LOG_RESULT=OK logged to %s and registered artefact in state.json" % path)
    else:
        print("LOG_RESULT=PARTIAL logged to %s but state not updated: %s" % (path, note))


if __name__ == "__main__":
    main()
