---
name: Define Your Interviewees
description: Decide who to interview, their exact role, and how many, before writing a single message. Day 1, after refining the idea.
when_to_use: Day 1 discovery, after d1-refine-idea, before building the contact list.
---

# Define Your Interviewees

**What this does.** Turns your idea brief into a precise interview target: one segment, the exact role (and the buyer if different), a number between 8 and 12 with a reason, and three screening questions.
**Why it matters.** The right ten conversations are worth more than fifty random ones, and everything downstream points at whoever you pick here.
**You are ready for this when.** `01-discovery/idea-brief.md` exists.

## Before you start
Read `01-discovery/idea-brief.md`, especially the riskiest assumption you flagged. That assumption decides who to talk to. No brief yet? Run d1-refine-idea first. This skill only decides and writes it down: no outreach, nothing to sign off.

## Steps
1. Name ONE segment as "people who [do this job] at [this kind of place]". Narrow beats broad.
2. Name the exact job title, not the department. "Head of compliance", not "someone in compliance".
3. Separate pain from payer. Note both. If they differ, you must talk to both, which changes your number.
4. Set the number, 8 to 12. Under 5 is anecdote; over 15 leaves no time to synthesise before Day 2. Write it with a one-sentence reason. If pain and payer differ, split it (e.g. 8 users plus 3 buyers).
5. Write three screening questions that confirm someone is in your segment, each answerable in the first two minutes. At least one must be able to return a "no".
6. Sanity-check against the riskiest assumption. If these exact people cannot prove or kill it, change the target now.

Do not branch by business type. Software, hardware and services founders all need the same right humans on Day 1.

## The artefact
Writes `01-discovery/interview-target-spec.md` using `${CLAUDE_SKILL_DIR}/references/interview-target-spec-template.md`. A stranger could read it and know within ten seconds whether the person across from them qualifies.

## Done when
1. Segment and exact role both named.
2. Target number stated with a reason.
3. Three screening questions written, at least one able to disqualify.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-define-interviewees \
  --artefact 01-discovery/interview-target-spec.md \
  --result "target: <N> interviews"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"1":{"target":"define interviewees","outcome":"target: <N> interviews","complete":true}}}'
```

## If it goes wrong
If the idea serves two very different buyers, do not average them. Pick the one that best tests your riskiest assumption, and park the second at the bottom of the spec. If you cannot find 8 people on-island, widen the place (Jersey to Channel Islands, or UK) before the role, and record it in DECISIONS.md with a one-line rationale.
