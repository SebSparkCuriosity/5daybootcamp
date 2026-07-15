---
name: Build The Sales Deck
description: Builds the Day 4 deck that closes one named prospect: problem, solution, proof, pricing, ask, in 10 to 14 slides, with proof lifted from real tester quotes. Use after you have prioritised the feedback.
when_to_use: Day 4 GTM, after d4-prioritise has ranked your buyers, before you take the deck into a Day 5 sales conversation. This is the one-buyer closing deck, not the Day 2 hand-out pitch deck.
argument-hint: [prospect name]
---

# Build The Sales Deck

**What this does.** Turns your Day 4 buyer ranking and your real tester quotes into one branded deck aimed at closing a single named prospect: the problem in their words, what you built, proof from people like them, the price, and one clear next step.
**Why it matters.** The Day 2 pitch deck explains your business to a stranger. This one does a different job: it moves one specific buyer from "interesting" to "yes". So it is narrower, warmer, and it leans on proof, real lines from real testers, not on your own claims. A prospect who hears their own words read back, then sees two other people got the result they want, is a prospect who signs.
**You are ready for this when.** `04-gtm/feedback-synthesis.md` exists (from d4-prioritise), and so does `02-market/messaging.md`.

## Before you start
Name the prospect first. This deck is for one person, so decide who before you build. Take the top buyer from `04-gtm/feedback-synthesis.md`. If the founder passed a name as the argument, use that instead.

Read these, because the deck is assembled from them, not invented here:
- `04-gtm/feedback-synthesis.md`, for the ranked buyers and, more important, the verbatim tester quotes and the results they reported. This is where your proof comes from.
- `02-market/messaging.md`, for the one-line proposition and the words you have already tested on this market. The deck should sound like your messaging, not a fresh voice.
- `02-market/proposition.md` and, if it exists, `02-market/pricing.md`, for what one customer pays. If neither states a price, use the Spark default framing: fixed price from 2,000 pounds, live in one to six weeks, and flag the exact figure as a number to confirm with the founder.
- `.spark/brand/brand.json`, for the colours, fonts and contact details the builder stamps on every slide.
- `.spark/state.json`, for `business_type` and the founder's name.

One rule runs through this skill, the same as the pitch deck: every proof point traces to a real source. Proof means a verbatim tester quote with the speaker's role attached (never their name), sat next to the result they reported. No invented quotes. No borrowed testimonials. If you are short of proof, that is a signal to go and get one more tester on the phone, not to make one up.

Guardrail: this skill builds a file. It sends nothing and spends nothing. Showing the deck to the real prospect is outreach, so pause for the founder's explicit sign-off before that happens, in the Day 5 selling skills. The price on the deck is money the prospect will spend, so confirm the exact figure with the founder before the deck leaves the room.

Open `${CLAUDE_SKILL_DIR}/references/sales-deck-outline.md` now: that is the slide shape, in order, with the five core sections marked. Open `${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml` too: a filled-in example you copy and overwrite.

