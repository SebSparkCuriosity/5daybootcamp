---
name: Journey State
description: Owns the shared .spark/state.json schema and the one safe helper every skill uses to read and update it, so no two skills ever clobber each other's fields.
when_to_use: Internal only. Any skill that needs to read or write journey state calls the helper documented here. Not invoked directly by the founder.
user-invocable: false
---

# Journey State

**What this does.** Defines the one shared state file, `.spark/state.json`, and hands every other skill a safe read-merge-write helper so concurrent skills never overwrite each other's fields.
**Why it matters.** Five days of skills all read and write the same small file. If two of them save at once, or one saves the whole object to change one field, work gets lost silently. This skill removes that risk: every write is a merge, atomic, backed up, and lock-guarded.
**You are ready for this when.** Always. This is the plumbing the rest of the plugin stands on. It produces no artefact of its own.

## Before you start
There is nothing to read first. The helper creates `.spark/state.json` from the default schema the first time it runs, so no skill has to check whether the file exists. Never open `.spark/state.json` by hand and never write it with `Edit` or `Write`. Go through the helper, every time.

## The schema
`.spark/state.json` is a single JSON object. These are its fields and nothing else invents new top-level keys without a good reason.

```json
{
  "founder": "",
  "business_type": "",
  "idea": "",
  "headline_target": "",
  "current_day": 1,
  "days": {
    "1": { "target": "", "outcome": "", "complete": false },
    "2": { "target": "", "outcome": "", "complete": false },
    "3": { "target": "", "outcome": "", "complete": false },
    "4": { "target": "", "outcome": "", "complete": false },
    "5": { "target": "", "outcome": "", "complete": false }
  },
  "artefacts": []
}
```

What each field means:

`founder` is the person's first name. `business_type` is exactly one of `"software"`, `"hardware"` or `"services"`, and it decides which path the build and ship skills follow, so set it early and set it once. `idea` is the one-line description of what they are building. `headline_target` is the single numeric promise for the week, for example "one paying customer by Friday". `current_day` is an integer 1 to 5.

`days` holds five entries keyed `"1"` to `"5"`. Each has a `target` (the day's numeric goal), an `outcome` (what actually happened, filled in at the end of the day) and `complete` (a boolean, true only when the day's done-condition is met).

`artefacts` is an append-only list. Each entry is `{ "skill": "d1-...", "path": "01-discovery/...", "result": "the numeric result", "at": "ISO timestamp" }`. Treat it as a history: add to it, never rewrite it.

## How every other skill calls it
There is exactly one helper: `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. Call it with `python3`. It prints the full new state to stdout so you can confirm the change landed.

To read the current state without changing anything:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read
```

To change one or more fields, pass a JSON merge patch. A merge patch touches only the keys you name and leaves everything else alone, so you never have to send the whole object:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"founder":"Seb","business_type":"services","current_day":1}'
```

Nested fields merge too. To mark Day 1 complete and record its outcome without disturbing the other days:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"1":{"complete":true,"outcome":"10 interviews booked"}}}'
```

To record that a skill produced an artefact, use `--append-artefact`. This adds one entry to the `artefacts` list and leaves the existing entries in place. The `at` timestamp is added for you if you omit it:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --append-artefact '{"skill":"d1-define-interviewees","path":"01-discovery/interview-target-spec.md","result":"10 interviews targeted"}'
```

You can pipe a patch on stdin instead of passing it as an argument, useful when the JSON is large or built by another tool. Use `-` as the value:

```bash
echo '{"headline_target":"one paying customer by Friday"}' \
  | python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --patch -
```

One rule to remember: to add an artefact, always use `--append-artefact`. If you send an `artefacts` array inside `--patch` it replaces the whole list, because a merge patch replaces arrays. That is the one way to lose history, so do not do it.

## What the helper guarantees
It creates `.spark/state.json` from the default schema if the file is missing, so no skill needs to bootstrap it. It writes atomically through a temporary file and `os.replace`, so a reader never sees a half-written file. It keeps a `.bak` copy of the previous state before every write. It takes an exclusive lock for the duration of each read-merge-write, so two skills running at once queue rather than collide. If it finds the file present but corrupt or half-written, it moves the bad copy to `state.json.broken`, resets to the default schema, and tells you on stderr rather than crashing.

It finds the state file by walking up from the current directory to the nearest `.spark` folder, falling back to `./.spark/state.json`. Pass `--file <path>` to point it somewhere else, for example in tests.

## The artefact
None. This skill owns the schema and the helper. The only file it touches is `.spark/state.json`, and only through the helper. The helper script lives at `scripts/update-state.py` and the full field-by-field reference is in `references/schema.md`.

## Done when
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read` prints a valid JSON object with all seven top-level fields present, and a merge patch followed by a read shows the patched field changed while every other field is untouched. That is the one observable test: patch one field, read it back, count that exactly one field moved.

## Log it
This skill does not log to `CHANGELOG.md` or write to state on its own behalf, because it has no artefact. The skills that call it do the logging: each one appends its own line to `CHANGELOG.md` via the logbook helper and records its progress here with a `--patch` and an `--append-artefact` call. This skill is the mechanism, not the author.

## If it goes wrong
If the helper reports on stderr that it moved a corrupt file to `state.json.broken`, the previous good copy is still in `state.json.bak`. Compare the two, decide which is right, and if you want the backup back, copy it over `state.json` and re-run your patch. If `python3` is missing the skill cannot run at all: install Python 3, since the whole plugin depends on it. If file locking is unavailable on the platform the helper still works, it just proceeds without the lock and warns quietly, so avoid running two writes at the exact same instant.
