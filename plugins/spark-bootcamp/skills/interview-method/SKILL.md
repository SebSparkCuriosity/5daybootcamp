---
name: Interview Method
description: The shared craft behind every customer conversation this week: how to ask, what to listen for, and how to tell a real buying signal from a polite compliment. Internal knowledge base.
when_to_use: Internal only. Read automatically inside run-interview and synthesise-interviews on Day 1 (discovery) and Day 4 (product-test). Not run directly by the founder.
user-invocable: false
---

# Interview Method

**What this does.** Holds the three references that make a founder's customer conversations useful instead of flattering: how to ask about behaviour not opinions, how to frame the job the customer is hiring you for, and how to read willingness to pay.
**Why it matters.** Most first-time founders leave an interview delighted and none the wiser. They pitched, the other person was polite, and everyone agreed the idea was "really interesting". That is the failure mode. This skill is the craft that stops it. Ask about the past, not the future. Dig into what actually happened. Treat compliments as noise and money, time and referrals as signal. Get this right and ten conversations tell you the truth. Get it wrong and fifty tell you nothing.
**You are ready for this when.** Another skill has called you. This skill produces no artefact of its own and the founder never runs it directly.

## Before you start
This is not a skill the founder runs. It is the shared method that `run-interview` and `synthesise-interviews` load before they act, on Day 1 and again on Day 4. When one of those skills reaches the point of writing questions, coaching a live conversation, or reading a transcript for signal, it reads the relevant reference here first and applies it.

There is no branch by business type in the method itself. A software founder, a hardware founder and a services founder all ask about past behaviour and all read the same buying signals. What differs is the product they later build, not how they listen. So this skill stays path-neutral. The calling skill handles the path.

## The three references

Load whichever one the calling skill needs. All live under `${CLAUDE_SKILL_DIR}/references/`.

### 1. The Mom Test: `references/mom-test.md`
The core rule of interviewing: ask questions even your mum could not lie to you about. That means asking about specific things that already happened, never about a hypothetical future. "Would you buy this?" is worthless. "Walk me through the last time you dealt with this problem" is gold. This reference covers the three Mom Test rules, the questions that break them, the fixed versions, and how to steer away from pitching when you are itching to.

Read this before writing any interview question and before any live conversation.

### 2. Jobs to be done: `references/jtbd.md`
People do not buy products, they hire them to make progress in a situation. This reference frames the interview around the job the customer is trying to get done: the situation that triggers it, what they use today, and what "done well" looks like to them. It gives you the job-story format and a ready set of JTBD interview questions you can lift straight into a script.

Read this when shaping the arc of the conversation, so the questions ladder up to a job rather than wandering.

### 3. Willingness-to-pay signals: `references/wtp-signals.md`
The hardest read in any interview: does this person actually want it enough to pay, or are they just being nice? This reference separates polite compliments (noise) from commitment and advance (signal). Commitment is giving up something real: money, time, reputation, a firm next step. It gives you a signal-versus-noise table, the specific things to listen for, and how to end a conversation with a concrete ask that tests the signal.

Read this before synthesising interviews, so you score conversations on behaviour and commitment, not on warmth.

## The method in one paragraph
Ask about the past, in specifics, without pitching. Anchor every question to a real job the person is trying to get done. Then judge what you heard by what they did and what they are willing to give up, not by how much they liked you. A founder who does these three things learns more from eight honest conversations than from fifty happy ones.

## Done when
The calling skill has read the reference it needs and can quote the specific rule it is applying, for example "Mom Test rule 2: ask for specifics in the past, not generics about the future." This skill writes no artefact and updates no state; the skills that call it do that.

## Log it
Nothing to log here. This skill produces no artefact and touches no state. The skills that read it, `run-interview` and `synthesise-interviews`, own the CHANGELOG.md line and the `.spark/state.json` update for the work they produce.

## If it goes wrong
If a reference file is missing or will not load, do not stall the conversation. Fall back to the one-paragraph method above, which is the whole skill compressed: past behaviour, real job, commitment over compliments. Warn the founder that the detailed reference could not be read, carry on with the fallback, and flag it so the file can be restored.
