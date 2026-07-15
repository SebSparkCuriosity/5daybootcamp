---
name: Map The Market
description: Name the players, the value chain and the substitutes for your validated problem, every incumbent sourced. Use first thing on Day 2 once the problem is locked.
when_to_use: Day 2 market work, the opening step, straight after d1-validated-problem has written validated-problem.md and target-segment.md.
---

# Map The Market

**What this does.** Turns your one-sentence problem into a picture of the market around it: the segments who feel it, the value chain that serves them today, the named incumbents already in the space (each with a source), and the substitutes people reach for instead. It writes a written map and a simple diagram.
**Why it matters.** You cannot position against a market you have not drawn. Founders who skip this either think they have no competition (they always do, it is called "a spreadsheet and a phone call") or panic at the giants and miss the soft underbelly. Draw the board first. Then you can see where you fit, who you take work from, and what you are genuinely better at.
**You are ready for this when.** `01-discovery/validated-problem.md` and `01-discovery/target-segment.md` both exist.

## Before you start
Read `01-discovery/validated-problem.md` for the problem sentence and the verdict, and `01-discovery/target-segment.md` for the named segment. If the Day 1 verdict was INSUFFICIENT EVIDENCE, stop: go back and reach 5 solid interviews first. Mapping a market for a problem you have not validated is drawing a castle in fog.

Guardrail on sources: every incumbent you name carries a source. A URL, a company registry entry, an interviewee who named them, or a note that you found them on a specific directory. If you cannot source it, you do not name it. We do not fabricate the competition, and we do not fabricate market size numbers. Any figure is either sourced or written down as an assumption in plain sight.

Open `references/market-map-template.md` and `references/sourcing-a-market.md` before you write. The first is the structure to fill in. The second tells you where to find real Jersey and UK players in twenty minutes.

## Steps
1. Restate the problem in one line at the top of the map, lifted verbatim from `validated-problem.md`. Everything below must serve this problem. If a player or a substitute does not touch this problem, it does not belong on the map.
2. **Segments.** Name at least 3 segments who feel this problem, starting with your target segment from Day 1. A segment is a "who", not a "what": trust administrators at small Jersey trust companies, sole-practitioner advocates, family-run restaurants doing under 40 covers. For each, write one line on how sharply they feel the problem, so you can rank them later.
3. **Value chain.** Lay out at least 4 stages of how the job gets done today, left to right, from the customer's first trigger to the outcome they want. For a services problem that might be: find a provider, scope the work, deliver it, review and repeat. Name where the pain and the money concentrate. That concentration is usually where you should aim.
4. **Incumbents.** Name at least 6 real players already serving this problem, each with a source (see the guardrail above). Split them into three honest buckets: direct (solve the same problem the same way), adjacent (solve a neighbouring problem and could swing into yours), and DIY or "big generic tool" (the spreadsheet, the manual process, the global SaaS nobody loves). Founders who list only direct competitors miss the ones that actually take their lunch.
5. **Substitutes.** Name at least 3 things people use instead of buying anything: a manual workaround, a junior member of staff, a free tool, doing nothing and living with the pain. Substitutes are your real competition on Day 5. "We do it in Excel and complain" beats most sales pitches.
6. **The gap.** Write two or three sentences naming where the map is thin: a segment nobody serves well, a value-chain stage everyone does badly, a substitute that clearly is not good enough. This is your opening. It feeds straight into Day 2's positioning work, so make it specific.
7. Build the diagram. Fill in `02-market/market-map.json` with your segments, stages, incumbents and substitutes, then run the builder (see The artefact). It renders a one-page HTML board you can eyeball and, later, drop in front of a prospect.

## The artefact
Writes three files under `02-market/`.

`market-map.md` in Markdown, following `references/market-map-template.md`: the problem line, the segments, the value chain, the incumbent table (name, bucket, one line on what they do, source), the substitutes, and the gap paragraph.

`market-map.json`, a small structured data file holding the same segments, stages, incumbents and substitutes. This is the input to the diagram, so state and picture never drift.

`market-map.html`, a self-contained one-page diagram built by the script:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/build_map.py \
  --root . \
  --data 02-market/market-map.json \
  --out 02-market/market-map.html
```

The script reads your brand colours from `.spark/brand/brand.json` if it exists and falls back to Spark's dark green and gold if it does not. It needs no external libraries.

Good looks like a map a stranger could read in one minute and correctly point to where you plan to win.

## Done when
All of these are true, and each is countable: `market-map.md` names at least 3 segments, lays out at least 4 value-chain stages, names at least 6 incumbents each with a source, and names at least 3 substitutes; the gap paragraph is written; and `market-map.html` exists and opens as a single readable page. If any count is short, the map is not done. Do not round up by inventing players.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-market-map`, artefact path `02-market/market-map.md`, and the numeric result (count of sourced incumbents, for example "7 incumbents mapped"). Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: set days.2 target if not already set, record the outcome (segments, incumbents and substitutes counted), and register the three artefacts. If your map changed your mind about which segment to chase first, log that as a dated decision with its rationale in DECISIONS.md.

## If it goes wrong
If you can only find 3 or 4 incumbents, you are probably searching too narrowly. Widen from "someone doing exactly my thing" to "someone the customer pays to make this problem smaller today", and add the DIY and big-generic-tool buckets: they are always populated. Use `references/sourcing-a-market.md` for where to look. If the diagram script fails to run, the map is still complete without it: the `market-map.md` file is the artefact of record, and the HTML is a convenience. Fix the diagram later; do not let a broken render block Day 2. If you genuinely cannot find real competitors after an honest hour, that is a signal, not a win: either the problem is not painful enough to have attracted anyone, or you have defined it so narrowly nobody else has noticed. Re-read your Day 1 evidence before you celebrate an empty market.
