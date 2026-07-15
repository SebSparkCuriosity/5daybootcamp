---
name: Craft The Proposition
description: Turns customer jobs, pains and gains into one proposition statement under 25 words, each tagged to a real Day 1 quote, plus the customer's numeric success metric with a baseline. Use on Day 2 after positioning.
when_to_use: Day 2 market work, after d2-positioning has written positioning.md, once discovery-findings.md exists. The last Day 2 step before Day 3 build.
---

# Craft The Proposition

**What this does.** Turns what you learned in your interviews into one sentence a stranger understands, and names the one number your customer needs to move.
**Why it matters.** A proposition is not a slogan. It is a promise you can prove. Do it properly and two things happen: your Day 3 build knows exactly what to make, and Friday's pricing has a number to anchor to. Skip the number and you are selling a feeling, which nobody in Jersey finance pays for.
**You are ready for this when.** `01-discovery/discovery-findings.md` and `02-market/positioning.md` both exist.

## Before you start
Read both files first:
- `01-discovery/discovery-findings.md`: your interview synthesis. This is the raw material. Every job, pain and gain you claim below must trace back to a real quote in here.
- `02-market/positioning.md`: where you sit against the alternatives. The proposition must fit the position, not fight it.

Open `${CLAUDE_SKILL_DIR}/references/proposition-template.md`. That is the shape of the write-up, and it is the format the checker understands.

One rule above all: no quote, no claim. We use the Value Proposition Canvas, and the whole point of it here is discipline. If you cannot tag a job, pain or gain to something a real person actually said in an interview, it does not go on the page. Founders love inventing pains their product happens to solve. This skill stops that. Every line earns its place with a quote.

## What the Value Proposition Canvas is
Two halves. The right half is the customer: their **jobs** (what they are trying to get done), their **pains** (what goes wrong or costs them today), their **gains** (what a better world looks like). The left half is your offer, and you only build the left half once the right half is honest. Most people rush to the offer. Do the customer half first, from quotes, and the offer half almost writes itself.

Keep the three straight:
- **Job**: the task or goal, stated as a verb. "Reconcile client accounts every month end."
- **Pain**: the friction, cost, risk or fear attached to that job today. "It takes three days and one transposed digit fails the audit."
- **Gain**: the outcome they would happily pay for. "Month-end done in a morning, clean enough that the regulator nods."

## Steps
1. Pull the quotes. Go through `discovery-findings.md` and lift the sharpest verbatim lines, the ones that made you sit up. Number them Q1, Q2, Q3 and so on. You want at least nine strong quotes, because you will tag at least three jobs, three pains and three gains.
2. Fill the customer half of the canvas in the template. Write at least three jobs, three pains and three gains. Against each one, in brackets, put the quote tag it comes from, like `(quote: Q3)`. If you reach for a job or pain and no quote backs it, delete it. This is the hard bit and the whole value.
3. Rank each list. Put the most important job, the worst pain and the most wanted gain at the top. You are looking for the one pain that, if you killed it, they would switch supplier. That pain becomes the spine of the statement.
4. Write the proposition statement. One sentence, under 25 words. Name who it is for, the top pain you remove or gain you deliver, and how you are different (from positioning.md). Plain words. Read it aloud: if you run out of breath or reach for jargon, cut it. The checker counts the words, so keep it tight.
5. Name the success metric. This is Spark's promise made concrete: every proposition carries a number. State the one measure your customer would use to know it worked, its baseline today, the target you are aiming for, and how it is measured. Format it "move X from [baseline] to [target], measured by [method]". For example "cut month-end reconciliation from 3 days to half a day, measured by the finance lead's own timesheet". No baseline, no metric: a target with nothing to measure against is a wish.
6. Sanity-check against positioning. Read the statement and the metric next to `positioning.md`. Do they tell the same story? If the position says "the auditable one" but the metric is pure speed, one of them is wrong. Fix it now, before Day 3 builds the wrong thing.
7. Run the checker: `python3 ${CLAUDE_SKILL_DIR}/scripts/proposition_check.py 02-market/proposition.md`. It counts the tagged jobs, pains and gains, counts the words in your statement, and checks the metric has a baseline and a target. It prints PASS or names exactly what is missing. Fix what it flags and re-run until it passes.

## The artefact
Writes `02-market/proposition.md` in Markdown, following `${CLAUDE_SKILL_DIR}/references/proposition-template.md`.

It contains: a numbered quote bank lifted from discovery; the customer half of the Value Proposition Canvas (jobs, pains, gains, at least three each, every line tagged to a quote); the one-sentence proposition statement under 25 words; and the success metric with its baseline, target and measurement method.

Good looks like a page where a sceptic can point at any pain and you can show them the exact quote it came from, the statement reads in one breath, and the metric is a number they could actually check in a month.

This is the same across software, hardware and services. What differs later is what you build to deliver the promise, not the promise itself. So there is no path branch here: one proposition, one number, whatever you are selling.

## Done when
All true, and the checker confirms it:
- At least three jobs, three pains and three gains, each tagged to a numbered quote from discovery.
- A proposition statement of fewer than 25 words.
- A stated customer success metric with a baseline and a target ("move X from A to B, measured by C").

`02-market/proposition.md` exists and `proposition_check.py` prints PASS.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d2-proposition`, artefact path `02-market/proposition.md`, and the numeric result (the success metric, for example "cut month-end from 3 days to 0.5 days"). Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: record the Day 2 outcome (the statement and the metric) and register the artefact. If the proposition changed your mind about the segment or the position, log that as a dated decision with its rationale in DECISIONS.md.

## If it goes wrong
If you cannot find three real quotes for a pain, you have not done enough discovery on that pain, and the honest move is to narrow the proposition to the pains you can prove, not to invent the rest. A narrow proposition backed by quotes beats a broad one backed by hope.

If you cannot name a baseline for the metric because nobody measures it today, that is itself a finding: your first job with the customer may be to start measuring. Write the metric as "currently unmeasured, we will establish the baseline in week one, target [X]" and flag it as an assumption. Do not leave the number blank.

If the checker will not run, `02-market/proposition.md` is still the artefact of record. Count the words and the tags by hand against the Done when list, and fix the script later. Never let a broken script block Day 2.
