---
name: Audit Pack
description: Compiles the week's changelog, decisions and logged artefacts into one regulator-ready pack that opens with your target versus what you achieved. Use on Day 5 or any time you need proof.
when_to_use: Day 5 review (called by d5-review), or any time a regulator, investor or client asks "show me what you built and how".
---

# Audit Pack

**What this does.** Compiles CHANGELOG.md, DECISIONS.md and every artefact logged in state.json into one clean pack, opening with your headline target versus what you actually achieved.
**Why it matters.** In regulated Jersey sectors, "trust me" is not evidence. This pack is the evidence: every artefact with a date and a number, every decision with a reason, in one file you can hand to a regulator, an investor or a buyer without editing. Auditable by default is the whole point of the week.
**You are ready for this when.** `.spark/state.json` exists and at least one artefact has been logged. You can run it half-way through the week to see progress, but it shines on Day 5.

## Before you start
Reads three files from the founder's project root:
- `.spark/state.json` (via the journey-state helper for the headline and artefact list)
- `CHANGELOG.md` (the append-only log)
- `DECISIONS.md` (the decision log)

This pack reports what was recorded. It does not invent results. If a number is missing from a log line, it shows a dash, not a guess. Do not edit the logs to make the pack look better: the value is that it matches reality.

## Steps
1. Confirm the three inputs exist. Missing files are fine, the pack will note them, but a missing CHANGELOG.md usually means no skill has logged yet, so run the day skills first.
2. Run the compiler:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_pack.py --root .
   ```
   Run it from the founder's project root, or pass `--root /path/to/project`.
3. Open `.spark/deliverables/audit-pack.md` and read the headline first. Does "Achieved" honestly answer "Target"? If the target was a number (for example "10 booked calls") and the achieved line does not carry that number, the week's logging is thin. Fix the logs, do not fix the pack.
4. Scan the artefact table. Every row needs a date and a number. A dash in the Number column means a skill logged an artefact without its numeric result. Go back and re-log that line properly, then rebuild.
5. Read the decision log at the foot. Each decision should carry a rationale a stranger could follow. If one reads as "we just did it", add the why to DECISIONS.md and rebuild.
6. This pack is the same for software, hardware and services founders. The three paths differ in what they build, not in how they prove it, so there is no path branch here.

## The artefact
Writes `.spark/deliverables/audit-pack.md` in Markdown, with four sections in this order: Headline outcome (target versus achieved), Artefacts (a dated, numbered table), Change log (the raw CHANGELOG.md), Decision log (the raw DECISIONS.md). It ends with the standard draft-and-review notice.

What good looks like: a reader who has never met you understands, in the first ten seconds, what you set out to do and whether you did it, then can trace every claim to a dated, numbered artefact below.

## Done when
The pack opens with the headline outcome (target and achieved both present) and every logged artefact appears in the table with a date and a number. Concretely: the script's "Artefacts in pack" count equals the number of entries in `state.json.artefacts`, and no row in the table shows a dash where a number should be.

## Log it
Append one line to CHANGELOG.md and record the artefact in state.json:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill audit-pack \
  --path .spark/deliverables/audit-pack.md \
  --result "<N> artefacts compiled"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  add-artefact --skill audit-pack \
  --path .spark/deliverables/audit-pack.md \
  --result "<N> artefacts compiled"
```
Replace `<N>` with the artefact count the script printed.

## If it goes wrong
If `state.json` is missing or unreadable, the script still writes a pack with the changelog and decisions and flags the gap in the headline. Recover the state file (or re-run the day skills) and rebuild.

If the artefact table is empty but you know work was done, the day skills logged to CHANGELOG.md but never called the state helper's `add-artefact`. The changelog section will still show the work; re-run the missing `add-artefact` calls to populate the table, then rebuild.
