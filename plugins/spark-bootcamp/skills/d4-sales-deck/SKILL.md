---
name: Build The Sales Deck
description: Builds the Day 4 deck that closes one named prospect: problem, solution, proof, pricing, ask, in 10 to 14 slides, proof from real tester quotes.
when_to_use: Day 4 GTM, after d4-prioritise ranks buyers, before the Day 5 sale. The one-buyer closing deck, not the Day 2 pitch.
argument-hint: [prospect name]
---

# Build The Sales Deck

**What this does.** Turns your buyer ranking and real tester quotes into one branded deck aimed at closing a single named prospect.
**Why it matters.** A prospect who hears their own words read back, then sees two others got the result they want, is a prospect who signs.
**You are ready for this when.** `04-gtm/feedback-synthesis.md` (from d4-prioritise) and `02-market/messaging.md` exist.

## Before you start
Name the prospect first: the top buyer in `04-gtm/feedback-synthesis.md`, or the argument if passed. The deck is assembled from these, not invented:
- `04-gtm/feedback-synthesis.md`: ranked buyers, verbatim tester quotes, reported results (your proof).
- `02-market/messaging.md`: the tested proposition and words.
- `02-market/proposition.md` and, if present, `02-market/pricing.md`: what one customer pays. If neither states a price, use the Spark default (fixed price from 2,000 pounds, live in one to six weeks) and flag the figure to confirm.
- `.spark/brand/brand.json`: colours, fonts, contact. `.spark/state.json`: `business_type`, founder name.

Every proof point is a verbatim quote with the speaker's role (never their name) beside the result. No invented or borrowed quotes; short of proof, phone another tester. Guardrail: this builds a file, sends and spends nothing. Confirm the exact price before it goes on a slide; showing the deck is Day 5 outreach, so sign-off waits there.

Open `${CLAUDE_SKILL_DIR}/references/sales-deck-outline.md` (slide shape, five core sections marked) and `${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml` (filled example).

## Steps
1. `cp ${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml 04-gtm/sales-deck-content.yaml`. Edit the copy, never the example.
2. Personalise the title block: `title` is the outcome this prospect wants, one line from messaging; `subtitle` names the prospect and carries the headline number.
3. Build the five core sections in order, all present or the deck fails:
   - **Problem.** Their pain in their words: a verbatim quote from their role, plus what it costs today.
   - **Solution.** What you built, one plain sentence, then before-and-after outcome.
   - **Proof.** At least two real tester quotes (with role) beside the result reported. The section that closes.
   - **Pricing.** What this prospect pays and gets, one number. Spark default: fixed price from 2,000 pounds, live in one to six weeks.
   - **The ask.** One named, dated next step ("Sign the order form Monday"), not "let us know your thoughts".
4. Add supporting slides for 10 to 14 total (title counts as one): how it works, why now, scope, timeline, short "why us". Follow the outline. One point per slide.
5. Branch on the "how it works" slide only:

   ## For software
   Describe the working slice on its public URL and the outcome, in three steps. Put a clickable link on the slide.

   ## For hardware
   Point to the CAD render or physical mock plus the pre-order or waitlist proof.

   ## For services
   Point to the one sample deliverable and the bookable intake.

6. Pull proof from `04-gtm/feedback-synthesis.md`: quote verbatim, attach role, add result, keep a `source:` line under each (builder ignores it). Floor two, three better. Confirm the price before committing it; if unsure, write the Spark default and flag "confirm before sending".
7. Build: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/house-style/scripts/build_deck.py --content 04-gtm/sales-deck-content.yaml --brand .spark/brand/brand.json --out 04-gtm/sales-deck`. Writes `04-gtm/sales-deck.pptx`, or a self-contained `sales-deck.html` (with the one install line) if python-pptx is absent.
8. Read it as the prospect: 10 to 14 slides, five sections present, two or more real quotes, final slide names a next step. Fix the YAML and re-run; overwrites cleanly.

## The artefact
Under `04-gtm/`: `sales-deck-content.yaml` (source of truth, each proof point carries `source:`) and `sales-deck.pptx` (or `sales-deck.html`), branded from `brand.json`. Good is a 10 to 14 slide deck for one named prospect, all five core sections, two or more sourced quotes, ending on a slide they could act on today.

## Done when
`04-gtm/sales-deck.pptx` (or `.html`) exists and opens; 10 to 14 slides; all five core sections present; proof carries at least 2 verbatim quotes each with role and result; final slide states one named next step; re-running reproduces the deck without error.

## Log it
Append one line via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d4-sales-deck`, artefact path `04-gtm/sales-deck.pptx`, numeric result (e.g. "12-slide deck, 3 proof points, price 2,500 pounds"). Then set the Day 4 outcome via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. Log any price or scope call in DECISIONS.md.

## If it goes wrong
No .pptx (python-pptx missing): builder writes `sales-deck.html`, which presents in any browser with arrow keys. Not blocked. Fewer than two real quotes: stop and phone the next tester in `feedback-synthesis.md`; never pad proof with unsourced assertions. YAML fails to parse: builder prints the line, usually a quote containing a colon; wrap the value in double quotes and rebuild.
