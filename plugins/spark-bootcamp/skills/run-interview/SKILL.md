---
name: Run Interview
description: The reusable interview engine. Runs a call live as a prompt sheet and note-capture, then writes one structured record with 3+ verbatim quotes and logged consent. Takes a mode [discovery|product-test].
when_to_use: Day 1 discovery, once per interview after your target and contacts are set. Again Day 4 in product-test mode, once per test session in front of the thing you built.
argument-hint: [discovery|product-test]
---

# Run Interview

**What this does.** Runs one customer conversation end to end: a live prompt sheet and note capture during the call, then one structured record after it, with the context, three or more verbatim quotes, the job and pain you observed, and in product-test mode a buying-signal score from 0 to 5 with the evidence. Consent is logged before you start.
**Why it matters.** The interview is where the truth lives, and it is the easiest thing in the week to do badly. Ask about the future and people are kind and wrong. Pitch, and the honest answers stop. This engine keeps you asking about the past, in specifics, capturing real words, and then forces you to write down what you actually saw while it is fresh. One clean record per call is what makes Day 1 synthesis and the Day 4 go or no-go possible.
**You are ready for this when.** In discovery mode, `01-discovery/interview-target-spec.md` exists and you have a call booked. In product-test mode, you have built the thing a prospect can act on (the live page, prototype or sample deliverable) and a tester in front of it.

## Before you start
Pick the mode. `discovery` is Day 1, understanding the problem. `product-test` is Day 4, watching someone use what you built.

This skill reads:
- The interview craft in `interview-method`: `mom-test.md` (ask about the past, never the hypothetical) and `jtbd.md` (frame the conversation around the job). Load the relevant one before the call via `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/`.
- The live prompt sheet for the mode: `${CLAUDE_SKILL_DIR}/references/prompt-sheet-discovery.md` or `${CLAUDE_SKILL_DIR}/references/prompt-sheet-product-test.md`.
- In product-test mode, the scoring rubric: `${CLAUDE_SKILL_DIR}/references/buying-signal-rubric.md`.
- Consent wording from `data-protection`: your filled `.spark/deliverables/data-protection/consent.md` if it exists, otherwise the plugin reference. The scaffold script pulls this in for you.

Guardrail: this is a human-in-the-loop call with a real person. Log consent before a single question. If they decline recording, take written notes only. Keep every record in local files, not the cloud, unless the person agreed to a specific tool.

## Steps
1. Read the craft. Open `mom-test.md` and, for the arc of the conversation, `jtbd.md`. You should be able to quote the one rule you are applying: ask for specifics in the past, not generics about the future.
2. Scaffold the record. Run from your project root, which creates the file, embeds the consent block, and leaves slots to fill:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/new_session.py" --mode discovery --name "alex-trust-officer" --root .
   ```
   In product-test mode, drop `--name`; the script auto-numbers the session:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/new_session.py" --mode product-test --root .
   ```
3. Open the matching prompt sheet and keep it beside you. Glance at it, do not read it out.
4. Log consent first. Read the consent block aloud or show it, then fill the four fields in the record: name or pseudonym, date, consent yes or no, recording yes or no. Do not start until consent is a clear yes.
5. Run the call from the prompt sheet. Capture their exact words in quote marks as you go. Quote now, paraphrase later. You are aiming for three or more verbatim quotes you could not have invented.
6. Fill the record straight after, while it is fresh: the context, the three-plus quotes, and the job and pain you observed in their language. Never write down what you wish they had said.

## For software
The Day 4 test is someone using your deployed slice on its public URL. Give them one real task, then go quiet and watch where they stall. The step they hesitate at is your fix list, not a moment to jump in and help.

## For hardware
The Day 4 test is the prototype (a CAD render or physical mock) next to the pre-order or waitlist page. Watch two things: do they understand what it is, and do they act on the page. A sign-up with a real work email is the signal, a nod is not.

## For services
The Day 4 test is the sample deliverable plus the bookable intake page. Watch whether the sample makes them trust the work and whether they will actually book. Booking, or committing a date, is the signal.

## Score the buying signal (product-test mode only)
Fill the `__ / 5` line using `buying-signal-rubric.md`. Score what they DID, not what they said: 0 polite, 1 interest, 2 time, 3 reputation (an intro or a reference), 4 intent (signed with real details), 5 money now. Write one line of evidence naming the specific action. "Signed the pre-order with a work email" is evidence; "seemed keen" is not.

## The artefact
Discovery mode writes `01-discovery/interviews/<name>.md`. Product-test mode writes `04-gtm/tests/sessions/session-NN.md`. Both are Markdown with the same spine: consent log, context, three-plus verbatim quotes, the job and pain observed, and a next step. The product-test record adds the buying-signal score and its evidence.

Good looks like: a stranger could read the record and know who you spoke to, what they said in their own words, what they were trying to get done, and (on Day 4) exactly what they were willing to commit.

## Done when
One record exists for the session with consent logged (the four fields filled) and three or more verbatim quotes in quote marks. In product-test mode, add a buying-signal score from 0 to 5 with one line of evidence. Every `[TO COMPLETE]` marker is gone.

## Log it
Append one line to CHANGELOG.md and record the artefact in state.json. Set the result to the observable outcome: quote count for discovery, the score for product-test.
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill run-interview \
  --artefact 01-discovery/interviews/alex-trust-officer.md \
  --result "4 verbatim quotes captured"
```
For a product-test session, point `--artefact` at the session file and set the result to the score, for example `--result "buying-signal 4/5, signed pre-order"`. Then mark day progress (day 1 for discovery, day 4 for product-test):
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days": {"1": {"outcome": "5 discovery interviews recorded"}}}'
```

## If it goes wrong
If the craft references or a prompt sheet will not load, do not stall the call. Fall back to the one line that is the whole method: ask about the past, in specifics, without pitching, and score commitment over compliments. Warn that the reference could not be read and carry on.

If `state.json` or the consent file is missing, the scaffold script still writes a working record and tells you which consent source it used. If it fell back to the built-in consent block, run `data-protection` to generate your own, then paste the correct wording into the record before the call.

If a call yields fewer than three real quotes, the record is not done. Usually the cause was pitching or hypothetical questions. Note it, and run the next one closer to the Mom Test.
