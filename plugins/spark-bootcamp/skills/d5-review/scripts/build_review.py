#!/usr/bin/env python3
"""Assemble the week into one index and score it honestly.

Reads the founder's project, finds the five core artefacts plus the deal,
pulls every headline number out of .spark/state.json, and writes two files:

  05-sale/LAUNCH-PACKAGE.md   the index: links to the five core artefacts and
                              the deal, the headline numbers, and a
                              keep-it-running section for the built MVP.
  05-sale/SCORECARD.md        target versus achieved, day by day.

Pure standard library. It never crashes: a missing state file, a missing
artefact or a missing helper all degrade to a clear note in the output and a
line on stderr. It links whatever exists and marks the rest ABSENT, honestly.

Usage:
  build_review.py --root .            # run from the founder's project root
  build_review.py --root /path/to/project

The last line it prints is the machine-readable result the skill checks:
  REVIEW_RESULT core_linked=<n>/5 deal=<present|absent> headline_numbers=<m>
"""

import argparse
import json
import os
import re
import subprocess
import sys

URL_RE = re.compile(r"https?://[^\s)\"'<>]+")

# The five core artefacts, in the order they appear in the index. Each slot has
# an ordered candidate list: the first path that exists on disk wins. Slots that
# can carry a live URL name the files to grep for one.
SLOTS = [
    {
        "key": "mvp",
        "label": "1. The MVP: the working slice, prototype or sample deliverable",
        "candidates": [
            "03-product/site/index.html",
            "03-product/BUILD-LOG.md",
            "03-product/sample-deliverable.md",
            "03-product/prototype.md",
            "03-product/prototype",
            "03-product",
        ],
        "url_from": ["03-product/BUILD-LOG.md", "03-product/site/accessibility-report.md"],
    },
    {
        "key": "pitch",
        "label": "2. The pitch deck: the investor and partner story",
        "candidates": [
            "02-market/pitch-deck.pptx",
            "02-market/pitch-deck.html",
            "02-market/deck-content.yaml",
        ],
    },
    {
        "key": "sales",
        "label": "3. The sales deck: addressed to your named buyer",
        "candidates": [
            "04-gtm/sales-deck.pptx",
            "04-gtm/sales-deck.html",
            "04-gtm/sales-deck-content.yaml",
        ],
    },
    {
        "key": "site",
        "label": "4. The brochure and live page a prospect can act on",
        "candidates": [
            "03-product/site/index.html",
            "04-gtm/landing-page.md",
            "04-gtm/funnel.md",
        ],
        "url_from": ["03-product/site/accessibility-report.md", "03-product/BUILD-LOG.md"],
    },
    {
        "key": "launch",
        "label": "5. The launch checklist: who to contact, in what order, with what message",
        "candidates": [
            "04-gtm/gtm-plan.md",
            "04-gtm/outreach-list.md",
            "04-gtm/funnel.md",
        ],
    },
]

DEAL = {
    "key": "deal",
    "label": "The deal: the ask made and the outcome",
    "candidates": [
        "05-sale/WON-DEAL.md",
        "05-sale/PROPOSAL.md",
        "05-sale/outreach-log.md",
        "05-sale/RATE-CARD.md",
    ],
}