## Steps
1. Copy the example into place: `cp ${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml 04-gtm/sales-deck-content.yaml`. Edit that copy. Never edit the example in the skill folder.
2. Personalise the title block. `title` is the outcome this prospect wants, in one line, lifted from your messaging. `subtitle` names the prospect and carries the headline number, for example "Prepared for Jane Roe, Head of Trust Admin. Live in three weeks, fixed price from 2,000 pounds." A deck addressed to one person out-closes a generic one every time.
3. Build the five core sections in order. These five must all be present, or the deck does not do its job:
   - **Problem.** Their pain, in the customer's words. Lead with a verbatim quote from someone in their role, and name what it costs today.
   - **Solution.** What you built or will build, one plain sentence, then the before-and-after. The outcome, not a feature list.
   - **Proof.** At least two proof points, each a real tester quote (with the speaker's role) beside the result they reported. This is the section that closes. Do not skimp on it.
   - **Pricing.** What this prospect pays and what they get for it. One number, stated plainly. Spark default: fixed price from 2,000 pounds, live in one to six weeks.
   - **The ask and next step.** Exactly what you want the prospect to do next, named and dated: "Start the pilot Monday", "Sign the one-page order form", "Book the 30-minute kickoff". Not "let us know your thoughts". A named next step is the difference between a nice chat and a sale.
4. Add the supporting slides around the core five to land between 10 and 14 slides total (the title block counts as one): how it works, why now, what is in and out of scope, timeline, and a short "why us" if the prospect does not know you. Follow the outline for the order. Keep one point per slide.
5. Branch by path on the "how it works" slide only:

   ## For software
   Describe the working slice on its public URL and the outcome it produces, in three plain steps. If the prospect can click it, put the link on the slide.

   ## For hardware
   Point to the CAD render or physical mock and the pre-order or waitlist proof. Show the thing, then the proof that others want it.

   ## For services
   Point to the one sample deliverable and the bookable intake. Show what they get and how they start.

6. Pull your proof straight from `04-gtm/feedback-synthesis.md`. Copy each quote verbatim, attach the speaker's role, and put the reported result next to it. Keep a `source:` line under every proof point in the YAML (the builder ignores it, it is your audit trail). Two proof points is the floor. Three is better.
7. Confirm the price with the founder before you commit it to a slide. This is money the prospect will spend. If the founder is not sure yet, write the Spark default framing and flag the exact figure as "confirm before sending".
8. Build the deck: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/house-style/scripts/build_deck.py --content 04-gtm/sales-deck-content.yaml --brand .spark/brand/brand.json --out 04-gtm/sales-deck`. The builder reads your brand tokens and writes `04-gtm/sales-deck.pptx`. If python-pptx is not installed it writes a self-contained `sales-deck.html` instead and prints the one install line. Either file is a valid deck.
9. Open the file and read it as the prospect would. Count the slides: between 10 and 14. Check all five core sections are present, that the proof section carries at least two real tester quotes, and that the final slide names a specific next step. Fix the YAML and re-run as often as you like: the build is repeatable and overwrites cleanly.

## The artefact
Writes two files under `04-gtm/`:
- `04-gtm/sales-deck-content.yaml`, the source of truth for the deck, in YAML. Every proof point carries a `source:` note.
- `04-gtm/sales-deck.pptx` (or `sales-deck.html` if python-pptx is absent), the built deck, branded from `brand.json`.

Good looks like a 10 to 14 slide deck, addressed to one named prospect, in your brand colours and fonts, that carries all five core sections, sits two or more real tester quotes in the proof section with the result each reported, and ends on a slide the prospect could act on today.

## Done when
All true: `04-gtm/sales-deck.pptx` (or `.html`) exists and opens cleanly; it has between 10 and 14 slides; the five core sections (problem, solution, proof, pricing, ask) are all present; the proof section carries at least 2 verbatim tester quotes, each with a role and a reported result; the final slide states one named next step; and re-running the builder on the same YAML reproduces the deck without error.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d4-sales-deck`, artefact path `04-gtm/sales-deck.pptx`, and the numeric result, for example "12-slide sales deck for Jane Roe, 3 proof points, price 2,500 pounds". Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: record the Day 4 outcome and register both artefacts. If confirming the price or the scope changed a call the founder made, log it with its rationale in DECISIONS.md.

## If it goes wrong
If the builder cannot produce a .pptx (python-pptx missing), it writes `sales-deck.html` instead and tells you the one-line fix. The HTML deck opens in any browser and presents with the arrow keys, so you are not blocked: use it Friday and install python-pptx later if you want the .pptx.

If you have fewer than two real tester quotes, stop and get one more. A closing deck stands on its proof. Do not pad the proof section with your own assertions or a quote you cannot source: one weak, unsourced proof slide undoes the whole deck. Phone the next tester on the ranked list in `feedback-synthesis.md` and get a line you can use.

If the YAML fails to parse, the builder prints the line it choked on. The usual cause is a quote containing a colon: wrap the whole value in double quotes and rebuild.
