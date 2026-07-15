---
name: Nail The ICP
description: Nails one ideal customer profile and the words that move them, sharpened by real test feedback. Use on Day 4 after the product tests are scored.
when_to_use: Day 4 GTM, after d4-prioritise has ranked buyers and testers. The step where you decide exactly who you are selling to on Friday and the exact words you will use.
---

# Nail The ICP

**What this does.** Turns Monday's segment and Tuesday's proposition into one ideal customer profile with three hard criteria, one buyer-facing one-liner, and answers to the five objections real testers actually raised.
**Why it matters.** On Friday you will only reach a handful of people, and you will say roughly the same thing to each. If "who this is for" is fuzzy, you waste half of them on the wrong person and stumble on the first objection. This skill removes both risks. It steals the words that landed in your tests and drops the words that did not, so your Day 5 calls open warm and close cleaner.
**You are ready for this when.** `02-market/proposition.md`, `02-market/positioning.md` and `04-gtm/buying-signal-scorecard.csv` all exist.

## Before you start
Read these exact paths:
- `02-market/proposition.md`: the segment, the pain, the promise and the numeric outcome you committed to on Tuesday.
- `02-market/positioning.md`: where you sit against the alternatives, and the one-line USP. Your ICP must fit that position, not fight it.
- `04-gtm/buying-signal-scorecard.csv`: who scored Hot and Warm in the tests, and why. The Hot rows are your real ICP made flesh. Read what they had in common.
- `.spark/state.json` for `business_type` and the founder's name.
- `01-discovery/` interview notes and `04-gtm/tests/sessions/*.md` if they exist, for the customer's own words and the objections they raised out loud.

Do not invent an ICP from thin air. The scorecard already tells you who leaned in. Your job is to describe them precisely, not to guess.

Guardrail: this skill writes words, it sends nothing. The messaging feeds Day 5 outreach, which goes out only after your explicit sign-off.

## Steps
1. Read the Hot and Warm rows in the scorecard first. Note what the top scorers share: sector, size, role, the pain they named, the trigger that made them act. Patterns in real buyers beat any persona you could dream up.
2. Write the ICP as ONE sentence with exactly three criteria. Format: "A [role] at a [type and size of firm] who [observable trigger or pain]." Three criteria, no more. Each criterion must be something you can check before a call, not a mood. "A compliance lead at a Jersey trust firm of 20 to 80 staff who files client reviews by hand" is checkable. "An ambitious forward-thinker" is not.
3. Sanity-check the ICP against the scorecard. At least half your Hot rows should match all three criteria. If they do not, your criteria are wrong, not your buyers. Widen or swap a criterion until the Hot rows fit, then stop.
4. Write the one-liner: the single sentence you say when this exact person asks "so what do you do?". Format: "[We help] [the ICP] [reach the outcome] [without the pain]." Keep it under 20 words. Lead with their outcome, not your mechanism. Steal a phrase a Hot tester actually used if one fits.
5. Answer the five objections. List the five reasons this ICP gives for not buying, pulled from the test sessions and interviews where you have them. For each, write a two or three sentence answer that a nervous buyer would accept, backed by a number, a named result, a demo or a real quote. An objection with no evidence behind the answer is a weakness, so flag it as one to close before Friday.
   - The five almost always include price, trust, switching effort, "does it actually work", and timing. Use your real objections where you have them, these five as the fallback.
6. Branch by path (below) so the proof fits how your business earns trust.
7. Run the checker: `python3 ${CLAUDE_SKILL_DIR}/scripts/icp_check.py 04-gtm/messaging.md`. It counts the ICP criteria, the one-liner words and the answered objections, and prints PASS or names exactly what is missing. Fix what it flags and re-run until it passes.

The full template, the objection bank and a worked Jersey example live in `${CLAUDE_SKILL_DIR}/references/messaging-template.md`.

## For software
Your proof is the working slice on its public URL. Answer the "does it actually work" objection by pointing at what the deployed page visibly does and the number it hits: "reconciles a 200-line statement in 8 minutes, try it on yours". Answer switching effort with how little the buyer has to change to get started.

## For hardware
Your proof is the prototype and early demand. Answer "does it actually work" with the render or physical mock and the outcome it demonstrates. Answer trust and timing with the waitlist or pre-order count if you have one: "31 firms have put down intent" beats "lots of interest". Where you have no number yet, mark it a claim to prove, do not inflate it.

## For services
Your proof is the sample deliverable and your own track record. Answer "does it actually work" by showing the one finished sample and the time or cost it saved. Answer price by framing it against the hours the ICP spends today. Answer trust with a named result or a testimonial where you have one.

## The artefact
Writes `04-gtm/messaging.md` in Markdown, following `${CLAUDE_SKILL_DIR}/references/messaging-template.md`. It holds: the ICP sentence with its three criteria called out, the one-liner, the five objections each with an evidence-backed answer and an evidence flag, and a short note on which Hot testers the ICP is drawn from.

What good looks like: a teammate who missed the week can read the file and know exactly who to ring on Friday, what to open with, and what to say when the buyer pushes back, with a number or a quote behind every answer.

## Done when
- The ICP is one sentence with exactly 3 checkable criteria.
- The one-liner is under 20 words.
- 5 objections each have an answer, and `icp_check.py` prints PASS.

## Log it
Append one line to CHANGELOG.md via the logbook helper, recording the artefact path and the numeric result:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-icp-messaging \
  --artefact 04-gtm/messaging.md \
  --result "ICP set (3 criteria), one-liner <N> words, 5 objections answered"
```
Then update state via the journey-state helper, recording the Day 4 outcome and registering the artefact:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"ICP nailed to 3 criteria, one-liner and 5 answered objections ready for Day 5"}}}' \
  --append-artefact '{"skill":"d4-icp-messaging","path":"04-gtm/messaging.md","result":"ICP 3 criteria, one-liner <N> words, 5 objections"}'
```
If sharpening the ICP changed who you will call on Friday, or dropped a segment you had been chasing, log that as a dated decision with its rationale in DECISIONS.md (`log.py --decision "..." --rationale "..."`).

## If it goes wrong
- **Every Hot row looks different.** You are early, or your tests hit a mixed crowd. Pick the single Hot row with the strongest Pain and Budget and write the ICP around that one person. Note it is provisional and widen after Day 5.
- **Cannot get the one-liner under 20 words.** You are describing two customers or two outcomes. Cut to the one ICP and the one outcome that Friday depends on. The rest goes on the landing page later, not in the opening line.
- **An objection has no evidence behind its answer.** Do not fake proof. Downgrade the answer to an honest "here is how we would show you" and flag it red, so Day 5 opens by earning that proof rather than claiming it.
- **The checker will not run.** `04-gtm/messaging.md` is still the artefact of record. Count the three criteria, the one-liner words and the five objections by hand against the Done when list, and fix the script later. Never let a broken script block Day 4.
