---
name: Start
description: The front door of the sprint. Captures your name, path, one-sentence idea, bootcamp Monday and numeric weekly target, then opens the journey. Run first.
when_to_use: Run once, 2 to 4 weeks before your bootcamp Monday, before any other skill except doctor. Initialises .spark/state.json and hands you to the coach.
---

# Start

**What this does.** Sets up your sprint: name, business type, one-sentence idea, your bootcamp Monday, and the one number you chase that week. Writes `.spark/state.json` and points you at the coach.
**Why it matters.** The interviews that make Day 1 work get booked weeks in advance, so this runs 2 to 4 weeks early. Four sharp decisions now mean the week aims at a real buyer instead of ending busy with nothing to sell.
**You are ready for this when.** You have a rough idea and an hour. This reads nothing; the idea comes from you.

You can run each day in a fresh session (or `/clear`); coach rebuilds your position from disk, so nothing is lost.

## Before you start
No prior artefact, this is step zero. Do not overthink the idea. It needs to be clear enough to invite the right interviewees; the deep development conversation happens on Day 1, and Days 1 and 2 prove or kill it.

## Steps
1. **Get their first name.** Use it from here on. No titles.
2. **Pick one path.** `software` (code that runs), `hardware` (a physical object you ship), `services` (productised time and expertise). If it is a mix, choose the part the customer pays for first.
3. **Write the idea as ONE sentence, together.** Ask where the idea came from and who it is for before touching the wording; a couple of genuine questions beat a template. Then shape their answer: "[product] helps [who] do [job] so they [get outcome]." If it will not fit one line, it is not clear enough to sell; keep talking until it does. Their words, not yours.
4. **Name the bootcamp Monday.** Ask which Monday the week starts. For the Digital Jersey autumn cohort that is Monday 14 September 2026. Write it as an ISO date; every interview invitation points at it.
5. **Set the headline target with a number.** Ask: "What does success look like by that Friday, as a number?" Pass: "one paying customer at GBP 2,000+", "3 signed pilots". Fail: "validate the market". No number, no proceeding. Prefer one paying customer over any vanity metric.
6. **Read it back.** Say all five aloud (name, path, idea, Monday, target) and get an explicit "yes" before writing.
7. **Initialise state** via the journey-state helper (never hand-edit):

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
     --patch '{"founder":"<first name>","business_type":"<software|hardware|services>","idea":"<the one sentence>","headline_target":"<the target with its number>","current_day":1,"prework":{"bootcamp_monday":"<YYYY-MM-DD>","interviews_booked":0,"complete":false}}'
   ```

   It creates `.spark/` and day folders and sets the five-day skeleton. See `references/state-shape.md` for the exact object.

## The artefact
Writes `.spark/state.json` via the journey-state helper. Good: `founder` a name, `business_type` one allowed string, `idea` a single sentence, `headline_target` has a digit, `prework.bootcamp_monday` an ISO date, `current_day` is `1`. Read it back to validate.

## Done when
1. `.spark/state.json` exists and parses as valid JSON.
2. `business_type` is exactly `software`, `hardware` or `services`.
3. `idea` is one sentence (one full stop, no line breaks).
4. `headline_target` contains at least one digit.
5. `prework.bootcamp_monday` is a real Monday in the future.
6. You have told the founder to run `/spark-bootcamp:coach`.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill start \
  --artefact ".spark/state.json" \
  --result "<the headline target>"
```
Then: "You are set up. Run `/spark-bootcamp:coach` and I will walk you through the pre-work: booking your Day 1 interviews starts now, not on the Monday."

## If it goes wrong
- **Helper missing or errors.** Do not hand-write `.spark/state.json`; a malformed file breaks every later skill. Tell the founder journey-state has not installed and stop. Fix by reinstalling.
- **Founder resists a number.** Do not proceed. Offer three sharp path-specific options (services: "3 signed pilots", "GBP 5,000 booked", "1 client at GBP 2,000+") and let them pick.
- **Idea will not fit one sentence.** Usually two ideas tangled. Ask which one a customer pays for first, start there.
