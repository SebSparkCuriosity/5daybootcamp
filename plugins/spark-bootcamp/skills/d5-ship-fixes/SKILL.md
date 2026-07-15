---
name: Ship The Fixes
description: Ship the three triage fixes, prove the demo happy path runs end to end once, then commit with a timestamp. Day 5, after triage.
when_to_use: Day 5, after triage, before d4-book-sale. Triggers "ship the fixes", "make the demo work", "demo-ready".
argument-hint: [optional-commit-message]
---

# Ship The Fixes

**What this does.** Builds the three triage fixes, runs the demo from first click to value moment once, and commits with a timestamp.
**Why it matters.** Friday is not for new features: it is for making one clean route work so a real person can watch it and believe it.
**You are ready for this when.** `05-sale/TRIAGE.md` names the three fixes and your Day 3 MVP is live.

## Before you start
Read, in order: `05-sale/TRIAGE.md` (the only three fixes; if missing, take the top 3 flagged **BUILD FRIDAY** in `04-gtm/feedback-synthesis.md`), the Day 3 live URL and repo in `03-product/BUILD-LOG.md`, `.spark/state.json` for `business_type`, `.spark/brand/brand.json`.

Two hard rules. Three fixes, no more: a genuine fourth must displace one in TRIAGE.md with a reason in DECISIONS.md. Pause for sign-off before you spend or send: deploying is fine, but switching Stripe test to live, buying, or messaging the buyer waits for d4-book-sale. Hard stop **14:00 Friday**: after that, take the fallback below.

## Steps
1. Copy the three fixes into a worklist: one line each (what, "done" looks like, which screen).
2. Take ONE fix, describe it in a sentence, make the change, check it on the running MVP. Commit after each fix so you can roll back.
3. When all three are in, write the demo script from `${CLAUDE_SKILL_DIR}/references/demo-script-template.md`: one route in, one route out, ending on the value moment.
4. Prove it: run the happy path top to bottom, as a stranger would, once, on the live thing. Do not skip, do not fix as you go.
5. If it breaks, that break is your next fix. Fix, then restart the happy path from the top. It counts only when one unbroken run reaches the value moment.
6. Deploy, then commit with a timestamp via the helper below.

## For software
Make each fix, run locally, deploy to the same Day 3 Vercel URL (no new URL, no spend). Happy path is the one PRD action live: land, act, see the result recorded. Run it on phone and laptop. Good: a stranger opens the URL, follows the script, the result lands where you can point at it.

## For hardware
Fixes usually land on the page or render, not the mock. Happy path: show render or mock, tell the promise, take the buyer through leaving real intent (email, or refundable deposit in Stripe test mode; a live key waits for d4-book-sale). Good: the prototype reads as real and you complete the capture yourself on the live page.

## For services
Fixes usually sharpen the sample or the intake form. Happy path: walk the sample deliverable, state the package and one fixed price, take them through the live intake or booking. Good: the sample stands up and you book a slot yourself to prove it submits.

## The artefact
The updated MVP: three fixes live at the Day 3 URL, committed with a timestamp. Plus `05-sale/DEMO-SCRIPT.md` from the template: happy path, setup, payoff line, untouched routes, live-recovery plan. Commit:
```
bash ${CLAUDE_SKILL_DIR}/scripts/commit-fixes.sh "closes top 3 triage fixes"
```
It stamps `[YYYY-MM-DD HH:MM]` and prints the short hash. If the MVP is not a git repo, it exits cleanly: log the artefact time by hand.

## Done when
- The three TRIAGE.md fixes are shipped and live at the Day 3 URL. Not two, not four. Three.
- The demo happy path runs end to end **once**, unbroken, first click to value moment, on the live thing.
- The changes are committed with a timestamp (hash and time), or the artefact time is logged for a non-repo MVP.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-ship-fixes \
  --artefact 05-sale/DEMO-SCRIPT.md \
  --result "3 fixes shipped, demo happy path verified end to end, commit <short-hash> at <HH:MM>"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"5": {"outcome": "3 fixes shipped, demo verified, commit <short-hash>", "complete": false}}}'
```
Leave Day 5 `complete` false: done when the sale is booked. If a fourth fix displaced one, note which and why in DECISIONS.md.

## If it goes wrong
- **14:00 and not all three in.** Ship what you have, cut the script to a happy path using only what works, note the unshipped fix as a fast-follow in DEMO-SCRIPT.md.
- **Happy path will not run clean.** Make the breaking step your one fix, even if it drops a lower-ranked item. Reaching the value moment beats three fixes and a broken run.
- **Commit fails.** Usually an unset git identity: the helper prints the two `git config` lines. Set them, re-run. If the MVP is not code, the changelog timestamp is your audit trail.
- **Nothing live to fix (Day 3 slipped).** Use the Day 3 minimum-shippable fallback: one live page with one working action on a public URL, then demo that.
