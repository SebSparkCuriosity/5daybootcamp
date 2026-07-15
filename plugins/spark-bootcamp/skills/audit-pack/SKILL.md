---
name: Audit Pack
description: Compiles the week's changelog, decisions and logged artefacts into one regulator-ready pack, opening with target versus achieved.
when_to_use: Day 5 review (called by d5-review), or when a regulator, investor or client asks to see what you built.
---

# Audit Pack

**What this does.** Compiles CHANGELOG.md, DECISIONS.md and every logged artefact into one clean pack, opening with your headline target versus what you achieved.
**Why it matters.** In regulated Jersey sectors "trust me" is not evidence, so this pack becomes the evidence you hand a regulator, investor or buyer without editing.
**You are ready for this when.** `.spark/state.json` exists and at least one artefact has been logged.

## Before you start
Reads three files from the founder's project root: `.spark/state.json` (via journey-state), `CHANGELOG.md`, `DECISIONS.md`. Reports what was recorded; never invents results. Missing numbers show a dash, not a guess. Do not edit logs to flatter the pack.

## Steps
1. Confirm the three inputs exist. A missing CHANGELOG.md usually means no skill has logged yet, so run the day skills first.
2. Run the compiler:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_pack.py --root .
   ```
   Run from the project root, or pass `--root /path/to/project`.
3. Open `.spark/deliverables/audit-pack.md` and read the headline. If "Achieved" does not carry the target's number, the logging is thin. Fix the logs, not the pack.
4. Scan the artefact table. A dash in the Number column means an artefact was logged without its numeric result. Re-log that line, then rebuild.
5. Read the decision log. Each decision needs a rationale a stranger could follow. Add any missing why to DECISIONS.md and rebuild.
6. Same for software, hardware and services: the paths differ in what they build, not how they prove it, so no path branch here.

## The artefact
Writes `.spark/deliverables/audit-pack.md` in Markdown, four sections in order: Headline outcome (target versus achieved), Artefacts (dated, numbered table), Change log (raw CHANGELOG.md), Decision log (raw DECISIONS.md). Ends with the standard draft-and-review notice. A stranger should grasp what you set out to do and whether you did it within ten seconds, then trace every claim below.

## Done when
The pack opens with target and achieved both present, and every logged artefact appears with a date and a number: the script's "Artefacts in pack" count equals `state.json.artefacts` entries, with no dash where a number should be.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill audit-pack \
  --artefact .spark/deliverables/audit-pack.md \
  --result "<N> artefacts compiled"
```
Replace `<N>` with the artefact count the script printed.

## If it goes wrong
If `state.json` is missing, the script still writes a pack from the changelog and decisions and flags the gap. Recover the state file and rebuild. If the artefact table is empty but work was done, those skills logged to CHANGELOG.md but not to state.json: re-run each skill's Log it step (the `log.py` call registers the artefact in state), then rebuild.
