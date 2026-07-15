---
name: Go-To-Market Plan
description: Names your first 10 customers, ranks them by warmth, gives each a next action, and hands #1 to Day 5. Use on Day 4 once you have buying signals and landing captures.
when_to_use: Day 4 GTM, after the landing page is live and the buying-signal scorecard exists, before Day 5's first sale. Trigger phrases, "who do I sell to first", "who is my first customer", "build my prospect list".
---

# Go-To-Market Plan

**What this does.** Turns your scattered signals into one ranked list of 10 named people, warmest first, each with a single next action, and hands the warmest one straight to Day 5.
**Why it matters.** By Day 4 you have interest from three places: people who scored well in interviews, people who filled in your landing page, and your own scorecard. On their own they are noise. Ranked by warmth, they become a queue you work top to top down. The warmest prospect closes far faster than a cold one, so you start there, not at the top of an alphabet.
**You are ready for this when.** `04-gtm/buying-signal-scorecard.csv` exists and your landing page has been live long enough to capture at least a few real visitors.

## Before you start
Read these three inputs (the script pulls them for you, but know what they are):

- `04-gtm/buying-signal-scorecard.csv`: your scored signals from Day 3.
- The landing capture store: whoever filled in your Day 4 page. For software and services this is usually `04-gtm/landing-captures.csv`; for hardware it is your pre-order or waitlist export, same path. If your capture lives in Supabase or a form tool, export it to that CSV first.
- `01-discovery/interviews/` or `01-discovery/interview-notes.md`: the interviewees you tagged with a strong buying signal on Day 1.

Guardrail: this skill plans outreach. It does not send anything. No message goes out and no money is spent until Day 5, and only after you say yes.

## Steps
1. Run the ranker. It merges the three sources, de-duplicates by name and email, and scores each person's warmth 0 to 100:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/rank_prospects.py
   ```

   It reads the paths above and writes a draft table to `04-gtm/prospect-ranking.csv`. If a source is missing it says so and carries on with what it has.

2. Understand the warmth score so you can trust it or overrule it. Warmth rewards three things: they showed intent (paid a deposit, booked a call, asked "when can I buy"), they match your target segment exactly, and they engaged more than once. The formula lives in `references/warmth-model.md`. A deposit or booked call beats a mailing-list sign-up every time.

3. Cut the list to exactly 10. Fewer than 10 and Day 5 runs dry if the first few say no. More than 10 and you spread yourself thin in a single week. If the ranker found fewer than 10 real people, that is your finding: your top of funnel is too narrow, and fixing that matters more than a tidy list. Note it and carry the shorter list.

4. Give every one of the 10 a single next action. Not three. One. The action names the channel and the ask: "Email Priya, reference the deposit she left, offer a 20 minute call this week." A next action with no channel and no ask is a wish, not a plan.

5. Branch the next action by path, because warmth means different things:

   ## For software
   Warmest are people who used the deployed slice and hit its limit. Next action, book a call and offer to switch on the paid tier for them live.

   ## For hardware
   Warmest are people who left a real deposit or pre-order. Next action, confirm the deposit, give a ship or demo date, ask for the balance or the next commitment.

   ## For services
   Warmest are people who booked an intake slot or replied to the sample deliverable. Next action, send the one-page proposal with the fixed price and a start date.

6. Pick #1 and write down why in one sentence. This is the person Day 5 opens with. Warmest score usually wins, but if a slightly cooler prospect is a faster yes (they hold the budget, they replied today), promote them and record the reason in `DECISIONS.md`.

## The artefact
Writes `04-gtm/gtm-plan.md` in Markdown. Good looks like: a ranked table of 10 (rank, name, source, segment match, warmth score, next action, channel), then a short "First customer" section naming #1 with the one-sentence reason and the exact opening message you will send on Day 5. The supporting `04-gtm/prospect-ranking.csv` sits alongside it as the raw ranked data.

Every name is a real person from a real source. Never pad the list with invented prospects. If you only have 6, the plan shows 6 and flags the gap.

## Done when
`04-gtm/gtm-plan.md` lists up to 10 named prospects ranked by warmth score, every prospect has one next action with a named channel, and #1 is named with a one-sentence reason and a drafted opening message ready for Day 5.

## Log it
Append one line to CHANGELOG.md via the logbook helper, with the number of ranked prospects as the numeric result:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-gtm-plan \
  --artefact 04-gtm/gtm-plan.md \
  --result "10 prospects ranked, #1 handed to Day 5"
```

Then update state via the journey-state helper: set `days.4.outcome` to the count. Do not set `complete` here; the day is closed by checkpoint after d4-book-sale.

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"10 ranked, #1 chosen"}}}'
```

If you promoted a cooler prospect to #1, record the why in DECISIONS.md.

## If it goes wrong
If the ranker finds fewer than 10 people, do not invent names. Widen the funnel instead: post the landing page in one more place today, message two interviewees you have not contacted, and re-run the ranker tomorrow morning before Day 5. A shorter honest list beats a padded one. If a source file is missing entirely, the script tells you which one and ranks on what remains, so you still get a usable queue.
