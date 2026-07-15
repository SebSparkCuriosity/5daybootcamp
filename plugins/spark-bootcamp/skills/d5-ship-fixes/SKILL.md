---
name: Ship The Fixes
description: Ships the three triage fixes and proves the demo happy path runs end to end once, then commits with a timestamp. Use on Day 5 after triage, before you get in front of the buyer.
when_to_use: Day 5 sale, straight after the triage that picked the three fixes, before d4-book-sale puts you in front of a real buyer. Trigger on "ship the fixes", "make the demo work", "get it demo-ready".
argument-hint: [optional-commit-message]
---

# Ship The Fixes

**What this does.** Builds the three fixes from your triage, then runs the demo from the buyer's first click to the value moment, once, all the way through, and commits the lot with a timestamp.
**Why it matters.** Friday is not the day to add features. It is the day to make one clean route work so a real person can watch it and believe it. Three fixes, not thirty. A demo that runs once, on purpose, beats a product that half-works in ten places. If the happy path breaks in front of the buyer, the sale dies, so you prove it first, alone.
**You are ready for this when.** `05-sale/TRIAGE.md` exists and names the three fixes, and your MVP is live from Day 3.

## Before you start
Read these, in this order:
- `05-sale/TRIAGE.md`: the three fixes, ranked. These are the only three you build today. If this file is missing, fall back to the top 3 flagged **BUILD FRIDAY** in `04-gtm/feedback-synthesis.md`. Do not invent a fourth.
- Your MVP: the live URL and repo from Day 3 (`03-product/BUILD-LOG.md` records both).
- `.spark/state.json`: read `business_type`. It decides what "the demo" means below.
- `.spark/brand/brand.json`: so any new screen still looks like you.

Two hard rules for today.
- **Three fixes. No more.** Every extra thing you touch is a new way to break the demo an hour before the call. If a fourth idea is genuinely a must, it displaces one of the three in TRIAGE.md, in writing, with a reason in DECISIONS.md. The count stays at three.
- **You pause for sign-off before you spend or send.** Deploying a fix is fine. Switching a Stripe test key to live, buying anything, or messaging the buyer waits for the founder to say yes. That sign-off belongs to d4-book-sale, not here.

Set a hard stop: **14:00 Friday**. If the three fixes are not shipped and the demo not proven by then, you switch to the fallback at the bottom. You still walk into the call with something that runs.

## Steps
1. Copy the three fixes out of TRIAGE.md into a short worklist. One line each: what it is, what "done" looks like, which screen or step it touches.
2. Take ONE fix. Tell Claude what it is in one sentence and let it make the change. Small edits, one fix at a time. After each, look at it with your own eyes on the running MVP.
3. Commit after each fix so you can roll back cleanly if the next one breaks something. Use the fix name in the message.
4. When all three are in, write the demo script: the exact happy path you will run in front of the buyer, and nothing else. Use the template at `${CLAUDE_SKILL_DIR}/references/demo-script-template.md`. One route in, one route out, ending on the value moment.
5. Now prove it. Run the happy path from the top, as a stranger would, once, all the way through, on the live thing. Do not skip a step. Do not fix as you go. Either it runs end to end or it does not.
6. If it breaks, that break is your next fix. Fix it, then start the happy path again from step one. It only counts when a single unbroken run reaches the value moment.
7. Deploy the updated MVP and commit everything with a timestamp using the helper below. The timestamp is your audit trail: it shows exactly when Friday's fixes landed.

## For software
The MVP is the deployed slice. "The demo" is a live click-through on the public URL.
- Make each fix, run it locally, then deploy to the same Vercel URL from Day 3. No new URL, no spend.
- The happy path is the one action from your PRD, start to finish, on the live site: land, act, see the result recorded. Run it once on your phone as well as your laptop, because the buyer will be looking at a screen you do not control.
- Good looks like: a stranger opens the URL, follows your demo script, and the result lands where you can point at it (a row in Supabase, a confirmation on screen).

## For hardware
The MVP is the prototype plus the pre-order or waitlist page. "The demo" is the story of the product plus a real act of intent.
- Fixes usually land on the page or the render, not the physical mock: a clearer hero shot, a sharper promise, a capture that actually fires.
- The happy path is: show the render or mock, tell the promise, then take the buyer through leaving real intent on the live page (an email, or a refundable deposit in Stripe test mode). A live deposit key waits for sign-off in d4-book-sale.
- Good looks like: the prototype reads as real, and you complete the capture yourself on the live page, seeing the intent recorded.

## For services
The MVP is the sample deliverable plus the bookable intake page. "The demo" is showing the finished work, then booking.
- Fixes usually sharpen the sample (make the one deliverable genuinely good) or the intake (make the booking form actually submit).
- The happy path is: walk the buyer through the sample deliverable, state the package and the one fixed price, then take them through the intake or booking on the live page.
- Good looks like: the sample stands up to scrutiny, and you book a slot yourself through the live form to prove it submits.

## The artefact
Two things.
1. The updated MVP: the three fixes shipped and live at the Day 3 URL, committed with a timestamp. The commit hash and time are the record that Friday's work landed.
2. `05-sale/DEMO-SCRIPT.md` (Markdown), from the template: the happy path, the setup, the payoff line, the routes you do not touch, and a recovery plan if it breaks live.

Commit the updated MVP with a timestamp:
```
bash ${CLAUDE_SKILL_DIR}/scripts/commit-fixes.sh "closes top 3 triage fixes"
```
It stages everything, commits with your message and a `[YYYY-MM-DD HH:MM]` stamp, and prints the short hash. If the MVP is not a git repo (a services sample, a hardware mock), it says so and exits cleanly: record the artefact time in the changelog by hand instead.

## Done when
- The three fixes from TRIAGE.md are shipped and live at the Day 3 URL. Not two, not four. Three.
- The demo happy path runs end to end **once**, unbroken, from first click to the value moment, on the live thing, following DEMO-SCRIPT.md.
- The changes are committed with a timestamp (you have the commit hash and the time), or, for a non-repo MVP, the artefact time is logged.

## Log it
Append one line to CHANGELOG.md via the logbook helper:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-ship-fixes \
  --artefact 05-sale/DEMO-SCRIPT.md \
  --result "3 fixes shipped, demo happy path verified end to end, commit <short-hash> at <HH:MM>"
```
Then set the Day 5 outcome via the journey-state helper (it takes an RFC 7386 merge patch):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"5": {"outcome": "3 fixes shipped, demo verified, commit <short-hash>", "complete": false}}}'
```
Leave Day 5 `complete` false: the day is done when the sale is booked, not when the demo runs. If a fourth fix displaced one of the three, add a line to DECISIONS.md saying which and why.

## If it goes wrong
- **14:00 Friday and the three fixes are not all in.** Ship the fixes you have, then cut the demo script down to a happy path that only uses what works. A shorter demo that runs beats a longer one that stalls. Note the unshipped fix as a fast-follow in DEMO-SCRIPT.md.
- **The happy path will not run clean.** Find the single step that breaks and make that your one fix, even if it means dropping a lower-ranked triage item. A demo that reaches the value moment is worth more than three fixes and a broken run.
- **The commit fails.** It is almost always an unset git identity; the helper prints the two `git config` lines to fix it. Set them, re-run the helper. If the MVP genuinely is not code, the changelog timestamp is your audit trail instead.
- **Nothing is live to fix (Day 3 slipped).** Use the Day 3 minimum-shippable fallback first: get one live page with one working action onto a public URL, then treat that page as the thing your demo script walks through.
