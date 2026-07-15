---
name: Set The Price
description: Turn your pricing model into three real packages, one recommended, each traced to a value assumption, floor GBP 2,000. Day 5, before the offer.
when_to_use: Day 5, after d5-pricing-model and proposition. Triggers on "what do I charge", "set my price", "rate card", "good better best".
---

# Set The Price

**What this does.** Turns your pricing model into three named packages (good, better, best) with real numbers, marks one recommended, and ties every price to a value assumption you can defend out loud.
**Why it matters.** Founders freeze on price, and a buyer decides in seconds whether it feels fair, so we anchor on value and engineer the middle package to win.
**You are ready for this when.** `05-sale/PRICING-MODEL.md` and `02-market/proposition.md` both exist.

## Before you start
Read `05-sale/PRICING-MODEL.md` (model, cost floor, willingness-to-pay), `02-market/proposition.md` (promise, numeric outcome), and `.spark/state.json` (`business_type`, `founder`, `headline_target`).

Guardrail: this sets numbers, it does not send them. No price goes to a prospect until the founder reads the rate card aloud and signs off.

Floor is GBP 2,000. No package below it. If the maths lands lower, fix the scope, do not drop the price.

## Steps
1. **Anchor on value, not cost.** Write the buyer's number first: what does solving this save or make them per year? Pull from `proposition.md` and interviews. Your price is a fraction of that. Never invent it; flag as an assumption if unevidenced.
2. **Set the recommended (better) package first.** Price at 10 to 20 percent of the annual value. Round clean (GBP 3,500, not 3,470). This anchors the rest.
3. **Build the good package below it.** Strip scope, not quality. Price 55 to 70 percent of recommended, never below GBP 2,000. If stripping takes you under, make the recommended one the entry point and say so.
4. **Build the best package above it.** Add speed, depth, done-for-you, ongoing support. Price 1.6 to 2.2 times recommended. It rarely sells; its job is to make the middle look sensible.
5. **Trace every price to one value assumption.** Beside each number write a sentence starting "Worth it because...". If you cannot, the price is guessed.
6. **Run the check script** to confirm floor, ordering and recommended flag before writing the file.
7. **Branch by path for what is included only.** The prices work the same everywhere; the contents differ.

### For software
Slices of the deployed product plus service. Good: working slice, self-serve. Better: slice plus setup and your data loaded. Best: slice, setup, custom integration, a month of priority fixes. Price on outcome, not features or seats.

### For hardware
Packages map to commitment, since nothing ships yet. Good: paid pre-order deposit reserving a unit. Better: pre-order plus early-access pricing. Best: a small pilot batch or founder-edition bundle. State what money buys now versus later. Never price a prototype as a shipped product.

### For services
Scope tiers of the productised service. Good: the sample deliverable, once. Better: deliverable plus a review cycle and handover call. Best: monthly retainer or multi-part programme. Price on the client's outcome, not your hours.

## The artefact
Writes `05-sale/RATE-CARD.md` in Markdown, in order: one-line annual value to the buyer (sourced or flagged); a three-column table (name, price GBP, included, "Worth it because..."); the recommended package named with one line on why; a note on what the good package leaves out. Good: three clean numbers at or above GBP 2,000, the middle clearly best value.

## Done when
- Three packages priced, all at or above GBP 2,000.
- Exactly one marked recommended.
- Each price carries a "Worth it because..." assumption.
- `05-sale/RATE-CARD.md` exists and passes `scripts/price-check.py`.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d5-price-number \
  --artefact 05-sale/RATE-CARD.md \
  --result "recommended GBP <number>"
```
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"5":{"outcome":"Rate card set: 3 packages, recommended GBP <number>"}}}'
```
If a price rested on an unsourced value figure, record it in `DECISIONS.md`: the number, that it is an assumption, how you would test it with the first buyer.

## If it goes wrong
If the check script will not run, verify by hand: all three at or above 2000, exactly one recommended, one "Worth it because..." each. If you cannot find any value figure, price the recommended package at GBP 2,000, mark the value line as an assumption, and note in `DECISIONS.md` that the first sale is the test.
