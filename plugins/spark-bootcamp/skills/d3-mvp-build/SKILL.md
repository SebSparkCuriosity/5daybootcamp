---
name: Build The MVP
description: Build the thin slice live, one issue at a time, until a real prospect can act on it. Day 3, after the blueprint.
when_to_use: Day 3, after d3-blueprint and d3-tech-stack. Triggers on "build it", "ship the MVP", "make it live".
argument-hint: [optional-issue-number]
---

# Build The MVP

**What this does.** Builds your thin slice for real, one issue at a time, and puts something live a prospect can click, book or pay on today.
**Why it matters.** This is the day the idea stops being a document and becomes a thing one real person can act on.
**You are ready for this when.** `03-product/docs/PRD.md`, `03-product/docs/blueprint.md`, `03-product/docs/tech-stack.md` exist and your build issues are listed.

## Before you start
Read: `03-product/docs/PRD.md` (the one action), `03-product/docs/blueprint.md` (the slice), `03-product/github.md` (issue list), `03-product/docs/tech-stack.md`, `.spark/brand/brand.json`, and `.spark/state.json` for `business_type` (it decides everything below).

Pause for founder sign-off before spending money (domain, paid tier, live Stripe key) or sending anything to a real prospect. Deploying a page is fine. Hard stop 17:00 Wednesday: if not live, switch to the fallback below.

## Steps
1. Order the issues so the first produces something visible on screen. When it lands, show the founder and take corrections immediately: they react better to a real screen than to a plan, and five minutes now beats an hour at 16:00.
2. Take ONE issue, tell Claude in one sentence, let it write the code. One small commit per issue with the issue number (`git commit -m "closes #3: ..."`).
3. Log each issue in `03-product/BUILD-LOG.md` (template in `references/build-log-template.md`).
4. Repeat until the PRD action works end to end locally.
5. Deploy to a public URL, run the smoke check against it, then do the action yourself on your phone as a stranger would.

## For software
Deployed working slice. Default stack: Next.js, Supabase, Vercel. Scaffold the app, wire Supabase for the one or two tables the action touches, build only critical-path screens, deploy to Vercel free tier (no spend). Good: a stranger takes the action and it lands in Supabase.

## For hardware
Not manufacturing. Produce one hero prototype image (CAD render or photographed mock). Build a pre-order/waitlist page (Next.js, Vercel free tier). Email capture needs no sign-off; a refundable Stripe deposit is built in test mode today, pause for sign-off before the live key. Good: a public URL recording real intent.

## For services
Produce ONE genuinely good sample deliverable as proof. Write the productised package (one price, one turnaround, no menu). Build a bookable intake page (Next.js, Vercel free tier) showing package, sample and a booking/intake form. Book a slot yourself. Good: a public URL where a prospect reads the offer, sees the sample, and books.

## The artefact
`03-product/BUILD-LOG.md` (Markdown): one line per closed issue, time-stamped, commit hash, what now works. Record the public URL at the top. Smoke-check it:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/smoke-check.py <your-public-url>
```

## Done when
Something live on a public URL a real prospect can act on, smoke check returns HTTP 200, you have completed the action yourself on the live URL, and every closed issue is committed with its number. State URL and issue count in the log.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-mvp-build \
  --artefact 03-product/BUILD-LOG.md --result "live: <url>, N issues closed"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"outcome":"live: <url>"}}}'
```

## If it goes wrong
Minimum-shippable fallback at 17:00 Wednesday: deploy one live landing page (Next.js on Vercel, or static) with the PRD promise and one working lead-capture field; that counts as the live URL. Turn the demo into a clickable prototype or two-minute walkthrough for Day 4. Log honestly what shipped and what slipped, set the day complete. If the smoke check returns anything but 200, fix the deploy before logging complete.
