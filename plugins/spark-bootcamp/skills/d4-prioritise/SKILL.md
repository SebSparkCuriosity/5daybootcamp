---
name: Prioritise The Feedback
description: Turns your product-test sessions into one ranked change list and one ranked list of buyers, so Friday builds the right three fixes and calls the warmest people first. Use on Day 4 after the tests.
when_to_use: Day 4 GTM, after you have run the product-test sessions and captured any inbound enquiries. Sits between synthesise-interviews (product-test mode) and Day 5 selling.
---

# Prioritise The Feedback

**What this does.** Reads every product-test session plus every landing-page enquiry, scores each requested change with RICE and MoSCoW, and ranks every tester by how likely they are to buy.
**Why it matters.** By Friday you can build three things, not thirty, and you can only phone a handful of people. This skill decides which three fixes and which people, using numbers instead of the loudest voice in the room. Get this wrong and you spend Day 5 polishing something nobody will pay for.
**You are ready for this when.** `04-gtm/tests/sessions/` holds at least one session file written by synthesise-interviews in product-test mode.

## Before you start
Read these exact paths:
- `04-gtm/tests/sessions/*.md`, one file per tester, each holding what they said, what they struggled with, and any change they asked for.
- The landing-site capture store, whichever exists: `04-gtm/site/captures.csv`, `04-gtm/captures.json`, or `.spark/deliverables/captures.csv`. These are the people who left an email or clicked pre-order on your live page. Treat them as the warmest hand-raisers you have.
- `.spark/state.json` for `business_type` and the founder's name.

If no capture store exists yet, carry on with the sessions alone and note it. Do not invent enquiries.

Guardrail: this skill only reads and scores. It sends nothing and spends nothing. Outreach to the ranked buyers happens on Day 5, after your explicit sign-off.

## Steps
1. Pull every distinct change request out of the session files. One request per line. Merge duplicates and keep a count of how many testers asked for each, because frequency feeds Reach.
2. Score each change with RICE. RICE gives you one comparable number per change so the list ranks itself.
   - **Reach**: how many of your testers (and captured enquirers) this change touches. Use the real count, not a guess.
   - **Impact**: how much it moves someone from interested to paying. Score 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal.
   - **Confidence**: how sure you are, as a percentage. 100% you watched it happen, 80% one clear account, 50% a hunch. Never round a hunch up.
   - **Effort**: person-days to build it. Half a day is 0.5. Be honest, Friday is short.
   - Score = (Reach x Impact x Confidence) / Effort. Higher wins.
3. Tag each change with MoSCoW so effort maps to the sale, not to neatness: Must (the sale dies without it), Should (strong pull, not fatal), Could (nice, later), Won't (parked this week, written down so it is not lost).
4. Flag the top 3. Sort by RICE, break ties by favouring Must over Should. Those three are your Friday build list. Everything else waits.
5. Rank the testers by buying intent into a scorecard. Score each person 0 to 3 on four signals, then total out of 12. Anyone from the capture store starts at the top of the warmth order because they already acted on your live page.
   - **Pain** (0 to 3): did they describe the problem as urgent and expensive, or mild?
   - **Budget** (0 to 3): can they spend, and did money come up without you forcing it?
   - **Timing** (0 to 3): do they need this now, this quarter, or someday?
   - **Pull** (0 to 3): did they ask what it costs, ask to be kept posted, or leave an email or pre-order?
6. Run the scorer to do the arithmetic and write both files:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --project .`
   It reads a small YAML block you fill in (the script prints the template on first run) and writes the synthesis and the scorecard. If PyYAML is missing it falls back to a plain key:value format and still runs. If Python itself is unavailable, the reference file has the formulas so you can do it by hand.

The full worked example, the MoSCoW definitions and the tie-break rules live in `${CLAUDE_SKILL_DIR}/references/scoring-guide.md`.

## The artefact
Two files:
- `04-gtm/feedback-synthesis.md` in Markdown: every change with its Reach, Impact, Confidence, Effort, RICE score and MoSCoW tag, sorted highest RICE first, with the top 3 flagged **BUILD FRIDAY**. A short opening paragraph names the single clearest signal across all sessions.
- `04-gtm/buying-signal-scorecard.csv`: one row per tester with the four signal scores, the total out of 12, a warmth band (Hot 9 to 12, Warm 5 to 8, Cool 0 to 4), a "from live page" flag, and the rank. Sorted hottest first.

What good looks like: someone who missed every session can read the two files and know exactly what to build on Friday and who to ring first, with a number behind each call.

## Done when
- Every change request has all four RICE inputs, a RICE score and a MoSCoW tag. No blanks.
- Exactly 3 changes carry the **BUILD FRIDAY** flag.
- Every tester appears in the scorecard with a total out of 12 and a rank, sorted hottest first.

## Log it
Append one line to CHANGELOG.md via the logbook helper, recording the artefact paths and the numeric result (changes scored, top 3 flagged, testers ranked):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-prioritise \
  --path 04-gtm/feedback-synthesis.md \
  --result "<N> changes scored, top 3 flagged, <M> testers ranked"
```
Then update state via the journey-state helper, setting the Day 4 outcome:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --set-day-outcome 4 "Feedback prioritised: 3 fixes chosen for Friday, <M> testers ranked by buying intent" \
  --add-artefact d4-prioritise 04-gtm/feedback-synthesis.md "<N> changes, <M> testers"
```
If a rationale drove a close call (a low-RICE change promoted to Must, or a tester bumped up the ranking), add a line to DECISIONS.md saying why.

## If it goes wrong
- **Only one or two sessions.** RICE still works, Confidence just drops. Score honestly on low Confidence and note that Friday's build list is provisional until more evidence lands.
- **No clear top 3 (a three-way tie).** Break it with MoSCoW first, then with Effort: ship the cheapest of the tied changes so Friday has slack.
- **No capture store and thin buying signals.** Rank on Pain and Timing alone, band everyone Cool or Warm, and treat Day 5 as a warm-up round rather than a close. Be honest about it in the synthesis.
