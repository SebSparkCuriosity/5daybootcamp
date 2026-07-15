---
name: Triage The Fixes
description: Sorts Day 4 feedback into Fix Now (max 3, each under 90 minutes), Park and Roadmap, so you ship the right three changes before you sell. Use first thing on Day 5.
when_to_use: Day 5, straight after Day 4 gtm feedback, before you touch the live page or send anything to a prospect.
---

# Triage The Fixes

**What this does.** Turns your pile of Day 4 feedback into a ruthless three-item fix list, with everything else parked or roadmapped so it stops nagging you.
**Why it matters.** On Day 5 you have hours, not days, and one job: get a real prospect to act on your live page. Feedback always outruns time. Founders who try to fix everything ship nothing. Pick the three changes that move a buyer, do them fast, and let the rest wait.
**You are ready for this when.** `04-gtm/feedback-synthesis.md` exists.

## Before you start
Read `04-gtm/feedback-synthesis.md` in full. Read `.spark/state.json` for your `headline_target` and `business_type`. Note your Day 5 target: it is the tie-breaker whenever two items compete for a Fix Now slot.

Guardrail: this skill only classifies. It does not change your page, spend money or contact anyone. Building the fixes comes next, after you have signed off this list.

## Steps
1. List every distinct item from the synthesis. One line each, plain language. Merge duplicates. If two people said the same thing, that counts once but note it, repetition matters later.
2. Score each item on two things, 1 to 3. Impact: how much does fixing this help a real prospect say yes today? Effort: your honest estimate in minutes to a done, live change. Anything you cannot estimate is a Roadmap item by default, because unknown effort on Day 5 is a trap.
3. Sort into three buckets using this rule, in order:
   - **Fix Now**: high impact (3), and under 90 minutes each. Maximum three items. If more than three qualify, keep the three that best serve your Day 5 target and demote the rest to Park.
   - **Park**: real, worth doing, but not today. It waits until after your first sale.
   - **Roadmap**: bigger bets, unknown effort, or anything needing money or another person. Write it down so it is safe to ignore this week.
4. Total the Fix Now minutes. If the three add up to more than your remaining build time, cut the weakest one to Park. Two solid fixes beat three rushed ones.
5. Branch by path and sanity-check the Fix Now list against what a buyer actually touches:

## For software
Favour fixes on the live page the prospect lands on: the headline, the one call to action, a broken signup, a confusing price. A backend refactor is Park unless it visibly breaks the slice.

## For hardware
Favour the render, the pre-order or waitlist page, and the payment intent flow. If the CAD looks unfinished or the pre-order button does not take a real intent, that is a Fix Now. Tooling and materials questions are Roadmap.

## For services
Favour the sample deliverable and the bookable intake page. If the sample is thin or the booking link is fiddly, Fix Now. Adding a second package is Park.

6. Write each Fix Now item as an instruction you could hand to someone else: what changes, where, and the observable result. Vague fixes overrun.

## The artefact
Writes `05-sale/TRIAGE.md` in Markdown. Use the template in `references/triage-template.md`. Good looks like: every synthesis item appears exactly once, a three-column or three-section split, Fix Now holding at most three items each with an effort estimate under 90 minutes and a total, and a one-line reason for each Park and Roadmap call. Record the reasoning for anything non-obvious in `DECISIONS.md` too.

To check your work, run the validator:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/check-triage.py 05-sale/TRIAGE.md
```

It confirms Fix Now has at most three items and each is under 90 minutes, and prints a clear pass or fail.

## Done when
Every synthesis item is classified into exactly one bucket, Fix Now holds three items or fewer, each Fix Now item carries an effort estimate under 90 minutes, and the validator prints PASS.

## Log it
Append one line to CHANGELOG.md via the logbook helper, with the artefact path and the numeric result (the Fix Now count and total minutes):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-triage \
  --artefact 05-sale/TRIAGE.md \
  --result "Fix Now: 3 items, 210 min total; 5 parked, 4 roadmapped"
```

Then update state via the journey-state helper, marking Day 5 progress:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"outcome":"triaged; 3 fixes queued","complete":true}}}'
```

## If it goes wrong
No feedback worth acting on? That is a finding, not a failure. Write TRIAGE.md with an empty Fix Now list and a one-line note saying the page is good enough to sell as is, then move straight to building the sale. Too much feedback and everything feels urgent? Force the ranking: score impact honestly, keep only the top three, and trust that Park is not the same as never.
