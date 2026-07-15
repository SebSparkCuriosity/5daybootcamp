---
name: Scan The Competition
description: Lays your rivals side by side, scores them on the dimensions buyers actually care about, and names the one gap you exploit. Use on Day 2 after the market map.
when_to_use: Day 2 market work, straight after d2-market-map, before you write the proposition. Trigger phrases: "who are my competitors", "competitor analysis", "how do I stand out", "find the gap".
---

# Scan The Competition

**What this does.** Puts at least six real rivals in one table, scores each on at least five dimensions, and ends on one written sentence naming the gap you own.
**Why it matters.** You are not the first person to notice this problem. Buyers already have a way of coping, a spreadsheet, an incumbent, a rival, or doing nothing. If you cannot say in one sentence how you differ, neither can they, and they will not switch. The gap is the reason you exist. Find it now, before you build anything, so Day 3 builds the right thing.
**You are ready for this when.** `02-market/market-map.md` exists.

## Before you start
Read `02-market/market-map.md`, especially the segment you chose and the pain you are targeting. Read `01-discovery/interview-target-spec.md` if it exists, so you compare rivals against the buyer you actually chase.

One guardrail: never invent numbers. Every cell in the matrix is either something you read on the rival's own site (cite the URL) or a labelled assumption you will test. A pretty table full of guesses is worse than no table. Where a figure is a guess, write "assumption" in the cell.

## Steps
1. List the rivals. Aim for six to eight. Include three kinds: direct rivals (same job, same buyer), indirect rivals (a different tool that solves the same pain), and the status quo (the spreadsheet, the manual process, or "do nothing"). The status quo is a competitor. It wins more deals than any rival, so it goes in the table.
2. Pick your dimensions. Five or more, and they must be the ones your buyer weighs, not the ones that flatter you. Good defaults: price, who it is built for, main strength, main weakness, and one that matters in a regulated Jersey setting (data residency, audit trail, or local support). See `references/dimensions.md` for a fuller menu by sector.
3. Fill the matrix. One row per rival, one column per dimension. For each cell, capture the fact and its source. Keep it short: a phrase, not a paragraph. Put the raw table in `competitor-matrix.csv` so it is sortable and auditable.
4. Score honestly. For each dimension, mark who leads. If a rival beats you on something real, write it down. The point is to find where you win, and you only find that by admitting where you lose.
5. Name the gap. Look down the columns for a dimension where every rival is weak and your buyer cares. That underserved column is your gap. Write it as one sentence: "Every rival [does this weakly], and our buyer [feels this pain], so we win by [this]." One gap. Not three.
6. Sanity-check the gap against reality. Can you actually deliver it in five days? If the gap needs a feature you cannot ship this week, pick the next-best gap you can prove. Record the reasoning in `DECISIONS.md`.

Branch only where sourcing differs.

## For software
Rivals are usually easy to find and read. Pull pricing from their pricing page, features from their product pages, and reviews from G2 or Capterra. Cite each URL. Watch for rivals who hide pricing: "price on request" is itself a data point (often it means expensive and slow to buy), so note it.

## For hardware
Rivals include existing products and DIY workarounds. Sources are spec sheets, Amazon or trade-supplier listings, and manufacturer pages. Compare on unit price, lead time, build quality, and warranty as well as the buyer-facing dimensions. If a rival is a physical incumbent with no website, a phone call or a distributor catalogue is a valid source. Cite it.

## For services
Rivals are other firms, freelancers, and the client doing it in-house. Sources are their services pages, LinkedIn, and any published day rates or packages. Compare on price model (fixed vs hourly), turnaround, specialism, and how productised the offer is. A vague "we do bespoke consulting" rival is beatable on clarity alone, so score clarity as a dimension.

## The artefact
Writes two files in `02-market/`:

- `competitor-matrix.csv`: the raw grid. Column 1 is the rival name, then one column per dimension, then a `source` column holding the URLs or notes backing that row. At least 6 data rows (one per rival) and at least 5 dimension columns.
- `competitors.md`: the readable write-up. A short intro naming the buyer, the matrix rendered as a table, a two-line read on each rival, and the closing gap sentence in bold. Add the draft disclaimer only if you cite legal or regulatory claims about a rival.

Run `python ${CLAUDE_SKILL_DIR}/scripts/scaffold_matrix.py 02-market/competitor-matrix.csv` to write a starter CSV with the default columns, then fill it in. The script checks your finished file too: run it again and it counts rows, dimensions and sourced cells, and tells you what is missing.

What good looks like: a reader who knows nothing about your market can look at the table and see, in ten seconds, who the players are and where the hole is. Every row traces to a source. The gap sentence is specific enough that Day 3 knows what to build.

## Done when
`competitor-matrix.csv` holds 6 or more rival rows across 5 or more dimension columns, every row has a non-empty source, and `competitors.md` ends with one bold gap sentence. Verify by running the scaffold script in check mode: it prints PASS when all four conditions hold.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the numeric result (rivals compared, e.g. "7 rivals x 6 dimensions, 1 gap named"):

```
python ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-competitor-scan \
  --path 02-market/competitors.md \
  --result "7 rivals x 6 dimensions compared, gap named"
```

Update state via the journey-state helper, recording the gap as the Day 2 progress:

```
python ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --add-artefact d2-competitor-scan 02-market/competitors.md "gap: <one line>" \
  --set-day 2 outcome "<the gap sentence>"
```

If the gap changed your plan, add a line to `DECISIONS.md` saying which gap you chose and why.

## If it goes wrong
Cannot find six rivals? Widen the net. Add the status quo, add adjacent tools, add the in-house option. If a market genuinely has fewer than six players, that is a finding: either you have found white space (good, note it) or the market is tiny (worrying, flag it and reconsider the segment). Four well-sourced rivals plus the status quo plus a clear "no direct rival exists" note beats six padded with guesses. Never inflate the table to hit the number.
