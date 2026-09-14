#!/usr/bin/env python3
"""Fail when the plugin changed but its version did not.

Claude Code caches a marketplace install in a directory keyed on the version
string, so `claude plugin update` on an unchanged version reports "already at
the latest version" and pulls nothing. A release that edits a skill without
bumping the version never reaches a founder who already installed. This check
makes that impossible to ship.

    python3 tools/check_version_bump.py [base-ref]

Default base ref is origin/main. Exit 0 when clean or when there is nothing to
compare against (a shallow clone, or main itself). Exit 1 when the plugin
changed and the version did not.
"""

import json
import subprocess
import sys

PLUGIN_DIR = "plugins/spark-bootcamp"
PLUGIN_JSON = f"{PLUGIN_DIR}/.claude-plugin/plugin.json"


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False)


def version_at(ref):
    out = git("show", f"{ref}:{PLUGIN_JSON}")
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout).get("version")
    except ValueError:
        return None


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"

    if git("rev-parse", "--verify", base).returncode != 0:
        print(f"SKIP  base ref {base} is not available, nothing to compare")
        return 0

    merge_base = git("merge-base", base, "HEAD").stdout.strip()
    if not merge_base:
        print(f"SKIP  no merge base with {base}")
        return 0
    if merge_base == git("rev-parse", "HEAD").stdout.strip():
        print(f"SKIP  HEAD is an ancestor of {base}, no new commits to check")
        return 0

    changed = git("diff", "--name-only", merge_base, "HEAD", "--", PLUGIN_DIR)
    files = [f for f in changed.stdout.splitlines() if f.strip()]
    if not files:
        print("PASS  no plugin files changed, no bump needed")
        return 0

    old = version_at(merge_base)
    new = version_at("HEAD")
    if new is None:
        print("FAIL  cannot read the version from plugin.json at HEAD")
        return 1
    if old is not None and old == new:
        print(f"FAIL  {len(files)} plugin file(s) changed but the version is "
              f"still {new}. Founders who already installed will never receive "
              f"this. Bump the version in {PLUGIN_JSON} and in the marketplace "
              f"entry.")
        for f in files[:10]:
            print(f"        {f}")
        if len(files) > 10:
            print(f"        ... and {len(files) - 10} more")
        return 1

    print(f"PASS  {len(files)} plugin file(s) changed, version {old} -> {new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
