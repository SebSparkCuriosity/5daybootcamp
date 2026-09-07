---
name: Write Your Invitations
description: Drafts the messages (email, WhatsApp or LinkedIn) that book interviews for bootcamp Monday, weeks in advance. Personalised per contact, nothing sent without your yes.
when_to_use: Pre-work, straight after the invite list, 2 to 4 weeks before the bootcamp Monday.
---

# Write Your Invitations

**What this does.** Turns your invite list into ready-to-send invitations to a real interview slot on bootcamp Monday: templates per channel (email, WhatsApp, LinkedIn), a follow-up, and a personalised message per name.
**Why it matters.** Nobody is free tomorrow. Invitations sent 2 to 4 weeks ahead are what put 8 to 12 real conversations in the Monday diary, and people say yes to helping, not to being sold to.
**You are ready for this when.** `00-prework/invite-list.csv` exists with 20+ rows.

## Before you start
Read `00-prework/invite-list.csv` (name, role, channel, warmth, notes) and `.spark/state.json` for `founder`, `idea` and `prework.bootcamp_monday`. Every date in every template comes from that field, plus the Tuesday after it as overflow: never hardcode a date. If `prework.bootcamp_monday` is missing or already past, stop and send the founder back to `start`.

Guardrail: nothing goes out until the founder approves it. This skill drafts and stops. It never sends and never spends.

Already sent these by hand? Do not re-send: write up what actually went out (channel, wording, date) so the pack matches reality, then move straight to `p0-schedule` to log the replies.

## Steps
1. Set the ask with the founder: 20 to 25 minutes on the named Monday (or Tuesday morning), remote or in person, to learn from them. Not a pitch. Lead with why you picked them.
2. Choose one booking method together: a scheduling link (Calendly free tier, GBP 0) with ONLY the Monday afternoon and Tuesday morning windows open is the default; otherwise offer two concrete slots with times. Same method for everyone.
3. Fill the channel templates from `${CLAUDE_SKILL_DIR}/references/invitation-templates.md` in the founder's voice, not yours: draft, read aloud, adjust until it sounds like them.
   - **Email**: cold, warm and intro-request variants, with the date in the first three lines.
   - **WhatsApp**: two sentences and the link. For hot and warm contacts only.
   - **LinkedIn**: under 300 characters for a connection note, longer once connected.
4. Write the follow-up: one friendly line for non-repliers after 4 to 5 working days, and one final nudge a week after that. No guilt.
5. Personalise every row: right template, right channel from the CSV, at least one clause that names the real reason you picked them.
6. Keep one light PS recruiting Thursday testers: whether they would give what you build a two-minute look later in the week. Track who says yes.
7. Assemble the pack, show the first three messages, wait for an explicit "send these". Then the founder sends, hottest names first.

## The artefact
Writes `00-prework/invitation-pack.md` in Markdown: (1) the interview date(s) and booking method; (2) templates per channel plus follow-ups; (3) one block per contact with name, channel, exact text, and a `Tester: yes/no/ask` flag; (4) tester tally. Good: every message names a real person, a real reason and the real date, sendable today.

## Done when
Channel templates plus two follow-ups exist, 20+ personalised messages are ready, the interview date from state appears in every one, and one booking method is chosen and written into the pack.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: today's date, skill id `p0-invitations`, artefact `00-prework/invitation-pack.md`, and the count of personalised messages ready. Log the booking-tool choice in DECISIONS.md.

## Optionally: create Gmail drafts
Only if the founder approves after reviewing the pack:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/create-gmail-drafts.py 00-prework/invitation-pack.md
```

Writes drafts, never sends. If Gmail is not connected it prints the messages to copy by hand. Sending is always the founder's click.

## If it goes wrong
Thin replies after a week: change one thing, not everything. Shorten the ask, or switch a quiet email contact to WhatsApp or LinkedIn. A quiet warm contact is data: send the intro-request to someone who can vouch for you. Track every reply in `p0-schedule`; that skill owns the chase.
