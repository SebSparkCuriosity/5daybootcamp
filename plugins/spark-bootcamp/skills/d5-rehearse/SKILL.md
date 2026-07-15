---
name: Rehearse The Sale
description: Role-plays the sale until the ask feels natural. Objection handling, the money ask, and the close. Use on Day 5 before you get on a real call.
when_to_use: Day 5, after the proposal and messaging exist, before the live sales conversation with a real prospect.
---

# Rehearse The Sale

**What this does.** Runs a full sales role-play, drills 8 or more objections until you have a crisp answer to each, and makes you say the price out loud until it stops wobbling.
**Why it matters.** The sale is not won by the deck. It is won by whether you can name the price without flinching and answer the "it's too expensive" line without apologising. Most first-time founders freeze at exactly those two moments. We fix that here, in private, before it costs you a real customer.
**You are ready for this when.** `05-sale/PROPOSAL.md` and `02-market/messaging.md` both exist, and Day 4 produced an objections list.

## Before you start
Read these, in this order:

- `05-sale/PROPOSAL.md`: the offer, the scope, the price. This is what you are selling.
- `02-market/messaging.md`: the words that already land with this buyer.
- `04-gtm/messaging.md` (or wherever d4-icp-messaging wrote its objections): the objections you already flagged.
- `.spark/state.json`: `business_type`, so you rehearse the right ask (a subscription, a pre-order, a booked engagement).

Guardrail: this is rehearsal only. Do not contact a real prospect from inside this skill. The live call is the next step, after you sign off that you are ready.

## Steps
1. Pull the price and the ask out of `PROPOSAL.md` and write them at the top of a scratch note, in one sentence each. Example: "The price is £2,000, fixed. The ask is: shall we start Monday?" If you cannot state both in one breath, the proposal is not ready and you go back a step.

2. Build the objection bank. Run the helper to seed it from your Day 4 list plus the eight objections every Jersey buyer raises:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build-objections.py \
     --day4 04-gtm/messaging.md \
     --out 05-sale/OBJECTIONS.md
   ```

   If the file path differs, pass the real one. The script never crashes on a missing file, it just falls back to the standard eight. See `${CLAUDE_SKILL_DIR}/references/objection-library.md` for the full set and model answers.

3. Answer every objection in your own words. For each one, write the answer in three parts: acknowledge (one line), reframe (the number or the proof), redirect (a question that moves forward). Do not argue. A price objection is usually a value question wearing a costume.

4. Rehearse the money ask out loud. Say the price, then stop talking. Silence after the number is the whole skill. Say it ten times until you no longer add "but we could be flexible" on the end. Time yourself: the ask should take under 8 seconds and end on a question.

5. Run one full role-play, start to close. Claude plays the buyer. Use the scripted flow below and have Claude throw at least 3 objections from your bank mid-conversation, unannounced. Do not read from a page. Play the whole thing through once without stopping, even when it gets awkward.

6. Score the run against the checklist in `references/roleplay-flow.md`: did you open with their problem, did you name the price without hedging, did you handle every objection with acknowledge/reframe/redirect, did you actually ask for the close. If you miss any, run it again. Two clean runs beats one lucky one.

7. Write the final `SALE-SCRIPT.md`: your opening, your discovery questions, the demo or sample walkthrough branched to your path, the ask, and the two closes (the assumptive close and the fallback close).

## For software
The ask is usually a paid pilot or first month, not a signature on a twelve-month contract. Rehearse pointing at the live URL: "you saw it work, here is what the first month costs." The close is "shall I turn on your account today?".

## For hardware
You are asking for real payment intent, not a handshake. Rehearse the pre-order ask against the render or mock: "the deposit is £X, fully refundable until we ship, and it holds your place in the first batch." The close is "shall I take the deposit now?".

## For services
You are selling the productised package and one sample deliverable. Rehearse anchoring on the sample: "this is what you get, the fee is £X for the package." The close is "shall I send the intake link so we start this week?".

## The artefact
Writes two files:

- `05-sale/SALE-SCRIPT.md` (Markdown): the full flow, opening to close, branched to your business path, with the price and the ask stated in plain words.
- `05-sale/OBJECTIONS.md` (Markdown): every objection with your three-part answer, at least 8 of them, seeded by the helper and finished in your voice.

What good looks like: you can read neither file and still run the call, because saying it aloud eight times put it in your head.

## Done when
- One full role-play has been played start to close.
- 8 or more objections are answered in `OBJECTIONS.md`, each with acknowledge, reframe and redirect.
- The money ask has been said aloud (rehearsed, not just written), ends on a question, and takes under 8 seconds.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the numeric result (objections rehearsed):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-rehearse \
  --artefact 05-sale/SALE-SCRIPT.md \
  --result "1 full role-play, 12 objections answered, ask rehearsed"
```

Then update state via the journey-state helper (Day 5 progress, and add both artefacts):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"target":"Sale rehearsed","outcome":"12 objections, ask under 8s","complete":true}}}' \
  --append-artefact '{"skill":"d5-rehearse","path":"05-sale/OBJECTIONS.md","result":"12 objections answered"}'
```

## If it goes wrong
If the role-play keeps collapsing at the price, the problem is upstream, not here. Go back to `PROPOSAL.md` and check the value is quantified: a number the buyer keeps or earns that is visibly bigger than the fee. Rehearsing confidence into a weak offer does not work. Fix the offer, then come back and drill the ask again.
