---
name: Write Your Outreach
description: Drafts messages that book interviews by asking for help, not selling: three templates, a follow-up, personalised per contact, and recruits Day 4 testers.
when_to_use: Day 1, straight after the interview list, before you send anything.
---

# Write Your Outreach

**What this does.** Turns your contact list into ready-to-send messages: three templates (cold, warm, intro-request), one follow-up, and a personalised message per name.
**Why it matters.** People say yes to helping and no to being sold to, and the message decides whether the conversations happen at all.
**You are ready for this when.** `01-discovery/interview-list.csv` exists with 20+ rows.

## Before you start
Read `01-discovery/interview-list.csv` (name, role, relationship, hook) and `.spark/state.json` for your `founder` name and `idea`.

Guardrail: nothing goes out until you approve it. This skill drafts and stops. It never sends and never spends.

## Steps
1. Set a small ask: 20 to 25 minutes to learn from them. Not a pitch. Lead with why you picked them.
2. Recruit Day 4 testers in the same breath: add one line asking if they will react to what you build on Thursday. Track who says yes.
3. Fill the three templates from `${CLAUDE_SKILL_DIR}/references/outreach-templates.md`, in your voice:
   - **Cold**: one sentence on why them, then the ask.
   - **Warm**: skip the throat-clearing, get to the ask.
   - **Intro-request**: forwardable, so a mutual contact can paste it straight to the target.
4. Write the follow-up: one friendly line for non-repliers after three to four working days. No guilt.
5. Personalise every row: right template, real hook from the CSV, at least one personal clause each.
6. Choose one booking method: a scheduling link (Calendly free tier, £0) is default, it removes three emails per booking. Otherwise offer two concrete slots. Same method for everyone.
7. Assemble the pack, show the first three messages, wait for an explicit "send these".

## The artefact
Writes `01-discovery/outreach-pack.md` in Markdown: (1) booking method chosen; (2) templates (cold, warm, intro-request, follow-up); (3) one block per contact with name, channel, exact text, and a `Tester: yes/no/ask` flag; (4) tester tally. Good: every message names a real person and reason, the Day 4 line is in all of them, sendable today.

## Done when
Three templates plus one follow-up exist, 20+ personalised messages are ready, and one booking method is chosen and written into the pack.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: today's date, skill id `d1-write-outreach`, artefact `01-discovery/outreach-pack.md`, and the count of personalised messages ready. Record Day 1 progress via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. Log any booking-tool choice in DECISIONS.md.

## Optionally: create Gmail drafts
Only if the founder approves after reviewing the pack:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/create-gmail-drafts.py 01-discovery/outreach-pack.md
```

Writes drafts, never sends. If Gmail is not connected it prints the messages to copy by hand. Sending is always the founder's click.

## If it goes wrong
Thin replies after two days: change one thing, not everything. Shorten the ask, or move the tester line to its own follow-up. A quiet warm contact is data: send the intro-request to someone who can vouch for you.
