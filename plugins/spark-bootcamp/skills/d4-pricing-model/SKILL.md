---
name: Choose The Pricing Model
description: Commit to ONE pricing model, name the value metric, and give each rejected model a one-line reason. Day 4, before the sales deck carries a price.
when_to_use: Day 4, after d4-icp-messaging, before the sales deck. When you catch yourself saying "I'll just charge for time".
---

# Choose The Pricing Model

**What this does.** Picks one pricing model and why, names what you charge against (the value metric), and records a reason for each rejected model.
**Why it matters.** How you charge decides who buys and how fast they say yes, and this afternoon's sales deck carries a price slide, so the model and floor get fixed now. The exact number is Friday morning's first job (`d5-price-number`).
**You are ready for this when.** `02-market/proposition.md` exists and names the customer success metric.

## Before you start
Read the success metric in `02-market/proposition.md` and `business_type` + `headline_target` in `.spark/state.json`. Read `${CLAUDE_SKILL_DIR}/references/pricing-models.md` (the four models, when each wins, Jersey and regulated notes).

A working discussion (10 to 15 minutes), and ask before proposing: what does this buyer already pay for similar outcomes, and do they say yes faster to a one-off or to recurring spend? The founder answers from their world; you score the models against it.

Guardrail: this chooses a model and value metric only. No proposal, no payment. Money moves in the sale step.

## Steps
1. Write the customer success metric in one line. If it is fuzzy ("saves time"), sharpen to a number first: you cannot price a feeling.
2. Name the value metric: the one unit your price scales with (the customer's value, not your effort). Per fund, per matter, per seat, per report, one-off per system. Pick one.
3. Score the four models (one-off build fee, pay-for-access plus build-in-partnership, subscription, retainer) against your success and value metrics. Read the "when it wins" line for each in the reference.
4. The founder chooses ONE, with your recommendation and its number on the table. Reason in two sentences: why it fits this buyer and value metric, and what it does to the first yes. Favour a real payment inside five days over lifetime value on paper.
5. Give each rejected model a specific one-line reason it lost.
6. Sanity-check against Jersey and regulated sectors: a capital line item (one-off) often clears faster than new recurring spend. Note any constraint that shaped the choice.
7. Set a first-price range: a floor and ceiling with one reason each. Spark's floor is £2,000 fixed; do not go below without a written reason.

## The artefact
Writes `04-gtm/PRICING-MODEL.md`. Good: success metric restated in one line; value metric in three words or fewer; chosen model with two-sentence reason; four-row table (model, when it wins, verdict) with each rejected row carrying a reason; any Jersey/regulatory constraint; floor and ceiling with a reason each. Use `${CLAUDE_SKILL_DIR}/references/pricing-model-template.md`.

## Done when
One model chosen and named, value metric named, each of the three rejected models has a one-line reason, and the file carries a floor and ceiling.

## Log it
Append one line to CHANGELOG.md:
- `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d4-pricing-model --artefact 04-gtm/PRICING-MODEL.md --result "floor GBP 2,000"`
Record the choice and its reason in DECISIONS.md.

## If it goes wrong
Cannot separate two models: default to one-off build fee for hardware and services, pay-for-access plus build-in-partnership for software, and write "provisional, revisit after first sale". If the success metric will not sharpen into a number, go back to `d2` and fix the proposition first.
