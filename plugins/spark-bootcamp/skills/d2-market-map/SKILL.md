---
name: Map The Market
description: Name the players, value chain and substitutes for your validated problem, every incumbent sourced. Run first on Day 2.
when_to_use: Day 2 opener, straight after d1-validated-problem writes validated-problem.md and target-segment.md.
---

# Map The Market

**What this does.** Turns your one-sentence problem into a market picture: the segments who feel it, the value chain serving them, the named incumbents (each sourced), and the substitutes people reach for instead. Writes a map and a diagram.
**Why it matters.** You cannot position against a market you have not drawn, so draw the board first and you can see where you fit and who you take work from.
**You are ready for this when.** `01-discovery/validated-problem.md` and `01-discovery/target-segment.md` both exist.

## Before you start
Read `01-discovery/validated-problem.md` for the problem and verdict, and `01-discovery/target-segment.md` for the segment. If the Day 1 verdict was INSUFFICIENT EVIDENCE, stop and reach 5 solid interviews first.

Guardrail: every incumbent carries a source (URL, registry entry, interviewee, directory). No source, no name. Never fabricate players or market-size numbers: any figure is sourced or written down as an assumption in plain sight.

Open `references/market-map-template.md` (the structure) and `references/sourcing-a-market.md` (where to find real Jersey and UK players) before you write.

## Steps
1. Restate the problem verbatim from `validated-problem.md` at the top. If a player or substitute does not touch it, it is off the map.
2. **Segments.** Name at least 3 who feel this problem, starting with your Day 1 target. A segment is a "who", not a "what". One line each on how sharply they feel it.
3. **Value chain.** Lay out at least 4 stages of how the job gets done today, left to right, trigger to outcome. Name where pain and money concentrate: that is usually where to aim.
4. **Incumbents.** Name at least 6 real players, each sourced, in three buckets: direct, adjacent, and DIY or big generic tool.
5. **Substitutes.** Name at least 3 things people use instead of buying: a manual workaround, a junior staffer, a free tool, doing nothing.
6. **The gap.** Two or three specific sentences on where the map is thin. This is your opening and feeds Day 2 positioning.
7. Fill `02-market/market-map.json` with segments, stages, incumbents and substitutes, then run the builder (see The artefact).

## The artefact
Writes three files under `02-market/`.
`market-map.md` following `references/market-map-template.md`: problem line, segments, value chain, incumbent table (name, bucket, one line, source), substitutes, gap paragraph.
`market-map.json`, the same data structured, feeding the diagram so state and picture never drift.
`market-map.html`, a self-contained one-page diagram from the script (reads brand colours from `.spark/brand/brand.json`, falls back to Spark dark green and gold, no external libraries):

```
python3 ${CLAUDE_SKILL_DIR}/scripts/build_map.py \
  --root . \
  --data 02-market/market-map.json \
  --out 02-market/market-map.html
```

Good looks like a map a stranger reads in one minute and correctly points to where you plan to win.

## Done when
`market-map.md` names at least 3 segments, at least 4 value-chain stages, at least 6 sourced incumbents and at least 3 substitutes; the gap paragraph is written; and `market-map.html` opens as a single readable page. If any count is short, it is not done. Do not invent players.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-market-map`, artefact path `02-market/market-map.md`, numeric result (sourced incumbent count, e.g. "7 incumbents mapped"). Then set the Day 2 target and outcome via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. If the map changed which segment you chase first, log a dated decision in DECISIONS.md.

## If it goes wrong
Only 3 or 4 incumbents means you are searching too narrowly: widen from "doing exactly my thing" to "someone the customer pays to shrink this problem today", and populate the DIY and big-generic-tool buckets. Use `references/sourcing-a-market.md`. If the diagram script fails, `market-map.md` is still the artefact of record: fix the render later, do not block Day 2. If you truly find no competitors after an honest hour, that is a signal not a win: re-read your Day 1 evidence.
