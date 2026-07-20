---
name: Write Your Interview Script
description: Co-writes a Mom Test-proof discovery script with you (8+ non-leading, past-behaviour questions) plus a how-to-run guide, and picks a recording method.
when_to_use: Day 1, after d1-interview-plan, before the first booked call. Last prep before the afternoon interviews.
---

# Write Your Interview Script

**What this does.** Drafts the discovery script with you, question by question: eight or more questions that cannot be flattered, in your own voice, plus a guide for running, recording and transcribing the call.
**Why it matters.** A good script is the difference between ten conversations that prove or kill your idea and ten that leave you where you started. A question in your own voice survives a nervous first call; a perfect one in someone else's does not.
**You are ready for this when.** `01-discovery/interview-plan.md` exists.

## Before you start
Read `01-discovery/idea-brief.md` (especially the riskiest assumption) and `01-discovery/interview-plan.md`. Load the craft from `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/`: `mom-test.md` (compulsory) and `jtbd.md` (shapes the arc). This is co-writing, not ghost-writing (about 30 minutes): for each area, ask what the founder most wants to learn, draft together, and keep their phrasing wherever it passes the test.

## Steps
1. Read the Mom Test rule that matters: ask for specifics in the past, never generics about the future. Say it to the founder in one line before drafting anything.
2. Scaffold both files from your project root:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/scaffold.py" --root .
   ```
   This writes `01-discovery/interview-script.md` and `01-discovery/how-to-run.md` with traps removed. If it fails, copy the templates from `${CLAUDE_SKILL_DIR}/references/` by hand.
3. Work the four areas in order: how they do the job today; the last time the problem bit and what it cost; what they have tried or paid for; who else is in the decision. For each, ask the founder "what do you most need to hear about this?", draft two or three questions together, and test every one against the Mom Test as a pair. If it can be answered "yes" or "sounds good", rewrite it together using the fix column in `mom-test.md`.
4. Point at least two questions straight at the riskiest assumption from the brief. Facts, not opinions. Say which two they are.
5. Keep the founder's wording wherever it survives the test. Eight or more questions total, all about their past and their world.
6. Do not branch by business type. Software, hardware and services founders run the same discovery call.
7. Co-write `how-to-run.md`: how to open (thank, set time, ask consent to record, promise no selling), how to avoid pitching, how to record and transcribe, how to close (ask who else, and whether you can return). Have the founder say the opening out loud once; tighten what stumbles.
8. Choose one recording default together: online calls use the platform's own recording and auto-transcript (Meet, Zoom, Teams, free, with consent); in person use a phone voice memo plus a free transcriber; if the interviewee declines, notes only, filled straight after. Write the choice into `how-to-run.md` and the slot left in the interview plan.

## The artefact
Two Markdown files. `01-discovery/interview-script.md`: opening lines, eight or more past-behaviour questions grouped by the four areas, closing questions. `01-discovery/how-to-run.md`: how to open, how to avoid pitching, one named recording method, how to close. A nervous first-timer could run a clean call from it cold, in their own voice.

## Done when
1. `interview-script.md` holds eight or more questions, every one about the past or current behaviour, not a hypothetical.
2. `how-to-run.md` names one recording and transcription method as the default.
3. At least two questions point at the riskiest assumption, and the founder can say which.
4. The founder has read the opening aloud once.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-write-script \
  --artefact 01-discovery/interview-script.md \
  --result "<N> non-leading questions, recorder chosen"
```

## If it goes wrong
If the references or templates will not load, do not stall: the method is one line, ask about the past, in specifics, without pitching. Draft your eight against that together and note the reference could not be read. Stuck at five questions? Put the idea away and ask what this person actually did last month that touches the problem. If a prospect gives you only fifteen minutes, cut to your best five aimed at the riskiest assumption and note the trim in DECISIONS.md.
