---
name: Define Your Interviewees
description: Decide exactly who to interview, what role they hold, and how many, before you write a single message. Use on Day 1 after refining the idea.
when_to_use: Day 1 discovery, straight after d1-refine-idea, before building the contact list.
---

# Define Your Interviewees

**What this does.** Turns your idea brief into a precise interview target: one segment, the exact role to speak to (and the buyer, if that is a different person), a number between 8 and 12 with a reason, and three screening questions.
**Why it matters.** Most first-time founders interview the wrong people and get warm, useless answers. The right ten conversations are worth more than fifty random ones. Get this right and everything downstream, the market map, the proposition, the sale, points at real buyers.
**You are ready for this when.** `01-discovery/idea-brief.md` exists.

## Before you start
Read `01-discovery/idea-brief.md`, and in particular the riskiest assumption you flagged in it. That assumption decides who you must talk to. If there is no idea brief yet, stop and run d1-refine-idea first.

One guardrail: this skill only decides who to talk to and writes it down. It does not contact anyone. No outreach happens here, so there is nothing to sign off yet.

## Steps
1. Name the ONE segment you are testing first. Not three. One. Write it as "people who [do this job] at [this kind of place]". Example: "operations managers at Jersey fund administrators with 20 to 80 staff". Narrow beats broad. You can widen later; you cannot un-blur a fuzzy answer.

2. Name the exact role. Be specific about the job title, not the department. "Head of compliance", not "someone in compliance".

3. Separate the pain from the payer. The person who feels the problem is often not the person who signs the invoice. Note both. If they are the same person, say so. If they differ, you will need to talk to both, and that changes your number.

4. Set the number. Aim for 8 to 12 interviews. Fewer than 5 and you are guessing off anecdotes; more than 15 in a week and you will not have time to synthesise them before Day 2. Write the number down with its reason in one sentence. If pain and payer differ, split the number (for example, 8 users plus 3 buyers).

5. Write three screening questions that confirm someone is genuinely in your segment before you spend a slot on them. Each one should have a right answer you can hear in the first two minutes of a call. A good screen disqualifies people, so make at least one question capable of a "no".

6. Sanity-check against the riskiest assumption. Will these exact people be able to prove or kill that assumption? If the honest answer is no, change the target now, before you build the contact list. This is the whole point of the exercise.

Do not branch by business type here. Software, hardware and services founders all need the same thing on Day 1: the right humans to talk to. The path only changes what you build later, not who you learn from now.

## The artefact
Writes `01-discovery/interview-target-spec.md` in Markdown, using the template at `${CLAUDE_SKILL_DIR}/references/interview-target-spec-template.md`. It contains: the one segment, the exact role, the buyer (marked "same as user" or named separately), the target number with its one-sentence reason, and the three screening questions.

What good looks like: a stranger could read the spec and know within ten seconds whether the person sitting across from them qualifies. The segment names a job and a place. The number has a reason, not just a figure. At least one screening question can return a "no".

## Done when
Three conditions, all observable in the file:
1. The segment and the exact role are both named.
2. The target number is stated with a reason (a number and a because, in one sentence).
3. Three screening questions are written, and at least one can disqualify a person.

## Log it
Append one line to CHANGELOG.md via the logbook helper, recording the artefact path and the target number:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-define-interviewees \
  --artefact 01-discovery/interview-target-spec.md \
  --result "target: <N> interviews"
```

The log.py call above already registers the artefact in `.spark/state.json`, so no separate state update is needed for it. To record Day 1 progress, use the journey-state helper with a merge patch:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"days":{"1":{"target":"define interviewees","outcome":"target: <N> interviews","complete":true}}}'
```

Never edit `.spark/state.json` by hand. Always go through the helper so a skill running alongside this one cannot clobber the file.

## If it goes wrong
If you cannot name a single segment because the idea genuinely serves two very different buyers, do not average them into a mush. Pick the one that best tests your riskiest assumption this week, write it down, and note the second segment as "parked for later" at the bottom of the spec. One clear target beats two blurry ones.

If you cannot find 8 people in your chosen segment on the whole island, that is a finding, not a failure. Widen the place (Jersey to the Channel Islands, or to the UK) before you widen the role, and record the change in DECISIONS.md with a one-line rationale.
