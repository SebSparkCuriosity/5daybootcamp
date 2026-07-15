---
name: Checkpoint
description: Bookends each day with a number. "checkpoint open" sets today's one target; "checkpoint close" records the outcome and marks the day done.
when_to_use: Twice daily. Open each morning to commit to one number; close at night to record what happened and unlock tomorrow.
argument-hint: [open|close]
---

# Checkpoint

**What this does.** Puts a number at both ends of every day: one target committed in the morning, one honest outcome recorded at night.
**Why it matters.** A day with no target is a day you cannot grade, and this is the discipline that keeps the sprint pointed at a paying customer.
**You are ready for this when.** `.spark/state.json` exists (`/spark-bootcamp:start` has run).

## Before you start
Reads `.spark/state.json` (via the script, read only) and writes it via the journey-state helper. Human-in-the-loop: the founder names the number, you sharpen and read it back, write nothing until they say yes. If no argument is given, ask open or close first.

## Steps
Run the display script to see the briefing (reads state read only):

```
python3 "${CLAUDE_SKILL_DIR}/scripts/checkpoint.py" <open|close>
```

### For "open" (morning)
1. Read yesterday's target and outcome back (or Day 1's headline target) in one line.
2. State the day's job as printed. That is the shape, not the target.
3. Get ONE observable, countable number the founder commits to by tonight. No number, no open. `references/day-targets.md` has a menu to prompt them; never impose one.
4. Read it back, get an explicit yes.
5. Write it (only after the yes), using the current day number:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
     --patch '{"days":{"<n>":{"target":"<the one confirmed target, with its number>"}}}'
   ```

### For "close" (night)
1. Say back the target committed this morning.
2. Get the actual outcome with the number. Log the truth, no rounding up ("6 interviews held", not "good progress").
3. Check today's logged artefacts. If work was done but nothing logged, the day's skills did not finish cleanly. Sort that first.
4. On Day 4, clear the Thursday gate: is the Friday sales meeting booked, named prospect and time in the diary? If no, stop and help them book it. Do not mark Day 4 complete until confirmed.
5. Read the outcome back, get a yes.
6. Write the outcome and mark complete (only after the yes):

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
     --patch '{"days":{"<n>":{"outcome":"<what actually happened, with the number>","complete":true}}}'
   ```

   Then advance to tomorrow (skip after Day 5):

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
     --patch '{"current_day":<n+1>}'
   ```

7. Point at tomorrow's first command in plain words. After Day 5, point them at `/spark-bootcamp:coach`.

## The artefact
No new file. Output is `.spark/state.json` itself. After open, `days.<n>.target` holds one string with a digit. After close, `days.<n>.outcome` holds the real result, `days.<n>.complete` is `true`, and `current_day` has advanced (except after Day 5).

## Done when
- **open**: `days.<n>.target` is one confirmed string with at least one digit, and the founder said yes.
- **close**: `days.<n>.outcome` is set, `days.<n>.complete` is `true`, and (Days 1 to 4) `current_day` advanced by one. On Day 4, the Thursday gate was answered before completion.

## Log it
On **close** only, append one line to `CHANGELOG.md`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill checkpoint \
  --artefact ".spark/state.json" \
  --result "Day <n> closed: target <target>, outcome <outcome>"
```

Open does not log; setting a target is a plan, and the logbook records outcomes.

## If it goes wrong
- **journey-state helper missing or errors.** Do not hand-edit `.spark/state.json`. Tell the founder to reinstall the plugin, then stop.
- **Founder will not name a number at open.** That is the signal. Offer three sharp options from `references/day-targets.md`. No number, no open.
- **They want to close a day never opened.** Run `checkpoint open` first, set the number, then close.
- **Day 4 gate fails and they want to close anyway.** Hold the line warmly. Keep the day open and help them book the slot.
