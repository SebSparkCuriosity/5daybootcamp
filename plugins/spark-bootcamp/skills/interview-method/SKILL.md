---
name: Interview Method
description: The shared craft behind every customer conversation: how to ask, what to listen for, and how to tell a buying signal from a polite compliment. Internal.
when_to_use: Internal only. Read inside run-interview (Day 1) and synthesise-interviews (Day 4). Not run by the founder.
user-invocable: false
---

# Interview Method

**What this does.** Holds three references that make customer conversations useful instead of flattering.
**Why it matters.** Most first-time founders leave an interview delighted and none the wiser, because a polite chat feels like validation and it is not.
**You are ready for this when.** Another skill has called you. This skill produces no artefact and the founder never runs it.

## Before you start
Loaded by `run-interview` and `synthesise-interviews` before they write questions, coach a live conversation, or read a transcript. Path-neutral: software, hardware and services founders all ask about past behaviour and read the same signals. The calling skill handles the business path.

## The three references
Load whichever the calling skill needs, from `${CLAUDE_SKILL_DIR}/references/`.

1. **The Mom Test: `references/mom-test.md`.** Ask about specific things that already happened, never a hypothetical future. Read before writing any question and before any live conversation.
2. **Jobs to be done: `references/jtbd.md`.** Frame the conversation around the job the customer is hiring the product for. Read when shaping the arc so questions ladder up to a job.
3. **Willingness-to-pay signals: `references/wtp-signals.md`.** Separate polite compliments (noise) from commitment (money, time, reputation, a firm next step). Read before synthesising, so you score on behaviour not warmth.

## The method in one paragraph
Ask about the past, in specifics, without pitching. Anchor every question to a real job. Judge what you heard by what they did and what they will give up, not how much they liked you.

## Done when
The calling skill has read the reference it needs and can quote the rule it is applying. This skill writes no artefact and updates no state.

## Log it
Nothing to log. The calling skills own the CHANGELOG.md line and the `.spark/state.json` update.

## If it goes wrong
If a reference will not load, do not stall. Fall back to the one-paragraph method (past behaviour, real job, commitment over compliments), warn the founder the detailed reference could not be read, and flag it for restore.
