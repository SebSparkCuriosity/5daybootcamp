---
name: Build Your Interview List
description: Turns your target spec into 20+ named, reachable humans, each with a channel and a warmth rating, so you can book 8 to 12 real conversations. Use on Day 1 after defining interviewees.
when_to_use: Day 1 discovery, straight after d1-define-interviewees, before you write any outreach. This is the list you will actually message.
---

# Build Your Interview List

**What this does.** Turns your interview target spec into a list of 20 or more named, reachable people, each with a way to contact them and a warmth rating.
**Why it matters.** You need 20 names to land 8 to 12 conversations. Roughly half of anyone you approach will not reply or cannot make time, so a list of 10 leaves you short and a list of 20 gives you room. Naming real humans now is what turns a plan into a week of booked calls. Vague plans to "ask around" do not survive contact with a busy week.
**You are ready for this when.** `01-discovery/interview-target-spec.md` exists and names one segment, the role, the target number and three screening questions.

## Before you start
Read `01-discovery/interview-target-spec.md`. Everyone you add must clear the segment and the three screening questions from that file. If you cannot say yes to all three for a name, do not add it.

Jersey is small, and that cuts both ways. You are probably two introductions from almost anyone on the island, which is a gift. But the pool per niche is shallow, so you will run out of obvious names fast and need the tactics in `references/sourcing-tactics.md`. Read it before you start hunting.

Guardrail: this step gathers contacts, it does not send anything. Do not message a single person until the outreach step, and not before you have signed off the message. Names and business contact details are fine to collect. Keep the list on your own machine, do not publish it, and do not add notes about a person you would be uncomfortable showing them.

## Steps
1. Empty the easy buckets first. Open the sourcing tactics reference and work top to bottom: your own phone contacts, past colleagues and clients, LinkedIn first connections, then the Jersey-specific sources (industry bodies, member directories, event attendee lists, the parish and networking scenes). Warm names are worth five cold ones, so mine them before you touch a cold channel.
2. Add each person straight into the CSV as you find them. Do not batch it up in your head. Use the template in `references/interview-list-template.csv` and copy its header exactly.
3. For every row, fill four things at minimum: name, where they work or what they do, the single best channel to reach them (LinkedIn, warm intro via a named person, or email), and a warmth rating. If a field is a guess, mark it so.
4. Rate warmth honestly with three levels. Hot: you know them or have a direct mutual who will introduce you today. Warm: one clear introduction away, or you have met once. Cold: no connection, you would be arriving unannounced. Aim for at least 6 hot or warm names, because those book fastest and give you momentum in the first two days.
5. When you hit 20, keep going to 25 if the names come easily. Overshooting costs you ten minutes now and saves you a scramble on Day 2 when three people go quiet.
6. Sanity-check the list against the spec one last time. Cut anyone who does not clear the screening questions, even if they were easy to find. A padded list of the wrong people is worse than a short list of the right ones, because it tempts you to waste slots.

## The artefact
Writes `01-discovery/interview-list.csv` in CSV format, using the header from `references/interview-list-template.csv`:

`name,role_or_business,channel,contact_detail,warmth,source,notes`

Good looks like: 20 or more rows, every row has a name, a channel and a warmth rating, at least 6 rows rated hot or warm, and every row plausibly clears your three screening questions. Contact detail can be blank for a warm-intro row where the intro carries the contact, but the intro person must be named in the notes.

## Done when
The CSV holds 20 or more prospects, each row has a channel and a warmth rating, and at least 6 rows are rated hot or warm. Count the rows before you move on.

## Log it
Append one line to CHANGELOG.md via the logbook helper, with today's date, the skill id `d1-build-list`, the artefact path `01-discovery/interview-list.csv`, and the numeric result (the count of prospects listed):

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d1-build-list --path 01-discovery/interview-list.csv --result "23 prospects"`

Then update state via the journey-state helper so Day 1 progress reflects the finished list:

`python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --add-artefact d1-build-list:01-discovery/interview-list.csv:"23 prospects"`

## If it goes wrong
Cannot reach 20 that clear the screening questions? You have found a real signal, not a dead end. Either the segment is too narrow to serve, or your reach into it is thin. Do two things. First, widen the geography: Guernsey, the Isle of Man and the UK are all in scope, and a Jersey trust or fund niche often has a natural sister market next door. Second, before you widen the segment itself, go back to `d1-define-interviewees` and check whether an adjacent role feels the same pain, because a broader net that still passes the screening questions beats a lower bar. If you are stuck at, say, 12 solid names, run the 12 anyway rather than stall, and note the shortfall in DECISIONS.md so the market-map step knows the sample was small.
