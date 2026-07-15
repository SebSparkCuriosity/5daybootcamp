---
name: Write Your Interview Script
description: Writes a Mom Test-proof discovery script (8+ non-leading, past-behaviour questions) plus a how-to-run guide, and picks one recording and transcription method. Use on Day 1 after defining who to interview.
when_to_use: Day 1 discovery, straight after d1-define-interviewees and before d1-build-list and run-interview. This is the last thing you prepare before you start booking calls.
---

# Write Your Interview Script

**What this does.** Turns your interview target into two ready-to-use files: a discovery script with eight or more questions that cannot be flattered, and a short guide for running the call, recording it, and turning it into a transcript.
**Why it matters.** A good script is the difference between ten conversations that kill or prove your idea and ten that leave you exactly where you started. Ask about the future and people are kind and wrong. Pitch, and the honest answers stop. This skill bakes the Mom Test into the questions themselves, so the discipline is on the page and not just in your head. It also settles the boring-but-fatal question of how you capture the call, because a conversation you cannot remember is a conversation you did not have.
**You are ready for this when.** `01-discovery/interview-target-spec.md` exists.

## Before you start
Read these first:
- `01-discovery/idea-brief.md`, and in particular the riskiest assumption you flagged. Your best questions attack that assumption directly.
- `01-discovery/interview-target-spec.md`, so the questions fit the exact role you decided to speak to.
- The craft in `interview-method`: `mom-test.md` is compulsory, `jtbd.md` shapes the arc of the conversation. Load them via `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/`.

If `interview-target-spec.md` does not exist, stop and run d1-define-interviewees first. You cannot write good questions for a person you have not named.

One guardrail: this skill only writes files. It contacts nobody and spends nothing, so there is nothing to sign off yet. Sign-off comes when you send outreach, not now.

## Steps
1. Read the Mom Test rules until you can say the one that matters out loud: ask for specifics in the past, never generics about the future. Every question you write is tested against that rule.

2. Scaffold the two files. Run from your project root:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/scaffold.py" --root .
   ```
   This writes `01-discovery/interview-script.md` and `01-discovery/how-to-run.md` from the templates, with slots to fill and every leading-question trap already removed. If the script cannot run, copy the templates from `${CLAUDE_SKILL_DIR}/references/` by hand.

3. Write eight or more questions, all about their past and their world, none about your idea. Use the fix column in `mom-test.md` as your pattern. Every question must be answerable with a story, not a yes. A quick test: if the question can be answered "yes" or "sounds good", rewrite it. "When did you last try to solve X, and what did you do?" is a keeper. "Would you use a tool that did X?" is not, so bin it.

4. Cover the four things a discovery call must surface, in this order: how they do the job today, the last time the problem bit and what it cost them, what they have already tried or paid for, and who else is involved in the decision. That last one finds the buyer when the buyer is not the person in front of you.

5. Point at least two questions straight at your riskiest assumption. If the assumption is "trust officers spend hours reconciling by hand", ask "walk me through the last reconciliation you did, start to finish" and "how long did that take you". Facts, not opinions.

6. Do not branch by business type. Software, hardware and services founders all run the same discovery call on Day 1: understand the problem before you build anything. The path only changes what you build on Day 3, not what you ask this week.

7. Write the how-to-run guide, covering four moments: how to open (thank them, set the time, ask for consent to record, promise you are not selling), how to avoid pitching (keep your idea in your pocket, turn "what are you building?" back to them), how to record and transcribe (see below), and how to close (ask who else you should talk to, and whether you can come back).

8. Choose your recording method now, not on the call. The recommendation: record the call and paste the transcript into run-interview. That keeps your hands free to listen. Use one method as your default:
   - For online calls, turn on the meeting platform's own recording and auto-transcript (Google Meet, Zoom or Teams all do this free, with the person's consent). It is free, consented in one click, and the transcript lands in your files.
   - For in-person calls, record on your phone's voice memo app and run the audio through a free transcription tool afterwards.
   - If they decline recording, take written notes only and fill the record straight after, while it is fresh.
   Write your chosen default into `how-to-run.md`. One method, decided, so you are not fumbling with settings while a busy person waits.

## The artefact
Writes two files in Markdown:
- `01-discovery/interview-script.md`: the opening lines, eight or more past-behaviour questions grouped by the four things above, and the closing questions.
- `01-discovery/how-to-run.md`: how to open, how to avoid pitching, your chosen recording and transcription method stated as one default, and how to close.

What good looks like: a nervous first-time interviewer could pick up the script cold and run a clean call from it. Not one question can be answered with a flattering yes. The recording method is a single named choice, not a menu.

## Done when
Three conditions, all checkable in the files:
1. `interview-script.md` holds eight or more questions, and every one asks about the past or their current behaviour, not a hypothetical.
2. `how-to-run.md` names one recording and transcription method as the default.
3. At least two questions point directly at the riskiest assumption from the idea brief.

## Log it
Append one line to CHANGELOG.md via the logbook helper, recording the artefact and the question count:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-write-script \
  --artefact 01-discovery/interview-script.md \
  --result "<N> non-leading questions, recorder chosen"
```

The logbook helper registers the script in state.json for you. Then record the second artefact and Day 1 progress via the journey-state helper:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --append-artefact '{"skill":"d1-write-script","path":"01-discovery/how-to-run.md","result":"recording method chosen"}'
```

Never edit `.spark/state.json` by hand. Always go through the helper so a skill running alongside this one cannot clobber the file.

## If it goes wrong
If the craft references or the templates will not load, do not stall. The whole method fits in one line: ask about the past, in specifics, without pitching. Write your eight questions against that, warn that the reference could not be read, and carry on.

If you cannot get past five questions, you are probably still thinking about your idea rather than their world. Put the idea away completely and ask yourself: what has this person actually done in the last month that touches the problem? Every real action is a question.

If a busy prospect will only give you fifteen minutes, do not cut the questions to fit. Cut to your best five, all aimed at the riskiest assumption, and note the trim in DECISIONS.md with a one-line reason.
