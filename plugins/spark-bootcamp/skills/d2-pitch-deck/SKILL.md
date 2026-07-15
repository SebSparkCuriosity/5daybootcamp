---
name: Build The Pitch Deck
description: Assembles Day 2 into a branded 12-slide pitch deck for investors and partners. Every claim traces to a Day 1 quote or a sourced figure. Use once the market work is done.
when_to_use: Day 2, last thing, after market map, sizing, competitor scan, positioning and pricing exist, and brand.json is written. This is the hand-out deck, not the Day 4 sales deck.
---

# Build The Pitch Deck

**What this does.** Turns everything you learned on Day 2 into one branded, 12-slide pitch deck a stranger can read without you in the room.
**Why it matters.** By Friday you need to talk about your business to people who did not sit in your interviews: an investor, a partner, a first believer. A deck forces the week into one story and shows the gaps. This is not the deck that closes a single prospect. That is the Day 4 sales deck, built for one buyer. This one is the general hand-out: the whole picture, honest, on brand, sourced.
**You are ready for this when.** `02-market/market-sizing.md` exists, and so does at least one Day 1 quote in `01-discovery/discovery-synthesis.md`.

## Before you start
Read these, because the deck is assembled from them, not invented here:
- `02-market/market-map.md` and `02-market/market-sizing.md` (the market and the TAM, SAM, SOM figures)
- `02-market/competitor-scan.md` (who the buyer uses today)
- `02-market/positioning.md` and `02-market/proposition.md` (your one-line story)
- `02-market/pricing.md` (what one customer pays)
- `01-discovery/discovery-synthesis.md` for verbatim quotes, with `01-discovery/validated-problem.md` as backup
- `.spark/brand/brand.json` for the colours, fonts and contact details

One rule runs through this skill: every hard claim on a slide traces to a source. A source is a quote with a person's role attached, or a figure with a report, register, URL or named assumption behind it. No source, no slide. We do not launder a guess by putting it in a deck. If you have not measured a number yet (a target time, for example), write it as a target and flag it. Never fabricate a market figure: lift them from the sizing you already did.

Open `${CLAUDE_SKILL_DIR}/references/pitch-deck-outline.md` now. That is the 12-slide shape, in order, with what belongs on each slide. Open `${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml` too: that is a filled-in example you copy and overwrite.

Guardrail: nothing here is sent or spent. You are building a file, not contacting anyone. When you later show it to a real investor or partner, that is outreach, so pause for sign-off then, in the Day 4 skills.

## Steps
1. Copy the example into place: `cp ${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml 02-market/deck-content.yaml`. You will edit that copy. Never edit the example in the skill folder.
2. Set the title block. `title` is your one-line company purpose (lift it from `positioning.md` or `proposition.md`). `subtitle` carries the who and the headline number. This becomes slide 1.
3. Fill the 11 slides in order, following the outline: problem, solution, why now, market, product, competition, model, go-to-market, traction, team, the ask. One point per slide. Lead each with the number or the claim, never with throat-clearing.
4. Put a real Day 1 quote on the problem slide (slide 2) and a second on the traction slide (slide 10). Copy them verbatim from `discovery-synthesis.md`, with the speaker's role, never their name. A quote in the customer's words does more than a paragraph of yours.
5. Put the TAM on the market slide (slide 5), with SAM and SOM under it, each with a currency symbol, copied exactly from `market-sizing.md`. Do not round them into new numbers.
6. Branch by path on the product slide (slide 6) only:
   - **software**: describe the working slice and the outcome it produces. Three steps, plain English.
   - **hardware**: point to the CAD render or physical mock, and the pre-order or waitlist proof.
   - **services**: point to the one sample deliverable and the bookable intake.
7. Against every hard claim in the YAML, keep a `source:` line (the builder ignores it, it is your audit trail). If a claim has no source, cut it or downgrade it to a flagged assumption.
8. Build the deck: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/house-style/scripts/build_deck.py --content 02-market/deck-content.yaml --brand .spark/brand/brand.json --out 02-market/pitch-deck`. The builder reads your brand tokens and writes `02-market/pitch-deck.pptx`. If python-pptx is not installed it writes a self-contained `pitch-deck.html` instead and prints the one install line. Either file is a valid deck.
9. Open the file and read it end to end as a stranger would. Count the slides: 12. Check the quote is there, the TAM is there, and nothing on any slide is unsourced. Fix the YAML and re-run as many times as you like: the build is repeatable and overwrites cleanly.

## The artefact
Writes two files under `02-market/`:
- `02-market/deck-content.yaml`, the source of truth for the deck, in YAML. Every slide's claims carry a `source:` note.
- `02-market/pitch-deck.pptx` (or `.html` if python-pptx is absent), the built deck, branded from `brand.json`.

Good looks like 12 slides in the Sequoia and Kawasaki order, in your brand colours and fonts, that a partner could read cold and understand what you do, for whom, how big the prize is, and what you want from them. A verbatim Day 1 quote on the problem slide, the TAM on the market slide, and not one figure a sceptic could not trace back to a source.

## Done when
All true: `02-market/pitch-deck.pptx` (or `.html`) exists and opens cleanly; it has 12 slides; a verbatim Day 1 quote appears on the problem slide and the TAM figure (with a currency symbol) appears on the market slide; and re-running the builder on the same YAML reproduces the deck without error.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-pitch-deck`, artefact path `02-market/pitch-deck.pptx`, and the numeric result, for example "12-slide pitch deck, TAM £42m". Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: record the Day 2 outcome and register both artefacts. If building the deck exposed a gap in the story that changed a decision, log it with its rationale in DECISIONS.md.

## If it goes wrong
If the builder cannot produce a .pptx (python-pptx missing), it writes `pitch-deck.html` instead and tells you the one-line fix. The HTML deck opens in any browser and presents with the arrow keys, so you are not blocked: ship it and install python-pptx later if you want the .pptx.

If you are short a Day 1 quote, do not invent one. Go back to `interview-notes.md` and lift a real line, or run one more short interview. A deck with a genuine voice on slide 2 is worth more than a polished deck of your own assertions.

If the YAML fails to parse, the builder prints the line it choked on. The usual cause is a quote containing a colon: wrap the whole value in double quotes and rebuild.
