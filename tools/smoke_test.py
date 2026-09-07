#!/usr/bin/env python3
"""Run the pre-work chain and the start of Day 1 for real, in a scratch project.

The linter checks structure: frontmatter, cross-skill contracts, no broken
paths. It never actually runs a skill's scripts. This does. It plays a
synthetic founder through doctor, start, and the pre-work and Day 1 skills
that have deterministic helpers, then asserts the artefacts and state.json
end up in the shape every later skill depends on.

Run from the repo root:

    python3 tools/smoke_test.py

Exit 0 when every step and every assertion passes. Exit 1 on the first
failure, with the command and the reason. CI runs this on every push, right
after the structural lint.

What it does NOT cover: the deep-conversation skills (p0-interview-triage,
d1-refine-idea, d1-interview-plan, and friends) write their artefacts from a
template Claude fills in conversation. There is no script to run for those,
so this test writes a plausible filled-in version by hand, the same shape a
real conversation would produce, then checks the mechanical parts: does the
file exist, does logging register it, does state.json end up valid.
"""

import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(REPO, "plugins", "spark-bootcamp", "skills")

JOURNEY_STATE = os.path.join(SKILLS, "journey-state", "scripts", "update-state.py")
LOGBOOK = os.path.join(SKILLS, "logbook", "scripts", "log.py")
DOCTOR_CHECK = os.path.join(SKILLS, "doctor", "scripts", "doctor-check.sh")
DOCTOR_PREWORK = os.path.join(SKILLS, "doctor", "references", "prework.md")
D1_SCAFFOLD = os.path.join(SKILLS, "d1-write-script", "scripts", "scaffold.py")

FAILURES = []


def check(label, condition, detail=""):
    if condition:
        print("  [PASS] %s" % label)
    else:
        FAILURES.append("%s%s" % (label, (": " + detail) if detail else ""))
        print("  [FAIL] %s%s" % (label, (": " + detail) if detail else ""))


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        FAILURES.append("command failed (%s): %s\n%s" % (proc.returncode, " ".join(cmd), proc.stderr))
        print("  [FAIL] command failed: %s" % " ".join(cmd))
        print(proc.stderr)
    return proc


def state_patch(root, patch):
    return run([sys.executable, JOURNEY_STATE, "--file",
                os.path.join(root, ".spark", "state.json"),
                "--patch", json.dumps(patch)])


def log_artefact(root, skill, artefact, result):
    return run([sys.executable, LOGBOOK, "--root", root,
                "--skill", skill, "--artefact", artefact, "--result", result])


