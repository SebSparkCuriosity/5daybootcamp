---
name: Plan Usability Tests
description: Turns your Day 1 interview into a usability and buying-signal test against the live MVP, then books 5 sessions. Day 4.
when_to_use: Day 4 go-to-market, straight after the MVP deploys. Run before any test session happens.
---

# Plan Usability Tests

**What this does.** Rewrites your Day 1 interview into a usability test against the live MVP: real tasks on the URL plus three probes reading whether they would pay, then books 5 sessions.
**Why it matters.** You now have a thing, so the question changes from "is the pain real?" to "does my build remove it, and is that worth money?", and watching five people fumble it teaches you more than fifty surveys.
**You are ready for this when.** The MVP is live on a public URL (in `.spark/state.json` day 3 outcome and `03-product/BUILD-LOG.md`) and `03-product/story-map.md` exists.

## Before you start
Read: `.spark/state.json` (`founder`, `business_type`, day 3 outcome with the live MVP URL, every task runs against it); `03-product/story-map.md` (backbone click-path and acceptance criteria, your tasks come off these); `00-prework/invite-list.csv` and `00-prework/invitation-pack.md` (the testers who said yes in pre-work, the five you book).

Two quick questions before drafting (5 minutes): what is the one thing the founder most wants to learn from watching people tomorrow, and which five names from the tester tally do they trust to show up? Their answers shape the tasks and the bookings.

Guardrail: **you contact testers, but nothing goes out until you approve it.** This skill drafts booking messages and stops. It never sends and never spends. A confirmed booking means a real reply to a real slot.

## Steps
1. **Reframe the goal in one line** at the top: "Can a first-time user complete the core action on [URL] without me, and would they pay?" Cut anything that does not serve it.
2. **Turn the backbone into tasks.** Write 4 or more tasks as things to attempt, not questions ("Book a valuation", not "what do you think?"). Each names a start point on the URL, the action, and an observable success condition (your Day 3 acceptance criteria). Order them as a real user would move.
3. **Write the three buying-signal probes.** Use the price-reaction, switch-cost and commitment probes in `${CLAUDE_SKILL_DIR}/references/task-and-probe-bank.md`. Adapt wording to your idea and path. Do not add a fourth to soften them.
4. **Set observation rules.** One line each: watch, do not rescue; think aloud; time each task; note the first hesitation, that is your worst friction.
5. **Book 5 sessions of 30 minutes.** Pull flagged testers from the tally. Message each a specific slot in the next 48 hours (same method as Day 1). Five is the number: fewer and a no-show wrecks the read, more and you cannot synthesise before Day 5. Draft, then stop for sign-off before sending.
6. **Draft the invites with the helper** once approved. It turns the booking table into ready-to-send messages, never sends or spends, saves a copy by the plan:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/book-sessions.py 04-gtm/tests/usability-test-plan.md --founder "[your name]" --url "[live MVP URL]"
   ```

7. **Track confirmations.** Confirmed only when the tester says yes to a specific time. You need 5 within 48 hours. If a tester goes cold, move to the next name.

## The artefact
Writes `04-gtm/tests/usability-test-plan.md` in Markdown, structured on `${CLAUDE_SKILL_DIR}/references/usability-test-plan-template.md`: one-line goal; live URL; task list (4+, each with start point, action, success condition); three buying-signal probes; observation rules; booking table (name, channel, slot, status: drafted/sent/confirmed) plus a confirmed count. Good: a colleague could run a session unaided.

## Done when
5 sessions confirmed within 48 hours (5 rows marked confirmed), 4 or more tasks each with an observable success condition, and exactly 3 buying-signal probes. Count all three before you log.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-usability-plan \
  --artefact 04-gtm/tests/usability-test-plan.md \
  --result "5 sessions confirmed, 4 tasks, 3 buying-signal probes"
```

Then update `.spark/state.json`:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"5 usability sessions confirmed"}}}'
```

If you changed the booking method or dropped a task, note why in DECISIONS.md via the logbook `--decision`/`--rationale` mode.

## If it goes wrong
Cannot get 5 in 48 hours? Book what you can (3 is a working floor), run those, keep the rest open for walk-up recruits from Day 4 outreach. If Day 1 testers went quiet, the follow-up line from your outreach pack, sent once, usually recovers two. If nobody bites, rehearse one session with a colleague to sharpen tasks and probes, then treat the first real tester as your fifth.
