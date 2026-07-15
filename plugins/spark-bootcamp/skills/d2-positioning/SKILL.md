---
name: Fix Your Positioning
description: Fixes where you win and states the one USP a rival cannot claim, using a Moore statement and a 2x2 map. Use on Day 2 after the competitor scan.
when_to_use: Day 2 market work, straight after d2-competitor-scan, before you write the proposition or build anything. Trigger phrases: "how do I position this", "what's my USP", "where do I win", "positioning statement", "positioning map".
---

# Fix Your Positioning

**What this does.** Fixes the corner of the market you own, in three pieces: a Geoffrey Moore positioning statement, a 2x2 map with your rivals plotted, and one USP under 20 words that no rival can honestly claim.
**Why it matters.** Positioning is the decision that makes every later decision easier. It tells Day 3 what to build, Day 4 what to say, and Day 5 why a prospect should pay you and not the incumbent. Get it wrong and you build a slightly different version of what already exists. Get it right and you have a sentence a buyer repeats to a colleague. That sentence is worth more than any feature.
**You are ready for this when.** `02-market/competitors.md` and `01-discovery/target-segment.md` both exist.

## Before you start
Read `02-market/competitors.md`, especially the gap sentence at the foot and the dimensions in the matrix. Read `01-discovery/target-segment.md` for the exact buyer you chose. The gap you named yesterday is the raw material: today you turn it into a position you can state and defend.

Open `references/moore-and-usp.md` and keep it beside you. It holds the Moore template, the axis choices, and the three-part USP test you must pass.

One guardrail: do not invent a difference. Every claim in your position must be true and provable this week. A USP a rival can copy in an afternoon is not a position, it is a slogan. If you cannot back the claim, weaken it until you can.

## Steps
1. Write the Moore statement first. Use the exact format in `references/moore-and-usp.md`: for [buyer] who [need], [business] is a [category] that [benefit], unlike [rival or status quo] we [the one thing they cannot claim]. Fill every bracket. The category must be one your buyer already recognises in one second, not a phrase you invented.
2. Pick two axes for the map. Take them from the dimensions in `competitors.md`: the two where buyers disagree most about what they want. Do not pick two axes that measure the same thing (price and value collapse onto a diagonal and tell you nothing). Good pairs are in the reference.
3. Plot at least six players. Your direct rivals, the adjacent tools, and the status quo (the spreadsheet, the incumbent, doing nothing). Give each an x and a y from 0.0 to 1.0. Mark yourself. You must land in a corner no rival occupies. If you sit on top of a rival, your axes are wrong or you are not yet differentiated. Fix that before you continue.
4. Write the one USP. One sentence, under 20 words, that survives all three tests in the reference: the word count, the rival test (no competitor could say it straight-faced), and the buyer test (it names a benefit your interviewees actually asked for). Cut until only you can say it.
5. Sanity-check against Day 3. Can you actually deliver the thing your USP promises, in the live page you ship this week? If the USP leans on a capability you cannot demonstrate by Friday, it is a wish, not a position. Pick a claim you can prove, and record the swap in `DECISIONS.md`.

Branch only where the axes and the deliverable differ.

## For software
Your axes are usually feature-facing (breadth of workflow, depth, integration) crossed with a buyer-facing one (price, local fit, auditability). Your USP should point at the working slice you deploy on Day 3, so the position and the demo agree. If the USP names a feature, that feature must be in the slice.

## For hardware
Your axes are usually physical (unit price, build quality, lead time) crossed with fit for the buyer's setting. Your USP should be something the prototype or CAD render on Day 3 visibly proves, or that the pre-order page can honestly promise. Do not claim a spec you have not prototyped.

## For services
Your axes are usually price model (fixed vs hourly) and specialism, or turnaround against depth. Your USP should be provable in the sample deliverable you produce on Day 3. "We are the only firm that hands you a finished X in 48 hours" only holds if the sample proves the 48 hours. A productised, clearly named offer beats a vague rival on clarity alone, so make clarity part of the position.

## The artefact
Writes two files in `02-market/`:

- `positioning.md` in Markdown: the buyer named at the top, the full Moore statement in a block quote, a short paragraph on the two axes and why you chose them, the 2x2 rendered as a small table or described in prose with each player's quadrant, the six-plus players listed with their placement, and the one USP in bold at the foot. If you make any regulatory or legal claim about a rival, add the draft disclaimer.
- `positioning-map.html` in HTML: the same data rendered as a one-page 2x2 you can put in front of a prospect, gold dot for you, built from your brand colours.

Both read from one structured file so they never drift. Write the data once, render the picture from it:

```
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --init 02-market/positioning.json   # skeleton to fill in
# fill positioning.json: moore, usp, two axes, 6+ players with x/y coordinates
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --data 02-market/positioning.json --out 02-market/positioning-map.html --root .
```

Then write the readable `positioning.md` from the same data.

What good looks like: a reader who has never met your market can look at the map and, in ten seconds, see where you sit and why it is empty around you. The Moore statement has no brackets left in it. The USP is short enough to say out loud without pausing, and only you can say it.

## Done when
`positioning.md` holds a complete Moore statement (no [placeholders] left), the 2x2 has 6 or more players placed with coordinates, and the USP is under 20 words. Verify with the script in check mode: it prints PASS when all three hold.

```
python ${CLAUDE_SKILL_DIR}/scripts/build_map.py --check 02-market/positioning.json
```

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the numeric result:

```
python ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-positioning \
  --path 02-market/positioning.md \
  --result "Moore statement + 2x2 with 7 players, USP in 11 words"
```

Update state via the journey-state helper, recording the USP as the Day 2 outcome:

```
python ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --add-artefact d2-positioning 02-market/positioning.md "USP: <the one line>" \
  --set-day 2 outcome "<the USP>"
```

If your position changed which segment or claim you chase, add a dated line to `DECISIONS.md` saying what you chose and why.

## If it goes wrong
Cannot find a corner no rival owns? Your axes are probably wrong. Swap one for a dimension where buyers disagree more, and re-plot. If every honest axis pair still lands you on top of a rival, that is a real finding: your idea is not yet differentiated, and Day 3 must build the thing that separates you, not a lookalike. Say so in `DECISIONS.md` and narrow the offer until a gap appears.

USP keeps failing the rival test? You are describing a feature, not a difference. Go back to your interview notes and the gap sentence in `competitors.md`, and lead with the outcome the buyer begged for, not the mechanism. If the diagram script will not run, the map is still complete: `positioning.md` is the artefact of record and the HTML is a convenience. Fix the render later, do not let it block Day 2.
