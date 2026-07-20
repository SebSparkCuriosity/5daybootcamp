---
name: Rehearse The Sale
description: Role-play the sale until the ask feels natural. Objection handling, the money ask, the close. Day 5, before a real call.
when_to_use: Day 5, after the proposal and messaging exist, before the live sales call.
---

# Rehearse The Sale

**What this does.** Runs a full sales role-play, drills 8+ objections, and makes you say the price out loud until it stops wobbling.
**Why it matters.** The sale is won by naming the price without flinching and answering "it's too expensive" without apologising, and we fix both here, in private, before it costs you a real customer.
**You are ready for this when.** `05-sale/PROPOSAL.md` and `02-market/messaging.md` exist, and Day 4 produced an objections list.

## Before you start
Read `05-sale/PROPOSAL.md` (offer, scope, price), `02-market/messaging.md`, the Day 4 objections (`04-gtm/messaging.md`), and `.spark/state.json` for `business_type`.
Guardrail: rehearsal only. Do not contact a real prospect from here.

## Steps
1. Write the price and the ask at the top of a scratch note, one sentence each. If you cannot state both in one breath, the proposal is not ready: go back a step.
2. Build the objection bank from your Day 4 list plus the standard eight:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build-objections.py \
     --day4 04-gtm/messaging.md \
     --out 05-sale/OBJECTIONS.md
   ```
   The script falls back to the standard eight on a missing file. Model answers: `${CLAUDE_SKILL_DIR}/references/objection-library.md`.
3. Answer every objection in your own words, three parts: acknowledge, reframe (number or proof), redirect (a forward question). Do not argue.
4. Rehearse the ask out loud. Say the price, then stop. Say it ten times until you drop "but we could be flexible". Under 8 seconds, ending on a question.
5. Run one full role-play, start to close. Claude plays the buyer and throws 3+ objections unannounced. Play it through without stopping.
6. Score against `references/roleplay-flow.md`. Miss any and run it again. Two clean runs beats one lucky one.
7. Write `05-sale/SALE-SCRIPT.md`: opening, discovery questions, demo/sample walkthrough (branched to your path), the ask, and both closes (assumptive and fallback).

## For software
Ask for a paid pilot or first month, not a 12-month signature. Point at the live URL. Close: "shall I turn on your account today?".

## For hardware
Ask for real payment intent against the render or mock: "the deposit is £X, refundable until we ship, holds your batch place." Close: "shall I take the deposit now?".

## For services
Anchor on the sample deliverable: "this is what you get, the fee is £X for the package." Close: "shall I send the intake link so we start this week?".

## The artefact
Writes `05-sale/SALE-SCRIPT.md` (full flow, branched, price and ask in plain words) and `05-sale/OBJECTIONS.md` (8+ objections, each with acknowledge/reframe/redirect). Good means you can run the call without reading either.

## Done when
- One full role-play played start to close.
- 8+ objections answered in `OBJECTIONS.md`, each with acknowledge, reframe and redirect.
- The money ask said aloud, ending on a question, under 8 seconds.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-rehearse \
  --artefact 05-sale/SALE-SCRIPT.md \
  --result "1 full role-play, 12 objections answered, ask rehearsed"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"outcome":"12 objections, ask under 8s"}}}' \
  --append-artefact '{"skill":"d5-rehearse","path":"05-sale/OBJECTIONS.md","result":"12 objections answered"}'
```

## If it goes wrong
If the role-play keeps collapsing at the price, the problem is upstream. Go back to `PROPOSAL.md` and check the value is quantified: a number the buyer keeps or earns, visibly bigger than the fee. Fix the offer, then drill the ask again.
