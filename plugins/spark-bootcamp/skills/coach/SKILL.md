---
name: Coach
description: Your always-on guide. Run it any time you are lost and it tells you where you are, what you have finished, and the one command to run next.
when_to_use: Any point in the five days when you are unsure what to do next. Run it after start, between skills, at the top of each day, or whenever you lose the thread.
---

# Coach

**What this does.** Reads your journey state, works out exactly where you are in the five days, and shows you three things: where you are, what you have finished, and the one command to run next.
**Why it matters.** Five days move fast and it is easy to lose the thread, especially when a day has several steps. The coach is the map. It never does the work for you and it never sends you down two paths at once. It points at one next move so you always know the single thing to do now.
**You are ready for this when.** You have run `/spark-bootcamp:start` at least once, so `.spark/state.json` exists. If you have not, the coach will notice and send you to start.

## Before you start
The coach reads one file: `.spark/state.json`, via the routing script. It reads nothing else and writes nothing. It is safe to run as often as you like.

It also checks the day folders (`01-discovery/` through `05-sale/`) to see which artefacts already exist. That is how it knows which step you have reached inside the current day.

One rule: the coach only points. It will not run the next skill for you, and it will not do the work of any day. That is deliberate. You stay in control, and every real step is an explicit choice you make.

## Steps
1. Run the routing script from the founder's project root:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/coach-route.py"
   ```

   If the founder is working in a subfolder, pass the project root explicitly:
   `python3 "${CLAUDE_SKILL_DIR}/scripts/coach-route.py" /path/to/project`. The script walks up the tree to find `.spark/state.json`, so most of the time no argument is needed.

2. Read the three blocks it prints back to the founder, warmly and by their first name. Do not add a fourth thing. The whole point of the coach is one clear next move, so resist the urge to list options.

3. Hand them the single command from the "Your next move" block. Say it plainly: "Run this next." Then stop. Let them run it.

4. If they ask "what comes after that?", tell them to run the coach again once the step is done. The map updates itself from state, so it will always be current. Do not read the whole week out to them; that is how founders freeze.

## The artefact
The coach produces no artefact. It is pure navigation. Its output is the three blocks printed to screen: WHERE YOU ARE, WHAT YOU HAVE FINISHED, YOUR NEXT MOVE. What good looks like: the founder can see their day, their target, what is already logged, and exactly one command to run, with no ambiguity about which.

The routing logic lives in `scripts/coach-route.py`, and the human-readable map of days and skills is in `references/journey-map.md`.

## Done when
All three are true:
1. The founder has been shown their current day (1 to 5) and that day's target, read from `.spark/state.json`.
2. They have been shown what is finished so far: the days signed off and the count of artefacts logged.
3. They have been given exactly 1 next command to run, and no second option.

## Log it
The coach deliberately does not write to `CHANGELOG.md` and does not update `.spark/state.json`. It produces no artefact and it runs many times a day, so logging every run would bury the real work in noise. The changelog stays a clean record of things built, not things checked. The skills the coach points at do their own logging when they finish. This is the one skill in the plugin that reads state and never writes it.

## If it goes wrong
- **No `.spark/state.json` yet.** The script says so and sends the founder to `/spark-bootcamp:start`. That is the correct first move; do not try to route around it.
- **The state file will not parse.** The script reports the error in plain words and points at `/spark-bootcamp:start` to rebuild it. Never hand-patch `state.json`; a malformed spine breaks every skill downstream.
- **The next command names a skill the founder cannot find.** The routing table in `scripts/coach-route.py` is the source of truth. If a day's skills shipped under different ids, update the map there in one place and re-run. The founder should still be told their day and which folder the work lands in.
- **`python3` is not found.** Run `/spark-bootcamp:doctor` to check the setup, then run the coach again.
