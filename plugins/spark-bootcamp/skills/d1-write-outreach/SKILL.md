---
name: Write Your Outreach
description: Writes messages that book interviews by asking for help, not selling. Three templates plus a follow-up, personalised per contact, and recruits Day 4 testers. Use on Day 1 after the contact list.
when_to_use: Day 1 discovery, straight after the interview list is built, before you send anything. This is the last Day 1 step before conversations start.
---

# Write Your Outreach

**What this does.** Turns your contact list into ready-to-send messages: three templates (cold, warm, intro-request), one follow-up, and a personalised message for every name on the list.
**Why it matters.** People say yes to helping and no to being sold to. The whole point of Day 1 is to book real conversations, and the message decides whether they happen. Get the ask right and your calendar fills. Get it wrong and you burn your best contacts on a pitch nobody wanted.
**You are ready for this when.** `01-discovery/interview-list.csv` exists and has at least 20 rows.

## Before you start
Read `01-discovery/interview-list.csv`. Note the columns you have per contact: name, their role, how you know them (cold, warm, or someone who can introduce you), and any personal hook. Read `.spark/state.json` for your `founder` name and `idea` so the messages sound like you, not a template.

Guardrail, read this twice: **nothing goes out until you approve it.** This skill drafts and stops. It never sends on its own, and it never spends money. If you want Gmail drafts created for you, that is offered at the end, and even then a draft is not a sent message. You press send.

## Steps
1. **Set the ask, and make it small.** You are asking for 20 to 25 minutes of their time to learn from them. You are not asking them to buy, to commit, or to "hop on a call about an exciting opportunity". Lead with respect for their time and a genuine reason you picked them.
2. **Recruit Day 4 testers in the same breath.** This is the bit most founders miss. At the end of every message, add one line asking if they would be willing to look at what you build on Thursday and give two minutes of reaction. That single sentence lines up your Day 4 test group four days early, when getting testers on the day itself is the thing that most often fails. Track who says yes.
3. **Fill the three templates.** Open `references/outreach-templates.md` at `${CLAUDE_SKILL_DIR}/references/outreach-templates.md`. Adapt each to your voice and idea:
   - **Cold**: someone you do not know. One sentence on why them specifically, then the small ask.
   - **Warm**: someone you know. Skip the throat-clearing, get to the ask.
   - **Intro-request**: sent to a mutual contact, asking them to forward you on. Make it forwardable: write it so they can paste it straight to the target.
4. **Write the follow-up.** One short, friendly nudge for people who do not reply in three to four working days. No guilt, no "just circling back". A single line: still keen to learn from them, happy to work around their diary.
5. **Personalise every row.** For each of the 20+ contacts, pick the right template and drop in the specific hook from the CSV: their firm, a shared connection, something they said or wrote. A message that could go to anyone gets a reply from no one. Aim for at least one genuinely personal clause per message.
6. **Choose one booking method.** Pick a single way to lock in a time so you are not playing email tennis. A scheduling link (Calendly free tier, £0) is the default recommendation because it removes three back-and-forth emails per booking. If you would rather not, offer two concrete slots in the message itself. Decide now and use the same method for everyone.
7. **Assemble the pack and stop for sign-off.** Write everything to the artefact below, then show the founder the first three personalised messages and wait for an explicit "send these" before anything leaves.

## The artefact
Writes `01-discovery/outreach-pack.md` in Markdown, with these sections in order:
1. **Booking method**: the one method chosen and the link or the two slots.
2. **Templates**: cold, warm, intro-request, and the follow-up, each ready to copy.
3. **Personalised messages**: one block per contact, headed with their name and channel (email, LinkedIn, WhatsApp), the exact text, and a `Tester: yes/no/ask` flag for the Day 4 line.
4. **Tester tally**: a running count of who has agreed to test on Thursday.

What good looks like: every message names a real person and a real reason, the Day 4 tester line is in all of them, and you could send the whole pack today without editing another word.

## Done when
Three templates plus one follow-up exist, 20 or more personalised messages are ready or sent, and one booking method is chosen and written into the pack. Count the message blocks: 20 is the floor.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: today's date, skill id `d1-write-outreach`, artefact path `01-discovery/outreach-pack.md`, and the numeric result (the count of personalised messages ready). Then update `.spark/state.json` via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: add an artefact entry and record Day 1 progress. If you chose a booking method or a scheduling tool, log the reason in DECISIONS.md.

## Optionally: create Gmail drafts
If, and only if, the founder approves after reviewing the pack, you can create Gmail drafts so they are ready to press send. Run:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/create-gmail-drafts.py 01-discovery/outreach-pack.md
```

This writes drafts, never sends. It degrades gracefully: if the Gmail tools are not connected it prints the messages to the terminal so you can copy them by hand, and it never crashes. Sending is always the founder's own click.

## If it goes wrong
If replies are thin after two days, do not rewrite everything. Change one thing: shorten the ask, or move the Day 4 tester line to its own follow-up. If a warm contact goes quiet, that is data, not failure. Send the intro-request to someone who can vouch for you and the reply rate jumps.
