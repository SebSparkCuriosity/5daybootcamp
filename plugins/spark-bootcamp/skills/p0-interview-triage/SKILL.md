---
name: Triage Your Interviewees
description: A short working conversation that decides who you will interview on bootcamp Monday: one segment, the exact role, 8 to 12 people, three screening questions.
when_to_use: Pre-work, 2 to 4 weeks before the bootcamp Monday, straight after start, before building the invite list.
---

# Triage Your Interviewees

**What this does.** Talks the interview target out of you: one segment, the exact role (and the buyer if different), a number between 8 and 12, and three screening questions.
**Why it matters.** Diaries fill weeks ahead, so you invite people now, long before the idea is fully developed. The right ten conversations are worth more than fifty random ones.
**You are ready for this when.** `.spark/state.json` exists with `idea` filled (run `start` first).

## Before you start
Read state for `founder`, `idea` and `prework.bootcamp_monday`. This is a conversation, not a form (about 30 minutes): ask one question at a time, listen, and capture the founder's own words. It is a light triage, good enough to invite the right people; the deep idea work happens on Day 1.

Already worked this out on paper, from a workpack or your own notes? Good, this goes in minutes: read back what you have, tighten anything vague against the steps below, and write it. Skip nothing, but do not re-litigate a call already made.

## Steps
1. Ask who they picture when they imagine the idea working. Push from category to person: not "small businesses" but "the office manager at a 15-person Jersey trust company". Their answer names the segment: "people who [do this job] at [this kind of place]".
2. Ask for the exact job title of the person who feels the pain. "Head of compliance", not "someone in compliance". If they are unsure, ask who they last saw struggle with it.
3. Ask who would sign the invoice. If pain and payer differ, note both; you need to hear from both, which changes the number.
4. Propose a number between 8 and 12 with a reason, then ask if it fits their reach. Under 5 is anecdote; over 15 leaves no time to synthesise. If pain and payer differ, split it (e.g. 8 users plus 3 buyers).
5. Draft three screening questions together, each answerable in the first two minutes of a call. At least one must be able to return a "no". Test them on the founder: would their last real example pass?
6. Ask the kill question: "if this idea dies, who would have killed it?" If the people just named cannot prove or kill the idea, change the target now, out loud, and say why.
7. Read the whole spec back and get an explicit yes before writing it.

Do not branch by business type. Software, hardware and services founders all need the same right humans in the room.

## The artefact
Writes `00-prework/interview-target-spec.md` using `${CLAUDE_SKILL_DIR}/references/interview-target-spec-template.md`. A stranger could read it and know within ten seconds whether the person across from them qualifies.

## Done when
1. Segment and exact role both named, in words the founder agreed to.
2. Target number stated with a reason.
3. Three screening questions written, at least one able to disqualify.
4. The founder has said yes to the read-back.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill p0-interview-triage \
  --artefact 00-prework/interview-target-spec.md \
  --result "target: <N> interviews"
```

## If it goes wrong
If the idea serves two very different buyers, do not average them. Talk both through, pick the one whose "no" would hurt the idea most, and park the second at the bottom of the spec. If the founder cannot see 8 reachable people on-island, widen the place (Jersey to Channel Islands, or UK) before the role, and record it in DECISIONS.md with a one-line rationale.
