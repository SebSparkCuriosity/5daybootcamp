---
name: Logbook
description: Owns the one logging format every skill appends to. Internal helper. Every skill that makes an artefact or a decision calls it, so the audit trail stays consistent.
when_to_use: Internal only. Any skill calls the helper documented here at the end of its work to append to CHANGELOG.md and register the artefact in state.json, or to record a decision in DECISIONS.md. Not invoked directly by the founder.
user-invocable: false
---

# Logbook

**What this does.** Defines the one logging format for the whole bootcamp and hands every other skill a single helper to append to it: a changelog line plus an artefact record, or a decision with its rationale.
**Why it matters.** Auditable by default is the Spark promise. If ten skills each invent their own log format, the trail is useless. This skill removes that: one format, one helper, every write consistent, and CHANGELOG.md and state.json never drift apart. It produces no artefact of its own. It is the plumbing under everyone else's.
**You are ready for this when.** Always. Skills call it at the end of their work.

## Before you start
Never open `CHANGELOG.md` or `DECISIONS.md` with `Edit` or `Write`, and never append the artefact to `state.json` by hand. Go through the helper, every time. It creates each file with a header on first use, keeps the pipe format intact, and calls the journey-state helper for you so the log and the state stay in step.

## The format
One line per event, newest at the bottom.

CHANGELOG.md: `YYYY-MM-DD HH:MM | <skill-id> | <artefact path> | <numeric result>`

DECISIONS.md: `YYYY-MM-DD HH:MM | <decision> | <rationale>`

The `<numeric result>` is the point. Every artefact this plugin makes carries a number or an observable fact ("10 interviews targeted", "1 landing page live", "GBP 2,000 price set"). Put that number here. A log line with no number is a smell: go back and give the work a target.

## Steps
1. When your skill has written its artefact, log it. Call the helper once, with your skill id, the artefact path (relative to the project root), and the numeric result:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
     --skill "d1-define-interviewees" \
     --artefact "01-discovery/interview-target-spec.md" \
     --result "10 interviews targeted"
   ```
   This appends the changelog line and registers the artefact in `state.json.artefacts` via the journey-state helper, in one call. You do not append the artefact separately.
2. When your skill helps the founder make a real decision with a reason behind it (which path, which segment, which price), record it:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
     --decision "Chose the services path" \
     --rationale "Founder already sells advisory hours; fastest route to a paying customer"
   ```
   Keep the rationale to one line. If it needs a paragraph, it is two decisions.
3. Read the helper's last line. `LOG_RESULT=OK` means the log line landed and the state was updated. `LOG_RESULT=PARTIAL` means the changelog line landed but the state was not updated (the journey-state helper was missing or errored): tell the founder, and note it, but do not treat it as a hard failure. The artefact still exists and the log still records it.

## The artefact
None. This skill writes no output of its own. It writes into two shared files, CHANGELOG.md and DECISIONS.md, on behalf of whichever skill called it, and updates `state.json.artefacts` through the journey-state helper.

## Done when
The calling skill can point to exactly one new line at the bottom of CHANGELOG.md (or DECISIONS.md) carrying today's date and, for a changelog line, a number in the last field. One event, one line.

## Log it
This skill is the log. There is nothing further to record. The helper it owns is what every other skill's "Log it" step calls.

## If it goes wrong
The helper never crashes. If it cannot reach the journey-state helper it still writes the changelog line and prints `LOG_RESULT=PARTIAL` with the reason, so the trail is never lost. If a field contains a pipe or a newline the helper swaps it for a safe character so the format stays parseable. If CHANGELOG.md or DECISIONS.md is somehow unwritable, the helper prints the error and exits non-zero: check the folder is the project root and that you have write permission, then run the same command again. It only ever appends, so re-running after a fix is safe.
