---
name: Run Interview
description: Reusable interview engine. Runs a call as a live prompt sheet, then writes one record with 3+ verbatim quotes and logged consent. Modes discovery|product-test.
when_to_use: Day 1 discovery once per interview; again Day 4 product-test once per test session.
argument-hint: [discovery|product-test]
---

# Run Interview

**What this does.** Runs one customer call end to end: a live prompt sheet and note capture, then one structured record with context, three-plus verbatim quotes, the job and pain observed, and (product-test) a 0 to 5 buying-signal score with evidence.
**Why it matters.** The interview is where the truth lives and the easiest thing to do badly: ask about the future and people are kind and wrong, so this engine keeps you asking about the past in specifics and writing down what you actually saw.
**You are ready for this when.** Discovery: `01-discovery/interview-plan.md` exists and `00-prework/interview-schedule.md` holds today's booked calls. Product-test: you have built the thing (page, prototype or sample) and a tester in front of it.

## Before you start
Pick the mode. `discovery` (Day 1) understands the problem; `product-test` (Day 4) watches someone use what you built.

Reads: the craft in `interview-method` (`mom-test.md`, `jtbd.md`) via `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/`; the mode's prompt sheet at `${CLAUDE_SKILL_DIR}/references/prompt-sheet-discovery.md` or `prompt-sheet-product-test.md`; product-test scoring at `${CLAUDE_SKILL_DIR}/references/buying-signal-rubric.md`; consent from your `.spark/deliverables/data-protection/consent.md` if it exists, else the plugin reference.

Guardrail: real person, human in the loop. Log consent before a single question. If they decline recording, written notes only. Keep records in local files.

## Steps
1. Read `mom-test.md` and `jtbd.md`. Apply the one rule: ask for specifics in the past, not generics about the future.
2. Scaffold the record from your project root (creates the file, embeds consent, leaves slots):
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/new_session.py" --mode discovery --name "alex-trust-officer" --root .
   ```
   In product-test mode, drop `--name` and the script auto-numbers:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/new_session.py" --mode product-test --root .
   ```
3. Keep the matching prompt sheet beside you. Glance, do not read it out.
4. Log consent first: read the block aloud, fill the four fields (name or pseudonym, date, consent y/n, recording y/n). Do not start until consent is a clear yes.
5. Run the call from the sheet. Capture exact words in quote marks as you go. Aim for three or more verbatim quotes you could not have invented.
6. Fill the record straight after: context, the three-plus quotes, the job and pain in their language. Never write what you wish they had said.

## For software
Day 4 test is someone using your deployed slice on its public URL. Give one real task, then go quiet and watch where they stall. The step they hesitate at is your fix list.

## For hardware
Day 4 test is the prototype (CAD render or physical mock) next to the pre-order or waitlist page. Watch: do they understand it, and do they act. A sign-up with a real work email is the signal, a nod is not.

## For services
Day 4 test is the sample deliverable plus the bookable intake page. Watch whether the sample earns trust and whether they book. Booking, or committing a date, is the signal.

## Score the buying signal (product-test mode only)
Fill the `__ / 5` line using `buying-signal-rubric.md`. Score what they DID: 0 polite, 1 interest, 2 time, 3 reputation (intro or reference), 4 intent (signed with real details), 5 money now. Add one line of evidence naming the action ("signed the pre-order with a work email", not "seemed keen").

## The artefact
Discovery writes `01-discovery/interviews/<name>.md`; product-test writes `04-gtm/tests/sessions/session-NN.md`. Both Markdown, same spine: consent log, context, three-plus verbatim quotes, job and pain observed, next step. Product-test adds the score and its evidence. Good: a stranger could read it and know who you spoke to, their words, their job, and what they would commit.

## Done when
One record exists with consent logged (four fields filled) and three-plus verbatim quotes in quote marks. Product-test adds a 0 to 5 score with one line of evidence. Every `[TO COMPLETE]` marker is gone.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill run-interview \
  --artefact 01-discovery/interviews/alex-trust-officer.md \
  --result "4 verbatim quotes captured"
```
For product-test, point `--artefact` at the session file and set `--result` to the score. Then mark day progress (day 1 discovery, day 4 product-test):
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days": {"1": {"outcome": "5 discovery interviews recorded"}}}'
```

## If it goes wrong
If a reference or prompt sheet will not load, do not stall the call: fall back to the whole method in one line, ask about the past in specifics without pitching and score commitment over compliments, then warn the reference could not be read. If `state.json` or the consent file is missing, the scaffold script still writes a working record and names the consent source it used; if it fell back to the built-in block, run `data-protection` and paste the correct wording before the call. Fewer than three real quotes means the record is not done, usually from pitching or hypotheticals: run the next one closer to the Mom Test.
