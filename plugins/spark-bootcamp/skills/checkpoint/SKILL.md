---
name: Checkpoint
description: Bookends each day with a number. Run "checkpoint open" to set today's one target, "checkpoint close" to record the actual outcome and mark the day done.
when_to_use: Twice a day, every day of the sprint. Open first thing each morning to commit to one number; close last thing at night to record what really happened and unlock tomorrow.
argument-hint: [open|close]
---

# Checkpoint

**What this does.** Puts a number at both ends of every day: one target you commit to in the morning, one honest outcome you record at night.
**Why it matters.** Five days is short and a day with no target is a day you cannot grade. This is the discipline that keeps the whole sprint pointed at a paying customer instead of feeling busy. Open sets the number. Close tells the truth about it. Nothing gets marked done without a result you could read off a page.
**You are ready for this when.** `.spark/state.json` exists, which means `/spark-bootcamp:start` has run. That is the only prerequisite.

## Before you start
This skill reads `.spark/state.json` (via the display script below, read only) and writes to it (via the journey-state helper). It touches nothing else. It never does the day's work; it bookends it.

One guardrail: this is a human-in-the-loop step. The founder names the number. You sharpen it and read it back, but you do not write anything until they say yes. No target invented on their behalf, no outcome logged that they have not confirmed.

The argument decides the mode. `open` runs in the morning, `close` at night. If no argument is given, ask which one they mean before doing anything.

## Steps

First, work out where the founder is. Run the display script; it prints the briefing you will talk through. It reads `.spark/state.json` read only, so it is safe to run any time.

```
python3 "${CLAUDE_SKILL_DIR}/scripts/checkpoint.py" <open|close>
```

### For "open" (morning)

1. **Read yesterday back.** The script prints yesterday's target and outcome (or, on Day 1, the week's headline target). Say it to the founder in one line so today builds on something real, not a blank page.
2. **Name today's shape.** The script prints the day's job in one line, for example "ship the smallest slice a real prospect can act on". That is the shape, not the target.
3. **Get ONE number.** Ask the founder for a single target they commit to by tonight. One, not three. It must be observable and countable: you could tell at 6pm whether it happened. If they cannot name a number, do not open the day. Reshape it with them. `references/day-targets.md` has a menu of targets that pass, by path and by day, to prompt them. Never impose one; help them pick.
4. **Read it back and get a yes.** Say the target aloud. Get an explicit "yes, that's it" before you write.
5. **Write the target.** Only after the yes:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" set-day \
     --day <n> --target "<the one confirmed target, with its number>"
   ```

   Use the current day number the script reported. Do not hand-edit `state.json`; the helper serialises writes so parallel skills never clobber each other.

### For "close" (night)

1. **Show the target.** The script prints the target the founder committed to this morning. Say it back.
2. **Get the actual outcome.** Ask what really happened, with the number. Hit, beat or miss, you log the truth. No rounding up. If they hit 6 interviews against a target of 10, the outcome is "6 interviews held", not "good progress".
3. **Check the day's artefacts.** The script lists what was logged under today's folder. If the founder did the work but nothing is logged, the day's skills did not finish cleanly. Sort that before closing.
4. **On Day 4, clear the Thursday gate.** This is the one that decides the week. Before you close Day 4, answer one question out loud: is the Friday sales meeting booked, with a named prospect and a time in the diary? If yes, close and move on. If no, stop. Friday has nothing to close without a booked meeting, so the real Day 4 job is not done. Do not mark Day 4 complete until that slot is confirmed. The script prints this gate for you.
5. **Read the outcome back and get a yes.** Confirm the wording before you write.
6. **Write the outcome and mark the day complete.** Only after the yes:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" set-day \
     --day <n> --outcome "<what actually happened, with the number>" --complete
   ```

   Then advance the sprint to tomorrow (skip this after Day 5, which is the last day):

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" set-current-day <n+1>
   ```

7. **Point at tomorrow.** The script prints tomorrow's first command. Say it in plain words: "Tomorrow, open with `/spark-bootcamp:d2-market-map`." After Day 5, point them at `/spark-bootcamp:coach` to see where they landed.

## The artefact
No new file. Checkpoint's output is the state itself: `.spark/state.json`, updated via the journey-state helper. After `open`, `days.<n>.target` holds one string with a digit in it. After `close`, `days.<n>.outcome` holds the real result and `days.<n>.complete` is `true`, and `current_day` has advanced (except after Day 5). What good looks like: read the day back and both the target and the outcome name a number.

## Done when
One of these is true, depending on the mode:
- **open**: `days.<n>.target` is set to one confirmed string containing at least one digit, and the founder said yes to it.
- **close**: `days.<n>.outcome` is set to the actual result, `days.<n>.complete` is `true`, and (for Days 1 to 4) `current_day` has advanced by one. On Day 4 close specifically, the Thursday gate has been answered out loud before the day was marked complete.

## Log it
On **close** only, append one line to `CHANGELOG.md` summarising the day, target against outcome:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill checkpoint \
  --artefact ".spark/state.json" \
  --result "Day <n> closed: target <target>, outcome <outcome>"
```

The state write in the steps above is the state update, so there is no separate one here. `open` does not log to the CHANGELOG; it only sets the target. Setting a target is a plan, not an outcome, and the logbook records outcomes.

## If it goes wrong
- **The journey-state helper is missing or errors.** Do not hand-edit `.spark/state.json`. A malformed state file breaks every skill after this one. Tell the founder the journey-state skill has not installed correctly and stop. The fix is reinstalling the plugin, not patching the file.
- **The founder will not name a number at open.** That is the signal, not an obstacle. Offer three sharp options for their path from `references/day-targets.md` and let them pick or adapt. No number, no open.
- **They want to close a day they never opened.** There is no target to grade against. Run `checkpoint open` first, set the number, then close. A day with no target cannot be marked complete honestly.
- **Day 4 gate fails and they want to close anyway.** Hold the line, warmly. Closing Day 4 without a booked Friday meeting means Day 5 has no sale to make. The kind thing is to keep the day open and help them book the slot, not to wave it through.
