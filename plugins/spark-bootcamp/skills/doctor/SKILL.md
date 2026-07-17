---
name: Doctor
description: Verifies your machine, builds the project skeleton, and writes the pre-work checklist. Run once, first, right after installing.
when_to_use: The very first command, before /spark-bootcamp:start. Re-run any time a later day says a tool is missing.
---

# Doctor

**What this does.** Verifies your machine has the tools the week needs, builds your empty project skeleton, and writes the pre-work checklist for the weeks before your bootcamp Monday.
**Why it matters.** Three bits of pre-work take weeks, not minutes: booking your Day 1 interviews (nobody is free tomorrow), a bank account that can receive money, and a trading entity. Doctor surfaces them 2 to 4 weeks out, while there is still time.
**You are ready for this when.** You have installed the plugin and are sitting in the folder your project should live in.

Doctor verifies, it does not install, and never installs Claude Code itself (Digital Jersey runs a setup session for that). Missing tools get a fix and it carries on. Re-running is always safe: it never overwrites `CHANGELOG.md`, `DECISIONS.md`, or an existing `.spark/prework.md`.

## Before you start
First skill, so no prior artefact. Confirm the current directory is where the founder wants their project. If unsure, have them `cd` or agree a folder and create it.

## Steps
1. Confirm the project folder. The current working directory is where the skeleton lands. Get a yes before writing.
2. Run the check-and-scaffold script (verifies machine, lays out folders, writes report in one pass):
   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/doctor-check.sh" "$(pwd)" "${CLAUDE_SKILL_DIR}/references/prework.md"
   ```
   It prints a report and a final `DOCTOR_RESULT=READY ...` or `DOCTOR_RESULT=NEEDS_FIX ...`. Always exits cleanly, so read the report, not the exit code.
3. Read the report back in plain English. For each `[PASS]`, "that's sorted". For each `[FAIL]`/`[WARN]`, say what it means and read out the fix. Stay warm: a missing GitHub CLI is a five-minute job.
4. Node, GitHub, Supabase and Vercel only matter for the software build path. A hardware or services founder can leave those unticked on purpose.
5. Walk them through `.spark/prework.md`. Land the three slow items hard: booking the Day 1 interviews (invitations out 2 to 4 weeks before the bootcamp Monday), the business bank account (one to three weeks in Jersey) and the trading entity. Start all three today.
6. Make them name a week's budget in `.spark/prework.md` (a realistic week is GBP 10 to GBP 25 on free tiers). If the idea needs a paid API, name it and set a hard spend cap now.
7. Log it, then print the final line exactly as in "Done when".

## The artefact
Writes into the founder's project:
- `.spark/doctor-report.txt`: dated machine report, one line per check with a fix for failures, plus the layout it created. Plain text.
- The skeleton: `.spark/`, `.spark/brand/`, `.spark/deliverables/`, the pre-work folder (`00-prework`), the five day folders (`01-discovery` through `05-sale`), and empty-with-header `CHANGELOG.md` and `DECISIONS.md`.
- `.spark/prework.md`: the pre-work checklist, copied from this skill's `references/prework.md`. Its first section books the Day 1 interviews.

It does not create `.spark/state.json` (that belongs to `start`). The report notes this with a `[SKIP]` line.

## Done when
The summary reads `Needs a fix: 0` (all pass, or every unresolved item is a warning consciously skipped for the path), the nine folders and two logs exist, and `.spark/prework.md` is written. Then print exactly this and nothing after:
```
Ready. Run /spark-bootcamp:start
```
If any `[FAIL]` remains, do not print it. Read the fixes, let the founder act, run doctor again.

## Log it
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill doctor \
  --path .spark/doctor-report.txt \
  --result "machine verified, N checks passed, project laid out"
```
Do not touch `.spark/state.json`; it does not exist yet and `start` owns creating it.

## If it goes wrong
If the script cannot write (permissions), it prints the report to screen and marks the folder line `[FAIL]`. Move to a folder the founder owns (home is safest) and re-run.
If `python3` is missing, append the changelog line by hand: `YYYY-MM-DD  doctor  .spark/doctor-report.txt  machine verified, project laid out`.
If `bash` is missing on Windows, git working means Git Bash or WSL is present, so the script runs. If not, create the nine folders and two logs by hand, copy `references/prework.md` to `.spark/prework.md`, and note checks were manual.
