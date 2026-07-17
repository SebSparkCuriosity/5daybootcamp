---
name: Go-To-Market Plan
description: Ranks your first 10 named customers by warmth, gives each one next action, hands #1 to Day 5. Use on Day 4 once buying signals and landing captures exist.
when_to_use: "Day 4 GTM, after landing page live and scorecard exists. Trigger: who do I sell to first, build my prospect list."
---

# Go-To-Market Plan

**What this does.** Turns scattered signals into one ranked list of 10 named people, warmest first, each with one next action, and hands #1 to Day 5.
**Why it matters.** The warmest prospect closes far faster than a cold one, so you start there, not at the top of an alphabet.
**You are ready for this when.** `04-gtm/buying-signal-scorecard.csv` exists and your landing page has captured real visitors.

## Before you start
The ranker reads three inputs: `04-gtm/buying-signal-scorecard.csv`, the landing capture store (`04-gtm/landing-captures.csv`, or your hardware pre-order/waitlist export at the same path; export from Supabase or a form tool to that CSV first), and `01-discovery/interviews/` or `01-discovery/interview-notes.md`.

Guardrail: this skill plans outreach. It sends nothing and spends nothing until Day 5, and only after you say yes.

## Steps
1. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/rank_prospects.py`. It merges the three sources, de-duplicates by name and email, scores warmth 0 to 100, and writes `04-gtm/prospect-ranking.csv`. Missing sources are flagged and skipped.
2. Walk the list with the founder, name by name (15 minutes): they know warmth the model cannot see (a shared history, a feud, a budget freeze). Trust or overrule the score together; every overrule gets one line in DECISIONS.md. Warmth rewards intent (deposit, booked call, "when can I buy"), exact segment match, and repeat engagement. Formula in `references/warmth-model.md`.
3. Cut to exactly 10. Fewer starves Day 5; more spreads you thin. If the ranker found fewer than 10 real people, that is the finding: your funnel is too narrow. Note it, carry the shorter list, do not invent names.
4. Give each of the 10 one next action naming the channel and the ask. One, not three.
5. Branch the next action by path:

   ## For software
   Warmest used the deployed slice and hit its limit. Book a call, offer to switch on the paid tier live.

   ## For hardware
   Warmest left a deposit or pre-order. Confirm it, give a ship or demo date, ask for the balance or next commitment.

   ## For services
   Warmest booked an intake slot or replied to the sample. Send the one-page proposal with fixed price and start date.

6. Pick #1 and write one sentence on why. Warmest usually wins; if a cooler prospect is a faster yes (holds budget, replied today), promote them and record the reason in `DECISIONS.md`.

## The artefact
Writes `04-gtm/gtm-plan.md`: a ranked table of 10 (rank, name, source, segment match, warmth score, next action, channel), then a "First customer" section naming #1 with the reason and the exact opening message for Day 5. `04-gtm/prospect-ranking.csv` sits alongside as raw data. Every name is real. If you only have 6, show 6 and flag the gap.

## Done when
`04-gtm/gtm-plan.md` lists up to 10 named prospects ranked by warmth, each has one next action with a named channel, and #1 is named with a one-sentence reason and a drafted opening message.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-gtm-plan \
  --artefact 04-gtm/gtm-plan.md \
  --result "10 prospects ranked, #1 handed to Day 5"
```

Set the outcome (not complete; checkpoint closes the day after d4-book-sale):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"10 ranked, #1 chosen"}}}'
```

## If it goes wrong
If the ranker finds fewer than 10, do not invent names. Widen the funnel: post the landing page in one more place, message two uncontacted interviewees, re-run tomorrow before Day 5. If a source file is missing, the script names it and ranks on what remains.
