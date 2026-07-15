---
name: Launch The Landing Site
description: Put your public shopfront live on the real domain, with working lead capture, on-brand, and a privacy notice. Use on Day 3 after the MVP slice.
when_to_use: Day 3 product, after d3-mvp-build and d3-domain-email, once brand.json and the privacy notice exist. Trigger on "launch the site", "landing page", "put the shopfront live".
argument-hint: [optional-domain]
---

# Launch The Landing Site

**What this does.** Builds your one public page, on your real domain, that a prospect lands on and acts on: signs up, reserves, or books. It reads your brand so it looks like you, links your privacy notice, and sends every capture to a store you can read.
**Why it matters.** This is the page every Day 4 email, post and call points at. No page, no place to send people. It has to look like the same company as your deck, it has to capture leads somewhere you can actually see them, and it has to be legible to someone on a phone with poor eyesight. Get those three right and Day 4 has a target to aim at.
**You are ready for this when.** `02-market/proposition.md`, `.spark/brand/brand.json` and `.spark/deliverables/data-protection/privacy-notice.md` all exist, and you have a live URL from `d3-mvp-build` and a domain from `d3-domain-email`.

## Before you start
Reads from the founder's project:
- `02-market/proposition.md`: your headline promise and the one metric. This is the words on the page.
- `.spark/brand/brand.json`: colours, fonts, logo, tagline. This is the look.
- `.spark/deliverables/data-protection/privacy-notice.md`: the notice you must link before you collect a single name.
- `.spark/state.json` (via journey-state): `business_type` decides the page variant, `founder` and `idea` fill gaps.

Two guardrails, both hard.
1. **You pause for sign-off before the page goes public and before it points at your real domain.** Deploying to a preview URL is fine. Pointing the real domain at it, or switching a payment field to a live key, waits for the founder to say yes.
2. **No capture without the privacy notice live.** If the notice link 404s, the page is not launchable. Fix the link first.

## Steps
1. Build the page from your brand and proposition in one command. The script reads `brand.json` and `proposition.md`, picks the right variant from `business_type`, links the privacy notice, and writes a finished `index.html`:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_landing.py --root .
   ```
   It degrades gracefully: if the brand file is thin or the proposition headline is missing, it fills a neutral default, writes the page anyway, and prints exactly what it guessed so you can fix it.
2. Read the page in a browser. Check the headline is the promise from your proposition, the number is on it, and the logo and colours match your deck. Change the copy in `index.html` directly if the tone is off. The script wrote a draft, not scripture.
3. Wire the capture store. Every variant posts to one Supabase table, `captures`, so all three paths read the same way on Day 4. Follow `${CLAUDE_SKILL_DIR}/references/capture-store.md` to create the table (one insert-only policy, no reads from the browser) and paste your project URL and anon key into the two placeholders near the top of `index.html`. No Supabase yet? The reference gives you the Formspree fallback, which needs no backend.
4. Run the accessibility check against the finished file. This is not a nicety in a regulated sector, it is table stakes:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/a11y_check.py 03-product/site/index.html --root .
   ```
   It writes `03-product/site/accessibility-report.md` and prints PASS or a numbered list of flags: colour contrast, missing form labels, non-keyboard-reachable controls, images with no alt text. Fix every flag you can. Note any you consciously accept, with a reason, at the bottom of the report.
5. Deploy to a preview URL first (Vercel free tier, no spend, no sign-off). Do the capture action yourself as a stranger would, on your phone, and confirm the row lands in the `captures` store.
6. **Stop here and get founder sign-off.** Show them the preview URL and the accessibility report. Only on an explicit yes do you point the real domain at the deployment.
7. Point the real domain at it (the DNS you set up in `d3-domain-email`). Reload the live domain, take the action once more on the real URL, and confirm the test row lands.

## For software
The page is a signup or a "start free" that drops the visitor into the working slice you built. CTA: "Create your account" or "Start free". Capture the email on submit, then redirect to the app. The `captures` row proves the funnel works even before the app does.

## For hardware
The page is a pre-order or waitlist. Put the CAD render or product shot as the hero. CTA: "Reserve yours" (refundable deposit) or "Join the waitlist" (email only). A waitlist email needs no spend and no sign-off. A deposit touches money, so build it in Stripe test mode today and pause for sign-off before a live key. Either way the intent lands in `captures`.

## For services
The page is a bookable intake. Show the one sample deliverable as proof and the fixed price. CTA: "Book a call" or "Request the package". An embedded booking form or a Calendly-style embed both count, as long as the submission also writes a `captures` row so Day 4 can read it.

## The artefact
Writes, under the founder's project:
- `03-product/site/index.html`: the finished, on-brand, single-page site. Self-contained, inline styles, one capture form, the privacy notice linked in the footer. What good looks like: a stranger reads the headline, understands the promise and the number in ten seconds, and can complete the one action on a phone.
- `03-product/site/accessibility-report.md`: the pass/flag output of the a11y check, with any accepted flags noted and reasoned.
- The capture store: a Supabase `captures` table (or Formspree endpoint), and the live deployment on your real domain. Record the live URL at the top of the accessibility report.

## Done when
The page is live on your real domain (not a preview URL), a test submission you made yourself lands as a row in the `captures` store where you can read it, and `a11y_check.py` prints PASS or every flag it raised is either fixed or noted as consciously accepted in the report. State the live domain and the capture count (at least 1, your own test) as the result.

## Log it
Append one line to CHANGELOG.md (the logbook helper also registers the artefact in state.json):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-landing-site \
  --artefact 03-product/site/index.html \
  --result "live: <your-domain>, 1 test capture, a11y PASS"
```
Then update state:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"3": {"outcome": "landing live: <your-domain>"}}}' \
  --append-artefact '{"skill":"d3-landing-site","path":"03-product/site/index.html","result":"live: <your-domain>, 1 test capture"}'
```
If the accessibility check changed a colour or a layout decision, log that as a dated line with its rationale in DECISIONS.md.

## If it goes wrong
If you cannot get the real domain to resolve by end of day, launch on the preview URL and treat that as the live page for Day 4. Record it honestly in the report as "preview URL, custom domain pending" and set the DNS as tomorrow's first job. A page a prospect can reach beats a domain nobody can.

If the capture store will not connect, fall back to the Formspree endpoint in `references/capture-store.md` (email capture, no backend, free tier). It emails you each submission and you paste them into `04-gtm/captures.jsonl` by hand. Slower, but Day 4 still has leads to work.

If `a11y_check.py` cannot run (a parsing error, a Python it does not like), the report is still the artefact of record. Walk the four checks by hand against the finished page: contrast from `brand.json`, a label on every field, every control reachable by Tab, alt text on every image. Never let a broken script block the launch.
