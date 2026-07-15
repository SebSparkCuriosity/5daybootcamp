#!/usr/bin/env python3
"""Scaffold one interview record for the Spark bootcamp.

The interview engine is a live companion first and a record second. This
script does the record half: it creates ONE structured file at the right path
for the mode, pre-filled with the consent log, the context block, three empty
verbatim-quote slots, the job/pain section, and (in product-test mode) the
buying-signal score with its rubric. You fill it during and just after the
call. The file is the auditable artefact; the running prompt sheet lives in
references/.

Two modes, two paths:
  discovery      -> 01-discovery/interviews/<name>.md
  product-test   -> 04-gtm/tests/sessions/session-NN.md   (NN auto-increments)

Consent wording is reused from data-protection. The script prefers the
founder's own filled copy at .spark/deliverables/data-protection/consent.md;
if that is missing it falls back to the plugin's consent reference; if that
too is missing it embeds a short built-in block. It never crashes: a missing
state file, a missing consent file or a missing library all degrade to a clear
message and a working record.

Usage:
  # Discovery interview, names the file after the interviewee (or a pseudonym)
  new_session.py --mode discovery --name "alex-trust-officer" --root .

  # Product test, auto-numbers the session
  new_session.py --mode product-test --root .

  # Force a specific session number
  new_session.py --mode product-test --session 3 --root .
"""

import argparse
import datetime
import os
import re
import sys


BUILTIN_CONSENT = (
    '"Thanks for making time. Before we begin: I would like to take notes, '
    "and I may record this call so I do not miss anything. The notes stay in "
    "local files under my control. I will use them only to understand the "
    "problem I am researching. I will not share your name or anything that "
    "identifies you outside this work without asking you first. You can stop "
    "at any time, skip any question, and ask me to delete your notes "
    'afterwards. Is that alright, and are you happy for me to record?"'
)


def now_date():
    return datetime.date.today().isoformat()


def find_root(start):
    """Walk up from start until a .spark dir is found; else return start."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".spark")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start)
        cur = parent


def read_state(root):
    """Best-effort read of state.json. Never raises."""
    path = os.path.join(root, ".spark", "state.json")
    try:
        import json
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def load_consent(root):
    """Return (consent_text, source_label). Tries three sources in order."""
    # 1. The founder's own filled draft.
    own = os.path.join(root, ".spark", "deliverables", "data-protection", "consent.md")
    block = extract_interview_block(own)
    if block:
        return block, "your filled consent.md"

    # 2. The plugin reference (this script lives in the plugin tree).
    here = os.path.dirname(os.path.abspath(__file__))
    plugin_ref = os.path.normpath(
        os.path.join(here, "..", "..", "data-protection", "references", "consent.md")
    )
    block = extract_interview_block(plugin_ref)
    if block:
        return block, "the plugin consent reference"

    # 3. Built-in fallback.
    return BUILTIN_CONSENT, "the built-in fallback (run data-protection to get your own)"


def extract_interview_block(path):
    """Pull the interview-consent paragraph out of a consent.md file.

    Returns the quoted script under the '## Interview consent' heading, or None.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return None
    # Grab the first quoted "..." after the interview-consent heading.
    m = re.search(r"##\s*Interview consent.*?\n(.*?)(?:\n##|\Z)", text, re.S | re.I)
    chunk = m.group(1) if m else text
    q = re.search(r'"(.+?)"', chunk, re.S)
    if q:
        return '"' + q.group(1).strip() + '"'
    return None


def next_session_number(sessions_dir):
    """Highest existing session-NN + 1, or 1 if none / unreadable."""
    try:
        nums = []
        for fn in os.listdir(sessions_dir):
            m = re.match(r"session-(\d+)\.md$", fn)
            if m:
                nums.append(int(m.group(1)))
        return (max(nums) + 1) if nums else 1
    except Exception:
        return 1


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "interviewee"


def discovery_record(founder, business, consent_text, consent_source):
    return f"""# Discovery interview

Founder: {founder or "[TO COMPLETE]"}
Business: {business or "[TO COMPLETE]"}
Date: {now_date()}
Mode: discovery

## Consent (log this before you start)
Read aloud or show, from {consent_source}:

> {consent_text}

Record the four fields. Do not start until consent is a clear yes.

| Field | Value |
|---|---|
| Interviewee (first name or pseudonym) | [TO COMPLETE] |
| Date consent given | {now_date()} |
| Consent given (yes / no) | [TO COMPLETE] |
| Recording allowed (yes / no) | [TO COMPLETE] |

If recording is a no, take written notes only. Keep this file local.

## Context
Who they are, the kind of place they work, and the situation that triggered
the problem. Two or three sentences. Facts, not your interpretation yet.

[TO COMPLETE]

## Verbatim quotes (need 3 or more)
Their exact words, not your paraphrase. A quote earns its place when it is
about something that actually happened, not a hypothetical. Aim for the past
tense: "last month I had to...", not "I would probably...".

1. "[TO COMPLETE]"
2. "[TO COMPLETE]"
3. "[TO COMPLETE]"

## The job and the pain observed
What were they really trying to get done, and what did the current way cost
them (time, money, risk, stress)? Name the job in their language. Note what
they use today and where it breaks.

[TO COMPLETE]

## Signal seen (behaviour, not compliments)
What did they DO about this problem already? Money spent, tools tried, a
workaround built, someone they asked. Behaviour is signal; "sounds great" is
noise.

[TO COMPLETE]

## Next step
Any concrete ask you made and their answer (a referral, a follow-up, a look at
what they use now).

[TO COMPLETE]
"""