def read_state(root):
    """Read state through the sanctioned journey-state helper. Fall back to
    reading the file directly, then to an empty default. Returns (state, note)."""
    helper = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "journey-state", "scripts", "update-state.py")
    )
    state_file = os.path.join(root, ".spark", "state.json")
    if os.path.exists(helper):
        try:
            proc = subprocess.run(
                [sys.executable, helper, "--file", state_file, "--read"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return json.loads(proc.stdout), ""
        except Exception as exc:
            pass  # fall through to direct read
    if os.path.exists(state_file):
        try:
            with open(state_file, encoding="utf-8") as fh:
                return json.load(fh), "read state.json directly (journey-state helper unavailable)"
        except Exception as exc:
            return {}, "could not parse state.json (%s); scorecard will be thin" % exc
    return {}, "no .spark/state.json found; scorecard will be thin"


def first_existing(root, candidates):
    for rel in candidates:
        if os.path.exists(os.path.join(root, rel)):
            return rel
    return None


def find_url(root, files):
    for rel in files or []:
        full = os.path.join(root, rel)
        if not os.path.exists(full) or os.path.isdir(full):
            continue
        try:
            with open(full, encoding="utf-8", errors="replace") as fh:
                head = fh.read(8000)
        except Exception:
            continue
        m = URL_RE.search(head)
        if m:
            return m.group(0).rstrip(".,)")
    return None


def resolve(root, slot):
    path = first_existing(root, slot["candidates"])
    url = find_url(root, slot.get("url_from")) if path else None
    return {"label": slot["label"], "key": slot["key"], "path": path, "url": url}


def link_cell(item):
    if not item["path"]:
        return "ABSENT"
    cell = "[`%s`](../%s)" % (item["path"], item["path"])
    if item["url"]:
        cell += " and live at [%s](%s)" % (item["url"], item["url"])
    return cell


def headline_numbers(state):
    """Every number the founder committed to and what came back. One block."""
    lines = []
    ht = state.get("headline_target") or ""
    if ht:
        lines.append("- **Headline target for the week:** %s" % ht)
    else:
        lines.append("- **Headline target for the week:** not recorded in state.json")
    days = state.get("days") or {}
    day_names = {"1": "Discovery", "2": "Market", "3": "Product", "4": "Go to market", "5": "The sale"}
    for n in ["1", "2", "3", "4", "5"]:
        d = days.get(n) or {}
        target = d.get("target") or "not set"
        outcome = d.get("outcome") or "not recorded"
        lines.append("- **Day %s (%s):** target %s, achieved %s" % (n, day_names[n], target, outcome))
    return "\n".join(lines)


def keep_it_running(state):
    """The honest hand-over for the built MVP, branched by business path. Uses
    [TO COMPLETE: ...] markers for anything the script cannot know for certain,
    the same convention the paperwork skill uses. Never invents an account."""
    bt = (state.get("business_type") or "").strip().lower()

    common_tail = (
        "\n### What you are committing to the customer\n"
        "Write this as if the customer will hold you to it, because they will. "
        "Put numbers on it.\n\n"
        "- **Response time:** [TO COMPLETE: e.g. I reply within 1 working day, "
        "Jersey hours 09:00 to 17:30.]\n"
        "- **Fix window for a breakage:** [TO COMPLETE: e.g. anything that stops "
        "the core action gets a fix inside 2 working days.]\n"
        "- **What is in scope:** [TO COMPLETE: the one workflow you built and "
        "nothing else, unless quoted separately.]\n"
        "- **What is out of scope:** [TO COMPLETE: new features, other teams, "
        "out-of-hours cover.]\n"
        "- **How they reach you:** [TO COMPLETE: the one channel, e.g. "
        "seb@yourdomain.com. Not five channels.]\n"
        "- **Review date:** [TO COMPLETE: the date you both sit down and decide "
        "whether to continue, e.g. 4 weeks from go-live.]\n"
    )

    if bt == "software":
        return (
            "## Keep it running\n\n"
            "Claude built this. That does not mean it runs itself. Here is exactly "
            "what it sits on, how to put a change live, and where the edges are.\n\n"
            "### Who owns which account\n"
            "You cannot keep it running if you cannot log in. Fill every marker "
            "today, while you still remember.\n\n"
            "| Thing | Provider | Who owns the login |\n"
            "|-------|----------|--------------------|\n"
            "| Code | GitHub | [TO COMPLETE: org/repo and the account email] |\n"
            "| Hosting | Vercel | [TO COMPLETE: account email] |\n"
            "| Database and auth | Supabase | [TO COMPLETE: project ref and account email] |\n"
            "| Domain | [TO COMPLETE: registrar] | [TO COMPLETE: account email] |\n"
            "| Email and DNS | [TO COMPLETE: provider] | [TO COMPLETE: account email] |\n\n"
            "### How to put a change live\n"
            "1. Make the change in the code.\n"
            "2. Push to the `main` branch. Vercel rebuilds and deploys on its own, "
            "usually inside 2 minutes.\n"
            "3. To force a deploy without a code change, run `vercel --prod` from "
            "the project root, or press Redeploy in the Vercel dashboard.\n"
            "4. Database changes go through a Supabase migration, not by hand in the "
            "table editor, so the change is logged and repeatable.\n\n"
            "### Known limits (read before you promise anything)\n"
            "- Free tiers have caps. A Supabase free project pauses after 7 days with "
            "no traffic, and a Vercel hobby project is for non-commercial use. Move to "
            "a paid plan (roughly £20 to £25 a month each) before a real customer "
            "relies on it.\n"
            "- There are no automated database backups unless you turned them on. "
            "[TO COMPLETE: state your backup schedule, or that there is none yet.]\n"
            "- There is one environment. A change goes straight to the customer, so "
            "test on the live URL before you tell them it is done.\n"
            "- [TO COMPLETE: any rate limits, third-party API quotas or secrets that "
            "expire.]\n"
            + common_tail
        )

    if bt == "hardware":
        return (
            "## Keep it running\n\n"
            "The prototype is a render or a mock, not a shipped unit. The live thing "
            "you must keep running is the pre-order or waitlist page and the money "
            "behind it. Here is what it sits on and where the edges are.\n\n"
            "### Who owns which account\n"
            "| Thing | Provider | Who owns the login |\n"
            "|-------|----------|--------------------|\n"
            "| CAD and render files | [TO COMPLETE: tool] | [TO COMPLETE: account email] |\n"
            "| Pre-order and deposits | Stripe (or similar) | [TO COMPLETE: account email] |\n"
            "| Waitlist and customer data | [TO COMPLETE: store] | [TO COMPLETE: account email] |\n"
            "| Site and domain | [TO COMPLETE: host and registrar] | [TO COMPLETE: account email] |\n\n"
            "### How to put a change live\n"
            "1. Update the page copy or the render, then republish the page.\n"
            "2. To change the deposit amount, edit the product or payment link in "
            "Stripe. Test it with a real card in test mode first.\n"
            "3. Keep the deposit list exportable. You will need every name and amount "
            "when units are ready.\n\n"
            "### Known limits (read before you promise anything)\n"
            "- A deposit is intent, not a delivered product. Say so on the page.\n"
            "- Your lead time is an assumption until a unit ships. [TO COMPLETE: state "
            "the lead time you quoted and how confident you are.]\n"
            "- Refund terms must be written down before you take the first deposit. "
            "[TO COMPLETE: your refund policy in one sentence.]\n"
            + common_tail
        )

    if bt == "services":
        return (
            "## Keep it running\n\n"
            "The live thing is the intake page and the sample deliverable behind it. "
            "The service is you, so the real limit is your time. Here is what it sits "
            "on and where the edges are.\n\n"
            "### Who owns which account\n"
            "| Thing | Provider | Who owns the login |\n"
            "|-------|----------|--------------------|\n"
            "| Booking and intake | [TO COMPLETE: Cal.com, Calendly, etc.] | [TO COMPLETE: account email] |\n"
            "| Payment | Stripe (or similar) | [TO COMPLETE: account email] |\n"
            "| Sample deliverable and template | [TO COMPLETE: where it lives] | [TO COMPLETE: owner] |\n"
            "| Site and domain | [TO COMPLETE: host and registrar] | [TO COMPLETE: account email] |\n\n"
            "### How to put a change live\n"
            "1. Update the package scope or price on the intake page, then republish.\n"
            "2. Change availability in the booking tool, not by email. One source of "
            "truth for when you are free.\n"
            "3. Keep the sample deliverable as a template you can reuse, so the second "
            "client takes less time than the first.\n\n"
            "### Known limits (read before you promise anything)\n"
            "- Your capacity is finite. [TO COMPLETE: how many of these you can deliver "
            "per week without dropping quality, e.g. 2.]\n"
            "- The sample is one example, not the full service. Say what changes for a "
            "real engagement.\n"
            "- [TO COMPLETE: revision rounds included in the price, and what a further "
            "round costs.]\n"
            + common_tail
        )

    # Unknown or unset path: give the software-shaped version as the structure,
    # but flag loudly that the path was not set.
    return (
        "## Keep it running\n\n"
        "**Business path not set in state.json.** This hand-over is written to the "
        "software shape as a default. Set `business_type` on Day 1 and re-run so the "
        "right version lands.\n\n"
        "### Who owns which account\n"
        "| Thing | Provider | Who owns the login |\n"
        "|-------|----------|--------------------|\n"
        "| Code | [TO COMPLETE] | [TO COMPLETE: account email] |\n"
        "| Hosting | [TO COMPLETE] | [TO COMPLETE: account email] |\n"
        "| Data | [TO COMPLETE] | [TO COMPLETE: account email] |\n"
        "| Domain | [TO COMPLETE] | [TO COMPLETE: account email] |\n\n"
        "### Known limits\n"
        "- [TO COMPLETE: what could stop this working, and who fixes it.]\n"
        + common_tail
    )


def build_launch_package(root, state, items, deal):
    linked = sum(1 for it in items if it["path"])
    total = len(items)
    ht = state.get("headline_target") or "not recorded"

    # Honest headline: did the deal land? The founder's own outcome line on Day 5
    # is the truth; we quote it rather than judge it.
    day5 = (state.get("days") or {}).get("5") or {}
    achieved = day5.get("outcome") or "not recorded"

    out = []
    out.append("# Launch package\n")
    out.append("The whole week in one place. Five core artefacts, the deal, every "
               "number you set against what came back, and how to keep the thing "
               "running after today.\n")
    out.append("## Headline\n")
    out.append("**Target:** %s  " % ht)
    out.append("**Achieved:** %s\n" % achieved)
    out.append("## The five core artefacts\n")
    out.append("| # | Artefact | Where it is |")
    out.append("|---|----------|-------------|")
    for it in items:
        num_and_rest = it["label"].split(". ", 1)
        n = num_and_rest[0]
        rest = num_and_rest[1] if len(num_and_rest) > 1 else it["label"]
        out.append("| %s | %s | %s |" % (n, rest, link_cell(it)))
    out.append("")
    out.append("## The deal\n")
    out.append("%s\n" % (link_cell(deal) if deal["path"] else
                         "ABSENT. No deal artefact found. If a real prospect was asked "
                         "to act, log it in `05-sale/WON-DEAL.md` and rebuild."))
    out.append("## Every headline number\n")
    out.append(headline_numbers(state))
    out.append("")
    out.append(keep_it_running(state))
    out.append("")
    out.append("## Proof")
    out.append("The full audit trail, every artefact with a date and a number and "
               "every decision with a reason, is in "
               "`.spark/deliverables/audit-pack.md`. Run the audit-pack skill if it "
               "is not there yet.\n")
    out.append("---")
    out.append("_Built by the Spark five-day bootcamp. This package indexes your own "
               "work; it does not warrant it._")

    path = os.path.join(root, "05-sale", "LAUNCH-PACKAGE.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return linked, total


def build_scorecard(root, state):
    ht = state.get("headline_target") or "not recorded"
    day5 = (state.get("days") or {}).get("5") or {}
    achieved = day5.get("outcome") or "not recorded"
    days = state.get("days") or {}
    day_names = {"1": "Discovery", "2": "Market", "3": "Product", "4": "Go to market", "5": "The sale"}

    numbers_stated = 0
    if state.get("headline_target"):
        numbers_stated += 1

    out = []
    out.append("# Scorecard\n")
    out.append("Target versus achieved. No spin. If a cell says \"not recorded\", the "
               "logging was thin that day, not that nothing happened. Fix the log, "
               "not the scorecard.\n")
    out.append("## The week\n")
    out.append("**Headline target:** %s  " % ht)
    out.append("**Headline achieved:** %s\n" % achieved)
    out.append("## Day by day\n")
    out.append("| Day | Target | Achieved | Signed off |")
    out.append("|-----|--------|----------|------------|")
    for n in ["1", "2", "3", "4", "5"]:
        d = days.get(n) or {}
        target = d.get("target") or "not set"
        outcome = d.get("outcome") or "not recorded"
        if d.get("target"):
            numbers_stated += 1
        signed = "yes" if d.get("complete") else "no"
        out.append("| %s. %s | %s | %s | %s |" % (n, day_names[n], target, outcome, signed))
    out.append("")
    out.append("## Your one honest sentence\n")
    out.append("[TO COMPLETE: in one sentence, did you hit the headline number, and "
               "what is the single most important thing you learned this week?]\n")
    out.append("---")
    out.append("_Spark five-day bootcamp scorecard._")

    path = os.path.join(root, "05-sale", "SCORECARD.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return numbers_stated


def main():
    ap = argparse.ArgumentParser(description="Assemble and score the Spark bootcamp week")
    ap.add_argument("--root", default=".", help="Founder's project root (holds .spark)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    state, note = read_state(root)
    if note:
        sys.stderr.write(note + "\n")

    items = [resolve(root, slot) for slot in SLOTS]
    deal = resolve(root, DEAL)

    linked, total = build_launch_package(root, state, items, deal)
    numbers = build_scorecard(root, state)

    print("Wrote 05-sale/LAUNCH-PACKAGE.md and 05-sale/SCORECARD.md")
    for it in items:
        status = it["path"] if it["path"] else "ABSENT"
        print("  %-7s -> %s" % (it["key"], status))
    print("  deal    -> %s" % (deal["path"] if deal["path"] else "ABSENT"))
    print("REVIEW_RESULT core_linked=%d/%d deal=%s headline_numbers=%d" % (
        linked, total, "present" if deal["path"] else "absent", numbers))


if __name__ == "__main__":
    main()
