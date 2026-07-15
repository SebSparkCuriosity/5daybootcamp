#!/usr/bin/env bash
# commit-fixes.sh: commit today's shipped fixes with a timestamp, and print the
# short commit hash so the founder can record it in the changelog.
#
# It is deliberately dull. It stages everything, commits with a message you pass
# (or a sensible default), and stamps the commit so the audit trail shows exactly
# when Friday's fixes landed. It never forces, never rebases, never touches a
# remote. If this is not a git repo, or there is nothing to commit, it says so in
# plain English and exits 0, so the skill can carry on and log the day by hand.
#
# Usage:
#   commit-fixes.sh                       # default message
#   commit-fixes.sh "closes top 3 triage fixes"   # your own message
#
# Exit codes: 0 always for the expected cases (committed, nothing to commit, not
# a repo). Only an unexpected git failure returns non-zero.

set -u

msg="${1:-}"
stamp="$(date '+%Y-%m-%d %H:%M')"

# Are we in a git repo?
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "COMMIT_RESULT=SKIPPED not a git repository."
  echo "No commit made. If your MVP is a repo, run this from inside it."
  echo "If your MVP is not code (a services package, a hardware mock), record the"
  echo "artefact time in CHANGELOG.md instead: your timestamp is the audit trail."
  exit 0
fi

# Anything to commit?
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "COMMIT_RESULT=NOCHANGES nothing to commit."
  echo "The working tree is clean. Either the fixes are already committed, or"
  echo "nothing changed. Check 'git log -1' to confirm the last commit is today's."
  exit 0
fi

if [ -z "$msg" ]; then
  msg="Day 5: ship top 3 triage fixes, demo happy path verified"
fi
full_msg="${msg} [${stamp}]"

git add -A || { echo "COMMIT_RESULT=ERROR git add failed."; exit 1; }

if git commit -m "$full_msg" >/dev/null 2>&1; then
  short="$(git rev-parse --short HEAD 2>/dev/null || echo '?')"
  echo "COMMIT_RESULT=OK committed ${short} at ${stamp}"
  echo "Message: ${full_msg}"
  echo "Record the hash ${short} and the time ${stamp} in your changelog result."
else
  # Most likely git identity is unset. Tell the founder exactly how to fix it.
  echo "COMMIT_RESULT=ERROR git commit failed."
  echo "The usual cause is an unset identity. Set it once, then re-run:"
  echo "  git config user.name  \"Your Name\""
  echo "  git config user.email \"you@example.com\""
  exit 1
fi
