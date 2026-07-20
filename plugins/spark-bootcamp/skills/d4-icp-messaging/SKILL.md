---
name: Nail The ICP
description: Turns your segment and proposition into one ideal customer profile, a buyer one-liner and answers to five real objections. Day 4.
when_to_use: Day 4 GTM, after d4-prioritise ranks buyers. Decide exactly who you sell to Friday and the words you use.
---

# Nail The ICP

**What this does.** Turns Monday's segment and Tuesday's proposition into one ideal customer profile with three hard criteria, one buyer-facing one-liner, and answers to the five objections real testers raised.
**Why it matters.** On Friday you reach only a handful of people and say roughly the same thing to each, so fuzzy targeting and a fumbled objection cost you half of them.
**You are ready for this when.** `02-market/proposition.md`, `02-market/positioning.md` and `04-gtm/buying-signal-scorecard.csv` exist.

## Before you start
Read: `02-market/proposition.md` (segment, pain, promise, numeric outcome), `02-market/positioning.md` (USP your ICP must fit), `04-gtm/buying-signal-scorecard.csv` (who scored Hot and Warm, and why), `.spark/state.json` (`business_type`, founder name), and `01-discovery/` notes plus `04-gtm/tests/sessions/*.md` for the buyer's own words and objections.

Describe the buyers the scorecard shows, do not invent a persona. Run the words as a short discussion (10 to 15 minutes): the founder says these sentences out loud on Friday, so they draft them with you, not receive them. Guardrail: this writes words only. Day 5 outreach goes out after your sign-off.

## Steps
1. Read the Hot and Warm rows. Note what top scorers share: sector, size, role, pain, trigger.
2. Write the ICP as ONE sentence, exactly three checkable criteria: "A [role] at a [type and size of firm] who [observable trigger or pain]."
3. Sanity-check: at least half your Hot rows must match all three criteria. If not, widen or swap a criterion until they fit, then stop.
4. Write the one-liner, under 20 words: "[We help] [the ICP] [reach the outcome] [without the pain]." Lead with their outcome. Steal a Hot tester's phrase if it fits.
5. Answer the five objections (usually price, trust, switching effort, "does it actually work", timing). The founder answers each out loud first, in their own words (they will have to on Friday); then tighten together to two or three sentences backed by a number, named result, demo or quote. Flag any answer with no evidence as one to close before Friday.
6. Branch by path (below) so the proof fits how you earn trust.
7. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/icp_check.py 04-gtm/messaging.md`. Fix what it flags, re-run until PASS.

Template, objection bank and worked example: `${CLAUDE_SKILL_DIR}/references/messaging-template.md`.

## For software
Proof is the working slice on its public URL. Answer "does it actually work" by pointing at what the page does and its number ("reconciles a 200-line statement in 8 minutes"). Answer switching effort with how little the buyer changes to start.

## For hardware
Proof is the prototype and early demand. Answer "does it actually work" with the render or mock and its outcome. Answer trust and timing with the waitlist or pre-order count ("31 firms have put down intent"). No number yet, mark it a claim to prove.

## For services
Proof is the sample deliverable and your track record. Answer "does it actually work" with the finished sample and the time or cost it saved. Answer price against the hours the ICP spends today. Answer trust with a named result or testimonial.

## The artefact
Writes `04-gtm/messaging.md` in Markdown per `${CLAUDE_SKILL_DIR}/references/messaging-template.md`: the ICP sentence with its three criteria, the one-liner, five objections each with an evidence-backed answer and evidence flag, and which Hot testers the ICP draws from. Good: a teammate who missed the week knows who to ring Friday, what to open with and what to say when pushed back.

## Done when
- ICP is one sentence with exactly 3 checkable criteria.
- One-liner is under 20 words.
- 5 objections each have an answer, and `icp_check.py` prints PASS.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-icp-messaging \
  --artefact 04-gtm/messaging.md \
  --result "ICP set (3 criteria), one-liner <N> words, 5 objections answered"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"ICP nailed to 3 criteria, one-liner and 5 answered objections ready for Day 5"}}}'
```
If sharpening the ICP changed who you call Friday, log a dated decision in DECISIONS.md (`log.py --decision "..." --rationale "..."`).

## If it goes wrong
- **Every Hot row differs.** Pick the row with strongest Pain and Budget, write the ICP around that one person, mark it provisional, widen after Day 5.
- **One-liner won't go under 20 words.** You are describing two customers or outcomes. Cut to the one Friday depends on.
- **An objection has no evidence.** Do not fake proof. Downgrade to an honest "here is how we would show you" and flag it red.
- **Checker won't run.** `04-gtm/messaging.md` is still the artefact. Count the criteria, one-liner words and objections by hand against Done when, fix the script later.
