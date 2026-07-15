---
name: Plan Usability Tests
description: Turns your interview engine into a usability and buying-signal test, then books 5 sessions against the live MVP. Use on Day 4 once the MVP is live and you have testers lined up.
when_to_use: Day 4 go-to-market, straight after the MVP is deployed. Reuses the Thursday testers you recruited on Day 1. Run this before any test session happens.
---

# Plan Usability Tests

**What this does.** Rewrites your Day 1 interview approach into a usability test against the live MVP: real tasks a person attempts on the URL, plus three probes that read whether they would actually pay. Then it books 5 sessions.
**Why it matters.** On Day 1 you asked people about a problem. Now you have a thing, so the question changes. You are no longer testing whether the pain is real, you are testing whether your build removes it and whether removing it is worth money to them. Watching five real people fumble your MVP for 30 minutes will teach you more than reading fifty survey answers. And the buying-signal probes stop you mistaking politeness for demand.
**You are ready for this when.** The MVP is live on a public URL (recorded in `.spark/state.json` day 3 outcome and `03-product/BUILD-LOG.md`), and `03-product/story-map.md` exists.

## Before you start
Read these, in order:
- `.spark/state.json`: your `founder` name, `business_type`, and the day 3 outcome, which holds the live MVP URL. That URL is the thing every task runs against.
- `03-product/story-map.md`: the backbone click-path and the acceptance criteria. Your test tasks come straight off this. If the story map says "land, see offer, give one input, see result, leave payment intent", those steps are your tasks.
- `01-discovery/interview-list.csv` and `01-discovery/outreach-pack.md`: the testers you flagged on Day 1 (the ones who said yes to looking at what you build on Thursday) and the running tester tally. These are the five people you book. You recruited them four days ago for exactly this moment.

Guardrail, read it twice: **you contact testers, but nothing goes out until you approve it.** This skill drafts the booking messages and stops. It never sends on its own and it never spends money. Confirming a booking means a real person has replied yes to a real slot, not that you posted a message into the void.

## Steps
1. **Reframe the goal in one line.** Write it at the top of the plan: "Can a first-time user complete the core action on [URL] without me, and would they pay for it?" Everything in the test serves that sentence. If a task or a question does not, cut it.
2. **Turn the backbone into tasks.** Take the story-map backbone and write at least 4 tasks as things to attempt, not questions to answer. "Book a valuation" beats "what do you think of the booking flow?". Each task names a starting point on the URL, the action, and the observable success condition (the same acceptance criteria you already wrote on Day 3). Order them the way a real user would move.
3. **Write the three buying-signal probes.** These are the sharp bit. A polite "this is nice" is worthless. You want signals that cost the tester something to give. Use the three in `${CLAUDE_SKILL_DIR}/references/task-and-probe-bank.md`: a price-reaction probe, a switch-cost probe, and a commitment probe (the one that asks for a small real action now). Adapt the wording to your idea and business path. Do not add a fourth to soften them.
4. **Set the observation rules.** One line each: you watch, you do not rescue. Ask them to think aloud. Time each task. Note the first point they hesitate, because that is your worst friction. Silence while they struggle is the most useful 20 seconds of the session.
5. **Book 5 sessions of 30 minutes.** Pull your flagged testers from the tester tally. Message them with a specific slot inside the next 48 hours (a scheduling link or two concrete times, same method you chose on Day 1). Five is the number: fewer than 5 and one no-show wrecks your read, more than 5 in a day and you will not synthesise them before Day 5. Draft every message, then stop for sign-off before sending.
6. **Draft the invites with the helper.** Once approved, run the helper to turn the plan's booking table into a ready-to-send message for each tester. It never sends and never spends, and it saves a copy next to the plan:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/book-sessions.py 04-gtm/tests/usability-test-plan.md --founder "[your name]" --url "[live MVP URL]"
   ```

   If the plan or its booking table is not filled in yet, the helper prints a blank template rather than crashing.
7. **Track confirmations.** A booking is confirmed only when the tester has said yes to a specific time. Keep the count in the plan. You need 5 confirmed within 48 hours. If a flagged tester goes cold, go to the next name on the list rather than waiting.

## The artefact
Writes `04-gtm/tests/usability-test-plan.md` in Markdown, using `${CLAUDE_SKILL_DIR}/references/usability-test-plan-template.md` as the structure. Sections in order: the one-line goal; the live URL under test; the task list (4 or more, each with start point, action, success condition); the three buying-signal probes; the observation rules; and a booking table with one row per tester (name, channel, proposed slot, status: drafted / sent / confirmed) plus a confirmed count.

What good looks like: a colleague could run a session from this plan without asking you a thing, every task has an observable pass or fail, the three probes each cost the tester something to answer, and the booking table shows 5 confirmed.

## Done when
5 sessions are confirmed within 48 hours (5 rows marked confirmed in the booking table), the plan holds 4 or more tasks each with an observable success condition, and exactly 3 buying-signal probes are written. Count all three before you log.

## Log it
Append one line to CHANGELOG.md via the logbook helper:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-usability-plan \
  --artefact 04-gtm/tests/usability-test-plan.md \
  --result "5 sessions confirmed, 4 tasks, 3 buying-signal probes"
```

Then update `.spark/state.json` via the journey-state helper, recording day 4 progress and the confirmed-session count as the outcome:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"current_day": 4, "days": {"4": {"target": "5 usability sessions booked against the live MVP", "outcome": "5 sessions confirmed", "complete": true}}}'
```

The logbook helper registers the artefact in state.json for you. If you changed the booking method or dropped a task, note why in DECISIONS.md via the logbook `--decision`/`--rationale` mode.

## If it goes wrong
If you cannot get 5 confirmed in 48 hours, do not stall the week. Book what you can (3 is a working floor), run those, and keep the remaining slots open for walk-up recruits from Day 4 outreach. If your Day 1 testers have gone quiet, that is a signal in itself: the follow-up line from your outreach pack, sent once, usually recovers two of them. If nobody bites at all, run one session with a colleague as a rehearsal so your tasks and probes are sharp before the real ones land, then treat the first real tester as your fifth.
