---
name: Set The Price
description: Turn your pricing model into three real packages with numbers, one recommended, each traced to a value assumption, floor GBP 2,000. Use on Day 5 before you send the offer.
when_to_use: Day 5 sale, after d5-pricing-model and the proposition are written, before you build the offer or intake page. Triggers on "what do I charge", "set my price", "rate card", "good better best".
---

# Set The Price

**What this does.** Turns your pricing model into three named packages (good, better, best) with real numbers, marks one as recommended, and ties every price to a value assumption you can defend out loud.
**Why it matters.** Founders freeze on price. They either pluck a number from thin air or copy a competitor and hope. Both lose money and trust. A buyer decides in seconds whether a price feels fair, and "fair" comes from value, not from your costs. Three packages beat one because they give the buyer a choice about how much, not whether. The middle one is where most people land, and that is the one you engineer to win.
**You are ready for this when.** `05-sale/PRICING-MODEL.md` and `02-market/proposition.md` both exist.

## Before you start
Read three files:
- `05-sale/PRICING-MODEL.md`: the model, the cost floor, the willingness-to-pay signals from your interviews.
- `02-market/proposition.md`: the promise and the numeric outcome you sell.
- `.spark/state.json`: `business_type`, `founder`, `headline_target`.

Guardrail: this skill sets numbers, it does not send them. Do not put a price in front of a real prospect until the founder has read the rate card aloud and signed off. No money moves in this step.

The Spark floor is GBP 2,000. No package sits below it. If your maths lands lower, either the scope is too small to sell or you have undervalued the outcome. Fix the scope, do not drop the price.

## Steps
1. **Anchor on value, not cost.** Write the buyer's number first: what does solving this save or make them, per month or per year? Pull it from `proposition.md` and your interview notes. If a client saves 6 hours a week at GBP 50 an hour, that is roughly GBP 15,000 a year of value. Your price is a fraction of that, not a multiple of your effort. Never invent this figure. If you have no evidence, flag it as an assumption in the rate card.
2. **Set the recommended (better) package first.** This is your default win. Price it at 10 to 20 percent of the annual value you just wrote. Round to a clean number (GBP 3,500, not GBP 3,470). This anchors the other two.
3. **Build the good package below it.** Strip scope, not quality. Remove the nice-to-haves, keep the core outcome. Price it around 55 to 70 percent of the recommended one, and never below GBP 2,000. If stripping scope takes you under GBP 2,000, the good package is not viable: make the recommended one your entry point instead and say so.
4. **Build the best package above it.** Add the things a serious buyer will actually pay more for: speed, depth, a done-for-you element, ongoing support. Price it at 1.6 to 2.2 times the recommended one. This package rarely sells, and that is fine. Its job is to make the middle look sensible.
5. **Trace every price to one value assumption.** Beside each number, write the single sentence that justifies it, starting "Worth it because...". If you cannot write that sentence, the price is guessed and the buyer will feel it.
6. **Run the check script.** Use it to confirm the floor, the ordering and the recommended flag before you write the file. See "If it goes wrong" for the manual version.
7. **Branch by path only for what is included.** The three prices work the same way for every business. What sits inside each package differs. See below.

### For software
Each package is a slice of the deployed product plus a level of service. Good: the working slice, self-serve. Better: the slice plus setup and your data loaded. Best: the slice, setup, a custom integration and a month of priority fixes. Price on the outcome the software produces, not on features or seats.

### For hardware
Packages map to commitment, since the product is not shipping yet. Good: a paid pre-order deposit that reserves a unit. Better: pre-order plus early-access pricing on the full unit. Best: a small pilot batch or a founder-edition bundle. State clearly what money buys now and what it buys later. Never price a prototype as if it were a shipped product.

### For services
Packages are scope tiers of the productised service. Good: the one sample deliverable, once. Better: the deliverable plus a review cycle and a handover call. Best: the deliverable delivered monthly as a retainer, or a multi-part programme. Price on the client's outcome, not on your hours or day rate.

## The artefact
Writes `05-sale/RATE-CARD.md` in Markdown. It contains, in this order:
- A one-line statement of the annual value to the buyer, sourced or flagged as an assumption.
- A three-column comparison table: package name, price in GBP, what is included, the "Worth it because..." line.
- The recommended package named explicitly, with one sentence on why it is the default.
- A short note on what is deliberately left out of the good package, so the founder can explain the jump.

What good looks like: three clean numbers, all at or above GBP 2,000, the middle one clearly the best value on the page, and a founder who can say each price out loud without flinching.

## Done when
- Three packages are priced, all at or above GBP 2,000.
- Exactly one is marked recommended.
- Each price carries a "Worth it because..." value assumption.
- `05-sale/RATE-CARD.md` exists and passes `scripts/price-check.py`.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the recommended price as the numeric result:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d5-price-number \
  --artefact 05-sale/RATE-CARD.md \
  --result "recommended GBP <number>"
```

Update the journey state:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"5":{"outcome":"Rate card set: 3 packages, recommended GBP <number>"}}}'
```

If a price rested on a value figure you could not source, record it in `DECISIONS.md`: the number, that it is an assumption, and how you would test it with the first buyer.

## If it goes wrong
If the check script will not run (Python missing), verify by hand: all three prices at or above 2000, exactly one line marked recommended, and one "Worth it because..." per package. If you genuinely cannot find any value figure, do not stall. Price the recommended package at GBP 2,000, mark the value line as an assumption, and note in `DECISIONS.md` that the first sale is the test. Shipping a defensible guess beats a blank page.
