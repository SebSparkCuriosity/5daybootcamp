---
name: Set Up GitHub
description: Creates a versioned home for the build: a GitHub repo, a five-line README, and one open issue per Must from your MoSCoW list. Use on Day 3, before you write code.
when_to_use: Day 3 product build, after d3-requirements (MoSCoW) and d3-tech-stack, before the first line of code ships.
---

# Set Up GitHub

**What this does.** Creates a live GitHub repository, adds a five-line README, and opens one issue per Must from your MoSCoW list, so every promise you made has a tracked home.
**Why it matters.** A repo is where the build lives and where the audit trail starts. Regulators, investors and future you all ask the same question: what did you decide, and when? GitHub answers it for free. Even if you are building hardware or a service, your docs, drawings and sample deliverables belong somewhere versioned, not in a folder called Final_v3_ACTUAL.
**You are ready for this when.** `03-product/requirements-moscow.md` and `03-product/tech-stack.md` both exist.

## Before you start
Read these three files:
- `03-product/requirements-moscow.md`, for the Must list. Each Must becomes one issue.
- `03-product/tech-stack.md`, for the one-line description of what you are building.
- `.spark/state.json`, for `founder`, `idea` and `business_type`.

Guardrail: creating a repo is free and spends no money, so no sign-off is needed. But do not make the repo public if your idea brief or interviews contain a client's confidential information. Default to private. You can flip it to public later in one click.

You need a GitHub account and the `gh` command-line tool authenticated. Most non-technical founders have neither yet. That is fine. The helper script walks you through it and checks every step. Run it first:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-github.py --check
```

If it reports "gh not authenticated", follow the walkthrough in `${CLAUDE_SKILL_DIR}/references/github-auth-walkthrough.md`. It takes about four minutes and you do it once.

## Steps
1. Run the check above. If `gh` is missing or not logged in, stop and do the walkthrough, then run the check again. Do not proceed until it prints "ready".
2. Pick a repo name. Keep it short, lower case, hyphenated: for example `harbour-fund-portal`. The script suggests one from your idea; accept it or type your own.
3. Draft the five-line README. It is not marketing. Five plain lines: what this is, who it is for, the one Must-have outcome, the stack (or "docs and assets" for non-software), and the status ("Day 3 build, in progress"). The script drafts it from your files; read it and fix anything wrong.
4. Confirm the Must list. The script reads `requirements-moscow.md` and pulls out every line under the Must heading. Check the count out loud: "I have N Musts, so I expect N issues." If the count looks wrong, fix the MoSCoW file first, this is your last clean chance.
5. Create the repo, push the README, and open one issue per Must. Run:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/setup-github.py --create
   ```
   The script prints the repo URL and every issue URL as it goes.
6. Open the repo URL in your browser. Confirm the README shows on the front page and the Issues tab holds one issue per Must. That is the whole job.

The paths differ only in what the README says and what the first issues track. The mechanics are identical.

## For software
The README's stack line names your real stack (default: Next.js, Supabase, Vercel). Issues are the Musts as buildable slices: "User can submit the intake form", not "Build the form". This repo will hold your actual code by end of Day 3.

## For hardware
The README's stack line reads "Docs, CAD and pre-order page". Issues track the prototype and the payment-intent page: "CAD render of v1 enclosure", "Waitlist page live and taking a deposit". The repo holds drawings, renders and the landing-page code, versioned so you can prove what changed.

## For services
The README's stack line reads "Sample deliverable and intake page". Issues track the productised package: "One sample deliverable written", "Bookable intake page live". The repo holds your sample work and the page, so a prospect's questions map to a tracked commit.

## The artefact
Two things:
- A live GitHub repository, private by default, reachable at a URL like `https://github.com/<you>/<repo>`, with a README on the front page and one open issue per Must.
- `03-product/github.md`, a short record: the repo URL, the issue count, and a line per issue with its number and title. This is what the audit pack reads later, so the repo's state survives even if GitHub is unreachable at review time.

What good looks like: click the repo URL, see a README a stranger understands in fifteen seconds, and an Issues tab where the open count equals your Must count.

## Done when
The repo URL returns 200 (reachable), the README is present on the front page, and the number of open issues equals the number of Musts in `requirements-moscow.md`. The script prints all three as a final PASS/FAIL line; you want PASS.

## Log it
Append to CHANGELOG.md via the logbook helper, with the numeric result (issue count):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-github-setup \
  --path 03-product/github.md \
  --result "repo live, <N> Must issues open"
```
Update state via the journey-state helper (records the artefact and Day 3 progress):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --add-artefact d3-github-setup 03-product/github.md "repo live, <N> issues" \
  --set-day-outcome 3 "GitHub repo live with <N> Must issues"
```

## If it goes wrong
If `gh` will not authenticate on the founder's machine (corporate laptop, locked-down network), fall back to the browser: create the repo at github.com/new, paste the README the script drafted (it saves a copy to `03-product/README.draft.md`), and open each Must as an issue by hand from the list the script prints. Slower, same result. Then write `03-product/github.md` yourself with the URL and issue list. If GitHub is blocked entirely on-island, use the same flow on a phone hotspot; the repo is portable.
