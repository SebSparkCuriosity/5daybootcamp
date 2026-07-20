---
name: Build Your Invite List
description: Turns your target spec into 20+ named, reachable people, each with a channel and warmth rating, ready to invite to bootcamp Monday interviews.
when_to_use: Pre-work, straight after p0-interview-triage, before you write the invitations.
---

# Build Your Invite List

**What this does.** Turns your interview target spec into 20 or more named, reachable people, each with a contact channel and a warmth rating.
**Why it matters.** Roughly half of anyone you approach will not reply, so 20 names is what lands 8 to 12 booked interviews on bootcamp Monday.
**You are ready for this when.** `00-prework/interview-target-spec.md` exists and names one segment, the role, the target number and three screening questions.

## Before you start
Read `00-prework/interview-target-spec.md`. Everyone you add must clear the segment and its three screening questions. If you cannot say yes to all three, do not add the name. Read `references/sourcing-tactics.md` before hunting: the pool per niche is shallow.

This is the founder's network, so work it together: ask where they already know people before searching anywhere else. Guardrail: this step gathers contacts only. Send nothing until the invitations step. Business contact details are fine to collect; keep the list on your own machine and add no note you would not show the person.

## Steps
1. Empty the easy buckets first, working the sourcing tactics reference top to bottom: phone contacts, past colleagues and clients, LinkedIn first connections, then Jersey sources (industry bodies, member directories, event lists, parish and networking scenes). One warm name beats five cold.
2. Add each person into the CSV as you find them, using the header from `references/interview-list-template.csv` copied exactly.
3. Fill four fields minimum per row: name, role or business, best channel (email, WhatsApp, LinkedIn, or a warm intro via a named person), and warmth. Mark any guess.
4. Rate warmth in three levels. Hot: you know them or a direct mutual introduces you today. Warm: one introduction away, or met once. Cold: arriving unannounced. Aim for at least 6 hot or warm.
5. At 20, push to 25 if names come easily. Overshooting now saves a scramble the week before the bootcamp.
6. Sanity-check against the spec. Cut anyone who fails the screening questions, however easy they were to find.

## The artefact
Writes `00-prework/invite-list.csv`, header from `references/interview-list-template.csv`:
`name,role_or_business,channel,contact_detail,warmth,source,notes`
Good: 20 or more rows, each with a name, channel and warmth, at least 6 hot or warm, all clearing the screening questions. Contact detail may be blank on a warm-intro row if the intro person is named in notes.

## Done when
The CSV holds 20 or more prospects, each row has a channel and a warmth rating, and at least 6 rows are hot or warm. Count the rows.

## Log it
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill p0-invite-list --artefact 00-prework/invite-list.csv --result "23 prospects"`

## If it goes wrong
Cannot reach 20 that clear the screening questions? That is a signal: the segment is too narrow or your reach is thin. First widen geography (Guernsey, Isle of Man, UK are in scope). Then check with `p0-interview-triage` whether an adjacent role feels the same pain, before lowering the bar. Stuck at 12 solid names? Invite the 12 and note the shortfall in DECISIONS.md so the market-map step knows the sample was small.
