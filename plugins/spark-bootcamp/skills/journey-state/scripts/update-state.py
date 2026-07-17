#!/usr/bin/env python3
"""Safe read-merge-write helper for .spark/state.json.

This is the ONLY sanctioned way to touch the journey state file. It reads
the current state (creating it with the default schema if it is missing or
unreadable), applies a JSON merge patch (RFC 7386), and writes the result
back atomically, keeping a .bak backup. It never crashes on a missing or
half-written file: it falls back to the default schema and reports what it did.

Usage:
  # Merge a patch given on the command line
  update-state.py --patch '{"current_day": 2, "days": {"1": {"complete": true}}}'

  # Merge a patch piped on stdin
  echo '{"business_type": "services"}' | update-state.py --patch -

  # Append one artefact record (safe append, does not replace the array)
  update-state.py --append-artefact '{"skill":"p0-interview-triage",
      "path":"00-prework/interview-target-spec.md",
      "result":"10 interviews targeted"}'

  # Just read and print the current state (no write)
  update-state.py --read

Merge patch rules (RFC 7386): objects merge key by key, a null value deletes
that key, and any scalar or array value replaces what was there. To ADD an
artefact without replacing the whole list, use --append-artefact, not --patch.
"""

import argparse
import datetime
import json
import os
import sys
import tempfile

# Optional file locking. Absent on some platforms; we degrade gracefully.
try:
    import fcntl  # type: ignore
    HAVE_FCNTL = True
except Exception:
    HAVE_FCNTL = False


def default_state():
    """The canonical starting schema. Kept in one place on purpose."""
    day = lambda: {"target": "", "outcome": "", "complete": False}
    return {
        "founder": "",
        "business_type": "",          # "software" | "hardware" | "services"
        "idea": "",
        "headline_target": "",
        "prework": {
            "bootcamp_monday": "",    # ISO date of the bootcamp's Monday
            "interviews_booked": 0,
            "complete": False,        # set by p0-schedule at 8+ booked
        },
        "current_day": 1,
        "days": {
            "1": day(),
            "2": day(),
            "3": day(),
            "4": day(),
            "5": day(),
        },
        "artefacts": [],              # [{skill, path, result, at}]
    }


def find_state_path(explicit):
    """Locate .spark/state.json. Prefer an explicit --file. Otherwise walk up
    from the current directory looking for an existing .spark folder, and fall
    back to ./.spark/state.json in the current directory."""
    if explicit:
        return os.path.abspath(explicit)
    here = os.getcwd()
    cur = here
    while True:
        candidate = os.path.join(cur, ".spark")
        if os.path.isdir(candidate):
            return os.path.join(candidate, "state.json")
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.join(here, ".spark", "state.json")


def read_state(path):
    """Read state, returning (state, note). Never raises on bad input: a
    missing or corrupt file yields the default schema and a note saying so."""
    if not os.path.exists(path):
        return default_state(), "created new state from default schema"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("state root is not an object")
        return data, ""
    except Exception as exc:
        # File is present but unreadable or half-written. Do not lose it:
        # keep a copy of whatever was there before we overwrite.
        try:
            broken = path + ".broken"
            os.replace(path, broken)
            note = "existing state was unreadable (%s); moved it to %s and reset to default" % (
                exc, os.path.basename(broken))
        except Exception:
            note = "existing state was unreadable (%s); reset to default" % exc
        return default_state(), note


def merge_patch(target, patch):
    """Apply an RFC 7386 JSON merge patch and return the result."""
    if not isinstance(patch, dict):
        return patch
    if not isinstance(target, dict):
        target = {}
    for key, value in patch.items():
        if value is None:
            target.pop(key, None)
        elif isinstance(value, dict):
            target[key] = merge_patch(target.get(key), value)
        else:
            target[key] = value
    return target


def now_iso():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def atomic_write(path, state):
    """Back up the current file, then write atomically via a temp file and
    os.replace so a reader never sees a half-written state."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as src:
                content = src.read()
            with open(path + ".bak", "w", encoding="utf-8") as dst:
                dst.write(content)
        except Exception:
            pass  # A missing backup must never block a good write.
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def parse_json_arg(value, label):
    """Read JSON from a string, or from stdin when the value is '-'."""
    if value == "-":
        value = sys.stdin.read()
    try:
        return json.loads(value)
    except Exception as exc:
        sys.stderr.write("Could not parse %s as JSON: %s\n" % (label, exc))
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="Safe read-merge-write for .spark/state.json")
    ap.add_argument("--patch", help="JSON merge patch, or '-' to read from stdin")
    ap.add_argument("--append-artefact", help="JSON object appended to artefacts[] (skill, path, result); 'at' is added automatically")
    ap.add_argument("--file", help="Path to state.json (default: nearest .spark/state.json)")
    ap.add_argument("--read", action="store_true", help="Read and print current state, no write")
    args = ap.parse_args()

    path = find_state_path(args.file)

    # A best-effort exclusive lock around the whole read-merge-write so two
    # skills running at once cannot interleave. Degrades to no lock quietly.
    lock_handle = None
    if HAVE_FCNTL and not args.read:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            lock_handle = open(path + ".lock", "w")
            fcntl.flock(lock_handle, fcntl.LOCK_EX)
        except Exception:
            lock_handle = None

    try:
        state, note = read_state(path)

        if args.read:
            print(json.dumps(state, indent=2, ensure_ascii=False))
            return

        changed = False

        if args.patch:
            patch = parse_json_arg(args.patch, "--patch")
            state = merge_patch(state, patch)
            changed = True

        if args.append_artefact:
            artefact = parse_json_arg(args.append_artefact, "--append-artefact")
            if not isinstance(artefact, dict):
                sys.stderr.write("--append-artefact must be a JSON object\n")
                sys.exit(2)
            artefact.setdefault("at", now_iso())
            if not isinstance(state.get("artefacts"), list):
                state["artefacts"] = []
            state["artefacts"].append(artefact)
            changed = True

        if not changed:
            # No patch and no artefact: still ensure the file exists on disk
            # with the default schema, so later skills can rely on it.
            atomic_write(path, state)
            if note:
                sys.stderr.write(note + "\n")
            print(json.dumps(state, indent=2, ensure_ascii=False))
            return

        atomic_write(path, state)
        if note:
            sys.stderr.write(note + "\n")
        print(json.dumps(state, indent=2, ensure_ascii=False))
    finally:
        if lock_handle is not None:
            try:
                fcntl.flock(lock_handle, fcntl.LOCK_UN)
                lock_handle.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
