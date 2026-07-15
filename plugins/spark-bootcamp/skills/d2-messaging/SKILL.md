---
name: Write Your Messaging
description: Turn your proposition into the words the business uses everywhere: a one-liner under 12 words, three messages with proof, and a 60-word pitch. Use on Day 2 after the proposition.
when_to_use: Day 2 market work, straight after d2-proposition, before the landing page and any outreach. Whenever you need the sentence you say when someone asks "so what do you do?".
---

# Write Your Messaging

**What this does.** Turns your proposition into the exact words you use everywhere: one line, three proof-backed messages, and a pitch you can say in 30 seconds.
**Why it matters.** People do not buy the thing you built. They buy the sentence they can repeat to someone else. If you cannot say what you do in under 12 words, your prospect cannot say it for you, and word of mouth dies in the room. Nail the words now and the landing page, the emails and the sales call all write themselves.
**You are ready for this when.** `02-market/proposition.md` exists.

## Before you start
Read `02-market/proposition.md`: the segment, the pain, the promise and the numeric outcome you committed to. Read `01-discovery/` interview notes if they exist, because the strongest messages steal the customer's own words. If `.spark/brand/brand.json` exists, match its tone. Do not invent proof. Every claim you make must trace to a real number, a real interview quote, or be flagged as an assumption.

## Steps
1. Draft the one-liner. Format: "[We help] [segment] [do the outcome] [without the pain]." Keep it under 12 words. No jargon, no "leverage", no "solutions". A twelve-year-old should understand it. Write five, keep one.
2. Write the three key messages. These are the three things you most want a prospect to believe. Each one is a claim plus its proof. A message with no proof is a slogan, and slogans do not sell. Proof is a number, a named result, a demo, or a direct quote from an interview.
3. Rank the three. Lead with the one that answers "why should I care?", not "how does it work?". Care first, mechanics second.
4. Write the 60-word pitch. This is what you say when someone gives you 30 seconds: hook, what you do, who for, the proof, the ask. Aim for 55 to 65 words. Read it aloud. If you run out of breath or stumble, cut a clause.
5. Branch by path (below) to sharpen the proof so it fits how your business actually earns trust.
6. Pressure-test. Read the one-liner to one person who is not in your business. If they cannot repeat it back roughly right, it is too clever. Rewrite it.

## For software
Your proof is the working slice. Point at what the product visibly does: "cuts reconciliation from 3 hours to 8 minutes", not "streamlines workflows". If the slice is not built yet, use the interview pain as proof of demand and flag the performance number as a target.

## For hardware
Your proof is the prototype and early demand. Lead with the tangible outcome and the pre-order or waitlist count if you have one: "14 firms on the waitlist" beats "strong interest". If there is no render or mock yet, describe the demonstrable result and mark it a claim to prove on Day 3.

## For services
Your proof is the sample deliverable and your track record. Name the result and the turnaround: "a board-ready risk pack in 5 working days, fixed fee". Vague scope kills service sales, so the pitch must make the deliverable and the price shape concrete.

## The artefact
Writes `02-market/messaging.md` in Markdown, with four sections: the one-liner (with its word count in brackets), the three key messages (each as "Claim -> Proof"), the ranked order with a one-line reason, and the 60-word pitch (with its word count). Good looks like: a stranger reads it and can tell you who you help, what changes for them, and why they should believe you, in under a minute.

Run the checker to confirm the counts: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-messaging.py 02-market/messaging.md`. See `${CLAUDE_SKILL_DIR}/references/messaging-examples.md` for worked examples across the three paths.

## Done when
The one-liner is under 12 words, there are exactly three key messages and each has a proof line, and the pitch is between 55 and 65 words. The checker prints PASS on all three.

## Log it
Append one line to CHANGELOG.md via the logbook helper (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`): date, `d2-messaging`, `02-market/messaging.md`, and the numeric result (one-liner word count and pitch word count). Then update `.spark/state.json` via the journey-state helper (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`): set the day 2 outcome and append the artefact entry.

## If it goes wrong
Cannot get the one-liner under 12 words? You are trying to say two things. Cut to the one segment and one outcome that matter most this week; the rest goes on the page later. No proof for a message? Do not fake it. Either downgrade the claim to "we believe" and flag it as an assumption to test, or replace it with a message you can actually back. A pitch that will not sit under 65 words usually has two audiences in it. Pick one.
