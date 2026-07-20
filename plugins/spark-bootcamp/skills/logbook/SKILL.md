---
name: Logbook
description: The one logging format every skill appends to. Internal helper for a consistent audit trail across CHANGELOG.md, DECISIONS.md and state.json.
when_to_use: Internal only. Skills call this helper at the end of their work to log an artefact or record a decision. Not run by the founder.
user-invocable: false
---

# Logbook

**What this does.** Defines the one logging format for the bootcamp and hands every skill a single helper to append to it: a changelog line plus artefact record, or a decision with its rationale.
**Why it matters.** Auditable by default is the Spark promise, so one shared format keeps the trail useful and stops CHANGELOG.md and state.json drifting apart.
**You are ready for this when.** Always. Skills call it at the end of their work.

## Before you start
Never edit `CHANGELOG.md`, `DECISIONS.md` or `state.json.artefacts` by hand. Go through the helper. It creates each file on first use, keeps the pipe format intact, and updates state via the journey-state helper for you.

## The format
One line per event, newest at the bottom.

- CHANGELOG.md: `YYYY-MM-DD HH:MM | <skill-id> | <artefact path> | <numeric result>`
- DECISIONS.md: `YYYY-MM-DD HH:MM | <decision> | <rationale>`

Every artefact carries a number or observable fact. A log line with no number is a smell: go back and give the work a target.

## Steps
1. When your skill has written its artefact, log it once (path relative to project root). This appends the changelog line and registers the artefact in `state.json.artefacts` in one call, so do not append the artefact separately:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
     --skill "p0-interview-triage" \
     --artefact "00-prework/interview-target-spec.md" \
     --result "10 interviews targeted"
   ```
2. When the founder makes a real decision with a reason (path, segment, price), record it with a one-line rationale:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
     --decision "Chose the services path" \
     --rationale "Founder already sells advisory hours; fastest route to a paying customer"
   ```
3. Read the last line. `LOG_RESULT=OK` means log and state updated. `LOG_RESULT=PARTIAL` means the changelog landed but state did not (journey-state missing or errored): note it for the founder, but it is not a hard failure.

## The artefact
None. Writes into CHANGELOG.md and DECISIONS.md on behalf of the calling skill, and updates `state.json.artefacts` via journey-state.

## Done when
The calling skill can point to exactly one new line at the bottom of CHANGELOG.md (or DECISIONS.md) with today's date and, for a changelog line, a number in the last field.

## Log it
This skill is the log. Nothing further to record.

## If it goes wrong
The helper never crashes. If it cannot reach journey-state it still writes the changelog line and prints `LOG_RESULT=PARTIAL` with the reason. It swaps any pipe or newline in a field for a safe character. If a file is unwritable it prints the error and exits non-zero: check you are in the project root with write permission, then re-run. It only appends, so re-running is safe.