def product_test_record(session_no, founder, business, consent_text, consent_source):
    return f"""# Product-test session {session_no:02d}

Founder: {founder or "[TO COMPLETE]"}
Business: {business or "[TO COMPLETE]"}
Date: {now_date()}
Mode: product-test

## Consent (log this before you start)
Read aloud or show, from {consent_source}:

> {consent_text}

Record the four fields. Do not start until consent is a clear yes.

| Field | Value |
|---|---|
| Tester (first name or pseudonym) | [TO COMPLETE] |
| Date consent given | {now_date()} |
| Consent given (yes / no) | [TO COMPLETE] |
| Recording allowed (yes / no) | [TO COMPLETE] |

If recording is a no, take written notes only. Keep this file local.

## Context
Who the tester is and how close they are to your real buyer. What you put in
front of them (the live page, prototype or sample deliverable) and the one
task you asked them to attempt.

[TO COMPLETE]

## Verbatim quotes (need 3 or more)
Their exact words as they used the thing. Capture confusion, surprise and the
moment they understood the price. Real words, not your summary.

1. "[TO COMPLETE]"
2. "[TO COMPLETE]"
3. "[TO COMPLETE]"

## The job and the pain observed
Did the thing move the job forward for them, and where did it stall? Note the
exact step where they hesitated or got stuck.

[TO COMPLETE]

## Buying-signal score: __ / 5
Score what they DID, not what they said. Commitment means giving up something
real: money, a firm date, a name, their reputation. See the rubric below and
in references/buying-signal-rubric.md.

0  Polite. Compliments only. No action offered.
1  Interest. Asked to be kept posted, nothing given.
2  Time. Agreed a specific follow-up or to try it properly.
3  Reputation. Gave a warm intro or their name as a reference.
4  Intent. Signed a waitlist, pre-order or letter of intent with real details.
5  Money. Paid, deposited, or committed a purchase order now.

Evidence for the score (the specific action, in one line):

[TO COMPLETE]

## Next step
The concrete ask you made and their answer.

[TO COMPLETE]
"""


def main():
    ap = argparse.ArgumentParser(description="Scaffold one Spark interview record.")
    ap.add_argument("--mode", required=True, choices=["discovery", "product-test"])
    ap.add_argument("--name", help="Interviewee slug for discovery mode (a first name or pseudonym)")
    ap.add_argument("--session", type=int, help="Force a product-test session number")
    ap.add_argument("--root", default=".", help="Project root holding .spark (default: nearest ancestor)")
    args = ap.parse_args()

    root = find_root(args.root)
    state = read_state(root)
    founder = state.get("founder", "")
    business = ""  # the founder fills the business line; brand name lives in brand.json
    consent_text, consent_source = load_consent(root)

    if args.mode == "discovery":
        name = args.name or "interviewee"
        slug = slugify(name)
        out_dir = os.path.join(root, "01-discovery", "interviews")
        rel = os.path.join("01-discovery", "interviews", slug + ".md")
        body = discovery_record(founder, business, consent_text, consent_source)
    else:
        out_dir = os.path.join(root, "04-gtm", "tests", "sessions")
        num = args.session if args.session else next_session_number(out_dir)
        rel = os.path.join("04-gtm", "tests", "sessions", "session-%02d.md" % num)
        body = product_test_record(num, founder, business, consent_text, consent_source)

    out_path = os.path.join(root, rel)
    if os.path.exists(out_path):
        sys.stderr.write(
            "A record already exists at %s. Not overwriting. "
            "Delete it or pick another name/session to start fresh.\n" % rel
        )
        sys.exit(1)

    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(body)
    except Exception as e:
        sys.stderr.write("Could not write the record: %s\n" % e)
        sys.exit(1)

    print("Wrote %s" % rel)
    print("Consent wording pulled from: %s" % consent_source)
    print("Fill it live, then this record is done when it has consent logged "
          "and 3+ verbatim quotes"
          + (" and a buying-signal score with evidence." if args.mode == "product-test" else "."))


if __name__ == "__main__":
    main()
