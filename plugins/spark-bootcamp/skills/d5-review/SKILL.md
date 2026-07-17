---
name: Review The Week
description: Packages the whole week into one index, scores it honestly, and calls audit-pack. The last thing you run on Day 5, after the deal is closed.
when_to_use: Day 5 final step, after d5-close wrote 05-sale/WON-DEAL.md. Hands you a launch package, a scorecard, and a keep-it-running plan.
---

# Review The Week

**What this does.** Pulls the five core artefacts (MVP, pitch deck, sales deck, brochure or live page, launch checklist) plus the deal into one index, states every headline number, scores target versus achieved, and calls audit-pack.
**Why it matters.** By Friday your week is scattered across five folders; this gives a prospect, partner or regulator one honest link and writes down how to keep the MVP running after you leave.
**You are ready for this when.** `05-sale/WON-DEAL.md` exists and `.spark/state.json` records your headline target and each day's outcome.

## Before you start
This links what exists and invents nothing; missing numbers get marked ABSENT, not invented. Reads from the project root: `.spark/state.json` (via journey-state), the five core artefacts (`03-product/site/index.html` or `03-product/BUILD-LOG.md`, `02-market/pitch-deck.*`, `04-gtm/sales-deck.*`, `03-product/site/index.html`, `04-gtm/gtm-plan.md`), and the deal (`05-sale/WON-DEAL.md`, falling back to `05-sale/PROPOSAL.md` or `05-sale/outreach-log.md`). If a number is missing, go log it properly; do not type a flattering one.

## Steps
1. If `05-sale/WON-DEAL.md` does not exist, stop and run d5-close first.
2. Build the package and scorecard, from the project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_review.py --root .
   ```
   Last line reads `REVIEW_RESULT core_linked=<n>/5 deal=<present|absent> headline_numbers=<m>`.
3. If `core_linked` is below 5, build or move the missing artefact, then re-run.
4. Open `05-sale/LAUNCH-PACKAGE.md`. Check "Achieved" honestly answers "Target", every core row links a real file, and the live page row carries a working URL.
5. Fill the keep-it-running section: replace every `[TO COMPLETE: ...]` marker (Vercel owner, refund policy, delivery capacity). Background in `${CLAUDE_SKILL_DIR}/references/keep-it-running.md`.
6. Open `05-sale/SCORECARD.md` and ask the founder for the honest sentence at the foot: did you hit the headline number, and what is the single most important thing you learned? Their words, verbatim. No spin.
7. Call audit-pack:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/audit-pack/scripts/build_pack.py --root .
   ```

## The artefact
Two Markdown files under `05-sale/`: `LAUNCH-PACKAGE.md` (headline target versus achieved, table linking the five core artefacts and the deal, every headline number, and a keep-it-running section branched by business path) and `SCORECARD.md` (day-by-day target versus achieved with sign-off, and your one sentence). Also triggers `.spark/deliverables/audit-pack.md`. Good: a stranger sees in ten seconds what you set out to do and whether you did it, with no blank markers left.

## Done when
Script prints `core_linked=5/5` and `deal=present`, `LAUNCH-PACKAGE.md` states every headline number (target plus all five days), and `.spark/deliverables/audit-pack.md` exists. Concretely: `grep -c "TO COMPLETE" 05-sale/LAUNCH-PACKAGE.md` returns 0.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-review \
  --artefact 05-sale/LAUNCH-PACKAGE.md \
  --result "5/5 core artefacts linked, deal present"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"current_day": 5, "days": {"5": {"complete": true, "outcome": "week packaged and scored"}}}'
```

## If it goes wrong
If `core_linked` stays below 5 because an artefact lives at an unchecked path, move it to the expected path (see Before you start) or add its real path to the top of the matching candidate list in `${CLAUDE_SKILL_DIR}/scripts/build_review.py`, then re-run. If `state.json` is unreadable, the script still writes both files with "not recorded" and warns on stderr: recover state, then rebuild. If audit-pack cannot run, note the gap and compile it by hand from CHANGELOG.md and DECISIONS.md.
