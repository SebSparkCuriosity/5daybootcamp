---
name: Triage The Fixes
description: Sorts Day 4 feedback into Fix Now (max 3, each under 90 min), Park and Roadmap, so you ship the right three changes before you sell.
when_to_use: Day 5, straight after Day 4 gtm feedback, before you touch the live page or sell.
---

# Triage The Fixes

**What this does.** Turns your Day 4 feedback into a ruthless three-item fix list, with everything else parked or roadmapped.
**Why it matters.** On Day 5 you have hours and one job: get a real prospect to act on your live page, so fixing everything means shipping nothing.
**You are ready for this when.** `04-gtm/feedback-synthesis.md` exists.

## Before you start
Read `04-gtm/feedback-synthesis.md` in full. Read `.spark/state.json` for `headline_target` and `business_type`; your Day 5 target is the tie-breaker between competing Fix Now items. The Fix Now list is the founder's call (10 minutes): you score and propose, they choose the three, and a swap against the numbers gets its reason in DECISIONS.md. This skill only classifies: it does not change your page, spend money or contact anyone.

## Steps
1. List every distinct item from the synthesis, one line each. Merge duplicates but note repetition.
2. Score each 1 to 3 on Impact (does fixing it make a prospect say yes today?) and Effort (honest minutes to a live change). Anything you cannot estimate goes to Roadmap.
3. Bucket in this order:
   - **Fix Now**: impact 3 and under 90 minutes each. Max three. If more qualify, keep the three that best serve your Day 5 target.
   - **Park**: real, worth doing, but waits until after your first sale.
   - **Roadmap**: bigger bets, unknown effort, or anything needing money or another person.
4. Total the Fix Now minutes. If they exceed your remaining build time, cut the weakest to Park.
5. Branch and sanity-check the Fix Now list against what a buyer touches:

## For software
Favour the live page: headline, the one call to action, broken signup, confusing price. Backend refactors are Park unless they visibly break the slice.

## For hardware
Favour the render, pre-order or waitlist page, and payment intent flow. Unfinished CAD or a button not taking real intent is Fix Now. Tooling and materials are Roadmap.

## For services
Favour the sample deliverable and the bookable intake page. Thin sample or fiddly booking link is Fix Now. A second package is Park.

6. Write each Fix Now item as a handoff instruction: what changes, where, and the observable result.

## The artefact
Writes `05-sale/TRIAGE.md` in Markdown, using `references/triage-template.md`. Every synthesis item appears once; three sections; Fix Now holds at most three items each with an under-90-min estimate plus a total; one-line reason for each Park and Roadmap. Record non-obvious calls in `DECISIONS.md`. Validate:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/check-triage.py 05-sale/TRIAGE.md
```

## Done when
Every synthesis item is in exactly one bucket, Fix Now holds three or fewer, each Fix Now item has an estimate under 90 minutes, and the validator prints PASS.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-triage \
  --artefact 05-sale/TRIAGE.md \
  --result "Fix Now: 3 items, 210 min total; 5 parked, 4 roadmapped"
```

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"outcome":"triaged; 3 fixes queued"}}}'
```

## If it goes wrong
No feedback worth acting on? Write TRIAGE.md with an empty Fix Now list and a note that the page is good enough to sell as is, then build the sale. Everything feels urgent? Force the ranking, keep the top three, and trust that Park is not never.
