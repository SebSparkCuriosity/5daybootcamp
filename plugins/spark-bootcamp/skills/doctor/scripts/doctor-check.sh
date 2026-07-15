#!/usr/bin/env bash
# doctor-check.sh
# Verifies the founder's machine, lays out the .spark project skeleton, and
# writes .spark/doctor-report.txt. It VERIFIES, it does not install anything.
# It never crashes: a missing tool is reported with a fix, not a stack trace.
#
# Usage: doctor-check.sh [PROJECT_ROOT] [PREWORK_SOURCE]
#   PROJECT_ROOT    where to lay out the founder's project (default: current directory)
#   PREWORK_SOURCE  path to the skill's references/prework.md to copy in (optional)
#
# Exit code is always 0. Read the report for pass/fail; a founder should never
# see this script "fail" and panic.

set -u

PROJECT_ROOT="${1:-$(pwd)}"
PREWORK_SOURCE="${2:-}"
REPORT="${PROJECT_ROOT}/.spark/doctor-report.txt"

PASS_COUNT=0
FAIL_COUNT=0

# Buffer the report body so we can write it in one go.
BODY=""
line() { BODY="${BODY}$1"$'\n'; }

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  line "  [PASS] $1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  line "  [FAIL] $1"
  line "         Fix: $2"
}

warn() {
  line "  [WARN] $1"
  line "         Note: $2"
}

have() { command -v "$1" >/dev/null 2>&1; }

# --- Header ---------------------------------------------------------------
line "Spark Bootcamp: doctor report"
line "Generated: $(date '+%Y-%m-%d %H:%M')"
line "Project:   ${PROJECT_ROOT}"
line ""
line "Machine checks"
line "--------------"

# --- git ------------------------------------------------------------------
if have git; then
  GIT_V="$(git --version 2>/dev/null | head -n1)"
  pass "git installed (${GIT_V})"
else
  fail "git not found" "Install git. Mac: 'brew install git'. Windows: git-scm.com. Linux: 'sudo apt install git'."
fi

# --- Node (need 20 or newer for the software build path) ------------------
if have node; then
  NODE_RAW="$(node --version 2>/dev/null)"          # e.g. v20.11.1
  NODE_MAJOR="$(printf '%s' "${NODE_RAW}" | sed 's/^v//; s/\..*//')"
  if [ -n "${NODE_MAJOR}" ] && [ "${NODE_MAJOR}" -ge 20 ] 2>/dev/null; then
    pass "Node ${NODE_RAW} (20+ needed for the build day)"
  else
    warn "Node ${NODE_RAW} is older than 20" "The software build day expects Node 20+. Install the current LTS from nodejs.org. Hardware and services paths do not need it."
  fi
else
  warn "Node not found" "Only the software build path needs Node 20+. If you are building hardware or a service you can skip this. Otherwise install the LTS from nodejs.org."
fi

# --- A code editor (VS Code is the default we recommend) ------------------
if have code; then
  pass "VS Code CLI ('code') on PATH"
elif have cursor; then
  pass "Cursor CLI ('cursor') on PATH"
else
  warn "No editor CLI detected on PATH" "You do not strictly need one, but VS Code makes the week easier. Install it from code.visualstudio.com, then run 'Shell Command: Install code command in PATH'."
fi

# --- GitHub CLI or auth ---------------------------------------------------
if have gh; then
  if gh auth status >/dev/null 2>&1; then
    pass "GitHub CLI installed and authenticated"
  else
    fail "GitHub CLI installed but not logged in" "Run 'gh auth login' and follow the prompts. This lets the build day push your code to GitHub."
  fi
else
  warn "GitHub CLI ('gh') not found" "Recommended for the software build path so your code lands on GitHub. Install from cli.github.com, then run 'gh auth login'. Hardware and services paths can skip it."
fi

# --- Claude Code presence (informational) ---------------------------------
if have claude; then
  pass "Claude Code CLI on PATH"
else
  warn "Claude Code CLI not detected on PATH" "You are clearly running inside Claude Code, so this is only cosmetic. Digital Jersey's setup session covers the install. doctor does not install it."
fi

