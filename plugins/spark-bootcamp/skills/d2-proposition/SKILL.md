---
name: Craft The Proposition
description: Turns customer jobs, pains and gains into one proposition under 25 words, each tagged to a real Day 1 quote, plus a numeric success metric.
when_to_use: Day 2, after d2-positioning, once discovery-findings.md exists. Last Day 2 step before build.
---

# Craft The Proposition

**What this does.** Turns your interviews into one sentence a stranger understands, and names the one number your customer needs to move.
**Why it matters.** A proposition is a promise you can prove: get it right and Day 3 knows what to build and Friday's pricing has a number to anchor to.
**You are ready for this when.** `01-discovery/discovery-findings.md` and `02-market/positioning.md` both exist.

## Before you start
Read `01-discovery/discovery-findings.md` (the raw material) and `02-market/positioning.md` (the proposition must fit the position). Open `${CLAUDE_SKILL_DIR}/references/proposition-template.md` for the shape. A working discussion of about 15 minutes: the quote work is mechanical, the promise is the founder's. One rule: no quote, no claim. Every job, pain or gain must trace to a real interview line.

The Value Proposition Canvas, customer half first: **jobs** (task, stated as a verb), **pains** (friction/cost/risk today), **gains** (outcome they'd pay for). Do the customer half honestly and the offer half writes itself.

## Steps
1. Pull the sharpest verbatim quotes from `discovery-findings.md`. Number them Q1, Q2, Q3... Aim for at least nine.
2. Fill the customer half in the template: at least three jobs, three pains, three gains, each tagged like `(quote: Q3)`. No quote backing it, delete it.
3. Rank each list with the founder: offer your top pick with the tally behind it, then ask which pain would really make their buyer switch supplier. Their call stands. That pain is the spine of the statement.
4. Write the proposition together: ask the founder to make the promise out loud first ("what do you promise this buyer?"), then cut to one sentence under 25 words. Who it's for, the top pain removed or gain delivered, how you differ (from positioning.md). Plain words, read aloud, their phrasing kept where it survives.
5. Name the success metric: "move X from [baseline] to [target], measured by [method]". No baseline, no metric.
6. Sanity-check statement and metric against `positioning.md`: same story? Fix now, before Day 3.
7. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/proposition_check.py 02-market/proposition.md`. Fix what it flags, re-run until PASS.

## The artefact
Writes `02-market/proposition.md` in Markdown per `${CLAUDE_SKILL_DIR}/references/proposition-template.md`: numbered quote bank, customer half of the canvas (three each, all tagged), the under-25-word statement, and the metric with baseline, target and method. A sceptic can point at any pain and see its quote. Same across software, hardware and services: one proposition, one number.

## Done when
- At least three jobs, three pains, three gains, each tagged to a numbered quote.
- Proposition statement under 25 words.
- Metric with baseline and target ("move X from A to B, measured by C").
- `02-market/proposition.md` exists and `proposition_check.py` prints PASS.

## Log it
Append one line via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-proposition`, artefact path `02-market/proposition.md`, result (the metric, e.g. "cut month-end from 3 days to 0.5 days"). Record the Day 2 outcome via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. If the proposition changed your segment or position, log a dated decision in DECISIONS.md.

## If it goes wrong
No three quotes for a pain: narrow the proposition to what you can prove, don't invent the rest. No baseline because nobody measures it: write "currently unmeasured, we will establish the baseline in week one, target [X]" and flag it as an assumption. Never leave the number blank. Checker won't run: count words and tags by hand against Done when, fix the script later.
