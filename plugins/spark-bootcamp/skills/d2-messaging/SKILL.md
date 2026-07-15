---
name: Write Your Messaging
description: Turn your proposition into words: a one-liner under 12 words, three proof-backed messages, and a 60-word pitch. Day 2, after the proposition.
when_to_use: Day 2, straight after d2-proposition, before the landing page and any outreach.
---

# Write Your Messaging

**What this does.** Turns your proposition into the exact words you use everywhere: one line, three proof-backed messages, and a 30-second pitch.
**Why it matters.** People buy the sentence they can repeat to someone else, so if you cannot say what you do in under 12 words, word of mouth dies in the room.
**You are ready for this when.** `02-market/proposition.md` exists.

## Before you start
Read `02-market/proposition.md` (segment, pain, promise, numeric outcome) and `01-discovery/` notes if they exist, because the strongest messages steal the customer's own words. Match `.spark/brand/brand.json` tone if present. Do not invent proof: every claim traces to a real number or quote, or is flagged as an assumption.

## Steps
1. Draft the one-liner: "[We help] [segment] [do the outcome] [without the pain]." Under 12 words, no jargon. Write five, keep one.
2. Write three key messages: the three things you most want a prospect to believe. Each is a claim plus proof (a number, named result, demo, or interview quote). No proof, no message.
3. Rank them. Lead with "why should I care?", not "how does it work?".
4. Write the 60-word pitch: hook, what you do, who for, proof, ask. Aim 55 to 65 words. Read it aloud; if you stumble, cut a clause.
5. Branch by path (below) to sharpen the proof.
6. Pressure-test: read the one-liner to someone outside the business. If they cannot repeat it back, it is too clever. Rewrite.

## For software
Proof is the working slice: "cuts reconciliation from 3 hours to 8 minutes", not "streamlines workflows". No slice yet? Use interview pain as demand and flag the number as a target.

## For hardware
Proof is the prototype and early demand: "14 firms on the waitlist" beats "strong interest". No render yet? Describe the result and mark it a claim to prove on Day 3.

## For services
Proof is the sample deliverable and track record: "a board-ready risk pack in 5 working days, fixed fee". Make the deliverable and price shape concrete.

## The artefact
Writes `02-market/messaging.md`: the one-liner (with word count), three messages each as "Claim -> Proof", the ranked order with a one-line reason, and the 60-word pitch (with word count). Good: a stranger can tell you who you help, what changes, and why to believe you, in under a minute. Check counts: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-messaging.py 02-market/messaging.md`. Worked examples in `${CLAUDE_SKILL_DIR}/references/messaging-examples.md`.

## Done when
One-liner under 12 words, exactly three key messages each with a proof line, pitch between 55 and 65 words. The checker prints PASS on all three.

## Log it
Append to CHANGELOG.md via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, `d2-messaging`, `02-market/messaging.md`, and the numeric result (one-liner and pitch word counts). Set the day 2 outcome via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`.

## If it goes wrong
Cannot get under 12 words? You are saying two things: cut to one segment and one outcome. No proof? Downgrade the claim to "we believe" and flag it, or replace it. Pitch over 65 words usually has two audiences; pick one.
