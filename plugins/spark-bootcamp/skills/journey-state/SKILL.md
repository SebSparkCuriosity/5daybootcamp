---
name: Journey State
description: Owns .spark/state.json and the one safe read-merge-write helper every skill uses, so concurrent skills never clobber each other's fields.
when_to_use: Internal only. Any skill reading or writing journey state calls the helper here. Not run by the founder.
user-invocable: false
---

# Journey State

**What this does.** Defines `.spark/state.json` and gives every skill one safe read-merge-write helper so concurrent skills never overwrite each other.
**Why it matters.** Five days of skills share one small file, and this plumbing means no founder's work is ever lost to a clashing save.
**You are ready for this when.** Always. It is the plumbing under the plugin and produces no artefact.

## Before you start
Nothing to read first. The helper creates `.spark/state.json` from the default schema on first run. Never open, `Edit` or `Write` that file by hand. Go through the helper every time.

## The schema
Full field-by-field reference: `references/schema.md`. `.spark/state.json` is one JSON object with seven top-level fields: `founder` (first name), `business_type` (exactly `"software"`, `"hardware"` or `"services"`, set once, early), `idea` (one line), `headline_target` (the week's numeric promise), `current_day` (1 to 5), `days` (entries `"1"` to `"5"`, each `{target, outcome, complete}`), and `artefacts` (append-only list of `{skill, path, result, at}`).

## How every other skill calls it
One helper: `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`, run with `python3`. It prints the full new state to stdout.

- Read: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read`
- Change fields with a JSON merge patch (touches only named keys, nested keys merge): `python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --patch '{"days":{"1":{"complete":true,"outcome":"10 interviews booked"}}}'`
- Add an artefact (never via `--patch`, which replaces the whole array and loses history): `python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --append-artefact '{"skill":"d1-define-interviewees","path":"01-discovery/interview-target-spec.md","result":"10 interviews targeted"}'`
- Pipe a patch on stdin with `--patch -` when the JSON is large.
- `--file <path>` points it elsewhere (tests); otherwise it walks up to the nearest `.spark`.

## What the helper guarantees
Creates the file from default schema if missing. Writes atomically via temp file and `os.replace`, keeps a `.bak` of the previous state, and holds an exclusive lock per read-merge-write so parallel skills queue not collide. A corrupt file is moved to `state.json.broken`, reset to default, and reported on stderr.

## The artefact
None. Owns only `.spark/state.json`, touched only through the helper.

## Done when
`--read` prints a valid JSON object with all seven top-level fields, and a patch followed by a read shows exactly one field changed and the rest untouched.

## Log it
This skill does not log. The skills that call it do: each appends its own `CHANGELOG.md` line via logbook and records progress with `--patch` and `--append-artefact`.

## If it goes wrong
If stderr reports a move to `state.json.broken`, the last good copy is in `state.json.bak`: compare, and copy it back over `state.json` then re-run your patch if wanted. No `python3` means the plugin cannot run, so install Python 3. If locking is unavailable it proceeds unlocked with a quiet warning, so avoid two simultaneous writes.
