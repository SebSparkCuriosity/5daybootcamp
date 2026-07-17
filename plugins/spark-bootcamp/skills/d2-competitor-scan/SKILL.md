---
name: Scan The Competition
description: Puts your rivals side by side, scores them on what buyers care about, and names the one gap you own. Day 2, after the market map.
when_to_use: Day 2, after d2-market-map, before the proposition. "who are my competitors", "how do I stand out", "find the gap".
---

# Scan The Competition

**What this does.** Puts six or more real rivals in one table, scores each on five or more dimensions, and ends on one sentence naming the gap you own.
**Why it matters.** Buyers already cope somehow, so if you cannot say in one sentence how you differ, they will not switch, and Day 3 builds the wrong thing.
**You are ready for this when.** `02-market/market-map.md` exists.

## Before you start
Read `02-market/market-map.md` (your chosen segment and pain) and `00-prework/interview-target-spec.md` if it exists. Never invent numbers: every cell is a fact from the rival's own site (cite the URL) or a cell marked "assumption".

## Steps
1. List six to eight rivals: direct (same job, same buyer), indirect (different tool, same pain), and the status quo (spreadsheet, manual process, "do nothing"). The status quo wins the most deals, so include it.
2. Pick five or more dimensions your buyer weighs, not ones that flatter you. Defaults: price, who it is for, main strength, main weakness, one regulated-Jersey concern (data residency, audit trail, local support). Fuller menu in `references/dimensions.md`.
3. Fill the matrix in `competitor-matrix.csv`: one row per rival, one column per dimension, each cell a short phrase plus its source.
4. Score honestly. Mark who leads each dimension. Write down where a rival beats you.
5. Name the gap. Find one column where every rival is weak and your buyer cares. Write it as one sentence: every rival does X weakly, our buyer feels Y, so we win by Z. One gap.
6. Sanity-check: can you deliver it in five days? If not, pick the next-best provable gap. Record the reasoning in `DECISIONS.md`.

Branch only where sourcing differs.

## For software
Pull pricing, features and reviews from the rival's pricing/product pages and G2 or Capterra. Cite each URL. "Price on request" is itself a data point (usually expensive, slow to buy); note it.

## For hardware
Sources are spec sheets, Amazon or trade-supplier listings, and manufacturer pages. Compare unit price, lead time, build quality and warranty too. A physical incumbent with no website: a distributor catalogue or phone call is a valid, cited source.

## For services
Rivals are firms, freelancers and in-house. Sources are services pages, LinkedIn, published day rates. Compare price model (fixed vs hourly), turnaround, specialism and how productised the offer is. Score clarity: a vague "bespoke consulting" rival is beatable on clarity alone.

## The artefact
Two files in `02-market/`:
- `competitor-matrix.csv`: rival name, one column per dimension, a `source` column. 6+ rows, 5+ dimension columns.
- `competitors.md`: intro naming the buyer, the matrix as a table, a two-line read per rival, the gap sentence in bold. Add the draft disclaimer only if you cite legal or regulatory claims.

Run `python ${CLAUDE_SKILL_DIR}/scripts/scaffold_matrix.py 02-market/competitor-matrix.csv` to write a starter CSV, then fill it. Run it again to check rows, dimensions and sourced cells.

## Done when
`competitor-matrix.csv` holds 6+ rival rows across 5+ dimension columns, every row has a non-empty source, and `competitors.md` ends with one bold gap sentence. The scaffold script prints PASS when all four hold.

## Log it
```
python ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-competitor-scan \
  --artefact 02-market/competitors.md \
  --result "7 rivals x 6 dimensions compared, gap named"
```
```
python ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"2":{"outcome":"<the gap sentence>"}}}'
```
If the gap changed your plan, add a line to `DECISIONS.md` saying which gap and why.

## If it goes wrong
Cannot find six rivals? Add the status quo, adjacent tools, the in-house option. Fewer than six real players is itself a finding: white space (note it) or a tiny market (flag it, reconsider the segment). Four well-sourced rivals plus a clear "no direct rival" note beats six padded with guesses.
