---
name: Book The Sale
description: Takes your warmest named prospect and gets a confirmed Friday meeting in the calendar. Use on Day 4 after the GTM plan, before Thursday's checkpoint closes.
when_to_use: Day 4 go-to-market, straight after gtm-plan. The gating number on Thursday's close: no confirmed Friday slot, Day 4 is not done.
---

# Book The Sale

**What this does.** Turns the single warmest prospect in your GTM plan into a confirmed Friday meeting: the right person, a specific time, and a reply that says yes.
**Why it matters.** Everything this week points at one thing, a real conversation with a real buyer on Friday. Nothing else in the plan actually books it. Regulated buyers in finance, trust and law rarely take a same-day meeting, so if you ask on Friday morning you have already lost. You ask on Thursday, for Friday, with a time already on the table.
**You are ready for this when.** `04-gtm/gtm-plan.md` exists and names at least one prospect.

## Before you start
Read `04-gtm/gtm-plan.md` and pick the ONE warmest prospect. Warmest means: a named human, a real channel to reach them (email, LinkedIn, phone, a mutual introduction), and a reason they would care this week. Not a company. A person.

Read `.spark/brand/brand.json` for your name and one-line proposition if it exists.

Guardrail: this skill drafts the message and gets it right. It does not send anything or book anything on anyone's behalf until you have read it and said go. Human sign-off before the message leaves your hands. That is a hard rule.

## Steps
1. Name the person. One line: who they are, where they work, and the single sentence of pain your idea removes for them. If you cannot write that sentence, they are not your warmest prospect. Pick again.
2. Choose the channel they actually reply on. A trust officer replies to email, not a LinkedIn DM. A tradesperson replies to a text. Match the channel to the person, not to your comfort.
3. Offer two specific Friday times, not "are you free Friday?". Give them a 20-minute slot and a fallback, for example "Friday 15 July, 10:00 or 14:00, 20 minutes, video or your office". A choice of two converts far better than an open question. One decision, not a diary negotiation.
4. Draft the ask with the helper: run `python3 ${CLAUDE_SKILL_DIR}/scripts/draft-ask.py` and answer the prompts. It writes a tight message using the structure in `${CLAUDE_SKILL_DIR}/references/ask-templates.md`: one line of context, the reason it helps them, the two times, a one-line no-pressure exit. Keep it under 120 words. Regulated buyers distrust a wall of text.
5. Read the draft out loud. Cut anything that sounds like a pitch. You are asking for 20 minutes to learn, not to sell. Sign off, then send it yourself through your own email or messaging.
6. When they reply, lock it. Confirm the time in writing and, if you use Google Calendar, create the hold so it is real and it reminds both of you. The helper prints the exact confirmation line.
7. If they go quiet by Thursday afternoon, send one short nudge and move to your second-warmest prospect in parallel. Two live asks beat one perfect one.

## The artefact
Writes `04-gtm/friday-meeting.md` in Markdown: the prospect (name, role, firm), the channel, the two times offered, the message you sent, the reply, and the confirmed slot (date, time, format, calendar link if any). The helper scaffolds it; you fill the reply and confirmation once they land.

Good looks like: a named person, a specific Friday time both parties have agreed in writing, and a calendar entry that exists.

## Done when
The warmest prospect has a confirmed Friday slot (specific date and time, agreed in writing) recorded in `04-gtm/friday-meeting.md`, before Day 4 closes. One confirmed meeting. That is the number Thursday's checkpoint prints.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py` (date, `d4-book-sale`, `04-gtm/friday-meeting.md`, result "1 Friday meeting confirmed"). Update `.spark/state.json` through `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: set days.4 outcome to the confirmed slot and mark progress.

## If it goes wrong
No reply from the first prospect by Thursday close: fall back to the second-warmest name and send the same ask. Still nothing by end of day: book a "warm practice" meeting with the friendliest contact who fits your segment, so Friday still happens and you learn something real. A booked practice conversation beats an empty Friday. Log which fallback you used and why in DECISIONS.md.