# --- Project scaffold -----------------------------------------------------
line ""
line "Project layout"
line "--------------"

mk_dir() {
  if [ -d "$1" ]; then
    line "  [KEPT]    $1 (already there)"
  else
    if mkdir -p "$1" 2>/dev/null; then
      line "  [CREATED] $1"
    else
      line "  [FAIL]    could not create $1 (check folder permissions)"
      FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
  fi
}

touch_file() {
  if [ -f "$1" ]; then
    line "  [KEPT]    $1 (already there, left untouched)"
  else
    if printf '%s' "$2" > "$1" 2>/dev/null; then
      line "  [CREATED] $1"
    else
      line "  [FAIL]    could not create $1 (check folder permissions)"
      FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
  fi
}

mk_dir "${PROJECT_ROOT}/.spark"
mk_dir "${PROJECT_ROOT}/.spark/brand"
mk_dir "${PROJECT_ROOT}/.spark/deliverables"
mk_dir "${PROJECT_ROOT}/01-discovery"
mk_dir "${PROJECT_ROOT}/02-market"
mk_dir "${PROJECT_ROOT}/03-product"
mk_dir "${PROJECT_ROOT}/04-gtm"
mk_dir "${PROJECT_ROOT}/05-sale"

# CHANGELOG.md and DECISIONS.md: created empty-with-header, never clobbered.
touch_file "${PROJECT_ROOT}/CHANGELOG.md" "# Changelog

Every artefact the bootcamp produces gets one line here: date, skill, path, result.
Append-only. Do not rewrite history.
"
touch_file "${PROJECT_ROOT}/DECISIONS.md" "# Decisions

Every call worth remembering, with the reason behind it. Newest at the bottom.
"

# Note: .spark/state.json is intentionally NOT created here.
# 'start' creates it once the founder names the business and picks a path.
line "  [SKIP]    ${PROJECT_ROOT}/.spark/state.json (created by /spark-bootcamp:start)"

# --- Pre-work checklist copy ----------------------------------------------
line ""
line "Pre-work checklist"
line "------------------"
PREWORK_DEST="${PROJECT_ROOT}/.spark/prework.md"
if [ -n "${PREWORK_SOURCE}" ] && [ -f "${PREWORK_SOURCE}" ]; then
  if [ -f "${PREWORK_DEST}" ]; then
    line "  [KEPT]    ${PREWORK_DEST} (already there, your ticks are safe)"
  elif cp "${PREWORK_SOURCE}" "${PREWORK_DEST}" 2>/dev/null; then
    line "  [CREATED] ${PREWORK_DEST} (tick this off before Monday)"
  else
    line "  [FAIL]    could not copy pre-work checklist to ${PREWORK_DEST}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
else
  line "  [WARN]    pre-work source not supplied; write ${PREWORK_DEST} by hand from the skill's references/prework.md"
fi

# --- Summary --------------------------------------------------------------
line ""
line "Summary"
line "-------"
line "  Passed: ${PASS_COUNT}    Needs a fix: ${FAIL_COUNT}"
if [ "${FAIL_COUNT}" -eq 0 ]; then
  line "  Machine is ready. Do the pre-work in .spark/prework.md, then run /spark-bootcamp:start."
else
  line "  Fix the [FAIL] items above, then run doctor again."
fi

# --- Write the report (create .spark first in case scaffold failed) -------
mkdir -p "${PROJECT_ROOT}/.spark" 2>/dev/null
if printf '%s' "${BODY}" > "${REPORT}" 2>/dev/null; then
  :
else
  # Last-resort fallback: at least print it.
  echo "Could not write ${REPORT}. Printing report to screen instead:"
fi

# Always echo the report so Claude and the founder can read it inline.
printf '%s' "${BODY}"

# Machine-readable tail line for the skill to branch on.
if [ "${FAIL_COUNT}" -eq 0 ]; then
  echo "DOCTOR_RESULT=READY passed=${PASS_COUNT} fails=0"
else
  echo "DOCTOR_RESULT=NEEDS_FIX passed=${PASS_COUNT} fails=${FAIL_COUNT}"
fi

exit 0
