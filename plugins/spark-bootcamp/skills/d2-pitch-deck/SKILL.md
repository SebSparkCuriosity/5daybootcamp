---
name: Build The Pitch Deck
description: Assembles Day 2 into a branded 12-slide pitch deck. Every claim traces to a Day 1 quote or a sourced figure. Run once the market work is done.
when_to_use: Day 2, last thing, after market map, sizing, competitors, positioning, pricing and brand.json exist.
---

# Build The Pitch Deck

**What this does.** Turns Day 2 into one branded, 12-slide pitch deck a stranger can read without you in the room.
**Why it matters.** By Friday you must tell your story to people who never sat in your interviews, and a deck forces the week into one honest picture.
**You are ready for this when.** `02-market/market-sizing.md` exists and `01-discovery/discovery-findings.md` holds at least one Day 1 quote.

## Before you start
The deck is assembled from these, not invented: `02-market/market-map.md`, `02-market/market-sizing.md`, `02-market/competitors.md`, `02-market/positioning.md`, `02-market/proposition.md`, `01-discovery/discovery-findings.md` (quotes), `.spark/brand/brand.json`. The model slide carries your revenue-model hypothesis from the proposition, flagged as an assumption: pricing is fixed on Day 4, not today.

Every hard claim traces to a source: a quote with a role, or a figure with a report, register, URL or named assumption. No source, no slide. Never fabricate a market figure. Unmeasured numbers go in as flagged targets.

Read `${CLAUDE_SKILL_DIR}/references/pitch-deck-outline.md` (12-slide shape) and `${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml` (filled example). Nothing here is sent or spent.

## Steps
1. Copy the example: `cp ${CLAUDE_SKILL_DIR}/references/deck-content.example.yaml 02-market/deck-content.yaml`. Edit the copy, never the original.
2. Set the title block: `title` is your one-line purpose (from positioning or proposition), `subtitle` the who plus headline number. Slide 1.
3. Fill the 11 remaining slides in outline order: problem, solution, why now, market, product, competition, model, go-to-market, traction, team, ask. One point per slide, lead with the number.
4. Verbatim Day 1 quote on the problem slide (2) and traction slide (10), from `discovery-findings.md`, with role not name.
5. TAM on the market slide (5), SAM and SOM under it, each with a currency symbol, copied exactly from `market-sizing.md`. Do not re-round.
6. Branch by path on the product slide (6) only:
   - **software**: the working slice and the outcome, three plain steps.
   - **hardware**: the CAD render or physical mock, and the pre-order or waitlist proof.
   - **services**: the one sample deliverable and the bookable intake.
7. Keep a `source:` line against every hard claim (the builder ignores it, it is your audit trail). No source: cut it or flag it as an assumption.
8. Build: `python3 ${CLAUDE_PLUGIN_ROOT}/skills/house-style/scripts/build_deck.py --content 02-market/deck-content.yaml --brand .spark/brand/brand.json --out 02-market/pitch-deck`. Writes `pitch-deck.pptx`, or `pitch-deck.html` with an install line if python-pptx is absent.
9. Read it with the founder, slide by slide, as a stranger would (10 minutes). Confirm 12 slides, the quote, the TAM, nothing unsourced, and take one round of corrections in their words. Fix the YAML and re-run: builds are repeatable.

## The artefact
Writes `02-market/deck-content.yaml` (source of truth, `source:` notes) and `02-market/pitch-deck.pptx` (or `.html`), branded from `brand.json`. Good is 12 slides a partner reads cold and understands what you do, for whom, how big the prize, and the ask, with no figure a sceptic cannot trace.

## Done when
`02-market/pitch-deck.pptx` (or `.html`) opens cleanly with 12 slides; a verbatim Day 1 quote is on the problem slide and the TAM (with currency symbol) is on the market slide; re-running the builder reproduces the deck without error.

## Log it
Append one line via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-pitch-deck`, artefact `02-market/pitch-deck.pptx`, numeric result (e.g. "12-slide pitch deck, TAM £42m"). Record the Day 2 outcome via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. Log any decision the deck exposed in DECISIONS.md.

## If it goes wrong
No .pptx (python-pptx missing): the builder writes `pitch-deck.html` with the one-line fix. It opens in any browser and presents with arrow keys, so ship it. Short a quote: lift a real line from `interview-notes.md` or run one more interview, never invent. YAML fails to parse: the usual cause is a colon in a quote, so wrap the value in double quotes and rebuild.