def read_state(root):
    path = os.path.join(root, ".spark", "state.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write(root, rel_path, content):
    full = os.path.join(root, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return full


def main():
    tmp = tempfile.mkdtemp(prefix="spark-smoke-")
    keep = "--keep" in sys.argv
    try:
        print("Scratch project: %s\n" % tmp)

        # --- doctor: machine check, scaffold, pre-work checklist -----------
        print("doctor")
        run(["bash", DOCTOR_CHECK, tmp, DOCTOR_PREWORK])
        for d in (".spark", "00-prework", "01-discovery", "02-market",
                  "03-product", "04-gtm", "05-sale"):
            check("doctor creates %s" % d, os.path.isdir(os.path.join(tmp, d)))
        check("doctor writes CHANGELOG.md", os.path.exists(os.path.join(tmp, "CHANGELOG.md")))
        check("doctor writes DECISIONS.md", os.path.exists(os.path.join(tmp, "DECISIONS.md")))
        check("doctor writes .spark/prework.md", os.path.exists(os.path.join(tmp, ".spark", "prework.md")))
        check("doctor does not create state.json", not os.path.exists(os.path.join(tmp, ".spark", "state.json")))

        # --- start: capture the five facts, always a real future Monday ----
        print("\nstart")
        today = datetime.date.today()
        days_to_monday = (7 - today.weekday()) % 7 or 7  # next Monday, at least 14 days out
        bootcamp_monday = today + datetime.timedelta(days=days_to_monday + 14)
        state_patch(tmp, {
            "founder": "Alex",
            "business_type": "services",
            "idea": "Alex helps Jersey trust companies clear KYC backlogs so compliance teams stop missing renewal deadlines.",
            "headline_target": "one paying client at GBP 2,000+",
            "current_day": 1,
            "prework": {"bootcamp_monday": bootcamp_monday.isoformat(), "interviews_booked": 0, "complete": False},
        })
        state = read_state(tmp)
        check("state.json is the default schema plus start's patch", state.get("founder") == "Alex")
        check("business_type is a valid path", state.get("business_type") in ("software", "hardware", "services"))
        check("headline_target has a digit", any(c.isdigit() for c in state.get("headline_target", "")))
        check("bootcamp_monday is a real future Monday",
              datetime.date.fromisoformat(state["prework"]["bootcamp_monday"]) > today
              and datetime.date.fromisoformat(state["prework"]["bootcamp_monday"]).weekday() == 0)
        lead_days = (datetime.date.fromisoformat(state["prework"]["bootcamp_monday"]) - today).days
        check("pre-work lead time is at least 14 days", lead_days >= 14, "%d days" % lead_days)

        # --- p0-interview-triage: target spec (conversation, filled here) --
        print("\np0-interview-triage")
        write(tmp, "00-prework/interview-target-spec.md", (
            "# Interview Target Spec\n\n"
            "## Segment\nHeads of compliance at Jersey trust companies with 20-80 staff.\n\n"
            "## Role\nHead of Compliance\n\n"
            "## Buyer\nSame as user\n\n"
            "## Target number and reason\nTarget: 10 interviews.\nReason: single segment, one buyer, 10 is enough to see a pattern.\n\n"
            "## Screening questions\n1. Do you personally review KYC renewal files? -> yes\n"
            "2. Roughly how many renewals cross your desk a month? -> 10+\n"
            "3. Have you missed or nearly missed a renewal deadline this year? -> yes disqualifies a clean 'no'\n\n"
            "## Riskiest assumption check\nAssumption: compliance teams track renewals in spreadsheets, not their case system.\nYes, these people can prove or kill it.\n"
        ))
        log_artefact(tmp, "p0-interview-triage", "00-prework/interview-target-spec.md", "target: 10 interviews")

        # --- p0-invite-list: 20+ named, reachable people --------------------
        print("\np0-invite-list")
        rows = ["name,role_or_business,channel,contact_detail,warmth,source,notes"]
        for i in range(1, 22):
            rows.append("Contact %d,Head of Compliance,email,contact%d@example.je,warm,LinkedIn,Screens clean" % (i, i))
        write(tmp, "00-prework/invite-list.csv", "\n".join(rows) + "\n")
        log_artefact(tmp, "p0-invite-list", "00-prework/invite-list.csv", "21 named contacts")
        with open(os.path.join(tmp, "00-prework", "invite-list.csv"), encoding="utf-8") as fh:
            row_count = sum(1 for _ in fh) - 1
        check("invite list has 20+ rows", row_count >= 20, "%d rows" % row_count)

        # --- p0-invitations: drafted, never sent -----------------------------
        print("\np0-invitations")
        write(tmp, "00-prework/invitation-pack.md", (
            "# Invitation Pack\n\nInterview date: %s (afternoon), overflow %s morning.\n\n"
            "## Templates\nEmail, WhatsApp, LinkedIn variants here.\n\n"
            "## Personalised messages\n21 messages, one per contact.\n"
        ) % (state["prework"]["bootcamp_monday"],
             (datetime.date.fromisoformat(state["prework"]["bootcamp_monday"]) + datetime.timedelta(days=1)).isoformat()))
        log_artefact(tmp, "p0-invitations", "00-prework/invitation-pack.md", "21 personalised messages ready")

        # --- p0-schedule: replies tracked to 8+ booked -----------------------
        print("\np0-schedule")
        write(tmp, "00-prework/interview-schedule.md", "# Interview Schedule\n\nBooked: 8 of 10\n")
        state_patch(tmp, {"prework": {"interviews_booked": 8, "complete": True}})
        log_artefact(tmp, "p0-schedule", "00-prework/interview-schedule.md", "8 of 10 booked")
        state = read_state(tmp)
        check("pre-work closes at 8+ booked", state["prework"]["interviews_booked"] >= 8)
        check("prework.complete is true", state["prework"]["complete"] is True)

        # --- d1-refine-idea and d1-interview-plan: hand-authored -------------
        print("\nd1-refine-idea, d1-interview-plan")
        write(tmp, "01-discovery/idea-brief.md", "# Idea Brief\n\nRiskiest assumption: compliance teams track renewals in spreadsheets.\n")
        log_artefact(tmp, "d1-refine-idea", "01-discovery/idea-brief.md", "riskiest assumption named")
        write(tmp, "01-discovery/interview-plan.md", "# Interview Plan\n\n8 booked, hold 6+, floor 5.\n")
        log_artefact(tmp, "d1-interview-plan", "01-discovery/interview-plan.md", "8 interviews planned for today")
        state_patch(tmp, {"days": {"1": {"target": "hold 6+ of 8 booked interviews, floor 5"}}})

        # --- d1-write-script: the one skill with a real scaffold script -----
        print("\nd1-write-script")
        run([sys.executable, D1_SCAFFOLD, "--root", tmp])
        script_path = os.path.join(tmp, "01-discovery", "interview-script.md")
        how_to_run_path = os.path.join(tmp, "01-discovery", "how-to-run.md")
        check("scaffold writes interview-script.md", os.path.exists(script_path))
        check("scaffold writes how-to-run.md", os.path.exists(how_to_run_path))
        with open(script_path, encoding="utf-8") as fh:
            script_text = fh.read()
        check("script template is non-trivial", len(script_text.strip()) > 200, "%d chars" % len(script_text.strip()))
        log_artefact(tmp, "d1-write-script", "01-discovery/interview-script.md", "8 non-leading questions, recorder chosen")

        # --- final shape: what coach and every later skill relies on --------
        print("\nfinal state")
        state = read_state(tmp)
        check("state.json still parses as one object", isinstance(state, dict))
        check("current_day is 1", state.get("current_day") == 1)
        check("days.1.target is set", bool(state.get("days", {}).get("1", {}).get("target")))
        artefact_skills = [a.get("skill") for a in state.get("artefacts", [])]
        expected_skills = ["p0-interview-triage", "p0-invite-list", "p0-invitations",
                            "p0-schedule", "d1-refine-idea", "d1-interview-plan", "d1-write-script"]
        for skill in expected_skills:
            check("state.artefacts registered %s" % skill, skill in artefact_skills)

        changelog = os.path.join(tmp, "CHANGELOG.md")
        with open(changelog, encoding="utf-8") as fh:
            changelog_text = fh.read()
        for skill in expected_skills:
            check("CHANGELOG.md logs %s" % skill, ("| %s | " % skill) in changelog_text)

    finally:
        if keep:
            print("\n--keep passed: scratch project left at %s" % tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    print()
    if FAILURES:
        print("%d failure(s):" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        sys.exit(1)
    print("Pre-work + Day 1 smoke test: all checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
