---
name: Size The Market
description: Sizes TAM, SAM and SOM two ways, top-down and bottom-up, then triangulates. Shows the maths and sources every assumption. Use on Day 2 once the market map is drawn.
when_to_use: Day 2 market work, straight after d2-market-map has written market-map.md, before you position or price.
---

# Size The Market

**What this does.** Puts a defensible number on your market at three levels (TAM, SAM, SOM), worked out two independent ways and checked against each other.
**Why it matters.** A market you cannot size is a market you are guessing at. Do it once, properly, and you learn two things: whether the prize is big enough to bother, and whether your story holds together. The two methods are the point. Top-down flatters you; bottom-up keeps you honest. When they disagree, the gap is the most useful thing on the page, because it tells you exactly which assumption you have not thought through.
**You are ready for this when.** `02-market/market-map.md` exists.

## Before you start
Read `02-market/market-map.md`. Your sizing is only as good as the segment and incumbents you named there. Lift the one-line market definition from the top of that file: everything here sizes that market and no other.

One rule above all others: this skill invents no numbers. Every figure is either sourced (a URL, a named report with a year, a public register, your own interview list, your pricing draft) or it is written down as an assumption in plain sight. The script enforces this: leave a source blank and it flags the number as UNSOURCED. We do not launder a guess into a model by putting it in a table. If the honest answer is "I am assuming this", write exactly that.

Open `references/market-sizing-template.md` before you write. That is the shape of the write-up.

Definitions, kept straight so you do not muddle them:
- **TAM**, Total Addressable Market: everyone with the problem, if you owned 100% of the world.
- **SAM**, Serviceable Addressable Market: the slice you can actually reach and serve, given your geography, segment and product. For most bootcamp founders this is Jersey plus perhaps the other Islands, one segment.
- **SOM**, Serviceable Obtainable Market: what you could realistically win inside a year or two, being one small firm. This is the number that decides whether the business is worth building.

## Steps
1. Name the market in one line at the top, lifted verbatim from `market-map.md`. If you cannot state it in one line, go back to the map.
2. Generate the inputs file. Run the script in template mode: `python3 ${CLAUDE_SKILL_DIR}/scripts/size.py --template 02-market/market-sizing-inputs.json`. This writes a JSON file with every field you must fill in and a short note on each.
3. Fill in the **top-down** block. Start from a published total market value (the whole spend in this market, per year) and cut it down with two fractions: the addressable fraction (the share you could serve) and the obtainable fraction (the share you could win). Source the total value properly. The two fractions are usually your judgement: mark them as assumptions and say why you chose each. Top-down without a sourced total is astrology, so if you cannot find one, say so and lean on the bottom-up.
4. Fill in the **bottom-up** block. Start from the ground: how many real customers have this problem (a count you can defend, from a register, a directory, or your Day 1 interview list), what fraction you can actually reach, what fraction of those you win in year one (be honest: 1% to 10% is normal, not 50%), and what one customer pays you per year (your pricing draft or a comparable). The script multiplies these up.
5. Run the sizing: `python3 ${CLAUDE_SKILL_DIR}/scripts/size.py --assumptions 02-market/market-sizing-inputs.json --out 02-market/market-sizing.md --csv 02-market/market-sizing.csv`. It prints TAM, SAM and SOM both ways, the gap between them, and a verdict.
6. Read the gap. The script triangulates on SOM, the number that matters, and passes when the two methods land within 2x of each other. If they are further apart, that is not a failure, it is a finding: one of your assumptions is wrong. Usually it is the obtainable fraction (top-down optimism) or the win fraction (bottom-up realism). Change the assumption you least believe, note why, and re-run. Do not average two numbers you do not trust.
7. Write it up in `market-sizing.md` following the template: the market line, the table the script produced, the top-down and bottom-up workings in words, the triangulation verdict, and an assumptions register listing every unsourced number in plain sight. Then state in two sentences what the SOM means for the sale: at your price, how many customers is the year-one SOM, and could you actually work through that many by Day 5?

## The artefact
Writes two files under `02-market/`, plus a small inputs file.

`market-sizing.md` in Markdown, following `references/market-sizing-template.md`: the market line, the results table (top-down, bottom-up and gap for each of TAM, SAM, SOM), the workings for both methods with a source or an explicit assumption against every number, the triangulation verdict, and the assumptions register.

`market-sizing.csv`: the six figures (three layers, two methods) plus the gap ratio and currency, one row per layer, for anyone who wants to check the arithmetic in a spreadsheet.

`02-market/market-sizing-inputs.json` holds your assumptions and their sources, so the model is reproducible: change an input, re-run, and both output files update.

Good looks like a page where a sceptic can retrace every number to a source or a clearly-owned assumption, and the two methods agree closely enough that you believe the SOM.

## Done when
All true: TAM, SAM and SOM are each stated with a currency symbol; both methods (top-down and bottom-up) are shown for each layer; and the two SOM figures are within 2x of each other, OR the write-up names the single assumption that explains the gap. `market-sizing.md` and `market-sizing.csv` both exist. If any number in the tables has no source and is not listed in the assumptions register, the sizing is not done.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-market-sizing`, artefact path `02-market/market-sizing.md`, and the numeric result (the SOM, for example "SOM £120,000 year one"). Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: record the Day 2 outcome (the three figures and the gap ratio) and register the artefacts. If sizing changed your mind about whether the market is worth chasing, log that as a dated decision with its rationale in DECISIONS.md.

## If it goes wrong
If you cannot find a sourced total market value, drop the top-down and rely on the bottom-up alone, but say clearly in the write-up that you have only one method and treat the number with more caution. Bottom-up is almost always available: you can count customers and set a price even when no analyst has published a total.

If the two methods are miles apart (5x or more) and you cannot reconcile them, do not paper over it. Write the gap up honestly and name your best single explanation. A sized market with an admitted weakness beats a tidy number nobody believes.

If the script fails to run, `market-sizing.md` is still the artefact of record: do the arithmetic by hand from the template, show your working, and fix the script later. Never let a broken render block Day 2.
