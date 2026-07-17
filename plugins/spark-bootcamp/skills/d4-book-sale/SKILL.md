---
name: Book The Sale
description: Turns your warmest named prospect into a confirmed Friday meeting. Day 4, after gtm-plan, before Thursday's checkpoint closes.
when_to_use: Day 4, straight after gtm-plan. No confirmed Friday slot means Day 4 is not done.
---

# Book The Sale

**What this does.** Turns the single warmest prospect in your GTM plan into a confirmed Friday meeting: right person, specific time, a reply that says yes.
**Why it matters.** The whole week points at one real conversation with a real buyer, and regulated buyers rarely take a same-day meeting, so you ask on Thursday for Friday with a time already on the table.
**You are ready for this when.** `04-gtm/gtm-plan.md` exists and names at least one prospect.

## Before you start
Read `04-gtm/gtm-plan.md` and pick the ONE warmest prospect: a named human, a real channel to reach them, and a reason they care this week. A person, not a company. Read `.spark/brand/brand.json` for your name and proposition if it exists.

Guardrail: this skill drafts and refines the message only. Nothing sends or books until you have read it and said go. Human sign-off before it leaves your hands. Hard rule.

## Steps
1. Choose the person with the founder: ask why THIS one, and listen for a real reason (budget, timing, pain), not alphabetical comfort. Then name them: who they are, where they work, the one sentence of pain you remove. Can't write it? Pick again together.
2. Choose the channel they actually reply on (email for a trust officer, text for a tradesperson). Match to the person, not your comfort.
3. Offer two specific 20-minute Friday times plus a fallback, never "are you free Friday?". Two choices convert far better than an open question.
4. Draft the ask: run `python3 ${CLAUDE_SKILL_DIR}/scripts/draft-ask.py` and answer the prompts. It uses `${CLAUDE_SKILL_DIR}/references/ask-templates.md`: one line of context, why it helps them, the two times, a no-pressure exit. Under 120 words.
5. Read it aloud, cut anything that sounds like a pitch (you want 20 minutes to learn, not to sell), then send it yourself.
6. When they reply, lock it: confirm the time in writing and, in Google Calendar, create the hold. The helper prints the confirmation line.
7. Quiet by Thursday afternoon: send one short nudge and start your second-warmest prospect in parallel.

## The artefact
Writes `04-gtm/friday-meeting.md`: prospect (name, role, firm), channel, two times offered, the message sent, the reply, the confirmed slot (date, time, format, calendar link). The helper scaffolds it; you fill the reply and confirmation.

## Done when
The warmest prospect has a confirmed Friday slot (specific date and time, agreed in writing) in `04-gtm/friday-meeting.md` before Day 4 closes. One confirmed meeting.

## Log it
Append one line via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py` (date, `d4-book-sale`, `04-gtm/friday-meeting.md`, result "1 Friday meeting confirmed"). Set days.4 outcome to the confirmed slot through `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --patch`.

## If it goes wrong
No reply from the first prospect by Thursday close: send the same ask to the second-warmest name. Still nothing: book a "warm practice" meeting with the friendliest contact in your segment, so Friday still happens. Log which fallback you used and why in DECISIONS.md.
