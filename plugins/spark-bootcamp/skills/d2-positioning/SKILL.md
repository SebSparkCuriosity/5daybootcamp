---
name: Fix Your Positioning
description: Fix the corner of the market you own with a Moore statement, a 2x2 map and one USP no rival can claim. Day 2, after the competitor scan.
when_to_use: "Day 2, after d2-competitor-scan. Triggers: how do I position this, what's my USP, where do I win, positioning map."
---

# Fix Your Positioning

**What this does.** Fixes the corner of the market you own: a Geoffrey Moore positioning statement, a 2x2 map with rivals plotted, and one USP under 20 words no rival can honestly claim.
**Why it matters.** Positioning is the one decision that makes every later decision easier: it tells Day 3 what to build, Day 4 what to say, and Day 5 why a prospect pays you and not the incumbent.
**You are ready for this when.** `02-market/competitors.md` and `01-discovery/target-segment.md` both exist.

## Before you start
Read the gap sentence and matrix dimensions in `02-market/competitors.md`, and the buyer in `01-discovery/target-segment.md`. Open `references/moore-and-usp.md` for the Moore template, axis choices and three-part USP test. Guardrail: every claim must be true and provable this week. If you cannot back it, weaken it.

## Steps
1. Write the Moore statement using the exact format in `references/moore-and-usp.md`. Fill every bracket. The category must be one your buyer recognises in one second.
2. Pick two axes from the `competitors.md` dimensions: the two where buyers disagree most. Do not pick two that measure the same thing.
3. Plot at least six players (direct rivals, adjacent tools, the status quo), each with x and y from 0.0 to 1.0. Mark yourself in a corner no rival occupies. On top of a rival means your axes are wrong: fix before continuing.
4. Write the USP: one sentence, under 20 words, passing all three tests in the reference. Cut until only you can say it.
5. Sanity-check against Day 3: can you deliver what the USP promises in the page you ship this week? If not, pick a provable claim and record the swap in `DECISIONS.md`.

Branch only where the axes and deliverable differ.

## For software
Axes usually feature-facing (breadth, depth, integration) crossed with buyer-facing (price, local fit, auditability). The USP points at the Day 3 working slice, and any feature it names must be in that slice.

## For hardware
Axes usually physical (unit price, build quality, lead time) crossed with fit for the buyer's setting. The USP must be something the Day 3 prototype or CAD render visibly proves. Do not claim an unprototyped spec.

## For services
Axes usually price model (fixed vs hourly) and specialism, or turnaround against depth. The USP must be provable in the Day 3 sample deliverable. A clearly named offer beats a vague rival on clarity, so make clarity part of the position.

## The artefact
Writes two files in `02-market/`. Both read from one structured file so they never drift:

```
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --init 02-market/positioning.json
# fill positioning.json: moore, usp, two axes, 6+ players with x/y coordinates
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --data 02-market/positioning.json --out 02-market/positioning-map.html --root .
```

- `positioning.md`: buyer at top, Moore statement in a block quote, the two axes and why, the 2x2 with each player's quadrant, 6+ players placed, USP in bold at the foot. Any regulatory or legal claim about a rival carries the draft disclaimer (have a qualified lawyer review this before use).
- `positioning-map.html`: the same data as a one-page 2x2 for a prospect, gold dot for you, in your brand colours.

## Done when
`positioning.md` holds a complete Moore statement (no [placeholders]), the 2x2 has 6+ players with coordinates, and the USP is under 20 words. Verify:

```
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --check 02-market/positioning.json
```

## Log it
```
python ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-positioning \
  --artefact 02-market/positioning.md \
  --result "Moore statement + 2x2 with 7 players, USP in 11 words"
python ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"2":{"outcome":"<the USP>"}}}'
```
If your position changed which segment or claim you chase, add a dated line to `DECISIONS.md`.

## If it goes wrong
No empty corner? Your axes are wrong: swap one for a dimension where buyers disagree more, and re-plot. If every honest pair still lands you on a rival, your idea is not yet differentiated: say so in `DECISIONS.md` and narrow the offer until a gap appears. USP failing the rival test means you are describing a feature: lead with the outcome the buyer begged for. If the script will not run, `positioning.md` is the artefact of record; fix the render later.
