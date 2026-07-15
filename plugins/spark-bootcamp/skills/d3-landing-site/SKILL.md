---
name: Launch The Landing Site
description: Put your public shopfront live on your real domain, on-brand, with working lead capture and a privacy notice. Day 3, after the MVP slice.
when_to_use: Day 3, after d3-mvp-build and d3-domain-email. Trigger on "launch the site", "landing page", "put the shopfront live".
argument-hint: [optional-domain]
---

# Launch The Landing Site

**What this does.** Builds your one public page on your real domain that a prospect lands on and acts on: signs up, reserves, or books.
**Why it matters.** This is the page every Day 4 email, post and call points at, so it has to look like you, capture leads where you can see them, and read cleanly on a phone.
**You are ready for this when.** `02-market/proposition.md`, `.spark/brand/brand.json` and `.spark/deliverables/data-protection/privacy-notice.md` exist, plus a live URL from `d3-mvp-build` and a domain from `d3-domain-email`.

## Before you start
Reads: `02-market/proposition.md` (the words), `.spark/brand/brand.json` (the look), `.spark/deliverables/data-protection/privacy-notice.md` (link before any capture), `.spark/state.json` via journey-state (`business_type` picks the variant).

Two hard guardrails: pause for founder sign-off before the page goes public or points at the real domain (preview URLs are fine); no capture without the privacy notice live (fix a 404 link first).

## Steps
1. Build the page: `python3 ${CLAUDE_SKILL_DIR}/scripts/build_landing.py --root .`. It reads brand.json and proposition.md, picks the variant, links the notice, writes `index.html`, and prints anything it guessed.
2. Read the page in a browser. Confirm the headline is your promise with the number on it, logo and colours match. Edit `index.html` directly if the tone is off.
3. Wire the capture store. Every variant posts to one Supabase `captures` table. Follow `${CLAUDE_SKILL_DIR}/references/capture-store.md` to create it (insert-only, no browser reads) and paste your project URL and anon key into `index.html`. No Supabase? Use the Formspree fallback in that reference.
4. Run the a11y check: `python3 ${CLAUDE_SKILL_DIR}/scripts/a11y_check.py 03-product/site/index.html --root .`. It writes `03-product/site/accessibility-report.md` and prints PASS or numbered flags (contrast, labels, keyboard reach, alt text). Fix every flag, or note any you consciously accept with a reason.
5. Deploy to a preview URL first (Vercel free tier). Do the capture action yourself on your phone; confirm the row lands in `captures`.
6. **Stop for founder sign-off.** Show the preview URL and the a11y report. Only on an explicit yes, point the real domain at it.
7. Point the real domain (the DNS from `d3-domain-email`). Reload, take the action once more on the real URL, confirm the row lands.

## For software
Signup or "start free" that drops the visitor into your working slice. CTA: "Create your account" or "Start free". Capture email on submit, then redirect to the app.

## For hardware
Pre-order or waitlist with the CAD render or product shot as hero. CTA: "Reserve yours" (refundable deposit) or "Join the waitlist" (email only). A waitlist needs no spend. A deposit touches money: build it in Stripe test mode today, pause for sign-off before a live key.

## For services
Bookable intake showing the one sample deliverable and the fixed price. CTA: "Book a call" or "Request the package". A form or Calendly-style embed both count, as long as the submission also writes a `captures` row.

## The artefact
Writes `03-product/site/index.html` (self-contained, inline styles, one capture form, privacy notice in the footer) and `03-product/site/accessibility-report.md`. Plus the capture store (Supabase `captures` table or Formspree) and the live deployment. Record the live URL at the top of the report. Good looks like: a stranger reads the headline, gets the promise and number in ten seconds, and completes the one action on a phone.

## Done when
Live on your real domain (not a preview), a test submission you made lands as a row in `captures`, and `a11y_check.py` prints PASS or every flag is fixed or noted as accepted. State the live domain and the capture count (at least 1) as the result.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-landing-site \
  --artefact 03-product/site/index.html \
  --result "live: <your-domain>, 1 test capture, a11y PASS"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"3": {"outcome": "landing live: <your-domain>"}}}'
```
If the a11y check changed a colour or layout, log that as a dated line with rationale in DECISIONS.md.

## If it goes wrong
Domain won't resolve by end of day: launch on the preview URL, treat it as the live page for Day 4, record "preview URL, custom domain pending", set DNS as tomorrow's first job.
Capture store won't connect: use the Formspree fallback in `references/capture-store.md`; paste emailed submissions into `04-gtm/captures.jsonl` by hand.
`a11y_check.py` won't run: walk the four checks by hand (contrast, labels, Tab reach, alt text). Never let a broken script block the launch.
