---
name: Review The Week
description: Packages the whole week into one index and scores it honestly, then calls audit-pack. The last thing you run on Day 5, after the deal is closed and logged.
when_to_use: Day 5, the final step, after d5-close has written 05-sale/WON-DEAL.md. Use it to hand yourself a launch package, an honest scorecard, and a keep-it-running plan for the MVP.
---

# Review The Week

**What this does.** Pulls the five core artefacts you built (MVP, pitch deck, sales deck, brochure or live page, launch checklist) plus the deal into one index, states every headline number, writes an honest scorecard of target versus achieved, and calls audit-pack.
**Why it matters.** By Friday afternoon your week is scattered across five folders and your own head. A prospect, a partner or a regulator wants one link, not a tour. This gives you that link, tells you honestly whether you hit your number, and, crucially, writes down how to keep the Claude-built MVP running once you walk away from the bootcamp. A working product nobody can log into is not an asset.
**You are ready for this when.** Day 5 is otherwise done: `05-sale/WON-DEAL.md` exists (from d5-close), and `.spark/state.json` records your headline target and each day's outcome.

## Before you start
This skill reads a lot and invents nothing. It links what exists and marks the rest ABSENT. It reads, from the founder's project root:
- `.spark/state.json` (via the journey-state helper): the headline target and every day's target and outcome.
- The five core artefacts, wherever they landed: `03-product/site/index.html` or `03-product/BUILD-LOG.md` (the MVP), `02-market/pitch-deck.*`, `04-gtm/sales-deck.*`, `03-product/site/index.html` (the live page), `04-gtm/gtm-plan.md` (the launch checklist).
- The deal: `05-sale/WON-DEAL.md`, falling back to `05-sale/PROPOSAL.md` or `05-sale/outreach-log.md`.

Guardrail: this is a review, not a rewrite. If a number is missing, the fix is to go back and log it properly, not to type a flattering one into the package. The whole value of the pack is that it matches reality.

## Steps
1. Confirm the deal is closed and logged. If `05-sale/WON-DEAL.md` does not exist, stop and run d5-close first. Reviewing a week with no logged ask is reviewing half a week.
2. Build the package and scorecard in one command, run from the founder's project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_review.py --root .
   ```
   It resolves each of the five core slots to the first file that exists, pulls the live URL out of `BUILD-LOG.md` or the accessibility report where there is one, and writes both artefacts. Its last line reads `REVIEW_RESULT core_linked=<n>/5 deal=<present|absent> headline_numbers=<m>`.
3. Read that result line. If `core_linked` is below 5, one of the core artefacts never got built or landed somewhere the script does not look. Go build or move it, then re-run. Do not hand over a package with holes in it and hope nobody notices.
4. Open `05-sale/LAUNCH-PACKAGE.md`. Check the headline: does "Achieved" honestly answer "Target"? Check every core row links to a real file, and that the live page row carries a working URL.
5. Fill the keep-it-running section. This is the part founders skip and regret. Every `[TO COMPLETE: ...]` marker is a fact only you know: which account owns Vercel, your refund policy, how many clients a week you can actually deliver. The background on all four parts is in `${CLAUDE_SKILL_DIR}/references/keep-it-running.md`. Replace every marker. A blank marker is a problem you are posting to your future self.
6. Open `05-sale/SCORECARD.md` and write the one honest sentence at the foot: did you hit the headline number, and what is the single most important thing you learned? One sentence. No spin.
7. Call audit-pack to compile the full evidence trail:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/audit-pack/scripts/build_pack.py --root .
   ```
   That writes `.spark/deliverables/audit-pack.md`, the dated and numbered proof behind every claim in your package.

## The artefact
Writes two files under `05-sale/`, both Markdown:
- `05-sale/LAUNCH-PACKAGE.md`: the index. A headline (target versus achieved), a table linking the five core artefacts, the deal, every headline number in one block, and a keep-it-running section (account ownership, how to redeploy, known limits, and your honest support commitment), branched to your business path.
- `05-sale/SCORECARD.md`: a day-by-day table of target versus achieved with a sign-off column, and your one honest sentence.

It also triggers `.spark/deliverables/audit-pack.md` via the audit-pack skill.

Good looks like: a stranger opens LAUNCH-PACKAGE.md, sees in ten seconds what you set out to do and whether you did it, clicks straight through to the live page and every deck, and finds a keep-it-running section with no blank markers left.

## Done when
The script prints `core_linked=5/5` (all five core artefacts linked) and `deal=present`, `LAUNCH-PACKAGE.md` states every headline number (the headline target plus all five days), the keep-it-running section has zero `[TO COMPLETE: ...]` markers remaining, and `.spark/deliverables/audit-pack.md` exists. Concretely: `grep -c "TO COMPLETE" 05-sale/LAUNCH-PACKAGE.md` returns 0.

## Log it
Log both artefacts to CHANGELOG.md (the logbook helper also registers each one in `state.json`), then mark Day 5 complete:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-review \
  --artefact 05-sale/LAUNCH-PACKAGE.md \
  --result "5/5 core artefacts linked, deal present"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-review \
  --artefact 05-sale/SCORECARD.md \
  --result "<M> headline numbers scored"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"current_day": 5, "days": {"5": {"complete": true, "outcome": "week packaged and scored"}}}'
```
Replace `<M>` with the `headline_numbers` count the script printed. Then log the closing decision:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Closed the bootcamp week" \
  --rationale "Launch package and scorecard assembled; audit pack compiled as evidence"
```

## If it goes wrong
If `core_linked` stays below 5 because an artefact lives at a path the script does not check, either move it to the expected path (see Before you start) or add its real path to the top of the matching candidate list in `${CLAUDE_SKILL_DIR}/scripts/build_review.py`, then re-run. If `state.json` is missing or unreadable, the script still writes both files with "not recorded" in the number cells and tells you on stderr: recover the state file, or re-run the day skills, then rebuild. If audit-pack cannot run, the package still stands on its own; note the gap and compile the audit pack by hand from CHANGELOG.md and DECISIONS.md.
