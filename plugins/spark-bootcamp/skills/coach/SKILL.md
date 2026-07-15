---
name: Coach
description: Your always-on guide. Run it any time you are lost: it tells you where you are, what you have finished, and the one command to run next.
when_to_use: Any point in the five days when you are unsure what to do next. After start, between skills, at the top of each day.
---

# Coach

**What this does.** Reads your journey state and shows three things: where you are, what you have finished, and the one command to run next.
**Why it matters.** Five days move fast and it is easy to lose the thread, so the coach is the map that always points at your single next move.
**You are ready for this when.** You have run `/spark-bootcamp:start` at least once, so `.spark/state.json` exists.

## Before you start
Reads only `.spark/state.json` (via the routing script) and checks day folders `01-discovery/` through `05-sale/` to see which artefacts exist. Writes nothing. Safe to run repeatedly. The coach only points: it never runs the next skill or does the work.

## Steps
1. Run the routing script from the project root:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/coach-route.py"
   ```

   From a subfolder, pass the root: `python3 "${CLAUDE_SKILL_DIR}/scripts/coach-route.py" /path/to/project`. It walks up to find `.spark/state.json`.

2. Read the three blocks back to the founder warmly, by first name. Do not add a fourth thing.
3. Hand them the single command from "Your next move". Say "Run this next." Then stop.
4. If they ask what comes after, tell them to run the coach again once the step is done. Do not read the whole week out.

## The artefact
No artefact. Output is three blocks printed to screen: WHERE YOU ARE, WHAT YOU HAVE FINISHED, YOUR NEXT MOVE. Logic lives in `scripts/coach-route.py`; the day and skill map in `references/journey-map.md`.

## Done when
1. The founder has seen their current day (1 to 5) and that day's target from `.spark/state.json`.
2. They have seen what is finished: days signed off and count of artefacts logged.
3. They have exactly 1 next command, and no second option.

## Log it
Nothing. The coach never writes to `CHANGELOG.md` or `.spark/state.json`; it runs many times a day and the skills it points at do their own logging. This is the one skill that reads state and never writes it.

## If it goes wrong
- **No `.spark/state.json` yet.** The script sends the founder to `/spark-bootcamp:start`. Correct first move.
- **State will not parse.** The script reports the error and points at `/spark-bootcamp:start`. Never hand-patch `state.json`.
- **Next command names a skill not found.** The table in `scripts/coach-route.py` is the source of truth; fix ids there in one place and re-run.
- **`python3` not found.** Run `/spark-bootcamp:doctor`, then run the coach again.
