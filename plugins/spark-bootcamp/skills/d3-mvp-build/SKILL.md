---
name: Build The MVP
description: Build the thin slice live, one issue at a time, with Claude doing the coding, until there is something a real prospect can act on. Use on Day 3 after the blueprint.
when_to_use: Day 3 product, straight after d3-blueprint and d3-tech-stack, before Day 4 go-to-market. Trigger on "build it", "ship the MVP", "make it live".
argument-hint: [optional-issue-number]
---

# Build The MVP

**What this does.** Builds your thin slice for real, one issue at a time, and puts something live that a prospect can click, book or pay on today.
**Why it matters.** Day 3 is the day the idea stops being a document and becomes a thing. You do not build the whole product. You build the smallest slice that lets one real person take one real action, and you get it onto a public URL. A live page beats a perfect plan every time.
**You are ready for this when.** `03-product/PRD.md`, `03-product/blueprint.md` and `03-product/tech-stack.md` all exist, and your build issues are listed (in the repo, or in `03-product/blueprint.md`).

## Before you start
Read these, in this order:
- `03-product/PRD.md`: the one action a prospect must be able to take.
- `03-product/blueprint.md`: the slice and its issue list.
- `03-product/tech-stack.md`: what you chose to build on.
- `.spark/brand/brand.json`: colours, name, logo, so the live thing looks like you.
- `.spark/state.json`: read `business_type`. It decides everything below.

One rule for today, and it is not optional. **You pause for sign-off before you spend any money** (a domain, a paid Vercel tier, a Stripe live key) and **before anything goes out to a real prospect**. Deploying a page is fine. Charging a card, or emailing your list, waits for the founder to say yes.

Set a hard stop: **17:00 Wednesday**. If the functional slice is not live by then, you switch to the minimum-shippable fallback at the bottom of this skill. Nobody ends Day 3 having failed.

## Steps
1. Open the issue list from the blueprint. Order it so the very first issue produces something visible on screen, even if it is ugly. Visible progress keeps you honest.
2. Take ONE issue. Tell Claude what it is, in one sentence, and let it write the code. Small commits, one per issue.
3. After each issue: run it locally, look at it with your own eyes, then commit with the issue number in the message (`git commit -m "closes #3: capture email on landing page"`).
4. Log the issue in `03-product/BUILD-LOG.md` (one line: time, issue, what now works, commit hash). Use the template in `references/build-log-template.md`.
5. Repeat until the one action from the PRD works end to end on your own machine.
6. Deploy to a public URL. Then run the smoke check (below) against that URL. Do not trust "it worked locally".
7. When it is live, do the action yourself as a stranger would, on your phone, on the real URL. If you can complete it, you are done. If you cannot, that is your next issue.

## For software
Build the deployed working slice. Default stack: Next.js, Supabase, Vercel.
1. Scaffold the Next.js app if the repo is empty. Wire Supabase for any data the action needs (a signup, a booking, a saved record). Keep the schema to the one or two tables the action touches, no more.
2. Build only the screens on the critical path. One page that does the job beats five that half-work.
3. Deploy to Vercel. The free tier is enough for Day 3, so no spend and no sign-off needed yet. You get a public `*.vercel.app` URL. That is your live URL.
4. Smoke-check the URL, then do the action end to end on the live site.
Good looks like: a stranger lands on the URL, takes the one action, and the result lands in Supabase where you can see it.

## For hardware
You are not manufacturing this week. You are proving people want it enough to leave money or an email.
1. Produce the demonstrable prototype: a CAD render, a rendered product shot, or a physical mock you photograph well. One clear hero image beats a rough animation.
2. Build the pre-order or waitlist page (Next.js on Vercel, same free tier). Put the render front and centre, the promise from your PRD, and one clear action.
3. Take real payment intent. A waitlist email capture needs no spend and no sign-off. A refundable pre-order deposit through Stripe touches money, so you build it in test mode today and pause for founder sign-off before switching to a live key.
4. Deploy, smoke-check, and leave your own email or test card through the live page.
Good looks like: a public URL showing the prototype, with a working capture that records a real person's intent.

## For services
Prove the package is real by showing one finished piece of it, then let someone book you.
1. Produce ONE sample deliverable: the actual thing a client would receive (a sample report, a worked audit, a filled template). Make it genuinely good. This is your proof.
2. Write the productised package: what they get, the fixed price, the turnaround. One package, one price. No menu.
3. Build the bookable intake page (Next.js on Vercel free tier): the package, the sample as proof, and a booking or intake form. A form or a Calendly-style embed both count.
4. Deploy, smoke-check, and book a slot yourself through the live page to prove the form works.
Good looks like: a public URL where a prospect reads the offer, sees the sample, and books a call or submits an intake.

## The artefact
Two things.
1. `03-product/BUILD-LOG.md` (Markdown): the running log. One line per closed issue, time-stamped, with the commit hash and what now works. This is your Day 3 audit trail.
2. The deployed artefact itself: a public URL. Record that URL at the top of `BUILD-LOG.md` and pass it to the state helper as the day's result.

Run the smoke check to confirm the URL is genuinely live:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/smoke-check.py <your-public-url>
```
It reports the HTTP status and response time, and it degrades gracefully if a library is missing.

## Done when
There is something live on a public URL that a real prospect can act on, the smoke check returns HTTP 200, you have completed the one action yourself on the live URL, and every closed issue is committed with its issue number in the message. State the URL and the count of closed issues in the log.

## Log it
Append one line to `CHANGELOG.md`:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-mvp-build \
  --path 03-product/BUILD-LOG.md --result "live: <url>, N issues closed"
```
Then update state:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --day 3 --outcome "live: <url>" --complete true \
  --artefact d3-mvp-build:03-product/BUILD-LOG.md:"live: <url>, N issues closed"
```

## If it goes wrong
The minimum-shippable fallback. Use it the moment 17:00 Wednesday arrives without a working functional slice. It is not defeat. It is Day 3 shipped.
1. Deploy a single live landing page (Next.js on Vercel, or a static page) with the promise from your PRD and one working lead-capture field. That page, live and capturing, counts as the day's live URL.
2. Turn the demo into a clickable prototype or a short walkthrough: a Figma prototype, a slide click-through, or a two-minute screen recording of the intended flow. That becomes what you show prospects on Day 4.
3. Log it honestly in `BUILD-LOG.md`: what shipped, what slipped to a fast-follow, and the one blocking issue. Set the day complete with the fallback URL as the result. You still have a live page a real prospect can act on tomorrow, which is the whole point.

If the smoke check fails (anything other than 200), the URL is not live. Fix the deploy before you log the day complete. A page nobody can reach is not shipped.
