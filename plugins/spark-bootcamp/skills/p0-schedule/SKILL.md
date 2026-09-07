---
name: Track Your Interview Schedule
description: Turns replies into a booked Monday interview schedule. Run it whenever replies land: it logs each yes, assigns a slot, queues the chase, and counts you to 8.
when_to_use: Pre-work, after invitations go out. Re-run each time replies arrive, until 8 to 12 interviews are booked and pre-work closes.
---

# Track Your Interview Schedule

**What this does.** Keeps the one live picture of your bootcamp Monday: who is booked and when, who is thinking, who has gone quiet, and how far you are from 8.
**Why it matters.** Replies trickle in over weeks and memory is a bad diary. Eight or more booked conversations before the bootcamp starts is what makes Day 1 work.
**You are ready for this when.** `00-prework/invitation-pack.md` exists and at least one invitation has been sent.

## Before you start
Read `.spark/state.json` (`prework.bootcamp_monday`, `prework.interviews_booked`), `00-prework/interview-schedule.md` if it exists, and `00-prework/invite-list.csv` for reserves. Ask the founder what has come in since last time; paste replies if easier. Guardrail: you draft confirmations and chases, the founder sends them.

Interviews already booked outside the plugin, from a workpack? Skip straight here even if the earlier pre-work artefacts do not exist yet: ask who is booked and when, write the schedule from that, and log it. Backfill `p0-interview-triage` and `p0-invite-list` after, in ten minutes, only so `coach` and later skills have the full record.

## Steps
1. For each yes: agree a 25-minute slot on the bootcamp Monday afternoon or the Tuesday morning overflow, with 10+ minutes between slots. Cap Monday at 8 slots; from the ninth yes, book Tuesday morning by default (the day only holds so many honest conversations). Add the row: name, role, channel, confirmed time, format (call or in person), status BOOKED.
2. Draft the confirmation with the exact time, the format and the joining detail. Founder sends it.
3. For each maybe: record what they need (a different time, more context) and draft the reply.
4. For silence: at 4 to 5 working days queue follow-up one from the invitation pack; a week later, follow-up two; after that, mark LAPSED and pull the next warmest reserve from the invite list into a fresh invitation.
5. Update the tally in state every run (see Log it). Read the founder the number: "You are at 6 of 8".
6. At 8 or more booked, close pre-work: set `prework.complete` to true, congratulate them, and point at `/spark-bootcamp:coach` for what Day 1 will look like.
7. One week out with fewer than 8: escalate together. More invitations from reserves, the Digital Jersey shared interviewee pool, or widen geography. Accepting 5 to 7 is a conscious call the founder makes, logged in DECISIONS.md. Under 5, pre-work stays open: Day 1 cannot validate on anecdotes.

## The artefact
Writes `00-prework/interview-schedule.md` using `${CLAUDE_SKILL_DIR}/references/schedule-template.md`: the booked-slot table (time, name, role, channel, format, status), the tally against target, the waiting list with next action per name. Good: the founder could run Monday from this page alone.

## Done when
1. Every reply received is reflected in the schedule with a status.
2. Every BOOKED row has a confirmed time on the bootcamp Monday (or Tuesday morning) and a format.
3. `prework.interviews_booked` in state matches the BOOKED count.
4. Pre-work closes only at 8+, or at 5 to 7 by a logged founder decision.

## Log it
On each material update:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill p0-schedule \
  --artefact 00-prework/interview-schedule.md \
  --result "<N> of <target> interviews booked"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"prework":{"interviews_booked":<N>}}'
```
When closing pre-work, patch `{"prework":{"interviews_booked":<N>,"complete":true}}` instead and record the decision if under 8.

## If it goes wrong
A booked name cancels: thank them, offer the overflow window, and pull a reserve regardless. Everyone books Tuesday and Monday is empty: fine, the interviews matter more than the day; tell the coach the plan shifted by noting it in DECISIONS.md. The founder froze and sent nothing: do not scold, pick the three hottest names and get those three messages out today.
