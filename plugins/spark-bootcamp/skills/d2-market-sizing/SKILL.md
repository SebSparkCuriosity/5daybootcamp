---
name: Size The Market
description: Sizes TAM, SAM and SOM two ways, top-down and bottom-up, then triangulates and sources every assumption. Day 2, after the market map.
when_to_use: Day 2, straight after d2-market-map writes market-map.md, before you position or price.
---

# Size The Market

**What this does.** Puts a defensible number on your market at three levels (TAM, SAM, SOM), worked two independent ways and checked against each other.
**Why it matters.** A market you cannot size is a market you are guessing at, and the two methods are the point: top-down flatters you, bottom-up keeps you honest, and the gap between them shows the assumption you have not thought through.
**You are ready for this when.** `02-market/market-map.md` exists.

## Before you start
Read `02-market/market-map.md` and lift its one-line market definition. Open `references/market-sizing-template.md` for the write-up shape. Invent no numbers: every figure is sourced (URL, named report with year, register, interview list, pricing draft) or written down as an assumption in plain sight. The script flags blanks as UNSOURCED.

TAM: everyone with the problem. SAM: the slice you can reach and serve (geography plus one segment). SOM: what you realistically win in a year or two as one small firm, the number that decides if this is worth building.

The judgement lives in the assumptions, so talk them through first (10 minutes). Ask in plain English: how many of these firms could you realistically reach, how many would you win in year one, and what would one pay? Offer your own number with a reason for each, then let the founder set it, push back, or say "you decide" (logged in DECISIONS.md). The founder owns every assumption the register carries.

## Steps
1. Name the market in one line at the top, verbatim from `market-map.md`.
2. Generate inputs: `python3 ${CLAUDE_SKILL_DIR}/scripts/size.py --template 02-market/market-sizing-inputs.json`.
3. Fill the **top-down** block: a sourced total market value, times an addressable fraction, times an obtainable fraction. Source the total; mark both fractions as assumptions and say why.
4. Fill the **bottom-up** block: defensible customer count (register, directory, Day 1 interviews), reachable fraction, year-one win fraction (1% to 10% is normal), and annual price per customer.
5. Run: `python3 ${CLAUDE_SKILL_DIR}/scripts/size.py --assumptions 02-market/market-sizing-inputs.json --out 02-market/market-sizing.md --csv 02-market/market-sizing.csv`.
6. Read the gap. It triangulates on SOM and passes within 2x. Wider is a finding, not a failure: change the assumption you least believe (usually obtainable or win fraction), note why, re-run. Never average numbers you distrust.
7. Write up `market-sizing.md` per the template: market line, results table, both workings in words, triangulation verdict, assumptions register. Close with two sentences on what the SOM means for the sale: how many customers at your price, and could you work through that many by Day 5?

## The artefact
Under `02-market/`: `market-sizing.md` (market line, results table, both workings with a source or explicit assumption per number, verdict, register), `market-sizing.csv` (six figures plus gap ratio and currency, one row per layer), and `market-sizing-inputs.json` (assumptions and sources, so a changed input re-runs both outputs). Good means a sceptic can retrace every number.

## Done when
TAM, SAM, SOM each stated with a currency symbol; both methods shown for each layer; the two SOM figures within 2x, OR the write-up names the single assumption explaining the gap. Both `market-sizing.md` and `market-sizing.csv` exist. Any unsourced number not in the register means not done.

## Log it
Append to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-market-sizing`, artefact `02-market/market-sizing.md`, numeric result (e.g. "SOM £120,000 year one"). Then set the Day 2 outcome (three figures and gap ratio) via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. If sizing changed your mind on chasing this market, log a dated decision in DECISIONS.md.

## If it goes wrong
No sourced total? Drop top-down, rely on bottom-up alone, and say so in the write-up. Methods 5x apart and irreconcilable? Write the gap up honestly and name your best single explanation. Script fails? `market-sizing.md` is still the artefact of record: do the arithmetic by hand from the template and fix the script later.
