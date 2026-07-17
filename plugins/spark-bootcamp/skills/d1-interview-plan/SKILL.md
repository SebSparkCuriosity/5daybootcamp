---
name: Plan The Interview Day
description: Turns your booked schedule and developed idea into this afternoon's run plan: who you meet, when, what each conversation must test, and the day's number.
when_to_use: Day 1 mid-morning, after d1-refine-idea, before the script. The interviews were booked in pre-work; this plans how to run them.
---

# Plan The Interview Day

**What this does.** Walks through today's booked interviews with you, one name at a time, and agrees what each conversation is for. Ends with a run plan and one number for the day.
**Why it matters.** You booked these people weeks ago, before the idea was developed. Ten minutes per name now is what turns a diary of calls into a test of your riskiest assumption.
**You are ready for this when.** `01-discovery/idea-brief.md` exists and `00-prework/interview-schedule.md` holds booked slots.

## Before you start
Read `01-discovery/idea-brief.md` (the riskiest assumption above all), `00-prework/interview-schedule.md` and `00-prework/interview-target-spec.md`. This is a conversation: discuss each booked name with the founder rather than deciding for them. Guardrail: do not cancel anyone on the day; a same-day cancellation burns goodwill you will want on Thursday.

## Steps
1. Check fit together. For each booked name, ask the founder: does this person still clear the three screening questions against this morning's sharpened idea? Mark each KEEP, REWEIGHT (still useful, different emphasis) or MISMATCH (run it anyway, as learning about the adjacent segment).
2. Agree one focus per person: the assumption from the brief this conversation is best placed to test, plus one true thing the founder knows about them to open with.
3. Confirm logistics out loud: times, format, joining links, 10+ minute buffers, and where notes will live. The recording method comes next in `d1-write-script`; leave a slot for it.
4. Set the day's number with the founder: N booked, hold at least N minus 2, and 5 held is the floor tonight's synthesis needs. Get an explicit yes to the number.
5. If fewer than 8 are booked, list who to chase at lunch from the reserves in `00-prework/invite-list.csv`, hottest first.
6. Read the plan back and write it.

## The artefact
Writes `01-discovery/interview-plan.md`: the run table (time, name, role, format, fit verdict, focus assumption, opener), the day's number, and the lunch chase list if needed. Good: the founder could run the afternoon from this one page with their phone on silent.

## Done when
1. Every booked slot has a fit verdict, one focus assumption and an opener.
2. The day's number is stated with the founder's yes: "N booked, hold at least N-2, floor 5".
3. Logistics confirmed for every slot.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-interview-plan \
  --artefact 01-discovery/interview-plan.md \
  --result "<N> interviews planned for today"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"1":{"target":"hold <N-2>+ of <N> booked interviews, floor 5"}}}'
```

## If it goes wrong
Half the schedule turned MISMATCH because the idea moved this morning: run them anyway and add two questions about the new direction; real people beat a perfect sample. Someone cancels before lunch: offer tomorrow's overflow window, pull a reserve, and adjust the number honestly rather than quietly. Nothing booked at all: pre-work slipped; spend the afternoon on warm phone calls from the invite list and log the true count tonight.
