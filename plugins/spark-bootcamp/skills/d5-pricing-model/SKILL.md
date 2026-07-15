---
name: Choose The Pricing Model
description: Commits to ONE pricing model with the reason written down, names the value metric, and gives every rejected model a one-line reason. Use on Day 5 before you set a number.
when_to_use: Day 5 sale, after the proposition is written and before you build the offer or the price. Whenever you catch yourself saying "I'll just charge for my time".
---

# Choose The Pricing Model

**What this does.** Picks one pricing model and writes down why, names the thing you charge against (the value metric), and records a one-line reason for each model you rejected.
**Why it matters.** How you charge decides who buys, how fast they say yes, and whether the work is worth doing. Founders default to hourly because it feels safe. It is the worst of the four for almost everyone here: it caps your income at the clock, invites haggling, and tells a regulated buyer nothing about the outcome. Choose the model first, then the number. Not the other way round.
**You are ready for this when.** `02-market/proposition.md` exists and names the customer success metric.

## Before you start
Read `02-market/proposition.md`, specifically the customer success metric (the numeric outcome the customer gets). Read `.spark/state.json` for `business_type` and `headline_target`. If you have not read `${CLAUDE_SKILL_DIR}/references/pricing-models.md`, read it now: it explains the four models, when each wins, and the Jersey and regulated-sector notes.

Guardrail: this skill chooses a model and a value metric. It does not send a proposal or take a payment. No money moves until the founder signs off in the sale step.

## Steps
1. Write down the customer success metric from `proposition.md` in one line. Everything below hangs off this. If it is fuzzy ("saves time", "peace of mind"), stop and sharpen it to a number first, because you cannot price a feeling.
2. Name the value metric: the single unit your price scales with. Not your effort, the customer's value. Examples: per fund administered, per matter opened, per seat, per property listed, per report produced, one-off per system built. Pick one. The right value metric goes up when the customer gets more value and stays flat when you simply work harder.
3. Score the four models against your success metric and value metric. The four are: one-off build fee, pay-for-access plus build-in-partnership, subscription, retainer. Full descriptions and fit rules are in `references/pricing-models.md`. Read the "when it wins" line for each.
4. Choose ONE. Write the reason in two sentences: why it fits this buyer and this value metric, and what it does to speed of the first yes. Favour the model that gets a real payment inside five days over the one that maximises lifetime value on paper. A signed one-off beats a hypothetical subscription every time this week.
5. Give each of the three rejected models a one-line reason it lost. Be specific: "retainer rejected: buyer will not commit monthly before seeing one result" beats "not a good fit".
6. Sanity-check against Jersey and the regulated sectors. Trust, fund, wealth and law buyers have procurement rules and budget cycles. A capital line item (one-off build fee) often clears faster than a new recurring subscription, which may need sign-off you cannot get in a week. The reference file has the detail. Note any constraint that shaped your choice.
7. Set a first-price range, not a final number. State a floor and a ceiling with one reason each. Spark's own floor is £2,000 fixed; do not price a serious professional-services build below it without a reason written down.

## The artefact
Writes `05-sale/PRICING-MODEL.md` in Markdown. What good looks like: the customer success metric restated in one line; the value metric named in three words or fewer; the chosen model with a two-sentence reason; a four-row comparison table (model, when it wins, verdict) with three rejected rows carrying a one-line reason each; any Jersey or regulatory constraint noted; and a first-price floor and ceiling with a reason for each. Use the template in `${CLAUDE_SKILL_DIR}/references/pricing-model-template.md`.

## Done when
One model is chosen and named, the value metric is named, and each of the three rejected models has a written one-line reason. The file also carries a price floor and ceiling.

## Log it
Append one line to CHANGELOG.md via the logbook helper: date, `d5-pricing-model`, `05-sale/PRICING-MODEL.md`, and the numeric result (the chosen floor, for example "floor GBP 2,000"). Record the choice and its reason in DECISIONS.md. Update `.spark/state.json` through the journey-state helper: set the Day 5 target or outcome to reflect the chosen model. Use the exact helper paths:
- log: `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`
- state: `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`

## If it goes wrong
If you genuinely cannot separate two models, default to the one-off build fee for hardware and services and pay-for-access plus build-in-partnership for software, and write "provisional, revisit after first sale" in the reason. A provisional model you can price today beats a perfect model you argue about all week. If the success metric will not sharpen into a number, go back to `d2` and fix the proposition before pricing anything.
