---
name: Doctor
description: Checks your machine, lays out your project, and prints the pre-work you must do before Monday. Run this once, first, straight after installing the plugin.
when_to_use: The very first command of the bootcamp, before /spark-bootcamp:start. Run it again any time a later day complains a tool is missing.
---

# Doctor

**What this does.** Verifies your machine has the tools the week needs, builds your empty project skeleton, and writes a pre-work checklist you can tick off before Monday.
**Why it matters.** Two bits of pre-work take days, not minutes: a bank account that can receive money, and a trading entity. You take a real payment on Friday, so if these are not started early the week stalls at the finish line. Doctor surfaces them now, while there is still time.
**You are ready for this when.** You have installed the plugin (`/plugin install spark-bootcamp@spark`) and you are sitting in the folder you want your bootcamp project to live in.

Doctor verifies, it does not install. It never installs Claude Code itself: Digital Jersey runs a setup session for that. If a tool is missing, doctor tells you exactly how to fix it and carries on.

## Before you start
Doctor reads nothing. It is the first skill, so there is no prior artefact. It writes into the current folder, so confirm with the founder that the current directory is where they want their project. If they are unsure, ask them to `cd` to the right place, or agree a folder name and create it first.

One guardrail: doctor never overwrites `CHANGELOG.md`, `DECISIONS.md`, or a `.spark/prework.md` that already exists. Re-running doctor is always safe.

## Steps
1. Confirm the project folder with the founder. The current working directory is where the skeleton lands. Get a yes before writing anything.
2. Run the check-and-scaffold script. It verifies the machine, lays out the folders, and writes the report in one pass:
   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/doctor-check.sh" "$(pwd)" "${CLAUDE_SKILL_DIR}/references/prework.md"
   ```
   The script prints a report and a final line, either `DOCTOR_RESULT=READY ...` or `DOCTOR_RESULT=NEEDS_FIX ...`. It always exits cleanly, so read the report, do not judge by an exit code.
3. Read the report back to the founder in plain English. For every `[PASS]`, a quick "that's sorted". For every `[FAIL]` or `[WARN]`, say what it means for them and read out the fix. Be warm about it: a missing GitHub CLI is a five-minute job, not a crisis.
4. Explain which warnings matter for their path, if they already know it. Node, GitHub, Supabase and Vercel only matter for the software build path. A hardware or services founder can leave those unticked on purpose. Do not nag them about tools they will never use.
5. Walk them through the pre-work checklist at `.spark/prework.md`. Do not let them close the session thinking it is optional. Land the two slow items hard: the business bank account (one to three weeks to open in Jersey) and the trading entity. Tell them to start those today.
6. Make them name a number for the week's budget. Open `.spark/prework.md`, find the budget line, and get them to write a figure (a realistic week is GBP 10 to GBP 25 because everything else runs on free tiers). If their idea needs a paid API, get them to name it and set a hard spend cap now.
7. Log it (see below), then print the final line exactly as written in "Done when".

This skill spends no money and sends nothing, so there is no outreach or payment to pause for. It only ever reads your machine and writes into your own project folder.

## The artefact
Writes three things into the founder's project:

- `.spark/doctor-report.txt`: the dated machine report, one line per check with a fix for anything that failed, plus the folder layout it created. Plain text.
- The project skeleton: `.spark/`, `.spark/brand/`, `.spark/deliverables/`, the five day folders (`01-discovery` through `05-sale`), and empty-with-header `CHANGELOG.md` and `DECISIONS.md`.
- `.spark/prework.md`: the Sunday-before checklist (accounts, entity and bank, domain and email, the budget), copied from this skill's `references/prework.md` for the founder to tick off.

It deliberately does not create `.spark/state.json`. That belongs to `/spark-bootcamp:start`, which writes it once the founder names the business and picks a path. The report notes this with a `[SKIP]` line so nothing looks missing.

What good looks like: the report ends `Passed: N   Needs a fix: 0`, every folder exists, and the founder can open `.spark/prework.md` and start ticking.

## Done when
The script's summary reads `Needs a fix: 0` (all checks pass, or every unresolved item is a warning the founder has consciously chosen to skip for their path), the eight folders and two logs exist, and `.spark/prework.md` is written. When that holds, print exactly this and nothing after it:

```
Ready. Run /spark-bootcamp:start
```

If any `[FAIL]` remains, do not print that line. Read the fixes, let the founder act, then run doctor again.

## Log it
Append one line to `CHANGELOG.md` through the logbook helper, recording that setup completed and how many checks passed:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill doctor \
  --path .spark/doctor-report.txt \
  --result "machine verified, N checks passed, project laid out"
```

Do not touch `.spark/state.json` here. It does not exist yet, and `start` owns creating it. Doctor is the one skill that runs before the state machine exists, so there is nothing to update, only the changelog to seed.

## If it goes wrong
If the script cannot write into the folder (a permissions error), it prints the report to screen instead of saving it and marks the folder line `[FAIL]`. Move to a folder the founder owns (their home directory is safest), then run doctor again.

If `python3` is not found when logging, append the changelog line by hand instead: open `CHANGELOG.md` and add one line in the format `YYYY-MM-DD  doctor  .spark/doctor-report.txt  machine verified, project laid out`. The logbook helper is only a convenience; the audit trail is the point.

If the founder is on Windows and `bash` is missing, they are running Git Bash or WSL under the hood already if git works, so the script runs. If it genuinely will not, create the eight folders and two log files by hand from the layout above, copy `references/prework.md` to `.spark/prework.md`, and note in the report that machine checks were done manually.
