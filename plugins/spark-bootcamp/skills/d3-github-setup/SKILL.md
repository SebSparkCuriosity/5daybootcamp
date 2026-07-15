---
name: Set Up GitHub
description: Creates a GitHub repo, a five-line README, and one open issue per Must from your MoSCoW list. Use on Day 3, before you write code.
when_to_use: Day 3, after d3-moscow and d3-tech-stack, before the first line of code.
---

# Set Up GitHub

**What this does.** Creates a live GitHub repo, adds a five-line README, and opens one issue per Must from your MoSCoW list.
**Why it matters.** A repo is where the build lives and where your audit trail starts, so every promise you made has a tracked home instead of a folder called Final_v3_ACTUAL.
**You are ready for this when.** `03-product/requirements-moscow.md` and `03-product/docs/tech-stack.md` both exist.

## Before you start
Read `03-product/requirements-moscow.md` (the Must list, one issue each), `03-product/docs/tech-stack.md` (the one-line description) and `.spark/state.json` (`founder`, `idea`, `business_type`).

Guardrail: repos are free, no sign-off needed. Default to private if any brief or interview holds confidential client information; flip to public later in one click.

You need `gh` authenticated. If you have neither account nor CLI, that is fine: the helper checks and walks you through it. Run first:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-github.py --check
```
If it says "gh not authenticated", follow `${CLAUDE_SKILL_DIR}/references/github-auth-walkthrough.md` (about four minutes, once).

## Steps
1. Run the check. If `gh` is missing or logged out, do the walkthrough, then re-run. Do not proceed until it prints "ready".
2. Pick a repo name: short, lower case, hyphenated (`harbour-fund-portal`). Accept the script's suggestion or type your own.
3. Draft the five-line README: what this is, who it is for, the one Must-have outcome, the stack (or "docs and assets"), the status. The script drafts it; read it and fix anything wrong.
4. Confirm the Must count. Say it out loud: "N Musts, so N issues." If it looks wrong, fix the MoSCoW file first, this is your last clean chance.
5. Create the repo, push the README, open one issue per Must:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/setup-github.py --create
   ```
6. Open the repo URL. Confirm the README shows on the front page and the Issues tab holds one issue per Must.

The mechanics are identical across paths; only the README and first issues differ.

## For software
Stack line names your real stack (default: Next.js, Supabase, Vercel). Issues are Musts as buildable slices: "User can submit the intake form", not "Build the form".

## For hardware
Stack line reads "Docs, CAD and pre-order page". Issues track the prototype and payment-intent page: "CAD render of v1 enclosure", "Waitlist page live and taking a deposit".

## For services
Stack line reads "Sample deliverable and intake page". Issues track the productised package: "One sample deliverable written", "Bookable intake page live".

## The artefact
A live GitHub repo (private by default) at `https://github.com/<you>/<repo>`, with a README on the front page and one open issue per Must. Plus `03-product/github.md`: the repo URL, issue count, and a line per issue (number and title), so the audit pack survives even if GitHub is unreachable.

## Done when
The repo URL returns 200, the README is on the front page, and open issues equal the Musts in `requirements-moscow.md`. The script prints a final PASS/FAIL; you want PASS.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-github-setup \
  --artefact 03-product/github.md \
  --result "repo live, <N> Must issues open"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"outcome":"GitHub repo live with <N> Must issues"}}}'
```

## If it goes wrong
If `gh` will not authenticate (locked-down laptop or network), fall back to the browser: create the repo at github.com/new, paste the README the script saved to `03-product/README.draft.md`, open each Must by hand from the printed list, then write `03-product/github.md` yourself. If GitHub is blocked on-island, use a phone hotspot; the repo is portable.
